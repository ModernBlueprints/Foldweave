"""Live GPT-5.6 and recorded-replay DecisionCard providers."""

import json
from collections.abc import Mapping
from datetime import datetime
from time import perf_counter
from typing import Any, Protocol, cast

from openai import AsyncOpenAI
from pydantic import ValidationError

from name_atlas.domain import DecisionCard, EvidencePacket

from .errors import (
    LiveConfigurationError,
    LiveParsedOutputMissingError,
    LiveRefusalError,
    LiveResponseStatusError,
    LiveTransportError,
    ReplayFingerprintMismatchError,
    ReplayModelMismatchError,
    ReplayRecordInvalidError,
    ReplaySchemaMismatchError,
)
from .evidence import (
    canonical_evidence_text,
    evidence_fingerprint,
    validate_decision_card,
)
from .models import (
    DECISION_CARD_SCHEMA_VERSION,
    DEFAULT_LIVE_POLICY,
    MODEL_ALIAS,
    LiveProviderPolicy,
    RecordedDecisionCard,
    ReplayUsage,
    oslo_tz,
)

DECISION_CARD_INSTRUCTIONS = (
    "You are producing a neutral decision card for a human archivist. "
    "Use only the canonical evidence JSON supplied by the application. "
    "Explain possible interpretations and possible meaning loss, cite only "
    "supplied evidence IDs, and explain only supplied candidate paths. State "
    "uncertainty plainly and ask exactly one discriminating human question. "
    "Never approve, verify, certify, choose, or finalize a path. Never claim "
    "that a proposal is safe, correct, exportable, or semantically true. "
    "Return only the DecisionCard structured output."
)

STANDARD_INPUT_USD_PER_MILLION = 5.0
STANDARD_CACHED_INPUT_USD_PER_MILLION = 0.5
STANDARD_OUTPUT_USD_PER_MILLION = 30.0


class _ResponsesResource(Protocol):
    async def parse(self, **kwargs: object) -> object:
        """Return an OpenAI parsed response."""


class _AsyncResponsesClient(Protocol):
    responses: _ResponsesResource


def _has_refusal(response: object) -> bool:
    for output_item in cast(Any, getattr(response, "output", ()) or ()):
        if getattr(output_item, "type", None) == "refusal":
            return True
        for content_item in getattr(output_item, "content", ()) or ():
            if getattr(content_item, "type", None) == "refusal":
                return True
            if getattr(content_item, "refusal", None):
                return True
    return False


def _optional_nonnegative_int(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _usage_from_response(response: object, latency_ms: float) -> ReplayUsage:
    usage = getattr(response, "usage", None)
    input_details = getattr(usage, "input_tokens_details", None)
    output_details = getattr(usage, "output_tokens_details", None)
    input_tokens = _optional_nonnegative_int(getattr(usage, "input_tokens", None))
    cached_input_tokens = _optional_nonnegative_int(
        getattr(input_details, "cached_tokens", None)
    )
    output_tokens = _optional_nonnegative_int(getattr(usage, "output_tokens", None))
    estimated_cost_usd = _estimate_standard_cost(
        input_tokens=input_tokens,
        cached_input_tokens=cached_input_tokens,
        output_tokens=output_tokens,
    )
    return ReplayUsage(
        input_tokens=input_tokens,
        cached_input_tokens=cached_input_tokens,
        output_tokens=output_tokens,
        reasoning_tokens=_optional_nonnegative_int(
            getattr(output_details, "reasoning_tokens", None)
        ),
        total_tokens=_optional_nonnegative_int(getattr(usage, "total_tokens", None)),
        latency_ms=latency_ms,
        estimated_cost_usd=estimated_cost_usd,
    )


def _estimate_standard_cost(
    *,
    input_tokens: int | None,
    cached_input_tokens: int | None,
    output_tokens: int | None,
) -> float | None:
    """Estimate standard GPT-5.6 Sol token cost from reported usage."""

    if input_tokens is None or output_tokens is None:
        return None
    cached = cached_input_tokens or 0
    if cached > input_tokens:
        return None
    uncached = input_tokens - cached
    return (
        uncached * STANDARD_INPUT_USD_PER_MILLION
        + cached * STANDARD_CACHED_INPUT_USD_PER_MILLION
        + output_tokens * STANDARD_OUTPUT_USD_PER_MILLION
    ) / 1_000_000


class LiveDecisionCardProvider:
    """Bounded live provider using the official async Responses API."""

    provider_kind = "live"

    def __init__(
        self,
        client: _AsyncResponsesClient,
        *,
        policy: LiveProviderPolicy = DEFAULT_LIVE_POLICY,
    ) -> None:
        self._client = client
        self.policy = policy
        self.last_record: RecordedDecisionCard | None = None

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        *,
        policy: LiveProviderPolicy = DEFAULT_LIVE_POLICY,
    ) -> "LiveDecisionCardProvider":
        """Create a provider with bounded SDK timeout and retry settings."""

        if not api_key.strip():
            raise LiveConfigurationError(
                "Configure OPENAI_API_KEY locally before using the live provider."
            )
        client = AsyncOpenAI(
            api_key=api_key,
            timeout=policy.timeout_seconds,
            max_retries=policy.sdk_max_retries,
        )
        return cls(client, policy=policy)

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        """Generate, validate, and retain a sanitized replay record."""

        outbound_text = canonical_evidence_text(packet)
        fingerprint = evidence_fingerprint(packet)
        started = perf_counter()
        try:
            response = await self._client.responses.parse(
                model=MODEL_ALIAS,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": outbound_text,
                            }
                        ],
                    }
                ],
                instructions=DECISION_CARD_INSTRUCTIONS,
                text_format=DecisionCard,
                max_output_tokens=self.policy.max_output_tokens,
                store=False,
                timeout=self.policy.timeout_seconds,
            )
        except Exception as exc:
            raise LiveTransportError(
                "GPT-5.6 request failed; the proposal remains unresolved."
            ) from exc

        latency_ms = (perf_counter() - started) * 1_000
        if getattr(response, "error", None) is not None:
            raise LiveResponseStatusError(
                "GPT-5.6 returned an error; the proposal remains unresolved."
            )
        if getattr(response, "status", None) != "completed":
            raise LiveResponseStatusError(
                "GPT-5.6 response was not completed; the proposal remains unresolved."
            )
        if _has_refusal(response):
            raise LiveRefusalError(
                "GPT-5.6 refused the request; the proposal remains unresolved."
            )

        parsed = getattr(response, "output_parsed", None)
        if parsed is None:
            raise LiveParsedOutputMissingError(
                "GPT-5.6 returned no parsed DecisionCard; "
                "the proposal remains unresolved."
            )
        card = validate_decision_card(parsed, packet)
        self.last_record = RecordedDecisionCard(
            model=MODEL_ALIAS,
            schema_version=DECISION_CARD_SCHEMA_VERSION,
            evidence_fingerprint=fingerprint,
            generated_at=datetime.now(tz=oslo_tz),
            decision_card=card,
            usage=_usage_from_response(response, latency_ms),
        )
        return card


def load_recorded_decision_card(
    value: str | bytes | bytearray | Mapping[str, object] | RecordedDecisionCard,
) -> RecordedDecisionCard:
    """Load a replay record with explicit model and schema mismatch failures."""

    if isinstance(value, RecordedDecisionCard):
        return value

    parsed_json: object | None = None
    if isinstance(value, (str, bytes, bytearray)):
        try:
            parsed_json = json.loads(value)
        except (json.JSONDecodeError, UnicodeDecodeError, TypeError) as exc:
            raise ReplayRecordInvalidError(
                "Recorded GPT-5.6 response is not valid JSON."
            ) from exc
        candidate = parsed_json
    else:
        candidate = value

    if not isinstance(candidate, Mapping):
        raise ReplayRecordInvalidError(
            "Recorded GPT-5.6 response must be a JSON object."
        )
    if "model" not in candidate or "schema_version" not in candidate:
        raise ReplayRecordInvalidError(
            "Recorded GPT-5.6 response is missing model or schema_version."
        )
    if candidate["model"] != MODEL_ALIAS:
        raise ReplayModelMismatchError(f"Replay model must be exactly {MODEL_ALIAS}.")
    if candidate["schema_version"] != DECISION_CARD_SCHEMA_VERSION:
        raise ReplaySchemaMismatchError(
            f"Replay schema must be exactly {DECISION_CARD_SCHEMA_VERSION}."
        )

    try:
        if isinstance(value, (str, bytes, bytearray)):
            return RecordedDecisionCard.model_validate_json(value)
        return RecordedDecisionCard.model_validate(candidate)
    except ValidationError as exc:
        raise ReplayRecordInvalidError(
            "Recorded GPT-5.6 response failed schema validation."
        ) from exc


class RecordedReplayDecisionCardProvider:
    """Evidence-bound provider for one real, recorded GPT-5.6 response."""

    provider_kind = "replay"

    def __init__(
        self,
        record: str | bytes | bytearray | Mapping[str, object] | RecordedDecisionCard,
    ) -> None:
        self.record = load_recorded_decision_card(record)

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        """Return the recorded card only for its exact canonical evidence."""

        expected_fingerprint = evidence_fingerprint(packet)
        if self.record.evidence_fingerprint != expected_fingerprint:
            raise ReplayFingerprintMismatchError(
                "Recorded GPT-5.6 response does not match the outbound evidence."
            )
        return validate_decision_card(self.record.decision_card, packet)
