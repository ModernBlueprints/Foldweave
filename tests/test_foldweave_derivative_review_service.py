"""Integrated immutable receiver-parent to direct derivative-child regressions."""

from __future__ import annotations

import json
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from threading import Barrier
from typing import Literal

import pytest
from connected_change_fixtures import make_connected_change_fixture

from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    FolderRefactorJobV3,
    GptDerivativeJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.connected_change.service import (
    execute_prepared_foldweave_derivative,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeRevisionTurnInputV1,
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
)
from name_atlas.folder_refactor.live_planner_policy import DEFAULT_LIVE_REVISION_POLICY
from name_atlas.folder_refactor.live_planner_provider import (
    _revision_responses_request,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.transaction import FolderTransactionPaths
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService


class _ScriptedDerivativeProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(
        self,
        revision: FolderPlanRevisionV1 | None,
        *,
        error: Exception | None = None,
    ) -> None:
        self._revision = revision
        self._error = error
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
        if self._error is not None:
            raise self._error
        assert self._revision is not None
        return FolderRevisionProviderResponseV1(
            provider_kind="deterministic",
            call_id=f"derivative-service-{self.calls}",
            revision=self._revision,
        )


class _ScriptedFollowupProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(
        self,
        revision: FolderPlanRevisionV1 | None,
        *,
        error: Exception | None = None,
    ) -> None:
        self._revision = revision
        self._error = error
        self.calls = 0
        self.inputs: list[FolderPlannerRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.calls += 1
        self.inputs.append(turn_input)
        if self._error is not None:
            raise self._error
        assert self._revision is not None
        return FolderRevisionProviderResponseV1(
            provider_kind="deterministic",
            call_id=f"derivative-followup-{self.calls}",
            revision=self._revision,
        )


class _SurfaceProviderFactory:
    """Create schema-correct providers for browser and CLI routing tests."""

    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self, service: FoldweaveReviewService) -> None:
        self._service = service
        self.calls = 0

    def initial_provider(self) -> object:
        raise AssertionError("derivative routing must not request an initial provider")

    def revision_provider(self) -> object:
        raise AssertionError("derivative routing must not request a root provider")

    def derivative_revision_provider(
        self,
        job_path: Path,
    ) -> _ScriptedDerivativeProvider | _ScriptedFollowupProvider:
        self.calls += 1
        job = self._service.status(job_path)
        assert isinstance(job.authority, GptDerivativeJobAuthorityV3)
        if job.authority.authority_state == "awaiting_model_response":
            return _provider_for_child(job)
        assert job.preview is not None
        assert job.candidate_plan is not None
        mapping = next(
            item for item in job.candidate_plan.file_mappings if not item.protected
        )
        return _ScriptedFollowupProvider(
            FolderPlanRevisionV1(
                base_candidate_fingerprint=job.preview.compiled_candidate_fingerprint,
                entries=(
                    FolderPlanRevisionEntryV1(
                        file_id=mapping.file_id,
                        replacement_target_path=(
                            f"surface-followup/{Path(mapping.target_path).name}"
                        ),
                        rationale="Exercise the second routed derivative turn.",
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            )
        )


@dataclass(frozen=True, slots=True)
class _ReceiverParentContext:
    service: FoldweaveReviewService
    parent: FolderRefactorJobV3
    output_parent: Path
    child_output: Path
    change_file_path: Path


def test_create_or_resume_derivative_child_is_parent_immutable_and_concurrent(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    barrier = Barrier(2)

    def create() -> FolderRefactorJobV3:
        barrier.wait(timeout=5)
        return context.service.create_or_resume_derivative_child(
            context.parent.job_path,
            output_parent=context.child_output,
            instruction="Move one document into a collaborative review folder.",
            idempotency_key="derivative-create-once",
            provider_kind="deterministic",
            channel="native_app",
        )

    with ThreadPoolExecutor(max_workers=2) as executor:
        results = tuple(
            future.result(timeout=15)
            for future in (executor.submit(create), executor.submit(create))
        )

    assert results[0] == results[1]
    child = results[0]
    assert child.lifecycle is FolderJobLifecycleV3.REVISING
    assert child.revision == 0
    assert child.candidate_plan is None
    assert isinstance(child.authority, GptDerivativeJobAuthorityV3)
    assert child.authority.authority_state == "awaiting_model_response"
    assert child.authority.pending_direct_revision is not None
    assert child.authority.pending_direct_revision.response_turn == 1
    assert context.parent.job_path.read_bytes() == parent_before

    derivative_jobs = tuple(
        path
        for path in context.parent.job_path.parent.glob("*.json")
        if path.name not in {"origin.json", "receiver.json"}
    )
    assert derivative_jobs == (child.job_path,)

    with pytest.raises(
        FolderJobV3IdempotencyConflict,
        match="another exact request",
    ):
        context.service.create_or_resume_derivative_child(
            context.parent.job_path,
            output_parent=context.child_output,
            instruction="Conflicting instruction for the same retry key.",
            idempotency_key="derivative-create-once",
            provider_kind="deterministic",
            channel="native_app",
        )
    assert context.parent.job_path.read_bytes() == parent_before


@pytest.mark.anyio
async def test_direct_derivative_turn_executes_only_after_exact_acceptance(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    child = _create_child(context, key="derivative-success")
    provider = _provider_for_child(child)

    reviewed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )

    assert provider.calls == 1
    assert provider.inputs[0] == child.authority.pending_direct_revision
    assert reviewed.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert reviewed.proposal_revision == 1
    assert reviewed.candidate_plan is not None
    assert reviewed.preview is not None
    assert reviewed.preview.proposal_basis == "gpt_derivative"
    assert isinstance(reviewed.authority, GptDerivativeJobAuthorityV3)
    assert reviewed.authority.authority_state == "completed"
    assert reviewed.authority.evidence_ledger is not None
    assert reviewed.authority.evidence_ledger.planning_basis == "derivative"
    assert reviewed.authority.execution_origin is not None
    assert reviewed.authority.execution_origin.kind == "gpt_revised_from_change_file"
    assert context.parent.job_path.read_bytes() == parent_before

    forbidden_retry = _ScriptedDerivativeProvider(
        None,
        error=AssertionError("completed derivative retry must be provider-free"),
    )
    assert (
        await context.service.submit_direct_derivative_revision(
            reviewed.job_path,
            provider=forbidden_retry,
        )
        == reviewed
    )
    assert forbidden_retry.calls == 0

    assert tuple(context.child_output.iterdir()) == ()
    verified = context.service.accept(
        reviewed.job_path,
        expected_revision=reviewed.revision,
        preview_fingerprint=reviewed.preview.preview_fingerprint,
        candidate_fingerprint=reviewed.preview.compiled_candidate_fingerprint,
        output_parent=context.child_output,
        result_folder_name=reviewed.candidate_plan.result_folder_name,
        idempotency_key="derivative-accept-v2",
        channel="native_app",
    )

    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert verified.execution_authorization is not None
    assert verified.destination_reservation is not None
    assert verified.pending_result_path is None
    assert verified.final_result_path is not None
    assert verified.final_result_path.is_dir()
    assert context.parent.job_path.read_bytes() == parent_before
    change_file_path, change_file_fingerprint, receipt_fingerprint = (
        context.service.get_change_file(verified.job_path)
    )
    change_file = parse_connected_change_file_any(change_file_path.read_bytes())
    assert change_file.schema_version == "connected-change-file.v2"
    assert change_file.change_file_fingerprint == change_file_fingerprint
    assert change_file.originating_receipt.receipt_fingerprint == receipt_fingerprint
    assert change_file.core.lineage.parent_change_file_fingerprint == (
        reviewed.authority.parent_binding.imported_change_file_fingerprint
    )
    verification = context.service.verify_result(verified.job_path)
    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert verification.job_id == verified.job_id

    assert (
        context.service.accept(
            reviewed.job_path,
            expected_revision=reviewed.revision,
            preview_fingerprint=reviewed.preview.preview_fingerprint,
            candidate_fingerprint=reviewed.preview.compiled_candidate_fingerprint,
            output_parent=context.child_output,
            result_folder_name=reviewed.candidate_plan.result_folder_name,
            idempotency_key="derivative-accept-v2",
            channel="native_app",
        )
        == verified
    )


@pytest.mark.anyio
async def test_direct_derivative_supports_second_revision_and_exact_retry(
    tmp_path: Path,
) -> None:
    """A direct child can use its second bounded turn without losing lineage."""

    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    child = _create_child(context, key="derivative-second-turn")
    first = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=_provider_for_child(child),
    )
    assert first.preview is not None
    assert first.candidate_plan is not None
    editable = next(
        item for item in first.candidate_plan.file_mappings if not item.protected
    )
    followup = _ScriptedFollowupProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=first.preview.compiled_candidate_fingerprint,
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=editable.file_id,
                    replacement_target_path=(
                        f"second-review/{Path(editable.target_path).name}"
                    ),
                    rationale="Apply the second bounded derivative instruction.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )
    request = {
        "expected_revision": first.revision,
        "preview_fingerprint": first.preview.preview_fingerprint,
        "candidate_fingerprint": first.preview.compiled_candidate_fingerprint,
        "instruction": "Move the reviewed document into second review.",
        "idempotency_key": "derivative-second-turn-revision",
    }

    second = await context.service.revise(
        first.job_path,
        **request,
        provider=followup,
    )

    assert followup.calls == 1
    assert followup.inputs[0].schema_version == (
        "folder-planner-revision-turn-input.v1"
    )
    assert second.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert second.proposal_revision == 2
    assert second.revision_attempt_count == 2
    assert isinstance(second.authority, GptDerivativeJobAuthorityV3)
    assert second.authority.authority_state == "completed"
    assert second.authority.evidence_ledger is not None
    assert second.authority.evidence_ledger.user_revision_count == 2
    assert second.authority.parent_binding == first.authority.parent_binding
    assert context.parent.job_path.read_bytes() == parent_before

    first_input = child.authority.pending_direct_revision
    assert first_input is not None
    serialized_first = json.loads(
        _revision_responses_request(
            first_input,
            policy=DEFAULT_LIVE_REVISION_POLICY,
        )["input"][0]["content"][0]["text"]
    )
    serialized_followup = json.loads(
        _revision_responses_request(
            followup.inputs[0],
            policy=DEFAULT_LIVE_REVISION_POLICY,
        )["input"][0]["content"][0]["text"]
    )
    assert serialized_first == first_input.model_dump(mode="json")
    assert serialized_followup == followup.inputs[0].model_dump(mode="json")
    assert serialized_first["schema_version"] == (
        "folder-derivative-revision-turn-input.v1"
    )
    assert serialized_followup["schema_version"] == (
        "folder-planner-revision-turn-input.v1"
    )

    forbidden_retry = _ScriptedFollowupProvider(
        None,
        error=AssertionError("terminal direct retry must not call the provider"),
    )
    assert (
        await context.service.revise(
            first.job_path,
            **request,
            provider=forbidden_retry,
        )
        == second
    )
    assert forbidden_retry.calls == 0


@pytest.mark.anyio
async def test_derivative_provider_failure_preserves_review_without_parent_mutation(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    child = _create_child(context, key="derivative-provider-failure")
    provider = _ScriptedDerivativeProvider(
        None,
        error=RuntimeError("provider unavailable"),
    )

    failed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )

    assert provider.calls == 1
    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert failed.blocker_code is None
    assert failed.revision_failure is not None
    assert failed.revision_failure.code == "derivative_revision_failed"
    assert isinstance(failed.authority, GptDerivativeJobAuthorityV3)
    assert failed.authority.authority_state == "failed"
    assert failed.authority.failure is not None
    assert failed.authority.evidence_ledger is None
    assert failed.candidate_plan == failed.authority.parent_binding.parent_candidate
    assert failed.preview is not None
    assert failed.preview.proposal_basis == "imported_change_file"
    assert context.parent.job_path.read_bytes() == parent_before

    retried = await context.service.submit_direct_derivative_revision(
        failed.job_path,
        provider=_ScriptedDerivativeProvider(
            None,
            error=AssertionError("must not run"),
        ),
    )
    assert retried == failed

    kept = context.service.keep_previous_proposal(
        failed.job_path,
        expected_revision=failed.revision,
        preview_fingerprint=failed.preview.preview_fingerprint,
        candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
        idempotency_key="keep-after-derivative-provider-failure",
    )
    assert kept == context.parent
    preserved_child = context.service.status(failed.job_path)
    assert preserved_child.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert preserved_child.authority == failed.authority


@pytest.mark.anyio
async def test_derivative_mechanical_failure_allows_an_exact_sibling_retry(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    child = _create_child(context, key="derivative-mechanical-failure")
    assert isinstance(child.authority, GptDerivativeJobAuthorityV3)
    parent = child.authority.parent_binding
    mapping = next(
        item for item in parent.parent_candidate.file_mappings if not item.protected
    )
    provider = _ScriptedDerivativeProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=parent.parent_candidate_fingerprint,
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=mapping.file_id,
                    replacement_target_path=mapping.target_path,
                    rationale="Return the same path to trigger the no-change check.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )

    failed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )

    assert provider.calls == 1
    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert failed.blocker_code is None
    assert failed.revision_failure is not None
    assert failed.revision_failure.code == "revision_no_change"
    assert isinstance(failed.authority, GptDerivativeJobAuthorityV3)
    assert failed.authority.authority_state == "failed"
    assert failed.authority.evidence_ledger is None
    assert failed.preview is not None
    sibling = context.service.create_or_resume_derivative_child(
        context.parent.job_path,
        output_parent=context.child_output,
        instruction="Try another change after the rejected first proposal.",
        idempotency_key="derivative-mechanical-sibling",
        provider_kind="deterministic",
        channel="native_app",
    )
    retried = await context.service.submit_direct_derivative_revision(
        sibling.job_path,
        provider=_provider_for_child(sibling),
    )
    assert retried.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert retried.job_id != failed.job_id
    assert context.parent.job_path.read_bytes() == parent_before


def test_interrupted_derivative_recovery_never_retries_provider(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="derivative-interrupted")

    recovered = context.service.recover_interrupted_direct_derivative(child.job_path)

    assert recovered.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert recovered.blocker_code is None
    assert recovered.revision_failure is not None
    assert recovered.revision_failure.code == "derivative_provider_interrupted"
    assert isinstance(recovered.authority, GptDerivativeJobAuthorityV3)
    assert recovered.authority.authority_state == "failed"
    assert recovered.authority.failure is not None


@pytest.mark.anyio
@pytest.mark.parametrize("changed_input", ["source", "change_file"])
async def test_derivative_input_staleness_blocks_before_provider(
    tmp_path: Path,
    changed_input: str,
) -> None:
    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    child = _create_child(context, key=f"derivative-stale-{changed_input}")
    provider = _provider_for_child(child)
    if changed_input == "source":
        source_file = context.parent.source_root / "incoming" / "cover-art.png"
        source_file.write_bytes(source_file.read_bytes() + b"changed")
    else:
        metadata = context.change_file_path.stat()
        os.utime(
            context.change_file_path,
            ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 1_000_000),
        )

    failed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )

    assert provider.calls == 0
    assert failed.lifecycle is FolderJobLifecycleV3.STALE
    assert failed.staleness is not None
    assert failed.staleness.code == (
        "source_changed" if changed_input == "source" else "change_file_changed"
    )
    assert failed.execution_authorization is None
    assert failed.destination_reservation is None
    assert failed.pending_result_path is None
    assert context.parent.job_path.read_bytes() == parent_before


@pytest.mark.anyio
async def test_resume_authorized_derivative_execution_uses_bound_finalizer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="derivative-resume-barrier")
    reviewed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=_provider_for_child(child),
    )
    assert reviewed.preview is not None
    assert reviewed.candidate_plan is not None

    with monkeypatch.context() as bypass:
        bypass.setattr(
            context.service,
            "_execute_locked",
            lambda _writer, job, *, progress_callback: job,
        )
        executing = context.service.accept(
            reviewed.job_path,
            expected_revision=reviewed.revision,
            preview_fingerprint=reviewed.preview.preview_fingerprint,
            candidate_fingerprint=reviewed.preview.compiled_candidate_fingerprint,
            output_parent=context.child_output,
            result_folder_name=reviewed.candidate_plan.result_folder_name,
            idempotency_key="derivative-resume-barrier-accept",
            channel="native_app",
        )
    assert executing.lifecycle is FolderJobLifecycleV3.EXECUTING
    assert tuple(context.child_output.iterdir()) == ()

    verified = context.service.resume_authorized_execution(executing.job_path)
    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert verified.execution_authorization == executing.execution_authorization
    assert verified.final_result_path is not None
    assert verified.final_result_path.is_dir()
    change_file_path = context.service.get_change_file(verified.job_path)[0]
    assert parse_connected_change_file_any(
        change_file_path.read_bytes()
    ).schema_version == ("connected-change-file.v2")


@pytest.mark.anyio
async def test_resume_derivative_rejects_changed_parent_without_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="derivative-resume-stale")
    reviewed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=_provider_for_child(child),
    )
    assert reviewed.preview is not None
    assert reviewed.candidate_plan is not None
    with monkeypatch.context() as bypass:
        bypass.setattr(
            context.service,
            "_execute_locked",
            lambda _writer, job, *, progress_callback: job,
        )
        executing = context.service.accept(
            reviewed.job_path,
            expected_revision=reviewed.revision,
            preview_fingerprint=reviewed.preview.preview_fingerprint,
            candidate_fingerprint=reviewed.preview.compiled_candidate_fingerprint,
            output_parent=context.child_output,
            result_folder_name=reviewed.candidate_plan.result_folder_name,
            idempotency_key="derivative-resume-stale-accept",
            channel="native_app",
        )
    metadata = context.change_file_path.stat()
    os.utime(
        context.change_file_path,
        ns=(metadata.st_atime_ns, metadata.st_mtime_ns + 1_000_000),
    )

    stale = context.service.resume_authorized_execution(executing.job_path)

    assert stale.lifecycle is FolderJobLifecycleV3.STALE
    assert stale.staleness is not None
    assert stale.staleness.code == "change_file_changed"
    assert context.service.status(executing.job_path) == stale
    assert tuple(context.child_output.iterdir()) == ()


@pytest.mark.anyio
async def test_derivative_child_survives_parent_acceptance_and_service_restart(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="derivative-parent-branch-order")
    parent_snapshot = child.authority.parent_binding

    parent_verified = _accept_parent_unchanged(
        context,
        key="derivative-parent-branch-order-accept",
    )
    assert parent_verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert parent_verified.revision > parent_snapshot.parent_job_revision

    restarted = FoldweaveReviewService()
    provider = _provider_for_child(child)
    reviewed = await restarted.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )

    assert provider.calls == 1
    assert reviewed.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert reviewed.preview is not None
    assert reviewed.candidate_plan is not None
    verified = restarted.accept(
        reviewed.job_path,
        expected_revision=reviewed.revision,
        preview_fingerprint=reviewed.preview.preview_fingerprint,
        candidate_fingerprint=reviewed.preview.compiled_candidate_fingerprint,
        output_parent=context.child_output,
        result_folder_name=reviewed.candidate_plan.result_folder_name,
        idempotency_key="derivative-child-after-parent-accept",
        channel="native_app",
    )
    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert restarted.status(context.parent.job_path) == parent_verified


@pytest.mark.anyio
async def test_derivative_child_revalidates_source_after_parent_acceptance(
    tmp_path: Path,
) -> None:
    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="derivative-parent-advanced-stale-source")
    parent_verified = _accept_parent_unchanged(
        context,
        key="derivative-parent-advanced-stale-source-accept",
    )
    source_file = context.parent.source_root / "incoming" / "cover-art.png"
    source_file.write_bytes(source_file.read_bytes() + b"changed-after-parent-accept")
    provider = _provider_for_child(child)

    failed = await FoldweaveReviewService().submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )

    assert provider.calls == 0
    assert failed.lifecycle is FolderJobLifecycleV3.STALE
    assert failed.execution_authorization is None
    assert failed.final_result_path is None
    assert FoldweaveReviewService().status(context.parent.job_path) == parent_verified
    assert tuple(context.child_output.iterdir()) == ()


@pytest.mark.anyio
async def test_browser_receiver_send_changes_routes_both_derivative_turns(
    tmp_path: Path,
) -> None:
    """The native/browser facade forks T2 and keeps the parent unchanged."""

    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    assert context.parent.preview is not None
    factory = _SurfaceProviderFactory(context.service)
    browser = FoldweaveBrowserReviewService(
        job_path=context.parent.job_path,
        service=context.service,
        provider_factory=factory,
        review_channel="native_app",
    )
    first = await browser.revise_review(
        job_id=context.parent.job_id,
        expected_revision=context.parent.revision,
        preview_fingerprint=context.parent.preview.preview_fingerprint,
        candidate_fingerprint=context.parent.preview.compiled_candidate_fingerprint,
        instruction="Build Martin's first derivative proposal.",
        idempotency_key="browser-derivative-first",
    )
    assert first.proposal_revision == 1
    assert browser.job_path != context.parent.job_path
    assert factory.calls == 1

    second = await browser.revise_review(
        job_id=first.job_id,
        expected_revision=first.job_revision,
        preview_fingerprint=first.preview_fingerprint,
        candidate_fingerprint=first.candidate_fingerprint,
        instruction="Refine Martin's derivative proposal.",
        idempotency_key="browser-derivative-second",
    )
    assert second.proposal_revision == 2
    assert factory.calls == 2
    assert context.parent.job_path.read_bytes() == parent_before


def test_cli_receiver_revise_routes_to_derivative_child(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The CLI forks the receiver parent instead of revising it in place."""

    context = _build_receiver_parent(tmp_path)
    parent_before = context.parent.job_path.read_bytes()
    factory = _SurfaceProviderFactory(context.service)

    class _CliFactory:
        provider_kind = factory.provider_kind

        def __init__(self, **_kwargs: object) -> None:
            pass

        def derivative_revision_provider(
            self,
            job_path: Path,
        ) -> _ScriptedDerivativeProvider | _ScriptedFollowupProvider:
            return factory.derivative_revision_provider(job_path)

        def revision_provider(self) -> object:
            return factory.revision_provider()

    import name_atlas.foldweave_provider_factory as provider_module
    import name_atlas.foldweave_review_cli as cli_module

    monkeypatch.setattr(provider_module, "FoldweaveDirectProviderFactory", _CliFactory)
    monkeypatch.setattr(
        cli_module,
        "resolve_foldweave_budget_authority",
        lambda **_kwargs: object(),
    )
    assert (
        cli_module.run_revise(
            (
                str(context.parent.job_path),
                "--instruction",
                "Build Martin's CLI derivative proposal.",
                "--idempotency-key",
                "cli-derivative-first",
            ),
            environ={},
        )
        == 0
    )
    child_paths = tuple(
        path
        for path in context.parent.job_path.parent.glob("*.json")
        if path.name not in {"origin.json", "receiver.json"}
    )
    assert len(child_paths) == 1
    child = context.service.status(child_paths[0])
    assert child.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert child.proposal_revision == 1
    assert factory.calls == 1
    assert (
        cli_module.run_revise(
            (
                str(child.job_path),
                "--instruction",
                "Refine Martin's CLI derivative proposal.",
                "--idempotency-key",
                "cli-derivative-second",
            ),
            environ={},
        )
        == 0
    )
    second = context.service.status(child.job_path)
    assert second.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert second.proposal_revision == 2
    assert factory.calls == 2
    assert context.parent.job_path.read_bytes() == parent_before


@pytest.mark.anyio
async def test_promoted_derivative_recovery_precedes_mutable_input_checks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="derivative-promoted-recovery")
    reviewed = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=_provider_for_child(child),
    )
    assert reviewed.preview is not None
    assert reviewed.candidate_plan is not None

    def promote_without_final_checkpoint(
        _writer: object,
        job: FolderRefactorJobV3,
        *,
        progress_callback: object,
    ) -> FolderRefactorJobV3:
        assert progress_callback is None
        assert job.pending_result_path is not None
        assert job.final_result_path is not None
        prepared = context.service._prepare_derivative_execution(job)
        result = execute_prepared_foldweave_derivative(
            prepared=prepared,
            output_parent=job.output_parent,
            job_id=job.job_id,
            transaction_paths=FolderTransactionPaths(
                job_id=job.job_id,
                pending_root=job.pending_result_path,
                final_root=job.final_result_path,
            ),
        )
        assert result.folder_run.result_root == job.final_result_path
        assert not job.pending_result_path.exists()
        return job

    with monkeypatch.context() as lost_checkpoint:
        lost_checkpoint.setattr(
            context.service,
            "_execute_locked",
            promote_without_final_checkpoint,
        )
        executing = context.service.accept(
            reviewed.job_path,
            expected_revision=reviewed.revision,
            preview_fingerprint=reviewed.preview.preview_fingerprint,
            candidate_fingerprint=reviewed.preview.compiled_candidate_fingerprint,
            output_parent=context.child_output,
            result_folder_name=reviewed.candidate_plan.result_folder_name,
            idempotency_key="derivative-promoted-recovery-accept",
            channel="native_app",
        )
    assert executing.lifecycle is FolderJobLifecycleV3.EXECUTING
    assert executing.final_result_path is not None
    assert executing.final_result_path.is_dir()

    _accept_parent_unchanged(
        context,
        key="derivative-promoted-parent-accept",
    )
    source_file = context.parent.source_root / "incoming" / "cover-art.png"
    source_file.write_bytes(source_file.read_bytes() + b"changed-after-promotion")

    recovered = FoldweaveReviewService().resume_authorized_execution(executing.job_path)

    assert recovered.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert recovered.pending_result_path is None
    assert recovered.final_result_path == executing.final_result_path
    assert recovered.verified_artifacts is not None
    assert recovered.execution_authorization == executing.execution_authorization


def _build_receiver_parent(tmp_path: Path) -> _ReceiverParentContext:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    service = FoldweaveReviewService()
    jobs = (tmp_path / "jobs").resolve()
    origin_output = (tmp_path / "origin-output").resolve()
    receiver_output = (tmp_path / "receiver-output").resolve()
    child_output = (tmp_path / "child-output").resolve()
    for directory in (jobs, origin_output, receiver_output, child_output):
        directory.mkdir(parents=True)
    origin = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=jobs / "origin.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="derivative-service-origin",
    )
    assert origin.preview is not None
    verified = service.accept(
        origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=origin_output,
        result_folder_name=fixture.result_name,
        idempotency_key="derivative-service-origin-accept",
        channel="native_app",
    )
    change_file_path = service.get_change_file(verified.job_path)[0]
    parent = service.prepare_application_review(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=jobs / "receiver.json",
        idempotency_key="derivative-service-parent",
    )
    assert parent.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert isinstance(parent.authority, CapsuleAppliedJobAuthorityV2)
    return _ReceiverParentContext(
        service=service,
        parent=parent,
        output_parent=receiver_output,
        child_output=child_output,
        change_file_path=change_file_path,
    )


def _accept_parent_unchanged(
    context: _ReceiverParentContext,
    *,
    key: str,
) -> FolderRefactorJobV3:
    parent = context.service.status(context.parent.job_path)
    assert parent.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert parent.preview is not None
    assert parent.candidate_plan is not None
    return context.service.accept(
        parent.job_path,
        expected_revision=parent.revision,
        preview_fingerprint=parent.preview.preview_fingerprint,
        candidate_fingerprint=parent.preview.compiled_candidate_fingerprint,
        output_parent=context.output_parent,
        result_folder_name=parent.candidate_plan.result_folder_name,
        idempotency_key=key,
        channel="native_app",
    )


def _create_child(
    context: _ReceiverParentContext,
    *,
    key: str,
) -> FolderRefactorJobV3:
    return context.service.create_or_resume_derivative_child(
        context.parent.job_path,
        output_parent=context.child_output,
        instruction="Move one document into a collaborative review folder.",
        idempotency_key=key,
        provider_kind="deterministic",
        channel="native_app",
    )


def _provider_for_child(
    child: FolderRefactorJobV3,
) -> _ScriptedDerivativeProvider:
    assert isinstance(child.authority, GptDerivativeJobAuthorityV3)
    parent = child.authority.parent_binding
    mapping = next(
        item for item in parent.parent_candidate.file_mappings if not item.protected
    )
    return _ScriptedDerivativeProvider(
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
