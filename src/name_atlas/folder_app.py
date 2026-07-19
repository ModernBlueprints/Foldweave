"""Server-rendered Organize and Apply journeys for connected folders."""

from __future__ import annotations

import asyncio
import hmac
import os
import secrets
from collections.abc import AsyncIterator, Callable, Coroutine
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Protocol, TypeVar, runtime_checkable
from urllib.parse import parse_qs, urlsplit

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.trustedhost import TrustedHostMiddleware

from name_atlas.folder_refactor.receipt_contracts import (
    FolderRestoreReport,
)
from name_atlas.native_bridge import (
    MacOSNativePathBridge,
    NativeOpenStatus,
    NativePathBridge,
    NativePathRole,
    NativeSelectionStatus,
)

PACKAGE_ROOT = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=PACKAGE_ROOT / "templates")
MAX_FORM_BODY_BYTES = 32_768
MAX_REQUEST_CHARACTERS = 8_000
PLANNER_LABEL = "Deterministic A3 planner — no API call"
ORGANIZE_WORKING_STAGES = (
    "Reading folder",
    "GPT-5.6 is planning",
    "Checking every file and destination",
    "Creating the new folder",
    "Updating supported links",
    "Verifying the result",
)
DEVELOPMENT_WORKING_STAGES = (
    "Reading folder",
    "Deterministic planning — no API call",
    "Checking every file and destination",
    "Creating the new folder",
    "Updating supported links",
    "Verifying the result",
)
APPLY_WORKING_STAGES = (
    "Reading folder",
    "Matching the shared change",
    "Checking every file and destination",
    "Creating the new folder",
    "Updating supported links",
    "Verifying the result",
)
WORKING_STAGES = ORGANIZE_WORKING_STAGES
_ServiceResult = TypeVar("_ServiceResult")


class FolderWebLifecycle(StrEnum):
    """Server-owned A1–A3 presentation states."""

    IDLE = "idle"
    PLANNING = "planning"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    VERIFIED = "verified"
    BLOCKED = "blocked"


class FolderJourney(StrEnum):
    """The two truthful browser transactions."""

    ORGANIZE = "organize"
    APPLY = "apply"


class FolderWorkPhase(StrEnum):
    """Coarse presentation phases reported by one durable service authority."""

    READING = "reading"
    PLANNING = "planning"
    CHECKING = "checking"
    CREATING = "creating"
    UPDATING_LINKS = "updating_links"
    VERIFYING = "verifying"


FolderProgressCallback = Callable[[FolderWorkPhase], None]


@dataclass(frozen=True, slots=True)
class FolderRunPresentation:
    """Plain facts returned by an injected folder transaction service."""

    source_root: Path
    output_parent: Path
    result_root: Path
    data_root: Path
    source_file_count: int
    path_change_count: int
    source_unchanged: bool
    all_files_present_once: bool
    deterministic_proof_passed: bool
    supported_link_count: int = 0
    supported_link_update_count: int = 0
    independent_verification_passed: bool = False
    reconstruction_available: bool = False
    receipt_fingerprint: str | None = None
    change_file_fingerprint: str | None = None
    originating_receipt_fingerprint: str | None = None
    organized_tree_commitment: str | None = None
    execution_role: str | None = None
    technical_facts: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        """Reject presentation claims that are malformed or internally unsafe."""

        for field_name in ("source_root", "output_parent", "result_root", "data_root"):
            if not getattr(self, field_name).is_absolute():
                raise ValueError(f"{field_name} must be an absolute local path.")
        if self.source_file_count < 1:
            raise ValueError("A completed result must account for at least one file.")
        if not 0 <= self.path_change_count <= self.source_file_count:
            raise ValueError("Path-change count is outside the source-file count.")
        if not 0 <= self.supported_link_update_count <= self.supported_link_count:
            raise ValueError(
                "Supported-link update count must be within the checked-link count."
            )
        if not (
            self.source_unchanged
            and self.all_files_present_once
            and self.deterministic_proof_passed
        ):
            raise ValueError("A Done presentation cannot contain a failed core proof.")
        if self.data_root != self.result_root / "data":
            raise ValueError("The user folder must be the result's data directory.")
        if self.execution_role not in {None, "origin", "receiver"}:
            raise ValueError("Result execution role is unsupported.")


@dataclass(frozen=True, slots=True)
class FolderClarificationRequest:
    """One compact missing-intent question bound to an existing service job."""

    question: str
    continuation_token: str

    def __post_init__(self) -> None:
        """Keep the single clarification bounded and unambiguous."""

        if not self.question or self.question != self.question.strip():
            raise ValueError("Clarification question must be nonempty and trimmed.")
        if len(self.question) > 1_000 or "\x00" in self.question:
            raise ValueError("Clarification question is too large or contains NUL.")
        if (
            not self.continuation_token
            or self.continuation_token != self.continuation_token.strip()
            or len(self.continuation_token) > 256
        ):
            raise ValueError("Clarification continuation token is invalid.")
        if "\x00" in self.continuation_token:
            raise ValueError("Clarification continuation token contains NUL.")


FolderRunOutcome = FolderRunPresentation | FolderClarificationRequest


@dataclass(frozen=True, slots=True)
class FolderWebCheckpoint:
    """Read-only durable state used to seed a reconstructed browser process."""

    lifecycle: FolderWebLifecycle
    source_root: Path
    output_parent: Path
    request: str
    journey: FolderJourney = FolderJourney.ORGANIZE
    clarification: FolderClarificationRequest | None = None
    blocker: str | None = None
    result: FolderRunPresentation | None = None
    resume_required: bool = False

    def __post_init__(self) -> None:
        if not self.source_root.is_absolute() or not self.output_parent.is_absolute():
            raise ValueError("Browser checkpoint paths must be absolute.")
        if not self.request.strip():
            raise ValueError("Browser checkpoint request cannot be blank.")
        if self.lifecycle is FolderWebLifecycle.AWAITING_CLARIFICATION:
            if self.clarification is None or self.resume_required:
                raise ValueError("Clarification checkpoint requires only its question.")
        elif self.clarification is not None:
            raise ValueError("Only clarification state may carry a question.")
        if self.lifecycle is FolderWebLifecycle.BLOCKED:
            if not self.blocker or self.resume_required:
                raise ValueError("Blocked checkpoint requires only an exact blocker.")
        elif self.blocker is not None:
            raise ValueError("Only blocked state may retain a blocker.")
        if self.lifecycle is FolderWebLifecycle.PLANNING:
            if not self.resume_required:
                raise ValueError("Planning checkpoint must resume automatically.")
        elif self.resume_required:
            raise ValueError("Only planning state can request automatic resume.")
        if self.lifecycle is FolderWebLifecycle.VERIFIED:
            if self.result is None or self.resume_required:
                raise ValueError("Verified checkpoint requires only verified facts.")
        elif self.result is not None:
            raise ValueError("Only verified state may carry completed facts.")


@runtime_checkable
class FolderRunService(Protocol):
    """Execute one bounded folder transaction without giving the UI authority."""

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunOutcome:
        """Return verified facts or one bound missing-intent question."""
        ...


@runtime_checkable
class ConnectedFolderRunService(FolderRunService, Protocol):
    """Run the receiver journey through the same durable domain services."""

    evidence_disclosure_required: bool
    planner_label: str
    planner_note: str

    async def apply_shared_change(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> FolderRunPresentation:
        """Return only a fully verified receiver result."""
        ...


@runtime_checkable
class ConnectedChangeDownloadService(FolderRunService, Protocol):
    """Capture verified Change File bytes for one terminal result."""

    def get_change_file_download(self) -> Any:
        """Return bounded verified bytes and download identities."""
        ...


@runtime_checkable
class ReadOnlyDurableCheckpointService(FolderRunService, Protocol):
    """Expose status projection that is guaranteed to perform no mutation."""

    durable_status_is_read_only: bool

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Return one read-only persisted checkpoint."""
        ...


@runtime_checkable
class ClarifyingFolderRunService(FolderRunService, Protocol):
    """Optional service capability for continuing the same job once."""

    async def continue_after_clarification(
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderRunPresentation:
        """Continue the existing job with exactly one plain-text answer."""
        ...


@runtime_checkable
class ResumableFolderRunService(FolderRunService, Protocol):
    """Service that can seed and resume one exact persisted local job.

    Clarification continuation is an independent optional capability. A durable
    receiver job and a zero-question origin job must still rehydrate after a
    process restart without pretending that they can answer a GPT question.
    """

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Return current durable presentation state without provider activity."""
        ...

    async def resume_existing_job(self) -> FolderRunOutcome:
        """Continue exact durable planning/execution without creating a job."""
        ...


@runtime_checkable
class StartupRehydratingFolderRunService(FolderRunService, Protocol):
    """Service that revalidates local inputs exactly once during app startup."""

    def rehydrate_web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Persist input staleness without provider, budget, copy, or execution."""
        ...


@runtime_checkable
class WorkerThreadFolderRunService(FolderRunService, Protocol):
    """Service whose bounded synchronous internals must not run on the web loop."""

    @property
    def run_in_worker_thread(self) -> bool:
        """Return true when each complete service operation needs one worker thread."""
        ...


@runtime_checkable
class ProgressReportingFolderRunService(FolderRunService, Protocol):
    """Service that emits presentation-only progress without ceding authority."""

    def set_progress_callback(
        self,
        callback: FolderProgressCallback | None,
        /,
    ) -> None:
        """Install or clear the current browser's thread-safe phase callback."""
        ...


@runtime_checkable
class FolderResultActionService(FolderRunService, Protocol):
    """Run proof and reconstruction actions against one verified result."""

    def verify_again(self) -> Any:
        """Re-run the source-free, keyless verifier without mutating the job."""
        ...

    def recreate_original(self, destination: Path) -> FolderRestoreReport:
        """Create one separately verified original-layout reconstruction."""
        ...


@dataclass(frozen=True, slots=True)
class DeterministicFolderRunService:
    """Bridge the browser shell to the complete deterministic A3 transaction."""

    result_folder_name: str = "name-atlas-organized-copy"
    target_prefix: str = "organized"

    @property
    def run_in_worker_thread(self) -> bool:
        """Keep the legacy A1 scan/copy/proof bridge off the web event loop."""

        return True

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunPresentation:
        """Run the truthful no-API A3 planner and expose verified facts only."""

        # Keep the legacy deterministic planner outside the provider-free
        # Connected Change import path. The standard C2 browser can therefore
        # open directly into Apply without importing any planner authority.
        from name_atlas.folder_refactor.planner import (
            DeterministicDevelopmentPlanner,
        )
        from name_atlas.folder_refactor.transaction import run_folder_refactor

        planner = DeterministicDevelopmentPlanner(
            result_folder_name=self.result_folder_name,
            target_prefix=self.target_prefix,
        )
        result = await run_folder_refactor(
            source_root=source_root,
            output_parent=output_parent,
            request=request,
            planner=planner,
        )
        checks = {check.check_id: check.passed for check in result.report.checks}
        deterministic_proof_passed = bool(checks) and all(checks.values())
        return FolderRunPresentation(
            source_root=source_root.resolve(strict=True),
            output_parent=output_parent.resolve(strict=True),
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
            deterministic_proof_passed=deterministic_proof_passed,
            independent_verification_passed=False,
            reconstruction_available=False,
            technical_facts=(
                ("Source commitment", result.report.source_commitment),
                ("Staged data commitment", result.report.staged_data_commitment),
                ("Portable package", "BagIt validation passed"),
            ),
        )


@dataclass(slots=True)
class _FolderWebState:
    lifecycle: FolderWebLifecycle = FolderWebLifecycle.IDLE
    source_value: str = ""
    request_value: str = ""
    output_value: str = ""
    change_file_value: str = ""
    journey: FolderJourney | None = None
    evidence_disclosure_required: bool = False
    outbound_evidence_will_be_sent: bool = False
    current_stage: int = 0
    completed_stage_count: int = 0
    result: FolderRunPresentation | None = None
    clarification: FolderClarificationRequest | None = None
    clarification_answer: str | None = None
    clarification_answer_count: int = 0
    clarification_error: str | None = None
    blocker: str | None = None
    notice: str | None = None
    csrf_token: str = field(
        default_factory=lambda: secrets.token_urlsafe(32),
        repr=False,
    )
    worker: asyncio.Task[None] | None = field(default=None, repr=False)
    submission_gate: asyncio.Lock = field(
        default_factory=asyncio.Lock,
        repr=False,
    )


class FolderFormError(ValueError):
    """The local Start form is incomplete or malformed."""


def create_folder_app(
    service: FolderRunService,
    *,
    initial_source: Path | None = None,
    initial_output_parent: Path | None = None,
    planner_label: str = PLANNER_LABEL,
    planner_note: str | None = None,
    native_bridge: NativePathBridge | None = None,
) -> FastAPI:
    """Create one loopback UI around the injected durable transaction service."""

    connected_enabled = isinstance(service, ConnectedFolderRunService)
    if connected_enabled:
        planner_label = service.planner_label
        planner_note = service.planner_note
    elif planner_note is None:
        planner_note = "This deterministic development transaction makes no API call."
    desktop_bridge = native_bridge or MacOSNativePathBridge()

    checkpoint_error: str | None = None
    try:
        if isinstance(service, StartupRehydratingFolderRunService):
            checkpoint = service.rehydrate_web_checkpoint()
        elif isinstance(service, ResumableFolderRunService):
            checkpoint = service.web_checkpoint()
        else:
            checkpoint = None
    except Exception as exc:  # noqa: BLE001 - corrupt local state must still render
        checkpoint = None
        checkpoint_error = (
            f"Durable job state could not be rehydrated: {_safe_error_text(exc)}"
        )
    state = _state_from_checkpoint(
        checkpoint,
        initial_source=initial_source,
        initial_output_parent=initial_output_parent,
    )
    if checkpoint_error is not None:
        _block_browser_result(state, checkpoint_error)
    state.evidence_disclosure_required = (
        service.evidence_disclosure_required if connected_enabled else False
    )
    state.outbound_evidence_will_be_sent = bool(
        getattr(service, "outbound_evidence_will_be_sent", False)
    )
    default_request = getattr(service, "default_request", None)
    if (
        connected_enabled
        and not state.request_value
        and isinstance(default_request, str)
    ):
        state.request_value = default_request

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            if (
                checkpoint is not None
                and checkpoint.resume_required
                and isinstance(service, ResumableFolderRunService)
            ):
                state.worker = asyncio.create_task(
                    _resume_job(state=state, service=service),
                    name="name-atlas-a2-resume-job",
                )
            yield
        finally:
            if state.worker is not None and not state.worker.done():
                if _uses_worker_thread(service):
                    await _await_mutating_worker(state.worker)
                else:
                    state.worker.cancel()
                    with suppress(asyncio.CancelledError):
                        await state.worker

    app = FastAPI(
        title="Reversible Name Atlas",
        description=(
            "Describe the change. Keep supported Markdown links. Prove the result."
        ),
        version="0.4.0-c2",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.state.folder_web_state = state
    app.state.folder_run_service = service
    app.state.native_path_bridge = desktop_bridge
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["127.0.0.1", "localhost", "testserver", "[::1]"],
    )

    @app.middleware("http")
    async def reject_cross_origin_mutations(request: Request, call_next):
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            origin = request.headers.get("origin")
            if origin is not None and not _origin_matches_host(
                origin,
                request.headers.get("host", ""),
            ):
                return HTMLResponse("Cross-origin request blocked.", status_code=403)
            if request.headers.get("sec-fetch-site", "").casefold() == "cross-site":
                return HTMLResponse("Cross-site request blocked.", status_code=403)
        return await call_next(request)

    app.mount(
        "/static",
        StaticFiles(directory=PACKAGE_ROOT / "static"),
        name="static",
    )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def root(request: Request) -> Response:
        await _refresh_terminal_checkpoint(state, service)
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        if not connected_enabled:
            return _redirect("/start")
        state.journey = None
        return TEMPLATES.TemplateResponse(
            request=request,
            name="folder/home.html",
            context=_base_context(
                state=state,
                planner_label=planner_label,
                planner_note=planner_note,
            ),
        )

    @app.get("/start", response_class=HTMLResponse, include_in_schema=False)
    async def start(request: Request) -> HTMLResponse:
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        state.journey = FolderJourney.ORGANIZE
        if not state.output_value and state.source_value:
            state.output_value = _derived_output_parent(state.source_value)
        return _render_start(
            request=request,
            state=state,
            planner_label=planner_label,
            planner_note=planner_note,
        )

    @app.post("/start", response_class=HTMLResponse, include_in_schema=False)
    async def start_job(request: Request) -> Response:
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        try:
            source_root, user_request, output_parent = await _parse_start_form(
                request,
                expected_csrf_token=state.csrf_token,
                require_evidence_acknowledgement=(state.evidence_disclosure_required),
            )
        except FolderFormError as exc:
            async with state.submission_gate:
                if state.lifecycle is not FolderWebLifecycle.IDLE:
                    return _redirect(_next_path(state))
                state.blocker = str(exc)
                return _render_start(
                    request=request,
                    state=state,
                    planner_label=planner_label,
                    planner_note=planner_note,
                    status_code=422,
                )
        async with state.submission_gate:
            if state.lifecycle is not FolderWebLifecycle.IDLE:
                return _redirect(_next_path(state))
            state.source_value = str(source_root)
            state.request_value = user_request
            state.output_value = str(output_parent)
            state.journey = FolderJourney.ORGANIZE
            _begin_working_state(state)
            state.worker = asyncio.create_task(
                _run_job(
                    state=state,
                    service=service,
                    source_root=source_root,
                    output_parent=output_parent,
                    user_request=user_request,
                ),
                name="name-atlas-a2-folder-job",
            )
        await asyncio.sleep(0)
        return _redirect("/working")

    @app.get("/apply", response_class=HTMLResponse, include_in_schema=False)
    async def apply_change(request: Request) -> Response:
        if not connected_enabled:
            return HTMLResponse(
                "Change File application is unavailable.", status_code=404
            )
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        state.journey = FolderJourney.APPLY
        if not state.output_value and state.source_value:
            state.output_value = _derived_output_parent(state.source_value)
        return TEMPLATES.TemplateResponse(
            request=request,
            name="folder/apply.html",
            context=_base_context(
                state=state,
                planner_label=planner_label,
                planner_note=planner_note,
            ),
        )

    @app.post("/apply", response_class=HTMLResponse, include_in_schema=False)
    async def apply_change_job(request: Request) -> Response:
        if not connected_enabled:
            return HTMLResponse(
                "Change File application is unavailable.", status_code=404
            )
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        try:
            change_file, source_root, output_parent = await _parse_apply_form(
                request,
                expected_csrf_token=state.csrf_token,
            )
        except FolderFormError as exc:
            async with state.submission_gate:
                if state.lifecycle is not FolderWebLifecycle.IDLE:
                    return _redirect(_next_path(state))
                state.blocker = str(exc)
                state.journey = FolderJourney.APPLY
                response = TEMPLATES.TemplateResponse(
                    request=request,
                    name="folder/apply.html",
                    context=_base_context(
                        state=state,
                        planner_label=planner_label,
                        planner_note=planner_note,
                    ),
                )
                response.status_code = 422
                return response
        async with state.submission_gate:
            if state.lifecycle is not FolderWebLifecycle.IDLE:
                return _redirect(_next_path(state))
            state.change_file_value = str(change_file)
            state.source_value = str(source_root)
            state.output_value = str(output_parent)
            state.request_value = "Applying the selected Name Atlas Change File"
            state.journey = FolderJourney.APPLY
            _begin_working_state(state)
            state.worker = asyncio.create_task(
                _run_apply_job(
                    state=state,
                    service=service,
                    change_file_path=change_file,
                    source_root=source_root,
                    output_parent=output_parent,
                ),
                name="name-atlas-c2-apply-change-job",
            )
        await asyncio.sleep(0)
        return _redirect("/working")

    @app.get("/working", response_class=HTMLResponse, include_in_schema=False)
    async def working(request: Request) -> Response:
        await _refresh_terminal_checkpoint(state, service)
        if state.lifecycle is FolderWebLifecycle.IDLE:
            return _redirect("/")
        if state.lifecycle is FolderWebLifecycle.VERIFIED:
            return _redirect("/done")
        return TEMPLATES.TemplateResponse(
            request=request,
            name="folder/working.html",
            context=_base_context(
                state=state,
                planner_label=planner_label,
                planner_note=planner_note,
            ),
        )

    @app.get("/status", include_in_schema=False)
    async def status() -> JSONResponse:
        await _refresh_terminal_checkpoint(state, service)
        stages = _working_stages(state)
        payload: dict[str, str | int | bool | None] = {
            "lifecycle": state.lifecycle.value,
            "current_stage": state.current_stage,
            "completed_stage_count": state.completed_stage_count,
            "stage_count": len(stages),
            "journey": None if state.journey is None else state.journey.value,
            "done_url": (
                "/done" if state.lifecycle is FolderWebLifecycle.VERIFIED else None
            ),
            "blocked": state.lifecycle is FolderWebLifecycle.BLOCKED,
            "clarification_required": (
                state.lifecycle is FolderWebLifecycle.AWAITING_CLARIFICATION
            ),
        }
        return JSONResponse(payload)

    @app.post("/clarify", include_in_schema=False)
    async def clarify(request: Request) -> Response:
        if (
            state.lifecycle is not FolderWebLifecycle.AWAITING_CLARIFICATION
            or state.clarification is None
        ):
            return HTMLResponse(
                "Clarification is not active for this job.",
                status_code=409,
            )
        if state.clarification_answer_count != 0:
            return HTMLResponse(
                "The one clarification answer has already been used.",
                status_code=409,
            )
        try:
            answer = await _parse_clarification_form(
                request,
                expected_csrf_token=state.csrf_token,
            )
        except FolderFormError as exc:
            async with state.submission_gate:
                if (
                    state.lifecycle is not FolderWebLifecycle.AWAITING_CLARIFICATION
                    or state.clarification_answer_count != 0
                ):
                    return HTMLResponse(
                        "The one clarification answer has already been used.",
                        status_code=409,
                    )
                state.clarification_error = str(exc)
                response = TEMPLATES.TemplateResponse(
                    request=request,
                    name="folder/working.html",
                    context=_base_context(
                        state=state,
                        planner_label=planner_label,
                        planner_note=planner_note,
                    ),
                )
                response.status_code = 422
                return response
        if not isinstance(service, ClarifyingFolderRunService):
            state.blocker = (
                "clarification_continuation_unavailable: the injected service "
                "cannot continue the same job"
            )
            state.lifecycle = FolderWebLifecycle.BLOCKED
            return _redirect("/working")

        async with state.submission_gate:
            if (
                state.lifecycle is not FolderWebLifecycle.AWAITING_CLARIFICATION
                or state.clarification is None
                or state.clarification_answer_count != 0
            ):
                return HTMLResponse(
                    "The one clarification answer has already been used.",
                    status_code=409,
                )
            state.clarification_answer = answer
            state.clarification_answer_count = 1
            state.clarification_error = None
            state.lifecycle = FolderWebLifecycle.PLANNING
            state.current_stage = 1
            state.completed_stage_count = 1
            state.worker = asyncio.create_task(
                _continue_job(
                    state=state,
                    service=service,
                    clarification=state.clarification,
                    answer=answer,
                ),
                name="name-atlas-a2-clarification-continuation",
            )
        await asyncio.sleep(0)
        return _redirect("/working")

    @app.get("/done", response_class=HTMLResponse, include_in_schema=False)
    async def done(request: Request) -> Response:
        await _refresh_terminal_checkpoint(state, service)
        if state.lifecycle is not FolderWebLifecycle.VERIFIED or state.result is None:
            return _redirect(_next_path(state))
        return TEMPLATES.TemplateResponse(
            request=request,
            name="folder/done.html",
            context=_base_context(
                state=state,
                planner_label=planner_label,
                planner_note=planner_note,
            ),
        )

    @app.post("/choose-path", include_in_schema=False)
    async def choose_path(request: Request) -> JSONResponse:
        if not connected_enabled:
            return JSONResponse(
                {"status": "unavailable", "message": "Native selection unavailable."},
                status_code=404,
            )
        if not _is_loopback_request(request):
            return JSONResponse(
                {"status": "failed", "message": "Loopback access required."},
                status_code=403,
            )
        try:
            role = await _parse_picker_form(
                request,
                expected_csrf_token=state.csrf_token,
            )
        except FolderFormError as exc:
            return JSONResponse(
                {"status": "failed", "message": str(exc)},
                status_code=422,
            )
        selection = await desktop_bridge.choose_path(role)
        payload: dict[str, str] = {"status": selection.status.value}
        if selection.status is NativeSelectionStatus.SELECTED:
            assert selection.path is not None
            selected_path = selection.path
            if role is NativePathRole.RESTORE_DESTINATION:
                selected_path = _derive_absent_restore_child(
                    selected_path,
                    state.result,
                )
            payload["path"] = str(selected_path)
        else:
            payload["message"] = _native_selection_message(selection.status)
        return JSONResponse(payload)

    @app.get("/download-change-file", include_in_schema=False)
    async def download_change_file() -> Response:
        await _refresh_terminal_checkpoint(state, service)
        if state.lifecycle is not FolderWebLifecycle.VERIFIED or state.result is None:
            return HTMLResponse("A verified result is required.", status_code=409)
        if not isinstance(service, ConnectedChangeDownloadService):
            return HTMLResponse("Change File download is unavailable.", status_code=409)
        try:
            download = await asyncio.to_thread(service.get_change_file_download)
            filename = _safe_download_filename(download.filename)
        except Exception as exc:  # noqa: BLE001 - exact service blocker is displayed
            _block_browser_result(
                state,
                f"Change File download blocked: {_safe_error_text(exc)}",
            )
            return HTMLResponse(state.blocker or "Download blocked.", status_code=409)
        return Response(
            content=download.payload,
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Cache-Control": "no-store",
                "X-Content-Type-Options": "nosniff",
            },
        )

    @app.post("/show-in-finder", include_in_schema=False)
    async def show_in_finder(request: Request) -> Response:
        await _refresh_terminal_checkpoint(state, service)
        if state.lifecycle is not FolderWebLifecycle.VERIFIED or state.result is None:
            return HTMLResponse("A verified result is required.", status_code=409)
        try:
            await _parse_result_action_form(
                request,
                expected_csrf_token=state.csrf_token,
                require_destination=False,
            )
        except FolderFormError as exc:
            return HTMLResponse(str(exc), status_code=422)
        if not isinstance(service, FolderResultActionService):
            return HTMLResponse(
                "Independent verification is unavailable.", status_code=409
            )
        if not await _verified_result_remains_valid(state, service):
            return _redirect("/working")
        assert state.result is not None
        opened = await desktop_bridge.show_in_finder(state.result.data_root)
        if opened.status is NativeOpenStatus.OPENED:
            state.notice = "The verified new folder was opened in Finder."
        elif opened.status is NativeOpenStatus.UNAVAILABLE:
            state.notice = (
                "Finder integration is unavailable here. Copy the displayed new-folder "
                "path instead."
            )
        else:
            state.notice = (
                "Finder could not open the verified folder. Copy the displayed path "
                "instead."
            )
        return _redirect(_next_path(state))

    @app.post("/verify-again", include_in_schema=False)
    async def verify_again(request: Request) -> Response:
        if state.lifecycle is not FolderWebLifecycle.VERIFIED or state.result is None:
            return HTMLResponse("A verified result is required.", status_code=409)
        try:
            await _parse_result_action_form(
                request,
                expected_csrf_token=state.csrf_token,
                require_destination=False,
            )
        except FolderFormError as exc:
            return HTMLResponse(str(exc), status_code=422)
        if not isinstance(service, FolderResultActionService):
            return HTMLResponse(
                "Independent keyless verification is unavailable.",
                status_code=409,
            )
        try:
            verification = await asyncio.to_thread(service.verify_again)
        except Exception as exc:  # noqa: BLE001 - exact service blocker is displayed
            _block_browser_result(
                state,
                f"Independent verification blocked: {_safe_error_text(exc)}",
            )
        else:
            if _verification_passed(verification):
                state.notice = "Independent keyless verification passed again."
            else:
                failures = ", ".join(verification.failed_check_ids)
                _block_browser_result(
                    state,
                    f"Independent verification blocked: {failures or 'unknown'}.",
                )
        return _redirect(_next_path(state))

    @app.post("/recreate-original", include_in_schema=False)
    async def recreate_original(request: Request) -> Response:
        if state.lifecycle is not FolderWebLifecycle.VERIFIED or state.result is None:
            return HTMLResponse("A verified result is required.", status_code=409)
        try:
            destination = await _parse_result_action_form(
                request,
                expected_csrf_token=state.csrf_token,
                require_destination=True,
            )
        except FolderFormError as exc:
            return HTMLResponse(str(exc), status_code=422)
        if destination is None:
            raise AssertionError("Reconstruction destination was not parsed.")
        if not isinstance(service, FolderResultActionService):
            return HTMLResponse(
                "Original-layout reconstruction is unavailable.",
                status_code=409,
            )
        try:
            report = await asyncio.to_thread(service.recreate_original, destination)
        except Exception as exc:  # noqa: BLE001 - exact service blocker is displayed
            message = f"Original-layout reconstruction blocked: {_safe_error_text(exc)}"
            if _reconstruction_failure_invalidates_result(exc):
                _block_browser_result(state, message)
            else:
                state.notice = message
        else:
            state.notice = (
                f"Original layout recreated and verified at {report.destination}."
            )
        return _redirect(_next_path(state))

    return app


async def _run_job(
    *,
    state: _FolderWebState,
    service: FolderRunService,
    source_root: Path,
    output_parent: Path,
    user_request: str,
) -> None:
    state.current_stage = 0
    state.completed_stage_count = 0
    clear_progress = _bind_progress_callback(service, state)
    try:
        outcome = await _invoke_service(
            service,
            lambda: service.plan_and_create_copy(
                source_root=source_root,
                output_parent=output_parent,
                request=user_request,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - service errors are user-visible blockers
        state.blocker = _safe_error_text(exc)
        state.lifecycle = FolderWebLifecycle.BLOCKED
        return
    finally:
        clear_progress()
    _apply_outcome(state, outcome)


async def _run_apply_job(
    *,
    state: _FolderWebState,
    service: ConnectedFolderRunService,
    change_file_path: Path,
    source_root: Path,
    output_parent: Path,
) -> None:
    """Run one provider-free receiver transaction through the same worker boundary."""

    clear_progress = _bind_progress_callback(service, state)
    try:
        result = await _invoke_service(
            service,
            lambda: service.apply_shared_change(
                change_file_path=change_file_path,
                source_root=source_root,
                output_parent=output_parent,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - exact service blocker is displayed
        state.blocker = _safe_error_text(exc)
        state.lifecycle = FolderWebLifecycle.BLOCKED
        return
    finally:
        clear_progress()
    _complete_job(state, result)


async def _continue_job(
    *,
    state: _FolderWebState,
    service: ClarifyingFolderRunService,
    clarification: FolderClarificationRequest,
    answer: str,
) -> None:
    clear_progress = _bind_progress_callback(service, state)
    try:
        outcome = await _invoke_service(
            service,
            lambda: service.continue_after_clarification(
                continuation_token=clarification.continuation_token,
                answer=answer,
            ),
        )
    except Exception as exc:  # noqa: BLE001 - service errors are user-visible blockers
        state.blocker = _safe_error_text(exc)
        state.lifecycle = FolderWebLifecycle.BLOCKED
        return
    finally:
        clear_progress()
    if not isinstance(outcome, FolderRunPresentation):
        state.blocker = "second_clarification_not_allowed"
        state.lifecycle = FolderWebLifecycle.BLOCKED
        return
    _complete_job(state, outcome)


def _complete_job(state: _FolderWebState, result: FolderRunPresentation) -> None:
    state.result = result
    state.clarification = None
    state.clarification_error = None
    state.blocker = None
    stages = _working_stages(state)
    state.current_stage = len(stages) - 1
    state.completed_stage_count = len(stages)
    state.lifecycle = FolderWebLifecycle.VERIFIED


def _apply_outcome(state: _FolderWebState, outcome: FolderRunOutcome) -> None:
    """Apply only the two declared service outcomes to server-owned state."""

    if isinstance(outcome, FolderClarificationRequest):
        if state.clarification_answer_count != 0 or state.clarification is not None:
            state.blocker = "second_clarification_not_allowed"
            state.lifecycle = FolderWebLifecycle.BLOCKED
            return
        state.clarification = outcome
        state.lifecycle = FolderWebLifecycle.AWAITING_CLARIFICATION
        return
    if not isinstance(outcome, FolderRunPresentation):
        state.blocker = "invalid_folder_run_outcome"
        state.lifecycle = FolderWebLifecycle.BLOCKED
        return
    _complete_job(state, outcome)


async def _resume_job(
    *,
    state: _FolderWebState,
    service: ResumableFolderRunService,
) -> None:
    """Resume one exact durable job without starting another provider sequence."""

    state.current_stage = 0
    state.completed_stage_count = 0
    clear_progress = _bind_progress_callback(service, state)
    try:
        outcome = await _invoke_service(
            service,
            service.resume_existing_job,
        )
    except Exception as exc:  # noqa: BLE001 - durable blockers are user-visible
        state.blocker = _safe_error_text(exc)
        state.lifecycle = FolderWebLifecycle.BLOCKED
        return
    finally:
        clear_progress()
    _apply_outcome(state, outcome)


async def _invoke_service(
    service: FolderRunService,
    operation: Callable[[], Coroutine[Any, Any, _ServiceResult]],
) -> _ServiceResult:
    """Run one complete durable operation without splitting its authority."""

    if _uses_worker_thread(service):
        thread_task = asyncio.create_task(
            asyncio.to_thread(_run_service_operation, operation),
            name="name-atlas-folder-service-thread",
        )
        try:
            return await asyncio.shield(thread_task)
        except asyncio.CancelledError:
            return await _await_service_thread(thread_task)
    return await operation()


def _run_service_operation(
    operation: Callable[[], Coroutine[Any, Any, _ServiceResult]],
) -> _ServiceResult:
    """Own one worker-thread event loop for one complete service operation."""

    return asyncio.run(operation())


def _uses_worker_thread(service: FolderRunService) -> bool:
    return (
        isinstance(service, WorkerThreadFolderRunService)
        and service.run_in_worker_thread
    )


async def _await_service_thread(
    thread_task: asyncio.Task[_ServiceResult],
) -> _ServiceResult:
    """Defer cancellation until the one mutation-owning thread reaches safety."""

    while not thread_task.done():
        try:
            await asyncio.shield(thread_task)
        except asyncio.CancelledError:
            continue
    return thread_task.result()


def _bind_progress_callback(
    service: FolderRunService,
    state: _FolderWebState,
) -> Callable[[], None]:
    """Route worker-thread progress back onto the server event loop."""

    if not isinstance(service, ProgressReportingFolderRunService):
        return lambda: None
    event_loop = asyncio.get_running_loop()

    def report(phase: FolderWorkPhase) -> None:
        event_loop.call_soon_threadsafe(_apply_work_phase, state, phase)

    service.set_progress_callback(report)
    return lambda: service.set_progress_callback(None)


def _apply_work_phase(state: _FolderWebState, phase: FolderWorkPhase) -> None:
    """Advance browser presentation monotonically; never change durable state."""

    phase_index = {
        FolderWorkPhase.READING: 0,
        FolderWorkPhase.PLANNING: 1,
        FolderWorkPhase.CHECKING: 2,
        FolderWorkPhase.CREATING: 3,
        FolderWorkPhase.UPDATING_LINKS: 4,
        FolderWorkPhase.VERIFYING: 5,
    }[phase]
    if state.lifecycle is FolderWebLifecycle.PLANNING:
        state.current_stage = max(state.current_stage, phase_index)
        state.completed_stage_count = max(
            state.completed_stage_count,
            phase_index,
        )


async def _await_mutating_worker(worker: asyncio.Task[None]) -> None:
    """Keep shutdown from abandoning a thread that still owns a mutation lock."""

    while not worker.done():
        try:
            await asyncio.shield(worker)
        except asyncio.CancelledError:
            continue
    await worker


def _state_from_checkpoint(
    checkpoint: FolderWebCheckpoint | None,
    *,
    initial_source: Path | None,
    initial_output_parent: Path | None,
) -> _FolderWebState:
    """Seed browser presentation from observed durable state or empty defaults."""

    if checkpoint is None:
        return _FolderWebState(
            source_value="" if initial_source is None else str(initial_source),
            output_value=(
                "" if initial_output_parent is None else str(initial_output_parent)
            ),
        )
    state = _FolderWebState(
        lifecycle=checkpoint.lifecycle,
        source_value=str(checkpoint.source_root),
        request_value=checkpoint.request,
        output_value=str(checkpoint.output_parent),
        journey=checkpoint.journey,
        blocker=checkpoint.blocker,
        clarification=checkpoint.clarification,
        result=checkpoint.result,
    )
    if checkpoint.lifecycle in {
        FolderWebLifecycle.PLANNING,
        FolderWebLifecycle.AWAITING_CLARIFICATION,
    }:
        state.current_stage = 1
        state.completed_stage_count = 1
    elif checkpoint.lifecycle is FolderWebLifecycle.VERIFIED:
        stages = _working_stages(state)
        state.current_stage = len(stages) - 1
        state.completed_stage_count = len(stages)
    return state


async def _parse_start_form(
    request: Request,
    *,
    expected_csrf_token: str,
    require_evidence_acknowledgement: bool = False,
) -> tuple[Path, str, Path]:
    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip()
    if content_type != "application/x-www-form-urlencoded":
        raise FolderFormError("The Start form must use URL-encoded local fields.")
    body = await request.body()
    if not body or len(body) > MAX_FORM_BODY_BYTES:
        raise FolderFormError("The Start form is empty or too large.")
    try:
        fields = parse_qs(
            body.decode("utf-8", errors="strict"),
            encoding="utf-8",
            errors="strict",
            strict_parsing=True,
            max_num_fields=5,
            keep_blank_values=True,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise FolderFormError("The Start form is not valid UTF-8 form data.") from exc
    expected = {"source_root", "user_request", "output_parent", "csrf_token"}
    if require_evidence_acknowledgement:
        expected.add("evidence_disclosure_acknowledged")
    if set(fields) != expected or any(len(fields[key]) != 1 for key in expected):
        raise FolderFormError("Exactly the displayed Start fields are required.")

    if not hmac.compare_digest(fields["csrf_token"][0], expected_csrf_token):
        raise FolderFormError("The Start form security token is invalid or expired.")
    if require_evidence_acknowledgement and (
        fields["evidence_disclosure_acknowledged"][0] != "true"
    ):
        raise FolderFormError(
            "Acknowledge the displayed GPT evidence and retention disclosure."
        )

    source_text = fields["source_root"][0].strip()
    request_text = fields["user_request"][0].strip()
    output_text = fields["output_parent"][0].strip()
    if not source_text or not request_text or not output_text:
        raise FolderFormError("Folder, request, and result location are all required.")
    if "\x00" in source_text or "\x00" in request_text or "\x00" in output_text:
        raise FolderFormError("Start fields cannot contain a NUL character.")
    if len(request_text) > MAX_REQUEST_CHARACTERS:
        raise FolderFormError(
            "The plain-English request cannot exceed "
            f"{MAX_REQUEST_CHARACTERS} characters."
        )
    source_root = Path(source_text).expanduser()
    output_parent = Path(output_text).expanduser()
    if not source_root.is_absolute() or not output_parent.is_absolute():
        raise FolderFormError(
            "Folder and result location must be absolute local paths."
        )
    return source_root, request_text, output_parent


async def _parse_apply_form(
    request: Request,
    *,
    expected_csrf_token: str,
) -> tuple[Path, Path, Path]:
    """Parse exactly the four receiver fields and no planner authority."""

    fields = await _parse_urlencoded_fields(
        request,
        expected_names={
            "change_file",
            "source_root",
            "output_parent",
            "csrf_token",
        },
        form_name="Apply",
    )
    if not hmac.compare_digest(fields["csrf_token"], expected_csrf_token):
        raise FolderFormError("The Apply form security token is invalid or expired.")
    values = (
        fields["change_file"].strip(),
        fields["source_root"].strip(),
        fields["output_parent"].strip(),
    )
    if any(not value or "\x00" in value for value in values):
        raise FolderFormError(
            "Change File, project folder, and result location are all required."
        )
    change_file, source_root, output_parent = (
        Path(value).expanduser() for value in values
    )
    if not all(
        path.is_absolute() for path in (change_file, source_root, output_parent)
    ):
        raise FolderFormError("Apply paths must be absolute local paths.")
    return change_file, source_root, output_parent


async def _parse_picker_form(
    request: Request,
    *,
    expected_csrf_token: str,
) -> NativePathRole:
    fields = await _parse_urlencoded_fields(
        request,
        expected_names={"role", "csrf_token"},
        form_name="Path selection",
    )
    if not hmac.compare_digest(fields["csrf_token"], expected_csrf_token):
        raise FolderFormError(
            "The path-selection security token is invalid or expired."
        )
    try:
        return NativePathRole(fields["role"])
    except ValueError as exc:
        raise FolderFormError("The path-selection role is unsupported.") from exc


async def _parse_urlencoded_fields(
    request: Request,
    *,
    expected_names: set[str],
    form_name: str,
) -> dict[str, str]:
    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip()
    if content_type != "application/x-www-form-urlencoded":
        raise FolderFormError(f"The {form_name} form must use URL-encoded fields.")
    body = await request.body()
    if not body or len(body) > MAX_FORM_BODY_BYTES:
        raise FolderFormError(f"The {form_name} form is empty or too large.")
    try:
        parsed = parse_qs(
            body.decode("utf-8", errors="strict"),
            encoding="utf-8",
            errors="strict",
            strict_parsing=True,
            max_num_fields=len(expected_names),
            keep_blank_values=True,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise FolderFormError(
            f"The {form_name} form is not valid UTF-8 form data."
        ) from exc
    if set(parsed) != expected_names or any(
        len(parsed[name]) != 1 for name in expected_names
    ):
        raise FolderFormError(f"Exactly the displayed {form_name} fields are required.")
    return {name: parsed[name][0] for name in expected_names}


async def _parse_clarification_form(
    request: Request,
    *,
    expected_csrf_token: str,
) -> str:
    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip()
    if content_type != "application/x-www-form-urlencoded":
        raise FolderFormError("The clarification answer must be URL-encoded text.")
    body = await request.body()
    if not body or len(body) > MAX_FORM_BODY_BYTES:
        raise FolderFormError("The clarification answer is empty or too large.")
    try:
        fields = parse_qs(
            body.decode("utf-8", errors="strict"),
            encoding="utf-8",
            errors="strict",
            strict_parsing=True,
            max_num_fields=2,
            keep_blank_values=True,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise FolderFormError(
            "The clarification answer is not valid UTF-8 text."
        ) from exc
    expected = {"answer", "csrf_token"}
    if set(fields) != expected or any(len(fields[key]) != 1 for key in expected):
        raise FolderFormError("Exactly one clarification answer is required.")
    if not hmac.compare_digest(fields["csrf_token"][0], expected_csrf_token):
        raise FolderFormError(
            "The clarification form security token is invalid or expired."
        )
    answer = fields["answer"][0]
    if not answer.strip():
        raise FolderFormError("The clarification answer cannot be empty.")
    if len(answer) > 4_000 or "\x00" in answer:
        raise FolderFormError("The clarification answer is too large or contains NUL.")
    return answer


async def _parse_result_action_form(
    request: Request,
    *,
    expected_csrf_token: str,
    require_destination: bool,
) -> Path | None:
    """Parse one CSRF-bound Done action without accepting extra authority."""

    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip()
    if content_type != "application/x-www-form-urlencoded":
        raise FolderFormError("The result action must use URL-encoded local fields.")
    body = await request.body()
    if not body or len(body) > MAX_FORM_BODY_BYTES:
        raise FolderFormError("The result action is empty or too large.")
    try:
        fields = parse_qs(
            body.decode("utf-8", errors="strict"),
            encoding="utf-8",
            errors="strict",
            strict_parsing=True,
            max_num_fields=2,
            keep_blank_values=True,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise FolderFormError(
            "The result action is not valid UTF-8 form data."
        ) from exc
    expected = (
        {"csrf_token", "restore_destination"} if require_destination else {"csrf_token"}
    )
    if set(fields) != expected or any(len(fields[key]) != 1 for key in expected):
        raise FolderFormError(
            "Exactly the displayed result-action fields are required."
        )
    if not hmac.compare_digest(fields["csrf_token"][0], expected_csrf_token):
        raise FolderFormError("The result-action security token is invalid or expired.")
    if not require_destination:
        return None
    destination_text = fields["restore_destination"][0].strip()
    if not destination_text or "\x00" in destination_text:
        raise FolderFormError(
            "The reconstruction destination must be a nonempty local path."
        )
    destination = Path(destination_text).expanduser()
    if not destination.is_absolute():
        raise FolderFormError("The reconstruction destination must be absolute.")
    return destination


def _base_context(
    *,
    state: _FolderWebState,
    planner_label: str,
    planner_note: str | None = None,
) -> dict[str, object]:
    journey = state.journey or FolderJourney.ORGANIZE
    return {
        "state": state,
        "journey": journey.value,
        "stages": _visible_working_stages(state, planner_label),
        "planner_label": (
            "Change File application — no GPT or API"
            if journey is FolderJourney.APPLY
            else planner_label
        ),
        "planner_note": (
            "The receiver is matched and verified locally through fixed code."
            if journey is FolderJourney.APPLY
            else planner_note
        ),
        "evidence_disclosure_required": state.evidence_disclosure_required,
        "notice": state.notice,
    }


def _render_start(
    *,
    request: Request,
    state: _FolderWebState,
    planner_label: str,
    planner_note: str | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    response = TEMPLATES.TemplateResponse(
        request=request,
        name="folder/start.html",
        context=_base_context(
            state=state,
            planner_label=planner_label,
            planner_note=planner_note,
        ),
    )
    response.status_code = status_code
    return response


def _next_path(state: _FolderWebState) -> str:
    if state.lifecycle is FolderWebLifecycle.IDLE:
        return "/"
    if state.lifecycle is FolderWebLifecycle.VERIFIED:
        return "/done"
    return "/working"


def _block_browser_result(state: _FolderWebState, blocker: str) -> None:
    """Make the latest failed receiver check the browser's visible authority."""

    state.lifecycle = FolderWebLifecycle.BLOCKED
    state.blocker = blocker
    state.result = None
    state.notice = None


def _redirect(path: str) -> RedirectResponse:
    return RedirectResponse(path, status_code=303)


def _safe_error_text(exc: Exception) -> str:
    text = " ".join(str(exc).split())
    if not text:
        return "The folder transaction was blocked without a usable explanation."
    return text[:1_000]


def _reconstruction_failure_invalidates_result(exc: Exception) -> bool:
    """Distinguish retryable destination failures from proof-authority failures."""

    retryable_destination_codes = {
        "destination_exists",
        "destination_must_be_absolute",
        "destination_must_share_result_parent",
        "destination_overlaps_result",
        "destination_overlaps_source",
        "destination_parent_invalid",
        "destination_type_invalid",
        "pending_cleanup_failed",
        "pending_destination_conflict",
        "promotion_failed",
        "source_root_invalid",
    }
    code = getattr(exc, "code", None)
    return not isinstance(code, str) or code not in retryable_destination_codes


def _working_stages(state: _FolderWebState) -> tuple[str, ...]:
    if state.journey is FolderJourney.APPLY:
        return APPLY_WORKING_STAGES
    return ORGANIZE_WORKING_STAGES


def _visible_working_stages(
    state: _FolderWebState,
    planner_label: str,
) -> tuple[str, ...]:
    """Project exact origin-specific language without changing job authority."""

    if state.journey is FolderJourney.APPLY:
        return APPLY_WORKING_STAGES
    if "no api call" in planner_label.casefold():
        return DEVELOPMENT_WORKING_STAGES
    return ORGANIZE_WORKING_STAGES


def _begin_working_state(state: _FolderWebState) -> None:
    state.lifecycle = FolderWebLifecycle.PLANNING
    state.current_stage = 0
    state.completed_stage_count = 0
    state.result = None
    state.clarification = None
    state.clarification_answer = None
    state.clarification_answer_count = 0
    state.clarification_error = None
    state.blocker = None
    state.notice = None


def _derived_output_parent(source_value: str) -> str:
    try:
        source = Path(source_value).expanduser()
    except (TypeError, ValueError):
        return ""
    if not source.is_absolute():
        return ""
    return str(source.parent)


def _derive_absent_restore_child(
    selected_parent: Path,
    result: FolderRunPresentation | None,
) -> Path:
    base_name = (
        f"{result.source_root.name}-original-layout"
        if result is not None and result.source_root.name
        else "name-atlas-original-layout"
    )
    candidate = selected_parent / base_name
    suffix = 2
    while os.path.lexists(candidate):
        candidate = selected_parent / f"{base_name}-{suffix}"
        suffix += 1
    return candidate


def _native_selection_message(status: NativeSelectionStatus) -> str:
    return {
        NativeSelectionStatus.CANCELLED: (
            "Selection cancelled. Manual paths remain available."
        ),
        NativeSelectionStatus.UNAVAILABLE: (
            "Native selection is unavailable. Enter an absolute path manually."
        ),
        NativeSelectionStatus.TIMEOUT: (
            "Native selection timed out. Enter an absolute path manually."
        ),
        NativeSelectionStatus.FAILED: (
            "Native selection failed. Enter an absolute path manually."
        ),
        NativeSelectionStatus.SELECTED: "Path selected.",
    }[status]


def _is_loopback_request(request: Request) -> bool:
    if request.client is None:
        return False
    host = request.client.host.casefold()
    return host in {"127.0.0.1", "::1", "localhost", "testclient"}


def _safe_download_filename(filename: str) -> str:
    if (
        not filename.isascii()
        or not filename.endswith(".nameatlas-change.json")
        or not filename
        or len(filename.encode("utf-8")) > 255
        or any(ord(character) < 32 or ord(character) == 127 for character in filename)
        or any(character in filename for character in ('"', "\\", "/"))
    ):
        return "name-atlas.nameatlas-change.json"
    return filename


def _verification_passed(verification: Any) -> bool:
    status = getattr(verification, "status", None)
    value = getattr(status, "value", status)
    return value == "verified" and not tuple(
        getattr(verification, "failed_check_ids", ())
    )


async def _verified_result_remains_valid(
    state: _FolderWebState,
    service: FolderResultActionService,
) -> bool:
    try:
        verification = await asyncio.to_thread(service.verify_again)
    except Exception as exc:  # noqa: BLE001 - exact service blocker is displayed
        _block_browser_result(
            state,
            f"Independent verification blocked: {_safe_error_text(exc)}",
        )
        return False
    if not _verification_passed(verification):
        failures = ", ".join(getattr(verification, "failed_check_ids", ()))
        _block_browser_result(
            state,
            f"Independent verification blocked: {failures or 'unknown'}.",
        )
        return False
    return True


async def _refresh_terminal_checkpoint(
    state: _FolderWebState,
    service: FolderRunService,
) -> None:
    """Apply only durable terminal status; never trigger provider or mutation work."""

    if (
        state.lifecycle is FolderWebLifecycle.VERIFIED and state.result is not None
    ) or state.lifecycle is FolderWebLifecycle.BLOCKED:
        # App construction already rehydrates and verifies durable terminal state.
        # Terminal actions independently reverify their own authority; ordinary
        # page/status reads must not repeatedly hash an arbitrarily large result.
        return
    if not isinstance(service, ReadOnlyDurableCheckpointService):
        return
    if not service.durable_status_is_read_only:
        return
    if state.worker is not None and not state.worker.done():
        # The in-process worker owns the durable writer and reports presentation
        # progress directly. Reading across its atomic revision replacement can
        # observe an intentionally transient inode and must not turn a healthy
        # transaction into a browser-level blocker.
        return

    checkpoint: FolderWebCheckpoint | None = None
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            checkpoint = await asyncio.to_thread(service.web_checkpoint)
            last_error = None
            break
        except Exception as exc:  # noqa: BLE001 - exact final failure is displayed
            last_error = exc
            if attempt < 2:
                await asyncio.sleep(0.01)
    if last_error is not None:
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            _block_browser_result(state, _safe_error_text(last_error))
        return
    if checkpoint is None:
        return
    if checkpoint.lifecycle is FolderWebLifecycle.VERIFIED:
        state.lifecycle = FolderWebLifecycle.VERIFIED
        state.journey = checkpoint.journey
        state.result = checkpoint.result
        state.blocker = None
        stages = _working_stages(state)
        state.current_stage = len(stages) - 1
        state.completed_stage_count = len(stages)
    elif checkpoint.lifecycle is FolderWebLifecycle.BLOCKED:
        state.lifecycle = FolderWebLifecycle.BLOCKED
        state.journey = checkpoint.journey
        state.blocker = checkpoint.blocker
        state.result = None


def _origin_matches_host(origin: str, host: str) -> bool:
    """Require an explicitly supplied browser Origin to match the loopback Host."""

    try:
        parsed = urlsplit(origin)
    except ValueError:
        return False
    return (
        parsed.scheme == "http"
        and parsed.username is None
        and parsed.password is None
        and parsed.path in {"", "/"}
        and parsed.query == ""
        and parsed.fragment == ""
        and parsed.netloc.casefold() == host.casefold()
    )
