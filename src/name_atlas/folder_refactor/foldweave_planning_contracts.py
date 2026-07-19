"""Truthful composite planning contracts for Foldweave review-era jobs."""

from __future__ import annotations

import uuid
from typing import Literal, Protocol, Self, runtime_checkable

from pydantic import Field, JsonValue, field_validator, model_validator

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.contracts import SHA256_PATTERN, StrictFrozenModel
from name_atlas.folder_refactor.naming import validate_target_path
from name_atlas.folder_refactor.receipt_contracts import (
    FolderEvidenceLedger,
    FolderPlannerUsage,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

FOLDWEAVE_PLANNER_CONTRACT_VERSION = "foldweave-planner-contract.v1"
FOLDWEAVE_F0B_CONTRACT_FREEZE_VERSION = "foldweave-f0b-contract-freeze.v1"
FOLDWEAVE_F0B_REPLAY_SCHEMA_VERSION = "folder-planner-replay.v2"
FOLDWEAVE_F0B_REPLAY_FINGERPRINT_DOMAIN = "foldweave:folder-planner-replay:v2"
FOLDWEAVE_F0B_REPLAY_FIXTURE_DOMAIN = "foldweave:folder-planner-replay-fixture:v2"
FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH = (
    "initial_plan",
    "initial_review",
    "sparse_revision",
    "revised_review",
    "exact_acceptance",
    "execution_and_verification",
)
MAX_FOLDWEAVE_REVISIONS = 2


class FoldweaveF0bContractFreezeV1(StrictFrozenModel):
    """One pre-call identity for every F0b planning qualification surface."""

    schema_version: Literal["foldweave-f0b-contract-freeze.v1"] = (
        FOLDWEAVE_F0B_CONTRACT_FREEZE_VERSION
    )
    initial_prompt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    initial_tools_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_prompt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_tools_fingerprint: str = Field(pattern=SHA256_PATTERN)
    preview_review_contract_fingerprint: str = Field(pattern=SHA256_PATTERN)
    derivative_planning_contract_fingerprint: str = Field(pattern=SHA256_PATTERN)
    qualification_provider_profile_fingerprint: str = Field(pattern=SHA256_PATTERN)
    replay_schema_version: Literal["folder-planner-replay.v2"] = (
        FOLDWEAVE_F0B_REPLAY_SCHEMA_VERSION
    )
    replay_envelope_identity_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_schema_version: Literal["folder-evidence-ledger.v2"] = (
        "folder-evidence-ledger.v2"
    )
    evidence_envelope_contract_fingerprint: str = Field(pattern=SHA256_PATTERN)
    fixture_name: Literal["sofia-apollo-native-root-review.v1"]
    fixture_fingerprint: str = Field(pattern=SHA256_PATTERN)
    qualification_call_graph: tuple[str, ...] = Field(min_length=6, max_length=6)
    initial_provider_attempts_min: Literal[2] = 2
    initial_provider_attempts_max: Literal[3] = 3
    revision_provider_attempts: Literal[1] = 1
    total_provider_attempts_min: Literal[3] = 3
    total_provider_attempts_max: Literal[4] = 4
    qualification_call_graph_fingerprint: str = Field(pattern=SHA256_PATTERN)
    contract_freeze_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_pre_call_freeze(self) -> Self:
        if self.qualification_call_graph != FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH:
            raise ValueError("F0b qualification call graph is not the frozen graph.")
        if not (
            self.total_provider_attempts_min
            == self.initial_provider_attempts_min + self.revision_provider_attempts
            and self.total_provider_attempts_max
            == self.initial_provider_attempts_max + self.revision_provider_attempts
        ):
            raise ValueError("F0b qualification attempt bounds are inconsistent.")
        call_graph_payload = {
            "domain": "foldweave:f0b:qualification-call-graph:v1",
            "nodes": self.qualification_call_graph,
            "initial_provider_attempts_min": self.initial_provider_attempts_min,
            "initial_provider_attempts_max": self.initial_provider_attempts_max,
            "revision_provider_attempts": self.revision_provider_attempts,
            "total_provider_attempts_min": self.total_provider_attempts_min,
            "total_provider_attempts_max": self.total_provider_attempts_max,
        }
        if self.qualification_call_graph_fingerprint != canonical_sha256(
            call_graph_payload
        ):
            raise ValueError("F0b qualification call-graph fingerprint is invalid.")
        payload = self.model_dump(mode="json", exclude={"contract_freeze_fingerprint"})
        if self.contract_freeze_fingerprint != canonical_sha256(payload):
            raise ValueError("F0b composite contract-freeze fingerprint is invalid.")
        return self


class FolderPlanRevisionEntryV1(StrictFrozenModel):
    """One exact sparse replacement proposed by a planning host."""

    file_id: str = Field(pattern=SHA256_PATTERN)
    replacement_target_path: str = Field(min_length=1, max_length=1_024)
    rationale: str = Field(min_length=1, max_length=1_000)
    evidence_ids: tuple[str, ...] = Field(min_length=1, max_length=16)

    @model_validator(mode="after")
    def require_bounded_entry(self) -> Self:
        validate_target_path(
            self.replacement_target_path,
            original_path=self.replacement_target_path,
            protected=False,
        )
        if self.evidence_ids != tuple(sorted(set(self.evidence_ids))):
            raise ValueError("Revision evidence IDs must be sorted and unique.")
        return self


class FolderPlanRevisionV1(StrictFrozenModel):
    """Strict sparse model output bound to one visible candidate."""

    schema_version: Literal["folder-plan-revision.v1"] = "folder-plan-revision.v1"
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    replacement_result_folder_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=240,
    )
    entries: tuple[FolderPlanRevisionEntryV1, ...] = Field(default=(), max_length=500)

    @model_validator(mode="after")
    def require_sparse_sorted_entries(self) -> Self:
        if self.replacement_result_folder_name is None and not self.entries:
            raise ValueError(
                "Sparse revision requires a result-name or file-path replacement."
            )
        file_ids = tuple(entry.file_id for entry in self.entries)
        if file_ids != tuple(sorted(file_ids)) or len(file_ids) != len(set(file_ids)):
            raise ValueError(
                "Sparse revision entries must be file-ID sorted and unique."
            )
        return self


class FolderPlannerRevisionTurnInputV1(StrictFrozenModel):
    """Exact bounded input to one sparse revision provider turn."""

    schema_version: Literal["folder-planner-revision-turn-input.v1"] = (
        "folder-planner-revision-turn-input.v1"
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    expected_job_revision: int = Field(ge=0)
    proposal_revision: int = Field(ge=0, lt=MAX_FOLDWEAVE_REVISIONS)
    response_turn: int = Field(ge=2, le=8)
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    store: Literal[False] = False
    max_output_tokens: Literal[8192] = 8192
    request: str = Field(min_length=1, max_length=8_000)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    revision_instruction: str = Field(min_length=1, max_length=20_000)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_candidate: FolderAcceptedPlanV2
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    prior_transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)
    turn_contract_freeze_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    immediate_parent_candidate_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError(
                "Revision job ID must be lowercase UUID4 hexadecimal text."
            )
        return value

    @model_validator(mode="after")
    def require_exact_bindings(self) -> Self:
        if (
            self.turn_contract_freeze_fingerprint is None
            and "turn_contract_freeze_fingerprint" in self.model_fields_set
        ):
            raise ValueError(
                "Revision contract freeze may be omitted only by a historical record."
            )
        if self.request_fingerprint != request_fingerprint(self.request):
            raise ValueError("Revision request fingerprint does not match its text.")
        if self.source_commitment != self.base_candidate.source_commitment:
            raise ValueError("Revision candidate targets another source commitment.")
        if self.request_fingerprint != self.base_candidate.request_fingerprint:
            raise ValueError("Revision candidate targets another user request.")
        if self.evidence_fingerprint != self.base_candidate.evidence_fingerprint:
            raise ValueError("Revision candidate targets another evidence authority.")
        if self.base_candidate_fingerprint != canonical_sha256(self.base_candidate):
            raise ValueError("Revision base candidate fingerprint is invalid.")
        if (self.imported_change_file_fingerprint is None) != (
            self.match_report_fingerprint is None
        ):
            raise ValueError("Derivative revision requires both imported bindings.")
        return self


def canonical_revision_turn_input_payload(
    turn_input: FolderPlannerRevisionTurnInputV1,
) -> dict[str, JsonValue]:
    """Return the exact new or historical revision-input hash payload."""

    payload = turn_input.model_dump(mode="json")
    if turn_input.turn_contract_freeze_fingerprint is None:
        if "turn_contract_freeze_fingerprint" in turn_input.model_fields_set:
            raise ValueError("Explicit null revision contract freeze is invalid.")
        payload.pop("turn_contract_freeze_fingerprint", None)
    return payload


def canonical_revision_turn_input_bytes(
    turn_input: FolderPlannerRevisionTurnInputV1,
) -> bytes:
    """Serialize one revision input without changing historical omissions."""

    return canonical_json_bytes(canonical_revision_turn_input_payload(turn_input))


def revision_turn_input_fingerprint(
    turn_input: FolderPlannerRevisionTurnInputV1,
) -> str:
    """Fingerprint one revision input without changing historical omissions."""

    return canonical_sha256(canonical_revision_turn_input_payload(turn_input))


class FolderRevisionProviderResponseV1(StrictFrozenModel):
    """One observable sparse-revision response with no execution authority."""

    schema_version: Literal["folder-revision-provider-response.v1"] = (
        "folder-revision-provider-response.v1"
    )
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model: str | None = Field(default=None, min_length=1, max_length=200)
    observable_output_items: tuple[JsonValue, ...] = ()
    call_id: str = Field(min_length=1, max_length=128)
    revision: FolderPlanRevisionV1

    @model_validator(mode="after")
    def require_truthful_model_identity(self) -> Self:
        if self.provider_kind == "live" and self.returned_model is None:
            raise ValueError(
                "Live revision responses require a returned model identity."
            )
        return self


@runtime_checkable
class FolderPlanRevisionProvider(Protocol):
    """Return one strict sparse revision without filesystem authority."""

    provider_kind: Literal["deterministic", "live", "recorded_replay"]

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]: ...

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1: ...


class FolderRevisionTurnRecordV1(StrictFrozenModel):
    """One complete observable sparse-revision turn."""

    schema_version: Literal["folder-revision-turn-record.v1"] = (
        "folder-revision-turn-record.v1"
    )
    input: FolderPlannerRevisionTurnInputV1
    input_bytes: int = Field(ge=1, le=512 * 1024)
    input_fingerprint: str = Field(pattern=SHA256_PATTERN)
    response: FolderRevisionProviderResponseV1
    usage: FolderPlannerUsage | None = None
    turn_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_turn(self) -> Self:
        if self.input_bytes != len(canonical_revision_turn_input_bytes(self.input)):
            raise ValueError("Revision input byte count is invalid.")
        if self.input_fingerprint != revision_turn_input_fingerprint(self.input):
            raise ValueError("Revision input fingerprint is invalid.")
        if self.response.provider_kind != self.input.provider_kind:
            raise ValueError("Revision response uses another provider origin.")
        if (
            self.response.revision.base_candidate_fingerprint
            != self.input.base_candidate_fingerprint
        ):
            raise ValueError("Sparse revision targets another base candidate.")
        if self.input.provider_kind == "live":
            if (
                self.usage is None
                or self.usage.response_turn != self.input.response_turn
            ):
                raise ValueError("Live revision requires exact observable usage.")
        elif self.usage is not None:
            raise ValueError("Model-free revision cannot claim direct API usage.")
        payload = revision_turn_record_payload(self)
        if self.turn_fingerprint != canonical_sha256(payload):
            raise ValueError("Revision turn fingerprint is invalid.")
        return self


def revision_turn_record_payload(
    turn: FolderRevisionTurnRecordV1,
) -> dict[str, JsonValue]:
    """Return one exact turn payload across the legacy omission boundary."""

    payload = turn.model_dump(mode="json", exclude={"turn_fingerprint"})
    payload["input"] = canonical_revision_turn_input_payload(turn.input)
    return payload


class FolderPlanningSegmentV1(StrictFrozenModel):
    """One immutable initial-plan or user-revision transcript segment."""

    schema_version: Literal["folder-planning-segment.v1"] = "folder-planning-segment.v1"
    segment_kind: Literal["initial_plan", "user_revision"]
    outcome: Literal["accepted", "rejected"]
    selected: bool
    proposal_revision_before: int = Field(ge=0, le=2)
    proposal_revision_after: int = Field(ge=0, le=2)
    first_response_turn: int = Field(ge=1, le=8)
    last_response_turn: int = Field(ge=1, le=8)
    base_candidate_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    base_preview_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    revision_instruction_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    observable_records: tuple[JsonValue, ...] = Field(min_length=1)
    final_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    segment_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_segment_shape(self) -> Self:
        if self.last_response_turn < self.first_response_turn:
            raise ValueError("Planning segment turn range is reversed.")
        derivative_fields = (
            self.base_candidate_fingerprint,
            self.base_preview_fingerprint,
            self.revision_instruction_fingerprint,
        )
        if self.segment_kind == "initial_plan":
            if (
                self.outcome != "accepted"
                or not self.selected
                or self.proposal_revision_before != 0
                or self.proposal_revision_after != 0
            ):
                raise ValueError("Initial planning segment must produce proposal zero.")
            if any(value is not None for value in derivative_fields):
                raise ValueError("Initial planning cannot claim revision bindings.")
        else:
            if any(value is None for value in derivative_fields):
                raise ValueError("Revision segment lacks exact parent bindings.")
            expected_after = self.proposal_revision_before + (1 if self.selected else 0)
            if self.proposal_revision_after != expected_after:
                raise ValueError("Revision segment proposal revision is invalid.")
            if self.selected != (self.outcome == "accepted"):
                raise ValueError("Revision selection and outcome disagree.")
        payload = self.model_dump(mode="json", exclude={"segment_fingerprint"})
        if self.segment_fingerprint != canonical_sha256(payload):
            raise ValueError("Planning segment fingerprint is invalid.")
        return self


class FolderEvidenceLedgerV2(StrictFrozenModel):
    """Composite initial-plus-revision evidence without resetting counters."""

    schema_version: Literal["folder-evidence-ledger.v2"] = "folder-evidence-ledger.v2"
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    request_scope: Literal["rename_and_move_every_file"]
    planning_basis: Literal["fresh", "derivative", "recorded_replay"]
    model_transport: Literal[
        "responses_api",
        "chatgpt_hosted",
        "codex_hosted",
        "recorded_replay",
        "deterministic_development",
    ]
    contract_freeze_fingerprint: str = Field(pattern=SHA256_PATTERN)
    initial_ledger: FolderEvidenceLedger
    segments: tuple[FolderPlanningSegmentV1, ...] = Field(min_length=1, max_length=3)
    response_turn_count: int = Field(ge=1, le=8)
    evidence_call_count: int = Field(ge=0, le=24)
    clarification_count: int = Field(ge=0, le=1)
    full_plan_submission_count: int = Field(ge=1, le=3)
    sparse_revision_submission_count: int = Field(ge=0, le=2)
    user_revision_count: int = Field(ge=0, le=MAX_FOLDWEAVE_REVISIONS)
    selected_proposal_revision: int = Field(ge=0, le=MAX_FOLDWEAVE_REVISIONS)
    returned_model_ids: tuple[str, ...] = ()
    usage: tuple[FolderPlannerUsage, ...] = ()
    store_false: bool | None = None
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError(
                "Evidence job ID must be lowercase UUID4 hexadecimal text."
            )
        return value

    @model_validator(mode="after")
    def require_complete_composite_transcript(self) -> Self:
        initial = self.initial_ledger
        if not (
            self.job_id == initial.job_id
            and self.source_commitment == initial.source_commitment
            and self.request_fingerprint == initial.request_fingerprint
            and self.request_scope == initial.request_scope
            and self.evidence_call_count == initial.evidence_call_count
            and self.full_plan_submission_count == initial.plan_submission_count
            and self.evidence_fingerprint == initial.evidence_fingerprint
        ):
            raise ValueError("Composite evidence differs from its initial ledger.")
        if self.segments[0].segment_kind != "initial_plan":
            raise ValueError("Composite evidence must begin with initial planning.")
        initial_segment = self.segments[0]
        if not (
            initial_segment.first_response_turn == 1
            and initial_segment.last_response_turn == initial.response_turn_count
            and initial_segment.final_candidate_fingerprint
            == initial.accepted_plan_fingerprint
        ):
            raise ValueError("Initial planning segment differs from its ledger.")
        expected_clarifications = 1 if initial.clarification_question is not None else 0
        if self.clarification_count != expected_clarifications:
            raise ValueError("Composite clarification count is invalid.")
        expected_transport = {
            "deterministic": "deterministic_development",
            "live": "responses_api",
            "recorded_replay": "recorded_replay",
        }[initial.provider_kind]
        if (
            self.model_transport
            in {
                "deterministic_development",
                "responses_api",
                "recorded_replay",
            }
            and self.model_transport != expected_transport
        ):
            raise ValueError("Initial provider and model transport disagree.")
        expected_turn = 1
        expected_candidate: str | None = None
        revision_count = 0
        selected_revision_count = 0
        expected_returned_ids = list(initial.returned_model_ids)
        expected_usage = list(initial.usage)
        explicit_revision_contract_seen = False
        for segment_index, segment in enumerate(self.segments):
            if segment.first_response_turn != expected_turn:
                raise ValueError("Planning segments must be globally contiguous.")
            if segment.segment_kind == "user_revision":
                revision_count += 1
                if segment.proposal_revision_before != selected_revision_count:
                    raise ValueError("Revision segment proposal counter is invalid.")
                if segment.base_candidate_fingerprint != expected_candidate:
                    raise ValueError("Revision segment does not bind its parent plan.")
                if len(segment.observable_records) != 1:
                    raise ValueError("Revision segment must contain one exact turn.")
                # Observable records are deliberately JSON-mode values. Validate
                # them through the JSON boundary so strict tuple fields accept
                # canonical JSON arrays without weakening Python-side strictness.
                turn = FolderRevisionTurnRecordV1.model_validate_json(
                    canonical_json_bytes(segment.observable_records[0]),
                    strict=True,
                )
                if turn.input.turn_contract_freeze_fingerprint is None:
                    if explicit_revision_contract_seen:
                        raise ValueError(
                            "Historical contract omission cannot follow an explicit "
                            "binding."
                        )
                else:
                    explicit_revision_contract_seen = True
                if turn.input.response_turn != segment.first_response_turn:
                    raise ValueError("Revision segment contains another response turn.")
                if (
                    _provider_transport(turn.input.provider_kind)
                    != self.model_transport
                ):
                    raise ValueError("Revision provider and transport disagree.")
                returned_model = turn.response.returned_model
                if (
                    returned_model is not None
                    and returned_model not in expected_returned_ids
                ):
                    expected_returned_ids.append(returned_model)
                if turn.usage is not None:
                    expected_usage.append(turn.usage)
                if segment.selected:
                    selected_revision_count += 1
                    expected_candidate = segment.final_candidate_fingerprint
                elif segment.final_candidate_fingerprint != expected_candidate:
                    raise ValueError(
                        "Rejected revision changed the selected candidate."
                    )
            else:
                if segment_index != 0:
                    raise ValueError(
                        "Initial planning segment must appear exactly once."
                    )
                expected_candidate = segment.final_candidate_fingerprint
            expected_turn = segment.last_response_turn + 1
        if self.response_turn_count != expected_turn - 1:
            raise ValueError("Composite response-turn count is invalid.")
        if not (
            revision_count
            == self.user_revision_count
            == self.sparse_revision_submission_count
        ):
            raise ValueError("Composite revision counters do not agree.")
        if self.selected_proposal_revision != selected_revision_count:
            raise ValueError("Selected proposal revision count is invalid.")
        if self.accepted_plan_fingerprint != expected_candidate:
            raise ValueError("Composite evidence names another final candidate.")
        if self.returned_model_ids != tuple(expected_returned_ids):
            raise ValueError("Composite returned-model identities are invalid.")
        if self.usage != tuple(expected_usage):
            raise ValueError("Composite usage differs from its exact turn records.")
        usage_turns = tuple(item.response_turn for item in self.usage)
        if self.model_transport == "responses_api":
            if self.store_false is not True:
                raise ValueError("Direct planning requires store=false.")
            if usage_turns != tuple(range(1, self.response_turn_count + 1)):
                raise ValueError("Direct planning requires usage for every turn.")
            if not self.returned_model_ids:
                raise ValueError("Direct planning requires returned model identities.")
        elif self.store_false is not None:
            raise ValueError("Only direct API planning records store=false.")
        payload = self.model_dump(mode="json", exclude={"transcript_fingerprint"})
        if self.transcript_fingerprint != canonical_sha256(payload):
            raise ValueError("Composite transcript fingerprint is invalid.")
        return self


class GptPlannedExecutionOriginV2(StrictFrozenModel):
    """Orthogonal observable provenance for a reviewed Foldweave transaction."""

    schema_version: Literal["folder-execution-origin.v2"] = "folder-execution-origin.v2"
    kind: Literal["gpt_planned", "gpt_revised_from_change_file"]
    planning_basis: Literal["fresh", "derivative", "recorded_replay"]
    model_transport: Literal[
        "responses_api",
        "chatgpt_hosted",
        "codex_hosted",
        "recorded_replay",
        "deterministic_development",
    ]
    model_alias: Literal["gpt-5.6"] | None = None
    returned_model_ids: tuple[str, ...] = ()
    observable_transcript: tuple[JsonValue, ...]
    clarification_question: str | None = None
    clarification_answer: str | None = None
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    provider_call_count: int = Field(ge=0, le=8)
    api_used: bool
    store_false: bool | None = None
    external_network_used: bool
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )

    @model_validator(mode="after")
    def require_truthful_transport(self) -> Self:
        if (self.clarification_question is None) != (self.clarification_answer is None):
            raise ValueError("Clarification question and answer must appear together.")
        derivative = self.kind == "gpt_revised_from_change_file"
        if derivative != (self.planning_basis == "derivative"):
            raise ValueError("Execution kind and planning basis disagree.")
        if derivative != (self.imported_change_file_fingerprint is not None):
            raise ValueError("Derivative origin lacks imported Change File authority.")
        if derivative != (self.match_report_fingerprint is not None):
            raise ValueError("Derivative origin lacks match-report authority.")
        if self.model_transport == "responses_api":
            if not (
                self.api_used
                and self.external_network_used
                and self.store_false is True
                and self.model_alias == "gpt-5.6"
                and self.returned_model_ids
                and self.provider_call_count >= 1
            ):
                raise ValueError("Direct execution origin lacks truthful API metadata.")
        else:
            expected_network = self.model_transport in {
                "chatgpt_hosted",
                "codex_hosted",
            }
            if (
                self.api_used
                or self.store_false is not None
                or self.provider_call_count != 0
                or self.model_alias is not None
                or self.external_network_used != expected_network
            ):
                raise ValueError(
                    "Host/replay provenance contains impossible transport facts."
                )
        return self


def _provider_transport(
    provider_kind: Literal["deterministic", "live", "recorded_replay"],
) -> Literal[
    "responses_api",
    "recorded_replay",
    "deterministic_development",
]:
    return {
        "deterministic": "deterministic_development",
        "live": "responses_api",
        "recorded_replay": "recorded_replay",
    }[provider_kind]


def build_planning_segment(
    *,
    segment_kind: Literal["initial_plan", "user_revision"],
    outcome: Literal["accepted", "rejected"],
    selected: bool,
    proposal_revision_before: int,
    proposal_revision_after: int,
    first_response_turn: int,
    last_response_turn: int,
    observable_records: tuple[JsonValue, ...],
    final_candidate_fingerprint: str,
    base_candidate_fingerprint: str | None = None,
    base_preview_fingerprint: str | None = None,
    revision_instruction_fingerprint: str | None = None,
) -> FolderPlanningSegmentV1:
    """Build one canonical segment without a self-referential fingerprint."""

    values = {
        "segment_kind": segment_kind,
        "outcome": outcome,
        "selected": selected,
        "proposal_revision_before": proposal_revision_before,
        "proposal_revision_after": proposal_revision_after,
        "first_response_turn": first_response_turn,
        "last_response_turn": last_response_turn,
        "base_candidate_fingerprint": base_candidate_fingerprint,
        "base_preview_fingerprint": base_preview_fingerprint,
        "revision_instruction_fingerprint": revision_instruction_fingerprint,
        "observable_records": observable_records,
        "final_candidate_fingerprint": final_candidate_fingerprint,
    }
    draft = FolderPlanningSegmentV1.model_construct(
        **values,
        segment_fingerprint="0" * 64,
    )
    return FolderPlanningSegmentV1(
        **values,
        segment_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"segment_fingerprint"})
        ),
    )


def build_revision_turn_record(
    *,
    turn_input: FolderPlannerRevisionTurnInputV1,
    response: FolderRevisionProviderResponseV1,
    usage: FolderPlannerUsage | None,
) -> FolderRevisionTurnRecordV1:
    """Build one canonical observable revision turn."""

    if turn_input.turn_contract_freeze_fingerprint is None:
        raise ValueError("New revision turns require an exact contract freeze.")

    values = {
        "input": turn_input,
        "input_bytes": len(canonical_revision_turn_input_bytes(turn_input)),
        "input_fingerprint": revision_turn_input_fingerprint(turn_input),
        "response": response,
        "usage": usage,
    }
    draft = FolderRevisionTurnRecordV1.model_construct(
        **values,
        turn_fingerprint="0" * 64,
    )
    return FolderRevisionTurnRecordV1(
        **values,
        turn_fingerprint=canonical_sha256(revision_turn_record_payload(draft)),
    )


def build_foldweave_f0b_contract_freeze() -> FoldweaveF0bContractFreezeV1:
    """Build the complete deterministic F0b freeze without touching credentials."""

    # Local imports avoid making the planner contract module depend on the v3 job
    # module while that job module imports the planning contracts it persists.
    from name_atlas.folder_refactor.connected_change.job_v3 import (
        FolderExecutionAuthorizationV1,
        FolderJobLifecycleV3,
        FolderRefactorJobV3,
    )
    from name_atlas.folder_refactor.connected_change.preview import (
        FolderPlanPreviewV1,
    )
    from name_atlas.folder_refactor.demo_fixtures import (
        FOLDWEAVE_F0B_FIXTURE_FINGERPRINT,
        FOLDWEAVE_F0B_FIXTURE_NAME,
    )
    from name_atlas.folder_refactor.foldweave_revision_prompt import (
        FOLDWEAVE_REVISION_INSTRUCTIONS_FINGERPRINT,
        FOLDWEAVE_REVISION_TOOL_SCHEMA_FINGERPRINT,
    )
    from name_atlas.folder_refactor.live_planner_provider import (
        DEFAULT_LIVE_PLANNER_POLICY,
        DEFAULT_LIVE_REVISION_POLICY,
    )
    from name_atlas.folder_refactor.planner_prompt import (
        FOLDWEAVE_PLANNER_INSTRUCTIONS_FINGERPRINT,
        FOLDWEAVE_PLANNER_TOOL_SCHEMA_FINGERPRINT,
    )

    preview_review_contract_fingerprint = canonical_sha256(
        {
            "domain": "foldweave:f0b:preview-review-contract:v1",
            "preview_schema": FolderPlanPreviewV1.model_json_schema(mode="validation"),
            "authorization_schema": (
                FolderExecutionAuthorizationV1.model_json_schema(mode="validation")
            ),
            "job_schema": FolderRefactorJobV3.model_json_schema(mode="validation"),
            "job_lifecycle": tuple(item.value for item in FolderJobLifecycleV3),
        }
    )
    derivative_planning_contract_fingerprint = canonical_sha256(
        {
            "domain": "foldweave:f0b:derivative-planning-contract:v1",
            "revision_input_schema": (
                FolderPlannerRevisionTurnInputV1.model_json_schema(mode="validation")
            ),
            "sparse_revision_schema": FolderPlanRevisionV1.model_json_schema(
                mode="validation"
            ),
            "planning_basis": "derivative",
            "proposal_basis": "gpt_derivative",
            "required_parent_bindings": (
                "imported_change_file_fingerprint",
                "match_report_fingerprint",
                "immediate_parent_candidate_fingerprint",
            ),
        }
    )
    evidence_envelope_contract_fingerprint = canonical_sha256(
        {
            "domain": "foldweave:f0b:evidence-envelope-contract:v2",
            "initial_evidence_schema": FolderEvidenceLedger.model_json_schema(
                mode="validation"
            ),
            "composite_evidence_schema": FolderEvidenceLedgerV2.model_json_schema(
                mode="validation"
            ),
        }
    )
    replay_envelope_identity_fingerprint = canonical_sha256(
        {
            "domain": "foldweave:f0b:replay-envelope-identity:v2",
            "schema_version": FOLDWEAVE_F0B_REPLAY_SCHEMA_VERSION,
            "fingerprint_domain": FOLDWEAVE_F0B_REPLAY_FINGERPRINT_DOMAIN,
            "fixture_domain": FOLDWEAVE_F0B_REPLAY_FIXTURE_DOMAIN,
            "evidence_schema_version": "folder-evidence-ledger.v2",
            "initial_turn_schema_version": "folder-planner-turn-input.v1",
            "revision_turn_schema_version": ("folder-planner-revision-turn-input.v1"),
            "binds_contract_freeze_fingerprint": True,
            "binds_fixture_fingerprint": True,
        }
    )
    qualification_provider_profile_fingerprint = canonical_sha256(
        {
            "domain": "foldweave:f0b:qualification-provider-profile:v1",
            "transport": "responses_api",
            "endpoint": "https://api.openai.com/v1",
            "model": "gpt-5.6",
            "store": False,
            "sdk_max_retries": DEFAULT_LIVE_PLANNER_POLICY.sdk_max_retries,
            "follow_redirects": False,
            "initial": {
                "timeout_seconds": DEFAULT_LIVE_PLANNER_POLICY.timeout_seconds,
                "max_output_tokens": DEFAULT_LIVE_PLANNER_POLICY.max_output_tokens,
                "reasoning_effort": DEFAULT_LIVE_PLANNER_POLICY.reasoning_effort,
                "tool_choice": "required",
                "parallel_tool_calls": True,
                "max_tool_calls": 24,
            },
            "revision": {
                "timeout_seconds": DEFAULT_LIVE_REVISION_POLICY.timeout_seconds,
                "max_output_tokens": DEFAULT_LIVE_REVISION_POLICY.max_output_tokens,
                "reasoning_effort": DEFAULT_LIVE_REVISION_POLICY.reasoning_effort,
                "tool_choice": "submit_plan_revision",
                "parallel_tool_calls": False,
                "max_tool_calls": 1,
            },
        }
    )
    call_graph_payload = {
        "domain": "foldweave:f0b:qualification-call-graph:v1",
        "nodes": FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH,
        "initial_provider_attempts_min": 2,
        "initial_provider_attempts_max": 3,
        "revision_provider_attempts": 1,
        "total_provider_attempts_min": 3,
        "total_provider_attempts_max": 4,
    }
    values = {
        "initial_prompt_fingerprint": (FOLDWEAVE_PLANNER_INSTRUCTIONS_FINGERPRINT),
        "initial_tools_fingerprint": FOLDWEAVE_PLANNER_TOOL_SCHEMA_FINGERPRINT,
        "revision_prompt_fingerprint": (FOLDWEAVE_REVISION_INSTRUCTIONS_FINGERPRINT),
        "revision_tools_fingerprint": FOLDWEAVE_REVISION_TOOL_SCHEMA_FINGERPRINT,
        "preview_review_contract_fingerprint": (preview_review_contract_fingerprint),
        "derivative_planning_contract_fingerprint": (
            derivative_planning_contract_fingerprint
        ),
        "qualification_provider_profile_fingerprint": (
            qualification_provider_profile_fingerprint
        ),
        "replay_envelope_identity_fingerprint": (replay_envelope_identity_fingerprint),
        "evidence_envelope_contract_fingerprint": (
            evidence_envelope_contract_fingerprint
        ),
        "fixture_name": FOLDWEAVE_F0B_FIXTURE_NAME,
        "fixture_fingerprint": FOLDWEAVE_F0B_FIXTURE_FINGERPRINT,
        "qualification_call_graph": FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH,
        "qualification_call_graph_fingerprint": canonical_sha256(call_graph_payload),
    }
    draft = FoldweaveF0bContractFreezeV1.model_construct(
        **values,
        contract_freeze_fingerprint="0" * 64,
    )
    return FoldweaveF0bContractFreezeV1(
        **values,
        contract_freeze_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"contract_freeze_fingerprint"})
        ),
    )


def foldweave_contract_freeze_fingerprint(
    *,
    initial_prompt_fingerprint: str,
    initial_tools_fingerprint: str,
    revision_prompt_fingerprint: str,
    revision_tools_fingerprint: str,
) -> str:
    """Return the full F0b freeze only when all supplied planner IDs agree."""

    freeze = build_foldweave_f0b_contract_freeze()
    supplied = (
        initial_prompt_fingerprint,
        initial_tools_fingerprint,
        revision_prompt_fingerprint,
        revision_tools_fingerprint,
    )
    expected = (
        freeze.initial_prompt_fingerprint,
        freeze.initial_tools_fingerprint,
        freeze.revision_prompt_fingerprint,
        freeze.revision_tools_fingerprint,
    )
    if supplied != expected:
        raise ValueError("Supplied planner identities differ from the F0b freeze.")
    return freeze.contract_freeze_fingerprint


def build_initial_composite_evidence(
    *,
    initial_ledger: FolderEvidenceLedger,
    accepted_plan: FolderAcceptedPlanV2,
    contract_freeze_fingerprint: str,
    planning_basis: Literal["fresh", "derivative", "recorded_replay"] = "fresh",
    model_transport: Literal[
        "responses_api",
        "chatgpt_hosted",
        "codex_hosted",
        "recorded_replay",
        "deterministic_development",
    ],
) -> FolderEvidenceLedgerV2:
    """Promote one accepted initial transcript into composite v2 authority."""

    accepted_fingerprint = canonical_sha256(accepted_plan)
    if initial_ledger.accepted_plan_fingerprint != accepted_fingerprint:
        raise ValueError("Initial evidence names another accepted Foldweave plan.")
    segment = build_planning_segment(
        segment_kind="initial_plan",
        outcome="accepted",
        selected=True,
        proposal_revision_before=0,
        proposal_revision_after=0,
        first_response_turn=1,
        last_response_turn=initial_ledger.response_turn_count,
        observable_records=tuple(
            turn.model_dump(mode="json") for turn in initial_ledger.observable_turns
        ),
        final_candidate_fingerprint=accepted_fingerprint,
    )
    values = {
        "job_id": initial_ledger.job_id,
        "source_commitment": initial_ledger.source_commitment,
        "request_fingerprint": initial_ledger.request_fingerprint,
        "request_scope": initial_ledger.request_scope,
        "planning_basis": planning_basis,
        "model_transport": model_transport,
        "contract_freeze_fingerprint": contract_freeze_fingerprint,
        "initial_ledger": initial_ledger,
        "segments": (segment,),
        "response_turn_count": initial_ledger.response_turn_count,
        "evidence_call_count": initial_ledger.evidence_call_count,
        "clarification_count": (
            1 if initial_ledger.clarification_question is not None else 0
        ),
        "full_plan_submission_count": initial_ledger.plan_submission_count,
        "sparse_revision_submission_count": 0,
        "user_revision_count": 0,
        "selected_proposal_revision": 0,
        "returned_model_ids": initial_ledger.returned_model_ids,
        "usage": initial_ledger.usage,
        "store_false": initial_ledger.store_false,
        "evidence_fingerprint": initial_ledger.evidence_fingerprint,
        "accepted_plan_fingerprint": accepted_fingerprint,
    }
    draft = FolderEvidenceLedgerV2.model_construct(
        **values,
        transcript_fingerprint="0" * 64,
    )
    return FolderEvidenceLedgerV2(
        **values,
        transcript_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"transcript_fingerprint"})
        ),
    )


def append_successful_revision_evidence(
    *,
    ledger: FolderEvidenceLedgerV2,
    turn: FolderRevisionTurnRecordV1,
    accepted_plan: FolderAcceptedPlanV2,
    base_preview_fingerprint: str,
    revision_instruction_fingerprint: str,
) -> FolderEvidenceLedgerV2:
    """Append one successful sparse turn without rewriting prior segments."""

    if turn.input.response_turn != ledger.response_turn_count + 1:
        raise ValueError("Revision turn does not extend the exact ledger prefix.")
    if turn.input.prior_transcript_fingerprint != ledger.transcript_fingerprint:
        raise ValueError("Revision turn targets another planner transcript.")
    if turn.input.base_candidate_fingerprint != ledger.accepted_plan_fingerprint:
        raise ValueError("Revision turn targets another selected candidate.")
    if turn.input.base_preview_fingerprint != base_preview_fingerprint:
        raise ValueError("Revision turn targets another selected preview.")
    if turn.input.revision_instruction_fingerprint != revision_instruction_fingerprint:
        raise ValueError("Revision turn targets another user instruction.")
    accepted_fingerprint = canonical_sha256(accepted_plan)
    proposal_before = ledger.selected_proposal_revision
    segment = build_planning_segment(
        segment_kind="user_revision",
        outcome="accepted",
        selected=True,
        proposal_revision_before=proposal_before,
        proposal_revision_after=proposal_before + 1,
        first_response_turn=turn.input.response_turn,
        last_response_turn=turn.input.response_turn,
        observable_records=(turn.model_dump(mode="json"),),
        base_candidate_fingerprint=turn.input.base_candidate_fingerprint,
        base_preview_fingerprint=base_preview_fingerprint,
        revision_instruction_fingerprint=revision_instruction_fingerprint,
        final_candidate_fingerprint=accepted_fingerprint,
    )
    returned_ids = tuple(
        dict.fromkeys(
            (*ledger.returned_model_ids,)
            + (
                (turn.response.returned_model,)
                if turn.response.returned_model is not None
                else ()
            )
        )
    )
    usage = ledger.usage + ((turn.usage,) if turn.usage is not None else ())
    values = {
        **{
            field_name: getattr(ledger, field_name)
            for field_name in FolderEvidenceLedgerV2.model_fields
            if field_name != "transcript_fingerprint"
        },
        "segments": (*ledger.segments, segment),
        "response_turn_count": turn.input.response_turn,
        "sparse_revision_submission_count": (
            ledger.sparse_revision_submission_count + 1
        ),
        "user_revision_count": ledger.user_revision_count + 1,
        "selected_proposal_revision": ledger.selected_proposal_revision + 1,
        "returned_model_ids": returned_ids,
        "usage": usage,
        "accepted_plan_fingerprint": accepted_fingerprint,
    }
    draft = FolderEvidenceLedgerV2.model_construct(
        **values,
        transcript_fingerprint="0" * 64,
    )
    return FolderEvidenceLedgerV2(
        **values,
        transcript_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"transcript_fingerprint"})
        ),
    )


def append_failed_revision_evidence(
    *,
    ledger: FolderEvidenceLedgerV2,
    turn: FolderRevisionTurnRecordV1,
    base_preview_fingerprint: str,
    revision_instruction_fingerprint: str,
) -> FolderEvidenceLedgerV2:
    """Preserve a rejected sparse response while keeping the prior candidate."""

    if turn.input.response_turn != ledger.response_turn_count + 1:
        raise ValueError("Rejected revision does not extend the ledger prefix.")
    if turn.input.prior_transcript_fingerprint != ledger.transcript_fingerprint:
        raise ValueError("Rejected revision targets another planner transcript.")
    if turn.input.base_candidate_fingerprint != ledger.accepted_plan_fingerprint:
        raise ValueError("Rejected revision targets another selected candidate.")
    if turn.input.base_preview_fingerprint != base_preview_fingerprint:
        raise ValueError("Rejected revision targets another selected preview.")
    if turn.input.revision_instruction_fingerprint != revision_instruction_fingerprint:
        raise ValueError("Rejected revision targets another user instruction.")
    segment = build_planning_segment(
        segment_kind="user_revision",
        outcome="rejected",
        selected=False,
        proposal_revision_before=ledger.selected_proposal_revision,
        proposal_revision_after=ledger.selected_proposal_revision,
        first_response_turn=turn.input.response_turn,
        last_response_turn=turn.input.response_turn,
        observable_records=(turn.model_dump(mode="json"),),
        base_candidate_fingerprint=turn.input.base_candidate_fingerprint,
        base_preview_fingerprint=base_preview_fingerprint,
        revision_instruction_fingerprint=revision_instruction_fingerprint,
        final_candidate_fingerprint=ledger.accepted_plan_fingerprint,
    )
    returned_ids = tuple(
        dict.fromkeys(
            (*ledger.returned_model_ids,)
            + (
                (turn.response.returned_model,)
                if turn.response.returned_model is not None
                else ()
            )
        )
    )
    usage = ledger.usage + ((turn.usage,) if turn.usage is not None else ())
    values = {
        **{
            field_name: getattr(ledger, field_name)
            for field_name in FolderEvidenceLedgerV2.model_fields
            if field_name != "transcript_fingerprint"
        },
        "segments": (*ledger.segments, segment),
        "response_turn_count": turn.input.response_turn,
        "sparse_revision_submission_count": (
            ledger.sparse_revision_submission_count + 1
        ),
        "user_revision_count": ledger.user_revision_count + 1,
        "returned_model_ids": returned_ids,
        "usage": usage,
    }
    draft = FolderEvidenceLedgerV2.model_construct(
        **values,
        transcript_fingerprint="0" * 64,
    )
    return FolderEvidenceLedgerV2(
        **values,
        transcript_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"transcript_fingerprint"})
        ),
    )


def build_execution_origin_v2(
    ledger: FolderEvidenceLedgerV2,
    *,
    imported_change_file_fingerprint: str | None = None,
    match_report_fingerprint: str | None = None,
) -> GptPlannedExecutionOriginV2:
    """Project one complete ledger into orthogonal truthful provenance."""

    direct = ledger.model_transport == "responses_api"
    derivative = ledger.planning_basis == "derivative"
    observable = tuple(
        record for segment in ledger.segments for record in segment.observable_records
    )
    return GptPlannedExecutionOriginV2(
        kind=("gpt_revised_from_change_file" if derivative else "gpt_planned"),
        planning_basis=ledger.planning_basis,
        model_transport=ledger.model_transport,
        model_alias="gpt-5.6" if direct else None,
        returned_model_ids=ledger.returned_model_ids,
        observable_transcript=observable,
        clarification_question=ledger.initial_ledger.clarification_question,
        clarification_answer=ledger.initial_ledger.clarification_answer,
        evidence_fingerprint=ledger.evidence_fingerprint,
        evidence_transcript_fingerprint=ledger.transcript_fingerprint,
        accepted_plan_fingerprint=ledger.accepted_plan_fingerprint,
        provider_call_count=(ledger.response_turn_count if direct else 0),
        api_used=direct,
        store_false=True if direct else None,
        external_network_used=(
            ledger.model_transport
            in {"responses_api", "chatgpt_hosted", "codex_hosted"}
        ),
        imported_change_file_fingerprint=imported_change_file_fingerprint,
        match_report_fingerprint=match_report_fingerprint,
    )
