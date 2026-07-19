"""Provider-free launch path for the Foldweave review browser."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Literal

import uvicorn

from name_atlas.config import DEFAULT_PORT, LOOPBACK_HOST
from name_atlas.folder_app import create_folder_app
from name_atlas.foldweave_paths import (
    foldweave_paths,
    resolve_foldweave_budget_authority,
    resolve_foldweave_job_path,
)
from name_atlas.foldweave_provider_factory import FoldweaveDirectProviderFactory
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService
from name_atlas.native_settings import (
    DirectEndpointProfile,
    EnvironmentCredentialStore,
)

FoldweaveAppMode = Literal["live", "development"]
LOGGER = logging.getLogger(__name__)


def build_foldweave_app_parser() -> argparse.ArgumentParser:
    """Build the F0a app parser without provider or budget initialization."""

    parser = argparse.ArgumentParser(
        prog="foldweave app",
        description=(
            "Run the Foldweave review-before-execution application on loopback."
        ),
        epilog=(
            "The default durable job is stored under "
            "~/Library/Application Support/Foldweave/jobs/. Development and "
            "automation may set FOLDWEAVE_STATE_ROOT to an absolute alternate "
            "root, or select one exact file with --job."
        ),
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help=(
            "Run the supported F0a browser fallback and print its loopback URL "
            "(the native shell is not live yet)."
        ),
    )
    parser.add_argument(
        "--mode",
        choices=("live", "development"),
        default="live",
        help=(
            "Use direct GPT-5.6 planning from the local environment (default), "
            "or explicit deterministic development planning."
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Optional existing source folder to prefill for a new job.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional existing output parent to prefill for a new job.",
    )
    parser.add_argument(
        "--job",
        type=Path,
        default=None,
        help="Optional exact durable v3 job JSON file.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Loopback port (default: {DEFAULT_PORT}).",
    )
    return parser


def run_foldweave_app(argv: Sequence[str] | None = None) -> int:
    """Parse and start the currently supported Foldweave application surface."""

    args = build_foldweave_app_parser().parse_args(argv)
    return _run_foldweave_browser(
        browser=args.browser,
        mode=args.mode,
        source=args.source,
        output=args.output,
        job=args.job,
        port=args.port,
    )


def _run_foldweave_browser(
    *,
    browser: bool,
    mode: FoldweaveAppMode,
    source: Path | None,
    output: Path | None,
    job: Path | None,
    port: int,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Resolve local inputs and run one deterministic review application."""

    if not browser:
        print(
            "Startup blocked: the native Foldweave shell is not available in "
            "the F0a gate; pass --browser.",
            file=sys.stderr,
        )
        return 2
    if mode not in {"live", "development"}:
        print("Startup blocked: Foldweave mode is unsupported.", file=sys.stderr)
        return 2
    if not 1 <= port <= 65_535:
        print("Startup blocked: port must be between 1 and 65535.", file=sys.stderr)
        return 2

    try:
        job_path = resolve_foldweave_job_path(job, environ=environ)
        initial_source: Path | None = None
        initial_output_parent: Path | None = None
        if not os.path.lexists(job_path):
            initial_source = _resolve_optional_directory(source, label="source")
            initial_output_parent = _resolve_optional_directory(
                output,
                label="output",
            )
            if initial_output_parent is None and initial_source is not None:
                initial_output_parent = initial_source.parent

        environment = os.environ if environ is None else environ
        provider_factory = None
        if mode == "live":
            budget_authority = resolve_foldweave_budget_authority(environ=environment)
            provider_factory = FoldweaveDirectProviderFactory(
                job_path=job_path,
                credential_store=EnvironmentCredentialStore(environment),
                endpoint=DirectEndpointProfile.official(),
                budget_authority=budget_authority,
            )
        service = FoldweaveBrowserReviewService(
            job_path=job_path,
            provider_factory=provider_factory,
            review_channel="browser",
        )
        app = create_folder_app(
            service,
            initial_source=initial_source,
            initial_output_parent=initial_output_parent,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        print(
            f"Startup blocked: Foldweave review application cannot be opened: {exc}",
            file=sys.stderr,
        )
        return 2

    logging.basicConfig(level=logging.INFO)
    LOGGER.info("Starting Foldweave %s review on loopback.", mode)
    print(f"Foldweave: http://{LOOPBACK_HOST}:{port}")
    print(
        "Live GPT-5.6 review"
        if mode == "live"
        else "Deterministic development review — no OpenAI API call"
    )
    print(f"FolderRefactorJobV3: {job_path}")
    uvicorn.run(app, host=LOOPBACK_HOST, port=port, log_level="info")
    return 0


def foldweave_state_root(
    *,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Return the production state root or one explicit absolute override."""

    return foldweave_paths(environ=environ).state_root


def default_foldweave_job_path(
    *,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Return the stable v3 job path used for application restart recovery."""

    return foldweave_paths(environ=environ).active_job


def _resolve_optional_directory(path: Path | None, *, label: str) -> Path | None:
    if path is None:
        return None
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise NotADirectoryError(f"{label} must be an existing directory")
    return resolved
