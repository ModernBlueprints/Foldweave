"""Strict role-aware receipt contracts shared by Change Files and verifiers."""

from __future__ import annotations

import re
import uuid
from typing import Literal, Self, TypeAlias

from pydantic import Field, ValidationError, field_validator, model_validator

from name_atlas.folder_refactor.connected_change.organized_tree import (
    OrganizedTreeSnapshot,
)
from name_atlas.folder_refactor.contracts import SHA256_PATTERN, StrictFrozenModel
from name_atlas.folder_refactor.receipt_contracts import (
    FolderArtifactCommitment,
    FolderReceiptEnvelope,
    FolderStagedDataMember,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)

CONNECTED_RECEIPT_CLAIMS = (
    "Source-free verification proves internal consistency, not historical "
    "authenticity.",
    "The Change File transfers no project payload bytes but discloses names, "
    "structure, sizes, hashes, supported relationships, the instruction, and "
    "proof identifiers.",
    "The receipt is not authentication, a signature, proof of authorship, or "
    "tamper-proofing.",
    "Reconstruction covers in-scope relative paths and bytes within the supported "
    "Name Atlas contract.",
)

_CONNECTED_COMMON_RECEIPT_ARTIFACT_PATHS = frozenset(
    {
        "bag-info.txt",
        "bagit.txt",
        "manifest-sha256.txt",
        "name-atlas/accepted_plan.json",
        "name-atlas/change_ledger.json",
        "name-atlas/execution_origin.json",
        "name-atlas/forward_path_map.csv",
        "name-atlas/reference_graph.json",
        "name-atlas/reverse_path_map.csv",
        "name-atlas/source_snapshot.json",
        "name-atlas/user_request.json",
        "name-atlas/verification_report.json",
    }
)
_CONNECTED_ROLE_RECEIPT_ARTIFACT_PATHS = {
    "origin": frozenset({"name-atlas/evidence_ledger.json"}),
    "receiver": frozenset({"name-atlas/connected_change_match_report.json"}),
}
_ORIGINAL_CONTENT_PATH = re.compile(r"name-atlas/original-content/[a-f0-9]{64}\.bin\Z")

FOLDWEAVE_RECEIPT_CLAIMS = (
    "Source-free verification proves internal consistency, not historical "
    "authenticity.",
    "The Foldweave Change File transfers no project payload bytes but discloses "
    "names, structure, sizes, hashes, supported relationships, the instruction, "
    "lineage, and proof identifiers.",
    "The receipt is not authentication, a signature, proof of authorship, or "
    "tamper-proofing.",
    "Reconstruction recreates the source selected for this transaction, not an "
    "earlier collaboration ancestor.",
)

_FOLDWEAVE_REVIEW_ARTIFACT_PATHS = frozenset(
    {
        "name-atlas/execution_authorization.json",
        "name-atlas/plan_preview.json",
    }
)
_FOLDWEAVE_ROLE_RECEIPT_ARTIFACT_PATHS = {
    "origin": frozenset({"name-atlas/evidence_ledger.json"}),
    "receiver": frozenset({"name-atlas/connected_change_match_report.json"}),
    "derivative": frozenset(
        {
            "name-atlas/connected_change_match_report.json",
            "name-atlas/evidence_ledger.json",
        }
    ),
}


class FolderReceiptCoreV2(StrictFrozenModel):
    """Immutable role-aware v2 receipt core with no self-reference."""

    schema_version: Literal["folder-change-receipt.v2"] = "folder-change-receipt.v2"
    execution_role: Literal["origin", "receiver"]
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    source_file_count: int = Field(ge=1, le=500)
    source_directory_count: int = Field(ge=0, le=1_000)
    source_bytes: int = Field(ge=0)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    reference_graph_fingerprint: str = Field(pattern=SHA256_PATTERN)
    execution_origin_fingerprint: str = Field(pattern=SHA256_PATTERN)
    change_ledger_fingerprint: str = Field(pattern=SHA256_PATTERN)
    verification_report_fingerprint: str = Field(pattern=SHA256_PATTERN)
    connected_change_core_fingerprint: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    imported_change_file_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    originating_receipt_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    artifact_commitments: tuple[FolderArtifactCommitment, ...] = Field(min_length=1)
    staged_data_members: tuple[FolderStagedDataMember, ...] = Field(min_length=1)
    staged_data_commitment: str = Field(pattern=SHA256_PATTERN)
    organized_tree: OrganizedTreeSnapshot
    map_row_count: int = Field(ge=1, le=500)
    path_change_count: int = Field(ge=0, le=500)
    supported_link_count: int = Field(ge=0, le=10_000)
    rewritten_link_count: int = Field(ge=0, le=10_000)
    producer_bagit_messages: tuple[str, ...] = Field(min_length=1)
    claims: tuple[str, ...] = CONNECTED_RECEIPT_CLAIMS

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("job_id must be lowercase UUID4 hexadecimal text.")
        return value

    @model_validator(mode="after")
    def require_role_and_counts(self) -> Self:
        paths = tuple(item.path for item in self.artifact_commitments)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("Artifact commitments must be path-sorted and unique.")
        required_paths = connected_required_receipt_artifact_paths(self.execution_role)
        path_set = set(paths)
        missing_paths = sorted(required_paths - path_set)
        unsupported_paths = sorted(
            path
            for path in path_set - required_paths
            if _ORIGINAL_CONTENT_PATH.fullmatch(path) is None
        )
        if missing_paths:
            raise ValueError(
                f"Receipt omits required role-specific artifacts: {missing_paths!r}."
            )
        if unsupported_paths:
            raise ValueError(
                "Receipt commits unsupported, role-incompatible, or circular "
                f"artifacts: {unsupported_paths!r}."
            )
        staged_paths = tuple(item.path for item in self.staged_data_members)
        if staged_paths != tuple(sorted(staged_paths)) or len(staged_paths) != len(
            set(staged_paths)
        ):
            raise ValueError("Staged members must be path-sorted and unique.")
        if self.source_file_count != len(self.staged_data_members):
            raise ValueError("Receipt staged-data count must equal source file count.")
        if self.organized_tree.file_count != self.source_file_count:
            raise ValueError("Organized-tree file count differs from the source.")
        if self.map_row_count != self.source_file_count:
            raise ValueError("Receipt map-row count must equal source file count.")
        if self.path_change_count > self.map_row_count:
            raise ValueError("Path-change count exceeds complete map rows.")
        receiver_fields = (
            self.imported_change_file_fingerprint,
            self.imported_change_file_sha256,
            self.originating_receipt_fingerprint,
            self.match_report_fingerprint,
            self.match_report_sha256,
        )
        if self.execution_role == "origin":
            if any(value is not None for value in receiver_fields):
                raise ValueError("An origin receipt cannot carry receiver bindings.")
        elif any(value is None for value in receiver_fields):
            raise ValueError("A receiver receipt requires every incoming binding.")
        if self.claims != CONNECTED_RECEIPT_CLAIMS:
            raise ValueError("Receipt claim boundaries differ from the contract.")
        return self


def connected_required_receipt_artifact_paths(
    execution_role: Literal["origin", "receiver"],
) -> frozenset[str]:
    """Return the exact static raw-commitment set for one v2 receipt role."""

    return (
        _CONNECTED_COMMON_RECEIPT_ARTIFACT_PATHS
        | _CONNECTED_ROLE_RECEIPT_ARTIFACT_PATHS[execution_role]
    )


class FolderReceiptEnvelopeV2(StrictFrozenModel):
    """v2 receipt envelope whose fingerprint is outside its own hash domain."""

    receipt: FolderReceiptCoreV2
    receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_fingerprint(self) -> Self:
        if canonical_sha256(self.receipt) != self.receipt_fingerprint:
            raise ValueError("Receipt fingerprint does not match its v2 core.")
        return self


class FolderReceiptCoreV3(StrictFrozenModel):
    """Review- and lineage-aware receipt core with no envelope self-reference."""

    schema_version: Literal["folder-change-receipt.v3"] = "folder-change-receipt.v3"
    execution_role: Literal["origin", "receiver", "derivative"]
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    source_file_count: int = Field(ge=1, le=500)
    source_directory_count: int = Field(ge=0, le=1_000)
    source_bytes: int = Field(ge=0)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    reference_graph_fingerprint: str = Field(pattern=SHA256_PATTERN)
    execution_origin_fingerprint: str = Field(pattern=SHA256_PATTERN)
    execution_authorization_fingerprint: str = Field(pattern=SHA256_PATTERN)
    plan_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    compiled_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    change_ledger_fingerprint: str = Field(pattern=SHA256_PATTERN)
    verification_report_fingerprint: str = Field(pattern=SHA256_PATTERN)
    connected_change_core_schema_version: Literal[
        "connected-change-core.v1",
        "connected-change-core.v2",
    ]
    connected_change_core_fingerprint: str = Field(pattern=SHA256_PATTERN)
    lineage_generation: int = Field(ge=0, le=32)
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    imported_change_file_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    originating_receipt_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    artifact_commitments: tuple[FolderArtifactCommitment, ...] = Field(min_length=1)
    staged_data_members: tuple[FolderStagedDataMember, ...] = Field(min_length=1)
    staged_data_commitment: str = Field(pattern=SHA256_PATTERN)
    organized_tree: OrganizedTreeSnapshot
    map_row_count: int = Field(ge=1, le=500)
    path_change_count: int = Field(ge=0, le=500)
    supported_link_count: int = Field(ge=0, le=10_000)
    rewritten_link_count: int = Field(ge=0, le=10_000)
    producer_bagit_messages: tuple[str, ...] = Field(min_length=1)
    claims: tuple[str, ...] = FOLDWEAVE_RECEIPT_CLAIMS

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("job_id must be lowercase UUID4 hexadecimal text.")
        return value

    @model_validator(mode="after")
    def require_role_proof_and_counts(self) -> Self:
        paths = tuple(item.path for item in self.artifact_commitments)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("Artifact commitments must be path-sorted and unique.")
        required_paths = foldweave_required_receipt_artifact_paths(self.execution_role)
        path_set = set(paths)
        missing_paths = sorted(required_paths - path_set)
        unsupported_paths = sorted(
            path
            for path in path_set - required_paths
            if _ORIGINAL_CONTENT_PATH.fullmatch(path) is None
        )
        if missing_paths:
            raise ValueError(
                f"Receipt omits required role-specific artifacts: {missing_paths!r}."
            )
        if unsupported_paths:
            raise ValueError(
                "Receipt commits unsupported, role-incompatible, or circular "
                f"artifacts: {unsupported_paths!r}."
            )
        staged_paths = tuple(item.path for item in self.staged_data_members)
        if staged_paths != tuple(sorted(staged_paths)) or len(staged_paths) != len(
            set(staged_paths)
        ):
            raise ValueError("Staged members must be path-sorted and unique.")
        if self.source_file_count != len(self.staged_data_members):
            raise ValueError("Receipt staged-data count must equal source file count.")
        if self.organized_tree.file_count != self.source_file_count:
            raise ValueError("Organized-tree file count differs from the source.")
        if self.map_row_count != self.source_file_count:
            raise ValueError("Receipt map-row count must equal source file count.")
        if self.path_change_count > self.map_row_count:
            raise ValueError("Path-change count exceeds complete map rows.")
        receiver_fields = (
            self.imported_change_file_fingerprint,
            self.imported_change_file_sha256,
            self.originating_receipt_fingerprint,
            self.match_report_fingerprint,
            self.match_report_sha256,
        )
        if self.execution_role == "origin":
            if any(value is not None for value in receiver_fields):
                raise ValueError("An origin receipt cannot carry receiver bindings.")
            if self.lineage_generation != 0:
                raise ValueError("A root origin receipt must use generation zero.")
        elif any(value is None for value in receiver_fields):
            raise ValueError(
                "A receiver or derivative receipt requires every incoming binding."
            )
        if self.execution_role == "derivative":
            if self.connected_change_core_schema_version != "connected-change-core.v2":
                raise ValueError("A derivative receipt requires a v2 Change File Core.")
            if self.lineage_generation < 1:
                raise ValueError("A derivative receipt requires non-root lineage.")
        if self.claims != FOLDWEAVE_RECEIPT_CLAIMS:
            raise ValueError("Receipt claim boundaries differ from the contract.")
        return self


class FolderReceiptEnvelopeV3(StrictFrozenModel):
    """v3 receipt envelope whose fingerprint excludes the envelope field."""

    receipt: FolderReceiptCoreV3
    receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_fingerprint(self) -> Self:
        if folder_receipt_v3_fingerprint(self.receipt) != self.receipt_fingerprint:
            raise ValueError("Receipt fingerprint does not match its v3 core.")
        return self


FolderReceiptEnvelopeAny: TypeAlias = (
    FolderReceiptEnvelope | FolderReceiptEnvelopeV2 | FolderReceiptEnvelopeV3
)


def foldweave_required_receipt_artifact_paths(
    execution_role: Literal["origin", "receiver", "derivative"],
) -> frozenset[str]:
    """Return the exact non-circular portable authority set for v3."""

    return (
        _CONNECTED_COMMON_RECEIPT_ARTIFACT_PATHS
        | _FOLDWEAVE_REVIEW_ARTIFACT_PATHS
        | _FOLDWEAVE_ROLE_RECEIPT_ARTIFACT_PATHS[execution_role]
    )


def folder_receipt_v3_fingerprint(core: FolderReceiptCoreV3) -> str:
    """Hash only the immutable v3 receipt core."""

    return canonical_sha256(core)


def build_folder_receipt_envelope_v3(
    core: FolderReceiptCoreV3,
) -> FolderReceiptEnvelopeV3:
    """Finalize a v3 receipt without referencing a future Change File envelope."""

    return FolderReceiptEnvelopeV3(
        receipt=core,
        receipt_fingerprint=folder_receipt_v3_fingerprint(core),
    )


def parse_folder_receipt_envelope_any(data: bytes) -> FolderReceiptEnvelopeAny:
    """Strictly dispatch canonical receipt bytes across v1, v2, and v3."""

    from name_atlas.folder_refactor.portable_artifacts import (
        FolderPortableArtifactError,
        strict_json_object,
    )

    try:
        raw = strict_json_object(data)
    except FolderPortableArtifactError:
        raise
    if set(raw) != {"receipt", "receipt_fingerprint"}:
        raise FolderPortableArtifactError("Receipt envelope fields are not exact.")
    receipt = raw.get("receipt")
    if not isinstance(receipt, dict):
        raise FolderPortableArtifactError("Receipt core must be an object.")
    model_type: type[FolderReceiptEnvelopeAny]
    schema_version = receipt.get("schema_version")
    if schema_version == "folder-change-receipt.v1":
        model_type = FolderReceiptEnvelope
    elif schema_version == "folder-change-receipt.v2":
        model_type = FolderReceiptEnvelopeV2
    elif schema_version == "folder-change-receipt.v3":
        model_type = FolderReceiptEnvelopeV3
    else:
        raise FolderPortableArtifactError("Receipt schema version is unsupported.")
    try:
        envelope = model_type.model_validate_json(data, strict=True)
    except ValidationError as exc:
        raise FolderPortableArtifactError(
            "Receipt does not satisfy its declared schema."
        ) from exc
    if canonical_json_bytes(envelope) != data:
        raise FolderPortableArtifactError("Receipt must use canonical JSON bytes.")
    return envelope
