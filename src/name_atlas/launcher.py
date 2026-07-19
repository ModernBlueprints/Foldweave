"""Minimal console launcher with provider-free early command dispatch."""

from __future__ import annotations

import sys
from collections.abc import Sequence


def run(argv: Sequence[str] | None = None) -> int:
    """Dispatch commands before importing unrelated runtime authorities."""

    arguments = list(sys.argv[1:] if argv is None else argv)
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
