"""Acceptance checks for the thin repository-backed Codex plugin."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPOSITORY / "plugins/foldweave"
LEGACY_PLUGIN_ROOT = REPOSITORY / "plugins/name-atlas"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin/plugin.json"
MCP_CONFIG = PLUGIN_ROOT / ".mcp.json"
MARKETPLACE = REPOSITORY / ".agents/plugins/marketplace.json"


def _json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_plugin_manifest_is_thin_and_points_to_the_shared_mcp_config() -> None:
    manifest = _json(PLUGIN_MANIFEST)

    assert manifest["name"] == "foldweave"
    version = manifest["version"]
    assert isinstance(version, str)
    assert re.fullmatch(r"0\.1\.0(?:\+codex\.[0-9A-Za-z.-]+)?", version)
    assert version.count("+codex.") <= 1
    assert manifest["mcpServers"] == "./.mcp.json"
    assert "skills" not in manifest
    assert "apps" not in manifest
    assert "hooks" not in manifest
    assert "[TODO:" not in PLUGIN_MANIFEST.read_text(encoding="utf-8")
    interface = manifest["interface"]
    assert isinstance(interface, dict)
    assert interface["displayName"] == "Foldweave"
    assert interface["shortDescription"] == (
        "Change the structure. Keep the connections."
    )
    assert interface["category"] == "Productivity"
    assert len(interface["defaultPrompt"]) == 3


def test_plugin_launches_the_existing_server_without_a_developer_path() -> None:
    configuration = _json(MCP_CONFIG)

    assert configuration == {
        "mcpServers": {
            "foldweave": {
                "command": "uv",
                "args": [
                    "run",
                    "--frozen",
                    "foldweave",
                    "mcp",
                    "--transport",
                    "stdio",
                ],
            }
        }
    }
    assert str(REPOSITORY) not in MCP_CONFIG.read_text(encoding="utf-8")


def test_repository_marketplace_uses_one_relative_plugin_entry() -> None:
    marketplace = _json(MARKETPLACE)

    assert marketplace["name"] == "personal"
    assert marketplace["plugins"] == [
        {
            "name": "foldweave",
            "source": {"source": "local", "path": "./plugins/foldweave"},
            "policy": {
                "installation": "AVAILABLE",
                "authentication": "ON_INSTALL",
            },
            "category": "Productivity",
        }
    ]


def test_plugin_documents_install_use_and_uninstall_from_a_clean_clone() -> None:
    readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")

    for required_text in (
        "uv sync --frozen",
        "/Applications/ChatGPT.app/Contents/Resources/codex",
        '"$CODEX_BIN" plugin marketplace add .',
        '"$CODEX_BIN" plugin add foldweave@personal',
        '"$CODEX_BIN" plugin remove foldweave@personal',
        "create_or_resume_planning_job",
        "submit_plan_revision",
        "get_plan_preview",
        "prepare_change_application",
        "accept_plan_and_create_copy",
        "get_change_file",
        "recreate_original",
        "Codex supplies model inference",
    ):
        assert required_text in readme


def test_active_plugin_surfaces_use_only_foldweave_branding() -> None:
    active_paths = (
        MARKETPLACE,
        PLUGIN_MANIFEST,
        MCP_CONFIG,
        PLUGIN_ROOT / "README.md",
    )
    predecessor_branding = (
        "Reversible Name Atlas",
        "Name Atlas",
        "name-atlas",
    )

    for path in active_paths:
        text = path.read_text(encoding="utf-8")
        for predecessor in predecessor_branding:
            assert predecessor not in text

    assert not any(path.is_file() for path in LEGACY_PLUGIN_ROOT.rglob("*"))
