"""Persistent conservative GPT-5.6 budget ledger tests."""

from pathlib import Path

import pytest

from name_atlas.decision_cards import (
    BudgetLedgerError,
    DecisionCardCapExhaustedError,
    PersistentBudgetLedger,
    microusd_to_usd,
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
