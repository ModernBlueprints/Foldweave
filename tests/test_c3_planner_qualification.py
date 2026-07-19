"""Pre-provider C3 qualification on the final hero and ambiguity fixtures."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any, Literal

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
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV2,
)
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.demo_fixtures import (
    AMBIGUITY_ANSWER,
    AMBIGUITY_REQUEST,
    HERO_REQUEST,
    ambiguity_target_paths,
    hero_target_paths,
    materialize_ambiguity_fixture,
    materialize_hero_fixture,
)
from name_atlas.folder_refactor.live_planner_provider import (
    LiveFolderPlannerProvider,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    PlannerInventoryFile,
)
from name_atlas.folder_refactor.planner_recording import (
    RecordedPlannerProvider,
    build_folder_planner_replay,
)
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    parse_portable_model,
    read_regular_bytes,
)
from name_atlas.folder_refactor.serialization import canonical_json_bytes


class _FixtureResponses:
    """Produce exact fake Responses calls from the persisted turn state."""

    def __init__(self, fixture_kind: Literal["hero", "ambiguity"]) -> None:
        self.fixture_kind = fixture_kind
        self.calls = 0

    async def create(self, **kwargs: Any) -> object:
        self.calls += 1
        turn = _turn_from_request(kwargs)
        if turn.response_turn == 1:
            output = _evidence_calls(turn)
        elif self.fixture_kind == "ambiguity" and turn.response_turn == 2:
            output = [_clarification_call(turn)]
        else:
            output = [_submit_call(turn, fixture_kind=self.fixture_kind)]
        return SimpleNamespace(
            id=f"unpersisted-provider-id-{self.calls}",
            model="gpt-5.6-sol-2026-07-01",
            status="completed",
            error=None,
            usage=SimpleNamespace(
                input_tokens=500 + self.calls,
                output_tokens=100,
                total_tokens=600 + self.calls,
                input_tokens_details=SimpleNamespace(cached_tokens=0),
                output_tokens_details=SimpleNamespace(reasoning_tokens=25),
            ),
            output=output,
        )


def _turn_from_request(kwargs: dict[str, Any]) -> FolderPlannerTurnInput:
    assert kwargs["model"] == "gpt-5.6"
    assert kwargs["store"] is False
    text = kwargs["input"][0]["content"][0]["text"]
    return FolderPlannerTurnInput.model_validate_json(text, strict=True)


def _initial_files(turn: FolderPlannerTurnInput) -> tuple[PlannerInventoryFile, ...]:
    initial = turn.evidence_ledger.initial_evidence
    assert isinstance(initial, dict)
    files = initial["files"]
    assert isinstance(files, list)
    return tuple(PlannerInventoryFile.model_validate(item) for item in files)


def _function_call(
    *,
    name: str,
    call_id: str,
    arguments: dict[str, Any],
) -> SimpleNamespace:
    return SimpleNamespace(
        type="function_call",
        name=name,
        call_id=call_id,
        arguments=canonical_json_bytes(arguments).decode("utf-8"),
        status="completed",
    )


def _evidence_calls(turn: FolderPlannerTurnInput) -> list[SimpleNamespace]:
    calls: list[SimpleNamespace] = []
    for file in _initial_files(turn):
        if file.protected or not file.relative_path.casefold().endswith(".md"):
            continue
        calls.append(
            _function_call(
                name="read_text_excerpt",
                call_id=f"read-{len(calls) + 1}",
                arguments={
                    "file_id": file.file_id,
                    "start_byte": 0,
                    "max_bytes": 4_096,
                },
            )
        )
        calls.append(
            _function_call(
                name="inspect_markdown_links",
                call_id=f"links-{len(calls) + 1}",
                arguments={
                    "file_id": file.file_id,
                    "cursor": None,
                    "page_size": 50,
                },
            )
        )
    assert calls
    return calls


def _clarification_call(turn: FolderPlannerTurnInput) -> SimpleNamespace:
    evidence_ids = [item.fingerprint for item in turn.evidence_ledger.records]
    return _function_call(
        name="request_clarification",
        call_id="ask-approved-candidate",
        arguments={
            "reason": "missing_user_intent",
            "question": "Which presentation candidate did the client approve?",
            "missing_facts": ["approved_presentation_candidate"],
            "evidence_ids": evidence_ids,
        },
    )


def _submit_call(
    turn: FolderPlannerTurnInput,
    *,
    fixture_kind: Literal["hero", "ambiguity"],
) -> SimpleNamespace:
    if fixture_kind == "ambiguity":
        assert turn.clarification_answer == AMBIGUITY_ANSWER
        targets = ambiguity_target_paths()
        result_name = "northstar-presentations"
    else:
        targets = hero_target_paths()
        result_name = "northstar"
    evidence_ids = tuple(item.fingerprint for item in turn.evidence_ledger.records) or (
        "initial_inventory",
    )
    plan = FolderPlan(
        source_commitment=turn.source_commitment,
        request_fingerprint=turn.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=turn.evidence_ledger.evidence_fingerprint,
        result_folder_name=result_name,
        entries=tuple(
            FolderPlanEntry(
                file_id=file.file_id,
                original_path=file.relative_path,
                proposed_target=targets[file.relative_path],
                rationale="Use the bounded project evidence and exact user request.",
                evidence_ids=evidence_ids,
            )
            for file in _initial_files(turn)
            if not file.protected
        ),
        exclusions=(),
    )
    return _function_call(
        name="submit_plan",
        call_id="submit-final-plan",
        arguments={"plan": plan.model_dump(mode="json")},
    )


def _provider(
    responses: _FixtureResponses,
    *,
    existing_usage=(),
) -> LiveFolderPlannerProvider:
    return LiveFolderPlannerProvider(
        SimpleNamespace(responses=responses),
        budget=PersistentBudgetLedger(
            path=None,
            live_call_cap=13,
            cost_cap_usd=10,
        ),
        existing_usage=existing_usage,
    )


def _tree(root: Path) -> dict[str, bytes | None]:
    result: dict[str, bytes | None] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        result[relative] = path.read_bytes() if path.is_file() else None
    return result


def _organized_commitment(job) -> str:
    assert job.final_result_path is not None
    receipt = parse_portable_model(
        read_regular_bytes(job.final_result_path, CHANGE_RECEIPT_PATH),
        FolderReceiptEnvelopeV2,
    )
    return receipt.receipt.organized_tree.commitment


@pytest.mark.anyio
async def test_final_hero_qualifies_live_origin_receiver_and_reconstruction(
    tmp_path: Path,
) -> None:
    fixture = materialize_hero_fixture(tmp_path / "hero")
    sofia_before = _tree(fixture.sofia_root)
    martin_before = _tree(fixture.martin_root)
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    responses = _FixtureResponses("hero")
    origin = await ConnectedOriginPlanningService().start(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=tmp_path / "jobs" / "hero-origin.json",
        request=HERO_REQUEST,
        idempotency_key="qualify-final-hero-origin",
        provider=_provider(responses),
    )

    assert origin.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert responses.calls == 2
    assert isinstance(origin.authority, GptPlannedJobAuthorityV2)
    assert tuple(
        item.response_turn for item in origin.authority.planner_checkpoint.usage
    ) == (1, 2)
    change_path, _change_id, _origin_receipt = (
        ConnectedChangeJobService().get_change_file(origin.job_path)
    )
    receiver = ConnectedChangeJobService().start_application(
        change_file_path=change_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=tmp_path / "jobs" / "hero-receiver.json",
        idempotency_key="qualify-final-hero-receiver",
    )
    assert receiver.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert _organized_commitment(origin) == _organized_commitment(receiver)
    restored = ConnectedChangeJobService().recreate_original(
        receiver.job_path,
        tmp_path / "martin-recreated",
    )
    assert all(check.passed for check in restored.checks)
    assert _tree(restored.destination) == martin_before
    assert _tree(fixture.sofia_root) == sofia_before
    assert _tree(fixture.martin_root) == martin_before


@pytest.mark.anyio
async def test_final_ambiguity_qualifies_one_restart_safe_question(
    tmp_path: Path,
) -> None:
    fixture = materialize_ambiguity_fixture(tmp_path / "ambiguity")
    output = tmp_path / "ambiguity-output"
    output.mkdir()
    responses = _FixtureResponses("ambiguity")
    service = ConnectedOriginPlanningService()
    waiting = await service.start(
        source_root=fixture.source_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "ambiguity.json",
        request=AMBIGUITY_REQUEST,
        idempotency_key="qualify-final-ambiguity",
        provider=_provider(responses),
    )

    assert waiting.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION
    assert responses.calls == 2
    assert isinstance(waiting.authority, GptPlannedJobAuthorityV2)
    checkpoint = waiting.authority.planner_checkpoint
    assert checkpoint.clarification_question == (
        "Which presentation candidate did the client approve?"
    )
    assert tuple(item.response_turn for item in checkpoint.usage) == (1, 2)
    resumed_provider = _provider(responses, existing_usage=checkpoint.usage)
    verified = await service.answer(
        waiting.job_path,
        continuation_token=waiting.job_id,
        answer=AMBIGUITY_ANSWER,
        provider=resumed_provider,
    )

    assert verified.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert responses.calls == 3
    assert isinstance(verified.authority, GptPlannedJobAuthorityV2)
    final_checkpoint = verified.authority.planner_checkpoint
    assert final_checkpoint.clarification_question == checkpoint.clarification_question
    assert final_checkpoint.clarification_answer == AMBIGUITY_ANSWER
    assert tuple(item.response_turn for item in final_checkpoint.usage) == (1, 2, 3)
    clarification_calls = sum(
        call["tool_name"] == "request_clarification"
        for turn in final_checkpoint.observable_transcript
        for call in turn["tool_calls"]
    )
    assert clarification_calls == 1

    evidence = verified.authority.evidence_ledger
    assert evidence is not None
    assert verified.accepted_plan is not None
    _path, change_fingerprint, receipt_fingerprint = (
        ConnectedChangeJobService().get_change_file(verified.job_path)
    )
    replay = build_folder_planner_replay(
        fixture_kind="clarification",
        fixture_name="final-ambiguity-qualification",
        request=AMBIGUITY_REQUEST,
        live_evidence_ledger=evidence,
        accepted_plan=verified.accepted_plan,
        originating_receipt_fingerprint=receipt_fingerprint,
        change_file_fingerprint=change_fingerprint,
    )
    replay_bytes = canonical_json_bytes(replay)
    replay_fixture = materialize_ambiguity_fixture(tmp_path / "ambiguity-replay")
    replay_output = tmp_path / "ambiguity-replay-output"
    replay_output.mkdir()
    replay_service = ConnectedOriginPlanningService()
    replay_job = await replay_service.start(
        source_root=replay_fixture.source_root,
        output_parent=replay_output,
        job_path=tmp_path / "jobs" / "ambiguity-replay.json",
        request=AMBIGUITY_REQUEST,
        idempotency_key="qualify-final-ambiguity-replay",
        provider=RecordedPlannerProvider(replay_bytes),
    )
    assert replay_job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION
    replay_verified = await replay_service.answer(
        replay_job.job_path,
        continuation_token=replay_job.job_id,
        answer=AMBIGUITY_ANSWER,
        provider=RecordedPlannerProvider(replay_bytes),
    )
    assert replay_verified.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert isinstance(replay_verified.authority, GptPlannedJobAuthorityV2)
    replay_evidence = replay_verified.authority.evidence_ledger
    assert replay_evidence is not None
    assert replay_evidence.provider_kind == "recorded_replay"
    assert replay_evidence.usage == ()
