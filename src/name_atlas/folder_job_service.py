"""Durable browser/CLI adapter for the AI-first folder workflow."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path

from name_atlas.folder_app import (
    FolderClarificationRequest,
    FolderProgressCallback,
    FolderRunOutcome,
    FolderRunPresentation,
    FolderWebCheckpoint,
    FolderWebLifecycle,
    FolderWorkPhase,
)
from name_atlas.folder_refactor.inventory import FolderScan
from name_atlas.folder_refactor.job import (
    FolderJobLifecycle,
    FolderRefactorJob,
    FolderRefactorJobStore,
    FolderRefactorJobWriter,
    build_new_job,
)
from name_atlas.folder_refactor.job_planning import JobPlannerCheckpoint
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.planner_evidence import (
    LocalFolderEvidenceService,
    PlannerEvidenceError,
)
from name_atlas.folder_refactor.planner_orchestrator import PlannerOrchestrator
from name_atlas.folder_refactor.planner_provider import (
    DeterministicDevelopmentPlannerProvider,
    PlannerProvider,
)
from name_atlas.folder_refactor.transaction import (
    FolderRunResult,
    FolderTransactionError,
    FolderTransactionPhase,
    execute_accepted_folder_plan,
    maximum_rewritten_markdown_bytes,
    preflight_output_parent,
    recover_completed_folder_run,
    scan_folder_with_references,
)
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.verification.bagit_validator import BagItPackageValidator

PlannerProviderFactory = Callable[[FolderRefactorJob], PlannerProvider]


class FolderJobServiceError(RuntimeError):
    """The persisted folder workflow cannot continue or produce a result."""


class JobBackedFolderRunService:
    """Join durable planner state to one copy-only browser transaction."""

    def __init__(
        self,
        *,
        job_path: Path,
        provider_factory: PlannerProviderFactory | None = None,
        result_folder_name: str = "name-atlas-organized-copy",
        target_prefix: str = "organized",
    ) -> None:
        self._job_path = job_path.expanduser().resolve(strict=False)
        self._provider_factory = provider_factory or (
            lambda _job: DeterministicDevelopmentPlannerProvider(
                result_folder_name=result_folder_name,
                target_prefix=target_prefix,
            )
        )
        self._completed_presentation: FolderRunPresentation | None = None
        self._completed_request: str | None = None
        self._progress_callback: FolderProgressCallback | None = None

    @property
    def run_in_worker_thread(self) -> bool:
        """Keep scanning, planning, copying, and proof off the web loop."""

        return True

    def set_progress_callback(
        self,
        callback: FolderProgressCallback | None,
        /,
    ) -> None:
        """Install one presentation-only callback for the current browser process."""

        self._progress_callback = callback

    @property
    def job_path(self) -> Path:
        """Return the exact absolute durable job path."""

        return self._job_path

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Project current durable state without invoking a provider."""

        if self._completed_presentation is not None:
            result = self._completed_presentation
            if self._completed_request is None:
                raise FolderJobServiceError("completed_presentation_without_request")
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.VERIFIED,
                source_root=result.source_root,
                output_parent=result.output_parent,
                request=self._completed_request,
                result=result,
            )
        if not os.path.lexists(self._job_path):
            return None
        store = FolderRefactorJobStore(self._job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if job.lifecycle is FolderJobLifecycle.EXECUTING:
                final_root = _final_root(job)
                if os.path.lexists(final_root):
                    try:
                        job, scan, graph = self._scan_job(writer, job)
                        result = self._recover_existing_result(job, scan, graph)
                    except (FolderJobServiceError, FolderTransactionError) as exc:
                        self._mark_blocked(
                            writer,
                            "existing_result_recovery_failed",
                            str(exc),
                        )
                        job = writer.load()
                    else:
                        presentation = _presentation(job, result)
                        self._completed_presentation = presentation
                        self._completed_request = job.user_request
                        return FolderWebCheckpoint(
                            lifecycle=FolderWebLifecycle.VERIFIED,
                            source_root=presentation.source_root,
                            output_parent=presentation.output_parent,
                            request=job.user_request,
                            result=presentation,
                        )
        if job.lifecycle is FolderJobLifecycle.AWAITING_CLARIFICATION:
            progress = job.planner_progress
            if progress is None or progress.clarification_question is None:
                raise FolderJobServiceError("awaiting_clarification_without_question")
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.AWAITING_CLARIFICATION,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                clarification=FolderClarificationRequest(
                    question=progress.clarification_question,
                    continuation_token=job.job_id,
                ),
            )
        if job.lifecycle in {
            FolderJobLifecycle.PLANNING,
            FolderJobLifecycle.EXECUTING,
        }:
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.PLANNING,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                resume_required=True,
            )
        if job.lifecycle in {FolderJobLifecycle.STALE, FolderJobLifecycle.BLOCKED}:
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.BLOCKED,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                blocker=_job_blocker(job),
            )
        raise FolderJobServiceError(
            "verified_job_presentation_requires_A3_receipt_rehydration"
        )

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunOutcome:
        """Create one absent durable job, plan it, and execute if accepted."""

        if os.path.lexists(self._job_path):
            raise FolderJobServiceError(
                "job_already_exists: resume the exact job or choose an absent path"
            )
        self._report_progress(FolderWorkPhase.READING)
        scan, reference_graph = scan_folder_with_references(source_root)
        resolved_output_parent = preflight_output_parent(
            source_root=scan.source_root,
            output_parent=output_parent,
            source_bytes=scan.inventory.total_bytes,
            rewritten_markdown_original_bytes=maximum_rewritten_markdown_bytes(scan),
        )
        job = build_new_job(
            source_root=scan.source_root,
            output_parent=resolved_output_parent,
            job_path=self._job_path,
            user_request=request,
            scan=scan,
        )
        store = FolderRefactorJobStore(self._job_path)
        with store.writer() as writer:
            saved = writer.save(job, expected_revision=None)
            return await self._continue_job(
                writer=writer,
                job=saved,
                scan=scan,
                reference_graph=reference_graph,
                answer=None,
            )

    async def continue_after_clarification(
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderRunPresentation:
        """Persist the one answer and continue the exact existing job."""

        store = FolderRefactorJobStore(self._job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if continuation_token != job.job_id:
                raise FolderJobServiceError("clarification_job_token_mismatch")
            if job.lifecycle is not FolderJobLifecycle.AWAITING_CLARIFICATION:
                raise FolderJobServiceError("clarification_not_active")
            job, scan, reference_graph = self._scan_job(writer, job)
            outcome = await self._continue_job(
                writer=writer,
                job=job,
                scan=scan,
                reference_graph=reference_graph,
                answer=answer,
            )
        if not isinstance(outcome, FolderRunPresentation):
            raise FolderJobServiceError("second_clarification_not_allowed")
        return outcome

    async def resume_existing_job(self) -> FolderRunOutcome:
        """Continue a persisted planning/execution state exactly once."""

        store = FolderRefactorJobStore(self._job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if job.lifecycle is FolderJobLifecycle.AWAITING_CLARIFICATION:
                progress = job.planner_progress
                if progress is None or progress.clarification_question is None:
                    raise FolderJobServiceError(
                        "awaiting_clarification_without_question"
                    )
                return FolderClarificationRequest(
                    question=progress.clarification_question,
                    continuation_token=job.job_id,
                )
            if job.lifecycle not in {
                FolderJobLifecycle.PLANNING,
                FolderJobLifecycle.EXECUTING,
            }:
                raise FolderJobServiceError(_job_blocker(job))
            self._report_progress(FolderWorkPhase.READING)
            job, scan, reference_graph = self._scan_job(writer, job)
            return await self._continue_job(
                writer=writer,
                job=job,
                scan=scan,
                reference_graph=reference_graph,
                answer=None,
            )

    async def _continue_job(
        self,
        *,
        writer: FolderRefactorJobWriter,
        job: FolderRefactorJob,
        scan: FolderScan,
        reference_graph: FolderReferenceGraph,
        answer: str | None,
    ) -> FolderRunOutcome:
        preflight_output_parent(
            source_root=scan.source_root,
            output_parent=job.output_parent,
            source_bytes=scan.inventory.total_bytes,
            rewritten_markdown_original_bytes=maximum_rewritten_markdown_bytes(scan),
        )
        if job.lifecycle is FolderJobLifecycle.EXECUTING:
            self._report_progress(FolderWorkPhase.CHECKING)
            return self._execute(writer, job, scan, reference_graph)
        self._report_progress(FolderWorkPhase.PLANNING)
        provider = self._provider_factory(job)
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
            checkpoint=JobPlannerCheckpoint(writer),
        )
        try:
            progress = job.planner_progress or orchestrator.initial_progress()
        except PlannerEvidenceError as exc:
            self._mark_blocked(writer, exc.code, exc.message)
            raise FolderJobServiceError(f"{exc.code}: {exc.message}") from exc
        if answer is None:
            progress = await orchestrator.run(progress)
        else:
            progress = await orchestrator.answer_clarification(progress, answer)
        latest = writer.load()
        if progress.status == "awaiting_clarification":
            if progress.clarification_question is None:
                raise FolderJobServiceError("awaiting_clarification_without_question")
            return FolderClarificationRequest(
                question=progress.clarification_question,
                continuation_token=latest.job_id,
            )
        if progress.status == "blocked":
            raise FolderJobServiceError(
                f"{progress.blocker_code}: planner could not produce an accepted plan"
            )
        if progress.status != "accepted":
            raise FolderJobServiceError("planner_stopped_without_terminal_outcome")
        self._report_progress(FolderWorkPhase.CHECKING)
        return self._execute(writer, latest, scan, reference_graph)

    def _execute(
        self,
        writer: FolderRefactorJobWriter,
        job: FolderRefactorJob,
        scan: FolderScan,
        reference_graph: FolderReferenceGraph,
    ) -> FolderRunPresentation:
        if job.accepted_plan is None:
            raise FolderJobServiceError("execution_without_accepted_plan")
        final_root = _final_root(job)
        if os.path.lexists(final_root):
            self._report_progress(FolderWorkPhase.VERIFYING)
            try:
                result = self._recover_existing_result(job, scan, reference_graph)
            except FolderTransactionError as exc:
                self._mark_blocked(
                    writer,
                    "existing_result_recovery_failed",
                    str(exc),
                )
                raise FolderJobServiceError(str(exc)) from exc
            presentation = _presentation(job, result)
            self._completed_presentation = presentation
            self._completed_request = job.user_request
            return presentation
        try:
            result = execute_accepted_folder_plan(
                initial_scan=scan,
                output_parent=job.output_parent,
                request=job.user_request,
                accepted_plan=job.accepted_plan,
                reference_graph=reference_graph,
                bag_writer=BagItWriter(),
                package_validator=BagItPackageValidator(),
                progress_callback=self._report_transaction_phase,
            )
        except FolderTransactionError as exc:
            self._mark_blocked(writer, "folder_transaction_blocked", str(exc))
            raise FolderJobServiceError(str(exc)) from exc
        presentation = _presentation(job, result)
        self._completed_presentation = presentation
        self._completed_request = job.user_request
        return presentation

    def _report_transaction_phase(self, phase: FolderTransactionPhase) -> None:
        mapped = {
            FolderTransactionPhase.CREATING_RESULT: FolderWorkPhase.CREATING,
            FolderTransactionPhase.UPDATING_SUPPORTED_LINKS: (
                FolderWorkPhase.UPDATING_LINKS
            ),
            FolderTransactionPhase.VERIFYING_RESULT: FolderWorkPhase.VERIFYING,
        }[phase]
        self._report_progress(mapped)

    def _report_progress(self, phase: FolderWorkPhase) -> None:
        callback = self._progress_callback
        if callback is not None:
            callback(phase)

    @staticmethod
    def _recover_existing_result(
        job: FolderRefactorJob,
        scan: FolderScan,
        reference_graph: FolderReferenceGraph,
    ) -> FolderRunResult:
        if job.accepted_plan is None:
            raise FolderJobServiceError("execution_without_accepted_plan")
        return recover_completed_folder_run(
            initial_scan=scan,
            output_parent=job.output_parent,
            request=job.user_request,
            accepted_plan=job.accepted_plan,
            reference_graph=reference_graph,
            package_validator=BagItPackageValidator(),
        )

    def _scan_job(
        self,
        writer: FolderRefactorJobWriter,
        job: FolderRefactorJob,
    ) -> tuple[FolderRefactorJob, FolderScan, FolderReferenceGraph]:
        scan, graph = scan_folder_with_references(job.source_root)
        rehydrated = writer.rehydrate_against(scan)
        if rehydrated.lifecycle is FolderJobLifecycle.STALE:
            raise FolderJobServiceError("source_changed: durable inventory mismatch")
        return rehydrated, scan, graph

    def _mark_blocked(
        self,
        writer: FolderRefactorJobWriter,
        code: str,
        message: str,
    ) -> None:
        current = writer.load()
        if current.lifecycle.terminal:
            return
        payload = current.model_dump(mode="python")
        payload.update(
            {
                "lifecycle": FolderJobLifecycle.BLOCKED,
                "blocker_code": code,
                "blocker_message": message[:2_000],
                "pending_result_path": None,
            }
        )
        candidate = FolderRefactorJob.model_validate(payload, strict=True)
        writer.save(candidate, expected_revision=current.revision)


def _presentation(
    job: FolderRefactorJob,
    result: FolderRunResult,
) -> FolderRunPresentation:
    checks = {check.check_id: check.passed for check in result.report.checks}
    return FolderRunPresentation(
        source_root=job.source_root,
        output_parent=job.output_parent,
        result_root=result.result_root,
        data_root=result.data_root,
        source_file_count=result.report.file_count,
        path_change_count=result.report.path_change_count,
        supported_link_count=result.report.supported_link_count,
        supported_link_update_count=result.report.rewritten_link_count,
        source_unchanged=checks.get("source_unchanged") is True,
        all_files_present_once=(
            checks.get("complete_file_bijection") is True
            and checks.get("payload_hashes_preserved") is True
        ),
        deterministic_proof_passed=bool(checks) and all(checks.values()),
        independent_verification_passed=False,
        reconstruction_available=False,
        technical_facts=(
            ("Job ID", job.job_id),
            ("Source commitment", result.report.source_commitment),
            ("Staged data commitment", result.report.staged_data_commitment),
            ("Portable package", "BagIt validation passed"),
        ),
    )


def _job_blocker(job: FolderRefactorJob) -> str:
    if job.lifecycle is FolderJobLifecycle.STALE:
        if job.stale_differences:
            changed = ", ".join(
                difference.kind.value for difference in job.stale_differences[:5]
            )
            return f"source_changed: {changed}"
        if job.source_scan_blocker is not None:
            return f"source_scan_failed: {job.source_scan_blocker.detail}"
        return "source_changed"
    if job.blocker_code is not None:
        return f"{job.blocker_code}: {job.blocker_message}"
    return f"job_not_resumable:{job.lifecycle.value}"


def _final_root(job: FolderRefactorJob) -> Path:
    if job.accepted_plan is None:
        raise FolderJobServiceError("execution_without_accepted_plan")
    return job.output_parent / job.accepted_plan.result_folder_name
