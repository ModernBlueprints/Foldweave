"""Strict observable contracts for bounded folder-planner orchestration."""

from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import Field, JsonValue, model_validator

from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderAcceptedPlan,
    FolderPlan,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

MAX_RESPONSE_TURNS = 8
MAX_EVIDENCE_CALLS = 24
MAX_EVIDENCE_RESULT_BYTES = 16 * 1024
MAX_AGGREGATE_RESULT_BYTES = 128 * 1024
MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES = 512 * 1024
MAX_OUTPUT_TOKENS = 32_768
MAX_PLAN_SUBMISSIONS = 3
UNOBSERVED_LIVE_FAILURE_CODES = frozenset(
    {
        "provider_request_failed",
        "provider_origin_mismatch",
        "provider_response_error",
        "provider_response_invalid",
        "provider_timeout",
        "provider_transport_error",
        "provider_turn_incomplete",
    }
)


class PlannerInventoryFile(StrictFrozenModel):
    """Disclosed planner metadata for one source file, without raw digest data."""

    member_kind: Literal["regular_file"] = "regular_file"
    file_id: str = Field(pattern=SHA256_PATTERN)
    relative_path: str = Field(min_length=1, max_length=4_096)
    size: int = Field(ge=0)
    protected: bool
    evidence_eligible: bool


class ListInventoryPageCall(StrictFrozenModel):
    """Request one deterministic page of portable inventory metadata."""

    tool_name: Literal["list_inventory_page"] = "list_inventory_page"
    call_id: str = Field(min_length=1, max_length=128)
    cursor: str | None = Field(default=None, pattern=r"^inv:[a-f0-9]{16}:[0-9]+$")
    page_size: int = Field(default=50, ge=1, le=100)


class ReadTextExcerptCall(StrictFrozenModel):
    """Request one bounded excerpt by stable, evidence-eligible file ID."""

    tool_name: Literal["read_text_excerpt"] = "read_text_excerpt"
    call_id: str = Field(min_length=1, max_length=128)
    file_id: str = Field(pattern=SHA256_PATTERN)
    start_byte: int = Field(ge=0)
    max_bytes: int = Field(ge=1, le=MAX_EVIDENCE_RESULT_BYTES)


class InspectMarkdownLinksCall(StrictFrozenModel):
    """Request deterministic supported-link context for one Markdown file."""

    tool_name: Literal["inspect_markdown_links"] = "inspect_markdown_links"
    call_id: str = Field(min_length=1, max_length=128)
    file_id: str = Field(pattern=SHA256_PATTERN)
    cursor: str | None = Field(default=None, pattern=r"^links:[a-f0-9]{16}:[0-9]+$")
    page_size: int = Field(default=50, ge=1, le=100)


class SubmitPlanCall(StrictFrozenModel):
    """Submit one complete plan for deterministic compilation."""

    tool_name: Literal["submit_plan"] = "submit_plan"
    call_id: str = Field(min_length=1, max_length=128)
    plan: FolderPlan


class RequestClarificationCall(StrictFrozenModel):
    """Request the one allowed missing-intent answer."""

    tool_name: Literal["request_clarification"] = "request_clarification"
    call_id: str = Field(min_length=1, max_length=128)
    reason: Literal["missing_user_intent"] = "missing_user_intent"
    question: str = Field(min_length=1, max_length=1_000)
    missing_facts: tuple[str, ...] = Field(min_length=1, max_length=8)
    evidence_ids: tuple[str, ...] = Field(min_length=1, max_length=16)


PlannerToolCall = Annotated[
    ListInventoryPageCall
    | ReadTextExcerptCall
    | InspectMarkdownLinksCall
    | SubmitPlanCall
    | RequestClarificationCall,
    Field(discriminator="tool_name"),
]


class ProviderToolResponse(StrictFrozenModel):
    """One observable provider response containing declared tool calls."""

    kind: Literal["tool_calls"] = "tool_calls"
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model: str | None = Field(default=None, min_length=1, max_length=200)
    observable_output_items: tuple[JsonValue, ...] = ()
    tool_calls: tuple[PlannerToolCall, ...] = Field(min_length=1, max_length=24)

    @model_validator(mode="after")
    def require_one_terminal_shape(self) -> Self:
        _require_response_shape(
            provider_kind=self.provider_kind,
            returned_model=self.returned_model,
            blocker_code=None,
            tool_calls=self.tool_calls,
        )
        return self


class ProviderBlockedResponse(StrictFrozenModel):
    """One terminal provider-side blocker with no fabricated clarification."""

    kind: Literal["blocked"] = "blocked"
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model: str | None = Field(default=None, min_length=1, max_length=200)
    blocker_code: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    message: str = Field(min_length=1, max_length=2_000)
    observable_output_items: tuple[JsonValue, ...] = ()

    @model_validator(mode="after")
    def require_truthful_model_origin(self) -> Self:
        if self.provider_kind == "live" and self.returned_model is None:
            raise ValueError("A live blocker must record its returned model ID.")
        if self.provider_kind != "live" and self.returned_model is not None:
            raise ValueError(
                "Only a live blocker may claim a returned provider model ID."
            )
        return self


FolderProviderResponse = Annotated[
    ProviderToolResponse | ProviderBlockedResponse,
    Field(discriminator="kind"),
]


class EvidenceCallRecord(StrictFrozenModel):
    """One exact counted evidence-tool invocation and stable result."""

    response_turn: int = Field(ge=1, le=MAX_RESPONSE_TURNS)
    evidence_call_number: int = Field(ge=1, le=MAX_EVIDENCE_CALLS)
    call_id: str = Field(min_length=1, max_length=128)
    tool_name: Literal[
        "list_inventory_page",
        "read_text_excerpt",
        "inspect_markdown_links",
    ]
    arguments: JsonValue
    status: Literal["success", "rejected", "failed"]
    result: JsonValue | None = None
    error_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    truncated: bool
    cache_hit: bool
    byte_count: int = Field(ge=0, le=MAX_EVIDENCE_RESULT_BYTES)
    fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_result_binding(self) -> Self:
        if self.status == "success":
            if self.result is None or self.error_code is not None:
                raise ValueError("Successful evidence requires only a result.")
        elif self.result is not None or self.error_code is None:
            raise ValueError("Rejected or failed evidence requires only an error code.")
        payload = evidence_record_payload(self)
        if self.byte_count != len(canonical_json_bytes(payload["outcome"])):
            raise ValueError("Evidence byte count does not match its outcome bytes.")
        if self.fingerprint != canonical_sha256(payload):
            raise ValueError("Evidence-call fingerprint does not match its bytes.")
        return self


class FolderEvidenceLedger(StrictFrozenModel):
    """Complete path-neutral evidence authority for one planner session."""

    schema_version: Literal["folder-evidence-ledger.v1"] = "folder-evidence-ledger.v1"
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    initial_evidence: JsonValue
    initial_evidence_bytes: int = Field(
        ge=1,
        le=MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES,
    )
    records: tuple[EvidenceCallRecord, ...] = ()
    aggregate_result_bytes: int = Field(ge=0, le=MAX_AGGREGATE_RESULT_BYTES)
    total_outbound_evidence_bytes: int = Field(
        ge=1,
        le=MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES,
    )
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_ledger_binding(self) -> Self:
        if self.initial_evidence_bytes != len(
            canonical_json_bytes(self.initial_evidence)
        ):
            raise ValueError("Initial evidence byte count is not exact.")
        numbers = tuple(record.evidence_call_number for record in self.records)
        if numbers != tuple(range(1, len(self.records) + 1)):
            raise ValueError("Evidence records must use contiguous call numbers.")
        ordering = tuple(
            (record.response_turn, record.evidence_call_number)
            for record in self.records
        )
        if ordering != tuple(sorted(ordering)):
            raise ValueError("Evidence records must use turn/call order.")
        aggregate = sum(record.byte_count for record in self.records)
        if self.aggregate_result_bytes != aggregate:
            raise ValueError("Aggregate evidence-result bytes are not exact.")
        if (
            self.total_outbound_evidence_bytes
            != self.initial_evidence_bytes + aggregate
        ):
            raise ValueError("Total outbound evidence bytes are not exact.")
        if self.evidence_fingerprint != canonical_sha256(evidence_ledger_payload(self)):
            raise ValueError("Evidence-ledger fingerprint does not match its bytes.")
        return self


class PlannerCompilerFailure(StrictFrozenModel):
    """Stable mechanical feedback returned after one rejected plan."""

    submission_number: int = Field(ge=1, le=MAX_PLAN_SUBMISSIONS)
    code: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    detail: str = Field(min_length=1, max_length=2_000)


class PlannerObservableTurn(StrictFrozenModel):
    """One counted provider turn with only observable response material."""

    response_turn: int = Field(ge=1, le=MAX_RESPONSE_TURNS)
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model: str | None = Field(default=None, min_length=1, max_length=200)
    observable_output_items: tuple[JsonValue, ...]
    tool_calls: tuple[PlannerToolCall, ...] = Field(default=(), max_length=24)
    blocker_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    input_bytes: int = Field(ge=1, le=MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES)
    input_fingerprint: str = Field(pattern=SHA256_PATTERN)
    input_payload: JsonValue
    response_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_response_fingerprint(self) -> Self:
        _require_response_shape(
            provider_kind=self.provider_kind,
            returned_model=self.returned_model,
            blocker_code=self.blocker_code,
            tool_calls=self.tool_calls,
        )
        if self.input_bytes != len(canonical_json_bytes(self.input_payload)):
            raise ValueError("Observable response input byte count is not exact.")
        if self.input_fingerprint != canonical_sha256(self.input_payload):
            raise ValueError("Observable response input fingerprint is not exact.")
        if self.response_fingerprint != canonical_sha256(observable_turn_payload(self)):
            raise ValueError("Observable response fingerprint is not exact.")
        return self


class PlannerTurnHistoryItem(StrictFrozenModel):
    """Compact prior response passed forward without recursively repeating inputs."""

    response_turn: int = Field(ge=1, le=MAX_RESPONSE_TURNS)
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model: str | None = Field(default=None, min_length=1, max_length=200)
    observable_output_items: tuple[JsonValue, ...]
    tool_calls: tuple[PlannerToolCall, ...] = Field(default=(), max_length=24)
    blocker_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    response_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_valid_history_shape(self) -> Self:
        _require_response_shape(
            provider_kind=self.provider_kind,
            returned_model=self.returned_model,
            blocker_code=self.blocker_code,
            tool_calls=self.tool_calls,
        )
        return self


class PlannerEvidenceReservation(StrictFrozenModel):
    """One evidence invocation durably counted before local execution."""

    response_turn: int = Field(ge=1, le=MAX_RESPONSE_TURNS)
    tool_call_index: int = Field(ge=0, le=23)
    evidence_call_number: int = Field(ge=1, le=MAX_EVIDENCE_CALLS)
    call: Annotated[
        ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
        Field(discriminator="tool_name"),
    ]
    reservation_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_reservation(self) -> Self:
        if self.reservation_fingerprint != canonical_sha256(
            evidence_reservation_payload(self)
        ):
            raise ValueError("Evidence reservation fingerprint is not exact.")
        return self


class FolderPlannerProgress(StrictFrozenModel):
    """Restart-safe bounded planner state, excluding local filesystem authority."""

    schema_version: Literal["folder-planner-progress.v1"] = "folder-planner-progress.v1"
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    status: Literal["planning", "awaiting_clarification", "accepted", "blocked"]
    response_turns: int = Field(ge=0, le=MAX_RESPONSE_TURNS)
    pending_response_turn: int | None = Field(
        default=None,
        ge=1,
        le=MAX_RESPONSE_TURNS,
    )
    pending_response_input_bytes: int | None = Field(
        default=None,
        ge=1,
        le=MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES,
    )
    pending_response_input_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    pending_response_input_payload: JsonValue | None = None
    processing_response_turn: int | None = Field(
        default=None,
        ge=1,
        le=MAX_RESPONSE_TURNS,
    )
    processing_tool_call_index: int | None = Field(default=None, ge=0, le=23)
    pending_evidence_call: PlannerEvidenceReservation | None = None
    evidence_calls: int = Field(ge=0, le=MAX_EVIDENCE_CALLS)
    evidence_calls_observed: int = Field(ge=0, le=MAX_RESPONSE_TURNS * 24)
    outbound_evidence_bytes: int = Field(
        ge=0,
        le=MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES,
    )
    plan_submissions: int = Field(ge=0, le=MAX_PLAN_SUBMISSIONS)
    evidence_ledger: FolderEvidenceLedger
    turns: tuple[PlannerObservableTurn, ...] = ()
    compiler_failures: tuple[PlannerCompilerFailure, ...] = ()
    clarification_question: str | None = Field(
        default=None,
        min_length=1,
        max_length=1_000,
    )
    clarification_answer: str | None = Field(
        default=None,
        min_length=1,
        max_length=4_000,
    )
    accepted_plan: FolderAcceptedPlan | None = None
    blocker_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )

    @model_validator(mode="after")
    def require_state_consistency(self) -> Self:
        turn_numbers = tuple(turn.response_turn for turn in self.turns)
        if turn_numbers != tuple(range(1, len(self.turns) + 1)):
            raise ValueError("Observable turns must be contiguous and ordered.")
        expected_used = len(self.turns) + (1 if self.pending_response_turn else 0)
        if self.response_turns != expected_used:
            raise ValueError("Response-turn count does not match durable turn state.")
        if self.pending_response_turn is not None:
            if self.pending_response_turn != self.response_turns:
                raise ValueError("Pending turn must be the latest reserved turn.")
            if self.status != "planning":
                raise ValueError("Only planning progress may retain a pending turn.")
            if (
                self.pending_response_input_bytes is None
                or self.pending_response_input_fingerprint is None
                or self.pending_response_input_payload is None
            ):
                raise ValueError("A pending turn requires its exact input commitment.")
            if self.pending_response_input_bytes != len(
                canonical_json_bytes(self.pending_response_input_payload)
            ) or self.pending_response_input_fingerprint != canonical_sha256(
                self.pending_response_input_payload
            ):
                raise ValueError("Pending turn input commitment is not exact.")
        elif (
            self.pending_response_input_bytes is not None
            or self.pending_response_input_fingerprint is not None
            or self.pending_response_input_payload is not None
        ):
            raise ValueError("Only a pending turn may retain an input commitment.")
        expected_outbound = sum(turn.input_bytes for turn in self.turns) + (
            self.pending_response_input_bytes or 0
        )
        if self.outbound_evidence_bytes != expected_outbound:
            raise ValueError("Outbound byte total does not match durable turn inputs.")
        processing_fields = (
            self.processing_response_turn,
            self.processing_tool_call_index,
        )
        if (processing_fields[0] is None) != (processing_fields[1] is None):
            raise ValueError("Response-processing cursor fields must appear together.")
        if self.processing_response_turn is not None:
            if self.pending_response_turn is not None or not self.turns:
                raise ValueError("A response cursor requires one completed response.")
            turn = self.turns[-1]
            if (
                turn.response_turn != self.processing_response_turn
                or turn.blocker_code is not None
                or self.processing_tool_call_index >= len(turn.tool_calls)
            ):
                raise ValueError("Response-processing cursor is not executable.")
            if self.status not in {"planning", "blocked"}:
                raise ValueError("Only planning or failed processing retains a cursor.")
        if self.pending_evidence_call is not None:
            reservation = self.pending_evidence_call
            if self.processing_response_turn is None:
                raise ValueError("Evidence reservation requires a response cursor.")
            turn = self.turns[-1]
            if (
                reservation.response_turn != self.processing_response_turn
                or reservation.tool_call_index != self.processing_tool_call_index
                or turn.tool_calls[self.processing_tool_call_index] != reservation.call
            ):
                raise ValueError("Evidence reservation does not match the cursor.")
        if self.pending_evidence_call is not None and (
            self.status not in {"planning", "blocked"}
            or self.pending_response_turn is not None
        ):
            raise ValueError(
                "A pending evidence call requires completed-response processing."
            )
        expected_evidence_calls = len(self.evidence_ledger.records) + (
            1 if self.pending_evidence_call is not None else 0
        )
        if self.evidence_calls != expected_evidence_calls:
            raise ValueError("Evidence-call count does not match records/reservation.")
        if self.evidence_calls_observed < self.evidence_calls:
            raise ValueError("Observed evidence calls cannot be below executed calls.")
        if self.plan_submissions != len(self.compiler_failures) + (
            1 if self.accepted_plan is not None else 0
        ):
            raise ValueError("Plan-submission count is inconsistent.")
        if self.status == "awaiting_clarification":
            if (
                self.clarification_question is None
                or self.clarification_answer is not None
            ):
                raise ValueError("Awaiting clarification requires only one question.")
            if (
                not self.turns
                or not self.turns[-1].tool_calls
                or not isinstance(
                    self.turns[-1].tool_calls[0], RequestClarificationCall
                )
                or self.turns[-1].tool_calls[0].question.strip()
                != self.clarification_question
            ):
                raise ValueError(
                    "Awaiting clarification must derive from the latest tool call."
                )
        elif (
            self.clarification_question is not None
            and self.clarification_answer is None
        ):
            raise ValueError("A retained clarification question requires its answer.")
        if (
            self.clarification_answer is not None
            and self.clarification_question is None
        ):
            raise ValueError("A clarification answer requires its retained question.")
        if self.status == "accepted":
            if self.accepted_plan is None or self.blocker_code is not None:
                raise ValueError("Accepted progress requires only an accepted plan.")
            if (
                not self.turns
                or not self.turns[-1].tool_calls
                or not isinstance(self.turns[-1].tool_calls[0], SubmitPlanCall)
            ):
                raise ValueError("Accepted progress must follow a submitted plan.")
        elif self.accepted_plan is not None:
            raise ValueError("Only accepted progress may retain an accepted plan.")
        if self.status == "blocked":
            if self.blocker_code is None:
                raise ValueError("Blocked progress requires a stable blocker code.")
        elif self.blocker_code is not None:
            raise ValueError("Only blocked progress may retain a blocker code.")
        for index, turn in enumerate(self.turns):
            turn_input = _validate_turn_input_payload(turn.input_payload)
            if (
                turn_input.job_id != self.job_id
                or turn_input.provider_kind != self.provider_kind
                or turn.provider_kind != self.provider_kind
                or turn_input.response_turn != index + 1
                or turn_input.request_fingerprint
                != self.evidence_ledger.request_fingerprint
                or turn_input.source_commitment
                != self.evidence_ledger.source_commitment
                or turn_input.evidence_ledger.initial_evidence
                != self.evidence_ledger.initial_evidence
                or turn_input.evidence_ledger.initial_evidence_bytes
                != self.evidence_ledger.initial_evidence_bytes
                or turn_input.prior_turns
                != tuple(planner_history_item(item) for item in self.turns[:index])
                or turn_input.evidence_ledger.records
                != self.evidence_ledger.records[
                    : len(turn_input.evidence_ledger.records)
                ]
                or turn_input.compiler_failures
                != self.compiler_failures[: len(turn_input.compiler_failures)]
            ):
                raise ValueError("Observable turn input is not bound to this session.")
        if self.pending_response_input_payload is not None:
            pending_input = _validate_turn_input_payload(
                self.pending_response_input_payload
            )
            if (
                pending_input.job_id != self.job_id
                or pending_input.provider_kind != self.provider_kind
                or pending_input.response_turn != self.pending_response_turn
                or pending_input.request_fingerprint
                != self.evidence_ledger.request_fingerprint
                or pending_input.source_commitment
                != self.evidence_ledger.source_commitment
                or pending_input.evidence_ledger != self.evidence_ledger
                or pending_input.prior_turns
                != tuple(planner_history_item(item) for item in self.turns)
            ):
                raise ValueError("Pending turn input is not bound to this session.")
        return self


class FolderPlannerTurnInput(StrictFrozenModel):
    """Exact bounded input passed to one provider response turn."""

    schema_version: Literal["folder-planner-turn-input.v1"] = (
        "folder-planner-turn-input.v1"
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    response_turn: int = Field(ge=1, le=MAX_RESPONSE_TURNS)
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    tool_schema_version: Literal["folder-planner-tools.v1"] = "folder-planner-tools.v1"
    store: Literal[False] = False
    max_output_tokens: Literal[32768] = MAX_OUTPUT_TOKENS
    request: str = Field(min_length=1, max_length=8_000)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    evidence_ledger: FolderEvidenceLedger
    prior_turns: tuple[PlannerTurnHistoryItem, ...]
    compiler_failures: tuple[PlannerCompilerFailure, ...]
    clarification_question: str | None = None
    clarification_answer: str | None = None

    @model_validator(mode="after")
    def require_exact_bindings(self) -> Self:
        if self.request_fingerprint != request_fingerprint(self.request):
            raise ValueError("Turn request fingerprint does not match its text.")
        if self.request_fingerprint != self.evidence_ledger.request_fingerprint:
            raise ValueError("Turn request and evidence request fingerprints differ.")
        if self.source_commitment != self.evidence_ledger.source_commitment:
            raise ValueError("Turn request and evidence source commitments differ.")
        if len(self.prior_turns) != self.response_turn - 1:
            raise ValueError("Turn request must contain every prior observable turn.")
        prior_numbers = tuple(turn.response_turn for turn in self.prior_turns)
        if prior_numbers != tuple(range(1, self.response_turn)):
            raise ValueError("Prior observable turns must be contiguous and ordered.")
        if (
            self.clarification_answer is not None
            and self.clarification_question is None
        ):
            raise ValueError("A clarification answer requires its question.")
        return self


def evidence_record_payload(record: EvidenceCallRecord) -> dict[str, JsonValue]:
    """Return the record hash domain without its own fingerprint."""

    outcome: dict[str, JsonValue] = {
        "error_code": record.error_code,
        "result": record.result,
        "status": record.status,
        "truncated": record.truncated,
    }
    return {
        "arguments": record.arguments,
        "cache_hit": record.cache_hit,
        "call_id": record.call_id,
        "evidence_call_number": record.evidence_call_number,
        "outcome": outcome,
        "response_turn": record.response_turn,
        "tool_name": record.tool_name,
    }


def evidence_ledger_payload(ledger: FolderEvidenceLedger) -> dict[str, JsonValue]:
    """Return the ledger hash domain without its own fingerprint."""

    return {
        "aggregate_result_bytes": ledger.aggregate_result_bytes,
        "initial_evidence": ledger.initial_evidence,
        "initial_evidence_bytes": ledger.initial_evidence_bytes,
        "records": [record.model_dump(mode="json") for record in ledger.records],
        "request_fingerprint": ledger.request_fingerprint,
        "schema_version": ledger.schema_version,
        "source_commitment": ledger.source_commitment,
        "total_outbound_evidence_bytes": ledger.total_outbound_evidence_bytes,
    }


def observable_turn_payload(turn: PlannerObservableTurn) -> dict[str, JsonValue]:
    """Return the response hash domain without its own fingerprint."""

    return {
        "blocker_code": turn.blocker_code,
        "input_bytes": turn.input_bytes,
        "input_fingerprint": turn.input_fingerprint,
        "input_payload": turn.input_payload,
        "observable_output_items": list(turn.observable_output_items),
        "provider_kind": turn.provider_kind,
        "response_turn": turn.response_turn,
        "returned_model": turn.returned_model,
        "tool_calls": [call.model_dump(mode="json") for call in turn.tool_calls],
    }


def planner_history_item(turn: PlannerObservableTurn) -> PlannerTurnHistoryItem:
    """Project one durable response into the exact non-recursive provider history."""

    return PlannerTurnHistoryItem(
        response_turn=turn.response_turn,
        provider_kind=turn.provider_kind,
        returned_model=turn.returned_model,
        observable_output_items=turn.observable_output_items,
        tool_calls=turn.tool_calls,
        blocker_code=turn.blocker_code,
        response_fingerprint=turn.response_fingerprint,
    )


def _require_response_shape(
    *,
    provider_kind: Literal["deterministic", "live", "recorded_replay"],
    returned_model: str | None,
    blocker_code: str | None,
    tool_calls: tuple[PlannerToolCall, ...],
) -> None:
    """Share one strict response-shape authority across live and durable forms."""

    if blocker_code is not None:
        if tool_calls:
            raise ValueError("A blocked response cannot also retain tool calls.")
    elif not tool_calls:
        raise ValueError("A successful provider response requires a tool call.")
    terminal_calls = tuple(
        call
        for call in tool_calls
        if isinstance(call, SubmitPlanCall | RequestClarificationCall)
    )
    evidence_calls = tuple(
        call
        for call in tool_calls
        if isinstance(
            call,
            ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
        )
    )
    if terminal_calls and evidence_calls:
        raise ValueError(
            "A provider response cannot mix evidence and terminal tool calls."
        )
    if len(terminal_calls) > 1:
        raise ValueError("A provider response may contain one terminal call.")
    call_ids = tuple(call.call_id for call in tool_calls)
    if len(call_ids) != len(set(call_ids)):
        raise ValueError("Provider tool-call IDs must be unique per response.")
    if (
        provider_kind == "live"
        and returned_model is None
        and blocker_code not in UNOBSERVED_LIVE_FAILURE_CODES
    ):
        raise ValueError(
            "A live response must record its returned model ID unless the "
            "request failed before a provider response was observed."
        )
    if provider_kind != "live" and returned_model is not None:
        raise ValueError("Only a live response may claim a returned model ID.")


def _validate_turn_input_payload(payload: JsonValue) -> FolderPlannerTurnInput:
    """Validate one canonical JSON-mode provider input without type coercion."""

    return FolderPlannerTurnInput.model_validate_json(
        canonical_json_bytes(payload),
        strict=True,
    )


def evidence_reservation_payload(
    reservation: PlannerEvidenceReservation,
) -> dict[str, JsonValue]:
    """Return the reservation hash domain without its own fingerprint."""

    return {
        "call": reservation.call.model_dump(mode="json"),
        "evidence_call_number": reservation.evidence_call_number,
        "response_turn": reservation.response_turn,
        "tool_call_index": reservation.tool_call_index,
    }
