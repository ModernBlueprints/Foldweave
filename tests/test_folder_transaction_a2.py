"""Integrated A2 copy transaction with deterministic Markdown preservation."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

import name_atlas.folder_refactor.transaction as transaction_module
from name_atlas.folder_refactor.compiler import compile_plan
from name_atlas.folder_refactor.contracts import (
    AcceptedFileMapping,
    FolderAcceptedPlan,
    FolderPlan,
    FolderPlanEntry,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.markdown_links import build_reference_graph
from name_atlas.folder_refactor.serialization import request_fingerprint
from name_atlas.folder_refactor.transaction import (
    FolderTransactionError,
    FolderTransactionPaths,
    execute_accepted_folder_plan,
)
from name_atlas.verification import BagItPackageValidator
from name_atlas.verification.bag_writer import BagItWriter

REQUEST = "Move the note and report into a clear handoff folder."


def _digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def test_moved_note_and_target_keep_the_same_supported_link(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    markdown = b"Briefing: [approved report](<reports/apollo final.txt#summary>)\r\n"
    (source / "reports").mkdir()
    (source / "brief.md").write_bytes(markdown)
    (source / "reports" / "apollo final.txt").write_bytes(b"approved\n")
    before = {
        path.relative_to(source).as_posix(): (path.stat().st_ino, path.read_bytes())
        for path in source.rglob("*")
        if path.is_file()
    }
    scan = scan_folder(source)
    graph = build_reference_graph(
        scan.inventory,
        {"brief.md": markdown},
    )
    targets = {
        "brief.md": "handoff/overview.md",
        "reports/apollo final.txt": "handoff/final report.txt",
    }
    plan = FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="a" * 64,
        result_folder_name="northstar-handoff",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=targets[item.relative_path],
                rationale="Creates the requested clear handoff structure.",
                evidence_ids=("initial_inventory",),
            )
            for item in scan.inventory.files
        ),
        exclusions=(),
    )
    accepted = compile_plan(
        scan.inventory,
        REQUEST,
        plan,
        known_evidence_ids={"initial_inventory"},
        evidence_fingerprint="a" * 64,
        reference_graph=graph,
    )

    result = execute_accepted_folder_plan(
        initial_scan=scan,
        output_parent=output,
        request=REQUEST,
        accepted_plan=accepted,
        reference_graph=graph,
        bag_writer=BagItWriter(),
        package_validator=BagItPackageValidator(),
        transaction_paths=FolderTransactionPaths(
            job_id="123e4567e89b42d3a456426614174000",
            pending_root=(
                output / ".name-atlas-123e4567e89b42d3a456426614174000.pending"
            ),
            final_root=output / "northstar-handoff",
        ),
    )

    staged_note = result.data_root / "handoff" / "overview.md"
    staged_target = result.data_root / "handoff" / "final report.txt"
    assert staged_note.read_bytes() == (
        b"Briefing: [approved report](<final%20report.txt#summary>)\r\n"
    )
    assert staged_target.read_bytes() == b"approved\n"
    reference = result.reference_graph.references[0]
    assert reference.target_file_id == next(
        item.file_id
        for item in scan.inventory.files
        if item.relative_path == "reports/apollo final.txt"
    )
    assert reference.proposed_destination == "final%20report.txt#summary"
    assert reference.verification_status == "rewritten"

    original_copy = (
        result.result_root
        / "name-atlas"
        / "original-content"
        / f"{reference.source_file_id}.bin"
    )
    assert original_copy.read_bytes() == markdown
    assert _digest(original_copy) == next(
        item.sha256
        for item in scan.inventory.files
        if item.file_id == reference.source_file_id
    )
    portable_graph = FolderReferenceGraph.model_validate_json(
        (result.result_root / "name-atlas" / "reference_graph.json").read_bytes(),
        strict=True,
    )
    assert portable_graph == result.reference_graph
    assert result.report.supported_link_count == 1
    assert result.report.rewritten_link_count == 1
    assert result.report.rewritten_markdown_file_count == 1
    checks = {check.check_id: check.passed for check in result.report.checks}
    assert checks["supported_markdown_links_resolve"] is True
    assert BagItPackageValidator().validate(result.result_root).valid is True

    after = {
        path.relative_to(source).as_posix(): (path.stat().st_ino, path.read_bytes())
        for path in source.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_one_note_can_contain_unchanged_and_rewritten_links(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    (source / "sub").mkdir(parents=True)
    output.mkdir()
    markdown = b"[a](a.txt) [b](sub/b.txt)\n"
    (source / "notes.md").write_bytes(markdown)
    (source / "a.txt").write_bytes(b"a")
    (source / "sub" / "b.txt").write_bytes(b"b")
    scan = scan_folder(source)
    graph = build_reference_graph(scan.inventory, {"notes.md": markdown})
    targets = {
        "a.txt": "docs/a.txt",
        "notes.md": "docs/notes.md",
        "sub/b.txt": "docs/b-final.txt",
    }
    plan = FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="a" * 64,
        result_folder_name="mixed-links",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=targets[item.relative_path],
                rationale="Preserve one relationship and update the other.",
                evidence_ids=("initial_inventory",),
            )
            for item in scan.inventory.files
        ),
        exclusions=(),
    )
    accepted = compile_plan(
        scan.inventory,
        REQUEST,
        plan,
        known_evidence_ids={"initial_inventory"},
        evidence_fingerprint="a" * 64,
        reference_graph=graph,
    )

    result = execute_accepted_folder_plan(
        initial_scan=scan,
        output_parent=output,
        request=REQUEST,
        accepted_plan=accepted,
        reference_graph=graph,
        bag_writer=BagItWriter(),
        package_validator=BagItPackageValidator(),
    )

    assert (result.data_root / "docs" / "notes.md").read_bytes() == (
        b"[a](a.txt) [b](b-final.txt)\n"
    )
    assert [item.verification_status for item in result.reference_graph.references] == [
        "unchanged",
        "rewritten",
    ]


@pytest.mark.parametrize("retained_reference_count", [0, 1])
def test_incomplete_reference_graph_cannot_promote(
    tmp_path: Path,
    retained_reference_count: int,
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    markdown = b"[one](one.txt) [two](two.txt)\n"
    (source / "notes.md").write_bytes(markdown)
    (source / "one.txt").write_bytes(b"one")
    (source / "two.txt").write_bytes(b"two")
    scan = scan_folder(source)
    complete_graph = build_reference_graph(
        scan.inventory,
        {"notes.md": markdown},
    )
    incomplete_graph = FolderReferenceGraph(
        source_commitment=complete_graph.source_commitment,
        references=complete_graph.references[:retained_reference_count],
        ignored=complete_graph.ignored,
    )
    plan = FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="a" * 64,
        result_folder_name="incomplete-graph",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=f"handoff/{item.relative_path}",
                rationale="Move the complete project together.",
                evidence_ids=("initial_inventory",),
            )
            for item in scan.inventory.files
        ),
        exclusions=(),
    )
    accepted = compile_plan(
        scan.inventory,
        REQUEST,
        plan,
        known_evidence_ids={"initial_inventory"},
        evidence_fingerprint="a" * 64,
        reference_graph=complete_graph,
    )

    with pytest.raises(
        FolderTransactionError,
        match="reference graph is incomplete",
    ):
        execute_accepted_folder_plan(
            initial_scan=scan,
            output_parent=output,
            request=REQUEST,
            accepted_plan=accepted,
            reference_graph=incomplete_graph,
            bag_writer=BagItWriter(),
            package_validator=BagItPackageValidator(),
        )

    assert not (output / "incomplete-graph").exists()


def test_corrupt_rewrite_is_blocked_before_promotion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    markdown = b"[target](target.txt)\n"
    (source / "notes.md").write_bytes(markdown)
    (source / "target.txt").write_bytes(b"target")
    scan = scan_folder(source)
    graph = build_reference_graph(scan.inventory, {"notes.md": markdown})
    plan = FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="a" * 64,
        result_folder_name="corrupt-rewrite",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=(
                    "moved/docs/notes.md"
                    if item.relative_path == "notes.md"
                    else "moved/docs/assets/target.txt"
                ),
                rationale="Move both files.",
                evidence_ids=("initial_inventory",),
            )
            for item in scan.inventory.files
        ),
        exclusions=(),
    )
    accepted = compile_plan(
        scan.inventory,
        REQUEST,
        plan,
        known_evidence_ids={"initial_inventory"},
        evidence_fingerprint="a" * 64,
        reference_graph=graph,
    )

    def corrupt_writer(**kwargs):
        destination = kwargs["destination"]
        destination.write_bytes(b"[target](missing.txt)\n")
        return 22, "0" * 64

    monkeypatch.setattr(
        transaction_module,
        "_copy_rewritten_markdown",
        corrupt_writer,
    )
    with pytest.raises(
        FolderTransactionError,
        match="exact-span reapplication",
    ):
        execute_accepted_folder_plan(
            initial_scan=scan,
            output_parent=output,
            request=REQUEST,
            accepted_plan=accepted,
            reference_graph=graph,
            bag_writer=BagItWriter(),
            package_validator=BagItPackageValidator(),
        )
    assert not (output / "corrupt-rewrite").exists()


def test_execution_rebinds_protected_flags_to_inventory(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    (source / ".env.local").write_bytes(b"secret")
    (source / "notes.txt").write_bytes(b"notes")
    scan = scan_folder(source)
    by_path = {item.relative_path: item for item in scan.inventory.files}
    graph = build_reference_graph(scan.inventory, {})
    forged = FolderAcceptedPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="a" * 64,
        result_folder_name="forged-protection",
        file_mappings=(
            AcceptedFileMapping(
                file_id=by_path[".env.local"].file_id,
                original_path=".env.local",
                target_path="config/env.local",
                protected=False,
                planner_supplied=True,
            ),
            AcceptedFileMapping(
                file_id=by_path["notes.txt"].file_id,
                original_path="notes.txt",
                target_path="notes.txt",
                protected=False,
                planner_supplied=True,
            ),
        ),
        empty_directories=(),
    )

    with pytest.raises(FolderTransactionError, match="does not match the source"):
        execute_accepted_folder_plan(
            initial_scan=scan,
            output_parent=output,
            request=REQUEST,
            accepted_plan=forged,
            reference_graph=graph,
            bag_writer=BagItWriter(),
            package_validator=BagItPackageValidator(),
        )
