"""Minimal console launcher with provider-free early command dispatch."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

COMMAND_HELP = (
    ("demo", "Run the bundled live or recorded Connected Change demonstration."),
    ("run", "Run the local Connected Change browser application."),
    ("apply-change", "Apply a Name Atlas Change File without GPT or an API key."),
    ("verify-receipt", "Independently verify a portable Name Atlas result."),
    ("restore-receipt", "Recreate the original layout from a verified result."),
    ("mcp", "Run the shared seven-tool Name Atlas STDIO MCP server."),
)


def build_root_parser() -> argparse.ArgumentParser:
    """Build the complete provider-free top-level command index."""

    parser = argparse.ArgumentParser(
        prog="name-atlas",
        description=(
            "Plan, apply, verify, and reconstruct connected-folder changes "
            "without modifying the selected source folder."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    for command, help_text in COMMAND_HELP:
        subparsers.add_parser(command, add_help=False, help=help_text)
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Dispatch commands before importing unrelated runtime authorities."""

    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        build_root_parser().print_help(sys.stderr)
        return 2
    if arguments[0] in {"-h", "--help"}:
        build_root_parser().print_help()
        return 0
    if arguments and arguments[0] == "mcp":
        from name_atlas.mcp_server import run_mcp_server

        return run_mcp_server(arguments[1:])
    if arguments and arguments[0] == "apply-change":
        from name_atlas.connected_cli import run_apply_change

        return run_apply_change(arguments[1:])
    if arguments and arguments[0] == "run":
        from name_atlas.connected_browser_cli import run_connected_browser

        return run_connected_browser(arguments[1:])
    if arguments and arguments[0] == "demo":
        from name_atlas.connected_browser_cli import run_connected_demo

        return run_connected_demo(arguments[1:])

    from name_atlas.cli import run as run_legacy_cli

    return run_legacy_cli(arguments)


def main() -> None:
    """Console-script entry point."""

    raise SystemExit(run())


if __name__ == "__main__":
    main()
