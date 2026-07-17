"""Application-shell tests."""

from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from name_atlas.app import create_app
from name_atlas.cases import CaseLifecycle
from name_atlas.config import RuntimeConfig
from name_atlas.domain import RunMode
from name_atlas.verification import BagItPackageValidator
from name_atlas.workflow import (
    UnavailableReplayDecisionCardProvider,
    WorkflowSession,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_replay_shell_exposes_safe_runtime_status() -> None:
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        root = await client.get("/")
        response = await client.get("/atlas")
        health = await client.get("/healthz")

    assert root.status_code == 303
    assert root.headers["location"] == "/atlas"
    assert response.status_code == 200
    assert "Refactor the collection." in response.text
    assert "Replay provider configured" in response.text
    assert "loopback only" in response.text
    assert "No Migration Case is loaded" in response.text
    assert response.text.count('aria-current="page"') == 1
    assert health.json() == {
        "status": "blocked",
        "mode": "replay",
        "model": "gpt-5.6",
        "api_key_configured": False,
    }


@pytest.mark.anyio
async def test_live_shell_is_blocked_without_api_key() -> None:
    config = RuntimeConfig.from_environment(mode=RunMode.LIVE, environ={})
    transport = httpx.ASGITransport(app=create_app(config))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        health = await client.get("/healthz")

    assert health.json()["status"] == "blocked"
    assert "OPENAI_API_KEY" not in str(health.json())


@pytest.mark.anyio
async def test_every_workbench_route_is_directly_inspectable_without_case() -> None:
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        responses = {
            path: await client.get(path)
            for path in ("/atlas", "/decide", "/stage", "/verify", "/handoff")
        }
        guarded_stage = await client.post("/stage")
        guarded_decision = await client.post("/approve-low-risk")

    for path, response in responses.items():
        assert response.status_code == 200
        assert response.text.count('aria-current="page"') == 1
        assert f'href="{path}" aria-current="page"' in response.text
        assert "BLOCKED" in response.text or "INCOMPLETE" in response.text
    assert guarded_stage.status_code == 303
    assert guarded_stage.headers["location"] == "/stage"
    assert guarded_decision.status_code == 303
    assert guarded_decision.headers["location"] == "/decide"


@pytest.mark.anyio
async def test_root_and_stage_follow_server_owned_workflow_state(
    tmp_path: Path,
) -> None:
    source = tmp_path / "single-family-source"
    _write_low_risk_package(source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=UnavailableReplayDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
        case_path=tmp_path / "case.json",
        case_name="Route state case",
    )
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config, workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        unresolved_root = await client.get("/")
        direct_pages = {
            path: await client.get(path)
            for path in ("/atlas", "/decide", "/stage", "/verify", "/handoff")
        }
        blocked_stage = await client.post("/stage")
        stage_after_blocked_request = workflow.stage_result
        approved = await client.post("/approve-low-risk")
        ready_root = await client.get("/")
        staged = await client.post("/stage")
        assert workflow.case is not None
        assert workflow.stage_result is not None
        stage_result_after_success = workflow.stage_result
        workflow.case = workflow.case.model_copy(
            update={
                "lifecycle": CaseLifecycle.READY_TO_STAGE,
                "receipt_fingerprint": None,
            }
        )
        verified = await client.get("/verify")
        proof_only_root = await client.get("/")
        workflow.case = workflow.case.model_copy(
            update={
                "lifecycle": CaseLifecycle.HANDOFF_READY,
                "receipt_fingerprint": "a" * 64,
                "local_paths": workflow.case.local_paths.model_copy(
                    update={
                        "stage_path": workflow.stage_result.stage_root,
                        "handoff_path": workflow.stage_result.stage_root,
                    }
                ),
            }
        )
        handoff_root = await client.get("/")
        handoff = await client.get("/handoff")
        repeated_stage = await client.post("/stage")
        workflow.stage_result = None
        restarted_verify = await client.get("/verify")
        restarted_handoff = await client.get("/handoff")

    assert unresolved_root.status_code == 303
    assert unresolved_root.headers["location"] == "/decide"
    assert all(response.status_code == 200 for response in direct_pages.values())
    assert "Route state case" in direct_pages["/atlas"].text
    assert workflow.case is not None
    assert workflow.case.case_id[:12] in direct_pages["/atlas"].text
    assert "INCOMPLETE" in direct_pages["/verify"].text
    assert "INCOMPLETE" in direct_pages["/handoff"].text
    assert blocked_stage.status_code == 303
    assert blocked_stage.headers["location"] == "/stage"
    assert stage_after_blocked_request is None
    assert stage_result_after_success is not None
    assert approved.status_code == 303
    assert approved.headers["location"] == "/decide"
    assert ready_root.headers["location"] == "/stage"
    assert staged.status_code == 303
    assert staged.headers["location"] == "/verify"
    assert "INCOMPLETE" in verified.text
    assert "Verified round-trip integrity" in verified.text
    assert proof_only_root.headers["location"] == "/verify"
    assert handoff_root.headers["location"] == "/handoff"
    assert "verify-receipt" in handoff.text
    assert repeated_stage.status_code == 303
    assert repeated_stage.headers["location"] == "/stage"
    assert "persistent case records a receiver-verified handoff" in (
        restarted_verify.text
    )
    assert "verify-receipt" in restarted_handoff.text
    workflow.close()


@pytest.mark.anyio
async def test_application_lifespan_releases_case_lock(tmp_path: Path) -> None:
    source = tmp_path / "lifespan-source"
    _write_low_risk_package(source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=UnavailableReplayDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
        case_path=tmp_path / "case.json",
    )
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    app = create_app(config, workflow)

    with patch.object(workflow, "close", wraps=workflow.close) as close:
        async with app.router.lifespan_context(app):
            pass

    close.assert_called_once_with()


@pytest.mark.anyio
async def test_root_distinguishes_refused_review_from_stale_case(
    tmp_path: Path,
) -> None:
    source = tmp_path / "blocked-case-source"
    _write_low_risk_package(source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=UnavailableReplayDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
        case_path=tmp_path / "case.json",
    )
    workflow.refuse(workflow.package.families[0].family_id)
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config, workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        refused_root = await client.get("/")
        assert workflow.case is not None
        workflow.case = workflow.case.model_copy(
            update={"lifecycle": CaseLifecycle.STALE}
        )
        stale_root = await client.get("/")
        stale_atlas = await client.get("/atlas")

    assert refused_root.headers["location"] == "/decide"
    assert stale_root.headers["location"] == "/atlas"
    assert "Migration Case is stale" in stale_atlas.text
    workflow.close()


def _write_low_risk_package(root: Path) -> None:
    (root / "objects").mkdir(parents=True)
    (root / "metadata").mkdir()
    (root / "objects" / "plain note.txt").write_text("plain", encoding="utf-8")
    (root / "metadata" / "metadata.csv").write_text(
        "filename,dc.identifier,dc.title\nobjects/plain note.txt,LOW-0001,Plain note\n",
        encoding="utf-8",
    )
