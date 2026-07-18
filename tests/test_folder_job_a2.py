"""A2 acceptance tests for the persistent FolderRefactorJob authority."""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from pydantic import ValidationError

from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.job import (
    FolderJobBecameStaleError,
    FolderJobFinalizedError,
    FolderJobLifecycle,
    FolderJobLoadError,
    FolderJobLockError,
    FolderJobRevisionError,
    FolderRefactorJob,
    FolderRefactorJobStore,
    JobSourceDifferenceKind,
    build_new_job,
    canonical_job_bytes,
    compare_job_source,
    default_job_path,
    load_job,
    oslo_tz,
)


def _paths(tmp_path: Path) -> tuple[Path, Path, Path]:
    source = tmp_path / "source"
    output = tmp_path / "output"
    job_path = tmp_path / "state" / "job.json"
    source.mkdir()
    output.mkdir()
    (source / "notes.txt").write_text("alpha", encoding="utf-8")
    return source, output, job_path


def _new_job(
    tmp_path: Path,
    *,
    clock: datetime | None = None,
) -> tuple[FolderRefactorJob, FolderRefactorJobStore, Path]:
    source, output, job_path = _paths(tmp_path)
    timestamp = clock or datetime(2026, 7, 18, 16, 0, tzinfo=oslo_tz)
    job = build_new_job(
        source_root=source,
        output_parent=output,
        job_path=job_path,
        user_request="Organize the project for handoff.",
        display_name="Handoff",
        clock=lambda: timestamp,
    )
    store = FolderRefactorJobStore(
        job_path,
        clock=lambda: timestamp + timedelta(minutes=1),
    )
    return job, store, source


def _persist_new(
    tmp_path: Path,
) -> tuple[FolderRefactorJob, FolderRefactorJobStore, Path]:
    job, store, source = _new_job(tmp_path)
    with store.writer() as writer:
        saved = writer.save(job, expected_revision=None)
    return saved, store, source


def test_default_job_path_uses_uuid4_hex_and_exact_directory(
    tmp_path: Path,
) -> None:
    path = default_job_path(base_directory=tmp_path)

    assert path.parent == (tmp_path / ".name-atlas" / "jobs").resolve()
    assert path.suffix == ".json"
    identifier = path.stem
    assert uuid.UUID(hex=identifier).version == 4
    assert uuid.UUID(hex=identifier).hex == identifier


def test_new_job_round_trips_strict_canonical_bytes(tmp_path: Path) -> None:
    saved, store, source = _persist_new(tmp_path)

    loaded = store.load()

    assert loaded == saved
    assert loaded.schema_version == "folder-refactor-job.v1"
    assert loaded.revision == 0
    assert loaded.lifecycle is FolderJobLifecycle.PLANNING
    assert loaded.source_root == source.resolve()
    assert loaded.source_inventory.source_commitment
    assert loaded.planner_progress is None
    assert loaded.accepted_plan is None
    assert store.path.read_bytes() == canonical_job_bytes(loaded)
    assert store.path.read_bytes().endswith(b"\n")


def test_job_model_and_loader_fail_closed_on_unknown_or_corrupt_fields(
    tmp_path: Path,
) -> None:
    saved, store, _ = _persist_new(tmp_path)
    payload = saved.model_dump(mode="json")
    payload["unexpected"] = True

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        FolderRefactorJob.model_validate(payload)

    store.path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(FolderJobLoadError, match="corrupt, or unsupported"):
        load_job(store.path)

    store.path.write_text("{not-json", encoding="utf-8")
    with pytest.raises(FolderJobLoadError, match="corrupt, or unsupported"):
        load_job(store.path)


def test_loader_rejects_symlink_and_wrong_persisted_path(tmp_path: Path) -> None:
    saved, store, _ = _persist_new(tmp_path)
    alias = tmp_path / "alias.json"
    alias.symlink_to(store.path)

    with pytest.raises(FolderJobLoadError, match="regular file"):
        load_job(alias)

    wrong_path = tmp_path / "wrong.json"
    wrong_path.write_bytes(canonical_job_bytes(saved))
    with pytest.raises(FolderJobLoadError, match="persisted local pointer"):
        load_job(wrong_path)


def test_expected_revision_and_immutable_identity_are_enforced(tmp_path: Path) -> None:
    saved, store, _ = _persist_new(tmp_path)

    with store.writer() as writer:
        updated = writer.save(saved, expected_revision=0)
    assert updated.revision == 1
    assert updated.updated_at > saved.updated_at

    with (
        store.writer() as writer,
        pytest.raises(FolderJobRevisionError, match="revision changed"),
    ):
        writer.save(updated, expected_revision=0)

    changed_request = updated.model_copy(update={"user_request": "Different"})
    with (
        store.writer() as writer,
        pytest.raises(FolderJobRevisionError, match="immutable"),
    ):
        writer.save(changed_request, expected_revision=1)


def test_process_lock_fails_closed_on_second_writer(tmp_path: Path) -> None:
    _, store, _ = _persist_new(tmp_path)

    second_writer = store.writer()
    with store.writer(), pytest.raises(FolderJobLockError, match="already open"):
        second_writer.__enter__()


def test_blocked_job_is_terminal_and_immutable(tmp_path: Path) -> None:
    saved, store, _ = _persist_new(tmp_path)
    blocked_candidate = saved.model_copy(
        update={
            "lifecycle": FolderJobLifecycle.BLOCKED,
            "blocker_code": "unsupported_request",
            "blocker_message": "The request requires deletion.",
        }
    )
    with store.writer() as writer:
        blocked = writer.save(blocked_candidate, expected_revision=0)

    assert blocked.lifecycle is FolderJobLifecycle.BLOCKED
    with (
        store.writer() as writer,
        pytest.raises(FolderJobFinalizedError, match="immutable"),
    ):
        writer.save(blocked, expected_revision=1)


@pytest.mark.parametrize(
    ("mutation", "expected_kind"),
    [
        ("resize", JobSourceDifferenceKind.RESIZED),
        ("content", JobSourceDifferenceKind.CONTENT_CHANGED),
        ("replace", JobSourceDifferenceKind.REPLACED),
        ("rename", JobSourceDifferenceKind.RENAMED),
        ("add", JobSourceDifferenceKind.ADDED),
        ("remove", JobSourceDifferenceKind.REMOVED),
    ],
)
def test_source_comparison_reports_exact_deterministic_difference(
    tmp_path: Path,
    mutation: str,
    expected_kind: JobSourceDifferenceKind,
) -> None:
    job, _, source = _new_job(tmp_path)
    member = source / "notes.txt"
    if mutation == "resize":
        member.write_text("longer", encoding="utf-8")
    elif mutation == "content":
        member.write_text("omega", encoding="utf-8")
    elif mutation == "replace":
        replacement = source / "replacement.tmp"
        replacement.write_text("alpha", encoding="utf-8")
        os.replace(replacement, member)
    elif mutation == "rename":
        member.rename(source / "renamed.txt")
    elif mutation == "add":
        (source / "added.txt").write_text("new", encoding="utf-8")
    elif mutation == "remove":
        member.unlink()
        (source / "remaining.txt").write_text("remain", encoding="utf-8")

    differences = compare_job_source(job, scan_folder(source))

    assert expected_kind in {difference.kind for difference in differences}
    assert differences == tuple(
        sorted(
            differences,
            key=lambda item: (
                (item.before or item.after).relative_path,
                item.kind.value,
                item.after.relative_path if item.after else "",
            ),
        )
    )


def test_rehydrate_persists_exact_stale_transition(tmp_path: Path) -> None:
    saved, store, source = _persist_new(tmp_path)
    (source / "notes.txt").write_text("omega", encoding="utf-8")

    stale = store.rehydrate()

    assert stale.revision == saved.revision + 1
    assert stale.lifecycle is FolderJobLifecycle.STALE
    assert [item.kind for item in stale.stale_differences] == [
        JobSourceDifferenceKind.CONTENT_CHANGED
    ]
    assert stale.stale_differences[0].before.relative_path == "notes.txt"
    assert stale.stale_differences[0].after.relative_path == "notes.txt"
    assert store.load() == stale
    with (
        store.writer() as writer,
        pytest.raises(FolderJobFinalizedError, match="immutable"),
    ):
        writer.save(stale, expected_revision=stale.revision)


def test_stale_before_state_must_bind_to_immutable_snapshot(tmp_path: Path) -> None:
    _, store, source = _persist_new(tmp_path)
    (source / "notes.txt").write_text("omega", encoding="utf-8")
    stale = store.rehydrate()
    difference = stale.stale_differences[0]
    assert difference.before is not None
    forged_before = difference.before.model_copy(
        update={"inode": difference.before.inode + 1}
    )
    forged_difference = difference.model_copy(update={"before": forged_before})
    payload = {
        **stale.model_dump(mode="python"),
        "stale_differences": (forged_difference,),
    }

    with pytest.raises(ValidationError, match="must match the job snapshot"):
        FolderRefactorJob.model_validate(payload, strict=True)


def test_mutation_rescan_persists_stale_before_rejecting_candidate(
    tmp_path: Path,
) -> None:
    saved, store, source = _persist_new(tmp_path)
    (source / "notes.txt").write_text("changed", encoding="utf-8")

    with (
        store.writer() as writer,
        pytest.raises(FolderJobBecameStaleError) as captured,
    ):
        writer.save(saved, expected_revision=0)

    assert captured.value.stale_job.lifecycle is FolderJobLifecycle.STALE
    assert store.load() == captured.value.stale_job


def test_scan_failure_persists_exact_stale_blocker(tmp_path: Path) -> None:
    saved, store, source = _persist_new(tmp_path)
    (source / "notes.txt").unlink()
    source.rmdir()

    stale = store.rehydrate()

    assert stale.revision == saved.revision + 1
    assert stale.lifecycle is FolderJobLifecycle.STALE
    assert stale.stale_differences == ()
    assert stale.source_scan_blocker.code == "source_scan_failed"
    assert "cannot be inspected" in stale.source_scan_blocker.detail


def test_job_path_cannot_overlap_source_or_output(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    (source / "notes.txt").write_text("alpha", encoding="utf-8")

    with pytest.raises(ValidationError, match="job state cannot be inside"):
        build_new_job(
            source_root=source,
            output_parent=output,
            job_path=source / ".name-atlas" / "jobs" / "job.json",
            user_request="Organize it.",
        )
