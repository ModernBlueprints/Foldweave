"""Restart-safe planner continuation through the sole v2 job authority."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    convert_planner_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.evidence import (
    build_planner_origin_evidence,
)
from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
    ConnectedChangeJobServiceError,
    FolderIdempotencyScope,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    FolderJobLifecycleV2,
    FolderJobV2FinalizedError,
    FolderOperationIdempotencyBindingV2,
    FolderRefactorJobV2,
    FolderRefactorJobV2Store,
    FolderRefactorJobV2Writer,
    GptPlannedJobAuthorityV2,
    GptPlannerCheckpointV2,
    bind_operation_idempotency,
    evolve_job_v2,
)
from name_atlas.folder_refactor.inventory import FolderScan
from name_atlas.folder_refactor.planner_contracts import FolderPlannerProgress
from name_atlas.folder_refactor.planner_evidence import LocalFolderEvidenceService
from name_atlas.folder_refactor.planner_orchestrator import (
    PlannerOrchestrator,
    create_planner_progress,
)
from name_atlas.folder_refactor.planner_provider import PlannerProvider
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.folder_refactor.transaction import (
    FolderTransactionProgress,
    scan_folder_with_references,
)


@dataclass(slots=True)
class ConnectedPlannerCheckpointWriter:
    """Persist every planner transition as the same revisioned v2 job."""

    writer: FolderRefactorJobV2Writer
    usage: tuple[FolderPlannerUsage, ...] = ()
    usage_source: Callable[[], tuple[FolderPlannerUsage, ...]] | None = None
    operation_idempotency: tuple[FolderOperationIdempotencyBindingV2, ...] | None = None
    latest_job: FolderRefactorJobV2 | None = field(default=None, init=False)

    def current_usage(self) -> tuple[FolderPlannerUsage, ...]:
        """Merge the persisted prefix with the provider's observed prefix."""

        observed = self.usage_source() if self.usage_source is not None else ()
        if not observed:
            return self.usage
        if observed[: len(self.usage)] == self.usage:
            return observed
        if observed[0].response_turn == len(self.usage) + 1:
            combined = self.usage + observed
            if tuple(item.response_turn for item in combined) == tuple(
                range(1, len(combined) + 1)
            ):
                return combined
        raise ConnectedChangeJobServiceError(
            "planner_usage_prefix_mismatch",
            "Provider usage differs from the durable append-only prefix.",
        )

    def __call__(self, progress: FolderPlannerProgress) -> None:
        """Convert only accepted output; retain complete progress at every step."""

        current = self.writer.load()
        usage = self.current_usage()
        if not isinstance(current.authority, GptPlannedJobAuthorityV2):
            raise ConnectedChangeJobServiceError(
                "planner_authority_mismatch",
                "Planner continuation requires GPT-planned job authority.",
            )

        accepted_plan = None
        evidence_ledger = None
        execution_origin = None
        accepted_plan_fingerprint = None
        if progress.status == "accepted":
            if progress.accepted_plan is None:
                raise ConnectedChangeJobServiceError(
                    "accepted_planner_plan_missing",
                    "Accepted planner progress lacks its complete map.",
                )
            accepted_plan = convert_planner_accepted_plan(
                inventory=current.source_inventory,
                request=current.user_request,
                plan=progress.accepted_plan,
            )
            accepted_plan_fingerprint = canonical_sha256(accepted_plan)
            execution_origin, evidence_ledger = build_planner_origin_evidence(
                progress=progress,
                accepted_plan=accepted_plan,
                usage=usage,
            )

        checkpoint = GptPlannerCheckpointV2.from_progress(
            progress,
            accepted_plan_fingerprint=accepted_plan_fingerprint,
            usage=usage,
        )
        authority = GptPlannedJobAuthorityV2(
            planner_checkpoint=checkpoint,
            evidence_ledger=evidence_ledger,
            execution_origin=execution_origin,
        )
        lifecycle = {
            "planning": FolderJobLifecycleV2.PLANNING,
            "awaiting_clarification": FolderJobLifecycleV2.AWAITING_CLARIFICATION,
            "accepted": FolderJobLifecycleV2.EXECUTING,
            "blocked": FolderJobLifecycleV2.BLOCKED,
        }[progress.status]
        candidate = evolve_job_v2(
            current,
            authority=authority,
            operation_idempotency=(
                current.operation_idempotency
                if self.operation_idempotency is None
                else self.operation_idempotency
            ),
            accepted_plan=accepted_plan,
            lifecycle=lifecycle,
            blocker_code=checkpoint.blocker_code,
            blocker_message=checkpoint.blocker_message,
        )
        self.latest_job = self.writer.save(candidate, expected_current=current)


class ConnectedOriginPlanningService:
    """Run one provider through persisted v2 progress, then shared execution."""

    def __init__(
        self,
        *,
        job_service: ConnectedChangeJobService | None = None,
    ) -> None:
        self._jobs = job_service or ConnectedChangeJobService()

    def create(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        request: str,
        idempotency_key: str,
        provider_kind: Literal["deterministic", "live", "recorded_replay"],
        idempotency_scope: FolderIdempotencyScope = "jobs_directory",
    ) -> FolderRefactorJobV2:
        """Persist one resumable planner job without consuming a provider turn."""

        scan, _reference_graph = scan_folder_with_references(source_root)
        job_id = uuid.uuid4().hex
        initial_progress = create_planner_progress(
            scan.inventory,
            request,
            job_id=job_id,
            provider_kind=provider_kind,
        )
        return self._jobs.create_planned_origin_job(
            source_root=scan.source_root,
            output_parent=output_parent,
            job_path=job_path,
            request=request,
            idempotency_key=idempotency_key,
            scan=scan,
            planner_progress=initial_progress,
            idempotency_scope=idempotency_scope,
        )

    async def start(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        request: str,
        idempotency_key: str,
        provider: PlannerProvider,
        progress_callback: FolderTransactionProgress | None = None,
        usage: tuple[FolderPlannerUsage, ...] = (),
        idempotency_scope: FolderIdempotencyScope = "jobs_directory",
    ) -> FolderRefactorJobV2:
        """Create or reuse one job, then continue its exact planner state."""

        job = self.create(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            request=request,
            idempotency_key=idempotency_key,
            provider_kind=provider.provider_kind,
            idempotency_scope=idempotency_scope,
        )
        return await self.resume(
            job.job_path,
            provider=provider,
            progress_callback=progress_callback,
            usage=usage,
        )

    async def resume(
        self,
        job_path: Path,
        *,
        provider: PlannerProvider,
        progress_callback: FolderTransactionProgress | None = None,
        usage: tuple[FolderPlannerUsage, ...] = (),
    ) -> FolderRefactorJobV2:
        """Resume planning or shared deterministic execution without duplication."""

        job = self._jobs.status(job_path)
        if job.lifecycle.terminal:
            return job
        if job.lifecycle is FolderJobLifecycleV2.EXECUTING:
            return self._jobs.run_or_resume(
                job_path,
                progress_callback=progress_callback,
            )
        if job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
            return job
        job = await self._continue_planner(
            job_path,
            provider=provider,
            answer=None,
            expected_job_id=None,
            expected_revision=None,
            expected_question_fingerprint=None,
            usage=usage,
        )
        if job.lifecycle is FolderJobLifecycleV2.EXECUTING:
            return self._jobs.run_or_resume(
                job_path,
                progress_callback=progress_callback,
            )
        return job

    async def answer(
        self,
        job_path: Path,
        *,
        continuation_token: str,
        answer: str,
        provider: PlannerProvider,
        expected_revision: int | None = None,
        expected_question_fingerprint: str | None = None,
        progress_callback: FolderTransactionProgress | None = None,
        usage: tuple[FolderPlannerUsage, ...] = (),
    ) -> FolderRefactorJobV2:
        """Persist the sole answer before consuming another provider turn."""

        job = await self._continue_planner(
            job_path,
            provider=provider,
            answer=answer,
            expected_job_id=continuation_token,
            expected_revision=expected_revision,
            expected_question_fingerprint=expected_question_fingerprint,
            usage=usage,
        )
        if job.lifecycle is FolderJobLifecycleV2.EXECUTING:
            return self._jobs.run_or_resume(
                job_path,
                progress_callback=progress_callback,
            )
        return job

    def persist_clarification_answer(
        self,
        job_path: Path,
        *,
        answer: str,
        idempotency_key: str,
        expected_revision: int,
        expected_question_fingerprint: str,
    ) -> FolderRefactorJobV2:
        """Persist one exactly bound answer without constructing a provider."""

        normalized = answer.strip()
        if not normalized or len(answer) > 4_000 or "\x00" in answer:
            raise ConnectedChangeJobServiceError(
                "clarification_answer_invalid",
                "Clarification answer must be nonblank bounded plain text.",
            )
        store = FolderRefactorJobV2Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if not isinstance(job.authority, GptPlannedJobAuthorityV2):
                raise ConnectedChangeJobServiceError(
                    "planner_authority_mismatch",
                    "Clarification requires GPT-planned job authority.",
                )
            progress = job.authority.planner_checkpoint.progress
            if progress is None or progress.clarification_question is None:
                raise ConnectedChangeJobServiceError(
                    "clarification_not_active",
                    "The durable job has no persisted clarification question.",
                )
            observed_question_fingerprint = clarification_question_fingerprint(
                job_id=job.job_id,
                question=progress.clarification_question,
            )
            if observed_question_fingerprint != expected_question_fingerprint:
                raise ConnectedChangeJobServiceError(
                    "clarification_question_mismatch",
                    "The clarification answer targets another exact question.",
                )
            operation_idempotency = bind_operation_idempotency(
                job,
                operation="answer_clarification",
                idempotency_key=idempotency_key,
                request={
                    "job_handle": job.job_id,
                    "expected_revision": expected_revision,
                    "question_fingerprint": expected_question_fingerprint,
                    "answer": answer,
                },
            )
            if progress.clarification_answer is not None:
                if progress.clarification_answer == answer:
                    return job
                raise ConnectedChangeJobServiceError(
                    "clarification_answer_conflict",
                    "A different clarification answer is already durable.",
                )
            if job.revision != expected_revision:
                raise ConnectedChangeJobServiceError(
                    "clarification_revision_mismatch",
                    "The clarification answer targets another durable revision.",
                )
            if job.lifecycle is not FolderJobLifecycleV2.AWAITING_CLARIFICATION:
                raise ConnectedChangeJobServiceError(
                    "clarification_not_active",
                    "The durable job is not waiting for a clarification answer.",
                )
            answered_progress = FolderPlannerProgress.model_validate(
                {
                    **progress.model_dump(mode="python"),
                    "status": "planning",
                    "clarification_answer": answer,
                }
            )
            checkpoint = ConnectedPlannerCheckpointWriter(
                writer,
                usage=job.authority.planner_checkpoint.usage,
                operation_idempotency=operation_idempotency,
            )
            checkpoint(answered_progress)
            if checkpoint.latest_job is None:
                raise ConnectedChangeJobServiceError(
                    "planner_checkpoint_missing",
                    "Clarification answer produced no durable checkpoint.",
                )
            return checkpoint.latest_job

    async def _continue_planner(
        self,
        job_path: Path,
        *,
        provider: PlannerProvider,
        answer: str | None,
        expected_job_id: str | None,
        expected_revision: int | None,
        expected_question_fingerprint: str | None,
        usage: tuple[FolderPlannerUsage, ...],
    ) -> FolderRefactorJobV2:
        store = FolderRefactorJobV2Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if expected_job_id is not None and job.job_id != expected_job_id:
                raise ConnectedChangeJobServiceError(
                    "clarification_token_mismatch",
                    "The clarification answer targets another durable job.",
                )
            if expected_revision is not None and job.revision != expected_revision:
                raise ConnectedChangeJobServiceError(
                    "clarification_revision_mismatch",
                    "The clarification answer targets another durable revision.",
                )
            if job.lifecycle.terminal:
                if job.lifecycle is FolderJobLifecycleV2.STALE:
                    return job
                raise ConnectedChangeJobServiceError(
                    "clarification_not_active",
                    "The durable job is no longer waiting for an answer.",
                )
            if not isinstance(job.authority, GptPlannedJobAuthorityV2):
                raise ConnectedChangeJobServiceError(
                    "planner_authority_mismatch",
                    "Planner continuation requires GPT-planned job authority.",
                )
            progress = job.authority.planner_checkpoint.progress
            persisted_usage = job.authority.planner_checkpoint.usage
            if progress is None:
                raise ConnectedChangeJobServiceError(
                    "planner_progress_missing",
                    "This compatibility job has no resumable planner progress.",
                )
            if expected_question_fingerprint is not None:
                question = progress.clarification_question
                if (
                    question is None
                    or clarification_question_fingerprint(
                        job_id=job.job_id,
                        question=question,
                    )
                    != expected_question_fingerprint
                ):
                    raise ConnectedChangeJobServiceError(
                        "clarification_question_mismatch",
                        "The clarification answer targets another exact question.",
                    )
            if progress.provider_kind != provider.provider_kind:
                raise ConnectedChangeJobServiceError(
                    "planner_provider_origin_mismatch",
                    "The provider origin differs from persisted planner authority.",
                )
            if answer is None:
                if job.lifecycle is not FolderJobLifecycleV2.PLANNING:
                    return job
            elif job.lifecycle is not FolderJobLifecycleV2.AWAITING_CLARIFICATION:
                raise ConnectedChangeJobServiceError(
                    "clarification_not_active",
                    "The durable job is not waiting for a clarification answer.",
                )

            scan, reference_graph = scan_folder_with_references(job.source_root)
            refreshed = writer.rehydrate()
            if refreshed.lifecycle.terminal:
                return refreshed
            _require_same_job_source(refreshed, scan)
            base_usage = usage or persisted_usage
            checkpoint = ConnectedPlannerCheckpointWriter(
                writer,
                usage=base_usage,
                usage_source=lambda: getattr(provider, "usage", ()),
            )
            orchestrator = PlannerOrchestrator(
                job_id=refreshed.job_id,
                scan=scan,
                request=refreshed.user_request,
                provider=provider,
                evidence_service=LocalFolderEvidenceService(
                    scan,
                    reference_graph=reference_graph,
                ),
                reference_graph=reference_graph,
                checkpoint=checkpoint,
            )
            try:
                if answer is None:
                    await orchestrator.run(progress)
                else:
                    await orchestrator.answer_clarification(progress, answer)
            except FolderJobV2FinalizedError:
                persisted = writer.load()
                if persisted.lifecycle is FolderJobLifecycleV2.STALE:
                    return persisted
                raise
            if checkpoint.latest_job is None:
                raise ConnectedChangeJobServiceError(
                    "planner_checkpoint_missing",
                    "Planner continuation produced no durable checkpoint.",
                )
            return checkpoint.latest_job


def _require_same_job_source(job: FolderRefactorJobV2, scan: FolderScan) -> None:
    scan_files = tuple(
        (
            item.relative_path,
            item.device,
            item.inode,
            item.size,
            item.modified_ns,
        )
        for item in scan.local_file_identities
    )
    job_files = tuple(
        (
            item.relative_path,
            item.device,
            item.inode,
            item.size,
            item.modified_ns,
        )
        for item in job.local_file_identities
    )
    scan_directories = tuple(
        (item.relative_path, item.device, item.inode, item.modified_ns)
        for item in scan.local_directory_identities
    )
    job_directories = tuple(
        (item.relative_path, item.device, item.inode, item.modified_ns)
        for item in job.local_directory_identities
    )
    if (
        scan.source_root != job.source_root
        or scan.inventory != job.source_inventory
        or scan_files != job_files
        or scan_directories != job_directories
    ):
        raise ConnectedChangeJobServiceError(
            "planner_source_changed",
            "The source changed while Markdown context was read.",
        )


def clarification_question_fingerprint(*, job_id: str, question: str) -> str:
    """Bind one exact user-visible question to its durable planner job."""

    return canonical_sha256(
        {
            "domain": "name-atlas:clarification-question:v1",
            "job_id": job_id,
            "question": question,
        }
    )
