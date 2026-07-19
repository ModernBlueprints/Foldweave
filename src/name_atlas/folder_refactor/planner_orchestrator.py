"""Durable bounded orchestration for the AI-first folder planner."""

from __future__ import annotations

import uuid
from collections.abc import Callable

from name_atlas.folder_refactor.compiler import PlanCompilationError, compile_plan
from name_atlas.folder_refactor.contracts import FolderInventory
from name_atlas.folder_refactor.inventory import (
    FolderScan,
    FolderScanError,
    scan_folder,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.planner_contracts import (
    MAX_EVIDENCE_CALLS,
    MAX_PLAN_SUBMISSIONS,
    MAX_RESPONSE_TURNS,
    MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES,
    FolderPlannerProgress,
    FolderPlannerTurnInput,
    InspectMarkdownLinksCall,
    ListInventoryPageCall,
    PlannerCompilerFailure,
    PlannerEvidenceReservation,
    PlannerObservableTurn,
    ProviderBlockedResponse,
    ProviderToolResponse,
    ReadTextExcerptCall,
    RequestClarificationCall,
    SubmitPlanCall,
    evidence_reservation_payload,
    observable_turn_payload,
    planner_history_item,
)
from name_atlas.folder_refactor.planner_evidence import (
    EvidenceService,
    PlannerEvidenceError,
    append_evidence_execution,
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.planner_provider import (
    PlannerProvider,
    PlannerProviderError,
)
from name_atlas.folder_refactor.request_policy import classify_unsupported_request
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

CheckpointWriter = Callable[[FolderPlannerProgress], None]
EvidenceCall = ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall


class PlannerOrchestrationError(RuntimeError):
    """The supplied planner state does not belong to this orchestration."""


def create_planner_progress(
    inventory: FolderInventory,
    request: str,
    *,
    job_id: str,
    provider_kind: str,
) -> FolderPlannerProgress:
    """Create one strict empty planner state bound to source and request."""

    return FolderPlannerProgress(
        job_id=job_id,
        provider_kind=provider_kind,
        status="planning",
        response_turns=0,
        pending_response_turn=None,
        pending_response_input_bytes=None,
        pending_response_input_fingerprint=None,
        pending_response_input_payload=None,
        processing_response_turn=None,
        processing_tool_call_index=None,
        pending_evidence_call=None,
        evidence_calls=0,
        evidence_calls_observed=0,
        outbound_evidence_bytes=0,
        plan_submissions=0,
        evidence_ledger=create_initial_evidence_ledger(inventory, request),
        turns=(),
        compiler_failures=(),
        clarification_question=None,
        clarification_answer=None,
        accepted_plan=None,
        blocker_code=None,
    )


class PlannerOrchestrator:
    """Own every counter, transition, and mechanical acceptance decision."""

    def __init__(
        self,
        *,
        job_id: str,
        scan: FolderScan,
        request: str,
        provider: PlannerProvider,
        evidence_service: EvidenceService,
        reference_graph: FolderReferenceGraph,
        checkpoint: CheckpointWriter | None = None,
    ) -> None:
        try:
            parsed_job_id = uuid.UUID(hex=job_id)
        except ValueError as exc:
            raise PlannerOrchestrationError(
                "Planner job ID must be a lowercase UUID4 hex value."
            ) from exc
        if parsed_job_id.version != 4 or parsed_job_id.hex != job_id:
            raise PlannerOrchestrationError(
                "Planner job ID must be a lowercase UUID4 hex value."
            )
        if not request.strip():
            raise PlannerOrchestrationError("Planner request cannot be blank.")
        self._job_id = job_id
        self._scan = scan
        self._request = request
        self._provider = provider
        self._evidence_service = evidence_service
        if reference_graph.source_commitment != scan.inventory.source_commitment:
            raise PlannerOrchestrationError(
                "Planner reference graph targets a different source."
            )
        self._reference_graph = reference_graph
        self._checkpoint = checkpoint or (lambda _progress: None)
        self._request_blocker = classify_unsupported_request(
            request,
            scan.inventory,
        )

    def initial_progress(self) -> FolderPlannerProgress:
        """Create the only empty progress state valid for this session."""

        return create_planner_progress(
            self._scan.inventory,
            self._request,
            job_id=self._job_id,
            provider_kind=self._provider.provider_kind,
        )

    async def run(
        self,
        progress: FolderPlannerProgress,
    ) -> FolderPlannerProgress:
        """Continue automatically until accepted, clarified, or blocked."""

        self._require_bound_progress(progress)
        if progress.status != "planning":
            return progress
        if self._request_blocker is not None:
            return self._persist(self._blocked(progress, self._request_blocker.code))
        if progress.pending_response_turn is not None:
            progress = self._resolve_incomplete_turn(progress)
            return self._persist(progress)
        if progress.pending_evidence_call is not None:
            return self._persist(self._blocked(progress, "evidence_call_incomplete"))

        while progress.status == "planning":
            if not self._source_is_unchanged():
                return self._persist(self._blocked(progress, "source_changed"))
            if progress.processing_response_turn is not None:
                progress = await self._process_persisted_response(progress)
                continue
            if progress.response_turns >= MAX_RESPONSE_TURNS:
                return self._persist(
                    self._blocked(progress, "response_turn_limit_exceeded")
                )

            turn_input = self._turn_input(progress)
            turn_input_payload = turn_input.model_dump(mode="json")
            outbound_bytes = len(canonical_json_bytes(turn_input_payload))
            input_fingerprint = canonical_sha256(turn_input_payload)
            if (
                progress.outbound_evidence_bytes + outbound_bytes
                > MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES
            ):
                return self._persist(
                    self._blocked(progress, "outbound_evidence_limit_exceeded")
                )

            turn_number = progress.response_turns + 1
            progress = self._replace(
                progress,
                response_turns=turn_number,
                pending_response_turn=turn_number,
                pending_response_input_bytes=outbound_bytes,
                pending_response_input_fingerprint=input_fingerprint,
                pending_response_input_payload=turn_input_payload,
                outbound_evidence_bytes=(
                    progress.outbound_evidence_bytes + outbound_bytes
                ),
            )
            progress = self._persist(progress)
            try:
                response = await self._provider.exchange(turn_input)
            except PlannerProviderError as exc:
                progress = self._complete_failed_turn(
                    progress,
                    code=_provider_failure_code(exc),
                )
                return self._persist(progress)

            if not isinstance(response, ProviderToolResponse | ProviderBlockedResponse):
                progress = self._complete_failed_turn(
                    progress,
                    code="provider_response_invalid",
                )
                return self._persist(progress)

            progress = self._record_response(progress, response)
            progress = self._persist(progress)
        return progress

    async def answer_clarification(
        self,
        progress: FolderPlannerProgress,
        answer: str,
    ) -> FolderPlannerProgress:
        """Persist the sole answer, then continue within remaining budgets."""

        self._require_bound_progress(progress)
        if progress.status != "awaiting_clarification":
            raise PlannerOrchestrationError(
                "Planner is not waiting for a clarification answer."
            )
        normalized = answer.strip()
        if not normalized or len(normalized) > 4_000 or "\x00" in normalized:
            raise PlannerOrchestrationError(
                "Clarification answer must be nonblank bounded plain text."
            )
        progress = self._replace(
            progress,
            status="planning",
            clarification_answer=answer,
        )
        progress = self._persist(progress)
        return await self.run(progress)

    async def _process_persisted_response(
        self,
        progress: FolderPlannerProgress,
    ) -> FolderPlannerProgress:
        """Finish the durably recorded response before another provider turn."""

        if (
            progress.processing_response_turn is None
            or progress.processing_tool_call_index is None
        ):
            raise PlannerOrchestrationError("No provider response awaits processing.")
        turn = progress.turns[-1]
        call = turn.tool_calls[progress.processing_tool_call_index]
        if isinstance(call, SubmitPlanCall):
            return await self._process_plan(progress, call)
        if isinstance(call, RequestClarificationCall):
            return self._process_clarification(progress, call)
        return await self._process_evidence_calls(progress)

    async def _process_evidence_calls(
        self,
        progress: FolderPlannerProgress,
    ) -> FolderPlannerProgress:
        if (
            progress.processing_response_turn is None
            or progress.processing_tool_call_index is None
        ):
            raise PlannerOrchestrationError("Evidence processing lacks a cursor.")
        turn = progress.turns[-1]
        while progress.processing_tool_call_index is not None:
            call_index = progress.processing_tool_call_index
            call = turn.tool_calls[call_index]
            if not isinstance(
                call,
                ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
            ):
                return self._persist(
                    self._blocked(progress, "invalid_evidence_tool_response")
                )
            if progress.evidence_calls >= MAX_EVIDENCE_CALLS:
                return self._persist(
                    self._blocked(
                        self._replace(
                            progress,
                            evidence_calls_observed=(
                                progress.evidence_calls_observed + 1
                            ),
                        ),
                        "evidence_call_limit_exceeded",
                    )
                )
            reservation_payload = {
                "call": call.model_dump(mode="json"),
                "evidence_call_number": progress.evidence_calls + 1,
                "response_turn": progress.processing_response_turn,
                "tool_call_index": call_index,
            }
            reservation = PlannerEvidenceReservation(
                response_turn=progress.processing_response_turn,
                tool_call_index=call_index,
                evidence_call_number=progress.evidence_calls + 1,
                call=call,
                reservation_fingerprint=canonical_sha256(reservation_payload),
            )
            if reservation.reservation_fingerprint != canonical_sha256(
                evidence_reservation_payload(reservation)
            ):
                raise AssertionError("Evidence reservation hash domain diverged.")
            progress = self._replace(
                progress,
                evidence_calls=progress.evidence_calls + 1,
                evidence_calls_observed=progress.evidence_calls_observed + 1,
                pending_evidence_call=reservation,
            )
            progress = self._persist(progress)
            execution = self._evidence_service.execute(call)
            try:
                ledger = append_evidence_execution(
                    progress.evidence_ledger,
                    response_turn=progress.response_turns,
                    call=call,
                    execution=execution,
                )
            except PlannerEvidenceError as exc:
                return self._persist(self._blocked(progress, exc.code))
            next_index = call_index + 1
            cursor_updates: dict[str, object] = {
                "processing_response_turn": progress.processing_response_turn,
                "processing_tool_call_index": next_index,
            }
            if next_index >= len(turn.tool_calls):
                cursor_updates = {
                    "processing_response_turn": None,
                    "processing_tool_call_index": None,
                }
            progress = self._replace(
                progress,
                pending_evidence_call=None,
                evidence_ledger=ledger,
                **cursor_updates,
            )
            progress = self._persist(progress)
            if execution.error_code == "source_changed":
                return self._persist(self._blocked(progress, "source_changed"))
        return progress

    async def _process_plan(
        self,
        progress: FolderPlannerProgress,
        call: SubmitPlanCall,
    ) -> FolderPlannerProgress:
        if not self._source_is_unchanged():
            return self._persist(self._blocked(progress, "source_changed"))
        submission_number = progress.plan_submissions + 1
        try:
            accepted = compile_plan(
                self._scan.inventory,
                self._request,
                call.plan,
                known_evidence_ids=self._known_evidence_ids(progress),
                evidence_fingerprint=progress.evidence_ledger.evidence_fingerprint,
                reference_graph=self._reference_graph,
            )
        except PlanCompilationError as exc:
            failure = PlannerCompilerFailure(
                submission_number=submission_number,
                code=exc.code,
                detail=f"Mechanical plan check failed: {exc.code}",
            )
            progress = self._replace(
                progress,
                plan_submissions=submission_number,
                compiler_failures=(*progress.compiler_failures, failure),
                processing_response_turn=None,
                processing_tool_call_index=None,
            )
            progress = self._persist(progress)
            if submission_number >= MAX_PLAN_SUBMISSIONS:
                return self._persist(
                    self._blocked(progress, "plan_repair_limit_exceeded")
                )
            return progress
        progress = self._replace(
            progress,
            status="accepted",
            plan_submissions=submission_number,
            accepted_plan=accepted,
            processing_response_turn=None,
            processing_tool_call_index=None,
        )
        return self._persist(progress)

    def _process_clarification(
        self,
        progress: FolderPlannerProgress,
        call: RequestClarificationCall,
    ) -> FolderPlannerProgress:
        if progress.clarification_question is not None or progress.plan_submissions > 0:
            return self._persist(
                self._blocked(progress, "second_clarification_not_allowed")
            )
        unknown = set(call.evidence_ids) - self._known_clarification_evidence_ids(
            progress
        )
        if unknown:
            return self._persist(
                self._blocked(progress, "unknown_clarification_evidence")
            )
        question = call.question.strip()
        if not question:
            return self._persist(
                self._blocked(progress, "invalid_clarification_question")
            )
        progress = self._replace(
            progress,
            status="awaiting_clarification",
            clarification_question=question,
            processing_response_turn=None,
            processing_tool_call_index=None,
        )
        return self._persist(progress)

    def _turn_input(self, progress: FolderPlannerProgress) -> FolderPlannerTurnInput:
        return FolderPlannerTurnInput(
            job_id=self._job_id,
            response_turn=progress.response_turns + 1,
            provider_kind=self._provider.provider_kind,
            request=self._request,
            request_fingerprint=request_fingerprint(self._request),
            source_commitment=self._scan.inventory.source_commitment,
            evidence_ledger=progress.evidence_ledger,
            prior_turns=tuple(planner_history_item(turn) for turn in progress.turns),
            compiler_failures=progress.compiler_failures,
            clarification_question=progress.clarification_question,
            clarification_answer=progress.clarification_answer,
        )

    def _record_response(
        self,
        progress: FolderPlannerProgress,
        response: ProviderToolResponse | ProviderBlockedResponse,
    ) -> FolderPlannerProgress:
        if progress.pending_response_turn is None:
            raise PlannerOrchestrationError("Provider response has no reserved turn.")
        if (
            progress.pending_response_input_bytes is None
            or progress.pending_response_input_fingerprint is None
            or progress.pending_response_input_payload is None
        ):
            raise PlannerOrchestrationError("Provider turn lacks its input commitment.")
        if response.provider_kind != self._provider.provider_kind:
            return self._complete_failed_turn(
                progress,
                code="provider_origin_mismatch",
            )
        payload = {
            "blocker_code": (
                response.blocker_code
                if isinstance(response, ProviderBlockedResponse)
                else None
            ),
            "input_bytes": progress.pending_response_input_bytes,
            "input_fingerprint": progress.pending_response_input_fingerprint,
            "input_payload": progress.pending_response_input_payload,
            "observable_output_items": list(response.observable_output_items),
            "provider_kind": response.provider_kind,
            "response_turn": progress.pending_response_turn,
            "returned_model": response.returned_model,
            "tool_calls": (
                []
                if isinstance(response, ProviderBlockedResponse)
                else [item.model_dump(mode="json") for item in response.tool_calls]
            ),
        }
        turn = PlannerObservableTurn(
            response_turn=progress.pending_response_turn,
            provider_kind=response.provider_kind,
            returned_model=response.returned_model,
            observable_output_items=response.observable_output_items,
            tool_calls=(
                ()
                if isinstance(response, ProviderBlockedResponse)
                else response.tool_calls
            ),
            blocker_code=(
                response.blocker_code
                if isinstance(response, ProviderBlockedResponse)
                else None
            ),
            input_bytes=progress.pending_response_input_bytes,
            input_fingerprint=progress.pending_response_input_fingerprint,
            input_payload=progress.pending_response_input_payload,
            response_fingerprint=canonical_sha256(payload),
        )
        if turn.response_fingerprint != canonical_sha256(observable_turn_payload(turn)):
            raise AssertionError("Observable turn hash domain diverged.")
        updates: dict[str, object] = {
            "pending_response_turn": None,
            "pending_response_input_bytes": None,
            "pending_response_input_fingerprint": None,
            "pending_response_input_payload": None,
            "turns": (*progress.turns, turn),
        }
        if isinstance(response, ProviderBlockedResponse):
            updates.update(
                {
                    "status": "blocked",
                    "blocker_code": response.blocker_code,
                    "processing_response_turn": None,
                    "processing_tool_call_index": None,
                }
            )
        else:
            updates.update(
                {
                    "processing_response_turn": turn.response_turn,
                    "processing_tool_call_index": 0,
                }
            )
        return self._replace(progress, **updates)

    def _complete_failed_turn(
        self,
        progress: FolderPlannerProgress,
        *,
        code: str,
    ) -> FolderPlannerProgress:
        turn_number = progress.pending_response_turn
        if (
            turn_number is None
            or progress.pending_response_input_bytes is None
            or progress.pending_response_input_fingerprint is None
            or progress.pending_response_input_payload is None
        ):
            raise PlannerOrchestrationError("Provider failure has no reserved turn.")
        payload = {
            "blocker_code": code,
            "input_bytes": progress.pending_response_input_bytes,
            "input_fingerprint": progress.pending_response_input_fingerprint,
            "input_payload": progress.pending_response_input_payload,
            "observable_output_items": [],
            "provider_kind": self._provider.provider_kind,
            "response_turn": turn_number,
            "returned_model": None,
            "tool_calls": [],
        }
        turn = PlannerObservableTurn(
            response_turn=turn_number,
            provider_kind=self._provider.provider_kind,
            returned_model=None,
            observable_output_items=(),
            tool_calls=(),
            blocker_code=code,
            input_bytes=progress.pending_response_input_bytes,
            input_fingerprint=progress.pending_response_input_fingerprint,
            input_payload=progress.pending_response_input_payload,
            response_fingerprint=canonical_sha256(payload),
        )
        return self._replace(
            progress,
            status="blocked",
            pending_response_turn=None,
            pending_response_input_bytes=None,
            pending_response_input_fingerprint=None,
            pending_response_input_payload=None,
            turns=(*progress.turns, turn),
            blocker_code=code,
        )

    def _resolve_incomplete_turn(
        self,
        progress: FolderPlannerProgress,
    ) -> FolderPlannerProgress:
        return self._complete_failed_turn(
            progress,
            code="provider_turn_incomplete",
        )

    def _blocked(
        self,
        progress: FolderPlannerProgress,
        code: str,
    ) -> FolderPlannerProgress:
        updates: dict[str, object] = {
            "status": "blocked",
            "blocker_code": code,
        }
        if progress.pending_evidence_call is None:
            updates.update(
                {
                    "processing_response_turn": None,
                    "processing_tool_call_index": None,
                }
            )
        return self._replace(progress, **updates)

    def _known_evidence_ids(
        self,
        progress: FolderPlannerProgress,
    ) -> frozenset[str]:
        return frozenset(
            {"initial_inventory"}
            | {record.fingerprint for record in progress.evidence_ledger.records}
        )

    def _known_clarification_evidence_ids(
        self,
        progress: FolderPlannerProgress,
    ) -> frozenset[str]:
        """Accept exact evidence digests and unambiguous observed tool-call IDs.

        The Responses API naturally refers back to a tool result by its call ID.
        Those IDs remain bound to the complete evidence record in the observable
        transcript. Plan entries continue to require content-addressed evidence
        fingerprints; this narrow alias applies only to the one user question.
        """

        records = progress.evidence_ledger.records
        call_ids = tuple(record.call_id for record in records)
        unique_call_ids = {
            call_id for call_id in call_ids if call_ids.count(call_id) == 1
        }
        return self._known_evidence_ids(progress) | frozenset(unique_call_ids)

    def _require_bound_progress(self, progress: FolderPlannerProgress) -> None:
        if (
            progress.evidence_ledger.source_commitment
            != self._scan.inventory.source_commitment
            or progress.evidence_ledger.request_fingerprint
            != request_fingerprint(self._request)
            or progress.job_id != self._job_id
            or progress.provider_kind != self._provider.provider_kind
        ):
            raise PlannerOrchestrationError(
                "Planner progress targets a different source or request."
            )

    def _source_is_unchanged(self) -> bool:
        try:
            current = scan_folder(self._scan.source_root)
        except (FolderScanError, OSError):
            return False
        return (
            current.inventory.source_commitment
            == self._scan.inventory.source_commitment
            and current.local_file_identities == self._scan.local_file_identities
            and current.local_directory_identities
            == self._scan.local_directory_identities
        )

    def _persist(self, progress: FolderPlannerProgress) -> FolderPlannerProgress:
        self._checkpoint(progress)
        return progress

    @staticmethod
    def _replace(
        progress: FolderPlannerProgress,
        **updates: object,
    ) -> FolderPlannerProgress:
        payload = progress.model_dump(mode="python")
        payload.update(updates)
        return FolderPlannerProgress.model_validate(payload, strict=True)


def _provider_failure_code(exc: PlannerProviderError) -> str:
    name = type(exc).__name__
    mapping = {
        "PlannerProviderResponseError": "provider_response_error",
        "PlannerProviderTimeoutError": "provider_timeout",
        "PlannerProviderTransportError": "provider_transport_error",
        "ScriptedProviderExhaustedError": "provider_script_exhausted",
    }
    return mapping.get(name, "provider_request_failed")
