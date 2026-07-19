"""Persistent conservative GPT-5.6 budget ledger tests."""

import fcntl
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from name_atlas.decision_cards import (
    C3_LIVE_CALL_CAP,
    HISTORICAL_LIVE_CALL_CAP,
    BudgetLedgerError,
    BudgetSnapshot,
    DecisionCardCapExhaustedError,
    PersistentBudgetLedger,
    microusd_to_usd,
    migrate_live_call_cap,
)


def test_reservation_persists_and_call_cap_survives_restart(tmp_path: Path) -> None:
    path = tmp_path / "api_budget.json"
    first = PersistentBudgetLedger(
        path=path,
        live_call_cap=1,
        cost_cap_usd=10.0,
    )

    reserved = first.reserve(reservation_usd=0.75, provider_attempts=1)
    restarted = PersistentBudgetLedger(
        path=path,
        live_call_cap=1,
        cost_cap_usd=10.0,
    )

    assert reserved.live_requests_reserved == 1
    assert restarted.snapshot.provider_attempts_reserved == 1
    assert microusd_to_usd(restarted.snapshot.committed_cost_microusd) == 0.75
    with pytest.raises(DecisionCardCapExhaustedError, match="cap is exhausted"):
        restarted.reserve(reservation_usd=0.75, provider_attempts=1)


def test_reported_cost_never_releases_committed_reservation(tmp_path: Path) -> None:
    ledger = PersistentBudgetLedger(
        path=tmp_path / "api_budget.json",
        live_call_cap=8,
        cost_cap_usd=10.0,
    )
    ledger.reserve(reservation_usd=0.75, provider_attempts=1)

    updated = ledger.record_reported_cost(0.0025)

    assert microusd_to_usd(updated.committed_cost_microusd) == 0.75
    assert microusd_to_usd(updated.reported_estimated_cost_microusd) == 0.0025


def test_invalid_or_mismatched_persistent_record_fails_closed(
    tmp_path: Path,
) -> None:
    path = tmp_path / "api_budget.json"
    path.write_text("not-json", encoding="utf-8")

    with pytest.raises(BudgetLedgerError, match="invalid"):
        PersistentBudgetLedger(
            path=path,
            live_call_cap=8,
            cost_cap_usd=10.0,
        )

    path.unlink()
    ledger = PersistentBudgetLedger(
        path=path,
        live_call_cap=8,
        cost_cap_usd=10.0,
    )
    ledger.reserve(reservation_usd=0.75, provider_attempts=1)
    with pytest.raises(BudgetLedgerError, match="does not match"):
        PersistentBudgetLedger(
            path=path,
            live_call_cap=7,
            cost_cap_usd=10.0,
        )


def _historical_ledger(path: Path) -> PersistentBudgetLedger:
    ledger = PersistentBudgetLedger(
        path=path,
        live_call_cap=HISTORICAL_LIVE_CALL_CAP,
        cost_cap_usd=10.0,
    )
    ledger.reserve_microusd(
        reservation_microusd=679_000,
        provider_attempts=1,
    )
    ledger.record_reported_cost_microusd(38_200)
    return ledger


def test_c3_migration_is_atomic_idempotent_and_preserves_history(
    tmp_path: Path,
) -> None:
    path = tmp_path / "api_budget.json"
    before = _historical_ledger(path).snapshot
    before_values = before.model_dump(mode="python")

    migrated = migrate_live_call_cap(path=path)
    first_bytes = path.read_bytes()
    repeated = migrate_live_call_cap(path=path)

    assert migrated.configured_live_call_cap == C3_LIVE_CALL_CAP
    assert repeated == migrated
    assert path.read_bytes() == first_bytes
    assert migrated.model_dump(mode="python") == {
        **before_values,
        "configured_live_call_cap": C3_LIVE_CALL_CAP,
    }
    assert not tuple(tmp_path.glob(".api_budget.json.*.tmp"))


def test_c3_migration_write_failure_preserves_original_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = tmp_path / "api_budget.json"
    _historical_ledger(path)
    original = path.read_bytes()

    def fail_replace(source: object, destination: object) -> None:
        del source, destination
        raise OSError("injected atomic promotion failure")

    monkeypatch.setattr(os, "replace", fail_replace)
    with pytest.raises(BudgetLedgerError, match="written atomically"):
        migrate_live_call_cap(path=path)

    assert path.read_bytes() == original
    assert not tuple(tmp_path.glob(".api_budget.json.*.tmp"))


def test_c3_migration_requires_a_valid_existing_ledger(tmp_path: Path) -> None:
    path = tmp_path / "api_budget.json"
    with pytest.raises(BudgetLedgerError, match="required for migration"):
        migrate_live_call_cap(path=path)
    assert not path.exists()

    path.write_text("not-json", encoding="utf-8")
    with pytest.raises(BudgetLedgerError, match="invalid"):
        migrate_live_call_cap(path=path)


def test_strict_live_planner_requires_existing_historical_ledger(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing.json"
    with pytest.raises(BudgetLedgerError, match="required for live planning"):
        PersistentBudgetLedger.open_existing_live_planner(path=missing)
    assert not missing.exists()

    zero_state = tmp_path / "zero.json"
    snapshot = BudgetSnapshot(
        configured_live_call_cap=C3_LIVE_CALL_CAP,
        configured_cost_cap_microusd=10_000_000,
        live_requests_reserved=0,
        provider_attempts_reserved=0,
        committed_cost_microusd=0,
        reported_estimated_cost_microusd=0,
        updated_at=datetime.now(tz=ZoneInfo("Europe/Oslo")),
    )
    zero_state.write_text(snapshot.model_dump_json(), encoding="utf-8")
    with pytest.raises(BudgetLedgerError, match="historical provider authority"):
        PersistentBudgetLedger.open_existing_live_planner(path=zero_state)


@pytest.mark.parametrize(
    ("snapshot_update", "message"),
    (
        ({"configured_live_call_cap": 7}, "not eligible"),
        ({"configured_cost_cap_microusd": 9_000_000}, "cost authority"),
        ({"reported_estimated_cost_microusd": 38_199}, "history does not match"),
    ),
)
def test_c3_migration_rejects_incompatible_historical_authority(
    tmp_path: Path,
    snapshot_update: dict[str, int],
    message: str,
) -> None:
    path = tmp_path / "api_budget.json"
    snapshot = BudgetSnapshot(
        configured_live_call_cap=HISTORICAL_LIVE_CALL_CAP,
        configured_cost_cap_microusd=10_000_000,
        live_requests_reserved=1,
        provider_attempts_reserved=1,
        committed_cost_microusd=679_000,
        reported_estimated_cost_microusd=38_200,
        updated_at=datetime.now(tz=ZoneInfo("Europe/Oslo")),
    ).model_copy(update=snapshot_update)
    path.write_text(snapshot.model_dump_json(), encoding="utf-8")

    with pytest.raises(BudgetLedgerError, match=message):
        migrate_live_call_cap(path=path)


def test_strict_live_planner_uses_exact_microdollar_accounting(
    tmp_path: Path,
) -> None:
    path = tmp_path / "api_budget.json"
    _historical_ledger(path)
    migrate_live_call_cap(path=path)
    ledger = PersistentBudgetLedger.open_existing_live_planner(path=path)

    reserved = ledger.reserve_microusd(
        reservation_microusd=1_250_001,
        provider_attempts=1,
    )
    reported = ledger.record_reported_cost_microusd(125_001)

    assert reserved.live_requests_reserved == 2
    assert reserved.provider_attempts_reserved == 2
    assert reserved.committed_cost_microusd == 1_929_001
    assert reported.reported_estimated_cost_microusd == 163_201
    assert reported.committed_cost_microusd == 1_929_001

    path.unlink()
    with pytest.raises(BudgetLedgerError, match="required for live planning"):
        ledger.reserve_microusd(
            reservation_microusd=1,
            provider_attempts=1,
        )
    assert not path.exists()


def test_c3_migration_and_strict_live_planner_fail_on_lock_contention(
    tmp_path: Path,
) -> None:
    migration_path = tmp_path / "migration.json"
    _historical_ledger(migration_path)
    migration_lock = migration_path.with_suffix(".json.lock")
    with migration_lock.open("a+b") as lock_stream:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(BudgetLedgerError, match="locked by another process"):
            migrate_live_call_cap(path=migration_path)
        with pytest.raises(BudgetLedgerError, match="locked by another process"):
            PersistentBudgetLedger.open_existing_live_planner(path=migration_path)

    migrate_live_call_cap(path=migration_path)
    ledger = PersistentBudgetLedger.open_existing_live_planner(path=migration_path)
    with migration_lock.open("a+b") as lock_stream:
        fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(BudgetLedgerError, match="locked by another process"):
            ledger.reserve_microusd(
                reservation_microusd=1,
                provider_attempts=1,
            )


@pytest.mark.parametrize(
    ("snapshot_update", "message"),
    (
        ({"live_requests_reserved": 14}, "reserved live requests"),
        ({"provider_attempts_reserved": 0}, "provider attempts"),
        ({"committed_cost_microusd": 10_000_001}, "committed exposure"),
        (
            {"reported_estimated_cost_microusd": 680_000},
            "reported cost",
        ),
    ),
)
def test_budget_snapshot_rejects_internally_inconsistent_authority(
    snapshot_update: dict[str, int],
    message: str,
) -> None:
    base = {
        "configured_live_call_cap": C3_LIVE_CALL_CAP,
        "configured_cost_cap_microusd": 10_000_000,
        "live_requests_reserved": 1,
        "provider_attempts_reserved": 1,
        "committed_cost_microusd": 679_000,
        "reported_estimated_cost_microusd": 38_200,
        "updated_at": datetime.now(tz=ZoneInfo("Europe/Oslo")),
    }

    with pytest.raises(ValueError, match=message):
        BudgetSnapshot.model_validate({**base, **snapshot_update})
