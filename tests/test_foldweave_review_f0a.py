"""F0a review-barrier and exact-acceptance integration evidence."""

from __future__ import annotations

import builtins
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
from connected_change_fixtures import (
    make_connected_change_fixture,
    portable_tree,
    tree_state,
)

from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
)

_FORBIDDEN_RECEIVER_IMPORTS = (
    "name_atlas.decision_cards.budget",
    "name_atlas.decision_cards.providers",
    "name_atlas.folder_refactor.planner_provider",
)


def test_f0a_origin_and_receiver_review_accept_converge_and_reconstruct(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Both journeys stop for review, then exact acceptance converges."""

    monkeypatch.chdir(tmp_path)
    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    jobs = tmp_path / "jobs"
    sofia_output = tmp_path / "sofia-output"
    martin_output = tmp_path / "martin-output"
    for directory in (jobs, sofia_output, martin_output):
        directory.mkdir()

    sofia_before = tree_state(fixture.sofia_root)
    martin_before = tree_state(fixture.martin_root)
    budget_path = tmp_path / ".name-atlas" / "api_budget.json"

    origin = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=sofia_output,
        job_path=jobs / "sofia.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="f0a-sofia-review",
    )

    _assert_reviewing_without_output(origin, sofia_output)
    assert _regular_file_paths(origin.preview.current_tree_members) == (
        _source_file_paths(fixture.sofia_root)
    )
    assert _regular_file_paths(origin.preview.proposed_tree_members) == set(
        fixture.target_paths.values()
    )
    assert _empty_directory_paths(origin.preview.current_tree_members) == {"empty/keep"}
    assert _empty_directory_paths(origin.preview.proposed_tree_members) == {
        "empty/keep"
    }
    _assert_preview_counts(
        origin.preview.counts,
        changed_path_count=3,
        renamed_count=2,
        moved_count=3,
    )
    assert service.status(origin.job_path) == origin
    assert tree_state(fixture.sofia_root) == sofia_before

    accepted_origin = service.accept(
        job_path=origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=sofia_output,
        result_folder_name=fixture.result_name,
        idempotency_key="f0a-accept-sofia",
        channel="native_app",
    )
    _assert_verified_separate_result(
        accepted_origin,
        source_root=fixture.sofia_root,
        output_parent=sofia_output,
    )
    assert tree_state(fixture.sofia_root) == sofia_before

    change_file_path = _change_file_path(service.get_change_file(origin.job_path))
    change_file_before = _file_state(change_file_path)
    watched_imports_before = _watched_imports()
    with monkeypatch.context() as receiver_guard:
        receiver_guard.setattr(builtins, "__import__", _guarded_receiver_import())
        receiver = service.prepare_application_review(
            change_file_path=change_file_path,
            source_root=fixture.martin_root,
            output_parent=martin_output,
            job_path=jobs / "martin.json",
            idempotency_key="f0a-martin-review",
        )

    _assert_reviewing_without_output(receiver, martin_output)
    assert _watched_imports() == watched_imports_before
    assert not budget_path.exists()
    assert _regular_file_paths(receiver.preview.current_tree_members) == (
        _source_file_paths(fixture.martin_root)
    )
    assert _regular_file_paths(receiver.preview.proposed_tree_members) == set(
        fixture.target_paths.values()
    )
    assert _empty_directory_paths(receiver.preview.current_tree_members) == {
        "empty/keep"
    }
    assert _empty_directory_paths(receiver.preview.proposed_tree_members) == {
        "empty/keep"
    }
    _assert_preview_counts(
        receiver.preview.counts,
        changed_path_count=5,
        renamed_count=5,
        moved_count=5,
    )
    assert service.status(receiver.job_path) == receiver
    assert tree_state(fixture.martin_root) == martin_before
    assert _file_state(change_file_path) == change_file_before

    receiver_review_revision = receiver.revision
    receiver_preview_fingerprint = receiver.preview.preview_fingerprint
    receiver_candidate_fingerprint = receiver.preview.compiled_candidate_fingerprint
    accepted_receiver = service.accept(
        job_path=receiver.job_path,
        expected_revision=receiver_review_revision,
        preview_fingerprint=receiver_preview_fingerprint,
        candidate_fingerprint=receiver_candidate_fingerprint,
        output_parent=martin_output,
        result_folder_name=fixture.result_name,
        idempotency_key="f0a-accept-martin",
        channel="native_app",
    )
    _assert_verified_separate_result(
        accepted_receiver,
        source_root=fixture.martin_root,
        output_parent=martin_output,
    )
    assert accepted_origin.final_result_path != accepted_receiver.final_result_path
    assert accepted_origin.verified_artifacts is not None
    assert accepted_receiver.verified_artifacts is not None
    assert (
        accepted_origin.verified_artifacts.organized_tree_commitment
        == accepted_receiver.verified_artifacts.organized_tree_commitment
    )

    for job in (accepted_origin, accepted_receiver):
        verification = service.verify_result(job.job_path)
        assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
        assert verification.job_id == job.job_id

    assert accepted_receiver.final_result_path is not None
    result_before_retry = tree_state(accepted_receiver.final_result_path)
    receiver_job_before_retry = receiver.job_path.read_bytes()
    repeated = service.accept(
        job_path=receiver.job_path,
        expected_revision=receiver_review_revision,
        preview_fingerprint=receiver_preview_fingerprint,
        candidate_fingerprint=receiver_candidate_fingerprint,
        output_parent=martin_output,
        result_folder_name=fixture.result_name,
        idempotency_key="f0a-accept-martin",
        channel="native_app",
    )
    assert repeated == accepted_receiver
    assert receiver.job_path.read_bytes() == receiver_job_before_retry
    assert tuple(martin_output.iterdir()) == (accepted_receiver.final_result_path,)
    assert tree_state(accepted_receiver.final_result_path) == result_before_retry

    restored = tmp_path / "restored" / "martin-original"
    restored.parent.mkdir()
    report = service.recreate_original(receiver.job_path, restored)
    assert report.source_commitment == (
        accepted_receiver.source_inventory.source_commitment
    )
    assert portable_tree(restored) == portable_tree(fixture.martin_root)
    assert portable_tree(restored) != portable_tree(fixture.sofia_root)
    assert tree_state(fixture.sofia_root) == sofia_before
    assert tree_state(fixture.martin_root) == martin_before
    assert _file_state(change_file_path) == change_file_before


@pytest.mark.parametrize(
    "mismatch",
    ["stale_revision", "preview_fingerprint", "candidate_fingerprint"],
)
def test_f0a_accept_refuses_stale_or_mismatched_authority_without_execution(
    tmp_path: Path,
    mismatch: str,
) -> None:
    """Acceptance cannot execute anything other than the visible revision."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    source_before = tree_state(fixture.sofia_root)
    service = FoldweaveReviewService()
    reviewing = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / f"{mismatch}.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key=f"f0a-review-{mismatch}",
    )
    _assert_reviewing_without_output(reviewing, output)
    job_before = reviewing.job_path.read_bytes()

    expected_revision = reviewing.revision
    preview_fingerprint = reviewing.preview.preview_fingerprint
    candidate_fingerprint = reviewing.preview.compiled_candidate_fingerprint
    if mismatch == "stale_revision":
        expected_revision += 1
    elif mismatch == "preview_fingerprint":
        preview_fingerprint = _different_sha256(preview_fingerprint)
    elif mismatch == "candidate_fingerprint":
        candidate_fingerprint = _different_sha256(candidate_fingerprint)
    else:
        raise AssertionError(f"Unhandled mismatch: {mismatch}")

    with pytest.raises(RuntimeError):
        service.accept(
            job_path=reviewing.job_path,
            expected_revision=expected_revision,
            preview_fingerprint=preview_fingerprint,
            candidate_fingerprint=candidate_fingerprint,
            output_parent=output,
            result_folder_name=fixture.result_name,
            idempotency_key=f"f0a-rejected-accept-{mismatch}",
            channel="native_app",
        )

    assert service.status(reviewing.job_path) == reviewing
    assert reviewing.job_path.read_bytes() == job_before
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.sofia_root) == source_before


def test_f0a_changed_source_terminally_stales_before_acceptance(
    tmp_path: Path,
) -> None:
    """A reviewed preview cannot authorize a source that changed afterward."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    reviewing = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "source-stale.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="f0a-source-stale-review",
    )
    _assert_reviewing_without_output(reviewing, output)
    changed = fixture.sofia_root / "media" / "cover.png"
    changed.write_bytes(changed.read_bytes() + b"changed after review")

    stale = service.accept(
        job_path=reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=fixture.result_name,
        idempotency_key="f0a-source-stale-accept",
        channel="native_app",
    )

    assert stale.lifecycle is FolderJobLifecycleV3.STALE
    assert stale.staleness is not None
    assert stale.staleness.code == "source_changed"
    assert stale.execution_authorization is None
    assert stale.pending_result_path is None
    assert stale.final_result_path is None
    assert tuple(output.iterdir()) == ()


def test_f0a_changed_change_file_terminally_stales_receiver_review(
    tmp_path: Path,
) -> None:
    """Receiver acceptance binds the exact imported Change File identity."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=tmp_path / "jobs" / "change-source.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="f0a-change-source-review",
    )
    verified_origin = service.accept(
        job_path=origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=origin_output,
        result_folder_name=fixture.result_name,
        idempotency_key="f0a-change-source-accept",
        channel="native_app",
    )
    change_file_path = _change_file_path(
        service.get_change_file(verified_origin.job_path)
    )
    receiver = service.prepare_application_review(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=tmp_path / "jobs" / "change-receiver.json",
        idempotency_key="f0a-change-receiver-review",
    )
    _assert_reviewing_without_output(receiver, receiver_output)
    metadata = change_file_path.stat()
    os.utime(
        change_file_path,
        ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 1_000_000),
    )

    stale = service.accept(
        job_path=receiver.job_path,
        expected_revision=receiver.revision,
        preview_fingerprint=receiver.preview.preview_fingerprint,
        candidate_fingerprint=receiver.preview.compiled_candidate_fingerprint,
        output_parent=receiver_output,
        result_folder_name=fixture.result_name,
        idempotency_key="f0a-change-receiver-accept",
        channel="native_app",
    )

    assert stale.lifecycle is FolderJobLifecycleV3.STALE
    assert stale.staleness is not None
    assert stale.staleness.code == "change_file_changed"
    assert tuple(receiver_output.iterdir()) == ()


def _assert_reviewing_without_output(job: Any, output_parent: Path) -> None:
    assert job.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert job.preview is not None
    assert job.preview.counts is not None
    _assert_sha256(job.preview.preview_fingerprint)
    _assert_sha256(job.preview.compiled_candidate_fingerprint)
    assert job.pending_result_path is None
    assert job.final_result_path is None
    assert job.verified_artifacts is None
    assert tuple(output_parent.iterdir()) == ()


def _assert_verified_separate_result(
    job: Any,
    *,
    source_root: Path,
    output_parent: Path,
) -> None:
    assert job.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert job.pending_result_path is None
    assert job.final_result_path is not None
    assert job.final_result_path.parent == output_parent.resolve()
    assert job.final_result_path != source_root.resolve()
    assert job.final_result_path.is_dir()
    assert job.verified_artifacts is not None
    assert job.preview is not None
    assert job.execution_authorization is not None
    assert (
        job.execution_authorization.preview_fingerprint
        == job.preview.preview_fingerprint
    )
    assert (
        job.execution_authorization.candidate_fingerprint
        == job.preview.compiled_candidate_fingerprint
    )
    assert tuple(output_parent.iterdir()) == (job.final_result_path,)


def _regular_file_paths(members: tuple[Any, ...]) -> set[str]:
    return {
        member.relative_path
        for member in members
        if member.member_kind == "regular_file"
    }


def _empty_directory_paths(members: tuple[Any, ...]) -> set[str]:
    return {
        member.relative_path
        for member in members
        if member.member_kind == "empty_directory"
    }


def _source_file_paths(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()
    }


def _assert_preview_counts(
    counts: Any,
    *,
    changed_path_count: int,
    renamed_count: int,
    moved_count: int,
) -> None:
    assert counts.file_count == 6
    assert counts.empty_directory_count == 1
    assert counts.changed_path_count == changed_path_count
    assert counts.renamed_count == renamed_count
    assert counts.moved_count == moved_count
    assert counts.link_count == 2
    assert counts.link_updated_count == 2
    assert counts.protected_count == 1
    assert counts.blocker_count == 0


def _change_file_path(download: Any) -> Path:
    path = download[0] if isinstance(download, tuple) else download.path
    assert isinstance(path, Path)
    assert path.is_file()
    return path


def _file_state(path: Path) -> tuple[int, int, int, int, bytes]:
    metadata = path.lstat()
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        path.read_bytes(),
    )


def _assert_sha256(value: str) -> None:
    assert len(value) == 64
    assert set(value) <= set("0123456789abcdef")


def _different_sha256(value: str) -> str:
    _assert_sha256(value)
    replacement = "0" if value[0] != "0" else "1"
    return replacement + value[1:]


def _watched_imports() -> frozenset[str]:
    return frozenset(
        name
        for name in sys.modules
        if any(
            name == forbidden or name.startswith(f"{forbidden}.")
            for forbidden in _FORBIDDEN_RECEIVER_IMPORTS
        )
    )


def _guarded_receiver_import() -> Any:
    original_import = builtins.__import__

    def guarded_import(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> ModuleType:
        if any(
            name == forbidden or name.startswith(f"{forbidden}.")
            for forbidden in _FORBIDDEN_RECEIVER_IMPORTS
        ):
            raise AssertionError(
                f"Receiver review imported forbidden authority: {name}"
            )
        return original_import(name, globals, locals, fromlist, level)

    return guarded_import
