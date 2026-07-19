"""Browser adapter over the durable Connected Change service authority."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from name_atlas.folder_app import (
    FolderJourney,
    FolderProgressCallback,
    FolderRunOutcome,
    FolderRunPresentation,
    FolderWebCheckpoint,
    FolderWebLifecycle,
    FolderWorkPhase,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file,
)
from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
    ConnectedChangeJobServiceError,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
    FolderJobLifecycleV2,
    FolderRefactorJobV2,
    GptPlannedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_PATH,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV2,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerification,
    ConnectedReceiptVerificationStatus,
)
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    canonical_portable_json_bytes,
    parse_portable_model,
    read_regular_bytes,
)
from name_atlas.folder_refactor.receipt_contracts import FolderRestoreReport
from name_atlas.folder_refactor.transaction import FolderTransactionPhase

if TYPE_CHECKING:
    from name_atlas.folder_refactor.planner_provider import PlannerProvider

DETERMINISTIC_BROWSER_REQUEST = (
    "Prepare this project for handoff. Keep every file and every supported "
    "Markdown link working."
)


@dataclass(frozen=True, slots=True)
class ConnectedChangeDownload:
    """Verified Change File bytes captured before the HTTP response is built."""

    payload: bytes
    filename: str
    change_file_fingerprint: str
    originating_receipt_fingerprint: str


class ConnectedBrowserRunService:
    """Expose one durable v2 job through the shared browser protocols."""

    result_folder_name = "name-atlas-organized-copy"
    target_prefix = "organized"
    planner_label = "Deterministic development planning — no API call"
    planner_note = (
        "C2 exercises the complete Connected Change transaction without a provider. "
        "Live and recorded GPT-5.6 planning are qualified in C3."
    )
    evidence_disclosure_required = True
    outbound_evidence_will_be_sent = False
    default_request = DETERMINISTIC_BROWSER_REQUEST
    durable_status_is_read_only = True

    def __init__(
        self,
        *,
        job_path: Path,
        service: ConnectedChangeJobService | None = None,
        planner_provider_factory: Callable[[], PlannerProvider] | None = None,
        planner_label: str | None = None,
        planner_note: str | None = None,
        outbound_evidence_will_be_sent: bool | None = None,
        default_request: str | None = None,
        change_file_download_name: str | None = None,
    ) -> None:
        self._job_path = job_path.expanduser().resolve(strict=False)
        self._service = service or ConnectedChangeJobService()
        self._planner_provider_factory = planner_provider_factory
        self._progress_callback: FolderProgressCallback | None = None
        if planner_label is not None:
            self.planner_label = planner_label
        if planner_note is not None:
            self.planner_note = planner_note
        if outbound_evidence_will_be_sent is not None:
            self.outbound_evidence_will_be_sent = outbound_evidence_will_be_sent
        if default_request is not None:
            self.default_request = default_request
        self._change_file_download_name = change_file_download_name

    @property
    def run_in_worker_thread(self) -> bool:
        """Keep the complete durable filesystem transaction off the web loop."""

        return True

    @property
    def job_path(self) -> Path:
        """Return the one durable browser job path."""

        return self._job_path

    def set_progress_callback(
        self,
        callback: FolderProgressCallback | None,
        /,
    ) -> None:
        """Install one presentation-only callback for the active web process."""

        self._progress_callback = callback

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunOutcome:
        """Run the complete truthful deterministic-development origin path."""

        self._report(FolderWorkPhase.READING)
        self._report(FolderWorkPhase.PLANNING)
        from name_atlas.folder_refactor.connected_change.planning import (
            ConnectedOriginPlanningService,
        )

        planner = ConnectedOriginPlanningService(job_service=self._service)
        job = await planner.start(
            source_root=source_root,
            output_parent=output_parent,
            job_path=self._job_path,
            request=request,
            idempotency_key=_web_idempotency_key(self._job_path, "organize"),
            provider=self._new_planner_provider(),
            progress_callback=self._transaction_progress,
            idempotency_scope="exact_path",
        )
        return self._job_outcome(job)

    async def apply_shared_change(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> FolderRunPresentation:
        """Apply one Change File without planner, provider, API, or budget use."""

        self._report(FolderWorkPhase.READING)
        self._report(FolderWorkPhase.CHECKING)
        job = self._service.start_application(
            change_file_path=change_file_path,
            source_root=source_root,
            output_parent=output_parent,
            job_path=self._job_path,
            idempotency_key=_web_idempotency_key(self._job_path, "apply"),
            progress_callback=self._transaction_progress,
            idempotency_scope="exact_path",
        )
        return self._terminal_presentation(job)

    async def resume_existing_job(self) -> FolderRunOutcome:
        """Continue the exact persisted v2 job without creating another job."""

        job = self._service.status(self._job_path)
        self._report(FolderWorkPhase.READING)
        if job.lifecycle is FolderJobLifecycleV2.PLANNING and isinstance(
            job.authority, GptPlannedJobAuthorityV2
        ):
            self._report(FolderWorkPhase.PLANNING)
            from name_atlas.folder_refactor.connected_change.planning import (
                ConnectedOriginPlanningService,
            )

            planner = ConnectedOriginPlanningService(job_service=self._service)
            job = await planner.resume(
                job.job_path,
                provider=self._new_planner_provider(),
                progress_callback=self._transaction_progress,
            )
        elif job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
            return self._job_outcome(job)
        else:
            self._report(FolderWorkPhase.CHECKING)
            job = self._service.run_or_resume(
                self._job_path,
                progress_callback=self._transaction_progress,
            )
        return self._job_outcome(job)

    async def continue_after_clarification(
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderRunPresentation:
        """Persist one answer, continue planning, and execute the accepted map."""

        self._report(FolderWorkPhase.PLANNING)
        from name_atlas.folder_refactor.connected_change.planning import (
            ConnectedOriginPlanningService,
        )

        planner = ConnectedOriginPlanningService(job_service=self._service)
        job = await planner.answer(
            self._job_path,
            continuation_token=continuation_token,
            answer=answer,
            provider=self._new_planner_provider(),
            progress_callback=self._transaction_progress,
        )
        outcome = self._job_outcome(job)
        if not isinstance(outcome, FolderRunPresentation):
            raise ConnectedChangeJobServiceError(
                "second_clarification_not_allowed",
                "A completed clarification cannot produce another user question.",
            )
        return outcome

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Project the persisted v2 job without provider, budget, or mutation."""

        if not os.path.lexists(self._job_path):
            return None
        return self._web_checkpoint_for_job(self._service.status(self._job_path))

    def rehydrate_web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Persist startup staleness before projecting a nonterminal browser job."""

        if not os.path.lexists(self._job_path):
            return None
        return self._web_checkpoint_for_job(self._service.rehydrate(self._job_path))

    def _web_checkpoint_for_job(
        self,
        job: FolderRefactorJobV2,
    ) -> FolderWebCheckpoint:
        """Project an already loaded durable job without further mutation."""

        journey = _job_journey(job)
        if job.lifecycle is FolderJobLifecycleV2.VERIFIED:
            try:
                result = self._presentation(job)
            except Exception as exc:  # noqa: BLE001 - terminal proof is fail-closed
                return FolderWebCheckpoint(
                    lifecycle=FolderWebLifecycle.BLOCKED,
                    source_root=job.source_root,
                    output_parent=job.output_parent,
                    request=job.user_request,
                    journey=journey,
                    blocker=(
                        "Independent verification blocked: "
                        f"{' '.join(str(exc).split())[:1_000]}"
                    ),
                )
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.VERIFIED,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=journey,
                result=result,
            )
        if job.lifecycle in {
            FolderJobLifecycleV2.PLANNING,
            FolderJobLifecycleV2.EXECUTING,
        }:
            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.PLANNING,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=journey,
                resume_required=True,
            )
        if job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
            checkpoint = job.authority
            if not isinstance(checkpoint, GptPlannedJobAuthorityV2):
                raise ConnectedChangeJobServiceError(
                    "clarification_authority_invalid",
                    "Clarification state does not have GPT planning authority.",
                )
            question = checkpoint.planner_checkpoint.clarification_question
            if question is None:
                raise ConnectedChangeJobServiceError(
                    "clarification_question_missing",
                    "Clarification state has no bound question.",
                )
            from name_atlas.folder_app import FolderClarificationRequest

            return FolderWebCheckpoint(
                lifecycle=FolderWebLifecycle.AWAITING_CLARIFICATION,
                source_root=job.source_root,
                output_parent=job.output_parent,
                request=job.user_request,
                journey=journey,
                clarification=FolderClarificationRequest(
                    question=question,
                    continuation_token=job.job_id,
                ),
            )
        return FolderWebCheckpoint(
            lifecycle=FolderWebLifecycle.BLOCKED,
            source_root=job.source_root,
            output_parent=job.output_parent,
            request=job.user_request,
            journey=journey,
            blocker=_job_blocker(job),
        )

    def verify_again(self) -> ConnectedReceiptVerification:
        """Run source-free verification without changing the durable job."""

        return self._service.verify_result(self._job_path)

    def recreate_original(self, destination: Path) -> FolderRestoreReport:
        """Recreate this job's own source paths through the shared engine."""

        return self._service.recreate_original(self._job_path, destination)

    def get_change_file_download(self) -> ConnectedChangeDownload:
        """Capture and rebind verified Change File bytes before HTTP streaming."""

        path, expected_fingerprint, expected_originating_receipt = (
            self._service.get_change_file(self._job_path)
        )
        job = self._service.status(self._job_path)
        if job.final_result_path is None:
            raise ConnectedChangeJobServiceError(
                "verified_result_path_missing",
                "The verified job does not retain its result path.",
            )
        payload = read_regular_bytes(job.final_result_path, CONNECTED_CHANGE_PATH)
        change_file = parse_connected_change_file(payload)
        repeated = self._service.get_change_file(self._job_path)
        if (
            path != job.final_result_path / CONNECTED_CHANGE_PATH
            or repeated != (path, expected_fingerprint, expected_originating_receipt)
            or change_file.change_file_fingerprint != expected_fingerprint
            or change_file.originating_receipt.receipt_fingerprint
            != expected_originating_receipt
        ):
            raise ConnectedChangeJobServiceError(
                "result_changed_during_download",
                "The verified Change File changed while it was prepared.",
            )
        result_name = (
            job.accepted_plan.result_folder_name
            if job.accepted_plan is not None
            else "name-atlas"
        )
        return ConnectedChangeDownload(
            payload=payload,
            filename=(
                self._change_file_download_name
                or f"{result_name}.nameatlas-change.json"
            ),
            change_file_fingerprint=expected_fingerprint,
            originating_receipt_fingerprint=expected_originating_receipt,
        )

    def _terminal_presentation(
        self,
        job: FolderRefactorJobV2,
    ) -> FolderRunPresentation:
        if job.lifecycle is not FolderJobLifecycleV2.VERIFIED:
            blocker = _job_blocker(job)
            raise ConnectedChangeJobServiceError(job.lifecycle.value, blocker)
        return self._presentation(job)

    def _job_outcome(self, job: FolderRefactorJobV2) -> FolderRunOutcome:
        if job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
            if not isinstance(job.authority, GptPlannedJobAuthorityV2):
                raise ConnectedChangeJobServiceError(
                    "clarification_authority_invalid",
                    "Clarification state lacks GPT planning authority.",
                )
            question = job.authority.planner_checkpoint.clarification_question
            if question is None:
                raise ConnectedChangeJobServiceError(
                    "clarification_question_missing",
                    "Clarification state has no bound question.",
                )
            from name_atlas.folder_app import FolderClarificationRequest

            return FolderClarificationRequest(
                question=question,
                continuation_token=job.job_id,
            )
        return self._terminal_presentation(job)

    def _new_planner_provider(self) -> PlannerProvider:
        if self._planner_provider_factory is not None:
            return self._planner_provider_factory()
        from name_atlas.folder_refactor.planner_provider import (
            DeterministicDevelopmentPlannerProvider,
        )

        return DeterministicDevelopmentPlannerProvider(
            result_folder_name=self.result_folder_name,
            target_prefix=self.target_prefix,
            allowed_request=DETERMINISTIC_BROWSER_REQUEST,
        )

    def _presentation(self, job: FolderRefactorJobV2) -> FolderRunPresentation:
        if job.final_result_path is None:
            raise ConnectedChangeJobServiceError(
                "verified_result_path_missing",
                "The verified job lacks its final result path.",
            )
        verification = self._service.verify_result(job.job_path)
        if verification.status is not ConnectedReceiptVerificationStatus.VERIFIED:
            raise ConnectedChangeJobServiceError(
                "result_verification_blocked",
                ",".join(verification.failed_check_ids),
            )
        receipt_payload = read_regular_bytes(job.final_result_path, CHANGE_RECEIPT_PATH)
        receipt = parse_portable_model(receipt_payload, FolderReceiptEnvelopeV2)
        if canonical_portable_json_bytes(receipt) != receipt_payload:
            raise ConnectedChangeJobServiceError(
                "result_receipt_noncanonical",
                "The verified receipt is not canonical JSON.",
            )
        core = receipt.receipt
        change_path, change_fingerprint, originating_receipt = (
            self._service.get_change_file(job.job_path)
        )
        if change_path != job.final_result_path / CONNECTED_CHANGE_PATH:
            raise ConnectedChangeJobServiceError(
                "change_file_path_mismatch",
                "The verified Change File path differs from the result.",
            )
        return FolderRunPresentation(
            source_root=job.source_root,
            output_parent=job.output_parent,
            result_root=job.final_result_path,
            data_root=job.final_result_path / "data",
            source_file_count=core.source_file_count,
            path_change_count=core.path_change_count,
            supported_link_count=core.supported_link_count,
            supported_link_update_count=core.rewritten_link_count,
            source_unchanged=True,
            all_files_present_once=True,
            deterministic_proof_passed=True,
            independent_verification_passed=True,
            reconstruction_available=True,
            receipt_fingerprint=receipt.receipt_fingerprint,
            change_file_fingerprint=change_fingerprint,
            originating_receipt_fingerprint=originating_receipt,
            organized_tree_commitment=core.organized_tree.commitment,
            execution_role=core.execution_role,
            technical_facts=(
                ("Job ID", job.job_id),
                ("Receipt fingerprint", receipt.receipt_fingerprint),
                ("Change File fingerprint", change_fingerprint),
                ("Organized-tree commitment", core.organized_tree.commitment),
                ("Independent verification", "Passed without GPT or source"),
            ),
        )

    def _transaction_progress(self, phase: FolderTransactionPhase) -> None:
        mapped = {
            FolderTransactionPhase.CREATING_RESULT: FolderWorkPhase.CREATING,
            FolderTransactionPhase.UPDATING_SUPPORTED_LINKS: (
                FolderWorkPhase.UPDATING_LINKS
            ),
            FolderTransactionPhase.VERIFYING_RESULT: FolderWorkPhase.VERIFYING,
        }[phase]
        self._report(mapped)

    def _report(self, phase: FolderWorkPhase) -> None:
        callback = self._progress_callback
        if callback is not None:
            callback(phase)


def _job_journey(job: FolderRefactorJobV2) -> FolderJourney:
    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
        return FolderJourney.APPLY
    return FolderJourney.ORGANIZE


def _job_blocker(job: FolderRefactorJobV2) -> str:
    if job.lifecycle is FolderJobLifecycleV2.STALE:
        return "source_or_change_file_stale: start a fresh job with unchanged inputs"
    if job.blocker_code is not None:
        return f"{job.blocker_code}: {job.blocker_message or 'transaction blocked'}"
    return f"job_not_verified: {job.lifecycle.value}"


def _web_idempotency_key(job_path: Path, operation: str) -> str:
    digest = hashlib.sha256(str(job_path).encode("utf-8")).hexdigest()
    return f"web-{operation}:{digest}"
