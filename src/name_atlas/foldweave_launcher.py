"""Minimal Foldweave command launcher with truthful early dispatch."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

COMMAND_HELP = (
    (
        "app",
        "Run the native Foldweave review application or its browser fallback.",
    ),
    (
        "mcp",
        "Run the provider-free Foldweave hosted-planning MCP Apps server.",
    ),
    (
        "companion",
        "Pair or run the outbound-only Foldweave ChatGPT companion.",
    ),
    ("demo", "Prepare the bundled recorded proposal for review."),
    ("run", "Prepare a connected-folder proposal for exact review."),
    ("apply-change", "Prepare a shared change for receiver-local review."),
    ("preview", "Inspect the exact persisted review DTO."),
    ("revise", "Request one bounded revision of a reviewed proposal."),
    ("accept", "Accept one exact preview and create a verified copy."),
    ("verify-receipt", "Independently verify a portable result."),
    ("restore-receipt", "Recreate the source selected for one transaction."),
)


def build_root_parser() -> argparse.ArgumentParser:
    """Build the provider-free Foldweave command index."""

    parser = argparse.ArgumentParser(
        prog="foldweave",
        description=(
            "Review a connected-folder structure before creating a separate copy."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")
    for command, help_text in COMMAND_HELP:
        subparsers.add_parser(command, add_help=False, help=help_text)
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Dispatch supported commands before importing application authorities."""

    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments:
        build_root_parser().print_help(sys.stderr)
        return 2
    if arguments[0] in {"-h", "--help"}:
        build_root_parser().print_help()
        return 0
    if arguments[0] == "app":
        from name_atlas.foldweave_native_cli import run_foldweave_app

        return run_foldweave_app(arguments[1:])
    if arguments[0] == "mcp":
        from name_atlas.foldweave_chatgpt_mcp import run_foldweave_mcp_server

        return run_foldweave_mcp_server(arguments[1:])
    if arguments[0] == "companion":
        from name_atlas.foldweave_companion_cli import run_foldweave_companion

        return run_foldweave_companion(arguments[1:])
    if arguments[0] in {
        "run",
        "apply-change",
        "preview",
        "revise",
        "accept",
        "verify-receipt",
        "restore-receipt",
    }:
        from name_atlas import foldweave_review_cli

        dispatch = {
            "run": foldweave_review_cli.run_prepare_origin,
            "apply-change": foldweave_review_cli.run_prepare_application,
            "preview": foldweave_review_cli.run_preview,
            "revise": foldweave_review_cli.run_revise,
            "accept": foldweave_review_cli.run_accept,
            "verify-receipt": foldweave_review_cli.run_legacy_verify,
            "restore-receipt": foldweave_review_cli.run_legacy_restore,
        }
        return dispatch[arguments[0]](arguments[1:])
    if arguments[0] == "demo":
        from name_atlas.foldweave_demo_cli import run_foldweave_demo

        return run_foldweave_demo(arguments[1:])

    print(f"foldweave: unknown command: {arguments[0]}", file=sys.stderr)
    build_root_parser().print_help(sys.stderr)
    return 2


def main() -> None:
    """Console-script entry point."""

    raise SystemExit(run())


if __name__ == "__main__":
    main()
