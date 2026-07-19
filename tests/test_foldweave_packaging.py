"""Static acceptance tests for the checked-in Foldweave app bundle profile."""

from __future__ import annotations

import ast
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
SPEC_PATH = PROJECT_ROOT / "packaging" / "Foldweave.spec"
ENTRY_PATH = PROJECT_ROOT / "packaging" / "foldweave_entry.py"


def test_pyinstaller_profile_is_windowed_arm64_onedir_with_required_assets() -> None:
    specification = SPEC_PATH.read_text(encoding="utf-8")

    ast.parse(specification, filename=str(SPEC_PATH))
    assert "exclude_binaries=True" in specification
    assert "console=False" in specification
    assert 'target_arch="arm64"' in specification
    assert 'name="Foldweave.app"' in specification
    assert 'bundle_identifier="com.modernblueprints.foldweave"' in specification
    assert "codesign_identity=None" in specification
    assert "COLLECT(" in specification
    assert "BUNDLE(" in specification
    assert "onefile" not in specification.casefold()
    for required_asset in ("templates", "static", "recordings"):
        assert f'PACKAGE_ROOT / "{required_asset}"' in specification
    assert 'PROJECT_ROOT / "LICENSE"' in specification
    assert 'PROJECT_ROOT / "THIRD_PARTY_NOTICES.md"' in specification
    assert 'copy_metadata("bagit")' in specification
    for forbidden in ("Electron", "Tauri", "React development server"):
        assert forbidden not in specification


def test_windowed_entry_uses_only_the_native_composition_root() -> None:
    entry = ENTRY_PATH.read_text(encoding="utf-8")

    assert "from name_atlas.foldweave_native_cli import main" in entry
    assert "foldweave_browser_cli" not in entry
    assert "uvicorn.run" not in entry
    assert "webview" not in entry


def test_primary_foldweave_cli_remains_the_lazy_top_level_launcher() -> None:
    configuration = tomllib.loads(
        (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    )

    assert configuration["project"]["scripts"]["foldweave"] == (
        "name_atlas.foldweave_launcher:main"
    )
