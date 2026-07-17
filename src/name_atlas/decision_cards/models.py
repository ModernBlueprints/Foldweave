"""Immutable serialized contracts for GPT-5.6 generation and replay."""

from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator

from name_atlas.domain import DecisionCard, EvidencePacket

MODEL_ALIAS = "gpt-5.6"
DECISION_CARD_SCHEMA_VERSION = "decision-card.v1"
oslo_tz = ZoneInfo("Europe/Oslo")


class _StrictFrozenProviderModel(BaseModel):
    """Strict immutable base for provider-owned serialized data."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class CanonicalEvidenceEnvelope(_StrictFrozenProviderModel):
    """Complete cache and replay identity for one outbound evidence packet."""

    model: Literal["gpt-5.6"]
    schema_version: Literal["decision-card.v1"]
    packet: EvidencePacket


class LiveProviderPolicy(_StrictFrozenProviderModel):
    """Bounded SDK behavior for one live provider instance."""

    timeout_seconds: float = Field(ge=1.0, le=60.0)
    sdk_max_retries: int = Field(ge=0, le=2)
    max_output_tokens: int = Field(ge=256, le=4_000)


DEFAULT_LIVE_POLICY = LiveProviderPolicy(
    timeout_seconds=45.0,
    sdk_max_retries=0,
    max_output_tokens=1_800,
)


class ReplayUsage(_StrictFrozenProviderModel):
    """Sanitized usage facts retained with a recorded response."""

    input_tokens: int | None = Field(ge=0)
    cached_input_tokens: int | None = Field(ge=0)
    output_tokens: int | None = Field(ge=0)
    reasoning_tokens: int | None = Field(ge=0)
    total_tokens: int | None = Field(ge=0)
    latency_ms: float = Field(ge=0.0)
    estimated_cost_usd: float | None = Field(ge=0.0)


class RecordedDecisionCard(_StrictFrozenProviderModel):
    """One sanitized, evidence-bound real GPT-5.6 response for replay."""

    model: Literal["gpt-5.6"]
    schema_version: Literal["decision-card.v1"]
    evidence_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    generated_at: datetime
    decision_card: DecisionCard
    usage: ReplayUsage

    @field_validator("generated_at")
    @classmethod
    def require_oslo_aware_timestamp(cls, value: datetime) -> datetime:
        """Reject naive or non-Oslo-offset replay timestamps."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("generated_at must be timezone-aware")
        oslo_value = value.astimezone(oslo_tz)
        if value.utcoffset() != oslo_value.utcoffset():
            raise ValueError("generated_at must use the Europe/Oslo offset")
        return value
