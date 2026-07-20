"""Native Foldweave composition tests that never open a real window."""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from name_atlas import foldweave_browser_cli, foldweave_native_cli
from name_atlas.foldweave_companion_cli import EmbeddedCompanionRuntime
from name_atlas.foldweave_companion_supervisor import FoldweaveCompanionSupervisor
from name_atlas.foldweave_pairing_service import FoldweavePairingService
from name_atlas.native_bridge import MacOSNativePathBridge
from name_atlas.native_settings import (
    CredentialStatus,
    EnvironmentCredentialStore,
    MacOSKeychainCredentialStore,
    NativeSettingsService,
)


def test_native_parser_has_a_finder_launchable_default() -> None:
    arguments = foldweave_native_cli.build_foldweave_native_parser().parse_args([])

    assert arguments.browser is False
    assert arguments.mode == "live"
    assert arguments.qualification_environment_credential is False
    assert arguments.source is None
    assert arguments.output is None
    assert arguments.job is None


def test_browser_flag_delegates_exactly_without_composing_native_authority(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: list[str] = []
    monkeypatch.setattr(
        foldweave_browser_cli,
        "run_foldweave_app",
        lambda arguments: captured.extend(arguments) or 0,
    )

    arguments = [
        "--browser",
        "--mode",
        "development",
        "--port",
        "8765",
    ]
    assert foldweave_native_cli.run_foldweave_app(arguments) == 0
    assert captured == arguments


def test_native_composition_uses_one_job_control_plane_and_trusted_adapters(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    state_root = tmp_path / "state"
    captured: dict[str, object] = {}

    class CapturedReviewService:
        def __init__(self, *, job_path: Path, **kwargs: object) -> None:
            captured["job_path"] = job_path
            captured["review_service_kwargs"] = kwargs

    def capture_app(service: object, **kwargs: object) -> object:
        app = object()
        captured["service"] = service
        captured["app"] = app
        captured.update(kwargs)
        return app

    def capture_window(**kwargs: object) -> None:
        captured["window"] = kwargs

    monkeypatch.setattr(
        foldweave_native_cli,
        "FoldweaveBrowserReviewService",
        CapturedReviewService,
    )
    monkeypatch.setattr(foldweave_native_cli, "create_folder_app", capture_app)

    result = foldweave_native_cli.run_foldweave_app(
        [
            "--mode",
            "development",
            "--source",
            str(source),
            "--output",
            str(output),
        ],
        environ={"FOLDWEAVE_STATE_ROOT": str(state_root)},
        platform_name="darwin",
        window_runner=capture_window,
    )

    expected_job = (state_root / "jobs" / "active.json").resolve(strict=False)
    assert result == 0
    assert captured["job_path"] == expected_job
    assert captured["initial_source"] == source.resolve(strict=True)
    assert captured["initial_output_parent"] == output.resolve(strict=True)
    assert isinstance(captured["native_bridge"], MacOSNativePathBridge)
    pairing = captured["pairing_service"]
    assert isinstance(pairing, FoldweavePairingService)
    assert pairing.state_store.path == (state_root / "companion-pairing.json")
    supervisor = pairing.runtime_lifecycle
    assert isinstance(supervisor, FoldweaveCompanionSupervisor)
    assert pairing.runtime_status is supervisor
    assert isinstance(supervisor.runtime, EmbeddedCompanionRuntime)
    assert captured["review_service_kwargs"]["service"] is (
        supervisor.runtime.service._review
    )
    settings = captured["native_settings"]
    assert isinstance(settings, NativeSettingsService)
    assert isinstance(settings.store, MacOSKeychainCredentialStore)
    nonce = captured["health_instance_nonce"]
    assert isinstance(nonce, str)
    assert len(nonce) == 64
    assert captured["window"] == {
        "app": captured["app"],
        "instance_nonce": nonce,
        "lock_path": (state_root / "runtime.lock").resolve(strict=False),
        "title": "Foldweave",
    }


def test_native_qualification_uses_environment_without_keychain_persistence(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    composition = foldweave_native_cli.compose_foldweave_native_app(
        source=None,
        output=None,
        job=None,
        mode="live",
        environ={
            "FOLDWEAVE_STATE_ROOT": str(state_root),
            "OPENAI_API_KEY": "test-only-qualification-placeholder",
        },
        qualification_environment_credential=True,
    )
    settings = composition.app.state.native_settings

    assert isinstance(settings.store, EnvironmentCredentialStore)
    assert settings.view().credential.configured is True
    assert settings.view().credential.store_kind == "environment"
    assert not state_root.exists()

    with TestClient(composition.app) as client:
        response = client.get("/settings")

    assert response.status_code == 200
    assert "Configured in qualification environment" in response.text
    assert "never enters this web view or the product-user Keychain item" in (
        response.text
    )
    assert "Configure key" not in response.text
    assert "Remove key" not in response.text


def test_native_qualification_credential_requires_live_mode(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="requires live mode"):
        foldweave_native_cli.compose_foldweave_native_app(
            source=None,
            output=None,
            job=None,
            mode="development",
            environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")},
            qualification_environment_credential=True,
        )


def test_real_composition_exposes_health_settings_and_review_routes(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    composition = foldweave_native_cli.compose_foldweave_native_app(
        source=None,
        output=None,
        job=None,
        environ={"FOLDWEAVE_STATE_ROOT": str(state_root)},
    )

    paths = {route.path for route in composition.app.routes}
    assert composition.app.title == "Foldweave"
    assert {"/healthz", "/settings", "/review"} <= paths
    assert isinstance(
        composition.app.state.native_settings,
        NativeSettingsService,
    )
    pairing = composition.app.state.pairing_service
    assert isinstance(pairing, FoldweavePairingService)
    assert pairing.runtime_lifecycle is composition.companion_supervisor
    assert pairing.runtime_status is composition.companion_supervisor
    assert isinstance(
        composition.companion_supervisor.runtime,
        EmbeddedCompanionRuntime,
    )
    assert composition.companion_supervisor.state_store.path == (
        state_root / "companion-pairing.json"
    )
    assert composition.app.state.health_instance_nonce == composition.instance_nonce
    assert not state_root.exists()


def test_settings_distinguish_unavailable_keychain_from_not_configured(
    tmp_path: Path,
) -> None:
    composition = foldweave_native_cli.compose_foldweave_native_app(
        source=None,
        output=None,
        job=None,
        mode="development",
        environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")},
    )

    class UnavailableCredentialStore:
        def status(self) -> CredentialStatus:
            return CredentialStatus(
                configured=False,
                store_kind="keychain",
                status_code="keychain_status_failed",
            )

        def read(self) -> str:
            raise AssertionError("Settings rendering must not read a credential.")

        def write(self, value: str) -> None:
            del value
            raise AssertionError("Settings rendering must not write a credential.")

        def remove(self) -> bool:
            raise AssertionError("Settings rendering must not remove a credential.")

    composition.app.state.native_settings.store = UnavailableCredentialStore()

    with TestClient(composition.app) as client:
        response = client.get("/settings")

    assert response.status_code == 200
    assert "could not read macOS Keychain state" in response.text
    assert "keychain_status_failed" not in response.text
    assert "Not configured" not in response.text


def test_existing_job_rehydrates_without_reapplying_source_prefill(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job = tmp_path / "jobs" / "active.json"
    job.parent.mkdir()
    job.write_text("{}", encoding="utf-8")
    captured: dict[str, object] = {}

    class CapturedReviewService:
        def __init__(self, *, job_path: Path, **kwargs: object) -> None:
            captured["job_path"] = job_path
            captured["review_service_kwargs"] = kwargs

    def capture_app(_service: object, **kwargs: object) -> object:
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(
        foldweave_native_cli,
        "FoldweaveBrowserReviewService",
        CapturedReviewService,
    )
    monkeypatch.setattr(foldweave_native_cli, "create_folder_app", capture_app)

    composition = foldweave_native_cli.compose_foldweave_native_app(
        source=tmp_path / "missing-source",
        output=tmp_path / "missing-output",
        job=job,
        environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")},
    )

    assert composition.job_path == job.resolve(strict=True)
    assert captured["initial_source"] is None
    assert captured["initial_output_parent"] is None


def test_native_launch_fails_closed_off_macos(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        foldweave_native_cli.run_foldweave_app(
            ["--mode", "development"],
            platform_name="linux",
        )
        == 2
    )
    assert "only on macOS Apple Silicon" in capsys.readouterr().err


def test_native_launch_fails_closed_on_non_arm_macos(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        foldweave_native_cli.run_foldweave_app(
            ["--mode", "development"],
            platform_name="darwin",
            machine_name="x86_64",
        )
        == 2
    )
    assert "only on macOS Apple Silicon" in capsys.readouterr().err
