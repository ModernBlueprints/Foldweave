"""Bounded live and recorded DecisionCard provider tests."""

import asyncio
import json
from datetime import datetime
from types import SimpleNamespace
from typing import Any
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from name_atlas.decision_cards import (
    DECISION_CARD_INSTRUCTIONS,
    DECISION_CARD_SCHEMA_VERSION,
    MODEL_ALIAS,
    AuthorityClaimError,
    LiveConfigurationError,
    LiveDecisionCardProvider,
    LiveParsedOutputMissingError,
    LiveRefusalError,
    LiveResponseStatusError,
    LiveTransportError,
    MalformedDecisionCardError,
    RecordedDecisionCard,
    RecordedReplayDecisionCardProvider,
    ReplayFingerprintMismatchError,
    ReplayModelMismatchError,
    ReplayRecordInvalidError,
    ReplaySchemaMismatchError,
    ReplayUsage,
    UnknownCandidatePathError,
    UnknownEvidenceIdError,
    canonical_evidence_text,
    evidence_fingerprint,
    load_recorded_decision_card,
    validate_decision_card,
)
from name_atlas.decision_cards import providers as provider_module
from name_atlas.domain import (
    CandidateExplanation,
    DecisionCard,
    EvidencePacket,
    EvidenceRef,
    LinkedObservation,
    TransformationStep,
)

oslo_tz = ZoneInfo("Europe/Oslo")


def _packet(
    *, profile_description: str = "Fixed repository-ready profile"
) -> EvidencePacket:
    return EvidencePacket(
        family_id="a" * 64,
        original_paths=("objects/campaña.tif",),
        proposed_paths=("objects/ID-001__campana__original.tif",),
        transformation_steps=(
            TransformationStep(
                operation="remove_combining_marks",
                before="campaña",
                after="campana",
            ),
        ),
        candidate_paths=(
            "objects/ID-001__campana__original.tif",
            "objects/ID-001__campaña__original.tif",
        ),
        neighboring_paths=("objects/ID-002__retrato__original.tif",),
        metadata_evidence=(
            EvidenceRef(
                evidence_id="metadata:title",
                label="dc.title",
                value="Campaña comunitaria",
            ),
        ),
        derivative_evidence=(
            EvidenceRef(
                evidence_id="relationship:access",
                label="access derivative",
                value="manualNormalization/access/campaña.jpg",
            ),
        ),
        risk_signals=("combining_marks_removed",),
        profile_description=profile_description,
    )


def _card() -> DecisionCard:
    return DecisionCard(
        possible_interpretations=(
            LinkedObservation(
                text="The source may denote a campaign.",
                evidence_ids=("metadata:title",),
            ),
        ),
        possible_meaning_loss=(
            LinkedObservation(
                text="Removing the mark may obscure the source spelling.",
                evidence_ids=("metadata:title", "relationship:access"),
            ),
        ),
        uncertainty="The bounded evidence does not establish intended spelling.",
        why_the_distinction_matters=(
            "The descriptor remains visible to repository users."
        ),
        discriminating_question="Which supplied spelling preserves the intended name?",
        candidate_explanations=(
            CandidateExplanation(
                candidate_path="objects/ID-001__campana__original.tif",
                explanation="This candidate follows the fixed transformation trace.",
                evidence_ids=("metadata:title",),
            ),
        ),
    )


def _usage() -> ReplayUsage:
    return ReplayUsage(
        input_tokens=100,
        cached_input_tokens=0,
        output_tokens=80,
        reasoning_tokens=20,
        total_tokens=180,
        latency_ms=250.0,
        estimated_cost_usd=None,
    )


def _record(packet: EvidencePacket | None = None) -> RecordedDecisionCard:
    bounded_packet = packet or _packet()
    return RecordedDecisionCard(
        model=MODEL_ALIAS,
        schema_version=DECISION_CARD_SCHEMA_VERSION,
        evidence_fingerprint=evidence_fingerprint(bounded_packet),
        generated_at=datetime(2026, 7, 17, 18, 0, tzinfo=oslo_tz),
        decision_card=_card(),
        usage=_usage(),
    )


class _FakeResponses:
    def __init__(self, response: object) -> None:
        self.response = response
        self.kwargs: dict[str, object] | None = None

    async def parse(self, **kwargs: object) -> object:
        self.kwargs = kwargs
        return self.response


class _FailingResponses:
    async def parse(self, **kwargs: object) -> object:
        del kwargs
        raise TimeoutError("simulated transport timeout")


class _FakeClient:
    def __init__(self, response: object) -> None:
        self.responses = _FakeResponses(response)


class _FailingClient:
    def __init__(self) -> None:
        self.responses = _FailingResponses()


def _response(
    *,
    parsed: object = None,
    status: str = "completed",
    error: object = None,
    output: tuple[object, ...] = (),
) -> SimpleNamespace:
    usage = SimpleNamespace(
        input_tokens=100,
        input_tokens_details=SimpleNamespace(cached_tokens=5),
        output_tokens=80,
        output_tokens_details=SimpleNamespace(reasoning_tokens=20),
        total_tokens=180,
    )
    return SimpleNamespace(
        status=status,
        error=error,
        output=output,
        output_parsed=parsed,
        usage=usage,
    )


def test_canonical_text_is_stable_complete_and_evidence_bound() -> None:
    packet = _packet()
    text = canonical_evidence_text(packet)
    decoded = json.loads(text)

    assert text == canonical_evidence_text(packet)
    assert decoded["model"] == "gpt-5.6"
    assert decoded["schema_version"] == "decision-card.v1"
    assert decoded["packet"]["original_paths"] == ["objects/campaña.tif"]
    assert len(evidence_fingerprint(packet)) == 64
    assert evidence_fingerprint(packet) != evidence_fingerprint(
        _packet(profile_description="Changed profile")
    )


def test_structured_output_has_required_fields_and_forbids_extra_authority() -> None:
    schema = DecisionCard.model_json_schema()

    assert set(schema["required"]) == set(DecisionCard.model_fields)
    malformed = _card().model_dump(mode="python") | {"approved": True}
    with pytest.raises(MalformedDecisionCardError):
        validate_decision_card(malformed, _packet())


def test_output_rejects_unknown_evidence_candidate_and_authority_prose() -> None:
    unknown_evidence = _card().model_copy(
        update={
            "possible_interpretations": (
                LinkedObservation(
                    text="An unsupported interpretation.",
                    evidence_ids=("metadata:invented",),
                ),
            )
        }
    )
    with pytest.raises(UnknownEvidenceIdError):
        validate_decision_card(unknown_evidence, _packet())

    unknown_candidate = _card().model_copy(
        update={
            "candidate_explanations": (
                CandidateExplanation(
                    candidate_path="objects/invented.tif",
                    explanation="Not mechanically supplied.",
                    evidence_ids=("metadata:title",),
                ),
            )
        }
    )
    with pytest.raises(UnknownCandidatePathError):
        validate_decision_card(unknown_candidate, _packet())

    authority_claim = _card().model_copy(
        update={"uncertainty": "The proposal is approved."}
    )
    with pytest.raises(AuthorityClaimError):
        validate_decision_card(authority_claim, _packet())


def test_live_provider_uses_exact_responses_parse_shape_without_network() -> None:
    packet = _packet()
    fake_client = _FakeClient(_response(parsed=_card()))
    provider = LiveDecisionCardProvider(fake_client)

    result = asyncio.run(provider.generate(packet))

    assert result == _card()
    assert fake_client.responses.kwargs == {
        "model": "gpt-5.6",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": canonical_evidence_text(packet),
                    }
                ],
            }
        ],
        "instructions": DECISION_CARD_INSTRUCTIONS,
        "text_format": DecisionCard,
        "max_output_tokens": 1_800,
        "store": False,
        "timeout": 45.0,
    }
    assert provider.policy.sdk_max_retries == 0
    assert provider.last_record is not None
    assert provider.last_record.model == "gpt-5.6"
    assert provider.last_record.evidence_fingerprint == evidence_fingerprint(packet)
    assert provider.last_record.generated_at.utcoffset().total_seconds() == 7_200
    assert provider.last_record.usage.cached_input_tokens == 5
    assert provider.last_record.usage.estimated_cost_usd == pytest.approx(0.0028775)


def test_live_provider_factory_applies_bounded_sdk_retry_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    fake_client = _FakeClient(_response(parsed=_card()))

    def fake_async_openai(**kwargs: object) -> _FakeClient:
        captured.update(kwargs)
        return fake_client

    monkeypatch.setattr(provider_module, "AsyncOpenAI", fake_async_openai)

    provider = LiveDecisionCardProvider.from_api_key("test-only-placeholder")

    assert captured == {
        "api_key": "test-only-placeholder",
        "timeout": 45.0,
        "max_retries": 0,
    }
    assert provider.policy.max_output_tokens == 1_800


def test_live_provider_rejects_empty_local_key_configuration() -> None:
    with pytest.raises(LiveConfigurationError, match="locally"):
        LiveDecisionCardProvider.from_api_key("   ")


def test_live_provider_wraps_transport_failure_without_raw_output() -> None:
    provider = LiveDecisionCardProvider(_FailingClient())

    with pytest.raises(LiveTransportError, match="proposal remains unresolved"):
        asyncio.run(provider.generate(_packet()))

    assert provider.last_record is None


@pytest.mark.parametrize(
    ("response", "expected_error"),
    [
        (_response(parsed=_card(), status="incomplete"), LiveResponseStatusError),
        (
            _response(parsed=_card(), error=SimpleNamespace(code="provider_error")),
            LiveResponseStatusError,
        ),
        (
            _response(
                parsed=_card(),
                output=(
                    SimpleNamespace(
                        type="message",
                        content=(
                            SimpleNamespace(type="refusal", refusal="Cannot comply"),
                        ),
                    ),
                ),
            ),
            LiveRefusalError,
        ),
        (_response(parsed=None), LiveParsedOutputMissingError),
    ],
)
def test_live_provider_fails_closed_on_unusable_response(
    response: object,
    expected_error: type[Exception],
) -> None:
    provider = LiveDecisionCardProvider(_FakeClient(response))

    with pytest.raises(expected_error):
        asyncio.run(provider.generate(_packet()))

    assert provider.last_record is None


def test_recorded_replay_accepts_only_exact_evidence() -> None:
    packet = _packet()
    provider = RecordedReplayDecisionCardProvider(_record(packet).model_dump_json())

    assert asyncio.run(provider.generate(packet)) == _card()
    with pytest.raises(ReplayFingerprintMismatchError):
        asyncio.run(
            provider.generate(_packet(profile_description="Changed after recording"))
        )


@pytest.mark.parametrize(
    ("update", "expected_error"),
    [
        ({"model": "gpt-5.6-sol"}, ReplayModelMismatchError),
        ({"schema_version": "decision-card.v2"}, ReplaySchemaMismatchError),
    ],
)
def test_replay_loader_visibly_rejects_wrong_identity(
    update: dict[str, str],
    expected_error: type[Exception],
) -> None:
    payload = json.loads(_record().model_dump_json())
    payload.update(update)

    with pytest.raises(expected_error):
        load_recorded_decision_card(json.dumps(payload))


def test_replay_loader_rejects_missing_malformed_and_non_oslo_records() -> None:
    with pytest.raises(ReplayRecordInvalidError):
        load_recorded_decision_card("not-json")
    with pytest.raises(ReplayRecordInvalidError):
        load_recorded_decision_card(json.dumps({"model": "gpt-5.6"}))

    payload = json.loads(_record().model_dump_json())
    payload["generated_at"] = "2026-07-17T16:00:00+00:00"
    with pytest.raises(ReplayRecordInvalidError):
        load_recorded_decision_card(json.dumps(payload))


def test_provider_owned_models_are_strict_frozen_and_extra_forbidden() -> None:
    record = _record()
    with pytest.raises(ValidationError):
        record.generated_at = datetime.now(tz=oslo_tz)  # type: ignore[misc]

    payload: dict[str, Any] = record.model_dump(mode="python")
    payload["unexpected"] = True
    with pytest.raises(ReplayRecordInvalidError):
        load_recorded_decision_card(payload)
