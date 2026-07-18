"""Strict serialized contracts for AI-first folder refactoring."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from name_atlas.folder_refactor.naming import (
    validate_complete_target_tree,
    validate_result_folder_name,
    validate_target_path,
)
from name_atlas.folder_refactor.serialization import canonical_sha256

SHA256_PATTERN = r"^[a-f0-9]{64}$"
MAX_MARKDOWN_ADAPTER_BYTES = 16 * 1024 * 1024


class StrictFrozenModel(BaseModel):
    """Immutable fail-closed base for every portable contract."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class FolderFile(StrictFrozenModel):
    """One regular source file with a stable path-bound identity."""

    member_kind: Literal["regular_file"] = "regular_file"
    file_id: str = Field(pattern=SHA256_PATTERN)
    relative_path: str = Field(min_length=1, max_length=4_096)
    size: int = Field(ge=0)
    sha256: str = Field(pattern=SHA256_PATTERN)
    protected: bool
    evidence_eligible: bool
    protection_reasons: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_protection_flags(self) -> FolderFile:
        """Keep evidence and protection flags internally consistent."""

        _validate_portable_source_path(self.relative_path)
        if self.protected and self.evidence_eligible:
            raise ValueError("Protected files cannot be eligible for content evidence.")
        if self.protected and not self.protection_reasons:
            raise ValueError("Protected files require at least one protection reason.")
        if not self.protected and self.protection_reasons:
            raise ValueError("Unprotected files cannot carry protection reasons.")
        identity_payload = {
            "domain": "name-atlas:folder-file-id:v1",
            "original_relative_path": self.relative_path,
            "payload_sha256": self.sha256,
            "size": self.size,
        }
        if self.file_id != canonical_sha256(identity_payload):
            raise ValueError("File identity does not match its path, size, and digest.")
        return self


class FolderEmptyDirectory(StrictFrozenModel):
    """One explicit source directory containing no members."""

    member_kind: Literal["empty_directory"] = "empty_directory"
    relative_path: str = Field(min_length=1, max_length=4_096)
    protected: Literal[True] = True
    evidence_eligible: Literal[False] = False

    @model_validator(mode="after")
    def validate_path(self) -> FolderEmptyDirectory:
        """Require one portable relative source path."""

        _validate_portable_source_path(self.relative_path)
        return self


class FolderInventory(StrictFrozenModel):
    """Path-neutral complete inventory for the supported source folder."""

    schema_version: Literal["folder-inventory.v1"] = "folder-inventory.v1"
    files: tuple[FolderFile, ...] = Field(min_length=1, max_length=500)
    empty_directories: tuple[FolderEmptyDirectory, ...] = ()
    directory_count: int = Field(ge=0, le=1_000)
    total_bytes: int = Field(ge=0)
    source_commitment: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_complete_inventory(self) -> FolderInventory:
        """Reject unordered, duplicate, or internally inconsistent inventories."""

        file_paths = [item.relative_path for item in self.files]
        empty_paths = [item.relative_path for item in self.empty_directories]
        if file_paths != sorted(file_paths) or len(file_paths) != len(set(file_paths)):
            raise ValueError("Inventory files must be sorted and path-unique.")
        if empty_paths != sorted(empty_paths) or len(empty_paths) != len(
            set(empty_paths)
        ):
            raise ValueError("Empty directories must be sorted and path-unique.")
        if set(file_paths) & set(empty_paths):
            raise ValueError("A path cannot be both a file and an empty directory.")
        if self.directory_count < len(self.empty_directories):
            raise ValueError(
                "Directory count cannot be below the empty-directory count."
            )
        if self.total_bytes != sum(item.size for item in self.files):
            raise ValueError("Inventory total bytes do not match its files.")
        expected = compute_inventory_commitment(
            files=self.files,
            empty_directories=self.empty_directories,
            directory_count=self.directory_count,
            total_bytes=self.total_bytes,
        )
        if self.source_commitment != expected:
            raise ValueError("Inventory source commitment does not match its members.")
        return self


class FolderPlanEntry(StrictFrozenModel):
    """One planner-proposed target for one eligible source file."""

    file_id: str = Field(pattern=SHA256_PATTERN)
    original_path: str = Field(min_length=1, max_length=4_096)
    proposed_target: str = Field(min_length=1, max_length=1_024)
    rationale: str = Field(min_length=1, max_length=1_000)
    evidence_ids: tuple[str, ...] = Field(min_length=1)


class FolderPlan(StrictFrozenModel):
    """Complete planner submission before deterministic compilation."""

    schema_version: Literal["folder-plan.v1"] = "folder-plan.v1"
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    request_scope: Literal["rename_and_move_every_file"]
    evidence_schema_version: Literal["folder-evidence-ledger.v1"] = (
        "folder-evidence-ledger.v1"
    )
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    result_folder_name: str = Field(min_length=1, max_length=240)
    entries: tuple[FolderPlanEntry, ...] = ()
    exclusions: tuple[str, ...]


class PlanOutcome(StrictFrozenModel):
    """Planner produced one complete candidate plan."""

    schema_version: Literal["folder-planner-outcome.v1"] = "folder-planner-outcome.v1"
    kind: Literal["plan"] = "plan"
    plan: FolderPlan


class ClarificationOutcome(StrictFrozenModel):
    """Planner requires one bounded missing-intent answer."""

    schema_version: Literal["folder-planner-outcome.v1"] = "folder-planner-outcome.v1"
    kind: Literal["clarification"] = "clarification"
    question: str = Field(min_length=1, max_length=1_000)


class BlockedOutcome(StrictFrozenModel):
    """Planner cannot produce a valid plan within the supported contract."""

    schema_version: Literal["folder-planner-outcome.v1"] = "folder-planner-outcome.v1"
    kind: Literal["blocked"] = "blocked"
    blocker_code: str = Field(min_length=1, max_length=128)
    message: str = Field(min_length=1, max_length=2_000)


FolderPlannerOutcome = Annotated[
    PlanOutcome | ClarificationOutcome | BlockedOutcome,
    Field(discriminator="kind"),
]


class AcceptedFileMapping(StrictFrozenModel):
    """One mechanically accepted source-to-result file mapping."""

    file_id: str = Field(pattern=SHA256_PATTERN)
    original_path: str = Field(min_length=1, max_length=4_096)
    target_path: str = Field(min_length=1, max_length=1_024)
    protected: bool
    planner_supplied: bool

    @model_validator(mode="after")
    def validate_paths(self) -> AcceptedFileMapping:
        """Keep each portable map row syntactically path-neutral."""

        _validate_portable_source_path(self.original_path)
        return self


class FolderAcceptedPlan(StrictFrozenModel):
    """Immutable complete map authorized for copy-only execution."""

    schema_version: Literal["folder-accepted-plan.v1"] = "folder-accepted-plan.v1"
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    request_scope: Literal["rename_and_move_every_file"]
    evidence_schema_version: Literal["folder-evidence-ledger.v1"] = (
        "folder-evidence-ledger.v1"
    )
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    result_folder_name: str = Field(min_length=1, max_length=240)
    file_mappings: tuple[AcceptedFileMapping, ...] = Field(
        min_length=1,
        max_length=500,
    )
    empty_directories: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_complete_map(self) -> FolderAcceptedPlan:
        """Reject reordered, duplicate, or authority-inconsistent accepted maps."""

        validate_result_folder_name(self.result_folder_name)
        originals = [item.original_path for item in self.file_mappings]
        file_ids = [item.file_id for item in self.file_mappings]
        if originals != sorted(originals) or len(originals) != len(set(originals)):
            raise ValueError("Accepted mappings must be sorted and source-path unique.")
        if len(file_ids) != len(set(file_ids)):
            raise ValueError("Accepted mappings must contain unique file IDs.")
        for mapping in self.file_mappings:
            validate_target_path(
                mapping.target_path,
                original_path=mapping.original_path,
                protected=mapping.protected,
            )
            if mapping.protected:
                invalid_protected_mapping = (
                    mapping.planner_supplied
                    or mapping.original_path != mapping.target_path
                )
                if invalid_protected_mapping:
                    raise ValueError(
                        "Protected mappings must be injected and unchanged."
                    )
            elif not mapping.planner_supplied:
                raise ValueError("Eligible mappings must originate from the planner.")
        empty_paths = list(self.empty_directories)
        if empty_paths != sorted(empty_paths) or len(empty_paths) != len(
            set(empty_paths)
        ):
            raise ValueError("Accepted empty directories must be sorted and unique.")
        for path in empty_paths:
            validate_target_path(path, original_path=path, protected=True)
        targets = [item.target_path for item in self.file_mappings]
        validate_complete_target_tree(targets, empty_paths)
        return self


class FolderVerificationCheck(StrictFrozenModel):
    """One deterministic fact in the A1 proof report."""

    check_id: str = Field(min_length=1, max_length=128)
    passed: bool
    detail: str = Field(min_length=1, max_length=1_000)


class FolderVerificationReport(StrictFrozenModel):
    """Path-neutral deterministic report for one created result."""

    schema_version: Literal["folder-verification-report.v1"] = (
        "folder-verification-report.v1"
    )
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    result_folder_name: str = Field(min_length=1, max_length=240)
    staged_data_commitment: str = Field(pattern=SHA256_PATTERN)
    file_count: int = Field(ge=1, le=500)
    path_change_count: int = Field(ge=0, le=500)
    protected_file_count: int = Field(ge=0, le=500)
    empty_directory_count: int = Field(ge=0, le=1_000)
    supported_link_count: int = Field(default=0, ge=0)
    rewritten_link_count: int = Field(default=0, ge=0)
    rewritten_markdown_file_count: int = Field(default=0, ge=0, le=500)
    checks: tuple[FolderVerificationCheck, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def require_complete_success(self) -> FolderVerificationReport:
        """Require truthful link counts and a completely passing report."""

        if self.rewritten_link_count > self.supported_link_count:
            raise ValueError("Rewritten-link count exceeds supported-link count.")
        if any(not check.passed for check in self.checks):
            raise ValueError("A promoted verification report cannot contain failures.")
        return self


def compute_inventory_commitment(
    *,
    files: tuple[FolderFile, ...],
    empty_directories: tuple[FolderEmptyDirectory, ...],
    directory_count: int,
    total_bytes: int,
) -> str:
    """Compute the frozen path-neutral inventory commitment."""

    payload = {
        "domain": "name-atlas:folder-inventory:v1",
        "directory_count": directory_count,
        "empty_directories": [
            item.model_dump(mode="json") for item in empty_directories
        ],
        "files": [item.model_dump(mode="json") for item in files],
        "total_bytes": total_bytes,
    }
    return canonical_sha256(payload)


def _validate_portable_source_path(value: str) -> None:
    """Reject source paths that cannot be represented safely and portably."""

    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("Source path is not valid UTF-8.") from exc
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise ValueError("Source path must be a relative POSIX path.")
    if any(ord(character) < 32 or 127 <= ord(character) <= 159 for character in value):
        raise ValueError("Source path contains a control character.")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError("Source path contains an empty or dot segment.")
    if PurePosixPath(value).as_posix() != value:
        raise ValueError("Source path is not normalized POSIX syntax.")
