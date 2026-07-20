"""Strict F1 derivative-child authority and transcript contract tests."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import pytest
from connected_change_fixtures import make_connected_change_fixture
from pydantic import ValidationError

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
    build_connected_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.derivative import (
    FolderDerivativeCreationBindingV1,
    FolderDerivativeParentBindingV1,
    _next_derivative_generation,
    build_derivative_creation_binding,
    build_derivative_parent_binding,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
    FolderIdempotencyBindingV2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
    GptDerivativeJobAuthorityV3,
    build_recreate_original_operation_binding_v3,
    build_revision_instruction,
    canonical_job_v3_bytes,
    parse_job_v3_bytes,
)
from name_atlas.folder_refactor.connected_change.preview import (
    FolderPlanPreviewV1,
    build_folder_plan_preview,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.service import (
    create_connected_change_origin,
)
from name_atlas.folder_refactor.foldweave_host_contracts import (
    FolderHostDerivativePendingRevisionV1,
    FolderHostPendingRevisionV1,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeRevisionTurnInputV1,
    FolderDerivativeRevisionTurnRecordV1,
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
    build_derivative_composite_evidence,
    build_derivative_evidence_ledger,
    build_derivative_revision_turn_record,
    build_execution_origin_v2,
)
from name_atlas.folder_refactor.planner_evidence import (
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.serialization import canonical_sha256


@dataclass(frozen=True, slots=True)
class _DerivativeContext:
    parent: FolderRefactorJobV3
    parent_binding: FolderDerivativeParentBindingV1
    creation_binding: FolderDerivativeCreationBindingV1
    instruction: Any
    turn_input: FolderDerivativeRevisionTurnInputV1
    turn: FolderDerivativeRevisionTurnRecordV1
    accepted_plan: FolderAcceptedPlanV2
    child_preview: FolderPlanPreviewV1
    child_job_path: Path


def test_derivative_turn_one_requires_all_portable_parent_bindings(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    assert context.turn_input.response_turn == 1

    root_payload = context.turn_input.model_dump(
        mode="python",
        exclude={"schema_version"},
    )
    root_payload.update(
        response_turn=1,
        imported_change_file_fingerprint=None,
        match_report_fingerprint=None,
        immediate_parent_candidate_fingerprint=None,
        evidence_fingerprint=context.parent.candidate_plan.evidence_fingerprint,
    )
    with pytest.raises(ValidationError, match="greater than or equal to 2"):
        FolderPlannerRevisionTurnInputV1.model_validate(root_payload, strict=True)

    partial_payload = context.turn_input.model_dump(mode="python")
    partial_payload.pop("immediate_parent_candidate_fingerprint")
    with pytest.raises(ValidationError, match="immediate_parent_candidate"):
        FolderDerivativeRevisionTurnInputV1.model_validate(
            partial_payload,
            strict=True,
        )


def test_host_root_turn_one_is_rejected_but_derivative_pending_is_explicit(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    common = {
        "job_id": context.creation_binding.child_job_id,
        "model_transport": "chatgpt_hosted",
        "expected_job_revision": 0,
        "proposal_revision": 0,
        "response_turn": 1,
        "base_candidate_fingerprint": (
            context.parent_binding.parent_candidate_fingerprint
        ),
        "base_preview_fingerprint": (context.parent_binding.parent_preview_fingerprint),
        "revision_instruction_fingerprint": (
            context.instruction.instruction_fingerprint
        ),
        "evidence_fingerprint": context.creation_binding.evidence_fingerprint,
        "prior_transcript_fingerprint": context.creation_binding.binding_fingerprint,
        "turn_contract_freeze_fingerprint": (
            context.creation_binding.contract_freeze_fingerprint
        ),
        "idempotency_key_sha256": context.creation_binding.idempotency_key_sha256,
    }
    with pytest.raises(ValidationError, match="greater than or equal to 2"):
        FolderHostPendingRevisionV1(
            **common,
            pending_fingerprint="0" * 64,
        )

    evidence_state = create_initial_evidence_ledger(
        context.parent.source_inventory,
        context.parent.user_request,
    )
    derivative_values = {
        **common,
        "initial_evidence_fingerprint": evidence_state.evidence_fingerprint,
        "evidence_state": evidence_state,
        "imported_change_file_fingerprint": (
            context.parent_binding.imported_change_file_fingerprint
        ),
        "match_report_fingerprint": (
            context.parent_binding.match_report.match_report_fingerprint
        ),
        "immediate_parent_candidate_fingerprint": (
            context.parent_binding.parent_candidate_fingerprint
        ),
    }
    draft = FolderHostDerivativePendingRevisionV1.model_construct(
        **derivative_values,
        pending_fingerprint="0" * 64,
    )
    pending = FolderHostDerivativePendingRevisionV1(
        **derivative_values,
        pending_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"pending_fingerprint"})
        ),
    )
    assert pending.response_turn == 1


def test_derivative_turn_uses_fresh_receiver_local_evidence_without_weakening_root(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    parent = context.parent
    assert parent.candidate_plan is not None
    assert (
        context.turn_input.evidence_fingerprint
        != parent.candidate_plan.evidence_fingerprint
    )
    assert (
        context.accepted_plan.evidence_fingerprint
        == context.turn_input.evidence_fingerprint
    )

    root_payload = context.turn_input.model_dump(
        mode="python",
        exclude={"schema_version"},
    )
    root_payload.update(
        response_turn=2,
        imported_change_file_fingerprint=None,
        match_report_fingerprint=None,
        immediate_parent_candidate_fingerprint=None,
    )
    with pytest.raises(ValidationError, match="another evidence authority"):
        FolderPlannerRevisionTurnInputV1.model_validate(root_payload, strict=True)


def test_pending_and_completed_derivative_authority_are_schema_distinct_and_round_trip(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    parent = context.parent
    pending_authority = GptDerivativeJobAuthorityV3(
        authority_state="awaiting_model_response",
        model_transport="deterministic_development",
        parent_binding=context.parent_binding,
        creation_binding=context.creation_binding,
        pending_direct_revision=context.turn_input,
    )
    pending_job = _child_job(
        context,
        authority=pending_authority,
        revision=0,
        proposal_revision=0,
        lifecycle=FolderJobLifecycleV3.REVISING,
        candidate_plan=None,
        reference_graph=None,
        preview=None,
    )
    parsed_pending = parse_job_v3_bytes(
        canonical_job_v3_bytes(pending_job),
        expected_path=context.child_job_path,
    )
    assert isinstance(parsed_pending.authority, GptDerivativeJobAuthorityV3)
    assert parsed_pending.authority.authority_state == "awaiting_model_response"
    assert parsed_pending.candidate_plan is None

    evidence_state = create_initial_evidence_ledger(
        parent.source_inventory,
        parent.user_request,
    )
    derivative_initial = build_derivative_evidence_ledger(
        job_id=context.creation_binding.child_job_id,
        evidence_state=evidence_state,
        model_transport="deterministic_development",
        parent_binding_fingerprint=context.parent_binding.binding_fingerprint,
        creation_binding_fingerprint=context.creation_binding.binding_fingerprint,
        contract_freeze_fingerprint=(
            context.creation_binding.contract_freeze_fingerprint
        ),
        imported_change_file_fingerprint=(
            context.parent_binding.imported_change_file_fingerprint
        ),
        match_report_fingerprint=(
            context.parent_binding.match_report.match_report_fingerprint
        ),
        immediate_parent_candidate_fingerprint=(
            context.parent_binding.parent_candidate_fingerprint
        ),
        immediate_parent_preview_fingerprint=(
            context.parent_binding.parent_preview_fingerprint
        ),
        revision_instruction_fingerprint=(context.instruction.instruction_fingerprint),
        turn=context.turn,
        accepted_plan=context.accepted_plan,
    )
    composite = build_derivative_composite_evidence(
        initial_ledger=derivative_initial,
        accepted_plan=context.accepted_plan,
        contract_freeze_fingerprint="f" * 64,
    )
    origin = build_execution_origin_v2(
        composite,
        imported_change_file_fingerprint=(
            context.parent_binding.imported_change_file_fingerprint
        ),
        match_report_fingerprint=(
            context.parent_binding.match_report.match_report_fingerprint
        ),
    )
    completed_authority = GptDerivativeJobAuthorityV3(
        authority_state="completed",
        model_transport="deterministic_development",
        parent_binding=context.parent_binding,
        creation_binding=context.creation_binding,
        evidence_ledger=composite,
        execution_origin=origin,
    )
    completed_job = _child_job(
        context,
        authority=completed_authority,
        revision=1,
        proposal_revision=1,
        lifecycle=FolderJobLifecycleV3.REVIEWING,
        candidate_plan=context.accepted_plan,
        reference_graph=parent.reference_graph,
        preview=context.child_preview,
    )
    parsed_completed = parse_job_v3_bytes(
        canonical_job_v3_bytes(completed_job),
        expected_path=context.child_job_path,
    )
    assert isinstance(parsed_completed.authority, GptDerivativeJobAuthorityV3)
    assert parsed_completed.authority.authority_state == "completed"
    assert parsed_completed.preview is not None
    assert parsed_completed.preview.proposal_basis == "gpt_derivative"
    assert composite.full_plan_submission_count == 0
    assert composite.sparse_revision_submission_count == 1
    assert composite.segments[0].segment_kind == "user_revision"

    mixed = completed_authority.model_dump(mode="python")
    mixed["pending_direct_revision"] = context.turn_input.model_dump(mode="python")
    with pytest.raises(ValidationError, match="evidence and provenance only"):
        GptDerivativeJobAuthorityV3.model_validate(mixed, strict=True)


def test_derivative_preview_requires_change_file_match_and_parent_together(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    preview_payload = context.child_preview.model_dump(mode="python")
    preview_payload["match_report_fingerprint"] = None
    preview_payload["preview_fingerprint"] = canonical_sha256(
        {
            key: value
            for key, value in preview_payload.items()
            if key != "preview_fingerprint"
        }
    )
    with pytest.raises(ValidationError, match="requires Change File, match"):
        FolderPlanPreviewV1.model_validate(preview_payload, strict=True)


def test_derivative_parent_generation_is_derived_from_actual_parent(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "legacy-projects")
    legacy_output = (tmp_path / "legacy-output").resolve()
    legacy_output.mkdir()
    legacy = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=legacy_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    parsed_legacy_parent = parse_connected_change_file_any(
        legacy.change_file_path.read_bytes()
    )
    assert parsed_legacy_parent.schema_version == "connected-change-file.v1"
    assert _next_derivative_generation(parsed_legacy_parent) == 1
    legacy_receiver_output = (tmp_path / "legacy-receiver-output").resolve()
    legacy_receiver_output.mkdir()
    legacy_receiver = FoldweaveReviewService().prepare_application_review(
        change_file_path=legacy.change_file_path,
        source_root=fixture.martin_root,
        output_parent=legacy_receiver_output,
        job_path=(tmp_path / "legacy-jobs" / "martin.json").resolve(),
        idempotency_key="legacy-derivative-parent-review",
    )
    assert isinstance(legacy_receiver.authority, CapsuleAppliedJobAuthorityV2)
    assert legacy_receiver.authority.match_report is not None
    assert legacy_receiver.candidate_plan is not None
    assert legacy_receiver.preview is not None
    legacy_binding = build_derivative_parent_binding(
        parent_job_id=legacy_receiver.job_id,
        parent_job_path=legacy_receiver.job_path,
        parent_source_root=legacy_receiver.source_root,
        parent_job_revision=legacy_receiver.revision,
        parent_proposal_revision=legacy_receiver.proposal_revision,
        parent_source_commitment=(legacy_receiver.source_inventory.source_commitment),
        parent_candidate=legacy_receiver.candidate_plan,
        parent_preview=legacy_receiver.preview,
        change_file_binding=legacy_receiver.authority.change_file_binding,
        match_report=legacy_receiver.authority.match_report,
    )
    assert legacy_binding.generation == 1

    context = _build_context(tmp_path)
    assert (
        context.parent_binding.change_file_binding.change_file.schema_version
        == "connected-change-file.v2"
    )
    assert context.parent_binding.generation == 1

    payload = context.parent_binding.model_dump(
        mode="python",
        exclude={"binding_fingerprint"},
    )
    payload["generation"] = 2
    fingerprint_payload = context.parent_binding.model_dump(
        mode="json",
        exclude={"binding_fingerprint"},
    )
    fingerprint_payload["generation"] = 2
    payload["binding_fingerprint"] = canonical_sha256(fingerprint_payload)
    with pytest.raises(ValidationError, match="derived from its exact Change File"):
        FolderDerivativeParentBindingV1(**payload)


def test_derivative_creation_request_identity_precedes_child_allocation(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    first = context.creation_binding
    second = build_derivative_creation_binding(
        parent_binding=context.parent_binding,
        child_job_id=uuid.uuid4().hex,
        child_job_path=(tmp_path / "jobs" / "retry-allocation.json").resolve(),
        source_root=first.source_root,
        output_parent=first.output_parent,
        revision_instruction_fingerprint=first.revision_instruction_fingerprint,
        evidence_fingerprint=first.evidence_fingerprint,
        contract_freeze_fingerprint=first.contract_freeze_fingerprint,
        model_transport=first.model_transport,
        channel=first.channel,
        idempotency_key_sha256=first.idempotency_key_sha256,
    )
    changed = build_derivative_creation_binding(
        parent_binding=context.parent_binding,
        child_job_id=uuid.uuid4().hex,
        child_job_path=(tmp_path / "jobs" / "changed-output.json").resolve(),
        source_root=first.source_root,
        output_parent=(tmp_path / "another-output").resolve(),
        revision_instruction_fingerprint=first.revision_instruction_fingerprint,
        evidence_fingerprint=first.evidence_fingerprint,
        contract_freeze_fingerprint=first.contract_freeze_fingerprint,
        model_transport=first.model_transport,
        channel=first.channel,
        idempotency_key_sha256=first.idempotency_key_sha256,
    )

    assert first.request_fingerprint == second.request_fingerprint
    assert first.binding_fingerprint != second.binding_fingerprint
    assert changed.request_fingerprint != first.request_fingerprint


def _build_context(tmp_path: Path) -> _DerivativeContext:
    tmp_path.mkdir(parents=True, exist_ok=True)
    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    jobs = (tmp_path / "jobs").resolve()
    sofia_output = (tmp_path / "sofia-output").resolve()
    martin_output = (tmp_path / "martin-output").resolve()
    child_output = (tmp_path / "child-output").resolve()
    for directory in (jobs, sofia_output, martin_output, child_output):
        directory.mkdir(parents=True)
    origin = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=sofia_output,
        job_path=jobs / "sofia.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="derivative-origin-review",
    )
    assert origin.preview is not None
    verified = service.accept(
        job_path=origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=sofia_output,
        result_folder_name=fixture.result_name,
        idempotency_key="derivative-origin-accept",
        channel="native_app",
    )
    change_file_path = service.get_change_file(verified.job_path)[0]
    parent = service.prepare_application_review(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=martin_output,
        job_path=jobs / "martin.json",
        idempotency_key="derivative-parent-review",
    )
    assert parent.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert isinstance(parent.authority, CapsuleAppliedJobAuthorityV2)
    assert parent.authority.match_report is not None
    assert parent.candidate_plan is not None
    assert parent.reference_graph is not None
    assert parent.preview is not None
    parent_binding = build_derivative_parent_binding(
        parent_job_id=parent.job_id,
        parent_job_path=parent.job_path,
        parent_source_root=parent.source_root,
        parent_job_revision=parent.revision,
        parent_proposal_revision=parent.proposal_revision,
        parent_source_commitment=parent.source_inventory.source_commitment,
        parent_candidate=parent.candidate_plan,
        parent_preview=parent.preview,
        change_file_binding=parent.authority.change_file_binding,
        match_report=parent.authority.match_report,
    )
    instruction = build_revision_instruction(
        base_candidate_fingerprint=parent_binding.parent_candidate_fingerprint,
        base_preview_fingerprint=parent_binding.parent_preview_fingerprint,
        instruction="Move one document into a collaborative review folder.",
        idempotency_key="derivative-child-instruction",
    )
    evidence_state = create_initial_evidence_ledger(
        parent.source_inventory,
        parent.user_request,
    )
    child_job_id = uuid.uuid4().hex
    child_job_path = (jobs / "martin-child.json").resolve()
    creation = build_derivative_creation_binding(
        parent_binding=parent_binding,
        child_job_id=child_job_id,
        child_job_path=child_job_path,
        source_root=parent.source_root,
        output_parent=child_output,
        revision_instruction_fingerprint=instruction.instruction_fingerprint,
        evidence_fingerprint=evidence_state.evidence_fingerprint,
        contract_freeze_fingerprint="f" * 64,
        model_transport="deterministic_development",
        channel="native_app",
        idempotency_key_sha256=canonical_sha256(
            {"domain": "test:derivative-key:v1", "key": "child"}
        ),
    )
    replacement = next(
        item for item in parent.candidate_plan.file_mappings if not item.protected
    )
    revision = FolderPlanRevisionV1(
        base_candidate_fingerprint=parent_binding.parent_candidate_fingerprint,
        entries=(
            FolderPlanRevisionEntryV1(
                file_id=replacement.file_id,
                replacement_target_path=(
                    "collaborative-review/"
                    + PurePosixPath(replacement.target_path).name
                ),
                rationale="Separate this document for collaborative review.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    turn_input = FolderDerivativeRevisionTurnInputV1(
        job_id=child_job_id,
        expected_job_revision=0,
        proposal_revision=0,
        response_turn=1,
        provider_kind="deterministic",
        request=parent.user_request,
        request_fingerprint=parent.candidate_plan.request_fingerprint,
        source_commitment=parent.source_inventory.source_commitment,
        revision_instruction=instruction.instruction,
        revision_instruction_fingerprint=instruction.instruction_fingerprint,
        base_candidate=parent.candidate_plan,
        base_candidate_fingerprint=parent_binding.parent_candidate_fingerprint,
        base_preview_fingerprint=parent_binding.parent_preview_fingerprint,
        evidence_fingerprint=evidence_state.evidence_fingerprint,
        prior_transcript_fingerprint=creation.binding_fingerprint,
        turn_contract_freeze_fingerprint="f" * 64,
        imported_change_file_fingerprint=(
            parent_binding.imported_change_file_fingerprint
        ),
        match_report_fingerprint=parent_binding.match_report.match_report_fingerprint,
        immediate_parent_candidate_fingerprint=(
            parent_binding.parent_candidate_fingerprint
        ),
    )
    response = FolderRevisionProviderResponseV1(
        provider_kind="deterministic",
        returned_model=None,
        observable_output_items=(),
        call_id="derivative-turn-1",
        revision=revision,
    )
    turn = build_derivative_revision_turn_record(
        turn_input=turn_input,
        response=response,
        usage=None,
    )
    target_by_file_id = {
        item.file_id: (
            revision.entries[0].replacement_target_path
            if item.file_id == replacement.file_id
            else item.target_path
        )
        for item in parent.candidate_plan.file_mappings
        if not item.protected
    }
    accepted_plan = build_connected_accepted_plan(
        inventory=parent.source_inventory,
        request=parent.user_request,
        evidence_fingerprint=evidence_state.evidence_fingerprint,
        result_folder_name=parent.candidate_plan.result_folder_name,
        target_by_file_id=target_by_file_id,
        execution_authority="gpt_plan",
        evidence_schema_version="folder-evidence-ledger.v2",
    )
    child_preview = build_folder_plan_preview(
        job_id=child_job_id,
        expected_job_revision=1,
        proposal_revision=1,
        proposal_basis="gpt_derivative",
        inventory=parent.source_inventory,
        reference_graph=parent.reference_graph,
        accepted_plan=accepted_plan,
        imported_change_file_fingerprint=(
            parent_binding.imported_change_file_fingerprint
        ),
        match_report_fingerprint=parent_binding.match_report.match_report_fingerprint,
        immediate_parent_candidate_fingerprint=(
            parent_binding.parent_candidate_fingerprint
        ),
    )
    return _DerivativeContext(
        parent=parent,
        parent_binding=parent_binding,
        creation_binding=creation,
        instruction=instruction,
        turn_input=turn_input,
        turn=turn,
        accepted_plan=accepted_plan,
        child_preview=child_preview,
        child_job_path=child_job_path,
    )


def _child_job(
    context: _DerivativeContext,
    *,
    authority: GptDerivativeJobAuthorityV3,
    revision: int,
    proposal_revision: int,
    lifecycle: FolderJobLifecycleV3,
    candidate_plan: FolderAcceptedPlanV2 | None,
    reference_graph: Any,
    preview: FolderPlanPreviewV1 | None,
) -> FolderRefactorJobV3:
    parent = context.parent
    return FolderRefactorJobV3(
        revision=revision,
        proposal_revision=proposal_revision,
        revision_attempt_count=1,
        clarification_count=0,
        job_id=context.creation_binding.child_job_id,
        display_name="Foldweave derivative child",
        created_at=parent.updated_at,
        updated_at=parent.updated_at,
        source_root=parent.source_root,
        output_parent=context.creation_binding.output_parent,
        job_path=context.child_job_path,
        source_inventory=parent.source_inventory,
        local_file_identities=parent.local_file_identities,
        local_directory_identities=parent.local_directory_identities,
        user_request=parent.user_request,
        idempotency=FolderIdempotencyBindingV2(
            key_sha256=context.creation_binding.idempotency_key_sha256,
            request_fingerprint=context.creation_binding.request_fingerprint,
        ),
        operation_idempotency=(
            build_recreate_original_operation_binding_v3(
                job_id=context.creation_binding.child_job_id,
                idempotency_key="derivative-child-instruction",
            ),
        ),
        authority=authority,
        candidate_plan=candidate_plan,
        reference_graph=reference_graph,
        preview=preview,
        revision_instruction=context.instruction,
        immediate_parent_job_id=parent.job_id,
        immediate_parent_candidate_fingerprint=(
            context.parent_binding.parent_candidate_fingerprint
        ),
        lifecycle=lifecycle,
    )
