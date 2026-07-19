"""End-to-end live-transcript recording and keyless planner replay tests."""

from __future__ import annotations

import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from name_atlas.decision_cards.budget import PersistentBudgetLedger
from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    FolderJobLifecycleV2,
    GptPlannedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.planning import (
    ConnectedOriginPlanningService,
)
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.live_planner_provider import (
    LiveFolderPlannerProvider,
)
from name_atlas.folder_refactor.planner_contracts import PlannerInventoryFile
from name_atlas.folder_refactor.planner_recording import (
    RecordedPlannerProvider,
    build_folder_planner_replay,
    load_folder_planner_replay,
)
from name_atlas.folder_refactor.serialization import canonical_json_bytes
from name_atlas.folder_refactor.transaction import scan_folder_with_references

REQUEST = "Prepare this project for handoff. Keep every file."


class _OneResponseResource:
    def __init__(self, response: object) -> None:
        self.response = response
        self.calls = 0

    async def create(self, **kwargs: Any) -> object:
        del kwargs
        self.calls += 1
        return self.response


def _source(root: Path) -> Path:
    root.mkdir(parents=True)
    (root / "notes.md").write_bytes(b"Use the [report](report.txt#approved).\r\n")
    (root / "report.txt").write_bytes(b"Client-approved report.\n")
    (root / ".env.example").write_bytes(b"DEMO_MODE=connected\n")
    (root / "empty" / "keep").mkdir(parents=True)
    return root


def _plan(source: Path) -> FolderPlan:
    scan, _reference_graph = scan_folder_with_references(source)
    initial_files = tuple(
        PlannerInventoryFile(
            file_id=item.file_id,
            relative_path=item.relative_path,
            size=item.size,
            protected=item.protected,
            evidence_eligible=item.evidence_eligible,
        )
        for item in scan.inventory.files
    )
    targets = {
        "notes.md": "handoff/project-notes.md",
        "report.txt": "deliverables/approved-report.txt",
    }
    from name_atlas.folder_refactor.planner_evidence import (
        create_initial_evidence_ledger,
    )

    evidence = create_initial_evidence_ledger(scan.inventory, REQUEST)
    return FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=evidence.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=evidence.evidence_fingerprint,
        result_folder_name="recorded-result",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=targets[item.relative_path],
                rationale="Prepare the connected handoff layout.",
                evidence_ids=("initial_inventory",),
            )
            for item in initial_files
            if not item.protected
        ),
        exclusions=(),
    )


def _live_response(plan: FolderPlan) -> SimpleNamespace:
    arguments = canonical_json_bytes({"plan": plan.model_dump(mode="json")}).decode(
        "utf-8"
    )
    return SimpleNamespace(
        id="provider-response-id-must-not-persist",
        model="gpt-5.6-sol-2026-07-01",
        status="completed",
        error=None,
        usage=SimpleNamespace(
            input_tokens=150,
            output_tokens=80,
            total_tokens=230,
            input_tokens_details=SimpleNamespace(cached_tokens=0),
            output_tokens_details=SimpleNamespace(reasoning_tokens=20),
        ),
        output=[
            SimpleNamespace(
                type="function_call",
                name="submit_plan",
                call_id="submit-complete-plan",
                arguments=arguments,
                status="completed",
            )
        ],
    )


@pytest.mark.anyio
async def test_successful_live_result_builds_exact_keyless_replay(
    tmp_path: Path,
) -> None:
    source = _source(tmp_path / "source")
    output = tmp_path / "live-results"
    output.mkdir()
    plan = _plan(source)
    responses = _OneResponseResource(_live_response(plan))
    live_provider = LiveFolderPlannerProvider(
        SimpleNamespace(responses=responses),
        budget=PersistentBudgetLedger(
            path=None,
            live_call_cap=13,
            cost_cap_usd=10,
        ),
    )

    live_job = await ConnectedOriginPlanningService().start(
        source_root=source,
        output_parent=output,
        job_path=tmp_path / "jobs" / "live.json",
        request=REQUEST,
        idempotency_key="record-live-planner-run",
        provider=live_provider,
    )

    assert live_job.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert responses.calls == 1
    assert isinstance(live_job.authority, GptPlannedJobAuthorityV2)
    evidence = live_job.authority.evidence_ledger
    assert evidence is not None
    assert evidence.provider_kind == "live"
    assert tuple(item.response_turn for item in evidence.usage) == (1,)
    assert live_job.accepted_plan is not None
    _path, change_fingerprint, receipt_fingerprint = (
        ConnectedChangeJobService().get_change_file(live_job.job_path)
    )
    replay = build_folder_planner_replay(
        fixture_kind="hero",
        fixture_name="recording-contract-test",
        request=REQUEST,
        live_evidence_ledger=evidence,
        accepted_plan=live_job.accepted_plan,
        originating_receipt_fingerprint=receipt_fingerprint,
        change_file_fingerprint=change_fingerprint,
    )
    replay_bytes = canonical_json_bytes(replay)
    assert load_folder_planner_replay(replay_bytes) == replay
    assert b"provider-response-id-must-not-persist" not in replay_bytes

    replay_source = tmp_path / "replay-source"
    shutil.copytree(source, replay_source)
    replay_output = tmp_path / "replay-results"
    replay_output.mkdir()
    replay_provider = RecordedPlannerProvider(replay_bytes)
    replay_job = await ConnectedOriginPlanningService().start(
        source_root=replay_source,
        output_parent=replay_output,
        job_path=tmp_path / "jobs" / "replay.json",
        request=REQUEST,
        idempotency_key="replay-recorded-planner-run",
        provider=replay_provider,
    )

    assert replay_job.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert replay_provider.consumed_count == 1
    assert replay_provider.usage == ()
    assert isinstance(replay_job.authority, GptPlannedJobAuthorityV2)
    replay_evidence = replay_job.authority.evidence_ledger
    assert replay_evidence is not None
    assert replay_evidence.provider_kind == "recorded_replay"
    assert replay_evidence.usage == ()
