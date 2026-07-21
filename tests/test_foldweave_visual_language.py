from __future__ import annotations

import re
import struct
from pathlib import Path
from xml.etree import ElementTree

PROJECT_ROOT = Path(__file__).resolve().parents[1]

AUTHORED_VISUAL_SOURCES = (
    PROJECT_ROOT / "src/name_atlas/static/folder.css",
    PROJECT_ROOT / "src/name_atlas/static/styles.css",
    PROJECT_ROOT / "src/name_atlas/templates/folder/base.html",
    PROJECT_ROOT / "src/name_atlas/templates/index.html",
    PROJECT_ROOT / "web/src/review.css",
    PROJECT_ROOT / "web/src/chatgpt-widget.css",
    PROJECT_ROOT / "gateway/src/gateway.ts",
    PROJECT_ROOT / "packaging/assets/foldweave-icon-master.svg",
)

PROHIBITED_PRESENTATION_PATTERNS = (
    re.compile(r"(?:linear|radial|conic)-gradient\s*\(", re.IGNORECASE),
    re.compile(r"drop-shadow\s*\(", re.IGNORECASE),
    re.compile(r"\btext-shadow\s*:", re.IGNORECASE),
    re.compile(r"\bbackdrop-filter\s*:", re.IGNORECASE),
    re.compile(r"#071426|#0b1c31|#38c8ff|#7c3aed|#00d4ff", re.IGNORECASE),
)


def test_active_authored_surfaces_exclude_rejected_cyber_visual_language() -> None:
    violations: list[str] = []
    for source_path in AUTHORED_VISUAL_SOURCES:
        source = source_path.read_text(encoding="utf-8")
        for pattern in PROHIBITED_PRESENTATION_PATTERNS:
            if pattern.search(source):
                violations.append(
                    f"{source_path.relative_to(PROJECT_ROOT)}: {pattern.pattern}"
                )
    assert violations == []


def test_active_renderers_do_not_force_blueprint_dark_mode() -> None:
    renderer_sources = (
        PROJECT_ROOT / "src/name_atlas/templates/folder/base.html",
        PROJECT_ROOT / "web/src/review-island.tsx",
        PROJECT_ROOT / "web/src/chatgpt-widget.tsx",
    )
    offenders = [
        str(path.relative_to(PROJECT_ROOT))
        for path in renderer_sources
        if "bp6-dark" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


def test_done_copy_control_keeps_blueprint_icon_at_native_control_size() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )
    copy_icon_rule = re.search(
        r"\.folder-result-path \.bp6-button img\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    assert copy_icon_rule is not None
    assert "width: 0.9rem !important;" in copy_icon_rule.group("body")
    assert "height: 0.9rem !important;" in copy_icon_rule.group("body")


def test_done_groups_proof_details_without_repeated_full_width_separators() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )
    template = (PROJECT_ROOT / "src/name_atlas/templates/folder/done.html").read_text(
        encoding="utf-8"
    )

    grouped_details = re.search(
        r"\.folder-panel--done \.folder-result-details > details \+ details\s*"
        r"\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    restore_control = re.search(
        r"\.folder-restore-control\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    assert grouped_details is not None
    assert "border-top: 0;" in grouped_details.group("body")
    assert restore_control is not None
    assert "border-top: 0;" in restore_control.group("body")
    assert '<details class="folder-technical-disclosure">' in template
    assert "<summary>Technical details</summary>" in template
    assert '<details class="folder-technical-disclosure" open>' not in template
    assert '<code id="result-data-path">' not in template
    assert "{{ state.result.display_folder_name }}" in template
    assert '<span class="folder-sr-only" id="result-data-path">' in template
    assert '<details class="folder-disclosure folder-restore-disclosure">' in template


def test_page_skip_target_does_not_draw_release_screenshot_outline() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )
    main_focus_rule = re.search(
        r"\.folder-main:focus,\s*\.folder-main:focus-visible\s*"
        r"\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    assert main_focus_rule is not None
    assert "outline: none !important;" in main_focus_rule.group("body")
    assert "box-shadow: none !important;" in main_focus_rule.group("body")


def test_native_form_groups_and_disclosures_keep_mac_style_alignment() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )
    base = (PROJECT_ROOT / "src/name_atlas/templates/folder/base.html").read_text(
        encoding="utf-8"
    )

    path_control_rule = re.search(
        r"\.folder-path-control\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    path_surface_rule = re.search(
        r"\.folder-path-surface\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    manual_rule = re.search(
        r"\.folder-manual-path\[open\]\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    manual_input_rule = re.search(
        r"\.folder-manual-path\[open\] > \.bp6-input\s*"
        r"\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    closed_key_storage_rule = re.search(
        r"\.folder-settings-surface > \.folder-disclosure:not\(\[open\]\)"
        r" > summary\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )

    assert path_control_rule is not None
    assert "padding: 0;" in path_control_rule.group("body")
    assert "background: transparent;" in path_control_rule.group("body")
    assert path_surface_rule is not None
    assert "padding: 0.9rem 1rem 1rem;" in path_surface_rule.group("body")
    assert "background: var(--folder-surface);" in path_surface_rule.group("body")
    assert manual_rule is not None
    assert "gap: 0.5rem;" in manual_rule.group("body")
    assert manual_input_rule is not None
    assert "margin-top: 0.35rem;" in manual_input_rule.group("body")
    assert closed_key_storage_rule is not None
    assert "padding: 0.7rem 0.8rem;" in closed_key_storage_rule.group("body")
    assert 'setFocusOrigin("pointer")' in base
    assert 'setFocusOrigin("keyboard")' in base

    start = (PROJECT_ROOT / "src/name_atlas/templates/folder/start.html").read_text(
        encoding="utf-8"
    )
    apply = (PROJECT_ROOT / "src/name_atlas/templates/folder/apply.html").read_text(
        encoding="utf-8"
    )
    assert start.count('class="folder-path-surface"') == 2
    assert apply.count('class="folder-path-surface"') == 3


def test_pointer_focus_does_not_draw_blue_disclosure_boxes() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )

    pointer_focus_rule = re.search(
        r"body\.folder-app :where\(a, button, input, textarea, summary\):focus\s*"
        r"\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )
    keyboard_summary_rule = re.search(
        r'html\[data-focus-origin="keyboard"\] body\.folder-app summary:focus\s*'
        r"\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )

    assert pointer_focus_rule is not None
    assert "outline: none;" in pointer_focus_rule.group("body")
    assert "box-shadow: none;" in pointer_focus_rule.group("body")
    assert keyboard_summary_rule is not None
    assert "outline" not in keyboard_summary_rule.group("body")
    assert "text-decoration: underline;" in keyboard_summary_rule.group("body")

    review_css = (PROJECT_ROOT / "web/src/review.css").read_text(encoding="utf-8")
    widget_css = (PROJECT_ROOT / "web/src/chatgpt-widget.css").read_text(
        encoding="utf-8"
    )
    assert ".fw-review .bp6-input:focus-visible" in review_css
    assert ".fw-decision-panel textarea:focus-visible" in review_css
    assert ".fw-review .bp6-input:focus," not in review_css
    assert (
        ".fw-decision-panel textarea:focus {\n  border-color: var(--fw-control-border);"
        in review_css
    )
    assert (
        ".fw-filter-menu[open] > summary {\n"
        "  background: var(--fw-selection);\n"
        "  border-color: var(--fw-control-border);" in review_css
    )
    assert ".fw-chatgpt-widget summary:focus-visible" in widget_css
    assert (
        ":where(button, input, textarea, summary):focus:not(:focus-visible)"
        in widget_css
    )


def test_settings_headings_use_native_sentence_case_without_tracking() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )
    heading_rule = re.search(
        r"\.folder-settings-group > h2\s*\{(?P<body>[^}]*)\}",
        css,
        flags=re.DOTALL,
    )

    assert heading_rule is not None
    assert "letter-spacing" not in heading_rule.group("body")
    assert "text-transform" not in heading_rule.group("body")


def test_start_and_apply_use_a_width_gated_short_desktop_layout() -> None:
    css = (PROJECT_ROOT / "src/name_atlas/static/folder.css").read_text(
        encoding="utf-8"
    )
    short_desktop = re.search(
        r"@media \(min-width: 50rem\) and \(max-height: 47\.5rem\)\s*"
        r"\{(?P<body>.*?)(?=\n@media \(max-width: 50rem\))",
        css,
        flags=re.DOTALL,
    )
    assert short_desktop is not None
    body = short_desktop.group("body")
    assert "--folder-group-gap: 0.65rem;" in body
    assert "min-height: 4.25rem;" in body
    assert ".folder-path-surface" in body


def test_foldweave_icon_is_flat_vector_source_with_1024_pixel_master() -> None:
    svg_path = PROJECT_ROOT / "packaging/assets/foldweave-icon-master.svg"
    root = ElementTree.parse(svg_path).getroot()
    assert root.attrib["width"] == "1024"
    assert root.attrib["height"] == "1024"
    assert root.attrib["viewBox"] == "0 0 1024 1024"

    png_path = PROJECT_ROOT / "packaging/assets/foldweave-icon-master.png"
    with png_path.open("rb") as png_file:
        assert png_file.read(8) == b"\x89PNG\r\n\x1a\n"
        chunk_length = struct.unpack(">I", png_file.read(4))[0]
        assert png_file.read(4) == b"IHDR"
        ihdr = png_file.read(chunk_length)
    width, height = struct.unpack(">II", ihdr[:8])
    assert (width, height) == (1024, 1024)
