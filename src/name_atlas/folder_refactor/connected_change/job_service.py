"""One durable cross-surface service for Connected Change v2 jobs."""

from __future__ import annotations

import hashlib
import logging
import os
import shutil
import stat
import time
import uuid
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

from name_atlas.folder_refactor.connected_change.contracts import (
    ConnectedChangeError,
)
from name_atlas.folder_refactor.connected_change.job_io import (
    DurableJobFileLock,
    DurableJobLockError,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    DEFAULT_V2_JOB_DIRECTORY,
    CapsuleAppliedJobAuthorityV2,
    FolderJobLifecycleV2,
    FolderJobV2FinalizedError,
    FolderJobV2IdempotencyConflict,
    FolderJobV2WriteError,
    FolderJobVerifiedArtifactsV2,
    FolderRefactorJobV2,
    FolderRefactorJobV2Store,
    FolderRefactorJobV2Writer,
    GptPlannedJobAuthorityV2,
    GptPlannerCheckpointV2,
    LegacyFolderJobV1Evidence,
    build_new_capsule_job_v2,
    build_new_gpt_job_v2,
    evolve_job_v2,
    expected_final_result_path_v2,
    expected_pending_result_path_v2,
    find_idempotent_job_v2,
    load_folder_job_record,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_PATH,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV2,
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
from name_atlas.folder_refactor.inventory import FolderScan
from name_atlas.folder_refactor.planner_contracts import FolderPlannerProgress
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    canonical_portable_json_bytes,
    parse_portable_model,
    read_regular_bytes,
)
from name_atlas.folder_refactor.receipt_contracts import FolderRestoreReport
from name_atlas.folder_refactor.serialization import (
    canonical_sha256,
    request_fingerprint,
)
from name_atlas.folder_refactor.transaction import (
    FolderTransactionError,
    FolderTransactionPaths,
    FolderTransactionProgress,
)
from name_atlas.verification.promotion import promote_directory_no_replace

logger = logging.getLogger(__name__)

FolderIdempotencyScope = Literal["exact_path", "jobs_directory"]


class ConnectedChangeJobServiceError(RuntimeError):
    """One stable durable Connected Change service failure."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class ConnectedChangeJobService:
    """Create, resume, verify, and reconstruct through one v2 job authority."""

    def create_application_job(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        idempotency_key: str,
        idempotency_scope: FolderIdempotencyScope = "jobs_directory",
    ) -> FolderRefactorJobV2:
        """Persist one receiver job before deterministic matching begins."""

        candidate = build_new_capsule_job_v2(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            change_file_path=change_file_path,
            idempotency_key=idempotency_key,
        )
        return self._save_or_reuse(candidate, idempotency_scope=idempotency_scope)

    def create_planned_origin_job(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        request: str,
        idempotency_key: str,
        scan: FolderScan,
        planner_progress: FolderPlannerProgress,
        idempotency_scope: FolderIdempotencyScope = "jobs_directory",
    ) -> FolderRefactorJobV2:
        """Persist one full-progress origin job before any provider turn."""

        candidate = build_new_gpt_job_v2(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            user_request=request,
            idempotency_key=idempotency_key,
            scan=scan,
            job_id=planner_progress.job_id,
            planner_progress=planner_progress,
        )
        return self._save_or_reuse(candidate, idempotency_scope=idempotency_scope)

    def start_application(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        idempotency_key: str,
        progress_callback: FolderTransactionProgress | None = None,
        idempotency_scope: FolderIdempotencyScope = "jobs_directory",
    ) -> FolderRefactorJobV2:
        """Create or resume one provider-free receiver transaction."""

        job = self.create_application_job(
            change_file_path=change_file_path,
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            idempotency_key=idempotency_key,
            idempotency_scope=idempotency_scope,
        )
        return self.run_or_resume(
            job.job_path,
            progress_callback=progress_callback,
        )

    def start_deterministic_origin(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        job_path: Path,
        request: str,
        result_folder_name: str,
        target_by_original_path: Mapping[str, str],
        idempotency_key: str,
        progress_callback: FolderTransactionProgress | None = None,
        idempotency_scope: FolderIdempotencyScope = "jobs_directory",
    ) -> FolderRefactorJobV2:
        """Persist and execute one truthful development origin transaction."""

        candidate = build_new_gpt_job_v2(
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            user_request=request,
            idempotency_key=idempotency_key,
        )
        job = self._save_or_reuse(
            candidate,
            idempotency_scope=idempotency_scope,
        )
        if job.lifecycle is FolderJobLifecycleV2.PLANNING:
            prepared = prepare_connected_change_origin(
                job_id=job.job_id,
                source_root=job.source_root,
                request=job.user_request,
                result_folder_name=result_folder_name,
                target_by_original_path=target_by_original_path,
            )
            self._persist_origin_preparation(job.job_path, prepared)
        return self.run_or_resume(
            job.job_path,
            progress_callback=progress_callback,
        )

    def run_or_resume(
        self,
        job_path: Path,
        *,
        progress_callback: FolderTransactionProgress | None = None,
    ) -> FolderRefactorJobV2:
        """Continue one exact durable job without duplicate work."""

        store = FolderRefactorJobV2Store(job_path)
        with store.writer() as writer:
            job = writer.load()
            if job.lifecycle.terminal:
                return job
            if _promoted_result_exists(job):
                assert job.final_result_path is not None
                return self._finalize_verified(
                    writer,
                    job,
                    job.final_result_path,
                )
            job = writer.rehydrate()
            if job.lifecycle.terminal:
                return job
            try:
                if job.lifecycle is FolderJobLifecycleV2.PLANNING:
                    if not isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
                        raise ConnectedChangeJobServiceError(
                            "origin_planning_requires_planner",
                            "The GPT origin requires its persisted planner "
                            "continuation.",
                        )
                    prepared = prepare_connected_change_application(
                        change_file_path=job.authority.change_file_binding.path,
                        source_root=job.source_root,
                    )
                    job = self._persist_application_preparation(
                        writer,
                        job,
                        prepared,
                    )
                if job.lifecycle is not FolderJobLifecycleV2.EXECUTING:
                    raise ConnectedChangeJobServiceError(
                        "job_not_executable",
                        f"Job lifecycle cannot execute: {job.lifecycle.value}.",
                    )
                if job.pending_result_path is None:
                    try:
                        job = writer.begin_execution(job)
                    except FolderJobV2WriteError as exc:
                        return self._mark_blocked_or_return_terminal(
                            writer,
                            job,
                            code="result_path_unavailable",
                            message=str(exc),
                        )
                prepared = self._rehydrate_prepared(job)
                recovered = self._recover_if_possible(writer, job)
                if recovered is not None:
                    return recovered
                result = execute_prepared_connected_change(
                    prepared=prepared,
                    output_parent=job.output_parent,
                    job_id=job.job_id,
                    transaction_paths=FolderTransactionPaths(
                        job_id=job.job_id,
                        pending_root=expected_pending_result_path_v2(job),
                        final_root=expected_final_result_path_v2(job),
                    ),
                    progress_callback=progress_callback,
                )
                return self._finalize_verified(
                    writer,
                    job,
                    result.folder_run.result_root,
                )
            except (ConnectedChangeError, FolderTransactionError) as exc:
                current = writer.rehydrate()
                if current.lifecycle is FolderJobLifecycleV2.STALE:
                    return current
                code = (
                    exc.code
                    if isinstance(exc, ConnectedChangeError)
                    else "folder_transaction_blocked"
                )
                blocked = self._mark_blocked_or_return_terminal(
                    writer,
                    current,
                    code=code,
                    message=str(exc),
                )
                return blocked
            except ConnectedChangeJobServiceError as exc:
                if exc.code == "origin_planning_requires_planner":
                    raise
                current = writer.rehydrate()
                if current.lifecycle.terminal:
                    return current
                return self._mark_blocked_or_return_terminal(
                    writer,
                    current,
                    code=exc.code,
                    message=exc.message,
                )

    def status(self, job_path: Path) -> FolderRefactorJobV2:
        """Read one durable job without provider, budget, copy, or mutation."""

        record = FolderRefactorJobV2Store(job_path).inspect()
        if not isinstance(record, FolderRefactorJobV2):
            raise ConnectedChangeJobServiceError(
                "legacy_job_read_only",
                "The selected v1 job is historical read-only evidence.",
            )
        return record

    def rehydrate(self, job_path: Path) -> FolderRefactorJobV2:
        """Revalidate one job's local inputs without provider or execution work."""

        record = FolderRefactorJobV2Store(job_path).load()
        if not isinstance(record, FolderRefactorJobV2):
            raise ConnectedChangeJobServiceError(
                "legacy_job_read_only",
                "The selected v1 job is historical read-only evidence.",
            )
        return record

    def verify_result(self, job_path: Path) -> ConnectedReceiptVerification:
        """Run source-free verification for one terminal result."""

        job = self._require_verified_job(job_path)
        assert job.final_result_path is not None
        verification, _receipt = self._read_bound_verified_result(
            job,
            job.final_result_path,
        )
        return verification

    def get_change_file(self, job_path: Path) -> tuple[Path, str, str]:
        """Return the verified local Change File and its two receipt identities."""

        job = self._require_verified_job(job_path)
        assert job.final_result_path is not None
        verification, receipt = self._read_bound_verified_result(
            job,
            job.final_result_path,
        )
        change_path = job.final_result_path / CONNECTED_CHANGE_PATH
        payload = read_regular_bytes(job.final_result_path, CONNECTED_CHANGE_PATH)
        from name_atlas.folder_refactor.connected_change.descriptors import (
            parse_connected_change_file,
        )

        change_file = parse_connected_change_file(payload)
        repeated_verification, repeated_receipt = self._read_bound_verified_result(
            job,
            job.final_result_path,
        )
        if (
            repeated_verification != verification
            or repeated_receipt != receipt
            or change_file.core_fingerprint
            != receipt.receipt.connected_change_core_fingerprint
        ):
            raise ConnectedChangeJobServiceError(
                "result_changed_during_read",
                "The verified result changed while its Change File was read.",
            )
        return (
            change_path,
            change_file.change_file_fingerprint,
            change_file.originating_receipt.receipt_fingerprint,
        )

    def recreate_original(
        self,
        job_path: Path,
        destination: Path,
    ) -> FolderRestoreReport:
        """Recreate this job's own source paths through the shared engine."""

        job = self._require_verified_job(job_path)
        assert job.final_result_path is not None
        source_root = _available_real_directory(job.source_root)
        return restore_connected_result(
            job.final_result_path,
            destination,
            source_root=source_root,
        )

    def _save_or_reuse(
        self,
        candidate: FolderRefactorJobV2,
        *,
        idempotency_scope: FolderIdempotencyScope,
    ) -> FolderRefactorJobV2:
        with _idempotency_creation_lock(candidate.job_path.parent):
            if os.path.lexists(candidate.job_path):
                record = load_folder_job_record(candidate.job_path)
                if (
                    isinstance(record, LegacyFolderJobV1Evidence)
                    or record.idempotency != candidate.idempotency
                ):
                    raise FolderJobV2IdempotencyConflict(
                        "Requested job path is already bound to another mutation."
                    )
                return record
            if idempotency_scope == "jobs_directory":
                existing = find_idempotent_job_v2(
                    candidate.job_path.parent,
                    candidate.idempotency,
                )
                if existing is not None:
                    return existing
            elif idempotency_scope != "exact_path":
                raise FolderJobV2IdempotencyConflict(
                    "Unsupported durable idempotency discovery scope."
                )
            store = FolderRefactorJobV2Store(candidate.job_path)
            with store.writer() as writer:
                return writer.save_new(candidate)

    def _persist_origin_preparation(
        self,
        job_path: Path,
        prepared: PreparedConnectedChangeOrigin,
    ) -> FolderRefactorJobV2:
        store = FolderRefactorJobV2Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if job.lifecycle is not FolderJobLifecycleV2.PLANNING:
                return job
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
                ),
                evidence_ledger=ledger,
                execution_origin=prepared.execution_origin,
            )
            try:
                candidate = evolve_job_v2(
                    job,
                    authority=authority,
                    accepted_plan=prepared.accepted_plan,
                    lifecycle=FolderJobLifecycleV2.EXECUTING,
                )
            except ValueError as exc:
                return self._mark_blocked_or_return_terminal(
                    writer,
                    job,
                    code="result_path_unavailable",
                    message=str(exc),
                )
            return writer.save(candidate, expected_current=job)

    def _persist_application_preparation(
        self,
        writer: FolderRefactorJobV2Writer,
        job: FolderRefactorJobV2,
        prepared: PreparedConnectedChangeApplication,
    ) -> FolderRefactorJobV2:
        if not isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
            raise ConnectedChangeJobServiceError(
                "job_authority_mismatch",
                "Receiver preparation requires capsule authority.",
            )
        authority = CapsuleAppliedJobAuthorityV2(
            change_file_binding=job.authority.change_file_binding,
            match_report=prepared.match_report,
            execution_origin=prepared.execution_origin,
        )
        try:
            candidate = evolve_job_v2(
                job,
                authority=authority,
                accepted_plan=prepared.accepted_plan,
                lifecycle=FolderJobLifecycleV2.EXECUTING,
            )
        except ValueError as exc:
            return self._mark_blocked_or_return_terminal(
                writer,
                job,
                code="result_path_unavailable",
                message=str(exc),
            )
        return writer.save(candidate, expected_current=job)

    def _rehydrate_prepared(
        self,
        job: FolderRefactorJobV2,
    ) -> PreparedConnectedChange:
        if job.accepted_plan is None:
            raise ConnectedChangeJobServiceError(
                "accepted_plan_missing",
                "Executing job lacks an accepted plan.",
            )
        if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
            prepared = prepare_connected_change_application(
                change_file_path=job.authority.change_file_binding.path,
                source_root=job.source_root,
            )
            if (
                prepared.accepted_plan != job.accepted_plan
                or prepared.match_report != job.authority.match_report
                or prepared.execution_origin != job.authority.execution_origin
            ):
                raise ConnectedChangeJobServiceError(
                    "persisted_receiver_authority_mismatch",
                    "Receiver preparation differs from the persisted job.",
                )
            return prepared
        ledger = job.authority.evidence_ledger
        origin = job.authority.execution_origin
        if ledger is None or origin is None:
            raise ConnectedChangeJobServiceError(
                "persisted_origin_authority_missing",
                "Executing origin lacks its evidence ledger or execution origin.",
            )
        return rehydrate_prepared_connected_change_origin(
            source_root=job.source_root,
            request=job.user_request,
            accepted_plan=job.accepted_plan,
            execution_origin=origin,
            evidence_ledger=ledger,
        )

    def _recover_if_possible(
        self,
        writer: FolderRefactorJobV2Writer,
        job: FolderRefactorJobV2,
    ) -> FolderRefactorJobV2 | None:
        assert job.pending_result_path is not None
        assert job.final_result_path is not None
        pending_exists = os.path.lexists(job.pending_result_path)
        final_exists = os.path.lexists(job.final_result_path)
        if pending_exists and final_exists:
            return self._mark_blocked_or_return_terminal(
                writer,
                job,
                code="execution_recovery_ambiguous",
                message="Both persisted pending and final results exist.",
            )
        if final_exists:
            return self._finalize_verified(writer, job, job.final_result_path)
        if not pending_exists:
            return None
        metadata = job.pending_result_path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            return self._mark_blocked_or_return_terminal(
                writer,
                job,
                code="execution_recovery_ambiguous",
                message="Persisted pending result is not a real directory.",
            )
        receipt_path = job.pending_result_path / CHANGE_RECEIPT_PATH
        if os.path.lexists(receipt_path):
            verification = verify_connected_result(job.pending_result_path)
            if (
                verification.status is ConnectedReceiptVerificationStatus.VERIFIED
                and verification.job_id == job.job_id
            ):
                self._read_bound_verified_result(job, job.pending_result_path)
                current = writer.rehydrate()
                if current.lifecycle is FolderJobLifecycleV2.STALE:
                    return current
                try:
                    promote_directory_no_replace(
                        current.pending_result_path,
                        current.final_result_path,
                    )
                except (FileExistsError, OSError) as exc:
                    return self._mark_blocked_or_return_terminal(
                        writer,
                        current,
                        code="execution_recovery_promotion_blocked",
                        message=str(exc),
                    )
                assert current.final_result_path is not None
                return self._finalize_verified(
                    writer,
                    current,
                    current.final_result_path,
                )
            logger.warning(
                "Regenerating incomplete pending result path=%s checks=%s",
                job.pending_result_path,
                ",".join(verification.failed_check_ids),
            )
        current = writer.rehydrate()
        if current.lifecycle is FolderJobLifecycleV2.STALE:
            return current
        size = _directory_size(job.pending_result_path)
        logger.warning(
            "Removing regenerable incomplete pending result path=%s bytes=%d "
            "reason=restart_before_receipt regeneration=rerun_same_persisted_job",
            job.pending_result_path,
            size,
        )
        try:
            shutil.rmtree(job.pending_result_path)
        except OSError as exc:
            return self._mark_blocked_or_return_terminal(
                writer,
                current,
                code="pending_cleanup_failed",
                message=str(exc),
            )
        return None

    def _finalize_verified(
        self,
        writer: FolderRefactorJobV2Writer,
        job: FolderRefactorJobV2,
        result_root: Path,
    ) -> FolderRefactorJobV2:
        try:
            verification, receipt = self._read_bound_verified_result(
                job,
                result_root,
            )
        except ConnectedChangeJobServiceError as exc:
            return self._mark_blocked_or_return_terminal(
                writer,
                job,
                code=exc.code,
                message=exc.message,
            )
        assert verification.receipt_fingerprint is not None
        assert verification.organized_tree_commitment is not None
        return writer.finalize_verified(
            job,
            artifacts=FolderJobVerifiedArtifactsV2(
                receipt_fingerprint=verification.receipt_fingerprint,
                organized_tree_commitment=verification.organized_tree_commitment,
                change_ledger_fingerprint=receipt.receipt.change_ledger_fingerprint,
                verification_fingerprint=canonical_sha256(verification),
            ),
        )

    @staticmethod
    def _mark_blocked_or_return_terminal(
        writer: FolderRefactorJobV2Writer,
        current: FolderRefactorJobV2,
        *,
        code: str,
        message: str,
    ) -> FolderRefactorJobV2:
        """Let a concurrent input-staleness transition win without leaking it."""

        try:
            return writer.mark_blocked(current, code=code, message=message)
        except FolderJobV2FinalizedError:
            persisted = writer.load()
            if persisted.lifecycle.terminal:
                return persisted
            raise

    def _read_bound_verified_result(
        self,
        job: FolderRefactorJobV2,
        result_root: Path,
    ) -> tuple[ConnectedReceiptVerification, FolderReceiptEnvelopeV2]:
        verification = verify_connected_result(result_root)
        if (
            verification.status is not ConnectedReceiptVerificationStatus.VERIFIED
            or verification.job_id != job.job_id
            or verification.receipt_fingerprint is None
            or verification.organized_tree_commitment is None
        ):
            raise ConnectedChangeJobServiceError(
                "result_verification_blocked",
                ",".join(verification.failed_check_ids),
            )
        receipt_payload = read_regular_bytes(result_root, CHANGE_RECEIPT_PATH)
        receipt = parse_portable_model(receipt_payload, FolderReceiptEnvelopeV2)
        if canonical_portable_json_bytes(receipt) != receipt_payload:
            raise ConnectedChangeJobServiceError(
                "result_receipt_noncanonical",
                "Verified result receipt is not canonical JSON.",
            )
        mismatch = _persisted_job_result_mismatch(job, verification, receipt)
        if mismatch is not None:
            raise ConnectedChangeJobServiceError(
                "persisted_job_result_mismatch",
                mismatch,
            )
        return verification, receipt

    def _require_verified_job(self, job_path: Path) -> FolderRefactorJobV2:
        job = self.status(job_path)
        if (
            job.lifecycle is not FolderJobLifecycleV2.VERIFIED
            or job.final_result_path is None
            or job.verified_artifacts is None
        ):
            raise ConnectedChangeJobServiceError(
                "job_not_verified",
                "The requested operation requires a verified terminal job.",
            )
        return job


def default_connected_change_job_path(
    *,
    project_root: Path | None = None,
) -> Path:
    """Return one absent UUID-named v2 job path without creating it."""

    root = (Path.cwd() if project_root is None else project_root).resolve(strict=False)
    return root / DEFAULT_V2_JOB_DIRECTORY / f"{uuid.uuid4().hex}.json"


def _available_real_directory(path: Path) -> Path | None:
    """Return a current real directory only for optional overlap protection."""

    try:
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            return None
        return path.resolve(strict=True)
    except (OSError, RuntimeError):
        return None


def _directory_size(root: Path) -> int:
    total = 0
    for directory, _directory_names, file_names in os.walk(root):
        for name in file_names:
            try:
                total += (Path(directory) / name).lstat().st_size
            except OSError:
                continue
    return total


def _promoted_result_exists(job: FolderRefactorJobV2) -> bool:
    return (
        job.lifecycle is FolderJobLifecycleV2.EXECUTING
        and job.pending_result_path is not None
        and job.final_result_path is not None
        and not os.path.lexists(job.pending_result_path)
        and os.path.lexists(job.final_result_path)
    )


def _persisted_job_result_mismatch(
    job: FolderRefactorJobV2,
    verification: ConnectedReceiptVerification,
    receipt: FolderReceiptEnvelopeV2,
) -> str | None:
    plan = job.accepted_plan
    origin = job.authority.execution_origin
    if plan is None or origin is None:
        return "Persisted job lacks its accepted plan or execution origin."
    core = receipt.receipt
    expected_role = (
        "receiver"
        if isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
        else "origin"
    )
    expected_common = {
        "execution_role": expected_role,
        "job_id": job.job_id,
        "source_commitment": job.source_inventory.source_commitment,
        "source_file_count": len(job.source_inventory.files),
        "source_directory_count": job.source_inventory.directory_count,
        "source_bytes": job.source_inventory.total_bytes,
        "request_fingerprint": request_fingerprint(job.user_request),
        "evidence_fingerprint": plan.evidence_fingerprint,
        "accepted_plan_fingerprint": canonical_sha256(plan),
        "execution_origin_fingerprint": canonical_sha256(origin),
    }
    for field_name, expected in expected_common.items():
        if getattr(core, field_name) != expected:
            return f"Receipt field differs from persisted job: {field_name}."
    if (
        verification.receipt_fingerprint != receipt.receipt_fingerprint
        or verification.organized_tree_commitment != core.organized_tree.commitment
    ):
        return "Independent verification identities differ from the receipt."

    commitments = {item.path: item for item in core.artifact_commitments}
    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
        binding = job.authority.change_file_binding
        report = job.authority.match_report
        if report is None:
            return "Persisted receiver job lacks its exact match report."
        expected_receiver = {
            "connected_change_core_fingerprint": (binding.change_file.core_fingerprint),
            "imported_change_file_fingerprint": (
                binding.change_file.change_file_fingerprint
            ),
            "imported_change_file_sha256": binding.raw_sha256,
            "originating_receipt_fingerprint": (
                binding.change_file.originating_receipt.receipt_fingerprint
            ),
            "match_report_fingerprint": report.match_report_fingerprint,
            "match_report_sha256": hashlib.sha256(
                canonical_portable_json_bytes(report)
            ).hexdigest(),
        }
        for field_name, expected in expected_receiver.items():
            if getattr(core, field_name) != expected:
                return (
                    f"Receiver receipt differs from persisted authority: {field_name}."
                )
    else:
        ledger = job.authority.evidence_ledger
        if ledger is None:
            return "Persisted origin job lacks its evidence ledger."
        evidence_commitment = commitments.get("name-atlas/evidence_ledger.json")
        expected_digest = hashlib.sha256(
            canonical_portable_json_bytes(ledger)
        ).hexdigest()
        if evidence_commitment is None or evidence_commitment.sha256 != expected_digest:
            return "Origin receipt does not commit the persisted evidence ledger."

    if job.verified_artifacts is not None:
        expected_verified = job.verified_artifacts
        if (
            expected_verified.receipt_fingerprint != receipt.receipt_fingerprint
            or expected_verified.organized_tree_commitment
            != core.organized_tree.commitment
            or expected_verified.change_ledger_fingerprint
            != core.change_ledger_fingerprint
            or expected_verified.verification_fingerprint
            != canonical_sha256(verification)
        ):
            return "Current result differs from the job's terminal proof identities."
    return None


@contextmanager
def _idempotency_creation_lock(jobs_directory: Path) -> Iterator[None]:
    lock_target = jobs_directory.resolve(strict=False) / ".idempotency-creation"
    deadline = time.monotonic() + 5.0
    lock: DurableJobFileLock | None = None
    while lock is None:
        candidate = DurableJobFileLock(lock_target)
        try:
            candidate.__enter__()
        except DurableJobLockError as exc:
            if time.monotonic() >= deadline:
                raise FolderJobV2IdempotencyConflict(
                    "Durable idempotency creation is busy; retry the same request."
                ) from exc
            time.sleep(0.01)
        else:
            lock = candidate
    try:
        yield
    finally:
        lock.__exit__(None, None, None)
