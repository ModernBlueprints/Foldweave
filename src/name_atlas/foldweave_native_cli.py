"""Native Foldweave composition root over the shared FastAPI control plane."""

from __future__ import annotations

import argparse
import os
import platform
import secrets
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from fastapi import FastAPI

from name_atlas.folder_app import create_folder_app
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.foldweave_companion import DeviceIdentityStore
from name_atlas.foldweave_companion_cli import EmbeddedCompanionRuntime
from name_atlas.foldweave_companion_client import (
    CompanionPairingClient,
    CompanionPairingStateStore,
)
from name_atlas.foldweave_companion_supervisor import (
    FoldweaveCompanionSupervisor,
)
from name_atlas.foldweave_host_service import FoldweaveHostPlanningService
from name_atlas.foldweave_job_locator import FoldweaveJobLocator
from name_atlas.foldweave_pairing_service import FoldweavePairingService
from name_atlas.foldweave_paths import (
    FoldweavePaths,
    foldweave_paths,
    resolve_foldweave_budget_authority,
    resolve_foldweave_job_path,
)
from name_atlas.foldweave_provider_factory import FoldweaveDirectProviderFactory
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService
from name_atlas.native_bridge import MacOSNativePathBridge
from name_atlas.native_runtime import NativeRuntimeError, run_native_window
from name_atlas.native_settings import (
    CredentialStore,
    EnvironmentCredentialStore,
    MacOSKeychainCredentialStore,
    NativeSettingsService,
)


class NativeWindowRunner(Protocol):
    """Run one fully composed native application until its window closes."""

    def __call__(
        self,
        *,
        app: FastAPI,
        instance_nonce: str,
        lock_path: Path,
        title: str = "Foldweave",
    ) -> None: ...


@dataclass(frozen=True, slots=True)
class FoldweaveNativeComposition:
    """One immutable native runtime assembly with shared durable authorities."""

    app: FastAPI
    instance_nonce: str
    paths: FoldweavePaths
    job_path: Path
    companion_supervisor: FoldweaveCompanionSupervisor


def build_foldweave_native_parser() -> argparse.ArgumentParser:
    """Build the provider-free native application parser."""

    parser = argparse.ArgumentParser(
        prog="foldweave app",
        description=(
            "Run the packaged Foldweave macOS application over one private "
            "loopback control plane."
        ),
        epilog=(
            "Pass --browser to use the supported browser fallback. The default "
            "durable state is stored under ~/Library/Application Support/Foldweave/."
        ),
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Use the supported loopback browser fallback instead of pywebview.",
    )
    parser.add_argument(
        "--mode",
        choices=("live", "development"),
        default="live",
        help=(
            "Use direct GPT-5.6 planning (default), or explicit provider-free "
            "deterministic development planning."
        ),
    )
    parser.add_argument(
        "--qualification-environment-credential",
        action="store_true",
        help=(
            "Use OPENAI_API_KEY only for bounded build qualification; the value "
            "is never copied into the product-user Keychain item."
        ),
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="Optional existing source folder to prefill for a new job.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional existing output parent to prefill for a new job.",
    )
    parser.add_argument(
        "--job",
        type=Path,
        default=None,
        help="Optional exact durable FolderRefactorJobV3 JSON file.",
    )
    parser.add_argument(
        "--job-id",
        default=None,
        help="Resume the exact v3 job with this embedded durable ID.",
    )
    return parser


def compose_foldweave_native_app(
    *,
    source: Path | None,
    output: Path | None,
    job: Path | None,
    job_id: str | None = None,
    mode: str = "development",
    environ: Mapping[str, str] | None = None,
    qualification_environment_credential: bool = False,
) -> FoldweaveNativeComposition:
    """Compose one native application without reading a key or opening a ledger."""

    if mode not in {"live", "development"}:
        raise ValueError("Foldweave native mode is unsupported.")
    if qualification_environment_credential and mode != "live":
        raise ValueError("The qualification environment credential requires live mode.")

    environment = os.environ if environ is None else environ
    paths = foldweave_paths(environ=environ)
    if job is not None and job_id is not None:
        raise ValueError("Select either --job or --job-id, not both.")
    job_path = (
        FoldweaveJobLocator(paths.jobs).resolve(job_id).path
        if job_id is not None
        else resolve_foldweave_job_path(job, environ=environ)
    )
    initial_source: Path | None = None
    initial_output_parent: Path | None = None
    if not os.path.lexists(job_path):
        initial_source = _resolve_optional_directory(source, label="source")
        initial_output_parent = _resolve_optional_directory(output, label="output")
        if initial_output_parent is None and initial_source is not None:
            initial_output_parent = initial_source.parent

    instance_nonce = secrets.token_hex(32)
    credential_store: CredentialStore = (
        EnvironmentCredentialStore(environment)
        if qualification_environment_credential
        else MacOSKeychainCredentialStore()
    )
    native_settings = NativeSettingsService(
        store=credential_store,
    )
    provider_factory = None
    if mode == "live":
        budget_authority = resolve_foldweave_budget_authority(environ=environ)
        provider_factory = FoldweaveDirectProviderFactory(
            job_path=job_path,
            credential_store=credential_store,
            endpoint=native_settings.endpoint,
            budget_authority=budget_authority,
        )
    native_bridge = MacOSNativePathBridge()
    domain_review_service = FoldweaveReviewService()
    review_service = FoldweaveBrowserReviewService(
        job_path=job_path,
        service=domain_review_service,
        provider_factory=provider_factory,
        review_channel="native_app",
    )
    identity_store = DeviceIdentityStore()
    pairing_state_store = CompanionPairingStateStore(path=paths.companion_pairing)
    host_service = FoldweaveHostPlanningService(
        paths=paths,
        native_bridge=native_bridge,
        review_service=domain_review_service,
        identity_store=identity_store,
    )
    companion_supervisor = FoldweaveCompanionSupervisor(
        state_store=pairing_state_store,
        runtime=EmbeddedCompanionRuntime(
            service=host_service,
            identity_store=identity_store,
        ),
    )
    pairing_service = FoldweavePairingService(
        state_store=pairing_state_store,
        pairing=CompanionPairingClient(
            identity_store=identity_store,
            state_store=pairing_state_store,
        ),
        runtime_status=companion_supervisor,
        runtime_lifecycle=companion_supervisor,
    )
    app = create_folder_app(
        review_service,
        initial_source=initial_source,
        initial_output_parent=initial_output_parent,
        native_bridge=native_bridge,
        native_settings=native_settings,
        pairing_service=pairing_service,
        health_instance_nonce=instance_nonce,
    )
    return FoldweaveNativeComposition(
        app=app,
        instance_nonce=instance_nonce,
        paths=paths,
        job_path=job_path,
        companion_supervisor=companion_supervisor,
    )


def run_foldweave_app(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    platform_name: str | None = None,
    machine_name: str | None = None,
    window_runner: NativeWindowRunner = run_native_window,
) -> int:
    """Run the native application or delegate exactly to the browser fallback."""

    arguments = list(sys.argv[1:] if argv is None else argv)
    if "--browser" in arguments:
        from name_atlas.foldweave_browser_cli import run_foldweave_app as run_browser

        return run_browser(arguments)

    args = build_foldweave_native_parser().parse_args(arguments)
    current_platform = sys.platform if platform_name is None else platform_name
    current_machine = platform.machine() if machine_name is None else machine_name
    if current_platform != "darwin" or current_machine != "arm64":
        print(
            "Startup blocked: the packaged Foldweave application is supported "
            "only on macOS Apple Silicon; pass --browser for the fallback.",
            file=sys.stderr,
        )
        return 2
    try:
        composition = compose_foldweave_native_app(
            source=args.source,
            output=args.output,
            job=args.job,
            job_id=args.job_id,
            mode=args.mode,
            environ=environ,
            qualification_environment_credential=(
                args.qualification_environment_credential
            ),
        )
        window_runner(
            app=composition.app,
            instance_nonce=composition.instance_nonce,
            lock_path=composition.paths.instance_lock,
            title="Foldweave",
        )
    except (NativeRuntimeError, OSError, RuntimeError, ValueError) as exc:
        print(
            f"Startup blocked: Foldweave could not open its native application: {exc}",
            file=sys.stderr,
        )
        return 2
    return 0


def _resolve_optional_directory(path: Path | None, *, label: str) -> Path | None:
    if path is None:
        return None
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise NotADirectoryError(f"{label} must be an existing directory")
    return resolved


def main() -> None:
    """Console and packaged-application entry point."""

    raise SystemExit(run_foldweave_app())


if __name__ == "__main__":
    main()
