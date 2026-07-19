"""Process-boundary recovery for Foldweave review-era jobs."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Literal

import pytest
from connected_change_fixtures import make_connected_change_fixture, tree_state

from name_atlas.folder_app import (
    FolderReviewHandle,
    FolderWebLifecycle,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    FolderRefactorJobV3Writer,
    GptPlannedJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
    FoldweaveReviewServiceError,
)
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderPlannerRevisionTurnInputV1,
    FolderRevisionProviderResponseV1,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    FolderProviderResponse,
    PlannerInventoryFile,
    ProviderToolResponse,
    RequestClarificationCall,
    SubmitPlanCall,
)
from name_atlas.folder_refactor.planner_provider import (
    DETERMINISTIC_DEVELOPMENT_REQUEST,
    DeterministicDevelopmentPlannerProvider,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import request_fingerprint
from name_atlas.foldweave_web_service import FoldweaveBrowserReviewService

QUESTION = "Which project section should be treated as the primary handoff?"
ANSWER = "Use the reviewed project section."


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _HangingInitialProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.inputs: list[FolderPlannerTurnInput] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        self.inputs.append(turn_input)
        self.started.set()
        await asyncio.Event().wait()
        raise AssertionError("Unreachable provider continuation.")


class _NeverCalledInitialProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self) -> None:
        self.inputs: list[FolderPlannerTurnInput] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        self.inputs.append(turn_input)
        raise AssertionError("Recovery must not repeat the provider turn.")


class _NeverCalledRevisionProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self) -> None:
        self.inputs: list[FolderPlannerRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.inputs.append(turn_input)
        raise AssertionError("Recovery must not repeat the revision provider turn.")


class _CountingProviderFactory:
    def __init__(self, initial_provider: object | None = None) -> None:
        self.initial_count = 0
        self.revision_count = 0
        self.initial_providers: list[object] = []
        self.revision_providers: list[_NeverCalledRevisionProvider] = []
        self._initial_provider = initial_provider

    def initial_provider(self):
        self.initial_count += 1
        provider = self._initial_provider or _NeverCalledInitialProvider()
        self.initial_providers.append(provider)
        return provider

    def revision_provider(self) -> _NeverCalledRevisionProvider:
        self.revision_count += 1
        provider = _NeverCalledRevisionProvider()
        self.revision_providers.append(provider)
        return provider


class _ClarifyingProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self) -> None:
        self.inputs: list[FolderPlannerTurnInput] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        self.inputs.append(turn_input)
        if turn_input.clarification_answer is None:
            return ProviderToolResponse(
                provider_kind="deterministic",
                observable_output_items=(
                    {
                        "type": "restart_clarification_question",
                        "response_turn": turn_input.response_turn,
                    },
                ),
                tool_calls=(
                    RequestClarificationCall(
                        call_id="restart-clarification-question",
                        question=QUESTION,
                        missing_facts=("primary_handoff_section",),
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            )
        assert turn_input.clarification_question == QUESTION
        assert turn_input.clarification_answer == ANSWER
        return ProviderToolResponse(
            provider_kind="deterministic",
            observable_output_items=(
                {
                    "type": "restart_clarified_plan",
                    "response_turn": turn_input.response_turn,
                },
            ),
            tool_calls=(
                SubmitPlanCall(
                    call_id="restart-clarified-plan",
                    plan=_complete_plan(turn_input),
                ),
            ),
        )


class _ClarifyingProviderFactory(_CountingProviderFactory):
    def initial_provider(self) -> _ClarifyingProvider:
        self.initial_count += 1
        provider = _ClarifyingProvider()
        self.initial_providers.append(provider)
        return provider


class _HangingRevisionProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.inputs: list[FolderPlannerRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.inputs.append(turn_input)
        self.started.set()
        await asyncio.Event().wait()
        raise AssertionError("Unreachable revision continuation.")


def _complete_plan(turn_input: FolderPlannerTurnInput) -> FolderPlan:
    initial = turn_input.evidence_ledger.initial_evidence
    assert isinstance(initial, dict)
    raw_files = initial.get("files")
    assert isinstance(raw_files, list)
    files = tuple(
        PlannerInventoryFile.model_validate(item, strict=True) for item in raw_files
    )
    return FolderPlan(
        source_commitment=turn_input.source_commitment,
        request_fingerprint=request_fingerprint(turn_input.request),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=turn_input.evidence_ledger.evidence_fingerprint,
        result_folder_name="foldweave-clarified-copy",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=f"clarified/{item.relative_path}",
                rationale="Apply the one durable clarification answer.",
                evidence_ids=("initial_inventory",),
            )
            for item in files
            if not item.protected
        ),
        exclusions=(),
    )


@pytest.mark.anyio
async def test_interrupted_initial_planning_blocks_without_duplicate_provider_turn(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "interrupted-planning.json"
    source_before = tree_state(fixture.sofia_root)
    first_provider = _HangingInitialProvider()
    review_service = FoldweaveReviewService()

    task = asyncio.create_task(
        review_service.prepare_planned_origin_review(
            source_root=fixture.sofia_root,
            output_parent=output,
            job_path=job_path,
            request=DETERMINISTIC_DEVELOPMENT_REQUEST,
            idempotency_key="restart-interrupted-initial",
            provider=first_provider,
        )
    )
    await asyncio.wait_for(first_provider.started.wait(), timeout=5)
    interrupted = FolderRefactorJobV3Store(job_path).inspect()
    assert interrupted.lifecycle is FolderJobLifecycleV3.PLANNING
    assert isinstance(interrupted.authority, GptPlannedJobAuthorityV3)
    progress = interrupted.authority.planner_checkpoint.progress
    assert progress is not None
    assert progress.pending_response_turn == 1
    assert len(first_provider.inputs) == 1
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    resume_provider = _NeverCalledInitialProvider()
    factory = _CountingProviderFactory(resume_provider)
    restarted = FoldweaveBrowserReviewService(
        job_path=job_path,
        provider_factory=factory,
    )
    checkpoint = restarted.rehydrate_web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle is FolderWebLifecycle.PLANNING
    assert checkpoint.resume_required
    assert factory.initial_count == 0

    with pytest.raises(ValueError, match="provider_turn_incomplete"):
        await restarted.resume_existing_job()

    blocked = FolderRefactorJobV3Store(job_path).inspect()
    assert blocked.lifecycle is FolderJobLifecycleV3.BLOCKED
    assert blocked.blocker_code == "provider_turn_incomplete"
    assert factory.initial_count == 0
    assert resume_provider.inputs == []
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.sofia_root) == source_before

    blocked_bytes = job_path.read_bytes()
    with pytest.raises(ValueError, match="provider_turn_incomplete"):
        await restarted.resume_existing_job()
    assert factory.initial_count == 0
    assert resume_provider.inputs == []
    assert job_path.read_bytes() == blocked_bytes
    assert tuple(output.iterdir()) == ()


@pytest.mark.anyio
async def test_clarification_rehydrates_and_continues_without_reasking(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "awaiting-clarification.json"
    source_before = tree_state(fixture.sofia_root)
    first_provider = _ClarifyingProvider()
    review_service = FoldweaveReviewService()

    waiting = await review_service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=job_path,
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="restart-clarification-initial",
        provider=first_provider,
    )
    assert waiting.lifecycle is FolderJobLifecycleV3.AWAITING_CLARIFICATION
    assert len(first_provider.inputs) == 1
    waiting_bytes = job_path.read_bytes()

    factory = _ClarifyingProviderFactory()
    restarted = FoldweaveBrowserReviewService(
        job_path=job_path,
        provider_factory=factory,
    )
    checkpoint = restarted.rehydrate_web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle is FolderWebLifecycle.AWAITING_CLARIFICATION
    assert checkpoint.clarification is not None
    assert checkpoint.clarification.question == QUESTION
    assert checkpoint.clarification.continuation_token == waiting.job_id
    assert factory.initial_count == 0
    assert job_path.read_bytes() == waiting_bytes

    review = await restarted.continue_after_clarification(
        continuation_token=waiting.job_id,
        answer=ANSWER,
    )
    assert isinstance(review, FolderReviewHandle)
    assert factory.initial_count == 1
    resumed_provider = factory.initial_providers[0]
    assert isinstance(resumed_provider, _ClarifyingProvider)
    assert len(resumed_provider.inputs) == 1
    resumed_input = resumed_provider.inputs[0]
    assert resumed_input.response_turn == 2
    assert resumed_input.clarification_question == QUESTION
    assert resumed_input.clarification_answer == ANSWER
    assert len(resumed_input.prior_turns) == 1
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.sofia_root) == source_before

    reviewing_bytes = job_path.read_bytes()
    with pytest.raises(
        FoldweaveReviewServiceError,
        match="clarification_not_active",
    ):
        await restarted.continue_after_clarification(
            continuation_token=waiting.job_id,
            answer=ANSWER,
        )
    assert factory.initial_count == 1
    assert job_path.read_bytes() == reviewing_bytes
    assert tuple(output.iterdir()) == ()


@pytest.mark.anyio
async def test_interrupted_revision_preserves_preview_and_exact_retry_is_provider_free(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "interrupted-revision.json"
    source_before = tree_state(fixture.sofia_root)
    review_service = FoldweaveReviewService()
    reviewing = await review_service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=job_path,
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="restart-revision-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.candidate_plan is not None
    assert reviewing.preview is not None
    instruction = "Place the handoff material in a reviewed section."
    revision_key = "restart-interrupted-revision"
    provider = _HangingRevisionProvider()

    task = asyncio.create_task(
        review_service.revise(
            job_path,
            expected_revision=reviewing.revision,
            preview_fingerprint=reviewing.preview.preview_fingerprint,
            candidate_fingerprint=(reviewing.preview.compiled_candidate_fingerprint),
            instruction=instruction,
            idempotency_key=revision_key,
            provider=provider,
        )
    )
    await asyncio.wait_for(provider.started.wait(), timeout=5)
    interrupted = FolderRefactorJobV3Store(job_path).inspect()
    assert interrupted.lifecycle is FolderJobLifecycleV3.REVISING
    assert interrupted.candidate_plan == reviewing.candidate_plan
    assert interrupted.preview == reviewing.preview
    assert len(provider.inputs) == 1
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    factory = _CountingProviderFactory()
    restarted = FoldweaveBrowserReviewService(
        job_path=job_path,
        provider_factory=factory,
        review_channel="native_app",
    )
    checkpoint = restarted.rehydrate_web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle is FolderWebLifecycle.REVIEWING
    assert checkpoint.review is not None
    recovered = FolderRefactorJobV3Store(job_path).inspect()
    assert recovered.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert recovered.revision_failure is not None
    assert recovered.revision_failure.code == "revision_provider_interrupted"
    assert recovered.candidate_plan == reviewing.candidate_plan
    assert recovered.preview is not None
    assert recovered.preview.current_tree_members == (
        reviewing.preview.current_tree_members
    )
    assert recovered.preview.proposed_tree_members == (
        reviewing.preview.proposed_tree_members
    )
    assert tuple(output.iterdir()) == ()
    assert factory.initial_count == 0
    assert factory.revision_count == 0

    exact_retry = await restarted.revise_review(
        job_id=recovered.job_id,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction=instruction,
        idempotency_key=revision_key,
    )
    assert exact_retry.job_revision == recovered.revision
    assert exact_retry.preview_fingerprint == recovered.preview.preview_fingerprint
    assert factory.revision_count == 0

    kept = await restarted.keep_previous_review(
        job_id=recovered.job_id,
        expected_revision=recovered.revision,
        preview_fingerprint=recovered.preview.preview_fingerprint,
        candidate_fingerprint=recovered.preview.compiled_candidate_fingerprint,
        idempotency_key="restart-keep-prior-preview",
    )
    verified = await restarted.accept_review(
        job_id=kept.job_id,
        expected_revision=kept.job_revision,
        preview_fingerprint=kept.preview_fingerprint,
        candidate_fingerprint=kept.candidate_fingerprint,
        output_parent=kept.output_parent,
        result_folder_name=kept.result_folder_name,
        idempotency_key="restart-accept-prior-preview",
    )
    result_before_retry = tree_state(verified.result_root)
    job_before_retry = job_path.read_bytes()
    repeated = await restarted.accept_review(
        job_id=kept.job_id,
        expected_revision=kept.job_revision,
        preview_fingerprint=kept.preview_fingerprint,
        candidate_fingerprint=kept.candidate_fingerprint,
        output_parent=kept.output_parent,
        result_folder_name=kept.result_folder_name,
        idempotency_key="restart-accept-prior-preview",
    )
    assert repeated == verified
    assert job_path.read_bytes() == job_before_retry
    assert tree_state(repeated.result_root) == result_before_retry
    assert tuple(output.iterdir()) == (repeated.result_root,)
    assert factory.initial_count == 0
    assert factory.revision_count == 0
    assert tree_state(fixture.sofia_root) == source_before


@pytest.mark.anyio
async def test_executing_job_rehydrates_once_without_duplicate_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "interrupted-execution.json"
    source_before = tree_state(fixture.sofia_root)
    review_service = FoldweaveReviewService()
    reviewing = await review_service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=job_path,
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="restart-execution-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.candidate_plan is not None
    assert reviewing.preview is not None

    def interrupt_before_copy(
        _service: FoldweaveReviewService,
        _writer: FolderRefactorJobV3Writer,
        job: FolderRefactorJobV3,
        *,
        progress_callback: object,
    ) -> FolderRefactorJobV3:
        del progress_callback
        assert job.lifecycle is FolderJobLifecycleV3.EXECUTING
        raise RuntimeError("Simulated process exit after durable authorization.")

    with monkeypatch.context() as interrupted:
        interrupted.setattr(
            FoldweaveReviewService,
            "_execute_locked",
            interrupt_before_copy,
        )
        with pytest.raises(RuntimeError, match="Simulated process exit"):
            review_service.accept(
                job_path,
                expected_revision=reviewing.revision,
                preview_fingerprint=reviewing.preview.preview_fingerprint,
                candidate_fingerprint=(
                    reviewing.preview.compiled_candidate_fingerprint
                ),
                output_parent=output,
                result_folder_name=reviewing.candidate_plan.result_folder_name,
                idempotency_key="restart-execution-accept",
                channel="native_app",
            )

    executing = FolderRefactorJobV3Store(job_path).inspect()
    assert executing.lifecycle is FolderJobLifecycleV3.EXECUTING
    assert executing.execution_authorization is not None
    assert tuple(output.iterdir()) == ()

    factory = _CountingProviderFactory()
    restarted = FoldweaveBrowserReviewService(
        job_path=job_path,
        provider_factory=factory,
        review_channel="native_app",
    )
    checkpoint = restarted.rehydrate_web_checkpoint()
    assert checkpoint is not None
    assert checkpoint.lifecycle is FolderWebLifecycle.VERIFIED
    recovered = FolderRefactorJobV3Store(job_path).inspect()
    assert recovered.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert recovered.final_result_path is not None
    assert tuple(output.iterdir()) == (recovered.final_result_path,)
    result_before_retry = tree_state(recovered.final_result_path)
    job_before_retry = job_path.read_bytes()

    repeated = restarted.rehydrate_web_checkpoint()
    assert repeated == checkpoint
    assert job_path.read_bytes() == job_before_retry
    assert tree_state(recovered.final_result_path) == result_before_retry
    assert tuple(output.iterdir()) == (recovered.final_result_path,)
    assert factory.initial_count == 0
    assert factory.revision_count == 0
    assert tree_state(fixture.sofia_root) == source_before
