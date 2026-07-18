"""Integrated durable browser-service tests for the A2 folder workflow."""

from __future__ import annotations

import asyncio
import threading
import time
from pathlib import Path
from typing import Literal

import httpx
import pytest

import name_atlas.folder_job_service as folder_job_service_module
import name_atlas.folder_refactor.planner_evidence as planner_evidence_module
from name_atlas.folder_app import (
    FolderClarificationRequest,
    FolderRunPresentation,
    FolderWorkPhase,
    create_folder_app,
)
from name_atlas.folder_job_service import (
    FolderJobServiceError,
    JobBackedFolderRunService,
)
from name_atlas.folder_refactor.inventory import FolderScan
from name_atlas.folder_refactor.job import (
    FolderJobLifecycle,
    FolderRefactorJobStore,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    ProviderToolResponse,
    RequestClarificationCall,
)
from name_atlas.folder_refactor.planner_provider import (
    DETERMINISTIC_DEVELOPMENT_REQUEST,
    DeterministicDevelopmentPlannerProvider,
)
from name_atlas.folder_refactor.transaction import FolderTransactionError

REQUEST = DETERMINISTIC_DEVELOPMENT_REQUEST


async def _wait_for_lifecycle(
    client: httpx.AsyncClient,
    expected: str,
) -> httpx.Response:
    for _ in range(100):
        response = await client.get("/status")
        if response.json()["lifecycle"] == expected:
            return response
        await asyncio.sleep(0.01)
    raise AssertionError(f"Lifecycle did not reach {expected}.")


def _source(tmp_path: Path) -> tuple[Path, Path]:
    source = tmp_path / "source"
    output = tmp_path / "results"
    source.mkdir()
    output.mkdir()
    (source / "note.md").write_text("[report](report.txt)\n", encoding="utf-8")
    (source / "report.txt").write_text("approved\n", encoding="utf-8")
    (source / ".env.local").write_text("DEMO=true\n", encoding="utf-8")
    return source, output


class _ClarificationProvider:
    def __init__(self, calls: list[FolderPlannerTurnInput]) -> None:
        self._calls = calls

    @property
    def provider_kind(self) -> Literal["deterministic"]:
        return "deterministic"

    async def exchange(self, turn_input: FolderPlannerTurnInput, /):
        self._calls.append(turn_input)
        if turn_input.clarification_answer is None:
            return ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(
                    RequestClarificationCall(
                        call_id="one-question",
                        question="Which presentation is approved for delivery?",
                        missing_facts=("approved_presentation",),
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            )
        return await DeterministicDevelopmentPlannerProvider(
            result_folder_name="clarified-result",
            allowed_request=turn_input.request,
        ).exchange(turn_input)


@pytest.mark.anyio
async def test_zero_question_job_creates_one_verified_process_result(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "zero-question.json"
    service = JobBackedFolderRunService(
        job_path=job_path,
        result_folder_name="organized-result",
    )
    phases: list[FolderWorkPhase] = []
    service.set_progress_callback(phases.append)

    result = await service.plan_and_create_copy(
        source_root=source,
        output_parent=output,
        request=REQUEST,
    )

    assert isinstance(result, FolderRunPresentation)
    assert result.supported_link_count == 1
    assert result.source_unchanged is True
    assert (result.data_root / "organized" / "note.md").is_file()
    assert (result.data_root / ".env.local").is_file()
    job = FolderRefactorJobStore(job_path).load()
    assert job.lifecycle is FolderJobLifecycle.EXECUTING
    assert job.accepted_plan is not None
    checkpoint = service.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.result == result
    assert phases == [
        FolderWorkPhase.READING,
        FolderWorkPhase.PLANNING,
        FolderWorkPhase.CHECKING,
        FolderWorkPhase.CREATING,
        FolderWorkPhase.UPDATING_LINKS,
        FolderWorkPhase.VERIFYING,
    ]


@pytest.mark.anyio
async def test_unsupported_request_blocks_before_provider_or_result(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "blocked.json"
    provider = DeterministicDevelopmentPlannerProvider()
    service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )

    with pytest.raises(FolderJobServiceError, match="file_deletion_unsupported"):
        await service.plan_and_create_copy(
            source_root=source,
            output_parent=output,
            request="Eliminate outdated files and organize the rest.",
        )

    assert provider.invocation_count == 0
    assert not any(output.iterdir())
    assert FolderRefactorJobStore(job_path).load().lifecycle is (
        FolderJobLifecycle.BLOCKED
    )


@pytest.mark.anyio
async def test_unrecorded_request_cannot_reach_done_or_create_result(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "unrecorded-request.json"
    provider = DeterministicDevelopmentPlannerProvider()
    service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )

    with pytest.raises(
        FolderJobServiceError,
        match="deterministic_request_not_recorded",
    ):
        await service.plan_and_create_copy(
            source_root=source,
            output_parent=output,
            request="Toss obsolete drafts and organize the rest.",
        )

    blocked = FolderRefactorJobStore(job_path).load()
    assert blocked.lifecycle is FolderJobLifecycle.BLOCKED
    assert blocked.blocker_code == "deterministic_request_not_recorded"
    assert provider.invocation_count == 1
    assert not any(output.iterdir())


@pytest.mark.anyio
async def test_oversized_initial_evidence_is_durably_blocked_before_provider(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "evidence-limit.json"
    provider = DeterministicDevelopmentPlannerProvider()
    service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    monkeypatch.setattr(
        planner_evidence_module,
        "MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES",
        64,
    )

    with pytest.raises(FolderJobServiceError, match="initial_evidence_limit_exceeded"):
        await service.plan_and_create_copy(
            source_root=source,
            output_parent=output,
            request=REQUEST,
        )

    blocked = FolderRefactorJobStore(job_path).load()
    assert blocked.lifecycle is FolderJobLifecycle.BLOCKED
    assert blocked.blocker_code == "initial_evidence_limit_exceeded"
    assert provider.invocation_count == 0
    assert not any(output.iterdir())


@pytest.mark.anyio
async def test_real_long_path_inventory_limit_rehydrates_as_terminal_blocker(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "results"
    source.mkdir()
    output.mkdir()
    deepest = source
    for character in ("a", "b", "c", "d"):
        deepest /= character * 200
        deepest.mkdir()
    for index in range(500):
        filename = f"{index:03d}-{'x' * 72}.txt"
        (deepest / filename).write_text("x", encoding="utf-8")

    job_path = tmp_path / "jobs" / "real-evidence-limit.json"
    provider = DeterministicDevelopmentPlannerProvider()
    service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )

    with pytest.raises(FolderJobServiceError, match="initial_evidence_limit_exceeded"):
        await service.plan_and_create_copy(
            source_root=source,
            output_parent=output,
            request=REQUEST,
        )

    blocked = FolderRefactorJobStore(job_path).load()
    assert blocked.lifecycle is FolderJobLifecycle.BLOCKED
    assert blocked.blocker_code == "initial_evidence_limit_exceeded"
    assert provider.invocation_count == 0
    assert not any(output.iterdir())

    restarted = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    checkpoint = restarted.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle.value == "blocked"
    assert checkpoint.blocker is not None
    assert checkpoint.blocker.startswith("initial_evidence_limit_exceeded:")
    assert provider.invocation_count == 0


@pytest.mark.anyio
async def test_protected_markdown_link_context_blocks_before_provider(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "results"
    source.mkdir()
    output.mkdir()
    (source / ".notes.md").write_text("[report](report.txt)\n", encoding="utf-8")
    (source / "report.txt").write_text("report\n", encoding="utf-8")
    provider = DeterministicDevelopmentPlannerProvider()
    job_path = tmp_path / "jobs" / "protected-link.json"
    service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )

    with pytest.raises(
        FolderTransactionError,
        match="protected_markdown_link_context_unsupported",
    ):
        await service.plan_and_create_copy(
            source_root=source,
            output_parent=output,
            request=REQUEST,
        )

    assert provider.invocation_count == 0
    assert not job_path.exists()
    assert not any(output.iterdir())


@pytest.mark.anyio
async def test_one_question_rehydrates_without_duplicate_provider_call(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "clarification.json"
    calls: list[FolderPlannerTurnInput] = []

    def provider_factory(_job: object) -> _ClarificationProvider:
        return _ClarificationProvider(calls)

    first_service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=provider_factory,
    )

    first = await first_service.plan_and_create_copy(
        source_root=source,
        output_parent=output,
        request="Put the approved presentation in final deliverables.",
    )
    assert isinstance(first, FolderClarificationRequest)
    assert len(calls) == 1

    resumed_service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=provider_factory,
    )
    checkpoint = resumed_service.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.clarification == first
    assert len(calls) == 1

    result = await resumed_service.continue_after_clarification(
        continuation_token=first.continuation_token,
        answer="Use the Northstar final presentation.",
    )

    assert result.result_root.name == "clarified-result"
    assert len(calls) == 2
    loaded = FolderRefactorJobStore(job_path).load()
    assert loaded.planner_progress is not None
    assert loaded.planner_progress.clarification_answer == (
        "Use the Northstar final presentation."
    )


@pytest.mark.anyio
async def test_executing_job_resumes_without_another_provider_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "resume-execution.json"
    provider = DeterministicDevelopmentPlannerProvider(
        result_folder_name="resumed-result"
    )
    first_service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )

    def crash_before_execution(*_args, **_kwargs):
        raise RuntimeError("simulated process stop before execution")

    monkeypatch.setattr(first_service, "_execute", crash_before_execution)
    with pytest.raises(RuntimeError, match="simulated process stop"):
        await first_service.plan_and_create_copy(
            source_root=source,
            output_parent=output,
            request=REQUEST,
        )
    assert provider.invocation_count == 1
    assert FolderRefactorJobStore(job_path).load().lifecycle is (
        FolderJobLifecycle.EXECUTING
    )

    resumed = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    result = await resumed.resume_existing_job()

    assert isinstance(result, FolderRunPresentation)
    assert result.result_root.name == "resumed-result"
    assert provider.invocation_count == 1


@pytest.mark.anyio
async def test_promoted_result_rehydrates_after_process_restart_without_new_work(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "completed-restart.json"
    provider = DeterministicDevelopmentPlannerProvider(
        result_folder_name="restart-safe-result"
    )
    first = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )

    original = await first.plan_and_create_copy(
        source_root=source,
        output_parent=output,
        request=REQUEST,
    )
    assert isinstance(original, FolderRunPresentation)
    assert provider.invocation_count == 1

    resumed = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    recovered = await resumed.resume_existing_job()

    assert recovered == original
    assert provider.invocation_count == 1
    assert FolderRefactorJobStore(job_path).load().lifecycle is (
        FolderJobLifecycle.EXECUTING
    )

    restarted = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    checkpoint = restarted.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle.value == "verified"
    assert checkpoint.result == original
    assert provider.invocation_count == 1


@pytest.mark.anyio
async def test_corrupt_existing_result_is_durably_blocked_on_restart(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "corrupt-restart.json"
    provider = DeterministicDevelopmentPlannerProvider(
        result_folder_name="corrupt-result"
    )
    first = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    original = await first.plan_and_create_copy(
        source_root=source,
        output_parent=output,
        request=REQUEST,
    )
    assert isinstance(original, FolderRunPresentation)
    (original.data_root / "organized" / "report.txt").write_text(
        "tampered\n",
        encoding="utf-8",
    )

    restarted = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: provider,
    )
    checkpoint = restarted.web_checkpoint()

    assert checkpoint is not None
    assert checkpoint.lifecycle.value == "blocked"
    assert checkpoint.blocker is not None
    assert checkpoint.blocker.startswith("existing_result_recovery_failed:")
    assert FolderRefactorJobStore(job_path).load().lifecycle is (
        FolderJobLifecycle.BLOCKED
    )
    assert provider.invocation_count == 1


@pytest.mark.anyio
async def test_source_change_rehydrates_as_stale_without_provider_call(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "stale.json"
    calls: list[FolderPlannerTurnInput] = []
    service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: _ClarificationProvider(calls),
    )

    outcome = await service.plan_and_create_copy(
        source_root=source,
        output_parent=output,
        request="Put the approved presentation in final deliverables.",
    )
    assert isinstance(outcome, FolderClarificationRequest)
    (source / "report.txt").write_text("changed\n", encoding="utf-8")

    restarted = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=lambda _job: _ClarificationProvider(calls),
    )
    checkpoint = restarted.web_checkpoint()

    assert checkpoint is not None
    assert checkpoint.blocker is not None
    assert checkpoint.blocker.startswith("source_changed:")
    assert len(calls) == 1


@pytest.mark.anyio
async def test_real_browser_start_to_done_uses_durable_job_service(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "browser-zero-question.json"
    service = JobBackedFolderRunService(
        job_path=job_path,
        result_folder_name="browser-result",
    )
    app = create_folder_app(service)
    transport = httpx.ASGITransport(app=app)

    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client,
    ):
        csrf_token = app.state.folder_web_state.csrf_token
        started = await client.post(
            "/start",
            data={
                "source_root": str(source),
                "user_request": REQUEST,
                "output_parent": str(output),
                "csrf_token": csrf_token,
            },
        )
        completed = await _wait_for_lifecycle(client, "verified")
        done = await client.get("/done")

    assert started.status_code == 303
    assert completed.json()["done_url"] == "/done"
    assert done.status_code == 200
    assert "3 of 3, exactly once" in done.text
    assert "Supported Markdown links checked</dt><dd>1" in done.text
    assert "Supported Markdown links updated</dt><dd>0" in done.text
    assert job_path.is_file()
    assert (output / "browser-result" / "data" / "organized" / "note.md").is_file()


@pytest.mark.anyio
async def test_real_browser_remains_responsive_during_slow_mechanical_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "responsive-browser.json"
    service = JobBackedFolderRunService(
        job_path=job_path,
        result_folder_name="responsive-result",
    )
    original_scan = folder_job_service_module.scan_folder_with_references
    scan_started = threading.Event()
    release_scan = threading.Event()

    def delayed_scan(source_root: Path) -> tuple[FolderScan, FolderReferenceGraph]:
        scan_started.set()
        if not release_scan.wait(timeout=2):
            raise RuntimeError("test scan release timed out")
        return original_scan(source_root)

    monkeypatch.setattr(
        folder_job_service_module,
        "scan_folder_with_references",
        delayed_scan,
    )
    app = create_folder_app(service)
    fallback_release = threading.Timer(1.0, release_scan.set)
    fallback_release.start()
    try:
        async with (
            app.router.lifespan_context(app),
            httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="http://testserver",
            ) as client,
        ):
            started_at = time.monotonic()
            started = await client.post(
                "/start",
                data={
                    "source_root": str(source),
                    "user_request": REQUEST,
                    "output_parent": str(output),
                    "csrf_token": app.state.folder_web_state.csrf_token,
                },
            )
            response_seconds = time.monotonic() - started_at
            assert await asyncio.to_thread(scan_started.wait, 0.5)
            status = await client.get("/status")
            working = await client.get("/working")

            assert started.status_code == 303
            assert response_seconds < 0.5
            assert status.json()["lifecycle"] == "planning"
            assert status.json()["current_stage"] == 0
            assert working.status_code == 200
            assert app.state.folder_web_state.worker is not None
            assert app.state.folder_web_state.worker.done() is False
            assert not (output / "responsive-result").exists()

            app.state.folder_web_state.worker.cancel()
            await asyncio.sleep(0)
            assert app.state.folder_web_state.worker.done() is False
            release_scan.set()
            completed = await _wait_for_lifecycle(client, "verified")

        assert completed.json()["done_url"] == "/done"
        assert (output / "responsive-result").is_dir()
        completed_job = FolderRefactorJobStore(job_path).load()
        assert completed_job.accepted_plan is not None
        assert completed_job.lifecycle is FolderJobLifecycle.EXECUTING
    finally:
        release_scan.set()
        fallback_release.cancel()
        fallback_release.join(timeout=1)


@pytest.mark.anyio
async def test_browser_restart_rehydrates_question_without_duplicate_turn(
    tmp_path: Path,
) -> None:
    source, output = _source(tmp_path)
    job_path = tmp_path / "jobs" / "browser-question.json"
    calls: list[FolderPlannerTurnInput] = []

    def provider_factory(_job: object) -> _ClarificationProvider:
        return _ClarificationProvider(calls)

    first_service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=provider_factory,
    )
    first_app = create_folder_app(first_service)

    async with (
        first_app.router.lifespan_context(first_app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=first_app),
            base_url="http://testserver",
        ) as client,
    ):
        csrf_token = first_app.state.folder_web_state.csrf_token
        await client.post(
            "/start",
            data={
                "source_root": str(source),
                "user_request": (
                    "Put the approved presentation in final deliverables."
                ),
                "output_parent": str(output),
                "csrf_token": csrf_token,
            },
        )
        await _wait_for_lifecycle(client, "awaiting_clarification")
    assert len(calls) == 1

    resumed_service = JobBackedFolderRunService(
        job_path=job_path,
        provider_factory=provider_factory,
    )
    resumed_app = create_folder_app(resumed_service)
    async with (
        resumed_app.router.lifespan_context(resumed_app),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=resumed_app),
            base_url="http://testserver",
        ) as client,
    ):
        root = await client.get("/", follow_redirects=False)
        question = await client.get("/working")
        assert len(calls) == 1
        answered = await client.post(
            "/clarify",
            data={
                "answer": "Use the Northstar final presentation.",
                "csrf_token": resumed_app.state.folder_web_state.csrf_token,
            },
        )
        await _wait_for_lifecycle(client, "verified")
        done = await client.get("/done")

    assert root.status_code == 303
    assert root.headers["location"] == "/working"
    assert "Which presentation is approved for delivery?" in question.text
    assert answered.status_code == 303
    assert len(calls) == 2
    assert "Your separate result is ready" in done.text
