"""Acceptance checks for the thin repository-backed Codex plugin."""

from __future__ import annotations

import json
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPOSITORY / "plugins/name-atlas"
PLUGIN_MANIFEST = PLUGIN_ROOT / ".codex-plugin/plugin.json"
MCP_CONFIG = PLUGIN_ROOT / ".mcp.json"
MARKETPLACE = REPOSITORY / ".agents/plugins/marketplace.json"


def _json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_plugin_manifest_is_thin_and_points_to_the_shared_mcp_config() -> None:
    manifest = _json(PLUGIN_MANIFEST)

    assert manifest["name"] == "name-atlas"
    assert manifest["version"] == "0.1.0"
    assert manifest["mcpServers"] == "./.mcp.json"
    assert "skills" not in manifest
    assert "apps" not in manifest
    assert "hooks" not in manifest
    assert "[TODO:" not in PLUGIN_MANIFEST.read_text(encoding="utf-8")
    interface = manifest["interface"]
    assert isinstance(interface, dict)
    assert interface["displayName"] == "Reversible Name Atlas"
    assert interface["category"] == "Productivity"
    assert len(interface["defaultPrompt"]) == 3


def test_plugin_launches_the_existing_server_without_a_developer_path() -> None:
    configuration = _json(MCP_CONFIG)

    assert configuration == {
        "mcpServers": {
            "name-atlas": {
                "command": "uv",
                "args": ["run", "--frozen", "name-atlas", "mcp"],
            }
        }
    }
    assert str(REPOSITORY) not in MCP_CONFIG.read_text(encoding="utf-8")


def test_repository_marketplace_uses_one_relative_plugin_entry() -> None:
    marketplace = _json(MARKETPLACE)

    assert marketplace["name"] == "personal"
    assert marketplace["plugins"] == [
        {
            "name": "name-atlas",
            "source": {"source": "local", "path": "./plugins/name-atlas"},
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
        "codex plugin marketplace add .",
        "codex plugin add name-atlas@personal",
        "codex plugin remove name-atlas@personal",
        "plan_and_create_copy",
        "apply_change_file",
        "OPENAI_API_KEY",
    ):
        assert required_text in readme
