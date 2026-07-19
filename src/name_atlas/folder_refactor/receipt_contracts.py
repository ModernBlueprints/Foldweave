"""Strict generic-folder proof, receipt, verifier, and reconstruction contracts."""

from __future__ import annotations

import hashlib
import re
import uuid
from datetime import datetime
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Literal, Self
from zoneinfo import ZoneInfo

from pydantic import Field, JsonValue, field_validator, model_validator

from name_atlas.domain import PackageValidationResult
from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.planner_contracts import (
    EvidenceCallRecord,
    FolderPlannerProgress,
    PlannerCompilerFailure,
    PlannerObservableTurn,
    SubmitPlanCall,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

oslo_tz = ZoneInfo("Europe/Oslo")

FOLDER_PACKAGE_CONTRACT_ID = "name-atlas-ordinary-folder.v1"
FOLDER_NAMING_PROFILE_ID = "name-atlas-cross-platform-safe.v1"
PROOF_HTML_PATH = "name-atlas/proof_and_restore.html"
RECEIPT_JSON_PATH = "name-atlas/change_receipt.json"

RECEIPT_CLAIM_BOUNDARIES = (
    "Source-free verification proves internal consistency against the committed "
    "source description, not historical authenticity.",
    "Supported connections are the declared inline relative Markdown links "
    "within the Name Atlas folder contract.",
    "Opaque files are carried byte-for-byte; their image, audio, video, PDF, "
    "spreadsheet, or Office contents are not interpreted.",
    "The receipt is not a signature, authentication, proof of authorship, "
    "institutional authorization, or tamper-proofing mechanism.",
    "Reconstruction covers in-scope relative paths and bytes, not timestamps, "
    "ownership, ACLs, extended attributes, resource forks, or arbitrary "
    "filesystem state.",
)


def _require_relative_posix(value: str) -> str:
    """Validate one path-neutral relative POSIX artifact path."""

    if not isinstance(value, str) or not value:
        raise ValueError("Portable path must be nonempty text.")
    if value.startswith("/") or "\\" in value or "\x00" in value:
        raise ValueError("Portable path must be relative POSIX syntax.")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value:
        raise ValueError("Portable path is not normalized POSIX syntax.")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError("Portable path contains an empty or dot segment.")
    return value


class FolderUserRequestArtifact(StrictFrozenModel):
    """Exact portable user request and its domain-separated fingerprint."""

    schema_version: Literal["folder-user-request.v1"] = "folder-user-request.v1"
    request: str = Field(min_length=1, max_length=8_000)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_fingerprint(self) -> Self:
        if self.request_fingerprint != request_fingerprint(self.request):
            raise ValueError("User-request fingerprint does not match exact text.")
        return self


class FolderPlannerUsage(StrictFrozenModel):
    """Observable per-turn usage for one truthful live planner request."""

    response_turn: int = Field(ge=1, le=8)
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    cached_input_tokens: int = Field(ge=0)
    reasoning_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    latency_ms: float | None = Field(default=None, ge=0.0)
    recorded_at: datetime | None = None
    estimated_cost_microusd: int = Field(ge=0)

    @model_validator(mode="after")
    def require_observable_usage_consistency(self) -> Self:
        if self.cached_input_tokens > self.input_tokens:
            raise ValueError("Cached input tokens cannot exceed input tokens.")
        if self.reasoning_tokens is not None and (
            self.reasoning_tokens > self.output_tokens
        ):
            raise ValueError("Reasoning tokens cannot exceed output tokens.")
        if self.total_tokens is not None and self.total_tokens != (
            self.input_tokens + self.output_tokens
        ):
            raise ValueError("Total tokens must equal input plus output tokens.")
        if self.recorded_at is not None:
            if self.recorded_at.tzinfo is None or self.recorded_at.utcoffset() is None:
                raise ValueError("Planner usage timestamp must be timezone-aware.")
            if (
                self.recorded_at.utcoffset()
                != self.recorded_at.astimezone(oslo_tz).utcoffset()
            ):
                raise ValueError("Planner usage timestamp must use Europe/Oslo.")
        return self


class FolderEvidenceLedger(StrictFrozenModel):
    """Portable bounded evidence plus the complete observable planner transcript."""

    schema_version: Literal["folder-evidence-ledger.v1"] = "folder-evidence-ledger.v1"
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    request_scope: Literal["rename_and_move_every_file"]
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model_ids: tuple[str, ...] = ()
    store_false: bool | None = None
    initial_evidence: JsonValue
    initial_evidence_bytes: int = Field(ge=1, le=512 * 1024)
    evidence_records: tuple[EvidenceCallRecord, ...] = ()
    aggregate_result_bytes: int = Field(ge=0, le=128 * 1024)
    total_outbound_evidence_bytes: int = Field(ge=1, le=512 * 1024)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    observable_turns: tuple[PlannerObservableTurn, ...] = ()
    compiler_failures: tuple[PlannerCompilerFailure, ...] = ()
    response_turn_count: int = Field(ge=1, le=8)
    evidence_call_count: int = Field(ge=0, le=24)
    plan_submission_count: int = Field(ge=1, le=3)
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
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    usage: tuple[FolderPlannerUsage, ...] = ()
    transcript_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("job_id must be lowercase UUID4 hexadecimal text.")
        return value

    @model_validator(mode="after")
    def require_complete_transcript(self) -> Self:
        evidence_payload: dict[str, JsonValue] = {
            "aggregate_result_bytes": self.aggregate_result_bytes,
            "initial_evidence": self.initial_evidence,
            "initial_evidence_bytes": self.initial_evidence_bytes,
            "records": [
                record.model_dump(mode="json") for record in self.evidence_records
            ],
            "request_fingerprint": self.request_fingerprint,
            "schema_version": "folder-planner-evidence-state.v1",
            "source_commitment": self.source_commitment,
            "total_outbound_evidence_bytes": self.total_outbound_evidence_bytes,
        }
        if self.evidence_fingerprint != canonical_sha256(evidence_payload):
            raise ValueError(
                "Portable evidence does not match its planner fingerprint."
            )
        turn_numbers = tuple(turn.response_turn for turn in self.observable_turns)
        if turn_numbers != tuple(range(1, len(self.observable_turns) + 1)):
            raise ValueError("Observable planner turns must be contiguous and ordered.")
        if self.response_turn_count != len(self.observable_turns):
            raise ValueError("Response-turn count does not match observable turns.")
        if self.evidence_call_count != len(self.evidence_records):
            raise ValueError("Evidence-call count does not match durable records.")
        if self.plan_submission_count != len(self.compiler_failures) + 1:
            raise ValueError(
                "An accepted transcript requires one final plan submission."
            )
        submit_count = sum(
            isinstance(call, SubmitPlanCall)
            for turn in self.observable_turns
            for call in turn.tool_calls
        )
        if submit_count != self.plan_submission_count:
            raise ValueError(
                "Plan-submission count does not match observable submit calls."
            )
        if (self.clarification_question is None) != (self.clarification_answer is None):
            raise ValueError("Clarification question and answer must appear together.")
        if any(
            turn.provider_kind != self.provider_kind for turn in self.observable_turns
        ):
            raise ValueError("Observable turns use more than one provider origin.")
        returned = tuple(
            dict.fromkeys(
                turn.returned_model
                for turn in self.observable_turns
                if turn.returned_model is not None
            )
        )
        if self.returned_model_ids != returned:
            raise ValueError("Returned-model IDs do not match observable turns.")
        if self.provider_kind == "live":
            if self.store_false is not True or not self.returned_model_ids:
                raise ValueError(
                    "A live transcript requires store=false and model IDs."
                )
        elif self.store_false is not None:
            raise ValueError("Only a live transcript records an API store setting.")
        usage_turns = tuple(item.response_turn for item in self.usage)
        if usage_turns != tuple(sorted(set(usage_turns))):
            raise ValueError("Usage records must use unique ascending turn numbers.")
        if self.provider_kind == "live" and usage_turns != tuple(
            range(1, self.response_turn_count + 1)
        ):
            raise ValueError(
                "Every successful live response turn requires one usage record."
            )
        if self.provider_kind != "live" and self.usage:
            raise ValueError("Only a live transcript may contain provider usage.")
        if self.transcript_fingerprint != canonical_sha256(
            folder_evidence_transcript_payload(self)
        ):
            raise ValueError("Portable planner-transcript fingerprint is not exact.")
        return self

    @classmethod
    def from_progress(
        cls,
        *,
        job_id: str,
        progress: FolderPlannerProgress,
        usage: tuple[FolderPlannerUsage, ...] = (),
        store_false: bool | None = None,
    ) -> Self:
        """Project accepted restart state into one path-neutral public artifact."""

        if progress.status != "accepted" or progress.accepted_plan is None:
            raise ValueError("Portable evidence requires one accepted planner result.")
        if progress.pending_response_turn is not None:
            raise ValueError("Portable evidence cannot retain a pending provider turn.")
        ledger = progress.evidence_ledger
        returned = tuple(
            dict.fromkeys(
                turn.returned_model
                for turn in progress.turns
                if turn.returned_model is not None
            )
        )
        fingerprint_payload: dict[str, JsonValue] = {
            "accepted_plan_fingerprint": canonical_sha256(progress.accepted_plan),
            "aggregate_result_bytes": ledger.aggregate_result_bytes,
            "clarification_answer": progress.clarification_answer,
            "clarification_question": progress.clarification_question,
            "compiler_failures": [
                failure.model_dump(mode="json")
                for failure in progress.compiler_failures
            ],
            "evidence_call_count": len(ledger.records),
            "evidence_fingerprint": ledger.evidence_fingerprint,
            "evidence_records": [
                record.model_dump(mode="json") for record in ledger.records
            ],
            "initial_evidence": ledger.initial_evidence,
            "initial_evidence_bytes": ledger.initial_evidence_bytes,
            "job_id": job_id,
            "model_alias": progress.model_alias,
            "observable_turns": [
                turn.model_dump(mode="json") for turn in progress.turns
            ],
            "plan_submission_count": progress.plan_submissions,
            "provider_kind": progress.provider_kind,
            "request_fingerprint": ledger.request_fingerprint,
            "request_scope": progress.accepted_plan.request_scope,
            "response_turn_count": len(progress.turns),
            "returned_model_ids": list(returned),
            "schema_version": "folder-evidence-ledger.v1",
            "source_commitment": ledger.source_commitment,
            "store_false": store_false,
            "total_outbound_evidence_bytes": ledger.total_outbound_evidence_bytes,
            "usage": [item.model_dump(mode="json") for item in usage],
        }
        return cls(
            accepted_plan_fingerprint=canonical_sha256(progress.accepted_plan),
            aggregate_result_bytes=ledger.aggregate_result_bytes,
            clarification_answer=progress.clarification_answer,
            clarification_question=progress.clarification_question,
            compiler_failures=progress.compiler_failures,
            evidence_call_count=len(ledger.records),
            evidence_fingerprint=ledger.evidence_fingerprint,
            evidence_records=ledger.records,
            initial_evidence=ledger.initial_evidence,
            initial_evidence_bytes=ledger.initial_evidence_bytes,
            job_id=job_id,
            model_alias=progress.model_alias,
            observable_turns=progress.turns,
            plan_submission_count=progress.plan_submissions,
            provider_kind=progress.provider_kind,
            request_fingerprint=ledger.request_fingerprint,
            request_scope=progress.accepted_plan.request_scope,
            response_turn_count=len(progress.turns),
            returned_model_ids=returned,
            source_commitment=ledger.source_commitment,
            store_false=store_false,
            total_outbound_evidence_bytes=ledger.total_outbound_evidence_bytes,
            usage=usage,
            transcript_fingerprint=canonical_sha256(fingerprint_payload),
        )


def folder_evidence_transcript_payload(
    artifact: FolderEvidenceLedger,
) -> dict[str, JsonValue]:
    """Return the public evidence artifact hash domain without its fingerprint."""

    payload = artifact.model_dump(mode="json", exclude={"transcript_fingerprint"})
    return payload


class FolderPathMapRow(StrictFrozenModel):
    """One complete generic source/result path and byte mapping."""

    file_id: str = Field(pattern=SHA256_PATTERN)
    original_path: str = Field(min_length=1, max_length=4_096)
    result_path: str = Field(min_length=1, max_length=1_024)
    original_size: int = Field(ge=0)
    original_sha256: str = Field(pattern=SHA256_PATTERN)
    result_size: int = Field(ge=0)
    result_sha256: str = Field(pattern=SHA256_PATTERN)
    protected: bool
    markdown_rewritten: bool

    @field_validator("original_path", "result_path")
    @classmethod
    def require_relative_posix(cls, value: str) -> str:
        return _require_relative_posix(value)


class FolderChangeEntry(StrictFrozenModel):
    """One receipt-bound explanation of an accepted file change."""

    file_id: str = Field(pattern=SHA256_PATTERN)
    original_path: str = Field(min_length=1, max_length=4_096)
    result_path: str = Field(min_length=1, max_length=1_024)
    original_size: int = Field(ge=0)
    original_sha256: str = Field(pattern=SHA256_PATTERN)
    result_size: int = Field(ge=0)
    result_sha256: str = Field(pattern=SHA256_PATTERN)
    protected: bool
    path_changed: bool
    markdown_rewritten: bool
    rewritten_reference_ids: tuple[str, ...] = ()
    original_content_path: str | None = Field(default=None, max_length=4_096)

    @model_validator(mode="after")
    def require_exact_shape(self) -> Self:
        _require_relative_posix(self.original_path)
        _require_relative_posix(self.result_path)
        if self.path_changed != (self.original_path != self.result_path):
            raise ValueError("Path-change flag does not match the mapped paths.")
        if self.protected and self.path_changed:
            raise ValueError("A protected file cannot change path.")
        if tuple(sorted(self.rewritten_reference_ids)) != self.rewritten_reference_ids:
            raise ValueError(
                "Rewritten reference IDs must be deterministically sorted."
            )
        expected_original = (
            f"name-atlas/original-content/{self.file_id}.bin"
            if self.markdown_rewritten
            else None
        )
        if self.original_content_path != expected_original:
            raise ValueError("Original-content path does not match rewrite status.")
        if self.markdown_rewritten != bool(self.rewritten_reference_ids):
            raise ValueError("Markdown rewrite status requires exact reference IDs.")
        return self


class FolderChangeLedger(StrictFrozenModel):
    """Complete deterministic file and supported-link change authority."""

    schema_version: Literal["folder-change-ledger.v1"] = "folder-change-ledger.v1"
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    reference_graph_fingerprint: str = Field(pattern=SHA256_PATTERN)
    entries: tuple[FolderChangeEntry, ...] = Field(min_length=1, max_length=500)
    file_count: int = Field(ge=1, le=500)
    source_bytes: int = Field(ge=0)
    result_bytes: int = Field(ge=0)
    path_change_count: int = Field(ge=0, le=500)
    protected_file_count: int = Field(ge=0, le=500)
    supported_link_count: int = Field(ge=0, le=10_000)
    rewritten_link_count: int = Field(ge=0, le=10_000)
    rewritten_markdown_file_count: int = Field(ge=0, le=500)

    @model_validator(mode="after")
    def require_complete_counts(self) -> Self:
        paths = tuple(entry.original_path for entry in self.entries)
        file_ids = tuple(entry.file_id for entry in self.entries)
        results = tuple(entry.result_path for entry in self.entries)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("Change-ledger entries must be source-path sorted.")
        if len(file_ids) != len(set(file_ids)) or len(results) != len(set(results)):
            raise ValueError("Change-ledger file IDs and result paths must be unique.")
        expected = {
            "file_count": len(self.entries),
            "source_bytes": sum(entry.original_size for entry in self.entries),
            "result_bytes": sum(entry.result_size for entry in self.entries),
            "path_change_count": sum(entry.path_changed for entry in self.entries),
            "protected_file_count": sum(entry.protected for entry in self.entries),
            "rewritten_link_count": sum(
                len(entry.rewritten_reference_ids) for entry in self.entries
            ),
            "rewritten_markdown_file_count": sum(
                entry.markdown_rewritten for entry in self.entries
            ),
        }
        for field_name, value in expected.items():
            if getattr(self, field_name) != value:
                raise ValueError(f"Change-ledger {field_name} is not exact.")
        if self.rewritten_link_count > self.supported_link_count:
            raise ValueError("Rewritten-link count exceeds supported-link count.")
        return self


class FolderArtifactCommitment(StrictFrozenModel):
    """Raw exact-byte receipt commitment for one authoritative tag file."""

    path: str = Field(min_length=1, max_length=4_096)
    size: int = Field(ge=0)
    sha256: str = Field(pattern=SHA256_PATTERN)

    _validate_path = field_validator("path")(_require_relative_posix)


class FolderStagedDataMember(StrictFrozenModel):
    """One regular payload member in the staged-data commitment domain."""

    path: str = Field(min_length=1, max_length=1_024)
    size: int = Field(ge=0)
    sha256: str = Field(pattern=SHA256_PATTERN)

    _validate_path = field_validator("path")(_require_relative_posix)


class FolderReceiptCore(StrictFrozenModel):
    """Immutable non-self-referential core of one generic folder receipt."""

    schema_version: Literal["folder-change-receipt.v1"] = "folder-change-receipt.v1"
    package_contract_id: Literal["name-atlas-ordinary-folder.v1"] = (
        FOLDER_PACKAGE_CONTRACT_ID
    )
    profile_id: Literal["name-atlas-cross-platform-safe.v1"] = FOLDER_NAMING_PROFILE_ID
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    source_file_count: int = Field(ge=1, le=500)
    source_directory_count: int = Field(ge=0, le=1_000)
    source_bytes: int = Field(ge=0)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    reference_graph_fingerprint: str = Field(pattern=SHA256_PATTERN)
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    provider_kind: Literal["deterministic", "live", "recorded_replay"]
    returned_model_ids: tuple[str, ...] = ()
    store_false: bool | None = None
    clarification_question: str | None = None
    clarification_answer: str | None = None
    staged_data_commitment: str = Field(pattern=SHA256_PATTERN)
    staged_data_file_count: int = Field(ge=1, le=500)
    staged_data_bytes: int = Field(ge=0)
    artifact_commitments: tuple[FolderArtifactCommitment, ...] = Field(min_length=12)
    map_row_count: int = Field(ge=1, le=500)
    path_change_count: int = Field(ge=0, le=500)
    supported_link_count: int = Field(ge=0, le=10_000)
    rewritten_link_count: int = Field(ge=0, le=10_000)
    rewritten_markdown_file_count: int = Field(ge=0, le=500)
    producer_bagit_validation: PackageValidationResult
    claim_boundaries: tuple[str, ...] = Field(min_length=1)
    proof_html_path: Literal["name-atlas/proof_and_restore.html"] = PROOF_HTML_PATH

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("job_id must be lowercase UUID4 hexadecimal text.")
        return value

    @model_validator(mode="after")
    def require_complete_acyclic_core(self) -> Self:
        paths = tuple(item.path for item in self.artifact_commitments)
        if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
            raise ValueError("Receipt artifact commitments must be path-sorted.")
        required = {
            "bag-info.txt",
            "bagit.txt",
            "manifest-sha256.txt",
            "name-atlas/accepted_plan.json",
            "name-atlas/change_ledger.json",
            "name-atlas/evidence_ledger.json",
            "name-atlas/forward_path_map.csv",
            "name-atlas/reference_graph.json",
            "name-atlas/reverse_path_map.csv",
            "name-atlas/source_snapshot.json",
            "name-atlas/user_request.json",
            "name-atlas/verification_report.json",
        }
        if not required.issubset(set(paths)):
            raise ValueError("Receipt omits a required authoritative artifact.")
        allowed = required | {
            path
            for path in paths
            if path.startswith("name-atlas/original-content/")
            and path.endswith(".bin")
            and re.fullmatch(r"[a-f0-9]{64}", Path(path).stem) is not None
        }
        if set(paths) != allowed:
            raise ValueError("Receipt commits an unsupported or circular artifact.")
        excluded = {
            RECEIPT_JSON_PATH,
            PROOF_HTML_PATH,
            "tagmanifest-sha256.txt",
        }
        if set(paths) & excluded:
            raise ValueError("Receipt commitment graph contains a circular edge.")
        if not self.producer_bagit_validation.valid:
            raise ValueError("A completed receipt requires producer BagIt success.")
        if self.claim_boundaries != RECEIPT_CLAIM_BOUNDARIES:
            raise ValueError("Receipt claim boundaries differ from the contract.")
        if self.map_row_count != self.source_file_count:
            raise ValueError("Receipt map count must equal source file count.")
        if self.staged_data_file_count != self.source_file_count:
            raise ValueError("Receipt staged-data count must equal source file count.")
        if self.path_change_count > self.map_row_count:
            raise ValueError("Receipt path-change count exceeds map rows.")
        if self.rewritten_link_count > self.supported_link_count:
            raise ValueError("Receipt rewritten-link count exceeds supported links.")
        if (self.clarification_question is None) != (self.clarification_answer is None):
            raise ValueError("Receipt clarification fields must appear together.")
        if self.provider_kind == "live":
            if self.store_false is not True or not self.returned_model_ids:
                raise ValueError("A live receipt requires store=false and model IDs.")
        elif self.store_false is not None:
            raise ValueError("Only a live receipt records an API store setting.")
        return self


class FolderReceiptEnvelope(StrictFrozenModel):
    """Machine receipt whose fingerprint is outside its own hash domain."""

    receipt: FolderReceiptCore
    receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_fingerprint(self) -> Self:
        if folder_receipt_fingerprint(self.receipt) != self.receipt_fingerprint:
            raise ValueError("Receipt fingerprint does not match ReceiptCore.")
        return self


def canonical_folder_receipt_core_bytes(core: FolderReceiptCore) -> bytes:
    """Return exact compact JSON bytes for the non-self-referential core."""

    return canonical_json_bytes(core.model_dump(mode="json", exclude_none=False))


def folder_receipt_fingerprint(core: FolderReceiptCore) -> str:
    """Return lowercase SHA-256 over the canonical receipt core bytes."""

    return hashlib.sha256(canonical_folder_receipt_core_bytes(core)).hexdigest()


def build_folder_receipt_envelope(core: FolderReceiptCore) -> FolderReceiptEnvelope:
    """Create the one self-validating receipt envelope."""

    return FolderReceiptEnvelope(
        receipt=core,
        receipt_fingerprint=folder_receipt_fingerprint(core),
    )


class FolderReceiptVerificationStatus(StrEnum):
    """Independent receiver-verification outcome."""

    VERIFIED = "verified"
    BLOCKED = "blocked"


class FolderReceiptVerificationCheck(StrictFrozenModel):
    """One stable receiver check and its concise evidence."""

    check_id: str = Field(pattern=r"^[a-z0-9_:-]{1,160}$")
    passed: bool
    detail: str = Field(min_length=1, max_length=2_000)


class FolderReceiptVerification(StrictFrozenModel):
    """Write-free `folder-receipt-verification.v1` result contract."""

    schema_version: Literal["folder-receipt-verification.v1"] = (
        "folder-receipt-verification.v1"
    )
    status: FolderReceiptVerificationStatus
    job_id: str | None = Field(default=None, pattern=r"^[a-f0-9]{32}$")
    receipt_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)
    checks: tuple[FolderReceiptVerificationCheck, ...] = Field(min_length=1)
    failed_check_ids: tuple[str, ...] = ()

    @field_validator("job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str | None) -> str | None:
        if value is None:
            return None
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("job_id must be lowercase UUID4 hexadecimal text.")
        return value

    @model_validator(mode="after")
    def require_status_agreement(self) -> Self:
        actual_failed = tuple(
            check.check_id for check in self.checks if not check.passed
        )
        if self.failed_check_ids != actual_failed:
            raise ValueError("Failed-check IDs do not match receiver checks.")
        if self.status is FolderReceiptVerificationStatus.VERIFIED:
            if (
                self.job_id is None
                or self.receipt_fingerprint is None
                or self.failed_check_ids
            ):
                raise ValueError(
                    "Verified receiver result requires a job ID and fingerprint only."
                )
        elif not self.failed_check_ids:
            raise ValueError("Blocked receiver result requires at least one failure.")
        return self


class FolderRestoreCheck(StrictFrozenModel):
    """One exact reconstruction proof fact."""

    check_id: str = Field(pattern=r"^[a-z0-9_:-]{1,160}$")
    passed: Literal[True] = True
    detail: str = Field(min_length=1, max_length=2_000)


class FolderRestoreReport(StrictFrozenModel):
    """Local result returned after exact original-layout reconstruction."""

    schema_version: Literal["folder-restore-report.v1"] = "folder-restore-report.v1"
    receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    destination: Path
    completed_at: datetime
    restored_file_count: int = Field(ge=1, le=500)
    restored_bytes: int = Field(ge=0)
    restored_empty_directory_count: int = Field(ge=0, le=1_000)
    checks: tuple[FolderRestoreCheck, ...] = Field(min_length=1)

    @field_validator("destination")
    @classmethod
    def require_absolute_destination(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("Restore destination must be an absolute local path.")
        return value

    @field_validator("completed_at")
    @classmethod
    def require_oslo_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Restore completion time must be timezone-aware.")
        oslo_value = value.astimezone(oslo_tz)
        if value.utcoffset() != oslo_value.utcoffset():
            raise ValueError("Restore completion time must use Europe/Oslo offset.")
        return value
