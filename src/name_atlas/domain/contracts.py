"""Serialized contracts at product and provider boundaries."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictFrozenModel(BaseModel):
    """Fail-closed base for immutable serialized contracts."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class RunMode(StrEnum):
    """Supported decision-card provider modes."""

    REPLAY = "replay"
    LIVE = "live"


class ContentRole(StrEnum):
    """Role of one content object inside its stable family."""

    ORIGINAL = "original"
    ACCESS = "access"
    PRESERVATION = "preservation"


class MemberKind(StrEnum):
    """Supported source-package member kinds."""

    CONTENT_OBJECT = "content_object"
    DECLARED_CONTROL_FILE = "declared_control_file"


class EvidenceRef(StrictFrozenModel):
    """One bounded piece of text supplied to a decision-card provider."""

    evidence_id: str = Field(min_length=1, max_length=128)
    label: str = Field(min_length=1, max_length=128)
    value: str = Field(max_length=4_000)


class TransformationStep(StrictFrozenModel):
    """One deterministic path transformation."""

    operation: str = Field(min_length=1, max_length=128)
    before: str = Field(max_length=1_024)
    after: str = Field(max_length=1_024)


class EvidencePacket(StrictFrozenModel):
    """The complete bounded outbound text contract for GPT-5.6."""

    family_id: str = Field(min_length=64, max_length=64, pattern=r"^[a-f0-9]{64}$")
    original_paths: tuple[str, ...] = Field(min_length=1)
    proposed_paths: tuple[str, ...] = Field(min_length=1)
    transformation_steps: tuple[TransformationStep, ...] = Field(min_length=1)
    candidate_paths: tuple[str, ...] = ()
    neighboring_paths: tuple[str, ...] = ()
    path_evidence: tuple[EvidenceRef, ...] = ()
    metadata_evidence: tuple[EvidenceRef, ...] = ()
    derivative_evidence: tuple[EvidenceRef, ...] = ()
    risk_signals: tuple[str, ...] = Field(min_length=1)
    profile_description: str = Field(min_length=1, max_length=4_000)


class LinkedObservation(StrictFrozenModel):
    """A model observation explicitly linked to supplied evidence."""

    text: str = Field(min_length=1, max_length=2_000)
    evidence_ids: tuple[str, ...] = Field(min_length=1)


class CandidateExplanation(StrictFrozenModel):
    """Neutral explanation of a mechanically supplied candidate path."""

    candidate_path: str = Field(min_length=1, max_length=1_024)
    explanation: str = Field(min_length=1, max_length=2_000)
    evidence_ids: tuple[str, ...] = Field(min_length=1)


class DecisionCard(StrictFrozenModel):
    """Advisory output with no approval or verification authority."""

    possible_interpretations: tuple[LinkedObservation, ...] = Field(min_length=1)
    possible_meaning_loss: tuple[LinkedObservation, ...] = Field(min_length=1)
    uncertainty: str = Field(min_length=1, max_length=2_000)
    why_the_distinction_matters: str = Field(min_length=1, max_length=2_000)
    discriminating_question: str = Field(min_length=1, max_length=1_000)
    candidate_explanations: tuple[CandidateExplanation, ...]


class PackageValidationResult(StrictFrozenModel):
    """Product-independent result returned by a BagIt validator boundary."""

    validator: Literal["bagit"]
    valid: bool
    messages: tuple[str, ...] = ()
