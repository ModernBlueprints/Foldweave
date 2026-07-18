"""Restart integration between bounded planner and durable job authority."""

from __future__ import annotations

import uuid
from pathlib import Path

import pytest

from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.inventory import FolderScan, scan_folder
from name_atlas.folder_refactor.job import (
    FolderJobLifecycle,
    FolderJobRevisionError,
    FolderRefactorJobStore,
    build_new_job,
)
from name_atlas.folder_refactor.job_planning import JobPlannerCheckpoint
from name_atlas.folder_refactor.markdown_links import build_reference_graph
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    ListInventoryPageCall,
    PlannerObservableTurn,
    ProviderToolResponse,
    RequestClarificationCall,
    SubmitPlanCall,
    observable_turn_payload,
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
from name_atlas.folder_refactor.planner_provider import ScriptedPlannerProvider
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

REQUEST = "Organize this project for handoff."


class _SimulatedCrash(RuntimeError):
    pass


async def _durable_reserved_turn(
    tmp_path: Path,
) -> tuple[FolderRefactorJobStore, FolderScan]:
    scan = _scan(tmp_path)
    store, job_id = _persist_new_job(tmp_path, scan)
    with store.writer() as writer:
        durable = JobPlannerCheckpoint(writer)

        def crash_after_reservation(progress) -> None:
            durable(progress)
            if progress.pending_response_turn is not None:
                raise _SimulatedCrash

        orchestrator = PlannerOrchestrator(
            job_id=job_id,
            scan=scan,
            request=REQUEST,
            provider=ScriptedPlannerProvider(()),
            evidence_service=_evidence(scan),
            reference_graph=_reference_graph(scan),
            checkpoint=crash_after_reservation,
        )
        with pytest.raises(_SimulatedCrash):
            await orchestrator.run(orchestrator.initial_progress())
    return store, scan


async def _durable_evidence_cursor(
    tmp_path: Path,
) -> tuple[FolderRefactorJobStore, FolderScan, ListInventoryPageCall]:
    scan = _scan(tmp_path)
    store, job_id = _persist_new_job(tmp_path, scan)
    call = ListInventoryPageCall(call_id="inventory", page_size=10)
    with store.writer() as writer:
        durable = JobPlannerCheckpoint(writer)

        def crash_after_cursor(progress) -> None:
            durable(progress)
            if (
                progress.processing_response_turn is not None
                and progress.pending_evidence_call is None
            ):
                raise _SimulatedCrash

        orchestrator = PlannerOrchestrator(
            job_id=job_id,
            scan=scan,
            request=REQUEST,
            provider=ScriptedPlannerProvider(
                (
                    ProviderToolResponse(
                        provider_kind="deterministic",
                        tool_calls=(call,),
                    ),
                )
            ),
            evidence_service=_evidence(scan),
            reference_graph=_reference_graph(scan),
            checkpoint=crash_after_cursor,
        )
        with pytest.raises(_SimulatedCrash):
            await orchestrator.run(orchestrator.initial_progress())
    return store, scan, call


def _scan(tmp_path: Path) -> FolderScan:
    source = tmp_path / "source"
    source.mkdir()
    (source / "note.md").write_text("[report](report.txt)\n", encoding="utf-8")
    (source / "report.txt").write_text("approved\n", encoding="utf-8")
    return scan_folder(source)


def _evidence(scan: FolderScan) -> LocalFolderEvidenceService:
    return LocalFolderEvidenceService(
        scan,
        reference_graph=_reference_graph(scan),
    )


def _reference_graph(scan: FolderScan):
    markdown = {"note.md": (scan.source_root / "note.md").read_bytes()}
    return build_reference_graph(scan.inventory, markdown)


def _persist_new_job(
    tmp_path: Path,
    scan: FolderScan,
) -> tuple[FolderRefactorJobStore, str]:
    output = tmp_path / "output"
    output.mkdir()
    job_id = uuid.uuid4().hex
    path = tmp_path / "state" / f"{job_id}.json"
    job = build_new_job(
        source_root=scan.source_root,
        output_parent=output,
        job_path=path,
        user_request=REQUEST,
        scan=scan,
        job_id=job_id,
    )
    store = FolderRefactorJobStore(path)
    with store.writer() as writer:
        writer.save(job, expected_revision=None)
    return store, job_id


def _accepted_submission(
    scan: FolderScan,
    evidence_call: ListInventoryPageCall,
) -> FolderPlan:
    expected_service = _evidence(scan)
    ledger = append_evidence_execution(
        create_initial_evidence_ledger(scan.inventory, REQUEST),
        response_turn=1,
        call=evidence_call,
        execution=expected_service.execute(evidence_call),
    )
    return FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=ledger.evidence_fingerprint,
        result_folder_name="organized-copy",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=f"organized/{item.relative_path}",
                rationale="Creates the requested handoff structure.",
                evidence_ids=(ledger.records[0].fingerprint,),
            )
            for item in scan.inventory.files
        ),
        exclusions=(),
    )


@pytest.mark.anyio
async def test_accepted_plan_is_revisioned_into_executing_job(tmp_path: Path) -> None:
    scan = _scan(tmp_path)
    store, job_id = _persist_new_job(tmp_path, scan)
    evidence_call = ListInventoryPageCall(call_id="inventory", page_size=10)
    submission = _accepted_submission(scan, evidence_call)
    provider = ScriptedPlannerProvider(
        (
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(evidence_call,),
            ),
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(SubmitPlanCall(call_id="plan", plan=submission),),
            ),
        )
    )
    with store.writer() as writer:
        checkpoint = JobPlannerCheckpoint(writer)
        orchestrator = PlannerOrchestrator(
            job_id=job_id,
            scan=scan,
            request=REQUEST,
            provider=provider,
            evidence_service=_evidence(scan),
            reference_graph=_reference_graph(scan),
            checkpoint=checkpoint,
        )
        result = await orchestrator.run(orchestrator.initial_progress())
    loaded = store.load()

    assert result.status == "accepted"
    assert loaded.lifecycle is FolderJobLifecycle.EXECUTING
    assert loaded.planner_progress == result
    assert loaded.accepted_plan == result.accepted_plan
    assert loaded.revision > 1


@pytest.mark.anyio
async def test_restart_after_question_uses_one_new_turn_only(tmp_path: Path) -> None:
    scan = _scan(tmp_path)
    store, job_id = _persist_new_job(tmp_path, scan)
    evidence_call = ListInventoryPageCall(call_id="inventory", page_size=10)
    submission = _accepted_submission(scan, evidence_call)
    expected_service = _evidence(scan)
    ledger = append_evidence_execution(
        create_initial_evidence_ledger(scan.inventory, REQUEST),
        response_turn=1,
        call=evidence_call,
        execution=expected_service.execute(evidence_call),
    )
    first_provider = ScriptedPlannerProvider(
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
                        question="Which report should lead?",
                        missing_facts=("lead_report",),
                        evidence_ids=(ledger.records[0].fingerprint,),
                    ),
                ),
            ),
        )
    )
    with store.writer() as writer:
        first = PlannerOrchestrator(
            job_id=job_id,
            scan=scan,
            request=REQUEST,
            provider=first_provider,
            evidence_service=_evidence(scan),
            reference_graph=_reference_graph(scan),
            checkpoint=JobPlannerCheckpoint(writer),
        )
        waiting = await first.run(first.initial_progress())
    assert store.load().lifecycle is FolderJobLifecycle.AWAITING_CLARIFICATION

    resumed_provider = ScriptedPlannerProvider(
        (
            ProviderToolResponse(
                provider_kind="deterministic",
                tool_calls=(SubmitPlanCall(call_id="plan", plan=submission),),
            ),
        )
    )
    with store.writer() as writer:
        resumed = PlannerOrchestrator(
            job_id=job_id,
            scan=scan,
            request=REQUEST,
            provider=resumed_provider,
            evidence_service=_evidence(scan),
            reference_graph=_reference_graph(scan),
            checkpoint=JobPlannerCheckpoint(writer),
        )
        result = await resumed.answer_clarification(
            writer.load().planner_progress,
            "Use the approved report.",
        )

    assert waiting.status == "awaiting_clarification"
    assert result.status == "accepted"
    assert result.response_turns == 3
    assert resumed_provider.consumed_count == 1
    assert store.load().lifecycle is FolderJobLifecycle.EXECUTING


@pytest.mark.anyio
async def test_durable_checkpoint_rejects_planner_counter_rewind(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    store, job_id = _persist_new_job(tmp_path, scan)
    initial = create_planner_progress(
        scan.inventory,
        REQUEST,
        job_id=job_id,
        provider_kind="deterministic",
    )

    with store.writer() as writer:
        durable = JobPlannerCheckpoint(writer)

        def crash_after_reservation(progress) -> None:
            durable(progress)
            if progress.pending_response_turn is not None:
                raise _SimulatedCrash

        orchestrator = PlannerOrchestrator(
            job_id=job_id,
            scan=scan,
            request=REQUEST,
            provider=ScriptedPlannerProvider(()),
            evidence_service=_evidence(scan),
            reference_graph=_reference_graph(scan),
            checkpoint=crash_after_reservation,
        )
        with pytest.raises(_SimulatedCrash):
            await orchestrator.run(initial)

    reserved = store.load()
    assert reserved.planner_progress is not None
    assert reserved.planner_progress.response_turns == 1
    assert reserved.planner_progress.pending_response_turn == 1
    with store.writer() as writer, pytest.raises(FolderJobRevisionError):
        JobPlannerCheckpoint(writer)(initial)

    unchanged = store.load()
    assert unchanged.revision == reserved.revision
    assert unchanged.planner_progress == reserved.planner_progress


@pytest.mark.anyio
async def test_durable_checkpoint_rejects_completion_for_other_input(
    tmp_path: Path,
) -> None:
    store, _scan_result = await _durable_reserved_turn(tmp_path)
    current = store.load().planner_progress
    assert current is not None
    assert current.pending_response_input_payload is not None

    mismatched_payload = dict(current.pending_response_input_payload)
    different_request = "A different valid request submitted after reservation."
    mismatched_input = FolderPlannerTurnInput(
        job_id=current.job_id,
        response_turn=1,
        provider_kind="deterministic",
        request=different_request,
        request_fingerprint=request_fingerprint(different_request),
        source_commitment=_scan_result.inventory.source_commitment,
        evidence_ledger=create_initial_evidence_ledger(
            _scan_result.inventory,
            different_request,
        ),
        prior_turns=(),
        compiler_failures=(),
    )
    mismatched_payload = mismatched_input.model_dump(mode="json")
    turn_payload = {
        "blocker_code": "provider_failed",
        "input_bytes": len(canonical_json_bytes(mismatched_payload)),
        "input_fingerprint": canonical_sha256(mismatched_payload),
        "input_payload": mismatched_payload,
        "observable_output_items": [],
        "provider_kind": "deterministic",
        "response_turn": 1,
        "returned_model": None,
        "tool_calls": [],
    }
    turn = PlannerObservableTurn(
        response_turn=1,
        provider_kind="deterministic",
        returned_model=None,
        observable_output_items=(),
        tool_calls=(),
        blocker_code="provider_failed",
        input_bytes=turn_payload["input_bytes"],
        input_fingerprint=turn_payload["input_fingerprint"],
        input_payload=mismatched_payload,
        response_fingerprint=canonical_sha256(turn_payload),
    )
    assert turn.response_fingerprint == canonical_sha256(observable_turn_payload(turn))
    forged = current.model_copy(
        update={
            "status": "blocked",
            "pending_response_turn": None,
            "pending_response_input_bytes": None,
            "pending_response_input_fingerprint": None,
            "pending_response_input_payload": None,
            "turns": (turn,),
            "blocker_code": "provider_failed",
            "outbound_evidence_bytes": turn.input_bytes,
        }
    )

    with (
        store.writer() as writer,
        pytest.raises(
            FolderJobRevisionError,
            match="does not satisfy the durable job contract",
        ),
    ):
        JobPlannerCheckpoint(writer)(forged)


@pytest.mark.anyio
async def test_durable_checkpoint_rejects_clearing_unprocessed_cursor(
    tmp_path: Path,
) -> None:
    store, _scan_result, _call = await _durable_evidence_cursor(tmp_path)
    current = store.load().planner_progress
    assert current is not None
    assert current.processing_response_turn == 1
    forged = current.model_copy(
        update={
            "processing_response_turn": None,
            "processing_tool_call_index": None,
        }
    )

    with store.writer() as writer, pytest.raises(FolderJobRevisionError):
        JobPlannerCheckpoint(writer)(forged)


@pytest.mark.anyio
async def test_durable_checkpoint_rejects_evidence_without_reservation(
    tmp_path: Path,
) -> None:
    store, scan, call = await _durable_evidence_cursor(tmp_path)
    current = store.load().planner_progress
    assert current is not None
    assert current.pending_evidence_call is None
    execution = _evidence(scan).execute(call)
    forged_ledger = append_evidence_execution(
        current.evidence_ledger,
        response_turn=1,
        call=call,
        execution=execution,
    )
    forged = current.model_copy(
        update={
            "processing_response_turn": None,
            "processing_tool_call_index": None,
            "evidence_calls": 1,
            "evidence_calls_observed": 1,
            "evidence_ledger": forged_ledger,
        }
    )

    with store.writer() as writer, pytest.raises(FolderJobRevisionError):
        JobPlannerCheckpoint(writer)(forged)
