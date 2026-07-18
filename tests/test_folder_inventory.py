"""AI-first generic-folder inventory contract tests."""

from __future__ import annotations

import os
from pathlib import Path

import pytest
from pydantic import ValidationError

import name_atlas.folder_refactor.inventory as inventory_module
from name_atlas.folder_refactor.contracts import FolderFile, FolderInventory
from name_atlas.folder_refactor.inventory import (
    MAX_DIRECTORY_COUNT,
    MAX_FILE_COUNT,
    FolderScanError,
    inventory_evidence_ids,
    scan_folder,
)


def _write(root: Path, relative_path: str, payload: bytes = b"payload") -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


def test_scan_is_complete_path_neutral_sorted_and_deterministic(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, "zeta/image.bin", b"\x00\x01")
    _write(source, "alpha/readme.md", b"# Read me\n")
    _write(source, ".env", b"TOKEN=not-a-real-secret\n")
    (source / "empty" / "nested").mkdir(parents=True)

    first = scan_folder(source)
    second = scan_folder(source)
    portable = first.inventory.model_dump(mode="json")

    assert first.source_root == source.resolve()
    assert first.inventory == second.inventory
    assert first.inventory.schema_version == "folder-inventory.v1"
    assert [item.relative_path for item in first.inventory.files] == [
        ".env",
        "alpha/readme.md",
        "zeta/image.bin",
    ]
    assert [item.relative_path for item in first.inventory.empty_directories] == [
        "empty/nested"
    ]
    assert first.inventory.directory_count == 4
    assert first.inventory.total_bytes == sum(
        item.size for item in first.inventory.files
    )
    assert str(source.resolve()) not in repr(portable)
    assert {item["member_kind"] for item in portable["files"]} == {"regular_file"}
    assert portable["empty_directories"][0]["member_kind"] == "empty_directory"


@pytest.mark.parametrize(
    ("relative_path", "expected_reasons"),
    [
        (".hidden", {"dot_path"}),
        (".git/config", {"dot_path"}),
        ("nested/.cache/value.txt", {"dot_path"}),
        ("folder/.ENV.production", {"dot_path", "environment_file"}),
        ("folder/.NPMRC", {"dot_path", "sensitive_basename"}),
        ("folder/ID_ED25519", {"sensitive_basename"}),
        ("folder/Credentials-prod.json", {"sensitive_prefix"}),
        ("folder/SecretsBackup.txt", {"sensitive_prefix"}),
        ("folder/private.PEM", {"sensitive_suffix"}),
        ("folder/vault.KDBX", {"sensitive_suffix"}),
    ],
)
def test_protected_members_are_included_fixed_and_evidence_denied(
    tmp_path: Path,
    relative_path: str,
    expected_reasons: set[str],
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, relative_path)

    scanned = scan_folder(source)
    member = scanned.inventory.files[0]

    assert member.relative_path == relative_path
    assert member.protected is True
    assert member.evidence_eligible is False
    assert set(member.protection_reasons) == expected_reasons
    assert f"inventory:{member.file_id}" in inventory_evidence_ids(scanned.inventory)


@pytest.mark.parametrize(
    ("relative_path", "eligible"),
    [
        ("notes.md", True),
        ("notes.MARKDOWN", True),
        ("brief.TXT", True),
        ("table.CSV", True),
        ("photo.jpg", False),
        ("document.pdf", False),
        ("opaque.bin", False),
    ],
)
def test_only_unprotected_supported_text_types_are_evidence_eligible(
    tmp_path: Path,
    relative_path: str,
    eligible: bool,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, relative_path)

    member = scan_folder(source).inventory.files[0]

    assert member.protected is False
    assert member.evidence_eligible is eligible
    assert member.protection_reasons == ()


def test_file_identity_binds_path_size_and_digest(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, "first.txt", b"identical")
    _write(source, "second.txt", b"identical")

    inventory = scan_folder(source).inventory
    first, second = inventory.files

    assert first.sha256 == second.sha256
    assert first.size == second.size
    assert first.file_id != second.file_id

    with pytest.raises(ValidationError, match="File identity"):
        FolderFile.model_validate(
            {**first.model_dump(mode="python"), "file_id": "f" * 64},
            strict=True,
        )


def test_markdown_adapter_limit_blocks_before_unbounded_parsing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    monkeypatch.setattr(inventory_module, "MAX_MARKDOWN_ADAPTER_BYTES", 8)
    _write(source, "large.md", b"123456789")

    with pytest.raises(FolderScanError, match="Markdown adapter byte limit"):
        scan_folder(source)

    opaque = tmp_path / "opaque"
    opaque.mkdir()
    _write(opaque, "large.bin", b"123456789")
    assert scan_folder(opaque).inventory.total_bytes == 9


def test_portable_commitment_ignores_local_inode_but_local_identity_detects_replacement(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    original = _write(source, "note.txt", b"same bytes")
    first = scan_folder(source)
    replacement = _write(source, "replacement.tmp", b"same bytes")
    replacement_inode = replacement.stat().st_ino
    replacement.replace(original)

    second = scan_folder(source)

    assert first.inventory.source_commitment == second.inventory.source_commitment
    assert first.local_file_identities[0].inode != replacement_inode
    assert second.local_file_identities[0].inode == replacement_inode
    assert first.local_file_identities != second.local_file_identities


def test_local_directory_identity_detects_path_preserving_replacement(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    original_directory = source / "notes"
    original_directory.mkdir()
    payload = _write(source, "notes/brief.txt", b"same member")
    first = scan_folder(source)

    replacement_directory = source / "replacement"
    replacement_directory.mkdir()
    original_inode = original_directory.stat().st_ino
    replacement_inode = replacement_directory.stat().st_ino
    payload.rename(replacement_directory / payload.name)
    original_directory.rmdir()
    replacement_directory.rename(original_directory)

    second = scan_folder(source)

    assert first.inventory.source_commitment == second.inventory.source_commitment
    assert first.local_file_identities == second.local_file_identities
    assert original_inode != replacement_inode
    first_notes = next(
        item
        for item in first.local_directory_identities
        if item.relative_path == "notes"
    )
    second_notes = next(
        item
        for item in second.local_directory_identities
        if item.relative_path == "notes"
    )
    assert first_notes.inode == original_inode
    assert second_notes.inode == replacement_inode
    assert first.local_directory_identities != second.local_directory_identities


def test_inventory_contract_rejects_tampered_totals_commitment_and_extra_fields(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, "note.txt")
    inventory = scan_folder(source).inventory
    raw = inventory.model_dump(mode="python")

    with pytest.raises(ValidationError, match="total bytes"):
        FolderInventory.model_validate(
            {**raw, "total_bytes": inventory.total_bytes + 1},
            strict=True,
        )
    with pytest.raises(ValidationError, match="source commitment"):
        FolderInventory.model_validate(
            {**raw, "source_commitment": "f" * 64},
            strict=True,
        )
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        FolderInventory.model_validate({**raw, "source_root": str(source)}, strict=True)


@pytest.mark.parametrize("member_kind", ["file_symlink", "directory_symlink", "fifo"])
def test_unsupported_members_fail_closed(
    tmp_path: Path,
    member_kind: str,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, "ordinary.txt")
    if member_kind == "file_symlink":
        (source / "alias.txt").symlink_to(source / "ordinary.txt")
    elif member_kind == "directory_symlink":
        target = tmp_path / "elsewhere"
        target.mkdir()
        (source / "alias-dir").symlink_to(target, target_is_directory=True)
    else:
        os.mkfifo(source / "named-pipe")

    with pytest.raises(FolderScanError, match="unsupported"):
        scan_folder(source)


def test_hard_link_fails_closed(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    original = _write(source, "ordinary.txt")
    os.link(original, source / "hard-link.txt")

    with pytest.raises(FolderScanError, match="Hard-linked"):
        scan_folder(source)


@pytest.mark.parametrize("bad_name", ["bad\\name.txt", "bad\nname.txt"])
def test_unsupported_source_path_fails_closed(
    tmp_path: Path,
    bad_name: str,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, bad_name)

    with pytest.raises(FolderScanError, match="source path|control character"):
        scan_folder(source)


def test_protected_path_that_cannot_remain_fixed_fails_before_planning(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, ".secret:key")

    with pytest.raises(FolderScanError, match="cannot satisfy the result profile"):
        scan_folder(source)


def test_empty_source_and_member_limits_fail_closed(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(FolderScanError, match="no regular files"):
        scan_folder(empty)

    too_many_files = tmp_path / "too-many-files"
    too_many_files.mkdir()
    for index in range(MAX_FILE_COUNT + 1):
        _write(too_many_files, f"{index:04d}.txt", b"")
    with pytest.raises(FolderScanError, match=f"more than {MAX_FILE_COUNT}"):
        scan_folder(too_many_files)

    too_many_directories = tmp_path / "too-many-directories"
    too_many_directories.mkdir()
    _write(too_many_directories, "ordinary.txt")
    for index in range(MAX_DIRECTORY_COUNT + 1):
        (too_many_directories / f"d-{index:04d}").mkdir()
    with pytest.raises(FolderScanError, match=f"more than {MAX_DIRECTORY_COUNT}"):
        scan_folder(too_many_directories)


@pytest.mark.parametrize("root_kind", ["missing", "file", "symlink"])
def test_source_root_must_be_an_existing_real_directory(
    tmp_path: Path,
    root_kind: str,
) -> None:
    root = tmp_path / root_kind
    if root_kind == "file":
        root.write_text("not a directory", encoding="utf-8")
    elif root_kind == "symlink":
        target = tmp_path / "real-directory"
        target.mkdir()
        root.symlink_to(target, target_is_directory=True)

    with pytest.raises(FolderScanError, match="Source root"):
        scan_folder(root)
