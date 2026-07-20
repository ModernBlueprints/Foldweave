"""Static acceptance tests for the checked-in Foldweave app bundle profile."""

from __future__ import annotations

import ast
import hashlib
import importlib.metadata
import struct
import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]
SPEC_PATH = PROJECT_ROOT / "packaging" / "Foldweave.spec"
ENTRY_PATH = PROJECT_ROOT / "packaging" / "foldweave_entry.py"
ICON_MASTER_PATH = PROJECT_ROOT / "packaging" / "assets" / "foldweave-icon-master.png"
ICON_PATH = PROJECT_ROOT / "packaging" / "assets" / "Foldweave.icns"
CPYTHON_LICENSE_SHA256 = (
    "3b2f81fe21d181c499c59a256c8e1968455d6689d269aa85373bfb6af41da3bf"
)
CPYTHON_LICENSE_APPENDIX_SHA256 = (
    "2b734ec5975b21b29ae8b9756a00fc3dfe701abe51687cec4c98a21c51005bca"
)


def test_pyinstaller_profile_is_windowed_arm64_onedir_with_required_assets() -> None:
    specification = SPEC_PATH.read_text(encoding="utf-8")

    ast.parse(specification, filename=str(SPEC_PATH))
    assert "exclude_binaries=True" in specification
    assert "console=False" in specification
    assert 'target_arch="arm64"' in specification
    assert 'name="Foldweave.app"' in specification
    assert 'bundle_identifier="com.modernblueprints.foldweave"' in specification
    assert "icon=str(ICON_PATH)" in specification
    assert "codesign_identity=None" in specification
    assert "COLLECT(" in specification
    assert "BUNDLE(" in specification
    assert "onefile" not in specification.casefold()
    for required_asset in ("templates", "static", "recordings"):
        assert f'PACKAGE_ROOT / "{required_asset}"' in specification
    assert 'PACKAGE_ROOT / "assets" / "chatgpt-widget"' in specification
    assert '"name_atlas/assets/chatgpt-widget"' in specification
    assert 'PROJECT_ROOT / "LICENSE"' in specification
    assert 'PROJECT_ROOT / "THIRD_PARTY_NOTICES.md"' in specification
    assert "PYTHON_RUNTIME_DISTRIBUTIONS" in specification
    assert "PACKAGING_RUNTIME_NOTICE_DISTRIBUTIONS" in specification
    assert '"bagit"' in specification
    assert '"mcp"' in specification
    assert '"websockets"' in specification
    assert '"pyinstaller"' in specification
    assert '"pyinstaller-hooks-contrib"' in specification
    assert "for data in copy_metadata(distribution_name)" in specification
    assert "PYTHON_LICENSE" in specification
    assert "PYTHON_LICENSE_APPENDIX" in specification
    assert '"licenses/cpython-3.11.9"' in specification
    assert 'collect_submodules("webview")' not in specification
    assert "excludes=excluded_build_and_test_modules" in specification
    for excluded_module in (
        "PyInstaller",
        "_distutils_hack",
        "_pyinstaller_hooks_contrib",
        "_pytest",
        "altgraph",
        "macholib",
        "packaging",
        "pygments",
        "pytest",
        "setuptools",
    ):
        assert f'"{excluded_module}"' in specification
    assert "hookspath=[str(HOOKS_ROOT)]" in specification
    bagit_hook = PROJECT_ROOT / "packaging" / "pyinstaller_hooks" / "hook-bagit.py"
    assert 'excludedimports = ["importlib_metadata"]' in bagit_hook.read_text(
        encoding="utf-8"
    )
    for hidden_import in (
        "webview.platforms.cocoa",
        "name_atlas.foldweave_chatgpt_mcp",
        "name_atlas.foldweave_companion_client",
        "name_atlas.foldweave_companion_supervisor",
        "mcp.server.streamable_http_manager",
    ):
        assert f'"{hidden_import}"' in specification
    for forbidden in ("Electron", "Tauri", "React development server"):
        assert forbidden not in specification


def test_foldweave_icon_master_and_bundle_asset_are_release_ready() -> None:
    icon_master = ICON_MASTER_PATH.read_bytes()
    assert icon_master.startswith(b"\x89PNG\r\n\x1a\n")
    width, height = struct.unpack(">II", icon_master[16:24])
    assert (width, height) == (1024, 1024)

    bundled_icon = ICON_PATH.read_bytes()
    assert bundled_icon[:4] == b"icns"
    assert len(bundled_icon) > 100_000


def test_native_build_runtime_metadata_and_cpython_licenses_are_available() -> None:
    specification = SPEC_PATH.read_text(encoding="utf-8")
    module = ast.parse(specification, filename=str(SPEC_PATH))
    assigned_names = {
        target.id
        for node in module.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    assert {
        "PYTHON_RUNTIME_DISTRIBUTIONS",
        "PACKAGING_RUNTIME_NOTICE_DISTRIBUTIONS",
    } <= assigned_names

    for distribution_name in (
        "mcp",
        "pywebview",
        "websockets",
        "pyinstaller",
        "pyinstaller-hooks-contrib",
    ):
        assert importlib.metadata.distribution(distribution_name).version

    license_root = Path(sys.base_prefix) / "lib" / "python3.11"
    python_license = license_root / "LICENSE.txt"
    license_appendix = (
        Path(sys.base_prefix)
        / "Resources"
        / "English.lproj"
        / "Documentation"
        / "_sources"
        / "license.rst.txt"
    )
    assert hashlib.sha256(python_license.read_bytes()).hexdigest() == (
        CPYTHON_LICENSE_SHA256
    )
    assert hashlib.sha256(license_appendix.read_bytes()).hexdigest() == (
        CPYTHON_LICENSE_APPENDIX_SHA256
    )


def test_foldweave_notice_covers_bundled_javascript_runtime() -> None:
    notice = (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")

    assert "Foldweave packages selected static assets and compiled JavaScript" in notice
    assert "`react` 18.3.1" in notice
    assert "`react-dom` 18.3.1" in notice
    assert "`@blueprintjs/core` 6.17.2" in notice
    assert "`react-transition-group` 4.4.5" in notice
    assert "`tslib` 2.6.3" in notice
    assert "does not redistribute Blueprint's React runtime" not in notice


def test_foldweave_notice_covers_native_python_and_packaging_runtime() -> None:
    notice = (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")

    for required_runtime in (
        "`openai` | 2.46.0",
        "`mcp` | 1.28.1",
        "`pywebview` | 6.2.1",
        "`rpds-py` | 2026.6.3",
        "`websockets` | 15.0.1",
        "CPython | 3.11.9",
        "OpenSSL | 3.0.13",
        "ncurses | 5.9.20120616",
        "XZ/liblzma | 5.2.3",
        "PyInstaller 6.21.0",
        "PyInstaller community hooks package 2026.6",
    ):
        assert required_runtime in notice
    for sbom_fingerprint in (
        "e88b4427a6b70097b9fead6aab292456b29a40049567c4c501a25be506a370d7",
        "95022207ef86610c13d768fac68a21fbf2edd8dcefc0a143154e84c5359b7c9c",
        "796c92c45da906a58f452cd49c458145028487f83297bafafb07669b0bcecc0f",
        "7d6726d9debc3c715f2860114b4ceccde59fa7e7b4d696953b3fc3cd3bb8a846",
    ):
        assert sbom_fingerprint in notice


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

    assert configuration["project"]["name"] == "foldweave"
    assert configuration["project"]["scripts"]["foldweave"] == (
        "name_atlas.foldweave_launcher:main"
    )
    assert configuration["project"]["scripts"]["name-atlas"] == (
        "name_atlas.launcher:main"
    )
