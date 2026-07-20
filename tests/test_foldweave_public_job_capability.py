"""Public per-job capability authority over the single durable v3 job."""

from __future__ import annotations

import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from connected_change_fixtures import make_connected_change_fixture

from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.foldweave_companion import (
    DeviceIdentityStore,
    TrustedPublicInvocationContextV1,
    trusted_public_invocation,
)
from name_atlas.foldweave_host_service import (
    FoldweaveHostPlanningService,
    FoldweaveHostServiceError,
)
from name_atlas.foldweave_local_handles import FoldweaveLocalHandleStore
from name_atlas.foldweave_paths import FoldweavePaths
from name_atlas.native_bridge import NativePathRole

oslo_tz = ZoneInfo("Europe/Oslo")
SCOPES = (
    "foldweave.execute",
    "foldweave.plan",
    "foldweave.review",
)
NOW = datetime(2026, 7, 20, 12, 0, tzinfo=oslo_tz)


class _MemoryKeychain:
    def __init__(self) -> None:
        self.items: dict[tuple[str, str], bytes] = {}

    def exists(self, *, service: str, account: str) -> bool:
        return (service, account) in self.items

    def read(self, *, service: str, account: str) -> bytes:
        return self.items[(service, account)]

    def write(self, *, service: str, account: str, value: bytes) -> None:
        self.items[(service, account)] = value

    def remove(self, *, service: str, account: str) -> bool:
        return self.items.pop((service, account), None) is not None


def _invocation(
    *,
    device_id: str,
    grant: str = "a" * 64,
    job_id: str | None = None,
    revoked_at: int | None = None,
) -> TrustedPublicInvocationContextV1:
    issued_at = int((NOW + timedelta(minutes=1)).timestamp() * 1_000)
    return TrustedPublicInvocationContextV1(
        device_id=device_id,
        session_id="session_" + "s" * 32,
        oauth_grant_fingerprint=grant,
        scopes=SCOPES,
        request_id="request_" + "r" * 24,
        issued_at=issued_at,
        expires_at=issued_at + 10_000,
        sequence=1,
        nonce="nonce_" + "n" * 24,
        body_sha256="b" * 64,
        operation_sha256="c" * 64,
        job_id=job_id,
        revoked_at=revoked_at,
    )


def _host_context(tmp_path: Path):
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    tokens = iter(("A" * 43, "B" * 43, "C" * 43, "D" * 43))
    handles = FoldweaveLocalHandleStore(
        clock=lambda: NOW,
        token_factory=lambda: next(tokens),
    )
    service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        handle_store=handles,
        identity_store=identity_store,
        clock=lambda: NOW,
    )
    creation = _invocation(device_id=identity.device_id)
    with trusted_public_invocation(creation):
        source = handles.register(
            role=NativePathRole.SOURCE_FOLDER,
            path=fixture.sofia_root,
            channel="chatgpt_hosted",
        )
        output_handle = handles.register(
            role=NativePathRole.OUTPUT_PARENT,
            path=output,
            channel="chatgpt_hosted",
        )
        job = service.create_or_resume_planning_job(
            source_handle=source.handle,
            output_handle=output_handle.handle,
            request=fixture.request,
            disclosure_acknowledged=True,
            idempotency_key="public-capability-origin",
            model_transport="chatgpt_hosted",
        )
    return (
        fixture,
        output,
        keychain,
        identity_store,
        identity,
        handles,
        service,
        job,
    )


def test_public_root_job_persists_only_hashed_capability_and_requires_exact_access(
    tmp_path: Path,
) -> None:
    (
        _fixture,
        _output,
        _keychain,
        _identity_store,
        identity,
        _handles,
        service,
        job,
    ) = _host_context(tmp_path)
    binding = job.public_job_capability
    assert binding is not None
    capability_id = _identity_store.derive_public_job_capability_id(
        job_id=job.job_id,
        device_id=binding.device_id,
        oauth_grant_fingerprint=binding.oauth_grant_fingerprint,
        scopes=binding.scopes,
        expires_at_ms=binding.expires_at_ms,
    )
    assert (
        binding.capability_id_sha256
        == hashlib.sha256(capability_id.encode("utf-8")).hexdigest()
    )
    assert capability_id.encode("utf-8") not in job.job_path.read_bytes()

    authorized = _invocation(
        device_id=identity.device_id,
        job_id=job.job_id,
    )
    with trusted_public_invocation(authorized):
        assert service.status(job.job_id) == job

    missing = _invocation(device_id=identity.device_id)
    with (
        trusted_public_invocation(missing),
        pytest.raises(FoldweaveHostServiceError) as captured,
    ):
        service.status(job.job_id)
    assert captured.value.code == "public_job_capability_required"

    wrong_job = _invocation(
        device_id=identity.device_id,
        job_id="f" * 32,
    )
    with (
        trusted_public_invocation(wrong_job),
        pytest.raises(FoldweaveHostServiceError) as captured,
    ):
        service.status(job.job_id)
    assert captured.value.code == "public_job_capability_required"


def test_public_job_rejects_other_grant_revocation_and_expiry(tmp_path: Path) -> None:
    (
        _fixture,
        _output,
        keychain,
        _identity_store,
        identity,
        _handles,
        service,
        job,
    ) = _host_context(tmp_path)

    other_grant = _invocation(
        device_id=identity.device_id,
        grant="d" * 64,
        job_id=job.job_id,
    )
    with (
        trusted_public_invocation(other_grant),
        pytest.raises(FoldweaveHostServiceError) as captured,
    ):
        service.status(job.job_id)
    assert captured.value.code == "public_job_capability_mismatch"

    revoked = _invocation(
        device_id=identity.device_id,
        job_id=job.job_id,
        revoked_at=int(NOW.timestamp() * 1_000),
    )
    with (
        trusted_public_invocation(revoked),
        pytest.raises(FoldweaveHostServiceError) as captured,
    ):
        service.status(job.job_id)
    assert captured.value.code == "public_oauth_grant_revoked"

    expired_service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        identity_store=DeviceIdentityStore(adapter=keychain),
        clock=lambda: NOW + timedelta(minutes=31),
    )
    with trusted_public_invocation(
        authorized := _invocation(
            device_id=identity.device_id,
            job_id=job.job_id,
        )
    ):
        assert authorized.job_id == job.job_id
        with pytest.raises(FoldweaveHostServiceError) as captured:
            expired_service.status(job.job_id)
    assert captured.value.code == "public_job_capability_expired"


def test_public_receiver_derivative_gets_distinct_child_capability(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    for directory in (origin_output, receiver_output):
        directory.mkdir()
    paths = FoldweavePaths(state_root=tmp_path / "state")
    paths.jobs.mkdir(parents=True)
    review = FoldweaveReviewService()
    origin = review.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=paths.jobs / "origin.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="public-capability-origin-proof",
    )
    assert origin.preview is not None
    verified = review.accept(
        origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=origin_output,
        result_folder_name=fixture.result_name,
        idempotency_key="public-capability-origin-accept",
        channel="native_app",
    )
    change_file = review.get_change_file(verified.job_path)[0]

    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    handles = FoldweaveLocalHandleStore(
        clock=lambda: NOW,
        token_factory=iter(("A" * 43, "B" * 43, "C" * 43)).__next__,
    )
    host = FoldweaveHostPlanningService(
        paths=paths,
        handle_store=handles,
        review_service=review,
        identity_store=identity_store,
        clock=lambda: NOW,
    )
    creation = _invocation(device_id=identity.device_id)
    with trusted_public_invocation(creation):
        change_handle = handles.register(
            role=NativePathRole.CHANGE_FILE,
            path=change_file,
            channel="chatgpt_hosted",
        )
        source_handle = handles.register(
            role=NativePathRole.SOURCE_FOLDER,
            path=fixture.martin_root,
            channel="chatgpt_hosted",
        )
        output_handle = handles.register(
            role=NativePathRole.OUTPUT_PARENT,
            path=receiver_output,
            channel="chatgpt_hosted",
        )
        parent = host.prepare_change_application(
            change_file_handle=change_handle.handle,
            source_handle=source_handle.handle,
            output_handle=output_handle.handle,
            idempotency_key="public-capability-receiver",
            channel="chatgpt_hosted",
        )
    assert parent.public_job_capability is not None

    parent_context = _invocation(
        device_id=identity.device_id,
        job_id=parent.job_id,
    )
    with trusted_public_invocation(parent_context):
        child = host.create_or_resume_derivative_child(
            parent_job_id=parent.job_id,
            instruction="Place one reviewed file in a collaboration folder.",
            idempotency_key="public-capability-derivative",
            model_transport="chatgpt_hosted",
        )
    assert child.public_job_capability is not None
    assert (
        child.public_job_capability.capability_id_sha256
        != parent.public_job_capability.capability_id_sha256
    )
    assert child.public_job_capability is not None
    assert child.immediate_parent_job_id == parent.job_id

    child_context = _invocation(
        device_id=identity.device_id,
        job_id=child.job_id,
    )
    with trusted_public_invocation(child_context):
        assert host.status(child.job_id) == child
