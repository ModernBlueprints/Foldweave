"""Browser adapter for the durable Foldweave v3 review authority."""

from __future__ import annotations

import os
from collections.abc import Callable, Mapping
from pathlib import Path

from name_atlas.connected_web_service import ConnectedChangeDownload
from name_atlas.folder_app import (
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
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerification,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.receipt_contracts import FolderRestoreReport
from name_atlas.folder_refactor.serialization import canonical_sha256

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
    ) -> None:
        self._job_path = job_path.expanduser().resolve(strict=False)
        self._service = service or FoldweaveReviewService()
        self._target_map_factory = target_map_factory or _default_target_map

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
            channel="browser",
        )
        if job.lifecycle is not FolderJobLifecycleV3.VERIFIED:
            detail = (
                job.staleness.detail
                if job.staleness is not None
                else job.blocker_message or f"Job ended in {job.lifecycle.value}."
            )
            raise ValueError(detail)
        return self._terminal_presentation(job)

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Project the current job without provider, budget, copy, or mutation."""

        if not os.path.lexists(self._job_path):
            return None
        return self._checkpoint(self._service.status(self._job_path))

    def rehydrate_web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Revalidate local inputs once before projecting a startup checkpoint."""

        if not os.path.lexists(self._job_path):
            return None
        job = FolderRefactorJobV3Store(self._job_path).load()
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
