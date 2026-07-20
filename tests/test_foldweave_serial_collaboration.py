"""Integrated Sofia/Martin serial-collaboration acceptance evidence."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest
from connected_change_fixtures import (
    make_connected_change_fixture,
    portable_tree,
    tree_state,
)

from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
    GptDerivativeJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.preview import FolderPlanTreeMember
from name_atlas.folder_refactor.connected_change.reconstruction import (
    restore_connected_result,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.service import (
    apply_connected_change,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage


class _OneTurnDerivativeProvider:
    """Return one deterministic sparse revision without external I/O."""

    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self, revision: FolderPlanRevisionV1) -> None:
        self._revision = revision
        self.calls = 0
        self.inputs: list[FolderDerivativeRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderDerivativeRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.calls += 1
        self.inputs.append(turn_input)
        return FolderRevisionProviderResponseV1(
            provider_kind="deterministic",
            call_id="serial-collaboration-derivative-turn",
            revision=self._revision,
        )


@pytest.mark.anyio
async def test_sofia_martin_sofia_serial_collaboration_is_proof_carrying(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """T1 can be accepted unchanged or forked into a self-contained T2."""

    monkeypatch.chdir(tmp_path)
    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    jobs = tmp_path / "jobs"
    sofia_t1_output = tmp_path / "sofia-t1-output"
    martin_t1_output = tmp_path / "martin-t1-output"
    martin_t2_output = tmp_path / "martin-t2-output"
    sofia_t2_output = tmp_path / "sofia-t2-output"
    prior_t1_t2_output = tmp_path / "prior-t1-t2-output"
    for directory in (
        jobs,
        sofia_t1_output,
        martin_t1_output,
        martin_t2_output,
        sofia_t2_output,
        prior_t1_t2_output,
    ):
        directory.mkdir()

    sofia_source_before = tree_state(fixture.sofia_root)
    martin_source_before = tree_state(fixture.martin_root)

    sofia_review = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=sofia_t1_output,
        job_path=jobs / "sofia-t1.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="serial-sofia-t1-review",
    )
    sofia_t1 = _accept_review(
        service,
        sofia_review,
        output_parent=sofia_t1_output,
        idempotency_key="serial-sofia-t1-accept",
    )
    cf1_path = service.get_change_file(sofia_t1.job_path)[0]
    cf1_before = _file_state(cf1_path)

    martin_review = service.prepare_application_review(
        change_file_path=cf1_path,
        source_root=fixture.martin_root,
        output_parent=martin_t1_output,
        job_path=jobs / "martin-t1.json",
        idempotency_key="serial-martin-t1-review",
    )

    assert martin_review.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert isinstance(martin_review.authority, CapsuleAppliedJobAuthorityV2)
    assert martin_review.preview is not None
    assert martin_review.candidate_plan is not None
    assert martin_review.authority.match_report.status == "matched"
    assert len(martin_review.authority.match_report.mappings) == len(
        martin_review.source_inventory.files
    )
    assert (
        sofia_t1.source_inventory.source_commitment
        != martin_review.source_inventory.source_commitment
    )
    source_member_paths = {
        item.relative_path for item in martin_review.source_inventory.files
    } | {
        item.relative_path for item in martin_review.source_inventory.empty_directories
    }
    assert _member_paths(martin_review.preview.current_tree_members) == (
        source_member_paths
    )
    assert _member_paths(martin_review.preview.proposed_tree_members) == (
        set(fixture.target_paths.values()) | {"empty/keep"}
    )
    assert tuple(martin_t1_output.iterdir()) == ()

    child = service.create_or_resume_derivative_child(
        martin_review.job_path,
        output_parent=martin_t2_output,
        instruction="Move one document into collaborative review.",
        idempotency_key="serial-martin-t2-child",
        provider_kind="deterministic",
        channel="native_app",
    )
    assert isinstance(child.authority, GptDerivativeJobAuthorityV3)
    assert child.authority.parent_binding.parent_job_id == martin_review.job_id
    assert child.authority.parent_binding.parent_candidate == (
        martin_review.candidate_plan
    )

    martin_t1 = _accept_review(
        service,
        martin_review,
        output_parent=martin_t1_output,
        idempotency_key="serial-martin-t1-accept-unchanged",
    )
    assert isinstance(martin_t1.authority, CapsuleAppliedJobAuthorityV2)
    assert martin_t1.authority.execution_origin is not None
    assert martin_t1.authority.execution_origin.kind == "capsule_applied"
    assert martin_t1.authority.execution_origin.provider_call_count == 0
    assert martin_t1.authority.execution_origin.api_used is False
    assert martin_t1.authority.execution_origin.external_network_used is False
    assert not (tmp_path / ".name-atlas" / "api_budget.json").exists()
    assert service.verify_result(martin_t1.job_path).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    assert (
        martin_t1.verified_artifacts is not None
        and sofia_t1.verified_artifacts is not None
        and martin_t1.verified_artifacts.organized_tree_commitment
        == sofia_t1.verified_artifacts.organized_tree_commitment
    )

    martin_t1_restored = tmp_path / "restored" / "martin-t1-original"
    martin_t1_restored.parent.mkdir()
    service.recreate_original(martin_t1.job_path, martin_t1_restored)
    assert portable_tree(martin_t1_restored) == portable_tree(fixture.martin_root)
    assert portable_tree(martin_t1_restored) != portable_tree(fixture.sofia_root)

    parent_after_unchanged_accept = martin_review.job_path.read_bytes()
    provider = _provider_for_child(child)
    martin_t2_review = await service.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )
    assert provider.calls == 1
    assert provider.inputs == [child.authority.pending_direct_revision]
    assert martin_t2_review.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert martin_t2_review.preview is not None
    assert martin_t2_review.candidate_plan is not None
    assert martin_t2_review.preview.proposal_basis == "gpt_derivative"
    assert tuple(martin_t2_output.iterdir()) == ()

    martin_t2 = _accept_review(
        service,
        martin_t2_review,
        output_parent=martin_t2_output,
        idempotency_key="serial-martin-t2-accept",
    )
    assert martin_review.job_path.read_bytes() == parent_after_unchanged_accept
    assert service.verify_result(martin_t2.job_path).status is (
        ConnectedReceiptVerificationStatus.VERIFIED
    )
    cf2_path = service.get_change_file(martin_t2.job_path)[0]
    cf2_before = _file_state(cf2_path)
    cf1 = parse_connected_change_file_any(cf1_path.read_bytes())
    cf2 = parse_connected_change_file_any(cf2_path.read_bytes())
    assert cf2.schema_version == "connected-change-file.v2"
    assert cf2.core.lineage.generation == 1
    assert cf2.core.lineage.parent_change_file_fingerprint == (
        cf1.change_file_fingerprint
    )
    assert cf2.core.lineage.parent_candidate_fingerprint == (
        martin_review.preview.compiled_candidate_fingerprint
    )
    assert cf2.originating_receipt.receipt.execution_role == "derivative"

    martin_t2_restored = tmp_path / "restored" / "martin-t2-source"
    service.recreate_original(martin_t2.job_path, martin_t2_restored)
    assert portable_tree(martin_t2_restored) == portable_tree(fixture.martin_root)

    sofia_t2 = apply_connected_change(
        change_file_path=cf2_path,
        source_root=fixture.sofia_root,
        output_parent=sofia_t2_output,
    )
    prior_t1_data = sofia_t1.final_result_path / "data"
    prior_t1_t2 = apply_connected_change(
        change_file_path=cf2_path,
        source_root=sofia_t1.final_result_path,
        output_parent=prior_t1_t2_output,
    )

    assert martin_t2.verified_artifacts is not None
    t2_commitment = martin_t2.verified_artifacts.organized_tree_commitment
    assert sofia_t2.organized_tree_commitment == t2_commitment
    assert prior_t1_t2.organized_tree_commitment == t2_commitment
    for result in (sofia_t2, prior_t1_t2):
        assert verify_connected_result(result.folder_run.result_root).status is (
            ConnectedReceiptVerificationStatus.VERIFIED
        )

    sofia_t2_restored = tmp_path / "restored" / "sofia-t2-source"
    restore_connected_result(sofia_t2.folder_run.result_root, sofia_t2_restored)
    assert portable_tree(sofia_t2_restored) == portable_tree(fixture.sofia_root)
    assert portable_tree(sofia_t2_restored) != portable_tree(fixture.martin_root)

    prior_t1_restored = tmp_path / "restored" / "prior-t1-data-source"
    restore_connected_result(
        prior_t1_t2.folder_run.result_root,
        prior_t1_restored,
    )
    assert portable_tree(prior_t1_restored) == portable_tree(prior_t1_data)

    assert tree_state(fixture.sofia_root) == sofia_source_before
    assert tree_state(fixture.martin_root) == martin_source_before
    assert _file_state(cf1_path) == cf1_before
    assert _file_state(cf2_path) == cf2_before


def _accept_review(
    service: FoldweaveReviewService,
    job: FolderRefactorJobV3,
    *,
    output_parent: Path,
    idempotency_key: str,
) -> FolderRefactorJobV3:
    assert job.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert job.preview is not None
    assert job.candidate_plan is not None
    return service.accept(
        job.job_path,
        expected_revision=job.revision,
        preview_fingerprint=job.preview.preview_fingerprint,
        candidate_fingerprint=job.preview.compiled_candidate_fingerprint,
        output_parent=output_parent,
        result_folder_name=job.candidate_plan.result_folder_name,
        idempotency_key=idempotency_key,
        channel="native_app",
    )


def _provider_for_child(child: FolderRefactorJobV3) -> _OneTurnDerivativeProvider:
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
                        f"collaborative-review/{Path(mapping.target_path).name}"
                    ),
                    rationale="Place this document in collaborative review.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )


def _member_paths(members: tuple[FolderPlanTreeMember, ...]) -> set[str]:
    return {member.relative_path for member in members}


def _file_state(path: Path) -> tuple[int, int, int, bytes]:
    metadata = path.stat()
    return (
        metadata.st_ino,
        metadata.st_mtime_ns,
        metadata.st_size,
        path.read_bytes(),
    )
