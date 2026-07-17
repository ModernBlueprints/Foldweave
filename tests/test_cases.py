"""Persistent Migration Case contract and crash-safe store tests."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from name_atlas import cases as case_module
from name_atlas.cases import (
    CardDisplayOrigin,
    CaseDecisionBinding,
    CaseDecisionCardRecord,
    CaseDecisionMethod,
    CaseEvidenceRecord,
    CaseFinalizedError,
    CaseLifecycle,
    CaseLoadError,
    CaseLockError,
    CaseRevisionError,
    CaseWriteError,
    LocalCasePointers,
    MigrationCase,
    MigrationCaseStore,
    canonical_case_bytes,
    card_fingerprint,
    default_case_path,
    new_migration_case,
)
from name_atlas.decision_cards import (
    build_evidence_packet,
    evidence_fingerprint,
    load_recorded_decision_card,
)
from name_atlas.decisions import approve_family
from name_atlas.package_import import SourcePackage, import_package
from name_atlas.proposals import PathProposal, build_proposals

HERO_ROOT = Path(__file__).parents[1] / "sample_data" / "hero"
REPLAY_PATH = (
    Path(__file__).parents[1]
    / "src"
    / "name_atlas"
    / "recordings"
    / "hero_decision_card.json"
)
oslo_tz = ZoneInfo("Europe/Oslo")


@pytest.fixture(scope="module")
def hero_contract() -> tuple[SourcePackage, tuple[PathProposal, ...]]:
    package = import_package(HERO_ROOT)
    return package, build_proposals(package.families)


def _new_case(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
    *,
    now: datetime | None = None,
) -> MigrationCase:
    package, proposals = hero_contract
    return new_migration_case(
        package,
        proposals,
        case_path=tmp_path / "case.json",
        output_root=tmp_path / "output",
        case_name="Hero migration",
        now=now or datetime(2026, 7, 18, 1, 0, tzinfo=oslo_tz),
    )


def _replace_case(case: MigrationCase, **updates: object) -> MigrationCase:
    values = case.model_dump(mode="python")
    values.update(updates)
    return MigrationCase.model_validate(values, strict=True)


def _change_snapshot_commitment(raw: bytes) -> bytes:
    value = json.loads(raw)
    value["source_snapshot"]["commitment"] = "f" * 64
    return json.dumps(value).encode()


def _meaning_review_records(
    package: SourcePackage,
    proposals: tuple[PathProposal, ...],
) -> tuple[CaseEvidenceRecord, CaseDecisionCardRecord, CaseDecisionBinding]:
    family = next(
        family
        for family in package.families
        if family.canonical_identifier == "NA-0001"
    )
    packet = build_evidence_packet(package, family, proposals)
    fingerprint = evidence_fingerprint(packet)
    replay = load_recorded_decision_card(REPLAY_PATH.read_bytes())
    assert replay.evidence_fingerprint == fingerprint
    decision = approve_family(
        family,
        proposals,
        semantic_card_available=True,
    )
    evidence = CaseEvidenceRecord(
        family_id=family.family_id,
        packet=packet,
        evidence_fingerprint=fingerprint,
    )
    card_record = CaseDecisionCardRecord(
        family_id=family.family_id,
        evidence_fingerprint=fingerprint,
        card=replay.decision_card,
        card_fingerprint=card_fingerprint(replay.decision_card),
        display_origin=CardDisplayOrigin.RECORDED_REPLAY,
        generated_at=replay.generated_at,
        usage=replay.usage,
    )
    binding = CaseDecisionBinding(
        family_id=family.family_id,
        decision=decision,
        decision_method=CaseDecisionMethod.INDIVIDUAL_APPROVAL,
        decision_timestamp=datetime(2026, 7, 18, 1, 5, tzinfo=oslo_tz),
        evidence_fingerprint=fingerprint,
        card_fingerprint=card_record.card_fingerprint,
    )
    return evidence, card_record, binding


def test_default_case_path_uses_exact_resolved_root_hash(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    case_directory = tmp_path / "workspace" / ".name-atlas" / "cases"

    selected = default_case_path(source, case_directory=case_directory)

    expected_digest = hashlib.sha256(
        f"case-root\0{source.resolve().as_posix()}".encode()
    ).hexdigest()[:16]
    assert selected == case_directory.resolve() / f"{expected_digest}.json"
    assert selected.is_absolute()


def test_new_case_is_strict_path_neutral_and_deterministic(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
) -> None:
    case = _new_case(tmp_path, hero_contract)

    assert case.schema_version == "migration-case.v1"
    assert case.revision == 0
    assert case.lifecycle is CaseLifecycle.REVIEW
    assert case.source_root == HERO_ROOT.resolve()
    assert "source_root" not in case.source_snapshot.model_dump(mode="json")
    assert canonical_case_bytes(case) == canonical_case_bytes(case)
    assert canonical_case_bytes(case).endswith(b"\n")
    assert b'"schema_version":"migration-case.v1"' in canonical_case_bytes(case)
    with pytest.raises(ValidationError):
        MigrationCase.model_validate(
            {**case.model_dump(mode="python"), "unexpected": True},
            strict=True,
        )


def test_nested_evidence_card_and_human_binding_survive_restart(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
) -> None:
    package, proposals = hero_contract
    case = _new_case(tmp_path, hero_contract)
    evidence, card, binding = _meaning_review_records(package, proposals)
    bound_case = _replace_case(
        case,
        evidence_records=(evidence,),
        card_records=(card,),
        decisions=(binding,),
    )
    store = MigrationCaseStore(bound_case.local_paths.case_path)

    with store.writer() as writer:
        saved = writer.save(bound_case, expected_revision=None)
    loaded = store.load()

    assert loaded == saved
    assert loaded.evidence_records == (evidence,)
    assert loaded.card_records == (card,)
    assert loaded.decisions == (binding,)
    assert loaded.decisions[0].decision.resolved_targets == (
        binding.decision.resolved_targets
    )
    assert bound_case.source_root.as_posix().encode() in canonical_case_bytes(
        bound_case
    )


def test_store_owns_monotonic_revision_and_rejects_stale_writer(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
) -> None:
    initial_time = datetime(2026, 7, 18, 1, 0, tzinfo=oslo_tz)
    update_time = initial_time + timedelta(minutes=3)
    case = _new_case(tmp_path, hero_contract, now=initial_time)
    store = MigrationCaseStore(
        case.local_paths.case_path,
        clock=lambda: update_time,
    )
    with store.writer() as writer:
        created = writer.save(case, expected_revision=None)

    changed = _replace_case(created, case_name="Reviewed hero migration")
    with store.writer() as writer:
        revision_one = writer.save(changed, expected_revision=0)

    assert revision_one.revision == 1
    assert revision_one.updated_at == update_time
    with (
        store.writer() as writer,
        pytest.raises(CaseRevisionError, match="revision changed"),
    ):
        writer.save(changed, expected_revision=0)
    assert store.load() == revision_one


def test_writer_lock_is_nonblocking_and_held_for_complete_context(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
) -> None:
    case = _new_case(tmp_path, hero_contract)
    first = MigrationCaseStore(case.local_paths.case_path)
    second = MigrationCaseStore(case.local_paths.case_path)

    with first.writer() as first_writer:
        first_writer.save(case, expected_revision=None)
        with (
            pytest.raises(CaseLockError, match="already open"),
            second.writer(),
        ):
            pytest.fail("A second writer unexpectedly acquired the case lock.")

    with second.writer() as second_writer:
        assert second_writer.load() == case


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda _: b"{not-json", "corrupt, or unsupported"),
        (
            lambda raw: json.dumps(
                {
                    **json.loads(raw),
                    "schema_version": "migration-case.v999",
                }
            ).encode(),
            "corrupt, or unsupported",
        ),
        (
            lambda raw: json.dumps({**json.loads(raw), "unexpected": True}).encode(),
            "corrupt, or unsupported",
        ),
        (_change_snapshot_commitment, "corrupt, or unsupported"),
    ],
)
def test_strict_load_blocks_corruption_unknown_schema_and_extra_fields(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
    mutation: Callable[[bytes], bytes],
    message: str,
) -> None:
    case = _new_case(tmp_path, hero_contract)
    path = case.local_paths.case_path
    path.write_bytes(mutation(canonical_case_bytes(case)))

    with pytest.raises(CaseLoadError, match=message):
        MigrationCaseStore(path).load()


def test_atomic_replace_failure_preserves_prior_revision(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    case = _new_case(tmp_path, hero_contract)
    store = MigrationCaseStore(case.local_paths.case_path)
    with store.writer() as writer:
        writer.save(case, expected_revision=None)
    original_bytes = case.local_paths.case_path.read_bytes()
    changed = _replace_case(case, case_name="Must not become durable")

    def fail_replace(source: Path, destination: Path) -> None:
        del source, destination
        raise OSError("simulated atomic replacement failure")

    monkeypatch.setattr(case_module.os, "replace", fail_replace)
    with (
        store.writer() as writer,
        pytest.raises(CaseWriteError, match="atomically"),
    ):
        writer.save(changed, expected_revision=0)

    assert case.local_paths.case_path.read_bytes() == original_bytes
    assert not tuple(case.local_paths.case_path.parent.glob(".case.json.*.tmp"))


def test_handoff_ready_case_is_read_only(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    (source / "objects").mkdir(parents=True)
    (source / "metadata").mkdir()
    (source / "objects" / "poster.svg").write_text("poster", encoding="utf-8")
    (source / "metadata" / "metadata.csv").write_text(
        "filename,dc.identifier,dc.title\n"
        "objects/poster.svg,LOW-0001,Ordinary poster\n",
        encoding="utf-8",
    )
    package = import_package(source)
    proposals = build_proposals(package.families)
    base = new_migration_case(
        package,
        proposals,
        case_path=tmp_path / "case.json",
        output_root=tmp_path / "output",
        case_name="Finalized low-risk case",
        now=datetime(2026, 7, 18, 1, 0, tzinfo=oslo_tz),
    )
    family = package.families[0]
    decision = CaseDecisionBinding(
        family_id=family.family_id,
        decision=approve_family(
            family,
            proposals,
            semantic_card_available=False,
        ),
        decision_method=CaseDecisionMethod.BATCH_APPROVAL,
        decision_timestamp=datetime(
            2026,
            7,
            18,
            1,
            10,
            tzinfo=oslo_tz,
        ),
        evidence_fingerprint=None,
        card_fingerprint=None,
    )
    finalized = _replace_case(
        base,
        decisions=(decision,),
        local_paths=LocalCasePointers(
            output_root=base.local_paths.output_root,
            case_path=base.local_paths.case_path,
            stage_path=(tmp_path / "output" / "stage").resolve(),
            handoff_path=(tmp_path / "handoff" / "bag").resolve(),
        ),
        receipt_fingerprint="a" * 64,
        lifecycle=CaseLifecycle.HANDOFF_READY,
    )
    store = MigrationCaseStore(finalized.local_paths.case_path)
    with store.writer() as writer:
        writer.save(finalized, expected_revision=None)

    with (
        store.writer() as writer,
        pytest.raises(CaseFinalizedError, match="read-only"),
    ):
        writer.save(finalized, expected_revision=0)


def test_writer_refuses_calls_outside_process_lock(
    tmp_path: Path,
    hero_contract: tuple[SourcePackage, tuple[PathProposal, ...]],
) -> None:
    case = _new_case(tmp_path, hero_contract)
    writer = MigrationCaseStore(case.local_paths.case_path).writer()

    with pytest.raises(CaseLockError, match="active process-held"):
        writer.save(case, expected_revision=None)
