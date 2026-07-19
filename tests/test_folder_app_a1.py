"""A1 acceptance tests for the AI-first Start, Working, and Done shell."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

import httpx
import pytest

from name_atlas.folder_app import (
    DeterministicFolderRunService,
    FolderRunPresentation,
    FolderRunService,
    create_folder_app,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _GatedFolderService:
    def __init__(self, tmp_path: Path) -> None:
        self.started = asyncio.Event()
        self.release = asyncio.Event()
        self.calls = 0
        self.tmp_path = tmp_path

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunPresentation:
        self.calls += 1
        assert source_root == self.tmp_path / "source"
        assert output_parent == self.tmp_path / "results"
        assert request == "Prepare this project for handoff."
        self.started.set()
        await self.release.wait()
        result_root = output_parent / "organized-project"
        return FolderRunPresentation(
            source_root=source_root,
            output_parent=output_parent,
            result_root=result_root,
            data_root=result_root / "data",
            source_file_count=4,
            path_change_count=3,
            source_unchanged=True,
            all_files_present_once=True,
            deterministic_proof_passed=True,
            technical_facts=(("Source commitment", "a" * 64),),
        )


class _BlockedFolderService:
    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunPresentation:
        del source_root, output_parent, request
        raise RuntimeError("protected_member_request: .env cannot be moved")


def _transport(service: FolderRunService) -> httpx.ASGITransport:
    return httpx.ASGITransport(app=create_folder_app(service))


def _csrf(response: httpx.Response) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    return match.group(1)


@pytest.mark.anyio
async def test_start_is_plain_exact_and_truthful(tmp_path: Path) -> None:
    service = _GatedFolderService(tmp_path)
    app = create_folder_app(
        service,
        initial_source=tmp_path / "preselected-source",
        initial_output_parent=tmp_path / "preselected-results",
    )
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        root = await client.get("/")
        response = await client.get("/start")

    assert root.status_code == 303
    assert root.headers["location"] == "/start"
    assert response.status_code == 200
    assert '<body class="bp6-dark folder-app">' in response.text
    assert response.text.count("<form") == 1
    assert 'name="source_root"' in response.text
    assert 'name="user_request"' in response.text
    assert 'name="output_parent"' in response.text
    assert "Folder to organize" in response.text
    assert "What should change?" in response.text
    assert "Result location" in response.text
    assert "Plan and create copy" in response.text
    assert "Your original folder will not be changed." in response.text
    assert "It does not send every file's bytes." in response.text
    assert (
        "OpenAI's standard abuse-monitoring and prompt-caching retention may still "
        "apply."
    ) in response.text
    assert "Deterministic A3 planner — no API call" in response.text
    assert str(tmp_path / "preselected-source") in response.text
    assert str(tmp_path / "preselected-results") in response.text
    assert "upload" not in response.text.lower()
    assert "Run safely" not in response.text
    assert "per-file" not in response.text.lower()


@pytest.mark.anyio
async def test_server_owned_start_working_done_transaction(tmp_path: Path) -> None:
    service = _GatedFolderService(tmp_path)
    transport = _transport(service)
    form = {
        "source_root": str(tmp_path / "source"),
        "user_request": "Prepare this project for handoff.",
        "output_parent": str(tmp_path / "results"),
    }

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        form["csrf_token"] = csrf_token
        started = await client.post("/start", data=form)
        await asyncio.wait_for(service.started.wait(), timeout=1)
        working_root = await client.get("/")
        working = await client.get("/working")
        status = await client.get("/status")
        duplicate = await client.post("/start", data=form)
        service.release.set()
        for _ in range(20):
            await asyncio.sleep(0)
            completed = await client.get("/status")
            if completed.json()["lifecycle"] == "verified":
                break
        done_root = await client.get("/")
        done = await client.get("/done")
        legacy = {
            route: await client.get(route)
            for route in ("/atlas", "/decide", "/stage", "/verify", "/handoff")
        }

    assert started.status_code == 303
    assert started.headers["location"] == "/working"
    assert working_root.headers["location"] == "/working"
    assert working.status_code == 200
    for stage in (
        "Reading folder",
        "Deterministic planning — no API call",
        "Checking every file and destination",
        "Creating the new folder",
        "Updating supported links",
        "Verifying the result",
    ):
        assert stage in working.text
    assert "This deterministic development transaction makes no API call." in (
        working.text
    )
    assert status.json()["lifecycle"] == "planning"
    assert duplicate.status_code == 303
    assert duplicate.headers["location"] == "/working"
    assert service.calls == 1
    assert completed.json()["lifecycle"] == "verified"
    assert done_root.headers["location"] == "/done"
    assert done.status_code == 200
    assert "Your new folder is ready" in done.text
    assert "4 of 4, exactly once" in done.text
    assert "Paths changed" in done.text and ">3<" in done.text
    assert "Original folder" in done.text and "Unchanged" in done.text
    assert "Files removed or overwritten" in done.text and "None" in done.text
    assert str(tmp_path / "results" / "organized-project" / "data") in done.text
    assert "See changes" in done.text
    assert "View proof" in done.text
    assert "Verify again" in done.text
    assert "Recreate original layout" in done.text
    assert all(response.status_code == 404 for response in legacy.values())


@pytest.mark.anyio
async def test_invalid_form_and_service_blocker_fail_closed(tmp_path: Path) -> None:
    gated = _GatedFolderService(tmp_path)
    invalid_transport = _transport(gated)
    blocked_transport = _transport(_BlockedFolderService())

    async with httpx.AsyncClient(
        transport=invalid_transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        invalid = await client.post(
            "/start",
            data={
                "source_root": "relative/source",
                "user_request": "Do this.",
                "output_parent": str(tmp_path),
                "csrf_token": csrf_token,
            },
        )
    async with httpx.AsyncClient(
        transport=blocked_transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        start = await client.post(
            "/start",
            data={
                "source_root": str(tmp_path / "source"),
                "user_request": "Move the protected file.",
                "output_parent": str(tmp_path / "results"),
                "csrf_token": csrf_token,
            },
        )
        assert start.status_code == 303
        for _ in range(20):
            await asyncio.sleep(0)
            status = await client.get("/status")
            if status.json()["lifecycle"] == "blocked":
                break
        blocked = await client.get("/working")

    assert invalid.status_code == 422
    assert "must be absolute local paths" in invalid.text
    assert gated.calls == 0
    assert status.json()["lifecycle"] == "blocked"
    assert "protected_member_request: .env cannot be moved" in blocked.text
    assert "The original folder remains unchanged." in blocked.text


@pytest.mark.anyio
async def test_mutating_forms_reject_untrusted_host_origin_and_csrf(
    tmp_path: Path,
) -> None:
    service = _GatedFolderService(tmp_path)
    app = create_folder_app(service)
    form = {
        "source_root": str(tmp_path / "source"),
        "user_request": "Prepare this project for handoff.",
        "output_parent": str(tmp_path / "results"),
        "csrf_token": app.state.folder_web_state.csrf_token,
    }

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        hostile_host = await client.post(
            "/start",
            data=form,
            headers={"host": "attacker.example"},
        )
        hostile_origin = await client.post(
            "/start",
            data=form,
            headers={"origin": "http://attacker.example"},
        )
        missing_csrf = await client.post(
            "/start",
            data={key: value for key, value in form.items() if key != "csrf_token"},
        )
        wrong_csrf = await client.post(
            "/start",
            data={**form, "csrf_token": "wrong-token"},
        )

    assert hostile_host.status_code == 400
    assert hostile_origin.status_code == 403
    assert missing_csrf.status_code == 422
    assert wrong_csrf.status_code == 422
    assert service.calls == 0


def test_completed_presentation_rejects_false_or_malformed_proof(
    tmp_path: Path,
) -> None:
    result_root = tmp_path / "result"

    with pytest.raises(ValueError, match="failed core proof"):
        FolderRunPresentation(
            source_root=tmp_path / "source",
            output_parent=tmp_path,
            result_root=result_root,
            data_root=result_root / "data",
            source_file_count=1,
            path_change_count=1,
            source_unchanged=False,
            all_files_present_once=True,
            deterministic_proof_passed=True,
        )
    with pytest.raises(ValueError, match="data directory"):
        FolderRunPresentation(
            source_root=tmp_path / "source",
            output_parent=tmp_path,
            result_root=result_root,
            data_root=result_root / "wrong",
            source_file_count=1,
            path_change_count=1,
            source_unchanged=True,
            all_files_present_once=True,
            deterministic_proof_passed=True,
        )


@pytest.mark.anyio
async def test_real_service_runs_start_to_bagit_backed_done(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output_parent = tmp_path / "results"
    (source / "notes").mkdir(parents=True)
    output_parent.mkdir()
    (source / "brief.txt").write_bytes(b"Northstar handoff brief\n")
    (source / "notes" / "plan.md").write_bytes(b"# Plan\n\nKeep every file.\n")
    (source / ".env.example").write_bytes(b"DEMO_VALUE=example\n")
    source_before = {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    }
    service = DeterministicFolderRunService(result_folder_name="actual-result")
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        response = await client.post(
            "/start",
            data={
                "source_root": str(source),
                "user_request": "Prepare this project folder for handoff.",
                "output_parent": str(output_parent),
                "csrf_token": csrf_token,
            },
        )
        assert response.status_code == 303
        for _ in range(100):
            await asyncio.sleep(0.01)
            status = await client.get("/status")
            if status.json()["lifecycle"] != "planning":
                break
        done = await client.get("/done")

    assert status.json()["lifecycle"] == "verified"
    assert done.status_code == 200
    assert "3 of 3, exactly once" in done.text
    assert "BagIt validation passed" in done.text
    result_root = output_parent / "actual-result"
    assert (result_root / "bagit.txt").is_file()
    assert (result_root / "data" / ".env.example").read_bytes() == (
        source_before[".env.example"]
    )
    assert {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    } == source_before
