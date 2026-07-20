"""Durable v2 authority for Connected Change and planner progress."""

from __future__ import annotations

import hashlib
import os
import stat
import uuid
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import TracebackType
from typing import Annotated, Any, Literal, Self
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    ValidationError,
    field_validator,
    model_validator,
)

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
    convert_planner_accepted_plan,
    validate_connected_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CHANGE_FILE_BYTES,
    CapsuleAppliedExecutionOrigin,
    ConnectedChangeFileAny,
    ConnectedChangeMatchReport,
    FolderExecutionOrigin,
    GptPlannedExecutionOrigin,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.job_io import (
    DurableJobFileLock,
    DurableJobLoadError,
    DurableJobLockError,
    DurableJobWriteError,
    StableRegularFileRead,
    atomic_write_regular_file,
    read_stable_regular_file,
)
from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderInventory,
)
from name_atlas.folder_refactor.inventory import (
    FolderScan,
    FolderScanError,
    LocalDirectoryIdentity,
    LocalFileIdentity,
    scan_folder,
)
from name_atlas.folder_refactor.planner_contracts import FolderPlannerProgress
from name_atlas.folder_refactor.portable_artifacts import (
    FolderPortableArtifactError,
    canonical_portable_json_bytes,
    strict_json_object,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderEvidenceLedger,
    FolderPlannerUsage,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

FOLDER_REFACTOR_JOB_V2_SCHEMA_VERSION = "folder-refactor-job.v2"
DEFAULT_V2_JOB_DIRECTORY = Path(".name-atlas/jobs")
MAX_DURABLE_JOB_BYTES = 32 * 1024 * 1024
oslo_tz = ZoneInfo("Europe/Oslo")


class FolderJobV2Error(RuntimeError):
    """Base error for Connected Change durable-job authority."""


class FolderJobV2LoadError(FolderJobV2Error):
    """A durable job is absent, corrupt, noncanonical, or unsupported."""


class FolderJobV2WriteError(FolderJobV2Error):
    """A durable v2 job could not be safely persisted."""


class FolderJobV2LockError(FolderJobV2WriteError):
    """Another process currently owns this durable v2 job's writer lock."""


class FolderJobV2RevisionError(FolderJobV2WriteError):
    """The expected durable revision or checkpoint does not match."""


class FolderJobV2FinalizedError(FolderJobV2WriteError):
    """A terminal v2 job cannot be changed in place."""


class FolderJobV2IdempotencyConflict(FolderJobV2WriteError):
    """An idempotency key was reused for a different canonical request."""


class LegacyV1NonterminalJobError(FolderJobV2LoadError):
    """A nonterminal v1 job cannot be silently interpreted as v2."""


class StrictFrozenJobV2Model(BaseModel):
    """Immutable strict base for local Connected Change job records."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class FolderJobLifecycleV2(StrEnum):
    """Complete lifecycle for one persistent Connected Change job."""

    PLANNING = "planning"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    EXECUTING = "executing"
    VERIFIED = "verified"
    STALE = "stale"
    BLOCKED = "blocked"

    @property
    def terminal(self) -> bool:
        """Return whether the job is immutable and requires a fresh job."""

        return self in {self.VERIFIED, self.STALE, self.BLOCKED}


class FolderMutationRequestV2(StrictFrozenJobV2Model):
    """Canonical local mutation request bound to one idempotency key."""

    operation: Literal["gpt_planned", "capsule_applied"]
    source_root: Path
    output_parent: Path
    user_request: str = Field(min_length=1, max_length=20_000)
    change_file_path: Path | None = None

    @field_validator("source_root", "output_parent", "change_file_path")
    @classmethod
    def require_absolute_paths(cls, value: Path | None) -> Path | None:
        if value is not None and not value.is_absolute():
            raise ValueError("Mutation-request paths must be absolute.")
        return value

    @model_validator(mode="after")
    def require_operation_shape(self) -> Self:
        if self.operation == "capsule_applied":
            if self.change_file_path is None:
                raise ValueError("Capsule application requires a Change File path.")
        elif self.change_file_path is not None:
            raise ValueError("GPT planning cannot carry a Change File path.")
        return self

    @property
    def fingerprint(self) -> str:
        """Return one domain-separated canonical mutation fingerprint."""

        return canonical_sha256(
            {
                "domain": "name-atlas:folder-mutation-request:v2",
                "request": self.model_dump(mode="json"),
            }
        )


class FolderIdempotencyBindingV2(StrictFrozenJobV2Model):
    """Persist only a bounded key hash and its exact request binding."""

    key_sha256: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)


class FolderOperationIdempotencyBindingV2(StrictFrozenJobV2Model):
    """One append-only tool mutation binding inside the existing job authority."""

    operation: Literal["answer_clarification", "recreate_original"]
    key_sha256: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)


class JobLocalFileIdentityV2(StrictFrozenJobV2Model):
    """Nonportable identity used only to detect local file replacement."""

    relative_path: str = Field(min_length=1, max_length=4_096)
    device: int = Field(ge=0)
    inode: int = Field(ge=0)
    size: int = Field(ge=0)
    modified_ns: int = Field(ge=0)

    @classmethod
    def from_scan(cls, value: LocalFileIdentity) -> Self:
        """Persist one scanner-owned regular-file identity."""

        return cls(
            relative_path=value.relative_path,
            device=value.device,
            inode=value.inode,
            size=value.size,
            modified_ns=value.modified_ns,
        )


class JobLocalDirectoryIdentityV2(StrictFrozenJobV2Model):
    """Nonportable identity used only to detect directory replacement."""

    relative_path: str = Field(min_length=1, max_length=4_096)
    device: int = Field(ge=0)
    inode: int = Field(ge=0)
    modified_ns: int = Field(ge=0)

    @classmethod
    def from_scan(cls, value: LocalDirectoryIdentity) -> Self:
        """Persist one scanner-owned directory identity."""

        return cls(
            relative_path=value.relative_path,
            device=value.device,
            inode=value.inode,
            modified_ns=value.modified_ns,
        )


class JobSourceDifferenceV2(StrictFrozenJobV2Model):
    """One exact member-level source difference from the immutable snapshot."""

    kind: Literal["added", "removed", "content_changed", "replaced"]
    member_kind: Literal["regular_file", "directory"]
    relative_path: str = Field(min_length=1, max_length=4_096)
    before_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)
    after_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_difference_shape(self) -> Self:
        if self.kind == "added":
            if self.before_fingerprint is not None or self.after_fingerprint is None:
                raise ValueError("An added member requires only an after fingerprint.")
        elif self.kind == "removed":
            if self.before_fingerprint is None or self.after_fingerprint is not None:
                raise ValueError("A removed member requires only a before fingerprint.")
        elif self.before_fingerprint is None or self.after_fingerprint is None:
            raise ValueError("A changed member requires before and after fingerprints.")
        elif self.before_fingerprint == self.after_fingerprint:
            raise ValueError("A changed member requires distinct fingerprints.")
        return self


class JobInputStalenessV2(StrictFrozenJobV2Model):
    """Terminal evidence that a source or imported Change File changed."""

    source_differences: tuple[JobSourceDifferenceV2, ...] = ()
    source_scan_error: str | None = Field(default=None, min_length=1, max_length=2_000)
    change_file_code: (
        Literal["change_file_changed", "change_file_unreadable"] | None
    ) = None
    change_file_detail: str | None = Field(default=None, min_length=1, max_length=2_000)

    @model_validator(mode="after")
    def require_stale_evidence(self) -> Self:
        change_material = self.change_file_code is not None
        if change_material != (self.change_file_detail is not None):
            raise ValueError("Change File staleness requires a code and detail.")
        if (
            not self.source_differences
            and self.source_scan_error is None
            and not change_material
        ):
            raise ValueError("Staleness requires exact source or Change File evidence.")
        if self.source_differences != tuple(
            sorted(
                self.source_differences,
                key=lambda item: (item.relative_path, item.member_kind, item.kind),
            )
        ):
            raise ValueError("Source differences must use deterministic ordering.")
        return self


class ChangeFileInputBindingV2(StrictFrozenJobV2Model):
    """Local identity and strict portable contents of an imported Change File."""

    path: Path
    device: int = Field(ge=0)
    inode: int = Field(ge=0)
    size: int = Field(ge=0, le=MAX_CHANGE_FILE_BYTES)
    modified_ns: int = Field(ge=0)
    raw_sha256: str = Field(pattern=SHA256_PATTERN)
    change_file: ConnectedChangeFileAny

    @field_validator("path")
    @classmethod
    def require_absolute_path(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("Change File path must be absolute.")
        return value

    @model_validator(mode="after")
    def require_exact_portable_binding(self) -> Self:
        payload = canonical_portable_json_bytes(self.change_file)
        if (
            len(payload) != self.size
            or canonical_sha256_bytes(payload) != self.raw_sha256
        ):
            raise ValueError("Change File local identity differs from canonical bytes.")
        return self


class GptPlannerCheckpointV2(StrictFrozenJobV2Model):
    """Durable complete planner progress plus its browser-facing projection."""

    status: Literal["planning", "awaiting_clarification", "accepted", "blocked"]
    observable_transcript: tuple[JsonValue, ...] = ()
    response_turn_count: int = Field(default=0, ge=0, le=8)
    evidence_call_count: int = Field(default=0, ge=0, le=24)
    clarification_question: str | None = Field(
        default=None, min_length=1, max_length=1_000
    )
    clarification_answer: str | None = Field(
        default=None, min_length=1, max_length=4_000
    )
    accepted_plan_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)
    blocker_code: str | None = Field(default=None, pattern=r"^[a-z0-9_:-]{1,128}$")
    blocker_message: str | None = Field(default=None, min_length=1, max_length=2_000)
    progress: FolderPlannerProgress | None = None
    usage: tuple[FolderPlannerUsage, ...] = ()

    @model_validator(mode="after")
    def require_status_shape(self) -> Self:
        question = self.clarification_question
        answer = self.clarification_answer
        blocker = self.blocker_code is not None or self.blocker_message is not None
        if self.status == "awaiting_clarification":
            if question is None or answer is not None:
                raise ValueError(
                    "Awaiting clarification requires one unanswered question."
                )
        elif (question is None) != (answer is None):
            raise ValueError(
                "Retained clarification requires both question and answer."
            )
        if self.status == "accepted":
            if self.accepted_plan_fingerprint is None or blocker:
                raise ValueError("Accepted planning requires one plan and no blocker.")
        elif self.accepted_plan_fingerprint is not None:
            raise ValueError("Only accepted planning can retain a plan fingerprint.")
        if self.status == "blocked":
            if self.blocker_code is None or self.blocker_message is None:
                raise ValueError("Blocked planning requires a code and message.")
        elif blocker:
            raise ValueError("Only blocked planning can retain blocker fields.")
        if self.progress is not None:
            progress = self.progress
            transcript = tuple(turn.model_dump(mode="json") for turn in progress.turns)
            if (
                self.status != progress.status
                or self.observable_transcript != transcript
                or self.response_turn_count != progress.response_turns
                or self.evidence_call_count != progress.evidence_calls
                or self.clarification_question != progress.clarification_question
                or self.clarification_answer != progress.clarification_answer
                or self.blocker_code != progress.blocker_code
            ):
                raise ValueError(
                    "Planner checkpoint projection differs from full progress."
                )
            if progress.status == "accepted":
                if progress.accepted_plan is None:
                    raise ValueError("Accepted progress lacks its planner plan.")
            elif self.accepted_plan_fingerprint is not None:
                raise ValueError(
                    "Nonaccepted progress cannot project an accepted plan."
                )
            usage_turns = tuple(item.response_turn for item in self.usage)
            if usage_turns != tuple(sorted(set(usage_turns))):
                raise ValueError("Planner usage must use unique ascending turns.")
            if any(turn > len(progress.turns) for turn in usage_turns):
                raise ValueError("Planner usage names an unobserved response turn.")
            if progress.provider_kind != "live" and self.usage:
                raise ValueError("Only live planning may retain provider usage.")
        elif self.usage:
            raise ValueError("Planner usage requires complete planner progress.")
        return self

    @classmethod
    def from_progress(
        cls,
        progress: FolderPlannerProgress,
        *,
        accepted_plan_fingerprint: str | None = None,
        usage: tuple[FolderPlannerUsage, ...] = (),
    ) -> Self:
        """Build one exact projection without reconstructing planner state."""

        if (progress.status == "accepted") != (accepted_plan_fingerprint is not None):
            raise ValueError(
                "Accepted planner progress and v2 plan fingerprint must coincide."
            )
        return cls(
            status=progress.status,
            observable_transcript=tuple(
                turn.model_dump(mode="json") for turn in progress.turns
            ),
            response_turn_count=progress.response_turns,
            evidence_call_count=progress.evidence_calls,
            clarification_question=progress.clarification_question,
            clarification_answer=progress.clarification_answer,
            accepted_plan_fingerprint=accepted_plan_fingerprint,
            blocker_code=progress.blocker_code,
            blocker_message=(
                f"Planner blocked: {progress.blocker_code}."
                if progress.status == "blocked"
                else None
            ),
            progress=progress,
            usage=usage,
        )


class GptPlannedJobAuthorityV2(StrictFrozenJobV2Model):
    """Authority for a plan created by GPT, replay, or deterministic development."""

    kind: Literal["gpt_planned"] = "gpt_planned"
    planner_checkpoint: GptPlannerCheckpointV2
    evidence_ledger: FolderEvidenceLedger | None = None
    execution_origin: GptPlannedExecutionOrigin | None = None

    @model_validator(mode="after")
    def require_origin_binding(self) -> Self:
        if self.planner_checkpoint.status == "accepted":
            if self.evidence_ledger is None:
                raise ValueError(
                    "Accepted GPT planning requires its exact evidence ledger."
                )
        elif self.evidence_ledger is not None:
            raise ValueError(
                "Only accepted GPT planning may retain a final evidence ledger."
            )
        if self.evidence_ledger is not None:
            ledger_transcript = tuple(
                turn.model_dump(mode="json")
                for turn in self.evidence_ledger.observable_turns
            )
            if (
                self.evidence_ledger.accepted_plan_fingerprint
                != self.planner_checkpoint.accepted_plan_fingerprint
                or self.evidence_ledger.response_turn_count
                != self.planner_checkpoint.response_turn_count
                or self.evidence_ledger.evidence_call_count
                != self.planner_checkpoint.evidence_call_count
                or ledger_transcript != self.planner_checkpoint.observable_transcript
            ):
                raise ValueError(
                    "GPT checkpoint differs from its exact final evidence ledger."
                )
            if self.evidence_ledger.usage != self.planner_checkpoint.usage:
                raise ValueError("GPT checkpoint usage differs from its evidence.")
        if self.execution_origin is not None:
            if self.planner_checkpoint.status != "accepted":
                raise ValueError("A GPT execution origin requires accepted planning.")
            if (
                self.execution_origin.accepted_plan_fingerprint
                != self.planner_checkpoint.accepted_plan_fingerprint
                or self.execution_origin.observable_transcript
                != self.planner_checkpoint.observable_transcript
            ):
                raise ValueError("GPT origin and planner checkpoint name another plan.")
            ledger = self.evidence_ledger
            if ledger is None or (
                self.execution_origin.evidence_fingerprint
                != ledger.evidence_fingerprint
                or self.execution_origin.clarification_question
                != ledger.clarification_question
                or self.execution_origin.clarification_answer
                != ledger.clarification_answer
            ):
                raise ValueError(
                    "GPT execution origin differs from its evidence ledger."
                )
        return self


class CapsuleAppliedJobAuthorityV2(StrictFrozenJobV2Model):
    """Durable authority for deterministic, provider-free Change File application."""

    kind: Literal["capsule_applied"] = "capsule_applied"
    change_file_binding: ChangeFileInputBindingV2
    match_report: ConnectedChangeMatchReport | None = None
    execution_origin: CapsuleAppliedExecutionOrigin | None = None

    @model_validator(mode="after")
    def require_origin_binding(self) -> Self:
        if (
            self.match_report is not None
            and self.match_report.core_fingerprint
            != self.change_file_binding.change_file.core_fingerprint
        ):
            raise ValueError("Match report targets another Change File Core.")
        if self.execution_origin is not None:
            if self.match_report is None or self.match_report.status != "matched":
                raise ValueError("Capsule execution origin requires a matched report.")
            if (
                self.execution_origin.change_file_fingerprint
                != self.change_file_binding.change_file.change_file_fingerprint
                or self.execution_origin.match_report_fingerprint
                != self.match_report.match_report_fingerprint
            ):
                raise ValueError("Capsule origin differs from its imported authority.")
        return self


FolderJobAuthorityV2 = Annotated[
    GptPlannedJobAuthorityV2 | CapsuleAppliedJobAuthorityV2,
    Field(discriminator="kind"),
]


class FolderJobVerifiedArtifactsV2(StrictFrozenJobV2Model):
    """Minimal immutable proof identities for one independently verified result."""

    receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    organized_tree_commitment: str = Field(pattern=SHA256_PATTERN)
    change_ledger_fingerprint: str = Field(pattern=SHA256_PATTERN)
    verification_fingerprint: str = Field(pattern=SHA256_PATTERN)
    verification_status: Literal["verified"] = "verified"


class FolderRefactorJobV2(StrictFrozenJobV2Model):
    """Sole durable mutable authority for a Connected Change origin or receiver job."""

    schema_version: Literal["folder-refactor-job.v2"] = (
        FOLDER_REFACTOR_JOB_V2_SCHEMA_VERSION
    )
    revision: int = Field(ge=0)
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
        default=(),
        max_length=2,
    )
    authority: FolderJobAuthorityV2
    accepted_plan: FolderAcceptedPlanV2 | None = None
    pending_result_path: Path | None = None
    final_result_path: Path | None = None
    verified_artifacts: FolderJobVerifiedArtifactsV2 | None = None
    lifecycle: FolderJobLifecycleV2 = FolderJobLifecycleV2.PLANNING
    blocker_code: str | None = Field(default=None, pattern=r"^[a-z0-9_:-]{1,128}$")
    blocker_message: str | None = Field(default=None, min_length=1, max_length=2_000)
    staleness: JobInputStalenessV2 | None = None

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        _require_uuid4_hex(value)
        return value

    @field_validator("created_at", "updated_at")
    @classmethod
    def require_oslo_timestamp(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value)

    @field_validator(
        "source_root",
        "output_parent",
        "job_path",
        "pending_result_path",
        "final_result_path",
    )
    @classmethod
    def require_absolute_local_paths(cls, value: Path | None) -> Path | None:
        if value is not None and not value.is_absolute():
            raise ValueError("Local FolderRefactorJobV2 paths must be absolute.")
        return value

    @model_validator(mode="after")
    def require_complete_authority(self) -> Self:
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot precede created_at.")
        operations = tuple(item.operation for item in self.operation_idempotency)
        if len(set(operations)) != len(operations):
            raise ValueError("Tool mutation idempotency operations must be unique.")
        _require_separate_paths(
            source_root=self.source_root,
            output_parent=self.output_parent,
            job_path=self.job_path,
        )
        _require_local_identity_bindings(self)
        _require_request_and_authority_bindings(self)
        _require_plan_and_origin_bindings(self)
        _require_exact_result_pointers(self)
        _require_lifecycle_shape(self)
        return self


class LegacyFolderJobV1Evidence(StrictFrozenJobV2Model):
    """Read-only identity for one terminal historical v1 job."""

    schema_version: Literal["folder-refactor-job.v1"] = "folder-refactor-job.v1"
    job_path: Path
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    revision: int = Field(ge=0)
    lifecycle: Literal["verified", "stale", "blocked"]
    raw_sha256: str = Field(pattern=SHA256_PATTERN)


FolderJobRecord = FolderRefactorJobV2 | LegacyFolderJobV1Evidence


def build_idempotency_binding(
    idempotency_key: str,
    request: FolderMutationRequestV2,
) -> FolderIdempotencyBindingV2:
    """Validate one caller key and bind it without persisting the plaintext key."""

    key_sha256 = _idempotency_key_sha256(idempotency_key)
    return FolderIdempotencyBindingV2(
        key_sha256=key_sha256,
        request_fingerprint=request.fingerprint,
    )


def build_operation_idempotency_binding(
    *,
    operation: Literal["answer_clarification", "recreate_original"],
    idempotency_key: str,
    request: JsonValue,
) -> FolderOperationIdempotencyBindingV2:
    """Bind one tool mutation without creating another ledger or authority."""

    return FolderOperationIdempotencyBindingV2(
        operation=operation,
        key_sha256=_idempotency_key_sha256(idempotency_key),
        request_fingerprint=operation_request_fingerprint(
            operation=operation,
            request=request,
        ),
    )


def bind_operation_idempotency(
    job: FolderRefactorJobV2,
    *,
    operation: Literal["answer_clarification", "recreate_original"],
    idempotency_key: str,
    request: JsonValue,
) -> tuple[FolderOperationIdempotencyBindingV2, ...]:
    """Return an exact retry or one append-only operation binding."""

    candidate = build_operation_idempotency_binding(
        operation=operation,
        idempotency_key=idempotency_key,
        request=request,
    )
    existing = tuple(
        item for item in job.operation_idempotency if item.operation == operation
    )
    if existing:
        if existing != (candidate,):
            raise FolderJobV2IdempotencyConflict(
                f"{operation} idempotency key is bound to another exact request."
            )
        return job.operation_idempotency
    return job.operation_idempotency + (candidate,)


def require_operation_idempotency(
    job: FolderRefactorJobV2,
    *,
    operation: Literal["answer_clarification", "recreate_original"],
    idempotency_key: str,
    request: JsonValue,
) -> None:
    """Require one prebound exact operation without mutating a terminal job."""

    candidate = build_operation_idempotency_binding(
        operation=operation,
        idempotency_key=idempotency_key,
        request=request,
    )
    matching = tuple(
        item for item in job.operation_idempotency if item.operation == operation
    )
    if matching != (candidate,):
        raise FolderJobV2IdempotencyConflict(
            f"{operation} idempotency key is not bound to this exact request."
        )


def operation_request_fingerprint(
    *,
    operation: Literal["answer_clarification", "recreate_original"],
    request: JsonValue,
) -> str:
    """Return one domain-separated canonical tool-mutation fingerprint."""

    return canonical_sha256(
        {
            "domain": "name-atlas:folder-operation-request:v2",
            "operation": operation,
            "request": request,
        }
    )


def _idempotency_key_sha256(idempotency_key: str) -> str:
    """Validate and hash one caller key without persisting its plaintext."""

    if not isinstance(idempotency_key, str):
        raise FolderJobV2WriteError("Idempotency key must be text.")
    if (
        not idempotency_key
        or idempotency_key != idempotency_key.strip()
        or len(idempotency_key.encode("utf-8")) > 256
        or any(
            ord(character) < 32 or ord(character) == 127
            for character in idempotency_key
        )
    ):
        raise FolderJobV2WriteError(
            "Idempotency key must be nonempty, trimmed, control-free UTF-8 "
            "up to 256 bytes."
        )
    return canonical_sha256(
        {
            "domain": "name-atlas:folder-idempotency-key:v2",
            "key": idempotency_key,
        }
    )


def build_change_file_input_binding(path: Path) -> ChangeFileInputBindingV2:
    """Read, strictly parse, and bind one canonical Change File exactly once."""

    try:
        observed = read_stable_regular_file(path, max_bytes=MAX_CHANGE_FILE_BYTES)
        change_file = parse_connected_change_file_any(observed.payload)
    except (DurableJobLoadError, ValueError) as exc:
        raise FolderJobV2LoadError("Change File is unreadable or invalid.") from exc
    if canonical_portable_json_bytes(change_file) != observed.payload:
        raise FolderJobV2LoadError("Change File must use exact canonical JSON bytes.")
    return _change_file_binding_from_read(observed, change_file)


def build_new_capsule_job_v2(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
    change_file_path: Path,
    idempotency_key: str,
    display_name: str | None = None,
    scan: FolderScan | None = None,
    job_id: str | None = None,
    clock: Callable[[], datetime] | None = None,
) -> FolderRefactorJobV2:
    """Construct an unsaved receiver job without planner/provider imports."""

    binding = build_change_file_input_binding(change_file_path)
    source_scan, resolved_output, resolved_job = _prepare_new_job_paths(
        source_root=source_root,
        output_parent=output_parent,
        job_path=job_path,
        scan=scan,
    )
    mutation = FolderMutationRequestV2(
        operation="capsule_applied",
        source_root=source_scan.source_root,
        output_parent=resolved_output,
        user_request=binding.change_file.core.request,
        change_file_path=binding.path,
    )
    return _build_new_job_v2(
        source_scan=source_scan,
        output_parent=resolved_output,
        job_path=resolved_job,
        user_request=binding.change_file.core.request,
        idempotency=build_idempotency_binding(idempotency_key, mutation),
        authority=CapsuleAppliedJobAuthorityV2(change_file_binding=binding),
        display_name=display_name,
        job_id=job_id,
        clock=clock,
    )


def build_new_gpt_job_v2(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
    user_request: str,
    idempotency_key: str,
    display_name: str | None = None,
    scan: FolderScan | None = None,
    job_id: str | None = None,
    clock: Callable[[], datetime] | None = None,
    planner_progress: FolderPlannerProgress | None = None,
) -> FolderRefactorJobV2:
    """Construct an unsaved GPT-planned job without importing planner code."""

    source_scan, resolved_output, resolved_job = _prepare_new_job_paths(
        source_root=source_root,
        output_parent=output_parent,
        job_path=job_path,
        scan=scan,
    )
    if planner_progress is not None:
        if job_id is None or planner_progress.job_id != job_id:
            raise FolderJobV2WriteError(
                "Complete planner progress requires the exact explicit job ID."
            )
        if (
            planner_progress.status != "planning"
            or planner_progress.evidence_ledger.source_commitment
            != source_scan.inventory.source_commitment
            or planner_progress.evidence_ledger.request_fingerprint
            != request_fingerprint(user_request)
        ):
            raise FolderJobV2WriteError(
                "Initial planner progress targets another source, request, or state."
            )
    mutation = FolderMutationRequestV2(
        operation="gpt_planned",
        source_root=source_scan.source_root,
        output_parent=resolved_output,
        user_request=user_request,
    )
    return _build_new_job_v2(
        source_scan=source_scan,
        output_parent=resolved_output,
        job_path=resolved_job,
        user_request=user_request,
        idempotency=build_idempotency_binding(idempotency_key, mutation),
        authority=GptPlannedJobAuthorityV2(
            planner_checkpoint=(
                GptPlannerCheckpointV2.from_progress(planner_progress)
                if planner_progress is not None
                else GptPlannerCheckpointV2(status="planning")
            )
        ),
        display_name=display_name,
        job_id=job_id,
        clock=clock,
    )


def evolve_job_v2(job: FolderRefactorJobV2, **updates: Any) -> FolderRefactorJobV2:
    """Build one strict same-revision mutation candidate for a store writer."""

    return FolderRefactorJobV2.model_validate(
        {**job.model_dump(mode="python"), **updates},
        strict=True,
    )


def canonical_job_v2_bytes(job: FolderRefactorJobV2) -> bytes:
    """Serialize every declared field deterministically with one final newline."""

    return canonical_json_bytes(job) + b"\n"


def parse_job_v2_bytes(data: bytes, *, expected_path: Path) -> FolderRefactorJobV2:
    """Strictly parse one canonical v2 record and validate its local pointer."""

    try:
        raw = strict_json_object(data)
        job = FolderRefactorJobV2.model_validate_json(data, strict=True)
    except (FolderPortableArtifactError, ValidationError) as exc:
        raise FolderJobV2LoadError(
            "FolderRefactorJobV2 is corrupt or unsupported."
        ) from exc
    if canonical_json_bytes(raw) + b"\n" != data:
        raise FolderJobV2LoadError("FolderRefactorJobV2 is not canonical JSON.")
    if job.job_path != expected_path.resolve(strict=False):
        raise FolderJobV2LoadError(
            "FolderRefactorJobV2 path differs from its persisted local pointer."
        )
    return job


def load_folder_job_record(path: Path) -> FolderJobRecord:
    """Strictly dispatch v2 jobs and terminal read-only v1 historical evidence."""

    try:
        observed = read_stable_regular_file(path, max_bytes=MAX_DURABLE_JOB_BYTES)
        raw = strict_json_object(observed.payload)
    except (DurableJobLoadError, FolderPortableArtifactError) as exc:
        raise FolderJobV2LoadError(
            "Durable job is unreadable or not strict JSON."
        ) from exc
    schema_version = raw.get("schema_version")
    if schema_version == FOLDER_REFACTOR_JOB_V2_SCHEMA_VERSION:
        return parse_job_v2_bytes(observed.payload, expected_path=observed.path)
    if schema_version == "folder-refactor-job.v1":
        return _load_legacy_v1_evidence(observed)
    raise FolderJobV2LoadError(
        f"Unsupported durable job schema version: {schema_version!r}."
    )


def find_idempotent_job_v2(
    jobs_directory: Path,
    binding: FolderIdempotencyBindingV2,
) -> FolderRefactorJobV2 | None:
    """Find one existing exact request without creating a second ledger or job."""

    if not jobs_directory.exists():
        return None
    metadata = jobs_directory.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise FolderJobV2LoadError("Jobs directory must be a real directory.")
    match: FolderRefactorJobV2 | None = None
    for path in sorted(jobs_directory.glob("*.json"), key=lambda item: item.name):
        record = load_folder_job_record(path)
        if isinstance(record, LegacyFolderJobV1Evidence):
            continue
        if record.idempotency.key_sha256 != binding.key_sha256:
            continue
        if record.idempotency.request_fingerprint != binding.request_fingerprint:
            raise FolderJobV2IdempotencyConflict(
                "Idempotency key is already bound to another canonical request."
            )
        if match is not None:
            raise FolderJobV2IdempotencyConflict(
                "Duplicate durable jobs share one idempotency binding."
            )
        match = record
    return match


def expected_pending_result_path_v2(job: FolderRefactorJobV2) -> Path:
    """Return the one pending path exclusively owned by this job."""

    return job.output_parent / f".name-atlas-{job.job_id}.pending"


def expected_final_result_path_v2(job: FolderRefactorJobV2) -> Path:
    """Return the accepted absent final result path for this job."""

    if job.accepted_plan is None:
        raise FolderJobV2WriteError("A final result path requires an accepted plan.")
    return job.output_parent / job.accepted_plan.result_folder_name


class FolderRefactorJobV2Store:
    """Path-bound strict load, input rehydration, and mutation entry point."""

    def __init__(
        self,
        path: Path,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock or (lambda: datetime.now(tz=oslo_tz))

    def inspect(self) -> FolderJobRecord:
        """Read one v2 or terminal historical v1 record without mutation."""

        return load_folder_job_record(self.path)

    def load(self) -> FolderRefactorJobV2:
        """Load one v2 record and terminally persist detected input staleness."""

        return self.rehydrate()

    def rehydrate(self) -> FolderRefactorJobV2:
        """Revalidate source and Change File under one process-held writer lock."""

        with self.writer() as writer:
            return writer.rehydrate()

    def writer(self) -> FolderRefactorJobV2Writer:
        """Return one non-blocking exclusive mutation context."""

        return FolderRefactorJobV2Writer(self.path, clock=self._clock)


class FolderRefactorJobV2Writer:
    """Expected-checkpoint mutation authority for one canonical v2 job file."""

    def __init__(self, path: Path, *, clock: Callable[[], datetime]) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock
        self._lock = DurableJobFileLock(self.path)

    def __enter__(self) -> Self:
        try:
            self._lock.__enter__()
        except DurableJobLockError as exc:
            raise FolderJobV2LockError(str(exc)) from exc
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self._lock.__exit__(exc_type, exc_value, traceback)

    def load(self) -> FolderRefactorJobV2:
        """Strictly load one v2 job while retaining mutation authority."""

        self._require_lock()
        record = load_folder_job_record(self.path)
        if isinstance(record, LegacyFolderJobV1Evidence):
            raise FolderJobV2LoadError(
                "A terminal v1 job is read-only historical evidence; create a "
                "fresh v2 job."
            )
        return record

    def rehydrate(self) -> FolderRefactorJobV2:
        """Return current state or persist one terminal stale transition."""

        current = self.load()
        if current.lifecycle.terminal:
            return current
        evidence = _detect_input_staleness(current)
        if evidence is None:
            return current
        stale = evolve_job_v2(
            current,
            revision=current.revision + 1,
            updated_at=self._now(),
            lifecycle=FolderJobLifecycleV2.STALE,
            staleness=evidence,
            blocker_code=None,
            blocker_message=None,
        )
        _write_job_v2(self.path, stale)
        return stale

    def save_new(self, job: FolderRefactorJobV2) -> FolderRefactorJobV2:
        """Persist one exact revision-zero job only while all inputs remain stable."""

        self._require_lock()
        if os.path.lexists(self.path):
            raise FolderJobV2RevisionError("Durable job already exists.")
        if job.job_path != self.path or job.revision != 0:
            raise FolderJobV2RevisionError(
                "A new v2 job requires its exact path and revision zero."
            )
        if _detect_input_staleness(job) is not None:
            raise FolderJobV2WriteError("Job input changed before initial persistence.")
        _write_job_v2(self.path, job)
        return job

    def save(
        self,
        candidate: FolderRefactorJobV2,
        *,
        expected_current: FolderRefactorJobV2,
    ) -> FolderRefactorJobV2:
        """Persist one validated successor against the exact current checkpoint."""

        self._require_lock()
        current = self.load()
        _require_exact_checkpoint(current, expected_current)
        if current.lifecycle.terminal:
            raise FolderJobV2FinalizedError(
                "Terminal FolderRefactorJobV2 is immutable; create a fresh job."
            )
        if candidate.revision != current.revision:
            raise FolderJobV2RevisionError(
                "Mutation candidate must retain the expected current revision."
            )
        if candidate.lifecycle is FolderJobLifecycleV2.STALE:
            raise FolderJobV2RevisionError(
                "Only input rehydration may mark a v2 job stale."
            )
        evidence = _detect_input_staleness(current)
        if evidence is not None:
            stale = evolve_job_v2(
                current,
                revision=current.revision + 1,
                updated_at=self._now(),
                lifecycle=FolderJobLifecycleV2.STALE,
                staleness=evidence,
            )
            _write_job_v2(self.path, stale)
            raise FolderJobV2FinalizedError(
                "FolderRefactorJobV2 became stale before mutation."
            )
        _require_immutable_job_identity(current, candidate)
        _require_lifecycle_transition(current.lifecycle, candidate.lifecycle)
        updated = evolve_job_v2(
            candidate,
            revision=current.revision + 1,
            updated_at=self._now(),
        )
        _write_job_v2(self.path, updated)
        return updated

    def begin_execution(
        self,
        current: FolderRefactorJobV2,
    ) -> FolderRefactorJobV2:
        """Persist exact owned result paths before any result write begins."""

        if current.lifecycle is not FolderJobLifecycleV2.EXECUTING:
            raise FolderJobV2RevisionError("Execution paths require an executing job.")
        if (
            current.pending_result_path is not None
            or current.final_result_path is not None
        ):
            raise FolderJobV2RevisionError("Execution paths were already persisted.")
        pending = expected_pending_result_path_v2(current)
        final = expected_final_result_path_v2(current)
        _require_absent(pending, label="Pending result")
        _require_absent(final, label="Final result")
        candidate = evolve_job_v2(
            current,
            pending_result_path=pending,
            final_result_path=final,
        )
        return self.save(candidate, expected_current=current)

    def mark_blocked(
        self,
        current: FolderRefactorJobV2,
        *,
        code: str,
        message: str,
    ) -> FolderRefactorJobV2:
        """Persist one exact terminal blocker without deleting owned evidence."""

        candidate = evolve_job_v2(
            current,
            lifecycle=FolderJobLifecycleV2.BLOCKED,
            blocker_code=code,
            blocker_message=message,
        )
        return self.save(candidate, expected_current=current)

    def finalize_verified(
        self,
        current: FolderRefactorJobV2,
        *,
        artifacts: FolderJobVerifiedArtifactsV2,
    ) -> FolderRefactorJobV2:
        """Persist terminal proof identities only after no-replace promotion."""

        if (
            current.lifecycle is not FolderJobLifecycleV2.EXECUTING
            or current.pending_result_path is None
            or current.final_result_path is None
        ):
            raise FolderJobV2RevisionError(
                "Verified finalization requires persisted execution paths."
            )
        if os.path.lexists(current.pending_result_path):
            raise FolderJobV2WriteError("Pending result still exists after promotion.")
        _require_real_directory(current.final_result_path, label="Final result")
        persisted = self.load()
        _require_exact_checkpoint(persisted, current)
        if persisted.lifecycle.terminal:
            raise FolderJobV2FinalizedError(
                "Terminal FolderRefactorJobV2 is immutable; create a fresh job."
            )
        candidate = evolve_job_v2(
            persisted,
            pending_result_path=None,
            verified_artifacts=artifacts,
            lifecycle=FolderJobLifecycleV2.VERIFIED,
        )
        _require_immutable_job_identity(persisted, candidate)
        _require_lifecycle_transition(persisted.lifecycle, candidate.lifecycle)
        updated = evolve_job_v2(
            candidate,
            revision=persisted.revision + 1,
            updated_at=self._now(),
        )
        _write_job_v2(self.path, updated)
        return updated

    def _now(self) -> datetime:
        return _require_oslo_timestamp(self._clock())

    def _require_lock(self) -> None:
        if not self._lock.held:
            raise FolderJobV2WriteError("V2 job writes require an active writer lock.")


def _build_new_job_v2(
    *,
    source_scan: FolderScan,
    output_parent: Path,
    job_path: Path,
    user_request: str,
    idempotency: FolderIdempotencyBindingV2,
    authority: GptPlannedJobAuthorityV2 | CapsuleAppliedJobAuthorityV2,
    display_name: str | None,
    job_id: str | None,
    clock: Callable[[], datetime] | None,
) -> FolderRefactorJobV2:
    identifier = job_id or uuid.uuid4().hex
    _require_uuid4_hex(identifier)
    now = _require_oslo_timestamp((clock or (lambda: datetime.now(tz=oslo_tz)))())
    reconstruction_binding = FolderOperationIdempotencyBindingV2(
        operation="recreate_original",
        key_sha256=idempotency.key_sha256,
        request_fingerprint=operation_request_fingerprint(
            operation="recreate_original",
            request={"job_handle": identifier},
        ),
    )
    return FolderRefactorJobV2(
        revision=0,
        job_id=identifier,
        display_name=display_name or source_scan.source_root.name or "Folder refactor",
        created_at=now,
        updated_at=now,
        source_root=source_scan.source_root,
        output_parent=output_parent,
        job_path=job_path,
        source_inventory=source_scan.inventory,
        local_file_identities=tuple(
            JobLocalFileIdentityV2.from_scan(item)
            for item in source_scan.local_file_identities
        ),
        local_directory_identities=tuple(
            JobLocalDirectoryIdentityV2.from_scan(item)
            for item in source_scan.local_directory_identities
        ),
        user_request=user_request,
        idempotency=idempotency,
        operation_idempotency=(reconstruction_binding,),
        authority=authority,
    )


def _prepare_new_job_paths(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
    scan: FolderScan | None,
) -> tuple[FolderScan, Path, Path]:
    source_scan = scan or scan_folder(source_root)
    resolved_source = source_root.resolve(strict=True)
    if source_scan.source_root != resolved_source:
        raise FolderJobV2WriteError("Source scan belongs to another source root.")
    resolved_output = output_parent.resolve(strict=True)
    _require_real_directory(resolved_output, label="Output parent")
    resolved_job = job_path.resolve(strict=False)
    _require_separate_paths(
        source_root=resolved_source,
        output_parent=resolved_output,
        job_path=resolved_job,
    )
    return source_scan, resolved_output, resolved_job


def _change_file_binding_from_read(
    observed: StableRegularFileRead,
    change_file: ConnectedChangeFileAny,
) -> ChangeFileInputBindingV2:
    return ChangeFileInputBindingV2(
        path=observed.path,
        device=observed.device,
        inode=observed.inode,
        size=observed.size,
        modified_ns=observed.modified_ns,
        raw_sha256=observed.sha256,
        change_file=change_file,
    )


def _load_legacy_v1_evidence(
    observed: StableRegularFileRead,
) -> LegacyFolderJobV1Evidence:
    """Lazy-load v1 only for strict historical dispatch, never receiver execution."""

    try:
        from name_atlas.folder_refactor.job import (
            FolderRefactorJob,
            canonical_job_bytes,
        )

        legacy = FolderRefactorJob.model_validate_json(observed.payload, strict=True)
    except (ImportError, ValidationError) as exc:
        raise FolderJobV2LoadError(
            "Historical v1 job is corrupt or unsupported."
        ) from exc
    if canonical_job_bytes(legacy) != observed.payload:
        raise FolderJobV2LoadError("Historical v1 job is not canonical JSON.")
    if legacy.job_path != observed.path:
        raise FolderJobV2LoadError("Historical v1 job path pointer differs.")
    lifecycle = str(legacy.lifecycle.value)
    if lifecycle not in {"verified", "stale", "blocked"}:
        raise LegacyV1NonterminalJobError(
            "Nonterminal folder-refactor-job.v1 state is read-only and cannot be "
            "resumed as v2; create a fresh FolderRefactorJobV2 from the "
            "unchanged source."
        )
    return LegacyFolderJobV1Evidence(
        job_path=observed.path,
        job_id=legacy.job_id,
        revision=legacy.revision,
        lifecycle=lifecycle,
        raw_sha256=observed.sha256,
    )


def _write_job_v2(path: Path, job: FolderRefactorJobV2) -> None:
    try:
        atomic_write_regular_file(path, canonical_job_v2_bytes(job))
    except DurableJobWriteError as exc:
        raise FolderJobV2WriteError(str(exc)) from exc


def _detect_input_staleness(job: FolderRefactorJobV2) -> JobInputStalenessV2 | None:
    try:
        current_scan = scan_folder(job.source_root)
    except FolderScanError as exc:
        return JobInputStalenessV2(source_scan_error=str(exc))
    differences = compare_job_source_v2(job, current_scan)
    change_code: Literal["change_file_changed", "change_file_unreadable"] | None = None
    change_detail: str | None = None
    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
        try:
            current_binding = build_change_file_input_binding(
                job.authority.change_file_binding.path
            )
        except FolderJobV2LoadError as exc:
            change_code = "change_file_unreadable"
            change_detail = str(exc)
        else:
            if current_binding != job.authority.change_file_binding:
                change_code = "change_file_changed"
                change_detail = (
                    "Imported Change File bytes or local file identity changed after "
                    "the durable job was created."
                )
    if not differences and change_code is None:
        return None
    return JobInputStalenessV2(
        source_differences=differences,
        change_file_code=change_code,
        change_file_detail=change_detail,
    )


def compare_job_source_v2(
    job: FolderRefactorJobV2,
    current_scan: FolderScan,
) -> tuple[JobSourceDifferenceV2, ...]:
    """Return deterministic exact member differences for one v2 source snapshot."""

    if current_scan.source_root != job.source_root:
        raise ValueError("Current scan belongs to another source root.")
    before_files = {item.relative_path: item for item in job.source_inventory.files}
    after_files = {item.relative_path: item for item in current_scan.inventory.files}
    before_local_files = {
        item.relative_path: item for item in job.local_file_identities
    }
    after_local_files = {
        item.relative_path: JobLocalFileIdentityV2.from_scan(item)
        for item in current_scan.local_file_identities
    }
    differences: list[JobSourceDifferenceV2] = []
    for relative_path in sorted(before_files.keys() | after_files.keys()):
        before_file = before_files.get(relative_path)
        after_file = after_files.get(relative_path)
        if before_file is None:
            differences.append(
                JobSourceDifferenceV2(
                    kind="added",
                    member_kind="regular_file",
                    relative_path=relative_path,
                    after_fingerprint=_file_state_fingerprint(
                        after_file,
                        after_local_files[relative_path],
                    ),
                )
            )
            continue
        if after_file is None:
            differences.append(
                JobSourceDifferenceV2(
                    kind="removed",
                    member_kind="regular_file",
                    relative_path=relative_path,
                    before_fingerprint=_file_state_fingerprint(
                        before_file,
                        before_local_files[relative_path],
                    ),
                )
            )
            continue
        before_local = before_local_files[relative_path]
        after_local = after_local_files[relative_path]
        before_fingerprint = _file_state_fingerprint(before_file, before_local)
        after_fingerprint = _file_state_fingerprint(after_file, after_local)
        if (before_local.device, before_local.inode) != (
            after_local.device,
            after_local.inode,
        ):
            kind: Literal["content_changed", "replaced"] = "replaced"
        elif (before_file.size, before_file.sha256) != (
            after_file.size,
            after_file.sha256,
        ):
            kind = "content_changed"
        else:
            continue
        differences.append(
            JobSourceDifferenceV2(
                kind=kind,
                member_kind="regular_file",
                relative_path=relative_path,
                before_fingerprint=before_fingerprint,
                after_fingerprint=after_fingerprint,
            )
        )

    before_directories = {
        item.relative_path: item for item in job.local_directory_identities
    }
    after_directories = {
        item.relative_path: JobLocalDirectoryIdentityV2.from_scan(item)
        for item in current_scan.local_directory_identities
    }
    for relative_path in sorted(before_directories.keys() | after_directories.keys()):
        before = before_directories.get(relative_path)
        after = after_directories.get(relative_path)
        if before is None:
            differences.append(
                JobSourceDifferenceV2(
                    kind="added",
                    member_kind="directory",
                    relative_path=relative_path,
                    after_fingerprint=_directory_state_fingerprint(after),
                )
            )
        elif after is None:
            differences.append(
                JobSourceDifferenceV2(
                    kind="removed",
                    member_kind="directory",
                    relative_path=relative_path,
                    before_fingerprint=_directory_state_fingerprint(before),
                )
            )
        elif (before.device, before.inode) != (after.device, after.inode):
            differences.append(
                JobSourceDifferenceV2(
                    kind="replaced",
                    member_kind="directory",
                    relative_path=relative_path,
                    before_fingerprint=_directory_state_fingerprint(before),
                    after_fingerprint=_directory_state_fingerprint(after),
                )
            )
    return tuple(
        sorted(
            differences,
            key=lambda item: (item.relative_path, item.member_kind, item.kind),
        )
    )


def _require_local_identity_bindings(job: FolderRefactorJobV2) -> None:
    file_paths = tuple(item.relative_path for item in job.local_file_identities)
    expected_files = tuple(item.relative_path for item in job.source_inventory.files)
    if file_paths != expected_files:
        raise ValueError("Local file identities must exactly match the inventory.")
    inventory_sizes = {
        item.relative_path: item.size for item in job.source_inventory.files
    }
    if any(
        item.size != inventory_sizes[item.relative_path]
        for item in job.local_file_identities
    ):
        raise ValueError("Local file identity sizes differ from the inventory.")
    directory_paths = tuple(
        item.relative_path for item in job.local_directory_identities
    )
    if (
        directory_paths != tuple(sorted(set(directory_paths)))
        or not directory_paths
        or directory_paths[0] != "."
        or len(directory_paths) != job.source_inventory.directory_count + 1
    ):
        raise ValueError(
            "Local directory identities must exactly account for the source."
        )
    empty = {item.relative_path for item in job.source_inventory.empty_directories}
    if not empty.issubset(set(directory_paths)):
        raise ValueError("Empty directories require local identity records.")


def _require_request_and_authority_bindings(job: FolderRefactorJobV2) -> None:
    if isinstance(job.authority, CapsuleAppliedJobAuthorityV2):
        if (
            job.user_request
            != job.authority.change_file_binding.change_file.core.request
        ):
            raise ValueError("Receiver request differs from the imported Change File.")
        mutation = FolderMutationRequestV2(
            operation="capsule_applied",
            source_root=job.source_root,
            output_parent=job.output_parent,
            user_request=job.user_request,
            change_file_path=job.authority.change_file_binding.path,
        )
    else:
        mutation = FolderMutationRequestV2(
            operation="gpt_planned",
            source_root=job.source_root,
            output_parent=job.output_parent,
            user_request=job.user_request,
        )
    if job.idempotency.request_fingerprint != mutation.fingerprint:
        raise ValueError("Idempotency binding names another canonical request.")


def _require_plan_and_origin_bindings(job: FolderRefactorJobV2) -> None:
    plan = job.accepted_plan
    if plan is not None:
        validate_connected_accepted_plan(
            inventory=job.source_inventory,
            request=job.user_request,
            plan=plan,
        )
    if isinstance(job.authority, GptPlannedJobAuthorityV2):
        checkpoint = job.authority.planner_checkpoint
        progress = checkpoint.progress
        ledger = job.authority.evidence_ledger
        origin: FolderExecutionOrigin | None = job.authority.execution_origin
        if progress is not None:
            if (
                progress.job_id != job.job_id
                or progress.evidence_ledger.source_commitment
                != job.source_inventory.source_commitment
                or progress.evidence_ledger.request_fingerprint
                != request_fingerprint(job.user_request)
            ):
                raise ValueError("Planner progress is bound to another durable job.")
            if ledger is not None and progress.provider_kind != ledger.provider_kind:
                raise ValueError("Planner progress and evidence provider differ.")
        if ledger is not None and (
            ledger.job_id != job.job_id
            or ledger.source_commitment != job.source_inventory.source_commitment
            or ledger.request_fingerprint != request_fingerprint(job.user_request)
        ):
            raise ValueError("GPT evidence ledger is bound to another durable job.")
        if plan is not None:
            if plan.execution_authority != "gpt_plan":
                raise ValueError("GPT job requires GPT-plan mapping authority.")
            if checkpoint.accepted_plan_fingerprint != canonical_sha256(plan):
                raise ValueError("Planner checkpoint differs from the accepted plan.")
            if ledger is None or (
                ledger.accepted_plan_fingerprint != canonical_sha256(plan)
                or ledger.evidence_fingerprint != plan.evidence_fingerprint
            ):
                raise ValueError("GPT evidence ledger differs from the accepted plan.")
            if progress is not None and (
                progress.accepted_plan is None
                or (
                    convert_planner_accepted_plan(
                        inventory=job.source_inventory,
                        request=job.user_request,
                        plan=progress.accepted_plan,
                    )
                    != plan
                )
            ):
                raise ValueError(
                    "Full planner progress differs from the connected plan."
                )
        elif checkpoint.accepted_plan_fingerprint is not None:
            raise ValueError("Planner checkpoint retains an absent accepted plan.")
        if origin is not None and (
            plan is None or origin.evidence_fingerprint != plan.evidence_fingerprint
        ):
            raise ValueError("GPT execution origin differs from the accepted plan.")
        if origin is not None and ledger is not None:
            expected_planner_kind = {
                "deterministic": "deterministic_development",
                "live": "live",
                "recorded_replay": "recorded_replay",
            }[ledger.provider_kind]
            if origin.planner_kind != expected_planner_kind:
                raise ValueError("GPT origin provider kind differs from its ledger.")
            if ledger.provider_kind == "live":
                if (
                    origin.provider_call_count != ledger.response_turn_count
                    or origin.store_false != ledger.store_false
                    or origin.returned_model_id not in ledger.returned_model_ids
                ):
                    raise ValueError(
                        "Live GPT origin metadata differs from its ledger."
                    )
            elif origin.provider_call_count != 0:
                raise ValueError("Non-live GPT origin cannot claim provider calls.")
    else:
        authority = job.authority
        report = authority.match_report
        origin = authority.execution_origin
        if (
            report is not None
            and report.receiver_source_commitment
            != job.source_inventory.source_commitment
        ):
            raise ValueError("Match report targets another receiver source.")
        if plan is not None:
            if plan.execution_authority != "change_file":
                raise ValueError("Receiver job requires Change File mapping authority.")
            if report is None or report.status != "matched":
                raise ValueError("Receiver accepted plan requires a matched report.")
        if origin is not None:
            if plan is None:
                raise ValueError("Capsule execution origin requires an accepted plan.")
            if origin.receiver_accepted_plan_fingerprint != canonical_sha256(plan):
                raise ValueError("Capsule origin differs from the receiver plan.")


def _require_exact_result_pointers(job: FolderRefactorJobV2) -> None:
    pending = job.pending_result_path
    final = job.final_result_path
    if job.accepted_plan is not None:
        _require_disjoint_result_authority(
            job,
            pending=expected_pending_result_path_v2(job),
            final=expected_final_result_path_v2(job),
        )
    if pending is not None and pending != expected_pending_result_path_v2(job):
        raise ValueError("Pending result pointer is not exactly owned by this job.")
    if final is not None and final != expected_final_result_path_v2(job):
        raise ValueError("Final result pointer differs from the accepted result name.")
    if (pending is None) != (
        final is None
    ) and job.lifecycle is not FolderJobLifecycleV2.VERIFIED:
        raise ValueError("Nonterminal execution pointers must appear together.")
    for path in (pending, final):
        if path is not None and path.parent != job.output_parent:
            raise ValueError("Result pointer must be an immediate output child.")


def _require_lifecycle_shape(job: FolderRefactorJobV2) -> None:
    blocker_material = job.blocker_code is not None or job.blocker_message is not None
    if job.lifecycle is FolderJobLifecycleV2.BLOCKED:
        if job.blocker_code is None or job.blocker_message is None:
            raise ValueError("Blocked job requires a code and message.")
    elif blocker_material:
        raise ValueError("Only a blocked job may retain blocker fields.")
    if isinstance(job.authority, GptPlannedJobAuthorityV2):
        checkpoint = job.authority.planner_checkpoint
        if checkpoint.status == "blocked" and (
            job.blocker_code != checkpoint.blocker_code
            or job.blocker_message != checkpoint.blocker_message
        ):
            raise ValueError("Blocked job differs from its planner blocker.")
    if job.lifecycle is FolderJobLifecycleV2.STALE:
        if job.staleness is None:
            raise ValueError("Stale job requires exact input evidence.")
    elif job.staleness is not None:
        raise ValueError("Only a stale job may retain staleness evidence.")

    origin = job.authority.execution_origin
    if job.lifecycle is FolderJobLifecycleV2.PLANNING:
        if (
            job.accepted_plan is not None
            or origin is not None
            or job.verified_artifacts is not None
        ):
            raise ValueError("Planning job cannot retain execution or proof authority.")
        if isinstance(job.authority, GptPlannedJobAuthorityV2) and (
            job.authority.planner_checkpoint.status != "planning"
        ):
            raise ValueError("Planning lifecycle requires matching planner progress.")
    elif job.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION:
        if (
            not isinstance(job.authority, GptPlannedJobAuthorityV2)
            or job.authority.planner_checkpoint.status != "awaiting_clarification"
            or job.accepted_plan is not None
            or origin is not None
        ):
            raise ValueError("Clarification lifecycle requires one GPT question only.")
    elif job.lifecycle in {
        FolderJobLifecycleV2.EXECUTING,
        FolderJobLifecycleV2.VERIFIED,
    }:
        if job.accepted_plan is None or origin is None:
            raise ValueError(
                "Executing and verified jobs require plan and origin authority."
            )
    if job.lifecycle is FolderJobLifecycleV2.VERIFIED:
        if (
            job.verified_artifacts is None
            or job.pending_result_path is not None
            or job.final_result_path is None
        ):
            raise ValueError(
                "Verified job requires final result and immutable proof identities."
            )
    elif job.verified_artifacts is not None:
        raise ValueError("Only a verified job may retain terminal proof identities.")


def _require_exact_checkpoint(
    current: FolderRefactorJobV2,
    expected: FolderRefactorJobV2,
) -> None:
    if current.revision != expected.revision or current != expected:
        raise FolderJobV2RevisionError(
            "Durable FolderRefactorJobV2 differs from the expected checkpoint."
        )


def _require_immutable_job_identity(
    current: FolderRefactorJobV2,
    candidate: FolderRefactorJobV2,
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
    )
    if any(getattr(current, field) != getattr(candidate, field) for field in fields):
        raise FolderJobV2RevisionError("Immutable v2 job identity changed.")
    if current.authority.kind != candidate.authority.kind:
        raise FolderJobV2RevisionError("Execution authority kind cannot change.")
    if isinstance(current.authority, CapsuleAppliedJobAuthorityV2) and (
        not isinstance(candidate.authority, CapsuleAppliedJobAuthorityV2)
        or (
            current.authority.change_file_binding
            != candidate.authority.change_file_binding
        )
    ):
        raise FolderJobV2RevisionError("Imported Change File authority changed.")
    if isinstance(current.authority, GptPlannedJobAuthorityV2):
        if not isinstance(candidate.authority, GptPlannedJobAuthorityV2):
            raise FolderJobV2RevisionError("GPT planning authority changed.")
        _require_gpt_planner_successor(
            current.authority.planner_checkpoint,
            candidate.authority.planner_checkpoint,
        )
    if (
        len(candidate.operation_idempotency) < len(current.operation_idempotency)
        or candidate.operation_idempotency[: len(current.operation_idempotency)]
        != current.operation_idempotency
    ):
        raise FolderJobV2RevisionError(
            "Tool mutation idempotency bindings are not append-only."
        )


def _require_gpt_planner_successor(
    current: GptPlannerCheckpointV2,
    candidate: GptPlannerCheckpointV2,
) -> None:
    """Reject any rewrite or rewind of observable durable planner history."""

    if current == candidate:
        return
    before = current.progress
    after = candidate.progress
    if before is None:
        pristine = GptPlannerCheckpointV2(status="planning")
        if current != pristine:
            raise FolderJobV2RevisionError(
                "Compatibility planner authority cannot be rewritten."
            )
        if after is None and (
            candidate.status != "accepted"
            or candidate.response_turn_count == 0
            or not candidate.observable_transcript
            or candidate.accepted_plan_fingerprint is None
        ):
            raise FolderJobV2RevisionError(
                "Compatibility planning may only persist one accepted result."
            )
        return
    if after is None:
        raise FolderJobV2RevisionError("Planner progress history cannot be removed.")

    immutable_fields = ("schema_version", "job_id", "provider_kind", "model_alias")
    if any(
        getattr(before, field) != getattr(after, field) for field in immutable_fields
    ):
        raise FolderJobV2RevisionError("Planner progress identity changed.")
    before_evidence = before.evidence_ledger
    after_evidence = after.evidence_ledger
    immutable_evidence_fields = (
        "schema_version",
        "source_commitment",
        "request_fingerprint",
        "initial_evidence",
        "initial_evidence_bytes",
    )
    if any(
        getattr(before_evidence, field) != getattr(after_evidence, field)
        for field in immutable_evidence_fields
    ):
        raise FolderJobV2RevisionError("Planner evidence identity changed.")

    _require_history_prefix(before.turns, after.turns, label="response turns")
    _require_history_prefix(
        before_evidence.records,
        after_evidence.records,
        label="evidence records",
    )
    _require_history_prefix(
        before.compiler_failures,
        after.compiler_failures,
        label="compiler failures",
    )
    _require_history_prefix(current.usage, candidate.usage, label="provider usage")

    monotonic_fields = (
        "response_turns",
        "evidence_calls",
        "evidence_calls_observed",
        "outbound_evidence_bytes",
        "plan_submissions",
    )
    if any(
        getattr(after, field) < getattr(before, field) for field in monotonic_fields
    ):
        raise FolderJobV2RevisionError("Planner counters cannot decrease.")
    evidence_monotonic_fields = (
        "aggregate_result_bytes",
        "total_outbound_evidence_bytes",
    )
    if any(
        getattr(after_evidence, field) < getattr(before_evidence, field)
        for field in evidence_monotonic_fields
    ):
        raise FolderJobV2RevisionError("Planner evidence counters cannot decrease.")

    if before.pending_response_turn is not None:
        if after.pending_response_turn == before.pending_response_turn:
            pending_fields = (
                "pending_response_input_bytes",
                "pending_response_input_fingerprint",
                "pending_response_input_payload",
            )
            if any(
                getattr(before, field) != getattr(after, field)
                for field in pending_fields
            ):
                raise FolderJobV2RevisionError(
                    "A reserved provider turn cannot change its committed input."
                )
        else:
            completed_index = before.pending_response_turn - 1
            if len(after.turns) <= completed_index:
                raise FolderJobV2RevisionError(
                    "A reserved provider turn cannot be discarded."
                )
            completed = after.turns[completed_index]
            if (
                completed.input_bytes != before.pending_response_input_bytes
                or completed.input_fingerprint
                != before.pending_response_input_fingerprint
                or completed.input_payload != before.pending_response_input_payload
            ):
                raise FolderJobV2RevisionError(
                    "A completed provider turn differs from its reservation."
                )

    if before.clarification_question is not None:
        if after.clarification_question != before.clarification_question:
            raise FolderJobV2RevisionError(
                "The durable clarification question cannot change or disappear."
            )
        if before.clarification_answer is not None:
            if after.clarification_answer != before.clarification_answer:
                raise FolderJobV2RevisionError(
                    "The durable clarification answer cannot change or disappear."
                )
        elif before.status == "awaiting_clarification":
            if after.status == "planning":
                if after.clarification_answer is None:
                    raise FolderJobV2RevisionError(
                        "Clarification continuation must persist exactly one answer."
                    )
            elif after.status == "awaiting_clarification":
                raise FolderJobV2RevisionError(
                    "An awaiting clarification checkpoint cannot be rewritten."
                )
            else:
                raise FolderJobV2RevisionError(
                    "Clarification must persist its answer before planner continuation."
                )
    elif after.clarification_question is not None and (
        after.status != "awaiting_clarification"
        or after.clarification_answer is not None
    ):
        raise FolderJobV2RevisionError(
            "A new clarification must first persist one unanswered question."
        )

    if before.accepted_plan is not None and after.accepted_plan != before.accepted_plan:
        raise FolderJobV2RevisionError("An accepted planner plan cannot change.")
    if before.status == "accepted":
        raise FolderJobV2RevisionError("Accepted planner authority is immutable.")


def _require_history_prefix(
    current: tuple[Any, ...],
    candidate: tuple[Any, ...],
    *,
    label: str,
) -> None:
    if len(candidate) < len(current) or candidate[: len(current)] != current:
        raise FolderJobV2RevisionError(f"Planner {label} are not append-only.")


def _require_lifecycle_transition(
    before: FolderJobLifecycleV2,
    after: FolderJobLifecycleV2,
) -> None:
    allowed = {
        FolderJobLifecycleV2.PLANNING: {
            FolderJobLifecycleV2.PLANNING,
            FolderJobLifecycleV2.AWAITING_CLARIFICATION,
            FolderJobLifecycleV2.EXECUTING,
            FolderJobLifecycleV2.BLOCKED,
        },
        FolderJobLifecycleV2.AWAITING_CLARIFICATION: {
            FolderJobLifecycleV2.PLANNING,
            FolderJobLifecycleV2.EXECUTING,
            FolderJobLifecycleV2.BLOCKED,
        },
        FolderJobLifecycleV2.EXECUTING: {
            FolderJobLifecycleV2.EXECUTING,
            FolderJobLifecycleV2.VERIFIED,
            FolderJobLifecycleV2.BLOCKED,
        },
    }
    if after not in allowed.get(before, set()):
        raise FolderJobV2RevisionError(
            f"Invalid v2 lifecycle transition: {before.value} -> {after.value}."
        )


def _file_state_fingerprint(file: Any, local: Any) -> str:
    return canonical_sha256(
        {
            "domain": "name-atlas:local-file-state:v2",
            "device": local.device,
            "file_id": file.file_id,
            "inode": local.inode,
            "relative_path": file.relative_path,
            "sha256": file.sha256,
            "size": file.size,
        }
    )


def _directory_state_fingerprint(directory: Any) -> str:
    return canonical_sha256(
        {
            "domain": "name-atlas:local-directory-state:v2",
            "device": directory.device,
            "inode": directory.inode,
            "relative_path": directory.relative_path,
        }
    )


def _require_separate_paths(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
) -> None:
    if _path_is_within(output_parent, source_root):
        raise ValueError("Output parent cannot equal or be inside the source tree.")
    if _paths_overlap(job_path.parent, source_root):
        raise ValueError("Local job state and source tree cannot overlap.")


def _require_disjoint_result_authority(
    job: FolderRefactorJobV2,
    *,
    pending: Path,
    final: Path,
) -> None:
    if pending.parent != job.output_parent or final.parent != job.output_parent:
        raise ValueError("Result paths must be immediate output-parent children.")
    if _paths_overlap(pending, final):
        raise ValueError("Pending and final result trees overlap.")
    for result_path in (pending, final):
        if _paths_overlap(result_path, job.source_root) or _paths_overlap(
            result_path,
            job.job_path.parent,
        ):
            raise ValueError("Exact result tree overlaps source or mutable job state.")


def _path_is_within(path: Path, root: Path) -> bool:
    resolved_path = path.resolve(strict=False)
    resolved_root = root.resolve(strict=False)
    return resolved_path == resolved_root or resolved_root in resolved_path.parents


def _paths_overlap(left: Path, right: Path) -> bool:
    left_resolved = left.resolve(strict=False)
    right_resolved = right.resolve(strict=False)
    return (
        left_resolved == right_resolved
        or left_resolved in right_resolved.parents
        or right_resolved in left_resolved.parents
    )


def _require_absent(path: Path, *, label: str) -> None:
    if os.path.lexists(path):
        raise FolderJobV2WriteError(f"{label} must be absent before execution.")


def _require_real_directory(path: Path, *, label: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise FolderJobV2WriteError(f"{label} is unavailable.") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise FolderJobV2WriteError(f"{label} must be a real directory.")


def _require_oslo_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Durable job timestamps must be timezone-aware.")
    if value.utcoffset() != value.astimezone(oslo_tz).utcoffset():
        raise ValueError("Durable job timestamps must use the Europe/Oslo offset.")
    return value


def _require_uuid4_hex(value: str) -> None:
    try:
        parsed = uuid.UUID(hex=value)
    except ValueError as exc:
        raise ValueError("job_id must be lowercase UUID4 hexadecimal text.") from exc
    if parsed.version != 4 or parsed.hex != value:
        raise ValueError("job_id must be lowercase UUID4 hexadecimal text.")


def canonical_sha256_bytes(payload: bytes) -> str:
    """Hash exact raw bytes without introducing another serialization domain."""

    return hashlib.sha256(payload).hexdigest()
