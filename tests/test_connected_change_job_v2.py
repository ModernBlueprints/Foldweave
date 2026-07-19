"""Focused C1 tests for the planner-free Connected Change job authority."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
)

from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
    FolderJobLifecycleV2,
    FolderJobV2FinalizedError,
    FolderJobV2IdempotencyConflict,
    FolderJobV2LoadError,
    FolderJobV2RevisionError,
    FolderJobV2WriteError,
    FolderJobVerifiedArtifactsV2,
    FolderMutationRequestV2,
    FolderRefactorJobV2,
    FolderRefactorJobV2Store,
    GptPlannedJobAuthorityV2,
    GptPlannerCheckpointV2,
    LegacyFolderJobV1Evidence,
    LegacyV1NonterminalJobError,
    build_idempotency_binding,
    build_new_capsule_job_v2,
    build_new_gpt_job_v2,
    canonical_job_v2_bytes,
    evolve_job_v2,
    find_idempotent_job_v2,
    load_folder_job_record,
)
from name_atlas.folder_refactor.connected_change.service import (
    create_connected_change_origin,
    prepare_connected_change_application,
)


@dataclass(frozen=True, slots=True)
class _CapsuleJobFixture:
    fixture: ConnectedChangeFixture
    change_file_path: Path
    output_parent: Path
    job_path: Path


@pytest.fixture
def capsule_job_fixture(tmp_path: Path) -> _CapsuleJobFixture:
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
    return _CapsuleJobFixture(
        fixture=fixture,
        change_file_path=origin.change_file_path,
        output_parent=receiver_output,
        job_path=tmp_path / "state" / "receiver.json",
    )


def _new_capsule_job(value: _CapsuleJobFixture) -> FolderRefactorJobV2:
    return build_new_capsule_job_v2(
        source_root=value.fixture.martin_root,
        output_parent=value.output_parent,
        job_path=value.job_path,
        change_file_path=value.change_file_path,
        idempotency_key="receiver-request-1",
    )


def _save_new(job: FolderRefactorJobV2) -> FolderRefactorJobV2Store:
    store = FolderRefactorJobV2Store(job.job_path)
    with store.writer() as writer:
        assert writer.save_new(job) == job
    return store


def test_capsule_job_is_canonical_strict_and_idempotent(
    capsule_job_fixture: _CapsuleJobFixture,
) -> None:
    job = _new_capsule_job(capsule_job_fixture)
    store = _save_new(job)

    assert store.load() == job
    assert job.authority.kind == "capsule_applied"
    assert job.authority.change_file_binding.path == (
        capsule_job_fixture.change_file_path.resolve()
    )
    assert job.authority.change_file_binding.change_file.core.request == (
        capsule_job_fixture.fixture.request
    )
    assert canonical_job_v2_bytes(job) == capsule_job_fixture.job_path.read_bytes()
    assert "receiver-request-1" not in capsule_job_fixture.job_path.read_text()

    mutation = FolderMutationRequestV2(
        operation="capsule_applied",
        source_root=capsule_job_fixture.fixture.martin_root.resolve(),
        output_parent=capsule_job_fixture.output_parent.resolve(),
        user_request=capsule_job_fixture.fixture.request,
        change_file_path=capsule_job_fixture.change_file_path.resolve(),
    )
    same_binding = build_idempotency_binding("receiver-request-1", mutation)
    assert find_idempotent_job_v2(job.job_path.parent, same_binding) == job

    different_request = FolderMutationRequestV2(
        operation="capsule_applied",
        source_root=capsule_job_fixture.fixture.martin_root.resolve(),
        output_parent=(capsule_job_fixture.output_parent.parent / "other").resolve(),
        user_request=capsule_job_fixture.fixture.request,
        change_file_path=capsule_job_fixture.change_file_path.resolve(),
    )
    conflict = build_idempotency_binding("receiver-request-1", different_request)
    with pytest.raises(FolderJobV2IdempotencyConflict, match="another canonical"):
        find_idempotent_job_v2(job.job_path.parent, conflict)


def test_capsule_job_progresses_to_verified_and_then_is_immutable(
    capsule_job_fixture: _CapsuleJobFixture,
) -> None:
    job = _new_capsule_job(capsule_job_fixture)
    store = _save_new(job)
    prepared = prepare_connected_change_application(
        change_file_path=capsule_job_fixture.change_file_path,
        source_root=capsule_job_fixture.fixture.martin_root,
    )
    authority = CapsuleAppliedJobAuthorityV2(
        change_file_binding=job.authority.change_file_binding,
        match_report=prepared.match_report,
        execution_origin=prepared.execution_origin,
    )
    candidate = evolve_job_v2(
        job,
        authority=authority,
        accepted_plan=prepared.accepted_plan,
        lifecycle=FolderJobLifecycleV2.EXECUTING,
    )
    with store.writer() as writer:
        executing = writer.save(candidate, expected_current=job)
    assert executing.revision == 1
    assert executing.authority.execution_origin.provider_call_count == 0
    assert executing.authority.execution_origin.api_used is False
    assert executing.authority.execution_origin.external_network_used is False

    with store.writer() as writer:
        begun = writer.begin_execution(executing)
    assert begun.revision == 2
    assert begun.pending_result_path is not None
    assert begun.final_result_path is not None
    begun.final_result_path.mkdir()
    artifacts = FolderJobVerifiedArtifactsV2(
        receipt_fingerprint="a" * 64,
        organized_tree_commitment="b" * 64,
        change_ledger_fingerprint="c" * 64,
        verification_fingerprint="d" * 64,
    )
    with store.writer() as writer:
        verified = writer.finalize_verified(begun, artifacts=artifacts)
    assert verified.revision == 3
    assert verified.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert store.load() == verified

    with (
        store.writer() as writer,
        pytest.raises(FolderJobV2FinalizedError, match="immutable"),
    ):
        writer.save(verified, expected_current=verified)


def test_revision_and_process_lock_fail_closed(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    (source / "note.txt").write_text("unchanged\n", encoding="utf-8")
    job = build_new_gpt_job_v2(
        source_root=source,
        output_parent=output,
        job_path=tmp_path / "state" / "job.json",
        user_request="Organize this project.",
        idempotency_key="gpt-request-1",
    )
    store = _save_new(job)
    first_writer = store.writer()
    with (
        first_writer,
        pytest.raises(FolderJobV2WriteError, match="already open"),
        store.writer(),
    ):
        pass

    blocked_candidate = evolve_job_v2(
        job,
        lifecycle=FolderJobLifecycleV2.BLOCKED,
        blocker_code="unsupported_request",
        blocker_message="The request is outside the supported contract.",
    )
    with store.writer() as writer:
        writer.save(blocked_candidate, expected_current=job)
    with (
        store.writer() as writer,
        pytest.raises(FolderJobV2RevisionError, match="expected checkpoint"),
    ):
        writer.save(blocked_candidate, expected_current=job)


def test_accepted_gpt_authority_requires_exact_evidence_ledger() -> None:
    with pytest.raises(ValueError, match="exact evidence ledger"):
        GptPlannedJobAuthorityV2(
            planner_checkpoint=GptPlannerCheckpointV2(
                status="accepted",
                accepted_plan_fingerprint="a" * 64,
            )
        )


def test_source_and_change_file_changes_terminally_stale_jobs(
    capsule_job_fixture: _CapsuleJobFixture,
    tmp_path: Path,
) -> None:
    source = tmp_path / "gpt-source"
    output = tmp_path / "gpt-output"
    source.mkdir()
    output.mkdir()
    source_file = source / "note.txt"
    source_file.write_text("before\n", encoding="utf-8")
    gpt_job = build_new_gpt_job_v2(
        source_root=source,
        output_parent=output,
        job_path=tmp_path / "gpt-state" / "job.json",
        user_request="Organize this project.",
        idempotency_key="gpt-stale-1",
    )
    gpt_store = _save_new(gpt_job)
    source_file.write_text("after!\n", encoding="utf-8")
    stale_source = gpt_store.load()
    assert stale_source.lifecycle is FolderJobLifecycleV2.STALE
    assert stale_source.revision == 1
    assert stale_source.staleness is not None
    assert stale_source.staleness.source_differences[0].relative_path == "note.txt"
    assert gpt_store.load() == stale_source

    capsule_job = _new_capsule_job(capsule_job_fixture)
    capsule_store = _save_new(capsule_job)
    original_bytes = capsule_job_fixture.change_file_path.read_bytes()
    replacement = capsule_job_fixture.change_file_path.with_suffix(".replacement")
    replacement.write_bytes(original_bytes)
    os.replace(replacement, capsule_job_fixture.change_file_path)
    stale_change = capsule_store.load()
    assert stale_change.lifecycle is FolderJobLifecycleV2.STALE
    assert stale_change.staleness is not None
    assert stale_change.staleness.change_file_code == "change_file_changed"


def test_strict_parser_rejects_noncanonical_and_unknown_fields(tmp_path: Path) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    (source / "note.txt").write_text("text\n", encoding="utf-8")
    job = build_new_gpt_job_v2(
        source_root=source,
        output_parent=output,
        job_path=tmp_path / "state" / "job.json",
        user_request="Organize this project.",
        idempotency_key="strict-1",
    )
    store = _save_new(job)
    store.path.write_bytes(canonical_job_v2_bytes(job) + b" ")
    with pytest.raises(FolderJobV2LoadError, match="not canonical"):
        load_folder_job_record(store.path)

    payload = job.model_dump(mode="json")
    payload["unexpected"] = True
    store.path.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(FolderJobV2LoadError, match="corrupt"):
        load_folder_job_record(store.path)


def test_v1_dispatch_is_terminal_read_only_and_nonterminal_requires_fresh_job(
    tmp_path: Path,
) -> None:
    from name_atlas.folder_refactor.job import (
        FolderJobLifecycle,
        FolderRefactorJob,
        build_new_job,
        canonical_job_bytes,
    )

    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    (source / "note.txt").write_text("text\n", encoding="utf-8")
    path = tmp_path / "state" / "legacy.json"
    legacy = build_new_job(
        source_root=source,
        output_parent=output,
        job_path=path,
        user_request="Organize this project.",
    )
    path.parent.mkdir()
    path.write_bytes(canonical_job_bytes(legacy))
    with pytest.raises(LegacyV1NonterminalJobError, match="fresh"):
        load_folder_job_record(path)

    terminal = FolderRefactorJob.model_validate(
        {
            **legacy.model_dump(mode="python"),
            "lifecycle": FolderJobLifecycle.BLOCKED,
            "blocker_code": "historical_blocker",
            "blocker_message": "Historical v1 job stopped.",
        },
        strict=True,
    )
    terminal_bytes = canonical_job_bytes(terminal)
    path.write_bytes(terminal_bytes)
    record = load_folder_job_record(path)
    assert isinstance(record, LegacyFolderJobV1Evidence)
    assert record.lifecycle == "blocked"
    assert record.raw_sha256 == canonical_sha256_bytes_for_test(terminal_bytes)


def test_receiver_job_module_does_not_import_provider_or_budget() -> None:
    command = (
        "import sys; "
        "import name_atlas.folder_refactor.connected_change.job_v2; "
        "forbidden={'name_atlas.folder_refactor.planner_provider',"
        "'name_atlas.decision_cards.providers','name_atlas.decision_cards.budget'}; "
        "assert not (forbidden & set(sys.modules)), forbidden & set(sys.modules)"
    )
    completed = subprocess.run(
        [sys.executable, "-c", command],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stderr


def canonical_sha256_bytes_for_test(payload: bytes) -> str:
    """Return the expected raw digest without importing a private implementation."""

    return hashlib.sha256(payload).hexdigest()
