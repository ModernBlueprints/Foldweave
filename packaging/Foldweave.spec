"""PyInstaller 6 onedir/windowed specification for macOS Apple Silicon."""

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules, copy_metadata

PROJECT_ROOT = Path(SPECPATH).resolve().parent
SOURCE_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SOURCE_ROOT / "name_atlas"
ENTRY_POINT = PROJECT_ROOT / "packaging" / "foldweave_entry.py"

datas = [
    (str(PACKAGE_ROOT / "templates"), "name_atlas/templates"),
    (str(PACKAGE_ROOT / "static"), "name_atlas/static"),
    (str(PACKAGE_ROOT / "recordings"), "name_atlas/recordings"),
    (str(PROJECT_ROOT / "LICENSE"), "."),
    (str(PROJECT_ROOT / "THIRD_PARTY_NOTICES.md"), "."),
] + copy_metadata("bagit")
hiddenimports = sorted(
    set(
        collect_submodules("uvicorn")
        + collect_submodules("webview")
        + [
            "AppKit",
            "Foundation",
            "PyObjCTools.AppHelper",
            "Quartz",
            "Security",
            "WebKit",
        ]
    )
)

analysis = Analysis(
    [str(ENTRY_POINT)],
    pathex=[str(SOURCE_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
python_archive = PYZ(analysis.pure)

executable = EXE(
    python_archive,
    analysis.scripts,
    [],
    exclude_binaries=True,
    name="Foldweave",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
)

collected = COLLECT(
    executable,
    analysis.binaries,
    analysis.datas,
    strip=False,
    upx=False,
    name="Foldweave",
)

application = BUNDLE(
    collected,
    name="Foldweave.app",
    icon=None,
    bundle_identifier="com.modernblueprints.foldweave",
    version="0.1.0",
    info_plist={
        "CFBundleDisplayName": "Foldweave",
        "CFBundleName": "Foldweave",
        "LSMinimumSystemVersion": "13.0",
        "NSHighResolutionCapable": True,
        "NSHumanReadableCopyright": "Copyright 2026 Modern Blueprints",
    },
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
)
