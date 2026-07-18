"""A2 server-owned one-question clarification acceptance."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

import httpx
import pytest

from name_atlas.folder_app import (
    FolderClarificationRequest,
    FolderRunOutcome,
    FolderRunPresentation,
    create_folder_app,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _presentation(tmp_path: Path) -> FolderRunPresentation:
    result_root = tmp_path / "results" / "clarified-result"
    return FolderRunPresentation(
        source_root=tmp_path / "source",
        output_parent=tmp_path / "results",
        result_root=result_root,
        data_root=result_root / "data",
        source_file_count=2,
        path_change_count=2,
        source_unchanged=True,
        all_files_present_once=True,
        deterministic_proof_passed=True,
    )


class _ClarifyingService:
    def __init__(self, tmp_path: Path) -> None:
        self.tmp_path = tmp_path
        self.initial_calls = 0
        self.continuation_calls = 0
        self.continuation_started = asyncio.Event()
        self.release = asyncio.Event()
        self.answer: str | None = None
        self.token: str | None = None

    async def plan_and_create_copy(
        self,
        *,
        source_root: Path,
        output_parent: Path,
        request: str,
    ) -> FolderRunOutcome:
        assert source_root == self.tmp_path / "source"
        assert output_parent == self.tmp_path / "results"
        assert request == "Put the approved presentation in final deliverables."
        self.initial_calls += 1
        return FolderClarificationRequest(
            question="Which presentation did you approve for delivery?",
            continuation_token="same-job-42",
        )

    async def continue_after_clarification(
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderRunPresentation:
        self.continuation_calls += 1
        self.token = continuation_token
        self.answer = answer
        self.continuation_started.set()
        await self.release.wait()
        return _presentation(self.tmp_path)


class _SecondQuestionService(_ClarifyingService):
    async def continue_after_clarification(  # type: ignore[override]
        self,
        *,
        continuation_token: str,
        answer: str,
    ) -> FolderClarificationRequest:
        del continuation_token, answer
        self.continuation_calls += 1
        return FolderClarificationRequest(
            question="Can you answer another question?",
            continuation_token="forbidden-second-question",
        )


async def _wait_for_lifecycle(
    client: httpx.AsyncClient,
    expected: str,
) -> httpx.Response:
    for _ in range(50):
        response = await client.get("/status")
        if response.json()["lifecycle"] == expected:
            return response
        await asyncio.sleep(0)
    raise AssertionError(f"Lifecycle did not reach {expected}.")


def _csrf(response: httpx.Response) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    return match.group(1)


@pytest.mark.anyio
async def test_one_question_continues_same_job_once(tmp_path: Path) -> None:
    service = _ClarifyingService(tmp_path)
    app = create_folder_app(service)
    transport = httpx.ASGITransport(app=app)
    start_form = {
        "source_root": str(tmp_path / "source"),
        "user_request": "Put the approved presentation in final deliverables.",
        "output_parent": str(tmp_path / "results"),
    }

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        start_form["csrf_token"] = _csrf(await client.get("/start"))
        started = await client.post("/start", data=start_form)
        awaiting = await _wait_for_lifecycle(client, "awaiting_clarification")
        first_view = await client.get("/working")
        refreshed_view = await client.get("/working")
        csrf_token = _csrf(first_view)
        invalid_answer = await client.post(
            "/clarify",
            data={"answer": "", "csrf_token": csrf_token},
        )
        answered = await client.post(
            "/clarify",
            data={
                "answer": "The Northstar final presentation.",
                "csrf_token": csrf_token,
            },
        )
        await asyncio.wait_for(service.continuation_started.wait(), timeout=1)
        duplicate_answer = await client.post(
            "/clarify",
            data={"answer": "A different answer."},
        )
        service.release.set()
        completed = await _wait_for_lifecycle(client, "verified")
        done = await client.get("/done")
        late_answer = await client.post(
            "/clarify",
            data={"answer": "A late second answer."},
        )

    assert started.status_code == 303
    assert awaiting.json()["clarification_required"] is True
    assert first_view.status_code == 200
    assert "Which presentation did you approve for delivery?" in first_view.text
    assert first_view.text.count('action="/clarify"') == 1
    assert 'name="answer"' in first_view.text
    assert "Answer and continue" in first_view.text
    assert "No file-by-file review is required." in first_view.text
    assert "no API call" in first_view.text
    assert refreshed_view.status_code == 200
    assert service.initial_calls == 1
    assert service.continuation_calls == 1
    assert invalid_answer.status_code == 422
    assert "cannot be empty" in invalid_answer.text
    assert answered.status_code == 303
    assert answered.headers["location"] == "/working"
    assert duplicate_answer.status_code == 409
    assert "Clarification is not active" in duplicate_answer.text
    assert service.token == "same-job-42"
    assert service.answer == "The Northstar final presentation."
    assert completed.json()["lifecycle"] == "verified"
    assert done.status_code == 200
    assert "2 of 2, exactly once" in done.text
    assert late_answer.status_code == 409


@pytest.mark.anyio
async def test_second_service_question_is_terminally_blocked(tmp_path: Path) -> None:
    service = _SecondQuestionService(tmp_path)
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
                "user_request": "Put the approved presentation in final deliverables.",
                "output_parent": str(tmp_path / "results"),
                "csrf_token": csrf_token,
            },
        )
        await _wait_for_lifecycle(client, "awaiting_clarification")
        csrf_token = _csrf(await client.get("/working"))
        response = await client.post(
            "/clarify",
            data={
                "answer": "The Northstar final presentation.",
                "csrf_token": csrf_token,
            },
        )
        blocked_status = await _wait_for_lifecycle(client, "blocked")
        blocked = await client.get("/working")

    assert response.status_code == 303
    assert blocked_status.json()["blocked"] is True
    assert "second_clarification_not_allowed" in blocked.text
    assert service.initial_calls == 1
    assert service.continuation_calls == 1
