"""Terminal-safe reconstruction authority for every new Foldweave v3 job."""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest
from connected_change_fixtures import make_connected_change_fixture

from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobV3IdempotencyConflict,
    FolderJobV3RevisionError,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    build_recreate_original_operation_binding_v3,
    require_recreate_original_operation_authority_v3,
    require_recreate_original_operation_idempotency_v3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.inventory import scan_folder


def _require_reconstruction_authority(
    job: FolderRefactorJobV3,
    *,
    idempotency_key: str,
) -> None:
    expected = build_recreate_original_operation_binding_v3(
        job_id=job.job_id,
        idempotency_key=idempotency_key,
    )
    assert job.operation_idempotency == (expected,)
    require_recreate_original_operation_authority_v3(job)
    require_recreate_original_operation_idempotency_v3(
        job,
        idempotency_key=idempotency_key,
    )
    with pytest.raises(
        FolderJobV3IdempotencyConflict,
        match="not bound to this exact job",
    ):
        require_recreate_original_operation_idempotency_v3(
            job,
            idempotency_key=f"{idempotency_key}-different",
        )


def _accept_origin(
    service: FoldweaveReviewService,
    review: FolderRefactorJobV3,
    *,
    output_parent: Path,
) -> FolderRefactorJobV3:
    assert review.preview is not None
    assert review.candidate_plan is not None
    return service.accept(
        review.job_path,
        expected_revision=review.revision,
        preview_fingerprint=review.preview.preview_fingerprint,
        candidate_fingerprint=review.preview.compiled_candidate_fingerprint,
        output_parent=output_parent,
        result_folder_name=review.candidate_plan.result_folder_name,
        idempotency_key=f"accept-{review.job_id}",
        channel="native_app",
    )


def test_origin_receiver_and_derivative_prebind_and_roundtrip_reconstruction(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    jobs = tmp_path / "jobs"
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    derivative_output = tmp_path / "derivative-output"
    for directory in (jobs, origin_output, receiver_output, derivative_output):
        directory.mkdir()

    origin_key = "v3-reconstruction-origin"
    origin = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=jobs / "origin.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key=origin_key,
    )
    _require_reconstruction_authority(origin, idempotency_key=origin_key)
    assert FolderRefactorJobV3Store(origin.job_path).inspect() == origin

    verified_origin = _accept_origin(
        service,
        origin,
        output_parent=origin_output,
    )
    change_file_path = service.get_change_file(verified_origin.job_path)[0]

    receiver_key = "v3-reconstruction-receiver"
    receiver_id = uuid.uuid4().hex
    receiver = service.prepare_application_review(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=jobs / f"{receiver_id}.json",
        idempotency_key=receiver_key,
        job_id=receiver_id,
    )
    assert receiver.job_id == receiver_id
    assert receiver.job_path == (jobs / f"{receiver_id}.json").resolve(strict=False)
    _require_reconstruction_authority(receiver, idempotency_key=receiver_key)
    assert FolderRefactorJobV3Store(receiver.job_path).inspect() == receiver
    repeated_receiver = service.prepare_application_review(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=jobs / f"{receiver_id}.json",
        idempotency_key=receiver_key,
        job_id=receiver_id,
    )
    assert repeated_receiver == receiver

    derivative_key = "v3-reconstruction-derivative"
    child = service.create_or_resume_derivative_child(
        receiver.job_path,
        output_parent=derivative_output,
        instruction="Move one document into the derivative review section.",
        idempotency_key=derivative_key,
        model_transport="chatgpt_hosted",
        channel="chatgpt_hosted",
    )
    _require_reconstruction_authority(child, idempotency_key=derivative_key)
    assert FolderRefactorJobV3Store(child.job_path).inspect() == child


def test_reconstruction_authority_is_immutable_and_terminal_restore_writes_no_job(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    output = tmp_path / "output"
    output.mkdir()
    origin_key = "v3-reconstruction-terminal"
    review = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "terminal.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key=origin_key,
    )
    review_bytes = review.job_path.read_bytes()
    invalid_successor = review.model_copy(
        update={
            "revision": review.revision + 1,
            "operation_idempotency": (),
        }
    )
    with pytest.raises(
        FolderJobV3IdempotencyConflict,
        match="one immutable job-bound authority",
    ):
        require_recreate_original_operation_authority_v3(invalid_successor)
    with FolderRefactorJobV3Store(review.job_path).writer() as writer:
        current = writer.load()
        with pytest.raises(
            FolderJobV3RevisionError,
            match="immutable job identity",
        ):
            writer.save(invalid_successor, expected_current=current)
    assert review.job_path.read_bytes() == review_bytes

    verified = _accept_origin(service, review, output_parent=output)
    _require_reconstruction_authority(verified, idempotency_key=origin_key)
    terminal_bytes = verified.job_path.read_bytes()
    destination = tmp_path / "restored-original"
    report = service.recreate_original(verified.job_path, destination)

    assert report.source_commitment == verified.source_inventory.source_commitment
    assert scan_folder(destination).inventory == verified.source_inventory
    assert verified.job_path.read_bytes() == terminal_bytes
    assert FolderRefactorJobV3Store(verified.job_path).inspect() == verified
