"""Durable Foldweave v3 review and exact-authorization authority."""

from __future__ import annotations

import os
import uuid
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import TracebackType
from typing import Any, Literal, Self
from zoneinfo import ZoneInfo

from pydantic import Field, field_validator, model_validator

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.connected_change.derivative import (
    FolderDerivativeCreationBindingV1,
    FolderDerivativeParentBindingV1,
)
from name_atlas.folder_refactor.connected_change.job_io import (
    DurableJobFileLock,
    DurableJobLoadError,
    DurableJobLockError,
    DurableJobWriteError,
    atomic_write_regular_file,
    read_stable_regular_file,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    MAX_DURABLE_JOB_BYTES,
    CapsuleAppliedJobAuthorityV2,
    FolderIdempotencyBindingV2,
    FolderOperationIdempotencyBindingV2,
    FolderRefactorJobV2,
    GptPlannedJobAuthorityV2,
    GptPlannerCheckpointV2,
    JobLocalDirectoryIdentityV2,
    JobLocalFileIdentityV2,
    LegacyFolderJobV1Evidence,
    build_change_file_input_binding,
    build_operation_idempotency_binding,
    load_folder_job_record,
    operation_request_fingerprint,
)
from name_atlas.folder_refactor.connected_change.preview import (
    FolderPlanPreviewV1,
    build_folder_plan_preview,
)
from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderInventory,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.foldweave_host_contracts import (
    FolderHostDerivativePendingRevisionV1,
    FolderHostDerivativeRevisionTurnRecordV1,
    FolderHostEvidenceLedgerV1,
    FolderHostPendingRevisionV1,
    FolderHostPlanningStateV1,
    HostModelTransport,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeEvidenceLedgerV1,
    FolderDerivativeRevisionTurnInputV1,
    FolderEvidenceLedgerV2,
    FolderPlannerRevisionTurnInputV1,
    FolderRevisionTurnRecordV1,
    GptPlannedExecutionOriginV2,
    revision_turn_input_fingerprint,
)
from name_atlas.folder_refactor.inventory import FolderScanError, scan_folder
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.portable_artifacts import (
    FolderPortableArtifactError,
    strict_json_object,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

FOLDER_REFACTOR_JOB_V3_SCHEMA_VERSION = "folder-refactor-job.v3"
FOLDER_PUBLIC_JOB_CAPABILITY_SCHEMA_VERSION = "folder-public-job-capability.v1"
FOLDER_EXECUTION_AUTHORIZATION_SCHEMA_VERSION = "folder-execution-authorization.v1"
FOLDER_KEEP_PREVIOUS_ACTION_SCHEMA_VERSION = "folder-keep-previous-action.v1"
FOLDER_HOST_MUTATION_BINDING_SCHEMA_VERSION = "folder-host-mutation-binding.v1"
FOLDER_HOST_REVISION_MUTATION_BINDING_SCHEMA_VERSION = (
    "folder-host-revision-mutation-binding.v1"
)
FOLDER_REVISION_MUTATION_BINDING_SCHEMA_VERSION = "folder-revision-mutation-binding.v1"
FOLDER_DESTINATION_RESERVATION_SCHEMA_VERSION = "folder-destination-reservation.v1"
DEFAULT_V3_JOB_DIRECTORY = Path(".foldweave/jobs")
oslo_tz = ZoneInfo("Europe/Oslo")


class FolderJobV3Error(RuntimeError):
    """Base failure for the Foldweave v3 authority."""


class FolderJobV3LoadError(FolderJobV3Error):
    """A v3 job is absent, corrupt, noncanonical, or unsupported."""


class LegacyV2NonterminalJobError(FolderJobV3LoadError):
    """A nonterminal v2 job cannot be silently interpreted or resumed as v3."""


class FolderJobV3WriteError(FolderJobV3Error):
    """A v3 job could not be persisted without weakening authority."""


class FolderJobV3LockError(FolderJobV3WriteError):
    """Another process currently owns the v3 writer lock."""


class FolderJobV3RevisionError(FolderJobV3WriteError):
    """A requested mutation does not target the exact current revision."""


class FolderJobV3FinalizedError(FolderJobV3WriteError):
    """A terminal v3 job cannot be changed in place."""


class FolderJobV3IdempotencyConflict(FolderJobV3WriteError):
    """An idempotency key is already bound to another exact operation."""


class FolderJobLifecycleV3(StrEnum):
    """Complete lifecycle declared for all Foldweave review-era jobs."""

    MATCHING = "matching"
    PLANNING = "planning"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    REVIEWING = "reviewing"
    REVISING = "revising"
    REVISION_FAILED = "revision_failed"
    EXECUTING = "executing"
    VERIFIED = "verified"
    STALE = "stale"
    BLOCKED = "blocked"

    @property
    def terminal(self) -> bool:
        """Return whether no further mutation is permitted."""

        return self in {self.VERIFIED, self.STALE, self.BLOCKED}


class FolderPublicJobCapabilityV1(StrictFrozenModel):
    """Hashed public authority bound immutably to one durable v3 job."""

    schema_version: Literal["folder-public-job-capability.v1"] = (
        FOLDER_PUBLIC_JOB_CAPABILITY_SCHEMA_VERSION
    )
    capability_id_sha256: str = Field(pattern=SHA256_PATTERN)
    device_id: str = Field(pattern=r"^fwd_[a-f0-9]{32}$")
    oauth_grant_fingerprint: str = Field(pattern=SHA256_PATTERN)
    scopes: tuple[
        Literal[
            "foldweave.execute",
            "foldweave.plan",
            "foldweave.review",
        ],
        ...,
    ] = Field(min_length=1, max_length=3)
    expires_at_ms: int = Field(gt=0)

    @model_validator(mode="after")
    def require_canonical_scopes(self) -> Self:
        if self.scopes != tuple(sorted(set(self.scopes))):
            raise ValueError("Public job capability scopes must be sorted and unique.")
        return self


class FolderExecutionAuthorizationV1(StrictFrozenModel):
    """Exact immutable human authorization for one visible preview."""

    schema_version: Literal["folder-execution-authorization.v1"] = (
        FOLDER_EXECUTION_AUTHORIZATION_SCHEMA_VERSION
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    expected_job_revision: int = Field(ge=0)
    proposal_revision: int = Field(ge=0, le=2)
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    output_parent: Path
    output_parent_fingerprint: str = Field(pattern=SHA256_PATTERN)
    result_folder_name: str = Field(min_length=1, max_length=240)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    channel: Literal[
        "native_app",
        "browser",
        "chatgpt_hosted",
        "codex_mcp",
        "local_mcp",
        "cli",
    ]
    authorization_timestamp: datetime
    authorization_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("output_parent")
    @classmethod
    def require_absolute_output_parent(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("Authorized output parent must be absolute.")
        return value

    @field_validator("authorization_timestamp")
    @classmethod
    def require_oslo_timestamp(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value)

    @model_validator(mode="after")
    def require_exact_fingerprint(self) -> Self:
        if self.output_parent_fingerprint != _output_parent_fingerprint(
            self.output_parent
        ):
            raise ValueError("Execution authorization output parent is invalid.")
        expected = _execution_authorization_fingerprint(self)
        if self.authorization_fingerprint != expected:
            raise ValueError("Execution authorization fingerprint is invalid.")
        if (self.imported_change_file_fingerprint is None) != (
            self.match_report_fingerprint is None
        ):
            raise ValueError(
                "Imported execution authorization requires both portable bindings."
            )
        return self


class FolderPortableExecutionAuthorizationV1(StrictFrozenModel):
    """Path-neutral projection of one exact internal execution authorization."""

    schema_version: Literal["folder-execution-authorization.v1"] = (
        FOLDER_EXECUTION_AUTHORIZATION_SCHEMA_VERSION
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    expected_job_revision: int = Field(ge=0)
    proposal_revision: int = Field(ge=0, le=2)
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    output_parent_fingerprint: str = Field(pattern=SHA256_PATTERN)
    result_folder_name: str = Field(min_length=1, max_length=240)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    channel: Literal[
        "native_app",
        "browser",
        "chatgpt_hosted",
        "codex_mcp",
        "local_mcp",
        "cli",
    ]
    authorization_timestamp: datetime
    authorization_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("authorization_timestamp")
    @classmethod
    def require_oslo_timestamp(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value)

    @model_validator(mode="after")
    def require_exact_fingerprint(self) -> Self:
        expected = _execution_authorization_fingerprint(self)
        if self.authorization_fingerprint != expected:
            raise ValueError("Portable execution authorization fingerprint is invalid.")
        if (self.imported_change_file_fingerprint is None) != (
            self.match_report_fingerprint is None
        ):
            raise ValueError(
                "Imported execution authorization requires both portable bindings."
            )
        return self


class FolderRevisionInstructionV1(StrictFrozenModel):
    """One durable user instruction bound to the exact visible preview."""

    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    instruction: str = Field(min_length=1, max_length=20_000)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_instruction_fingerprint(self) -> Self:
        expected = canonical_sha256(
            {
                "domain": "foldweave:revision-instruction:v1",
                "base_candidate_fingerprint": self.base_candidate_fingerprint,
                "base_preview_fingerprint": self.base_preview_fingerprint,
                "instruction": self.instruction,
                "idempotency_key_sha256": self.idempotency_key_sha256,
            }
        )
        if self.instruction_fingerprint != expected:
            raise ValueError("Revision instruction fingerprint is invalid.")
        return self


class FolderRevisionFailureV1(StrictFrozenModel):
    """One failed replacement while the prior complete preview remains valid."""

    code: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    detail: str = Field(min_length=1, max_length=2_000)
    attempted_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)


class FolderRevisionProviderFailureV1(StrictFrozenModel):
    """One provider attempt that produced no mechanically inspectable response."""

    schema_version: Literal["folder-revision-provider-failure.v1"] = (
        "folder-revision-provider-failure.v1"
    )
    attempt_index: int = Field(ge=1, le=2)
    response_turn: int = Field(ge=2, le=8)
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    turn_input_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    code: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    detail: str = Field(min_length=1, max_length=2_000)
    failure_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_failure_fingerprint(self) -> Self:
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"failure_fingerprint"})
        )
        if self.failure_fingerprint != expected:
            raise ValueError("Revision provider failure fingerprint is invalid.")
        return self


class FolderRevisionRejectionRecordV1(StrictFrozenModel):
    """Append-only reason why one observable sparse revision was rejected."""

    schema_version: Literal["folder-revision-rejection-record.v1"] = (
        "folder-revision-rejection-record.v1"
    )
    attempt_index: int = Field(ge=1, le=2)
    response_turn: int = Field(ge=2, le=8)
    segment_fingerprint: str = Field(pattern=SHA256_PATTERN)
    turn_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    contract_freeze_fingerprint: str = Field(pattern=SHA256_PATTERN)
    code: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    detail: str = Field(min_length=1, max_length=2_000)
    record_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_record_fingerprint(self) -> Self:
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"record_fingerprint"})
        )
        if self.record_fingerprint != expected:
            raise ValueError("Revision rejection record fingerprint is invalid.")
        return self


class FolderKeepPreviousActionV1(StrictFrozenModel):
    """One idempotent decision to retain a failed revision's prior preview."""

    schema_version: Literal["folder-keep-previous-action.v1"] = (
        FOLDER_KEEP_PREVIOUS_ACTION_SCHEMA_VERSION
    )
    base_job_revision: int = Field(ge=0)
    candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    action_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_action_fingerprint(self) -> Self:
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"action_fingerprint"})
        )
        if self.action_fingerprint != expected:
            raise ValueError("Keep-previous action fingerprint is invalid.")
        return self


class FolderHostMutationBindingV1(StrictFrozenModel):
    """One exact hosted clarification mutation bound to a caller retry key."""

    schema_version: Literal["folder-host-mutation-binding.v1"] = (
        FOLDER_HOST_MUTATION_BINDING_SCHEMA_VERSION
    )
    operation: Literal["request_clarification", "answer_clarification"]
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    expected_job_revision: int = Field(ge=0)
    question_fingerprint: str = Field(pattern=SHA256_PATTERN)
    answer_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_request_fingerprint(self) -> Self:
        if (self.operation == "request_clarification") != (
            self.answer_fingerprint is None
        ):
            raise ValueError(
                "Hosted clarification answer binding is present on the wrong operation."
            )
        expected = canonical_sha256(
            {
                "domain": "foldweave:host-clarification-mutation-request:v1",
                "operation": self.operation,
                "job_id": self.job_id,
                "expected_job_revision": self.expected_job_revision,
                "question_fingerprint": self.question_fingerprint,
                "answer_fingerprint": self.answer_fingerprint,
            }
        )
        if self.request_fingerprint != expected:
            raise ValueError(
                "Hosted clarification mutation request fingerprint is invalid."
            )
        return self


class FolderRevisionMutationBindingV1(StrictFrozenModel):
    """Append-only terminal outcome for one exact direct revision request."""

    schema_version: Literal["folder-revision-mutation-binding.v1"] = (
        FOLDER_REVISION_MUTATION_BINDING_SCHEMA_VERSION
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    base_job_revision: int = Field(ge=0)
    base_proposal_revision: int = Field(ge=0, le=2)
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    model_transport: Literal[
        "responses_api",
        "recorded_replay",
        "deterministic_development",
    ]
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    terminal_outcome: Literal[
        "proposal_replaced",
        "provider_failed",
        "mechanically_rejected",
    ]
    terminal_job_revision: int = Field(ge=1)
    resulting_proposal_revision: int = Field(ge=0, le=2)
    binding_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_fingerprints(self) -> Self:
        if self.terminal_job_revision != self.base_job_revision + 2:
            raise ValueError(
                "Direct revision binding must end two durable transitions "
                "after its base."
            )
        expected_proposal_revision = (
            self.base_proposal_revision + 1
            if self.terminal_outcome == "proposal_replaced"
            else self.base_proposal_revision
        )
        if self.resulting_proposal_revision != expected_proposal_revision:
            raise ValueError(
                "Direct revision outcome has an invalid proposal revision."
            )
        request_payload = {
            "domain": "foldweave:direct-revision-mutation-request:v1",
            "job_id": self.job_id,
            "base_job_revision": self.base_job_revision,
            "base_proposal_revision": self.base_proposal_revision,
            "base_candidate_fingerprint": self.base_candidate_fingerprint,
            "base_preview_fingerprint": self.base_preview_fingerprint,
            "revision_instruction_fingerprint": (self.revision_instruction_fingerprint),
            "model_transport": self.model_transport,
        }
        if self.request_fingerprint != canonical_sha256(request_payload):
            raise ValueError("Direct revision request fingerprint is invalid.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"binding_fingerprint"})
        )
        if self.binding_fingerprint != expected:
            raise ValueError("Direct revision mutation binding is invalid.")
        return self


class FolderHostRevisionMutationBindingV1(StrictFrozenModel):
    """Append-only terminal outcome for one exact hosted revision request."""

    schema_version: Literal["folder-host-revision-mutation-binding.v1"] = (
        FOLDER_HOST_REVISION_MUTATION_BINDING_SCHEMA_VERSION
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    base_job_revision: int = Field(ge=0)
    base_proposal_revision: int = Field(ge=0, le=2)
    base_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    base_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    model_transport: HostModelTransport
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    terminal_outcome: Literal["proposal_replaced", "mechanically_rejected"]
    terminal_job_revision: int = Field(ge=1)
    resulting_proposal_revision: int = Field(ge=0, le=2)
    binding_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_fingerprints(self) -> Self:
        if self.terminal_job_revision != self.base_job_revision + 2:
            raise ValueError(
                "Hosted revision binding must end two durable transitions "
                "after its base."
            )
        expected_proposal_revision = (
            self.base_proposal_revision + 1
            if self.terminal_outcome == "proposal_replaced"
            else self.base_proposal_revision
        )
        if self.resulting_proposal_revision != expected_proposal_revision:
            raise ValueError(
                "Hosted revision outcome has an invalid proposal revision."
            )
        request_payload = {
            "domain": "foldweave:hosted-revision-mutation-request:v1",
            "job_id": self.job_id,
            "base_job_revision": self.base_job_revision,
            "base_candidate_fingerprint": self.base_candidate_fingerprint,
            "base_preview_fingerprint": self.base_preview_fingerprint,
            "revision_instruction_fingerprint": (self.revision_instruction_fingerprint),
            "model_transport": self.model_transport,
        }
        if self.request_fingerprint != canonical_sha256(request_payload):
            raise ValueError("Hosted revision request fingerprint is invalid.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"binding_fingerprint"})
        )
        if self.binding_fingerprint != expected:
            raise ValueError("Hosted revision mutation binding is invalid.")
        return self


class FolderDestinationReservationV1(StrictFrozenModel):
    """One canonical result destination won before copy execution begins."""

    schema_version: Literal["folder-destination-reservation.v1"] = (
        FOLDER_DESTINATION_RESERVATION_SCHEMA_VERSION
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    authorized_job_revision: int = Field(ge=0)
    proposal_revision: int = Field(ge=0, le=2)
    candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    output_parent: Path
    result_folder_name: str = Field(min_length=1, max_length=240)
    final_result_path: Path
    reservation_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("output_parent", "final_result_path")
    @classmethod
    def require_canonical_absolute_path(cls, value: Path) -> Path:
        if not value.is_absolute() or value.resolve(strict=False) != value:
            raise ValueError(
                "Destination reservation paths must be canonical absolute paths."
            )
        return value

    @model_validator(mode="after")
    def require_exact_destination(self) -> Self:
        if (
            Path(self.result_folder_name).name != self.result_folder_name
            or self.result_folder_name in {".", ".."}
            or self.final_result_path
            != (self.output_parent / self.result_folder_name).resolve(strict=False)
        ):
            raise ValueError("Destination reservation names another result path.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"reservation_fingerprint"})
        )
        if self.reservation_fingerprint != expected:
            raise ValueError("Destination reservation fingerprint is invalid.")
        return self


class FolderJobStalenessV3(StrictFrozenModel):
    """Terminal observed evidence that an execution input changed."""

    code: Literal[
        "source_changed",
        "source_unreadable",
        "change_file_changed",
        "change_file_unreadable",
    ]
    detail: str = Field(min_length=1, max_length=2_000)


class FolderJobVerifiedArtifactsV3(StrictFrozenModel):
    """Minimal proof identities for one independently verified result."""

    receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    organized_tree_commitment: str = Field(pattern=SHA256_PATTERN)
    change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)
    verification_fingerprint: str = Field(pattern=SHA256_PATTERN)
    verification_status: Literal["verified"] = "verified"


class GptPlannedJobAuthorityV3(StrictFrozenModel):
    """Append-only initial and revision planning authority for new v3 jobs."""

    authority_schema_version: Literal["folder-gpt-planned-job-authority.v3"]
    kind: Literal["gpt_planned"] = "gpt_planned"
    planner_checkpoint: GptPlannerCheckpointV2
    evidence_ledger: FolderEvidenceLedgerV2 | None = None
    execution_origin: GptPlannedExecutionOriginV2 | None = None
    pending_revision_turn: FolderPlannerRevisionTurnInputV1 | None = None

    @model_validator(mode="after")
    def require_composite_authority(self) -> Self:
        accepted = self.planner_checkpoint.status == "accepted"
        if not (
            accepted
            == (self.evidence_ledger is not None)
            == (self.execution_origin is not None)
        ):
            raise ValueError(
                "Accepted v3 planning, evidence, and provenance must coincide."
            )
        if self.pending_revision_turn is not None and not accepted:
            raise ValueError("A pending revision requires accepted initial planning.")
        if self.evidence_ledger is not None:
            initial_fingerprint = self.planner_checkpoint.accepted_plan_fingerprint
            if (
                initial_fingerprint is None
                or self.evidence_ledger.segments[0].final_candidate_fingerprint
                != initial_fingerprint
            ):
                raise ValueError(
                    "Composite v3 evidence differs from the initial planner checkpoint."
                )
            checkpoint_progress = self.planner_checkpoint.progress
            initial = self.evidence_ledger.initial_ledger
            if checkpoint_progress is None or not (
                checkpoint_progress.status == "accepted"
                and initial.response_turn_count == checkpoint_progress.response_turns
                and initial.evidence_call_count == checkpoint_progress.evidence_calls
                and initial.clarification_question
                == checkpoint_progress.clarification_question
                and initial.clarification_answer
                == checkpoint_progress.clarification_answer
                and initial.usage == self.planner_checkpoint.usage
                and initial.observable_turns == checkpoint_progress.turns
                and initial.accepted_plan_fingerprint
                == self.planner_checkpoint.accepted_plan_fingerprint
            ):
                raise ValueError(
                    "Composite v3 evidence lacks its complete initial progress."
                )
        if self.execution_origin is not None:
            ledger = self.evidence_ledger
            expected_provider_calls = (
                ledger.response_turn_count
                if ledger is not None and ledger.model_transport == "responses_api"
                else 0
            )
            if ledger is None or not (
                self.execution_origin.evidence_fingerprint
                == ledger.evidence_fingerprint
                and self.execution_origin.evidence_transcript_fingerprint
                == ledger.transcript_fingerprint
                and self.execution_origin.accepted_plan_fingerprint
                == ledger.accepted_plan_fingerprint
                and self.execution_origin.provider_call_count == expected_provider_calls
            ):
                raise ValueError("V3 execution origin differs from composite evidence.")
        return self


class GptHostedJobAuthorityV3(StrictFrozenModel):
    """Observable ChatGPT/Codex planning authority with no direct API claims."""

    authority_schema_version: Literal["folder-gpt-hosted-job-authority.v3"] = (
        "folder-gpt-hosted-job-authority.v3"
    )
    kind: Literal["gpt_hosted"] = "gpt_hosted"
    model_transport: HostModelTransport
    planning_state: FolderHostPlanningStateV1
    evidence_ledger: FolderEvidenceLedgerV2 | None = None
    execution_origin: GptPlannedExecutionOriginV2 | None = None
    pending_revision: FolderHostPendingRevisionV1 | None = None

    @model_validator(mode="after")
    def require_truthful_hosted_authority(self) -> Self:
        accepted = self.planning_state.status == "accepted"
        if not (
            accepted
            == (self.evidence_ledger is not None)
            == (self.execution_origin is not None)
        ):
            raise ValueError(
                "Accepted hosted planning, evidence, and provenance must coincide."
            )
        if self.model_transport != self.planning_state.model_transport:
            raise ValueError("Hosted authority and planning transport disagree.")
        if self.pending_revision is not None and not accepted:
            raise ValueError("Hosted revision requires accepted initial planning.")
        if self.evidence_ledger is not None:
            initial = self.evidence_ledger.initial_ledger
            if not isinstance(initial, FolderHostEvidenceLedgerV1):
                raise ValueError("Hosted authority requires hosted initial evidence.")
            state = self.planning_state
            if not (
                self.evidence_ledger.model_transport == self.model_transport
                and initial.provider_kind == self.model_transport
                and initial.job_id == state.job_id
                and initial.source_commitment == state.source_commitment
                and initial.request_fingerprint == state.request_fingerprint
                and initial.evidence_state == state.evidence_state
                and initial.observable_records
                == tuple(event.model_dump(mode="json") for event in state.events)
                and initial.response_turn_count == state.response_turn_count
                and initial.plan_submission_count == state.plan_submission_count
                and initial.accepted_plan_fingerprint == state.accepted_plan_fingerprint
            ):
                raise ValueError(
                    "Hosted composite evidence differs from planning state."
                )
        if self.execution_origin is not None:
            ledger = self.evidence_ledger
            if ledger is None or not (
                self.execution_origin.model_transport == self.model_transport
                and self.execution_origin.provider_call_count == 0
                and not self.execution_origin.api_used
                and self.execution_origin.store_false is None
                and self.execution_origin.model_alias is None
                and not self.execution_origin.returned_model_ids
                and self.execution_origin.evidence_fingerprint
                == ledger.evidence_fingerprint
                and self.execution_origin.evidence_transcript_fingerprint
                == ledger.transcript_fingerprint
                and self.execution_origin.accepted_plan_fingerprint
                == ledger.accepted_plan_fingerprint
            ):
                raise ValueError("Hosted provenance differs from composite evidence.")
        if self.pending_revision is not None and (
            self.pending_revision.model_transport != self.model_transport
        ):
            raise ValueError("Hosted pending revision uses another transport.")
        return self


class GptDerivativeJobAuthorityV3(StrictFrozenModel):
    """Schema-distinct derivative child before or after one sparse response."""

    authority_schema_version: Literal["folder-gpt-derivative-job-authority.v3"] = (
        "folder-gpt-derivative-job-authority.v3"
    )
    kind: Literal["gpt_derivative"] = "gpt_derivative"
    authority_state: Literal["awaiting_model_response", "completed", "failed"]
    model_transport: Literal[
        "responses_api",
        "chatgpt_hosted",
        "codex_hosted",
        "recorded_replay",
        "deterministic_development",
    ]
    parent_binding: FolderDerivativeParentBindingV1
    creation_binding: FolderDerivativeCreationBindingV1
    pending_direct_revision: FolderDerivativeRevisionTurnInputV1 | None = None
    pending_host_revision: FolderHostDerivativePendingRevisionV1 | None = None
    pending_direct_followup_revision: FolderPlannerRevisionTurnInputV1 | None = None
    pending_host_followup_revision: FolderHostPendingRevisionV1 | None = None
    evidence_ledger: FolderEvidenceLedgerV2 | None = None
    execution_origin: GptPlannedExecutionOriginV2 | None = None
    failure: FolderRevisionFailureV1 | None = None
    failed_host_revision: FolderHostDerivativeRevisionTurnRecordV1 | None = None

    @model_validator(mode="after")
    def require_derivative_authority(self) -> Self:
        parent = self.parent_binding
        creation = self.creation_binding
        if not (
            creation.parent_binding_fingerprint == parent.binding_fingerprint
            and creation.source_root == parent.parent_source_root
            and creation.model_transport == self.model_transport
        ):
            raise ValueError("Derivative creation differs from its immutable parent.")
        direct = self.model_transport in {
            "responses_api",
            "recorded_replay",
            "deterministic_development",
        }
        if self.authority_state == "awaiting_model_response":
            if (
                (self.pending_direct_revision is not None) != direct
                or (self.pending_host_revision is not None) == direct
                or self.pending_direct_followup_revision is not None
                or self.pending_host_followup_revision is not None
                or self.evidence_ledger is not None
                or self.execution_origin is not None
                or self.failure is not None
                or self.failed_host_revision is not None
            ):
                raise ValueError(
                    "Pending derivative authority requires exactly one transport turn."
                )
            if direct:
                self._require_pending_direct()
            else:
                self._require_pending_host()
        elif self.authority_state == "completed" and (
            self.pending_direct_revision is not None
            or self.pending_host_revision is not None
            or self.evidence_ledger is None
            or self.execution_origin is None
            or self.failure is not None
            or self.failed_host_revision is not None
        ):
            raise ValueError(
                "Completed derivative authority requires evidence and provenance only."
            )
        elif self.authority_state == "completed":
            self._require_completed()
        elif (
            self.pending_direct_revision is not None
            or self.pending_host_revision is not None
            or self.pending_direct_followup_revision is not None
            or self.pending_host_followup_revision is not None
            or self.evidence_ledger is not None
            or self.execution_origin is not None
            or self.failure is None
        ):
            raise ValueError(
                "Failed derivative authority requires only exact failure evidence."
            )
        elif (
            self.failure.attempted_instruction_fingerprint
            != creation.revision_instruction_fingerprint
        ):
            raise ValueError("Derivative failure targets another instruction.")
        elif self.model_transport in {"chatgpt_hosted", "codex_hosted"}:
            failed_turn = self.failed_host_revision
            if failed_turn is not None and not (
                failed_turn.outcome == "rejected"
                and failed_turn.model_transport == self.model_transport
                and failed_turn.revision_instruction_fingerprint
                == creation.revision_instruction_fingerprint
                and failed_turn.failure_code == self.failure.code
                and failed_turn.failure_detail == self.failure.detail
            ):
                raise ValueError(
                    "Hosted derivative failure differs from its observable turn."
                )
        return self

    def _require_pending_direct(self) -> None:
        turn = self.pending_direct_revision
        assert turn is not None
        parent = self.parent_binding
        creation = self.creation_binding
        expected_provider_kind = {
            "responses_api": "live",
            "recorded_replay": "recorded_replay",
            "deterministic_development": "deterministic",
        }.get(self.model_transport)
        if not (
            turn.job_id == creation.child_job_id
            and turn.proposal_revision == 0
            and turn.response_turn == 1
            and turn.provider_kind == expected_provider_kind
            and turn.source_commitment == parent.parent_source_commitment
            and turn.request_fingerprint == parent.parent_candidate.request_fingerprint
            and turn.base_candidate == parent.parent_candidate
            and turn.base_candidate_fingerprint == parent.parent_candidate_fingerprint
            and turn.base_preview_fingerprint == parent.parent_preview_fingerprint
            and turn.revision_instruction_fingerprint
            == creation.revision_instruction_fingerprint
            and turn.evidence_fingerprint == creation.evidence_fingerprint
            and turn.prior_transcript_fingerprint == creation.binding_fingerprint
            and turn.turn_contract_freeze_fingerprint
            == creation.contract_freeze_fingerprint
            and turn.imported_change_file_fingerprint
            == parent.imported_change_file_fingerprint
            and turn.match_report_fingerprint
            == parent.match_report.match_report_fingerprint
            and turn.immediate_parent_candidate_fingerprint
            == parent.parent_candidate_fingerprint
        ):
            raise ValueError("Pending direct derivative targets another parent review.")

    def _require_pending_host(self) -> None:
        turn = self.pending_host_revision
        assert turn is not None
        parent = self.parent_binding
        creation = self.creation_binding
        if not (
            turn.job_id == creation.child_job_id
            and turn.model_transport == self.model_transport
            and turn.proposal_revision == 0
            and turn.response_turn == 1
            and turn.base_candidate_fingerprint == parent.parent_candidate_fingerprint
            and turn.base_preview_fingerprint == parent.parent_preview_fingerprint
            and turn.revision_instruction_fingerprint
            == creation.revision_instruction_fingerprint
            and turn.initial_evidence_fingerprint == creation.evidence_fingerprint
            and turn.evidence_state.source_commitment == parent.parent_source_commitment
            and turn.evidence_state.request_fingerprint
            == parent.parent_candidate.request_fingerprint
            and turn.evidence_fingerprint == turn.evidence_state.evidence_fingerprint
            and turn.prior_transcript_fingerprint == creation.binding_fingerprint
            and turn.turn_contract_freeze_fingerprint
            == creation.contract_freeze_fingerprint
            and turn.imported_change_file_fingerprint
            == parent.imported_change_file_fingerprint
            and turn.match_report_fingerprint
            == parent.match_report.match_report_fingerprint
            and turn.immediate_parent_candidate_fingerprint
            == parent.parent_candidate_fingerprint
        ):
            raise ValueError("Pending hosted derivative targets another parent review.")

    def _require_completed(self) -> None:
        ledger = self.evidence_ledger
        origin = self.execution_origin
        assert ledger is not None
        assert origin is not None
        initial = ledger.initial_ledger
        parent = self.parent_binding
        creation = self.creation_binding
        if not isinstance(initial, FolderDerivativeEvidenceLedgerV1):
            raise ValueError("Derivative authority requires derivative-first evidence.")
        if not (
            ledger.planning_basis == "derivative"
            and ledger.model_transport == self.model_transport
            and ledger.job_id == creation.child_job_id
            and ledger.source_commitment == parent.parent_source_commitment
            and ledger.request_fingerprint
            == parent.parent_candidate.request_fingerprint
            and initial.parent_binding_fingerprint == parent.binding_fingerprint
            and initial.creation_binding_fingerprint == creation.binding_fingerprint
            and initial.contract_freeze_fingerprint
            == creation.contract_freeze_fingerprint
            and initial.imported_change_file_fingerprint
            == parent.imported_change_file_fingerprint
            and initial.match_report_fingerprint
            == parent.match_report.match_report_fingerprint
            and initial.immediate_parent_candidate_fingerprint
            == parent.parent_candidate_fingerprint
            and initial.immediate_parent_preview_fingerprint
            == parent.parent_preview_fingerprint
            and initial.revision_instruction_fingerprint
            == creation.revision_instruction_fingerprint
            and (
                self.model_transport in {"chatgpt_hosted", "codex_hosted"}
                or initial.evidence_fingerprint == creation.evidence_fingerprint
            )
            and origin.kind == "gpt_revised_from_change_file"
            and origin.planning_basis == "derivative"
            and origin.model_transport == self.model_transport
            and origin.imported_change_file_fingerprint
            == parent.imported_change_file_fingerprint
            and origin.match_report_fingerprint
            == parent.match_report.match_report_fingerprint
            and origin.evidence_fingerprint == ledger.evidence_fingerprint
            and origin.evidence_transcript_fingerprint == ledger.transcript_fingerprint
            and origin.accepted_plan_fingerprint == ledger.accepted_plan_fingerprint
        ):
            raise ValueError(
                "Completed derivative evidence or provenance names another parent."
            )
        direct_pending = self.pending_direct_followup_revision
        host_pending = self.pending_host_followup_revision
        if direct_pending is not None and host_pending is not None:
            raise ValueError("Derivative follow-up has competing transport turns.")
        if direct_pending is not None and not (
            self.model_transport
            in {"responses_api", "recorded_replay", "deterministic_development"}
            and direct_pending.job_id == creation.child_job_id
            and direct_pending.proposal_revision == ledger.selected_proposal_revision
            and direct_pending.base_candidate_fingerprint
            == ledger.accepted_plan_fingerprint
            and direct_pending.evidence_fingerprint == ledger.evidence_fingerprint
            and direct_pending.prior_transcript_fingerprint
            == ledger.transcript_fingerprint
            and direct_pending.imported_change_file_fingerprint
            == parent.imported_change_file_fingerprint
            and direct_pending.match_report_fingerprint
            == parent.match_report.match_report_fingerprint
            and direct_pending.immediate_parent_candidate_fingerprint
            == parent.parent_candidate_fingerprint
        ):
            raise ValueError(
                "Direct derivative follow-up targets another completed transcript."
            )
        if host_pending is not None and not (
            self.model_transport in {"chatgpt_hosted", "codex_hosted"}
            and host_pending.job_id == creation.child_job_id
            and host_pending.model_transport == self.model_transport
            and host_pending.proposal_revision == ledger.selected_proposal_revision
            and host_pending.base_candidate_fingerprint
            == ledger.accepted_plan_fingerprint
            and host_pending.evidence_fingerprint == ledger.evidence_fingerprint
            and host_pending.prior_transcript_fingerprint
            == ledger.transcript_fingerprint
        ):
            raise ValueError(
                "Hosted derivative follow-up targets another completed transcript."
            )


# Existing F0a-era v3 files used the predecessor v2 authority. Keep them readable
# without weakening new-work authority. The two GPT models share a `kind` literal,
# so schema-shape validation, not an ambiguous discriminator, performs dispatch.
FolderJobAuthorityV3 = (
    GptDerivativeJobAuthorityV3
    | GptHostedJobAuthorityV3
    | GptPlannedJobAuthorityV3
    | GptPlannedJobAuthorityV2
    | CapsuleAppliedJobAuthorityV2
)


class FolderRefactorJobV3(StrictFrozenModel):
    """Sole durable authority for one Foldweave review-era transaction."""

    schema_version: Literal["folder-refactor-job.v3"] = (
        FOLDER_REFACTOR_JOB_V3_SCHEMA_VERSION
    )
    revision: int = Field(ge=0)
    proposal_revision: int = Field(default=0, ge=0, le=2)
    revision_attempt_count: int = Field(default=0, ge=0, le=2)
    clarification_count: int = Field(default=0, ge=0, le=1)
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    display_name: str = Field(min_length=1, max_length=200)
    created_at: datetime
    updated_at: datetime
    source_root: Path
    output_parent: Path
    job_path: Path
    source_inventory: FolderInventory
    local_file_identities: tuple[JobLocalFileIdentityV2, ...]
    local_directory_identities: tuple[JobLocalDirectoryIdentityV2, ...]
    user_request: str = Field(min_length=1, max_length=20_000)
    idempotency: FolderIdempotencyBindingV2
    operation_idempotency: tuple[FolderOperationIdempotencyBindingV2, ...] = Field(
        min_length=1,
        max_length=1,
    )
    public_job_capability: FolderPublicJobCapabilityV1 | None = None
    authority: FolderJobAuthorityV3
    candidate_plan: FolderAcceptedPlanV2 | None = None
    reference_graph: FolderReferenceGraph | None = None
    preview: FolderPlanPreviewV1 | None = None
    revision_instruction: FolderRevisionInstructionV1 | None = None
    revision_failure: FolderRevisionFailureV1 | None = None
    revision_provider_failures: tuple[FolderRevisionProviderFailureV1, ...] = Field(
        default=(),
        max_length=2,
    )
    revision_rejections: tuple[FolderRevisionRejectionRecordV1, ...] = Field(
        default=(),
        max_length=2,
    )
    keep_previous_actions: tuple[FolderKeepPreviousActionV1, ...] = Field(
        default=(),
        max_length=2,
    )
    host_mutation_bindings: tuple[FolderHostMutationBindingV1, ...] = Field(
        default=(),
        max_length=2,
    )
    revision_mutation_bindings: tuple[FolderRevisionMutationBindingV1, ...] = Field(
        default=(),
        max_length=2,
    )
    host_revision_mutation_bindings: tuple[FolderHostRevisionMutationBindingV1, ...] = (
        Field(
            default=(),
            max_length=2,
        )
    )
    immediate_parent_job_id: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{32}$",
    )
    immediate_parent_candidate_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    execution_authorization: FolderExecutionAuthorizationV1 | None = None
    destination_reservation: FolderDestinationReservationV1 | None = None
    pending_result_path: Path | None = None
    final_result_path: Path | None = None
    verified_artifacts: FolderJobVerifiedArtifactsV3 | None = None
    lifecycle: FolderJobLifecycleV3
    blocker_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    blocker_message: str | None = Field(default=None, min_length=1, max_length=2_000)
    staleness: FolderJobStalenessV3 | None = None

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("Foldweave job IDs must be lowercase UUID4 hex.")
        return value

    @field_validator("created_at", "updated_at")
    @classmethod
    def require_job_oslo_timestamp(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value)

    @field_validator(
        "source_root",
        "output_parent",
        "job_path",
        "pending_result_path",
        "final_result_path",
    )
    @classmethod
    def require_absolute_paths(cls, value: Path | None) -> Path | None:
        if value is not None and not value.is_absolute():
            raise ValueError("Foldweave job paths must be absolute.")
        return value

    @model_validator(mode="after")
    def require_complete_authority(self) -> Self:
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot precede created_at.")
        reconstruction = self.operation_idempotency[0]
        expected_request_fingerprint = operation_request_fingerprint(
            operation="recreate_original",
            request={"job_handle": self.job_id},
        )
        if not (
            reconstruction.operation == "recreate_original"
            and reconstruction.request_fingerprint == expected_request_fingerprint
        ):
            raise ValueError(
                "V3 jobs require one exact prebound reconstruction operation."
            )
        if self.preview is not None:
            if self.candidate_plan is None or self.reference_graph is None:
                raise ValueError(
                    "A preview requires one complete candidate and reference graph."
                )
            if (
                self.preview.job_id != self.job_id
                or self.preview.source_commitment
                != self.source_inventory.source_commitment
                or self.preview.proposal_revision != self.proposal_revision
                or self.preview.compiled_candidate_fingerprint
                != canonical_sha256(self.candidate_plan)
            ):
                raise ValueError("Preview targets another job, source, or candidate.")
            self._require_preview_authority()
            rebuilt = build_folder_plan_preview(
                job_id=self.job_id,
                expected_job_revision=self.preview.expected_job_revision,
                proposal_revision=self.proposal_revision,
                proposal_basis=self.preview.proposal_basis,
                inventory=self.source_inventory,
                reference_graph=self.reference_graph,
                accepted_plan=self.candidate_plan,
                imported_change_file_fingerprint=(
                    self.preview.imported_change_file_fingerprint
                ),
                match_report_fingerprint=self.preview.match_report_fingerprint,
                immediate_parent_candidate_fingerprint=(
                    self.preview.immediate_parent_candidate_fingerprint
                ),
            )
            if rebuilt != self.preview:
                raise ValueError(
                    "Persisted preview differs from its deterministic candidate "
                    "projection."
                )
        if self.candidate_plan is not None and (
            self.candidate_plan.source_commitment
            != self.source_inventory.source_commitment
        ):
            raise ValueError("Candidate plan targets another source.")
        if self.candidate_plan is not None and (
            self.candidate_plan.request_fingerprint
            != request_fingerprint(self.user_request)
        ):
            raise ValueError("Candidate plan targets another user request.")
        if isinstance(self.authority, GptPlannedJobAuthorityV3):
            ledger = self.authority.evidence_ledger
            origin = self.authority.execution_origin
            if self.candidate_plan is not None and (
                ledger is None
                or origin is None
                or not (
                    self.candidate_plan.evidence_schema_version
                    == "folder-evidence-ledger.v2"
                    and ledger.accepted_plan_fingerprint
                    == canonical_sha256(self.candidate_plan)
                    and ledger.evidence_fingerprint
                    == self.candidate_plan.evidence_fingerprint
                    and ledger.selected_proposal_revision == self.proposal_revision
                    and ledger.user_revision_count
                    + len(self.revision_provider_failures)
                    + (1 if self.authority.pending_revision_turn is not None else 0)
                    == self.revision_attempt_count
                    and origin.accepted_plan_fingerprint
                    == ledger.accepted_plan_fingerprint
                )
            ):
                raise ValueError(
                    "V3 candidate differs from its planning evidence authority."
                )
            if self.lifecycle is FolderJobLifecycleV3.REVISING:
                if (
                    self.authority.pending_revision_turn is None
                    or self.revision_instruction is None
                    or self.candidate_plan is None
                    or self.preview is None
                ):
                    raise ValueError(
                        "Revising requires the prior preview and reserved "
                        "provider turn."
                    )
                self._require_pending_revision_authority()
            elif (
                self.authority.pending_revision_turn is not None
                and self.lifecycle is not FolderJobLifecycleV3.BLOCKED
            ):
                raise ValueError(
                    "Only revising or terminal provider failure may retain a "
                    "pending provider turn."
                )
            elif self.authority.pending_revision_turn is not None:
                self._require_pending_revision_authority()
        elif isinstance(self.authority, GptHostedJobAuthorityV3):
            ledger = self.authority.evidence_ledger
            origin = self.authority.execution_origin
            if self.candidate_plan is not None and (
                ledger is None
                or origin is None
                or not (
                    self.candidate_plan.evidence_schema_version
                    == "folder-evidence-ledger.v2"
                    and ledger.accepted_plan_fingerprint
                    == canonical_sha256(self.candidate_plan)
                    and ledger.evidence_fingerprint
                    == self.candidate_plan.evidence_fingerprint
                    and ledger.selected_proposal_revision == self.proposal_revision
                    and ledger.user_revision_count
                    + (1 if self.authority.pending_revision is not None else 0)
                    == self.revision_attempt_count
                    and origin.accepted_plan_fingerprint
                    == ledger.accepted_plan_fingerprint
                )
            ):
                raise ValueError(
                    "Hosted candidate differs from its planning evidence authority."
                )
            if self.lifecycle is FolderJobLifecycleV3.REVISING:
                if (
                    self.authority.pending_revision is None
                    or self.revision_instruction is None
                    or self.candidate_plan is None
                    or self.preview is None
                ):
                    raise ValueError(
                        "Hosted revising requires the prior preview and exact "
                        "revision reservation."
                    )
                self._require_pending_host_revision_authority()
            elif (
                self.authority.pending_revision is not None
                and self.lifecycle is not FolderJobLifecycleV3.BLOCKED
            ):
                raise ValueError(
                    "Only hosted revising or terminal failure may retain a "
                    "pending revision."
                )
            elif self.authority.pending_revision is not None:
                self._require_pending_host_revision_authority()
        elif isinstance(self.authority, GptDerivativeJobAuthorityV3):
            parent = self.authority.parent_binding
            creation = self.authority.creation_binding
            derivative_state = self.authority.authority_state
            initial_instruction_required = (
                derivative_state in {"awaiting_model_response", "failed"}
                or self.revision_attempt_count == 1
            )
            if not (
                self.job_id == creation.child_job_id
                and self.job_path == creation.child_job_path
                and self.source_root == creation.source_root
                and self.output_parent == creation.output_parent
                and self.source_inventory.source_commitment
                == parent.parent_source_commitment
                and self.immediate_parent_job_id == parent.parent_job_id
                and self.immediate_parent_candidate_fingerprint
                == parent.parent_candidate_fingerprint
                and self.revision_instruction is not None
                and (
                    not initial_instruction_required
                    or self.revision_instruction.instruction_fingerprint
                    == creation.revision_instruction_fingerprint
                )
            ):
                raise ValueError(
                    "Derivative job identity differs from its parent or "
                    "creation binding."
                )
            if derivative_state == "awaiting_model_response":
                if not (
                    self.lifecycle
                    in {
                        FolderJobLifecycleV3.REVISING,
                        FolderJobLifecycleV3.STALE,
                    }
                    and self.proposal_revision == 0
                    and self.revision_attempt_count == 1
                    and self.candidate_plan is None
                    and self.reference_graph is None
                    and self.preview is None
                ):
                    raise ValueError(
                        "Pending derivative child must contain no model-produced plan."
                    )
            elif derivative_state == "failed":
                failure = self.authority.failure
                if not (
                    self.lifecycle
                    in {
                        FolderJobLifecycleV3.REVISION_FAILED,
                        FolderJobLifecycleV3.REVIEWING,
                    }
                    and self.proposal_revision == 0
                    and self.revision_attempt_count == 1
                    and self.candidate_plan == parent.parent_candidate
                    and self.reference_graph is not None
                    and self.preview is not None
                    and self.preview.job_id == self.job_id
                    and self.preview.proposal_basis == "imported_change_file"
                    and self.preview.compiled_candidate_fingerprint
                    == parent.parent_candidate_fingerprint
                    and failure is not None
                    and self.blocker_code is None
                    and self.blocker_message is None
                ):
                    raise ValueError(
                        "Failed derivative child must preserve its imported parent "
                        "review."
                    )
            else:
                ledger = self.authority.evidence_ledger
                origin = self.authority.execution_origin
                pending_direct_followup = (
                    self.authority.pending_direct_followup_revision
                )
                pending_host_followup = self.authority.pending_host_followup_revision
                pending_followup_count = sum(
                    item is not None
                    for item in (pending_direct_followup, pending_host_followup)
                )
                if (
                    self.candidate_plan is None
                    or self.preview is None
                    or ledger is None
                    or origin is None
                    or not (
                        self.candidate_plan.evidence_schema_version
                        == "folder-evidence-ledger.v2"
                        and ledger.accepted_plan_fingerprint
                        == canonical_sha256(self.candidate_plan)
                        and ledger.evidence_fingerprint
                        == self.candidate_plan.evidence_fingerprint
                        and ledger.selected_proposal_revision == self.proposal_revision
                        and ledger.user_revision_count + pending_followup_count
                        == self.revision_attempt_count
                        and origin.accepted_plan_fingerprint
                        == ledger.accepted_plan_fingerprint
                    )
                ):
                    raise ValueError(
                        "Derivative candidate differs from its completed authority."
                    )
                if self.lifecycle is FolderJobLifecycleV3.REVISING:
                    if (
                        pending_followup_count != 1
                        or self.revision_instruction is None
                        or self.candidate_plan is None
                        or self.preview is None
                    ):
                        raise ValueError(
                            "Hosted derivative follow-up requires the prior preview "
                            "and exact reservation."
                        )
                    if pending_host_followup is not None:
                        self._require_pending_host_derivative_followup_authority()
                elif pending_followup_count:
                    raise ValueError(
                        "Derivative follow-up may exist only while revising."
                    )
        if self.lifecycle in {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
        }:
            if self.candidate_plan is None or self.preview is None:
                raise ValueError("Reviewing requires a complete persisted preview.")
            if self.preview.expected_job_revision != self.revision:
                raise ValueError("Review preview does not target the current revision.")
            if (
                self.execution_authorization is not None
                or self.pending_result_path is not None
                or self.final_result_path is not None
                or self.verified_artifacts is not None
            ):
                raise ValueError("Reviewing cannot retain execution output authority.")
        elif self.lifecycle is FolderJobLifecycleV3.EXECUTING:
            self._require_authorized_execution()
            if self.verified_artifacts is not None:
                raise ValueError("Executing cannot already contain verified proof.")
        elif self.lifecycle is FolderJobLifecycleV3.VERIFIED:
            self._require_authorized_execution()
            if self.pending_result_path is not None:
                raise ValueError("Verified jobs cannot retain pending output.")
            if self.verified_artifacts is None:
                raise ValueError("Verified jobs require proof identities.")
        elif self.lifecycle in {
            FolderJobLifecycleV3.MATCHING,
            FolderJobLifecycleV3.PLANNING,
            FolderJobLifecycleV3.AWAITING_CLARIFICATION,
        }:
            if any(
                value is not None
                for value in (
                    self.candidate_plan,
                    self.reference_graph,
                    self.preview,
                    self.execution_authorization,
                    self.pending_result_path,
                    self.final_result_path,
                    self.verified_artifacts,
                )
            ):
                raise ValueError("Pre-review jobs cannot retain proposal output.")
        elif self.lifecycle is FolderJobLifecycleV3.REVISING:
            if self.execution_authorization is not None or any(
                value is not None
                for value in (
                    self.pending_result_path,
                    self.final_result_path,
                    self.verified_artifacts,
                )
            ):
                raise ValueError("Revising cannot retain execution output authority.")
        if self.lifecycle is FolderJobLifecycleV3.REVISION_FAILED:
            if self.revision_failure is None:
                raise ValueError("revision_failed requires exact failure evidence.")
            if isinstance(
                self.authority,
                (
                    GptPlannedJobAuthorityV3,
                    GptHostedJobAuthorityV3,
                    GptDerivativeJobAuthorityV3,
                ),
            ) and (
                self.revision_instruction is None
                or self.revision_failure.attempted_instruction_fingerprint
                != self.revision_instruction.instruction_fingerprint
            ):
                raise ValueError("Revision failure targets another instruction.")
        elif self.revision_failure is not None:
            raise ValueError("Only revision_failed may retain revision failure.")
        provider_instruction_fingerprints = tuple(
            failure.revision_instruction_fingerprint
            for failure in self.revision_provider_failures
        )
        if len(provider_instruction_fingerprints) != len(
            set(provider_instruction_fingerprints)
        ):
            raise ValueError("Revision provider failures must be unique.")
        provider_attempts = tuple(
            failure.attempt_index for failure in self.revision_provider_failures
        )
        if provider_attempts != tuple(sorted(provider_attempts)):
            raise ValueError("Revision provider failures must be attempt ordered.")
        rejection_attempts = tuple(
            rejection.attempt_index for rejection in self.revision_rejections
        )
        if rejection_attempts != tuple(sorted(set(rejection_attempts))):
            raise ValueError("Revision rejections must be unique and attempt ordered.")
        if isinstance(self.authority, GptPlannedJobAuthorityV3):
            self._require_revision_rejection_history()
        keep_keys = tuple(
            action.idempotency_key_sha256 for action in self.keep_previous_actions
        )
        if len(keep_keys) != len(set(keep_keys)):
            raise ValueError("Keep-previous idempotency keys must be unique.")
        host_mutation_keys = tuple(
            binding.idempotency_key_sha256 for binding in self.host_mutation_bindings
        )
        if len(host_mutation_keys) != len(set(host_mutation_keys)):
            raise ValueError("Hosted mutation idempotency keys must be unique.")
        if self.host_mutation_bindings and not isinstance(
            self.authority, GptHostedJobAuthorityV3
        ):
            raise ValueError("Hosted mutation bindings require hosted authority.")
        if any(
            binding.job_id != self.job_id for binding in self.host_mutation_bindings
        ):
            raise ValueError("Hosted mutation binding targets another job.")
        revision_mutation_keys = tuple(
            binding.idempotency_key_sha256
            for binding in self.revision_mutation_bindings
        )
        if len(revision_mutation_keys) != len(set(revision_mutation_keys)):
            raise ValueError("Direct revision mutation keys must be unique.")
        direct_revision_authority = isinstance(
            self.authority,
            GptPlannedJobAuthorityV3,
        ) or (
            isinstance(self.authority, GptDerivativeJobAuthorityV3)
            and self.authority.model_transport
            in {"responses_api", "recorded_replay", "deterministic_development"}
        )
        if self.revision_mutation_bindings and not direct_revision_authority:
            raise ValueError(
                "Direct revision bindings require direct planning authority."
            )
        if any(
            binding.job_id != self.job_id for binding in self.revision_mutation_bindings
        ):
            raise ValueError("Direct revision mutation binding targets another job.")
        terminal_revisions = tuple(
            binding.terminal_job_revision for binding in self.revision_mutation_bindings
        )
        if terminal_revisions != tuple(sorted(set(terminal_revisions))):
            raise ValueError(
                "Direct revision mutation bindings must be terminal-revision ordered."
            )
        host_revision_mutation_keys = tuple(
            binding.idempotency_key_sha256
            for binding in self.host_revision_mutation_bindings
        )
        if len(host_revision_mutation_keys) != len(set(host_revision_mutation_keys)):
            raise ValueError("Hosted revision mutation keys must be unique.")
        hosted_revision_authority = isinstance(
            self.authority,
            GptHostedJobAuthorityV3,
        ) or (
            isinstance(self.authority, GptDerivativeJobAuthorityV3)
            and self.authority.model_transport in {"chatgpt_hosted", "codex_hosted"}
        )
        if self.host_revision_mutation_bindings and not hosted_revision_authority:
            raise ValueError(
                "Hosted revision bindings require hosted planning authority."
            )
        if any(
            binding.job_id != self.job_id
            for binding in self.host_revision_mutation_bindings
        ):
            raise ValueError("Hosted revision mutation binding targets another job.")
        host_terminal_revisions = tuple(
            binding.terminal_job_revision
            for binding in self.host_revision_mutation_bindings
        )
        if host_terminal_revisions != tuple(sorted(set(host_terminal_revisions))):
            raise ValueError(
                "Hosted revision mutation bindings must be terminal-revision ordered."
            )
        if self.destination_reservation is not None:
            reservation = self.destination_reservation
            historical_without_authorization = (
                self.lifecycle
                in {FolderJobLifecycleV3.STALE, FolderJobLifecycleV3.BLOCKED}
                and self.execution_authorization is None
            )
            if (
                reservation.job_id != self.job_id
                or reservation.proposal_revision != self.proposal_revision
                or self.preview is None
                or reservation.candidate_fingerprint
                != self.preview.compiled_candidate_fingerprint
                or reservation.preview_fingerprint != self.preview.preview_fingerprint
                or reservation.output_parent != self.output_parent
                or self.candidate_plan is None
                or reservation.result_folder_name
                != self.candidate_plan.result_folder_name
                or reservation.final_result_path != expected_final_result_path_v3(self)
                or (
                    not historical_without_authorization
                    and (
                        self.execution_authorization is None
                        or reservation.authorized_job_revision
                        != self.execution_authorization.expected_job_revision
                    )
                )
            ):
                raise ValueError("Destination reservation targets another preview.")
        blocker = self.blocker_code is not None or self.blocker_message is not None
        if self.lifecycle is FolderJobLifecycleV3.BLOCKED:
            if self.blocker_code is None or self.blocker_message is None:
                raise ValueError("Blocked jobs require a code and message.")
        elif blocker:
            raise ValueError("Only blocked jobs may retain blocker fields.")
        if self.lifecycle is FolderJobLifecycleV3.STALE:
            if self.staleness is None:
                raise ValueError("Stale jobs require observed staleness evidence.")
        elif self.staleness is not None:
            raise ValueError("Only stale jobs may retain staleness evidence.")
        return self

    def _require_revision_rejection_history(self) -> None:
        ledger = self.authority.evidence_ledger
        if ledger is None:
            if self.revision_rejections:
                raise ValueError(
                    "Revision rejections require accepted planning evidence."
                )
            return
        rejected_segments = tuple(
            segment
            for segment in ledger.segments
            if segment.segment_kind == "user_revision" and not segment.selected
        )
        records_by_segment = {
            record.segment_fingerprint: record for record in self.revision_rejections
        }
        if len(records_by_segment) != len(self.revision_rejections):
            raise ValueError("Revision rejection segments must be unique.")
        for segment in rejected_segments:
            record = records_by_segment.get(segment.segment_fingerprint)
            if record is None:
                legacy_current_failure = (
                    self.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
                    and self.revision_failure is not None
                    and segment is rejected_segments[-1]
                )
                if not legacy_current_failure:
                    raise ValueError(
                        "A past rejected revision lacks append-only failure evidence."
                    )
                continue
            turn = FolderRevisionTurnRecordV1.model_validate_json(
                canonical_json_bytes(segment.observable_records[0]),
                strict=True,
            )
            effective_contract = (
                turn.input.turn_contract_freeze_fingerprint
                or ledger.contract_freeze_fingerprint
            )
            if not (
                record.response_turn == turn.input.response_turn
                and record.turn_fingerprint == turn.turn_fingerprint
                and record.revision_instruction_fingerprint
                == segment.revision_instruction_fingerprint
                == turn.input.revision_instruction_fingerprint
                and record.contract_freeze_fingerprint == effective_contract
            ):
                raise ValueError(
                    "Revision rejection record differs from its transcript segment."
                )
        rejected_fingerprints = {
            segment.segment_fingerprint for segment in rejected_segments
        }
        if set(records_by_segment) - rejected_fingerprints:
            raise ValueError("Revision rejection record names no rejected segment.")
        if (
            self.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
            and self.revision_failure is not None
            and self.revision_rejections
        ):
            latest = self.revision_rejections[-1]
            if (
                latest.segment_fingerprint == rejected_segments[-1].segment_fingerprint
                and latest.revision_instruction_fingerprint
                == self.revision_failure.attempted_instruction_fingerprint
                and not (
                    latest.code == self.revision_failure.code
                    and latest.detail == self.revision_failure.detail
                )
            ):
                raise ValueError(
                    "Current revision failure differs from append-only evidence."
                )

    def _require_pending_revision_authority(self) -> None:
        assert isinstance(self.authority, GptPlannedJobAuthorityV3)
        pending = self.authority.pending_revision_turn
        ledger = self.authority.evidence_ledger
        candidate = self.candidate_plan
        preview = self.preview
        instruction = self.revision_instruction
        assert pending is not None
        assert ledger is not None
        assert candidate is not None
        assert preview is not None
        assert instruction is not None
        expected_provider_kind = {
            "responses_api": "live",
            "recorded_replay": "recorded_replay",
            "deterministic_development": "deterministic",
        }.get(ledger.model_transport)
        expected_revision_delta = (
            1 if self.lifecycle is FolderJobLifecycleV3.REVISING else 2
        )
        if not (
            pending.job_id == self.job_id
            and pending.expected_job_revision == preview.expected_job_revision
            and pending.expected_job_revision + expected_revision_delta == self.revision
            and pending.proposal_revision == self.proposal_revision
            and pending.base_candidate == candidate
            and pending.base_candidate_fingerprint == canonical_sha256(candidate)
            and pending.base_preview_fingerprint == preview.preview_fingerprint
            and pending.revision_instruction == instruction.instruction
            and pending.revision_instruction_fingerprint
            == instruction.instruction_fingerprint
            and pending.prior_transcript_fingerprint == ledger.transcript_fingerprint
            and pending.response_turn == ledger.response_turn_count + 1
            and pending.source_commitment == self.source_inventory.source_commitment
            and pending.request == self.user_request
            and pending.request_fingerprint == request_fingerprint(self.user_request)
            and pending.evidence_fingerprint == ledger.evidence_fingerprint
            and pending.provider_kind == expected_provider_kind
        ):
            raise ValueError("Pending revision targets another durable review.")

    def _require_pending_host_revision_authority(self) -> None:
        assert isinstance(self.authority, GptHostedJobAuthorityV3)
        pending = self.authority.pending_revision
        ledger = self.authority.evidence_ledger
        candidate = self.candidate_plan
        preview = self.preview
        instruction = self.revision_instruction
        assert pending is not None
        assert ledger is not None
        assert candidate is not None
        assert preview is not None
        assert instruction is not None
        expected_revision_delta = (
            1 if self.lifecycle is FolderJobLifecycleV3.REVISING else 2
        )
        if not (
            pending.job_id == self.job_id
            and pending.expected_job_revision == preview.expected_job_revision
            and pending.expected_job_revision + expected_revision_delta == self.revision
            and pending.proposal_revision == self.proposal_revision
            and pending.base_candidate_fingerprint == canonical_sha256(candidate)
            and pending.base_preview_fingerprint == preview.preview_fingerprint
            and pending.revision_instruction_fingerprint
            == instruction.instruction_fingerprint
            and pending.idempotency_key_sha256 == instruction.idempotency_key_sha256
            and pending.prior_transcript_fingerprint == ledger.transcript_fingerprint
            and pending.response_turn == ledger.response_turn_count + 1
            and pending.evidence_fingerprint == ledger.evidence_fingerprint
            and pending.model_transport == self.authority.model_transport
        ):
            raise ValueError("Hosted pending revision targets another durable review.")

    def _require_pending_host_derivative_followup_authority(self) -> None:
        assert isinstance(self.authority, GptDerivativeJobAuthorityV3)
        pending = self.authority.pending_host_followup_revision
        ledger = self.authority.evidence_ledger
        candidate = self.candidate_plan
        preview = self.preview
        instruction = self.revision_instruction
        assert pending is not None
        assert ledger is not None
        assert candidate is not None
        assert preview is not None
        assert instruction is not None
        if not (
            pending.job_id == self.job_id
            and pending.expected_job_revision == preview.expected_job_revision
            and pending.expected_job_revision + 1 == self.revision
            and pending.proposal_revision == self.proposal_revision
            and pending.base_candidate_fingerprint == canonical_sha256(candidate)
            and pending.base_preview_fingerprint == preview.preview_fingerprint
            and pending.revision_instruction_fingerprint
            == instruction.instruction_fingerprint
            and pending.idempotency_key_sha256 == instruction.idempotency_key_sha256
            and pending.prior_transcript_fingerprint == ledger.transcript_fingerprint
            and pending.response_turn == ledger.response_turn_count + 1
            and pending.evidence_fingerprint == ledger.evidence_fingerprint
            and pending.model_transport == self.authority.model_transport
        ):
            raise ValueError(
                "Hosted derivative follow-up targets another durable review."
            )

    def _require_preview_authority(self) -> None:
        assert self.preview is not None
        assert self.reference_graph is not None
        if (
            self.reference_graph.source_commitment
            != self.source_inventory.source_commitment
        ):
            raise ValueError("Preview reference graph targets another source.")
        if isinstance(self.authority, CapsuleAppliedJobAuthorityV2):
            match_report = self.authority.match_report
            if (
                self.preview.proposal_basis != "imported_change_file"
                or match_report is None
                or self.preview.imported_change_file_fingerprint
                != (
                    self.authority.change_file_binding.change_file.change_file_fingerprint
                )
                or self.preview.match_report_fingerprint
                != match_report.match_report_fingerprint
            ):
                raise ValueError(
                    "Imported preview differs from its portable authority."
                )
        elif isinstance(self.authority, GptDerivativeJobAuthorityV3):
            parent = self.authority.parent_binding
            completed_preview = (
                self.authority.authority_state == "completed"
                and self.preview.proposal_basis == "gpt_derivative"
                and self.preview.immediate_parent_candidate_fingerprint
                == parent.parent_candidate_fingerprint
            )
            failed_parent_preview = (
                self.authority.authority_state == "failed"
                and self.preview.proposal_basis == "imported_change_file"
                and self.preview.immediate_parent_candidate_fingerprint is None
                and self.preview.compiled_candidate_fingerprint
                == parent.parent_candidate_fingerprint
            )
            if not (
                (completed_preview or failed_parent_preview)
                and self.preview.imported_change_file_fingerprint
                == parent.imported_change_file_fingerprint
                and self.preview.match_report_fingerprint
                == parent.match_report.match_report_fingerprint
            ):
                raise ValueError(
                    "Derivative preview differs from its immutable parent authority."
                )
        elif (
            self.preview.imported_change_file_fingerprint is not None
            or self.preview.match_report_fingerprint is not None
            or self.preview.proposal_basis
            != (
                "gpt_derivative"
                if self.immediate_parent_candidate_fingerprint is not None
                else "fresh_gpt_plan"
            )
        ):
            raise ValueError("GPT preview differs from its planning authority.")

    def _require_authorized_execution(self) -> None:
        authorization = self.execution_authorization
        if (
            self.candidate_plan is None
            or self.preview is None
            or authorization is None
            or self.final_result_path is None
        ):
            raise ValueError(
                "Execution requires candidate, preview, and authorization."
            )
        if self.lifecycle is FolderJobLifecycleV3.EXECUTING and (
            self.pending_result_path is None
        ):
            raise ValueError("Executing requires its exact pending output path.")
        if (
            authorization.job_id != self.job_id
            or authorization.expected_job_revision != self.preview.expected_job_revision
            or authorization.proposal_revision != self.proposal_revision
            or authorization.source_commitment
            != self.source_inventory.source_commitment
            or authorization.candidate_fingerprint
            != self.preview.compiled_candidate_fingerprint
            or authorization.preview_fingerprint != self.preview.preview_fingerprint
            or authorization.imported_change_file_fingerprint
            != self.preview.imported_change_file_fingerprint
            or authorization.match_report_fingerprint
            != self.preview.match_report_fingerprint
            or authorization.output_parent != self.output_parent
            or authorization.result_folder_name
            != self.candidate_plan.result_folder_name
        ):
            raise ValueError("Execution authorization targets another preview.")
        if self.final_result_path != (
            self.output_parent / self.candidate_plan.result_folder_name
        ):
            raise ValueError("Final result path differs from the authorized result.")
        if self.pending_result_path is not None and self.pending_result_path != (
            self.output_parent / f".name-atlas-{self.job_id}.pending"
        ):
            raise ValueError("Pending result path differs from the authorized job.")


def build_recreate_original_operation_binding_v3(
    *,
    job_id: str,
    idempotency_key: str,
) -> FolderOperationIdempotencyBindingV2:
    """Prebind the sole terminal-safe reconstruction mutation for one v3 job."""

    parsed = uuid.UUID(hex=job_id)
    if parsed.version != 4 or parsed.hex != job_id:
        raise ValueError("Foldweave job IDs must be lowercase UUID4 hex.")
    return build_operation_idempotency_binding(
        operation="recreate_original",
        idempotency_key=idempotency_key,
        request={"job_handle": job_id},
    )


def require_recreate_original_operation_idempotency_v3(
    job: FolderRefactorJobV3,
    *,
    idempotency_key: str,
) -> None:
    """Require the exact prebound reconstruction key without mutating a job."""

    candidate = build_operation_idempotency_binding(
        operation="recreate_original",
        idempotency_key=idempotency_key,
        request={"job_handle": job.job_id},
    )
    if job.operation_idempotency != (candidate,):
        raise FolderJobV3IdempotencyConflict(
            "recreate_original idempotency key is not bound to this exact job."
        )


def require_recreate_original_operation_authority_v3(
    job: FolderRefactorJobV3,
) -> None:
    """Require the job's immutable reconstruction authority without its raw seed."""

    expected_request_fingerprint = operation_request_fingerprint(
        operation="recreate_original",
        request={"job_handle": job.job_id},
    )
    if len(job.operation_idempotency) != 1:
        raise FolderJobV3IdempotencyConflict(
            "recreate_original requires one immutable job-bound authority."
        )
    binding = job.operation_idempotency[0]
    if not (
        binding.operation == "recreate_original"
        and binding.request_fingerprint == expected_request_fingerprint
    ):
        raise FolderJobV3IdempotencyConflict(
            "recreate_original authority is not bound to this exact job."
        )


FolderJobRecordV3 = (
    FolderRefactorJobV3 | FolderRefactorJobV2 | LegacyFolderJobV1Evidence
)


def evolve_job_v3(job: FolderRefactorJobV3, **updates: Any) -> FolderRefactorJobV3:
    """Build one fully validated v3 successor candidate."""

    return FolderRefactorJobV3.model_validate(
        {**job.model_dump(mode="python"), **updates},
        strict=True,
    )


def canonical_job_v3_bytes(job: FolderRefactorJobV3) -> bytes:
    """Serialize every declared field deterministically with one final newline."""

    return canonical_json_bytes(job) + b"\n"


def parse_job_v3_bytes(data: bytes, *, expected_path: Path) -> FolderRefactorJobV3:
    """Strictly parse one canonical v3 record at its bound local path."""

    try:
        raw = strict_json_object(data)
        job = FolderRefactorJobV3.model_validate_json(data, strict=True)
    except (FolderPortableArtifactError, ValueError) as exc:
        raise FolderJobV3LoadError("FolderRefactorJobV3 is corrupt.") from exc
    if canonical_json_bytes(raw) + b"\n" != data:
        raise FolderJobV3LoadError("FolderRefactorJobV3 is not canonical JSON.")
    if job.job_path != expected_path.resolve(strict=False):
        raise FolderJobV3LoadError("FolderRefactorJobV3 points to another path.")
    return job


def load_folder_job_record_v3(path: Path) -> FolderJobRecordV3:
    """Dispatch v3 plus terminal, byte-preserved v1/v2 historical evidence."""

    try:
        observed = read_stable_regular_file(path, max_bytes=MAX_DURABLE_JOB_BYTES)
        raw = strict_json_object(observed.payload)
    except (DurableJobLoadError, FolderPortableArtifactError) as exc:
        raise FolderJobV3LoadError("Durable job is unreadable or invalid.") from exc
    if raw.get("schema_version") == FOLDER_REFACTOR_JOB_V3_SCHEMA_VERSION:
        return parse_job_v3_bytes(observed.payload, expected_path=observed.path)
    try:
        record = load_folder_job_record(observed.path)
    except Exception as exc:
        raise FolderJobV3LoadError("Unsupported durable job schema.") from exc
    if isinstance(record, FolderRefactorJobV2) and not record.lifecycle.terminal:
        raise LegacyV2NonterminalJobError(
            "Nonterminal folder-refactor-job.v2 state cannot be resumed as v3; "
            "create a fresh FolderRefactorJobV3 from the unchanged source."
        )
    return record


class FolderRefactorJobV3Store:
    """Path-bound strict load, rehydration, and mutation entry point."""

    def __init__(
        self,
        path: Path,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock or (lambda: datetime.now(tz=oslo_tz))

    def inspect(self) -> FolderRefactorJobV3:
        """Read one exact v3 job without mutation."""

        record = load_folder_job_record_v3(self.path)
        if not isinstance(record, FolderRefactorJobV3):
            raise FolderJobV3LoadError(
                "Historical v1/v2 jobs are read-only; create a fresh v3 job."
            )
        return record

    def load(self) -> FolderRefactorJobV3:
        """Load and terminally persist any detected input staleness."""

        with self.writer() as writer:
            return writer.rehydrate()

    def writer(self) -> FolderRefactorJobV3Writer:
        return FolderRefactorJobV3Writer(self.path, clock=self._clock)


class FolderRefactorJobV3Writer:
    """Exclusive exact-revision mutation authority for one v3 job file."""

    def __init__(self, path: Path, *, clock: Callable[[], datetime]) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock
        self._lock = DurableJobFileLock(self.path)

    def __enter__(self) -> Self:
        try:
            self._lock.__enter__()
        except DurableJobLockError as exc:
            raise FolderJobV3LockError(str(exc)) from exc
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._lock.__exit__(exc_type, exc_value, traceback)

    def load(self) -> FolderRefactorJobV3:
        self._require_lock()
        return FolderRefactorJobV3Store(self.path).inspect()

    def rehydrate(self) -> FolderRefactorJobV3:
        """Return current state or atomically persist one stale transition."""

        current = self.load()
        if current.lifecycle.terminal:
            return current
        if (
            current.lifecycle is FolderJobLifecycleV3.EXECUTING
            and current.final_result_path is not None
            and os.path.lexists(current.final_result_path)
        ):
            # Promotion is the transaction commit point. A process may stop before
            # the final job checkpoint; independent result verification must recover
            # that state before later source changes are interpreted as pre-commit
            # staleness.
            return current
        evidence = _detect_input_staleness(current)
        if evidence is None:
            return current
        stale = evolve_job_v3(
            current,
            revision=current.revision + 1,
            updated_at=self._now(),
            lifecycle=FolderJobLifecycleV3.STALE,
            staleness=evidence,
            pending_result_path=None,
            final_result_path=None,
            execution_authorization=None,
        )
        _write_job_v3(self.path, stale)
        return stale

    def save_new(self, job: FolderRefactorJobV3) -> FolderRefactorJobV3:
        """Persist one exact revision-zero job while inputs remain stable."""

        self._require_lock()
        if os.path.lexists(self.path):
            raise FolderJobV3RevisionError("Durable job already exists.")
        if job.job_path != self.path or job.revision != 0:
            raise FolderJobV3RevisionError(
                "A new v3 job requires its exact path and revision zero."
            )
        if _detect_input_staleness(job) is not None:
            raise FolderJobV3WriteError("Job input changed before persistence.")
        _write_job_v3(self.path, job)
        return job

    def save(
        self,
        successor: FolderRefactorJobV3,
        *,
        expected_current: FolderRefactorJobV3,
    ) -> FolderRefactorJobV3:
        """Persist one fully validated next revision against the exact current job."""

        self._require_lock()
        current = self.load()
        _require_exact_checkpoint(current, expected_current)
        if current.lifecycle.terminal:
            raise FolderJobV3FinalizedError("Terminal v3 jobs are immutable.")
        if successor.revision != current.revision + 1:
            raise FolderJobV3RevisionError("Successor must be the next revision.")
        _require_immutable_identity(current, successor)
        _require_lifecycle_transition(current.lifecycle, successor.lifecycle)
        _require_transition_payload(current, successor)
        _require_append_only_action_history(current, successor)
        promoted_execution = (
            current.lifecycle is FolderJobLifecycleV3.EXECUTING
            and current.final_result_path is not None
            and os.path.lexists(current.final_result_path)
            and successor.lifecycle is FolderJobLifecycleV3.VERIFIED
        )
        if not promoted_execution and _detect_input_staleness(current) is not None:
            return self.rehydrate()
        _write_job_v3(self.path, successor)
        return successor

    def _now(self) -> datetime:
        return _require_oslo_timestamp(self._clock())

    def _require_lock(self) -> None:
        if not self._lock.held:
            raise FolderJobV3WriteError("V3 writes require an active writer lock.")


def build_execution_authorization(
    *,
    job: FolderRefactorJobV3,
    expected_job_revision: int,
    preview_fingerprint: str,
    candidate_fingerprint: str,
    output_parent: Path,
    result_folder_name: str,
    idempotency_key: str,
    channel: Literal[
        "native_app",
        "browser",
        "chatgpt_hosted",
        "codex_mcp",
        "local_mcp",
        "cli",
    ],
    clock: Callable[[], datetime] | None = None,
) -> FolderExecutionAuthorizationV1:
    """Bind one exact user action without persisting the plaintext retry key."""

    preview = job.preview
    if preview is None:
        raise FolderJobV3RevisionError("The job has no reviewable preview.")
    timestamp = (clock or (lambda: datetime.now(tz=oslo_tz)))()
    resolved_output_parent = output_parent.resolve(strict=False)
    payload = {
        "schema_version": FOLDER_EXECUTION_AUTHORIZATION_SCHEMA_VERSION,
        "job_id": job.job_id,
        "expected_job_revision": expected_job_revision,
        "proposal_revision": job.proposal_revision,
        "source_commitment": job.source_inventory.source_commitment,
        "imported_change_file_fingerprint": (preview.imported_change_file_fingerprint),
        "match_report_fingerprint": preview.match_report_fingerprint,
        "candidate_fingerprint": candidate_fingerprint,
        "preview_fingerprint": preview_fingerprint,
        "output_parent": resolved_output_parent,
        "output_parent_fingerprint": _output_parent_fingerprint(resolved_output_parent),
        "result_folder_name": result_folder_name,
        "idempotency_key_sha256": _authorization_key_sha256(idempotency_key),
        "channel": channel,
        "authorization_timestamp": _require_oslo_timestamp(timestamp),
    }
    fingerprint_payload = dict(payload)
    fingerprint_payload.pop("output_parent")
    fingerprint_payload["authorization_timestamp"] = payload[
        "authorization_timestamp"
    ].isoformat()
    return FolderExecutionAuthorizationV1(
        **payload,
        authorization_fingerprint=canonical_sha256(fingerprint_payload),
    )


def build_portable_execution_authorization(
    authorization: FolderExecutionAuthorizationV1,
) -> FolderPortableExecutionAuthorizationV1:
    """Project internal execution authority without disclosing its local path."""

    portable = FolderPortableExecutionAuthorizationV1.model_validate(
        authorization.model_dump(mode="python", exclude={"output_parent"}),
        strict=True,
    )
    if portable.authorization_fingerprint != authorization.authorization_fingerprint:
        raise ValueError("Portable execution authorization changed its identity.")
    return portable


def _output_parent_fingerprint(output_parent: Path) -> str:
    """Bind one exact internal destination without publishing its local path."""

    return canonical_sha256(
        {
            "domain": "foldweave:execution-output-parent:v1",
            "output_parent": output_parent.as_posix(),
        }
    )


def _execution_authorization_fingerprint(
    authorization: (
        FolderExecutionAuthorizationV1 | FolderPortableExecutionAuthorizationV1
    ),
) -> str:
    """Hash the common path-neutral authorization fields."""

    payload = authorization.model_dump(
        mode="json",
        exclude={"authorization_fingerprint", "output_parent"},
    )
    return canonical_sha256(payload)


def build_revision_instruction(
    *,
    base_candidate_fingerprint: str,
    base_preview_fingerprint: str,
    instruction: str,
    idempotency_key: str,
) -> FolderRevisionInstructionV1:
    """Bind one exact user revision without retaining its plaintext retry key."""

    normalized = instruction.strip()
    if not normalized or normalized != instruction or "\x00" in normalized:
        raise FolderJobV3RevisionError(
            "Revision instruction must be nonblank, trimmed UTF-8 text."
        )
    key_sha256 = _revision_key_sha256(idempotency_key)
    payload = {
        "base_candidate_fingerprint": base_candidate_fingerprint,
        "base_preview_fingerprint": base_preview_fingerprint,
        "instruction": instruction,
        "idempotency_key_sha256": key_sha256,
    }
    return FolderRevisionInstructionV1(
        **payload,
        instruction_fingerprint=canonical_sha256(
            {"domain": "foldweave:revision-instruction:v1", **payload}
        ),
    )


def build_revision_mutation_binding(
    *,
    job: FolderRefactorJobV3,
    terminal_outcome: Literal[
        "proposal_replaced",
        "provider_failed",
        "mechanically_rejected",
    ],
    terminal_job_revision: int,
    resulting_proposal_revision: int,
) -> FolderRevisionMutationBindingV1:
    """Finalize one exact direct revision retry binding append-only."""

    if isinstance(job.authority, GptPlannedJobAuthorityV3):
        pending = job.authority.pending_revision_turn
        ledger = job.authority.evidence_ledger
    elif isinstance(job.authority, GptDerivativeJobAuthorityV3) and (
        job.authority.model_transport
        in {"responses_api", "recorded_replay", "deterministic_development"}
    ):
        pending = job.authority.pending_direct_followup_revision
        ledger = job.authority.evidence_ledger
    else:
        raise FolderJobV3RevisionError(
            "Direct revision mutation binding requires direct planning authority."
        )
    instruction = job.revision_instruction
    if pending is None or instruction is None or ledger is None:
        raise FolderJobV3RevisionError(
            "Direct revision mutation binding lacks its reserved provider turn."
        )
    values = {
        "job_id": job.job_id,
        "base_job_revision": pending.expected_job_revision,
        "base_proposal_revision": pending.proposal_revision,
        "base_candidate_fingerprint": pending.base_candidate_fingerprint,
        "base_preview_fingerprint": pending.base_preview_fingerprint,
        "revision_instruction_fingerprint": instruction.instruction_fingerprint,
        "idempotency_key_sha256": instruction.idempotency_key_sha256,
        "model_transport": ledger.model_transport,
        "terminal_outcome": terminal_outcome,
        "terminal_job_revision": terminal_job_revision,
        "resulting_proposal_revision": resulting_proposal_revision,
    }
    request_payload = {
        "domain": "foldweave:direct-revision-mutation-request:v1",
        **{
            key: values[key]
            for key in (
                "job_id",
                "base_job_revision",
                "base_proposal_revision",
                "base_candidate_fingerprint",
                "base_preview_fingerprint",
                "revision_instruction_fingerprint",
                "model_transport",
            )
        },
    }
    values["request_fingerprint"] = canonical_sha256(request_payload)
    draft = FolderRevisionMutationBindingV1.model_construct(
        **values,
        binding_fingerprint="0" * 64,
    )
    return FolderRevisionMutationBindingV1(
        **values,
        binding_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"binding_fingerprint"})
        ),
    )


def build_host_revision_mutation_binding(
    *,
    job: FolderRefactorJobV3,
    terminal_outcome: Literal["proposal_replaced", "mechanically_rejected"],
    terminal_job_revision: int,
    resulting_proposal_revision: int,
) -> FolderHostRevisionMutationBindingV1:
    """Finalize one exact hosted revision retry binding append-only."""

    if isinstance(job.authority, GptHostedJobAuthorityV3):
        pending = job.authority.pending_revision
    elif isinstance(
        job.authority, GptDerivativeJobAuthorityV3
    ) and job.authority.model_transport in {"chatgpt_hosted", "codex_hosted"}:
        pending = job.authority.pending_host_followup_revision
    else:
        raise FolderJobV3RevisionError(
            "Hosted revision mutation binding requires hosted planning authority."
        )
    instruction = job.revision_instruction
    if pending is None or instruction is None:
        raise FolderJobV3RevisionError(
            "Hosted revision mutation binding lacks its reserved host turn."
        )
    values = {
        "job_id": job.job_id,
        "base_job_revision": pending.expected_job_revision,
        "base_proposal_revision": pending.proposal_revision,
        "base_candidate_fingerprint": pending.base_candidate_fingerprint,
        "base_preview_fingerprint": pending.base_preview_fingerprint,
        "revision_instruction_fingerprint": instruction.instruction_fingerprint,
        "idempotency_key_sha256": instruction.idempotency_key_sha256,
        "model_transport": job.authority.model_transport,
        "terminal_outcome": terminal_outcome,
        "terminal_job_revision": terminal_job_revision,
        "resulting_proposal_revision": resulting_proposal_revision,
    }
    request_payload = {
        "domain": "foldweave:hosted-revision-mutation-request:v1",
        **{
            key: values[key]
            for key in (
                "job_id",
                "base_job_revision",
                "base_candidate_fingerprint",
                "base_preview_fingerprint",
                "revision_instruction_fingerprint",
                "model_transport",
            )
        },
    }
    values["request_fingerprint"] = canonical_sha256(request_payload)
    draft = FolderHostRevisionMutationBindingV1.model_construct(
        **values,
        binding_fingerprint="0" * 64,
    )
    return FolderHostRevisionMutationBindingV1(
        **values,
        binding_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"binding_fingerprint"})
        ),
    )


def build_destination_reservation(
    *,
    job: FolderRefactorJobV3,
) -> FolderDestinationReservationV1:
    """Bind the exact canonical reviewed destination before any copy begins."""

    if job.preview is None or job.candidate_plan is None:
        raise FolderJobV3RevisionError(
            "Destination reservation requires one complete reviewed preview."
        )
    output_parent = job.output_parent.resolve(strict=False)
    final_result_path = (output_parent / job.candidate_plan.result_folder_name).resolve(
        strict=False
    )
    values = {
        "job_id": job.job_id,
        "authorized_job_revision": job.revision,
        "proposal_revision": job.proposal_revision,
        "candidate_fingerprint": job.preview.compiled_candidate_fingerprint,
        "preview_fingerprint": job.preview.preview_fingerprint,
        "output_parent": output_parent,
        "result_folder_name": job.candidate_plan.result_folder_name,
        "final_result_path": final_result_path,
    }
    draft = FolderDestinationReservationV1.model_construct(
        **values,
        reservation_fingerprint="0" * 64,
    )
    return FolderDestinationReservationV1(
        **values,
        reservation_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"reservation_fingerprint"})
        ),
    )


def build_revision_provider_failure(
    *,
    attempt_index: int,
    turn_input: FolderPlannerRevisionTurnInputV1,
    code: str,
    detail: str,
) -> FolderRevisionProviderFailureV1:
    """Record a bounded provider failure without fabricating a model response."""

    values = {
        "attempt_index": attempt_index,
        "response_turn": turn_input.response_turn,
        "provider_kind": turn_input.provider_kind,
        "turn_input_fingerprint": revision_turn_input_fingerprint(turn_input),
        "revision_instruction_fingerprint": (
            turn_input.revision_instruction_fingerprint
        ),
        "code": code,
        "detail": detail,
    }
    draft = FolderRevisionProviderFailureV1.model_construct(
        **values,
        failure_fingerprint="0" * 64,
    )
    return FolderRevisionProviderFailureV1(
        **values,
        failure_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"failure_fingerprint"})
        ),
    )


def build_revision_rejection_record(
    *,
    attempt_index: int,
    ledger: FolderEvidenceLedgerV2,
    failure: FolderRevisionFailureV1,
) -> FolderRevisionRejectionRecordV1:
    """Bind a mechanical rejection to its exact immutable transcript turn."""

    segment = ledger.segments[-1]
    if segment.segment_kind != "user_revision" or segment.selected:
        raise FolderJobV3RevisionError(
            "Mechanical rejection requires the latest rejected revision segment."
        )
    turn = FolderRevisionTurnRecordV1.model_validate_json(
        canonical_json_bytes(segment.observable_records[0]),
        strict=True,
    )
    if (
        segment.revision_instruction_fingerprint
        != failure.attempted_instruction_fingerprint
        or turn.input.revision_instruction_fingerprint
        != failure.attempted_instruction_fingerprint
    ):
        raise FolderJobV3RevisionError(
            "Mechanical rejection targets another revision instruction."
        )
    values = {
        "attempt_index": attempt_index,
        "response_turn": turn.input.response_turn,
        "segment_fingerprint": segment.segment_fingerprint,
        "turn_fingerprint": turn.turn_fingerprint,
        "revision_instruction_fingerprint": (failure.attempted_instruction_fingerprint),
        "contract_freeze_fingerprint": (
            turn.input.turn_contract_freeze_fingerprint
            or ledger.contract_freeze_fingerprint
        ),
        "code": failure.code,
        "detail": failure.detail,
    }
    draft = FolderRevisionRejectionRecordV1.model_construct(
        **values,
        record_fingerprint="0" * 64,
    )
    return FolderRevisionRejectionRecordV1(
        **values,
        record_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"record_fingerprint"})
        ),
    )


def build_keep_previous_action(
    *,
    base_job_revision: int,
    candidate_fingerprint: str,
    preview_fingerprint: str,
    idempotency_key: str,
) -> FolderKeepPreviousActionV1:
    """Bind one exact keep decision without retaining its plaintext retry key."""

    values = {
        "base_job_revision": base_job_revision,
        "candidate_fingerprint": candidate_fingerprint,
        "preview_fingerprint": preview_fingerprint,
        "idempotency_key_sha256": _keep_previous_key_sha256(idempotency_key),
    }
    draft = FolderKeepPreviousActionV1.model_construct(
        **values,
        action_fingerprint="0" * 64,
    )
    return FolderKeepPreviousActionV1(
        **values,
        action_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"action_fingerprint"})
        ),
    )


def host_clarification_question_fingerprint(question: str) -> str:
    """Fingerprint one exact, validated hosted clarification question."""

    normalized = question.strip()
    if not normalized or normalized != question or "\x00" in question:
        raise FolderJobV3RevisionError(
            "Clarification question must be nonblank, trimmed UTF-8 text."
        )
    return canonical_sha256(
        {
            "domain": "foldweave:host-clarification-question:v1",
            "text": question,
        }
    )


def build_host_mutation_binding(
    *,
    operation: Literal["request_clarification", "answer_clarification"],
    job_id: str,
    expected_job_revision: int,
    question_fingerprint: str,
    answer: str | None,
    idempotency_key: str,
) -> FolderHostMutationBindingV1:
    """Bind one hosted clarification mutation without persisting plaintext keys."""

    if operation == "request_clarification":
        if answer is not None:
            raise FolderJobV3RevisionError(
                "Clarification request binding cannot contain an answer."
            )
        answer_fingerprint = None
    else:
        if answer is None or not answer or answer != answer.strip() or "\x00" in answer:
            raise FolderJobV3RevisionError(
                "Clarification answer must be nonblank, trimmed UTF-8 text."
            )
        answer_fingerprint = canonical_sha256(
            {
                "domain": "foldweave:host-clarification-answer:v1",
                "text": answer,
            }
        )
    request_payload = {
        "domain": "foldweave:host-clarification-mutation-request:v1",
        "operation": operation,
        "job_id": job_id,
        "expected_job_revision": expected_job_revision,
        "question_fingerprint": question_fingerprint,
        "answer_fingerprint": answer_fingerprint,
    }
    return FolderHostMutationBindingV1(
        operation=operation,
        job_id=job_id,
        expected_job_revision=expected_job_revision,
        question_fingerprint=question_fingerprint,
        answer_fingerprint=answer_fingerprint,
        idempotency_key_sha256=_host_mutation_key_sha256(idempotency_key),
        request_fingerprint=canonical_sha256(request_payload),
    )


def expected_pending_result_path_v3(job: FolderRefactorJobV3) -> Path:
    """Return the existing engine's hidden job-owned pending path."""

    return job.output_parent / f".name-atlas-{job.job_id}.pending"


def expected_final_result_path_v3(job: FolderRefactorJobV3) -> Path:
    if job.candidate_plan is None:
        raise FolderJobV3WriteError("A final path requires a candidate plan.")
    return job.output_parent / job.candidate_plan.result_folder_name


def _write_job_v3(path: Path, job: FolderRefactorJobV3) -> None:
    try:
        atomic_write_regular_file(path, canonical_job_v3_bytes(job))
    except DurableJobWriteError as exc:
        raise FolderJobV3WriteError(str(exc)) from exc


def _detect_input_staleness(
    job: FolderRefactorJobV3,
) -> FolderJobStalenessV3 | None:
    try:
        scan = scan_folder(job.source_root)
    except (FolderScanError, OSError, ValueError) as exc:
        return FolderJobStalenessV3(
            code="source_unreadable",
            detail=f"Selected source cannot be rescanned: {exc}",
        )
    current_files = tuple(
        JobLocalFileIdentityV2.from_scan(item) for item in scan.local_file_identities
    )
    current_directories = tuple(
        JobLocalDirectoryIdentityV2.from_scan(item)
        for item in scan.local_directory_identities
    )
    if (
        scan.inventory != job.source_inventory
        or current_files != job.local_file_identities
        or current_directories != job.local_directory_identities
    ):
        return FolderJobStalenessV3(
            code="source_changed",
            detail="Selected source differs from the immutable review snapshot.",
        )
    change_file_binding = None
    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
        change_file_binding = job.authority.change_file_binding
    elif isinstance(job.authority, GptDerivativeJobAuthorityV3):
        change_file_binding = job.authority.parent_binding.change_file_binding
    if change_file_binding is not None:
        try:
            current_binding = build_change_file_input_binding(change_file_binding.path)
        except Exception as exc:
            return FolderJobStalenessV3(
                code="change_file_unreadable",
                detail=f"Imported Change File cannot be reverified: {exc}",
            )
        if current_binding != change_file_binding:
            return FolderJobStalenessV3(
                code="change_file_changed",
                detail="Imported Change File differs from the reviewed bytes.",
            )
    return None


def _require_exact_checkpoint(
    current: FolderRefactorJobV3,
    expected: FolderRefactorJobV3,
) -> None:
    if current != expected:
        raise FolderJobV3RevisionError("Durable v3 checkpoint changed.")


def _require_immutable_identity(
    current: FolderRefactorJobV3,
    successor: FolderRefactorJobV3,
) -> None:
    fields = (
        "schema_version",
        "job_id",
        "display_name",
        "created_at",
        "source_root",
        "output_parent",
        "job_path",
        "source_inventory",
        "local_file_identities",
        "local_directory_identities",
        "user_request",
        "idempotency",
        "operation_idempotency",
        "public_job_capability",
        "immediate_parent_job_id",
        "immediate_parent_candidate_fingerprint",
    )
    if any(getattr(current, field) != getattr(successor, field) for field in fields):
        raise FolderJobV3RevisionError("V3 mutation changed immutable job identity.")
    if type(current.authority) is not type(successor.authority):
        raise FolderJobV3RevisionError("V3 mutation changed its authority kind.")
    if isinstance(current.authority, CapsuleAppliedJobAuthorityV2) and (
        current.authority.change_file_binding != successor.authority.change_file_binding
    ):
        raise FolderJobV3RevisionError(
            "V3 mutation changed its imported Change File binding."
        )
    if isinstance(current.authority, GptDerivativeJobAuthorityV3):
        successor_authority = successor.authority
        assert isinstance(successor_authority, GptDerivativeJobAuthorityV3)
        if not (
            current.authority.parent_binding == successor_authority.parent_binding
            and current.authority.creation_binding
            == successor_authority.creation_binding
            and current.authority.model_transport == successor_authority.model_transport
        ):
            raise FolderJobV3RevisionError(
                "V3 mutation changed immutable derivative-child authority."
            )
    if current.reference_graph is not None and (
        successor.reference_graph != current.reference_graph
    ):
        raise FolderJobV3RevisionError("V3 mutation changed its reference graph.")


def _require_lifecycle_transition(
    current: FolderJobLifecycleV3,
    successor: FolderJobLifecycleV3,
) -> None:
    allowed = {
        FolderJobLifecycleV3.MATCHING: {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.PLANNING: {
            FolderJobLifecycleV3.PLANNING,
            FolderJobLifecycleV3.AWAITING_CLARIFICATION,
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.AWAITING_CLARIFICATION: {
            FolderJobLifecycleV3.AWAITING_CLARIFICATION,
            FolderJobLifecycleV3.PLANNING,
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.REVIEWING: {
            FolderJobLifecycleV3.REVISING,
            FolderJobLifecycleV3.EXECUTING,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.REVISING: {
            FolderJobLifecycleV3.REVISING,
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.REVISION_FAILED: {
            FolderJobLifecycleV3.REVISING,
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.EXECUTING: {
            FolderJobLifecycleV3.VERIFIED,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
    }
    if successor not in allowed.get(current, set()):
        raise FolderJobV3RevisionError(
            f"Invalid v3 transition: {current.value} -> {successor.value}."
        )


def _require_append_only_action_history(
    current: FolderRefactorJobV3,
    successor: FolderRefactorJobV3,
) -> None:
    """Permit only one exact action-history append at its declared transition."""

    provider_prefix = successor.revision_provider_failures[
        : len(current.revision_provider_failures)
    ]
    if provider_prefix != current.revision_provider_failures:
        raise FolderJobV3RevisionError(
            "Revision provider failure history is not append-only."
        )
    provider_added = len(successor.revision_provider_failures) - len(
        current.revision_provider_failures
    )
    if provider_added not in {0, 1}:
        raise FolderJobV3RevisionError(
            "A transition may append at most one provider failure."
        )
    if provider_added and not (
        current.lifecycle is FolderJobLifecycleV3.REVISING
        and successor.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    ):
        raise FolderJobV3RevisionError(
            "Provider failure history changed outside a failed revision."
        )

    rejection_prefix = successor.revision_rejections[: len(current.revision_rejections)]
    if rejection_prefix != current.revision_rejections:
        raise FolderJobV3RevisionError("Revision rejection history is not append-only.")
    rejection_added = len(successor.revision_rejections) - len(
        current.revision_rejections
    )
    if rejection_added not in {0, 1}:
        raise FolderJobV3RevisionError(
            "A transition may append at most one revision rejection."
        )
    if rejection_added and not (
        (
            current.lifecycle is FolderJobLifecycleV3.REVISING
            and successor.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
        )
        or (
            current.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
            and successor.lifecycle
            in {FolderJobLifecycleV3.REVISING, FolderJobLifecycleV3.REVIEWING}
        )
    ):
        raise FolderJobV3RevisionError(
            "Revision rejection history changed outside its exact transition."
        )

    keep_prefix = successor.keep_previous_actions[: len(current.keep_previous_actions)]
    if keep_prefix != current.keep_previous_actions:
        raise FolderJobV3RevisionError("Keep-previous history is not append-only.")
    keep_added = len(successor.keep_previous_actions) - len(
        current.keep_previous_actions
    )
    if keep_added not in {0, 1}:
        raise FolderJobV3RevisionError(
            "A transition may append at most one keep-previous action."
        )
    if keep_added:
        if not (
            current.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
            and successor.lifecycle is FolderJobLifecycleV3.REVIEWING
        ):
            raise FolderJobV3RevisionError(
                "Keep-previous history changed outside its exact transition."
            )
        action = successor.keep_previous_actions[-1]
        if (
            current.preview is None
            or action.base_job_revision != current.revision
            or action.candidate_fingerprint
            != current.preview.compiled_candidate_fingerprint
            or action.preview_fingerprint != current.preview.preview_fingerprint
        ):
            raise FolderJobV3RevisionError(
                "Keep-previous action targets another failed preview."
            )

    host_prefix = successor.host_mutation_bindings[
        : len(current.host_mutation_bindings)
    ]
    if host_prefix != current.host_mutation_bindings:
        raise FolderJobV3RevisionError(
            "Hosted mutation idempotency history is not append-only."
        )
    host_added = len(successor.host_mutation_bindings) - len(
        current.host_mutation_bindings
    )
    if host_added not in {0, 1}:
        raise FolderJobV3RevisionError(
            "A transition may append at most one hosted mutation binding."
        )
    if host_added:
        binding = successor.host_mutation_bindings[-1]
        expected_transition = {
            "request_clarification": (
                FolderJobLifecycleV3.PLANNING,
                FolderJobLifecycleV3.AWAITING_CLARIFICATION,
            ),
            "answer_clarification": (
                FolderJobLifecycleV3.AWAITING_CLARIFICATION,
                FolderJobLifecycleV3.PLANNING,
            ),
        }[binding.operation]
        if (
            current.lifecycle,
            successor.lifecycle,
        ) != expected_transition or binding.expected_job_revision != current.revision:
            raise FolderJobV3RevisionError(
                "Hosted mutation binding changed outside its exact transition."
            )

    revision_prefix = successor.revision_mutation_bindings[
        : len(current.revision_mutation_bindings)
    ]
    if revision_prefix != current.revision_mutation_bindings:
        raise FolderJobV3RevisionError(
            "Direct revision mutation history is not append-only."
        )
    revision_added = len(successor.revision_mutation_bindings) - len(
        current.revision_mutation_bindings
    )
    if revision_added not in {0, 1}:
        raise FolderJobV3RevisionError(
            "A transition may append at most one direct revision binding."
        )
    if revision_added:
        binding = successor.revision_mutation_bindings[-1]
        direct_authority = current.authority
        if isinstance(direct_authority, GptPlannedJobAuthorityV3):
            pending = direct_authority.pending_revision_turn
            ledger = direct_authority.evidence_ledger
        elif isinstance(direct_authority, GptDerivativeJobAuthorityV3) and (
            direct_authority.model_transport
            in {"responses_api", "recorded_replay", "deterministic_development"}
        ):
            pending = direct_authority.pending_direct_followup_revision
            ledger = direct_authority.evidence_ledger
        else:
            raise FolderJobV3RevisionError(
                "Direct revision binding requires direct planning authority."
            )
        instruction = current.revision_instruction
        if (
            pending is None
            or instruction is None
            or ledger is None
            or not (
                binding.job_id == current.job_id
                and binding.base_job_revision == pending.expected_job_revision
                and binding.base_proposal_revision == pending.proposal_revision
                and binding.base_candidate_fingerprint
                == pending.base_candidate_fingerprint
                and binding.base_preview_fingerprint == pending.base_preview_fingerprint
                and binding.revision_instruction_fingerprint
                == instruction.instruction_fingerprint
                and binding.idempotency_key_sha256 == instruction.idempotency_key_sha256
                and binding.model_transport == ledger.model_transport
            )
        ):
            raise FolderJobV3RevisionError(
                "Direct revision binding targets another reserved provider turn."
            )
        if not (
            current.lifecycle is FolderJobLifecycleV3.REVISING
            and successor.lifecycle
            in {
                FolderJobLifecycleV3.REVIEWING,
                FolderJobLifecycleV3.REVISION_FAILED,
            }
            and binding.terminal_job_revision == successor.revision
            and binding.resulting_proposal_revision == successor.proposal_revision
        ):
            raise FolderJobV3RevisionError(
                "Direct revision binding changed outside its terminal transition."
            )
        expected_outcome = (
            "proposal_replaced"
            if successor.lifecycle is FolderJobLifecycleV3.REVIEWING
            else (
                "provider_failed"
                if len(successor.revision_provider_failures)
                > len(current.revision_provider_failures)
                else "mechanically_rejected"
            )
        )
        if binding.terminal_outcome != expected_outcome:
            raise FolderJobV3RevisionError(
                "Direct revision binding records another terminal outcome."
            )
    if (
        current.lifecycle is FolderJobLifecycleV3.REVISING
        and successor.lifecycle
        in {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
        }
        and (
            isinstance(current.authority, GptPlannedJobAuthorityV3)
            or (
                isinstance(current.authority, GptDerivativeJobAuthorityV3)
                and current.authority.pending_direct_followup_revision is not None
            )
        )
        and revision_added != 1
    ):
        raise FolderJobV3RevisionError(
            "A direct revision terminal transition requires its retry binding."
        )

    host_revision_prefix = successor.host_revision_mutation_bindings[
        : len(current.host_revision_mutation_bindings)
    ]
    if host_revision_prefix != current.host_revision_mutation_bindings:
        raise FolderJobV3RevisionError(
            "Hosted revision mutation history is not append-only."
        )
    host_revision_added = len(successor.host_revision_mutation_bindings) - len(
        current.host_revision_mutation_bindings
    )
    if host_revision_added not in {0, 1}:
        raise FolderJobV3RevisionError(
            "A transition may append at most one hosted revision binding."
        )
    if host_revision_added:
        binding = successor.host_revision_mutation_bindings[-1]
        host_authority = current.authority
        if isinstance(host_authority, GptHostedJobAuthorityV3):
            pending = host_authority.pending_revision
        elif isinstance(
            host_authority, GptDerivativeJobAuthorityV3
        ) and host_authority.model_transport in {"chatgpt_hosted", "codex_hosted"}:
            pending = host_authority.pending_host_followup_revision
        else:
            raise FolderJobV3RevisionError(
                "Hosted revision binding requires hosted planning authority."
            )
        instruction = current.revision_instruction
        if (
            pending is None
            or instruction is None
            or not (
                binding.job_id == current.job_id
                and binding.base_job_revision == pending.expected_job_revision
                and binding.base_proposal_revision == pending.proposal_revision
                and binding.base_candidate_fingerprint
                == pending.base_candidate_fingerprint
                and binding.base_preview_fingerprint == pending.base_preview_fingerprint
                and binding.revision_instruction_fingerprint
                == instruction.instruction_fingerprint
                and binding.idempotency_key_sha256 == instruction.idempotency_key_sha256
                and binding.model_transport == host_authority.model_transport
            )
        ):
            raise FolderJobV3RevisionError(
                "Hosted revision binding targets another reserved host turn."
            )
        if not (
            current.lifecycle is FolderJobLifecycleV3.REVISING
            and successor.lifecycle
            in {
                FolderJobLifecycleV3.REVIEWING,
                FolderJobLifecycleV3.REVISION_FAILED,
            }
            and binding.terminal_job_revision == successor.revision
            and binding.resulting_proposal_revision == successor.proposal_revision
        ):
            raise FolderJobV3RevisionError(
                "Hosted revision binding changed outside its terminal transition."
            )
        expected_outcome = (
            "proposal_replaced"
            if successor.lifecycle is FolderJobLifecycleV3.REVIEWING
            else "mechanically_rejected"
        )
        if binding.terminal_outcome != expected_outcome:
            raise FolderJobV3RevisionError(
                "Hosted revision binding records another terminal outcome."
            )
    if (
        current.lifecycle is FolderJobLifecycleV3.REVISING
        and successor.lifecycle
        in {
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.REVISION_FAILED,
        }
        and (
            isinstance(current.authority, GptHostedJobAuthorityV3)
            or (
                isinstance(current.authority, GptDerivativeJobAuthorityV3)
                and current.authority.model_transport
                in {"chatgpt_hosted", "codex_hosted"}
                and current.authority.pending_host_followup_revision is not None
            )
        )
        and host_revision_added != 1
    ):
        raise FolderJobV3RevisionError(
            "A hosted revision terminal transition requires its retry binding."
        )

    reservation_changed = (
        successor.destination_reservation != current.destination_reservation
    )
    if reservation_changed and not (
        current.destination_reservation is None
        and current.lifecycle is FolderJobLifecycleV3.REVIEWING
        and successor.lifecycle is FolderJobLifecycleV3.EXECUTING
        and successor.destination_reservation is not None
        and successor.destination_reservation.authorized_job_revision
        == current.revision
    ):
        raise FolderJobV3RevisionError(
            "Destination reservation changed outside exact acceptance."
        )
    if (
        current.lifecycle is FolderJobLifecycleV3.REVIEWING
        and successor.lifecycle is FolderJobLifecycleV3.EXECUTING
        and not reservation_changed
    ):
        raise FolderJobV3RevisionError(
            "Execution must persist its destination reservation before copy."
        )


def _require_transition_payload(
    current: FolderRefactorJobV3,
    successor: FolderRefactorJobV3,
) -> None:
    """Keep the exact reviewed proposal immutable while authorizing execution."""

    if not (
        current.lifecycle is FolderJobLifecycleV3.REVIEWING
        and successor.lifecycle is FolderJobLifecycleV3.EXECUTING
    ):
        return
    permitted_changes = {
        "revision",
        "updated_at",
        "lifecycle",
        "execution_authorization",
        "destination_reservation",
        "pending_result_path",
        "final_result_path",
    }
    changed_review_fields = tuple(
        field_name
        for field_name in FolderRefactorJobV3.model_fields
        if field_name not in permitted_changes
        and getattr(current, field_name) != getattr(successor, field_name)
    )
    if changed_review_fields:
        raise FolderJobV3RevisionError(
            "Execution authorization changed the durable reviewed proposal: "
            + ", ".join(changed_review_fields)
            + "."
        )


def _authorization_key_sha256(value: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value.encode("utf-8")) > 256
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise FolderJobV3IdempotencyConflict(
            "Authorization idempotency key must be trimmed control-free text."
        )
    return canonical_sha256(
        {"domain": "foldweave:execution-authorization-key:v1", "key": value}
    )


def _revision_key_sha256(value: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value.encode("utf-8")) > 256
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise FolderJobV3IdempotencyConflict(
            "Revision idempotency key must be trimmed control-free text."
        )
    return canonical_sha256(
        {"domain": "foldweave:revision-idempotency-key:v1", "key": value}
    )


def _keep_previous_key_sha256(value: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value.encode("utf-8")) > 256
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise FolderJobV3IdempotencyConflict(
            "Keep-previous idempotency key must be trimmed control-free text."
        )
    return canonical_sha256(
        {"domain": "foldweave:keep-previous-idempotency-key:v1", "key": value}
    )


def _host_mutation_key_sha256(value: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or len(value.encode("utf-8")) > 256
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise FolderJobV3IdempotencyConflict(
            "Hosted mutation idempotency key must be trimmed control-free text."
        )
    return canonical_sha256(
        {"domain": "foldweave:host-mutation-idempotency-key:v1", "key": value}
    )


def _require_oslo_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Foldweave timestamps must be timezone-aware.")
    converted = value.astimezone(oslo_tz)
    if value != converted:
        raise ValueError("Foldweave timestamps must be expressed in Europe/Oslo.")
    return value
