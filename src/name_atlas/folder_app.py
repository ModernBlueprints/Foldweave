"""Server-rendered Start, Working, and Done shell for folder refactoring."""

from __future__ import annotations

import asyncio
import hmac
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

from name_atlas.folder_refactor.planner import DeterministicDevelopmentPlanner
from name_atlas.folder_refactor.transaction import run_folder_refactor

PACKAGE_ROOT = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=PACKAGE_ROOT / "templates")
MAX_FORM_BODY_BYTES = 32_768
MAX_REQUEST_CHARACTERS = 8_000
PLANNER_LABEL = "Deterministic A2 planner — no API call"
WORKING_STAGES = (
    "Reading folder",
    "Name Atlas is planning",
    "Checking every file and destination",
    "Creating a separate result",
    "Updating supported links",
    "Verifying result",
)
_ServiceResult = TypeVar("_ServiceResult")


class FolderWebLifecycle(StrEnum):
    """Server-owned A1/A2 presentation states."""

    IDLE = "idle"
    PLANNING = "planning"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    VERIFIED = "verified"
    BLOCKED = "blocked"


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
class ResumableFolderRunService(ClarifyingFolderRunService, Protocol):
    """Service that can seed and continue one exact persisted local job."""

    def web_checkpoint(self) -> FolderWebCheckpoint | None:
        """Return current durable presentation state without provider activity."""
        ...

    async def resume_existing_job(self) -> FolderRunOutcome:
        """Continue exact durable planning/execution without creating a job."""
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


@dataclass(frozen=True, slots=True)
class DeterministicFolderRunService:
    """Bridge the browser shell to the complete deterministic A2 transaction."""

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
        """Run the truthful no-API A2 planner and expose verified facts only."""

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


class FolderFormError(ValueError):
    """The local Start form is incomplete or malformed."""


def create_folder_app(
    service: FolderRunService,
    *,
    initial_source: Path | None = None,
    initial_output_parent: Path | None = None,
    planner_label: str = PLANNER_LABEL,
) -> FastAPI:
    """Create the A1 loopback UI around an injected folder transaction service."""

    checkpoint = (
        service.web_checkpoint()
        if isinstance(service, ResumableFolderRunService)
        else None
    )
    state = _state_from_checkpoint(
        checkpoint,
        initial_source=initial_source,
        initial_output_parent=initial_output_parent,
    )

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
        version="0.2.0-a2",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.state.folder_web_state = state
    app.state.folder_run_service = service
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

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        return _redirect(_next_path(state))

    @app.get("/start", response_class=HTMLResponse, include_in_schema=False)
    async def start(request: Request) -> HTMLResponse:
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        return _render_start(
            request=request,
            state=state,
            planner_label=planner_label,
        )

    @app.post("/start", response_class=HTMLResponse, include_in_schema=False)
    async def start_job(request: Request) -> Response:
        if state.lifecycle is not FolderWebLifecycle.IDLE:
            return _redirect(_next_path(state))
        try:
            source_root, user_request, output_parent = await _parse_start_form(
                request,
                expected_csrf_token=state.csrf_token,
            )
        except FolderFormError as exc:
            state.blocker = str(exc)
            return _render_start(
                request=request,
                state=state,
                planner_label=planner_label,
                status_code=422,
            )

        state.source_value = str(source_root)
        state.request_value = user_request
        state.output_value = str(output_parent)
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

    @app.get("/working", response_class=HTMLResponse, include_in_schema=False)
    async def working(request: Request) -> Response:
        if state.lifecycle is FolderWebLifecycle.IDLE:
            return _redirect("/start")
        if state.lifecycle is FolderWebLifecycle.VERIFIED:
            return _redirect("/done")
        return TEMPLATES.TemplateResponse(
            request=request,
            name="folder/working.html",
            context=_base_context(state=state, planner_label=planner_label),
        )

    @app.get("/status", include_in_schema=False)
    async def status() -> JSONResponse:
        payload: dict[str, str | int | bool | None] = {
            "lifecycle": state.lifecycle.value,
            "current_stage": state.current_stage,
            "completed_stage_count": state.completed_stage_count,
            "stage_count": len(WORKING_STAGES),
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
            state.clarification_error = str(exc)
            response = TEMPLATES.TemplateResponse(
                request=request,
                name="folder/working.html",
                context=_base_context(state=state, planner_label=planner_label),
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
        if state.lifecycle is not FolderWebLifecycle.VERIFIED or state.result is None:
            return _redirect(_next_path(state))
        return TEMPLATES.TemplateResponse(
            request=request,
            name="folder/done.html",
            context=_base_context(state=state, planner_label=planner_label),
        )

    @app.post("/verify-again", include_in_schema=False)
    async def verify_again() -> HTMLResponse:
        return HTMLResponse(
            "Independent keyless verification is introduced in A3.",
            status_code=409,
        )

    @app.post("/recreate-original", include_in_schema=False)
    async def recreate_original() -> HTMLResponse:
        return HTMLResponse(
            "Original-layout reconstruction is introduced in A3.",
            status_code=409,
        )

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
    state.current_stage = len(WORKING_STAGES) - 1
    state.completed_stage_count = len(WORKING_STAGES)
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
        state.current_stage = len(WORKING_STAGES) - 1
        state.completed_stage_count = len(WORKING_STAGES)
    return state


async def _parse_start_form(
    request: Request,
    *,
    expected_csrf_token: str,
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
            strict_parsing=True,
            max_num_fields=4,
            keep_blank_values=True,
        )
    except (UnicodeDecodeError, ValueError) as exc:
        raise FolderFormError("The Start form is not valid UTF-8 form data.") from exc
    expected = {"source_root", "user_request", "output_parent", "csrf_token"}
    if set(fields) != expected or any(len(fields[key]) != 1 for key in expected):
        raise FolderFormError("Exactly the displayed Start fields are required.")

    if not hmac.compare_digest(fields["csrf_token"][0], expected_csrf_token):
        raise FolderFormError("The Start form security token is invalid or expired.")

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


def _base_context(
    *,
    state: _FolderWebState,
    planner_label: str,
) -> dict[str, object]:
    return {
        "state": state,
        "stages": WORKING_STAGES,
        "planner_label": planner_label,
        "notice": state.notice,
    }


def _render_start(
    *,
    request: Request,
    state: _FolderWebState,
    planner_label: str,
    status_code: int = 200,
) -> HTMLResponse:
    response = TEMPLATES.TemplateResponse(
        request=request,
        name="folder/start.html",
        context=_base_context(state=state, planner_label=planner_label),
    )
    response.status_code = status_code
    return response


def _next_path(state: _FolderWebState) -> str:
    if state.lifecycle is FolderWebLifecycle.IDLE:
        return "/start"
    if state.lifecycle is FolderWebLifecycle.VERIFIED:
        return "/done"
    return "/working"


def _redirect(path: str) -> RedirectResponse:
    return RedirectResponse(path, status_code=303)


def _safe_error_text(exc: Exception) -> str:
    text = " ".join(str(exc).split())
    if not text:
        return "The folder transaction was blocked without a usable explanation."
    return text[:1_000]


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
