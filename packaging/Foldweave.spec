"""PyInstaller 6 onedir/windowed specification for macOS Apple Silicon."""

import sys
from pathlib import Path

from PyInstaller.utils.hooks import copy_metadata

PROJECT_ROOT = Path(SPECPATH).resolve().parent
SOURCE_ROOT = PROJECT_ROOT / "src"
PACKAGE_ROOT = SOURCE_ROOT / "name_atlas"
ENTRY_POINT = PROJECT_ROOT / "packaging" / "foldweave_entry.py"
ICON_PATH = PROJECT_ROOT / "packaging" / "assets" / "Foldweave.icns"
HOOKS_ROOT = PROJECT_ROOT / "packaging" / "pyinstaller_hooks"
PYTHON_LICENSE = Path(sys.base_prefix) / "lib" / "python3.11" / "LICENSE.txt"
PYTHON_LICENSE_APPENDIX = (
    Path(sys.base_prefix)
    / "Resources"
    / "English.lproj"
    / "Documentation"
    / "_sources"
    / "license.rst.txt"
)

for required_license in (PYTHON_LICENSE, PYTHON_LICENSE_APPENDIX):
    if not required_license.is_file():
        raise FileNotFoundError(
            f"Required CPython runtime license is unavailable: {required_license}"
        )

PYTHON_RUNTIME_DISTRIBUTIONS = (
    "annotated-doc",
    "annotated-types",
    "anyio",
    "attrs",
    "bagit",
    "bottle",
    "certifi",
    "cffi",
    "click",
    "cryptography",
    "distro",
    "fastapi",
    "h11",
    "httpcore",
    "httpx",
    "httpx-sse",
    "idna",
    "Jinja2",
    "jiter",
    "jsonschema",
    "jsonschema-specifications",
    "MarkupSafe",
    "mcp",
    "openai",
    "proxy_tools",
    "pydantic",
    "pydantic_core",
    "pydantic-settings",
    "pycparser",
    "PyJWT",
    "pyobjc-core",
    "pyobjc-framework-Cocoa",
    "pyobjc-framework-Quartz",
    "pyobjc-framework-Security",
    "pyobjc-framework-UniformTypeIdentifiers",
    "pyobjc-framework-WebKit",
    "python-dotenv",
    "python-multipart",
    "pywebview",
    "referencing",
    "rpds-py",
    "sniffio",
    "sse-starlette",
    "starlette",
    "tqdm",
    "typing-inspection",
    "typing_extensions",
    "uvicorn",
    "websockets",
)
PACKAGING_RUNTIME_NOTICE_DISTRIBUTIONS = (
    "pyinstaller",
    "pyinstaller-hooks-contrib",
)
metadata_datas = [
    data
    for distribution_name in (
        *PYTHON_RUNTIME_DISTRIBUTIONS,
        *PACKAGING_RUNTIME_NOTICE_DISTRIBUTIONS,
    )
    for data in copy_metadata(distribution_name)
]

datas = [
    (str(PACKAGE_ROOT / "templates"), "name_atlas/templates"),
    (str(PACKAGE_ROOT / "static"), "name_atlas/static"),
    (str(PACKAGE_ROOT / "recordings"), "name_atlas/recordings"),
    (
        str(PACKAGE_ROOT / "assets" / "chatgpt-widget"),
        "name_atlas/assets/chatgpt-widget",
    ),
    (str(PROJECT_ROOT / "LICENSE"), "."),
    (str(PROJECT_ROOT / "THIRD_PARTY_NOTICES.md"), "."),
    (str(PYTHON_LICENSE), "licenses/cpython-3.11.9"),
    (str(PYTHON_LICENSE_APPENDIX), "licenses/cpython-3.11.9"),
] + metadata_datas
hiddenimports = sorted(
    set(
        [
            "AppKit",
            "Foundation",
            "PyObjCTools.AppHelper",
            "Quartz",
            "Security",
            "WebKit",
            "mcp.server.fastmcp",
            "mcp.server.streamable_http",
            "mcp.server.streamable_http_manager",
            "name_atlas.foldweave_chatgpt_mcp",
            "name_atlas.foldweave_companion_client",
            "name_atlas.foldweave_companion_supervisor",
            "uvicorn.lifespan.on",
            "uvicorn.loops.asyncio",
            "uvicorn.protocols.http.h11_impl",
            "webview.platforms.cocoa",
        ]
    )
)
excluded_build_and_test_modules = [
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
]

analysis = Analysis(
    [str(ENTRY_POINT)],
    pathex=[str(SOURCE_ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(HOOKS_ROOT)],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_build_and_test_modules,
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
    icon=str(ICON_PATH),
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
