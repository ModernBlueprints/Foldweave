"""Foldweave review orchestration over the single Connected Change engine."""

from __future__ import annotations

import os
import uuid
from collections.abc import Mapping
from datetime import datetime
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from name_atlas.folder_refactor.connected_change.contracts import (
    ConnectedChangeError,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file,
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
    build_execution_authorization,
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
from name_atlas.folder_refactor.portable_artifacts import (
    canonical_portable_json_bytes,
)
from name_atlas.folder_refactor.receipt_contracts import FolderRestoreReport
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.folder_refactor.transaction import (
    FolderTransactionError,
    FolderTransactionPaths,
    FolderTransactionProgress,
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
