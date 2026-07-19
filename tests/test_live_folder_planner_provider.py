"""Strict no-retry Responses boundary tests for the live folder planner."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from name_atlas.decision_cards.budget import PersistentBudgetLedger
from name_atlas.folder_refactor.live_planner_provider import (
    LiveFolderPlannerProvider,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    ListInventoryPageCall,
    PlannerEvidenceState,
    ProviderBlockedResponse,
    ProviderToolResponse,
    evidence_ledger_payload,
)
from name_atlas.folder_refactor.planner_prompt import PLANNER_RESPONSE_TOOLS
from name_atlas.folder_refactor.planner_provider import (
    PlannerProviderTimeoutError,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

REQUEST = "Prepare this folder for handoff."


class FakeResponses:
    """Capture one request and return or raise one declared outcome."""

    def __init__(self, outcome: object) -> None:
        self.outcome = outcome
        self.requests: list[dict[str, Any]] = []

    async def create(self, **kwargs: Any) -> object:
        self.requests.append(kwargs)
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return self.outcome


def _ledger() -> PlannerEvidenceState:
    initial = {
        "files": [
            {
                "evidence_eligible": True,
                "file_id": "b" * 64,
                "relative_path": "brief.txt",
                "protected": False,
                "size": 12,
            }
        ]
    }
    initial_bytes = len(canonical_json_bytes(initial))
    draft = PlannerEvidenceState.model_construct(
        source_commitment="a" * 64,
        request_fingerprint=request_fingerprint(REQUEST),
        initial_evidence=initial,
        initial_evidence_bytes=initial_bytes,
        records=(),
        aggregate_result_bytes=0,
        total_outbound_evidence_bytes=initial_bytes,
        evidence_fingerprint="0" * 64,
    )
    return PlannerEvidenceState(
        source_commitment=draft.source_commitment,
        request_fingerprint=draft.request_fingerprint,
        initial_evidence=draft.initial_evidence,
        initial_evidence_bytes=draft.initial_evidence_bytes,
        records=(),
        aggregate_result_bytes=0,
        total_outbound_evidence_bytes=draft.total_outbound_evidence_bytes,
        evidence_fingerprint=canonical_sha256(evidence_ledger_payload(draft)),
    )


def _turn() -> FolderPlannerTurnInput:
    return FolderPlannerTurnInput(
        job_id="1" * 32,
        response_turn=1,
        provider_kind="live",
        request=REQUEST,
        request_fingerprint=request_fingerprint(REQUEST),
        source_commitment="a" * 64,
        evidence_ledger=_ledger(),
        prior_turns=(),
        compiler_failures=(),
    )


def _usage() -> SimpleNamespace:
    return SimpleNamespace(
        input_tokens=100,
        output_tokens=20,
        total_tokens=120,
        input_tokens_details=SimpleNamespace(cached_tokens=10),
        output_tokens_details=SimpleNamespace(reasoning_tokens=5),
    )


def _response(arguments: str) -> SimpleNamespace:
    return SimpleNamespace(
        id="resp_secret_provider_identifier",
        model="gpt-5.6-sol-2026-07-01",
        status="completed",
        error=None,
        usage=_usage(),
        output=[
            SimpleNamespace(type="reasoning", status="completed"),
            SimpleNamespace(
                type="function_call",
                name="list_inventory_page",
                call_id="call-1",
                arguments=arguments,
                status="completed",
            ),
        ],
    )


def _provider(outcome: object) -> tuple[LiveFolderPlannerProvider, FakeResponses]:
    responses = FakeResponses(outcome)
    client = SimpleNamespace(responses=responses)
    budget = PersistentBudgetLedger(path=None, live_call_cap=13, cost_cap_usd=10)
    return LiveFolderPlannerProvider(client, budget=budget), responses


@pytest.mark.anyio
async def test_live_provider_makes_one_strict_sanitized_responses_call() -> None:
    provider, responses = _provider(_response('{"cursor":null,"page_size":25}'))

    result = await provider.exchange(_turn())

    assert isinstance(result, ProviderToolResponse)
    assert result.returned_model == "gpt-5.6-sol-2026-07-01"
    assert result.tool_calls == (
        ListInventoryPageCall(call_id="call-1", cursor=None, page_size=25),
    )
    assert "resp_secret_provider_identifier" not in repr(result)
    assert len(provider.usage) == 1
    assert provider.usage[0].total_tokens == 120
    assert len(responses.requests) == 1
    request = responses.requests[0]
    assert request["model"] == "gpt-5.6"
    assert request["store"] is False
    assert request["max_output_tokens"] == 32_768
    assert request["tool_choice"] == "required"
    assert request["parallel_tool_calls"] is True
    assert request["timeout"] == 120.0
    assert len(request["tools"]) == 5
    assert all(tool["strict"] is True for tool in request["tools"])


@pytest.mark.anyio
async def test_live_provider_rejects_duplicate_argument_keys_after_observation() -> (
    None
):
    provider, _responses = _provider(
        _response('{"cursor":null,"cursor":null,"page_size":25}')
    )

    result = await provider.exchange(_turn())

    assert isinstance(result, ProviderBlockedResponse)
    assert result.blocker_code == "provider_response_invalid"
    assert len(provider.usage) == 1


@pytest.mark.anyio
async def test_transport_timeout_consumes_reservation_without_hidden_retry() -> None:
    provider, responses = _provider(TimeoutError("simulated"))

    with pytest.raises(PlannerProviderTimeoutError):
        await provider.exchange(_turn())

    assert len(responses.requests) == 1
    assert provider.usage == ()
    assert provider._budget.snapshot.live_requests_reserved == 1


def test_every_function_schema_requires_every_object_property() -> None:
    def inspect(node: object) -> None:
        if isinstance(node, dict):
            properties = node.get("properties")
            if isinstance(properties, dict):
                assert node.get("additionalProperties") is False
                assert node.get("required") == list(properties)
            assert "default" not in node
            for value in node.values():
                inspect(value)
        elif isinstance(node, list):
            for value in node:
                inspect(value)

    for tool in PLANNER_RESPONSE_TOOLS:
        inspect(tool["parameters"])
