"""Release-contract checks for the packaged C3 project fixtures."""

from __future__ import annotations

import hashlib
import wave
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import pytest

from name_atlas.folder_refactor.compiler import compile_plan
from name_atlas.folder_refactor.connected_change.descriptors import (
    build_connected_change_core,
)
from name_atlas.folder_refactor.connected_change.matcher import (
    match_connected_change,
)
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.demo_fixtures import (
    AMBIGUITY_ANSWER,
    AMBIGUITY_REQUEST,
    AMBIGUITY_TARGET_PATH_PAIRS,
    HERO_EMPTY_DIRECTORY,
    HERO_FILE_COUNT,
    HERO_LOGICAL_MEMBERS,
    HERO_MARKDOWN_FILE_COUNT,
    HERO_REQUEST,
    HERO_SUPPORTED_LINK_COUNT,
    ambiguity_target_paths,
    hero_correspondence,
    hero_target_paths,
    materialize_ambiguity_fixture,
    materialize_hero_fixture,
    packaged_fixture_templates,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_contracts import (
    FolderReferenceGraph,
    MarkdownReference,
)
from name_atlas.folder_refactor.markdown_links import (
    build_reference_graph,
    derive_reference_rewrites,
)
from name_atlas.folder_refactor.planner_evidence import (
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.serialization import request_fingerprint

MARKDOWN_SUFFIXES = frozenset({".md", ".markdown"})


def _reference_graph(root: Path) -> FolderReferenceGraph:
    scan = scan_folder(root)
    return build_reference_graph(
        scan.inventory,
        {
            item.relative_path: (root / item.relative_path).read_bytes()
            for item in scan.inventory.files
            if Path(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
        },
    )


def _outside_destination_bytes(
    payload: bytes,
    references: list[MarkdownReference],
) -> bytes:
    chunks: list[bytes] = []
    cursor = 0
    for reference in references:
        chunks.append(payload[cursor : reference.destination_start_byte])
        chunks.append(b"<supported-destination>")
        cursor = reference.destination_end_byte
    chunks.append(payload[cursor:])
    return b"".join(chunks)


def _references_by_source(
    graph: FolderReferenceGraph,
) -> dict[str, list[MarkdownReference]]:
    result: dict[str, list[MarkdownReference]] = defaultdict(list)
    for reference in graph.references:
        result[reference.source_path].append(reference)
    return result


def test_packaged_hero_has_exact_complete_file_and_link_surface() -> None:
    fixtures = packaged_fixture_templates()
    correspondence = hero_correspondence()
    expected_sofia_paths = {member.sofia_path for member in HERO_LOGICAL_MEMBERS}
    expected_martin_paths = {member.martin_path for member in HERO_LOGICAL_MEMBERS}

    sofia_scan = scan_folder(fixtures.sofia_root)
    martin_scan = scan_folder(fixtures.martin_root)
    sofia_paths = {item.relative_path for item in sofia_scan.inventory.files}
    martin_paths = {item.relative_path for item in martin_scan.inventory.files}
    sofia_graph = _reference_graph(fixtures.sofia_root)
    martin_graph = _reference_graph(fixtures.martin_root)

    assert len(HERO_LOGICAL_MEMBERS) == HERO_FILE_COUNT == 24
    assert sofia_paths == expected_sofia_paths
    assert martin_paths == expected_martin_paths
    assert len(sofia_scan.inventory.files) == HERO_FILE_COUNT
    assert len(martin_scan.inventory.files) == HERO_FILE_COUNT
    assert sum(path.endswith(".md") for path in sofia_paths) == (
        HERO_MARKDOWN_FILE_COUNT
    )
    assert sum(path.endswith(".md") for path in martin_paths) == (
        HERO_MARKDOWN_FILE_COUNT
    )
    assert len(sofia_graph.references) == HERO_SUPPORTED_LINK_COUNT == 23
    assert len(martin_graph.references) == HERO_SUPPORTED_LINK_COUNT
    assert sofia_graph.ignored.total == martin_graph.ignored.total == 0
    assert Counter(ref.target_path for ref in sofia_graph.references) == Counter(
        expected_sofia_paths - {".env.example"}
    )
    assert Counter(ref.target_path for ref in martin_graph.references) == Counter(
        expected_martin_paths - {".env.example"}
    )
    assert set(correspondence) == expected_sofia_paths
    assert set(correspondence.values()) == expected_martin_paths
    assert sofia_scan.inventory.source_commitment != (
        martin_scan.inventory.source_commitment
    )


def test_hero_layouts_preserve_payloads_and_markdown_relationships() -> None:
    fixtures = packaged_fixture_templates()
    correspondence = hero_correspondence()
    sofia_graph = _reference_graph(fixtures.sofia_root)
    martin_graph = _reference_graph(fixtures.martin_root)
    sofia_by_source = _references_by_source(sofia_graph)
    martin_by_source = _references_by_source(martin_graph)

    for member in HERO_LOGICAL_MEMBERS:
        sofia_bytes = (fixtures.sofia_root / member.sofia_path).read_bytes()
        martin_bytes = (fixtures.martin_root / member.martin_path).read_bytes()
        if Path(member.sofia_path).suffix.casefold() not in MARKDOWN_SUFFIXES:
            assert sofia_bytes == martin_bytes
            continue

        sofia_refs = sofia_by_source[member.sofia_path]
        martin_refs = martin_by_source[member.martin_path]
        assert _outside_destination_bytes(sofia_bytes, sofia_refs) == (
            _outside_destination_bytes(martin_bytes, martin_refs)
        )
        assert [
            (
                correspondence[reference.target_path],
                reference.fragment,
                reference.destination_style,
                reference.is_image,
            )
            for reference in sofia_refs
        ] == [
            (
                reference.target_path,
                reference.fragment,
                reference.destination_style,
                reference.is_image,
            )
            for reference in martin_refs
        ]


def test_materialized_hero_adds_one_real_empty_directory_and_protected_member(
    tmp_path: Path,
) -> None:
    fixture = materialize_hero_fixture(tmp_path / "hero")

    for root in (fixture.sofia_root, fixture.martin_root):
        scan = scan_folder(root)
        assert len(scan.inventory.files) == HERO_FILE_COUNT
        assert [item.relative_path for item in scan.inventory.empty_directories] == [
            HERO_EMPTY_DIRECTORY
        ]
        protected = [item for item in scan.inventory.files if item.protected]
        assert [item.relative_path for item in protected] == [".env.example"]
        assert protected[0].evidence_eligible is False
    assert fixture.request == HERO_REQUEST
    assert not any(
        path.name in {"manifest.json", ".gitkeep"} for path in fixture.root.rglob("*")
    )


def test_fixture_materializers_refuse_existing_destinations(tmp_path: Path) -> None:
    occupied = tmp_path / "occupied"
    occupied.mkdir()

    with pytest.raises(FileExistsError, match="already exists"):
        materialize_hero_fixture(occupied)
    with pytest.raises(FileExistsError, match="already exists"):
        materialize_ambiguity_fixture(occupied)


def test_binary_examples_are_valid_and_corresponding_payloads_are_unique() -> None:
    fixtures = packaged_fixture_templates()
    by_sofia_path = {member.sofia_path: member for member in HERO_LOGICAL_MEMBERS}
    payload_digests: list[str] = []
    for member in HERO_LOGICAL_MEMBERS:
        if member.sofia_path.endswith(".md"):
            continue
        payload = (fixtures.sofia_root / member.sofia_path).read_bytes()
        payload_digests.append(hashlib.sha256(payload).hexdigest())
    assert len(payload_digests) == len(set(payload_digests))

    assert (
        (fixtures.sofia_root / "working/design/Apollo-cover-draft.png")
        .read_bytes()
        .startswith(b"\x89PNG\r\n\x1a\n")
    )
    jpeg = (fixtures.sofia_root / "working/design/Apollo-layout-draft.jpg").read_bytes()
    assert jpeg.startswith(b"\xff\xd8\xff") and jpeg.endswith(b"\xff\xd9")
    with wave.open(
        str(fixtures.sofia_root / "working/audio/Apollo-narration-draft.wav"),
        "rb",
    ) as audio:
        assert audio.getnchannels() == 1
        assert audio.getframerate() == 8_000
        assert audio.getnframes() > 0
    mp3 = (
        fixtures.sofia_root / "working/audio/Apollo-interview-excerpt.mp3"
    ).read_bytes()
    assert mp3[0] == 0xFF and mp3[1] & 0xE0 == 0xE0
    pdf = (fixtures.sofia_root / "approved/Apollo-final-report.pdf").read_bytes()
    assert pdf.startswith(b"%PDF-1.4") and pdf.rstrip().endswith(b"%%EOF")
    with zipfile.ZipFile(
        fixtures.sofia_root / "working/data/Apollo-timeline-working.xlsx"
    ) as workbook:
        assert set(workbook.namelist()) == {
            "[Content_Types].xml",
            "_rels/.rels",
            "xl/_rels/workbook.xml.rels",
            "xl/workbook.xml",
            "xl/worksheets/sheet1.xml",
        }
        assert workbook.testzip() is None
    opaque = (
        fixtures.sofia_root / "working/cache/Apollo-layout-cache.bin"
    ).read_bytes()
    assert b"\x00" in opaque and opaque.endswith(b"\xff")
    assert by_sofia_path[".env.example"].target_path == ".env.example"


def test_ambiguity_fixture_genuinely_requires_one_missing_intent_answer(
    tmp_path: Path,
) -> None:
    fixture = materialize_ambiguity_fixture(tmp_path / "ambiguity")
    scan = scan_folder(fixture.source_root)
    graph = _reference_graph(fixture.source_root)
    approval = (fixture.source_root / "notes/client-approval.md").read_text(
        encoding="utf-8"
    )
    internal = (fixture.source_root / "notes/internal-review.md").read_text(
        encoding="utf-8"
    )
    candidates = sorted((fixture.source_root / "presentations").glob("*.pdf"))

    assert len(scan.inventory.files) == 4
    assert len(graph.references) == 4
    assert "do not record which candidate was approved" in approval
    assert "do not record which candidate is the internal version" in internal
    assert len(candidates) == 2
    assert candidates[0].read_bytes() != candidates[1].read_bytes()
    assert fixture.request == AMBIGUITY_REQUEST
    assert fixture.answer == AMBIGUITY_ANSWER
    assert ambiguity_target_paths() == dict(AMBIGUITY_TARGET_PATH_PAIRS)
    assert set(ambiguity_target_paths()) == {
        item.relative_path for item in scan.inventory.files
    }


def test_hero_target_plan_is_complete_suffix_preserving_and_cross_platform_safe() -> (
    None
):
    fixtures = packaged_fixture_templates()
    targets = hero_target_paths()
    scan = scan_folder(fixtures.sofia_root)

    assert set(targets) == {item.relative_path for item in scan.inventory.files}
    assert len(targets) == len(set(targets.values())) == HERO_FILE_COUNT
    assert sum(source != target for source, target in targets.items()) == 23
    for source, target in targets.items():
        assert Path(source).suffix == Path(target).suffix
        assert not target.startswith("/")
        assert "\\" not in target
        assert all(part not in {"", ".", ".."} for part in target.split("/"))


def test_hero_target_plan_compiles_and_rewrites_all_supported_links(
    tmp_path: Path,
) -> None:
    fixture = materialize_hero_fixture(tmp_path / "compile-hero")
    scan = scan_folder(fixture.sofia_root)
    graph = _reference_graph(fixture.sofia_root)
    evidence = create_initial_evidence_ledger(scan.inventory, fixture.request)
    targets = hero_target_paths()
    plan = FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(fixture.request),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=evidence.evidence_fingerprint,
        result_folder_name=fixture.result_folder_name,
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=targets[item.relative_path],
                rationale="Expected target for the packaged release fixture.",
                evidence_ids=("initial_inventory",),
            )
            for item in scan.inventory.files
            if not item.protected
        ),
        exclusions=(),
    )

    accepted = compile_plan(
        scan.inventory,
        fixture.request,
        plan,
        known_evidence_ids={"initial_inventory"},
        evidence_fingerprint=evidence.evidence_fingerprint,
        reference_graph=graph,
    )
    rewritten = derive_reference_rewrites(graph, accepted)

    assert {
        item.original_path: item.target_path for item in accepted.file_mappings
    } == (targets)
    assert accepted.empty_directories == (HERO_EMPTY_DIRECTORY,)
    assert len(rewritten.references) == HERO_SUPPORTED_LINK_COUNT
    assert all(item.verification_status == "rewritten" for item in rewritten.references)

    martin_scan = scan_folder(fixture.martin_root)
    martin_graph = _reference_graph(fixture.martin_root)
    core = build_connected_change_core(
        scan.inventory,
        graph,
        accepted,
        request=fixture.request,
        markdown_payloads={
            item.relative_path: (fixture.sofia_root / item.relative_path).read_bytes()
            for item in scan.inventory.files
            if Path(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
        },
        expected_organized_tree_commitment="0" * 64,
    )
    report = match_connected_change(
        core,
        martin_scan.inventory,
        martin_graph,
        markdown_payloads={
            item.relative_path: (fixture.martin_root / item.relative_path).read_bytes()
            for item in martin_scan.inventory.files
            if Path(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
        },
    )

    assert report.status == "matched"
    assert len(report.mappings) == HERO_FILE_COUNT
    assert report.blocker_code is None
