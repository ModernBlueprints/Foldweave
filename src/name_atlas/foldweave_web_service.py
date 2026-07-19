"""Browser adapter for the durable Foldweave v3 review authority."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from pathlib import Path

from name_atlas.connected_web_service import ConnectedChangeDownload
from name_atlas.folder_app import (
    FolderClarificationRequest,
    FolderJourney,
    FolderReviewHandle,
    FolderRunOutcome,
    FolderRunPresentation,
    FolderWebCheckpoint,
    FolderWebLifecycle,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    GptPlannedJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
    FoldweaveReviewServiceError,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerification,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.receipt_contracts import FolderRestoreReport
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.foldweave_provider_factory import (
    FoldweavePlanningProviderFactory,
)

TargetMapFactory = Callable[[Path, str], tuple[str, Mapping[str, str]]]


class FoldweaveBrowserReviewService:
    """Expose one v3 job through the existing loopback application shell."""

    planner_label = "Foldweave deterministic review — no API call"
    planner_note = (
        "This F0a walking transaction prepares a complete review without a "
        "provider call. Exact GPT-5.6 planning is qualified in the native gate."
    )
    evidence_disclosure_required = True
    outbound_evidence_will_be_sent = False
    default_request = (
        "Organize this connected project for handoff. Keep every file and every "
        "supported Markdown link working."
    )
    durable_status_is_read_only = True

    def __init__(
        self,
        *,
        job_path: Path,
        service: FoldweaveReviewService | None = None,
        target_map_factory: TargetMapFactory | None = None,
        provider_factory: FoldweavePlanningProviderFactory | None = None,
        review_channel: str = "browser",
    ) -> None:
        self._job_path = job_path.expanduser().resolve(strict=False)
        self._service = service or FoldweaveReviewService()
        self._target_map_factory = target_map_factory or _default_target_map
        self._provider_factory = provider_factory
        if review_channel not in {"browser", "native_app"}:
            raise ValueError("Browser review channel must be browser or native_app.")
        self._review_channel = review_channel
        if provider_factory is not None:
            self.planner_label = "Live GPT-5.6 planning"
            self.planner_note = (
                "GPT-5.6 receives only the bounded evidence disclosed below. "
                "Foldweave checks the complete proposal before review and creates "
                "nothing until exact acceptance."
            )
            self.outbound_evidence_will_be_sent = True

    @property
    def run_in_worker_thread(self) -> bool:
        """Keep scans, matching, copy, and proof off the web event loop."""

        return True

    @property
    def job_path(self) -> Path:
        return self._job_path

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunOutcome:
        """Prepare one complete origin preview without creating output."""

        if self._provider_factory is None:
            result_name, targets = self._target_map_factory(source_root, request)
            job = self._service.prepare_deterministic_origin_review(
                source_root=source_root,
                output_parent=output_parent,
                job_path=self._job_path,
                request=request,
                result_folder_name=result_name,
                target_by_original_path=targets,
                idempotency_key=_browser_job_key(self._job_path, "organize"),
            )
        else:
            job = await self._service.prepare_planned_origin_review(
                source_root=source_root,
                output_parent=output_parent,
                job_path=self._job_path,
                request=request,
                idempotency_key=_browser_job_key(self._job_path, "organize"),
                provider=self._provider_factory.initial_provider(),
            )
        return self._review_or_terminal(job)

    async def apply_shared_change(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> FolderRunPresentation | FolderReviewHandle:
        """Prepare Martin's receiver-local preview without model activity."""

        job = self._service.prepare_application_review(
            change_file_path=change_file_path,
            source_root=source_root,
            output_parent=output_parent,
            job_path=self._job_path,
            idempotency_key=_browser_job_key(self._job_path, "apply"),
        )
        return self._review_or_terminal(job)

    async def resume_existing_job(self) -> FolderRunOutcome:
        """Continue one exact persisted job without duplicating its operation."""

        job = self._service.status(self._job_path)
        if job.lifecycle is FolderJobLifecycleV3.MATCHING:
            if not isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
                raise ValueError("Matching job lacks Change File authority.")
            job = self._service.prepare_application_review(
                change_file_path=job.authority.change_file_binding.path,
                source_root=job.source_root,
                output_parent=job.output_parent,
                job_path=job.job_path,
                idempotency_key=_browser_job_key(job.job_path, "apply"),
            )
        elif job.lifecycle is FolderJobLifecycleV3.PLANNING:
            if self._provider_factory is None:
                result_name, targets = self._target_map_factory(
                    job.source_root,
                    job.user_request,
                )
                job = self._service.prepare_deterministic_origin_review(
                    source_root=job.source_root,
                    output_parent=job.output_parent,
                    job_path=job.job_path,
                    request=job.user_request,
                    result_folder_name=result_name,
                    target_by_original_path=targets,
                    idempotency_key=_browser_job_key(job.job_path, "organize"),
                )
            else:
                authority = job.authority
                progress = (
                    authority.planner_checkpoint.progress
                    if isinstance(authority, GptPlannedJobAuthorityV3)
                    else None
                )
                if progress is not None and progress.pending_response_turn is not None:
                    job = await self._service.recover_interrupted_planned_origin_review(
                        job.job_path
                    )
                else:
                    job = await self._service.resume_planned_origin_review(
                        job.job_path,
                        provider=self._provider_factory.initial_provider(),
                    )
        elif job.lifecycle is FolderJobLifecycleV3.AWAITING_CLARIFICATION:
            return _clarification_request(job)
        elif job.lifecycle is FolderJobLifecycleV3.REVISING:
            job = self._service.recover_interrupted_revision(job.job_path)
        elif job.lifecycle is FolderJobLifecycleV3.EXECUTING:
            job = self._service.resume_authorized_execution(job.job_path)
        return self._review_or_terminal(job)

    async def continue_after_clarification(
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderRunOutcome:
        """Continue the exact direct-planning job after its sole answer."""

        if self._provider_factory is None:
            raise ValueError("Live clarification is unavailable in this mode.")
        current = self._service.status(self._job_path)
        if current.job_id != continuation_token:
            raise FoldweaveReviewServiceError(
                "clarification_token_mismatch",
                "The clarification answer targets another durable job.",
            )
        if current.lifecycle is not FolderJobLifecycleV3.AWAITING_CLARIFICATION:
            raise FoldweaveReviewServiceError(
                "clarification_not_active",
                "The durable job is not waiting for a clarification answer.",
            )
        job = await self._service.answer_planned_origin_clarification(
            self._job_path,
            continuation_token=continuation_token,
            answer=answer,
            provider=self._provider_factory.initial_provider(),
        )
        return self._review_or_terminal(job)

    def get_plan_preview(self, job_id: str):
        """Return the complete persisted DTO for the active job only."""

        job = self._require_job_id(job_id)
        if job.preview is None:
            raise ValueError("Active Foldweave job has no review preview.")
        return job.preview

    async def accept_review(
        self,
        *,
        job_id: str,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        output_parent: Path,
        result_folder_name: str,
        idempotency_key: str,
    ) -> FolderRunPresentation:
        """Accept one exact browser-visible preview and return verified facts."""

        self._require_job_id(job_id)
        job = self._service.accept(
            self._job_path,
            expected_revision=expected_revision,
            preview_fingerprint=preview_fingerprint,
            candidate_fingerprint=candidate_fingerprint,
            output_parent=output_parent,
            result_folder_name=result_folder_name,
            idempotency_key=idempotency_key,
            channel=self._review_channel,
        )
        if job.lifecycle is not FolderJobLifecycleV3.VERIFIED:
            detail = (
                job.staleness.detail
                if job.staleness is not None
                else job.blocker_message or f"Job ended in {job.lifecycle.value}."
            )
            raise ValueError(detail)
        return self._terminal_presentation(job)

    async def revise_review(
        self,
        *,
        job_id: str,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        instruction: str,
        idempotency_key: str,
    ) -> FolderReviewHandle:
        """Run one bounded provider revision and return the replacement review."""

        self._require_job_id(job_id)
        if self._provider_factory is None:
            raise ValueError("Live proposal revision is unavailable in this mode.")
        job = await self._service.revise(
            self._job_path,
            expected_revision=expected_revision,
            preview_fingerprint=preview_fingerprint,
            candidate_fingerprint=candidate_fingerprint,
            instruction=instruction,
            idempotency_key=idempotency_key,
            provider_factory=self._provider_factory.revision_provider,
        )
        if job.lifecycle not in {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
        }:
            detail = job.blocker_message or f"Job ended in {job.lifecycle.value}."
            raise ValueError(detail)
        return _review_handle(job)

    async def keep_previous_review(
        self,
        *,
        job_id: str,
        expected_revision: int,
        preview_fingerprint: str,
        candidate_fingerprint: str,
        idempotency_key: str,
    ) -> FolderReviewHandle:
        """Dismiss one failed revision while retaining its prior valid proposal."""

        if not idempotency_key.strip():
            raise ValueError("Keep-proposal idempotency key is required.")
        self._require_job_id(job_id)
        job = self._service.keep_previous_proposal(
            self._job_path,
            expected_revision=expected_revision,
            preview_fingerprint=preview_fingerprint,
            candidate_fingerprint=candidate_fingerprint,
            idempotency_key=idempotency_key,
        )
        return _review_handle(job)

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Project the current job without provider, budget, copy, or mutation."""

        if not os.path.lexists(self._job_path):
            return None
        return self._checkpoint(self._service.status(self._job_path))

    def rehydrate_web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Revalidate local inputs once before projecting a startup checkpoint."""

        if not os.path.lexists(self._job_path):
            return None
        store = FolderRefactorJobV3Store(self._job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
        if job.lifecycle is FolderJobLifecycleV3.REVISING:
            job = self._service.recover_interrupted_revision(self._job_path)
        if job.lifecycle is FolderJobLifecycleV3.EXECUTING:
            job = self._service.resume_authorized_execution(self._job_path)
        return self._checkpoint(job)

    def get_change_file_download(self) -> ConnectedChangeDownload:
        """Capture exact verified bytes for one bounded download response."""

        path, fingerprint, receipt_fingerprint = self._service.get_change_file(
            self._job_path
        )
        payload = path.read_bytes()
        return ConnectedChangeDownload(
            payload=payload,
            filename="foldweave.foldweave-change.json",
            change_file_fingerprint=fingerprint,
            originating_receipt_fingerprint=receipt_fingerprint,
        )

    def verify_again(self) -> ConnectedReceiptVerification:
        return self._service.verify_result(self._job_path)

    def recreate_original(self, destination: Path) -> FolderRestoreReport:
        return self._service.recreate_original(self._job_path, destination)

    def _review_or_terminal(
        self,
        job: FolderRefactorJobV3,
    ) -> FolderReviewHandle | FolderRunPresentation:
        if job.lifecycle in {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
        }:
            return _review_handle(job)
        if job.lifecycle is FolderJobLifecycleV3.VERIFIED:
            return self._terminal_presentation(job)
        detail = (
            job.staleness.detail
            if job.staleness is not None
            else job.blocker_message or f"Job ended in {job.lifecycle.value}."
        )
        raise ValueError(detail)

    def _terminal_presentation(
        self,
        job: FolderRefactorJobV3,
    ) -> FolderRunPresentation:
        self._service.verify_result(job.job_path)
        _change_path, _change_fingerprint, originating_receipt = (
            self._service.get_change_file(job.job_path)
        )
        if job.preview is None or job.verified_artifacts is None:
            raise ValueError("Verified Foldweave job lacks preview or proof facts.")
        assert job.final_result_path is not None
        role = (
            "receiver"
            if isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
            else "origin"
        )
        return FolderRunPresentation(
            source_root=job.source_root,
            output_parent=job.output_parent,
            result_root=job.final_result_path,
            data_root=job.final_result_path / "data",
            source_file_count=job.preview.counts.file_count,
            path_change_count=job.preview.counts.changed_path_count,
            supported_link_count=job.preview.counts.link_count,
            supported_link_update_count=job.preview.counts.link_updated_count,
            source_unchanged=True,
            all_files_present_once=True,
            deterministic_proof_passed=True,
            independent_verification_passed=True,
            reconstruction_available=True,
            receipt_fingerprint=job.verified_artifacts.receipt_fingerprint,
            change_file_fingerprint=job.verified_artifacts.change_file_fingerprint,
            originating_receipt_fingerprint=originating_receipt,
            organized_tree_commitment=(
                job.verified_artifacts.organized_tree_commitment
            ),
            execution_role=role,
            technical_facts=(
                ("Preview fingerprint", job.preview.preview_fingerprint),
                (
                    "Candidate fingerprint",
                    job.preview.compiled_candidate_fingerprint,
                ),
                (
                    "Authorization fingerprint",
                    job.execution_authorization.authorization_fingerprint,
                ),
            ),
        )

    def _checkpoint(self, job: FolderRefactorJobV3) -> FolderWebCheckpoint:
        if job.lifecycle in {
            FolderJobLifecycleV3.MATCHING,
            FolderJobLifecycleV3.PLANNING,
            FolderJobLifecycleV3.EXECUTING,
        }:
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.PLANNING,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=(
                    FolderJourney.APPLY
                    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
                    else FolderJourney.ORGANIZE
                ),
                resume_required=True,
            )
        if job.lifecycle is FolderJobLifecycleV3.AWAITING_CLARIFICATION:
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.AWAITING_CLARIFICATION,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=FolderJourney.ORGANIZE,
                clarification=_clarification_request(job),
            )
        if job.lifecycle in {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
        }:
            handle = _review_handle(job)
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.REVIEWING,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=handle.journey,
                review=handle,
            )
        if job.lifecycle is FolderJobLifecycleV3.VERIFIED:
            result = self._terminal_presentation(job)
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.VERIFIED,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=(
                    FolderJourney.APPLY
                    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
                    else FolderJourney.ORGANIZE
                ),
                result=result,
            )
        detail = (
            job.staleness.detail
            if job.staleness is not None
            else job.blocker_message
            or f"Foldweave job requires a fresh start from {job.lifecycle.value}."
        )
        return FolderWebCheckpoint(
            lifecycle=FolderWebLifecycle.BLOCKED,
            source_root=job.source_root,
            output_parent=job.output_parent,
            request=job.user_request,
            journey=(
                FolderJourney.APPLY
                if isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
                else FolderJourney.ORGANIZE
            ),
            blocker=detail,
        )

    def _require_job_id(self, job_id: str) -> FolderRefactorJobV3:
        job = self._service.status(self._job_path)
        if job.job_id != job_id:
            raise ValueError("Requested review job is not active in this application.")
        return job


def _clarification_request(job: FolderRefactorJobV3) -> FolderClarificationRequest:
    authority = job.authority
    if not isinstance(authority, GptPlannedJobAuthorityV3):
        raise ValueError("Clarification state lacks GPT planning authority.")
    progress = authority.planner_checkpoint.progress
    question = None if progress is None else progress.clarification_question
    if question is None:
        raise ValueError("Clarification state lacks its persisted question.")
    return FolderClarificationRequest(
        question=question,
        continuation_token=job.job_id,
    )


def _review_handle(job: FolderRefactorJobV3) -> FolderReviewHandle:
    if job.preview is None or job.candidate_plan is None:
        raise ValueError("Reviewing Foldweave job lacks its complete preview.")
    return FolderReviewHandle(
        job_id=job.job_id,
        job_revision=job.revision,
        proposal_revision=job.proposal_revision,
        candidate_fingerprint=job.preview.compiled_candidate_fingerprint,
        preview_fingerprint=job.preview.preview_fingerprint,
        source_root=job.source_root,
        output_parent=job.output_parent,
        result_folder_name=job.candidate_plan.result_folder_name,
        journey=(
            FolderJourney.APPLY
            if isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
            else FolderJourney.ORGANIZE
        ),
        revision_available=(
            isinstance(job.authority, GptPlannedJobAuthorityV3)
            and job.authority.evidence_ledger is not None
            and job.revision_attempt_count < 2
            and job.proposal_revision < 2
        ),
        revision_attempts_remaining=(
            max(0, 2 - job.revision_attempt_count)
            if (
                isinstance(job.authority, GptPlannedJobAuthorityV3)
                and job.authority.evidence_ledger is not None
                and job.proposal_revision < 2
            )
            else 0
        ),
        revision_failure=(
            None if job.revision_failure is None else job.revision_failure.detail
        ),
    )


def _default_target_map(
    source_root: Path,
    _request: str,
) -> tuple[str, Mapping[str, str]]:
    scan = scan_folder(source_root)
    return (
        "foldweave-organized-copy",
        {
            item.relative_path: (
                item.relative_path
                if item.protected
                else f"organized/{item.relative_path}"
            )
            for item in scan.inventory.files
        },
    )


def _browser_job_key(job_path: Path, operation: str) -> str:
    return canonical_sha256(
        {
            "domain": "foldweave:browser-job:v1",
            "job_path": str(job_path),
            "operation": operation,
        }
    )
