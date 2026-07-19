"""Provider boundary and deterministic scripted provider for planner turns."""

from __future__ import annotations

from typing import Literal, Protocol, runtime_checkable

from pydantic import Field

from name_atlas.folder_refactor.contracts import (
    FolderPlan,
    FolderPlanEntry,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    FolderProviderResponse,
    PlannerInventoryFile,
    ProviderBlockedResponse,
    ProviderToolResponse,
    SubmitPlanCall,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    request_fingerprint,
)

DETERMINISTIC_DEVELOPMENT_REQUEST = (
    "Prepare this project for handoff. Keep every file and every supported "
    "Markdown link working."
)


class PlannerProviderError(RuntimeError):
    """A provider turn could not produce an observable response."""


class PlannerProviderTransportError(PlannerProviderError):
    """The declared provider transport failed before a response was available."""


class PlannerProviderTimeoutError(PlannerProviderTransportError):
    """The declared provider turn reached its timeout."""


class PlannerProviderResponseError(PlannerProviderError):
    """The provider rejected or failed the turn outside the response contract."""


class ScriptedProviderExhaustedError(PlannerProviderError):
    """A caller attempted a turn beyond the exact scripted sequence."""


class ScriptedProviderExceptionOutcome(StrictFrozenModel):
    """One declared exception consumed by exactly one scripted exchange."""

    kind: Literal["exception"] = "exception"
    error_kind: Literal["transport", "timeout", "provider"]
    message: str = Field(min_length=1, max_length=2_000)


ScriptedProviderOutcome = (
    ProviderToolResponse | ProviderBlockedResponse | ScriptedProviderExceptionOutcome
)


@runtime_checkable
class PlannerProvider(Protocol):
    """Exchange one exact bounded input for one observable provider response."""

    @property
    def provider_kind(self) -> Literal["deterministic", "live", "recorded_replay"]:
        """Return the truthful origin used for persisted turn metadata."""
        ...

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        """Return the append-only live usage prefix, or an empty tuple."""

        ...

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        """Perform exactly one provider turn with no implicit retry."""
        ...


class ScriptedPlannerProvider:
    """Consume an immutable response/exception script in exact call order."""

    def __init__(
        self,
        outcomes: tuple[ScriptedProviderOutcome, ...],
        *,
        provider_kind: Literal["deterministic", "recorded_replay"] = "deterministic",
    ) -> None:
        if type(outcomes) is not tuple:
            raise TypeError("Scripted provider outcomes must be an exact tuple.")
        allowed = (
            ProviderToolResponse,
            ProviderBlockedResponse,
            ScriptedProviderExceptionOutcome,
        )
        if any(not isinstance(outcome, allowed) for outcome in outcomes):
            raise TypeError(
                "Every scripted outcome must be a strict provider response or "
                "declared exception outcome."
            )
        mismatched = tuple(
            outcome
            for outcome in outcomes
            if isinstance(outcome, ProviderToolResponse | ProviderBlockedResponse)
            and outcome.provider_kind != provider_kind
        )
        if mismatched:
            raise ValueError(
                "Every scripted provider response must use the script's "
                "truthful origin."
            )
        self._outcomes = outcomes
        self._provider_kind = provider_kind
        self._next_index = 0
        self._received_inputs: list[FolderPlannerTurnInput] = []

    @property
    def provider_kind(self) -> Literal["deterministic", "recorded_replay"]:
        """Return the fixed truthful origin of this script."""

        return self._provider_kind

    @property
    def received_inputs(self) -> tuple[FolderPlannerTurnInput, ...]:
        """Return the exact immutable inputs for consumed scripted turns."""

        return tuple(self._received_inputs)

    @property
    def consumed_count(self) -> int:
        """Return the number of outcomes consumed, including declared failures."""

        return self._next_index

    @property
    def remaining_count(self) -> int:
        """Return the number of outcomes still available."""

        return len(self._outcomes) - self._next_index

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        """Consume one outcome; never retry, skip, or synthesize another turn."""

        if not isinstance(turn_input, FolderPlannerTurnInput):
            raise TypeError("Planner provider input must be FolderPlannerTurnInput.")
        if self._next_index >= len(self._outcomes):
            raise ScriptedProviderExhaustedError(
                "Scripted provider has no remaining outcome; no turn was consumed."
            )

        outcome = self._outcomes[self._next_index]
        self._next_index += 1
        self._received_inputs.append(turn_input)

        if isinstance(outcome, ScriptedProviderExceptionOutcome):
            _raise_declared_exception(outcome)
        return outcome


class DeterministicDevelopmentPlannerProvider:
    """Stateless A2 provider that submits one complete mechanical plan."""

    def __init__(
        self,
        *,
        result_folder_name: str = "name-atlas-organized-copy",
        target_prefix: str = "organized",
        allowed_request: str = DETERMINISTIC_DEVELOPMENT_REQUEST,
    ) -> None:
        if not allowed_request or allowed_request != allowed_request.strip():
            raise ValueError(
                "The deterministic development request must be nonempty and trimmed."
            )
        self._result_folder_name = result_folder_name
        self._target_prefix = target_prefix
        self._allowed_request = allowed_request
        self._allowed_request_fingerprint = request_fingerprint(allowed_request)
        self.invocation_count = 0

    @property
    def provider_kind(self) -> Literal["deterministic"]:
        return "deterministic"

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> FolderProviderResponse:
        """Derive a complete path-only plan from the persisted initial inventory."""

        self.invocation_count += 1
        if (
            turn_input.request != self._allowed_request
            or turn_input.request_fingerprint != self._allowed_request_fingerprint
        ):
            return ProviderBlockedResponse(
                provider_kind="deterministic",
                blocker_code="deterministic_request_not_recorded",
                message=(
                    "This deterministic development planner is bound to its exact "
                    "declared demonstration request. Arbitrary plain-English "
                    "planning requires the live GPT-5.6 provider."
                ),
                observable_output_items=(
                    {
                        "type": "deterministic_request_blocked",
                        "response_turn": turn_input.response_turn,
                    },
                ),
            )
        initial = turn_input.evidence_ledger.initial_evidence
        if not isinstance(initial, dict) or not isinstance(initial.get("files"), list):
            raise PlannerProviderResponseError(
                "Deterministic provider initial inventory is malformed."
            )
        try:
            files = tuple(
                PlannerInventoryFile.model_validate_json(
                    canonical_json_bytes(item),
                    strict=True,
                )
                for item in initial["files"]
            )
        except (TypeError, ValueError) as exc:
            raise PlannerProviderResponseError(
                "Deterministic provider could not parse the initial inventory."
            ) from exc
        plan = FolderPlan(
            source_commitment=turn_input.source_commitment,
            request_fingerprint=request_fingerprint(turn_input.request),
            request_scope="rename_and_move_every_file",
            evidence_fingerprint=turn_input.evidence_ledger.evidence_fingerprint,
            result_folder_name=self._result_folder_name,
            entries=tuple(
                FolderPlanEntry(
                    file_id=item.file_id,
                    original_path=item.relative_path,
                    proposed_target=f"{self._target_prefix}/{item.relative_path}",
                    rationale=(
                        "Deterministic A2 development path; live GPT-5.6 "
                        "planning is introduced at A4."
                    ),
                    evidence_ids=("initial_inventory",),
                )
                for item in files
                if not item.protected
            ),
            exclusions=(),
        )
        return ProviderToolResponse(
            provider_kind="deterministic",
            observable_output_items=(
                {
                    "type": "deterministic_development_plan",
                    "response_turn": turn_input.response_turn,
                },
            ),
            tool_calls=(
                SubmitPlanCall(
                    call_id=f"deterministic-plan-{turn_input.response_turn}",
                    plan=plan,
                ),
            ),
        )


def _raise_declared_exception(outcome: ScriptedProviderExceptionOutcome) -> None:
    if outcome.error_kind == "transport":
        raise PlannerProviderTransportError(outcome.message)
    if outcome.error_kind == "timeout":
        raise PlannerProviderTimeoutError(outcome.message)
    raise PlannerProviderResponseError(outcome.message)
