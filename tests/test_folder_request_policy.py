"""Fail-closed request-policy tests for the complete-file contract."""

from __future__ import annotations

from pathlib import Path

import pytest

from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.request_policy import classify_unsupported_request


def _inventory(tmp_path: Path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "notes.txt").write_text("notes", encoding="utf-8")
    (root / ".env.local").write_text("secret", encoding="utf-8")
    return scan_folder(root).inventory


@pytest.mark.parametrize(
    ("instruction", "code"),
    [
        ("Delete old files and organize the rest.", "file_deletion_unsupported"),
        ("Deduplicate this folder.", "deduplication_unsupported"),
        ("Merge the two documents.", "merge_unsupported"),
        ("Keep only final versions.", "selection_unsupported"),
        ("Unzip the archives and sort them.", "archive_extraction_unsupported"),
        ("Rewrite the document text.", "content_editing_unsupported"),
        ("Refactor the source code imports.", "code_refactor_unsupported"),
        (
            "Inspect and move .env.local into config.",
            "protected_member_request_unsupported",
        ),
        (
            "Get rid of every old draft and organize what remains.",
            "file_deletion_unsupported",
        ),
        (
            "Purge the junk images before preparing the handoff.",
            "file_deletion_unsupported",
        ),
        (
            "Move all hidden configuration files into settings.",
            "protected_member_request_unsupported",
        ),
        (
            "Eliminate outdated drafts and organize the rest.",
            "file_deletion_unsupported",
        ),
        (
            "Trash the junk images before handoff.",
            "file_deletion_unsupported",
        ),
        (
            "Keep the final versions and leave everything else out.",
            "selection_unsupported",
        ),
        (
            "Consolidate duplicate documents into one.",
            "merge_unsupported",
        ),
        (
            "Move all env files into config.",
            "protected_member_request_unsupported",
        ),
        (
            "Rename all config files for the new client.",
            "protected_member_request_unsupported",
        ),
        (
            "Weed out obsolete drafts and organize the rest.",
            "file_deletion_unsupported",
        ),
        (
            "Take obsolete drafts out of the folder, then organize what is left.",
            "file_deletion_unsupported",
        ),
        (
            "Strip the project of outdated drafts, then organize it.",
            "file_deletion_unsupported",
        ),
        (
            "Pare the folder down to current documents.",
            "file_deletion_unsupported",
        ),
        (
            "Dispose of draft files, then organize the rest.",
            "file_deletion_unsupported",
        ),
        (
            "Set aside only the final versions and organize those.",
            "selection_unsupported",
        ),
    ],
)
def test_explicit_unsupported_requests_have_stable_blockers(
    tmp_path: Path,
    instruction: str,
    code: str,
) -> None:
    blocker = classify_unsupported_request(instruction, _inventory(tmp_path))

    assert blocker is not None
    assert blocker.code == code


@pytest.mark.parametrize(
    "instruction",
    [
        "Organize every file into clear handoff folders.",
        "Rename Apollo-labelled paths to Northstar and keep every file.",
        "Remove Apollo from filenames while preserving all files.",
        "Do not delete any files; organize all of them.",
        "Never delete anything; prepare a handoff copy.",
        "Organize everything but do not move .env.local.",
        "Keep .env.local where it is and organize the rest.",
        "Do not inspect secrets; organize other files.",
    ],
)
def test_supported_path_only_requests_are_not_falsely_blocked(
    tmp_path: Path,
    instruction: str,
) -> None:
    assert classify_unsupported_request(instruction, _inventory(tmp_path)) is None


def test_generic_config_language_is_supported_without_protected_config(
    tmp_path: Path,
) -> None:
    root = tmp_path / "ordinary-config"
    root.mkdir()
    (root / "config.yaml").write_text("theme: dark\n", encoding="utf-8")

    blocker = classify_unsupported_request(
        "Move all config files into settings.",
        scan_folder(root).inventory,
    )

    assert blocker is None
