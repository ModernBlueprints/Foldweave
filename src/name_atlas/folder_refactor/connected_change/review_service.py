"""Foldweave review orchestration over the single Connected Change engine."""

from __future__ import annotations

import os
import time
import uuid
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from name_atlas.folder_refactor.compiler import PlanCompilationError
from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
    convert_planner_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    ConnectedChangeError,
)
from name_atlas.folder_refactor.connected_change.derivative import (
    FolderDerivativeCreationBindingV1,
    build_derivative_creation_binding,
    build_derivative_parent_binding,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.evidence import (
    build_deterministic_origin_evidence,
    build_planner_origin_evidence,
)
from name_atlas.folder_refactor.connected_change.job_io import (
    DurableJobFileLock,
    DurableJobLockError,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
    FolderIdempotencyBindingV2,
    FolderRefactorJobV2,
    GptPlannerCheckpointV2,
    JobLocalDirectoryIdentityV2,
    JobLocalFileIdentityV2,
    build_change_file_input_binding,
    build_new_capsule_job_v2,
    build_new_gpt_job_v2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderDestinationReservationV1,
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    FolderJobV3LoadError,
    FolderJobV3RevisionError,
    FolderJobVerifiedArtifactsV3,
    FolderPublicJobCapabilityV1,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    FolderRefactorJobV3Writer,
    FolderRevisionFailureV1,
    FolderRevisionInstructionV1,
    FolderRevisionRejectionRecordV1,
    GptDerivativeJobAuthorityV3,
    GptPlannedJobAuthorityV3,
    build_destination_reservation,
    build_execution_authorization,
    build_keep_previous_action,
    build_recreate_original_operation_binding_v3,
    build_revision_instruction,
    build_revision_mutation_binding,
    build_revision_provider_failure,
    build_revision_rejection_record,
    evolve_job_v3,
    expected_final_result_path_v3,
    expected_pending_result_path_v3,
    load_folder_job_record_v3,
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
    PreparedFoldweaveDerivative,
    execute_prepared_connected_change,
    execute_prepared_foldweave_derivative,
    prepare_connected_change_application,
    prepare_connected_change_origin,
    prepare_foldweave_derivative_execution,
    rehydrate_prepared_connected_change_origin,
)
from name_atlas.folder_refactor.connected_change.sparse_revision import (
    compile_sparse_revision_from_base,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerification,
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.contracts import (
    AcceptedFileMapping,
    FolderAcceptedPlan,
)
from name_atlas.folder_refactor.foldweave_host_contracts import (
    FolderHostDerivativeRevisionTurnRecordV1,
    FolderHostPlanRevisionV1,
    HostModelTransport,
    build_host_derivative_pending_revision,
    build_host_derivative_revision_turn,
    host_contract_freeze_fingerprint,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeRevisionTurnInputV1,
    FolderDerivativeRevisionTurnRecordV1,
    FolderEvidenceLedgerV2,
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionProvider,
    FolderPlanRevisionV1,
    FolderRevisionTurnRecordV1,
    append_failed_revision_evidence,
    append_successful_revision_evidence,
    build_derivative_composite_evidence,
    build_derivative_evidence_ledger,
    build_derivative_revision_turn_record,
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
from name_atlas.folder_refactor.planner_evidence import (
    LocalFolderEvidenceService,
    create_initial_evidence_ledger,
)
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
        initial_progress = create_planner_progress(
            seed.source_inventory,
            request,
            job_id=job_id,
            provider_kind="deterministic",
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
        observed = store.inspect()
        if isinstance(observed.authority, GptDerivativeJobAuthorityV3):
            return await self._revise_direct_derivative_followup(
                job_path,
                expected_revision=expected_revision,
                preview_fingerprint=preview_fingerprint,
                candidate_fingerprint=candidate_fingerprint,
                instruction=instruction,
                idempotency_key=idempotency_key,
                provider=provider,
                provider_factory=provider_factory,
            )
        with store.writer() as writer:
            job = writer.rehydrate()
            repeated = _revision_instruction_for_request(
                candidate_fingerprint=candidate_fingerprint,
                preview_fingerprint=preview_fingerprint,
                instruction=instruction,
                idempotency_key=idempotency_key,
            )
            completed_retry = _completed_revision_retry_or_none(
                job,
                expected_revision=expected_revision,
                instruction=repeated,
            )
            if completed_retry is not None:
                return completed_retry
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

    async def _revise_direct_derivative_followup(
        self,
        job_path: Path,
        *,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        instruction: str,
        idempotency_key: str,
        provider: FolderPlanRevisionProvider | None,
        provider_factory: Callable[[], FolderPlanRevisionProvider] | None,
    ) -> FolderRefactorJobV3:
        """Run the one remaining direct sparse turn on a completed child."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            repeated = _revision_instruction_for_request(
                candidate_fingerprint=candidate_fingerprint,
                preview_fingerprint=preview_fingerprint,
                instruction=instruction,
                idempotency_key=idempotency_key,
            )
            completed_retry = _completed_revision_retry_or_none(
                job,
                expected_revision=expected_revision,
                instruction=repeated,
            )
            if completed_retry is not None:
                return completed_retry
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
            authority = _require_completed_direct_derivative_authority(job)
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
            ledger = _require_derivative_composite_ledger(authority)
            if job.revision_attempt_count >= 2 or job.proposal_revision >= 2:
                raise FoldweaveReviewServiceError(
                    "revision_limit_reached",
                    "This derivative job has reached the two-revision limit.",
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
                revision_instruction_fingerprint=repeated.instruction_fingerprint,
                base_candidate=_require_candidate(job),
                base_candidate_fingerprint=candidate_fingerprint,
                base_preview_fingerprint=preview_fingerprint,
                evidence_fingerprint=ledger.evidence_fingerprint,
                prior_transcript_fingerprint=ledger.transcript_fingerprint,
                turn_contract_freeze_fingerprint=(
                    authority.creation_binding.contract_freeze_fingerprint
                ),
                imported_change_file_fingerprint=(
                    authority.parent_binding.imported_change_file_fingerprint
                ),
                match_report_fingerprint=(
                    authority.parent_binding.match_report.match_report_fingerprint
                ),
                immediate_parent_candidate_fingerprint=(
                    authority.parent_binding.parent_candidate_fingerprint
                ),
            )
            revising_authority = authority.model_copy(
                update={"pending_direct_followup_revision": turn_input}
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
                return _kept_review_target(job)
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
            saved = writer.save(successor, expected_current=job)
            return _kept_review_target(saved)

    def prepare_application_review(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        idempotency_key: str,
        job_id: str | None = None,
        public_job_capability: FolderPublicJobCapabilityV1 | None = None,
    ) -> FolderRefactorJobV3:
        """Create or resume one model-free receiver job through review only."""

        identifier = job_id or uuid.uuid4().hex
        seed = build_new_capsule_job_v2(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            change_file_path=change_file_path,
            idempotency_key=idempotency_key,
            job_id=identifier,
        )
        initial = _v3_from_seed(
            seed,
            lifecycle=FolderJobLifecycleV3.MATCHING,
            public_job_capability=public_job_capability,
        )
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

    def create_or_resume_derivative_child(
        self,
        parent_job_path: Path,
        *,
        output_parent: Path,
        instruction: str,
        idempotency_key: str,
        provider_kind: PlannerProviderKind | None = None,
        model_transport: HostModelTransport | None = None,
        channel: ReviewChannel,
        public_job_capability_factory: (
            Callable[[str], FolderPublicJobCapabilityV1 | None] | None
        ) = None,
    ) -> FolderRefactorJobV3:
        """Persist one immutable provider-neutral derivative child."""

        child, _created = self.create_or_resume_derivative_child_with_status(
            parent_job_path,
            output_parent=output_parent,
            instruction=instruction,
            idempotency_key=idempotency_key,
            provider_kind=provider_kind,
            model_transport=model_transport,
            channel=channel,
            public_job_capability_factory=public_job_capability_factory,
        )
        return child

    def create_or_resume_derivative_child_with_status(
        self,
        parent_job_path: Path,
        *,
        output_parent: Path,
        instruction: str,
        idempotency_key: str,
        provider_kind: PlannerProviderKind | None = None,
        model_transport: HostModelTransport | None = None,
        channel: ReviewChannel,
        public_job_capability_factory: (
            Callable[[str], FolderPublicJobCapabilityV1 | None] | None
        ) = None,
    ) -> tuple[FolderRefactorJobV3, bool]:
        """Return the exact child and whether this call created its authority."""

        if (provider_kind is None) == (model_transport is None):
            raise FoldweaveReviewServiceError(
                "derivative_transport_invalid",
                "Derivative creation requires exactly one direct or hosted transport.",
            )
        selected_transport = (
            _model_transport_for_provider(provider_kind)
            if provider_kind is not None
            else model_transport
        )
        assert selected_transport is not None
        idempotency_key_sha256 = canonical_sha256(
            {
                "domain": "foldweave:revision-idempotency-key:v1",
                "key": idempotency_key,
            }
        )
        existing = _derivative_child_retry_by_inputs_or_none(
            parent_job_path.resolve(strict=False).parent,
            parent_job_path=parent_job_path,
            output_parent=output_parent,
            instruction=instruction,
            idempotency_key_sha256=idempotency_key_sha256,
            model_transport=selected_transport,
            channel=channel,
        )
        if existing is not None:
            return existing, False

        with _derivative_parent_snapshot_lock(parent_job_path):
            parent = FolderRefactorJobV3Store(parent_job_path).inspect()
            prepared = self._require_fresh_derivative_parent(parent)
            candidate = _require_candidate(parent)
            preview = self.get_preview(parent.job_path)
            instruction_binding = build_revision_instruction(
                base_candidate_fingerprint=preview.compiled_candidate_fingerprint,
                base_preview_fingerprint=preview.preview_fingerprint,
                instruction=instruction,
                idempotency_key=idempotency_key,
            )
            change_file = parent.authority.change_file_binding.change_file
            lineage = getattr(change_file.core, "lineage", None)
            parent_generation = getattr(lineage, "generation", 0)
            parent_binding = build_derivative_parent_binding(
                parent_job_id=parent.job_id,
                parent_job_path=parent.job_path,
                parent_source_root=parent.source_root,
                parent_job_revision=parent.revision,
                parent_proposal_revision=parent.proposal_revision,
                parent_source_commitment=parent.source_inventory.source_commitment,
                parent_candidate=candidate,
                parent_preview=preview,
                change_file_binding=parent.authority.change_file_binding,
                match_report=parent.authority.match_report,
                generation=parent_generation + 1,
            )
            evidence_state = create_initial_evidence_ledger(
                prepared.initial_scan.inventory,
                parent.user_request,
            )
            resolved_output = output_parent.resolve(strict=True)
            if not resolved_output.is_dir():
                raise FoldweaveReviewServiceError(
                    "derivative_output_parent_invalid",
                    "Derivative output parent must be an existing directory.",
                )
            jobs_directory = parent.job_path.parent.resolve(strict=False)
            child_job_id = uuid.uuid4().hex
            child_job_path = jobs_directory / f"{child_job_id}.json"
            creation = build_derivative_creation_binding(
                parent_binding=parent_binding,
                child_job_id=child_job_id,
                child_job_path=child_job_path,
                source_root=parent.source_root,
                output_parent=resolved_output,
                revision_instruction_fingerprint=(
                    instruction_binding.instruction_fingerprint
                ),
                evidence_fingerprint=evidence_state.evidence_fingerprint,
                contract_freeze_fingerprint=(
                    host_contract_freeze_fingerprint()
                    if model_transport is not None
                    else FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT
                ),
                model_transport=selected_transport,
                channel=channel,
                idempotency_key_sha256=(instruction_binding.idempotency_key_sha256),
            )
            with _derivative_child_creation_lock(jobs_directory):
                existing = _derivative_child_retry_or_none(
                    jobs_directory,
                    creation=creation,
                )
                if existing is not None:
                    return existing, False
                turn_input = None
                host_turn_input = None
                if provider_kind is not None:
                    turn_input = FolderDerivativeRevisionTurnInputV1(
                        job_id=child_job_id,
                        expected_job_revision=0,
                        provider_kind=provider_kind,
                        request=parent.user_request,
                        request_fingerprint=request_fingerprint(parent.user_request),
                        source_commitment=parent.source_inventory.source_commitment,
                        revision_instruction=instruction_binding.instruction,
                        revision_instruction_fingerprint=(
                            instruction_binding.instruction_fingerprint
                        ),
                        base_candidate=candidate,
                        base_candidate_fingerprint=(
                            parent_binding.parent_candidate_fingerprint
                        ),
                        base_preview_fingerprint=(
                            parent_binding.parent_preview_fingerprint
                        ),
                        evidence_fingerprint=evidence_state.evidence_fingerprint,
                        prior_transcript_fingerprint=creation.binding_fingerprint,
                        turn_contract_freeze_fingerprint=(
                            creation.contract_freeze_fingerprint
                        ),
                        imported_change_file_fingerprint=(
                            parent_binding.imported_change_file_fingerprint
                        ),
                        match_report_fingerprint=(
                            parent_binding.match_report.match_report_fingerprint
                        ),
                        immediate_parent_candidate_fingerprint=(
                            parent_binding.parent_candidate_fingerprint
                        ),
                    )
                else:
                    host_turn_input = build_host_derivative_pending_revision(
                        job_id=child_job_id,
                        model_transport=selected_transport,
                        expected_job_revision=0,
                        proposal_revision=0,
                        response_turn=1,
                        base_candidate_fingerprint=(
                            parent_binding.parent_candidate_fingerprint
                        ),
                        base_preview_fingerprint=(
                            parent_binding.parent_preview_fingerprint
                        ),
                        revision_instruction_fingerprint=(
                            instruction_binding.instruction_fingerprint
                        ),
                        initial_evidence_fingerprint=(
                            evidence_state.evidence_fingerprint
                        ),
                        evidence_state=evidence_state,
                        evidence_fingerprint=evidence_state.evidence_fingerprint,
                        prior_transcript_fingerprint=creation.binding_fingerprint,
                        turn_contract_freeze_fingerprint=(
                            creation.contract_freeze_fingerprint
                        ),
                        imported_change_file_fingerprint=(
                            parent_binding.imported_change_file_fingerprint
                        ),
                        match_report_fingerprint=(
                            parent_binding.match_report.match_report_fingerprint
                        ),
                        immediate_parent_candidate_fingerprint=(
                            parent_binding.parent_candidate_fingerprint
                        ),
                        idempotency_key_sha256=(
                            instruction_binding.idempotency_key_sha256
                        ),
                    )
                authority = GptDerivativeJobAuthorityV3(
                    authority_state="awaiting_model_response",
                    model_transport=selected_transport,
                    parent_binding=parent_binding,
                    creation_binding=creation,
                    pending_direct_revision=turn_input,
                    pending_host_revision=host_turn_input,
                )
                now = _now()
                child = FolderRefactorJobV3(
                    revision=0,
                    proposal_revision=0,
                    revision_attempt_count=1,
                    job_id=child_job_id,
                    display_name=f"{parent.display_name[:189]} derivative",
                    created_at=now,
                    updated_at=now,
                    source_root=parent.source_root,
                    output_parent=resolved_output,
                    job_path=child_job_path,
                    source_inventory=parent.source_inventory,
                    local_file_identities=parent.local_file_identities,
                    local_directory_identities=parent.local_directory_identities,
                    user_request=parent.user_request,
                    idempotency=FolderIdempotencyBindingV2(
                        key_sha256=creation.idempotency_key_sha256,
                        request_fingerprint=creation.request_fingerprint,
                    ),
                    operation_idempotency=(
                        build_recreate_original_operation_binding_v3(
                            job_id=child_job_id,
                            idempotency_key=idempotency_key,
                        ),
                    ),
                    public_job_capability=(
                        public_job_capability_factory(child_job_id)
                        if public_job_capability_factory is not None
                        else None
                    ),
                    authority=authority,
                    revision_instruction=instruction_binding,
                    immediate_parent_job_id=parent.job_id,
                    immediate_parent_candidate_fingerprint=(
                        parent_binding.parent_candidate_fingerprint
                    ),
                    lifecycle=FolderJobLifecycleV3.REVISING,
                )
                store = FolderRefactorJobV3Store(child_job_path)
                with store.writer() as writer:
                    return writer.save_new(child), True

    async def submit_direct_derivative_revision(
        self,
        job_path: Path,
        *,
        provider: FolderPlanRevisionProvider,
    ) -> FolderRefactorJobV3:
        """Invoke one already-persisted derivative turn and stop at review."""

        call_lock = _derivative_provider_call_lock(job_path)
        with call_lock:
            current = self.status(job_path)
            if not isinstance(current.authority, GptDerivativeJobAuthorityV3):
                raise FoldweaveReviewServiceError(
                    "derivative_authority_mismatch",
                    "Direct derivative submission requires derivative authority.",
                )
            if current.authority.authority_state == "completed":
                return current
            if current.lifecycle is not FolderJobLifecycleV3.REVISING:
                return current
            turn_input = current.authority.pending_direct_revision
            if turn_input is None:
                raise FoldweaveReviewServiceError(
                    "derivative_turn_missing",
                    "Pending derivative child lacks its exact direct turn.",
                )
            if provider.provider_kind != turn_input.provider_kind:
                raise FoldweaveReviewServiceError(
                    "derivative_provider_mismatch",
                    "Derivative provider differs from the persisted direct turn.",
                )
            if tuple(provider.usage):
                raise FoldweaveReviewServiceError(
                    "derivative_usage_prefix_mismatch",
                    "Derivative provider must begin with no direct usage prefix.",
                )
            try:
                prepared = self._require_fresh_derivative_child(current)
            except Exception as exc:
                return self._block_if_current(
                    job_path,
                    expected=current,
                    code=_error_code(exc, "derivative_inputs_stale"),
                    message=str(exc),
                )
            try:
                response = await provider.exchange(turn_input)
                usage = _derivative_turn_usage(provider)
                turn = build_derivative_revision_turn_record(
                    turn_input=turn_input,
                    response=response,
                    usage=usage,
                )
                accepted_plan = _compile_derivative_first_revision(
                    current,
                    prepared=prepared,
                    turn=turn,
                )
            except Exception as exc:
                return self._persist_derivative_failure(
                    job_path,
                    expected=current,
                    code=_error_code(exc, "derivative_revision_failed"),
                    detail=str(exc),
                    prepared=prepared,
                )
            try:
                return self._persist_derivative_success(
                    job_path,
                    expected=current,
                    prepared=prepared,
                    turn=turn,
                    accepted_plan=accepted_plan,
                )
            except Exception as exc:
                return self._persist_derivative_failure(
                    job_path,
                    expected=current,
                    code=_error_code(exc, "derivative_revision_persistence_failed"),
                    detail=str(exc),
                    prepared=prepared,
                )

    def submit_host_derivative_revision(
        self,
        job_path: Path,
        *,
        call_id: str,
        revision: FolderHostPlanRevisionV1,
    ) -> FolderRefactorJobV3:
        """Compile one provider-free hosted derivative turn into T2 review."""

        with _derivative_provider_call_lock(job_path):
            current = self.status(job_path)
            authority = current.authority
            if not isinstance(authority, GptDerivativeJobAuthorityV3) or (
                authority.model_transport not in {"chatgpt_hosted", "codex_hosted"}
            ):
                raise FoldweaveReviewServiceError(
                    "derivative_authority_mismatch",
                    "Hosted derivative submission requires hosted child authority.",
                )
            repeated = _host_derivative_submission_retry_or_none(
                current,
                call_id=call_id,
                revision=revision,
            )
            if repeated is not None:
                return repeated
            pending = authority.pending_host_revision
            if (
                authority.authority_state != "awaiting_model_response"
                or current.lifecycle is not FolderJobLifecycleV3.REVISING
                or pending is None
            ):
                raise FoldweaveReviewServiceError(
                    "derivative_turn_missing",
                    "Hosted derivative child lacks its exact pending turn.",
                )
            try:
                prepared = self._require_fresh_derivative_child(current)
            except Exception as exc:
                return self._block_if_current(
                    job_path,
                    expected=current,
                    code=_error_code(exc, "derivative_inputs_stale"),
                    message=str(exc),
                )
            try:
                accepted_plan = _compile_host_derivative_first_revision(
                    current,
                    prepared=prepared,
                    revision=revision,
                )
            except (PlanCompilationError, ValueError) as exc:
                code = _error_code(exc, "derivative_revision_failed")
                detail = str(exc)
                rejected_turn = build_host_derivative_revision_turn(
                    model_transport=authority.model_transport,
                    response_turn=1,
                    call_id=call_id,
                    pending_revision_fingerprint=pending.pending_fingerprint,
                    base_candidate_fingerprint=pending.base_candidate_fingerprint,
                    base_preview_fingerprint=pending.base_preview_fingerprint,
                    revision_instruction_fingerprint=(
                        pending.revision_instruction_fingerprint
                    ),
                    evidence_fingerprint=pending.evidence_fingerprint,
                    prior_transcript_fingerprint=(pending.prior_transcript_fingerprint),
                    turn_contract_freeze_fingerprint=(
                        pending.turn_contract_freeze_fingerprint
                    ),
                    imported_change_file_fingerprint=(
                        pending.imported_change_file_fingerprint
                    ),
                    match_report_fingerprint=pending.match_report_fingerprint,
                    immediate_parent_candidate_fingerprint=(
                        pending.immediate_parent_candidate_fingerprint
                    ),
                    revision=revision,
                    outcome="rejected",
                    accepted_plan_fingerprint=None,
                    failure_code=code,
                    failure_detail=detail,
                )
                return self._persist_derivative_failure(
                    job_path,
                    expected=current,
                    code=code,
                    detail=detail,
                    host_turn=rejected_turn,
                    prepared=prepared,
                )
            accepted_turn = build_host_derivative_revision_turn(
                model_transport=authority.model_transport,
                response_turn=1,
                call_id=call_id,
                pending_revision_fingerprint=pending.pending_fingerprint,
                base_candidate_fingerprint=pending.base_candidate_fingerprint,
                base_preview_fingerprint=pending.base_preview_fingerprint,
                revision_instruction_fingerprint=(
                    pending.revision_instruction_fingerprint
                ),
                evidence_fingerprint=pending.evidence_fingerprint,
                prior_transcript_fingerprint=pending.prior_transcript_fingerprint,
                turn_contract_freeze_fingerprint=(
                    pending.turn_contract_freeze_fingerprint
                ),
                imported_change_file_fingerprint=(
                    pending.imported_change_file_fingerprint
                ),
                match_report_fingerprint=pending.match_report_fingerprint,
                immediate_parent_candidate_fingerprint=(
                    pending.immediate_parent_candidate_fingerprint
                ),
                revision=revision,
                outcome="accepted",
                accepted_plan_fingerprint=canonical_sha256(accepted_plan),
                failure_code=None,
                failure_detail=None,
            )
            return self._persist_derivative_success(
                job_path,
                expected=current,
                prepared=prepared,
                turn=accepted_turn,
                accepted_plan=accepted_plan,
            )

    def recover_interrupted_direct_derivative(
        self,
        job_path: Path,
    ) -> FolderRefactorJobV3:
        """Fail one interrupted derivative response closed without retry."""

        with _derivative_provider_call_lock(job_path):
            current = self.status(job_path)
            if (
                not isinstance(current.authority, GptDerivativeJobAuthorityV3)
                or current.authority.authority_state != "awaiting_model_response"
                or current.lifecycle is not FolderJobLifecycleV3.REVISING
            ):
                return current
            try:
                prepared = self._require_fresh_derivative_child(current)
            except Exception as exc:
                return self._block_if_current(
                    job_path,
                    expected=current,
                    code=_error_code(exc, "derivative_inputs_stale"),
                    message=str(exc),
                )
            return self._persist_derivative_failure(
                job_path,
                expected=current,
                code="derivative_provider_interrupted",
                detail=(
                    "The process stopped after reserving the derivative turn. No "
                    "provider retry was made; the immutable receiver parent remains "
                    "available unchanged."
                ),
                prepared=prepared,
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
            if not _promoted_result_exists(job):
                self._require_derivative_execution_ready(job)
            reservation = _require_destination_reservation(job)
            with _destination_reservation_lock(job.job_path.parent):
                _require_unique_destination_reservation(
                    job.job_path,
                    reservation,
                )
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
            if job.lifecycle in {
                FolderJobLifecycleV3.REVIEWING,
                FolderJobLifecycleV3.EXECUTING,
            } and not _promoted_result_exists(job):
                self._require_derivative_execution_ready(job)
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
                reservation = _require_destination_reservation(job)
                with _destination_reservation_lock(job.job_path.parent):
                    _require_unique_destination_reservation(
                        job.job_path,
                        reservation,
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
                reservation = build_destination_reservation(job=job)
                with _destination_reservation_lock(job.job_path.parent):
                    _require_unique_destination_reservation(
                        job.job_path,
                        reservation,
                    )
                    _require_absent_result_path(pending, label="Pending result")
                    _require_absent_result_path(final, label="Final result")
                    executing = evolve_job_v3(
                        job,
                        revision=job.revision + 1,
                        updated_at=_now(),
                        lifecycle=FolderJobLifecycleV3.EXECUTING,
                        execution_authorization=authorization,
                        destination_reservation=reservation,
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
        change_file = parse_connected_change_file_any(payload)
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
            authority = _require_direct_revision_authority(current)
            pending, _ledger = _direct_pending_and_ledger(authority)
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
            failed_authority = _clear_direct_pending(authority)
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
                revision_mutation_bindings=(
                    *current.revision_mutation_bindings,
                    build_revision_mutation_binding(
                        job=current,
                        terminal_outcome="provider_failed",
                        terminal_job_revision=current.revision + 1,
                        resulting_proposal_revision=current.proposal_revision,
                    ),
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
            authority = _require_direct_revision_authority(current)
            _pending, ledger = _direct_pending_and_ledger(authority)
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
                failed_authority = _replace_direct_revision_evidence(
                    authority,
                    ledger=failed_ledger,
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
                    revision_mutation_bindings=(
                        *current.revision_mutation_bindings,
                        build_revision_mutation_binding(
                            job=current,
                            terminal_outcome="mechanically_rejected",
                            terminal_job_revision=current.revision + 1,
                            resulting_proposal_revision=current.proposal_revision,
                        ),
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
            revised_authority = _replace_direct_revision_evidence(
                authority,
                ledger=revised_ledger,
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
                revision_mutation_bindings=(
                    *current.revision_mutation_bindings,
                    build_revision_mutation_binding(
                        job=current,
                        terminal_outcome="proposal_replaced",
                        terminal_job_revision=current.revision + 1,
                        resulting_proposal_revision=next_proposal_revision,
                    ),
                ),
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
            reviewed_plan = FolderAcceptedPlanV2(
                **prepared.accepted_plan.model_dump(
                    mode="python",
                    exclude={"evidence_schema_version"},
                ),
                evidence_schema_version="folder-evidence-ledger.v2",
            )
            _legacy_origin, initial_ledger = build_deterministic_origin_evidence(
                job_id=current.job_id,
                inventory=prepared.initial_scan.inventory,
                request=current.user_request,
                accepted_plan=reviewed_plan,
            )
            ledger = build_initial_composite_evidence(
                initial_ledger=initial_ledger,
                accepted_plan=reviewed_plan,
                contract_freeze_fingerprint=(FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT),
                model_transport="deterministic_development",
            )
            execution_origin = build_execution_origin_v2(ledger)
            planner_plan = FolderAcceptedPlan(
                source_commitment=reviewed_plan.source_commitment,
                request_fingerprint=reviewed_plan.request_fingerprint,
                request_scope=reviewed_plan.request_scope,
                evidence_fingerprint=reviewed_plan.evidence_fingerprint,
                result_folder_name=reviewed_plan.result_folder_name,
                file_mappings=tuple(
                    AcceptedFileMapping(
                        file_id=mapping.file_id,
                        original_path=mapping.original_path,
                        target_path=mapping.target_path,
                        protected=mapping.protected,
                        planner_supplied=not mapping.protected,
                    )
                    for mapping in reviewed_plan.file_mappings
                ),
                empty_directories=reviewed_plan.empty_directories,
            )
            progress = FolderPlannerProgress(
                job_id=current.job_id,
                provider_kind="deterministic",
                status="accepted",
                response_turns=initial_ledger.response_turn_count,
                evidence_calls=initial_ledger.evidence_call_count,
                evidence_calls_observed=initial_ledger.evidence_call_count,
                outbound_evidence_bytes=sum(
                    turn.input_bytes for turn in initial_ledger.observable_turns
                ),
                plan_submissions=initial_ledger.plan_submission_count,
                evidence_ledger=create_initial_evidence_ledger(
                    current.source_inventory,
                    current.user_request,
                ),
                turns=initial_ledger.observable_turns,
                compiler_failures=(),
                clarification_question=initial_ledger.clarification_question,
                clarification_answer=initial_ledger.clarification_answer,
                accepted_plan=planner_plan,
            )
            authority = GptPlannedJobAuthorityV3(
                authority_schema_version="folder-gpt-planned-job-authority.v3",
                planner_checkpoint=GptPlannerCheckpointV2.from_progress(
                    progress,
                    accepted_plan_fingerprint=ledger.accepted_plan_fingerprint,
                    usage=ledger.usage,
                ),
                evidence_ledger=ledger,
                execution_origin=execution_origin,
            )
            preview = build_folder_plan_preview(
                job_id=current.job_id,
                expected_job_revision=current.revision + 1,
                proposal_revision=0,
                proposal_basis="fresh_gpt_plan",
                inventory=prepared.initial_scan.inventory,
                reference_graph=prepared.reference_graph,
                accepted_plan=reviewed_plan,
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                authority=authority,
                candidate_plan=reviewed_plan,
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
            self._require_derivative_execution_ready(job)
            transaction_paths = FolderTransactionPaths(
                job_id=job.job_id,
                pending_root=job.pending_result_path,
                final_root=job.final_result_path,
            )
            if isinstance(job.authority, GptDerivativeJobAuthorityV3):
                prepared_derivative = self._prepare_derivative_execution(job)
                result = execute_prepared_foldweave_derivative(
                    prepared=prepared_derivative,
                    output_parent=job.output_parent,
                    job_id=job.job_id,
                    transaction_paths=transaction_paths,
                    progress_callback=progress_callback,
                )
            else:
                prepared = self._rehydrate_prepared(job)
                if job.execution_authorization is None or job.preview is None:
                    raise FoldweaveReviewServiceError(
                        "review_authority_missing",
                        "Reviewed execution lacks its exact preview or authorization.",
                    )
                result = execute_prepared_connected_change(
                    prepared=prepared,
                    output_parent=job.output_parent,
                    job_id=job.job_id,
                    execution_authorization=job.execution_authorization,
                    plan_preview=job.preview,
                    transaction_paths=transaction_paths,
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
        change_file = parse_connected_change_file_any(payload)
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

    def _prepare_derivative_execution(
        self,
        job: FolderRefactorJobV3,
    ) -> PreparedFoldweaveDerivative:
        """Reprove one exact authorized derivative without writing output."""

        authority = job.authority
        if not isinstance(authority, GptDerivativeJobAuthorityV3):
            raise FoldweaveReviewServiceError(
                "derivative_authority_mismatch",
                "Derivative execution requires one completed derivative authority.",
            )
        if (
            authority.authority_state != "completed"
            or authority.evidence_ledger is None
            or authority.execution_origin is None
            or job.candidate_plan is None
            or job.preview is None
            or job.execution_authorization is None
            or job.revision_instruction is None
        ):
            raise FoldweaveReviewServiceError(
                "derivative_execution_authority_incomplete",
                "Derivative execution lacks its complete reviewed authorization.",
            )
        self._require_fresh_derivative_child(job)
        try:
            return prepare_foldweave_derivative_execution(
                parent_change_file_path=(
                    authority.parent_binding.change_file_binding.path
                ),
                source_root=job.source_root,
                accepted_plan=job.candidate_plan,
                execution_origin=authority.execution_origin,
                evidence_ledger=authority.evidence_ledger,
                match_report=authority.parent_binding.match_report,
                parent_candidate=authority.parent_binding.parent_candidate,
                execution_authorization=job.execution_authorization,
                plan_preview=job.preview,
                revision_instruction_fingerprint=(
                    job.revision_instruction.instruction_fingerprint
                ),
            )
        except (ConnectedChangeError, ValueError) as exc:
            raise FoldweaveReviewServiceError(
                _error_code(exc, "derivative_execution_authority_invalid"),
                str(exc),
            ) from exc

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

    @staticmethod
    def _require_fresh_derivative_parent(
        parent: FolderRefactorJobV3,
    ) -> PreparedConnectedChangeApplication:
        """Reprove one immutable receiver review without mutating its job bytes."""

        if (
            parent.lifecycle is not FolderJobLifecycleV3.REVIEWING
            or not isinstance(parent.authority, CapsuleAppliedJobAuthorityV2)
            or parent.authority.match_report is None
            or parent.authority.execution_origin is None
            or parent.candidate_plan is None
            or parent.preview is None
            or parent.reference_graph is None
        ):
            raise FoldweaveReviewServiceError(
                "derivative_parent_not_reviewable",
                "A derivative child requires one complete immutable receiver review.",
            )
        try:
            current_binding = build_change_file_input_binding(
                parent.authority.change_file_binding.path
            )
            prepared = prepare_connected_change_application(
                change_file_path=parent.authority.change_file_binding.path,
                source_root=parent.source_root,
            )
        except Exception as exc:
            raise FoldweaveReviewServiceError(
                "derivative_parent_input_unreadable",
                "The receiver source or imported Change File cannot be reverified.",
            ) from exc
        current_files = tuple(
            JobLocalFileIdentityV2.from_scan(item)
            for item in prepared.initial_scan.local_file_identities
        )
        current_directories = tuple(
            JobLocalDirectoryIdentityV2.from_scan(item)
            for item in prepared.initial_scan.local_directory_identities
        )
        if (
            current_binding != parent.authority.change_file_binding
            or prepared.initial_scan.inventory != parent.source_inventory
            or current_files != parent.local_file_identities
            or current_directories != parent.local_directory_identities
            or prepared.accepted_plan != parent.candidate_plan
            or prepared.reference_graph != parent.reference_graph
            or prepared.match_report != parent.authority.match_report
            or prepared.execution_origin != parent.authority.execution_origin
        ):
            raise FoldweaveReviewServiceError(
                "derivative_parent_stale",
                "The receiver source, match, or imported Change File changed.",
            )
        return prepared

    def _require_fresh_derivative_child(
        self,
        child: FolderRefactorJobV3,
    ) -> PreparedConnectedChangeApplication:
        """Reprove current inputs against the child's immutable parent snapshot."""

        authority = child.authority
        if not isinstance(authority, GptDerivativeJobAuthorityV3):
            raise FoldweaveReviewServiceError(
                "derivative_authority_mismatch",
                "Operation requires one derivative child authority.",
            )
        binding = authority.parent_binding
        try:
            current_binding = build_change_file_input_binding(
                binding.change_file_binding.path
            )
            prepared = prepare_connected_change_application(
                change_file_path=binding.change_file_binding.path,
                source_root=binding.parent_source_root,
            )
        except Exception as exc:
            raise FoldweaveReviewServiceError(
                "derivative_parent_input_unreadable",
                "The receiver source or imported Change File cannot be reverified.",
            ) from exc
        current_files = tuple(
            JobLocalFileIdentityV2.from_scan(item)
            for item in prepared.initial_scan.local_file_identities
        )
        current_directories = tuple(
            JobLocalDirectoryIdentityV2.from_scan(item)
            for item in prepared.initial_scan.local_directory_identities
        )
        if not (
            child.source_root == binding.parent_source_root
            and child.source_inventory.source_commitment
            == binding.parent_source_commitment
            and child.source_inventory == prepared.initial_scan.inventory
            and child.local_file_identities == current_files
            and child.local_directory_identities == current_directories
        ):
            raise FoldweaveReviewServiceError(
                "derivative_child_source_mismatch",
                "The derivative child no longer targets its bound receiver source.",
            )
        if not (
            current_binding == binding.change_file_binding
            and prepared.accepted_plan == binding.parent_candidate
            and prepared.match_report == binding.match_report
            and (
                child.reference_graph is None
                or child.reference_graph == prepared.reference_graph
            )
        ):
            raise FoldweaveReviewServiceError(
                "derivative_parent_stale",
                "The receiver source, match, or imported Change File changed.",
            )
        return prepared

    def _persist_derivative_success(
        self,
        job_path: Path,
        *,
        expected: FolderRefactorJobV3,
        prepared: PreparedConnectedChangeApplication,
        turn: (
            FolderDerivativeRevisionTurnRecordV1
            | FolderHostDerivativeRevisionTurnRecordV1
        ),
        accepted_plan: FolderAcceptedPlanV2,
    ) -> FolderRefactorJobV3:
        """Persist one mechanically accepted derivative-first complete preview."""

        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.load()
            if current != expected or current.lifecycle.terminal:
                return current
            fresh = self._require_fresh_derivative_child(current)
            if fresh != prepared:
                raise FoldweaveReviewServiceError(
                    "derivative_inputs_changed",
                    "Derivative inputs changed while the provider turn was running.",
                )
            authority = current.authority
            if not isinstance(authority, GptDerivativeJobAuthorityV3):
                raise FoldweaveReviewServiceError(
                    "derivative_authority_mismatch",
                    "Derivative success targets another job authority.",
                )
            evidence_state = (
                authority.pending_host_revision.evidence_state
                if authority.pending_host_revision is not None
                else create_initial_evidence_ledger(
                    current.source_inventory,
                    current.user_request,
                )
            )
            initial_ledger = build_derivative_evidence_ledger(
                job_id=current.job_id,
                evidence_state=evidence_state,
                model_transport=authority.model_transport,
                parent_binding_fingerprint=authority.parent_binding.binding_fingerprint,
                creation_binding_fingerprint=(
                    authority.creation_binding.binding_fingerprint
                ),
                contract_freeze_fingerprint=(
                    authority.creation_binding.contract_freeze_fingerprint
                ),
                imported_change_file_fingerprint=(
                    authority.parent_binding.imported_change_file_fingerprint
                ),
                match_report_fingerprint=(
                    authority.parent_binding.match_report.match_report_fingerprint
                ),
                immediate_parent_candidate_fingerprint=(
                    authority.parent_binding.parent_candidate_fingerprint
                ),
                immediate_parent_preview_fingerprint=(
                    authority.parent_binding.parent_preview_fingerprint
                ),
                revision_instruction_fingerprint=(
                    authority.creation_binding.revision_instruction_fingerprint
                ),
                turn=turn,
                accepted_plan=accepted_plan,
            )
            ledger = build_derivative_composite_evidence(
                initial_ledger=initial_ledger,
                accepted_plan=accepted_plan,
                contract_freeze_fingerprint=(
                    authority.creation_binding.contract_freeze_fingerprint
                ),
            )
            origin = build_execution_origin_v2(
                ledger,
                imported_change_file_fingerprint=(
                    authority.parent_binding.imported_change_file_fingerprint
                ),
                match_report_fingerprint=(
                    authority.parent_binding.match_report.match_report_fingerprint
                ),
            )
            completed_authority = authority.model_copy(
                update={
                    "authority_state": "completed",
                    "pending_direct_revision": None,
                    "pending_host_revision": None,
                    "evidence_ledger": ledger,
                    "execution_origin": origin,
                }
            )
            preview = build_folder_plan_preview(
                job_id=current.job_id,
                expected_job_revision=current.revision + 1,
                proposal_revision=1,
                proposal_basis="gpt_derivative",
                inventory=current.source_inventory,
                reference_graph=fresh.reference_graph,
                accepted_plan=accepted_plan,
                imported_change_file_fingerprint=(
                    authority.parent_binding.imported_change_file_fingerprint
                ),
                match_report_fingerprint=(
                    authority.parent_binding.match_report.match_report_fingerprint
                ),
                immediate_parent_candidate_fingerprint=(
                    authority.parent_binding.parent_candidate_fingerprint
                ),
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                proposal_revision=1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.REVIEWING,
                authority=completed_authority,
                candidate_plan=accepted_plan,
                reference_graph=fresh.reference_graph,
                preview=preview,
            )
            return writer.save(successor, expected_current=current)

    @staticmethod
    def _persist_derivative_failure(
        job_path: Path,
        *,
        expected: FolderRefactorJobV3,
        code: str,
        detail: str,
        host_turn: FolderHostDerivativeRevisionTurnRecordV1 | None = None,
        prepared: PreparedFoldweaveDerivative | None = None,
    ) -> FolderRefactorJobV3:
        """Preserve the imported parent review after one failed child attempt."""

        safe_detail = detail.strip()[:2_000] or (
            "The derivative provider did not return a usable sparse revision."
        )
        store = FolderRefactorJobV3Store(job_path)
        with store.writer() as writer:
            current = writer.load()
            if current != expected or current.lifecycle.terminal:
                return current
            authority = current.authority
            instruction = current.revision_instruction
            if (
                not isinstance(authority, GptDerivativeJobAuthorityV3)
                or authority.authority_state != "awaiting_model_response"
                or instruction is None
            ):
                raise FoldweaveReviewServiceError(
                    "derivative_failure_authority_missing",
                    "Derivative failure lacks its immutable pending authority.",
                )
            failure = FolderRevisionFailureV1(
                code=code,
                detail=safe_detail,
                attempted_instruction_fingerprint=(instruction.instruction_fingerprint),
            )
            failed_authority = authority.model_copy(
                update={
                    "authority_state": "failed",
                    "pending_direct_revision": None,
                    "pending_host_revision": None,
                    "failure": failure,
                    "failed_host_revision": host_turn,
                }
            )
            if prepared is None:
                raise FoldweaveReviewServiceError(
                    "derivative_failure_preview_unavailable",
                    "A retryable derivative failure requires its verified parent "
                    "preview.",
                )
            parent = authority.parent_binding
            preview = build_folder_plan_preview(
                job_id=current.job_id,
                expected_job_revision=current.revision + 1,
                proposal_revision=0,
                proposal_basis="imported_change_file",
                inventory=current.source_inventory,
                reference_graph=prepared.reference_graph,
                accepted_plan=parent.parent_candidate,
                imported_change_file_fingerprint=(
                    parent.imported_change_file_fingerprint
                ),
                match_report_fingerprint=(parent.match_report.match_report_fingerprint),
            )
            successor = evolve_job_v3(
                current,
                revision=current.revision + 1,
                updated_at=_now(),
                lifecycle=FolderJobLifecycleV3.REVISION_FAILED,
                authority=failed_authority,
                candidate_plan=parent.parent_candidate,
                reference_graph=prepared.reference_graph,
                preview=preview,
                revision_failure=failure,
            )
            return writer.save(successor, expected_current=current)

    def _require_derivative_execution_ready(
        self,
        job: FolderRefactorJobV3,
    ) -> None:
        """Reprove derivative inputs before authorization or product output."""

        if not isinstance(job.authority, GptDerivativeJobAuthorityV3):
            return
        self._require_fresh_derivative_child(job)
        if (
            job.authority.authority_state != "completed"
            or job.authority.evidence_ledger is None
            or job.authority.execution_origin is None
            or job.candidate_plan is None
            or job.preview is None
            or job.revision_instruction is None
        ):
            raise FoldweaveReviewServiceError(
                "derivative_execution_authority_incomplete",
                "Derivative execution requires one complete reviewed child authority.",
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
    public_job_capability: FolderPublicJobCapabilityV1 | None = None,
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
        operation_idempotency=seed.operation_idempotency,
        public_job_capability=public_job_capability,
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


def _completed_revision_retry_or_none(
    job: FolderRefactorJobV3,
    *,
    expected_revision: int,
    instruction: FolderRevisionInstructionV1,
) -> FolderRefactorJobV3 | None:
    """Return an exact historical retry without constructing a provider."""

    matching = tuple(
        binding
        for binding in job.revision_mutation_bindings
        if binding.idempotency_key_sha256 == instruction.idempotency_key_sha256
    )
    if not matching:
        return None
    if len(matching) != 1:
        raise FolderJobV3IdempotencyConflict(
            "Duplicate direct revision bindings share one retry key."
        )
    binding = matching[0]
    if not (
        binding.job_id == job.job_id
        and binding.base_job_revision == expected_revision
        and binding.base_candidate_fingerprint == instruction.base_candidate_fingerprint
        and binding.base_preview_fingerprint == instruction.base_preview_fingerprint
        and binding.revision_instruction_fingerprint
        == instruction.instruction_fingerprint
    ):
        raise FolderJobV3IdempotencyConflict(
            "Revision retry key is bound to another exact request."
        )
    return job


def _require_v3_planning_authority(
    job: FolderRefactorJobV3,
) -> GptPlannedJobAuthorityV3:
    if not isinstance(job.authority, GptPlannedJobAuthorityV3):
        raise FoldweaveReviewServiceError(
            "planner_authority_mismatch",
            "Operation requires Foldweave v3 planning authority.",
        )
    return job.authority


DirectRevisionAuthority = GptPlannedJobAuthorityV3 | GptDerivativeJobAuthorityV3


def _require_completed_direct_derivative_authority(
    job: FolderRefactorJobV3,
) -> GptDerivativeJobAuthorityV3:
    authority = job.authority
    if not (
        isinstance(authority, GptDerivativeJobAuthorityV3)
        and authority.authority_state == "completed"
        and authority.model_transport
        in {"responses_api", "recorded_replay", "deterministic_development"}
    ):
        raise FoldweaveReviewServiceError(
            "derivative_revision_not_ready",
            "Direct derivative follow-up requires one completed direct child review.",
        )
    return authority


def _require_derivative_composite_ledger(
    authority: GptDerivativeJobAuthorityV3,
) -> FolderEvidenceLedgerV2:
    if authority.evidence_ledger is None:
        raise FoldweaveReviewServiceError(
            "planner_evidence_missing",
            "Derivative review lacks composite planner evidence.",
        )
    return authority.evidence_ledger


def _require_direct_revision_authority(
    job: FolderRefactorJobV3,
) -> DirectRevisionAuthority:
    authority = job.authority
    if isinstance(authority, GptPlannedJobAuthorityV3):
        return authority
    if isinstance(authority, GptDerivativeJobAuthorityV3) and (
        authority.authority_state == "completed"
        and authority.model_transport
        in {"responses_api", "recorded_replay", "deterministic_development"}
    ):
        return authority
    raise FoldweaveReviewServiceError(
        "planner_authority_mismatch",
        "Operation requires direct Foldweave planning authority.",
    )


def _direct_pending_and_ledger(
    authority: DirectRevisionAuthority,
) -> tuple[FolderPlannerRevisionTurnInputV1, FolderEvidenceLedgerV2]:
    if isinstance(authority, GptPlannedJobAuthorityV3):
        pending = authority.pending_revision_turn
        ledger = authority.evidence_ledger
    else:
        pending = authority.pending_direct_followup_revision
        ledger = authority.evidence_ledger
    if pending is None or ledger is None:
        raise FoldweaveReviewServiceError(
            "revision_authority_missing",
            "Direct revision lacks its reserved turn or evidence authority.",
        )
    return pending, ledger


def _clear_direct_pending(
    authority: DirectRevisionAuthority,
) -> DirectRevisionAuthority:
    field = (
        "pending_revision_turn"
        if isinstance(authority, GptPlannedJobAuthorityV3)
        else "pending_direct_followup_revision"
    )
    return authority.model_copy(update={field: None})


def _replace_direct_revision_evidence(
    authority: DirectRevisionAuthority,
    *,
    ledger: FolderEvidenceLedgerV2,
) -> DirectRevisionAuthority:
    if isinstance(authority, GptDerivativeJobAuthorityV3):
        origin = build_execution_origin_v2(
            ledger,
            imported_change_file_fingerprint=(
                authority.parent_binding.imported_change_file_fingerprint
            ),
            match_report_fingerprint=(
                authority.parent_binding.match_report.match_report_fingerprint
            ),
        )
        return authority.model_copy(
            update={
                "evidence_ledger": ledger,
                "execution_origin": origin,
                "pending_direct_followup_revision": None,
            }
        )
    return authority.model_copy(
        update={
            "evidence_ledger": ledger,
            "execution_origin": build_execution_origin_v2(ledger),
            "pending_revision_turn": None,
        }
    )


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


def _kept_review_target(job: FolderRefactorJobV3) -> FolderRefactorJobV3:
    """Return the immutable receiver parent after dismissing first-child failure."""

    authority = job.authority
    if (
        isinstance(authority, GptDerivativeJobAuthorityV3)
        and authority.authority_state == "failed"
    ):
        return FolderRefactorJobV3Store(
            authority.parent_binding.parent_job_path
        ).inspect()
    return job


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
        or not isinstance(
            job.authority,
            (GptPlannedJobAuthorityV3, GptDerivativeJobAuthorityV3),
        )
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
    evidence_records = getattr(ledger.initial_ledger, "evidence_records", ())
    ledger_evidence = {
        "initial_inventory",
        *(record.fingerprint for record in evidence_records),
    }
    return compile_sparse_revision_from_base(
        inventory=job.source_inventory,
        request=job.user_request,
        reference_graph=_require_reference_graph(job),
        base_candidate=_require_candidate(job),
        revision=turn.response.revision,
        evidence_fingerprint=ledger.evidence_fingerprint,
        known_evidence_ids=ledger_evidence,
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
            previous.immediate_parent_candidate_fingerprint
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


def _require_destination_reservation(
    job: FolderRefactorJobV3,
) -> FolderDestinationReservationV1:
    reservation = job.destination_reservation
    if reservation is None:
        raise FoldweaveReviewServiceError(
            "destination_reservation_missing",
            "Authorized execution lacks its durable destination reservation.",
        )
    return reservation


def _promoted_result_exists(job: FolderRefactorJobV3) -> bool:
    """Return whether an executing job already promoted its final result."""

    return (
        job.lifecycle is FolderJobLifecycleV3.EXECUTING
        and job.final_result_path is not None
        and os.path.lexists(job.final_result_path)
    )


@contextmanager
def _derivative_parent_snapshot_lock(parent_job_path: Path) -> Iterator[None]:
    """Hold the parent's ordinary writer lock while allocating one child."""

    yield from _bounded_durable_lock(
        parent_job_path.resolve(strict=False),
        busy_code="derivative_parent_busy",
        busy_message="Receiver parent authority is busy; retry the exact request.",
    )


@contextmanager
def _derivative_child_creation_lock(jobs_directory: Path) -> Iterator[None]:
    """Serialize semantic child allocation across all jobs in one state root."""

    yield from _bounded_durable_lock(
        jobs_directory.resolve(strict=False) / ".foldweave-derivative-children",
        busy_code="derivative_child_creation_busy",
        busy_message="Derivative child authority is busy; retry the exact request.",
    )


@contextmanager
def _derivative_provider_call_lock(job_path: Path) -> Iterator[None]:
    """Prevent duplicate provider calls while keeping the v3 writer unlocked."""

    yield from _bounded_durable_lock(
        job_path.resolve(strict=False).with_name(f".{job_path.name}.provider-call"),
        busy_code="derivative_provider_busy",
        busy_message="Derivative provider authority is busy; retry this child.",
    )


def _bounded_durable_lock(
    target: Path,
    *,
    busy_code: str,
    busy_message: str,
) -> Iterator[None]:
    """Acquire one non-reentrant process lock within a bounded wait."""

    deadline = time.monotonic() + 5.0
    lock: DurableJobFileLock | None = None
    while lock is None:
        candidate = DurableJobFileLock(target)
        try:
            candidate.__enter__()
        except DurableJobLockError as exc:
            if time.monotonic() >= deadline:
                raise FoldweaveReviewServiceError(
                    busy_code,
                    busy_message,
                ) from exc
            time.sleep(0.01)
        else:
            lock = candidate
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


def _derivative_child_retry_or_none(
    jobs_directory: Path,
    *,
    creation: FolderDerivativeCreationBindingV1,
) -> FolderRefactorJobV3 | None:
    """Return one exact child retry or reject conflicting key reuse."""

    matching: FolderRefactorJobV3 | None = None
    for candidate_path in sorted(
        jobs_directory.glob("*.json"),
        key=lambda item: item.name,
    ):
        try:
            record = load_folder_job_record_v3(candidate_path)
        except FolderJobV3LoadError as exc:
            raise FoldweaveReviewServiceError(
                "derivative_job_authority_unreadable",
                "A durable job in the shared state root cannot be validated.",
            ) from exc
        if not isinstance(record, FolderRefactorJobV3) or not isinstance(
            record.authority, GptDerivativeJobAuthorityV3
        ):
            continue
        existing = record.authority.creation_binding
        if existing.idempotency_key_sha256 != creation.idempotency_key_sha256:
            continue
        if existing.request_fingerprint != creation.request_fingerprint:
            raise FolderJobV3IdempotencyConflict(
                "Derivative child retry key is bound to another exact request."
            )
        if matching is not None:
            raise FolderJobV3IdempotencyConflict(
                "Derivative child retry key is bound to multiple durable jobs."
            )
        matching = record
    return matching


def _derivative_child_retry_by_inputs_or_none(
    jobs_directory: Path,
    *,
    parent_job_path: Path,
    output_parent: Path,
    instruction: str,
    idempotency_key_sha256: str,
    model_transport: str,
    channel: ReviewChannel,
) -> FolderRefactorJobV3 | None:
    """Resolve an exact creation retry even after the parent advances."""

    matching: FolderRefactorJobV3 | None = None
    parent_path = parent_job_path.resolve(strict=False)
    resolved_output = output_parent.resolve(strict=False)
    for candidate_path in sorted(
        jobs_directory.resolve(strict=False).glob("*.json"),
        key=lambda item: item.name,
    ):
        try:
            record = load_folder_job_record_v3(candidate_path)
        except FolderJobV3LoadError as exc:
            raise FoldweaveReviewServiceError(
                "derivative_job_authority_unreadable",
                "A durable job in the shared state root cannot be validated.",
            ) from exc
        if not isinstance(record, FolderRefactorJobV3) or not isinstance(
            record.authority,
            GptDerivativeJobAuthorityV3,
        ):
            continue
        creation = record.authority.creation_binding
        if creation.idempotency_key_sha256 != idempotency_key_sha256:
            continue
        exact = (
            record.authority.parent_binding.parent_job_path == parent_path
            and creation.output_parent == resolved_output
            and creation.model_transport == model_transport
            and creation.channel == channel
            and record.revision_instruction is not None
            and record.revision_instruction.instruction == instruction
        )
        if not exact:
            raise FolderJobV3IdempotencyConflict(
                "Derivative child retry key is permanently bound to another "
                "exact request."
            )
        if matching is not None:
            raise FolderJobV3IdempotencyConflict(
                "Derivative child retry key is bound to multiple durable jobs."
            )
        matching = record
    return matching


def _derivative_turn_usage(
    provider: FolderPlanRevisionProvider,
) -> FolderPlannerUsage | None:
    """Return the exact first-turn direct usage without inventing API metadata."""

    if provider.provider_kind != "live":
        if provider.usage:
            raise FoldweaveReviewServiceError(
                "derivative_usage_origin_invalid",
                "Model-free derivative planning cannot report direct API usage.",
            )
        return None
    matches = tuple(item for item in provider.usage if item.response_turn == 1)
    if len(matches) != 1 or len(provider.usage) != 1:
        raise FoldweaveReviewServiceError(
            "derivative_usage_missing",
            "Direct derivative planning lacks one exact observable usage record.",
        )
    return matches[0]


def _host_derivative_submission_retry_or_none(
    job: FolderRefactorJobV3,
    *,
    call_id: str,
    revision: FolderHostPlanRevisionV1,
) -> FolderRefactorJobV3 | None:
    """Resolve a durable hosted derivative submission retry or conflict."""

    authority = job.authority
    assert isinstance(authority, GptDerivativeJobAuthorityV3)
    raw_records: tuple[object, ...] = ()
    if authority.evidence_ledger is not None:
        raw_records = tuple(
            record
            for segment in authority.evidence_ledger.segments
            for record in segment.observable_records
        )
    if authority.failed_host_revision is not None:
        raw_records = (
            *raw_records,
            authority.failed_host_revision.model_dump(mode="json"),
        )
    matching = tuple(
        record
        for record in raw_records
        if isinstance(record, dict)
        and record.get("schema_version")
        == "folder-host-derivative-revision-turn-record.v1"
        and record.get("call_id") == call_id
    )
    if not matching:
        return None
    expected = revision.model_dump(mode="json")
    if len(matching) != 1 or matching[0].get("revision") != expected:
        raise FolderJobV3IdempotencyConflict(
            "Hosted derivative call ID is permanently bound to another sparse revision."
        )
    return job


def _compile_host_derivative_first_revision(
    job: FolderRefactorJobV3,
    *,
    prepared: PreparedConnectedChangeApplication,
    revision: FolderHostPlanRevisionV1,
) -> FolderAcceptedPlanV2:
    """Compile the first hosted sparse turn against the receiver parent."""

    authority = job.authority
    if not isinstance(authority, GptDerivativeJobAuthorityV3):
        raise FoldweaveReviewServiceError(
            "derivative_authority_mismatch",
            "Hosted derivative compilation requires derivative authority.",
        )
    pending = authority.pending_host_revision
    if pending is None:
        raise FoldweaveReviewServiceError(
            "derivative_turn_missing",
            "Hosted derivative compilation lacks its bounded evidence state.",
        )
    known_evidence_ids = {
        "initial_inventory",
        *(record.fingerprint for record in pending.evidence_state.records),
    }
    planner_revision = FolderPlanRevisionV1(
        base_candidate_fingerprint=revision.base_candidate_fingerprint,
        replacement_result_folder_name=revision.replacement_result_folder_name,
        entries=tuple(
            FolderPlanRevisionEntryV1(
                file_id=entry.file_id,
                replacement_target_path=entry.replacement_target_path,
                rationale=entry.rationale,
                evidence_ids=entry.evidence_ids,
            )
            for entry in revision.entries
        ),
    )
    return compile_sparse_revision_from_base(
        inventory=job.source_inventory,
        request=job.user_request,
        reference_graph=prepared.reference_graph,
        base_candidate=authority.parent_binding.parent_candidate,
        revision=planner_revision,
        evidence_fingerprint=pending.evidence_fingerprint,
        known_evidence_ids=known_evidence_ids,
    )


def _compile_derivative_first_revision(
    job: FolderRefactorJobV3,
    *,
    prepared: PreparedConnectedChangeApplication,
    turn: FolderDerivativeRevisionTurnRecordV1,
) -> FolderAcceptedPlanV2:
    """Compile one derivative-first sparse turn through the shared compiler."""

    authority = job.authority
    if not isinstance(authority, GptDerivativeJobAuthorityV3):
        raise FoldweaveReviewServiceError(
            "derivative_authority_mismatch",
            "Sparse derivative compilation requires derivative authority.",
        )
    evidence_state = create_initial_evidence_ledger(
        job.source_inventory,
        job.user_request,
    )
    if (
        evidence_state.evidence_fingerprint
        != authority.creation_binding.evidence_fingerprint
    ):
        raise FoldweaveReviewServiceError(
            "derivative_evidence_changed",
            "Receiver-local derivative evidence differs from child creation.",
        )
    known_evidence_ids = {
        "initial_inventory",
        *(record.fingerprint for record in evidence_state.records),
    }
    return compile_sparse_revision_from_base(
        inventory=job.source_inventory,
        request=job.user_request,
        reference_graph=prepared.reference_graph,
        base_candidate=authority.parent_binding.parent_candidate,
        revision=turn.response.revision,
        evidence_fingerprint=evidence_state.evidence_fingerprint,
        known_evidence_ids=known_evidence_ids,
    )


@contextmanager
def _destination_reservation_lock(jobs_directory: Path) -> Iterator[None]:
    """Serialize cross-job reservation decisions, never product execution."""

    lock_target = (
        jobs_directory.resolve(strict=False) / ".foldweave-destination-reservations"
    )
    deadline = time.monotonic() + 5.0
    lock: DurableJobFileLock | None = None
    while lock is None:
        candidate = DurableJobFileLock(lock_target)
        try:
            candidate.__enter__()
        except DurableJobLockError as exc:
            if time.monotonic() >= deadline:
                raise FoldweaveReviewServiceError(
                    "destination_reservation_busy",
                    "Destination authority is busy; retry the identical request.",
                ) from exc
            time.sleep(0.01)
        else:
            lock = candidate
    try:
        yield
    finally:
        lock.__exit__(None, None, None)


def _require_unique_destination_reservation(
    current_job_path: Path,
    reservation: FolderDestinationReservationV1,
) -> None:
    """Fail closed if another active durable job owns this exact destination."""

    jobs_directory = current_job_path.resolve(strict=False).parent
    for candidate_path in sorted(
        jobs_directory.glob("*.json"),
        key=lambda item: item.name,
    ):
        if candidate_path.resolve(strict=False) == current_job_path.resolve(
            strict=False
        ):
            continue
        try:
            record = load_folder_job_record_v3(candidate_path)
        except FolderJobV3LoadError as exc:
            raise FoldweaveReviewServiceError(
                "destination_authority_unreadable",
                "A durable job in the shared state root cannot be validated.",
            ) from exc
        if not isinstance(record, FolderRefactorJobV3):
            continue
        other = record.destination_reservation
        if (
            other is not None
            and record.lifecycle
            in {
                FolderJobLifecycleV3.EXECUTING,
                FolderJobLifecycleV3.VERIFIED,
            }
            and other.final_result_path == reservation.final_result_path
        ):
            raise FoldweaveReviewServiceError(
                "destination_already_reserved",
                "Another durable job already owns the reviewed result destination.",
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
