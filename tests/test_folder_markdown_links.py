"""Exact supported-subset tests for folder Markdown reference handling."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

import name_atlas.folder_refactor.markdown_links as markdown_links_module
from name_atlas.folder_refactor.contracts import (
    AcceptedFileMapping,
    FolderAcceptedPlan,
    FolderInventory,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.markdown_links import (
    MarkdownLinkError,
    apply_reference_rewrites,
    build_reference_graph,
    derive_reference_rewrites,
    verify_reference_rewrites,
)


def _write_source(root: Path, files: dict[str, bytes]) -> FolderInventory:
    for relative_path, payload in files.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    return scan_folder(root).inventory


def _markdown_payloads(
    root: Path,
    inventory: FolderInventory,
) -> dict[str, bytes]:
    return {
        item.relative_path: (root / item.relative_path).read_bytes()
        for item in inventory.files
        if Path(item.relative_path).suffix.casefold() in {".md", ".markdown"}
    }


def _accepted_plan(
    inventory: FolderInventory,
    targets: dict[str, str],
) -> FolderAcceptedPlan:
    mappings = tuple(
        AcceptedFileMapping(
            file_id=item.file_id,
            original_path=item.relative_path,
            target_path=(
                item.relative_path if item.protected else targets[item.relative_path]
            ),
            protected=item.protected,
            planner_supplied=not item.protected,
        )
        for item in inventory.files
    )
    return FolderAcceptedPlan(
        source_commitment=inventory.source_commitment,
        request_fingerprint="a" * 64,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint="b" * 64,
        result_folder_name="organized-copy",
        file_mappings=mappings,
        empty_directories=tuple(
            item.relative_path for item in inventory.empty_directories
        ),
    )


def test_scan_records_exact_utf8_byte_spans_and_ignored_counts(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = (
        "Préface [report](docs/report\\(1\\).pdf#page-%C3%A9) and "
        "![image](<assets/über image.png#hero>)\r\n"
        "[web](https://example.com/path) [section](#intro)\r\n"
        "`[inline](docs/report\\(1\\).pdf)`\r\n"
        "```markdown\r\n[fenced](docs/report\\(1\\).pdf)\r\n```\r\n"
        "    [indented](docs/report\\(1\\).pdf)\r\n"
    ).encode()
    inventory = _write_source(
        source,
        {
            "notes.md": markdown,
            "docs/report(1).pdf": b"report",
            "assets/über image.png": b"image",
        },
    )

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert graph.schema_version == "folder-reference-graph.v1"
    assert graph.source_commitment == inventory.source_commitment
    assert len(graph.references) == 2
    assert graph.ignored.external_schemes == 1
    assert graph.ignored.anchor_only == 1
    assert graph.ignored.total == 2
    report, image = graph.references
    assert report.source_path == image.source_path == "notes.md"
    assert report.target_path == "docs/report(1).pdf"
    assert report.original_destination_text == ("docs/report\\(1\\).pdf#page-%C3%A9")
    assert report.fragment == "#page-%C3%A9"
    assert report.destination_style == "token"
    assert report.is_image is False
    assert image.target_path == "assets/über image.png"
    assert image.original_destination_text == "assets/über image.png#hero"
    assert image.fragment == "#hero"
    assert image.destination_style == "angle"
    assert image.is_image is True
    for reference in graph.references:
        original = bytes.fromhex(reference.original_destination_bytes_hex)
        assert (
            markdown[reference.destination_start_byte : reference.destination_end_byte]
            == original
        )
        assert original.decode() == reference.original_destination_text
        assert reference.proposed_destination is None
        assert reference.verification_status == "pending"

    serialized = graph.model_dump_json()
    assert str(source.resolve()) not in serialized
    assert FolderReferenceGraph.model_validate_json(serialized, strict=True) == graph


def test_multiline_inline_code_is_not_scanned_as_a_link(tmp_path: Path) -> None:
    source = tmp_path / "source"
    markdown = b"`code starts\n[not a link](target.txt)\nends`\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert graph.references == ()


def test_inline_code_in_link_label_does_not_hide_supported_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = b"[read `target`](target.txt)\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert len(graph.references) == 1
    assert graph.references[0].target_path == "target.txt"


def test_derive_and_apply_rewrites_preserve_every_other_byte(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    original = (
        "α [report](docs/report\\(1\\).pdf#exact-fragment) | "
        "![image](<assets/über image.png>) ω\r\n"
    ).encode()
    inventory = _write_source(
        source,
        {
            "notes.md": original,
            "docs/report(1).pdf": b"report",
            "assets/über image.png": b"image",
        },
    )
    graph = build_reference_graph(inventory, {"notes.md": original})
    plan = _accepted_plan(
        inventory,
        {
            "notes.md": "handoff/overview.md",
            "docs/report(1).pdf": "handoff/final report(1).pdf",
            "assets/über image.png": "handoff/hero über image.png",
        },
    )

    derived = derive_reference_rewrites(graph, plan)
    rewritten = apply_reference_rewrites(
        original,
        source_file_id=graph.references[0].source_file_id,
        graph=derived,
    )

    assert [item.proposed_destination for item in derived.references] == [
        "final%20report%281%29.pdf#exact-fragment",
        "hero%20%C3%BCber%20image.png",
    ]
    assert all(item.verification_status == "rewritten" for item in derived.references)
    assert (
        rewritten
        == (
            "α [report](final%20report%281%29.pdf#exact-fragment) | "
            "![image](<hero%20%C3%BCber%20image.png>) ω\r\n"
        ).encode()
    )
    verify_reference_rewrites(
        original,
        rewritten,
        source_file_id=graph.references[0].source_file_id,
        graph=derived,
    )
    with pytest.raises(MarkdownLinkError) as raised:
        verify_reference_rewrites(
            original,
            rewritten + b"changed",
            source_file_id=graph.references[0].source_file_id,
            graph=derived,
        )
    assert raised.value.code == "staged_markdown_mismatch"


def test_percent_decodes_once_and_emits_one_canonical_policy(tmp_path: Path) -> None:
    source = tmp_path / "source"
    markdown = b"[literal](literal%252F%20name.txt)\n"
    inventory = _write_source(
        source,
        {
            "notes.md": markdown,
            "literal%2F name.txt": b"literal percent sequence",
        },
    )
    graph = build_reference_graph(inventory, {"notes.md": markdown})
    plan = _accepted_plan(
        inventory,
        {
            "notes.md": "done/notes.md",
            "literal%2F name.txt": "done/literal%2F name.txt",
        },
    )

    derived = derive_reference_rewrites(graph, plan)

    assert graph.references[0].target_path == "literal%2F name.txt"
    assert derived.references[0].proposed_destination == "literal%252F%20name.txt"
    assert derived.references[0].verification_status == "unchanged"
    assert (
        apply_reference_rewrites(
            markdown,
            source_file_id=graph.references[0].source_file_id,
            graph=derived,
        )
        == markdown
    )


def test_fragment_is_preserved_exactly_even_with_markdown_escapes(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = b"[target](target.txt#section\\(draft\\))\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )
    graph = build_reference_graph(inventory, {"notes.md": markdown})
    plan = _accepted_plan(
        inventory,
        {"notes.md": "done/notes.md", "target.txt": "done/renamed.txt"},
    )

    derived = derive_reference_rewrites(graph, plan)

    assert graph.references[0].fragment == "#section\\(draft\\)"
    assert derived.references[0].proposed_destination == (
        "renamed.txt#section\\(draft\\)"
    )


@pytest.mark.parametrize(
    ("destination", "expected_code"),
    [
        ("target.txt?download=1", "query_string_unsupported"),
        ("/target.txt", "absolute_path_unsupported"),
        ("C:/target.txt", "absolute_path_unsupported"),
        ("file:target.txt", "file_url_unsupported"),
        ("../target.txt", "outside_root_path"),
        ("folder", "directory_target"),
        ("missing.txt", "dangling_target"),
        ("bad%ZZ.txt", "malformed_percent_escape"),
        ("bad%2Fname.txt", "encoded_separator_ambiguity"),
        ("bad%5cname.txt", "encoded_separator_ambiguity"),
        ("bad%00name.txt", "decoded_nul"),
        ("bad%FFname.txt", "invalid_utf8_destination"),
        ("docs/report(1).pdf", "unsupported_local_link_syntax"),
        ("docs/a b.txt", "unsupported_local_link_syntax"),
    ],
)
def test_rejects_every_unsupported_or_ambiguous_local_destination(
    tmp_path: Path,
    destination: str,
    expected_code: str,
) -> None:
    source = tmp_path / "source"
    markdown = f"[target]({destination})\n".encode()
    inventory = _write_source(
        source,
        {
            "notes.md": markdown,
            "target.txt": b"target",
            "folder/member.txt": b"member",
            "docs/report(1).pdf": b"report",
            "docs/a b.txt": b"space",
        },
    )

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"notes.md": markdown})

    assert raised.value.code == expected_code


def test_resolution_is_logical_and_case_sensitive(tmp_path: Path) -> None:
    source = tmp_path / "source"
    markdown = b"[target](docs/case.txt)\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "docs/Case.txt": b"target"},
    )

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"notes.md": markdown})

    assert raised.value.code == "case_mismatched_target"
    assert "docs/Case.txt" in raised.value.message


def test_in_root_parent_traversal_is_still_outside_supported_subset(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = b"[target](../target.txt)\n"
    inventory = _write_source(
        source,
        {"sub/notes.md": markdown, "target.txt": b"target"},
    )

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"sub/notes.md": markdown})

    assert raised.value.code == "path_traversal_unsupported"


@pytest.mark.parametrize(
    "markdown",
    [
        b"[document]: target.txt\n[open][document]\n",
        b"[open][document]\n",
        b"[open][]\n",
    ],
)
def test_reference_style_local_links_and_definitions_block(
    tmp_path: Path,
    markdown: bytes,
) -> None:
    source = tmp_path / "source"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"notes.md": markdown})

    assert raised.value.code == "reference_style_local_unsupported"


def test_external_reference_style_is_ignored_and_counted(tmp_path: Path) -> None:
    source = tmp_path / "source"
    markdown = b"[site]: https://example.com\n[open][site]\n"
    inventory = _write_source(source, {"notes.md": markdown})

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert graph.references == ()
    assert graph.ignored.external_schemes == 1
    assert graph.ignored.anchor_only == 0


def test_anchor_reference_style_is_ignored_and_counted_as_anchor(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = b"[section]: #intro\n[go][section]\n"
    inventory = _write_source(source, {"notes.md": markdown})

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert graph.references == ()
    assert graph.ignored.external_schemes == 0
    assert graph.ignored.anchor_only == 1


def test_invalid_utf8_markdown_and_payload_binding_fail_closed(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    invalid = b"[target](target.txt)\n\xff"
    inventory = _write_source(
        source,
        {"notes.md": invalid, "target.txt": b"target"},
    )
    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"notes.md": invalid})
    assert raised.value.code == "invalid_utf8_markdown"

    valid_source = tmp_path / "valid"
    valid = b"[target](target.txt)\n"
    valid_inventory = _write_source(
        valid_source,
        {"notes.md": valid, "target.txt": b"target"},
    )
    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(valid_inventory, {"notes.md": valid + b"changed"})
    assert raised.value.code == "markdown_payload_binding_mismatch"


def test_requires_exact_markdown_payload_set(tmp_path: Path) -> None:
    source = tmp_path / "source"
    first = b"[target](target.txt)\n"
    second = b"second\n"
    inventory = _write_source(
        source,
        {
            "first.md": first,
            "second.markdown": second,
            "target.txt": b"target",
        },
    )

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"first.md": first})
    assert raised.value.code == "missing_markdown_payload"

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(
            inventory,
            {
                "first.md": first,
                "second.markdown": second,
                "target.txt": b"not accepted",
            },
        )
    assert raised.value.code == "unexpected_markdown_payload"


def test_apply_rejects_changed_original_span_and_underived_graph(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = b"prefix [target](target.txt) suffix\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )
    graph = build_reference_graph(inventory, {"notes.md": markdown})
    source_file_id = graph.references[0].source_file_id

    with pytest.raises(MarkdownLinkError) as raised:
        apply_reference_rewrites(
            markdown,
            source_file_id=source_file_id,
            graph=graph,
        )
    assert raised.value.code == "rewrite_not_derived"

    plan = _accepted_plan(
        inventory,
        {"notes.md": "done/notes.md", "target.txt": "done/target.txt"},
    )
    derived = derive_reference_rewrites(graph, plan)
    tampered = markdown.replace(b"target.txt", b"targot.txt")
    assert len(tampered) == len(markdown)
    with pytest.raises(MarkdownLinkError) as raised:
        apply_reference_rewrites(
            tampered,
            source_file_id=source_file_id,
            graph=derived,
        )
    assert raised.value.code == "reference_span_binding_mismatch"


def test_aggregate_supported_reference_limit_blocks_during_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "source"
    markdown = b"[one](target.txt) [two](target.txt) [three](target.txt)\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )
    monkeypatch.setattr(
        markdown_links_module,
        "MAX_SUPPORTED_MARKDOWN_REFERENCES",
        2,
    )

    with pytest.raises(MarkdownLinkError) as raised:
        build_reference_graph(inventory, {"notes.md": markdown})

    assert raised.value.code == "markdown_reference_limit_exceeded"


def test_large_unmatched_bracket_input_is_scanned_without_rescanning_suffixes(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = (b"[" * 20_000) + b"\n"
    inventory = _write_source(source, {"notes.md": markdown})

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert graph.references == ()


def test_large_backslash_run_is_scanned_without_repeated_escape_walks(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    markdown = (b"\\" * 20_000) + b"\n"
    inventory = _write_source(source, {"notes.md": markdown})

    graph = build_reference_graph(inventory, {"notes.md": markdown})

    assert graph.references == ()


def test_plan_and_graph_source_commitments_must_match(tmp_path: Path) -> None:
    source = tmp_path / "source"
    markdown = b"[target](target.txt)\n"
    inventory = _write_source(
        source,
        {"notes.md": markdown, "target.txt": b"target"},
    )
    graph = build_reference_graph(inventory, {"notes.md": markdown})
    plan = _accepted_plan(
        inventory,
        {"notes.md": "done/notes.md", "target.txt": "done/target.txt"},
    ).model_copy(update={"source_commitment": hashlib.sha256(b"other").hexdigest()})

    with pytest.raises(MarkdownLinkError) as raised:
        derive_reference_rewrites(graph, plan)

    assert raised.value.code == "accepted_plan_binding_mismatch"
