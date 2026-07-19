"""Durable Foldweave v3 review and exact-authorization authority."""

from __future__ import annotations

import os
import uuid
from collections.abc import Callable
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import TracebackType
from typing import Annotated, Any, Literal, Self
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
from name_atlas.folder_refactor.inventory import FolderScanError, scan_folder
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.portable_artifacts import (
    FolderPortableArtifactError,
    strict_json_object,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)

FOLDER_REFACTOR_JOB_V3_SCHEMA_VERSION = "folder-refactor-job.v3"
FOLDER_EXECUTION_AUTHORIZATION_SCHEMA_VERSION = "folder-execution-authorization.v1"
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
    instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_instruction_fingerprint(self) -> Self:
        expected = canonical_sha256(
            {
                "domain": "foldweave:revision-instruction:v1",
                "base_candidate_fingerprint": self.base_candidate_fingerprint,
                "base_preview_fingerprint": self.base_preview_fingerprint,
                "instruction": self.instruction,
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


FolderJobAuthorityV3 = Annotated[
    GptPlannedJobAuthorityV2 | CapsuleAppliedJobAuthorityV2,
    Field(discriminator="kind"),
]


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
        if self.lifecycle is FolderJobLifecycleV3.REVISION_FAILED:
            if self.revision_failure is None:
                raise ValueError("revision_failed requires exact failure evidence.")
        elif self.revision_failure is not None:
            raise ValueError("Only revision_failed may retain revision failure.")
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
            FolderJobLifecycleV3.AWAITING_CLARIFICATION,
            FolderJobLifecycleV3.REVIEWING,
            FolderJobLifecycleV3.STALE,
            FolderJobLifecycleV3.BLOCKED,
        },
        FolderJobLifecycleV3.AWAITING_CLARIFICATION: {
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


def _require_oslo_timestamp(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Foldweave timestamps must be timezone-aware.")
    converted = value.astimezone(oslo_tz)
    if value != converted:
        raise ValueError("Foldweave timestamps must be expressed in Europe/Oslo.")
    return value
