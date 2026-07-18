"""Loopback-only FastAPI application factory."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path, PurePosixPath
from shlex import quote
from urllib.parse import parse_qs

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from name_atlas.cases import CaseLifecycle, MigrationCaseError
from name_atlas.config import RuntimeConfig
from name_atlas.decision_cards import DecisionCardProviderError
from name_atlas.decisions import DecisionError
from name_atlas.receipts import (
    CHANGE_RECEIPT_HTML_PATH,
    CHANGE_RECEIPT_PATH,
    DECISION_LEDGER_PATH,
    FORWARD_PATH_MAP_PATH,
    ORIGINAL_METADATA_PATH,
    ORIGINAL_NORMALIZATION_PATH,
    PORTABLE_SOURCE_SNAPSHOT_PATH,
    REVERSE_PATH_MAP_PATH,
    VERIFICATION_REPORT_PATH,
    VERIFICATION_SUMMARY_PATH,
)
from name_atlas.receiver_verifier import (
    ReceiptCandidateError,
    ReceiptVerificationStatus,
    verify_receipt,
)
from name_atlas.staging import StagingError
from name_atlas.workflow import WorkflowSession

PACKAGE_ROOT = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=PACKAGE_ROOT / "templates")
MAX_FORM_BODY_BYTES = 4_096
WORKBENCH_STEPS = (
    {"number": "01", "key": "atlas", "label": "Atlas", "path": "/atlas"},
    {"number": "02", "key": "decide", "label": "Decide", "path": "/decide"},
    {"number": "03", "key": "stage", "label": "Stage", "path": "/stage"},
    {"number": "04", "key": "verify", "label": "Verify", "path": "/verify"},
    {"number": "05", "key": "handoff", "label": "Handoff", "path": "/handoff"},
)
RECEIVER_ARTIFACT_PATHS = frozenset(
    {
        PORTABLE_SOURCE_SNAPSHOT_PATH,
        DECISION_LEDGER_PATH,
        FORWARD_PATH_MAP_PATH,
        REVERSE_PATH_MAP_PATH,
        VERIFICATION_REPORT_PATH,
        VERIFICATION_SUMMARY_PATH,
        CHANGE_RECEIPT_PATH,
        CHANGE_RECEIPT_HTML_PATH,
        ORIGINAL_METADATA_PATH,
        ORIGINAL_NORMALIZATION_PATH,
    }
)


def create_app(
    config: RuntimeConfig,
    workflow: WorkflowSession | None = None,
) -> FastAPI:
    """Create the local application with server-owned workflow transitions."""

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if workflow is not None:
                workflow.close()

    app = FastAPI(
        title="Reversible Name Atlas",
        description="Refactor the collection. Hand over the proof.",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
        lifespan=lifespan,
    )
    app.state.runtime_config = config
    app.state.workflow = workflow
    app.state.notice = None
    app.state.notice_intent = "success"
    app.state.action_error = None
    app.state.receiver_verification = None
    app.state.receiver_verification_attempted = False
    app.mount(
        "/static",
        StaticFiles(directory=PACKAGE_ROOT / "static"),
        name="static",
    )

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        return RedirectResponse(
            url=_next_workbench_path(config=config, workflow=workflow),
            status_code=303,
        )

    @app.get("/atlas", response_class=HTMLResponse, include_in_schema=False)
    async def atlas(request: Request) -> HTMLResponse:
        return _render_workbench_page(
            request=request,
            app=app,
            config=config,
            workflow=workflow,
            active_page="atlas",
        )

    @app.get("/decide", response_class=HTMLResponse, include_in_schema=False)
    async def decide(request: Request) -> HTMLResponse:
        return _render_workbench_page(
            request=request,
            app=app,
            config=config,
            workflow=workflow,
            active_page="decide",
        )

    @app.get("/stage", response_class=HTMLResponse, include_in_schema=False)
    async def stage_page(request: Request) -> HTMLResponse:
        return _render_workbench_page(
            request=request,
            app=app,
            config=config,
            workflow=workflow,
            active_page="stage",
        )

    @app.get("/verify", response_class=HTMLResponse, include_in_schema=False)
    async def verify(request: Request) -> HTMLResponse:
        return _render_workbench_page(
            request=request,
            app=app,
            config=config,
            workflow=workflow,
            active_page="verify",
        )

    @app.get("/handoff", response_class=HTMLResponse, include_in_schema=False)
    async def handoff(request: Request) -> HTMLResponse:
        return _render_workbench_page(
            request=request,
            app=app,
            config=config,
            workflow=workflow,
            active_page="handoff",
        )

    @app.get("/healthz")
    async def health() -> dict[str, str | bool | int]:
        provider_ready = (
            config.replay_record_configured
            if config.mode.value == "replay"
            else config.api_key_configured
        )
        workflow_view = workflow.view_model() if workflow is not None else None
        case_lifecycle = _enum_text(
            workflow_view.get("case_lifecycle") if workflow_view is not None else None
        )
        ready = provider_ready and case_lifecycle not in {"stale", "blocked"}
        response: dict[str, str | bool | int] = {
            "status": "ready" if ready else "blocked",
            "mode": config.mode.value,
            "model": config.model,
            "api_key_configured": config.api_key_configured,
        }
        if workflow is not None:
            response.update(
                {
                    "families": len(workflow.package.families),
                    "content_objects": len(workflow.package.content_members),
                    "stage_verified": workflow.stage_result is not None,
                }
            )
            if case_lifecycle is not None:
                response["case_lifecycle"] = case_lifecycle
        return response

    @app.post("/families/{family_id}/generate", include_in_schema=False)
    async def generate_card(family_id: str) -> RedirectResponse:
        _clear_action_state(app)
        app.state.notice_intent = "neutral"
        if workflow is None:
            app.state.action_error = _missing_case_message()
            return _redirect_to("/decide")
        try:
            cache_hits_before = workflow.cache_hits
            await workflow.generate_card(family_id)
            if workflow.cache_hits > cache_hits_before:
                app.state.notice = (
                    "Validated cached card reused for identical evidence."
                )
            elif config.mode.value == "replay":
                app.state.notice = (
                    "Recorded GPT-5.6 response loaded for the exact visible packet."
                )
            else:
                app.state.notice = (
                    "Neutral GPT-5.6 decision card generated from the visible packet."
                )
            if workflow.replay_record_error is not None:
                app.state.action_error = workflow.replay_record_error
            elif workflow.budget_reporting_error is not None:
                app.state.action_error = workflow.budget_reporting_error
        except (DecisionCardProviderError, DecisionError, MigrationCaseError) as exc:
            app.state.action_error = str(exc)
        return _redirect_to("/decide")

    @app.post("/approve-low-risk", include_in_schema=False)
    async def approve_low_risk() -> RedirectResponse:
        _clear_action_state(app)
        if workflow is None:
            app.state.action_error = _missing_case_message()
            return _redirect_to("/decide")
        try:
            decisions = workflow.approve_low_risk()
            family_label = "family" if len(decisions) == 1 else "families"
            app.state.notice = (
                f"Human batch approval stored for {len(decisions)} low-risk "
                f"{family_label}."
            )
        except (DecisionError, MigrationCaseError) as exc:
            app.state.action_error = str(exc)
        return _redirect_to("/decide")

    @app.post("/families/{family_id}/approve", include_in_schema=False)
    async def approve(family_id: str) -> RedirectResponse:
        _clear_action_state(app)
        if workflow is None:
            app.state.action_error = _missing_case_message()
            return _redirect_to("/decide")
        try:
            workflow.approve(family_id)
            app.state.notice = "Human approval stored for the complete family."
        except (DecisionError, MigrationCaseError) as exc:
            app.state.action_error = str(exc)
        return _redirect_to("/decide")

    @app.post("/families/{family_id}/edit", include_in_schema=False)
    async def edit(family_id: str, request: Request) -> RedirectResponse:
        _clear_action_state(app)
        if workflow is None:
            app.state.action_error = _missing_case_message()
            return _redirect_to("/decide")
        body = await request.body()
        try:
            if len(body) > MAX_FORM_BODY_BYTES:
                raise DecisionError("Edited descriptor form is too large.")
            decoded = body.decode("utf-8", errors="strict")
            fields = parse_qs(decoded, strict_parsing=True, max_num_fields=4)
            descriptor_values = fields.get("descriptor", [])
            if len(descriptor_values) != 1:
                raise DecisionError("Exactly one edited descriptor is required.")
            workflow.edit(family_id, descriptor_values[0])
            app.state.notice = "Human descriptor stored across the complete family."
        except (
            UnicodeDecodeError,
            ValueError,
            DecisionError,
            MigrationCaseError,
        ) as exc:
            app.state.action_error = str(exc)
        return _redirect_to("/decide")

    @app.post("/families/{family_id}/refuse", include_in_schema=False)
    async def refuse(family_id: str) -> RedirectResponse:
        _clear_action_state(app)
        if workflow is None:
            app.state.action_error = _missing_case_message()
            return _redirect_to("/decide")
        try:
            workflow.refuse(family_id)
            app.state.notice = "Human refusal stored; complete export is blocked."
            app.state.notice_intent = "error"
        except (DecisionError, MigrationCaseError) as exc:
            app.state.action_error = str(exc)
        return _redirect_to("/decide")

    @app.post("/stage", include_in_schema=False)
    async def stage() -> RedirectResponse:
        _clear_action_state(app)
        if workflow is None:
            app.state.action_error = _missing_case_message()
            return _redirect_to("/stage")
        view = workflow.view_model()
        case_lifecycle = _enum_text(view.get("case_lifecycle"))
        if case_lifecycle == "stale":
            app.state.action_error = (
                "The Migration Case is stale; staging is blocked until a fresh "
                "case is created."
            )
            return _redirect_to("/stage")
        if case_lifecycle == "handoff_ready":
            app.state.action_error = (
                "A verified handoff already exists; this finalized case is read-only."
            )
            return _redirect_to("/stage")
        if not bool(view["export_ready"]):
            app.state.action_error = (
                "Staging is blocked until every required human decision is resolved."
            )
            return _redirect_to("/stage")
        if workflow.stage_result is not None:
            app.state.action_error = (
                "A verified handoff already exists; this workflow cannot "
                "stage it again."
            )
            return _redirect_to("/stage")
        try:
            workflow.stage()
            app.state.notice = (
                "Copy-only staged package verified and promoted for receiver review."
            )
        except (StagingError, MigrationCaseError) as exc:
            app.state.action_error = str(exc)
            return _redirect_to("/stage")
        return _redirect_to("/verify")

    @app.post("/rerun-verifier", include_in_schema=False)
    def rerun_verifier() -> RedirectResponse:
        """Rerun the pure receiver verifier against the finalized handoff."""

        _clear_action_state(app)
        app.state.receiver_verification = None
        app.state.receiver_verification_attempted = True
        handoff_root = _workflow_handoff_root(workflow)
        if handoff_root is None:
            app.state.action_error = (
                "No finalized handoff is available for receiver verification."
            )
            return _redirect_to("/handoff")
        try:
            result = verify_receipt(handoff_root)
        except ReceiptCandidateError as exc:
            app.state.action_error = str(exc)
            return _redirect_to("/handoff")
        app.state.receiver_verification = result
        if result.status is ReceiptVerificationStatus.VERIFIED:
            app.state.notice = (
                "Independent receiver verification passed for receipt "
                f"{result.receipt_fingerprint}."
            )
        else:
            blockers = ", ".join(result.failed_check_ids)
            app.state.action_error = f"Receiver verification BLOCKED: {blockers}."
        return _redirect_to("/handoff")

    @app.get(
        "/proof-artifacts/{artifact_path:path}",
        response_class=FileResponse,
        include_in_schema=False,
    )
    async def proof_artifact(artifact_path: str) -> FileResponse:
        stage_root = _workflow_handoff_root(workflow)
        if stage_root is None:
            raise HTTPException(status_code=404, detail="No verified proof exists.")
        stage_result = workflow.stage_result if workflow is not None else None
        allowed_paths = RECEIVER_ARTIFACT_PATHS
        if stage_result is not None:
            allowed_paths = allowed_paths.union(
                stage_result.artifacts.report.artifact_paths
            )
        if artifact_path not in allowed_paths:
            raise HTTPException(status_code=404, detail="Unknown proof artifact.")
        candidate = _resolve_regular_handoff_artifact(stage_root, artifact_path)
        if candidate is None:
            raise HTTPException(status_code=404, detail="Proof artifact is absent.")
        return FileResponse(candidate)

    return app


def _render_workbench_page(
    *,
    request: Request,
    app: FastAPI,
    config: RuntimeConfig,
    workflow: WorkflowSession | None,
    active_page: str,
) -> HTMLResponse:
    view = workflow.view_model() if workflow is not None else None
    receiver_verification = app.state.receiver_verification
    shell = _shell_context(
        config=config,
        workflow=workflow,
        view=view,
        receiver_verification=receiver_verification,
        receiver_verification_attempted=app.state.receiver_verification_attempted,
    )
    return TEMPLATES.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "config": config,
            "diagnostics": config.safe_diagnostics(),
            "view": view,
            "shell": shell,
            "steps": WORKBENCH_STEPS,
            "active_page": active_page,
            "page_status": _page_status(active_page=active_page, shell=shell),
            "notice": app.state.notice,
            "notice_intent": app.state.notice_intent,
            "action_error": app.state.action_error,
            "receiver_verification": receiver_verification,
        },
    )


def _shell_context(
    *,
    config: RuntimeConfig,
    workflow: WorkflowSession | None,
    view: dict[str, object] | None,
    receiver_verification: object | None = None,
    receiver_verification_attempted: bool = False,
) -> dict[str, object]:
    case = getattr(workflow, "case", None) if workflow is not None else None
    source_root = str(view["source_root"]) if view is not None else None
    case_name = _first_text(
        view.get("case_name") if view is not None else None,
        getattr(case, "case_name", None),
        getattr(workflow, "case_name", None) if workflow is not None else None,
        Path(source_root).name if source_root is not None else None,
        "No Migration Case loaded",
    )
    case_id = _first_text(
        view.get("case_id") if view is not None else None,
        getattr(case, "case_id", None),
        getattr(workflow, "case_id", None) if workflow is not None else None,
    )
    lifecycle_value = view.get("case_lifecycle") if view is not None else None
    if workflow is not None and lifecycle_value is None:
        lifecycle_value = (
            getattr(case, "lifecycle_state", None)
            or getattr(case, "lifecycle", None)
            or getattr(workflow, "lifecycle_state", None)
        )
    lifecycle = _enum_text(lifecycle_value)
    family_count = int(view["family_count"]) if view is not None else 0
    resolved_count = int(view["ready_count"]) if view is not None else 0
    unresolved_count = max(0, family_count - resolved_count)
    export_ready = bool(view["export_ready"]) if view is not None else False
    hard_blocker_count = int(view["hard_blocker_count"]) if view is not None else 0
    proof_ready = workflow is not None and workflow.stage_result is not None
    receipt_fingerprint = _receipt_fingerprint(workflow=workflow, view=view)
    handoff_ready = lifecycle == "handoff_ready" or (
        receipt_fingerprint is not None
        and view is not None
        and bool(view.get("handoff_path"))
    )
    handoff_root = _workflow_handoff_root(workflow)
    handoff_candidate_available = _is_regular_handoff_artifact(
        handoff_root,
        CHANGE_RECEIPT_PATH,
    )
    receiver_status = _enum_text(getattr(receiver_verification, "status", None))
    if receiver_verification_attempted:
        receiver_current_verified = receiver_status == "verified"
        receiver_blocked = not receiver_current_verified
    else:
        receiver_current_verified = (
            proof_ready
            and handoff_candidate_available
            and receipt_fingerprint is not None
        )
        receiver_blocked = handoff_ready and not handoff_candidate_available
    stale_or_import_blocked = view is None or lifecycle == "stale"
    case_blocked = lifecycle == "blocked"
    if stale_or_import_blocked or case_blocked:
        deterministic_status = "BLOCKED"
    elif handoff_ready and receiver_current_verified:
        deterministic_status = "VERIFIED"
    elif handoff_ready and receiver_blocked:
        deterministic_status = "BLOCKED"
    elif handoff_ready:
        deterministic_status = "RECEIPT FINALIZED"
    elif proof_ready:
        deterministic_status = "INCOMPLETE"
    elif hard_blocker_count:
        deterministic_status = "BLOCKED"
    elif export_ready:
        deterministic_status = "READY TO STAGE"
    else:
        deterministic_status = "INCOMPLETE"
    snapshot = view["snapshot"] if view is not None else None
    commitment = getattr(snapshot, "commitment", None)
    stage_root = str(handoff_root) if handoff_root is not None else None
    receipt_html_available = _is_regular_handoff_artifact(
        handoff_root,
        CHANGE_RECEIPT_HTML_PATH,
    )
    output_root = str(workflow.output_root) if workflow is not None else None
    stale_differences = (
        tuple(str(item) for item in view.get("stale_differences", ()))
        if view is not None
        else ()
    )
    source_scan_blocker = _first_text(
        view.get("source_scan_blocker") if view is not None else None
    )
    return {
        "case_name": case_name,
        "case_id": case_id,
        "case_id_short": f"{case_id[:12]}…" if case_id else "not persisted yet",
        "source_commitment": commitment,
        "source_commitment_short": (
            f"{commitment[:12]}…" if isinstance(commitment, str) else "unavailable"
        ),
        "mode_label": (
            "Recorded GPT-5.6 response"
            if config.mode.value == "replay" and config.replay_record_configured
            else f"{config.mode.value.title()} mode"
        ),
        "mode_compact_label": ("Replay" if config.mode.value == "replay" else "Live"),
        "resolved_count": resolved_count,
        "unresolved_count": unresolved_count,
        "hard_blocker_count": hard_blocker_count,
        "export_ready": export_ready,
        "proof_ready": proof_ready,
        "handoff_ready": handoff_ready,
        "handoff_candidate_available": handoff_candidate_available,
        "receiver_current_verified": receiver_current_verified,
        "receiver_blocked": receiver_blocked,
        "stale_or_import_blocked": stale_or_import_blocked,
        "case_blocked": case_blocked,
        "lifecycle": lifecycle,
        "deterministic_status": deterministic_status,
        "stage_root": stage_root,
        "output_root": output_root,
        "receipt_fingerprint": receipt_fingerprint,
        "receipt_html_available": receipt_html_available,
        "verifier_command": (
            f"uv run name-atlas verify-receipt {quote(stage_root)}"
            if stage_root is not None
            else None
        ),
        "restore_command": (
            f"uv run name-atlas restore-receipt {quote(stage_root)} RESTORE_DESTINATION"
            if stage_root is not None
            else None
        ),
        "stale_differences": stale_differences,
        "source_scan_blocker": source_scan_blocker,
    }


def _next_workbench_path(
    *,
    config: RuntimeConfig,
    workflow: WorkflowSession | None,
) -> str:
    if workflow is None:
        return "/atlas"
    view = workflow.view_model()
    shell = _shell_context(
        config=config,
        workflow=workflow,
        view=view,
    )
    if bool(shell["stale_or_import_blocked"]):
        return "/atlas"
    if bool(shell["handoff_ready"]):
        return "/handoff"
    if bool(shell["proof_ready"]):
        return "/verify"
    if not bool(view["export_ready"]):
        return "/decide"
    return "/stage"


def _page_status(*, active_page: str, shell: dict[str, object]) -> str:
    if bool(shell["stale_or_import_blocked"]):
        return "BLOCKED"
    if active_page == "atlas":
        return "INDEXED" if shell["source_commitment"] else "BLOCKED"
    if active_page == "decide":
        if not shell["source_commitment"]:
            return "BLOCKED"
        if int(shell["unresolved_count"]) == 0:
            return "COMPLETE"
        return (
            "BLOCKED"
            if bool(shell["case_blocked"]) or int(shell["hard_blocker_count"])
            else "INCOMPLETE"
        )
    if active_page == "stage":
        if bool(shell["handoff_ready"]):
            if bool(shell["receiver_current_verified"]):
                return "VERIFIED"
            if bool(shell["receiver_blocked"]):
                return "BLOCKED"
            return "INCOMPLETE"
        if bool(shell["proof_ready"]):
            return "COMPLETE"
        if bool(shell["export_ready"]):
            return "READY"
        return (
            "BLOCKED"
            if bool(shell["case_blocked"]) or int(shell["hard_blocker_count"])
            else "INCOMPLETE"
        )
    if active_page in {"verify", "handoff"}:
        if bool(shell["receiver_current_verified"]):
            return "VERIFIED"
        if bool(shell["handoff_ready"]) and bool(shell["receiver_blocked"]):
            return "BLOCKED"
        if bool(shell["handoff_ready"]):
            return "INCOMPLETE"
        if active_page == "verify" and bool(shell["proof_ready"]):
            return "INCOMPLETE"
        return (
            "BLOCKED"
            if bool(shell["case_blocked"]) or int(shell["hard_blocker_count"])
            else "INCOMPLETE"
        )
    return "INCOMPLETE"


def _receipt_fingerprint(
    *,
    workflow: WorkflowSession | None,
    view: dict[str, object] | None,
) -> str | None:
    if workflow is None:
        return None
    case = getattr(workflow, "case", None)
    candidates = [
        view.get("receipt_fingerprint") if view is not None else None,
        getattr(case, "receipt_fingerprint", None),
    ]
    if case is None:
        stage_result = workflow.stage_result
        candidates.extend(
            (
                getattr(workflow, "receipt_fingerprint", None),
                getattr(stage_result, "receipt_fingerprint", None),
            )
        )
    for candidate in candidates:
        if isinstance(candidate, str) and candidate:
            return candidate
    return None


def _workflow_handoff_root(workflow: WorkflowSession | None) -> Path | None:
    if workflow is None:
        return None
    if workflow.stage_result is not None:
        return workflow.stage_result.stage_root
    case = getattr(workflow, "case", None)
    if _enum_text(
        getattr(case, "lifecycle", None)
    ) != CaseLifecycle.HANDOFF_READY.value or not _is_sha256(
        getattr(case, "receipt_fingerprint", None)
    ):
        return None
    local_paths = getattr(case, "local_paths", None)
    handoff_path = getattr(local_paths, "handoff_path", None)
    return Path(handoff_path) if handoff_path is not None else None


def _is_regular_handoff_artifact(root: Path | None, relative_path: str) -> bool:
    return (
        root is not None
        and _resolve_regular_handoff_artifact(root, relative_path) is not None
    )


def _resolve_regular_handoff_artifact(
    root: Path,
    relative_path: str,
) -> Path | None:
    if root.is_symlink():
        return None
    try:
        resolved_root = root.resolve(strict=True)
        candidate = resolved_root
        for part in PurePosixPath(relative_path).parts:
            candidate /= part
            if candidate.is_symlink():
                return None
        resolved_candidate = candidate.resolve(strict=True)
        resolved_candidate.relative_to(resolved_root)
    except (OSError, RuntimeError, ValueError):
        return None
    return resolved_candidate if resolved_candidate.is_file() else None


def _is_sha256(value: object | None) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _enum_text(value: object | None) -> str | None:
    enum_value = getattr(value, "value", value)
    return str(enum_value).lower() if enum_value is not None else None


def _first_text(*values: object | None) -> str | None:
    for value in values:
        if value is not None and str(value):
            return str(value)
    return None


def _redirect_to(path: str) -> RedirectResponse:
    return RedirectResponse(url=path, status_code=303)


def _missing_case_message() -> str:
    return "No Migration Case is loaded; this server-side action is blocked."


def _clear_action_state(app: FastAPI) -> None:
    app.state.notice = None
    app.state.notice_intent = "success"
    app.state.action_error = None
