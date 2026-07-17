"""Judge-facing CLI tests."""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from name_atlas import cli
from name_atlas.receiver_verifier import ReceiptVerificationStatus


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
    case_path = tmp_path / "selected-package-case.json"

    exit_code = cli.run(
        [
            "demo",
            "--mode",
            "replay",
            "--source",
            str(source),
            "--output",
            str(output),
            "--case",
            str(case_path),
        ],
        environ={},
    )

    assert exit_code == 0
    workflow = called["app"].state.workflow
    assert workflow.package.root == source.resolve()
    assert workflow.output_root == output.resolve()
    assert workflow.case is not None
    assert workflow.case.local_paths.case_path == case_path.resolve()
    assert workflow.replay_record_path is None


def test_verify_receipt_dispatches_before_demo_or_provider_initialization(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = tmp_path / "received-bag"
    candidate.mkdir()
    provider_initialized = False

    def fail_if_provider_initializes(*args: Any, **kwargs: Any) -> None:
        nonlocal provider_initialized
        del args, kwargs
        provider_initialized = True

    monkeypatch.setattr(
        cli.LiveDecisionCardProvider,
        "from_api_key",
        fail_if_provider_initializes,
    )
    monkeypatch.setattr(
        cli,
        "verify_receipt",
        lambda *args, **kwargs: SimpleNamespace(
            status=ReceiptVerificationStatus.VERIFIED,
            receipt_fingerprint="a" * 64,
            failed_check_ids=(),
        ),
    )

    exit_code = cli.run(["verify-receipt", str(candidate)], environ={})

    assert exit_code == 0
    assert provider_initialized is False
    assert capsys.readouterr().out == f"VERIFIED {'a' * 64}\n"


def test_verify_receipt_reports_stable_blockers(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = tmp_path / "received-bag"
    candidate.mkdir()
    monkeypatch.setattr(
        cli,
        "verify_receipt",
        lambda *args, **kwargs: SimpleNamespace(
            status=ReceiptVerificationStatus.BLOCKED,
            receipt_fingerprint="b" * 64,
            failed_check_ids=("artifact_digest_mismatch:decision_ledger",),
        ),
    )

    exit_code = cli.run(["verify-receipt", str(candidate)], environ={})

    assert exit_code == 1
    assert capsys.readouterr().out == (
        "BLOCKED artifact_digest_mismatch:decision_ledger\n"
    )


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


def test_replay_compatibility_failure_releases_case_writer(
    monkeypatch: Any,
    capsys: Any,
) -> None:
    state = {"closed": False, "server_started": False}

    class IncompatibleWorkflow:
        case = None

        def __init__(self, **kwargs: Any) -> None:
            del kwargs

        def require_replay_record_compatible(self) -> None:
            raise cli.DecisionCardProviderError("record mismatch")

        def close(self) -> None:
            state["closed"] = True

    def fake_run(app: Any, **kwargs: Any) -> None:
        del app, kwargs
        state["server_started"] = True

    monkeypatch.setattr(cli, "WorkflowSession", IncompatibleWorkflow)
    monkeypatch.setattr(cli.uvicorn, "run", fake_run)

    exit_code = cli.run(["demo", "--mode", "replay"], environ={})

    assert exit_code == 2
    assert state == {"closed": True, "server_started": False}
    assert "Replay startup blocked: record mismatch" in capsys.readouterr().err
