"""Deterministic F2 portability, compatibility, and lineage-boundary acceptance."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from connected_change_fixtures import make_connected_change_fixture, portable_tree
from test_foldweave_serial_collaboration import (
    _accept_review,
    _OneTurnDerivativeProvider,
)

from name_atlas.folder_refactor.connected_change import (
    ConnectedChangeCore,
    ConnectedChangeError,
    ConnectedChangeLineageV1,
    ConnectedChangeMember,
    ConnectedChangeMemberBindingV1,
    build_connected_change_core_v2,
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CONNECTED_CHANGE_LINEAGE_BYTES,
    connected_change_member_id,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
    GptDerivativeJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.organized_tree import (
    OrganizedTreeMember,
    compute_organized_tree_commitment,
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
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    request_fingerprint,
)

_MAXIMUM_VALID_LINEAGE_BYTES = 95_329


@pytest.mark.anyio
async def test_legacy_parent_exports_portable_v2_child_without_parent_artifacts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A v1 parent can yield one independently portable and reconstructable CF2."""

    monkeypatch.chdir(tmp_path)
    producer = tmp_path / "producer"
    fixture = make_connected_change_fixture(producer / "projects")
    jobs = producer / "jobs"
    legacy_output = producer / "legacy-output"
    derivative_output = producer / "derivative-output"
    for directory in (jobs, legacy_output, derivative_output):
        directory.mkdir(parents=True)

    legacy = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=legacy_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    assert verify_connected_result(legacy.folder_run.result_root).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    cf1_bytes = legacy.change_file_path.read_bytes()
    cf1 = parse_connected_change_file_any(cf1_bytes)
    assert cf1.schema_version == "connected-change-file.v1"
    cf1_relative_path = legacy.change_file_path.relative_to(producer)

    service = FoldweaveReviewService()
    parent = service.prepare_application_review(
        change_file_path=legacy.change_file_path,
        source_root=fixture.martin_root,
        output_parent=derivative_output,
        job_path=jobs / "legacy-parent.json",
        idempotency_key="f2-legacy-parent-review",
    )
    assert parent.lifecycle is FolderJobLifecycleV3.REVIEWING
    child = service.create_or_resume_derivative_child(
        parent.job_path,
        output_parent=derivative_output,
        instruction="Move one document into the portable successor structure.",
        idempotency_key="f2-legacy-child",
        provider_kind="deterministic",
        channel="native_app",
    )
    reviewed = await service.submit_direct_derivative_revision(
        child.job_path,
        provider=_provider_for_generation(child, generation=1),
    )
    derivative = _accept_review(
        service,
        reviewed,
        output_parent=derivative_output,
        idempotency_key="f2-legacy-child-accept",
    )
    assert derivative.final_result_path is not None
    assert service.verify_result(derivative.job_path).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    cf2_path = service.get_change_file(derivative.job_path)[0]
    cf2_bytes = cf2_path.read_bytes()
    cf2 = parse_connected_change_file_any(cf2_bytes)
    assert cf2.schema_version == "connected-change-file.v2"
    assert cf2.core.lineage.generation == 1
    assert cf2.core.lineage.parent_change_file_schema_version == (
        "connected-change-file.v1"
    )
    assert cf2.core.lineage.parent_change_file_fingerprint == (
        cf1.change_file_fingerprint
    )

    isolated = tmp_path / "isolated-consumer"
    isolated.mkdir()
    copied_cf2 = isolated / "successor.foldweave-change.json"
    copied_result = isolated / "copied-derivative-result"
    copied_sofia = isolated / "raw-sofia-source"
    copied_martin = isolated / "martin-source-at-transaction-start"
    copied_t1_data = isolated / "verified-t1-data"
    shutil.copy2(cf2_path, copied_cf2)
    shutil.copytree(derivative.final_result_path, copied_result)
    shutil.copytree(fixture.sofia_root, copied_sofia)
    shutil.copytree(fixture.martin_root, copied_martin)
    shutil.copytree(legacy.folder_run.result_root / "data", copied_t1_data)
    assert copied_cf2.read_bytes() == cf2_bytes
    assert (
        copied_result / "name-atlas" / "connected_change_capsule.json"
    ).read_bytes() == cf2_bytes

    parent_paths = (
        legacy.change_file_path,
        legacy.folder_run.result_root,
        parent.job_path,
        derivative.job_path,
        derivative.final_result_path,
    )
    preserved_parent_evidence = tmp_path / "preserved-parent-evidence"
    producer.rename(preserved_parent_evidence)
    assert preserved_parent_evidence.is_dir()
    assert all(not path.exists() for path in parent_paths)
    assert (preserved_parent_evidence / cf1_relative_path).read_bytes() == cf1_bytes

    copied_verification = verify_connected_result(copied_result)
    assert copied_verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    copied_derivative_restoration = isolated / "restored-martin-source"
    restore_connected_result(copied_result, copied_derivative_restoration)
    assert portable_tree(copied_derivative_restoration) == portable_tree(copied_martin)

    raw_output = isolated / "raw-application-output"
    prior_output = isolated / "prior-t1-application-output"
    raw_output.mkdir()
    prior_output.mkdir()
    raw_application = apply_connected_change(
        change_file_path=copied_cf2,
        source_root=copied_sofia,
        output_parent=raw_output,
    )
    prior_application = apply_connected_change(
        change_file_path=copied_cf2,
        source_root=copied_t1_data,
        output_parent=prior_output,
    )

    assert copied_verification.organized_tree_commitment is not None
    expected_commitment = copied_verification.organized_tree_commitment
    assert raw_application.organized_tree_commitment == expected_commitment
    assert prior_application.organized_tree_commitment == expected_commitment
    for application in (raw_application, prior_application):
        assert verify_connected_result(application.folder_run.result_root).status is (
            ConnectedReceiptVerificationStatus.VERIFIED
        )

    restored_sofia = isolated / "restored-sofia-source"
    restored_t1 = isolated / "restored-prior-t1-data"
    restore_connected_result(raw_application.folder_run.result_root, restored_sofia)
    restore_connected_result(prior_application.folder_run.result_root, restored_t1)
    assert portable_tree(restored_sofia) == portable_tree(copied_sofia)
    assert portable_tree(restored_t1) == portable_tree(copied_t1_data)
    assert copied_cf2.read_bytes() == cf2_bytes


def test_maximum_current_schema_lineage_with_500_bindings_is_valid() -> None:
    """Exercise the largest exportable lineage shape instead of padded bytes."""

    members = tuple(
        sorted(
            (_member(index) for index in range(500)),
            key=lambda item: item.logical_member_id,
        )
    )
    bindings = tuple(
        ConnectedChangeMemberBindingV1(
            parent_logical_member_id=f"{index:064x}",
            child_logical_member_id=member.logical_member_id,
        )
        for index, member in enumerate(members)
    )
    lineage = ConnectedChangeLineageV1(
        generation=32,
        parent_generation=31,
        parent_change_file_schema_version="connected-change-file.v2",
        parent_core_schema_version="connected-change-core.v2",
        parent_change_file_fingerprint="a" * 64,
        parent_core_fingerprint="b" * 64,
        parent_originating_receipt_fingerprint="c" * 64,
        parent_organized_tree_commitment="d" * 64,
        parent_candidate_fingerprint="e" * 64,
        revision_instruction_fingerprint="f" * 64,
        member_bindings=bindings,
    )
    request = "Exercise the maximum current Foldweave lineage shape."
    tree_members = tuple(
        OrganizedTreeMember(
            member_kind="regular_file",
            relative_path=member.target_relative_path,
            size=member.byte_size,
            sha256=member.payload_sha256,
        )
        for member in members
    )
    complete = ConnectedChangeCore(
        request=request,
        request_fingerprint=request_fingerprint(request),
        requested_result_folder_name="Foldweave-maximum-lineage",
        origin_source_commitment="1" * 64,
        members=members,
        expected_file_count=500,
        expected_empty_directory_count=0,
        expected_supported_link_count=0,
        expected_organized_tree_commitment=(
            compute_organized_tree_commitment(tree_members)
        ),
        origin_proof_identifiers=("2" * 64, "3" * 64),
    )

    core = build_connected_change_core_v2(complete, lineage=lineage)
    payload = canonical_json_bytes(core.lineage)

    assert len(core.members) == 500
    assert len(core.lineage.member_bindings) == 500
    assert len(payload) == _MAXIMUM_VALID_LINEAGE_BYTES
    assert len(payload) < MAX_CONNECTED_CHANGE_LINEAGE_BYTES


@pytest.mark.anyio
async def test_real_generation_31_parent_exports_generation_32_and_33_blocks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Drive real finalized descendants through the inclusive generation limit."""

    monkeypatch.chdir(tmp_path)
    fixture = make_connected_change_fixture(tmp_path / "projects")
    jobs = tmp_path / "jobs"
    root_output = tmp_path / "root-output"
    jobs.mkdir()
    root_output.mkdir()
    root = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=root_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    current_cf = root.change_file_path
    service = FoldweaveReviewService()
    generation_31_result: FolderRefactorJobV3 | None = None
    generation_32_result: FolderRefactorJobV3 | None = None

    for generation in range(1, 33):
        output_parent = tmp_path / f"generation-{generation:02d}-output"
        output_parent.mkdir()
        parent = service.prepare_application_review(
            change_file_path=current_cf,
            source_root=fixture.martin_root,
            output_parent=output_parent,
            job_path=jobs / f"generation-{generation:02d}-parent.json",
            idempotency_key=f"f2-generation-{generation:02d}-parent",
        )
        assert parent.lifecycle is FolderJobLifecycleV3.REVIEWING
        child = service.create_or_resume_derivative_child(
            parent.job_path,
            output_parent=output_parent,
            instruction=f"Create verified lineage generation {generation}.",
            idempotency_key=f"f2-generation-{generation:02d}-child",
            provider_kind="deterministic",
            channel="native_app",
        )
        reviewed = await service.submit_direct_derivative_revision(
            child.job_path,
            provider=_provider_for_generation(child, generation=generation),
        )
        verified = _accept_review(
            service,
            reviewed,
            output_parent=output_parent,
            idempotency_key=f"f2-generation-{generation:02d}-accept",
        )
        assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
        current_cf = service.get_change_file(verified.job_path)[0]
        parsed = parse_connected_change_file_any(current_cf.read_bytes())
        assert parsed.schema_version == "connected-change-file.v2"
        assert parsed.core.lineage.generation == generation
        if generation == 31:
            generation_31_result = verified
        elif generation == 32:
            generation_32_result = verified

    assert generation_31_result is not None
    assert generation_32_result is not None
    assert service.verify_result(generation_31_result.job_path).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    assert service.verify_result(generation_32_result.job_path).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    generation_32_cf_bytes = current_cf.read_bytes()

    blocked_output = tmp_path / "generation-33-output"
    blocked_output.mkdir()
    generation_32_parent = service.prepare_application_review(
        change_file_path=current_cf,
        source_root=fixture.martin_root,
        output_parent=blocked_output,
        job_path=jobs / "generation-33-parent.json",
        idempotency_key="f2-generation-33-parent",
    )
    assert generation_32_parent.lifecycle is FolderJobLifecycleV3.REVIEWING
    job_paths_before = frozenset(jobs.iterdir())
    receipts_before = frozenset(tmp_path.rglob("folder_change_receipt.json"))
    change_files_before = frozenset(tmp_path.rglob("connected_change_capsule.json"))

    with pytest.raises(ConnectedChangeError) as error:
        service.create_or_resume_derivative_child(
            generation_32_parent.job_path,
            output_parent=blocked_output,
            instruction="Generation 33 must not allocate a child or output.",
            idempotency_key="f2-generation-33-child",
            provider_kind="deterministic",
            channel="native_app",
        )

    assert error.value.code == "change_file_lineage_generation_exceeded"
    assert frozenset(jobs.iterdir()) == job_paths_before
    assert frozenset(tmp_path.rglob("folder_change_receipt.json")) == receipts_before
    assert (
        frozenset(tmp_path.rglob("connected_change_capsule.json"))
        == change_files_before
    )
    assert tuple(blocked_output.iterdir()) == ()
    assert current_cf.read_bytes() == generation_32_cf_bytes


def _member(index: int) -> ConnectedChangeMember:
    origin = f"source/{index:03d}.txt"
    target = f"organized/{index:03d}.txt"
    provisional = ConnectedChangeMember.model_construct(
        logical_member_id="0" * 64,
        descriptor_kind="ordinary",
        origin_relative_path=origin,
        target_relative_path=target,
        protected_suffix=".txt",
        protected=False,
        byte_size=index + 1,
        payload_sha256=f"{index + 1:064x}",
        markdown_non_destination_sha256=None,
        link_slots=(),
    )
    return ConnectedChangeMember(
        **provisional.model_dump(mode="python", exclude={"logical_member_id"}),
        logical_member_id=connected_change_member_id(provisional),
    )


def _provider_for_generation(
    child: FolderRefactorJobV3,
    *,
    generation: int,
) -> _OneTurnDerivativeProvider:
    assert isinstance(child.authority, GptDerivativeJobAuthorityV3)
    parent = child.authority.parent_binding
    mapping = next(
        item for item in parent.parent_candidate.file_mappings if not item.protected
    )
    return _OneTurnDerivativeProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=parent.parent_candidate_fingerprint,
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=mapping.file_id,
                    replacement_target_path=(
                        f"generation-{generation:02d}/{Path(mapping.target_path).name}"
                    ),
                    rationale=f"Create verified lineage generation {generation}.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )
