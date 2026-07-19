"""Lazy live, replay, and development planner configuration for the browser."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from name_atlas.folder_refactor.demo_fixtures import HERO_REQUEST

PlannerMode = Literal["development", "live", "replay"]

PACKAGE_ROOT = Path(__file__).resolve().parent
_CHECKOUT_ROOT = PACKAGE_ROOT.parents[1]
PROJECT_ROOT = (
    _CHECKOUT_ROOT
    if (_CHECKOUT_ROOT / "pyproject.toml").is_file()
    and (_CHECKOUT_ROOT / "src" / "name_atlas").resolve() == PACKAGE_ROOT
    else Path.cwd()
)
BUDGET_LEDGER_PATH = PROJECT_ROOT / ".name-atlas" / "api_budget.json"
HERO_REPLAY_PATH = PACKAGE_ROOT / "recordings" / "folder_hero_zero_question.json"
AMBIGUITY_REPLAY_PATH = (
    PACKAGE_ROOT / "recordings" / "folder_ambiguity_one_question.json"
)
REPLAY_PATHS = (HERO_REPLAY_PATH, AMBIGUITY_REPLAY_PATH)


@dataclass(frozen=True, slots=True)
class PlannerModeConfiguration:
    """Truthful browser wording and a lazy provider constructor."""

    mode: PlannerMode
    planner_label: str
    planner_note: str
    outbound_evidence_will_be_sent: bool
    default_request: str
    provider_factory: Callable[[], object] | None


def planner_mode_configuration(
    mode: PlannerMode,
    *,
    job_path: Path,
    demo: bool,
    replay_path: Path = HERO_REPLAY_PATH,
) -> PlannerModeConfiguration:
    """Configure one mode without reading credentials or opening the budget."""

    if mode == "development":
        from name_atlas.connected_web_service import DETERMINISTIC_BROWSER_REQUEST

        return PlannerModeConfiguration(
            mode=mode,
            planner_label="Deterministic development planning — no API call",
            planner_note=(
                "This internal development route exercises the same fixed compiler "
                "and verified copy transaction without GPT."
            ),
            outbound_evidence_will_be_sent=False,
            default_request=DETERMINISTIC_BROWSER_REQUEST,
            provider_factory=None,
        )
    if mode == "replay":
        return PlannerModeConfiguration(
            mode=mode,
            planner_label="Recorded GPT-5.6 planning run",
            planner_note=(
                "This exact recorded planning run makes no API call and requires "
                "no API key. Its fixture, request, schemas, evidence, tool sequence, "
                "and accepted plan must all match."
            ),
            outbound_evidence_will_be_sent=False,
            default_request=HERO_REQUEST if demo else "",
            provider_factory=lambda: _recorded_provider(replay_path),
        )
    if mode != "live":
        raise ValueError(f"Unsupported planner mode: {mode}")
    return PlannerModeConfiguration(
        mode=mode,
        planner_label="Live GPT-5.6 planning",
        planner_note=(
            "GPT-5.6 receives only the bounded evidence disclosed below. Fixed "
            "code validates the complete plan before creating a separate result."
        ),
        outbound_evidence_will_be_sent=True,
        default_request=HERO_REQUEST if demo else "",
        provider_factory=lambda: _live_provider(job_path),
    )


def _recorded_provider(replay_path: Path) -> object:
    from name_atlas.folder_refactor.planner_recording import (
        RecordedPlannerProvider,
    )

    try:
        payload = replay_path.read_bytes()
    except OSError as exc:
        raise RuntimeError(
            "The recorded GPT-5.6 planning run is missing or unreadable."
        ) from exc
    return RecordedPlannerProvider(payload)


def provider_for_persisted_job(job_path: Path) -> object:
    """Construct only the provider origin already bound to one durable job."""

    from name_atlas.folder_refactor.connected_change.job_v2 import (
        FolderRefactorJobV2,
        FolderRefactorJobV2Store,
        GptPlannedJobAuthorityV2,
    )

    record = FolderRefactorJobV2Store(job_path).inspect()
    if not isinstance(record, FolderRefactorJobV2) or not isinstance(
        record.authority,
        GptPlannedJobAuthorityV2,
    ):
        raise RuntimeError("The durable job does not have GPT planning authority.")
    progress = record.authority.planner_checkpoint.progress
    provider_kind = (
        progress.provider_kind
        if progress is not None
        else (
            record.authority.evidence_ledger.provider_kind
            if record.authority.evidence_ledger is not None
            else None
        )
    )
    if provider_kind == "live":
        return _live_provider(record.job_path)
    if provider_kind != "recorded_replay":
        raise RuntimeError(
            "The durable job is not bound to a supported MCP planner origin."
        )

    from name_atlas.folder_refactor.planner_recording import (
        RecordedPlannerProvider,
        load_folder_planner_replay,
    )
    from name_atlas.folder_refactor.serialization import request_fingerprint

    expected_request = request_fingerprint(record.user_request)
    matches = []
    for replay_path in REPLAY_PATHS:
        try:
            replay = load_folder_planner_replay(replay_path.read_bytes())
        except (OSError, ValueError) as exc:
            raise RuntimeError(
                "A bundled GPT-5.6 planning recording is unavailable or invalid."
            ) from exc
        if (
            replay.source_commitment == record.source_inventory.source_commitment
            and replay.request_fingerprint == expected_request
        ):
            matches.append(replay)
    if len(matches) != 1:
        raise RuntimeError(
            "The durable job does not match exactly one bundled GPT-5.6 recording."
        )
    return RecordedPlannerProvider(matches[0])


def _live_provider(job_path: Path) -> object:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key.strip():
        raise RuntimeError(
            "Live GPT-5.6 planning is blocked: configure OPENAI_API_KEY locally."
        )
    from name_atlas.decision_cards.budget import PersistentBudgetLedger
    from name_atlas.folder_refactor.connected_change.job_v2 import (
        FolderRefactorJobV2,
        FolderRefactorJobV2Store,
        GptPlannedJobAuthorityV2,
    )
    from name_atlas.folder_refactor.live_planner_provider import (
        LiveFolderPlannerProvider,
    )

    existing_usage = ()
    if os.path.lexists(job_path):
        job = FolderRefactorJobV2Store(job_path).load()
        if isinstance(job, FolderRefactorJobV2) and isinstance(
            job.authority,
            GptPlannedJobAuthorityV2,
        ):
            existing_usage = job.authority.planner_checkpoint.usage
    budget = PersistentBudgetLedger.open_existing_foldweave_planner(
        path=BUDGET_LEDGER_PATH
    )
    return LiveFolderPlannerProvider.from_api_key(
        api_key,
        budget=budget,
        existing_usage=existing_usage,
    )
