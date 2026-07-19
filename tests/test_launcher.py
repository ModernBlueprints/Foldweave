"""Release-facing tests for the lazy top-level command index."""

from __future__ import annotations

from name_atlas.launcher import run


def test_top_level_help_lists_every_supported_release_command(capsys) -> None:
    assert run(["--help"]) == 0

    output = capsys.readouterr()
    assert output.err == ""
    for command in (
        "demo",
        "run",
        "apply-change",
        "verify-receipt",
        "restore-receipt",
        "mcp",
    ):
        assert command in output.out
    normalized = " ".join(output.out.split())
    assert "without modifying the selected source folder" in normalized


def test_no_command_prints_complete_help_and_returns_usage_error(capsys) -> None:
    assert run([]) == 2

    output = capsys.readouterr()
    assert output.out == ""
    assert "apply-change" in output.err
    assert "mcp" in output.err
