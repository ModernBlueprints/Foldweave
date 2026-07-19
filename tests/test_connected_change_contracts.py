"""Focused contract tests for payload-free Connected Change files."""

from __future__ import annotations

import json
from pathlib import Path, PurePosixPath

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
)
from pydantic import ValidationError

from name_atlas.folder_refactor.connected_change import (
    CapsuleAppliedExecutionOrigin,
    ConnectedChangeError,
    create_connected_change_file,
    parse_connected_change_file,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CHANGE_FILE_BYTES,
    ConnectedChangeCore,
    connected_change_core_fingerprint,
)
from name_atlas.folder_refactor.connected_change.service import (
    create_connected_change_origin,
)
from name_atlas.folder_refactor.contracts import (
    AcceptedFileMapping,
    FolderAcceptedPlan,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_links import (
    MARKDOWN_SUFFIXES,
    build_reference_graph,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)


def test_change_file_is_payload_free_strict_and_fingerprint_bound(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    output = tmp_path / "results"
    output.mkdir()
    result = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    payload = result.change_file_path.read_bytes()
    change_file = parse_connected_change_file(payload)

    assert parse_connected_change_file(payload) == change_file
    assert str(fixture.sofia_root).encode() not in payload
    assert b"shared presentation bytes" not in payload
    assert b"DEMO_MODE=northstar" not in payload
    assert change_file.core_fingerprint == canonical_sha256(change_file.core)

    tampered = json.loads(payload)
    tampered["core"]["request"] += " changed"
    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file(
            json.dumps(tampered, separators=(",", ":")).encode()
        )
    assert error.value.code == "change_file_fingerprint_mismatch"


def test_change_file_builder_rejects_minimal_self_hashed_fake_receipt(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    core = _build_fixture_core(fixture.sofia_root, fixture.target_paths, fixture)
    receipt_core = {
        "schema_version": "not-a-folder-change-receipt.v2",
        "connected_change_core_fingerprint": connected_change_core_fingerprint(core),
    }

    with pytest.raises(ConnectedChangeError) as error:
        create_connected_change_file(
            core,
            originating_receipt={
                "receipt": receipt_core,
                "receipt_fingerprint": canonical_sha256(receipt_core),
            },
        )

    assert error.value.code == "change_file_schema_invalid"


@pytest.mark.parametrize(
    "payload",
    [
        b'{"schema_version":"connected-change-file.v1",'
        b'"schema_version":"connected-change-file.v1"}',
        b'{"value":NaN}',
        b"[]",
        b"\xff",
    ],
)
def test_change_file_parser_rejects_non_strict_json(payload: bytes) -> None:
    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file(payload)
    assert error.value.code == "change_file_schema_invalid"


def test_change_file_parser_enforces_raw_16_mib_limit() -> None:
    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file(b" " * (MAX_CHANGE_FILE_BYTES + 1))
    assert error.value.code == "change_file_too_large"


@pytest.mark.parametrize(
    "mutation",
    ("result_folder", "member_target", "empty_directory_target"),
)
def test_change_file_parser_classifies_invalid_receiver_targets(
    tmp_path: Path,
    mutation: str,
) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    output = tmp_path / "results"
    output.mkdir()
    result = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    raw = json.loads(result.change_file_path.read_bytes())
    if mutation == "result_folder":
        raw["core"]["requested_result_folder_name"] = "../unsafe"
    elif mutation == "member_target":
        raw["core"]["members"][1]["target_relative_path"] = "../unsafe.txt"
    else:
        raw["core"]["empty_directory_requirements"][0] = "../unsafe"

    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file(_rehash_change_file(raw))

    assert error.value.code == "receiver_target_invalid"


def test_change_file_parser_keeps_other_schema_failures_distinct(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    output = tmp_path / "results"
    output.mkdir()
    result = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    raw = json.loads(result.change_file_path.read_bytes())
    raw["core"]["request"] = f" {raw['core']['request']} "
    raw["core"]["request_fingerprint"] = request_fingerprint(raw["core"]["request"])

    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file(_rehash_change_file(raw))

    assert error.value.code == "change_file_schema_invalid"


def test_capsule_execution_origin_is_mechanically_provider_free() -> None:
    digest = "a" * 64
    origin = CapsuleAppliedExecutionOrigin(
        change_file_fingerprint=digest,
        originating_receipt_fingerprint=digest,
        match_report_fingerprint=digest,
        receiver_accepted_plan_fingerprint=digest,
    )
    assert origin.provider_call_count == 0
    assert origin.api_used is False
    assert origin.external_network_used is False
    with pytest.raises(ValidationError):
        CapsuleAppliedExecutionOrigin(
            change_file_fingerprint=digest,
            originating_receipt_fingerprint=digest,
            match_report_fingerprint=digest,
            receiver_accepted_plan_fingerprint=digest,
            model_alias="gpt-5.6",
        )


def _build_fixture_core(
    source_root: Path,
    target_paths: dict[str, str],
    fixture: ConnectedChangeFixture,
) -> ConnectedChangeCore:
    inventory = scan_folder(source_root).inventory
    payloads = {
        item.relative_path: (source_root / item.relative_path).read_bytes()
        for item in inventory.files
        if PurePosixPath(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
    }
    graph = build_reference_graph(inventory, payloads)
    accepted = FolderAcceptedPlan(
        source_commitment=inventory.source_commitment,
        request_fingerprint=request_fingerprint(fixture.request),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="e" * 64,
        result_folder_name=fixture.result_name,
        file_mappings=tuple(
            AcceptedFileMapping(
                file_id=item.file_id,
                original_path=item.relative_path,
                target_path=target_paths[item.relative_path],
                protected=item.protected,
                planner_supplied=not item.protected,
            )
            for item in inventory.files
        ),
        empty_directories=tuple(
            item.relative_path for item in inventory.empty_directories
        ),
    )
    from name_atlas.folder_refactor.connected_change import (
        build_connected_change_core,
    )

    return build_connected_change_core(
        inventory,
        graph,
        accepted,
        request=fixture.request,
        markdown_payloads=payloads,
        expected_organized_tree_commitment="f" * 64,
        origin_proof_identifiers=("test-origin-proof",),
    )


def _rehash_change_file(raw: dict[str, object]) -> bytes:
    raw["core_fingerprint"] = canonical_sha256(raw["core"])
    raw["change_file_fingerprint"] = canonical_sha256(
        {key: value for key, value in raw.items() if key != "change_file_fingerprint"}
    )
    return canonical_json_bytes(raw)
