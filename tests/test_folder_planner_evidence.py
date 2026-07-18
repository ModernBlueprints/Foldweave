"""Focused safety and accounting tests for bounded folder evidence."""

from __future__ import annotations

from pathlib import Path

from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_links import build_reference_graph
from name_atlas.folder_refactor.planner_contracts import (
    MAX_EVIDENCE_RESULT_BYTES,
    InspectMarkdownLinksCall,
    ListInventoryPageCall,
    ReadTextExcerptCall,
)
from name_atlas.folder_refactor.planner_evidence import (
    LocalFolderEvidenceService,
    append_evidence_execution,
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.serialization import canonical_json_bytes


def _service(root: Path) -> tuple[LocalFolderEvidenceService, object]:
    scan = scan_folder(root)
    markdown = {
        item.relative_path: (root / item.relative_path).read_bytes()
        for item in scan.inventory.files
        if Path(item.relative_path).suffix.casefold() in {".md", ".markdown"}
    }
    graph = build_reference_graph(scan.inventory, markdown)
    return LocalFolderEvidenceService(scan, reference_graph=graph), scan


def test_protected_content_is_denied_without_leaking_bytes(tmp_path: Path) -> None:
    root = tmp_path / "source"
    root.mkdir()
    secret = "DO_NOT_EXPOSE_secret-sentinel"
    (root / ".env.local").write_text(secret, encoding="utf-8")
    (root / "notes.txt").write_text("ordinary", encoding="utf-8")
    service, scan = _service(root)
    protected = next(item for item in scan.inventory.files if item.protected)

    result = service.execute(
        ReadTextExcerptCall(
            call_id="protected",
            file_id=protected.file_id,
            start_byte=0,
            max_bytes=100,
        )
    )

    assert result.status == "rejected"
    assert result.error_code == "protected_content_denied"
    assert result.result is None
    assert secret not in repr(result)


def test_disclosed_inventory_omits_raw_content_digests(tmp_path: Path) -> None:
    root = tmp_path / "source"
    root.mkdir()
    (root / "notes.txt").write_text("ordinary evidence", encoding="utf-8")
    service, scan = _service(root)
    source_file = scan.inventory.files[0]

    ledger = create_initial_evidence_ledger(
        scan.inventory,
        "Organize this folder",
    )
    page = service.execute(ListInventoryPageCall(call_id="page", page_size=10))

    assert source_file.sha256 not in repr(ledger.initial_evidence)
    assert "sha256" not in repr(ledger.initial_evidence)
    assert "protection_reasons" not in repr(ledger.initial_evidence)
    assert page.result is not None
    assert "sha256" not in repr(page.result)
    assert "protection_reasons" not in repr(page.result)


def test_text_excerpt_is_utf8_bounded_and_ledger_bytes_are_exact(
    tmp_path: Path,
) -> None:
    root = tmp_path / "source"
    root.mkdir()
    text = ("ø" * 20_000) + "\n"
    (root / "notes.txt").write_text(text, encoding="utf-8")
    service, scan = _service(root)
    source_file = scan.inventory.files[0]
    call = ReadTextExcerptCall(
        call_id="excerpt",
        file_id=source_file.file_id,
        start_byte=0,
        max_bytes=MAX_EVIDENCE_RESULT_BYTES,
    )

    execution = service.execute(call)
    ledger = append_evidence_execution(
        create_initial_evidence_ledger(scan.inventory, "Organize this folder"),
        response_turn=1,
        call=call,
        execution=execution,
    )

    assert execution.status == "success"
    assert execution.truncated is True
    assert execution.result is not None
    assert execution.result["content_is_untrusted"] is True
    assert execution.result["returned_byte_count"] == len(
        execution.result["text"].encode("utf-8")
    )
    assert ledger.records[0].byte_count <= MAX_EVIDENCE_RESULT_BYTES
    assert ledger.aggregate_result_bytes == ledger.records[0].byte_count
    assert (
        len(
            canonical_json_bytes(
                {
                    "error_code": None,
                    "result": execution.result,
                    "status": "success",
                    "truncated": execution.truncated,
                }
            )
        )
        == ledger.records[0].byte_count
    )


def test_inventory_and_link_cursors_are_source_bound(tmp_path: Path) -> None:
    root = tmp_path / "source"
    root.mkdir()
    (root / "a.txt").write_text("a", encoding="utf-8")
    (root / "b.txt").write_text("b", encoding="utf-8")
    (root / "note.md").write_text("[a](a.txt)\n[b](b.txt)\n", encoding="utf-8")
    service, scan = _service(root)

    first_page = service.execute(
        ListInventoryPageCall(call_id="inventory-1", page_size=1)
    )
    assert first_page.status == "success"
    assert first_page.result is not None
    cursor = first_page.result["next_cursor"]
    assert isinstance(cursor, str)
    second_page = service.execute(
        ListInventoryPageCall(
            call_id="inventory-2",
            cursor=cursor,
            page_size=1,
        )
    )
    assert second_page.status == "success"
    assert second_page.result is not None
    assert second_page.result["offset"] == 1

    markdown = next(
        item for item in scan.inventory.files if item.relative_path == "note.md"
    )
    link_page = service.execute(
        InspectMarkdownLinksCall(
            call_id="links-1",
            file_id=markdown.file_id,
            page_size=1,
        )
    )
    assert link_page.status == "success"
    assert link_page.result is not None
    assert len(link_page.result["references"]) == 1
    assert isinstance(link_page.result["next_cursor"], str)


def test_cache_hit_still_rechecks_source_equality(tmp_path: Path) -> None:
    root = tmp_path / "source"
    root.mkdir()
    path = root / "notes.txt"
    path.write_text("before", encoding="utf-8")
    service, _scan = _service(root)
    call = ListInventoryPageCall(call_id="inventory", page_size=10)

    first = service.execute(call)
    path.write_text("after", encoding="utf-8")
    second = service.execute(call)

    assert first.status == "success"
    assert second.status == "rejected"
    assert second.error_code == "source_changed"
    assert second.cache_hit is False
