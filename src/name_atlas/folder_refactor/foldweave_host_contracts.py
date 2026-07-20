"""Truthful observable contracts for ChatGPT- and Codex-hosted planning."""

from __future__ import annotations

import uuid
from itertools import pairwise
from typing import Annotated, Literal, Self

from pydantic import Field, JsonValue, field_validator, model_validator

from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderPlan,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.naming import validate_target_path
from name_atlas.folder_refactor.planner_contracts import PlannerEvidenceState
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import canonical_sha256

HostModelTransport = Literal["chatgpt_hosted", "codex_hosted"]
MAX_HOST_PLAN_SUBMISSIONS = 3
MAX_HOST_RESPONSE_TURNS = 8


class FolderHostPlanRevisionEntryV1(StrictFrozenModel):
    """One host-supplied sparse path replacement."""

    file_id: str = Field(
        pattern=SHA256_PATTERN,
        description=(
            "Exact local member file_id from the current Foldweave preview. This "
            "identifies the member to revise and is never an evidence ID."
        ),
    )
    replacement_target_path: str = Field(min_length=1, max_length=1_024)
    rationale: str = Field(min_length=1, max_length=1_000)
    evidence_ids: tuple[str, ...] = Field(
        min_length=1,
        description=(
            "Exact permitted evidence identifiers supporting this replacement. "
            'For a path-only preview revision use exactly ["initial_inventory"]; '
            "never copy file_id or call_id into this field."
        ),
    )

    @model_validator(mode="after")
    def require_safe_relative_target(self) -> Self:
        validate_target_path(
            self.replacement_target_path,
            original_path=self.replacement_target_path,
            protected=False,
        )
        return self


class FolderHostPlanRevisionV1(StrictFrozenModel):
    """Strict sparse host output bound to one visible candidate."""

    schema_version: Literal["folder-host-plan-revision.v1"] = (
        "folder-host-plan-revision.v1"
    )
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    replacement_result_folder_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=240,
    )
    entries: tuple[FolderHostPlanRevisionEntryV1, ...] = Field(
        default=(),
        max_length=500,
    )

    @model_validator(mode="after")
    def require_sparse_sorted_entries(self) -> Self:
        if self.replacement_result_folder_name is None and not self.entries:
            raise ValueError(
                "Sparse hosted revision requires a result-name or path replacement."
            )
        file_ids = tuple(entry.file_id for entry in self.entries)
        if file_ids != tuple(sorted(file_ids)) or len(file_ids) != len(set(file_ids)):
            raise ValueError(
                "Hosted revision entries must be file-ID sorted and unique."
            )
        return self


class FolderHostEvidenceObservationV1(StrictFrozenModel):
    """One model-visible bounded evidence result observed through an MCP tool."""

    schema_version: Literal["folder-host-evidence-observation.v1"] = (
        "folder-host-evidence-observation.v1"
    )
    event_kind: Literal["evidence_call"] = "evidence_call"
    event_index: int = Field(ge=1, le=64)
    response_turn: int = Field(ge=1, le=MAX_HOST_RESPONSE_TURNS)
    evidence_call_number: int = Field(ge=1, le=24)
    evidence_record_fingerprint: str = Field(pattern=SHA256_PATTERN)
    event_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_fingerprint(self) -> Self:
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"event_fingerprint"})
        )
        if self.event_fingerprint != expected:
            raise ValueError("Hosted evidence observation fingerprint is invalid.")
        return self


class FolderHostPlanSubmissionV1(StrictFrozenModel):
    """One complete host-model plan submission and deterministic outcome."""

    schema_version: Literal["folder-host-plan-submission.v1"] = (
        "folder-host-plan-submission.v1"
    )
    event_kind: Literal["plan_submission"] = "plan_submission"
    event_index: int = Field(ge=1, le=64)
    response_turn: int = Field(ge=1, le=MAX_HOST_RESPONSE_TURNS)
    submission_index: int = Field(ge=1, le=MAX_HOST_PLAN_SUBMISSIONS)
    call_id: str = Field(min_length=1, max_length=128)
    plan: FolderPlan
    outcome: Literal["accepted", "rejected"]
    accepted_plan_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    compiler_failure_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    event_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_outcome_and_fingerprint(self) -> Self:
        if self.outcome == "accepted":
            if (
                self.accepted_plan_fingerprint is None
                or self.compiler_failure_fingerprint is not None
            ):
                raise ValueError("Accepted host plan requires only its plan identity.")
        elif (
            self.accepted_plan_fingerprint is not None
            or self.compiler_failure_fingerprint is None
        ):
            raise ValueError("Rejected host plan requires only compiler failure proof.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"event_fingerprint"})
        )
        if self.event_fingerprint != expected:
            raise ValueError("Hosted plan-submission fingerprint is invalid.")
        return self


class FolderHostClarificationEventV1(StrictFrozenModel):
    """One observable question or answer in the sole hosted clarification."""

    schema_version: Literal["folder-host-clarification-event.v1"] = (
        "folder-host-clarification-event.v1"
    )
    event_kind: Literal["clarification"] = "clarification"
    event_index: int = Field(ge=1, le=64)
    response_turn: int = Field(ge=1, le=MAX_HOST_RESPONSE_TURNS)
    phase: Literal["question", "answer"]
    text: str = Field(min_length=1, max_length=2_000)
    question_fingerprint: str = Field(pattern=SHA256_PATTERN)
    event_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_fingerprint(self) -> Self:
        if self.phase == "question":
            expected_question = canonical_sha256(
                {
                    "domain": "foldweave:host-clarification-question:v1",
                    "text": self.text,
                }
            )
            if self.question_fingerprint != expected_question:
                raise ValueError(
                    "Hosted clarification question fingerprint is invalid."
                )
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"event_fingerprint"})
        )
        if self.event_fingerprint != expected:
            raise ValueError("Hosted clarification event fingerprint is invalid.")
        return self


FolderHostPlanningEventV1 = Annotated[
    FolderHostEvidenceObservationV1
    | FolderHostPlanSubmissionV1
    | FolderHostClarificationEventV1,
    Field(discriminator="event_kind"),
]


class FolderHostCompilerFailureV1(StrictFrozenModel):
    """One deterministic rejection of a complete hosted plan submission."""

    schema_version: Literal["folder-host-compiler-failure.v1"] = (
        "folder-host-compiler-failure.v1"
    )
    submission_index: int = Field(ge=1, le=MAX_HOST_PLAN_SUBMISSIONS)
    call_id: str = Field(min_length=1, max_length=128)
    plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    code: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    detail: str = Field(min_length=1, max_length=2_000)
    failure_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_fingerprint(self) -> Self:
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"failure_fingerprint"})
        )
        if self.failure_fingerprint != expected:
            raise ValueError("Hosted compiler-failure fingerprint is invalid.")
        return self


class FolderHostPlanningStateV1(StrictFrozenModel):
    """Durable host-tool transcript before one candidate becomes reviewable."""

    schema_version: Literal["folder-host-planning-state.v1"] = (
        "folder-host-planning-state.v1"
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    model_transport: HostModelTransport
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_state: PlannerEvidenceState
    events: tuple[FolderHostPlanningEventV1, ...] = Field(default=(), max_length=64)
    compiler_failures: tuple[FolderHostCompilerFailureV1, ...] = Field(
        default=(),
        max_length=MAX_HOST_PLAN_SUBMISSIONS,
    )
    response_turn_count: int = Field(default=0, ge=0, le=MAX_HOST_RESPONSE_TURNS)
    plan_submission_count: int = Field(
        default=0,
        ge=0,
        le=MAX_HOST_PLAN_SUBMISSIONS,
    )
    clarification_question: str | None = Field(
        default=None,
        min_length=1,
        max_length=1_000,
    )
    clarification_answer: str | None = Field(
        default=None,
        min_length=1,
        max_length=2_000,
    )
    accepted_plan_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    status: Literal["planning", "awaiting_clarification", "accepted", "blocked"]
    state_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("Hosted planning job ID must be UUID4 hexadecimal text.")
        return value

    @model_validator(mode="after")
    def require_complete_state(self) -> Self:
        if not (
            self.source_commitment == self.evidence_state.source_commitment
            and self.request_fingerprint == self.evidence_state.request_fingerprint
        ):
            raise ValueError("Hosted planning state targets another evidence source.")
        if tuple(event.event_index for event in self.events) != tuple(
            range(1, len(self.events) + 1)
        ):
            raise ValueError("Hosted planning events must be contiguous and ordered.")
        response_turns = tuple(event.response_turn for event in self.events)
        if response_turns:
            if response_turns[0] != 1 or any(
                current < previous or current > previous + 1
                for previous, current in pairwise(response_turns)
            ):
                raise ValueError(
                    "Hosted event response turns must begin at one and remain "
                    "contiguous."
                )
            for previous_event, current_event in pairwise(self.events):
                if current_event.response_turn == previous_event.response_turn + 1:
                    valid_boundary = isinstance(
                        previous_event,
                        FolderHostPlanSubmissionV1,
                    ) or (
                        isinstance(previous_event, FolderHostClarificationEventV1)
                        and previous_event.phase == "question"
                        and isinstance(current_event, FolderHostClarificationEventV1)
                        and current_event.phase == "answer"
                    )
                    if not valid_boundary:
                        raise ValueError(
                            "Hosted response turns advance only after a plan "
                            "submission or clarification question."
                        )
                elif isinstance(previous_event, FolderHostPlanSubmissionV1):
                    raise ValueError(
                        "Hosted events after a plan submission require a new "
                        "response turn."
                    )
        evidence_events = tuple(
            event
            for event in self.events
            if isinstance(event, FolderHostEvidenceObservationV1)
        )
        if len(evidence_events) != len(self.evidence_state.records):
            raise ValueError("Hosted evidence events differ from the evidence ledger.")
        for event, record in zip(
            evidence_events,
            self.evidence_state.records,
            strict=True,
        ):
            if not (
                event.response_turn == record.response_turn
                and event.evidence_call_number == record.evidence_call_number
                and event.evidence_record_fingerprint == record.fingerprint
            ):
                raise ValueError("Hosted evidence event differs from its exact record.")
        submissions = tuple(
            event
            for event in self.events
            if isinstance(event, FolderHostPlanSubmissionV1)
        )
        if len(submissions) != self.plan_submission_count:
            raise ValueError("Hosted plan-submission count is invalid.")
        if tuple(item.submission_index for item in submissions) != tuple(
            range(1, len(submissions) + 1)
        ):
            raise ValueError("Hosted plan submissions must be contiguous and ordered.")
        rejected = tuple(item for item in submissions if item.outcome == "rejected")
        if len(rejected) != len(self.compiler_failures):
            raise ValueError(
                "Hosted compiler failures differ from rejected submissions."
            )
        for submission, failure in zip(rejected, self.compiler_failures, strict=True):
            if not (
                submission.submission_index == failure.submission_index
                and submission.call_id == failure.call_id
                and failure.plan_fingerprint == canonical_sha256(submission.plan)
                and submission.compiler_failure_fingerprint
                == failure.failure_fingerprint
            ):
                raise ValueError(
                    "Hosted rejection differs from compiler failure proof."
                )
        expected_turns = max(
            (event.response_turn for event in self.events),
            default=0,
        )
        if self.response_turn_count != expected_turns:
            raise ValueError("Hosted response-turn count is invalid.")
        clarification_events = tuple(
            event
            for event in self.events
            if isinstance(event, FolderHostClarificationEventV1)
        )
        questions = tuple(
            event for event in clarification_events if event.phase == "question"
        )
        answers = tuple(
            event for event in clarification_events if event.phase == "answer"
        )
        if len(questions) > 1 or len(answers) > 1:
            raise ValueError("Hosted planning permits one clarification only.")
        if bool(questions) != (self.clarification_question is not None):
            raise ValueError("Hosted clarification question evidence is incomplete.")
        if bool(answers) != (self.clarification_answer is not None):
            raise ValueError("Hosted clarification answer evidence is incomplete.")
        if questions and questions[0].text != self.clarification_question:
            raise ValueError(
                "Hosted clarification question text differs from evidence."
            )
        if answers and answers[0].text != self.clarification_answer:
            raise ValueError("Hosted clarification answer text differs from evidence.")
        if (
            questions
            and answers
            and (questions[0].question_fingerprint != answers[0].question_fingerprint)
        ):
            raise ValueError("Hosted clarification answer targets another question.")
        accepted = self.status == "accepted"
        if accepted != (self.accepted_plan_fingerprint is not None):
            raise ValueError("Hosted accepted state and plan identity must coincide.")
        if accepted:
            if not submissions or submissions[-1].outcome != "accepted":
                raise ValueError(
                    "Hosted accepted state lacks its final plan submission."
                )
            if (
                submissions[-1].accepted_plan_fingerprint
                != self.accepted_plan_fingerprint
            ):
                raise ValueError("Hosted accepted state names another plan.")
        elif any(item.outcome == "accepted" for item in submissions):
            raise ValueError("Hosted planning cannot continue after plan acceptance.")
        if self.status == "awaiting_clarification" and not (
            self.clarification_question is not None
            and self.clarification_answer is None
        ):
            raise ValueError("Hosted clarification state is incomplete.")
        if self.status == "planning" and (
            self.clarification_question is not None
            and self.clarification_answer is None
        ):
            raise ValueError("Unanswered hosted clarification must remain waiting.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"state_fingerprint"})
        )
        if self.state_fingerprint != expected:
            raise ValueError("Hosted planning-state fingerprint is invalid.")
        return self


class FolderHostEvidenceLedgerV1(StrictFrozenModel):
    """Accepted initial hosted transcript without direct-provider claims."""

    schema_version: Literal["folder-host-evidence-ledger.v1"] = (
        "folder-host-evidence-ledger.v1"
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    provider_kind: HostModelTransport
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    request_scope: Literal["rename_and_move_every_file"] = "rename_and_move_every_file"
    evidence_state: PlannerEvidenceState
    observable_records: tuple[JsonValue, ...] = Field(min_length=1, max_length=64)
    response_turn_count: int = Field(ge=1, le=MAX_HOST_RESPONSE_TURNS)
    evidence_call_count: int = Field(ge=0, le=24)
    plan_submission_count: int = Field(ge=1, le=MAX_HOST_PLAN_SUBMISSIONS)
    clarification_question: str | None = None
    clarification_answer: str | None = None
    returned_model_ids: tuple[str, ...] = ()
    usage: tuple[FolderPlannerUsage, ...] = ()
    store_false: None = None
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @property
    def evidence_records(self):
        """Expose the shared evidence-record contract used by the compiler."""

        return self.evidence_state.records

    @model_validator(mode="after")
    def require_host_only_evidence(self) -> Self:
        if not (
            self.source_commitment == self.evidence_state.source_commitment
            and self.request_fingerprint == self.evidence_state.request_fingerprint
            and self.evidence_call_count == len(self.evidence_state.records)
            and self.evidence_fingerprint == self.evidence_state.evidence_fingerprint
        ):
            raise ValueError("Hosted evidence ledger differs from bounded evidence.")
        if self.returned_model_ids or self.usage or self.store_false is not None:
            raise ValueError("Hosted evidence cannot claim direct API metadata.")
        if (self.clarification_question is None) != (self.clarification_answer is None):
            raise ValueError("Hosted clarification question and answer must coincide.")
        payload = self.model_dump(mode="json", exclude={"transcript_fingerprint"})
        if self.transcript_fingerprint != canonical_sha256(payload):
            raise ValueError("Hosted evidence transcript fingerprint is invalid.")
        return self


class FolderHostPendingRevisionV1(StrictFrozenModel):
    """Exact hosted revision reservation without API-provider assumptions."""

    schema_version: Literal["folder-host-pending-revision.v1"] = (
        "folder-host-pending-revision.v1"
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    model_transport: HostModelTransport
    expected_job_revision: int = Field(ge=0)
    proposal_revision: int = Field(ge=0, le=2)
    response_turn: int = Field(ge=2, le=MAX_HOST_RESPONSE_TURNS)
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    prior_transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    pending_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_fingerprint(self) -> Self:
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"pending_fingerprint"})
        )
        if self.pending_fingerprint != expected:
            raise ValueError("Hosted pending-revision fingerprint is invalid.")
        return self


class FolderHostRevisionTurnRecordV1(StrictFrozenModel):
    """One observable host-model sparse revision and deterministic outcome."""

    schema_version: Literal["folder-host-revision-turn-record.v1"] = (
        "folder-host-revision-turn-record.v1"
    )
    model_transport: HostModelTransport
    response_turn: int = Field(ge=2, le=MAX_HOST_RESPONSE_TURNS)
    call_id: str = Field(min_length=1, max_length=128)
    pending_revision_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    prior_transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision: FolderHostPlanRevisionV1
    outcome: Literal["accepted", "rejected"]
    accepted_plan_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    failure_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    failure_detail: str | None = Field(default=None, min_length=1, max_length=2_000)
    turn_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_outcome_and_fingerprint(self) -> Self:
        if self.outcome == "accepted":
            if (
                self.accepted_plan_fingerprint is None
                or self.failure_code is not None
                or self.failure_detail is not None
            ):
                raise ValueError("Accepted hosted revision has invalid outcome fields.")
        elif (
            self.accepted_plan_fingerprint is not None
            or self.failure_code is None
            or self.failure_detail is None
        ):
            raise ValueError("Rejected hosted revision lacks deterministic failure.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"turn_fingerprint"})
        )
        if self.turn_fingerprint != expected:
            raise ValueError("Hosted revision-turn fingerprint is invalid.")
        return self


class FolderHostDerivativePendingRevisionV1(StrictFrozenModel):
    """Exact hosted derivative reservation before its first model response."""

    schema_version: Literal["folder-host-derivative-pending-revision.v1"] = (
        "folder-host-derivative-pending-revision.v1"
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    model_transport: HostModelTransport
    expected_job_revision: int = Field(ge=0)
    proposal_revision: Literal[0] = 0
    response_turn: Literal[1] = 1
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    initial_evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_state: PlannerEvidenceState
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    prior_transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)
    turn_contract_freeze_fingerprint: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)
    match_report_fingerprint: str = Field(pattern=SHA256_PATTERN)
    immediate_parent_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    pending_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_derivative_parent_and_fingerprint(self) -> Self:
        if (
            self.base_candidate_fingerprint
            != self.immediate_parent_candidate_fingerprint
        ):
            raise ValueError(
                "Hosted derivative pending turn names another parent candidate."
            )
        if self.evidence_state.evidence_fingerprint != self.evidence_fingerprint:
            raise ValueError(
                "Hosted derivative pending evidence is not self-consistent."
            )
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"pending_fingerprint"})
        )
        if self.pending_fingerprint != expected:
            raise ValueError("Hosted derivative pending fingerprint is invalid.")
        return self


class FolderHostDerivativeRevisionTurnRecordV1(StrictFrozenModel):
    """First observable hosted sparse turn for one derivative child."""

    schema_version: Literal["folder-host-derivative-revision-turn-record.v1"] = (
        "folder-host-derivative-revision-turn-record.v1"
    )
    model_transport: HostModelTransport
    response_turn: Literal[1] = 1
    call_id: str = Field(min_length=1, max_length=128)
    pending_revision_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    prior_transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)
    turn_contract_freeze_fingerprint: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)
    match_report_fingerprint: str = Field(pattern=SHA256_PATTERN)
    immediate_parent_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision: FolderHostPlanRevisionV1
    outcome: Literal["accepted", "rejected"]
    accepted_plan_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    failure_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    failure_detail: str | None = Field(default=None, min_length=1, max_length=2_000)
    turn_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_outcome_parent_and_fingerprint(self) -> Self:
        if not (
            self.base_candidate_fingerprint
            == self.immediate_parent_candidate_fingerprint
            == self.revision.base_candidate_fingerprint
        ):
            raise ValueError("Hosted derivative turn names another parent candidate.")
        if self.outcome == "accepted":
            if (
                self.accepted_plan_fingerprint is None
                or self.failure_code is not None
                or self.failure_detail is not None
            ):
                raise ValueError(
                    "Accepted hosted derivative has invalid outcome fields."
                )
        elif (
            self.accepted_plan_fingerprint is not None
            or self.failure_code is None
            or self.failure_detail is None
        ):
            raise ValueError("Rejected hosted derivative lacks deterministic failure.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"turn_fingerprint"})
        )
        if self.turn_fingerprint != expected:
            raise ValueError("Hosted derivative turn fingerprint is invalid.")
        return self


def build_host_event(model_type, **values):
    """Build one canonical host event without duplicating hash-domain code."""

    draft = model_type.model_construct(**values, event_fingerprint="0" * 64)
    return model_type(
        **values,
        event_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"event_fingerprint"})
        ),
    )


def build_host_planning_state(**values) -> FolderHostPlanningStateV1:
    """Build one canonical hosted planning checkpoint."""

    draft = FolderHostPlanningStateV1.model_construct(
        **values,
        state_fingerprint="0" * 64,
    )
    return FolderHostPlanningStateV1(
        **values,
        state_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"state_fingerprint"})
        ),
    )


def build_host_compiler_failure(**values) -> FolderHostCompilerFailureV1:
    """Build one canonical deterministic hosted compiler failure."""

    draft = FolderHostCompilerFailureV1.model_construct(
        **values,
        failure_fingerprint="0" * 64,
    )
    return FolderHostCompilerFailureV1(
        **values,
        failure_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"failure_fingerprint"})
        ),
    )


def build_host_evidence_ledger(**values) -> FolderHostEvidenceLedgerV1:
    """Build one canonical accepted hosted evidence ledger."""

    draft = FolderHostEvidenceLedgerV1.model_construct(
        **values,
        transcript_fingerprint="0" * 64,
    )
    return FolderHostEvidenceLedgerV1(
        **values,
        transcript_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"transcript_fingerprint"})
        ),
    )


def build_host_pending_revision(**values) -> FolderHostPendingRevisionV1:
    """Build one canonical hosted revision reservation."""

    draft = FolderHostPendingRevisionV1.model_construct(
        **values,
        pending_fingerprint="0" * 64,
    )
    return FolderHostPendingRevisionV1(
        **values,
        pending_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"pending_fingerprint"})
        ),
    )


def build_host_revision_turn(**values) -> FolderHostRevisionTurnRecordV1:
    """Build one canonical observable hosted revision turn."""

    draft = FolderHostRevisionTurnRecordV1.model_construct(
        **values,
        turn_fingerprint="0" * 64,
    )
    return FolderHostRevisionTurnRecordV1(
        **values,
        turn_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"turn_fingerprint"})
        ),
    )


def build_host_derivative_pending_revision(
    **values,
) -> FolderHostDerivativePendingRevisionV1:
    """Build one canonical provider-free hosted derivative reservation."""

    draft = FolderHostDerivativePendingRevisionV1.model_construct(
        **values,
        pending_fingerprint="0" * 64,
    )
    return FolderHostDerivativePendingRevisionV1(
        **values,
        pending_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"pending_fingerprint"})
        ),
    )


def build_host_derivative_revision_turn(
    **values,
) -> FolderHostDerivativeRevisionTurnRecordV1:
    """Build one canonical observable hosted derivative sparse turn."""

    draft = FolderHostDerivativeRevisionTurnRecordV1.model_construct(
        **values,
        turn_fingerprint="0" * 64,
    )
    return FolderHostDerivativeRevisionTurnRecordV1(
        **values,
        turn_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"turn_fingerprint"})
        ),
    )


def host_contract_freeze_fingerprint() -> str:
    """Fingerprint the complete observable F0c host-planning contract."""

    return canonical_sha256(
        {
            "domain": "foldweave:host-planning-contract-freeze:v1",
            "host_tools": (
                "create_or_resume_planning_job",
                "list_inventory_page",
                "read_text_excerpt",
                "inspect_markdown_links",
                "submit_plan",
                "request_clarification",
                "answer_clarification",
                "get_plan_preview",
                "get_compiler_failures",
                "revise_plan",
                "submit_plan_revision",
                "job_status",
                "accept_plan_and_create_copy",
                "verify_result",
            ),
            "schemas": {
                "planning_state": FolderHostPlanningStateV1.model_json_schema(),
                "initial_ledger": FolderHostEvidenceLedgerV1.model_json_schema(),
                "pending_revision": FolderHostPendingRevisionV1.model_json_schema(),
                "revision_turn": FolderHostRevisionTurnRecordV1.model_json_schema(),
                "derivative_pending_revision": (
                    FolderHostDerivativePendingRevisionV1.model_json_schema()
                ),
                "derivative_revision_turn": (
                    FolderHostDerivativeRevisionTurnRecordV1.model_json_schema()
                ),
            },
        }
    )
