"""Human-owned family decisions and immutable resolved target maps."""

from __future__ import annotations

import unicodedata
from collections.abc import Iterator, Mapping
from enum import StrEnum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field, GetCoreSchemaHandler, model_validator
from pydantic_core import core_schema

from name_atlas.domain import ContentRole, TransformationStep
from name_atlas.proposals import (
    PathProposal,
    ProposalSource,
    ResolutionState,
    RiskCategory,
    VerificationState,
    edited_targets,
    refresh_collision_signals,
)

if TYPE_CHECKING:
    from name_atlas.package_import import ObjectFamily


class HumanAction(StrEnum):
    """The complete set of human authority states."""

    PENDING = "pending"
    APPROVED = "approved"
    EDITED = "edited"
    REFUSED = "refused"
    UNRESOLVED = "unresolved"


class FrozenRoleTargets(Mapping[ContentRole, str]):
    """Deeply immutable role-to-target map with deterministic serialization."""

    __slots__ = ("_mapping",)

    def __init__(self, values: Mapping[ContentRole, str]) -> None:
        self._mapping = dict(values)

    def __getitem__(self, key: ContentRole) -> str:
        return self._mapping[key]

    def __iter__(self) -> Iterator[ContentRole]:
        return iter(self._mapping)

    def __len__(self) -> int:
        return len(self._mapping)

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: object,
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        """Validate from a typed dict and serialize back to a JSON object."""

        del source_type
        mapping_schema = handler.generate_schema(dict[ContentRole, str])
        return core_schema.no_info_after_validator_function(
            cls,
            mapping_schema,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda value: dict(value),
                return_schema=mapping_schema,
            ),
        )


class HumanDecision(BaseModel):
    """One family-level human decision with a complete role-to-target map."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    family_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    action: HumanAction
    human_input: str | None
    resolved_targets: FrozenRoleTargets

    @model_validator(mode="after")
    def complete_state(self) -> HumanDecision:
        """Forbid partial or authority-inconsistent decision records."""

        resolved = self.action in {HumanAction.APPROVED, HumanAction.EDITED}
        if resolved and not self.resolved_targets:
            raise ValueError("Approved or edited decisions require resolved targets.")
        if not resolved and self.resolved_targets:
            raise ValueError("Unresolved or refused decisions cannot contain targets.")
        if self.action is HumanAction.EDITED and not self.human_input:
            raise ValueError("Edited decisions require the exact human descriptor.")
        if self.action is not HumanAction.EDITED and self.human_input is not None:
            raise ValueError("Only edited decisions may retain human descriptor input.")
        return self

    @property
    def export_ready(self) -> bool:
        """Return whether this human record supplies a complete target map."""

        return self.action in {HumanAction.APPROVED, HumanAction.EDITED}


class DecisionError(ValueError):
    """A proposed human decision fails the frozen transaction contract."""


def approve_family(
    family: ObjectFamily,
    proposals: tuple[PathProposal, ...],
    *,
    semantic_card_available: bool,
) -> HumanDecision:
    """Approve every role-specific proposed target as one atomic family action."""

    selected = _family_proposals(family, proposals)
    _require_resolvable(
        selected,
        semantic_card_available=semantic_card_available,
        allow_collision_resolution=False,
    )
    return HumanDecision(
        family_id=family.family_id,
        action=HumanAction.APPROVED,
        human_input=None,
        resolved_targets={
            proposal.role: proposal.proposed_relative_path for proposal in selected
        },
    )


def edit_family(
    family: ObjectFamily,
    proposals: tuple[PathProposal, ...],
    *,
    descriptor: str,
    semantic_card_available: bool,
    other_resolved_targets: tuple[str, ...] = (),
) -> HumanDecision:
    """Apply one exact human descriptor to every member in the family."""

    selected = _family_proposals(family, proposals)
    _require_resolvable(
        selected,
        semantic_card_available=semantic_card_available,
        allow_collision_resolution=True,
    )
    targets = edited_targets(family, descriptor)
    _require_unique_targets((*targets.values(), *other_resolved_targets))
    return HumanDecision(
        family_id=family.family_id,
        action=HumanAction.EDITED,
        human_input=descriptor,
        resolved_targets=targets,
    )


def refuse_family(family_id: str) -> HumanDecision:
    """Record an explicit human refusal without target authority."""

    return HumanDecision(
        family_id=family_id,
        action=HumanAction.REFUSED,
        human_input=None,
        resolved_targets={},
    )


def pending_family(family_id: str) -> HumanDecision:
    """Restore a provider-recovered family to human-pending state."""

    return HumanDecision(
        family_id=family_id,
        action=HumanAction.PENDING,
        human_input=None,
        resolved_targets={},
    )


def unresolved_family(family_id: str) -> HumanDecision:
    """Record a provider or evidence failure as explicitly unresolved."""

    return HumanDecision(
        family_id=family_id,
        action=HumanAction.UNRESOLVED,
        human_input=None,
        resolved_targets={},
    )


def proposals_after_decision(
    proposals: tuple[PathProposal, ...],
    decision: HumanDecision,
) -> tuple[PathProposal, ...]:
    """Return proposals with human and verification state updated, never hidden."""

    resolution = ResolutionState(decision.action.value)
    updated: list[PathProposal] = []
    for proposal in proposals:
        if proposal.family_id != decision.family_id:
            updated.append(proposal)
            continue
        update: dict[str, object] = {
            "human_resolution_state": resolution,
            "verification_state": (
                VerificationState.VERIFIED
                if decision.export_ready
                else VerificationState.BLOCKED
            ),
        }
        if decision.action is HumanAction.EDITED:
            target = decision.resolved_targets[proposal.role]
            update.update(
                {
                    "proposed_relative_path": target,
                    "proposal_source": ProposalSource.HUMAN_EDIT,
                    "transformation_steps": (
                        *proposal.transformation_steps,
                        TransformationStep(
                            operation="human_descriptor_edit",
                            before=proposal.proposed_relative_path,
                            after=target,
                        ),
                    ),
                    "risk_signals": tuple(
                        risk
                        for risk in proposal.risk_signals
                        if risk.category is not RiskCategory.COLLISION
                    ),
                }
            )
        updated.append(proposal.model_copy(update=update))
    return refresh_collision_signals(tuple(updated))


def _family_proposals(
    family: ObjectFamily,
    proposals: tuple[PathProposal, ...],
) -> tuple[PathProposal, ...]:
    selected = tuple(
        proposal for proposal in proposals if proposal.family_id == family.family_id
    )
    expected_roles = {
        ContentRole.ORIGINAL,
        *({ContentRole.ACCESS} if family.access is not None else set()),
        *({ContentRole.PRESERVATION} if family.preservation is not None else set()),
    }
    actual_roles = {proposal.role for proposal in selected}
    if actual_roles != expected_roles or len(selected) != len(expected_roles):
        raise DecisionError(
            f"Family {family.family_id} does not have one proposal per present role."
        )
    return selected


def _require_resolvable(
    proposals: tuple[PathProposal, ...],
    *,
    semantic_card_available: bool,
    allow_collision_resolution: bool,
) -> None:
    blocked_categories = {RiskCategory.POLICY, RiskCategory.LINKS}
    if not allow_collision_resolution:
        blocked_categories.add(RiskCategory.COLLISION)
    mechanical = [
        risk
        for proposal in proposals
        for risk in proposal.risk_signals
        if risk.category in blocked_categories
    ]
    if mechanical:
        raise DecisionError("Mechanical blockers must be resolved before approval.")
    has_meaning_risk = any(proposal.meaning_risks for proposal in proposals)
    if has_meaning_risk and not semantic_card_available:
        raise DecisionError(
            "A Meaning-risk family remains unresolved until a validated "
            "decision card exists."
        )


def _require_unique_targets(targets: tuple[str, ...]) -> None:
    comparisons = (
        ("exact", lambda value: value),
        ("NFC", lambda value: unicodedata.normalize("NFC", value)),
        (
            "NFC casefold",
            lambda value: unicodedata.normalize("NFC", value).casefold(),
        ),
    )
    for label, comparison in comparisons:
        keys = [comparison(target) for target in targets]
        if len(keys) != len(set(keys)):
            raise DecisionError(f"Resolved targets collide under {label} comparison.")
