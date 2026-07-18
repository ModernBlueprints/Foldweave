"""Exact-turn tests for the bounded scripted planner provider."""

from __future__ import annotations

import builtins

import pytest

from name_atlas.folder_refactor.planner_contracts import (
    FolderEvidenceLedger,
    FolderPlannerTurnInput,
    ListInventoryPageCall,
    PlannerObservableTurn,
    ProviderBlockedResponse,
    ProviderToolResponse,
    evidence_ledger_payload,
    observable_turn_payload,
    planner_history_item,
)
from name_atlas.folder_refactor.planner_provider import (
    PlannerProvider,
    PlannerProviderTransportError,
    ScriptedPlannerProvider,
    ScriptedProviderExceptionOutcome,
    ScriptedProviderExhaustedError,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

REQUEST = "Prepare this folder for handoff."


def _ledger() -> FolderEvidenceLedger:
    initial_evidence = {
        "files": [
            {
                "evidence_eligible": True,
                "file_id": "b" * 64,
                "path": "brief.txt",
                "protected": False,
                "size": 12,
            }
        ]
    }
    initial_bytes = len(canonical_json_bytes(initial_evidence))
    unbound = FolderEvidenceLedger.model_construct(
        source_commitment="a" * 64,
        request_fingerprint=request_fingerprint(REQUEST),
        initial_evidence=initial_evidence,
        initial_evidence_bytes=initial_bytes,
        records=(),
        aggregate_result_bytes=0,
        total_outbound_evidence_bytes=initial_bytes,
        evidence_fingerprint="d" * 64,
    )
    return FolderEvidenceLedger(
        source_commitment=unbound.source_commitment,
        request_fingerprint=unbound.request_fingerprint,
        initial_evidence=unbound.initial_evidence,
        initial_evidence_bytes=unbound.initial_evidence_bytes,
        records=(),
        aggregate_result_bytes=0,
        total_outbound_evidence_bytes=unbound.total_outbound_evidence_bytes,
        evidence_fingerprint=canonical_sha256(evidence_ledger_payload(unbound)),
    )


def _turn(number: int) -> FolderPlannerTurnInput:
    prior_turns = tuple(
        planner_history_item(_observable_turn(turn)) for turn in range(1, number)
    )
    return FolderPlannerTurnInput(
        job_id="1" * 32,
        response_turn=number,
        provider_kind="deterministic",
        request=REQUEST,
        request_fingerprint=request_fingerprint(REQUEST),
        source_commitment="a" * 64,
        evidence_ledger=_ledger(),
        prior_turns=prior_turns,
        compiler_failures=(),
    )


def _observable_turn(number: int) -> PlannerObservableTurn:
    call = ListInventoryPageCall(
        call_id=f"prior-call-{number}",
        cursor=None,
        page_size=25,
    )
    input_payload = _turn(number).model_dump(mode="json")
    input_bytes = len(canonical_json_bytes(input_payload))
    input_fingerprint = canonical_sha256(input_payload)
    unbound = PlannerObservableTurn.model_construct(
        response_turn=number,
        provider_kind="deterministic",
        returned_model=None,
        observable_output_items=(),
        tool_calls=(call,),
        blocker_code=None,
        input_bytes=input_bytes,
        input_fingerprint=input_fingerprint,
        input_payload=input_payload,
        response_fingerprint="d" * 64,
    )
    return PlannerObservableTurn(
        response_turn=number,
        provider_kind="deterministic",
        returned_model=None,
        observable_output_items=(),
        tool_calls=(call,),
        blocker_code=None,
        input_bytes=input_bytes,
        input_fingerprint=input_fingerprint,
        input_payload=input_payload,
        response_fingerprint=canonical_sha256(observable_turn_payload(unbound)),
    )


def _tool_response(call_id: str) -> ProviderToolResponse:
    return ProviderToolResponse(
        provider_kind="deterministic",
        observable_output_items=({"type": "scripted-test-output"},),
        tool_calls=(ListInventoryPageCall(call_id=call_id, cursor=None, page_size=25),),
    )


@pytest.mark.anyio
async def test_scripted_provider_consumes_exact_order_without_filesystem(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first = _tool_response("call-1")
    second = ProviderBlockedResponse(
        provider_kind="deterministic",
        blocker_code="scripted_terminal_block",
        message="The scripted test reached its declared blocker.",
    )
    provider = ScriptedPlannerProvider((first, second))
    first_input = _turn(1)
    second_input = _turn(2)

    def fail_open(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AssertionError("Planner provider must not access the filesystem.")

    monkeypatch.setattr(builtins, "open", fail_open)

    assert isinstance(provider, PlannerProvider)
    assert await provider.exchange(first_input) is first
    assert await provider.exchange(second_input) is second
    assert provider.received_inputs == (first_input, second_input)
    assert provider.consumed_count == 2
    assert provider.remaining_count == 0


@pytest.mark.anyio
async def test_exhaustion_prevents_an_extra_recorded_turn() -> None:
    response = _tool_response("only-call")
    provider = ScriptedPlannerProvider((response,))
    first_input = _turn(1)

    assert await provider.exchange(first_input) is response
    with pytest.raises(ScriptedProviderExhaustedError, match="no remaining outcome"):
        await provider.exchange(_turn(2))

    assert provider.received_inputs == (first_input,)
    assert provider.consumed_count == 1
    assert provider.remaining_count == 0


@pytest.mark.anyio
async def test_declared_transport_failure_consumes_one_turn_without_retry() -> None:
    later_response = _tool_response("must-not-be-consumed-as-retry")
    provider = ScriptedPlannerProvider(
        (
            ScriptedProviderExceptionOutcome(
                error_kind="transport",
                message="network path unavailable",
            ),
            later_response,
        )
    )
    failed_input = _turn(1)

    with pytest.raises(
        PlannerProviderTransportError,
        match="network path unavailable",
    ):
        await provider.exchange(failed_input)

    assert provider.received_inputs == (failed_input,)
    assert provider.consumed_count == 1
    assert provider.remaining_count == 1

    explicit_next_input = _turn(2)
    assert await provider.exchange(explicit_next_input) is later_response
    assert provider.received_inputs == (failed_input, explicit_next_input)


@pytest.mark.anyio
async def test_script_and_input_types_are_strict() -> None:
    response = _tool_response("strict-call")

    with pytest.raises(TypeError, match="exact tuple"):
        ScriptedPlannerProvider([response])  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="strict provider response"):
        ScriptedPlannerProvider((object(),))  # type: ignore[arg-type]

    provider = ScriptedPlannerProvider((response,))
    with pytest.raises(TypeError, match="FolderPlannerTurnInput"):
        await provider.exchange(object())  # type: ignore[arg-type]
    assert provider.received_inputs == ()
    assert provider.consumed_count == 0
    assert provider.remaining_count == 1
