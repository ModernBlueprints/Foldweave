"""Loopback-only FastAPI application factory."""

from pathlib import Path
from urllib.parse import parse_qs

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from name_atlas.config import RuntimeConfig
from name_atlas.decision_cards import DecisionCardProviderError
from name_atlas.decisions import DecisionError
from name_atlas.staging import StagingError
from name_atlas.workflow import WorkflowSession

PACKAGE_ROOT = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=PACKAGE_ROOT / "templates")
MAX_FORM_BODY_BYTES = 4_096


def create_app(
    config: RuntimeConfig,
    workflow: WorkflowSession | None = None,
) -> FastAPI:
    """Create the local application with safe startup diagnostics."""

    app = FastAPI(
        title="Reversible Name Atlas",
        description="Refactor the collection. Preserve every identity.",
        version="0.1.0",
        docs_url=None,
        redoc_url=None,
    )
    app.state.runtime_config = config
    app.state.workflow = workflow
    app.state.notice = None
    app.state.action_error = None
    app.mount(
        "/static",
        StaticFiles(directory=PACKAGE_ROOT / "static"),
        name="static",
    )

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index(request: Request) -> HTMLResponse:
        return TEMPLATES.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "config": config,
                "diagnostics": config.safe_diagnostics(),
                "view": workflow.view_model() if workflow is not None else None,
                "notice": app.state.notice,
                "action_error": app.state.action_error,
            },
        )

    @app.get("/healthz")
    async def health() -> dict[str, str | bool | int]:
        ready = (
            config.replay_record_configured
            if config.mode.value == "replay"
            else config.api_key_configured
        )
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
        return response

    if workflow is not None:

        @app.post("/families/{family_id}/generate", include_in_schema=False)
        async def generate_card(family_id: str) -> RedirectResponse:
            _clear_action_state(app)
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
                        "Neutral GPT-5.6 decision card generated from the visible "
                        "packet."
                    )
                if workflow.replay_record_error is not None:
                    app.state.action_error = workflow.replay_record_error
                elif workflow.budget_reporting_error is not None:
                    app.state.action_error = workflow.budget_reporting_error
            except (DecisionCardProviderError, DecisionError) as exc:
                app.state.action_error = str(exc)
            return RedirectResponse(url="/#decisions", status_code=303)

        @app.post("/approve-low-risk", include_in_schema=False)
        async def approve_low_risk() -> RedirectResponse:
            _clear_action_state(app)
            try:
                decisions = workflow.approve_low_risk()
                app.state.notice = (
                    f"Human batch approval stored for {len(decisions)} "
                    "low-risk families."
                )
            except DecisionError as exc:
                app.state.action_error = str(exc)
            return RedirectResponse(url="/#decisions", status_code=303)

        @app.post("/families/{family_id}/approve", include_in_schema=False)
        async def approve(family_id: str) -> RedirectResponse:
            _clear_action_state(app)
            try:
                workflow.approve(family_id)
                app.state.notice = "Human approval stored for the complete family."
            except DecisionError as exc:
                app.state.action_error = str(exc)
            return RedirectResponse(url="/#decisions", status_code=303)

        @app.post("/families/{family_id}/edit", include_in_schema=False)
        async def edit(family_id: str, request: Request) -> RedirectResponse:
            _clear_action_state(app)
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
            except (UnicodeDecodeError, ValueError, DecisionError) as exc:
                app.state.action_error = str(exc)
            return RedirectResponse(url="/#decisions", status_code=303)

        @app.post("/families/{family_id}/refuse", include_in_schema=False)
        async def refuse(family_id: str) -> RedirectResponse:
            _clear_action_state(app)
            try:
                workflow.refuse(family_id)
                app.state.notice = "Human refusal stored; complete export is blocked."
            except DecisionError as exc:
                app.state.action_error = str(exc)
            return RedirectResponse(url="/#decisions", status_code=303)

        @app.post("/stage", include_in_schema=False)
        async def stage() -> RedirectResponse:
            _clear_action_state(app)
            try:
                workflow.stage()
                app.state.notice = "Copy-only staged package verified and promoted."
            except StagingError as exc:
                app.state.action_error = str(exc)
            return RedirectResponse(url="/#proof", status_code=303)

        @app.get(
            "/proof-artifacts/{artifact_path:path}",
            response_class=FileResponse,
            include_in_schema=False,
        )
        async def proof_artifact(artifact_path: str) -> FileResponse:
            stage_result = workflow.stage_result
            if stage_result is None:
                raise HTTPException(status_code=404, detail="No verified proof exists.")
            if artifact_path not in stage_result.artifacts.report.artifact_paths:
                raise HTTPException(status_code=404, detail="Unknown proof artifact.")
            stage_root = stage_result.stage_root.resolve()
            candidate = (stage_root / artifact_path).resolve()
            try:
                candidate.relative_to(stage_root)
            except ValueError as exc:
                raise HTTPException(
                    status_code=404,
                    detail="Unknown proof artifact.",
                ) from exc
            if not candidate.is_file():
                raise HTTPException(status_code=404, detail="Proof artifact is absent.")
            return FileResponse(candidate)

    return app


def _clear_action_state(app: FastAPI) -> None:
    app.state.notice = None
    app.state.action_error = None
