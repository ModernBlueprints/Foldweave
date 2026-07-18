"""Strict, restart-safe authority for one AI-first folder-refactor job."""

from __future__ import annotations

import errno
import fcntl
import json
import os
import stat
import tempfile
import uuid
from collections import defaultdict
from collections.abc import Callable
from contextlib import suppress
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import TracebackType
from typing import Literal, Self
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

from name_atlas.folder_refactor.compiler import (
    PlanCompilationError,
    compile_plan,
    validate_accepted_plan,
)
from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderAcceptedPlan,
    FolderFile,
    FolderInventory,
)
from name_atlas.folder_refactor.inventory import (
    FolderScan,
    FolderScanError,
    LocalDirectoryIdentity,
    LocalFileIdentity,
    scan_folder,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerProgress,
    InspectMarkdownLinksCall,
    ListInventoryPageCall,
    ReadTextExcerptCall,
    RequestClarificationCall,
    SubmitPlanCall,
)
from name_atlas.folder_refactor.planner_evidence import (
    EvidenceExecution,
    LocalFolderEvidenceService,
    PlannerEvidenceError,
    append_evidence_execution,
    create_initial_evidence_ledger,
)
from name_atlas.folder_refactor.serialization import request_fingerprint

FOLDER_REFACTOR_JOB_SCHEMA_VERSION = "folder-refactor-job.v1"
DEFAULT_JOB_DIRECTORY = Path(".name-atlas/jobs")
oslo_tz = ZoneInfo("Europe/Oslo")


class FolderJobError(RuntimeError):
    """Base error for fail-closed folder-refactor job persistence."""


class FolderJobLoadError(FolderJobError):
    """A durable job is absent, unreadable, corrupt, or unsupported."""


class FolderJobWriteError(FolderJobError):
    """A job could not be persisted atomically."""


class FolderJobRevisionError(FolderJobWriteError):
    """The expected prior revision does not match durable state."""


class FolderJobLockError(FolderJobWriteError):
    """Another process currently owns the job writer lock."""


class FolderJobFinalizedError(FolderJobWriteError):
    """A terminal job cannot be changed in place."""


class FolderJobLifecycle(StrEnum):
    """Complete lifecycle for the AI-first local job authority."""

    PLANNING = "planning"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    EXECUTING = "executing"
    VERIFIED = "verified"
    STALE = "stale"
    BLOCKED = "blocked"

    @property
    def terminal(self) -> bool:
        """Return whether this lifecycle is immutable in the MVP."""

        return self in {self.VERIFIED, self.STALE, self.BLOCKED}


class JobSourceDifferenceKind(StrEnum):
    """Stable source-change classes that invalidate an active job."""

    ADDED = "added"
    REMOVED = "removed"
    RENAMED = "renamed"
    RESIZED = "resized"
    CONTENT_CHANGED = "content_changed"
    REPLACED = "replaced"


class _StrictFrozenJobModel(BaseModel):
    """Immutable fail-closed base for serialized local job records."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class JobLocalFileIdentity(_StrictFrozenJobModel):
    """Nonportable file identity retained only in the local job."""

    relative_path: str = Field(min_length=1, max_length=4_096)
    device: int = Field(ge=0)
    inode: int = Field(ge=0)
    size: int = Field(ge=0)
    modified_ns: int = Field(ge=0)

    @classmethod
    def from_scan(cls, identity: LocalFileIdentity) -> Self:
        """Create a strict persisted identity from one scanner record."""

        return cls(
            relative_path=identity.relative_path,
            device=identity.device,
            inode=identity.inode,
            size=identity.size,
            modified_ns=identity.modified_ns,
        )


class JobLocalDirectoryIdentity(_StrictFrozenJobModel):
    """Nonportable directory identity retained only in the local job."""

    relative_path: str = Field(min_length=1, max_length=4_096)
    device: int = Field(ge=0)
    inode: int = Field(ge=0)
    modified_ns: int = Field(ge=0)

    @classmethod
    def from_scan(cls, identity: LocalDirectoryIdentity) -> Self:
        """Create a strict persisted identity from one scanner record."""

        return cls(
            relative_path=identity.relative_path,
            device=identity.device,
            inode=identity.inode,
            modified_ns=identity.modified_ns,
        )


class JobSourceMemberState(_StrictFrozenJobModel):
    """Exact local facts for one side of a stale-source difference."""

    member_kind: Literal["regular_file", "directory"]
    relative_path: str = Field(min_length=1, max_length=4_096)
    size: int | None = Field(default=None, ge=0)
    sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    device: int = Field(ge=0)
    inode: int = Field(ge=0)

    @model_validator(mode="after")
    def require_kind_fields(self) -> Self:
        if self.member_kind == "regular_file":
            if self.size is None or self.sha256 is None:
                raise ValueError("A regular-file state requires size and SHA-256.")
        elif self.size is not None or self.sha256 is not None:
            raise ValueError("A directory state cannot carry file payload facts.")
        return self


class JobSourceDifference(_StrictFrozenJobModel):
    """One deterministic difference from the job snapshot to a fresh scan."""

    kind: JobSourceDifferenceKind
    before: JobSourceMemberState | None = None
    after: JobSourceMemberState | None = None

    @model_validator(mode="after")
    def require_difference_shape(self) -> Self:
        before = self.before
        after = self.after
        if self.kind is JobSourceDifferenceKind.ADDED:
            if before is not None or after is None:
                raise ValueError("An added member requires only an after state.")
        elif self.kind is JobSourceDifferenceKind.REMOVED:
            if before is None or after is not None:
                raise ValueError("A removed member requires only a before state.")
        elif before is None or after is None:
            raise ValueError("A changed member requires before and after states.")
        elif self.kind is JobSourceDifferenceKind.RENAMED:
            if (
                before.member_kind != "regular_file"
                or after.member_kind != "regular_file"
                or before.relative_path == after.relative_path
                or before.size != after.size
                or before.sha256 != after.sha256
            ):
                raise ValueError("A rename must preserve one regular payload.")
        elif self.kind is JobSourceDifferenceKind.RESIZED:
            if (
                before.member_kind != "regular_file"
                or after.member_kind != "regular_file"
                or before.relative_path != after.relative_path
                or before.size == after.size
            ):
                raise ValueError("A resized member must retain its regular-file path.")
        elif self.kind is JobSourceDifferenceKind.CONTENT_CHANGED:
            if (
                before.member_kind != "regular_file"
                or after.member_kind != "regular_file"
                or before.relative_path != after.relative_path
                or before.size != after.size
                or before.sha256 == after.sha256
            ):
                raise ValueError("A content change must retain path and byte size.")
        elif self.kind is JobSourceDifferenceKind.REPLACED and (
            before.relative_path != after.relative_path
            or before.member_kind != after.member_kind
            or (before.device, before.inode) == (after.device, after.inode)
        ):
            raise ValueError("A replacement requires changed local identity.")
        return self


class JobSourceScanBlocker(_StrictFrozenJobModel):
    """Stable failure when a fresh source inventory cannot be constructed."""

    code: Literal["source_scan_failed"] = "source_scan_failed"
    detail: str = Field(min_length=1, max_length=2_000)


class FolderRefactorJob(_StrictFrozenJobModel):
    """The sole mutable authority for one persisted folder-refactor workflow."""

    schema_version: Literal["folder-refactor-job.v1"] = (
        FOLDER_REFACTOR_JOB_SCHEMA_VERSION
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
    local_file_identities: tuple[JobLocalFileIdentity, ...]
    local_directory_identities: tuple[JobLocalDirectoryIdentity, ...]
    user_request: str = Field(min_length=1, max_length=8_000)
    planner_progress: FolderPlannerProgress | None = None
    accepted_plan: FolderAcceptedPlan | None = None
    change_ledger: JsonValue | None = None
    pending_result_path: Path | None = None
    final_result_path: Path | None = None
    receipt_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)
    lifecycle: FolderJobLifecycle = FolderJobLifecycle.PLANNING
    blocker_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )
    blocker_message: str | None = Field(default=None, min_length=1, max_length=2_000)
    stale_differences: tuple[JobSourceDifference, ...] = ()
    source_scan_blocker: JobSourceScanBlocker | None = None

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("job_id must be a lowercase UUID4 hexadecimal value.")
        return value

    @field_validator("created_at")
    @classmethod
    def require_created_at_in_oslo(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value, label="created_at")

    @field_validator("updated_at")
    @classmethod
    def require_updated_at_in_oslo(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value, label="updated_at")

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
            raise ValueError("Local FolderRefactorJob paths must be absolute.")
        return value

    @model_validator(mode="after")
    def require_complete_bindings(self) -> Self:
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot precede created_at.")
        _require_separate_local_paths(
            source_root=self.source_root,
            output_parent=self.output_parent,
            job_path=self.job_path,
        )
        for result_path in (self.pending_result_path, self.final_result_path):
            if result_path is not None:
                _require_result_pointer(
                    result_path,
                    source_root=self.source_root,
                    output_parent=self.output_parent,
                    job_path=self.job_path,
                )

        file_paths = tuple(item.relative_path for item in self.local_file_identities)
        expected_file_paths = tuple(
            item.relative_path for item in self.source_inventory.files
        )
        if file_paths != expected_file_paths:
            raise ValueError(
                "Local file identities must exactly match the portable inventory."
            )
        inventory_sizes = {
            item.relative_path: item.size for item in self.source_inventory.files
        }
        if any(
            identity.size != inventory_sizes[identity.relative_path]
            for identity in self.local_file_identities
        ):
            raise ValueError("Local file identity sizes must match the inventory.")

        directory_paths = tuple(
            item.relative_path for item in self.local_directory_identities
        )
        if directory_paths != tuple(sorted(directory_paths)) or len(
            directory_paths
        ) != len(set(directory_paths)):
            raise ValueError("Local directory identities must be sorted and unique.")
        if not directory_paths or directory_paths[0] != ".":
            raise ValueError("Local directory identities must include the source root.")
        if len(directory_paths) != self.source_inventory.directory_count + 1:
            raise ValueError(
                "Local directory identities must account for every source directory."
            )
        empty_paths = {
            item.relative_path for item in self.source_inventory.empty_directories
        }
        if not empty_paths.issubset(set(directory_paths)):
            raise ValueError("Empty directories must have local identity records.")

        if self.planner_progress is not None:
            ledger = self.planner_progress.evidence_ledger
            if self.planner_progress.job_id != self.job_id:
                raise ValueError("Planner progress is bound to another job ID.")
            if ledger.source_commitment != self.source_inventory.source_commitment:
                raise ValueError("Planner evidence is bound to another source.")
            if ledger.request_fingerprint != request_fingerprint(self.user_request):
                raise ValueError("Planner evidence is bound to another request.")
            initial_ledger = create_initial_evidence_ledger(
                self.source_inventory,
                self.user_request,
            )
            if (
                ledger.initial_evidence != initial_ledger.initial_evidence
                or ledger.initial_evidence_bytes
                != initial_ledger.initial_evidence_bytes
            ):
                raise ValueError(
                    "Planner initial evidence does not match the job inventory."
                )
            progress_plan = self.planner_progress.accepted_plan
            if progress_plan != self.accepted_plan:
                raise ValueError(
                    "Job and planner progress must retain the same accepted plan."
                )
        elif self.accepted_plan is not None:
            raise ValueError("An accepted plan requires persisted planner progress.")

        if self.accepted_plan is not None and (
            self.accepted_plan.source_commitment
            != self.source_inventory.source_commitment
            or self.accepted_plan.request_fingerprint
            != request_fingerprint(self.user_request)
        ):
            raise ValueError("Accepted plan is bound to another job input.")
        if self.accepted_plan is not None:
            try:
                validate_accepted_plan(
                    self.source_inventory,
                    self.user_request,
                    self.accepted_plan,
                )
            except PlanCompilationError as exc:
                raise ValueError(
                    "Accepted plan no longer matches the job inventory authority."
                ) from exc

        self._require_lifecycle_fields()
        return self

    def _require_lifecycle_fields(self) -> None:
        stale_material = bool(self.stale_differences) or self.source_scan_blocker
        blocker_material = (
            self.blocker_code is not None or self.blocker_message is not None
        )
        if self.lifecycle is FolderJobLifecycle.STALE:
            if bool(self.stale_differences) == (self.source_scan_blocker is not None):
                raise ValueError(
                    "A stale job requires exact differences or one scan blocker."
                )
        elif stale_material:
            raise ValueError("Only a stale job may retain source-change evidence.")

        if self.lifecycle is FolderJobLifecycle.BLOCKED:
            if self.blocker_code is None or self.blocker_message is None:
                raise ValueError("A blocked job requires a code and message.")
        elif blocker_material:
            raise ValueError("Only a blocked job may retain blocker fields.")

        if self.lifecycle is FolderJobLifecycle.PLANNING:
            if (
                self.planner_progress is not None
                and self.planner_progress.status != "planning"
            ):
                raise ValueError("Planning lifecycle requires planning progress.")
        elif self.lifecycle is FolderJobLifecycle.AWAITING_CLARIFICATION:
            if (
                self.planner_progress is None
                or self.planner_progress.status != "awaiting_clarification"
            ):
                raise ValueError(
                    "Awaiting-clarification lifecycle requires matching progress."
                )
        elif self.lifecycle in {
            FolderJobLifecycle.EXECUTING,
            FolderJobLifecycle.VERIFIED,
        } and (
            self.planner_progress is None
            or self.planner_progress.status != "accepted"
            or self.accepted_plan is None
        ):
            raise ValueError("Execution requires one accepted planner result.")

        if self.lifecycle is FolderJobLifecycle.VERIFIED:
            if (
                self.final_result_path is None
                or self.receipt_fingerprint is None
                or self.change_ledger is None
                or self.pending_result_path is not None
            ):
                raise ValueError(
                    "A verified job requires final result, receipt, and change ledger."
                )
        elif self.final_result_path is not None or self.receipt_fingerprint is not None:
            raise ValueError("Only a verified job may retain a finalized result.")

        if self.lifecycle is not FolderJobLifecycle.EXECUTING and (
            self.pending_result_path is not None
        ):
            raise ValueError("Only an executing job may retain a pending result path.")
        if self.change_ledger is not None and self.lifecycle in {
            FolderJobLifecycle.PLANNING,
            FolderJobLifecycle.AWAITING_CLARIFICATION,
        }:
            raise ValueError("A change ledger requires execution to have started.")

        sorted_differences = _sort_differences(self.stale_differences)
        if self.stale_differences != sorted_differences:
            raise ValueError("Stale differences must use deterministic order.")
        if len(self.stale_differences) != len(set(self.stale_differences)):
            raise ValueError("Stale differences must be unique.")
        if self.stale_differences:
            _require_stale_difference_bindings(self)


class FolderJobBecameStaleError(FolderJobWriteError):
    """A pre-mutation rescan durably transitioned the job to stale."""

    def __init__(self, stale_job: FolderRefactorJob) -> None:
        self.stale_job = stale_job
        super().__init__(
            "FolderRefactorJob source changed; the job is now terminal and stale."
        )


def default_job_path(
    *,
    base_directory: Path | None = None,
    job_id: str | None = None,
) -> Path:
    """Return an absolute default path for one fresh UUID4-named local job."""

    identifier = job_id or uuid.uuid4().hex
    _require_uuid4_hex(identifier)
    base = base_directory if base_directory is not None else Path.cwd()
    return (base / DEFAULT_JOB_DIRECTORY / f"{identifier}.json").resolve()


def build_new_job(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
    user_request: str,
    display_name: str | None = None,
    scan: FolderScan | None = None,
    job_id: str | None = None,
    clock: Callable[[], datetime] | None = None,
) -> FolderRefactorJob:
    """Construct an unsaved revision-zero job from one stable source scan."""

    source_scan = scan or scan_folder(source_root)
    resolved_source = source_root.resolve(strict=True)
    if source_scan.source_root != resolved_source:
        raise FolderJobWriteError("Source scan belongs to another source root.")
    identifier = job_id or uuid.uuid4().hex
    _require_uuid4_hex(identifier)
    now = (clock or (lambda: datetime.now(tz=oslo_tz)))()
    _require_oslo_timestamp(now, label="created_at")
    return FolderRefactorJob(
        revision=0,
        job_id=identifier,
        display_name=display_name or source_scan.source_root.name or "Folder refactor",
        created_at=now,
        updated_at=now,
        source_root=source_scan.source_root,
        output_parent=output_parent.resolve(strict=False),
        job_path=job_path.resolve(strict=False),
        source_inventory=source_scan.inventory,
        local_file_identities=tuple(
            JobLocalFileIdentity.from_scan(item)
            for item in source_scan.local_file_identities
        ),
        local_directory_identities=tuple(
            JobLocalDirectoryIdentity.from_scan(item)
            for item in source_scan.local_directory_identities
        ),
        user_request=user_request,
    )


def canonical_job_bytes(job: FolderRefactorJob) -> bytes:
    """Serialize every declared field deterministically with one final newline."""

    payload = json.dumps(
        job.model_dump(mode="json"),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return f"{payload}\n".encode()


def load_job(path: Path) -> FolderRefactorJob:
    """Strictly parse one regular durable job and validate its path binding."""

    resolved_path = path.resolve(strict=False)
    try:
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise FolderJobLoadError("FolderRefactorJob path must be a regular file.")
        job = FolderRefactorJob.model_validate_json(path.read_bytes(), strict=True)
    except FolderJobLoadError:
        raise
    except (OSError, ValidationError) as exc:
        raise FolderJobLoadError(
            "FolderRefactorJob is missing, unreadable, corrupt, or unsupported."
        ) from exc
    if job.job_path != resolved_path:
        raise FolderJobLoadError(
            "FolderRefactorJob path does not match its persisted local pointer."
        )
    return job


class FolderRefactorJobStore:
    """Path-bound strict load and process-held mutation entry point."""

    def __init__(
        self,
        path: Path,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock or (lambda: datetime.now(tz=oslo_tz))

    def load(self) -> FolderRefactorJob:
        """Strictly load and rescan, durably marking changed active input stale."""

        return self.rehydrate()

    def rehydrate(self) -> FolderRefactorJob:
        """Load, rescan, and durably mark an active changed source stale."""

        with self.writer() as writer:
            return writer.rehydrate()

    def writer(self) -> FolderRefactorJobWriter:
        """Return a context that owns exclusive mutation authority."""

        return FolderRefactorJobWriter(self.path, clock=self._clock)


class FolderRefactorJobWriter:
    """Non-blocking lock plus expected-revision atomic job writes."""

    def __init__(self, path: Path, *, clock: Callable[[], datetime]) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock
        self._lock_descriptor: int | None = None

    def __enter__(self) -> Self:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.path.with_suffix(f"{self.path.suffix}.lock")
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(lock_path, flags, 0o600)
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise FolderJobLockError("FolderRefactorJob lock is not a file.")
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except FolderJobLockError:
            with suppress(UnboundLocalError, OSError):
                os.close(descriptor)
            raise
        except (BlockingIOError, OSError) as exc:
            with suppress(UnboundLocalError, OSError):
                os.close(descriptor)
            raise FolderJobLockError(
                "FolderRefactorJob is already open for mutation."
            ) from exc
        self._lock_descriptor = descriptor
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc_value, traceback
        descriptor = self._lock_descriptor
        self._lock_descriptor = None
        if descriptor is not None:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
            finally:
                os.close(descriptor)

    def load(self) -> FolderRefactorJob:
        """Strictly load while retaining mutation authority."""

        self._require_lock()
        return load_job(self.path)

    def rehydrate(self) -> FolderRefactorJob:
        """Return exact current state or persist a terminal stale transition."""

        self._require_lock()
        current = load_job(self.path)
        if current.lifecycle.terminal:
            return current
        return self._rehydrate_current(current)

    def rehydrate_against(self, current_scan: FolderScan) -> FolderRefactorJob:
        """Compare an already completed safe scan while retaining the writer lock."""

        self._require_lock()
        current = load_job(self.path)
        if current.lifecycle.terminal:
            return current
        differences = compare_job_source(current, current_scan)
        if not differences:
            _revalidate_planner_evidence(current)
            return current
        return self._persist_stale(current, differences=differences, blocker=None)

    def save(
        self,
        job: FolderRefactorJob,
        *,
        expected_revision: int | None,
    ) -> FolderRefactorJob:
        """Create or mutate against one exact durable prior revision."""

        self._require_lock()
        if job.job_path != self.path:
            raise FolderJobWriteError("Job pointer does not match the store path.")

        if expected_revision is None:
            if os.path.lexists(self.path):
                raise FolderJobRevisionError(
                    "FolderRefactorJob already exists; expected revision is required."
                )
            if job.revision != 0:
                raise FolderJobRevisionError("A new job must start at revision zero.")
            differences, blocker = _rescan_job(job)
            if differences or blocker is not None:
                raise FolderJobWriteError(
                    "Source changed before the initial job could be persisted."
                )
            updated = job
        else:
            current = load_job(self.path)
            if current.revision != expected_revision:
                raise FolderJobRevisionError(
                    "FolderRefactorJob revision changed before this mutation."
                )
            if job.revision != expected_revision:
                raise FolderJobRevisionError(
                    "Mutation input must retain the expected prior revision."
                )
            if current.lifecycle.terminal:
                raise FolderJobFinalizedError(
                    "Terminal FolderRefactorJob is immutable; create a fresh job."
                )
            rehydrated = self._rehydrate_current(current)
            if rehydrated.lifecycle is FolderJobLifecycle.STALE:
                raise FolderJobBecameStaleError(rehydrated)
            _require_immutable_identity(current=current, candidate=job)
            _require_planner_progress_successor(
                current,
                job,
            )
            _require_lifecycle_transition(current.lifecycle, job.lifecycle)
            if job.lifecycle is FolderJobLifecycle.STALE:
                raise FolderJobRevisionError(
                    "Only source rehydration may mark a job stale."
                )
            updated = self._next_revision(job, expected_revision=expected_revision)

        _atomic_write_job(self.path, updated)
        return updated

    def _rehydrate_current(self, current: FolderRefactorJob) -> FolderRefactorJob:
        differences, blocker = _rescan_job(current)
        if not differences and blocker is None:
            _revalidate_planner_evidence(current)
            return current
        return self._persist_stale(current, differences=differences, blocker=blocker)

    def _persist_stale(
        self,
        current: FolderRefactorJob,
        *,
        differences: tuple[JobSourceDifference, ...],
        blocker: JobSourceScanBlocker | None,
    ) -> FolderRefactorJob:
        """Persist one exact terminal source-change transition."""

        stale = FolderRefactorJob.model_validate(
            {
                **current.model_dump(mode="python"),
                "lifecycle": FolderJobLifecycle.STALE,
                "stale_differences": differences,
                "source_scan_blocker": blocker,
                "blocker_code": None,
                "blocker_message": None,
                "pending_result_path": None,
                "revision": current.revision + 1,
                "updated_at": self._now(),
            },
            strict=True,
        )
        _atomic_write_job(self.path, stale)
        return stale

    def _next_revision(
        self,
        job: FolderRefactorJob,
        *,
        expected_revision: int,
    ) -> FolderRefactorJob:
        return FolderRefactorJob.model_validate(
            {
                **job.model_dump(mode="python"),
                "revision": expected_revision + 1,
                "updated_at": self._now(),
            },
            strict=True,
        )

    def _now(self) -> datetime:
        value = self._clock()
        return _require_oslo_timestamp(value, label="updated_at")

    def _require_lock(self) -> None:
        if self._lock_descriptor is None:
            raise FolderJobLockError(
                "FolderRefactorJob writes require an active writer lock."
            )


def compare_job_source(
    job: FolderRefactorJob,
    current_scan: FolderScan,
) -> tuple[JobSourceDifference, ...]:
    """Return exact deterministic source differences for one active job."""

    if current_scan.source_root != job.source_root:
        raise ValueError("Current scan belongs to another source root.")

    previous_files = {item.relative_path: item for item in job.source_inventory.files}
    current_files = {item.relative_path: item for item in current_scan.inventory.files}
    previous_local_files = {
        item.relative_path: item for item in job.local_file_identities
    }
    current_local_files = {
        item.relative_path: item for item in current_scan.local_file_identities
    }
    differences: list[JobSourceDifference] = []

    for relative_path in sorted(previous_files.keys() & current_files.keys()):
        before_file = previous_files[relative_path]
        after_file = current_files[relative_path]
        before = _file_member_state(before_file, previous_local_files[relative_path])
        after = _file_member_state(after_file, current_local_files[relative_path])
        if (before.device, before.inode) != (after.device, after.inode):
            differences.append(
                JobSourceDifference(
                    kind=JobSourceDifferenceKind.REPLACED,
                    before=before,
                    after=after,
                )
            )
        elif before.size != after.size:
            differences.append(
                JobSourceDifference(
                    kind=JobSourceDifferenceKind.RESIZED,
                    before=before,
                    after=after,
                )
            )
        elif before.sha256 != after.sha256:
            differences.append(
                JobSourceDifference(
                    kind=JobSourceDifferenceKind.CONTENT_CHANGED,
                    before=before,
                    after=after,
                )
            )

    removed_files = {
        path: _file_member_state(previous_files[path], previous_local_files[path])
        for path in previous_files.keys() - current_files.keys()
    }
    added_files = {
        path: _file_member_state(current_files[path], current_local_files[path])
        for path in current_files.keys() - previous_files.keys()
    }
    _consume_unique_renames(removed_files, added_files, differences)
    differences.extend(
        JobSourceDifference(kind=JobSourceDifferenceKind.REMOVED, before=member)
        for member in removed_files.values()
    )
    differences.extend(
        JobSourceDifference(kind=JobSourceDifferenceKind.ADDED, after=member)
        for member in added_files.values()
    )

    previous_directories = {
        item.relative_path: item for item in job.local_directory_identities
    }
    current_directories = {
        item.relative_path: item for item in current_scan.local_directory_identities
    }
    for relative_path in sorted(
        previous_directories.keys() & current_directories.keys()
    ):
        before = _directory_member_state(previous_directories[relative_path])
        after = _directory_member_state(current_directories[relative_path])
        if (before.device, before.inode) != (after.device, after.inode):
            differences.append(
                JobSourceDifference(
                    kind=JobSourceDifferenceKind.REPLACED,
                    before=before,
                    after=after,
                )
            )
    differences.extend(
        JobSourceDifference(
            kind=JobSourceDifferenceKind.REMOVED,
            before=_directory_member_state(previous_directories[path]),
        )
        for path in previous_directories.keys() - current_directories.keys()
    )
    differences.extend(
        JobSourceDifference(
            kind=JobSourceDifferenceKind.ADDED,
            after=_directory_member_state(current_directories[path]),
        )
        for path in current_directories.keys() - previous_directories.keys()
    )
    return _sort_differences(tuple(differences))


def _consume_unique_renames(
    removed: dict[str, JobSourceMemberState],
    added: dict[str, JobSourceMemberState],
    differences: list[JobSourceDifference],
) -> None:
    removed_by_payload: defaultdict[tuple[int | None, str | None], list[str]] = (
        defaultdict(list)
    )
    added_by_payload: defaultdict[tuple[int | None, str | None], list[str]] = (
        defaultdict(list)
    )
    for path, member in removed.items():
        removed_by_payload[(member.size, member.sha256)].append(path)
    for path, member in added.items():
        added_by_payload[(member.size, member.sha256)].append(path)
    for identity in sorted(removed_by_payload.keys() & added_by_payload.keys()):
        before_paths = removed_by_payload[identity]
        after_paths = added_by_payload[identity]
        if len(before_paths) != 1 or len(after_paths) != 1:
            continue
        before_path = before_paths[0]
        after_path = after_paths[0]
        differences.append(
            JobSourceDifference(
                kind=JobSourceDifferenceKind.RENAMED,
                before=removed.pop(before_path),
                after=added.pop(after_path),
            )
        )


def _file_member_state(
    file: FolderFile,
    local: JobLocalFileIdentity | LocalFileIdentity,
) -> JobSourceMemberState:
    return JobSourceMemberState(
        member_kind="regular_file",
        relative_path=file.relative_path,
        size=file.size,
        sha256=file.sha256,
        device=local.device,
        inode=local.inode,
    )


def _directory_member_state(
    local: JobLocalDirectoryIdentity | LocalDirectoryIdentity,
) -> JobSourceMemberState:
    return JobSourceMemberState(
        member_kind="directory",
        relative_path=local.relative_path,
        device=local.device,
        inode=local.inode,
    )


def _rescan_job(
    job: FolderRefactorJob,
) -> tuple[tuple[JobSourceDifference, ...], JobSourceScanBlocker | None]:
    try:
        current_scan = scan_folder(job.source_root)
    except FolderScanError as exc:
        return (), JobSourceScanBlocker(detail=str(exc))
    return compare_job_source(job, current_scan), None


def _revalidate_planner_evidence(job: FolderRefactorJob) -> None:
    """Recompute every persisted evidence call from the immutable local source."""

    progress = job.planner_progress
    if progress is None:
        return
    try:
        from name_atlas.folder_refactor.transaction import (
            scan_folder_with_references,
        )

        current_scan, reference_graph = scan_folder_with_references(job.source_root)
        if compare_job_source(job, current_scan):
            raise FolderJobLoadError(
                "FolderRefactorJob source changed during evidence revalidation."
            )
        service = LocalFolderEvidenceService(
            current_scan,
            reference_graph=reference_graph,
        )
        ledger = create_initial_evidence_ledger(
            job.source_inventory,
            job.user_request,
        )
        for record in progress.evidence_ledger.records:
            if not isinstance(record.arguments, dict):
                raise FolderJobLoadError(
                    "FolderRefactorJob evidence arguments are not an object."
                )
            call_payload = {
                "tool_name": record.tool_name,
                "call_id": record.call_id,
                **record.arguments,
            }
            if record.tool_name == "list_inventory_page":
                call = ListInventoryPageCall.model_validate(call_payload, strict=True)
            elif record.tool_name == "read_text_excerpt":
                call = ReadTextExcerptCall.model_validate(call_payload, strict=True)
            else:
                call = InspectMarkdownLinksCall.model_validate(
                    call_payload,
                    strict=True,
                )
            ledger = append_evidence_execution(
                ledger,
                response_turn=record.response_turn,
                call=call,
                execution=service.execute(call),
            )
        if ledger != progress.evidence_ledger:
            raise FolderJobLoadError(
                "FolderRefactorJob evidence no longer matches deterministic reads."
            )
    except FolderJobLoadError:
        raise
    except (
        OSError,
        TypeError,
        ValidationError,
        PlannerEvidenceError,
        ValueError,
    ) as exc:
        raise FolderJobLoadError(
            "FolderRefactorJob planner evidence is corrupt or cannot be revalidated."
        ) from exc


def _require_immutable_identity(
    *,
    current: FolderRefactorJob,
    candidate: FolderRefactorJob,
) -> None:
    immutable_fields = (
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
    )
    if any(
        getattr(current, field_name) != getattr(candidate, field_name)
        for field_name in immutable_fields
    ):
        raise FolderJobRevisionError(
            "Mutation attempted to change immutable FolderRefactorJob identity."
        )


def _require_planner_progress_successor(
    current_job: FolderRefactorJob,
    candidate_job: FolderRefactorJob,
) -> None:
    """Require exactly one legal durable planner transition per job save."""

    current = current_job.planner_progress
    candidate = candidate_job.planner_progress
    if current == candidate:
        return
    if candidate is None:
        raise FolderJobRevisionError("Planner progress cannot be erased.")
    if current is None:
        _require_initial_planner_transition(candidate)
        return
    if current.status in {"accepted", "blocked"}:
        raise FolderJobRevisionError("Terminal planner progress is immutable.")

    if current.pending_response_turn is not None:
        _require_provider_completion(current, candidate)
        return
    if current.pending_evidence_call is not None:
        if _is_block_transition(current, candidate):
            return
        _require_evidence_completion(current, candidate)
        return
    if current.status == "awaiting_clarification":
        if _is_block_transition(current, candidate):
            return
        _require_clarification_answer(current, candidate)
        return
    if current.processing_response_turn is not None:
        if _is_block_transition(current, candidate):
            return
        call = current.turns[-1].tool_calls[current.processing_tool_call_index]
        if isinstance(
            call,
            ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
        ):
            _require_evidence_reservation(current, candidate, call)
            return
        if isinstance(call, SubmitPlanCall):
            _require_plan_resolution(
                current_job=current_job,
                current=current,
                candidate=candidate,
                call=call,
            )
            return
        if isinstance(call, RequestClarificationCall):
            _require_clarification_request(current, candidate, call)
            return
        raise FolderJobRevisionError("Persisted planner cursor has no valid action.")
    if _is_block_transition(current, candidate):
        return
    _require_provider_reservation(current, candidate)


def _require_initial_planner_transition(candidate: FolderPlannerProgress) -> None:
    empty = _empty_progress_fields(candidate)
    if candidate.status == "blocked":
        if not empty or candidate.blocker_code is None:
            raise FolderJobRevisionError("Initial planner blocker is not empty-bound.")
        return
    if candidate.status != "planning" or candidate.pending_response_turn != 1:
        raise FolderJobRevisionError(
            "Initial planner checkpoint must reserve the first provider turn."
        )
    if not empty or candidate.response_turns != 1:
        raise FolderJobRevisionError("Initial provider reservation is malformed.")


def _empty_progress_fields(progress: FolderPlannerProgress) -> bool:
    return not any(
        (
            progress.turns,
            progress.evidence_ledger.records,
            progress.compiler_failures,
            progress.evidence_calls,
            progress.evidence_calls_observed,
            progress.plan_submissions,
            progress.processing_response_turn,
            progress.pending_evidence_call,
            progress.clarification_question,
            progress.clarification_answer,
            progress.accepted_plan,
        )
    )


def _require_provider_reservation(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
) -> None:
    _require_exact_changes(
        current,
        candidate,
        {
            "response_turns",
            "pending_response_turn",
            "pending_response_input_bytes",
            "pending_response_input_fingerprint",
            "pending_response_input_payload",
            "outbound_evidence_bytes",
        },
        "provider reservation",
    )
    if (
        candidate.status != "planning"
        or candidate.response_turns != current.response_turns + 1
        or candidate.pending_response_turn != candidate.response_turns
        or candidate.outbound_evidence_bytes <= current.outbound_evidence_bytes
    ):
        raise FolderJobRevisionError("Provider reservation is not the next turn.")


def _require_provider_completion(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
) -> None:
    appended = candidate.turns[len(current.turns) :]
    if candidate.turns[: len(current.turns)] != current.turns or len(appended) != 1:
        raise FolderJobRevisionError("Provider completion must append one turn.")
    turn = appended[0]
    if (
        turn.response_turn != current.pending_response_turn
        or turn.input_bytes != current.pending_response_input_bytes
        or turn.input_fingerprint != current.pending_response_input_fingerprint
        or turn.input_payload != current.pending_response_input_payload
    ):
        raise FolderJobRevisionError(
            "Provider completion does not match its durable input reservation."
        )
    expected_changes = {
        "pending_response_turn",
        "pending_response_input_bytes",
        "pending_response_input_fingerprint",
        "pending_response_input_payload",
        "turns",
    }
    if turn.blocker_code is None:
        expected_changes |= {
            "processing_response_turn",
            "processing_tool_call_index",
        }
        if (
            candidate.status != "planning"
            or candidate.processing_response_turn != turn.response_turn
            or candidate.processing_tool_call_index != 0
        ):
            raise FolderJobRevisionError("Provider action cursor was not preserved.")
    else:
        expected_changes |= {"status", "blocker_code"}
        if (
            candidate.status != "blocked"
            or candidate.blocker_code != turn.blocker_code
            or candidate.processing_response_turn is not None
        ):
            raise FolderJobRevisionError("Provider blocker transition is malformed.")
    _require_exact_changes(
        current,
        candidate,
        expected_changes,
        "provider completion",
    )


def _require_evidence_reservation(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
    call: ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
) -> None:
    _require_exact_changes(
        current,
        candidate,
        {"evidence_calls", "evidence_calls_observed", "pending_evidence_call"},
        "evidence reservation",
    )
    reservation = candidate.pending_evidence_call
    if (
        reservation is None
        or reservation.call != call
        or reservation.response_turn != current.processing_response_turn
        or reservation.tool_call_index != current.processing_tool_call_index
        or reservation.evidence_call_number != current.evidence_calls + 1
        or candidate.evidence_calls != current.evidence_calls + 1
        or candidate.evidence_calls_observed != current.evidence_calls_observed + 1
    ):
        raise FolderJobRevisionError("Evidence reservation is not the current call.")


def _require_evidence_completion(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
) -> None:
    reservation = current.pending_evidence_call
    if reservation is None:
        raise FolderJobRevisionError("Evidence completion lacks a reservation.")
    records = candidate.evidence_ledger.records
    if (
        records[: len(current.evidence_ledger.records)]
        != current.evidence_ledger.records
        or len(records) != len(current.evidence_ledger.records) + 1
    ):
        raise FolderJobRevisionError("Evidence completion must append one record.")
    record = records[-1]
    call = reservation.call
    if (
        record.response_turn != reservation.response_turn
        or record.evidence_call_number != reservation.evidence_call_number
        or record.call_id != call.call_id
        or record.tool_name != call.tool_name
    ):
        raise FolderJobRevisionError("Evidence record does not match its reservation.")
    expected_ledger = append_evidence_execution(
        current.evidence_ledger,
        response_turn=reservation.response_turn,
        call=call,
        execution=EvidenceExecution(
            status=record.status,
            result=record.result,
            error_code=record.error_code,
            truncated=record.truncated,
            cache_hit=record.cache_hit,
        ),
    )
    if candidate.evidence_ledger != expected_ledger:
        raise FolderJobRevisionError("Evidence ledger is not the reserved result.")
    turn = current.turns[-1]
    next_index = reservation.tool_call_index + 1
    if next_index == len(turn.tool_calls):
        expected_cursor = (None, None)
    else:
        expected_cursor = (reservation.response_turn, next_index)
    if (
        candidate.processing_response_turn,
        candidate.processing_tool_call_index,
    ) != expected_cursor:
        raise FolderJobRevisionError("Evidence cursor did not advance exactly once.")
    changes = {"pending_evidence_call", "evidence_ledger"}
    if candidate.processing_response_turn != current.processing_response_turn:
        changes.add("processing_response_turn")
    if candidate.processing_tool_call_index != current.processing_tool_call_index:
        changes.add("processing_tool_call_index")
    _require_exact_changes(current, candidate, changes, "evidence completion")


def _require_plan_resolution(
    *,
    current_job: FolderRefactorJob,
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
    call: SubmitPlanCall,
) -> None:
    known_evidence = {"initial_inventory"} | {
        record.fingerprint for record in current.evidence_ledger.records
    }
    try:
        from name_atlas.folder_refactor.transaction import (
            scan_folder_with_references,
        )

        current_scan, reference_graph = scan_folder_with_references(
            current_job.source_root
        )
    except (FolderScanError, OSError, ValueError) as exc:
        raise FolderJobRevisionError(
            "Accepted-plan transition cannot rebuild the source reference graph."
        ) from exc
    if compare_job_source(current_job, current_scan):
        raise FolderJobRevisionError(
            "Accepted-plan transition targets a changed source."
        )
    try:
        accepted = compile_plan(
            current_job.source_inventory,
            current_job.user_request,
            call.plan,
            known_evidence_ids=known_evidence,
            evidence_fingerprint=current.evidence_ledger.evidence_fingerprint,
            reference_graph=reference_graph,
        )
    except PlanCompilationError as exc:
        _require_exact_changes(
            current,
            candidate,
            {
                "plan_submissions",
                "compiler_failures",
                "processing_response_turn",
                "processing_tool_call_index",
            },
            "plan rejection",
        )
        if (
            candidate.status != "planning"
            or candidate.plan_submissions != current.plan_submissions + 1
            or candidate.compiler_failures[:-1] != current.compiler_failures
            or candidate.compiler_failures[-1].submission_number
            != candidate.plan_submissions
            or candidate.compiler_failures[-1].code != exc.code
            or candidate.processing_response_turn is not None
        ):
            raise FolderJobRevisionError("Compiler rejection is not exact.") from exc
        return
    _require_exact_changes(
        current,
        candidate,
        {
            "status",
            "plan_submissions",
            "accepted_plan",
            "processing_response_turn",
            "processing_tool_call_index",
        },
        "plan acceptance",
    )
    if (
        candidate.status != "accepted"
        or candidate.plan_submissions != current.plan_submissions + 1
        or candidate.accepted_plan != accepted
        or candidate.processing_response_turn is not None
    ):
        raise FolderJobRevisionError("Accepted plan is not the compiled submission.")


def _require_clarification_request(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
    call: RequestClarificationCall,
) -> None:
    _require_exact_changes(
        current,
        candidate,
        {
            "status",
            "clarification_question",
            "processing_response_turn",
            "processing_tool_call_index",
        },
        "clarification request",
    )
    if (
        candidate.status != "awaiting_clarification"
        or candidate.clarification_question != call.question.strip()
        or candidate.processing_response_turn is not None
    ):
        raise FolderJobRevisionError("Clarification does not match its tool call.")


def _require_clarification_answer(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
) -> None:
    _require_exact_changes(
        current,
        candidate,
        {"status", "clarification_answer"},
        "clarification answer",
    )
    if candidate.status != "planning" or candidate.clarification_answer is None:
        raise FolderJobRevisionError("Clarification answer is not durable.")


def _is_block_transition(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
) -> bool:
    if candidate.status != "blocked" or candidate.blocker_code is None:
        return False
    changes = _progress_changes(current, candidate)
    allowed = {
        "status",
        "blocker_code",
        "processing_response_turn",
        "processing_tool_call_index",
    }
    if candidate.blocker_code == "evidence_call_limit_exceeded":
        allowed.add("evidence_calls_observed")
        if candidate.evidence_calls_observed != current.evidence_calls_observed + 1:
            return False
    return changes.issubset(allowed) and {"status", "blocker_code"}.issubset(changes)


def _require_exact_changes(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
    expected: set[str],
    label: str,
) -> None:
    actual = _progress_changes(current, candidate)
    if actual != expected:
        raise FolderJobRevisionError(
            f"Planner {label} changed unexpected fields: "
            f"expected {sorted(expected)!r}; actual {sorted(actual)!r}."
        )


def _progress_changes(
    current: FolderPlannerProgress,
    candidate: FolderPlannerProgress,
) -> set[str]:
    return {
        field_name
        for field_name in FolderPlannerProgress.model_fields
        if getattr(current, field_name) != getattr(candidate, field_name)
    }


def _require_lifecycle_transition(
    current: FolderJobLifecycle,
    candidate: FolderJobLifecycle,
) -> None:
    allowed = {
        FolderJobLifecycle.PLANNING: {
            FolderJobLifecycle.PLANNING,
            FolderJobLifecycle.AWAITING_CLARIFICATION,
            FolderJobLifecycle.EXECUTING,
            FolderJobLifecycle.BLOCKED,
        },
        FolderJobLifecycle.AWAITING_CLARIFICATION: {
            FolderJobLifecycle.PLANNING,
            FolderJobLifecycle.BLOCKED,
        },
        FolderJobLifecycle.EXECUTING: {
            FolderJobLifecycle.EXECUTING,
            FolderJobLifecycle.VERIFIED,
            FolderJobLifecycle.BLOCKED,
        },
    }
    if candidate not in allowed[current]:
        raise FolderJobRevisionError(
            f"Unsupported lifecycle transition: {current} -> {candidate}."
        )


def _require_stale_difference_bindings(job: FolderRefactorJob) -> None:
    """Bind every persisted before-state to the immutable job snapshot."""

    expected_before: dict[str, JobSourceMemberState] = {}
    local_files = {item.relative_path: item for item in job.local_file_identities}
    for source_file in job.source_inventory.files:
        expected_before[source_file.relative_path] = _file_member_state(
            source_file,
            local_files[source_file.relative_path],
        )
    for directory in job.local_directory_identities:
        expected_before[directory.relative_path] = _directory_member_state(directory)

    before_paths = tuple(
        difference.before.relative_path
        for difference in job.stale_differences
        if difference.before is not None
    )
    after_paths = tuple(
        difference.after.relative_path
        for difference in job.stale_differences
        if difference.after is not None
    )
    if len(before_paths) != len(set(before_paths)):
        raise ValueError("Stale differences repeat an original source path.")
    if len(after_paths) != len(set(after_paths)):
        raise ValueError("Stale differences repeat a current source path.")
    for difference in job.stale_differences:
        before = difference.before
        if before is not None and expected_before.get(before.relative_path) != before:
            raise ValueError(
                "Stale-difference before states must match the job snapshot."
            )
    removed_paths = {
        difference.before.relative_path
        for difference in job.stale_differences
        if difference.kind is JobSourceDifferenceKind.REMOVED
        and difference.before is not None
    }
    for difference in job.stale_differences:
        after = difference.after
        if (
            difference.kind
            in {JobSourceDifferenceKind.ADDED, JobSourceDifferenceKind.RENAMED}
            and after is not None
            and after.relative_path in expected_before
            and after.relative_path not in removed_paths
        ):
            raise ValueError(
                "Added or renamed targets must not overwrite an unchanged snapshot "
                "member."
            )


def _atomic_write_job(path: Path, job: FolderRefactorJob) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        view = memoryview(canonical_job_bytes(job))
        while view:
            written = os.write(descriptor, view)
            if written == 0:
                raise OSError("FolderRefactorJob write made no progress.")
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    except OSError as exc:
        raise FolderJobWriteError(
            "FolderRefactorJob could not be written atomically."
        ) from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        with suppress(FileNotFoundError):
            temporary.unlink()


def _fsync_directory(directory: Path) -> None:
    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError as exc:
        if exc.errno in {errno.EINVAL, errno.ENOTSUP, errno.EROFS}:
            return
        raise
    try:
        try:
            os.fsync(descriptor)
        except OSError as exc:
            if exc.errno not in {errno.EINVAL, errno.ENOTSUP, errno.EROFS}:
                raise
    finally:
        os.close(descriptor)


def _require_oslo_timestamp(value: datetime, *, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware.")
    oslo_value = value.astimezone(oslo_tz)
    if value.utcoffset() != oslo_value.utcoffset():
        raise ValueError(f"{label} must use the Europe/Oslo offset.")
    return value


def _require_uuid4_hex(value: str) -> None:
    try:
        parsed = uuid.UUID(hex=value)
    except ValueError as exc:
        raise ValueError("job_id must be a lowercase UUID4 hexadecimal value.") from exc
    if parsed.version != 4 or parsed.hex != value:
        raise ValueError("job_id must be a lowercase UUID4 hexadecimal value.")


def _require_separate_local_paths(
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
) -> None:
    if _paths_overlap(source_root, output_parent):
        raise ValueError("Source and output-parent trees cannot overlap.")
    if _paths_overlap(source_root, job_path.parent):
        raise ValueError("Local job state cannot be inside the source tree.")
    if _paths_overlap(output_parent, job_path.parent):
        raise ValueError("Local job state cannot be inside the output tree.")


def _require_result_pointer(
    path: Path,
    *,
    source_root: Path,
    output_parent: Path,
    job_path: Path,
) -> None:
    if path == output_parent or output_parent not in path.parents:
        raise ValueError("Result pointers must be below the selected output parent.")
    if _paths_overlap(path, source_root) or _paths_overlap(path, job_path.parent):
        raise ValueError("Result pointers cannot overlap source or mutable job state.")


def _paths_overlap(left: Path, right: Path) -> bool:
    return left == right or left in right.parents or right in left.parents


def _difference_sort_key(
    difference: JobSourceDifference,
) -> tuple[str, str, str]:
    before_path = difference.before.relative_path if difference.before else ""
    after_path = difference.after.relative_path if difference.after else ""
    return (before_path or after_path, difference.kind.value, after_path)


def _sort_differences(
    differences: tuple[JobSourceDifference, ...],
) -> tuple[JobSourceDifference, ...]:
    return tuple(sorted(differences, key=_difference_sort_key))
