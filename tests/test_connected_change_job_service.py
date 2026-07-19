"""Durable C1 Connected Change service integration and restart tests."""

from __future__ import annotations

import multiprocessing
from pathlib import Path
from typing import Any

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
    portable_tree,
    tree_state,
)

import name_atlas.folder_refactor.connected_change.job_service as job_service_module
import name_atlas.folder_refactor.transaction as transaction_module
from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
    ConnectedChangeJobServiceError,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    FolderJobLifecycleV2,
    FolderJobV2IdempotencyConflict,
    FolderJobV2LoadError,
)
from name_atlas.folder_refactor.connected_change.service import (
    ConnectedChangeRunResult,
    create_connected_change_origin,
    execute_prepared_connected_change,
    prepare_connected_change_origin,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
)
from name_atlas.folder_refactor.portable_artifacts import CHANGE_RECEIPT_PATH
from name_atlas.verification.bag_writer import BagItWriter


class _InjectedProcessCrash(BaseException):
    """Simulate process loss without entering normal blocker handling."""


def _concurrent_receiver_create(
    start: Any,
    result_queue: Any,
    *,
    change_file: str,
    source: str,
    output: str,
    job_path: str,
    idempotency_key: str,
) -> None:
    start.wait(timeout=10)
    try:
        job = ConnectedChangeJobService().create_application_job(
            change_file_path=Path(change_file),
            source_root=Path(source),
            output_parent=Path(output),
            job_path=Path(job_path),
            idempotency_key=idempotency_key,
        )
    except Exception as exc:  # noqa: BLE001 - process boundary returns exact type
        result_queue.put(("error", exc.__class__.__name__, str(exc)))
    else:
        result_queue.put(("ok", job.job_id, str(job.job_path)))


def test_receiver_job_persists_executes_retries_and_reconstructs(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    source_before = tree_state(fixture.martin_root)
    change_before = origin.change_file_path.read_bytes()
    job_path = tmp_path / "jobs" / "receiver.json"
    service = ConnectedChangeJobService()

    verified = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=job_path,
        idempotency_key="receiver-retry-key-0001",
    )

    assert verified.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert verified.final_result_path is not None
    assert verified.verified_artifacts is not None
    assert verified.pending_result_path is None
    assert tree_state(fixture.martin_root) == source_before
    assert origin.change_file_path.read_bytes() == change_before
    verification = service.verify_result(job_path)
    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert verification.job_id == verified.job_id

    job_bytes = job_path.read_bytes()
    retried = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=job_path,
        idempotency_key="receiver-retry-key-0001",
    )
    assert retried == verified
    assert job_path.read_bytes() == job_bytes
    assert tuple(receiver_output.iterdir()) == (verified.final_result_path,)

    restored = tmp_path / "unrelated" / "martin-restored"
    restored.parent.mkdir()
    report = service.recreate_original(job_path, restored)
    assert report.source_commitment == verified.source_inventory.source_commitment
    assert portable_tree(restored) == portable_tree(fixture.martin_root)
    assert tree_state(fixture.martin_root) == source_before
    assert origin.change_file_path.read_bytes() == change_before


def test_receiver_output_collision_is_persisted_without_replacement(
    tmp_path: Path,
) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    collision = output / fixture.result_name
    collision.mkdir()
    sentinel = collision / "preserve-me.txt"
    sentinel.write_bytes(b"existing user result\n")
    service = ConnectedChangeJobService()

    blocked = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-output-collision",
    )

    assert blocked.lifecycle is FolderJobLifecycleV2.BLOCKED
    assert blocked.blocker_code == "result_path_unavailable"
    assert blocked.pending_result_path is None
    assert blocked.final_result_path is None
    assert sentinel.read_bytes() == b"existing user result\n"
    repeated = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-output-collision",
    )
    assert repeated == blocked
    assert sentinel.read_bytes() == b"existing user result\n"


def test_service_reconstructs_after_original_source_moves(tmp_path: Path) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    verified = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-source-moved-before-restore",
    )
    assert verified.final_result_path is not None
    result_before = tree_state(verified.final_result_path)
    change_before = origin.change_file_path.read_bytes()
    moved_source = tmp_path / "moved-martin-source"
    fixture.martin_root.rename(moved_source)
    restore_parent = tmp_path / "unrelated-restore"
    restore_parent.mkdir()
    destination = restore_parent / "martin-original"

    report = service.recreate_original(job_path, destination)

    assert report.destination == destination.resolve()
    assert portable_tree(destination) == portable_tree(moved_source)
    assert tree_state(verified.final_result_path) == result_before
    assert origin.change_file_path.read_bytes() == change_before


def test_receiver_job_status_is_read_only_and_changed_source_becomes_stale(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    job_path = tmp_path / "jobs" / "stale.json"
    service = ConnectedChangeJobService()
    planning = service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=job_path,
        idempotency_key="receiver-stale-key-0001",
    )
    assert planning.lifecycle is FolderJobLifecycleV2.PLANNING
    before_status = job_path.read_bytes()
    assert service.status(job_path) == planning
    assert job_path.read_bytes() == before_status

    changed = fixture.martin_root / "incoming" / "cover-art.png"
    changed.write_bytes(changed.read_bytes() + b"changed")
    stale = service.run_or_resume(job_path)

    assert stale.lifecycle is FolderJobLifecycleV2.STALE
    assert stale.staleness is not None
    assert not tuple(receiver_output.iterdir())


def test_origin_job_uses_durable_job_identity_and_idempotent_result(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "origin-output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "origin.json"
    service = ConnectedChangeJobService()

    verified = service.start_deterministic_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=job_path,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="origin-retry-key-000001",
    )

    assert verified.lifecycle is FolderJobLifecycleV2.VERIFIED
    verification = service.verify_result(job_path)
    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert verification.job_id == verified.job_id
    job_bytes = job_path.read_bytes()
    retried = service.start_deterministic_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=job_path,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="origin-retry-key-000001",
    )
    assert retried == verified
    assert job_path.read_bytes() == job_bytes


def test_conflicting_idempotency_key_reuse_blocks(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    first_output = tmp_path / "receiver-a"
    second_output = tmp_path / "receiver-b"
    for path in (origin_output, first_output, second_output):
        path.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    service = ConnectedChangeJobService()
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=first_output,
        job_path=tmp_path / "jobs" / "first.json",
        idempotency_key="receiver-conflict-key-01",
    )

    with pytest.raises(FolderJobV2IdempotencyConflict):
        service.create_application_job(
            change_file_path=origin.change_file_path,
            source_root=fixture.martin_root,
            output_parent=second_output,
            job_path=tmp_path / "jobs" / "second.json",
            idempotency_key="receiver-conflict-key-01",
        )


def test_exact_job_path_conflicting_binding_is_preserved_and_blocks(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    first_output = tmp_path / "receiver-a"
    second_output = tmp_path / "receiver-b"
    for path in (origin_output, first_output, second_output):
        path.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    service = ConnectedChangeJobService()
    job_path = tmp_path / "shared-json-directory" / "receiver.json"
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=first_output,
        job_path=job_path,
        idempotency_key="exact-path-first-binding-0001",
        idempotency_scope="exact_path",
    )
    first_job_bytes = job_path.read_bytes()

    with pytest.raises(
        FolderJobV2IdempotencyConflict,
        match="Requested job path is already bound to another mutation",
    ):
        service.create_application_job(
            change_file_path=origin.change_file_path,
            source_root=fixture.martin_root,
            output_parent=second_output,
            job_path=job_path,
            idempotency_key="exact-path-second-binding-0002",
            idempotency_scope="exact_path",
        )

    assert job_path.read_bytes() == first_job_bytes
    assert not tuple(first_output.iterdir())
    assert not tuple(second_output.iterdir())


def test_managed_job_directory_discovery_remains_strict(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    jobs = tmp_path / "managed-jobs"
    for path in (origin_output, receiver_output, jobs):
        path.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    unrelated = jobs / "unrelated.json"
    unrelated.write_bytes(b'{"unrelated":true}\n')
    before = unrelated.read_bytes()

    with pytest.raises(FolderJobV2LoadError, match="Unsupported durable job"):
        ConnectedChangeJobService().create_application_job(
            change_file_path=origin.change_file_path,
            source_root=fixture.martin_root,
            output_parent=receiver_output,
            job_path=jobs / "receiver.json",
            idempotency_key="managed-directory-strict-discovery",
            idempotency_scope="jobs_directory",
        )

    assert unrelated.read_bytes() == before
    assert not (jobs / "receiver.json").exists()
    assert not tuple(receiver_output.iterdir())


def test_restart_removes_owned_incomplete_pending_and_reexecutes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-incomplete-recovery",
    )

    def crash_with_partial_pending(*_args: object, **kwargs: object) -> None:
        paths = kwargs["transaction_paths"]
        paths.pending_root.mkdir()
        (paths.pending_root / "partial.tmp").write_bytes(b"regenerable")
        receipt_path = paths.pending_root / CHANGE_RECEIPT_PATH
        receipt_path.parent.mkdir()
        receipt_path.write_bytes(b"{}")
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            job_service_module,
            "execute_prepared_connected_change",
            crash_with_partial_pending,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.run_or_resume(job_path)

    interrupted = service.status(job_path)
    assert interrupted.lifecycle is FolderJobLifecycleV2.EXECUTING
    assert interrupted.pending_result_path is not None
    assert (interrupted.pending_result_path / "partial.tmp").is_file()
    resumed = service.run_or_resume(job_path)
    assert resumed.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert resumed.final_result_path is not None
    assert not interrupted.pending_result_path.exists()


def test_restart_promotes_a_complete_verified_pending_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-finalized-pending-recovery",
    )
    real_promote = transaction_module.promote_directory_no_replace

    def crash_before_promotion(_pending: Path, _final: Path) -> None:
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            transaction_module,
            "promote_directory_no_replace",
            crash_before_promotion,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.run_or_resume(job_path)

    interrupted = service.status(job_path)
    assert interrupted.lifecycle is FolderJobLifecycleV2.EXECUTING
    assert interrupted.pending_result_path is not None
    assert interrupted.final_result_path is not None
    assert (interrupted.pending_result_path / CHANGE_RECEIPT_PATH).is_file()
    assert not interrupted.final_result_path.exists()
    assert transaction_module.promote_directory_no_replace is real_promote

    resumed = service.run_or_resume(job_path)
    assert resumed.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert resumed.final_result_path is not None
    assert resumed.final_result_path.is_dir()
    assert not interrupted.pending_result_path.exists()


@pytest.mark.parametrize("post_promotion_change", ("source", "change_file"))
def test_restart_finalizes_an_already_promoted_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    post_promotion_change: str,
) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-promoted-recovery",
    )

    def crash_after_promotion(*_args: object, **_kwargs: object) -> None:
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            ConnectedChangeJobService,
            "_finalize_verified",
            crash_after_promotion,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.run_or_resume(job_path)

    interrupted = service.status(job_path)
    assert interrupted.lifecycle is FolderJobLifecycleV2.EXECUTING
    assert interrupted.pending_result_path is not None
    assert interrupted.final_result_path is not None
    assert not interrupted.pending_result_path.exists()
    assert interrupted.final_result_path.is_dir()
    if post_promotion_change == "source":
        changed = fixture.martin_root / "incoming" / "cover-art.png"
        changed.write_bytes(changed.read_bytes() + b"post-promotion")
    else:
        origin.change_file_path.write_bytes(
            origin.change_file_path.read_bytes() + b"\n"
        )

    resumed = service.run_or_resume(job_path)
    assert resumed.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert resumed.final_result_path == interrupted.final_result_path


def test_recovery_rejects_a_valid_result_for_another_persisted_plan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "origin-output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "origin.json"
    service = ConnectedChangeJobService()

    def crash_before_result(*_args: object, **_kwargs: object) -> None:
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            job_service_module,
            "execute_prepared_connected_change",
            crash_before_result,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.start_deterministic_origin(
                source_root=fixture.sofia_root,
                output_parent=output,
                job_path=job_path,
                request=fixture.request,
                result_folder_name=fixture.result_name,
                target_by_original_path=fixture.target_paths,
                idempotency_key="origin-recovery-binding",
            )

    interrupted = service.status(job_path)
    assert interrupted.lifecycle is FolderJobLifecycleV2.EXECUTING
    assert interrupted.final_result_path is not None
    different_targets = dict(fixture.target_paths)
    different_targets["notes/client-brief.md"] = "alternate/client-brief.md"
    different = prepare_connected_change_origin(
        job_id=interrupted.job_id,
        source_root=fixture.sofia_root,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=different_targets,
    )
    adopted = execute_prepared_connected_change(
        prepared=different,
        output_parent=output,
        job_id=interrupted.job_id,
    )
    assert adopted.folder_run.result_root == interrupted.final_result_path

    blocked = service.run_or_resume(job_path)
    assert blocked.lifecycle is FolderJobLifecycleV2.BLOCKED
    assert blocked.blocker_code == "persisted_job_result_mismatch"


def test_recovery_returns_stale_when_wrong_result_and_source_change_coincide(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "origin-output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "origin.json"
    service = ConnectedChangeJobService()

    def crash_before_result(*_args: object, **_kwargs: object) -> None:
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            job_service_module,
            "execute_prepared_connected_change",
            crash_before_result,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.start_deterministic_origin(
                source_root=fixture.sofia_root,
                output_parent=output,
                job_path=job_path,
                request=fixture.request,
                result_folder_name=fixture.result_name,
                target_by_original_path=fixture.target_paths,
                idempotency_key="origin-racing-staleness",
            )

    interrupted = service.status(job_path)
    assert interrupted.final_result_path is not None
    different_targets = dict(fixture.target_paths)
    different_targets["notes/client-brief.md"] = "alternate/client-brief.md"
    different = prepare_connected_change_origin(
        job_id=interrupted.job_id,
        source_root=fixture.sofia_root,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=different_targets,
    )
    adopted = execute_prepared_connected_change(
        prepared=different,
        output_parent=output,
        job_id=interrupted.job_id,
    )
    assert adopted.folder_run.result_root == interrupted.final_result_path
    changed = fixture.sofia_root / "media" / "cover.png"
    changed.write_bytes(changed.read_bytes() + b"changed-before-recovery")

    stale = service.run_or_resume(job_path)

    assert stale.lifecycle is FolderJobLifecycleV2.STALE
    assert stale.verified_artifacts is None
    assert stale.blocker_code is None
    assert service.status(job_path) == stale


def test_concurrent_identical_creation_returns_one_durable_job(
    tmp_path: Path,
) -> None:
    fixture, origin, output, _job_path = _receiver_job_inputs(tmp_path)
    jobs = tmp_path / "jobs"
    context = multiprocessing.get_context("spawn")
    start = context.Event()
    results = context.Queue()
    arguments = {
        "change_file": str(origin.change_file_path),
        "source": str(fixture.martin_root),
        "output": str(output),
        "idempotency_key": "receiver-multiprocess-idempotency",
    }
    processes = [
        context.Process(
            target=_concurrent_receiver_create,
            kwargs={
                "start": start,
                "result_queue": results,
                "job_path": str(jobs / f"candidate-{index}.json"),
                **arguments,
            },
        )
        for index in range(2)
    ]
    for process in processes:
        process.start()
    start.set()
    for process in processes:
        process.join(timeout=15)
        assert process.exitcode == 0
    observed = [results.get(timeout=2) for _process in processes]
    assert {item[0] for item in observed} == {"ok"}
    assert len({item[1] for item in observed}) == 1
    assert len({item[2] for item in observed}) == 1
    assert len(tuple(jobs.glob("*.json"))) == 1


def test_get_change_file_reverifies_current_result_bytes(tmp_path: Path) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    verified = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-tamper-read",
    )
    assert verified.final_result_path is not None
    other_output = tmp_path / "other-origin-output"
    other_output.mkdir()
    other_targets = dict(fixture.target_paths)
    other_targets["notes/client-brief.md"] = "alternate/client-brief.md"
    other = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=other_output,
        request=fixture.request,
        result_folder_name="northstar-other",
        target_by_original_path=other_targets,
    )
    result_change_file = verified.final_result_path / (
        "name-atlas/connected_change_capsule.json"
    )
    result_change_file.write_bytes(other.change_file_path.read_bytes())
    BagItWriter().finalize_tagmanifest(verified.final_result_path)

    with pytest.raises(ConnectedChangeJobServiceError) as raised:
        service.get_change_file(job_path)
    assert raised.value.code == "result_verification_blocked"


def test_restart_records_pending_cleanup_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-cleanup-failure",
    )

    def crash_with_partial_pending(*_args: object, **kwargs: object) -> None:
        paths = kwargs["transaction_paths"]
        paths.pending_root.mkdir()
        (paths.pending_root / "partial.tmp").write_bytes(b"regenerable")
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            job_service_module,
            "execute_prepared_connected_change",
            crash_with_partial_pending,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.run_or_resume(job_path)

    def fail_cleanup(_path: Path) -> None:
        raise PermissionError("injected cleanup refusal")

    with monkeypatch.context() as guarded:
        guarded.setattr(job_service_module.shutil, "rmtree", fail_cleanup)
        blocked = service.run_or_resume(job_path)
    assert blocked.lifecycle is FolderJobLifecycleV2.BLOCKED
    assert blocked.blocker_code == "pending_cleanup_failed"


def test_restart_records_complete_pending_promotion_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, origin, output, job_path = _receiver_job_inputs(tmp_path)
    service = ConnectedChangeJobService()
    service.create_application_job(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=output,
        job_path=job_path,
        idempotency_key="receiver-recovery-promotion-failure",
    )

    def crash_before_promotion(_pending: Path, _final: Path) -> None:
        raise _InjectedProcessCrash

    with monkeypatch.context() as guarded:
        guarded.setattr(
            transaction_module,
            "promote_directory_no_replace",
            crash_before_promotion,
        )
        with pytest.raises(_InjectedProcessCrash):
            service.run_or_resume(job_path)

    def fail_promotion(_pending: Path, _final: Path) -> None:
        raise FileExistsError("injected no-replace conflict")

    with monkeypatch.context() as guarded:
        guarded.setattr(
            job_service_module,
            "promote_directory_no_replace",
            fail_promotion,
        )
        blocked = service.run_or_resume(job_path)
    assert blocked.lifecycle is FolderJobLifecycleV2.BLOCKED
    assert blocked.blocker_code == "execution_recovery_promotion_blocked"


def test_receiver_result_name_equal_to_source_is_durably_blocked(
    tmp_path: Path,
) -> None:
    fixture, origin, _output, job_path = _receiver_job_inputs(tmp_path)
    colliding_source = fixture.martin_root.with_name(fixture.result_name)
    fixture.martin_root.rename(colliding_source)
    service = ConnectedChangeJobService()

    blocked = service.start_application(
        change_file_path=origin.change_file_path,
        source_root=colliding_source,
        output_parent=colliding_source.parent,
        job_path=job_path,
        idempotency_key="receiver-source-result-collision",
    )

    assert blocked.lifecycle is FolderJobLifecycleV2.BLOCKED
    assert blocked.blocker_code == "result_path_unavailable"
    assert service.status(job_path) == blocked
    assert colliding_source.is_dir()
    assert not (colliding_source.parent / fixture.result_name / "data").exists()


def test_origin_result_name_equal_to_source_is_durably_blocked(
    tmp_path: Path,
) -> None:
    source = tmp_path / "name-atlas-organized-copy"
    source.mkdir()
    (source / "note.txt").write_bytes(b"source remains\n")
    job_path = tmp_path / "jobs" / "origin-collision.json"
    service = ConnectedChangeJobService()

    blocked = service.start_deterministic_origin(
        source_root=source,
        output_parent=tmp_path,
        job_path=job_path,
        request="Prepare this project for handoff.",
        result_folder_name=source.name,
        target_by_original_path={"note.txt": "organized/note.txt"},
        idempotency_key="origin-source-result-collision",
    )

    assert blocked.lifecycle is FolderJobLifecycleV2.BLOCKED
    assert blocked.blocker_code == "result_path_unavailable"
    assert service.status(job_path) == blocked
    assert (source / "note.txt").read_bytes() == b"source remains\n"


def _receiver_job_inputs(
    tmp_path: Path,
) -> tuple[ConnectedChangeFixture, ConnectedChangeRunResult, Path, Path]:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    return fixture, origin, receiver_output, tmp_path / "jobs" / "receiver.json"
