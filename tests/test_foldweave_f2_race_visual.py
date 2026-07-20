"""Product-native F2 receiver review and parent/child race evidence."""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier

import httpx
import pytest
from connected_change_fixtures import tree_state
from test_foldweave_derivative_review_service import (
    _build_receiver_parent,
    _provider_for_child,
    _SurfaceProviderFactory,
)

from name_atlas.folder_app import create_folder_app
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewServiceError,
)
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_receiver_parent_and_derivative_child_race_for_one_destination(
    tmp_path: Path,
) -> None:
    """Only one exact parent/child acceptance can own a shared result path."""

    context = _build_receiver_parent(tmp_path)
    source_before = tree_state(context.parent.source_root)
    parent = context.parent
    assert parent.preview is not None
    assert parent.candidate_plan is not None

    child = context.service.create_or_resume_derivative_child(
        parent.job_path,
        output_parent=context.output_parent,
        instruction="Build Martin's derivative proposal for the same result target.",
        idempotency_key="f2-parent-child-race-create",
        provider_kind="deterministic",
        channel="native_app",
    )
    child = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=_provider_for_child(child),
    )
    assert child.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert child.preview is not None
    assert child.candidate_plan is not None
    assert child.candidate_plan.result_folder_name == (
        parent.candidate_plan.result_folder_name
    )
    assert tuple(context.output_parent.iterdir()) == ()

    contenders = (parent, child)
    barrier = Barrier(len(contenders))

    def accept(
        contender: FolderRefactorJobV3,
        *,
        synchronize: bool = True,
    ) -> FolderRefactorJobV3:
        assert contender.preview is not None
        assert contender.candidate_plan is not None
        if synchronize:
            barrier.wait(timeout=5)
        return context.service.accept(
            contender.job_path,
            expected_revision=contender.revision,
            preview_fingerprint=contender.preview.preview_fingerprint,
            candidate_fingerprint=(contender.preview.compiled_candidate_fingerprint),
            output_parent=context.output_parent,
            result_folder_name=contender.candidate_plan.result_folder_name,
            idempotency_key=f"f2-parent-child-race-accept-{contender.job_id}",
            channel="native_app",
        )

    successes: list[FolderRefactorJobV3] = []
    failures: list[tuple[FolderRefactorJobV3, FoldweaveReviewServiceError]] = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(accept, contender): contender for contender in contenders
        }
        for future, contender in futures.items():
            try:
                successes.append(future.result(timeout=30))
            except FoldweaveReviewServiceError as exc:
                failures.append((contender, exc))

    assert len(successes) == 1
    assert successes[0].lifecycle is FolderJobLifecycleV3.VERIFIED
    assert len(failures) == 1
    loser, failure = failures[0]
    assert failure.code == "destination_already_reserved"

    winner = successes[0]
    winner_request = next(
        contender for contender in contenders if contender.job_id == winner.job_id
    )
    assert winner.final_result_path is not None
    assert tuple(context.output_parent.iterdir()) == (winner.final_result_path,)
    assert all("pending" not in item.name for item in context.output_parent.iterdir())
    assert tree_state(context.parent.source_root) == source_before

    winner_bytes = winner.job_path.read_bytes()
    winner_result = tree_state(winner.final_result_path)
    exact_winner_retry = accept(winner_request, synchronize=False)
    assert exact_winner_retry == winner
    assert winner.job_path.read_bytes() == winner_bytes
    assert tree_state(winner.final_result_path) == winner_result

    loser_before_retry = loser.job_path.read_bytes()
    with pytest.raises(FoldweaveReviewServiceError) as repeated:
        accept(loser, synchronize=False)
    assert repeated.value.code == "destination_already_reserved"
    assert loser.job_path.read_bytes() == loser_before_retry
    durable_loser = context.service.status(loser.job_path)
    assert durable_loser.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert durable_loser.destination_reservation is None
    assert durable_loser.execution_authorization is None
    assert tree_state(context.parent.source_root) == source_before
    assert tuple(context.output_parent.iterdir()) == (winner.final_result_path,)


@pytest.mark.anyio
async def test_native_receiver_review_shows_t1_then_t2_delta_before_acceptance(
    tmp_path: Path,
) -> None:
    """Martin's loopback review moves from deterministic T1 to reviewed T2."""

    context = _build_receiver_parent(tmp_path)
    parent = context.parent
    source_before = tree_state(parent.source_root)
    parent_bytes = parent.job_path.read_bytes()
    factory = _SurfaceProviderFactory(context.service)
    browser = FoldweaveBrowserReviewService(
        job_path=parent.job_path,
        service=context.service,
        provider_factory=factory,
        review_channel="native_app",
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=create_folder_app(browser)),
        base_url="http://testserver",
    ) as client:
        review_page = await client.get("/review")
        assert review_page.status_code == 200
        assert 'data-journey="apply"' in review_page.text
        assert "Nothing has been copied yet" in review_page.text
        csrf_match = re.search(r'data-csrf-token="([^"]+)"', review_page.text)
        assert csrf_match is not None
        csrf = csrf_match.group(1)

        parent_status_response = await client.get(f"/api/jobs/{parent.job_id}/status")
        parent_preview_response = await client.get(f"/api/jobs/{parent.job_id}/preview")
        assert parent_status_response.status_code == 200
        assert parent_preview_response.status_code == 200
        parent_status = parent_status_response.json()
        parent_preview = parent_preview_response.json()

        assert parent_preview["proposal_basis"] == "imported_change_file"
        assert parent_preview["imported_change_file_fingerprint"] is not None
        assert parent_preview["match_report_fingerprint"] is not None
        assert parent_preview["immediate_parent_candidate_fingerprint"] is None
        assert factory.calls == 0
        assert not (tmp_path / ".name-atlas" / "api_budget.json").exists()

        current_paths = {
            item["relative_path"] for item in parent_preview["current_tree_members"]
        }
        proposed_paths = {
            item["relative_path"] for item in parent_preview["proposed_tree_members"]
        }
        actual_martin_paths = {
            path.relative_to(parent.source_root).as_posix()
            for path in parent.source_root.rglob("*")
            if path.is_file() or (path.is_dir() and not any(path.iterdir()))
        }
        assert current_paths == actual_martin_paths
        assert current_paths != proposed_paths
        assert tuple(context.output_parent.iterdir()) == ()
        assert tree_state(parent.source_root) == source_before

        revised = await client.post(
            f"/api/jobs/{parent.job_id}/revision",
            headers={"x-foldweave-csrf": csrf},
            json={
                "candidate_fingerprint": parent_status["candidate_fingerprint"],
                "expected_revision": parent_status["job_revision"],
                "idempotency_key": "f2-native-receiver-t2-revision",
                "instruction": "Build Martin's reviewed T2 proposal.",
                "preview_fingerprint": parent_status["preview_fingerprint"],
            },
        )
        assert revised.status_code == 200
        t2_status = revised.json()
        assert t2_status["job_id"] != parent.job_id
        assert t2_status["proposal_revision"] == 1
        assert factory.calls == 1
        assert parent.job_path.read_bytes() == parent_bytes

        t2_preview_response = await client.get(
            f"/api/jobs/{t2_status['job_id']}/preview"
        )
        assert t2_preview_response.status_code == 200
        t2_preview = t2_preview_response.json()
        assert t2_preview["proposal_basis"] == "gpt_derivative"
        assert (
            t2_preview["immediate_parent_candidate_fingerprint"]
            == (parent_preview["compiled_candidate_fingerprint"])
        )
        assert (
            t2_preview["current_tree_members"]
            == (parent_preview["current_tree_members"])
        )

        t1_by_id = {
            item["member_id"]: item["proposed_relative_path"]
            for item in parent_preview["member_changes"]
        }
        t2_by_id = {
            item["member_id"]: item["proposed_relative_path"]
            for item in t2_preview["member_changes"]
        }
        proposal_delta = {
            member_id: (t1_by_id[member_id], t2_path)
            for member_id, t2_path in t2_by_id.items()
            if t1_by_id[member_id] != t2_path
        }
        assert len(proposal_delta) == 1
        previous_path, t2_path = next(iter(proposal_delta.values()))
        assert previous_path in proposed_paths
        assert t2_path.startswith("collaborative-review/")
        assert tuple(context.output_parent.iterdir()) == ()
        assert tree_state(parent.source_root) == source_before

        accepted = await client.post(
            f"/api/jobs/{t2_status['job_id']}/accept",
            headers={"x-foldweave-csrf": csrf},
            json={
                "candidate_fingerprint": t2_status["candidate_fingerprint"],
                "expected_revision": t2_status["job_revision"],
                "idempotency_key": "f2-native-receiver-t2-accept",
                "output_parent": t2_status["output_parent"],
                "preview_fingerprint": t2_status["preview_fingerprint"],
                "result_folder_name": t2_status["result_folder_name"],
            },
        )
        assert accepted.status_code == 200
        assert accepted.json() == {"lifecycle": "verified", "done_url": "/done"}
        done = await client.get("/done")
        assert done.status_code == 200
        assert "Your new folder is ready" in done.text

    child = context.service.status(browser.job_path)
    assert child.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert child.final_result_path is not None
    assert child.final_result_path.parent == context.output_parent
    assert parent.job_path.read_bytes() == parent_bytes
    assert tree_state(parent.source_root) == source_before
    assert tuple(context.output_parent.iterdir()) == (child.final_result_path,)
    assert factory.calls == 1
    assert not (tmp_path / ".name-atlas" / "api_budget.json").exists()
