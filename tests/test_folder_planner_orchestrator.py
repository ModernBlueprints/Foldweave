"""Integrated A2 tests for bounded planning, repair, and clarification."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import pytest

import name_atlas.folder_refactor.planner_orchestrator as planner_module
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.inventory import FolderScan, scan_folder
from name_atlas.folder_refactor.markdown_links import build_reference_graph
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerProgress,
    FolderPlannerTurnInput,
    ListInventoryPageCall,
    ProviderToolResponse,
    RequestClarificationCall,
    SubmitPlanCall,
)
from name_atlas.folder_refactor.planner_evidence import (
    LocalFolderEvidenceService,
    append_evidence_execution,
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.planner_orchestrator import (
    PlannerOrchestrator,
    create_planner_progress,
)
from name_atlas.folder_refactor.planner_provider import (
    PlannerProviderError,
    PlannerProviderTimeoutError,
    PlannerProviderTransportError,
    ScriptedPlannerProvider,
    ScriptedProviderExceptionOutcome,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

REQUEST = "Organize this folder and keep every file."
TEST_JOB_ID = "123e4567e89b42d3a456426614174000"


class _SimulatedCrash(RuntimeError):
    pass


class _UnknownProviderError(PlannerProviderError):
    pass


class _LiveOutcomeProvider:
    def __init__(self, outcome: object) -> None:
        self._outcome = outcome
        self.invocation_count = 0

    @property
    def provider_kind(self) -> Literal["live"]:
        return "live"

    async def exchange(self, turn_input: FolderPlannerTurnInput, /):
        del turn_input
        self.invocation_count += 1
        if isinstance(self._outcome, BaseException):
            raise self._outcome
        return self._outcome


class _CountingEvidenceService:
    def __init__(self, scan: FolderScan) -> None:
        self._delegate = _evidence_service(scan)
        self.invocation_count = 0

    def execute(self, call):
        self.invocation_count += 1
        return self._delegate.execute(call)


def _scan(tmp_path: Path) -> FolderScan:
    root = tmp_path / "source"
    root.mkdir()
    (root / "notes.md").write_text("See [report](report.txt).\n", encoding="utf-8")
    (root / "report.txt").write_text("Approved report.\n", encoding="utf-8")
    return scan_folder(root)


def _evidence_service(scan: FolderScan) -> LocalFolderEvidenceService:
    return LocalFolderEvidenceService(
        scan,
        reference_graph=_reference_graph(scan),
    )


def _reference_graph(scan: FolderScan):
    markdown = {
        item.relative_path: (scan.source_root / item.relative_path).read_bytes()
        for item in scan.inventory.files
        if Path(item.relative_path).suffix.casefold() in {".md", ".markdown"}
    }
    return build_reference_graph(scan.inventory, markdown)


def _plan(
    scan: FolderScan,
    *,
    evidence_fingerprint: str,
    evidence_id: str,
    request_id: str | None = None,
) -> FolderPlan:
    return FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_id or request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name="organized-copy",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=f"organized/{item.relative_path}",
                rationale="Groups the material under the requested result.",
                evidence_ids=(evidence_id,),
            )
            for item in scan.inventory.files
            if not item.protected
        ),
        exclusions=(),
    )


def _expected_ledger(scan: FolderScan, call: ListInventoryPageCall):
    service = _evidence_service(scan)
    return append_evidence_execution(
        create_initial_evidence_ledger(scan.inventory, REQUEST),
        response_turn=1,
        call=call,
        execution=service.execute(call),
    )


def _orchestrator(
    scan: FolderScan,
    provider: ScriptedPlannerProvider,
    checkpoints: list,
) -> PlannerOrchestrator:
    return PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=provider,
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
        checkpoint=checkpoints.append,
    )


def _initial(
    scan: FolderScan,
    request: str = REQUEST,
) -> FolderPlannerProgress:
    return create_planner_progress(
        scan.inventory,
        request,
        job_id=TEST_JOB_ID,
        provider_kind="deterministic",
    )


@pytest.mark.anyio
async def test_zero_question_plan_runs_through_evidence_and_compiler(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    evidence_call = ListInventoryPageCall(
        call_id="inventory",
        page_size=10,
    )
    ledger = _expected_ledger(scan, evidence_call)
    submitted = _plan(
        scan,
        evidence_fingerprint=ledger.evidence_fingerprint,
        evidence_id=ledger.records[0].fingerprint,
    )
    provider = ScriptedPlannerProvider(
        (
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(evidence_call,),
            ),
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(SubmitPlanCall(call_id="plan", plan=submitted),),
            ),
        )
    )
    checkpoints: list = []
    orchestrator = _orchestrator(scan, provider, checkpoints)

    result = await orchestrator.run(_initial(scan))

    assert result.status == "accepted"
    assert result.accepted_plan is not None
    assert result.response_turns == 2
    assert result.evidence_calls == result.evidence_calls_observed == 1
    assert result.plan_submissions == 1
    assert result.clarification_question is None
    assert provider.consumed_count == 2
    assert any(item.pending_response_turn == 1 for item in checkpoints)
    assert any(
        item.pending_evidence_call is not None
        and item.pending_evidence_call.call.call_id == "inventory"
        for item in checkpoints
    )


@pytest.mark.anyio
async def test_one_question_answer_continues_same_bounded_planner(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    evidence_call = ListInventoryPageCall(call_id="inventory", page_size=10)
    ledger = _expected_ledger(scan, evidence_call)
    evidence_id = ledger.records[0].fingerprint
    submitted = _plan(
        scan,
        evidence_fingerprint=ledger.evidence_fingerprint,
        evidence_id=evidence_id,
    )
    provider = ScriptedPlannerProvider(
        (
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(evidence_call,),
            ),
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(
                    RequestClarificationCall(
                        call_id="question",
                        question="Which report should lead the handoff?",
                        missing_facts=("lead_report",),
                        evidence_ids=(evidence_call.call_id,),
                    ),
                ),
            ),
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(SubmitPlanCall(call_id="plan", plan=submitted),),
            ),
        )
    )
    orchestrator = _orchestrator(scan, provider, [])

    waiting = await orchestrator.run(_initial(scan))
    result = await orchestrator.answer_clarification(
        waiting,
        "Use the approved report.",
    )

    assert waiting.status == "awaiting_clarification"
    assert waiting.response_turns == 2
    assert result.status == "accepted"
    assert result.response_turns == 3
    assert result.clarification_answer == "Use the approved report."
    assert provider.consumed_count == 3


@pytest.mark.anyio
async def test_second_question_blocks_without_review_loop(tmp_path: Path) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(
        (
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(
                    RequestClarificationCall(
                        call_id="question-1",
                        question="Which report should lead?",
                        missing_facts=("lead_report",),
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            ),
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(
                    RequestClarificationCall(
                        call_id="question-2",
                        question="Can you decide another detail?",
                        missing_facts=("another_detail",),
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            ),
        )
    )
    orchestrator = _orchestrator(scan, provider, [])

    waiting = await orchestrator.run(_initial(scan))
    result = await orchestrator.answer_clarification(waiting, "Use report A.")

    assert result.status == "blocked"
    assert result.blocker_code == "second_clarification_not_allowed"
    assert result.response_turns == 2


@pytest.mark.anyio
async def test_two_repairs_are_allowed_but_third_rejection_blocks(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    initial = _initial(scan)
    invalid = _plan(
        scan,
        evidence_fingerprint=initial.evidence_ledger.evidence_fingerprint,
        evidence_id="initial_inventory",
        request_id="f" * 64,
    )
    provider = ScriptedPlannerProvider(
        tuple(
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(SubmitPlanCall(call_id=f"plan-{index}", plan=invalid),),
            )
            for index in range(3)
        )
    )
    orchestrator = _orchestrator(scan, provider, [])

    result = await orchestrator.run(initial)

    assert result.status == "blocked"
    assert result.blocker_code == "plan_repair_limit_exceeded"
    assert result.response_turns == 3
    assert result.plan_submissions == 3
    assert len(result.compiler_failures) == 3


@pytest.mark.anyio
async def test_provider_failure_consumes_one_turn_and_never_asks_user(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(
        (
            ScriptedProviderExceptionOutcome(
                error_kind="transport",
                message="declared transport failure",
            ),
        )
    )
    checkpoints: list = []
    orchestrator = _orchestrator(scan, provider, checkpoints)

    result = await orchestrator.run(_initial(scan))

    assert result.status == "blocked"
    assert result.blocker_code == "provider_transport_error"
    assert result.response_turns == 1
    assert result.clarification_question is None
    assert provider.consumed_count == 1
    assert any(item.pending_response_turn == 1 for item in checkpoints)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("failure", "expected_code"),
    [
        (PlannerProviderError("base failure"), "provider_request_failed"),
        (_UnknownProviderError("unknown failure"), "provider_request_failed"),
        (PlannerProviderTimeoutError("timeout"), "provider_timeout"),
        (PlannerProviderTransportError("transport"), "provider_transport_error"),
    ],
)
async def test_live_unobserved_failures_persist_without_model_or_pending_turn(
    tmp_path: Path,
    failure: PlannerProviderError,
    expected_code: str,
) -> None:
    scan = _scan(tmp_path)
    provider = _LiveOutcomeProvider(failure)
    orchestrator = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=provider,
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
    )
    initial = create_planner_progress(
        scan.inventory,
        REQUEST,
        job_id=TEST_JOB_ID,
        provider_kind="live",
    )

    result = await orchestrator.run(initial)

    assert result.status == "blocked"
    assert result.blocker_code == expected_code
    assert result.pending_response_turn is None
    assert result.turns[-1].returned_model is None
    assert result.turns[-1].blocker_code == expected_code
    assert provider.invocation_count == 1


@pytest.mark.anyio
async def test_live_provider_origin_mismatch_is_durably_blocked(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    provider = _LiveOutcomeProvider(
        ProviderToolResponse(
            provider_kind="deterministic",
            tool_calls=(ListInventoryPageCall(call_id="wrong-origin"),),
        )
    )
    orchestrator = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=provider,
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
    )
    initial = create_planner_progress(
        scan.inventory,
        REQUEST,
        job_id=TEST_JOB_ID,
        provider_kind="live",
    )

    result = await orchestrator.run(initial)

    assert result.status == "blocked"
    assert result.blocker_code == "provider_origin_mismatch"
    assert result.pending_response_turn is None
    assert result.turns[-1].returned_model is None
    assert provider.invocation_count == 1


@pytest.mark.anyio
async def test_invalid_live_provider_response_is_durably_blocked(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    provider = _LiveOutcomeProvider(object())
    orchestrator = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=provider,
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
    )
    initial = create_planner_progress(
        scan.inventory,
        REQUEST,
        job_id=TEST_JOB_ID,
        provider_kind="live",
    )

    result = await orchestrator.run(initial)

    assert result.status == "blocked"
    assert result.blocker_code == "provider_response_invalid"
    assert result.pending_response_turn is None
    assert result.turns[-1].returned_model is None
    assert provider.invocation_count == 1


@pytest.mark.anyio
async def test_source_change_blocks_before_provider_call(tmp_path: Path) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(())
    orchestrator = _orchestrator(scan, provider, [])
    (scan.source_root / "report.txt").write_text("changed", encoding="utf-8")

    result = await orchestrator.run(_initial(scan))

    assert result.status == "blocked"
    assert result.blocker_code == "source_changed"
    assert provider.consumed_count == 0


@pytest.mark.anyio
async def test_unsupported_delete_request_blocks_before_provider_call(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(())
    orchestrator = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request="Delete old files and organize the rest.",
        provider=provider,
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
    )
    initial = _initial(scan, "Delete old files and organize the rest.")

    result = await orchestrator.run(initial)

    assert result.status == "blocked"
    assert result.blocker_code == "file_deletion_unsupported"
    assert result.response_turns == 0
    assert provider.consumed_count == 0


@pytest.mark.anyio
async def test_eight_response_turns_are_a_hard_ceiling(tmp_path: Path) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(
        tuple(
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(
                    ListInventoryPageCall(
                        call_id=f"inventory-{index}",
                        page_size=1,
                    ),
                ),
            )
            for index in range(8)
        )
    )
    orchestrator = _orchestrator(scan, provider, [])

    result = await orchestrator.run(_initial(scan))

    assert result.status == "blocked"
    assert result.blocker_code == "response_turn_limit_exceeded"
    assert result.response_turns == 8
    assert provider.consumed_count == 8


@pytest.mark.anyio
async def test_twenty_fifth_evidence_call_is_observed_but_not_executed(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    first_batch = tuple(
        ListInventoryPageCall(call_id=f"inventory-{index}", page_size=1)
        for index in range(24)
    )
    provider = ScriptedPlannerProvider(
        (
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=first_batch,
            ),
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(
                    ListInventoryPageCall(call_id="inventory-overflow", page_size=1),
                ),
            ),
        )
    )
    orchestrator = _orchestrator(scan, provider, [])

    result = await orchestrator.run(_initial(scan))

    assert result.status == "blocked"
    assert result.blocker_code == "evidence_call_limit_exceeded"
    assert result.evidence_calls == 24
    assert result.evidence_calls_observed == 25
    assert result.response_turns == 2
    assert provider.consumed_count == 2


@pytest.mark.anyio
async def test_persisted_incomplete_provider_turn_is_never_replayed(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(())
    orchestrator = _orchestrator(scan, provider, [])
    initial = _initial(scan)
    turn_input = FolderPlannerTurnInput(
        job_id=TEST_JOB_ID,
        response_turn=1,
        provider_kind="deterministic",
        request=REQUEST,
        request_fingerprint=request_fingerprint(REQUEST),
        source_commitment=scan.inventory.source_commitment,
        evidence_ledger=initial.evidence_ledger,
        prior_turns=(),
        compiler_failures=(),
    )
    input_payload = turn_input.model_dump(mode="json")
    payload = initial.model_dump(mode="python")
    payload.update(
        {
            "outbound_evidence_bytes": len(canonical_json_bytes(input_payload)),
            "pending_response_input_bytes": len(canonical_json_bytes(input_payload)),
            "pending_response_input_fingerprint": canonical_sha256(input_payload),
            "pending_response_input_payload": input_payload,
            "pending_response_turn": 1,
            "response_turns": 1,
        }
    )
    interrupted = FolderPlannerProgress.model_validate(payload, strict=True)

    result = await orchestrator.run(interrupted)

    assert result.status == "blocked"
    assert result.blocker_code == "provider_turn_incomplete"
    assert result.response_turns == 1
    assert provider.consumed_count == 0


@pytest.mark.anyio
async def test_outbound_evidence_cap_blocks_before_reserving_a_turn(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    scan = _scan(tmp_path)
    provider = ScriptedPlannerProvider(())
    orchestrator = _orchestrator(scan, provider, [])
    initial = _initial(scan)
    monkeypatch.setattr(planner_module, "MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES", 1)

    result = await orchestrator.run(initial)

    assert result.status == "blocked"
    assert result.blocker_code == "outbound_evidence_limit_exceeded"
    assert result.response_turns == 0
    assert provider.consumed_count == 0


@pytest.mark.anyio
async def test_persisted_submit_action_is_processed_before_another_provider_turn(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    initial = _initial(scan)
    submitted = _plan(
        scan,
        evidence_fingerprint=initial.evidence_ledger.evidence_fingerprint,
        evidence_id="initial_inventory",
    )
    captured: list[FolderPlannerProgress] = []

    def crash_after_response(progress: FolderPlannerProgress) -> None:
        captured.append(progress)
        if progress.processing_response_turn == 1:
            raise _SimulatedCrash

    first = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=ScriptedPlannerProvider(
            (
                ProviderToolResponse(
                    provider_kind="deterministic",
                    tool_calls=(
                        SubmitPlanCall(call_id="persisted-plan", plan=submitted),
                    ),
                ),
            )
        ),
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
        checkpoint=crash_after_response,
    )
    with pytest.raises(_SimulatedCrash):
        await first.run(initial)

    persisted = captured[-1]
    resumed_provider = ScriptedPlannerProvider(())
    resumed = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=resumed_provider,
        evidence_service=_evidence_service(scan),
        reference_graph=_reference_graph(scan),
    )
    result = await resumed.run(persisted)

    assert result.status == "accepted"
    assert result.plan_submissions == 1
    assert result.response_turns == 1
    assert resumed_provider.consumed_count == 0


@pytest.mark.anyio
async def test_evidence_is_counted_before_execution_and_not_repeated_after_crash(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    captured: list[FolderPlannerProgress] = []
    first_evidence = _CountingEvidenceService(scan)

    def crash_after_reservation(progress: FolderPlannerProgress) -> None:
        captured.append(progress)
        if progress.pending_evidence_call is not None:
            raise _SimulatedCrash

    first = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=ScriptedPlannerProvider(
            (
                ProviderToolResponse(
                    provider_kind="deterministic",
                    tool_calls=(
                        ListInventoryPageCall(call_id="reserved", page_size=1),
                    ),
                ),
            )
        ),
        evidence_service=first_evidence,
        reference_graph=_reference_graph(scan),
        checkpoint=crash_after_reservation,
    )
    with pytest.raises(_SimulatedCrash):
        await first.run(_initial(scan))

    persisted = captured[-1]
    assert persisted.evidence_calls == 1
    assert persisted.evidence_ledger.records == ()
    assert first_evidence.invocation_count == 0
    resumed_evidence = _CountingEvidenceService(scan)
    resumed_provider = ScriptedPlannerProvider(())
    resumed = PlannerOrchestrator(
        job_id=TEST_JOB_ID,
        scan=scan,
        request=REQUEST,
        provider=resumed_provider,
        evidence_service=resumed_evidence,
        reference_graph=_reference_graph(scan),
    )
    result = await resumed.run(persisted)

    assert result.status == "blocked"
    assert result.blocker_code == "evidence_call_incomplete"
    assert result.evidence_calls == 1
    assert result.pending_evidence_call == persisted.pending_evidence_call
    assert resumed_evidence.invocation_count == 0
    assert resumed_provider.consumed_count == 0
