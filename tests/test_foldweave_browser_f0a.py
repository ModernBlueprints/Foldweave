"""Browser-level F0a evidence for Foldweave review-before-execution."""

from __future__ import annotations

import asyncio
import re
import time
from collections.abc import Mapping
from pathlib import Path

import httpx
import pytest
from connected_change_fixtures import make_connected_change_fixture, tree_state

from name_atlas.folder_app import create_folder_app
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_PATH,
)
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService


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


def _target_map_factory(
    result_name: str,
    target_paths: Mapping[str, str],
):
    def make_target_map(
        _source_root: Path,
        _request: str,
    ) -> tuple[str, Mapping[str, str]]:
        return result_name, target_paths

    return make_target_map


@pytest.mark.anyio
async def test_working_page_redirects_when_review_becomes_ready(
    tmp_path: Path,
) -> None:
    """The real polling page must route the browser into immutable review."""

    source_root = tmp_path / "source"
    output_parent = tmp_path / "output"
    source_root.mkdir()
    output_parent.mkdir()
    (source_root / "brief.md").write_text("# Brief\n", encoding="utf-8")

    def slow_target_map(
        _source_root: Path,
        _request: str,
    ) -> tuple[str, Mapping[str, str]]:
        time.sleep(0.2)
        return "organized-copy", {"brief.md": "Delivery/brief.md"}

    service = FoldweaveBrowserReviewService(
        job_path=tmp_path / "jobs" / "working.json",
        target_map_factory=slow_target_map,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(service)),
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        started = await client.post(
            "/start",
            data={
                "source_root": str(source_root),
                "user_request": "Move the brief into Delivery.",
                "output_parent": str(output_parent),
                "evidence_disclosure_acknowledged": "true",
                "csrf_token": _csrf(start),
            },
        )
        working = await client.get("/working")

        assert started.status_code == 303
        assert working.status_code == 200
        assert 'status.lifecycle === "reviewing"' in working.text
        assert 'window.location.assign("/review")' in working.text
        await _wait_for_lifecycle(client, "reviewing")
        assert tuple(output_parent.iterdir()) == ()


def _acceptance_payload(
    service: FoldweaveBrowserReviewService,
    *,
    idempotency_key: str,
) -> tuple[str, dict[str, object]]:
    checkpoint = service.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle.value == "reviewing"
    assert checkpoint.review is not None
    review = checkpoint.review
    return review.job_id, {
        "candidate_fingerprint": review.candidate_fingerprint,
        "expected_revision": review.job_revision,
        "idempotency_key": idempotency_key,
        "output_parent": str(review.output_parent),
        "preview_fingerprint": review.preview_fingerprint,
        "result_folder_name": review.result_folder_name,
    }


@pytest.mark.anyio
async def test_f0a_browser_origin_receiver_review_restart_accept_and_receipts(
    tmp_path: Path,
) -> None:
    """Both browser forms review exact trees before creating verified copies."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    sofia_before = tree_state(fixture.sofia_root)
    martin_before = tree_state(fixture.martin_root)
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin_job = tmp_path / "jobs" / "origin.json"
    receiver_job = tmp_path / "jobs" / "receiver.json"
    target_map_factory = _target_map_factory(
        fixture.result_name,
        fixture.target_paths,
    )
    origin_service = FoldweaveBrowserReviewService(
        job_path=origin_job,
        target_map_factory=target_map_factory,
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(origin_service)),
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        csrf_token = _csrf(start)
        started = await client.post(
            "/start",
            data={
                "source_root": str(fixture.sofia_root),
                "user_request": fixture.request,
                "output_parent": str(origin_output),
                "evidence_disclosure_acknowledged": "true",
                "csrf_token": csrf_token,
            },
        )
        status = await _wait_for_lifecycle(client, "reviewing")
        origin_job_id, origin_acceptance = _acceptance_payload(
            origin_service,
            idempotency_key="browser-accept-origin",
        )
        review = await client.get("/review")
        preview = await client.get(f"/api/jobs/{origin_job_id}/preview")

        assert started.status_code == 303
        assert started.headers["location"] == "/working"
        assert status["journey"] == "organize"
        assert status["review_url"] == "/review"
        assert review.status_code == 200
        assert 'id="foldweave-review-root"' in review.text
        assert "Nothing has been copied yet" in review.text
        assert preview.status_code == 200
        assert preview.headers["cache-control"] == "no-store"
        origin_preview = preview.json()
        assert origin_preview["schema_version"] == "folder-plan-preview.v1"
        assert origin_preview["proposal_basis"] == "fresh_gpt_plan"
        assert origin_preview["job_id"] == origin_job_id
        assert (
            origin_preview["expected_job_revision"]
            == (origin_acceptance["expected_revision"])
        )
        assert len(origin_preview["current_tree_members"]) == 7
        assert len(origin_preview["proposed_tree_members"]) == 7
        assert origin_preview["counts"]["file_count"] == 6
        assert origin_preview["counts"]["empty_directory_count"] == 1
        assert origin_preview["counts"]["link_count"] == 2
        assert tuple(origin_output.iterdir()) == ()
        assert tree_state(fixture.sofia_root) == sofia_before

    reviewing_job_bytes = origin_job.read_bytes()
    restarted_origin_service = FoldweaveBrowserReviewService(
        job_path=origin_job,
        target_map_factory=target_map_factory,
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(restarted_origin_service)),
        base_url="http://testserver",
    ) as restarted_client:
        restarted_root = await restarted_client.get("/", follow_redirects=False)
        restarted_review = await restarted_client.get("/review")
        restarted_preview = await restarted_client.get(
            f"/api/jobs/{origin_job_id}/preview"
        )
        restart_csrf_match = re.search(
            r'data-csrf-token="([^"]+)"',
            restarted_review.text,
        )
        assert restart_csrf_match is not None
        restarted_csrf = restart_csrf_match.group(1)

        assert restarted_root.status_code == 303
        assert restarted_root.headers["location"] == "/review"
        assert restarted_review.status_code == 200
        assert restarted_preview.json() == origin_preview
        assert origin_job.read_bytes() == reviewing_job_bytes
        assert tuple(origin_output.iterdir()) == ()

        accepted = await restarted_client.post(
            f"/api/jobs/{origin_job_id}/accept",
            headers={"x-foldweave-csrf": restarted_csrf},
            json=origin_acceptance,
        )
        done = await restarted_client.get("/done")

        assert accepted.status_code == 200
        assert accepted.json() == {"lifecycle": "verified", "done_url": "/done"}
        assert done.status_code == 200
        assert "Your new folder is ready" in done.text
        assert "Original folder</dt><dd>Unchanged" in done.text

        origin_checkpoint = restarted_origin_service.web_checkpoint()
        assert origin_checkpoint is not None
        assert origin_checkpoint.result is not None
        origin_result = origin_checkpoint.result
        origin_result_before_retry = tree_state(origin_result.result_root)
        origin_job_before_retry = origin_job.read_bytes()
        duplicate = await restarted_client.post(
            f"/api/jobs/{origin_job_id}/accept",
            headers={"x-foldweave-csrf": restarted_csrf},
            json=origin_acceptance,
        )

        assert duplicate.status_code == 409
        assert duplicate.json()["error"] == "review_not_current"
        assert origin_job.read_bytes() == origin_job_before_retry
        assert tree_state(origin_result.result_root) == origin_result_before_retry
        assert tuple(origin_output.iterdir()) == (origin_result.result_root,)

    change_file_path = origin_result.result_root / CONNECTED_CHANGE_PATH
    assert change_file_path.is_file()
    assert tree_state(fixture.sofia_root) == sofia_before

    receiver_service = FoldweaveBrowserReviewService(job_path=receiver_job)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(receiver_service)),
        base_url="http://testserver",
    ) as receiver_client:
        apply_page = await receiver_client.get("/apply")
        receiver_csrf = _csrf(apply_page)
        applied = await receiver_client.post(
            "/apply",
            data={
                "change_file": str(change_file_path),
                "source_root": str(fixture.martin_root),
                "output_parent": str(receiver_output),
                "csrf_token": receiver_csrf,
            },
        )
        receiver_status = await _wait_for_lifecycle(receiver_client, "reviewing")
        receiver_job_id, receiver_acceptance = _acceptance_payload(
            receiver_service,
            idempotency_key="browser-accept-receiver",
        )
        receiver_review = await receiver_client.get("/review")
        receiver_preview_response = await receiver_client.get(
            f"/api/jobs/{receiver_job_id}/preview"
        )

        assert applied.status_code == 303
        assert applied.headers["location"] == "/working"
        assert receiver_status["journey"] == "apply"
        assert receiver_status["review_url"] == "/review"
        assert receiver_review.status_code == 200
        assert "Nothing has been copied yet" in receiver_review.text
        receiver_preview = receiver_preview_response.json()
        assert receiver_preview["proposal_basis"] == "imported_change_file"
        assert receiver_preview["imported_change_file_fingerprint"] is not None
        assert receiver_preview["match_report_fingerprint"] is not None
        assert {
            item["relative_path"]
            for item in receiver_preview["current_tree_members"]
            if item["member_kind"] == "regular_file"
        } == {
            candidate.relative_to(fixture.martin_root).as_posix()
            for candidate in fixture.martin_root.rglob("*")
            if candidate.is_file()
        }
        assert {
            item["relative_path"]
            for item in receiver_preview["proposed_tree_members"]
            if item["member_kind"] == "regular_file"
        } == set(fixture.target_paths.values())
        assert tuple(receiver_output.iterdir()) == ()
        assert tree_state(fixture.martin_root) == martin_before

        receiver_accepted = await receiver_client.post(
            f"/api/jobs/{receiver_job_id}/accept",
            headers={"x-foldweave-csrf": receiver_csrf},
            json=receiver_acceptance,
        )
        receiver_done = await receiver_client.get("/done")

        assert receiver_accepted.status_code == 200
        assert receiver_accepted.json()["lifecycle"] == "verified"
        assert receiver_done.status_code == 200
        assert "Your new folder is ready" in receiver_done.text
        receiver_checkpoint = receiver_service.web_checkpoint()
        assert receiver_checkpoint is not None
        assert receiver_checkpoint.result is not None
        receiver_result = receiver_checkpoint.result

    assert tree_state(fixture.martin_root) == martin_before
    assert origin_result.organized_tree_commitment == (
        receiver_result.organized_tree_commitment
    )
    assert receiver_result.receipt_fingerprint is not None
    assert origin_result.receipt_fingerprint is not None
    assert receiver_result.originating_receipt_fingerprint == (
        origin_result.receipt_fingerprint
    )
    assert receiver_result.receipt_fingerprint != (
        receiver_result.originating_receipt_fingerprint
    )


@pytest.mark.anyio
async def test_f0a_browser_changed_source_acceptance_becomes_durable_blocker(
    tmp_path: Path,
) -> None:
    """A source change after review is terminally projected, not re-reviewable."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveBrowserReviewService(
        job_path=tmp_path / "jobs" / "source-stale.json",
        target_map_factory=_target_map_factory(
            fixture.result_name,
            fixture.target_paths,
        ),
    )
    app = create_folder_app(service)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        csrf_token = _csrf(start)
        await client.post(
            "/start",
            data={
                "source_root": str(fixture.sofia_root),
                "user_request": fixture.request,
                "output_parent": str(output),
                "evidence_disclosure_acknowledged": "true",
                "csrf_token": csrf_token,
            },
        )
        await _wait_for_lifecycle(client, "reviewing")
        job_id, acceptance = _acceptance_payload(
            service,
            idempotency_key="browser-source-stale",
        )
        changed_file = fixture.sofia_root / "media" / "cover.png"
        changed_file.write_bytes(changed_file.read_bytes() + b"changed after review")

        refused = await client.post(
            f"/api/jobs/{job_id}/accept",
            headers={"x-foldweave-csrf": csrf_token},
            json=acceptance,
        )
        status = await client.get("/status")
        root = await client.get("/", follow_redirects=False)
        working = await client.get("/working")

    assert refused.status_code == 409
    assert refused.json()["error"] == "acceptance_blocked"
    assert status.json()["lifecycle"] == "blocked"
    assert status.json()["blocked"] is True
    assert root.status_code == 303
    assert root.headers["location"] == "/working"
    assert working.status_code == 200
    assert "selected source differs from the immutable review snapshot" in (
        working.text.casefold()
    )
    assert tuple(output.iterdir()) == ()
    checkpoint = service.web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle.value == "blocked"
    assert checkpoint.review is None
    assert checkpoint.blocker is not None


@pytest.mark.anyio
async def test_f0a_browser_rejects_nonvisible_acceptance_without_output(
    tmp_path: Path,
) -> None:
    """The API refuses a stale fingerprint while keeping the valid review intact."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveBrowserReviewService(
        job_path=tmp_path / "jobs" / "mismatched-preview.json",
        target_map_factory=_target_map_factory(
            fixture.result_name,
            fixture.target_paths,
        ),
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(service)),
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        csrf_token = _csrf(start)
        await client.post(
            "/start",
            data={
                "source_root": str(fixture.sofia_root),
                "user_request": fixture.request,
                "output_parent": str(output),
                "evidence_disclosure_acknowledged": "true",
                "csrf_token": csrf_token,
            },
        )
        await _wait_for_lifecycle(client, "reviewing")
        job_id, acceptance = _acceptance_payload(
            service,
            idempotency_key="browser-mismatched-preview",
        )
        acceptance["preview_fingerprint"] = "0" * 64
        refused = await client.post(
            f"/api/jobs/{job_id}/accept",
            headers={"x-foldweave-csrf": csrf_token},
            json=acceptance,
        )
        status = await client.get("/status")
        review = await client.get("/review")

    assert refused.status_code == 422
    assert refused.json()["error"] == "acceptance_invalid"
    assert status.json()["lifecycle"] == "reviewing"
    assert review.status_code == 200
    assert tuple(output.iterdir()) == ()
