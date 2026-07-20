"""Thin reviewed CLI over the sole Foldweave v3 domain service."""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
    FolderMutationRequestV2,
    build_idempotency_binding,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
    GptDerivativeJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.serialization import canonical_json_bytes
from name_atlas.foldweave_paths import (
    resolve_foldweave_budget_authority,
    resolve_foldweave_job_path,
)

DEFAULT_REQUEST = (
    "Organize this connected project for handoff. Keep every file and every "
    "supported Markdown link working."
)


def run_prepare_origin(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Prepare one live or replay origin job and stop before execution."""

    parser = argparse.ArgumentParser(
        prog="foldweave run",
        description="Prepare a complete Foldweave proposal for exact review.",
    )
    parser.add_argument("--mode", choices=("live", "replay"), required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--job", type=Path, default=None)
    parser.add_argument("--request", default=None)
    parser.add_argument("--replay", type=Path, default=None)
    args = parser.parse_args(argv)
    environment = os.environ if environ is None else environ
    try:
        source = _existing_directory(args.source, label="source")
        output = (
            source.parent
            if args.output is None
            else _existing_directory(args.output, label="output")
        )
        job_path = resolve_foldweave_job_path(args.job, environ=environment)
        service = FoldweaveReviewService()
        request = args.request or _default_request(args.mode)
        retry_key = _derived_key(
            "run",
            job_path,
            str(source),
            str(output),
            request,
            args.mode,
        )
        expected_binding = build_idempotency_binding(
            retry_key,
            FolderMutationRequestV2(
                operation="gpt_planned",
                source_root=source,
                output_parent=output,
                user_request=request,
            ),
        )
        existing = None
        if os.path.lexists(job_path):
            existing = service.status(job_path)
            if existing.idempotency != expected_binding:
                raise ValueError(
                    "existing job is bound to another source, output, request, "
                    "or planning mode"
                )
            if existing.lifecycle is not FolderJobLifecycleV3.PLANNING:
                _print_job(existing)
                return _prepared_exit_code(existing)
        provider = _initial_provider(
            mode=args.mode,
            job_path=job_path,
            replay_path=args.replay,
            environment=environment,
        )
        if existing is not None:
            job = asyncio.run(
                service.resume_planned_origin_review(job_path, provider=provider)
            )
        else:
            job = asyncio.run(
                service.prepare_planned_origin_review(
                    source_root=source,
                    output_parent=output,
                    job_path=job_path,
                    request=request,
                    idempotency_key=retry_key,
                    provider=provider,
                )
            )
    except (OSError, RuntimeError, ValueError) as exc:
        return _blocked("RUN", exc)
    _print_job(job)
    return _prepared_exit_code(job)


def run_prepare_application(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Prepare one provider-free Change File application for exact review."""

    parser = argparse.ArgumentParser(
        prog="foldweave apply-change",
        description=(
            "Match a Foldweave Change File and stop at receiver-local review."
        ),
    )
    parser.add_argument("change_file", type=Path)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--job", type=Path, default=None)
    args = parser.parse_args(argv)
    environment = os.environ if environ is None else environ
    try:
        source = _existing_directory(args.source, label="source")
        output = (
            source.parent
            if args.output is None
            else _existing_directory(args.output, label="output")
        )
        change_file = args.change_file.expanduser().resolve(strict=True)
        if not change_file.is_file():
            raise ValueError("change_file must be a regular file")
        job_path = resolve_foldweave_job_path(args.job, environ=environment)
        job = FoldweaveReviewService().prepare_application_review(
            change_file_path=change_file,
            source_root=source,
            output_parent=output,
            job_path=job_path,
            idempotency_key=_derived_key(
                "apply-change",
                job_path,
                str(change_file),
                str(source),
                str(output),
            ),
        )
    except (OSError, RuntimeError, ValueError) as exc:
        return _blocked("APPLY", exc)
    _print_job(job)
    return _prepared_exit_code(job)


def run_preview(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Print the exact persisted preview DTO without mutating the job."""

    parser = argparse.ArgumentParser(prog="foldweave preview")
    parser.add_argument("job", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        job_path = resolve_foldweave_job_path(args.job, environ=environ)
        job = FoldweaveReviewService().status(job_path)
        if job.preview is None:
            raise ValueError(f"job has no preview in {job.lifecycle.value}")
    except (OSError, RuntimeError, ValueError) as exc:
        return _blocked("PREVIEW", exc)
    if args.json:
        print(canonical_json_bytes(job.preview).decode("utf-8"))
    else:
        _print_job(job)
        print(f"FILES {job.preview.counts.file_count}")
        print(f"CHANGED_PATHS {job.preview.counts.changed_path_count}")
        print(f"UPDATED_LINKS {job.preview.counts.link_updated_count}")
    return 0


def run_revise(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Request one bounded direct revision of an exact reviewed preview."""

    parser = argparse.ArgumentParser(prog="foldweave revise")
    parser.add_argument("job", type=Path)
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--idempotency-key", required=True)
    args = parser.parse_args(argv)
    environment = os.environ if environ is None else environ
    try:
        job_path = resolve_foldweave_job_path(args.job, environ=environment)
        service = FoldweaveReviewService()
        current = service.status(job_path)
        if (
            current.preview is None
            and isinstance(current.authority, GptDerivativeJobAuthorityV3)
            and current.authority.authority_state == "awaiting_model_response"
        ):
            job = service.recover_interrupted_direct_derivative(job_path)
            _print_job(job)
            return _prepared_exit_code(job)
        if current.preview is None:
            raise ValueError("job has no review preview")
        from name_atlas.foldweave_provider_factory import (
            FoldweaveDirectProviderFactory,
        )
        from name_atlas.native_settings import (
            DirectEndpointProfile,
            EnvironmentCredentialStore,
        )

        factory = FoldweaveDirectProviderFactory(
            job_path=job_path,
            credential_store=EnvironmentCredentialStore(environment),
            endpoint=DirectEndpointProfile.official(),
            budget_authority=resolve_foldweave_budget_authority(environ=environment),
        )
        if isinstance(current.authority, CapsuleAppliedJobAuthorityV2) or (
            isinstance(current.authority, GptDerivativeJobAuthorityV3)
            and current.authority.authority_state == "failed"
        ):
            parent_path = (
                current.job_path
                if isinstance(current.authority, CapsuleAppliedJobAuthorityV2)
                else current.authority.parent_binding.parent_job_path
            )
            child, created = service.create_or_resume_derivative_child_with_status(
                parent_path,
                output_parent=current.output_parent,
                instruction=args.instruction,
                idempotency_key=args.idempotency_key,
                provider_kind=factory.provider_kind,
                channel="cli",
            )
            if created:
                job = asyncio.run(
                    service.submit_direct_derivative_revision(
                        child.job_path,
                        provider=factory.derivative_revision_provider(child.job_path),
                    )
                )
            else:
                job = service.recover_interrupted_direct_derivative(child.job_path)
        else:

            def provider_factory():
                if isinstance(current.authority, GptDerivativeJobAuthorityV3):
                    return factory.derivative_revision_provider(current.job_path)
                return factory.revision_provider()

            job = asyncio.run(
                service.revise(
                    job_path,
                    expected_revision=current.revision,
                    preview_fingerprint=current.preview.preview_fingerprint,
                    candidate_fingerprint=(
                        current.preview.compiled_candidate_fingerprint
                    ),
                    instruction=args.instruction,
                    idempotency_key=args.idempotency_key,
                    provider_factory=provider_factory,
                )
            )
    except (OSError, RuntimeError, ValueError) as exc:
        return _blocked("REVISE", exc)
    _print_job(job)
    return _prepared_exit_code(job)


def run_accept(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
) -> int:
    """Accept one exact preview fingerprint and execute the separate copy."""

    parser = argparse.ArgumentParser(prog="foldweave accept")
    parser.add_argument("job", type=Path)
    parser.add_argument("--preview-fingerprint", required=True)
    parser.add_argument("--idempotency-key", required=True)
    args = parser.parse_args(argv)
    try:
        job_path = resolve_foldweave_job_path(args.job, environ=environ)
        service = FoldweaveReviewService()
        current = service.status(job_path)
        if current.preview is None or current.candidate_plan is None:
            raise ValueError("job has no complete review preview")
        if current.preview.preview_fingerprint != args.preview_fingerprint:
            raise ValueError("preview fingerprint differs from the durable job")
        job = service.accept(
            job_path,
            expected_revision=current.revision,
            preview_fingerprint=args.preview_fingerprint,
            candidate_fingerprint=(current.preview.compiled_candidate_fingerprint),
            output_parent=current.output_parent,
            result_folder_name=current.candidate_plan.result_folder_name,
            idempotency_key=args.idempotency_key,
            channel="cli",
        )
    except (OSError, RuntimeError, ValueError) as exc:
        return _blocked("ACCEPT", exc)
    _print_job(job)
    if job.lifecycle is not FolderJobLifecycleV3.VERIFIED:
        return 1
    assert job.final_result_path is not None
    assert job.verified_artifacts is not None
    print(f"RESULT {job.final_result_path}")
    print(f"RECEIPT {job.verified_artifacts.receipt_fingerprint}")
    return 0


def run_legacy_verify(argv: Sequence[str] | None = None) -> int:
    """Reuse the existing provider-free receipt verifier."""

    from name_atlas.cli import run as run_legacy_cli

    return run_legacy_cli(["verify-receipt", *(argv or ())])


def run_legacy_restore(argv: Sequence[str] | None = None) -> int:
    """Reuse the existing provider-free reconstruction engine."""

    from name_atlas.cli import run as run_legacy_cli

    return run_legacy_cli(["restore-receipt", *(argv or ())])


def _initial_provider(
    *,
    mode: str,
    job_path: Path,
    replay_path: Path | None,
    environment: Mapping[str, str],
):
    if mode == "replay":
        from name_atlas.connected_planner_runtime import HERO_REPLAY_PATH
        from name_atlas.folder_refactor.planner_recording import (
            RecordedPlannerProvider,
        )

        selected = HERO_REPLAY_PATH if replay_path is None else replay_path
        return RecordedPlannerProvider(selected.expanduser().read_bytes())
    from name_atlas.foldweave_provider_factory import FoldweaveDirectProviderFactory
    from name_atlas.native_settings import (
        DirectEndpointProfile,
        EnvironmentCredentialStore,
    )

    return FoldweaveDirectProviderFactory(
        job_path=job_path,
        credential_store=EnvironmentCredentialStore(environment),
        endpoint=DirectEndpointProfile.official(),
        budget_authority=resolve_foldweave_budget_authority(environ=environment),
    ).initial_provider()


def _default_request(mode: str) -> str:
    if mode == "replay":
        from name_atlas.folder_refactor.demo_fixtures import HERO_REQUEST

        return HERO_REQUEST
    return DEFAULT_REQUEST


def _existing_directory(path: Path, *, label: str) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise ValueError(f"{label} must be an existing directory")
    return resolved


def _derived_key(operation: str, job_path: Path, *parts: str) -> str:
    digest = hashlib.sha256(
        "\0".join((operation, str(job_path.resolve(strict=False)), *parts)).encode(
            "utf-8"
        )
    ).hexdigest()
    return f"foldweave-cli:{operation}:{digest}"


def _print_job(job: FolderRefactorJobV3) -> None:
    print(f"JOB_ID {job.job_id}")
    print(f"JOB {job.job_path}")
    print(f"LIFECYCLE {job.lifecycle.value}")
    if job.preview is not None:
        print(f"PREVIEW {job.preview.preview_fingerprint}")
        print(f"CANDIDATE {job.preview.compiled_candidate_fingerprint}")


def _prepared_exit_code(job: FolderRefactorJobV3) -> int:
    if job.lifecycle in {
        FolderJobLifecycleV3.REVIEWING,
        FolderJobLifecycleV3.REVISION_FAILED,
        FolderJobLifecycleV3.AWAITING_CLARIFICATION,
        FolderJobLifecycleV3.VERIFIED,
    }:
        return 0
    return 1


def _blocked(operation: str, exc: Exception) -> int:
    code = getattr(exc, "code", exc.__class__.__name__)
    print(f"{operation} BLOCKED {code}: {exc}", file=sys.stderr)
    return 1
