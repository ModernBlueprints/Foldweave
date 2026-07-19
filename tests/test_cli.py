"""Judge-facing CLI tests."""

import asyncio
import os
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from name_atlas import cli
from name_atlas.cases import CaseLifecycle, MigrationCaseStore
from name_atlas.folder_refactor import reconstruction
from name_atlas.receiver_verifier import ReceiptVerificationStatus


def test_runtime_roots_use_checkout_fixture_only_for_a_real_checkout(
    tmp_path: Path,
) -> None:
    checkout_root = tmp_path / "checkout"
    package_root = checkout_root / "src" / "name_atlas"
    package_root.mkdir(parents=True)
    (checkout_root / "pyproject.toml").touch()

    project_root, hero_root = cli._runtime_roots(package_root, tmp_path / "runner")

    assert project_root == checkout_root
    assert hero_root == checkout_root / "sample_data" / "hero"


def test_runtime_roots_prevent_invocation_directory_from_shadowing_wheel_hero(
    tmp_path: Path,
) -> None:
    package_root = tmp_path / "venv" / "site-packages" / "name_atlas"
    package_root.mkdir(parents=True)
    working_directory = tmp_path / "runner"
    (working_directory / "sample_data" / "hero").mkdir(parents=True)

    project_root, hero_root = cli._runtime_roots(package_root, working_directory)

    assert project_root == working_directory
    assert hero_root == package_root / "sample_data" / "hero"


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


def test_ai_first_development_run_is_a_supported_loopback_command(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    called: dict[str, Any] = {}
    source = tmp_path / "ordinary-folder"
    source.mkdir()
    (source / "note.txt").write_text("one file\n", encoding="utf-8")
    output = tmp_path / "results"
    output.mkdir()
    job_path = tmp_path / "jobs" / "folder-job.json"

    def fake_run(app: Any, **kwargs: Any) -> None:
        called["app"] = app
        called.update(kwargs)

    def fail_if_provider_initializes(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise AssertionError("A2 development mode must not initialize a provider.")

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)
    monkeypatch.setattr(
        cli.LiveDecisionCardProvider,
        "from_api_key",
        fail_if_provider_initializes,
    )

    exit_code = cli.run(
        [
            "run",
            "--mode",
            "development",
            "--source",
            str(source),
            "--output",
            str(output),
            "--job",
            str(job_path),
            "--port",
            "8124",
        ],
        environ={},
    )

    assert exit_code == 0
    assert called["host"] == "127.0.0.1"
    assert called["port"] == 8124
    assert called["app"].title == "Reversible Name Atlas"
    assert called["app"].state.folder_run_service.job_path == job_path.resolve()
    captured = capsys.readouterr()
    assert cli.PLANNER_LABEL in captured.out
    assert f"FolderRefactorJob: {job_path.resolve()}" in captured.out


def test_ai_first_development_run_rejects_invalid_startup_paths_and_port(
    tmp_path: Path,
    capsys: Any,
) -> None:
    output = tmp_path / "results"
    output.mkdir()

    missing_exit = cli.run(
        [
            "run",
            "--mode",
            "development",
            "--source",
            str(tmp_path / "missing"),
            "--output",
            str(output),
        ],
        environ={},
    )
    invalid_port_exit = cli.run(
        [
            "run",
            "--mode",
            "development",
            "--source",
            str(tmp_path),
            "--output",
            str(output),
            "--port",
            "70000",
        ],
        environ={},
    )

    assert missing_exit == 2
    assert invalid_port_exit == 2
    assert "Startup blocked:" in capsys.readouterr().err


def test_development_default_output_cannot_mutate_selected_source(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    source = tmp_path / "selected-source"
    source.mkdir()
    (source / "user.txt").write_text("keep me\n", encoding="utf-8")
    proposed_output = source / ".name-atlas" / "folder-results"
    job_path = tmp_path / "jobs" / "safe-job.json"
    monkeypatch.setattr(cli, "FOLDER_OUTPUT_ROOT", proposed_output)

    def fail_if_server_starts(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("Server must not start for overlapping paths.")

    monkeypatch.setattr(cli.uvicorn, "run", fail_if_server_starts)

    exit_code = cli.run(
        [
            "run",
            "--mode",
            "development",
            "--source",
            str(source),
            "--job",
            str(job_path),
        ],
        environ={},
    )

    assert exit_code == 2
    assert not proposed_output.exists()
    assert sorted(path.name for path in source.iterdir()) == ["user.txt"]
    assert "may not contain one another" in capsys.readouterr().err


def test_replay_cli_resumes_a_durable_post_decision_case(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    case_path = tmp_path / "ready-case.json"
    output = tmp_path / "stages"
    workflow = cli.WorkflowSession(
        source_root=cli.HERO_SOURCE_ROOT,
        output_root=output,
        decision_card_provider=cli.RecordedReplayDecisionCardProvider(
            cli.REPLAY_RECORD_PATH.read_bytes()
        ),
        package_validator=cli.BagItPackageValidator(),
        replay_record_path=cli.REPLAY_RECORD_PATH,
        case_path=case_path,
    )
    try:
        meaning_family = next(
            family
            for family in workflow.package.families
            if family.canonical_identifier == "NA-0001"
        )
        collision_family = next(
            family
            for family in workflow.package.families
            if family.canonical_identifier == "CASE-010"
        )
        asyncio.run(workflow.generate_card(meaning_family.family_id))
        workflow.approve_low_risk()
        workflow.edit(collision_family.family_id, "harbor-map-north")
        workflow.approve_low_risk()
        workflow.edit(meaning_family.family_id, "campaign-poster")
    finally:
        workflow.close()

    called: dict[str, Any] = {}

    def fake_run(app: Any, **kwargs: Any) -> None:
        called["app"] = app
        called.update(kwargs)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)
    exit_code = cli.run(
        [
            "demo",
            "--mode",
            "replay",
            "--source",
            str(cli.HERO_SOURCE_ROOT),
            "--output",
            str(output),
            "--case",
            str(case_path),
        ],
        environ={},
    )

    assert exit_code == 0
    resumed = called["app"].state.workflow
    assert resumed.view_model()["export_ready"] is True
    assert called["app"].state.runtime_config.replay_record_configured is True
    assert called["app"].state.runtime_config.provider_status == (
        "Recorded GPT-5.6 response"
    )


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


def test_folder_verify_receipt_dispatches_before_all_runtime_initialization(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")
    source = tmp_path / "optional-source"
    source.mkdir()
    called: dict[str, Any] = {}

    def fail_runtime_initialization(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise AssertionError("Receipt verification initialized a runtime service.")

    def fake_verify(
        result_root: Path,
        *,
        source_root: Path | None = None,
    ) -> SimpleNamespace:
        called["result_root"] = result_root
        called["source_root"] = source_root
        return SimpleNamespace(
            status=cli.FolderReceiptVerificationStatus.VERIFIED,
            receipt_fingerprint="c" * 64,
            failed_check_ids=(),
        )

    monkeypatch.setattr(cli, "verify_folder_receipt", fake_verify)
    monkeypatch.setattr(cli, "verify_receipt", fail_runtime_initialization)
    monkeypatch.setattr(
        cli.LiveDecisionCardProvider,
        "from_api_key",
        fail_runtime_initialization,
    )
    monkeypatch.setattr(cli, "WorkflowSession", fail_runtime_initialization)
    monkeypatch.setattr(cli, "JobBackedFolderRunService", fail_runtime_initialization)
    monkeypatch.setattr(cli.uvicorn, "run", fail_runtime_initialization)

    exit_code = cli.run(
        ["verify-receipt", str(candidate), "--source", str(source)],
        environ={"OPENAI_API_KEY": "must-not-be-read"},
    )

    assert exit_code == 0
    assert called == {"result_root": candidate, "source_root": source}
    captured = capsys.readouterr()
    assert captured.out == f"VERIFIED {'c' * 64}\n"
    assert captured.err == ""


def test_folder_verify_receipt_reports_stable_blockers(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")
    monkeypatch.setattr(
        cli,
        "verify_folder_receipt",
        lambda *args, **kwargs: SimpleNamespace(
            status=cli.FolderReceiptVerificationStatus.BLOCKED,
            receipt_fingerprint="d" * 64,
            failed_check_ids=("artifact_digest_mismatch:accepted_plan",),
        ),
    )

    exit_code = cli.run(["verify-receipt", str(candidate)], environ={})

    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == "BLOCKED artifact_digest_mismatch:accepted_plan\n"
    assert captured.err == ""


def test_folder_verify_receipt_candidate_error_returns_two(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")

    def fail_candidate(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise cli.FolderReceiptCandidateError("candidate cannot be opened")

    monkeypatch.setattr(cli, "verify_folder_receipt", fail_candidate)

    exit_code = cli.run(["verify-receipt", str(candidate)], environ={})

    assert exit_code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Receipt input error: candidate cannot be opened\n"


def test_unknown_folder_receipt_version_blocks_without_archive_dispatch(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v999")

    def fail_other_dispatch(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise AssertionError("Unknown folder receipt reached another verifier.")

    monkeypatch.setattr(cli, "verify_folder_receipt", fail_other_dispatch)
    monkeypatch.setattr(cli, "verify_receipt", fail_other_dispatch)

    assert cli.run(["verify-receipt", str(candidate)], environ={}) == 1
    captured = capsys.readouterr()
    assert captured.out == "BLOCKED receipt_schema_invalid\n"
    assert captured.err == ""


def test_unknown_folder_receipt_version_blocks_reconstruction_dispatch(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v999")
    destination = tmp_path / "recreated-original"

    def fail_other_dispatch(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise AssertionError("Unknown folder receipt reached reconstruction.")

    monkeypatch.setattr(cli, "_restore_folder_receipt", fail_other_dispatch)
    monkeypatch.setattr(cli, "restore_receipt", fail_other_dispatch)

    assert (
        cli.run(
            ["restore-receipt", str(candidate), str(destination)],
            environ={},
        )
        == 1
    )
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "RESTORE BLOCKED receipt_schema_invalid\n"


def test_damaged_folder_receipt_still_dispatches_by_portable_snapshot(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = tmp_path / "damaged-folder-result"
    proof_root = candidate / "name-atlas"
    proof_root.mkdir(parents=True)
    (proof_root / "change_receipt.json").write_bytes(b"{")
    (proof_root / "source_snapshot.json").write_text(
        '{"schema_version":"folder-inventory.v1"}',
        encoding="utf-8",
    )

    def fail_archive_dispatch(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise AssertionError("Damaged generic receipt reached archive verification.")

    monkeypatch.setattr(cli, "verify_receipt", fail_archive_dispatch)
    monkeypatch.setattr(
        cli,
        "verify_folder_receipt",
        lambda *args, **kwargs: SimpleNamespace(
            status=cli.FolderReceiptVerificationStatus.BLOCKED,
            receipt_fingerprint=None,
            failed_check_ids=("receipt_schema_invalid",),
        ),
    )

    exit_code = cli.run(["verify-receipt", str(candidate)], environ={})

    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == "BLOCKED receipt_schema_invalid\n"
    assert captured.err == ""


def test_folder_restore_receipt_dispatches_before_all_runtime_initialization(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")
    destination = tmp_path / "recreated-original"
    called: dict[str, Path] = {}

    def fail_runtime_initialization(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise AssertionError("Reconstruction initialized a runtime service.")

    def fake_restore(result_root: Path, restore_destination: Path) -> SimpleNamespace:
        called["result_root"] = result_root
        called["destination"] = restore_destination
        return SimpleNamespace(
            receipt_fingerprint="e" * 64,
            destination=restore_destination.resolve(),
        )

    monkeypatch.setattr(cli, "_restore_folder_receipt", fake_restore)
    monkeypatch.setattr(cli, "restore_receipt", fail_runtime_initialization)
    monkeypatch.setattr(
        cli.LiveDecisionCardProvider,
        "from_api_key",
        fail_runtime_initialization,
    )
    monkeypatch.setattr(cli, "WorkflowSession", fail_runtime_initialization)
    monkeypatch.setattr(cli, "JobBackedFolderRunService", fail_runtime_initialization)
    monkeypatch.setattr(cli.uvicorn, "run", fail_runtime_initialization)

    exit_code = cli.run(
        ["restore-receipt", str(candidate), str(destination)],
        environ={"OPENAI_API_KEY": "must-not-be-read"},
    )

    assert exit_code == 0
    assert called == {"result_root": candidate, "destination": destination}
    captured = capsys.readouterr()
    assert captured.out == f"RESTORED {'e' * 64} {destination.resolve()}\n"
    assert captured.err == ""


def test_folder_restore_receipt_exposes_bounded_failure_code(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")
    destination = tmp_path / "recreated-original"

    def fail_restore(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise cli._FolderRestoreBlocked(
            "receipt_verification_blocked",
            ("artifact_digest_mismatch:accepted_plan",),
        )

    monkeypatch.setattr(cli, "_restore_folder_receipt", fail_restore)

    exit_code = cli.run(
        ["restore-receipt", str(candidate), str(destination)],
        environ={},
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == (
        "RESTORE BLOCKED receipt_verification_blocked "
        "artifact_digest_mismatch:accepted_plan\n"
    )


def test_folder_restore_receipt_candidate_error_returns_two(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")
    destination = tmp_path / "recreated-original"

    def fail_candidate(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise cli.FolderReceiptCandidateError("candidate cannot be opened")

    monkeypatch.setattr(cli, "_restore_folder_receipt", fail_candidate)

    exit_code = cli.run(
        ["restore-receipt", str(candidate), str(destination)],
        environ={},
    )

    assert exit_code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "Restore input error: candidate cannot be opened\n"


def test_folder_restore_adapter_preserves_reconstruction_failure_code(
    monkeypatch: Any,
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = _receipt_schema_candidate(tmp_path, "folder-change-receipt.v1")
    destination = tmp_path / "recreated-original"

    def fail_reparse(_result_root: Path, _destination: Path) -> None:
        raise reconstruction.FolderReconstructionError(
            "receipt_reparse_failed",
            "portable authorities changed",
        )

    monkeypatch.setattr(reconstruction, "restore_folder_receipt", fail_reparse)

    exit_code = cli.run(
        ["restore-receipt", str(candidate), str(destination)],
        environ={},
    )

    assert exit_code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "RESTORE BLOCKED receipt_reparse_failed\n"


def test_verify_receipt_symlink_loop_is_a_usage_error(
    tmp_path: Path,
    capsys: Any,
) -> None:
    candidate = tmp_path / "received-bag"
    os.symlink(candidate.name, candidate)

    exit_code = cli.run(["verify-receipt", str(candidate)], environ={})

    captured = capsys.readouterr()
    assert exit_code == 2
    assert captured.out == ""
    assert captured.err.startswith("Receipt input error:")


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


def test_existing_case_records_disappeared_source_and_starts_blocked_view(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    started_apps: list[Any] = []

    def fake_run(app: Any, **kwargs: Any) -> None:
        del kwargs
        started_apps.append(app)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)
    source = tmp_path / "case-source"
    output = tmp_path / "case-stages"
    case_path = tmp_path / "persisted-case.json"
    shutil.copytree(cli.HERO_SOURCE_ROOT, source)
    arguments = [
        "demo",
        "--mode",
        "replay",
        "--source",
        str(source),
        "--output",
        str(output),
        "--case",
        str(case_path),
    ]

    assert cli.run(arguments, environ={}) == 0
    assert case_path.is_file()
    shutil.rmtree(source)

    assert cli.run(arguments, environ={}) == 0

    resumed_workflow = started_apps[-1].state.workflow
    assert resumed_workflow.case is not None
    assert resumed_workflow.case.lifecycle is CaseLifecycle.STALE
    assert resumed_workflow.case.source_scan_blocker is not None
    assert resumed_workflow.case.source_scan_blocker.code.value == "source_scan_failed"
    assert str(source.resolve(strict=False)) in (
        resumed_workflow.case.source_scan_blocker.detail
    )
    durable_case = MigrationCaseStore(case_path).load()
    assert durable_case.lifecycle is CaseLifecycle.STALE
    assert durable_case.source_scan_blocker == (
        resumed_workflow.case.source_scan_blocker
    )


def test_default_case_resumes_after_source_disappears(
    monkeypatch: Any,
    tmp_path: Path,
) -> None:
    started_apps: list[Any] = []

    def fake_run(app: Any, **kwargs: Any) -> None:
        del kwargs
        started_apps.append(app)

    monkeypatch.setattr(cli.uvicorn, "run", fake_run)
    monkeypatch.setattr(cli, "CASE_DIRECTORY", tmp_path / "cases")
    source = tmp_path / "default-case-source"
    output = tmp_path / "default-case-stages"
    shutil.copytree(cli.HERO_SOURCE_ROOT, source)
    arguments = [
        "demo",
        "--mode",
        "replay",
        "--source",
        str(source),
        "--output",
        str(output),
    ]

    assert cli.run(arguments, environ={}) == 0
    created_case_path = started_apps[-1].state.workflow.case_store.path
    assert created_case_path.is_file()
    shutil.rmtree(source)

    assert cli.run(arguments, environ={}) == 0
    resumed = started_apps[-1].state.workflow
    assert resumed.case is not None
    assert resumed.case.lifecycle is CaseLifecycle.STALE
    assert resumed.case.source_scan_blocker is not None
    assert resumed.case_store is not None
    assert resumed.case_store.path == created_case_path


def test_absent_case_still_requires_a_resolvable_source(
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
    missing_source = tmp_path / "missing-source"
    absent_case = tmp_path / "absent-case.json"

    exit_code = cli.run(
        [
            "demo",
            "--mode",
            "replay",
            "--source",
            str(missing_source),
            "--case",
            str(absent_case),
        ],
        environ={},
    )

    assert exit_code == 2
    assert server_started is False
    assert absent_case.exists() is False
    assert "source package cannot be opened" in capsys.readouterr().err


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


def _receipt_schema_candidate(tmp_path: Path, schema_version: str) -> Path:
    candidate = tmp_path / f"candidate-{schema_version}"
    receipt = candidate / "name-atlas" / "change_receipt.json"
    receipt.parent.mkdir(parents=True)
    receipt.write_text(
        '{"receipt":{"schema_version":"'
        f"{schema_version}"
        '"},"receipt_fingerprint":"'
        f"{'0' * 64}"
        '"}',
        encoding="utf-8",
    )
    return candidate
