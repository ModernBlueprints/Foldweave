"""Focused fixed-point receiver-matching tests for the C0 gate."""

from __future__ import annotations

from itertools import permutations
from pathlib import Path, PurePosixPath
from types import SimpleNamespace

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
    make_symmetric_fixture,
)

from name_atlas.folder_refactor.connected_change import (
    build_connected_change_core,
    build_receiver_descriptors,
    match_connected_change,
)
from name_atlas.folder_refactor.connected_change.contracts import ConnectedChangeCore
from name_atlas.folder_refactor.connected_change.matcher import _match_descriptors
from name_atlas.folder_refactor.contracts import (
    AcceptedFileMapping,
    FolderAcceptedPlan,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_links import (
    MARKDOWN_SUFFIXES,
    build_reference_graph,
)
from name_atlas.folder_refactor.serialization import request_fingerprint


def test_matcher_rebinds_duplicates_by_relationship_and_ignores_layout(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    core = _build_fixture_core(fixture.sofia_root, fixture.target_paths, fixture)
    inventory, graph, payloads = _receiver_inputs(fixture.martin_root)

    report = match_connected_change(
        core,
        inventory,
        graph,
        markdown_payloads=payloads,
    )

    assert report.status == "matched"
    assert report.blocker_code is None
    assert len(report.mappings) == 6
    paths_by_target = {
        mapping.target_relative_path: mapping.receiver_original_path
        for mapping in report.mappings
    }
    assert paths_by_target["deliverables/approved.txt"] == "originals/a-copy.txt"
    assert paths_by_target["research/supporting.txt"] == "originals/b-copy.txt"
    assert paths_by_target["assets/cover.png"] == "incoming/cover-art.png"


def test_matcher_is_sequence_order_invariant(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    core = _build_fixture_core(fixture.sofia_root, fixture.target_paths, fixture)
    inventory, graph, payloads = _receiver_inputs(fixture.martin_root)
    descriptors = build_receiver_descriptors(
        inventory,
        graph,
        markdown_payloads=payloads,
    )

    expected = _match_descriptors(
        core,
        descriptors,
        receiver_source_commitment=inventory.source_commitment,
        receiver_empty_directories=tuple(
            item.relative_path for item in inventory.empty_directories
        ),
    )
    permutation_count = 0
    for descriptor_order in permutations(descriptors):
        actual = _match_descriptors(
            core,
            descriptor_order,
            receiver_source_commitment=inventory.source_commitment,
            receiver_empty_directories=tuple(
                reversed(
                    tuple(item.relative_path for item in inventory.empty_directories)
                )
            ),
        )
        assert actual == expected
        permutation_count += 1

    assert permutation_count == 720


def test_matcher_blocks_symmetric_duplicate_group(tmp_path: Path) -> None:
    fixture = make_symmetric_fixture(tmp_path)
    origin_inventory = scan_folder(fixture.origin_root).inventory
    target_paths = {
        item.relative_path: f"organized/{item.relative_path}"
        for item in origin_inventory.files
    }
    fixture_contract = SimpleNamespace(
        request="Organize every file and preserve every supported link.",
        result_name="organized-copy",
    )
    core = _build_fixture_core(
        fixture.origin_root,
        target_paths,
        fixture_contract,
    )
    inventory, graph, payloads = _receiver_inputs(fixture.receiver_root)

    report = match_connected_change(
        core,
        inventory,
        graph,
        markdown_payloads=payloads,
    )
    assert report.status == "blocked"
    assert report.blocker_code == "receiver_ambiguous_duplicate_group"
    assert report.mappings == ()


@pytest.mark.parametrize(
    ("mutation", "expected_blocker"),
    [
        ("missing", "receiver_member_missing"),
        ("extra", "receiver_member_extra"),
        ("payload", "receiver_payload_changed"),
        ("markdown", "receiver_markdown_content_changed"),
        ("relationship", "receiver_relationship_changed"),
        ("suffix", "receiver_suffix_mismatch"),
        ("protected", "receiver_protected_member_mismatch"),
        ("empty_directory", "receiver_empty_directory_mismatch"),
    ],
)
def test_matcher_returns_exact_change_blocker(
    tmp_path: Path,
    mutation: str,
    expected_blocker: str,
) -> None:
    fixture = make_connected_change_fixture(tmp_path)
    core = _build_fixture_core(fixture.sofia_root, fixture.target_paths, fixture)
    _mutate_receiver(fixture, mutation)
    inventory, graph, payloads = _receiver_inputs(fixture.martin_root)

    report = match_connected_change(
        core,
        inventory,
        graph,
        markdown_payloads=payloads,
    )
    assert report.status == "blocked"
    assert report.blocker_code == expected_blocker


def _receiver_inputs(root: Path):  # type: ignore[no-untyped-def]
    inventory = scan_folder(root).inventory
    payloads = _markdown_payloads(root, inventory.files)
    return inventory, build_reference_graph(inventory, payloads), payloads


def _markdown_payloads(root: Path, files) -> dict[str, bytes]:  # type: ignore[no-untyped-def]
    return {
        item.relative_path: (root / item.relative_path).read_bytes()
        for item in files
        if PurePosixPath(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
    }


def _build_fixture_core(
    source_root: Path,
    target_paths: dict[str, str],
    fixture,
) -> ConnectedChangeCore:  # type: ignore[no-untyped-def]
    inventory = scan_folder(source_root).inventory
    payloads = _markdown_payloads(source_root, inventory.files)
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
    return build_connected_change_core(
        inventory,
        graph,
        accepted,
        request=fixture.request,
        markdown_payloads=payloads,
        expected_organized_tree_commitment="f" * 64,
        origin_proof_identifiers=("test-origin-proof",),
    )


def _mutate_receiver(fixture: ConnectedChangeFixture, mutation: str) -> None:
    root = fixture.martin_root
    if mutation == "missing":
        (root / "incoming/cover-art.png").unlink()
    elif mutation == "extra":
        (root / "extra.bin").write_bytes(b"extra\n")
    elif mutation == "payload":
        (root / "originals/a-copy.txt").write_bytes(b"changed presentation\n")
    elif mutation == "markdown":
        (root / "working/research.md").write_bytes(
            b"Changed prose: [document](../originals/b-copy.txt#draft)\r\n"
        )
    elif mutation == "relationship":
        (root / "working/research.md").write_bytes(
            b"Research item: [document](../originals/a-copy.txt#draft)\r\n"
        )
    elif mutation == "suffix":
        (root / "incoming/cover-art.png").rename(root / "incoming/cover-art.jpg")
    elif mutation == "protected":
        (root / ".env.local").write_bytes(b"DEMO_MODE=changed\n")
    elif mutation == "empty_directory":
        (root / "empty" / "keep").rmdir()
    else:
        raise AssertionError(f"Unhandled mutation: {mutation}")
