"""End-to-end v2 Change File and v3 receipt derivative finalization tests."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

from connected_change_fixtures import make_connected_change_fixture
from test_foldweave_derivative_contracts import _build_context, _child_job

from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
    parse_connected_change_file_v2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderPortableExecutionAuthorizationV1,
    GptDerivativeJobAuthorityV3,
    build_execution_authorization,
)
from name_atlas.folder_refactor.connected_change.preview import FolderPlanPreviewV1
from name_atlas.folder_refactor.connected_change.proof import (
    render_connected_proof_html,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH,
    FOLDWEAVE_PLAN_PREVIEW_PATH,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV3,
    parse_folder_receipt_envelope_any,
)
from name_atlas.folder_refactor.connected_change.reconstruction import (
    restore_connected_result,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.service import (
    apply_connected_change,
    create_connected_change_origin,
    execute_prepared_foldweave_derivative,
    prepare_foldweave_derivative_execution,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    build_derivative_composite_evidence,
    build_derivative_evidence_ledger,
    build_execution_origin_v2,
)
from name_atlas.folder_refactor.planner_evidence import (
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    read_regular_bytes,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)
from name_atlas.verification.bag_writer import BagItWriter


def test_derivative_finalizer_emits_self_contained_v2_v3_and_reconstructs(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    parent = context.parent
    evidence_state = create_initial_evidence_ledger(
        parent.source_inventory,
        parent.user_request,
    )
    derivative_evidence = build_derivative_evidence_ledger(
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
    evidence = build_derivative_composite_evidence(
        initial_ledger=derivative_evidence,
        accepted_plan=context.accepted_plan,
        contract_freeze_fingerprint=(
            context.creation_binding.contract_freeze_fingerprint
        ),
    )
    origin = build_execution_origin_v2(
        evidence,
        imported_change_file_fingerprint=(
            context.parent_binding.imported_change_file_fingerprint
        ),
        match_report_fingerprint=(
            context.parent_binding.match_report.match_report_fingerprint
        ),
    )
    authority = GptDerivativeJobAuthorityV3(
        authority_state="completed",
        model_transport="deterministic_development",
        parent_binding=context.parent_binding,
        creation_binding=context.creation_binding,
        evidence_ledger=evidence,
        execution_origin=origin,
    )
    child_job = _child_job(
        context,
        authority=authority,
        revision=1,
        proposal_revision=1,
        lifecycle=FolderJobLifecycleV3.REVIEWING,
        candidate_plan=context.accepted_plan,
        reference_graph=parent.reference_graph,
        preview=context.child_preview,
    )
    authorization = build_execution_authorization(
        job=child_job,
        expected_job_revision=child_job.revision,
        preview_fingerprint=context.child_preview.preview_fingerprint,
        candidate_fingerprint=(context.child_preview.compiled_candidate_fingerprint),
        output_parent=context.creation_binding.output_parent,
        result_folder_name=context.accepted_plan.result_folder_name,
        idempotency_key="derivative-finalizer-accept",
        channel="native_app",
    )
    prepared = prepare_foldweave_derivative_execution(
        parent_change_file_path=(context.parent_binding.change_file_binding.path),
        source_root=parent.source_root,
        accepted_plan=context.accepted_plan,
        execution_origin=origin,
        evidence_ledger=evidence,
        match_report=context.parent_binding.match_report,
        parent_candidate=context.parent_binding.parent_candidate,
        execution_authorization=authorization,
        plan_preview=context.child_preview,
        revision_instruction_fingerprint=(context.instruction.instruction_fingerprint),
    )
    result = execute_prepared_foldweave_derivative(
        prepared=prepared,
        output_parent=context.creation_binding.output_parent,
        job_id=context.creation_binding.child_job_id,
    )

    change_file = parse_connected_change_file_any(result.change_file_path.read_bytes())
    receipt = parse_folder_receipt_envelope_any(
        read_regular_bytes(result.folder_run.result_root, CHANGE_RECEIPT_PATH)
    )
    assert change_file.schema_version == "connected-change-file.v2"
    assert isinstance(receipt, FolderReceiptEnvelopeV3)
    assert receipt.receipt.execution_role == "derivative"
    assert change_file.originating_receipt == receipt
    assert change_file.core.lineage.parent_candidate_fingerprint == (
        context.parent_binding.parent_candidate_fingerprint
    )
    assert context.parent_binding.parent_candidate_fingerprint != (
        context.parent_binding.change_file_binding.change_file.originating_receipt.receipt.accepted_plan_fingerprint
    )
    verification = verify_connected_result(result.folder_run.result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert verification.schema_version == "folder-receipt-verification.v3"
    assert verification.receipt_fingerprint == receipt.receipt_fingerprint
    proof = (
        result.folder_run.result_root / "name-atlas" / "proof_and_restore.html"
    ).read_bytes()
    assert b"<title>Foldweave proof</title>" in proof
    assert b"Name Atlas proof" not in proof

    predecessor_verification = verify_connected_result(
        context.parent_binding.change_file_binding.path.parent.parent
    )
    assert predecessor_verification.status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    assert predecessor_verification.schema_version == "folder-receipt-verification.v3"

    restore_destination = (tmp_path / "martin-restored").resolve()
    restored = restore_connected_result(
        result.folder_run.result_root,
        restore_destination,
    )
    assert restored.source_commitment == parent.source_inventory.source_commitment

    tampered = (tmp_path / "tampered-lineage").resolve()
    shutil.copytree(result.folder_run.result_root, tampered)
    change_path = tampered / "name-atlas" / "connected_change_capsule.json"
    raw_change = json.loads(change_path.read_bytes())
    raw_change["core"]["lineage"]["parent_change_file_fingerprint"] = "0" * 64
    change_path.write_bytes(canonical_json_bytes(raw_change))
    BagItWriter().finalize_tagmanifest(tampered)
    blocked = verify_connected_result(tampered)
    assert blocked.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert "foldweave_receipt_invalid" in blocked.failed_check_ids

    forged_preview = (tmp_path / "forged-preview-authority").resolve()
    shutil.copytree(result.folder_run.result_root, forged_preview)
    _refingerprint_candidate_inconsistent_preview(forged_preview)
    forged_verification = verify_connected_result(forged_preview)
    assert forged_verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert forged_verification.schema_version == "folder-receipt-verification.v3"
    assert "plan_preview_mismatch" in forged_verification.failed_check_ids


def test_historical_v2_receipt_dispatch_remains_v2(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path / "legacy-projects")
    output = (tmp_path / "legacy-output").resolve()
    output.mkdir()
    legacy = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )

    verification = verify_connected_result(legacy.folder_run.result_root)

    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert verification.schema_version == "folder-receipt-verification.v2"


def test_v3_receiver_verifies_exact_imported_v1_change_file(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path / "compatibility-projects")
    origin_output = (tmp_path / "compatibility-origin-output").resolve()
    receiver_output = (tmp_path / "compatibility-receiver-output").resolve()
    origin_output.mkdir()
    receiver_output.mkdir()
    legacy = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    service = FoldweaveReviewService()
    reviewing = service.prepare_application_review(
        change_file_path=legacy.change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=(tmp_path / "compatibility-jobs" / "receiver.json").resolve(),
        idempotency_key="v3-receiver-import-v1-review",
    )
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    verified = service.accept(
        job_path=reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        output_parent=receiver_output,
        result_folder_name=reviewing.candidate_plan.result_folder_name,
        idempotency_key="v3-receiver-import-v1-accept",
        channel="native_app",
    )
    assert verified.final_result_path is not None

    verification = verify_connected_result(verified.final_result_path)

    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert verification.schema_version == "folder-receipt-verification.v3"


def test_descendant_v2_applies_to_raw_and_verified_prior_result(
    tmp_path: Path,
) -> None:
    context = _build_context(tmp_path)
    parent = context.parent
    evidence_state = create_initial_evidence_ledger(
        parent.source_inventory,
        parent.user_request,
    )
    derivative_evidence = build_derivative_evidence_ledger(
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
    evidence = build_derivative_composite_evidence(
        initial_ledger=derivative_evidence,
        accepted_plan=context.accepted_plan,
        contract_freeze_fingerprint=(
            context.creation_binding.contract_freeze_fingerprint
        ),
    )
    origin = build_execution_origin_v2(
        evidence,
        imported_change_file_fingerprint=(
            context.parent_binding.imported_change_file_fingerprint
        ),
        match_report_fingerprint=(
            context.parent_binding.match_report.match_report_fingerprint
        ),
    )
    authority = GptDerivativeJobAuthorityV3(
        authority_state="completed",
        model_transport="deterministic_development",
        parent_binding=context.parent_binding,
        creation_binding=context.creation_binding,
        evidence_ledger=evidence,
        execution_origin=origin,
    )
    child_job = _child_job(
        context,
        authority=authority,
        revision=1,
        proposal_revision=1,
        lifecycle=FolderJobLifecycleV3.REVIEWING,
        candidate_plan=context.accepted_plan,
        reference_graph=parent.reference_graph,
        preview=context.child_preview,
    )
    authorization = build_execution_authorization(
        job=child_job,
        expected_job_revision=child_job.revision,
        preview_fingerprint=context.child_preview.preview_fingerprint,
        candidate_fingerprint=(context.child_preview.compiled_candidate_fingerprint),
        output_parent=context.creation_binding.output_parent,
        result_folder_name=context.accepted_plan.result_folder_name,
        idempotency_key="derivative-descendant-accept",
        channel="native_app",
    )
    prepared = prepare_foldweave_derivative_execution(
        parent_change_file_path=context.parent_binding.change_file_binding.path,
        source_root=parent.source_root,
        accepted_plan=context.accepted_plan,
        execution_origin=origin,
        evidence_ledger=evidence,
        match_report=context.parent_binding.match_report,
        parent_candidate=context.parent_binding.parent_candidate,
        execution_authorization=authorization,
        plan_preview=context.child_preview,
        revision_instruction_fingerprint=(context.instruction.instruction_fingerprint),
    )
    derivative = execute_prepared_foldweave_derivative(
        prepared=prepared,
        output_parent=context.creation_binding.output_parent,
        job_id=context.creation_binding.child_job_id,
    )

    raw_output = (tmp_path / "raw-descendant-output").resolve()
    raw_output.mkdir()
    raw = apply_connected_change(
        change_file_path=derivative.change_file_path,
        source_root=(tmp_path / "projects" / "sofia-project").resolve(),
        output_parent=raw_output,
    )
    prior_output = (tmp_path / "prior-descendant-output").resolve()
    prior_output.mkdir()
    prior_result_root = context.parent_binding.change_file_binding.path.parent.parent
    prior = apply_connected_change(
        change_file_path=derivative.change_file_path,
        source_root=prior_result_root,
        output_parent=prior_output,
    )

    assert raw.organized_tree_commitment == derivative.organized_tree_commitment
    assert prior.organized_tree_commitment == derivative.organized_tree_commitment
    assert verify_connected_result(raw.folder_run.result_root).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    assert verify_connected_result(prior.folder_run.result_root).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )


def _refingerprint_candidate_inconsistent_preview(result_root: Path) -> None:
    """Forge a self-consistent preview envelope that diverges from its plan."""

    preview_path = result_root / FOLDWEAVE_PLAN_PREVIEW_PATH
    preview = json.loads(preview_path.read_bytes())
    changed = next(
        item
        for item in preview["member_changes"]
        if item["current_relative_path"] == "drafts/summary.md"
    )
    member_id = changed["member_id"]
    forged_path = "collaborative-review/unseen-plan.md"
    changed["proposed_relative_path"] = forged_path
    changed["rationale"] = "Fabricated preview path absent from the accepted plan."
    for member in preview["proposed_tree_members"]:
        if member["member_id"] == member_id:
            member["relative_path"] = forged_path
    for effect in preview["supported_link_effects"]:
        if effect["source_member_id"] == member_id:
            effect["proposed_source_path"] = forged_path
    preview["preview_fingerprint"] = canonical_sha256(
        {key: value for key, value in preview.items() if key != "preview_fingerprint"}
    )
    preview_bytes = canonical_json_bytes(preview)
    FolderPlanPreviewV1.model_validate_json(preview_bytes, strict=True)
    preview_path.write_bytes(preview_bytes)

    authorization_path = result_root / FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH
    authorization = json.loads(authorization_path.read_bytes())
    authorization["preview_fingerprint"] = preview["preview_fingerprint"]
    authorization["authorization_fingerprint"] = canonical_sha256(
        {
            key: value
            for key, value in authorization.items()
            if key != "authorization_fingerprint"
        }
    )
    authorization_bytes = canonical_json_bytes(authorization)
    FolderPortableExecutionAuthorizationV1.model_validate_json(
        authorization_bytes,
        strict=True,
    )
    authorization_path.write_bytes(authorization_bytes)

    receipt_path = result_root / CHANGE_RECEIPT_PATH
    receipt = json.loads(receipt_path.read_bytes())
    receipt_core = receipt["receipt"]
    receipt_core["plan_preview_fingerprint"] = preview["preview_fingerprint"]
    receipt_core["execution_authorization_fingerprint"] = authorization[
        "authorization_fingerprint"
    ]
    replacements = {
        FOLDWEAVE_PLAN_PREVIEW_PATH: preview_bytes,
        FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH: authorization_bytes,
    }
    for commitment in receipt_core["artifact_commitments"]:
        payload = replacements.get(commitment["path"])
        if payload is not None:
            commitment["size"] = len(payload)
            commitment["sha256"] = hashlib.sha256(payload).hexdigest()
    receipt["receipt_fingerprint"] = canonical_sha256(receipt_core)
    receipt_bytes = canonical_json_bytes(receipt)
    FolderReceiptEnvelopeV3.model_validate_json(receipt_bytes, strict=True)
    receipt_path.write_bytes(receipt_bytes)

    change_path = result_root / "name-atlas/connected_change_capsule.json"
    change_file = json.loads(change_path.read_bytes())
    change_file["originating_receipt"] = receipt
    change_file["change_file_fingerprint"] = canonical_sha256(
        {
            key: value
            for key, value in change_file.items()
            if key != "change_file_fingerprint"
        }
    )
    change_bytes = canonical_json_bytes(change_file)
    parse_connected_change_file_v2(change_bytes)
    change_path.write_bytes(change_bytes)

    proof_path = result_root / "name-atlas/proof_and_restore.html"
    proof_path.write_bytes(
        render_connected_proof_html(
            receipt["receipt_fingerprint"],
            receipt_core["organized_tree"]["commitment"],
            release_profile="foldweave",
        )
    )
    BagItWriter().finalize_tagmanifest(result_root)
