"""F0b loopback evidence for live-provider review, revision, and exact retries."""

from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Literal

import httpx
import pytest
from connected_change_fixtures import make_connected_change_fixture, tree_state

from name_atlas.folder_app import create_folder_app
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3Store,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
)
from name_atlas.folder_refactor.planner_provider import (
    DETERMINISTIC_DEVELOPMENT_REQUEST,
    DeterministicDevelopmentPlannerProvider,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _ScriptedRevisionProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self, revision: FolderPlanRevisionV1) -> None:
        self._revision = revision
        self.inputs: list[FolderPlannerRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.inputs.append(turn_input)
        return FolderRevisionProviderResponseV1(
            provider_kind="deterministic",
            call_id=f"browser-revision-{len(self.inputs)}",
            revision=self._revision,
        )


class _ProviderFactory:
    def __init__(self, job_path: Path) -> None:
        self._job_path = job_path
        self.initial_count = 0
        self.revision_count = 0
        self.revision_providers: list[_ScriptedRevisionProvider] = []

    def initial_provider(self) -> DeterministicDevelopmentPlannerProvider:
        self.initial_count += 1
        return DeterministicDevelopmentPlannerProvider()

    def revision_provider(self) -> _ScriptedRevisionProvider:
        self.revision_count += 1
        job = FolderRefactorJobV3Store(self._job_path).inspect()
        assert job.candidate_plan is not None
        assert job.preview is not None
        selected = next(
            mapping
            for mapping in job.candidate_plan.file_mappings
            if not mapping.protected
        )
        provider = _ScriptedRevisionProvider(
            FolderPlanRevisionV1(
                base_candidate_fingerprint=(job.preview.compiled_candidate_fingerprint),
                entries=(
                    FolderPlanRevisionEntryV1(
                        file_id=selected.file_id,
                        replacement_target_path=(
                            f"reviewed/{Path(selected.target_path).name}"
                        ),
                        rationale="Place this member in the reviewed section.",
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            )
        )
        self.revision_providers.append(provider)
        return provider


def _csrf(response: httpx.Response) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    return match.group(1)


def _review_csrf(response: httpx.Response) -> str:
    match = re.search(r'data-csrf-token="([^"]+)"', response.text)
    assert match is not None
    return match.group(1)


async def _wait_for_review(client: httpx.AsyncClient) -> dict[str, object]:
    for _ in range(500):
        response = await client.get("/status")
        payload = response.json()
        if payload["lifecycle"] == "reviewing":
            return payload
        if payload["lifecycle"] == "blocked":
            raise AssertionError(f"Foldweave browser job blocked: {payload}")
        await asyncio.sleep(0.01)
    raise AssertionError("Foldweave browser job did not reach review.")


@pytest.mark.anyio
async def test_f0b_browser_revision_and_accept_retries_are_exactly_idempotent(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "browser-f0b.json"
    source_before = tree_state(fixture.sofia_root)
    factory = _ProviderFactory(job_path)
    service = FoldweaveBrowserReviewService(
        job_path=job_path,
        provider_factory=factory,
        review_channel="native_app",
    )
    app = create_folder_app(service)

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as client:
        start = await client.get("/start")
        started = await client.post(
            "/start",
            data={
                "source_root": str(fixture.sofia_root),
                "user_request": DETERMINISTIC_DEVELOPMENT_REQUEST,
                "output_parent": str(output),
                "evidence_disclosure_acknowledged": "true",
                "csrf_token": _csrf(start),
            },
        )
        assert started.status_code == 303
        await _wait_for_review(client)
        review_page = await client.get("/review")
        csrf = _review_csrf(review_page)
        checkpoint = service.web_checkpoint()
        assert checkpoint is not None
        assert checkpoint.review is not None
        job_id = checkpoint.review.job_id
        review_status = (await client.get(f"/api/jobs/{job_id}/status")).json()
        revision_payload = {
            "candidate_fingerprint": review_status["candidate_fingerprint"],
            "expected_revision": review_status["job_revision"],
            "idempotency_key": "browser-f0b-revision-key",
            "instruction": "Place the selected member in a reviewed section.",
            "preview_fingerprint": review_status["preview_fingerprint"],
        }

        revised = await client.post(
            f"/api/jobs/{job_id}/revision",
            headers={"x-foldweave-csrf": csrf},
            json=revision_payload,
        )
        assert revised.status_code == 200
        revised_status = revised.json()
        assert revised_status["proposal_revision"] == 1
        assert tuple(output.iterdir()) == ()
        assert factory.revision_count == 1

        repeated_revision = await client.post(
            f"/api/jobs/{job_id}/revision",
            headers={"x-foldweave-csrf": csrf},
            json=revision_payload,
        )
        assert repeated_revision.status_code == 200
        assert repeated_revision.json() == revised_status
        assert factory.revision_count == 1

        acceptance = {
            "candidate_fingerprint": revised_status["candidate_fingerprint"],
            "expected_revision": revised_status["job_revision"],
            "idempotency_key": "browser-f0b-accept-key",
            "output_parent": revised_status["output_parent"],
            "preview_fingerprint": revised_status["preview_fingerprint"],
            "result_folder_name": revised_status["result_folder_name"],
        }
        accepted = await client.post(
            f"/api/jobs/{job_id}/accept",
            headers={"x-foldweave-csrf": csrf},
            json=acceptance,
        )
        assert accepted.status_code == 200
        assert accepted.json() == {"lifecycle": "verified", "done_url": "/done"}
        job = FolderRefactorJobV3Store(job_path).inspect()
        assert job.lifecycle is FolderJobLifecycleV3.VERIFIED
        assert job.execution_authorization is not None
        assert job.execution_authorization.channel == "native_app"
        assert job.final_result_path is not None
        result_before_retry = tree_state(job.final_result_path)
        job_before_retry = job_path.read_bytes()

        repeated_acceptance = await client.post(
            f"/api/jobs/{job_id}/accept",
            headers={"x-foldweave-csrf": csrf},
            json=acceptance,
        )
        assert repeated_acceptance.status_code == 200
        assert repeated_acceptance.json() == accepted.json()
        assert job_path.read_bytes() == job_before_retry
        assert tree_state(job.final_result_path) == result_before_retry

    assert factory.initial_count == 1
    assert factory.revision_count == 1
    assert len(factory.revision_providers) == 1
    assert len(factory.revision_providers[0].inputs) == 1
    assert tree_state(fixture.sofia_root) == source_before
    assert tuple(output.iterdir()) == (job.final_result_path,)
