"""C1 application-boundary refusal and external-input tests."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
    tree_state,
)

import name_atlas.folder_refactor.connected_change.service as connected_change_service
from name_atlas.domain import PackageValidationResult
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CHANGE_FILE_BYTES,
    ConnectedChangeError,
    ConnectedChangeMember,
    connected_change_member_id,
)
from name_atlas.folder_refactor.connected_change.service import (
    apply_connected_change,
    create_connected_change_origin,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)
from name_atlas.verification.bagit_validator import BagItPackageValidator


@pytest.mark.parametrize(
    ("mutation", "expected_blocker"),
    [
        ("missing", "receiver_member_missing"),
        ("extra", "receiver_member_extra"),
        ("suffix", "receiver_suffix_mismatch"),
        ("empty_directory", "receiver_empty_directory_mismatch"),
    ],
)
def test_application_refuses_structural_receiver_mismatch_without_output(
    tmp_path: Path,
    mutation: str,
    expected_blocker: str,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    _mutate_receiver(fixture, mutation)
    receiver_before = tree_state(fixture.martin_root)
    change_file_before = _file_state(change_file)
    output = tmp_path / "receiver-output"
    output.mkdir()

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=change_file,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == expected_blocker
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before
    assert _file_state(change_file) == change_file_before


@pytest.mark.parametrize(
    ("input_kind", "expected_blocker"),
    [
        ("missing", "change_file_schema_invalid"),
        ("directory", "change_file_schema_invalid"),
        ("symlink", "change_file_schema_invalid"),
        ("oversize", "change_file_too_large"),
    ],
)
def test_external_change_file_path_blocks_before_receiver_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    input_kind: str,
    expected_blocker: str,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    candidate = tmp_path / "input.nameatlas-change.json"
    if input_kind == "directory":
        candidate.mkdir()
    elif input_kind == "symlink":
        target = tmp_path / "actual.nameatlas-change.json"
        target.write_bytes(b"{}")
        candidate.symlink_to(target)
    elif input_kind == "oversize":
        with candidate.open("wb") as stream:
            stream.truncate(MAX_CHANGE_FILE_BYTES + 1)
    elif input_kind != "missing":
        raise AssertionError(f"Unhandled input kind: {input_kind}")
    output = tmp_path / "receiver-output"
    output.mkdir()
    receiver_before = tree_state(fixture.martin_root)
    monkeypatch.setattr(
        connected_change_service,
        "scan_folder_with_references",
        _unexpected_receiver_scan,
    )

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=candidate,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == expected_blocker
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before


def test_noncanonical_change_file_blocks_before_receiver_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    noncanonical = tmp_path / "noncanonical.nameatlas-change.json"
    noncanonical.write_bytes(change_file.read_bytes() + b"\n")
    output = tmp_path / "receiver-output"
    output.mkdir()
    receiver_before = tree_state(fixture.martin_root)
    monkeypatch.setattr(
        connected_change_service,
        "scan_folder_with_references",
        _unexpected_receiver_scan,
    )

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=noncanonical,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == "change_file_schema_invalid"
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before


@pytest.mark.parametrize(
    "mutation",
    [
        "envelope_version",
        "core_version",
        "matching_rule_version",
        "unknown_envelope_field",
        "unknown_core_field",
        "unknown_member_field",
        "receipt_version",
        "unknown_receipt_field",
    ],
)
def test_strict_change_file_versions_and_nested_fields_block_before_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    raw = json.loads(change_file.read_bytes())
    _mutate_strict_contract(raw, mutation)
    invalid = tmp_path / f"{mutation}.nameatlas-change.json"
    invalid.write_bytes(_reissue_change_file(raw))
    output = tmp_path / "receiver-output"
    output.mkdir()
    receiver_before = tree_state(fixture.martin_root)
    monkeypatch.setattr(
        connected_change_service,
        "scan_folder_with_references",
        _unexpected_receiver_scan,
    )

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=invalid,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == "change_file_schema_invalid"
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before


def test_invalid_receiver_target_returns_stable_blocker_before_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    raw = json.loads(change_file.read_bytes())
    members = raw["core"]["members"]
    member = next(
        item
        for item in members
        if item["descriptor_kind"] == "ordinary" and not item["protected"]
    )
    old_id = member["logical_member_id"]
    member["target_relative_path"] = "result/renamed.invalid"
    member["logical_member_id"] = connected_change_member_id(
        ConnectedChangeMember.model_construct(**member)
    )
    for source in members:
        for slot in source["link_slots"]:
            if slot["target_logical_member_id"] == old_id:
                slot["target_logical_member_id"] = member["logical_member_id"]
    members.sort(key=lambda item: item["logical_member_id"])
    invalid = tmp_path / "invalid-target.nameatlas-change.json"
    invalid.write_bytes(_reissue_change_file(raw))
    output = tmp_path / "receiver-output"
    output.mkdir()
    receiver_before = tree_state(fixture.martin_root)
    monkeypatch.setattr(
        connected_change_service,
        "scan_folder_with_references",
        _unexpected_receiver_scan,
    )

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=invalid,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == "receiver_target_invalid"
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before


def test_late_change_file_change_blocks_and_cleans_pending_result(
    tmp_path: Path,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    original_change_bytes = change_file.read_bytes()
    receiver_before = tree_state(fixture.martin_root)
    output = tmp_path / "receiver-output"
    output.mkdir()
    validator = _MutatingPackageValidator(
        lambda _pending_root: change_file.write_bytes(original_change_bytes + b"\n")
    )

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=change_file,
            source_root=fixture.martin_root,
            output_parent=output,
            package_validator=validator,
        )

    assert raised.value.code == "change_file_changed"
    assert validator.call_count >= 2
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before
    assert change_file.read_bytes() == original_change_bytes + b"\n"


def test_late_organized_tree_change_returns_stable_blocker_and_cleans_pending(
    tmp_path: Path,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    receiver_before = tree_state(fixture.martin_root)
    change_file_before = _file_state(change_file)
    output = tmp_path / "receiver-output"
    output.mkdir()

    def mutate_staged_data(pending_root: Path) -> None:
        target = pending_root / "data" / "assets" / "cover.png"
        target.write_bytes(target.read_bytes() + b"changed")

    validator = _MutatingPackageValidator(mutate_staged_data)
    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=change_file,
            source_root=fixture.martin_root,
            output_parent=output,
            package_validator=validator,
        )

    assert raised.value.code == "organized_tree_commitment_mismatch"
    assert validator.call_count == 1
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before
    assert _file_state(change_file) == change_file_before


class _MutatingPackageValidator:
    def __init__(self, mutation: Callable[[Path], None]) -> None:
        self._mutation = mutation
        self.call_count = 0
        self._delegate = BagItPackageValidator()

    def validate(self, bag_root: Path) -> PackageValidationResult:
        result = self._delegate.validate(bag_root)
        self.call_count += 1
        if self.call_count == 1:
            self._mutation(bag_root)
        return result


def _create_origin_fixture(
    tmp_path: Path,
) -> tuple[ConnectedChangeFixture, Path]:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "origin-output"
    output.mkdir()
    result = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    return fixture, result.change_file_path


def _mutate_receiver(fixture: ConnectedChangeFixture, mutation: str) -> None:
    root = fixture.martin_root
    if mutation == "missing":
        (root / "incoming" / "cover-art.png").unlink()
    elif mutation == "extra":
        (root / "extra.bin").write_bytes(b"extra\n")
    elif mutation == "suffix":
        (root / "incoming" / "cover-art.png").rename(
            root / "incoming" / "cover-art.jpg"
        )
    elif mutation == "empty_directory":
        (root / "empty" / "keep").rmdir()
    else:
        raise AssertionError(f"Unhandled mutation: {mutation}")


def _mutate_strict_contract(raw: dict[str, Any], mutation: str) -> None:
    if mutation == "envelope_version":
        raw["schema_version"] = "connected-change-file.v2"
    elif mutation == "core_version":
        raw["core"]["schema_version"] = "connected-change-core.v2"
    elif mutation == "matching_rule_version":
        raw["core"]["matching_rule_version"] = "unknown-matcher.v1"
    elif mutation == "unknown_envelope_field":
        raw["unknown"] = True
    elif mutation == "unknown_core_field":
        raw["core"]["unknown"] = True
    elif mutation == "unknown_member_field":
        raw["core"]["members"][0]["unknown"] = True
    elif mutation == "receipt_version":
        raw["originating_receipt"]["receipt"]["schema_version"] = (
            "folder-change-receipt.v3"
        )
    elif mutation == "unknown_receipt_field":
        raw["originating_receipt"]["receipt"]["unknown"] = True
    else:
        raise AssertionError(f"Unhandled strict-contract mutation: {mutation}")


def _reissue_change_file(raw: dict[str, Any]) -> bytes:
    core_fingerprint = canonical_sha256(raw["core"])
    raw["core_fingerprint"] = core_fingerprint
    receipt = raw["originating_receipt"]["receipt"]
    receipt["connected_change_core_fingerprint"] = core_fingerprint
    raw["originating_receipt"]["receipt_fingerprint"] = canonical_sha256(receipt)
    raw["change_file_fingerprint"] = canonical_sha256(
        {key: value for key, value in raw.items() if key != "change_file_fingerprint"}
    )
    return canonical_json_bytes(raw)


def _file_state(path: Path) -> tuple[int, int, int, int, bytes]:
    metadata = path.lstat()
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        path.read_bytes(),
    )


def _unexpected_receiver_scan(*_args: object, **_kwargs: object) -> None:
    raise AssertionError("Receiver source scan occurred before Change File rejection.")
