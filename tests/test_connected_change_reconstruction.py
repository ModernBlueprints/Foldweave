"""Receiver-specific v2 reconstruction tests."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

import pytest
from connected_change_fixtures import portable_tree, tree_state

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    build_connected_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.reconstruction import (
    _LoadedReceiverAuthorities,
    restore_connected_result,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.portable_artifacts import (
    ACCEPTED_PLAN_PATH,
    FORWARD_PATH_MAP_PATH,
    REVERSE_PATH_MAP_PATH,
    SOURCE_SNAPSHOT_PATH,
    canonical_portable_json_bytes,
    render_folder_path_map,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderArtifactCommitment,
    FolderPathMapRow,
)
from name_atlas.folder_refactor.reconstruction import FolderReconstructionError


@dataclass(frozen=True, slots=True)
class _ReceiptCore:
    source_commitment: str
    artifact_commitments: tuple[FolderArtifactCommitment, ...]


@dataclass(frozen=True, slots=True)
class _ReceiptEnvelope:
    receipt: _ReceiptCore
    receipt_fingerprint: str


@dataclass(frozen=True, slots=True)
class _Verification:
    status: str
    receipt_fingerprint: str | None
    failed_check_ids: tuple[str, ...] = ()


def _write(root: Path, relative_path: str, payload: bytes) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _receiver_authorities(tmp_path: Path) -> tuple[Path, _LoadedReceiverAuthorities]:
    source = tmp_path / "receiver-source"
    original_markdown = b"Use [asset](../originals/item.txt#final).\r\n"
    _write(source, "drafts/note.md", original_markdown)
    _write(source, "originals/item.txt", b"receiver payload\n")
    (source / "empty" / "keep").mkdir(parents=True)
    inventory = scan_folder(source).inventory
    by_path = {item.relative_path: item for item in inventory.files}
    plan = build_connected_accepted_plan(
        inventory=inventory,
        request="Apply the shared Northstar organization.",
        evidence_fingerprint="a" * 64,
        result_folder_name="northstar-shared",
        target_by_file_id={
            by_path["drafts/note.md"].file_id: "notes/client-brief.md",
            by_path["originals/item.txt"].file_id: "deliverables/item.txt",
        },
        execution_authority="change_file",
    )
    rewritten_markdown = b"Use [asset](../deliverables/item.txt#final).\r\n"
    rows = tuple(
        sorted(
            (
                FolderPathMapRow(
                    file_id=by_path["drafts/note.md"].file_id,
                    original_path="drafts/note.md",
                    result_path="notes/client-brief.md",
                    original_size=len(original_markdown),
                    original_sha256=hashlib.sha256(original_markdown).hexdigest(),
                    result_size=len(rewritten_markdown),
                    result_sha256=hashlib.sha256(rewritten_markdown).hexdigest(),
                    protected=False,
                    markdown_rewritten=True,
                ),
                FolderPathMapRow(
                    file_id=by_path["originals/item.txt"].file_id,
                    original_path="originals/item.txt",
                    result_path="deliverables/item.txt",
                    original_size=len(b"receiver payload\n"),
                    original_sha256=hashlib.sha256(b"receiver payload\n").hexdigest(),
                    result_size=len(b"receiver payload\n"),
                    result_sha256=hashlib.sha256(b"receiver payload\n").hexdigest(),
                    protected=False,
                    markdown_rewritten=False,
                ),
            ),
            key=lambda row: row.original_path,
        )
    )

    result = tmp_path / "received-result"
    _write(result, "data/notes/client-brief.md", rewritten_markdown)
    _write(result, "data/deliverables/item.txt", b"receiver payload\n")
    _write(
        result,
        f"name-atlas/original-content/{by_path['drafts/note.md'].file_id}.bin",
        original_markdown,
    )
    inventory_bytes = canonical_portable_json_bytes(inventory)
    plan_bytes = canonical_portable_json_bytes(plan)
    forward_bytes = render_folder_path_map(rows, reverse=False)
    reverse_bytes = render_folder_path_map(rows, reverse=True)
    receipt_bytes = b'{"schema_version":"folder-change-receipt.v2"}'
    payloads = {
        SOURCE_SNAPSHOT_PATH: inventory_bytes,
        ACCEPTED_PLAN_PATH: plan_bytes,
        FORWARD_PATH_MAP_PATH: forward_bytes,
        REVERSE_PATH_MAP_PATH: reverse_bytes,
    }
    commitments = tuple(
        FolderArtifactCommitment(
            path=path,
            size=len(payload),
            sha256=hashlib.sha256(payload).hexdigest(),
        )
        for path, payload in sorted(payloads.items())
    )
    fingerprint = "b" * 64
    envelope = _ReceiptEnvelope(
        receipt=_ReceiptCore(
            source_commitment=inventory.source_commitment,
            artifact_commitments=commitments,
        ),
        receipt_fingerprint=fingerprint,
    )
    return source, _LoadedReceiverAuthorities(
        inventory_bytes=inventory_bytes,
        accepted_plan_bytes=plan_bytes,
        receipt_bytes=receipt_bytes,
        forward_bytes=forward_bytes,
        reverse_bytes=reverse_bytes,
        inventory=inventory,
        accepted_plan=plan,
        envelope=envelope,
        path_rows=rows,
    )


def test_recreates_receivers_own_paths_bytes_and_empty_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, authorities = _receiver_authorities(tmp_path)
    result = tmp_path / "received-result"
    unrelated_parent = tmp_path / "unrelated-parent"
    unrelated_parent.mkdir()
    destination = unrelated_parent / "receiver-original-recreated"
    fingerprint = authorities.envelope.receipt_fingerprint
    verification_calls: list[Path] = []

    def verify(root: Path) -> _Verification:
        verification_calls.append(root)
        return _Verification(status="verified", receipt_fingerprint=fingerprint)

    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_verify_connected_result",
        verify,
    )
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_load_receiver_authorities",
        lambda _root: authorities,
    )
    source_before = tree_state(source)
    result_before = tree_state(result)

    report = restore_connected_result(result, destination)

    assert verification_calls == [result.resolve(), result.resolve()]
    assert report.receipt_fingerprint == fingerprint
    assert report.source_commitment == authorities.inventory.source_commitment
    assert report.destination == destination.resolve()
    assert report.restored_file_count == 2
    assert report.restored_empty_directory_count == 1
    assert portable_tree(destination) == portable_tree(source)
    assert (destination / "drafts" / "note.md").read_bytes() == (
        source / "drafts" / "note.md"
    ).read_bytes()
    assert tree_state(source) == source_before
    assert tree_state(result) == result_before


def test_known_receiver_source_overlap_is_refused_before_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, authorities = _receiver_authorities(tmp_path)
    result = tmp_path / "received-result"
    destination = source / "must-not-exist"
    fingerprint = authorities.envelope.receipt_fingerprint
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_verify_connected_result",
        lambda _root: _Verification(
            status="verified",
            receipt_fingerprint=fingerprint,
        ),
    )
    source_before = tree_state(source)
    result_before = tree_state(result)

    with pytest.raises(FolderReconstructionError) as raised:
        restore_connected_result(
            result,
            destination,
            source_root=source,
        )

    assert raised.value.code == "destination_overlaps_source"
    assert not destination.exists()
    assert tree_state(source) == source_before
    assert tree_state(result) == result_before


@pytest.mark.parametrize("parent_kind", ["missing", "symlink", "not_writable"])
def test_invalid_unrelated_destination_parent_is_refused_before_copy(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    parent_kind: str,
) -> None:
    _source, authorities = _receiver_authorities(tmp_path)
    result = tmp_path / "received-result"
    destination_parent = tmp_path / "destination-parent"
    if parent_kind == "symlink":
        real_parent = tmp_path / "real-parent"
        real_parent.mkdir()
        destination_parent.symlink_to(real_parent, target_is_directory=True)
    elif parent_kind == "not_writable":
        destination_parent.mkdir()
        destination_parent.chmod(0o500)
    destination = destination_parent / "must-not-exist"
    fingerprint = authorities.envelope.receipt_fingerprint
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_verify_connected_result",
        lambda _root: _Verification(
            status="verified",
            receipt_fingerprint=fingerprint,
        ),
    )
    result_before = tree_state(result)

    try:
        with pytest.raises(FolderReconstructionError) as raised:
            restore_connected_result(result, destination)
    finally:
        if parent_kind == "not_writable":
            destination_parent.chmod(0o700)

    assert raised.value.code == "destination_parent_invalid"
    assert not destination.exists()
    assert tree_state(result) == result_before


def test_competing_reconstruction_destination_is_preserved_without_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, authorities = _receiver_authorities(tmp_path)
    result = tmp_path / "received-result"
    unrelated_parent = tmp_path / "unrelated-parent"
    unrelated_parent.mkdir()
    destination = unrelated_parent / "receiver-original-recreated"
    fingerprint = authorities.envelope.receipt_fingerprint
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_verify_connected_result",
        lambda _root: _Verification(
            status="verified",
            receipt_fingerprint=fingerprint,
        ),
    )
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_load_receiver_authorities",
        lambda _root: authorities,
    )

    def competing_promotion(_pending: Path, final: Path) -> None:
        final.mkdir()
        (final / "user-data.txt").write_bytes(b"preserve me\n")
        raise FileExistsError(final)

    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "promote_directory_no_replace",
        competing_promotion,
    )
    source_before = tree_state(source)
    result_before = tree_state(result)

    with pytest.raises(FolderReconstructionError) as raised:
        restore_connected_result(result, destination, source_root=source)

    assert raised.value.code == "promotion_failed"
    assert (destination / "user-data.txt").read_bytes() == b"preserve me\n"
    assert tuple(unrelated_parent.glob(f".{destination.name}.pending-*")) == ()
    assert tree_state(source) == source_before
    assert tree_state(result) == result_before


def test_blocks_before_parsing_or_writing_when_verification_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result = tmp_path / "received-result"
    result.mkdir()
    destination = tmp_path / "must-not-exist"
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_verify_connected_result",
        lambda _root: _Verification(
            status="blocked",
            receipt_fingerprint=None,
            failed_check_ids=("change_file_fingerprint_mismatch",),
        ),
    )

    with pytest.raises(FolderReconstructionError) as raised:
        restore_connected_result(result, destination)

    assert raised.value.code == "receipt_verification_blocked"
    assert raised.value.failed_check_ids == ("change_file_fingerprint_mismatch",)
    assert not destination.exists()


def test_receiver_authority_mismatch_fails_before_pending_destination(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _source, authorities = _receiver_authorities(tmp_path)
    result = tmp_path / "received-result"
    destination = tmp_path / "must-not-exist"
    fingerprint = authorities.envelope.receipt_fingerprint
    mismatched = authorities.accepted_plan.model_copy(
        update={"execution_authority": "gpt_plan"}
    )
    altered = _LoadedReceiverAuthorities(
        inventory_bytes=authorities.inventory_bytes,
        accepted_plan_bytes=authorities.accepted_plan_bytes,
        receipt_bytes=authorities.receipt_bytes,
        forward_bytes=authorities.forward_bytes,
        reverse_bytes=authorities.reverse_bytes,
        inventory=authorities.inventory,
        accepted_plan=mismatched,
        envelope=authorities.envelope,
        path_rows=authorities.path_rows,
    )
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_verify_connected_result",
        lambda _root: _Verification(
            status="verified",
            receipt_fingerprint=fingerprint,
        ),
    )
    monkeypatch.setattr(
        "name_atlas.folder_refactor.connected_change.reconstruction."
        "_load_receiver_authorities",
        lambda _root: altered,
    )

    with pytest.raises(FolderReconstructionError) as raised:
        restore_connected_result(result, destination)

    assert raised.value.code == "receipt_reparse_failed"
    assert not destination.exists()
