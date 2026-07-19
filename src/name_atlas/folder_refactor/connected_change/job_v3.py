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
    FolderRefactorJobV2,
    GptPlannedJobAuthorityV2,
    GptPlannerCheckpointV2,
    JobLocalDirectoryIdentityV2,
    JobLocalFileIdentityV2,
    LegacyFolderJobV1Evidence,
    build_change_file_input_binding,
    load_folder_job_record,
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
from name_atlas.folder_refactor.foldweave_planning_contracts import (
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
FOLDER_EXECUTION_AUTHORIZATION_SCHEMA_VERSION = "folder-execution-authorization.v1"
FOLDER_KEEP_PREVIOUS_ACTION_SCHEMA_VERSION = "folder-keep-previous-action.v1"
DEFAULT_V3_JOB_DIRECTORY = Path(".foldweave/jobs")
oslo_tz = ZoneInfo("Europe/Oslo")


class FolderJobV3Error(RuntimeError):
    """Base failure for the Foldweave v3 authority."""


class FolderJobV3LoadError(FolderJobV3Error):
    """A v3 job is absent, corrupt, noncanonical, or unsupported."""


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
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"authorization_fingerprint"})
        )
        if self.authorization_fingerprint != expected:
            raise ValueError("Execution authorization fingerprint is invalid.")
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


# Existing F0a-era v3 files used the predecessor v2 authority. Keep them readable
# without weakening new-work authority. The two GPT models share a `kind` literal,
# so schema-shape validation, not an ambiguous discriminator, performs dispatch.
FolderJobAuthorityV3 = (
    GptPlannedJobAuthorityV3 | GptPlannedJobAuthorityV2 | CapsuleAppliedJobAuthorityV2
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
    immediate_parent_job_id: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{32}$",
    )
    immediate_parent_candidate_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    execution_authorization: FolderExecutionAuthorizationV1 | None = None
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
                    self.immediate_parent_candidate_fingerprint
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
            if isinstance(self.authority, GptPlannedJobAuthorityV3) and (
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
    """Strictly dispatch v3 while retaining historical v1/v2 readability."""

    try:
        observed = read_stable_regular_file(path, max_bytes=MAX_DURABLE_JOB_BYTES)
        raw = strict_json_object(observed.payload)
    except (DurableJobLoadError, FolderPortableArtifactError) as exc:
        raise FolderJobV3LoadError("Durable job is unreadable or invalid.") from exc
    if raw.get("schema_version") == FOLDER_REFACTOR_JOB_V3_SCHEMA_VERSION:
        return parse_job_v3_bytes(observed.payload, expected_path=observed.path)
    try:
        return load_folder_job_record(observed.path)
    except Exception as exc:
        raise FolderJobV3LoadError("Unsupported durable job schema.") from exc


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
        _require_append_only_action_history(current, successor)
        _require_transition_payload(current, successor)
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
        "output_parent": output_parent.resolve(strict=False),
        "result_folder_name": result_folder_name,
        "idempotency_key_sha256": _authorization_key_sha256(idempotency_key),
        "channel": channel,
        "authorization_timestamp": _require_oslo_timestamp(timestamp),
    }
    fingerprint_payload = {
        **payload,
        "output_parent": payload["output_parent"].as_posix(),
        "authorization_timestamp": payload["authorization_timestamp"].isoformat(),
    }
    return FolderExecutionAuthorizationV1(
        **payload,
        authorization_fingerprint=canonical_sha256(fingerprint_payload),
    )


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
    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
        try:
            current_binding = build_change_file_input_binding(
                job.authority.change_file_binding.path
            )
        except Exception as exc:
            return FolderJobStalenessV3(
                code="change_file_unreadable",
                detail=f"Imported Change File cannot be reverified: {exc}",
            )
        if current_binding != job.authority.change_file_binding:
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


def _require_oslo_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Foldweave timestamps must be timezone-aware.")
    converted = value.astimezone(oslo_tz)
    if value != converted:
        raise ValueError("Foldweave timestamps must be expressed in Europe/Oslo.")
    return value
