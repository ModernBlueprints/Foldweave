"""Provider-free launch path for the Foldweave review browser."""

from __future__ import annotations

import argparse
import logging
import os
import stat
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Literal

import uvicorn

from name_atlas.config import DEFAULT_PORT, LOOPBACK_HOST
from name_atlas.folder_app import create_folder_app
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService

FoldweaveAppMode = Literal["development"]
FOLDWEAVE_STATE_ROOT_ENV = "FOLDWEAVE_STATE_ROOT"
DEFAULT_FOLDWEAVE_STATE_ROOT = (
    Path.home() / "Library" / "Application Support" / "Foldweave"
)
DEFAULT_FOLDWEAVE_JOB_NAME = "active.json"

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
        choices=("development",),
        required=True,
        help="Use deterministic development planning; no OpenAI API call is made.",
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
    if mode != "development":
        print(
            "Startup blocked: only deterministic development mode is available "
            "in the F0a gate.",
            file=sys.stderr,
        )
        return 2
    if not 1 <= port <= 65_535:
        print("Startup blocked: port must be between 1 and 65535.", file=sys.stderr)
        return 2

    try:
        job_path = _resolve_job_path(job=job, environ=environ)
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

        service = FoldweaveBrowserReviewService(job_path=job_path)
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
    LOGGER.info(
        "Starting Foldweave deterministic development review on loopback; "
        "provider and budget authorities are not initialized."
    )
    print(f"Foldweave: http://{LOOPBACK_HOST}:{port}")
    print("Deterministic development review — no OpenAI API call")
    print(f"FolderRefactorJobV3: {job_path}")
    uvicorn.run(app, host=LOOPBACK_HOST, port=port, log_level="info")
    return 0


def foldweave_state_root(
    *,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Return the production state root or one explicit absolute override."""

    environment = os.environ if environ is None else environ
    configured = environment.get(FOLDWEAVE_STATE_ROOT_ENV, "").strip()
    if not configured:
        return DEFAULT_FOLDWEAVE_STATE_ROOT.expanduser().resolve(strict=False)
    candidate = Path(configured).expanduser()
    if not candidate.is_absolute():
        raise ValueError(f"{FOLDWEAVE_STATE_ROOT_ENV} must be an absolute path")
    return candidate.resolve(strict=False)


def default_foldweave_job_path(
    *,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Return the stable v3 job path used for application restart recovery."""

    return foldweave_state_root(environ=environ) / "jobs" / DEFAULT_FOLDWEAVE_JOB_NAME


def _resolve_job_path(
    *,
    job: Path | None,
    environ: Mapping[str, str] | None,
) -> Path:
    path = (
        default_foldweave_job_path(environ=environ)
        if job is None
        else job.expanduser().resolve(strict=False)
    )
    if path.suffix.lower() != ".json":
        raise ValueError("job must be one JSON file")
    if os.path.lexists(path):
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise ValueError("job must be a regular file, not a link or directory")
    elif os.path.lexists(path.parent) and not path.parent.is_dir():
        raise ValueError("job parent must be a directory")
    return path


def _resolve_optional_directory(path: Path | None, *, label: str) -> Path | None:
    if path is None:
        return None
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise NotADirectoryError(f"{label} must be an existing directory")
    return resolved
