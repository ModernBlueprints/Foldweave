"""Thin durable coordination layer for the shared Name Atlas MCP server."""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import stat
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from name_atlas.connected_planner_runtime import PROJECT_ROOT
from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
    ConnectedChangeJobServiceError,
    default_connected_change_job_path,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    DEFAULT_V2_JOB_DIRECTORY,
    CapsuleAppliedJobAuthorityV2,
    FolderJobLifecycleV2,
    FolderJobV2Error,
    FolderJobV2IdempotencyConflict,
    FolderJobV2LockError,
    FolderRefactorJobV2,
    FolderRefactorJobV2Store,
    GptPlannedJobAuthorityV2,
    LegacyFolderJobV1Evidence,
    load_folder_job_record,
    require_operation_idempotency,
)
from name_atlas.folder_refactor.connected_change.planning import (
    ConnectedOriginPlanningService,
    clarification_question_fingerprint,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.mcp_contracts import (
    AnswerClarificationRequest,
    ApplyChangeFileRequest,
    JobHandleRequest,
    McpChangeFileResult,
    McpJobStatus,
    McpReconstructionResult,
    McpVerificationResult,
    PlanAndCreateCopyRequest,
    RecreateOriginalRequest,
    VerifyResultRequest,
)

LOGGER = logging.getLogger(__name__)

_LOCK_RETRY_ATTEMPTS = 120
_LOCK_RETRY_SECONDS = 0.5

CONSENT_MESSAGE = (
    "Your original folder will not be changed. Name Atlas will create and verify "
    "a separate result. It sends GPT-5.6 your instruction, relative file names "
    "and folder structure, basic file metadata used to bind the plan, selected "
    "excerpts from eligible text and Markdown files, and supported Markdown-link "
    "context needed to plan the change. It does not send every file's bytes. Raw "
    "content hashes are kept local. Name Atlas sets store=false, so it does not "
    "ask OpenAI to store the generated response for later retrieval through the "
    "Responses API. OpenAI's standard abuse-monitoring and prompt-caching "
    "retention may still apply."
)


class McpServiceError(RuntimeError):
    """One stable MCP-adapter failure with no duplicated domain authority."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(slots=True)
class _RunningOperation:
    request_fingerprint: str
    task: asyncio.Task[None]


class _OperationRegistry:
    """Process-local scheduling only; durable jobs remain the sole authority."""

    def __init__(self) -> None:
        self._operations: dict[str, _RunningOperation] = {}
        self._lock = asyncio.Lock()

    async def launch(
        self,
        *,
        job_id: str,
        request_fingerprint: str,
        operation: Callable[[], Awaitable[None]],
    ) -> bool:
        """Launch at most one identical operation for a job in this process."""

        async with self._lock:
            existing = self._operations.get(job_id)
            if existing is not None and not existing.task.done():
                if existing.request_fingerprint == request_fingerprint:
                    return False

                async def run_after_existing() -> None:
                    with contextlib.suppress(Exception):
                        await existing.task
                    await operation()

                task = asyncio.create_task(
                    run_after_existing(),
                    name=f"name-atlas-mcp-{job_id}-continuation",
                )
                self._operations[job_id] = _RunningOperation(
                    request_fingerprint=request_fingerprint,
                    task=task,
                )
                task.add_done_callback(
                    lambda completed, *, identifier=job_id: self._completed(
                        identifier,
                        completed,
                    )
                )
                return True
            task = asyncio.create_task(
                operation(),
                name=f"name-atlas-mcp-{job_id}",
            )
            running = _RunningOperation(
                request_fingerprint=request_fingerprint,
                task=task,
            )
            self._operations[job_id] = running
            task.add_done_callback(
                lambda completed, *, identifier=job_id: self._completed(
                    identifier,
                    completed,
                )
            )
            return True

    def active(self, job_id: str) -> bool:
        """Return process liveness without treating it as workflow state."""

        running = self._operations.get(job_id)
        return running is not None and not running.task.done()

    async def wait(self) -> None:
        """Wait for every operation owned by this process to reach a safe state."""

        while True:
            async with self._lock:
                tasks = tuple(
                    running.task
                    for running in self._operations.values()
                    if not running.task.done()
                )
            if not tasks:
                return
            await asyncio.gather(*tasks, return_exceptions=True)

    def _completed(self, job_id: str, task: asyncio.Task[None]) -> None:
        current = self._operations.get(job_id)
        if current is not None and current.task is task:
            self._operations.pop(job_id, None)
        try:
            task.result()
        except asyncio.CancelledError:
            LOGGER.warning("MCP operation cancelled job_id=%s", job_id)
        except Exception:
            LOGGER.exception("MCP operation failed job_id=%s", job_id)


class NameAtlasMcpService:
    """Coordinate exactly seven high-level tools over existing domain services."""

    def __init__(
        self,
        *,
        project_root: Path = PROJECT_ROOT,
        job_service: ConnectedChangeJobService | None = None,
    ) -> None:
        self._project_root = project_root.expanduser().resolve(strict=False)
        self._jobs_directory = self._project_root / DEFAULT_V2_JOB_DIRECTORY
        self._jobs = job_service or ConnectedChangeJobService()
        self._operations = _OperationRegistry()

    async def recover_nonterminal_jobs(self) -> int:
        """Schedule durable work abandoned by an earlier STDIO process."""

        if not self._jobs_directory.exists():
            return 0
        try:
            records = await asyncio.to_thread(self._job_records)
        except Exception:  # noqa: BLE001 - diagnostics stay on STDERR
            LOGGER.exception("Could not inspect durable jobs during MCP startup")
            return 0

        scheduled = 0
        for job in records:
            if job.lifecycle.terminal or (
                job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION
            ):
                continue
            try:
                if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
                    await self._schedule_application_if_needed(job)
                else:
                    await self._schedule_origin_if_needed(job)
            except McpServiceError as exc:
                if exc.code == "live_credential_missing":
                    LOGGER.warning(
                        "Live MCP job awaits local credential job_id=%s",
                        job.job_id,
                    )
                    continue
                LOGGER.warning(
                    "MCP startup left unsupported job idle job_id=%s code=%s",
                    job.job_id,
                    exc.code,
                )
                continue
            scheduled += 1
        return scheduled

    async def wait_for_operations(self) -> None:
        """Keep normal server shutdown from abandoning an owned writer."""

        await self._operations.wait()

    async def plan_and_create_copy(
        self,
        request: PlanAndCreateCopyRequest,
    ) -> McpJobStatus:
        """Persist a consented origin job and schedule its bounded planner."""

        if request.evidence_disclosure_acknowledged is not True:
            return McpJobStatus(
                status="consent_required",
                message=CONSENT_MESSAGE,
            )
        try:
            candidate_source = _canonical_input_path(
                request.source_root,
                label="source_root",
            )
            candidate_output = (
                candidate_source.parent
                if request.output_parent is None
                else _canonical_input_path(
                    request.output_parent,
                    label="output_parent",
                )
            )
            existing = self._find_job_for_key(request.idempotency_key)
            if existing is not None:
                self._require_origin_retry(
                    existing,
                    source_root=candidate_source,
                    output_parent=candidate_output,
                    user_request=request.user_request,
                    mode=request.mode,
                )
                await self._schedule_origin_if_needed(existing)
                return self._project_job(existing)
            source_root = _require_directory(request.source_root, label="source_root")
            output_parent = (
                source_root.parent
                if request.output_parent is None
                else _require_directory(request.output_parent, label="output_parent")
            )
            if (
                request.mode == "live"
                and not os.environ.get(
                    "OPENAI_API_KEY",
                    "",
                ).strip()
            ):
                raise McpServiceError(
                    "live_credential_missing",
                    "Live GPT-5.6 planning requires OPENAI_API_KEY in the local "
                    "server environment.",
                )
            planner = ConnectedOriginPlanningService(job_service=self._jobs)
            job = await asyncio.to_thread(
                planner.create,
                source_root=source_root,
                output_parent=output_parent,
                job_path=default_connected_change_job_path(
                    project_root=self._project_root
                ),
                request=request.user_request,
                idempotency_key=request.idempotency_key,
                provider_kind=("live" if request.mode == "live" else "recorded_replay"),
                idempotency_scope="jobs_directory",
            )
            self._require_origin_retry(
                job,
                source_root=source_root,
                output_parent=output_parent,
                user_request=request.user_request,
                mode=request.mode,
            )
            await self._schedule_origin_if_needed(job)
            return self._project_job(job)
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            return self._blocked_job(exc)

    async def job_status(self, request: JobHandleRequest) -> McpJobStatus:
        """Read one exact durable job without mutation or continuation."""

        try:
            job = await asyncio.to_thread(self._resolve_handle, request.job_handle)
            job = await asyncio.to_thread(self._jobs.status, job.job_path)
            return self._project_job(job)
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            return self._blocked_job(exc)

    async def answer_clarification(
        self,
        request: AnswerClarificationRequest,
    ) -> McpJobStatus:
        """Persist one exact answer, then resume its already-bound provider."""

        try:
            job = await asyncio.to_thread(self._resolve_handle, request.job_handle)
            operation_request = {
                "job_handle": job.job_id,
                "expected_revision": request.expected_revision,
                "question_fingerprint": request.question_fingerprint,
                "answer": request.answer,
            }
            matching_answer = tuple(
                item
                for item in job.operation_idempotency
                if item.operation == "answer_clarification"
            )
            if matching_answer:
                require_operation_idempotency(
                    job,
                    operation="answer_clarification",
                    idempotency_key=request.idempotency_key,
                    request=operation_request,
                )
                if job.lifecycle.terminal:
                    return self._project_job(job)
                if job.lifecycle is FolderJobLifecycleV2.EXECUTING:
                    await self._schedule_origin_if_needed(job)
                    return self._project_job(job)
            mode = _provider_mode(job)
            if mode == "live" and not os.environ.get("OPENAI_API_KEY", "").strip():
                raise McpServiceError(
                    "live_credential_missing",
                    "Live GPT-5.6 continuation requires OPENAI_API_KEY in the "
                    "local server environment.",
                )
            planner = ConnectedOriginPlanningService(job_service=self._jobs)
            persisted = await asyncio.to_thread(
                planner.persist_clarification_answer,
                job.job_path,
                answer=request.answer,
                idempotency_key=request.idempotency_key,
                expected_revision=request.expected_revision,
                expected_question_fingerprint=request.question_fingerprint,
            )
            if persisted.lifecycle in {
                FolderJobLifecycleV2.PLANNING,
                FolderJobLifecycleV2.EXECUTING,
            }:
                answer_fingerprint = canonical_sha256(
                    {
                        "domain": "name-atlas:mcp-clarification-answer:v1",
                        "job_id": persisted.job_id,
                        "question_fingerprint": request.question_fingerprint,
                        "answer": request.answer,
                    }
                )
                await self._operations.launch(
                    job_id=persisted.job_id,
                    request_fingerprint=answer_fingerprint,
                    operation=lambda: self._resume_origin(persisted.job_path),
                )
            return self._project_job(persisted)
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            return self._blocked_job(exc)

    async def get_change_file(
        self,
        request: JobHandleRequest,
    ) -> McpChangeFileResult:
        """Return only verified Change File identities, never payload bytes."""

        try:
            job = await asyncio.to_thread(self._resolve_handle, request.job_handle)
            path, fingerprint, originating_receipt = await asyncio.to_thread(
                self._jobs.get_change_file,
                job.job_path,
            )
            return McpChangeFileResult(
                status="verified",
                message="Verified Name Atlas Change File is ready.",
                job_handle=job.job_id,
                change_file_path=str(path),
                change_file_fingerprint=fingerprint,
                originating_receipt_fingerprint=originating_receipt,
            )
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            code, message = _error_details(exc)
            return McpChangeFileResult(
                status="blocked",
                message=message,
                job_handle=request.job_handle,
                blocker_code=code,
            )

    async def apply_change_file(
        self,
        request: ApplyChangeFileRequest,
    ) -> McpJobStatus:
        """Persist and schedule one keyless deterministic receiver job."""

        try:
            candidate_change_file = _canonical_input_path(
                request.change_file_path,
                label="change_file_path",
            )
            candidate_source = _canonical_input_path(
                request.source_root,
                label="source_root",
            )
            candidate_output = (
                candidate_source.parent
                if request.output_parent is None
                else _canonical_input_path(
                    request.output_parent,
                    label="output_parent",
                )
            )
            existing = self._find_job_for_key(request.idempotency_key)
            if existing is not None:
                self._require_application_retry(
                    existing,
                    change_file_path=candidate_change_file,
                    source_root=candidate_source,
                    output_parent=candidate_output,
                )
                await self._schedule_application_if_needed(existing)
                return self._project_job(existing)
            change_file_path = _require_file(
                request.change_file_path,
                label="change_file_path",
            )
            source_root = _require_directory(request.source_root, label="source_root")
            output_parent = (
                source_root.parent
                if request.output_parent is None
                else _require_directory(request.output_parent, label="output_parent")
            )
            job = await asyncio.to_thread(
                self._jobs.create_application_job,
                change_file_path=change_file_path,
                source_root=source_root,
                output_parent=output_parent,
                job_path=default_connected_change_job_path(
                    project_root=self._project_root
                ),
                idempotency_key=request.idempotency_key,
                idempotency_scope="jobs_directory",
            )
            self._require_application_retry(
                job,
                change_file_path=change_file_path,
                source_root=source_root,
                output_parent=output_parent,
            )
            await self._schedule_application_if_needed(job)
            return self._project_job(job)
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            return self._blocked_job(exc)

    async def verify_result(
        self,
        request: VerifyResultRequest,
    ) -> McpVerificationResult:
        """Run the independent source-free verifier without any local job."""

        try:
            result_root = _require_directory(request.result_root, label="result_root")
            verification = await asyncio.to_thread(
                verify_connected_result,
                result_root,
            )
            if verification.status is ConnectedReceiptVerificationStatus.VERIFIED:
                return McpVerificationResult(
                    status="verified",
                    message="Independent source-free verification passed.",
                    result_root=str(result_root),
                    job_id=verification.job_id,
                    receipt_fingerprint=verification.receipt_fingerprint,
                    organized_tree_commitment=(verification.organized_tree_commitment),
                )
            return McpVerificationResult(
                status="blocked",
                message="Independent verification blocked the candidate result.",
                result_root=str(result_root),
                failed_check_ids=verification.failed_check_ids,
            )
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            code, message = _error_details(exc)
            return McpVerificationResult(
                status="blocked",
                message=message,
                result_root=request.result_root,
                failed_check_ids=(code,),
            )

    async def recreate_original(
        self,
        request: RecreateOriginalRequest,
    ) -> McpReconstructionResult:
        """Recreate one fixed sibling destination without overwriting anything."""

        result_root = ""
        destination = ""
        try:
            job = await asyncio.to_thread(self._resolve_handle, request.job_handle)
            require_operation_idempotency(
                job,
                operation="recreate_original",
                idempotency_key=request.idempotency_key,
                request={"job_handle": job.job_id},
            )
            if job.lifecycle is not FolderJobLifecycleV2.VERIFIED:
                raise McpServiceError(
                    "job_not_verified",
                    "Reconstruction requires a verified terminal job.",
                )
            if job.final_result_path is None or job.verified_artifacts is None:
                raise McpServiceError(
                    "verified_job_incomplete",
                    "The verified job lacks its complete result authority.",
                )
            result_root = str(job.final_result_path)
            restore_destination = job.final_result_path.parent / (
                f"{job.final_result_path.name}-original-layout"
            )
            destination = str(restore_destination)
            if os.path.lexists(restore_destination):
                return await asyncio.to_thread(
                    self._verify_existing_reconstruction,
                    job,
                    restore_destination,
                )
            report = await asyncio.to_thread(
                self._jobs.recreate_original,
                job.job_path,
                restore_destination,
            )
            return McpReconstructionResult(
                status="verified",
                message="Original layout was recreated and verified.",
                result_root=result_root,
                destination=str(report.destination),
                receipt_fingerprint=report.receipt_fingerprint,
                source_commitment=report.source_commitment,
                restored_file_count=report.restored_file_count,
                restored_bytes=report.restored_bytes,
                restored_empty_directory_count=(report.restored_empty_directory_count),
            )
        except Exception as exc:  # noqa: BLE001 - translate the bounded tool edge
            code, message = _error_details(exc)
            return McpReconstructionResult(
                status="blocked",
                message=message,
                result_root=result_root,
                destination=destination,
                blocker_code=code,
            )

    async def _resume_origin(self, job_path: Path) -> None:
        for attempt in range(_LOCK_RETRY_ATTEMPTS):
            try:
                await asyncio.to_thread(_resume_origin_worker, job_path)
                return
            except FolderJobV2LockError:
                if attempt + 1 == _LOCK_RETRY_ATTEMPTS:
                    LOGGER.warning(
                        "MCP origin recovery remains owned elsewhere job=%s",
                        job_path.name,
                    )
                    return
                await asyncio.sleep(_LOCK_RETRY_SECONDS)
            except Exception:  # noqa: BLE001 - persist a bounded terminal failure
                LOGGER.exception("MCP origin background operation failed")
                await self._persist_background_blocker(
                    job_path,
                    code="planner_background_failed",
                    message=(
                        "The persisted planner could not be resumed. Start a fresh "
                        "job after checking the selected mode and bundled recording."
                    ),
                )
                return

    async def _resume_application(self, job_path: Path) -> None:
        for attempt in range(_LOCK_RETRY_ATTEMPTS):
            try:
                await asyncio.to_thread(self._jobs.run_or_resume, job_path)
                return
            except FolderJobV2LockError:
                if attempt + 1 == _LOCK_RETRY_ATTEMPTS:
                    LOGGER.warning(
                        "MCP receiver recovery remains owned elsewhere job=%s",
                        job_path.name,
                    )
                    return
                await asyncio.sleep(_LOCK_RETRY_SECONDS)
            except Exception:  # noqa: BLE001 - persist a bounded terminal failure
                LOGGER.exception("MCP receiver background operation failed")
                await self._persist_background_blocker(
                    job_path,
                    code="application_background_failed",
                    message=(
                        "The persisted shared-change application could not be resumed."
                    ),
                )
                return

    async def _schedule_origin_if_needed(self, job: FolderRefactorJobV2) -> None:
        if job.lifecycle.terminal or (
            job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION
        ):
            return
        if job.lifecycle is FolderJobLifecycleV2.PLANNING:
            mode = _provider_mode(job)
            if mode == "live" and not os.environ.get("OPENAI_API_KEY", "").strip():
                raise McpServiceError(
                    "live_credential_missing",
                    "Live GPT-5.6 planning requires OPENAI_API_KEY in the local "
                    "server environment.",
                )
        await self._operations.launch(
            job_id=job.job_id,
            request_fingerprint=job.idempotency.request_fingerprint,
            operation=lambda: self._resume_origin(job.job_path),
        )

    async def _schedule_application_if_needed(
        self,
        job: FolderRefactorJobV2,
    ) -> None:
        if job.lifecycle.terminal:
            return
        await self._operations.launch(
            job_id=job.job_id,
            request_fingerprint=job.idempotency.request_fingerprint,
            operation=lambda: self._resume_application(job.job_path),
        )

    async def _persist_background_blocker(
        self,
        job_path: Path,
        *,
        code: str,
        message: str,
    ) -> None:
        try:
            await asyncio.to_thread(
                self._persist_background_blocker_sync,
                job_path,
                code,
                message,
            )
        except FolderJobV2LockError:
            LOGGER.info(
                "Another process owns failure resolution job=%s",
                job_path.name,
            )
        except Exception:  # noqa: BLE001 - diagnostics stay on STDERR
            LOGGER.exception("Could not persist MCP background blocker")

    @staticmethod
    def _persist_background_blocker_sync(
        job_path: Path,
        code: str,
        message: str,
    ) -> None:
        store = FolderRefactorJobV2Store(job_path)
        with store.writer() as writer:
            job = writer.rehydrate()
            if job.lifecycle.terminal:
                return
            writer.mark_blocked(job, code=code, message=message)

    def _find_job_for_key(self, key: str) -> FolderRefactorJobV2 | None:
        if not self._jobs_directory.exists():
            return None
        key_sha256 = _idempotency_key_sha256(key)
        match: FolderRefactorJobV2 | None = None
        for record in self._job_records():
            if record.idempotency.key_sha256 != key_sha256:
                continue
            if match is not None:
                raise McpServiceError(
                    "idempotency_key_ambiguous",
                    "More than one durable job uses this idempotency key.",
                )
            match = record
        return match

    @staticmethod
    def _require_origin_retry(
        job: FolderRefactorJobV2,
        *,
        source_root: Path,
        output_parent: Path,
        user_request: str,
        mode: Literal["live", "replay"],
    ) -> None:
        expected_provider = "live" if mode == "live" else "replay"
        if (
            not isinstance(job.authority, GptPlannedJobAuthorityV2)
            or job.source_root != source_root
            or job.output_parent != output_parent
            or job.user_request != user_request
            or _provider_mode(job) != expected_provider
        ):
            raise McpServiceError(
                "idempotency_key_conflict",
                "This idempotency key is bound to another exact origin request.",
            )

    @staticmethod
    def _require_application_retry(
        job: FolderRefactorJobV2,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> None:
        if (
            not isinstance(job.authority, CapsuleAppliedJobAuthorityV2)
            or job.authority.change_file_binding.path != change_file_path
            or job.source_root != source_root
            or job.output_parent != output_parent
        ):
            raise McpServiceError(
                "idempotency_key_conflict",
                "This idempotency key is bound to another exact receiver request.",
            )

    def _job_records(self) -> tuple[FolderRefactorJobV2, ...]:
        metadata = self._jobs_directory.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise McpServiceError(
                "jobs_directory_invalid",
                "The durable Name Atlas jobs directory is unavailable.",
            )
        records = []
        for candidate_path in sorted(
            self._jobs_directory.glob("*.json"),
            key=lambda candidate: candidate.name,
        ):
            record = load_folder_job_record(candidate_path)
            if isinstance(record, LegacyFolderJobV1Evidence):
                continue
            records.append(record)
        return tuple(records)

    def _resolve_handle(self, job_handle: str) -> FolderRefactorJobV2:
        if not self._jobs_directory.exists():
            raise McpServiceError(
                "job_not_found",
                "No durable Name Atlas job matches this handle.",
            )
        match: FolderRefactorJobV2 | None = None
        for record in self._job_records():
            if record.job_id != job_handle:
                continue
            if match is not None:
                raise McpServiceError(
                    "job_handle_ambiguous",
                    "More than one durable job matches this handle.",
                )
            match = record
        if match is None:
            raise McpServiceError(
                "job_not_found",
                "No durable Name Atlas job matches this handle.",
            )
        return match

    def _project_job(self, job: FolderRefactorJobV2) -> McpJobStatus:
        provider_kind = None
        question = None
        question_fingerprint = None
        active_operation = self._operations.active(job.job_id)
        if isinstance(job.authority, GptPlannedJobAuthorityV2):
            progress = job.authority.planner_checkpoint.progress
            provider_kind = (
                progress.provider_kind
                if progress is not None
                else (
                    job.authority.evidence_ledger.provider_kind
                    if job.authority.evidence_ledger is not None
                    else "deterministic"
                )
            )
            if job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
                question = job.authority.planner_checkpoint.clarification_question
                if question is not None:
                    question_fingerprint = clarification_question_fingerprint(
                        job_id=job.job_id,
                        question=question,
                    )
        blocked = job.lifecycle in {
            FolderJobLifecycleV2.BLOCKED,
            FolderJobLifecycleV2.STALE,
        }
        return McpJobStatus(
            status="blocked" if blocked else "accepted",
            message=_job_message(job, active_operation=active_operation),
            job_handle=job.job_id,
            job_id=job.job_id,
            revision=job.revision,
            lifecycle=job.lifecycle.value,
            execution_origin=job.authority.kind,
            provider_kind=provider_kind,
            active_operation=active_operation,
            clarification_question=question,
            clarification_question_fingerprint=question_fingerprint,
            result_root=(
                str(job.final_result_path)
                if job.final_result_path is not None
                else None
            ),
            receipt_fingerprint=(
                job.verified_artifacts.receipt_fingerprint
                if job.verified_artifacts is not None
                else None
            ),
            organized_tree_commitment=(
                job.verified_artifacts.organized_tree_commitment
                if job.verified_artifacts is not None
                else None
            ),
            blocker_code=(
                job.blocker_code
                or (
                    "source_or_change_file_stale"
                    if job.lifecycle is FolderJobLifecycleV2.STALE
                    else None
                )
            ),
        )

    def _blocked_job(self, exc: Exception) -> McpJobStatus:
        code, message = _error_details(exc)
        return McpJobStatus(
            status="blocked",
            message=message,
            blocker_code=code,
        )

    def _verify_existing_reconstruction(
        self,
        job: FolderRefactorJobV2,
        destination: Path,
    ) -> McpReconstructionResult:
        metadata = destination.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise McpServiceError(
                "reconstruction_destination_conflict",
                "The fixed reconstruction destination is not a real directory.",
            )
        observed = scan_folder(destination).inventory
        if observed != job.source_inventory:
            raise McpServiceError(
                "reconstruction_destination_conflict",
                "The existing reconstruction destination differs from the "
                "committed original layout.",
            )
        assert job.final_result_path is not None
        assert job.verified_artifacts is not None
        verification = verify_connected_result(job.final_result_path)
        if verification.status is not ConnectedReceiptVerificationStatus.VERIFIED:
            raise McpServiceError(
                "result_verification_blocked",
                ",".join(verification.failed_check_ids),
            )
        return McpReconstructionResult(
            status="verified",
            message="Existing original-layout reconstruction still verifies.",
            result_root=str(job.final_result_path),
            destination=str(destination),
            receipt_fingerprint=job.verified_artifacts.receipt_fingerprint,
            source_commitment=job.source_inventory.source_commitment,
            restored_file_count=len(job.source_inventory.files),
            restored_bytes=job.source_inventory.total_bytes,
            restored_empty_directory_count=len(job.source_inventory.empty_directories),
        )


def _resume_origin_worker(job_path: Path) -> None:
    """Construct the persisted provider and run it on one worker-thread loop."""

    job = ConnectedChangeJobService().status(job_path)
    if job.lifecycle.terminal or (
        job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION
    ):
        return
    if job.lifecycle is FolderJobLifecycleV2.EXECUTING:
        ConnectedChangeJobService().run_or_resume(job_path)
        return
    from name_atlas.connected_planner_runtime import provider_for_persisted_job

    provider = provider_for_persisted_job(job_path)
    asyncio.run(
        ConnectedOriginPlanningService().resume(
            job_path,
            provider=provider,
        )
    )


def _require_directory(value: str, *, label: str) -> Path:
    lexical = _absolute_lexical_path(value, label=label)
    try:
        lexical_metadata = lexical.lstat()
        if stat.S_ISLNK(lexical_metadata.st_mode):
            raise McpServiceError(
                f"{label}_invalid",
                f"{label} cannot be a symbolic link.",
            )
        path = lexical.resolve(strict=True)
        metadata = path.lstat()
    except McpServiceError:
        raise
    except (OSError, RuntimeError) as exc:
        raise McpServiceError(
            f"{label}_unavailable",
            f"{label} must be an existing readable directory.",
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise McpServiceError(
            f"{label}_invalid",
            f"{label} must be a real directory.",
        )
    return path


def _require_file(value: str, *, label: str) -> Path:
    lexical = _absolute_lexical_path(value, label=label)
    try:
        lexical_metadata = lexical.lstat()
        if stat.S_ISLNK(lexical_metadata.st_mode):
            raise McpServiceError(
                f"{label}_invalid",
                f"{label} cannot be a symbolic link.",
            )
        path = lexical.resolve(strict=True)
        metadata = path.lstat()
    except McpServiceError:
        raise
    except (OSError, RuntimeError) as exc:
        raise McpServiceError(
            f"{label}_unavailable",
            f"{label} must be an existing readable regular file.",
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise McpServiceError(
            f"{label}_invalid",
            f"{label} must be a real regular file.",
        )
    return path


def _absolute_lexical_path(value: str, *, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise McpServiceError(
            f"{label}_not_absolute",
            f"{label} must be an absolute local path.",
        )
    return path


def _canonical_input_path(value: str, *, label: str) -> Path:
    """Canonicalize an absolute retry path without requiring it to still exist."""

    lexical = _absolute_lexical_path(value, label=label)
    try:
        return lexical.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise McpServiceError(
            f"{label}_unavailable",
            f"{label} cannot be resolved as a local path.",
        ) from exc


def _idempotency_key_sha256(key: str) -> str:
    return canonical_sha256(
        {
            "domain": "name-atlas:folder-idempotency-key:v2",
            "key": key,
        }
    )


def _provider_mode(job: FolderRefactorJobV2) -> Literal["live", "replay"]:
    if not isinstance(job.authority, GptPlannedJobAuthorityV2):
        raise McpServiceError(
            "planner_authority_mismatch",
            "Clarification requires GPT-planned job authority.",
        )
    progress = job.authority.planner_checkpoint.progress
    provider_kind = (
        progress.provider_kind
        if progress is not None
        else (
            job.authority.evidence_ledger.provider_kind
            if job.authority.evidence_ledger is not None
            else None
        )
    )
    if provider_kind == "live":
        return "live"
    if provider_kind == "recorded_replay":
        return "replay"
    raise McpServiceError(
        "planner_provider_origin_mismatch",
        "The durable job is not bound to live or recorded GPT-5.6 planning.",
    )


def _job_message(
    job: FolderRefactorJobV2,
    *,
    active_operation: bool,
) -> str:
    if job.lifecycle is FolderJobLifecycleV2.PLANNING:
        if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
            return "Durable job is matching the shared change to this folder."
        mode = _provider_mode(job)
        if mode == "replay":
            return "Recorded GPT-5.6 planning run is in progress."
        if not active_operation and not os.environ.get("OPENAI_API_KEY", "").strip():
            return (
                "Live GPT-5.6 planning is paused because OPENAI_API_KEY is not "
                "available in the local server environment. Configure it, then "
                "repeat the exact plan_and_create_copy request and idempotency key."
            )
        return "Live GPT-5.6 planning is in progress."
    if job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
        return "Durable job is waiting for one clarification answer."
    if job.lifecycle is FolderJobLifecycleV2.EXECUTING:
        if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
            return "The shared change is being matched, copied, and verified."
        return "The accepted plan is being copied and verified."
    if job.lifecycle is FolderJobLifecycleV2.VERIFIED:
        return "The separate result is complete and independently verified."
    if job.lifecycle is FolderJobLifecycleV2.STALE:
        return "The source or Change File changed; start a fresh job."
    return job.blocker_message or "The durable Name Atlas job is blocked."


def _error_details(exc: Exception) -> tuple[str, str]:
    if isinstance(exc, McpServiceError | ConnectedChangeJobServiceError):
        return exc.code, exc.message
    if isinstance(exc, FolderJobV2IdempotencyConflict):
        return (
            "idempotency_key_conflict",
            "The idempotency key is bound to another exact mutation request.",
        )
    if isinstance(exc, FolderJobV2Error):
        return (
            "durable_job_rejected",
            "The durable Name Atlas job rejected this operation.",
        )
    LOGGER.exception("Unexpected MCP operation failure")
    code = "mcp_internal_failure"
    safe_code = "".join(
        character
        if character.islower() or character.isdigit() or character in "_:-"
        else "_"
        for character in code.lower()
    )[:128]
    return (
        safe_code or "mcp_internal_failure",
        "Name Atlas could not complete the operation. Check the local server "
        "diagnostics and retry only the same exact request.",
    )
