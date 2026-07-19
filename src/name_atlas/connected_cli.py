"""Provider-free command line surface for Connected Change application."""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Sequence
from pathlib import Path

from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
    ConnectedChangeJobServiceError,
    default_connected_change_job_path,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    FolderJobLifecycleV2,
    FolderJobV2Error,
)


def build_apply_change_parser() -> argparse.ArgumentParser:
    """Build the exact keyless Change File application parser."""

    parser = argparse.ArgumentParser(
        prog="name-atlas apply-change",
        description=(
            "Apply a verified Name Atlas Change File without GPT or an API key."
        ),
    )
    parser.add_argument("change_file", type=Path)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Result parent (default: .name-atlas/folder-results).",
    )
    parser.add_argument(
        "--job",
        type=Path,
        default=None,
        help=(
            "Resume this exact v2 job, or create it if absent "
            "(default: a new UUID-named .name-atlas/jobs file)."
        ),
    )
    return parser


def run_apply_change(argv: Sequence[str] | None = None) -> int:
    """Create or resume one deterministic provider-free receiver job."""

    args = build_apply_change_parser().parse_args(argv)
    try:
        source_root = args.source.expanduser().resolve(strict=True)
        if not source_root.is_dir():
            raise NotADirectoryError("source must be a readable directory")
        change_file_path = args.change_file.expanduser().resolve(strict=True)
        job_path = (
            args.job.expanduser().resolve(strict=False)
            if args.job is not None
            else default_connected_change_job_path()
        )
        if args.output is None:
            output_parent = (Path.cwd() / ".name-atlas" / "folder-results").resolve(
                strict=False
            )
            _require_separate_local_paths(source_root, output_parent, job_path)
            output_parent.mkdir(parents=True, exist_ok=True)
            output_parent = output_parent.resolve(strict=True)
        else:
            output_parent = args.output.expanduser().resolve(strict=True)
        if not output_parent.is_dir():
            raise NotADirectoryError("output must be an existing directory")
        job = ConnectedChangeJobService().start_application(
            change_file_path=change_file_path,
            source_root=source_root,
            output_parent=output_parent,
            job_path=job_path,
            idempotency_key=_cli_idempotency_key(job_path),
        )
    except (
        FolderJobV2Error,
        ConnectedChangeJobServiceError,
        OSError,
        ValueError,
    ) as exc:
        code = getattr(exc, "code", exc.__class__.__name__)
        print(f"APPLY BLOCKED {code}: {exc}", file=sys.stderr)
        return 1

    if job.lifecycle is not FolderJobLifecycleV2.VERIFIED:
        blocker = job.blocker_code or job.lifecycle.value
        print(f"APPLY BLOCKED {blocker}", file=sys.stderr)
        print(f"JOB {job.job_path}", file=sys.stderr)
        return 1
    if job.final_result_path is None or job.verified_artifacts is None:
        print("APPLY BLOCKED verified_job_incomplete", file=sys.stderr)
        return 1

    change_path, change_fingerprint, originating_receipt = (
        ConnectedChangeJobService().get_change_file(job.job_path)
    )
    print(f"VERIFIED {job.verified_artifacts.receipt_fingerprint}")
    print(f"JOB {job.job_path}")
    print(f"RESULT {job.final_result_path}")
    print(f"CHANGE_FILE {change_path}")
    print(f"CHANGE_FILE_FINGERPRINT {change_fingerprint}")
    print(f"ORIGINATING_RECEIPT {originating_receipt}")
    return 0


def _cli_idempotency_key(job_path: Path) -> str:
    """Bind CLI retries to the exact durable job path without persisting it raw."""

    digest = hashlib.sha256(
        str(job_path.resolve(strict=False)).encode("utf-8")
    ).hexdigest()
    return f"cli-apply-change:{digest}"


def _require_separate_local_paths(
    source_root: Path,
    output_parent: Path,
    job_path: Path,
) -> None:
    if _paths_overlap(source_root, output_parent):
        raise ValueError("source and output trees cannot overlap")
    if _paths_overlap(source_root, job_path.parent):
        raise ValueError("local job state cannot be inside the source tree")
    if _paths_overlap(output_parent, job_path.parent):
        raise ValueError("local job state cannot be inside the output tree")


def _paths_overlap(left: Path, right: Path) -> bool:
    resolved_left = left.resolve(strict=False)
    resolved_right = right.resolve(strict=False)
    return (
        resolved_left == resolved_right
        or resolved_left in resolved_right.parents
        or resolved_right in resolved_left.parents
    )
