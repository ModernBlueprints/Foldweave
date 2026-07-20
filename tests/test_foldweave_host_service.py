"""F0c hosted-planning authority over the shared v3 review engine."""

from __future__ import annotations

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from threading import Barrier
from zoneinfo import ZoneInfo

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
    tree_state,
)

from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    FolderRefactorJobV3,
    GptDerivativeJobAuthorityV3,
    GptHostedJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
)
from name_atlas.folder_refactor.contracts import (
    FolderPlan,
    FolderPlanEntry,
)
from name_atlas.folder_refactor.foldweave_host_contracts import (
    FolderHostPlanRevisionEntryV1,
    FolderHostPlanRevisionV1,
)
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.foldweave_host_service import (
    FoldweaveHostPlanningService,
    FoldweaveHostServiceError,
)
from name_atlas.foldweave_local_handles import (
    FoldweaveLocalHandleError,
    FoldweaveLocalHandleStore,
)
from name_atlas.foldweave_paths import FoldweavePaths
from name_atlas.native_bridge import NativePathRole

oslo_tz = ZoneInfo("Europe/Oslo")


def test_chatgpt_hosted_plan_revision_accept_and_verify(tmp_path: Path) -> None:
    """Hosted inference stays truthful while deterministic code owns execution."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    source_before = tree_state(fixture.sofia_root)
    tokens = iter(("A" * 43, "B" * 43))
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: next(tokens),
    )
    source_handle = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=fixture.sofia_root,
        channel="chatgpt_hosted",
    )
    output_handle = handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=output,
        channel="chatgpt_hosted",
    )
    service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        handle_store=handles,
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )

    job = service.create_or_resume_planning_job(
        source_handle=source_handle.handle,
        output_handle=output_handle.handle,
        request=fixture.request,
        disclosure_acknowledged=True,
        idempotency_key="chatgpt-f0c-create",
        model_transport="chatgpt_hosted",
    )
    assert job.lifecycle is FolderJobLifecycleV3.PLANNING
    assert isinstance(job.authority, GptHostedJobAuthorityV3)
    assert job.authority.evidence_ledger is None
    assert not tuple(output.iterdir())

    job, inventory_page, error_code = service.list_inventory_page(
        job_id=job.job_id,
        call_id="host_inventory_1",
    )
    assert error_code is None
    assert isinstance(inventory_page, dict)
    assert all("sha256" not in item for item in inventory_page["items"])
    evidence_fingerprint = (
        job.authority.planning_state.evidence_state.evidence_fingerprint
    )
    plan = FolderPlan(
        source_commitment=job.source_inventory.source_commitment,
        request_fingerprint=job.authority.planning_state.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name=fixture.result_name,
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=fixture.target_paths[item.relative_path],
                rationale="Organize the connected project for handoff.",
                evidence_ids=("initial_inventory",),
            )
            for item in job.source_inventory.files
            if not item.protected
        ),
        exclusions=(),
    )
    reviewing = service.submit_plan(
        job_id=job.job_id,
        call_id="host_submit_plan_1",
        plan=plan,
    )
    assert reviewing.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert reviewing.preview is not None
    assert isinstance(reviewing.authority, GptHostedJobAuthorityV3)
    assert reviewing.authority.execution_origin is not None
    origin = reviewing.authority.execution_origin
    assert origin.model_transport == "chatgpt_hosted"
    assert origin.provider_call_count == 0
    assert origin.api_used is False
    assert origin.store_false is None
    assert origin.model_alias is None
    assert origin.returned_model_ids == ()
    assert not tuple(output.iterdir())
    assert tree_state(fixture.sofia_root) == source_before

    first_mapping = next(
        mapping
        for mapping in reviewing.candidate_plan.file_mappings
        if not mapping.protected
    )
    revised_target = f"revised/{Path(first_mapping.target_path).name}"
    revising = service.begin_revision(
        job_id=reviewing.job_id,
        expected_revision=reviewing.revision,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        instruction="Place the first reviewed file in a revised folder.",
        idempotency_key="chatgpt-f0c-revision",
    )
    assert revising.lifecycle is FolderJobLifecycleV3.REVISING
    assert not tuple(output.iterdir())

    revision = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=canonical_sha256(reviewing.candidate_plan),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=first_mapping.file_id,
                replacement_target_path=revised_target,
                rationale="Apply the user's exact revision.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    revised = service.submit_plan_revision(
        job_id=reviewing.job_id,
        call_id="host_submit_revision_1",
        revision=revision,
    )
    assert revised.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert revised.proposal_revision == 1
    assert revised.preview is not None
    assert revised.preview.preview_fingerprint != reviewing.preview.preview_fingerprint
    assert not tuple(output.iterdir())

    verified = service.accept_plan_and_create_copy(
        job_id=revised.job_id,
        expected_revision=revised.revision,
        preview_fingerprint=revised.preview.preview_fingerprint,
        candidate_fingerprint=revised.preview.compiled_candidate_fingerprint,
        result_folder_name=revised.candidate_plan.result_folder_name,
        idempotency_key="chatgpt-f0c-accept",
        channel="chatgpt_hosted",
    )
    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert verified.final_result_path is not None
    assert verified.final_result_path.is_dir()
    assert tree_state(fixture.sofia_root) == source_before
    verification = service.verify_result(verified.job_id)
    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED


def test_opaque_handles_never_expose_local_paths(tmp_path: Path) -> None:
    """Public handle serialization is path-free and role/channel bound."""

    source = tmp_path / "private-source"
    source.mkdir()
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: "C" * 43,
    )
    public = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=source,
        channel="chatgpt_hosted",
    )
    encoded = public.model_dump_json()
    assert str(source) not in encoded
    assert public.display_name == source.name


def test_host_tool_retries_are_exact_and_conflicting_reuse_blocks(
    tmp_path: Path,
) -> None:
    """Host call IDs and revision keys bind one canonical request."""

    fixture, _, service, planning = _start_host_job(tmp_path)
    after_evidence, first_result, first_error = service.list_inventory_page(
        job_id=planning.job_id,
        call_id="inventory_retry",
        page_size=12,
    )
    retried, retry_result, retry_error = service.list_inventory_page(
        job_id=planning.job_id,
        call_id="inventory_retry",
        page_size=12,
    )
    assert retried == after_evidence
    assert retry_result == first_result
    assert retry_error == first_error
    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.list_inventory_page(
            job_id=planning.job_id,
            call_id="inventory_retry",
            page_size=13,
        )

    plan = _complete_host_plan(fixture, after_evidence)
    reviewing = service.submit_plan(
        job_id=planning.job_id,
        call_id="plan_retry",
        plan=plan,
    )
    assert (
        service.submit_plan(
            job_id=planning.job_id,
            call_id="plan_retry",
            plan=plan,
        )
        == reviewing
    )
    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.submit_plan(
            job_id=planning.job_id,
            call_id="plan_retry",
            plan=plan.model_copy(update={"result_folder_name": "Different Result"}),
        )

    revising = service.begin_revision(
        job_id=reviewing.job_id,
        expected_revision=reviewing.revision,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        instruction="Move one reviewed file into a focused folder.",
        idempotency_key="revision-retry",
    )
    assert (
        service.begin_revision(
            job_id=reviewing.job_id,
            expected_revision=reviewing.revision,
            candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
            preview_fingerprint=reviewing.preview.preview_fingerprint,
            instruction="Move one reviewed file into a focused folder.",
            idempotency_key="revision-retry",
        )
        == revising
    )
    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.begin_revision(
            job_id=reviewing.job_id,
            expected_revision=reviewing.revision,
            candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
            preview_fingerprint=reviewing.preview.preview_fingerprint,
            instruction="Use a conflicting instruction with the same retry key.",
            idempotency_key="revision-retry",
        )


def test_host_revision_binding_replays_accepted_request_in_later_states(
    tmp_path: Path,
) -> None:
    """An accepted hosted key remains exact through review and verification."""

    _, _, service, reviewing = _build_reviewing_host_job(tmp_path)
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    mapping = next(
        item for item in reviewing.candidate_plan.file_mappings if not item.protected
    )
    begin = {
        "job_id": reviewing.job_id,
        "expected_revision": reviewing.revision,
        "candidate_fingerprint": reviewing.preview.compiled_candidate_fingerprint,
        "preview_fingerprint": reviewing.preview.preview_fingerprint,
        "instruction": "Move one reviewed file into the durable-binding folder.",
        "idempotency_key": "host-accepted-binding",
    }
    revising = service.begin_revision(**begin)
    revision = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=canonical_sha256(reviewing.candidate_plan),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=mapping.file_id,
                replacement_target_path=(
                    f"durable-binding/{Path(mapping.target_path).name}"
                ),
                rationale="Exercise the durable hosted retry binding.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    revised = service.submit_plan_revision(
        job_id=revising.job_id,
        call_id="host-accepted-binding-turn",
        revision=revision,
    )
    assert revised.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert len(revised.host_revision_mutation_bindings) == 1
    binding = revised.host_revision_mutation_bindings[0]
    assert binding.terminal_outcome == "proposal_replaced"
    assert binding.terminal_job_revision == revised.revision
    assert service.begin_revision(**begin) == revised
    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.begin_revision(
            **{
                **begin,
                "instruction": "Conflicting reuse must remain permanently refused.",
            }
        )

    assert revised.preview is not None
    assert revised.candidate_plan is not None
    verified = service.accept_plan_and_create_copy(
        job_id=revised.job_id,
        expected_revision=revised.revision,
        preview_fingerprint=revised.preview.preview_fingerprint,
        candidate_fingerprint=revised.preview.compiled_candidate_fingerprint,
        result_folder_name=revised.candidate_plan.result_folder_name,
        idempotency_key="host-accepted-binding-execution",
        channel="chatgpt_hosted",
    )
    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert service.begin_revision(**begin) == verified


def test_host_revision_binding_replays_rejection_after_keep_previous(
    tmp_path: Path,
) -> None:
    """A rejected hosted key remains exact after its prior proposal is restored."""

    _, _, service, reviewing = _build_reviewing_host_job(tmp_path)
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    editable = tuple(
        item for item in reviewing.candidate_plan.file_mappings if not item.protected
    )
    begin = {
        "job_id": reviewing.job_id,
        "expected_revision": reviewing.revision,
        "candidate_fingerprint": reviewing.preview.compiled_candidate_fingerprint,
        "preview_fingerprint": reviewing.preview.preview_fingerprint,
        "instruction": "Create a deterministic collision for retry testing.",
        "idempotency_key": "host-rejected-binding",
    }
    revising = service.begin_revision(**begin)
    rejected = service.submit_plan_revision(
        job_id=revising.job_id,
        call_id="host-rejected-binding-turn",
        revision=FolderHostPlanRevisionV1(
            base_candidate_fingerprint=canonical_sha256(reviewing.candidate_plan),
            entries=(
                FolderHostPlanRevisionEntryV1(
                    file_id=editable[0].file_id,
                    replacement_target_path=editable[1].target_path,
                    rationale="Exercise deterministic collision refusal.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        ),
    )
    assert rejected.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert len(rejected.host_revision_mutation_bindings) == 1
    assert (
        rejected.host_revision_mutation_bindings[0].terminal_outcome
        == "mechanically_rejected"
    )
    assert service.begin_revision(**begin) == rejected

    kept = service.keep_previous_proposal(
        job_id=rejected.job_id,
        expected_revision=rejected.revision,
        preview_fingerprint=rejected.preview.preview_fingerprint,
        candidate_fingerprint=rejected.preview.compiled_candidate_fingerprint,
        idempotency_key="host-rejected-binding-keep",
    )
    assert kept.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert service.begin_revision(**begin) == kept
    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.begin_revision(
            **{
                **begin,
                "instruction": "Conflicting rejected-key reuse must remain refused.",
            }
        )


def test_interrupted_host_revision_retry_precedes_staleness_and_limits(
    tmp_path: Path,
) -> None:
    """An interrupted exact retry is read-only even after its source changes."""

    fixture, _, service, reviewing = _build_reviewing_host_job(tmp_path)
    assert reviewing.preview is not None
    begin = {
        "job_id": reviewing.job_id,
        "expected_revision": reviewing.revision,
        "candidate_fingerprint": reviewing.preview.compiled_candidate_fingerprint,
        "preview_fingerprint": reviewing.preview.preview_fingerprint,
        "instruction": "Reserve one hosted revision before interruption.",
        "idempotency_key": "host-interrupted-binding",
    }
    revising = service.begin_revision(**begin)
    changed_relative = next(
        item.relative_path
        for item in reviewing.source_inventory.files
        if not item.protected
    )
    changed = fixture.sofia_root / changed_relative
    changed.write_bytes(changed.read_bytes() + b"changed after reservation\n")

    restarted = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    assert restarted.begin_revision(**begin) == revising
    assert restarted.status(revising.job_id).lifecycle is FolderJobLifecycleV3.REVISING
    with pytest.raises(FolderJobV3IdempotencyConflict):
        restarted.begin_revision(
            **{
                **begin,
                "instruction": "Conflicting interrupted-key reuse must be refused.",
            }
        )
    assert restarted.status(revising.job_id).lifecycle is FolderJobLifecycleV3.REVISING


def test_concurrent_host_create_is_one_durable_idempotent_job(tmp_path: Path) -> None:
    """Concurrent retries cannot race into two job authorities."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    tokens = iter(("X" * 43, "Y" * 43))
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: next(tokens),
    )
    source_handle = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=fixture.sofia_root,
        channel="chatgpt_hosted",
    )
    output_handle = handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=output,
        channel="chatgpt_hosted",
    )
    paths = FoldweavePaths(state_root=tmp_path / "state")
    service = FoldweaveHostPlanningService(
        paths=paths,
        handle_store=handles,
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    barrier = Barrier(2)

    def create() -> FolderRefactorJobV3:
        barrier.wait()
        return service.create_or_resume_planning_job(
            source_handle=source_handle.handle,
            output_handle=output_handle.handle,
            request=fixture.request,
            disclosure_acknowledged=True,
            idempotency_key="concurrent-host-create",
            model_transport="chatgpt_hosted",
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        first, second = tuple(executor.map(lambda _: create(), range(2)))
    assert first.job_id == second.job_id
    assert tuple(paths.jobs.glob("*.json")) == (paths.jobs / f"{first.job_id}.json",)

    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.create_or_resume_planning_job(
            source_handle=source_handle.handle,
            output_handle=output_handle.handle,
            request="Use another request with the same key.",
            disclosure_acknowledged=True,
            idempotency_key="concurrent-host-create",
            model_transport="chatgpt_hosted",
        )


def test_failed_host_revision_preserves_and_restores_prior_preview(
    tmp_path: Path,
) -> None:
    """A mechanically invalid replacement cannot destroy the valid proposal."""

    _, _, service, reviewing = _build_reviewing_host_job(tmp_path)
    editable = tuple(
        mapping
        for mapping in reviewing.candidate_plan.file_mappings
        if not mapping.protected
    )
    assert len(editable) >= 2
    revising = service.begin_revision(
        job_id=reviewing.job_id,
        expected_revision=reviewing.revision,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        instruction="Place two files at the same destination.",
        idempotency_key="collision-revision",
    )
    invalid = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=canonical_sha256(reviewing.candidate_plan),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=editable[0].file_id,
                replacement_target_path=editable[1].target_path,
                rationale="Exercise deterministic collision refusal.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    failed = service.submit_plan_revision(
        job_id=revising.job_id,
        call_id="collision_submission",
        revision=invalid,
    )
    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert failed.preview.current_tree_members == reviewing.preview.current_tree_members
    assert (
        failed.preview.proposed_tree_members == reviewing.preview.proposed_tree_members
    )
    assert failed.preview.expected_job_revision == failed.revision
    assert failed.candidate_plan == reviewing.candidate_plan
    assert (
        service.submit_plan_revision(
            job_id=revising.job_id,
            call_id="collision_submission",
            revision=invalid,
        )
        == failed
    )

    kept = service.keep_previous_proposal(
        job_id=failed.job_id,
        expected_revision=failed.revision,
        preview_fingerprint=failed.preview.preview_fingerprint,
        candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
        idempotency_key="keep-valid-proposal",
    )
    assert kept.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert kept.preview.current_tree_members == reviewing.preview.current_tree_members
    assert kept.preview.proposed_tree_members == reviewing.preview.proposed_tree_members
    assert kept.candidate_plan == reviewing.candidate_plan


def test_failed_host_derivative_can_fork_again_and_use_second_revision(
    tmp_path: Path,
) -> None:
    """ChatGPT/Codex can retry a failed child, then refine its T2 preview."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    paths = FoldweavePaths(state_root=tmp_path / "state")
    paths.jobs.mkdir(parents=True)
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    for directory in (origin_output, receiver_output):
        directory.mkdir()
    review = FoldweaveReviewService()
    origin = review.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=paths.jobs / "origin.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="host-derivative-origin",
    )
    assert origin.preview is not None
    verified_origin = review.accept(
        origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=origin_output,
        result_folder_name=fixture.result_name,
        idempotency_key="host-derivative-origin-accept",
        channel="native_app",
    )
    parent = review.prepare_application_review(
        change_file_path=review.get_change_file(verified_origin.job_path)[0],
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=paths.jobs / "receiver.json",
        idempotency_key="host-derivative-parent",
    )
    assert parent.preview is not None
    assert parent.candidate_plan is not None
    parent_bytes = parent.job_path.read_bytes()
    host = FoldweaveHostPlanningService(
        paths=paths,
        clock=lambda: datetime(2026, 7, 20, 23, 0, tzinfo=oslo_tz),
    )

    first = host.begin_revision(
        job_id=parent.job_id,
        expected_revision=parent.revision,
        candidate_fingerprint=parent.preview.compiled_candidate_fingerprint,
        preview_fingerprint=parent.preview.preview_fingerprint,
        instruction="First imported-proposal change is mechanically invalid.",
        idempotency_key="host-derivative-first-failure",
    )
    assert isinstance(first.authority, GptDerivativeJobAuthorityV3)
    editable = next(
        item
        for item in first.authority.parent_binding.parent_candidate.file_mappings
        if not item.protected
    )
    failed = host.submit_plan_revision(
        job_id=first.job_id,
        call_id="host-derivative-invalid-turn",
        revision=FolderHostPlanRevisionV1(
            base_candidate_fingerprint=(
                first.authority.parent_binding.parent_candidate_fingerprint
            ),
            entries=(
                FolderHostPlanRevisionEntryV1(
                    file_id=editable.file_id,
                    replacement_target_path=editable.target_path,
                    rationale="Exercise the no-change refusal.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        ),
    )
    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert failed.preview is not None
    assert failed.candidate_plan == parent.candidate_plan

    sibling = host.begin_revision(
        job_id=failed.job_id,
        expected_revision=failed.revision,
        candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
        preview_fingerprint=failed.preview.preview_fingerprint,
        instruction="Try another change in a hosted review folder.",
        idempotency_key="host-derivative-sibling",
    )
    assert sibling.job_id != failed.job_id
    assert isinstance(sibling.authority, GptDerivativeJobAuthorityV3)
    first_valid = host.submit_plan_revision(
        job_id=sibling.job_id,
        call_id="host-derivative-valid-turn",
        revision=FolderHostPlanRevisionV1(
            base_candidate_fingerprint=(
                sibling.authority.parent_binding.parent_candidate_fingerprint
            ),
            entries=(
                FolderHostPlanRevisionEntryV1(
                    file_id=editable.file_id,
                    replacement_target_path=(
                        f"host-review/{Path(editable.target_path).name}"
                    ),
                    rationale="Create the first complete hosted derivative preview.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        ),
    )
    assert first_valid.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert first_valid.proposal_revision == 1
    assert first_valid.preview is not None
    assert first_valid.candidate_plan is not None

    second_pending = host.begin_revision(
        job_id=first_valid.job_id,
        expected_revision=first_valid.revision,
        candidate_fingerprint=first_valid.preview.compiled_candidate_fingerprint,
        preview_fingerprint=first_valid.preview.preview_fingerprint,
        instruction="Refine the derivative preview one final time.",
        idempotency_key="host-derivative-second-turn",
    )
    second = host.submit_plan_revision(
        job_id=second_pending.job_id,
        call_id="host-derivative-second-submission",
        revision=FolderHostPlanRevisionV1(
            base_candidate_fingerprint=canonical_sha256(first_valid.candidate_plan),
            entries=(
                FolderHostPlanRevisionEntryV1(
                    file_id=editable.file_id,
                    replacement_target_path=(
                        f"host-second-review/{Path(editable.target_path).name}"
                    ),
                    rationale="Use the second and final hosted derivative revision.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        ),
    )
    assert second.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert second.proposal_revision == 2
    assert second.revision_attempt_count == 2
    assert parent.job_path.read_bytes() == parent_bytes


def test_host_clarification_and_local_handle_authority_are_bounded(
    tmp_path: Path,
) -> None:
    """Hosted clarification is single-use and local handles expire by role/channel."""

    _, _, service, planning = _start_host_job(tmp_path / "clarification")
    waiting = service.request_clarification(
        job_id=planning.job_id,
        expected_revision=planning.revision,
        question="Should the archive remain grouped by year?",
        idempotency_key="question-1",
    )
    assert waiting.lifecycle is FolderJobLifecycleV3.AWAITING_CLARIFICATION
    assert (
        service.request_clarification(
            job_id=planning.job_id,
            expected_revision=planning.revision,
            question="Should the archive remain grouped by year?",
            idempotency_key="question-1",
        )
        == waiting
    )
    with pytest.raises(FoldweaveHostServiceError) as clarification_error:
        service.request_clarification(
            job_id=planning.job_id,
            expected_revision=waiting.revision,
            question="Should there be another clarification?",
            idempotency_key="question-2",
        )
    assert clarification_error.value.code == "clarification_limit_exceeded"
    resumed = service.answer_clarification(
        job_id=planning.job_id,
        expected_revision=waiting.revision,
        question_fingerprint=(
            waiting.authority.planning_state.events[-1].question_fingerprint
        ),
        answer="Yes, retain the yearly grouping.",
        idempotency_key="answer-1",
    )
    assert resumed.lifecycle is FolderJobLifecycleV3.PLANNING
    assert resumed.clarification_count == 1
    assert (
        service.answer_clarification(
            job_id=planning.job_id,
            expected_revision=waiting.revision,
            question_fingerprint=(
                waiting.authority.planning_state.events[-1].question_fingerprint
            ),
            answer="Yes, retain the yearly grouping.",
            idempotency_key="answer-1",
        )
        == resumed
    )
    with pytest.raises(FoldweaveHostServiceError) as answer_conflict:
        service.answer_clarification(
            job_id=planning.job_id,
            expected_revision=waiting.revision,
            question_fingerprint=(
                waiting.authority.planning_state.events[-1].question_fingerprint
            ),
            answer="No, use another answer for the same question.",
            idempotency_key="answer-1",
        )
    assert answer_conflict.value.code == "clarification_idempotency_conflict"

    selected = tmp_path / "selected"
    selected.mkdir()
    clock = [datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz)]
    handles = FoldweaveLocalHandleStore(
        clock=lambda: clock[0],
        token_factory=lambda: "H" * 43,
    )
    public = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=selected,
        channel="chatgpt_hosted",
    )
    with pytest.raises(FoldweaveLocalHandleError) as role_error:
        handles.resolve(
            public.handle,
            role=NativePathRole.OUTPUT_PARENT,
            channel="chatgpt_hosted",
        )
    assert role_error.value.code == "local_handle_role_mismatch"
    with pytest.raises(FoldweaveLocalHandleError) as channel_error:
        handles.resolve(
            public.handle,
            role=NativePathRole.SOURCE_FOLDER,
            channel="codex_hosted",
        )
    assert channel_error.value.code == "local_handle_channel_mismatch"
    clock[0] = datetime(2026, 7, 19, 20, 31, tzinfo=oslo_tz)
    with pytest.raises(FoldweaveLocalHandleError) as expiry_error:
        handles.resolve(
            public.handle,
            role=NativePathRole.SOURCE_FOLDER,
            channel="chatgpt_hosted",
        )
    assert expiry_error.value.code == "local_handle_expired"


def test_third_rejected_host_plan_blocks_with_fresh_job_guidance(
    tmp_path: Path,
) -> None:
    """The submission ceiling cannot leave an unusable planning state."""

    fixture, _, service, planning = _start_host_job(tmp_path)
    valid = _complete_host_plan(fixture, planning)
    editable = list(valid.entries)
    editable[0] = editable[0].model_copy(
        update={"proposed_target": editable[1].proposed_target}
    )
    invalid = valid.model_copy(update={"entries": tuple(editable)})
    current = planning
    for index in range(1, 4):
        current = service.submit_plan(
            job_id=planning.job_id,
            call_id=f"rejected_plan_{index}",
            plan=invalid,
        )
    assert current.lifecycle is FolderJobLifecycleV3.BLOCKED
    assert current.blocker_code == "host_plan_submission_exhausted"
    assert current.candidate_plan is None
    assert current.preview is None


def test_host_polling_is_byte_read_only_and_mutation_persists_staleness(
    tmp_path: Path,
) -> None:
    """Polling never mutates bytes; the next mutation persists staleness."""

    fixture, _, service, reviewing = _build_reviewing_host_job(tmp_path)
    changed_relative = next(
        item.relative_path
        for item in reviewing.source_inventory.files
        if not item.protected
    )
    changed = fixture.sofia_root / changed_relative
    changed.write_bytes(changed.read_bytes() + b"changed after review\n")

    job_path = reviewing.job_path
    before = job_path.read_bytes()
    assert service.status(reviewing.job_id) == reviewing
    assert service.get_plan_preview(reviewing.job_id) == reviewing.preview
    assert service.get_compiler_failures(reviewing.job_id) == ()
    assert job_path.read_bytes() == before

    assert reviewing.preview is not None
    with pytest.raises(FoldweaveHostServiceError):
        service.begin_revision(
            job_id=reviewing.job_id,
            expected_revision=reviewing.revision,
            candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
            preview_fingerprint=reviewing.preview.preview_fingerprint,
            instruction="Move the reviewed files into a new folder.",
            idempotency_key="stale-revision",
        )
    stale = service.status(reviewing.job_id)
    assert stale.lifecycle is FolderJobLifecycleV3.STALE
    assert stale.staleness is not None
    assert stale.staleness.code == "source_changed"


def test_importing_host_service_does_not_load_direct_api_or_budget_modules() -> None:
    """The keyless hosted entry point remains dependency-isolated at import time."""

    script = """
import sys
import name_atlas.foldweave_host_service
blocked = sorted(
    name
    for name in sys.modules
    if name == "openai"
    or name.startswith("openai.")
    or name == "name_atlas.decision_cards.budget"
    or name == "name_atlas.folder_refactor.live_planner_provider"
)
if blocked:
    raise SystemExit(",".join(blocked))
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def _start_host_job(
    tmp_path: Path,
) -> tuple[
    ConnectedChangeFixture,
    Path,
    FoldweaveHostPlanningService,
    FolderRefactorJobV3,
]:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    tokens = iter(("S" * 43, "O" * 43))
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: next(tokens),
    )
    source_handle = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=fixture.sofia_root,
        channel="chatgpt_hosted",
    )
    output_handle = handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=output,
        channel="chatgpt_hosted",
    )
    service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        handle_store=handles,
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    planning = service.create_or_resume_planning_job(
        source_handle=source_handle.handle,
        output_handle=output_handle.handle,
        request=fixture.request,
        disclosure_acknowledged=True,
        idempotency_key="host-test-create",
        model_transport="chatgpt_hosted",
    )
    return fixture, output, service, planning


def _complete_host_plan(
    fixture: ConnectedChangeFixture,
    planning: FolderRefactorJobV3,
) -> FolderPlan:
    authority = planning.authority
    assert isinstance(authority, GptHostedJobAuthorityV3)
    return FolderPlan(
        source_commitment=planning.source_inventory.source_commitment,
        request_fingerprint=authority.planning_state.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=(
            authority.planning_state.evidence_state.evidence_fingerprint
        ),
        result_folder_name=fixture.result_name,
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=fixture.target_paths[item.relative_path],
                rationale="Organize the connected project for handoff.",
                evidence_ids=("initial_inventory",),
            )
            for item in planning.source_inventory.files
            if not item.protected
        ),
        exclusions=(),
    )


def _build_reviewing_host_job(
    tmp_path: Path,
) -> tuple[
    ConnectedChangeFixture,
    Path,
    FoldweaveHostPlanningService,
    FolderRefactorJobV3,
]:
    fixture, output, service, planning = _start_host_job(tmp_path)
    reviewing = service.submit_plan(
        job_id=planning.job_id,
        call_id="host-test-plan",
        plan=_complete_host_plan(fixture, planning),
    )
    assert reviewing.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert reviewing.preview is not None
    return fixture, output, service, reviewing
