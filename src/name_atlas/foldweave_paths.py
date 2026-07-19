"""Stable application-owned paths for Foldweave native and browser surfaces."""

from __future__ import annotations

import os
import stat
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

FOLDWEAVE_STATE_ROOT_ENV = "FOLDWEAVE_STATE_ROOT"
FOLDWEAVE_BUDGET_LEDGER_ENV = "FOLDWEAVE_BUDGET_LEDGER"
DEFAULT_FOLDWEAVE_STATE_ROOT = (
    Path.home() / "Library" / "Application Support" / "Foldweave"
)
DEFAULT_FOLDWEAVE_JOB_NAME = "active.json"
DEFAULT_FOLDWEAVE_BUDGET_LEDGER_NAME = "api_budget.json"


@dataclass(frozen=True, slots=True)
class FoldweaveBudgetAuthority:
    """One selected budget authority for this Foldweave installation."""

    kind: Literal["qualification_existing", "installation_persistent"]
    path: Path

    def __post_init__(self) -> None:
        if self.kind not in {"qualification_existing", "installation_persistent"}:
            raise ValueError("Foldweave budget authority kind is unsupported.")
        if not self.path.is_absolute():
            raise ValueError("Foldweave budget authority path must be absolute.")


@dataclass(frozen=True, slots=True)
class FoldweavePaths:
    """One absolute state-root projection with no working-directory fallback."""

    state_root: Path

    def __post_init__(self) -> None:
        if not self.state_root.is_absolute():
            raise ValueError("Foldweave state root must be absolute.")

    @property
    def jobs(self) -> Path:
        return self.state_root / "jobs"

    @property
    def active_job(self) -> Path:
        return self.jobs / DEFAULT_FOLDWEAVE_JOB_NAME

    @property
    def budget_ledger(self) -> Path:
        return self.state_root / DEFAULT_FOLDWEAVE_BUDGET_LEDGER_NAME

    @property
    def preferences(self) -> Path:
        return self.state_root / "preferences"

    @property
    def diagnostics(self) -> Path:
        return self.state_root / "diagnostics"

    @property
    def instance_lock(self) -> Path:
        return self.state_root / "runtime.lock"


def foldweave_paths(
    *,
    environ: Mapping[str, str] | None = None,
) -> FoldweavePaths:
    """Resolve the production root or one explicit absolute test override."""

    environment = os.environ if environ is None else environ
    configured = environment.get(FOLDWEAVE_STATE_ROOT_ENV, "").strip()
    candidate = (
        DEFAULT_FOLDWEAVE_STATE_ROOT
        if not configured
        else Path(configured).expanduser()
    )
    if not candidate.is_absolute():
        raise ValueError(f"{FOLDWEAVE_STATE_ROOT_ENV} must be an absolute path.")
    _require_directory_or_absent(candidate, label="Foldweave state root")
    resolved = candidate.resolve(strict=False)
    _require_directory_or_absent(resolved, label="Foldweave state root")
    return FoldweavePaths(state_root=resolved)


def resolve_foldweave_job_path(
    job: Path | None,
    *,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Resolve one exact v3 JSON authority without creating it."""

    path = (
        foldweave_paths(environ=environ).active_job
        if job is None
        else job.expanduser().resolve(strict=False)
    )
    if not path.is_absolute() or path.suffix.casefold() != ".json":
        raise ValueError("Foldweave job must be one absolute JSON file.")
    if os.path.lexists(path):
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ValueError("Foldweave job must be a regular file.")
    else:
        _require_directory_or_absent(path.parent, label="Foldweave job parent")
    return path


def resolve_qualification_budget_ledger(
    *,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Resolve the explicitly injected sole build-qualification ledger."""

    environment = os.environ if environ is None else environ
    configured = environment.get(FOLDWEAVE_BUDGET_LEDGER_ENV, "").strip()
    if not configured:
        raise ValueError(
            f"{FOLDWEAVE_BUDGET_LEDGER_ENV} must name the sole existing ledger."
        )
    candidate = Path(configured).expanduser()
    if not candidate.is_absolute():
        raise ValueError(f"{FOLDWEAVE_BUDGET_LEDGER_ENV} must be absolute.")
    candidate_metadata = candidate.lstat()
    if stat.S_ISLNK(candidate_metadata.st_mode) or not stat.S_ISREG(
        candidate_metadata.st_mode
    ):
        raise ValueError("Foldweave budget ledger must be a regular file.")
    resolved = candidate.resolve(strict=True)
    metadata = resolved.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError("Foldweave budget ledger must be a regular file.")
    return resolved


def resolve_foldweave_budget_authority(
    *,
    environ: Mapping[str, str] | None = None,
) -> FoldweaveBudgetAuthority:
    """Select one strict qualification or lazy installation budget authority."""

    environment = os.environ if environ is None else environ
    if environment.get(FOLDWEAVE_BUDGET_LEDGER_ENV, "").strip():
        return FoldweaveBudgetAuthority(
            kind="qualification_existing",
            path=resolve_qualification_budget_ledger(environ=environment),
        )

    ledger = foldweave_paths(environ=environment).budget_ledger
    if os.path.lexists(ledger):
        metadata = ledger.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ValueError(
                "Foldweave installation budget ledger must be a regular file."
            )
    else:
        _require_directory_or_absent(
            ledger.parent,
            label="Foldweave installation budget parent",
        )
    return FoldweaveBudgetAuthority(
        kind="installation_persistent",
        path=ledger,
    )


def _require_directory_or_absent(path: Path, *, label: str) -> None:
    if not os.path.lexists(path):
        return
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"{label} must be a directory, not a link or file.")
