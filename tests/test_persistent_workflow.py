"""Integrated restart evidence for the durable Migration Case authority."""

from __future__ import annotations

import json
import shutil
from pathlib import Path, PurePosixPath

import pytest

from name_atlas.cases import CaseLifecycle, load_case
from name_atlas.decision_cards import RecordedReplayDecisionCardProvider
from name_atlas.receipts import DECISION_LEDGER_PATH
from name_atlas.receiver_verifier import (
    ReceiptVerificationStatus,
    verify_receipt,
)
from name_atlas.verification import BagItPackageValidator
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.workflow import WorkflowSession

PROJECT_ROOT = Path(__file__).parents[1]
HERO_ROOT = PROJECT_ROOT / "sample_data" / "hero"
REPLAY_RECORD = (
    PROJECT_ROOT / "src" / "name_atlas" / "recordings" / "hero_decision_card.json"
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_case_card_and_human_decisions_survive_process_restart(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    shutil.copytree(HERO_ROOT, source)
    output = tmp_path / "output"
    case_path = tmp_path / "hero.case.json"

    first = WorkflowSession(
        source_root=source,
        output_root=output,
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=case_path,
        case_name="Hero portable handoff",
    )
    meaning_family = next(
        family
        for family in first.package.families
        if family.canonical_identifier == "NA-0001"
    )
    collision_family = next(
        family
        for family in first.package.families
        if family.canonical_identifier == "CASE-010"
    )
    await first.generate_card(meaning_family.family_id)
    first.approve(meaning_family.family_id)
    first.approve_low_risk()
    first.edit(collision_family.family_id, "harbor-map-north")
    first.approve_low_risk()
    assert first.case is not None
    first_case_id = first.case.case_id
    first_revision = first.case.revision
    first_decisions = first.decisions.copy()
    first_card = first.cards[meaning_family.family_id]
    first.close()

    restarted = WorkflowSession(
        source_root=source,
        output_root=output,
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=case_path,
        case_name="Ignored on resume",
    )
    try:
        assert restarted.case is not None
        assert restarted.case.case_id == first_case_id
        assert restarted.case.revision == first_revision
        assert restarted.case.case_name == "Hero portable handoff"
        assert restarted.decisions == first_decisions
        assert restarted.cards[meaning_family.family_id] == first_card
        assert restarted.view_model()["export_ready"] is True
        assert restarted.view_model()["case_lifecycle"] == "ready_to_stage"
    finally:
        restarted.close()


@pytest.mark.anyio
async def test_r1_restart_stage_portable_verify_and_controlled_block(
    tmp_path: Path,
) -> None:
    source = tmp_path / "sender" / "source"
    source.parent.mkdir()
    shutil.copytree(HERO_ROOT, source)
    source_before = {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    }
    output = tmp_path / "sender" / "stages"
    case_path = tmp_path / "sender" / "cases" / "hero.case.json"

    first = WorkflowSession(
        source_root=source,
        output_root=output,
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=case_path,
        case_name="R1 portable handoff",
    )
    meaning_family = next(
        family
        for family in first.package.families
        if family.canonical_identifier == "NA-0001"
    )
    collision_family = next(
        family
        for family in first.package.families
        if family.canonical_identifier == "CASE-010"
    )
    await first.generate_card(meaning_family.family_id)
    first.approve(meaning_family.family_id)
    first.approve_low_risk()
    first.edit(collision_family.family_id, "harbor-map-north")
    first.approve_low_risk()
    assert first.case is not None
    case_id = first.case.case_id
    replay_card = first.cards[meaning_family.family_id]
    first.close()

    restarted = WorkflowSession(
        source_root=source,
        output_root=output,
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=case_path,
        case_name="Ignored on resume",
    )
    try:
        assert restarted.case is not None
        assert restarted.case.case_id == case_id
        assert restarted.cards[meaning_family.family_id] == replay_card
        assert restarted.cards_requested == 0
        assert restarted.replay_cards_used == 0
        result = restarted.stage()
        assert result.receipt_fingerprint is not None
        assert result.receiver_verification is not None
        assert result.receiver_verification.status is ReceiptVerificationStatus.VERIFIED
        assert restarted.case.lifecycle is CaseLifecycle.HANDOFF_READY
        assert restarted.case.receipt_fingerprint == result.receipt_fingerprint
        successful_handoff = result.stage_root
    finally:
        restarted.close()

    durable = load_case(case_path)
    assert durable.lifecycle is CaseLifecycle.HANDOFF_READY
    assert durable.case_id == case_id
    assert durable.receipt_fingerprint == result.receipt_fingerprint
    assert BagItPackageValidator().validate(successful_handoff).valid
    assert {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    } == source_before

    received_handoff = tmp_path / "receiver" / "copied-handoff"
    received_handoff.parent.mkdir()
    shutil.copytree(successful_handoff, received_handoff)
    received_result = verify_receipt(received_handoff)
    assert received_result.status is ReceiptVerificationStatus.VERIFIED
    assert received_result.receipt_fingerprint == result.receipt_fingerprint

    counterfactual = tmp_path / "receiver" / "altered-handoff"
    shutil.copytree(received_handoff, counterfactual)
    ledger_path = counterfactual / DECISION_LEDGER_PATH
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    resolved_targets = ledger["decisions"][0]["human_decision"]["resolved_targets"]
    role = next(iter(resolved_targets))
    original_target = PurePosixPath(resolved_targets[role])
    identity, _descriptor, role_and_extension = original_target.name.split("__", 2)
    resolved_targets[role] = (
        original_target.parent / f"{identity}__altered__{role_and_extension}"
    ).as_posix()
    ledger_path.write_text(
        json.dumps(
            ledger,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    BagItWriter().finalize_tagmanifest(counterfactual)
    assert BagItPackageValidator().validate(counterfactual).valid
    blocked = verify_receipt(counterfactual)
    assert blocked.status is ReceiptVerificationStatus.BLOCKED
    assert blocked.failed_check_ids == ("artifact_digest_mismatch:decision_ledger",)
    assert (
        verify_receipt(successful_handoff).status is ReceiptVerificationStatus.VERIFIED
    )
