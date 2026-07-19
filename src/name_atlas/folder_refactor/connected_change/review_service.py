"""Foldweave review orchestration over the single Connected Change engine."""

from __future__ import annotations

import os
import uuid
from collections.abc import Callable, Mapping
from datetime import datetime
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from name_atlas.folder_refactor.compiler import PlanCompilationError, compile_plan
from name_atlas.folder_refactor.connected_change.accepted_plan import (
    convert_planner_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    ConnectedChangeError,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file,
)
from name_atlas.folder_refactor.connected_change.evidence import (
    build_planner_origin_evidence,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
    FolderRefactorJobV2,
    GptPlannedJobAuthorityV2,
    GptPlannerCheckpointV2,
    build_new_capsule_job_v2,
    build_new_gpt_job_v2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    FolderJobV3RevisionError,
    FolderJobVerifiedArtifactsV3,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    FolderRefactorJobV3Writer,
    FolderRevisionFailureV1,
    FolderRevisionRejectionRecordV1,
    GptPlannedJobAuthorityV3,
    build_execution_authorization,
    build_keep_previous_action,
    build_revision_instruction,
    build_revision_provider_failure,
    build_revision_rejection_record,
    evolve_job_v3,
    expected_final_result_path_v3,
    expected_pending_result_path_v3,
)
from name_atlas.folder_refactor.connected_change.preview import (
    FolderPlanPreviewV1,
    build_folder_plan_preview,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_PATH,
)
from name_atlas.folder_refactor.connected_change.reconstruction import (
    restore_connected_result,
)
from name_atlas.folder_refactor.connected_change.service import (
    PreparedConnectedChange,
    PreparedConnectedChangeApplication,
    PreparedConnectedChangeOrigin,
    execute_prepared_connected_change,
    prepare_connected_change_application,
    prepare_connected_change_origin,
    rehydrate_prepared_connected_change_origin,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerification,
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderEvidenceLedgerV2,
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionProvider,
    FolderRevisionTurnRecordV1,
    append_failed_revision_evidence,
    append_successful_revision_evidence,
    build_execution_origin_v2,
    build_foldweave_f0b_contract_freeze,
    build_initial_composite_evidence,
    build_revision_turn_record,
)
from name_atlas.folder_refactor.inventory import FolderScan
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerProgress,
    FolderPlannerTurnInput,
    FolderProviderResponse,
)
from name_atlas.folder_refactor.planner_evidence import LocalFolderEvidenceService
from name_atlas.folder_refactor.planner_orchestrator import (
    PlannerOrchestrator,
    create_planner_progress,
)
from name_atlas.folder_refactor.planner_provider import PlannerProvider
from name_atlas.folder_refactor.portable_artifacts import (
    canonical_portable_json_bytes,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderPlannerUsage,
    FolderRestoreReport,
)
from name_atlas.folder_refactor.serialization import (
    canonical_sha256,
    request_fingerprint,
)
from name_atlas.folder_refactor.transaction import (
    FolderTransactionError,
    FolderTransactionPaths,
    FolderTransactionProgress,
    scan_folder_with_references,
)

oslo_tz = ZoneInfo("Europe/Oslo")
ReviewChannel = Literal[
    "native_app",
    "browser",
    "chatgpt_hosted",
    "codex_mcp",
    "local_mcp",
    "cli",
]
PlannerModelTransport = Literal[
    "responses_api",
    "recorded_replay",
    "deterministic_development",
]
PlannerProviderKind = Literal["deterministic", "live", "recorded_replay"]
FOLDWEAVE_F0B_CONTRACT_FREEZE = build_foldweave_f0b_contract_freeze()
FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT = (
    FOLDWEAVE_F0B_CONTRACT_FREEZE.contract_freeze_fingerprint
)


class _InterruptedTurnRecoveryProvider:
    """Represent a reserved turn that must fail closed without provider access."""

    def __init__(
        self,
        *,
        provider_kind: PlannerProviderKind,
        usage: tuple[FolderPlannerUsage, ...],
    ) -> None:
        self._provider_kind = provider_kind
        self._usage = usage

    @property
    def provider_kind(self) -> PlannerProviderKind:
        return self._provider_kind

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return self._usage

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        del turn_input
        raise AssertionError("Interrupted provider recovery cannot make another call.")


class FoldweaveReviewServiceError(RuntimeError):
    """One stable orchestration failure at the review authority boundary."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class FoldweaveReviewService:
    """Prepare, review, authorize, execute, and verify through one v3 job."""

    def prepare_deterministic_origin_review(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        request: str,
        result_folder_name: str,
        target_by_original_path: Mapping[str, str],
        idempotency_key: str,
    ) -> FolderRefactorJobV3:
        """Create or resume one provider-free origin job through review only."""

        job_id = uuid.uuid4().hex
        seed = build_new_gpt_job_v2(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            user_request=request,
            idempotency_key=idempotency_key,
            job_id=job_id,
        )
        initial = _v3_from_seed(seed, lifecycle=FolderJobLifecycleV3.PLANNING)
        job = self._save_or_reuse(initial)
        if job.lifecycle is not FolderJobLifecycleV3.PLANNING:
            return job
        try:
            prepared = prepare_connected_change_origin(
                job_id=job.job_id,
                source_root=job.source_root,
                request=job.user_request,
                result_folder_name=result_folder_name,
                target_by_original_path=target_by_original_path,
            )
            return self._persist_origin_review(job.job_path, prepared)
        except (ConnectedChangeError, FolderTransactionError, ValueError) as exc:
            return self._block_if_current(
                job.job_path,
                expected=job,
                code=_error_code(exc, "origin_review_preparation_blocked"),
                message=str(exc),
            )

    async def prepare_planned_origin_review(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        request: str,
        idempotency_key: str,
        provider: PlannerProvider,
    ) -> FolderRefactorJobV3:
        """Run bounded initial planning and stop at one immutable preview."""

        scan, reference_graph = scan_folder_with_references(source_root)
        job_id = uuid.uuid4().hex
        initial_progress = create_planner_progress(
            scan.inventory,
            request,
            job_id=job_id,
            provider_kind=provider.provider_kind,
        )
        seed = build_new_gpt_job_v2(
            source_root=scan.source_root,
            output_parent=output_parent,
            job_path=job_path,
            user_request=request,
            idempotency_key=idempotency_key,
            scan=scan,
            job_id=job_id,
            planner_progress=initial_progress,
        )
        initial = evolve_job_v3(
            _v3_from_seed(seed, lifecycle=FolderJobLifecycleV3.PLANNING),
            authority=GptPlannedJobAuthorityV3(
                authority_schema_version="folder-gpt-planned-job-authority.v3",
                planner_checkpoint=GptPlannerCheckpointV2.from_progress(
                    initial_progress
                ),
            ),
        )
        job = self._save_or_reuse(initial)
        if job.lifecycle is not FolderJobLifecycleV3.PLANNING:
            return job
        return await self._continue_initial_planner(
            job,
            provider=provider,
            scan=scan,
            reference_graph=reference_graph,
        )

    async def resume_planned_origin_review(
        self,
        job_path: Path,
        *,
        provider: PlannerProvider,
    ) -> FolderRefactorJobV3:
        """Resume only the exact persisted initial-planning checkpoint."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
        if job.lifecycle is not FolderJobLifecycleV3.PLANNING:
            return job
        scan, reference_graph = scan_folder_with_references(job.source_root)
        if scan.inventory != job.source_inventory:
            raise FoldweaveReviewServiceError(
                "planner_source_mismatch",
                "The current source differs from the persisted planning inventory.",
            )
        return await self._continue_initial_planner(
            job,
            provider=provider,
            scan=scan,
            reference_graph=reference_graph,
        )

    async def recover_interrupted_planned_origin_review(
        self,
        job_path: Path,
    ) -> FolderRefactorJobV3:
        """Resolve a reserved provider turn without credentials or another call."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
        if job.lifecycle is not FolderJobLifecycleV3.PLANNING:
            return job
        authority = _require_v3_planning_authority(job)
        progress = authority.planner_checkpoint.progress
        if progress is None or progress.pending_response_turn is None:
            return job
        scan, reference_graph = scan_folder_with_references(job.source_root)
        if scan.inventory != job.source_inventory:
            raise FoldweaveReviewServiceError(
                "planner_source_mismatch",
                "The current source differs from the persisted planning inventory.",
            )
        provider = _InterruptedTurnRecoveryProvider(
            provider_kind=progress.provider_kind,
            usage=authority.planner_checkpoint.usage,
        )
        return await self._continue_initial_planner(
            job,
            provider=provider,
            scan=scan,
            reference_graph=reference_graph,
        )

    async def answer_planned_origin_clarification(
        self,
        job_path: Path,
        *,
        continuation_token: str,
        answer: str,
        provider: PlannerProvider,
    ) -> FolderRefactorJobV3:
        """Persist the sole answer and continue toward an immutable preview."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
        if job.job_id != continuation_token:
            raise FoldweaveReviewServiceError(
                "clarification_token_mismatch",
                "The clarification answer targets another durable job.",
            )
        if job.lifecycle is not FolderJobLifecycleV3.AWAITING_CLARIFICATION:
            raise FoldweaveReviewServiceError(
                "clarification_not_active",
                "The durable job is not waiting for a clarification answer.",
            )
        scan, reference_graph = scan_folder_with_references(job.source_root)
        if scan.inventory != job.source_inventory:
            raise FoldweaveReviewServiceError(
                "planner_source_mismatch",
                "The current source differs from the persisted planning inventory.",
            )
        return await self._continue_initial_planner(
            job,
            provider=provider,
            scan=scan,
            reference_graph=reference_graph,
            clarification_answer=answer,
        )

    async def revise(
        self,
        job_path: Path,
        *,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        instruction: str,
        idempotency_key: str,
        provider: FolderPlanRevisionProvider | None = None,
        provider_factory: Callable[[], FolderPlanRevisionProvider] | None = None,
    ) -> FolderRefactorJobV3:
        """Bind one sparse revision, compile it, and retain a complete preview."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            repeated = _revision_instruction_for_request(
                candidate_fingerprint=candidate_fingerprint,
                preview_fingerprint=preview_fingerprint,
                instruction=instruction,
                idempotency_key=idempotency_key,
            )
            if job.revision_instruction is not None and (
                job.revision_instruction.idempotency_key_sha256
                == repeated.idempotency_key_sha256
            ):
                if job.revision_instruction != repeated:
                    raise FolderJobV3IdempotencyConflict(
                        "Revision retry key is bound to another exact request."
                    )
                return job
            if (provider is None) == (provider_factory is None):
                raise FoldweaveReviewServiceError(
                    "revision_provider_configuration_invalid",
                    "A new revision requires exactly one provider authority.",
                )
            if job.lifecycle not in {
                FolderJobLifecycleV3.REVIEWING,
                FolderJobLifecycleV3.REVISION_FAILED,
            }:
                raise FoldweaveReviewServiceError(
                    "job_not_revisable",
                    f"Job cannot be revised from {job.lifecycle.value}.",
                )
            self._require_exact_review_request(
                job,
                expected_revision=expected_revision,
                preview_fingerprint=preview_fingerprint,
                candidate_fingerprint=candidate_fingerprint,
                output_parent=job.output_parent,
                result_folder_name=_require_candidate(job).result_folder_name,
            )
            authority = _require_v3_planning_authority(job)
            ledger = _require_composite_ledger(authority)
            if job.revision_attempt_count >= 2 or job.proposal_revision >= 2:
                raise FoldweaveReviewServiceError(
                    "revision_limit_reached",
                    "This job has reached the two-revision limit.",
                )
            if provider is None:
                assert provider_factory is not None
                provider = provider_factory()
            _require_revision_provider_matches(ledger, provider)
            preserved_rejections = _revision_rejections_with_current_failure(job)
            turn_input = FolderPlannerRevisionTurnInputV1(
                job_id=job.job_id,
                expected_job_revision=job.revision,
                proposal_revision=job.proposal_revision,
                response_turn=ledger.response_turn_count + 1,
                provider_kind=provider.provider_kind,
                request=job.user_request,
                request_fingerprint=request_fingerprint(job.user_request),
                source_commitment=job.source_inventory.source_commitment,
                revision_instruction=instruction,
                revision_instruction_fingerprint=(repeated.instruction_fingerprint),
                base_candidate=_require_candidate(job),
                base_candidate_fingerprint=candidate_fingerprint,
                base_preview_fingerprint=preview_fingerprint,
                evidence_fingerprint=ledger.evidence_fingerprint,
                prior_transcript_fingerprint=ledger.transcript_fingerprint,
                turn_contract_freeze_fingerprint=(
                    FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT
                ),
                imported_change_file_fingerprint=(
                    job.preview.imported_change_file_fingerprint
                    if job.preview is not None
                    else None
                ),
                match_report_fingerprint=(
                    job.preview.match_report_fingerprint
                    if job.preview is not None
                    else None
                ),
                immediate_parent_candidate_fingerprint=(
                    job.immediate_parent_candidate_fingerprint
                ),
            )
            revising_authority = authority.model_copy(
                update={"pending_revision_turn": turn_input}
            )
            revising = evolve_job_v3(
                job,
                revision=job.revision + 1,
                revision_attempt_count=job.revision_attempt_count + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.REVISING,
                authority=revising_authority,
                revision_instruction=repeated,
                revision_failure=None,
                revision_rejections=preserved_rejections,
            )
            revising = writer.save(revising, expected_current=job)
        try:
            response = await provider.exchange(turn_input)
            usage = _revision_turn_usage(provider, turn_input.response_turn)
            turn = build_revision_turn_record(
                turn_input=turn_input,
                response=response,
                usage=usage,
            )
        except Exception as exc:
            return self._persist_revision_provider_failure(
                job_path,
                expected=revising,
                code=_error_code(exc, "revision_provider_failed"),
                detail=str(exc),
            )
        return self._persist_revision_response(
            job_path,
            expected=revising,
            turn=turn,
        )

    def keep_previous_proposal(
        self,
        job_path: Path,
        *,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        idempotency_key: str,
    ) -> FolderRefactorJobV3:
        """Return a failed revision to a fresh review-bound preview."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            repeated = build_keep_previous_action(
                base_job_revision=expected_revision,
                candidate_fingerprint=candidate_fingerprint,
                preview_fingerprint=preview_fingerprint,
                idempotency_key=idempotency_key,
            )
            matching_key = tuple(
                action
                for action in job.keep_previous_actions
                if action.idempotency_key_sha256 == repeated.idempotency_key_sha256
            )
            if matching_key:
                if len(matching_key) != 1 or matching_key[0] != repeated:
                    raise FolderJobV3IdempotencyConflict(
                        "Keep-proposal retry key is bound to another exact request."
                    )
                return job
            if job.lifecycle is not FolderJobLifecycleV3.REVISION_FAILED:
                raise FoldweaveReviewServiceError(
                    "revision_failure_unavailable",
                    "The job has no failed revision to dismiss.",
                )
            self._require_exact_review_request(
                job,
                expected_revision=expected_revision,
                preview_fingerprint=preview_fingerprint,
                candidate_fingerprint=candidate_fingerprint,
                output_parent=job.output_parent,
                result_folder_name=_require_candidate(job).result_folder_name,
            )
            preview = _rebuild_preview(job, expected_job_revision=job.revision + 1)
            preserved_rejections = _revision_rejections_with_current_failure(job)
            successor = evolve_job_v3(
                job,
                revision=job.revision + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.REVIEWING,
                preview=preview,
                revision_failure=None,
                revision_rejections=preserved_rejections,
                keep_previous_actions=(*job.keep_previous_actions, repeated),
            )
            return writer.save(successor, expected_current=job)

    def prepare_application_review(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        idempotency_key: str,
    ) -> FolderRefactorJobV3:
        """Create or resume one model-free receiver job through review only."""

        job_id = uuid.uuid4().hex
        seed = build_new_capsule_job_v2(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            change_file_path=change_file_path,
            idempotency_key=idempotency_key,
            job_id=job_id,
        )
        initial = _v3_from_seed(seed, lifecycle=FolderJobLifecycleV3.MATCHING)
        job = self._save_or_reuse(initial)
        if job.lifecycle is not FolderJobLifecycleV3.MATCHING:
            return job
        try:
            prepared = prepare_connected_change_application(
                change_file_path=change_file_path,
                source_root=job.source_root,
            )
            return self._persist_application_review(job.job_path, prepared)
        except (ConnectedChangeError, FolderTransactionError, ValueError) as exc:
            return self._block_if_current(
                job.job_path,
                expected=job,
                code=_error_code(exc, "receiver_review_preparation_blocked"),
                message=str(exc),
            )

    def status(self, job_path: Path) -> FolderRefactorJobV3:
        """Read one durable v3 job without mutation or provider activity."""

        return FolderRefactorJobV3Store(job_path).inspect()

    def get_preview(self, job_path: Path) -> FolderPlanPreviewV1:
        """Return the one complete renderer DTO persisted for this job."""

        job = self.status(job_path)
        if job.preview is None:
            raise FoldweaveReviewServiceError(
                "preview_unavailable",
                f"Job is not reviewable: {job.lifecycle.value}.",
            )
        return job.preview

    def resume_authorized_execution(
        self,
        job_path: Path,
        *,
        progress_callback: FolderTransactionProgress | None = None,
    ) -> FolderRefactorJobV3:
        """Resume only an already-persisted exact execution authorization."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if job.lifecycle is not FolderJobLifecycleV3.EXECUTING:
                return job
            return self._execute_locked(
                writer,
                job,
                progress_callback=progress_callback,
            )

    def recover_interrupted_revision(self, job_path: Path) -> FolderRefactorJobV3:
        """Fail one uncertain provider turn closed while preserving its preview."""

        current = FolderRefactorJobV3Store(job_path).inspect()
        if current.lifecycle is not FolderJobLifecycleV3.REVISING:
            return current
        return self._persist_revision_provider_failure(
            job_path,
            expected=current,
            code="revision_provider_interrupted",
            detail=(
                "The application closed before the revision provider response "
                "was durably recorded. No provider retry was made; the prior "
                "valid proposal remains available."
            ),
        )

    def accept(
        self,
        job_path: Path,
        *,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        output_parent: Path,
        result_folder_name: str,
        idempotency_key: str,
        channel: ReviewChannel,
        progress_callback: FolderTransactionProgress | None = None,
    ) -> FolderRefactorJobV3:
        """Persist exact authorization, then create and verify one separate copy."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if job.lifecycle is FolderJobLifecycleV3.STALE:
                return job
            if job.lifecycle is FolderJobLifecycleV3.BLOCKED:
                return job
            if job.lifecycle is FolderJobLifecycleV3.VERIFIED:
                self._require_exact_authorization_retry(
                    job,
                    expected_revision=expected_revision,
                    preview_fingerprint=preview_fingerprint,
                    candidate_fingerprint=candidate_fingerprint,
                    output_parent=output_parent,
                    result_folder_name=result_folder_name,
                    idempotency_key=idempotency_key,
                    channel=channel,
                )
                return job
            if job.lifecycle not in {
                FolderJobLifecycleV3.REVIEWING,
                FolderJobLifecycleV3.EXECUTING,
            }:
                raise FoldweaveReviewServiceError(
                    "job_not_reviewable",
                    f"Job cannot be accepted from {job.lifecycle.value}.",
                )
            if job.lifecycle is FolderJobLifecycleV3.EXECUTING:
                self._require_exact_authorization_retry(
                    job,
                    expected_revision=expected_revision,
                    preview_fingerprint=preview_fingerprint,
                    candidate_fingerprint=candidate_fingerprint,
                    output_parent=output_parent,
                    result_folder_name=result_folder_name,
                    idempotency_key=idempotency_key,
                    channel=channel,
                )
                executing = job
            else:
                self._require_exact_review_request(
                    job,
                    expected_revision=expected_revision,
                    preview_fingerprint=preview_fingerprint,
                    candidate_fingerprint=candidate_fingerprint,
                    output_parent=output_parent,
                    result_folder_name=result_folder_name,
                )
                pending = expected_pending_result_path_v3(job)
                final = expected_final_result_path_v3(job)
                _require_absent_result_path(pending, label="Pending result")
                _require_absent_result_path(final, label="Final result")
                authorization = build_execution_authorization(
                    job=job,
                    expected_job_revision=expected_revision,
                    preview_fingerprint=preview_fingerprint,
                    candidate_fingerprint=candidate_fingerprint,
                    output_parent=output_parent,
                    result_folder_name=result_folder_name,
                    idempotency_key=idempotency_key,
                    channel=channel,
                )
                executing = evolve_job_v3(
                    job,
                    revision=job.revision + 1,
                    updated_at=_now(),
                    lifecycle=FolderJobLifecycleV3.EXECUTING,
                    execution_authorization=authorization,
                    pending_result_path=pending,
                    final_result_path=final,
                    revision_failure=None,
                )
                executing = writer.save(executing, expected_current=job)
                if executing.lifecycle is FolderJobLifecycleV3.STALE:
                    return executing
            return self._execute_locked(
                writer,
                executing,
                progress_callback=progress_callback,
            )

    def verify_result(self, job_path: Path) -> ConnectedReceiptVerification:
        """Run the existing independent source-free verifier."""

        job = self._require_verified_job(job_path)
        assert job.final_result_path is not None
        verification = verify_connected_result(job.final_result_path)
        self._require_bound_verification(job, verification)
        return verification

    def get_change_file(self, job_path: Path) -> tuple[Path, str, str]:
        """Return one verified local Change File and its receipt identity."""

        job = self._require_verified_job(job_path)
        assert job.final_result_path is not None
        verification = self.verify_result(job_path)
        path = job.final_result_path / CONNECTED_CHANGE_PATH
        payload = path.read_bytes()
        change_file = parse_connected_change_file(payload)
        if canonical_portable_json_bytes(change_file) != payload:
            raise FoldweaveReviewServiceError(
                "change_file_changed",
                "Verified Change File no longer has canonical bytes.",
            )
        assert verification.receipt_fingerprint is not None
        return (
            path,
            change_file.change_file_fingerprint,
            change_file.originating_receipt.receipt_fingerprint,
        )

    def recreate_original(
        self,
        job_path: Path,
        destination: Path,
    ) -> FolderRestoreReport:
        """Recreate the source selected when this exact transaction began."""

        job = self._require_verified_job(job_path)
        assert job.final_result_path is not None
        source_root = job.source_root if job.source_root.is_dir() else None
        return restore_connected_result(
            job.final_result_path,
            destination,
            source_root=source_root,
        )

    async def _continue_initial_planner(
        self,
        job: FolderRefactorJobV3,
        *,
        provider: PlannerProvider,
        scan: FolderScan,
        reference_graph: FolderReferenceGraph,
        clarification_answer: str | None = None,
    ) -> FolderRefactorJobV3:
        """Continue one exact planner checkpoint without reconstructing authority."""

        authority = _require_v3_planning_authority(job)
        progress = authority.planner_checkpoint.progress
        if progress is None or progress.provider_kind != provider.provider_kind:
            raise FoldweaveReviewServiceError(
                "planner_progress_mismatch",
                "Durable planner progress differs from the selected provider.",
            )
        if tuple(provider.usage) != authority.planner_checkpoint.usage:
            raise FoldweaveReviewServiceError(
                "planner_usage_prefix_mismatch",
                "The provider usage prefix differs from durable planning evidence.",
            )
        model_transport = _model_transport_for_provider(provider.provider_kind)
        orchestrator = PlannerOrchestrator(
            job_id=job.job_id,
            scan=scan,
            request=job.user_request,
            provider=provider,
            evidence_service=LocalFolderEvidenceService(
                scan,
                reference_graph=reference_graph,
            ),
            reference_graph=reference_graph,
            checkpoint=lambda checkpoint: self._persist_planner_progress(
                job.job_path,
                reference_graph=reference_graph,
                progress=checkpoint,
                usage=provider.usage,
                model_transport=model_transport,
            ),
        )
        if clarification_answer is None:
            await orchestrator.run(progress)
        else:
            await orchestrator.answer_clarification(progress, clarification_answer)
        return self.status(job.job_path)

    def _persist_planner_progress(
        self,
        job_path: Path,
        *,
        reference_graph: FolderReferenceGraph,
        progress: FolderPlannerProgress,
        usage: tuple[FolderPlannerUsage, ...],
        model_transport: PlannerModelTransport,
    ) -> FolderRefactorJobV3:
        """Persist one exact initial-planner checkpoint into the v3 job."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.rehydrate()
            if current.lifecycle.terminal:
                return current
            current_authority = _require_v3_planning_authority(current)
            accepted_plan = None
            evidence_ledger = None
            execution_origin = None
            accepted_plan_fingerprint = None
            preview = None
            if progress.status == "accepted":
                if progress.accepted_plan is None:
                    raise FoldweaveReviewServiceError(
                        "accepted_planner_plan_missing",
                        "Accepted planner progress lacks its complete plan.",
                    )
                accepted_plan = convert_planner_accepted_plan(
                    inventory=current.source_inventory,
                    request=current.user_request,
                    plan=progress.accepted_plan,
                    evidence_schema_version="folder-evidence-ledger.v2",
                )
                accepted_plan_fingerprint = canonical_sha256(accepted_plan)
                _legacy_origin, initial_ledger = build_planner_origin_evidence(
                    progress=progress,
                    accepted_plan=accepted_plan,
                    usage=usage,
                )
                evidence_ledger = build_initial_composite_evidence(
                    initial_ledger=initial_ledger,
                    accepted_plan=accepted_plan,
                    contract_freeze_fingerprint=(FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT),
                    model_transport=model_transport,
                )
                execution_origin = build_execution_origin_v2(evidence_ledger)
                preview = build_folder_plan_preview(
                    job_id=current.job_id,
                    expected_job_revision=current.revision + 1,
                    proposal_revision=0,
                    proposal_basis="fresh_gpt_plan",
                    inventory=current.source_inventory,
                    reference_graph=reference_graph,
                    accepted_plan=accepted_plan,
                )
            checkpoint = GptPlannerCheckpointV2.from_progress(
                progress,
                accepted_plan_fingerprint=accepted_plan_fingerprint,
                usage=usage,
            )
            authority = GptPlannedJobAuthorityV3(
                authority_schema_version=(current_authority.authority_schema_version),
                planner_checkpoint=checkpoint,
                evidence_ledger=evidence_ledger,
                execution_origin=execution_origin,
            )
            lifecycle = {
                "planning": FolderJobLifecycleV3.PLANNING,
                "awaiting_clarification": (FolderJobLifecycleV3.AWAITING_CLARIFICATION),
                "accepted": FolderJobLifecycleV3.REVIEWING,
                "blocked": FolderJobLifecycleV3.BLOCKED,
            }[progress.status]
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                clarification_count=(
                    1
                    if progress.clarification_question is not None
                    else current.clarification_count
                ),
                updated_at=_now(),
                lifecycle=lifecycle,
                authority=authority,
                candidate_plan=accepted_plan,
                reference_graph=(
                    reference_graph if accepted_plan is not None else None
                ),
                preview=preview,
                blocker_code=checkpoint.blocker_code,
                blocker_message=checkpoint.blocker_message,
            )
            return writer.save(successor, expected_current=current)

    def _persist_revision_provider_failure(
        self,
        job_path: Path,
        *,
        expected: FolderRefactorJobV3,
        code: str,
        detail: str,
    ) -> FolderRefactorJobV3:
        """Preserve the prior preview when a provider returns no usable response."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.rehydrate()
            if current != expected or current.lifecycle.terminal:
                return current
            authority = _require_v3_planning_authority(current)
            pending = authority.pending_revision_turn
            instruction = current.revision_instruction
            if pending is None or instruction is None or current.preview is None:
                raise FoldweaveReviewServiceError(
                    "revision_authority_missing",
                    "Failed revision lacks its prior preview or reserved turn.",
                )
            safe_detail = detail.strip()[:2_000] or (
                "The planning provider did not return a usable revision."
            )
            provider_failure = build_revision_provider_failure(
                attempt_index=current.revision_attempt_count,
                turn_input=pending,
                code=code,
                detail=safe_detail,
            )
            failed_authority = authority.model_copy(
                update={"pending_revision_turn": None}
            )
            preview = _build_preview(
                current,
                accepted_plan=_require_candidate(current),
                expected_job_revision=current.revision + 1,
                proposal_revision=current.proposal_revision,
            )
            failure = FolderRevisionFailureV1(
                code=code,
                detail=safe_detail,
                attempted_instruction_fingerprint=(instruction.instruction_fingerprint),
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.REVISION_FAILED,
                authority=failed_authority,
                preview=preview,
                revision_failure=failure,
                revision_provider_failures=(
                    *current.revision_provider_failures,
                    provider_failure,
                ),
            )
            return writer.save(successor, expected_current=current)

    def _persist_revision_response(
        self,
        job_path: Path,
        *,
        expected: FolderRefactorJobV3,
        turn: FolderRevisionTurnRecordV1,
    ) -> FolderRefactorJobV3:
        """Compile one observed sparse response and persist its exact outcome."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.rehydrate()
            if current != expected or current.lifecycle.terminal:
                return current
            authority = _require_v3_planning_authority(current)
            ledger = _require_composite_ledger(authority)
            if current.preview is None or current.revision_instruction is None:
                raise FoldweaveReviewServiceError(
                    "revision_authority_missing",
                    "Revising job lacks its prior preview or instruction.",
                )
            try:
                accepted_plan = _compile_sparse_revision(
                    current,
                    ledger=ledger,
                    turn=turn,
                )
            except (PlanCompilationError, ValueError) as exc:
                failed_ledger = append_failed_revision_evidence(
                    ledger=ledger,
                    turn=turn,
                    base_preview_fingerprint=(current.preview.preview_fingerprint),
                    revision_instruction_fingerprint=(
                        current.revision_instruction.instruction_fingerprint
                    ),
                )
                failed_authority = authority.model_copy(
                    update={
                        "evidence_ledger": failed_ledger,
                        "execution_origin": build_execution_origin_v2(failed_ledger),
                        "pending_revision_turn": None,
                    }
                )
                preview = _build_preview(
                    current,
                    accepted_plan=_require_candidate(current),
                    expected_job_revision=current.revision + 1,
                    proposal_revision=current.proposal_revision,
                )
                failure = FolderRevisionFailureV1(
                    code=_error_code(exc, "revision_mechanical_check_failed"),
                    detail=str(exc)[:2_000],
                    attempted_instruction_fingerprint=(
                        current.revision_instruction.instruction_fingerprint
                    ),
                )
                rejection = build_revision_rejection_record(
                    attempt_index=current.revision_attempt_count,
                    ledger=failed_ledger,
                    failure=failure,
                )
                successor = evolve_job_v3(
                    current,
                    revision=current.revision + 1,
                    updated_at=_now(),
                    lifecycle=FolderJobLifecycleV3.REVISION_FAILED,
                    authority=failed_authority,
                    preview=preview,
                    revision_failure=failure,
                    revision_rejections=(
                        *current.revision_rejections,
                        rejection,
                    ),
                )
                return writer.save(successor, expected_current=current)
            revised_ledger = append_successful_revision_evidence(
                ledger=ledger,
                turn=turn,
                accepted_plan=accepted_plan,
                base_preview_fingerprint=current.preview.preview_fingerprint,
                revision_instruction_fingerprint=(
                    current.revision_instruction.instruction_fingerprint
                ),
            )
            revised_authority = authority.model_copy(
                update={
                    "evidence_ledger": revised_ledger,
                    "execution_origin": build_execution_origin_v2(revised_ledger),
                    "pending_revision_turn": None,
                }
            )
            next_proposal_revision = current.proposal_revision + 1
            preview = _build_preview(
                current,
                accepted_plan=accepted_plan,
                expected_job_revision=current.revision + 1,
                proposal_revision=next_proposal_revision,
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                proposal_revision=next_proposal_revision,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.REVIEWING,
                authority=revised_authority,
                candidate_plan=accepted_plan,
                preview=preview,
                revision_failure=None,
            )
            return writer.save(successor, expected_current=current)

    def _save_or_reuse(self, candidate: FolderRefactorJobV3) -> FolderRefactorJobV3:
        store = FolderRefactorJobV3Store(candidate.job_path)
        with store.writer() as writer:
            if os.path.lexists(candidate.job_path):
                existing = writer.load()
                if existing.idempotency != candidate.idempotency:
                    raise FolderJobV3IdempotencyConflict(
                        "Requested job path is bound to another exact request."
                    )
                return existing
            return writer.save_new(candidate)

    def _persist_origin_review(
        self,
        job_path: Path,
        prepared: PreparedConnectedChangeOrigin,
    ) -> FolderRefactorJobV3:
        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.rehydrate()
            if current.lifecycle is not FolderJobLifecycleV3.PLANNING:
                return current
            ledger = prepared.evidence_ledger
            authority = GptPlannedJobAuthorityV2(
                planner_checkpoint=GptPlannerCheckpointV2(
                    status="accepted",
                    observable_transcript=tuple(
                        turn.model_dump(mode="json") for turn in ledger.observable_turns
                    ),
                    response_turn_count=ledger.response_turn_count,
                    evidence_call_count=ledger.evidence_call_count,
                    clarification_question=ledger.clarification_question,
                    clarification_answer=ledger.clarification_answer,
                    accepted_plan_fingerprint=ledger.accepted_plan_fingerprint,
                    usage=ledger.usage,
                ),
                evidence_ledger=ledger,
                execution_origin=prepared.execution_origin,
            )
            preview = build_folder_plan_preview(
                job_id=current.job_id,
                expected_job_revision=current.revision + 1,
                proposal_revision=0,
                proposal_basis="fresh_gpt_plan",
                inventory=prepared.initial_scan.inventory,
                reference_graph=prepared.reference_graph,
                accepted_plan=prepared.accepted_plan,
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                authority=authority,
                candidate_plan=prepared.accepted_plan,
                reference_graph=prepared.reference_graph,
                preview=preview,
                lifecycle=FolderJobLifecycleV3.REVIEWING,
            )
            return writer.save(successor, expected_current=current)

    def _persist_application_review(
        self,
        job_path: Path,
        prepared: PreparedConnectedChangeApplication,
    ) -> FolderRefactorJobV3:
        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.rehydrate()
            if current.lifecycle is not FolderJobLifecycleV3.MATCHING:
                return current
            if not isinstance(current.authority, CapsuleAppliedJobAuthorityV2):
                raise FoldweaveReviewServiceError(
                    "authority_mismatch",
                    "Receiver review lacks imported Change File authority.",
                )
            authority = CapsuleAppliedJobAuthorityV2(
                change_file_binding=current.authority.change_file_binding,
                match_report=prepared.match_report,
                execution_origin=prepared.execution_origin,
            )
            preview = build_folder_plan_preview(
                job_id=current.job_id,
                expected_job_revision=current.revision + 1,
                proposal_revision=0,
                proposal_basis="imported_change_file",
                inventory=prepared.initial_scan.inventory,
                reference_graph=prepared.reference_graph,
                accepted_plan=prepared.accepted_plan,
                imported_change_file_fingerprint=(
                    prepared.change_file.change_file_fingerprint
                ),
                match_report_fingerprint=(
                    prepared.match_report.match_report_fingerprint
                ),
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                authority=authority,
                candidate_plan=prepared.accepted_plan,
                reference_graph=prepared.reference_graph,
                preview=preview,
                lifecycle=FolderJobLifecycleV3.REVIEWING,
            )
            return writer.save(successor, expected_current=current)

    def _execute_locked(
        self,
        writer: FolderRefactorJobV3Writer,
        job: FolderRefactorJobV3,
        *,
        progress_callback: FolderTransactionProgress | None,
    ) -> FolderRefactorJobV3:
        try:
            assert job.pending_result_path is not None
            assert job.final_result_path is not None
            if os.path.lexists(job.final_result_path):
                return self._recover_promoted_result(writer, job)
            prepared = self._rehydrate_prepared(job)
            result = execute_prepared_connected_change(
                prepared=prepared,
                output_parent=job.output_parent,
                job_id=job.job_id,
                transaction_paths=FolderTransactionPaths(
                    job_id=job.job_id,
                    pending_root=job.pending_result_path,
                    final_root=job.final_result_path,
                ),
                progress_callback=progress_callback,
            )
            if result.folder_run.result_root != job.final_result_path:
                raise FoldweaveReviewServiceError(
                    "result_path_mismatch",
                    "Execution promoted a result at another path.",
                )
            verification = verify_connected_result(job.final_result_path)
            self._require_bound_verification(job, verification)
            assert verification.receipt_fingerprint is not None
            assert verification.organized_tree_commitment is not None
            verified = evolve_job_v3(
                job,
                revision=job.revision + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.VERIFIED,
                pending_result_path=None,
                verified_artifacts=FolderJobVerifiedArtifactsV3(
                    receipt_fingerprint=verification.receipt_fingerprint,
                    organized_tree_commitment=(verification.organized_tree_commitment),
                    change_file_fingerprint=result.change_file_fingerprint,
                    verification_fingerprint=canonical_sha256(verification),
                ),
            )
            return writer.save(verified, expected_current=job)
        except (
            ConnectedChangeError,
            FolderTransactionError,
            FoldweaveReviewServiceError,
            ValueError,
        ) as exc:
            current = writer.load()
            if current.lifecycle.terminal:
                return current
            blocked = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.BLOCKED,
                blocker_code=_error_code(exc, "review_execution_blocked"),
                blocker_message=str(exc),
            )
            return writer.save(blocked, expected_current=current)

    def _recover_promoted_result(
        self,
        writer: FolderRefactorJobV3Writer,
        job: FolderRefactorJobV3,
    ) -> FolderRefactorJobV3:
        """Finalize one promoted result after a lost final job checkpoint."""

        assert job.pending_result_path is not None
        assert job.final_result_path is not None
        if os.path.lexists(job.pending_result_path):
            raise FoldweaveReviewServiceError(
                "execution_recovery_ambiguous",
                "Both pending and final result paths exist for the executing job.",
            )
        verification = verify_connected_result(job.final_result_path)
        self._require_bound_verification(job, verification)
        change_file_path = job.final_result_path / CONNECTED_CHANGE_PATH
        payload = change_file_path.read_bytes()
        change_file = parse_connected_change_file(payload)
        if canonical_portable_json_bytes(change_file) != payload:
            raise FoldweaveReviewServiceError(
                "execution_recovery_change_file_invalid",
                "Promoted result contains a noncanonical Change File.",
            )
        assert verification.receipt_fingerprint is not None
        assert verification.organized_tree_commitment is not None
        recovered = evolve_job_v3(
            job,
            revision=job.revision + 1,
            updated_at=_now(),
            lifecycle=FolderJobLifecycleV3.VERIFIED,
            pending_result_path=None,
            verified_artifacts=FolderJobVerifiedArtifactsV3(
                receipt_fingerprint=verification.receipt_fingerprint,
                organized_tree_commitment=verification.organized_tree_commitment,
                change_file_fingerprint=change_file.change_file_fingerprint,
                verification_fingerprint=canonical_sha256(verification),
            ),
        )
        return writer.save(recovered, expected_current=job)

    @staticmethod
    def _rehydrate_prepared(job: FolderRefactorJobV3) -> PreparedConnectedChange:
        if job.candidate_plan is None:
            raise FoldweaveReviewServiceError(
                "candidate_missing",
                "Authorized job lacks its complete candidate.",
            )
        if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
            prepared = prepare_connected_change_application(
                change_file_path=job.authority.change_file_binding.path,
                source_root=job.source_root,
            )
            if (
                prepared.accepted_plan != job.candidate_plan
                or prepared.match_report != job.authority.match_report
                or prepared.execution_origin != job.authority.execution_origin
            ):
                raise FoldweaveReviewServiceError(
                    "receiver_authority_changed",
                    "Recomputed receiver preparation differs from review authority.",
                )
            return prepared
        ledger = job.authority.evidence_ledger
        origin = job.authority.execution_origin
        if ledger is None or origin is None:
            raise FoldweaveReviewServiceError(
                "origin_authority_missing",
                "Authorized origin lacks its persisted planning evidence.",
            )
        return rehydrate_prepared_connected_change_origin(
            source_root=job.source_root,
            request=job.user_request,
            accepted_plan=job.candidate_plan,
            execution_origin=origin,
            evidence_ledger=ledger,
        )

    @staticmethod
    def _require_exact_review_request(
        job: FolderRefactorJobV3,
        *,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        output_parent: Path,
        result_folder_name: str,
    ) -> None:
        preview = job.preview
        candidate = job.candidate_plan
        if preview is None or candidate is None:
            raise FoldweaveReviewServiceError(
                "preview_unavailable",
                "The job has no complete review preview.",
            )
        if expected_revision != job.revision:
            raise FolderJobV3RevisionError("Acceptance targets a stale job revision.")
        if (
            preview_fingerprint != preview.preview_fingerprint
            or candidate_fingerprint != preview.compiled_candidate_fingerprint
        ):
            raise FolderJobV3RevisionError(
                "Acceptance targets another candidate or preview."
            )
        if output_parent.resolve(strict=False) != job.output_parent:
            raise FolderJobV3RevisionError(
                "Acceptance changes the reviewed output destination."
            )
        if result_folder_name != candidate.result_folder_name:
            raise FolderJobV3RevisionError(
                "Acceptance changes the reviewed result-folder name."
            )

    @staticmethod
    def _require_exact_authorization_retry(
        job: FolderRefactorJobV3,
        *,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        output_parent: Path,
        result_folder_name: str,
        idempotency_key: str,
        channel: ReviewChannel,
    ) -> None:
        authorization = job.execution_authorization
        if authorization is None:
            raise FoldweaveReviewServiceError(
                "authorization_missing",
                "Executing or verified job lacks authorization.",
            )
        repeated = build_execution_authorization(
            job=job,
            expected_job_revision=expected_revision,
            preview_fingerprint=preview_fingerprint,
            candidate_fingerprint=candidate_fingerprint,
            output_parent=output_parent,
            result_folder_name=result_folder_name,
            idempotency_key=idempotency_key,
            channel=channel,
            clock=lambda: authorization.authorization_timestamp,
        )
        if repeated != authorization:
            raise FolderJobV3IdempotencyConflict(
                "Acceptance retry is bound to another exact request."
            )

    def _require_verified_job(self, job_path: Path) -> FolderRefactorJobV3:
        job = self.status(job_path)
        if (
            job.lifecycle is not FolderJobLifecycleV3.VERIFIED
            or job.final_result_path is None
            or job.verified_artifacts is None
        ):
            raise FoldweaveReviewServiceError(
                "result_not_verified",
                f"Job has no verified result: {job.lifecycle.value}.",
            )
        return job

    @staticmethod
    def _require_bound_verification(
        job: FolderRefactorJobV3,
        verification: ConnectedReceiptVerification,
    ) -> None:
        if (
            verification.status is not ConnectedReceiptVerificationStatus.VERIFIED
            or verification.job_id != job.job_id
        ):
            raise FoldweaveReviewServiceError(
                "independent_verification_failed",
                "Result did not pass source-free verification for this job.",
            )

    def _block_if_current(
        self,
        job_path: Path,
        *,
        expected: FolderRefactorJobV3,
        code: str,
        message: str,
    ) -> FolderRefactorJobV3:
        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.rehydrate()
            if current.lifecycle.terminal:
                return current
            if current != expected:
                return current
            blocked = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.BLOCKED,
                blocker_code=code,
                blocker_message=message,
            )
            return writer.save(blocked, expected_current=current)


def _v3_from_seed(
    seed: FolderRefactorJobV2,
    *,
    lifecycle: Literal[
        FolderJobLifecycleV3.PLANNING,
        FolderJobLifecycleV3.MATCHING,
    ],
) -> FolderRefactorJobV3:
    return FolderRefactorJobV3(
        revision=seed.revision,
        job_id=seed.job_id,
        display_name=seed.display_name,
        created_at=seed.created_at,
        updated_at=seed.updated_at,
        source_root=seed.source_root,
        output_parent=seed.output_parent,
        job_path=seed.job_path,
        source_inventory=seed.source_inventory,
        local_file_identities=seed.local_file_identities,
        local_directory_identities=seed.local_directory_identities,
        user_request=seed.user_request,
        idempotency=seed.idempotency,
        authority=seed.authority,
        lifecycle=lifecycle,
    )


def _revision_instruction_for_request(
    *,
    candidate_fingerprint: str,
    preview_fingerprint: str,
    instruction: str,
    idempotency_key: str,
):
    return build_revision_instruction(
        base_candidate_fingerprint=candidate_fingerprint,
        base_preview_fingerprint=preview_fingerprint,
        instruction=instruction,
        idempotency_key=idempotency_key,
    )


def _require_v3_planning_authority(
    job: FolderRefactorJobV3,
) -> GptPlannedJobAuthorityV3:
    if not isinstance(job.authority, GptPlannedJobAuthorityV3):
        raise FoldweaveReviewServiceError(
            "planner_authority_mismatch",
            "Operation requires Foldweave v3 planning authority.",
        )
    return job.authority


def _require_composite_ledger(
    authority: GptPlannedJobAuthorityV3,
) -> FolderEvidenceLedgerV2:
    if authority.evidence_ledger is None:
        raise FoldweaveReviewServiceError(
            "planner_evidence_missing",
            "Review operation lacks composite planner evidence.",
        )
    return authority.evidence_ledger


def _require_candidate(job: FolderRefactorJobV3):
    if job.candidate_plan is None:
        raise FoldweaveReviewServiceError(
            "candidate_missing",
            "Review operation lacks a complete candidate.",
        )
    return job.candidate_plan


def _model_transport_for_provider(
    provider_kind: Literal["deterministic", "live", "recorded_replay"],
) -> PlannerModelTransport:
    return {
        "deterministic": "deterministic_development",
        "live": "responses_api",
        "recorded_replay": "recorded_replay",
    }[provider_kind]


def _require_revision_provider_matches(
    ledger: FolderEvidenceLedgerV2,
    provider: FolderPlanRevisionProvider,
) -> None:
    if _model_transport_for_provider(provider.provider_kind) != ledger.model_transport:
        raise FoldweaveReviewServiceError(
            "revision_provider_mismatch",
            "Revision provider differs from the durable planning transport.",
        )
    if provider.provider_kind == "live" and provider.usage != ledger.usage:
        raise FoldweaveReviewServiceError(
            "revision_usage_prefix_mismatch",
            "Revision provider usage differs from the durable direct prefix.",
        )


def _revision_turn_usage(
    provider: FolderPlanRevisionProvider,
    response_turn: int,
) -> FolderPlannerUsage | None:
    if provider.provider_kind != "live":
        if provider.usage:
            raise FoldweaveReviewServiceError(
                "revision_usage_origin_invalid",
                "Model-free revision cannot report direct API usage.",
            )
        return None
    matches = tuple(
        item for item in provider.usage if item.response_turn == response_turn
    )
    if len(matches) != 1:
        raise FoldweaveReviewServiceError(
            "revision_usage_missing",
            "Direct revision lacks one exact observable usage record.",
        )
    return matches[0]


def _revision_rejections_with_current_failure(
    job: FolderRefactorJobV3,
) -> tuple[FolderRevisionRejectionRecordV1, ...]:
    """Materialize one legacy current rejection before clearing UI state."""

    existing = job.revision_rejections
    if (
        job.lifecycle is not FolderJobLifecycleV3.REVISION_FAILED
        or job.revision_failure is None
        or not isinstance(job.authority, GptPlannedJobAuthorityV3)
        or job.authority.evidence_ledger is None
    ):
        return existing
    ledger = job.authority.evidence_ledger
    segment = ledger.segments[-1]
    if (
        segment.segment_kind != "user_revision"
        or segment.selected
        or segment.revision_instruction_fingerprint
        != job.revision_failure.attempted_instruction_fingerprint
        or any(
            record.segment_fingerprint == segment.segment_fingerprint
            for record in existing
        )
    ):
        return existing
    rejection = build_revision_rejection_record(
        attempt_index=job.revision_attempt_count,
        ledger=ledger,
        failure=job.revision_failure,
    )
    return (*existing, rejection)


def _compile_sparse_revision(
    job: FolderRefactorJobV3,
    *,
    ledger: FolderEvidenceLedgerV2,
    turn: FolderRevisionTurnRecordV1,
):
    candidate = _require_candidate(job)
    revision = turn.response.revision
    by_file_id = {item.file_id: item for item in revision.entries}
    mappings = {item.file_id: item for item in candidate.file_mappings}
    unknown = set(by_file_id) - set(mappings)
    protected = {
        file_id for file_id, mapping in mappings.items() if mapping.protected
    } & set(by_file_id)
    if unknown:
        raise PlanCompilationError(
            "revision_unknown_file_id",
            f"Sparse revision names unknown file IDs: {sorted(unknown)!r}.",
        )
    if protected:
        raise PlanCompilationError(
            "revision_protected_file",
            f"Sparse revision names protected file IDs: {sorted(protected)!r}.",
        )
    result_folder_name = (
        revision.replacement_result_folder_name or candidate.result_folder_name
    )
    changed_target = any(
        mappings[file_id].target_path != entry.replacement_target_path
        for file_id, entry in by_file_id.items()
    )
    if not changed_target and result_folder_name == candidate.result_folder_name:
        raise PlanCompilationError(
            "revision_no_change",
            "Sparse revision does not change the reviewed structure.",
        )
    entries = []
    for mapping in candidate.file_mappings:
        if mapping.protected:
            continue
        replacement = by_file_id.get(mapping.file_id)
        entries.append(
            FolderPlanEntry(
                file_id=mapping.file_id,
                original_path=mapping.original_path,
                proposed_target=(
                    replacement.replacement_target_path
                    if replacement is not None
                    else mapping.target_path
                ),
                rationale=(
                    replacement.rationale
                    if replacement is not None
                    else "Retained from the mechanically accepted base proposal."
                ),
                evidence_ids=(
                    replacement.evidence_ids
                    if replacement is not None
                    else ("initial_inventory",)
                ),
            )
        )
    complete = FolderPlan(
        source_commitment=candidate.source_commitment,
        request_fingerprint=candidate.request_fingerprint,
        request_scope=candidate.request_scope,
        evidence_fingerprint=ledger.evidence_fingerprint,
        result_folder_name=result_folder_name,
        entries=tuple(entries),
        exclusions=(),
    )
    known_evidence = {
        "initial_inventory",
        *(record.fingerprint for record in ledger.initial_ledger.evidence_records),
    }
    compiled = compile_plan(
        job.source_inventory,
        job.user_request,
        complete,
        known_evidence_ids=known_evidence,
        evidence_fingerprint=ledger.evidence_fingerprint,
        reference_graph=_require_reference_graph(job),
    )
    return convert_planner_accepted_plan(
        inventory=job.source_inventory,
        request=job.user_request,
        plan=compiled,
        evidence_schema_version="folder-evidence-ledger.v2",
    )


def _require_reference_graph(job: FolderRefactorJobV3) -> FolderReferenceGraph:
    if job.reference_graph is None:
        raise FoldweaveReviewServiceError(
            "reference_graph_missing",
            "Review operation lacks its immutable source reference graph.",
        )
    return job.reference_graph


def _build_preview(
    job: FolderRefactorJobV3,
    *,
    accepted_plan,
    expected_job_revision: int,
    proposal_revision: int,
) -> FolderPlanPreviewV1:
    previous = job.preview
    if previous is None:
        raise FoldweaveReviewServiceError(
            "preview_unavailable",
            "Review operation lacks its prior preview.",
        )
    return build_folder_plan_preview(
        job_id=job.job_id,
        expected_job_revision=expected_job_revision,
        proposal_revision=proposal_revision,
        proposal_basis=previous.proposal_basis,
        inventory=job.source_inventory,
        reference_graph=_require_reference_graph(job),
        accepted_plan=accepted_plan,
        imported_change_file_fingerprint=(previous.imported_change_file_fingerprint),
        match_report_fingerprint=previous.match_report_fingerprint,
        immediate_parent_candidate_fingerprint=(
            job.immediate_parent_candidate_fingerprint
        ),
    )


def _rebuild_preview(
    job: FolderRefactorJobV3,
    *,
    expected_job_revision: int,
) -> FolderPlanPreviewV1:
    return _build_preview(
        job,
        accepted_plan=_require_candidate(job),
        expected_job_revision=expected_job_revision,
        proposal_revision=job.proposal_revision,
    )


def _require_absent_result_path(path: Path, *, label: str) -> None:
    if os.path.lexists(path):
        raise FoldweaveReviewServiceError(
            "result_path_unavailable",
            f"{label} already exists: {path}",
        )


def _error_code(error: BaseException, fallback: str) -> str:
    code = getattr(error, "code", None)
    return code if isinstance(code, str) and code else fallback


def _now() -> datetime:
    return datetime.now(tz=oslo_tz)
