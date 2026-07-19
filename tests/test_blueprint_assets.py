"""Provenance, safety, and packaging checks for vendored Blueprint assets."""

from __future__ import annotations

import hashlib
import re
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
VENDOR_ROOT = PROJECT_ROOT / "src/name_atlas/static/vendor/blueprint"
ICON_ROOT = VENDOR_ROOT / "icons"
SVG_NAMESPACE = "http://www.w3.org/2000/svg"

EXPECTED_ICON_HASHES = {
    "chevron-right.svg": (
        "a8767948728333c16fead870a7bb1722c90b7a5c3216fe43319de8c94eb28493"
    ),
    "clipboard.svg": (
        "8303d5fee96cb8e943043df3ae8fd2cd9183860b55ccf5f5dd1394c8ad06530e"
    ),
    "database.svg": (
        "2922db1a1380e56ef312016ea34c256f9faf6afe0bf8a7e489ea5df92ee7e812"
    ),
    "diagram-tree.svg": (
        "5a1f27fd94f5731aec2e22fe57dedd6cd6a8d686ddf3a9dc7bcfab008b6576a9"
    ),
    "export.svg": ("271fcbc30849bca5ebcfd5f92ea33afeefc5398f965cb625b9ab644c14331012"),
    "help.svg": ("8ca7d60d8a1031ebd2a03a9d18934c6683fe195c5729f7b5b06c7954bbe58039"),
    "history.svg": ("edfdb3955b3d0ca04f3edff84629e7273e74387b728816dbe4dd0fa1b8e5eb37"),
    "tick-circle.svg": (
        "99dfcea0b90e42742afd60f174fc28a18ce94ed5d1ced3ce90568c9e8121166d"
    ),
    "warning-sign.svg": (
        "617429b93029fd5411b968df8f836553bdda5ee79649181ebdb2dfa6e17c9f9d"
    ),
}
EXPECTED_UPSTREAM_ICON_HASHES = (
    "f06ca353d3a2264f8a2260fc5a8b41197f56b1f8254faa55e29440021cfbc198",
    "40a20491ad645d3c1e1525083270951e7c389b5e987eb5fc9e0c2b2dda4c9fdd",
    "c655673b6384af8f67a2be09b0f463dfab441877e377cb42105ee1a290efa101",
    "c3312eca12caebab60a2522493a59f7bf9875ab66059227a9ec0bdd68d4b0caa",
    "ef69c5451f2e2131cf094c9401ef4e6532e7fead916b52026abd8df83ab467d0",
    "8e8562c006b16c08f3e50566bcf90e8a77c8acfefdf2951365d477f6e0a4c68b",
    "6422532b1c4607e9152c2ceb3f15e6a8e1f64339a6b4480a575602c345c474cb",
    "3e5534a83c0989cadc285fc4f748a2aecbd33fc29039d90da591c9b0b2681fc9",
    "d8e4ae34fc1f08e22d56264e5680085e30a7284f97100bfa7e7fb1188d841c66",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_blueprint_versions_sources_and_license_are_exact() -> None:
    notice = (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")

    assert "`@blueprintjs/core` 6.17.2" in notice
    assert "`@blueprintjs/icons` 6.13.0" in notice
    assert "https://registry.npmjs.org/@blueprintjs/core/-/core-6.17.2.tgz" in notice
    assert "https://registry.npmjs.org/@blueprintjs/icons/-/icons-6.13.0.tgz" in notice
    assert "df7649577a2b7c5548c07538fec57cded14c856b42db0ddeca2d36f315e74180" in notice
    assert "6344d90154a1d47d62989a90ca9e87d3055963fcd7ce9cd942843eb178b9837d" in notice
    assert "Apache-2.0" in notice
    for expected_hash in (
        *EXPECTED_UPSTREAM_ICON_HASHES,
        *EXPECTED_ICON_HASHES.values(),
    ):
        assert expected_hash in notice
    assert _sha256(VENDOR_ROOT / "LICENSE") == (
        "a6cba85bc92e0cff7a450b1d873c0eaa2e9fc96bf472df0247a26bec77bf3ff9"
    )


def test_compiled_core_css_is_exact_and_has_no_network_dependency() -> None:
    css_path = VENDOR_ROOT / "blueprint.css"
    css = css_path.read_text(encoding="utf-8")

    assert _sha256(css_path) == (
        "04c4dc66a0753f7256194af14f5f96f15a1a149e125898349b26c26c92ba377e"
    )
    assert ".bp6-dark" in css
    assert "@import" not in css
    asset_urls = re.findall(r"url\(([^)]+)\)", css)
    assert asset_urls
    assert all(value.strip("\"'").startswith("data:") for value in asset_urls)


def test_only_selected_inert_accessibility_ready_icons_are_vendored() -> None:
    actual_files = {path.name for path in ICON_ROOT.iterdir() if path.is_file()}

    assert actual_files == set(EXPECTED_ICON_HASHES)
    for name, expected_hash in EXPECTED_ICON_HASHES.items():
        icon_path = ICON_ROOT / name
        assert _sha256(icon_path) == expected_hash

        root = ET.fromstring(icon_path.read_bytes())
        assert root.tag == f"{{{SVG_NAMESPACE}}}svg"
        assert root.attrib == {
            "viewBox": "0 0 20 20",
            "fill": "currentColor",
            "focusable": "false",
            "aria-hidden": "true",
        }
        children = list(root)
        assert len(children) == 1
        assert children[0].tag == f"{{{SVG_NAMESPACE}}}path"
        assert set(children[0].attrib) == {"d"}
        assert children[0].attrib["d"]


def test_wheel_configuration_includes_notice_and_package_assets() -> None:
    configuration = tomllib.loads(
        (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )
    wheel = configuration["tool"]["hatch"]["build"]["targets"]["wheel"]

    assert wheel["packages"] == ["src/name_atlas"]
    assert wheel["force-include"] == {
        "THIRD_PARTY_NOTICES.md": "name_atlas/THIRD_PARTY_NOTICES.md",
        "sample_data/connected_change": "name_atlas/sample_data/connected_change",
        "sample_data/folder_a1": "name_atlas/sample_data/folder_a1",
        "sample_data/hero": "name_atlas/sample_data/hero",
    }
    assert not (PROJECT_ROOT / "package.json").exists()
    assert not (PROJECT_ROOT / "vite.config.js").exists()
    assert not (PROJECT_ROOT / "vite.config.ts").exists()
