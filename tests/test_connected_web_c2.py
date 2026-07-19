"""C2 browser acceptance for Organize, Apply, native paths, and durable proof."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from pathlib import Path

import httpx
import pytest
from connected_change_fixtures import (
    make_connected_change_fixture,
    portable_tree,
    tree_state,
)

from name_atlas.connected_web_service import (
    DETERMINISTIC_BROWSER_REQUEST,
    ConnectedBrowserRunService,
)
from name_atlas.folder_app import (
    FolderClarificationRequest,
    FolderRunPresentation,
    create_folder_app,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_PATH,
)
from name_atlas.native_bridge import (
    NativeOpenResult,
    NativeOpenStatus,
    NativePathRole,
    NativePathSelection,
    NativeSelectionStatus,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _csrf(response: httpx.Response) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    return match.group(1)


async def _wait_for_lifecycle(
    client: httpx.AsyncClient,
    expected: str,
    *,
    attempts: int = 500,
) -> dict[str, object]:
    last: dict[str, object] | None = None
    for _ in range(attempts):
        response = await client.get("/status")
        assert response.status_code == 200
        last = response.json()
        if last["lifecycle"] == expected:
            return last
        if last["lifecycle"] == "blocked":
            working = await client.get("/working")
            raise AssertionError(f"Browser transaction blocked: {working.text}")
        await asyncio.sleep(0.02)
    raise AssertionError(
        f"Browser transaction never reached {expected}; last status was {last}."
    )


@dataclass(slots=True)
class _FakeNativeBridge:
    selections: dict[NativePathRole, NativePathSelection] = field(default_factory=dict)
    selected_roles: list[NativePathRole] = field(default_factory=list)
    opened_paths: list[Path] = field(default_factory=list)
    open_result: NativeOpenResult = field(
        default_factory=lambda: NativeOpenResult(status=NativeOpenStatus.OPENED)
    )

    async def choose_path(self, role: NativePathRole) -> NativePathSelection:
        self.selected_roles.append(role)
        return self.selections.get(
            role,
            NativePathSelection(
                status=NativeSelectionStatus.UNAVAILABLE,
                reason_code="picker_unavailable",
            ),
        )

    async def show_in_finder(self, path: Path) -> NativeOpenResult:
        self.opened_paths.append(path)
        return self.open_result


class _GatedApplyService:
    """Connected UI double proving Apply never falls through to planning."""

    evidence_disclosure_required = True
    planner_label = "GPT-5.6 planning"
    planner_note = "Planning evidence is intentionally unavailable in Apply."

    def __init__(self, root: Path) -> None:
        self.root = root
        self.apply_started = asyncio.Event()
        self.release_apply = asyncio.Event()
        self.plan_calls = 0
        self.apply_calls = 0

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunPresentation:
        del source_root, output_parent, request
        self.plan_calls += 1
        raise AssertionError("Apply must never invoke the planning entry point.")

    async def apply_shared_change(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> FolderRunPresentation:
        self.apply_calls += 1
        assert change_file_path == self.root / "northstar.nameatlas-change.json"
        assert source_root == self.root / "martin-project"
        assert output_parent == self.root / "receiver-results"
        self.apply_started.set()
        await self.release_apply.wait()
        result_root = output_parent / "northstar-shared"
        return FolderRunPresentation(
            source_root=source_root,
            output_parent=output_parent,
            result_root=result_root,
            data_root=result_root / "data",
            source_file_count=6,
            path_change_count=5,
            supported_link_count=2,
            supported_link_update_count=2,
            source_unchanged=True,
            all_files_present_once=True,
            deterministic_proof_passed=True,
            independent_verification_passed=True,
            reconstruction_available=True,
            receipt_fingerprint="a" * 64,
            change_file_fingerprint="b" * 64,
            originating_receipt_fingerprint="c" * 64,
            organized_tree_commitment="d" * 64,
            execution_role="receiver",
        )


class _ConcurrentConnectedService:
    """Hold each journey open so concurrent submissions exercise the state gate."""

    evidence_disclosure_required = False
    planner_label = "Deterministic concurrency acceptance"
    planner_note = "No provider call is made by this route-level test double."

    def __init__(
        self,
        root: Path,
        *,
        planner_label: str | None = None,
    ) -> None:
        self.root = root
        if planner_label is not None:
            self.planner_label = planner_label
        self.plan_started = asyncio.Event()
        self.release_plan = asyncio.Event()
        self.apply_started = asyncio.Event()
        self.release_apply = asyncio.Event()
        self.plan_calls = 0
        self.apply_calls = 0

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunPresentation:
        self.plan_calls += 1
        assert request == "Organize this project once."
        self.plan_started.set()
        await self.release_plan.wait()
        return _presentation(
            source_root=source_root,
            output_parent=output_parent,
            execution_role="origin",
        )

    async def apply_shared_change(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> FolderRunPresentation:
        self.apply_calls += 1
        assert change_file_path == self.root / "northstar.nameatlas-change.json"
        self.apply_started.set()
        await self.release_apply.wait()
        return _presentation(
            source_root=source_root,
            output_parent=output_parent,
            execution_role="receiver",
        )


class _ClarifyingService:
    """Expose one bound question and hold its single continuation open."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.plan_calls = 0
        self.continuation_calls = 0
        self.continuation_started = asyncio.Event()
        self.release_continuation = asyncio.Event()

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderClarificationRequest:
        del source_root, output_parent
        self.plan_calls += 1
        assert request == "Prepare the approved presentation."
        return FolderClarificationRequest(
            question="Which presentation is approved for delivery?",
            continuation_token="one-question-token",
        )

    async def continue_after_clarification(
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderRunPresentation:
        self.continuation_calls += 1
        assert continuation_token == "one-question-token"
        assert answer == "Use the client-approved presentation."
        self.continuation_started.set()
        await self.release_continuation.wait()
        return _presentation(
            source_root=self.root / "source",
            output_parent=self.root / "results",
            execution_role="origin",
        )


@dataclass(frozen=True, slots=True)
class _VerificationResult:
    status: str
    receipt_fingerprint: str | None
    failed_check_ids: tuple[str, ...] = ()


class _ActionConnectedService:
    """Project successful and failed result-action outcomes through C2 routes."""

    evidence_disclosure_required = False
    planner_label = "Deterministic result-action acceptance"
    planner_note = "No provider call is made by this route-level test double."

    def __init__(self) -> None:
        self.block_verification = False
        self.verification_calls = 0

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunPresentation:
        assert request == "Create one verified result."
        return _presentation(
            source_root=source_root,
            output_parent=output_parent,
            execution_role="origin",
        )

    async def apply_shared_change(
        self,
        *,
        change_file_path: Path,
        source_root: Path,
        output_parent: Path,
    ) -> FolderRunPresentation:
        del change_file_path
        return _presentation(
            source_root=source_root,
            output_parent=output_parent,
            execution_role="receiver",
        )

    def verify_again(self) -> _VerificationResult:
        self.verification_calls += 1
        if self.block_verification:
            return _VerificationResult(
                status="blocked",
                receipt_fingerprint=None,
                failed_check_ids=("controlled_verification_failure",),
            )
        return _VerificationResult(
            status="verified",
            receipt_fingerprint="e" * 64,
        )

    def recreate_original(self, destination: Path) -> None:
        del destination
        raise AssertionError("This test double does not exercise reconstruction.")


def _presentation(
    *,
    source_root: Path,
    output_parent: Path,
    execution_role: str,
) -> FolderRunPresentation:
    result_root = output_parent / "northstar-shared"
    return FolderRunPresentation(
        source_root=source_root,
        output_parent=output_parent,
        result_root=result_root,
        data_root=result_root / "data",
        source_file_count=6,
        path_change_count=5,
        supported_link_count=2,
        supported_link_update_count=2,
        source_unchanged=True,
        all_files_present_once=True,
        deterministic_proof_passed=True,
        independent_verification_passed=True,
        reconstruction_available=True,
        receipt_fingerprint="a" * 64,
        change_file_fingerprint="b" * 64,
        originating_receipt_fingerprint="c" * 64,
        organized_tree_commitment="d" * 64,
        execution_role=execution_role,
    )


@pytest.mark.anyio
async def test_connected_home_consent_manual_paths_and_no_legacy_routes(
    tmp_path: Path,
) -> None:
    service = ConnectedBrowserRunService(job_path=tmp_path / "jobs" / "idle.json")
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        home = await client.get("/")
        organize = await client.get("/start")
        apply = await client.get("/apply")
        stylesheet = await client.get("/static/folder.css?v=c2-accessibility")
        csrf_token = _csrf(organize)
        no_consent = await client.post(
            "/start",
            data={
                "source_root": str(tmp_path / "source"),
                "user_request": "Prepare this folder for handoff.",
                "output_parent": str(tmp_path),
                "csrf_token": csrf_token,
            },
        )
        legacy = {
            path: await client.get(path)
            for path in ("/atlas", "/decide", "/stage", "/verify", "/handoff")
        }

    assert home.status_code == 200
    assert "Organize a folder" in home.text
    assert "Apply a shared change" in home.text
    assert 'href="/start"' in home.text
    assert 'href="/apply"' in home.text
    assert organize.status_code == 200
    assert 'name="source_root"' in organize.text
    assert 'name="output_parent"' in organize.text
    assert 'name="user_request"' in organize.text
    assert 'name="evidence_disclosure_acknowledged"' in organize.text
    assert "Choose folder…" in organize.text
    assert "Or enter the absolute path" in organize.text
    assert "Your original folder will not be changed." in organize.text
    assert "picker.focus({preventScroll: true});" in organize.text
    assert apply.status_code == 200
    assert "Choose Change File…" in apply.text
    assert "Choose your project folder…" in apply.text
    assert "Apply change and create copy" in apply.text
    assert stylesheet.status_code == 200
    assert "border: 1px solid #66717d;" in stylesheet.text
    assert ".folder-alert > span" in stylesheet.text
    assert "overflow-wrap: anywhere;" in stylesheet.text
    assert no_consent.status_code == 422
    assert "Exactly the displayed Start fields are required" in no_consent.text
    assert not service.job_path.exists()
    assert all(response.status_code == 404 for response in legacy.values())


@pytest.mark.anyio
async def test_apply_working_state_is_truthful_and_never_invokes_planning(
    tmp_path: Path,
) -> None:
    service = _GatedApplyService(tmp_path)
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        apply = await client.get("/apply")
        csrf_token = _csrf(apply)
        started = await client.post(
            "/apply",
            data={
                "change_file": str(tmp_path / "northstar.nameatlas-change.json"),
                "source_root": str(tmp_path / "martin-project"),
                "output_parent": str(tmp_path / "receiver-results"),
                "csrf_token": csrf_token,
            },
        )
        await asyncio.wait_for(service.apply_started.wait(), timeout=1)
        working = await client.get("/working")
        status = await client.get("/status")
        service.release_apply.set()
        await _wait_for_lifecycle(client, "verified")
        done = await client.get("/done")

    assert started.status_code == 303
    assert started.headers["location"] == "/working"
    assert status.json()["journey"] == "apply"
    assert "Matching the shared change" in working.text
    assert "Change File application — no GPT or API" in working.text
    assert "GPT-5.6 is planning" not in working.text
    assert "Name Atlas is planning the change" not in working.text
    assert "data-progress-list" in working.text
    assert 'aria-current="step"' in working.text
    assert "data-stage-status" in working.text
    assert "Current step: Reading folder" in working.text
    assert "updateNameAtlasProgress(status);" in working.text
    assert service.apply_calls == 1
    assert service.plan_calls == 0
    assert done.status_code == 200
    assert "Your new folder is ready" in done.text
    assert "Download Change File" in done.text
    assert "Show in Finder" in done.text
    assert "Verify again" in done.text
    assert "Recreate original layout" in done.text


@pytest.mark.anyio
@pytest.mark.parametrize(
    "planner_label",
    [
        "Recorded GPT-5.6 planning run",
        "Live GPT-5.6 planning",
    ],
)
async def test_gpt_origin_working_stage_is_truthful_for_live_and_replay(
    tmp_path: Path,
    planner_label: str,
) -> None:
    service = _ConcurrentConnectedService(
        tmp_path,
        planner_label=planner_label,
    )
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        started = await client.post(
            "/start",
            data={
                "source_root": str(tmp_path / "source"),
                "user_request": "Organize this project once.",
                "output_parent": str(tmp_path / "results"),
                "csrf_token": csrf_token,
            },
        )
        await asyncio.wait_for(service.plan_started.wait(), timeout=1)
        working = await client.get("/working")
        service.release_plan.set()
        await _wait_for_lifecycle(client, "verified")

    assert started.status_code == 303
    assert planner_label in working.text
    assert "GPT-5.6 is planning" in working.text
    assert "Deterministic planning — no API call" not in working.text
    assert "Matching the shared change" not in working.text


@pytest.mark.anyio
@pytest.mark.parametrize("journey", ["organize", "apply"])
async def test_concurrent_primary_submissions_start_exactly_one_worker(
    tmp_path: Path,
    journey: str,
) -> None:
    service = _ConcurrentConnectedService(tmp_path)
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        if journey == "organize":
            csrf_token = _csrf(await client.get("/start"))
            url = "/start"
            data = {
                "source_root": str(tmp_path / "source"),
                "user_request": "Organize this project once.",
                "output_parent": str(tmp_path / "results"),
                "csrf_token": csrf_token,
            }
            started_event = service.plan_started
            release_event = service.release_plan
        else:
            csrf_token = _csrf(await client.get("/apply"))
            url = "/apply"
            data = {
                "change_file": str(tmp_path / "northstar.nameatlas-change.json"),
                "source_root": str(tmp_path / "receiver-source"),
                "output_parent": str(tmp_path / "receiver-results"),
                "csrf_token": csrf_token,
            }
            started_event = service.apply_started
            release_event = service.release_apply

        responses = await asyncio.gather(
            client.post(url, data=data),
            client.post(url, data=data),
        )
        await asyncio.wait_for(started_event.wait(), timeout=1)

        assert [response.status_code for response in responses] == [303, 303]
        assert {response.headers["location"] for response in responses} == {"/working"}
        assert service.plan_calls + service.apply_calls == 1
        assert service.plan_calls == (1 if journey == "organize" else 0)
        assert service.apply_calls == (1 if journey == "apply" else 0)

        release_event.set()
        status = await _wait_for_lifecycle(client, "verified")

    assert status["journey"] == journey


@pytest.mark.anyio
async def test_concurrent_clarification_submissions_accept_exactly_one_answer(
    tmp_path: Path,
) -> None:
    service = _ClarifyingService(tmp_path)
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        started = await client.post(
            "/start",
            data={
                "source_root": str(tmp_path / "source"),
                "user_request": "Prepare the approved presentation.",
                "output_parent": str(tmp_path / "results"),
                "csrf_token": csrf_token,
            },
        )
        awaiting = await _wait_for_lifecycle(client, "awaiting_clarification")
        working = await client.get("/working")
        responses = await asyncio.gather(
            client.post(
                "/clarify",
                data={
                    "answer": "Use the client-approved presentation.",
                    "csrf_token": csrf_token,
                },
            ),
            client.post(
                "/clarify",
                data={
                    "answer": "Use the client-approved presentation.",
                    "csrf_token": csrf_token,
                },
            ),
        )
        await asyncio.wait_for(service.continuation_started.wait(), timeout=1)

        assert started.status_code == 303
        assert awaiting["clarification_required"] is True
        assert "Which presentation is approved for delivery?" in working.text
        assert sorted(response.status_code for response in responses) == [303, 409]
        assert service.plan_calls == 1
        assert service.continuation_calls == 1

        service.release_continuation.set()
        verified = await _wait_for_lifecycle(client, "verified")

    assert verified["journey"] == "organize"


@pytest.mark.anyio
async def test_manual_source_paths_derive_output_until_user_override() -> None:
    service = _ConcurrentConnectedService(Path("/tmp/name-atlas-c2-static"))
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        apply = await client.get("/apply")

    for response in (start, apply):
        assert response.status_code == 200
        assert 'name="source_root"' in response.text
        assert 'data-derive-output-target="output-parent"' in response.text
        assert 'name="output_parent"' in response.text
        assert 'field.name === "source_root"' in response.text
        assert 'field.name === "output_parent"' in response.text
        assert 'output.dataset.userOverridden !== "true"' in response.text
        assert 'field.dataset.userOverridden = field.value ? "true" : "false"' in (
            response.text
        )
        assert "output.value = deriveParent(source.value)" in response.text


@pytest.mark.anyio
async def test_native_picker_boundary_and_manual_fallback_are_exact(
    tmp_path: Path,
) -> None:
    selected_source = (tmp_path / "selected-source").resolve()
    bridge = _FakeNativeBridge(
        selections={
            NativePathRole.SOURCE_FOLDER: NativePathSelection(
                status=NativeSelectionStatus.SELECTED,
                path=selected_source,
            ),
            NativePathRole.CHANGE_FILE: NativePathSelection(
                status=NativeSelectionStatus.CANCELLED,
                reason_code="picker_cancelled",
            ),
        }
    )
    service = ConnectedBrowserRunService(job_path=tmp_path / "jobs" / "picker.json")
    transport = httpx.ASGITransport(
        app=create_folder_app(service, native_bridge=bridge)
    )

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        csrf_token = _csrf(start)
        selected = await client.post(
            "/choose-path",
            data={"role": "source_folder", "csrf_token": csrf_token},
        )
        cancelled = await client.post(
            "/choose-path",
            data={"role": "change_file", "csrf_token": csrf_token},
        )
        invalid_role = await client.post(
            "/choose-path",
            data={"role": "arbitrary_path", "csrf_token": csrf_token},
        )
        invalid_csrf = await client.post(
            "/choose-path",
            data={"role": "source_folder", "csrf_token": "wrong"},
        )
        extra_field = await client.post(
            "/choose-path",
            data={
                "role": "source_folder",
                "csrf_token": csrf_token,
                "path": "/browser-controlled/path",
            },
        )
        cross_origin = await client.post(
            "/choose-path",
            data={"role": "source_folder", "csrf_token": csrf_token},
            headers={"Origin": "http://malicious.example"},
        )

    assert selected.status_code == 200
    assert selected.json() == {"status": "selected", "path": str(selected_source)}
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert "Manual paths remain available" in cancelled.json()["message"]
    assert "path" not in cancelled.json()
    assert invalid_role.status_code == 422
    assert invalid_role.json()["status"] == "failed"
    assert invalid_csrf.status_code == 422
    assert extra_field.status_code == 422
    assert cross_origin.status_code == 403
    assert bridge.selected_roles == [
        NativePathRole.SOURCE_FOLDER,
        NativePathRole.CHANGE_FILE,
    ]
    assert 'name="source_root"' in start.text
    assert 'name="output_parent"' in start.text
    assert "Or enter the absolute path" in start.text
    assert not service.job_path.exists()


@pytest.mark.anyio
async def test_picker_statuses_restore_derivation_and_request_guards_are_exact(
    tmp_path: Path,
) -> None:
    restore_parent = tmp_path / "restore-parent"
    restore_parent.mkdir()
    occupied_child = restore_parent / "name-atlas-original-layout"
    occupied_child.mkdir()
    expected_restore = restore_parent / "name-atlas-original-layout-2"
    bridge = _FakeNativeBridge(
        selections={
            NativePathRole.SOURCE_FOLDER: NativePathSelection(
                status=NativeSelectionStatus.UNAVAILABLE,
                reason_code="picker_unavailable",
            ),
            NativePathRole.OUTPUT_PARENT: NativePathSelection(
                status=NativeSelectionStatus.TIMEOUT,
                reason_code="picker_timeout",
            ),
            NativePathRole.CHANGE_FILE: NativePathSelection(
                status=NativeSelectionStatus.FAILED,
                reason_code="picker_failed",
            ),
            NativePathRole.RESTORE_DESTINATION: NativePathSelection(
                status=NativeSelectionStatus.SELECTED,
                path=restore_parent,
            ),
        }
    )
    service = ConnectedBrowserRunService(job_path=tmp_path / "jobs" / "picker.json")
    transport = httpx.ASGITransport(
        app=create_folder_app(service, native_bridge=bridge)
    )

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        unavailable = await client.post(
            "/choose-path",
            data={"role": "source_folder", "csrf_token": csrf_token},
        )
        timeout = await client.post(
            "/choose-path",
            data={"role": "output_parent", "csrf_token": csrf_token},
        )
        failed = await client.post(
            "/choose-path",
            data={"role": "change_file", "csrf_token": csrf_token},
        )
        restore = await client.post(
            "/choose-path",
            data={"role": "restore_destination", "csrf_token": csrf_token},
        )
        cross_site = await client.post(
            "/choose-path",
            data={"role": "source_folder", "csrf_token": csrf_token},
            headers={"Sec-Fetch-Site": "cross-site"},
        )
        invalid_host = await client.get("/", headers={"Host": "malicious.example"})
        malformed_start = await client.post(
            "/start",
            content=(
                "source_root=%2Ftmp%2Fsource&user_request=%FF&"
                "output_parent=%2Ftmp&csrf_token=" + csrf_token
            ).encode("ascii"),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    assert unavailable.status_code == 200
    assert unavailable.json() == {
        "status": "unavailable",
        "message": "Native selection is unavailable. Enter an absolute path manually.",
    }
    assert timeout.status_code == 200
    assert timeout.json() == {
        "status": "timeout",
        "message": "Native selection timed out. Enter an absolute path manually.",
    }
    assert failed.status_code == 200
    assert failed.json() == {
        "status": "failed",
        "message": "Native selection failed. Enter an absolute path manually.",
    }
    assert restore.status_code == 200
    assert restore.json() == {"status": "selected", "path": str(expected_restore)}
    assert not expected_restore.exists()
    assert cross_site.status_code == 403
    assert invalid_host.status_code == 400
    assert malformed_start.status_code == 422
    assert "not valid UTF-8 form data" in malformed_start.text
    assert bridge.selected_roles == [
        NativePathRole.SOURCE_FOLDER,
        NativePathRole.OUTPUT_PARENT,
        NativePathRole.CHANGE_FILE,
        NativePathRole.RESTORE_DESTINATION,
    ]
    assert not service.job_path.exists()


@pytest.mark.anyio
async def test_verify_again_projects_success_then_replaces_it_with_failure(
    tmp_path: Path,
) -> None:
    service = _ActionConnectedService()
    transport = httpx.ASGITransport(app=create_folder_app(service))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        csrf_token = _csrf(await client.get("/start"))
        await client.post(
            "/start",
            data={
                "source_root": str(tmp_path / "source"),
                "user_request": "Create one verified result.",
                "output_parent": str(tmp_path / "results"),
                "csrf_token": csrf_token,
            },
        )
        await _wait_for_lifecycle(client, "verified")
        verified = await client.post(
            "/verify-again",
            data={"csrf_token": csrf_token},
        )
        verified_done = await client.get("/done")
        service.block_verification = True
        blocked = await client.post(
            "/verify-again",
            data={"csrf_token": csrf_token},
        )
        blocked_working = await client.get(blocked.headers["location"])
        unavailable_done = await client.get("/done", follow_redirects=False)

    assert verified.status_code == 303
    assert verified.headers["location"] == "/done"
    assert "Independent keyless verification passed again" in verified_done.text
    assert "Receipt " + ("e" * 64) not in verified_done.text
    assert blocked.status_code == 303
    assert blocked.headers["location"] == "/working"
    assert blocked_working.status_code == 200
    assert "controlled_verification_failure" in blocked_working.text
    assert unavailable_done.status_code == 303
    assert unavailable_done.headers["location"] == "/working"
    assert service.verification_calls == 2


@pytest.mark.anyio
async def test_real_origin_receiver_restart_download_finder_and_tamper_refusal(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    sofia_before = tree_state(fixture.sofia_root)
    martin_before = tree_state(fixture.martin_root)
    origin_output = tmp_path / "origin-results"
    receiver_output = tmp_path / "receiver-results"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin_job = tmp_path / "jobs" / "origin.json"
    receiver_job = tmp_path / "jobs" / "receiver.json"
    origin_bridge = _FakeNativeBridge()
    origin_service = ConnectedBrowserRunService(job_path=origin_job)
    origin_app = create_folder_app(origin_service, native_bridge=origin_bridge)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=origin_app),
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        csrf_token = _csrf(start)
        started = await client.post(
            "/start",
            data={
                "source_root": str(fixture.sofia_root),
                "user_request": DETERMINISTIC_BROWSER_REQUEST,
                "output_parent": str(origin_output),
                "evidence_disclosure_acknowledged": "true",
                "csrf_token": csrf_token,
            },
        )
        origin_status = await _wait_for_lifecycle(client, "verified")
        done = await client.get("/done")
        job_before_status = origin_job.read_bytes()
        repeated_status = await client.get("/status")
        job_after_status = origin_job.read_bytes()
        invalid_finder = await client.post(
            "/show-in-finder",
            data={
                "csrf_token": csrf_token,
                "path": "/browser-controlled/path",
            },
        )
        opened = await client.post(
            "/show-in-finder",
            data={"csrf_token": csrf_token},
        )
        opened_done = await client.get("/done")
        download = await client.get("/download-change-file")

    assert started.status_code == 303
    assert origin_status["journey"] == "organize"
    assert repeated_status.json()["lifecycle"] == "verified"
    assert job_before_status == job_after_status
    assert tree_state(fixture.sofia_root) == sofia_before
    checkpoint = origin_service.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.result is not None
    origin_result = checkpoint.result
    change_file_path = origin_result.result_root / CONNECTED_CHANGE_PATH
    assert done.status_code == 200
    assert "Your new folder is ready" in done.text
    assert "Ready and bound to this verified result" in done.text
    assert "Original folder</dt><dd>Unchanged" in done.text
    assert invalid_finder.status_code == 422
    assert origin_bridge.opened_paths == [origin_result.data_root]
    assert opened.status_code == 303
    assert "verified new folder was opened in Finder" in opened_done.text
    assert download.status_code == 200
    assert download.content == change_file_path.read_bytes()
    assert download.headers["content-type"] == "application/json"
    assert download.headers["cache-control"] == "no-store"
    assert download.headers["x-content-type-options"] == "nosniff"
    assert ".nameatlas-change.json" in download.headers["content-disposition"]

    restarted_service = ConnectedBrowserRunService(job_path=origin_job)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(restarted_service)),
        base_url="http://testserver",
    ) as restarted_client:
        restarted_root = await restarted_client.get("/")
        restarted_done = await restarted_client.get("/done")
        restart_job_before = origin_job.read_bytes()
        restarted_status = await restarted_client.get("/status")
        restart_job_after = origin_job.read_bytes()

    assert restarted_root.status_code == 303
    assert restarted_root.headers["location"] == "/done"
    assert restarted_done.status_code == 200
    assert restarted_status.json()["lifecycle"] == "verified"
    assert restart_job_before == restart_job_after

    restore_parent = tmp_path / "reconstructions"
    restore_parent.mkdir()
    receiver_bridge = _FakeNativeBridge(
        selections={
            NativePathRole.RESTORE_DESTINATION: NativePathSelection(
                status=NativeSelectionStatus.SELECTED,
                path=restore_parent,
            )
        }
    )
    receiver_service = ConnectedBrowserRunService(job_path=receiver_job)
    receiver_app = create_folder_app(
        receiver_service,
        native_bridge=receiver_bridge,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=receiver_app),
        base_url="http://testserver",
    ) as receiver_client:
        apply = await receiver_client.get("/apply")
        receiver_csrf = _csrf(apply)
        applied = await receiver_client.post(
            "/apply",
            data={
                "change_file": str(change_file_path),
                "source_root": str(fixture.martin_root),
                "output_parent": str(receiver_output),
                "csrf_token": receiver_csrf,
            },
        )
        receiver_status = await _wait_for_lifecycle(receiver_client, "verified")
        receiver_done = await receiver_client.get("/done")
        reverified = await receiver_client.post(
            "/verify-again",
            data={"csrf_token": receiver_csrf},
        )
        reverified_done = await receiver_client.get("/done")
        selected_restore = await receiver_client.post(
            "/choose-path",
            data={
                "role": "restore_destination",
                "csrf_token": receiver_csrf,
            },
        )
        restored_path = Path(selected_restore.json()["path"])
        recreated = await receiver_client.post(
            "/recreate-original",
            data={
                "restore_destination": str(restored_path),
                "csrf_token": receiver_csrf,
            },
        )
        recreated_done = await receiver_client.get("/done")

    assert applied.status_code == 303
    assert receiver_status["journey"] == "apply"
    assert receiver_done.status_code == 200
    assert "Your new folder is ready" in receiver_done.text
    assert "Ready and bound to this verified result" in receiver_done.text
    assert "GPT-5.6 is planning" not in receiver_done.text
    assert reverified.status_code == 303
    assert reverified.headers["location"] == "/done"
    assert "Independent keyless verification passed" in reverified_done.text
    assert selected_restore.status_code == 200
    assert restored_path == restore_parent / "martin-project-original-layout"
    assert recreated.status_code == 303
    assert recreated.headers["location"] == "/done"
    assert f"Original layout recreated and verified at {restored_path}" in (
        recreated_done.text
    )
    assert portable_tree(restored_path) == portable_tree(fixture.martin_root)
    assert receiver_bridge.selected_roles == [NativePathRole.RESTORE_DESTINATION]
    assert tree_state(fixture.martin_root) == martin_before
    receiver_checkpoint = receiver_service.web_checkpoint()
    assert receiver_checkpoint is not None
    assert receiver_checkpoint.result is not None
    assert (
        receiver_checkpoint.result.organized_tree_commitment
        == origin_result.organized_tree_commitment
    )

    receiver_change_file = (
        receiver_checkpoint.result.result_root / CONNECTED_CHANGE_PATH
    )
    receiver_change_file.write_bytes(receiver_change_file.read_bytes() + b"\n")
    rejected_destination = tmp_path / "must-not-be-created"
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=receiver_app),
        base_url="http://testserver",
    ) as tampered_receiver_client:
        rejected_reconstruction = await tampered_receiver_client.post(
            "/recreate-original",
            data={
                "restore_destination": str(rejected_destination),
                "csrf_token": receiver_csrf,
            },
        )
        tampered_receiver_status = await tampered_receiver_client.get("/status")
        tampered_receiver_working = await tampered_receiver_client.get("/working")

    assert rejected_reconstruction.status_code == 303
    assert rejected_reconstruction.headers["location"] == "/working"
    assert tampered_receiver_status.json()["lifecycle"] == "blocked"
    assert "receipt_verification_blocked" in tampered_receiver_working.text
    assert not rejected_destination.exists()

    change_file_path.write_bytes(change_file_path.read_bytes() + b"\n")
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=origin_app),
        base_url="http://testserver",
    ) as tampered_client:
        blocked_download = await tampered_client.get("/download-change-file")
        blocked_status = await tampered_client.get("/status")

    assert blocked_download.status_code == 409
    assert blocked_status.json()["lifecycle"] == "blocked"
    tampered_restart_app = create_folder_app(
        ConnectedBrowserRunService(job_path=origin_job)
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=tampered_restart_app),
        base_url="http://testserver",
    ) as tampered_restart_client:
        tampered_restart_root = await tampered_restart_client.get(
            "/", follow_redirects=False
        )
        tampered_restart_status = await tampered_restart_client.get("/status")
        tampered_restart_working = await tampered_restart_client.get("/working")

    assert tampered_restart_root.status_code == 303
    assert tampered_restart_root.headers["location"] == "/working"
    assert tampered_restart_status.json()["lifecycle"] == "blocked"
    assert "Independent verification blocked" in tampered_restart_working.text
    assert tree_state(fixture.sofia_root) == sofia_before
    assert tree_state(fixture.martin_root) == martin_before
