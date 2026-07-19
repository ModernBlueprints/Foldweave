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

    print(f"foldweave: unknown command: {arguments[0]}", file=sys.stderr)
    build_root_parser().print_help(sys.stderr)
    return 2


def main() -> None:
    """Console-script entry point."""

    raise SystemExit(run())


if __name__ == "__main__":
    main()
