"""Strict Foldweave Change File v2 and receipt v3 contract tests."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from connected_change_fixtures import make_connected_change_fixture
from pydantic import ValidationError

from name_atlas.folder_refactor.connected_change import (
    ConnectedChangeCore,
    ConnectedChangeError,
    ConnectedChangeLineageV1,
    ConnectedChangeMember,
    ConnectedChangeMemberBindingV1,
    build_connected_change_core_v2,
    build_connected_change_lineage,
    create_connected_change_file_v2,
    parse_connected_change_file_any,
    parse_connected_change_file_v2,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CONNECTED_CHANGE_LINEAGE_BYTES,
    connected_change_core_v2_fingerprint,
    connected_change_file_v2_fingerprint,
    connected_change_member_id,
    require_connected_change_lineage_size,
)
from name_atlas.folder_refactor.connected_change.derivative import (
    _next_derivative_generation,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    build_change_file_input_binding,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    build_portable_execution_authorization,
)
from name_atlas.folder_refactor.connected_change.organized_tree import (
    OrganizedTreeMember,
    OrganizedTreeSnapshot,
    compute_organized_tree_commitment,
    scan_organized_tree,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    build_foldweave_artifact_commitments,
    build_foldweave_receipt,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptCoreV3,
    FolderReceiptEnvelopeV3,
    build_folder_receipt_envelope_v3,
    foldweave_required_receipt_artifact_paths,
    parse_folder_receipt_envelope_any,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.contracts import (
    FolderInventory,
    FolderVerificationReport,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.planner_provider import (
    DETERMINISTIC_DEVELOPMENT_REQUEST,
    DeterministicDevelopmentPlannerProvider,
)
from name_atlas.folder_refactor.portable_artifacts import (
    ACCEPTED_PLAN_PATH,
    CHANGE_LEDGER_PATH,
    FORWARD_PATH_MAP_PATH,
    REFERENCE_GRAPH_PATH,
    SOURCE_SNAPSHOT_PATH,
    USER_REQUEST_PATH,
    VERIFICATION_REPORT_PATH,
    FolderPortableArtifactError,
    parse_folder_path_map,
    parse_portable_model,
    read_regular_bytes,
    staged_data_commitment,
    staged_data_members,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderArtifactCommitment,
    FolderChangeLedger,
    FolderStagedDataMember,
    FolderUserRequestArtifact,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)
from name_atlas.verification.bagit_validator import BagItPackageValidator

_REQUEST = "Create one connected client handoff."
_SOURCE_COMMITMENT = "a" * 64
_EVIDENCE_FINGERPRINT = "b" * 64
_ACCEPTED_PLAN_FINGERPRINT = "c" * 64
_CANDIDATE_FINGERPRINT = "d" * 64
_PAYLOAD_SHA256 = "e" * 64
_UUID4_HEX = "00000000000040008000000000000000"


def test_root_v2_change_file_is_canonical_payload_free_and_self_bound() -> None:
    core = _core_v2(target="organized/source.txt")
    receipt = _receipt_v3(core)
    change_file = create_connected_change_file_v2(
        core,
        originating_receipt=receipt,
    )
    payload = canonical_json_bytes(change_file)

    assert parse_connected_change_file_v2(payload) == change_file
    assert parse_connected_change_file_any(payload) == change_file
    assert change_file.core.lineage.generation == 0
    assert change_file.core_fingerprint == canonical_sha256(change_file.core)
    assert change_file.change_file_fingerprint == (
        connected_change_file_v2_fingerprint(change_file)
    )
    assert change_file.originating_receipt.receipt_fingerprint not in (
        change_file.originating_receipt.receipt.model_dump_json()
    )
    assert b"PAYLOAD-CONTENT-SENTINEL" not in payload
    assert b"/Users/" not in payload


def test_child_v2_is_complete_self_contained_and_immediate_parent_only() -> None:
    parent_core = _core_v2(target="organized/source.txt")
    parent = create_connected_change_file_v2(
        parent_core,
        originating_receipt=_receipt_v3(parent_core),
    )
    child_member = _member("final/source.txt")
    binding = ConnectedChangeMemberBindingV1(
        parent_logical_member_id=parent.core.members[0].logical_member_id,
        child_logical_member_id=child_member.logical_member_id,
    )
    lineage = build_connected_change_lineage(
        parent_change_file=parent,
        parent_candidate_fingerprint=_CANDIDATE_FINGERPRINT,
        revision_instruction_fingerprint="f" * 64,
        member_bindings=(binding,),
    )
    child_core = _core_v2(target="final/source.txt", lineage=lineage)
    child_receipt = _receipt_v3(
        child_core,
        execution_role="derivative",
        imported_change_file_fingerprint=parent.change_file_fingerprint,
        originating_receipt_fingerprint=(
            parent.originating_receipt.receipt_fingerprint
        ),
    )
    child = create_connected_change_file_v2(
        child_core,
        originating_receipt=child_receipt,
    )
    payload = canonical_json_bytes(child)

    assert parse_connected_change_file_any(payload) == child
    assert child.core.lineage.generation == 1
    assert child.core.lineage.parent_generation == 0
    assert child.core.lineage.parent_change_file_fingerprint == (
        parent.change_file_fingerprint
    )
    assert child.core.lineage.member_bindings == (binding,)
    assert parent.change_file_fingerprint.encode() in payload
    assert parent.core_fingerprint.encode() in payload
    assert canonical_json_bytes(parent) not in payload
    assert child.originating_receipt.receipt.connected_change_core_fingerprint == (
        child.core_fingerprint
    )
    assert child.change_file_fingerprint not in (
        child.originating_receipt.receipt.model_dump_json()
    )


def test_v2_parser_rejects_fingerprint_tampering_and_noncanonical_bytes() -> None:
    core = _core_v2(target="organized/source.txt")
    change_file = create_connected_change_file_v2(
        core,
        originating_receipt=_receipt_v3(core),
    )
    raw = json.loads(canonical_json_bytes(change_file))
    raw["core"]["request"] += " changed"
    tampered = canonical_json_bytes(raw)

    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file_v2(tampered)
    assert error.value.code == "change_file_fingerprint_mismatch"

    noncanonical = json.dumps(
        change_file.model_dump(mode="json"),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ).encode()
    with pytest.raises(ConnectedChangeError) as error:
        parse_connected_change_file_v2(noncanonical)
    assert error.value.code == "change_file_schema_invalid"


def test_lineage_generation_32_is_valid_and_generation_33_blocks() -> None:
    member = _member("generation-32/source.txt")
    lineage_32 = ConnectedChangeLineageV1(
        generation=32,
        parent_generation=31,
        parent_change_file_schema_version="connected-change-file.v2",
        parent_core_schema_version="connected-change-core.v2",
        parent_change_file_fingerprint="1" * 64,
        parent_core_fingerprint="2" * 64,
        parent_originating_receipt_fingerprint="3" * 64,
        parent_organized_tree_commitment="4" * 64,
        parent_candidate_fingerprint=_CANDIDATE_FINGERPRINT,
        revision_instruction_fingerprint="5" * 64,
        member_bindings=(
            ConnectedChangeMemberBindingV1(
                parent_logical_member_id="6" * 64,
                child_logical_member_id=member.logical_member_id,
            ),
        ),
    )
    core_32 = _core_v2(target="generation-32/source.txt", lineage=lineage_32)
    parent_32 = create_connected_change_file_v2(
        core_32,
        originating_receipt=_receipt_v3(
            core_32,
            execution_role="derivative",
            imported_change_file_fingerprint="1" * 64,
            originating_receipt_fingerprint="3" * 64,
        ),
    )
    assert parent_32.core.lineage.generation == 32
    with pytest.raises(ConnectedChangeError) as generation_error:
        _next_derivative_generation(parent_32)
    assert generation_error.value.code == "change_file_lineage_generation_exceeded"

    with pytest.raises(ConnectedChangeError) as error:
        build_connected_change_lineage(
            parent_change_file=parent_32,
            parent_candidate_fingerprint=_CANDIDATE_FINGERPRINT,
            revision_instruction_fingerprint="7" * 64,
            member_bindings=(
                ConnectedChangeMemberBindingV1(
                    parent_logical_member_id=member.logical_member_id,
                    child_logical_member_id="8" * 64,
                ),
            ),
        )
    assert error.value.code == "change_file_lineage_generation_exceeded"

    with pytest.raises(ValidationError):
        ConnectedChangeLineageV1(generation=33)


def test_derivative_generation_32_is_derived_from_v2_generation_31() -> None:
    member = _member("generation-31/source.txt")
    lineage_31 = ConnectedChangeLineageV1(
        generation=31,
        parent_generation=30,
        parent_change_file_schema_version="connected-change-file.v2",
        parent_core_schema_version="connected-change-core.v2",
        parent_change_file_fingerprint="1" * 64,
        parent_core_fingerprint="2" * 64,
        parent_originating_receipt_fingerprint="3" * 64,
        parent_organized_tree_commitment="4" * 64,
        parent_candidate_fingerprint=_CANDIDATE_FINGERPRINT,
        revision_instruction_fingerprint="5" * 64,
        member_bindings=(
            ConnectedChangeMemberBindingV1(
                parent_logical_member_id="6" * 64,
                child_logical_member_id=member.logical_member_id,
            ),
        ),
    )
    core_31 = _core_v2(target="generation-31/source.txt", lineage=lineage_31)
    parent_31 = create_connected_change_file_v2(
        core_31,
        originating_receipt=_receipt_v3(
            core_31,
            execution_role="derivative",
            imported_change_file_fingerprint="1" * 64,
            originating_receipt_fingerprint="3" * 64,
        ),
    )

    assert _next_derivative_generation(parent_31) == 32


def test_change_file_input_binding_strictly_dispatches_v2(tmp_path: Path) -> None:
    core = _core_v2(target="organized/source.txt")
    change_file = create_connected_change_file_v2(
        core,
        originating_receipt=_receipt_v3(core),
    )
    path = (tmp_path / "parent.foldweave-change.json").resolve()
    path.write_bytes(canonical_json_bytes(change_file))

    binding = build_change_file_input_binding(path)

    assert binding.change_file == change_file
    assert binding.change_file.schema_version == "connected-change-file.v2"


def test_lineage_canonical_byte_limit_is_inclusive() -> None:
    require_connected_change_lineage_size(b"x" * MAX_CONNECTED_CHANGE_LINEAGE_BYTES)
    with pytest.raises(ConnectedChangeError) as error:
        require_connected_change_lineage_size(
            b"x" * (MAX_CONNECTED_CHANGE_LINEAGE_BYTES + 1)
        )
    assert error.value.code == "change_file_lineage_too_large"


def test_receipt_any_dispatch_is_canonical_and_rejects_unknown_versions() -> None:
    core = _core_v2(target="organized/source.txt")
    receipt = _receipt_v3(core)
    payload = canonical_json_bytes(receipt)

    assert parse_folder_receipt_envelope_any(payload) == receipt
    with pytest.raises(FolderPortableArtifactError):
        parse_folder_receipt_envelope_any(b"\n" + payload)

    raw = json.loads(payload)
    raw["receipt"]["schema_version"] = "folder-change-receipt.v999"
    with pytest.raises(FolderPortableArtifactError):
        parse_folder_receipt_envelope_any(canonical_json_bytes(raw))


def test_derivative_receipt_must_bind_the_exact_immediate_parent() -> None:
    parent_core = _core_v2(target="organized/source.txt")
    parent = create_connected_change_file_v2(
        parent_core,
        originating_receipt=_receipt_v3(parent_core),
    )
    child_member = _member("final/source.txt")
    lineage = build_connected_change_lineage(
        parent_change_file=parent,
        parent_candidate_fingerprint=_CANDIDATE_FINGERPRINT,
        revision_instruction_fingerprint="f" * 64,
        member_bindings=(
            ConnectedChangeMemberBindingV1(
                parent_logical_member_id=parent.core.members[0].logical_member_id,
                child_logical_member_id=child_member.logical_member_id,
            ),
        ),
    )
    core = _core_v2(target="final/source.txt", lineage=lineage)
    wrong_receipt = _receipt_v3(
        core,
        execution_role="derivative",
        imported_change_file_fingerprint="9" * 64,
        originating_receipt_fingerprint=(
            parent.originating_receipt.receipt_fingerprint
        ),
    )

    with pytest.raises(ConnectedChangeError) as error:
        create_connected_change_file_v2(core, originating_receipt=wrong_receipt)
    assert error.value.code == "change_file_fingerprint_mismatch"


@pytest.mark.anyio
async def test_v3_receipt_builder_binds_review_core_and_exact_artifacts(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    reviewing = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "origin.json",
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="v3-receipt-origin",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    verified = service.accept(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=reviewing.candidate_plan.result_folder_name,
        idempotency_key="v3-receipt-accept",
        channel="cli",
    )
    assert verified.final_result_path is not None
    assert verified.preview is not None
    assert verified.execution_authorization is not None
    assert verified.candidate_plan is not None
    assert verified.reference_graph is not None
    evidence_ledger = verified.authority.evidence_ledger
    execution_origin = verified.authority.execution_origin
    assert evidence_ledger is not None
    assert execution_origin is not None

    result_root = verified.final_result_path
    root_change = parse_connected_change_file_any(
        read_regular_bytes(result_root, "name-atlas/connected_change_capsule.json")
    )
    assert root_change.schema_version == "connected-change-file.v2"
    assert root_change.core.lineage == ConnectedChangeLineageV1(generation=0)
    assert (
        parse_folder_receipt_envelope_any(
            canonical_json_bytes(root_change.originating_receipt)
        )
        == root_change.originating_receipt
    )
    root_core = root_change.core
    pending = tmp_path / "pending-authorities"
    shutil.copytree(result_root, pending)
    inventory = parse_portable_model(
        read_regular_bytes(result_root, SOURCE_SNAPSHOT_PATH),
        FolderInventory,
    )
    user_request = parse_portable_model(
        read_regular_bytes(result_root, USER_REQUEST_PATH),
        FolderUserRequestArtifact,
    )
    accepted_plan = parse_portable_model(
        read_regular_bytes(result_root, ACCEPTED_PLAN_PATH),
        type(verified.candidate_plan),
    )
    graph = parse_portable_model(
        read_regular_bytes(result_root, REFERENCE_GRAPH_PATH),
        FolderReferenceGraph,
    )
    path_rows = parse_folder_path_map(
        read_regular_bytes(result_root, FORWARD_PATH_MAP_PATH),
        reverse=False,
    )
    ledger = parse_portable_model(
        read_regular_bytes(result_root, CHANGE_LEDGER_PATH),
        FolderChangeLedger,
    )
    report = parse_portable_model(
        read_regular_bytes(result_root, VERIFICATION_REPORT_PATH),
        FolderVerificationReport,
    )
    staged = staged_data_members(result_root)
    staged_commitment = staged_data_commitment(staged)
    organized = scan_organized_tree(result_root / "data")
    artifacts = build_foldweave_artifact_commitments(
        pending,
        original_content_file_ids=tuple(
            sorted(
                path.stem
                for path in (pending / "name-atlas/original-content").glob("*.bin")
            )
        ),
        execution_role="origin",
    )
    bagit = BagItPackageValidator().validate(result_root)

    receipt_inputs = dict(
        execution_role="origin",
        job_id=verified.job_id,
        inventory=inventory,
        user_request=user_request,
        accepted_plan=accepted_plan,
        reference_graph=graph,
        path_rows=path_rows,
        change_ledger=ledger,
        report=report,
        execution_origin=execution_origin,
        execution_authorization=build_portable_execution_authorization(
            verified.execution_authorization
        ),
        plan_preview=verified.preview,
        connected_change_core=root_core,
        evidence_ledger=evidence_ledger,
        staged_members=staged,
        staged_data_commitment=staged_commitment,
        organized_tree=organized,
        producer_bagit_validation=bagit,
    )
    tampered_artifacts = tuple(
        item.model_copy(update={"sha256": "0" * 64})
        if item.path == ACCEPTED_PLAN_PATH
        else item
        for item in artifacts
    )
    with pytest.raises(ValueError, match="exact authority bytes"):
        build_foldweave_receipt(
            **receipt_inputs,
            artifact_commitments=tampered_artifacts,
        )
    receipt = build_foldweave_receipt(
        **receipt_inputs,
        artifact_commitments=artifacts,
    )

    assert receipt.receipt.schema_version == "folder-change-receipt.v3"
    assert receipt.receipt.execution_role == "origin"
    assert receipt.receipt.connected_change_core_fingerprint == (
        connected_change_core_v2_fingerprint(root_core)
    )
    assert receipt.receipt.execution_authorization_fingerprint == (
        verified.execution_authorization.authorization_fingerprint
    )
    assert receipt.receipt.plan_preview_fingerprint == (
        verified.preview.preview_fingerprint
    )
    assert parse_folder_receipt_envelope_any(canonical_json_bytes(receipt)) == receipt


def _member(target: str) -> ConnectedChangeMember:
    provisional = ConnectedChangeMember.model_construct(
        logical_member_id="0" * 64,
        descriptor_kind="ordinary",
        origin_relative_path="source.txt",
        target_relative_path=target,
        protected_suffix=".txt",
        protected=False,
        byte_size=7,
        payload_sha256=_PAYLOAD_SHA256,
        markdown_non_destination_sha256=None,
        link_slots=(),
    )
    return ConnectedChangeMember(
        **provisional.model_dump(mode="python", exclude={"logical_member_id"}),
        logical_member_id=connected_change_member_id(provisional),
    )


def _core_v2(
    *,
    target: str,
    lineage: ConnectedChangeLineageV1 | None = None,
):
    member = _member(target)
    tree_member = OrganizedTreeMember(
        member_kind="regular_file",
        relative_path=target,
        size=7,
        sha256=_PAYLOAD_SHA256,
    )
    tree_commitment = compute_organized_tree_commitment((tree_member,))
    complete = ConnectedChangeCore(
        request=_REQUEST,
        request_fingerprint=request_fingerprint(_REQUEST),
        requested_result_folder_name="Foldweave-result",
        origin_source_commitment=_SOURCE_COMMITMENT,
        members=(member,),
        expected_file_count=1,
        expected_empty_directory_count=0,
        expected_supported_link_count=0,
        expected_organized_tree_commitment=tree_commitment,
        origin_proof_identifiers=tuple(
            sorted((_EVIDENCE_FINGERPRINT, _ACCEPTED_PLAN_FINGERPRINT))
        ),
    )
    return build_connected_change_core_v2(
        complete,
        lineage=lineage or ConnectedChangeLineageV1(generation=0),
    )


def _receipt_v3(
    core,
    *,
    execution_role: str = "origin",
    imported_change_file_fingerprint: str | None = None,
    originating_receipt_fingerprint: str | None = None,
) -> FolderReceiptEnvelopeV3:
    target = core.members[0].target_relative_path
    tree_member = OrganizedTreeMember(
        member_kind="regular_file",
        relative_path=target,
        size=7,
        sha256=_PAYLOAD_SHA256,
    )
    tree = OrganizedTreeSnapshot(
        members=(tree_member,),
        commitment=compute_organized_tree_commitment((tree_member,)),
    )
    paths = foldweave_required_receipt_artifact_paths(execution_role)
    commitments = tuple(
        FolderArtifactCommitment(path=path, size=1, sha256="f" * 64)
        for path in sorted(paths)
    )
    receiver_values = (
        {
            "imported_change_file_fingerprint": imported_change_file_fingerprint,
            "imported_change_file_sha256": "1" * 64,
            "originating_receipt_fingerprint": originating_receipt_fingerprint,
            "match_report_fingerprint": "2" * 64,
            "match_report_sha256": "3" * 64,
        }
        if execution_role != "origin"
        else {}
    )
    receipt = FolderReceiptCoreV3(
        execution_role=execution_role,
        job_id=_UUID4_HEX,
        source_commitment=_SOURCE_COMMITMENT,
        source_file_count=1,
        source_directory_count=0,
        source_bytes=7,
        request_fingerprint=request_fingerprint(_REQUEST),
        evidence_fingerprint=_EVIDENCE_FINGERPRINT,
        accepted_plan_fingerprint=_ACCEPTED_PLAN_FINGERPRINT,
        reference_graph_fingerprint="4" * 64,
        execution_origin_fingerprint="5" * 64,
        execution_authorization_fingerprint="6" * 64,
        plan_preview_fingerprint="7" * 64,
        compiled_candidate_fingerprint=_CANDIDATE_FINGERPRINT,
        change_ledger_fingerprint="8" * 64,
        verification_report_fingerprint="9" * 64,
        connected_change_core_schema_version="connected-change-core.v2",
        connected_change_core_fingerprint=connected_change_core_v2_fingerprint(core),
        lineage_generation=core.lineage.generation,
        artifact_commitments=commitments,
        staged_data_members=(
            FolderStagedDataMember(
                path=target,
                size=7,
                sha256=_PAYLOAD_SHA256,
            ),
        ),
        staged_data_commitment="0" * 64,
        organized_tree=tree,
        map_row_count=1,
        path_change_count=1,
        supported_link_count=0,
        rewritten_link_count=0,
        producer_bagit_messages=("BagIt validation passed.",),
        **receiver_values,
    )
    return build_folder_receipt_envelope_v3(receipt)
