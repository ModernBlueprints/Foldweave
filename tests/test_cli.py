"""Judge-facing CLI tests."""

from pathlib import Path
from typing import Any

from name_atlas import cli


def test_live_mode_fails_clearly_without_api_key(capsys: Any) -> None:
    exit_code = cli.run(["demo", "--mode", "live"], environ={})

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "configure OPENAI_API_KEY locally" in captured.err


def test_replay_mode_runs_on_loopback(monkeypatch: Any) -> None:
    called: dict[str, Any] = {}

    def fake_run(app: Any, **kwargs: Any) -> None:
        called["app"] = app
        called.update(kwargs)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)

    exit_code = cli.run(
        ["demo", "--mode", "replay", "--port", "8123"],
        environ={},
    )

    assert exit_code == 0
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8123
    assert called["app"].title == "Reversible Name Atlas"
    runtime_config = called["app"].state.runtime_config
    assert runtime_config.replay_record_configured is True
    assert runtime_config.provider_status == "Recorded GPT-5.6 response"


def test_selected_supported_package_reaches_the_local_workbench(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    called: dict[str, Any] = {}

    def fake_run(app: Any, **kwargs: Any) -> None:
        called["app"] = app
        called.update(kwargs)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)
    source = cli.PROJECT_ROOT / "sample_data" / "negative_unresolved_meaning"
    output = tmp_path / "selected-package-stage"

    exit_code = cli.run(
        [
            "demo",
            "--mode",
            "replay",
            "--source",
            str(source),
            "--output",
            str(output),
        ],
        environ={},
    )

    assert exit_code == 0
    workflow = called["app"].state.workflow
    assert workflow.package.root == source.resolve()
    assert workflow.output_root == output.resolve()
    assert workflow.replay_record_path is None


def test_invalid_selected_package_fails_before_server_start(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    server_started = False

    def fake_run(app: Any, **kwargs: Any) -> None:
        nonlocal server_started
        del app, kwargs
        server_started = True

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)

    exit_code = cli.run(
        ["demo", "--mode", "replay", "--source", str(tmp_path / "absent")],
        environ={},
    )

    assert exit_code == 2
    assert server_started is False
    assert "Startup blocked:" in capsys.readouterr().err
