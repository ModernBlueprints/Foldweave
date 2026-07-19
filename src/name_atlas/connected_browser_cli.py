"""Provider-lazy console entry for the Connected Change browser product."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from collections.abc import Sequence
from pathlib import Path

import uvicorn

from name_atlas.config import DEFAULT_PORT, LOOPBACK_HOST
from name_atlas.connected_planner_runtime import (
    PROJECT_ROOT,
    PlannerMode,
    planner_mode_configuration,
)
from name_atlas.connected_web_service import ConnectedBrowserRunService
from name_atlas.folder_app import create_folder_app
from name_atlas.folder_refactor.connected_change.job_service import (
    default_connected_change_job_path,
)

LOGGER = logging.getLogger(__name__)
HERO_CHANGE_FILE_DOWNLOAD_NAME = "northstar.nameatlas-change.json"


def build_connected_browser_parser() -> argparse.ArgumentParser:
    """Build the browser parser without initializing a provider or budget."""

    parser = argparse.ArgumentParser(
        prog="name-atlas run",
        description="Run the local Connected Change browser application.",
    )
    parser.add_argument(
        "--mode",
        choices=("development", "live", "replay"),
        required=True,
        help="Select deterministic development, live GPT-5.6, or exact replay.",
    )
    parser.add_argument("--source", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--job", type=Path, default=None)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    return parser


def build_connected_demo_parser() -> argparse.ArgumentParser:
    """Build the fixed-fixture demo parser."""

    parser = argparse.ArgumentParser(
        prog="name-atlas demo",
        description="Run the final bundled Connected Change demonstration.",
    )
    parser.add_argument("--mode", choices=("replay", "live"), required=True)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    return parser


def run_connected_demo(argv: Sequence[str] | None = None) -> int:
    """Materialize the bundled hero once and start its truthful planner mode."""

    args = build_connected_demo_parser().parse_args(argv)
    demo_root = PROJECT_ROOT / ".name-atlas" / "connected-demo" / args.mode
    fixture_root = demo_root / "fixture"
    source = fixture_root / "sofia-apollo"
    if not fixture_root.exists():
        from name_atlas.folder_refactor.demo_fixtures import (
            materialize_hero_fixture,
        )

        materialize_hero_fixture(fixture_root)
    elif not source.is_dir():
        print(
            "Startup blocked: the existing bundled-demo fixture is incomplete.",
            file=sys.stderr,
        )
        return 2
    output = demo_root / "results"
    output.mkdir(parents=True, exist_ok=True)
    return _run_connected_browser(
        mode=args.mode,
        source=source,
        output=output,
        job=demo_root / "state" / "job.json",
        port=args.port,
        demo=True,
    )


def run_connected_browser(argv: Sequence[str] | None = None) -> int:
    """Start one loopback browser without eager provider initialization."""

    args = build_connected_browser_parser().parse_args(argv)
    return _run_connected_browser(
        mode=args.mode,
        source=args.source,
        output=args.output,
        job=args.job,
        port=args.port,
        demo=False,
    )


def _run_connected_browser(
    *,
    mode: PlannerMode,
    source: Path | None,
    output: Path | None,
    job: Path | None,
    port: int,
    demo: bool,
) -> int:
    """Resolve local paths and inject one lazy truthful planner factory."""

    if not 1 <= port <= 65_535:
        print("Startup blocked: port must be between 1 and 65535.", file=sys.stderr)
        return 2
    job_path = (
        job.expanduser().resolve(strict=False)
        if job is not None
        else default_connected_change_job_path()
    )
    initial_source: Path | None = None
    initial_output_parent: Path | None = None
    try:
        if not os.path.lexists(job_path):
            if source is not None:
                initial_source = source.expanduser().resolve(strict=True)
                if not initial_source.is_dir():
                    raise NotADirectoryError("source must be a readable directory")
            if output is not None:
                initial_output_parent = output.expanduser().resolve(strict=True)
            elif initial_source is not None:
                initial_output_parent = initial_source.parent
            if initial_output_parent is not None and not initial_output_parent.is_dir():
                raise NotADirectoryError("output must be an existing directory")
        _require_persisted_planner_mode(job_path=job_path, requested_mode=mode)
        mode_config = planner_mode_configuration(
            mode,
            job_path=job_path,
            demo=demo,
        )
        service = ConnectedBrowserRunService(
            job_path=job_path,
            planner_provider_factory=mode_config.provider_factory,
            planner_label=mode_config.planner_label,
            planner_note=mode_config.planner_note,
            outbound_evidence_will_be_sent=(mode_config.outbound_evidence_will_be_sent),
            default_request=mode_config.default_request,
            change_file_download_name=(
                HERO_CHANGE_FILE_DOWNLOAD_NAME if demo else None
            ),
        )
        app = create_folder_app(
            service,
            initial_source=initial_source,
            initial_output_parent=initial_output_parent,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(
            f"Startup blocked: Connected Change job cannot be opened: {exc}",
            file=sys.stderr,
        )
        return 2

    logging.basicConfig(level=logging.INFO)
    LOGGER.info(
        "Starting Reversible Name Atlas on loopback with provider-lazy routing."
    )
    print(f"Reversible Name Atlas: http://{LOOPBACK_HOST}:{port}")
    print(service.planner_label)
    print(f"FolderRefactorJob: {job_path}")
    uvicorn.run(app, host=LOOPBACK_HOST, port=port, log_level="info")
    return 0


def _require_persisted_planner_mode(
    *,
    job_path: Path,
    requested_mode: PlannerMode,
) -> None:
    """Refuse a label/provider mode that differs from durable GPT provenance."""

    if not os.path.lexists(job_path):
        return
    from name_atlas.folder_refactor.connected_change.job_v2 import (
        FolderRefactorJobV2Store,
        GptPlannedJobAuthorityV2,
    )

    job = FolderRefactorJobV2Store(job_path).load()
    if not isinstance(job.authority, GptPlannedJobAuthorityV2):
        return
    progress = job.authority.planner_checkpoint.progress
    provider_kind = (
        progress.provider_kind
        if progress is not None
        else (
            job.authority.evidence_ledger.provider_kind
            if job.authority.evidence_ledger is not None
            else None
        )
    )
    if provider_kind is None:
        raise ValueError(
            "the persisted GPT-planned job has no truthful provider-mode binding"
        )
    persisted_mode: PlannerMode = {
        "deterministic": "development",
        "live": "live",
        "recorded_replay": "replay",
    }[provider_kind]
    if persisted_mode != requested_mode:
        raise ValueError(
            "the persisted job was created in "
            f"{persisted_mode!r} mode; restart with --mode {persisted_mode}"
        )
