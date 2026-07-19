"""F0a launch-contract tests for the Foldweave browser application."""

from __future__ import annotations

from pathlib import Path

import pytest

from name_atlas import foldweave_browser_cli, foldweave_launcher


def test_foldweave_help_exposes_only_truthful_current_app_surface(capsys) -> None:
    assert foldweave_launcher.run(["--help"]) == 0

    output = capsys.readouterr()
    assert output.err == ""
    assert "app" in output.out
    assert "review" in output.out.lower()
    assert "live" not in output.out.lower()


def test_foldweave_app_parser_accepts_exact_development_browser_contract() -> None:
    args = foldweave_browser_cli.build_foldweave_app_parser().parse_args(
        [
            "--browser",
            "--mode",
            "development",
            "--source",
            "/tmp/source",
            "--output",
            "/tmp/output",
            "--job",
            "/tmp/job.json",
            "--port",
            "8765",
        ]
    )

    assert args.browser is True
    assert args.mode == "development"
    assert args.source == Path("/tmp/source")
    assert args.output == Path("/tmp/output")
    assert args.job == Path("/tmp/job.json")
    assert args.port == 8765


def test_default_job_uses_application_support_and_absolute_override(
    tmp_path: Path,
) -> None:
    default = foldweave_browser_cli.default_foldweave_job_path(environ={})
    override = foldweave_browser_cli.default_foldweave_job_path(
        environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")}
    )

    assert default == (
        Path.home()
        / "Library"
        / "Application Support"
        / "Foldweave"
        / "jobs"
        / "active.json"
    ).resolve(strict=False)
    assert override == (tmp_path / "state" / "jobs" / "active.json").resolve(
        strict=False
    )
    with pytest.raises(ValueError, match="must be an absolute path"):
        foldweave_browser_cli.default_foldweave_job_path(
            environ={"FOLDWEAVE_STATE_ROOT": "relative/state"}
        )


def test_f0a_launch_injects_review_service_and_never_starts_provider(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    job = tmp_path / "jobs" / "review.json"
    captured: dict[str, object] = {}

    class CapturedReviewService:
        def __init__(self, *, job_path: Path) -> None:
            captured["job_path"] = job_path

    def capture_app(service: object, **kwargs: object) -> object:
        captured["service"] = service
        captured.update(kwargs)
        return object()

    def capture_uvicorn(app: object, **kwargs: object) -> None:
        captured["app"] = app
        captured["uvicorn"] = kwargs

    monkeypatch.setattr(
        foldweave_browser_cli,
        "FoldweaveBrowserReviewService",
        CapturedReviewService,
    )
    monkeypatch.setattr(foldweave_browser_cli, "create_folder_app", capture_app)
    monkeypatch.setattr(foldweave_browser_cli.uvicorn, "run", capture_uvicorn)

    result = foldweave_browser_cli.run_foldweave_app(
        [
            "--browser",
            "--mode",
            "development",
            "--source",
            str(source),
            "--output",
            str(output),
            "--job",
            str(job),
            "--port",
            "8765",
        ]
    )

    assert result == 0
    assert captured["job_path"] == job.resolve(strict=False)
    assert captured["initial_source"] == source.resolve(strict=True)
    assert captured["initial_output_parent"] == output.resolve(strict=True)
    assert captured["uvicorn"] == {
        "host": "127.0.0.1",
        "port": 8765,
        "log_level": "info",
    }
    stdout = capsys.readouterr().out
    assert "Deterministic development review" in stdout
    assert "no OpenAI API call" in stdout
    assert "FolderRefactorJobV3" in stdout


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (["--mode", "development"], "pass --browser"),
        (
            ["--browser", "--mode", "development", "--port", "0"],
            "port must be between 1 and 65535",
        ),
    ],
)
def test_f0a_launch_refuses_unavailable_or_invalid_runtime(
    arguments: list[str],
    message: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert foldweave_browser_cli.run_foldweave_app(arguments) == 2
    assert message in capsys.readouterr().err


def test_foldweave_launcher_dispatches_app_without_legacy_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[str] = []

    monkeypatch.setattr(
        foldweave_browser_cli,
        "run_foldweave_app",
        lambda arguments: captured.extend(arguments) or 0,
    )

    assert foldweave_launcher.run(["app", "--browser", "--mode", "development"]) == 0
    assert captured == ["--browser", "--mode", "development"]
