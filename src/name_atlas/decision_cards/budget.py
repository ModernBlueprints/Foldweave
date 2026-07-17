"""Persistent fail-closed project budget accounting for live GPT-5.6 calls."""

from __future__ import annotations

import fcntl
import os
import tempfile
from collections.abc import Callable
from contextlib import suppress
from datetime import datetime
from decimal import ROUND_CEILING, Decimal
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .errors import BudgetLedgerError, DecisionCardCapExhaustedError
from .models import MODEL_ALIAS, oslo_tz

BUDGET_SCHEMA_VERSION = "gpt-budget.v1"
MICRO_USD = 1_000_000
MAX_PROJECT_COST_MICRO_USD = 10 * MICRO_USD


class BudgetSnapshot(BaseModel):
    """Conservative spend exposure and reported usage for this project."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    schema_version: Literal["gpt-budget.v1"] = BUDGET_SCHEMA_VERSION
    model: Literal["gpt-5.6"] = MODEL_ALIAS
    configured_live_call_cap: int = Field(ge=1, le=100)
    configured_cost_cap_microusd: int = Field(
        ge=1,
        le=MAX_PROJECT_COST_MICRO_USD,
    )
    live_requests_reserved: int = Field(ge=0)
    provider_attempts_reserved: int = Field(ge=0)
    committed_cost_microusd: int = Field(ge=0)
    reported_estimated_cost_microusd: int = Field(ge=0)
    updated_at: datetime

    @field_validator("updated_at")
    @classmethod
    def require_oslo_timestamp(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("updated_at must be timezone-aware")
        oslo_value = value.astimezone(oslo_tz)
        if value.utcoffset() != oslo_value.utcoffset():
            raise ValueError("updated_at must use the Europe/Oslo offset")
        return value


def usd_to_microusd(value: float) -> int:
    """Round a nonnegative USD exposure upward to integer micro-dollars."""

    if value < 0:
        raise ValueError("USD value cannot be negative.")
    return int(
        (Decimal(str(value)) * MICRO_USD).to_integral_value(rounding=ROUND_CEILING)
    )


def microusd_to_usd(value: int) -> float:
    """Convert exact micro-dollars to a display float."""

    return value / MICRO_USD


class PersistentBudgetLedger:
    """Atomically reserve live-call exposure before any provider request."""

    def __init__(
        self,
        *,
        path: Path | None,
        live_call_cap: int,
        cost_cap_usd: float,
    ) -> None:
        if live_call_cap < 1:
            raise ValueError("Live call cap must be at least one.")
        cost_cap_microusd = usd_to_microusd(cost_cap_usd)
        if not 0 < cost_cap_microusd <= MAX_PROJECT_COST_MICRO_USD:
            raise ValueError("Cost cap must be positive and no more than USD 10.")
        self.path = path
        self.live_call_cap = live_call_cap
        self.cost_cap_microusd = cost_cap_microusd
        self._memory_snapshot = self._initial_snapshot()
        if self.path is not None and self.path.exists():
            self._memory_snapshot = self._read_path(self.path)
            self._assert_configuration(self._memory_snapshot)

    @property
    def snapshot(self) -> BudgetSnapshot:
        """Return current committed state, reloading a persistent ledger."""

        if self.path is None:
            return self._memory_snapshot
        if not self.path.exists():
            return self._memory_snapshot
        snapshot = self._read_path(self.path)
        self._assert_configuration(snapshot)
        self._memory_snapshot = snapshot
        return snapshot

    def reserve(
        self,
        *,
        reservation_usd: float,
        provider_attempts: int,
    ) -> BudgetSnapshot:
        """Commit conservative exposure before making a live provider call."""

        reservation_microusd = usd_to_microusd(reservation_usd)
        if reservation_microusd < 1 or provider_attempts < 1:
            raise ValueError("A live reservation and provider attempt are required.")
        if self.path is None:
            self._memory_snapshot = self._reserved_snapshot(
                self._memory_snapshot,
                reservation_microusd=reservation_microusd,
                provider_attempts=provider_attempts,
            )
            return self._memory_snapshot
        return self._mutate_locked(
            lambda current: self._reserved_snapshot(
                current,
                reservation_microusd=reservation_microusd,
                provider_attempts=provider_attempts,
            )
        )

    def record_reported_cost(self, cost_usd: float) -> BudgetSnapshot:
        """Add provider-reported estimated cost without releasing reservation."""

        reported_microusd = usd_to_microusd(cost_usd)

        def update(current: BudgetSnapshot) -> BudgetSnapshot:
            reported_total = (
                current.reported_estimated_cost_microusd + reported_microusd
            )
            return current.model_copy(
                update={
                    "reported_estimated_cost_microusd": reported_total,
                    "committed_cost_microusd": max(
                        current.committed_cost_microusd,
                        reported_total,
                    ),
                    "updated_at": datetime.now(tz=oslo_tz),
                }
            )

        if self.path is None:
            self._memory_snapshot = update(self._memory_snapshot)
            return self._memory_snapshot
        return self._mutate_locked(update)

    def _reserved_snapshot(
        self,
        current: BudgetSnapshot,
        *,
        reservation_microusd: int,
        provider_attempts: int,
    ) -> BudgetSnapshot:
        self._assert_configuration(current)
        if current.live_requests_reserved >= self.live_call_cap:
            raise DecisionCardCapExhaustedError(
                "The configured live-call cap is exhausted; "
                "the proposal remains unresolved."
            )
        committed = current.committed_cost_microusd + reservation_microusd
        if committed > self.cost_cap_microusd:
            raise DecisionCardCapExhaustedError(
                "The configured GPT-5.6 cost cap cannot reserve another call; "
                "the proposal remains unresolved."
            )
        return current.model_copy(
            update={
                "live_requests_reserved": current.live_requests_reserved + 1,
                "provider_attempts_reserved": (
                    current.provider_attempts_reserved + provider_attempts
                ),
                "committed_cost_microusd": committed,
                "updated_at": datetime.now(tz=oslo_tz),
            }
        )

    def _mutate_locked(
        self,
        mutation: Callable[[BudgetSnapshot], BudgetSnapshot],
    ) -> BudgetSnapshot:
        if self.path is None:
            raise AssertionError("Persistent mutation requires a ledger path.")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.path.with_suffix(f"{self.path.suffix}.lock")
        with lock_path.open("a+b") as lock_stream:
            fcntl.flock(lock_stream.fileno(), fcntl.LOCK_EX)
            try:
                current = (
                    self._read_path(self.path)
                    if self.path.exists()
                    else self._initial_snapshot()
                )
                self._assert_configuration(current)
                updated = mutation(current)
                self._write_path(self.path, updated)
                self._memory_snapshot = updated
                return updated
            finally:
                fcntl.flock(lock_stream.fileno(), fcntl.LOCK_UN)

    def _initial_snapshot(self) -> BudgetSnapshot:
        return BudgetSnapshot(
            configured_live_call_cap=self.live_call_cap,
            configured_cost_cap_microusd=self.cost_cap_microusd,
            live_requests_reserved=0,
            provider_attempts_reserved=0,
            committed_cost_microusd=0,
            reported_estimated_cost_microusd=0,
            updated_at=datetime.now(tz=oslo_tz),
        )

    def _assert_configuration(self, snapshot: BudgetSnapshot) -> None:
        if (
            snapshot.configured_live_call_cap != self.live_call_cap
            or snapshot.configured_cost_cap_microusd != self.cost_cap_microusd
        ):
            raise BudgetLedgerError(
                "Persistent GPT budget configuration does not match this run."
            )

    @staticmethod
    def _read_path(path: Path) -> BudgetSnapshot:
        try:
            return BudgetSnapshot.model_validate_json(path.read_bytes())
        except (OSError, ValidationError) as exc:
            raise BudgetLedgerError(
                "Persistent GPT budget record is missing, unreadable, or invalid."
            ) from exc

    @staticmethod
    def _write_path(path: Path, snapshot: BudgetSnapshot) -> None:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
        )
        temporary = Path(temporary_name)
        try:
            payload = f"{snapshot.model_dump_json(indent=2)}\n".encode()
            view = memoryview(payload)
            while view:
                written = os.write(descriptor, view)
                view = view[written:]
            os.fsync(descriptor)
            os.close(descriptor)
            descriptor = -1
            os.replace(temporary, path)
            directory_descriptor = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except OSError as exc:
            raise BudgetLedgerError(
                "Persistent GPT budget record could not be written atomically."
            ) from exc
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            with suppress(FileNotFoundError):
                temporary.unlink()
