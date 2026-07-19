"""Strict portable contracts for path-independent Connected Change files."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV2,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    GptPlannedExecutionOriginV2,
)
from name_atlas.folder_refactor.naming import (
    validate_complete_target_tree,
    validate_result_folder_name,
    validate_target_path,
)
from name_atlas.folder_refactor.serialization import canonical_sha256

SHA256_PATTERN = r"^[a-f0-9]{64}$"
MAX_CHANGE_FILE_BYTES = 16 * 1024 * 1024
MATCHING_RULE_VERSION = "name-atlas-partition-refinement.v1"

CONNECTED_CHANGE_CLAIMS = (
    "no_project_payload_bytes_transferred",
    "receiver_application_requires_no_gpt_or_api_key",
    "supported_equivalent_projects_only",
)
CONNECTED_CHANGE_LIMITATIONS = (
    "project_names_structure_sizes_hashes_links_instruction_and_proof_are_disclosed",
    "not_sender_authentication_or_historical_authenticity",
    "ambiguous_or_changed_projects_block_instead_of_being_guessed",
)


class ConnectedChangeError(ValueError):
    """One stable fail-closed Connected Change blocker."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class StrictFrozenConnectedModel(BaseModel):
    """Immutable strict base for every Connected Change contract."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class ConnectedChangeLinkSlot(StrictFrozenConnectedModel):
    """One ordered supported Markdown relationship without destination bytes."""

    slot_index: int = Field(ge=0, le=9_999)
    is_image: bool
    syntax_class: Literal["angle", "token"]
    fragment: str | None
    target_logical_member_id: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_fragment_shape(self) -> Self:
        if self.fragment is not None and not self.fragment.startswith("#"):
            raise ValueError("A Markdown fragment must retain its leading '#'.")
        return self


class ConnectedChangeMember(StrictFrozenConnectedModel):
    """One payload-free logical member and its accepted result role."""

    logical_member_id: str = Field(pattern=SHA256_PATTERN)
    descriptor_kind: Literal["ordinary", "markdown"]
    origin_relative_path: str = Field(min_length=1, max_length=4_096)
    target_relative_path: str = Field(min_length=1, max_length=1_024)
    protected_suffix: str = Field(max_length=255)
    protected: bool
    byte_size: int | None = Field(default=None, ge=0)
    payload_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    markdown_non_destination_sha256: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    link_slots: tuple[ConnectedChangeLinkSlot, ...] = ()

    @model_validator(mode="after")
    def require_descriptor_shape(self) -> Self:
        _require_relative_posix(self.origin_relative_path, label="Origin path")
        _require_relative_posix(self.target_relative_path, label="Target path")
        validate_target_path(
            self.target_relative_path,
            original_path=self.origin_relative_path,
            protected=self.protected,
        )
        if self.descriptor_kind == "ordinary":
            if self.byte_size is None or self.payload_sha256 is None:
                raise ValueError("An ordinary descriptor requires size and SHA-256.")
            if self.markdown_non_destination_sha256 is not None or self.link_slots:
                raise ValueError("An ordinary descriptor cannot carry Markdown data.")
        else:
            if self.protected:
                raise ValueError("Protected files use exact ordinary descriptors.")
            if self.byte_size is not None or self.payload_sha256 is not None:
                raise ValueError("A Markdown descriptor cannot carry payload identity.")
            if self.markdown_non_destination_sha256 is None:
                raise ValueError(
                    "A Markdown descriptor requires its non-destination commitment."
                )
            indices = tuple(slot.slot_index for slot in self.link_slots)
            if indices != tuple(range(len(self.link_slots))):
                raise ValueError("Markdown link slots must be contiguous and ordered.")
        if self.protected and self.origin_relative_path != self.target_relative_path:
            raise ValueError("A protected member must retain its exact relative path.")
        if self.logical_member_id != connected_change_member_id(self):
            raise ValueError("Logical member ID does not match its immutable role.")
        return self


class ConnectedChangeCore(StrictFrozenConnectedModel):
    """Immutable payload-free instruction and logical project description."""

    schema_version: Literal["connected-change-core.v1"] = "connected-change-core.v1"
    matching_rule_version: Literal["name-atlas-partition-refinement.v1"] = (
        MATCHING_RULE_VERSION
    )
    request: str = Field(min_length=1, max_length=20_000)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    requested_result_folder_name: str = Field(min_length=1, max_length=240)
    origin_source_commitment: str = Field(pattern=SHA256_PATTERN)
    members: tuple[ConnectedChangeMember, ...] = Field(min_length=1, max_length=500)
    empty_directory_requirements: tuple[str, ...] = ()
    expected_file_count: int = Field(ge=1, le=500)
    expected_empty_directory_count: int = Field(ge=0, le=1_000)
    expected_supported_link_count: int = Field(ge=0, le=10_000)
    expected_organized_tree_commitment: str = Field(pattern=SHA256_PATTERN)
    origin_proof_identifiers: tuple[str, ...] = ()
    claims: tuple[str, ...] = CONNECTED_CHANGE_CLAIMS
    limitations: tuple[str, ...] = CONNECTED_CHANGE_LIMITATIONS

    @model_validator(mode="after")
    def require_complete_core(self) -> Self:
        from name_atlas.folder_refactor.serialization import request_fingerprint

        if self.request != self.request.strip():
            raise ValueError("The exact request must be nonempty and trimmed.")
        if self.request_fingerprint != request_fingerprint(self.request):
            raise ValueError("Request fingerprint does not match the exact request.")
        validate_result_folder_name(self.requested_result_folder_name)
        member_ids = tuple(member.logical_member_id for member in self.members)
        if member_ids != tuple(sorted(member_ids)) or len(member_ids) != len(
            set(member_ids)
        ):
            raise ValueError("Connected Change members must be ID-sorted and unique.")
        origins = tuple(member.origin_relative_path for member in self.members)
        targets = tuple(member.target_relative_path for member in self.members)
        if len(origins) != len(set(origins)) or len(targets) != len(set(targets)):
            raise ValueError("Origin and accepted target paths must be unique.")
        if self.expected_file_count != len(self.members):
            raise ValueError("Expected file count does not match logical members.")
        empty = self.empty_directory_requirements
        if empty != tuple(sorted(empty)) or len(empty) != len(set(empty)):
            raise ValueError("Empty-directory requirements must be sorted and unique.")
        for path in empty:
            _require_relative_posix(path, label="Empty-directory path")
            validate_target_path(path, original_path=path, protected=True)
        if self.expected_empty_directory_count != len(empty):
            raise ValueError("Expected empty-directory count is not exact.")
        expected_links = sum(len(member.link_slots) for member in self.members)
        if self.expected_supported_link_count != expected_links:
            raise ValueError("Expected supported-link count is not exact.")
        known = set(member_ids)
        if any(
            slot.target_logical_member_id not in known
            for member in self.members
            for slot in member.link_slots
        ):
            raise ValueError("A Markdown link targets an unknown logical member.")
        validate_complete_target_tree(list(targets), list(empty))
        if self.claims != CONNECTED_CHANGE_CLAIMS:
            raise ValueError("Connected Change claims differ from the frozen contract.")
        if self.limitations != CONNECTED_CHANGE_LIMITATIONS:
            raise ValueError(
                "Connected Change limitations differ from the frozen contract."
            )
        if tuple(
            sorted(self.origin_proof_identifiers)
        ) != self.origin_proof_identifiers or len(self.origin_proof_identifiers) != len(
            set(self.origin_proof_identifiers)
        ):
            raise ValueError("Origin proof identifiers must be sorted and unique.")
        if any(
            not identifier
            or len(identifier.encode("utf-8")) > 512
            or "\x00" in identifier
            for identifier in self.origin_proof_identifiers
        ):
            raise ValueError("Origin proof identifiers must be bounded UTF-8 text.")
        return self


class ConnectedChangeFile(StrictFrozenConnectedModel):
    """Transferable envelope whose fingerprint excludes itself."""

    schema_version: Literal["connected-change-file.v1"] = "connected-change-file.v1"
    core: ConnectedChangeCore
    core_fingerprint: str = Field(pattern=SHA256_PATTERN)
    originating_receipt: FolderReceiptEnvelopeV2
    change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_acyclic_fingerprints(self) -> Self:
        if self.core_fingerprint != connected_change_core_fingerprint(self.core):
            raise ValueError("Connected Change Core fingerprint mismatch.")
        receipt_core = self.originating_receipt.receipt
        if receipt_core.execution_role != "origin":
            raise ValueError("Originating receipt must declare the origin role.")
        if receipt_core.connected_change_core_fingerprint != self.core_fingerprint:
            raise ValueError("Originating receipt does not commit this Core.")
        if self.change_file_fingerprint != connected_change_file_fingerprint(self):
            raise ValueError("Connected Change File fingerprint mismatch.")
        return self


class ConnectedChangeMatchMapping(StrictFrozenConnectedModel):
    """One deterministic logical-role to receiver-file mapping."""

    logical_member_id: str = Field(pattern=SHA256_PATTERN)
    receiver_file_id: str = Field(pattern=SHA256_PATTERN)
    receiver_original_path: str = Field(min_length=1, max_length=4_096)
    target_relative_path: str = Field(min_length=1, max_length=1_024)

    @model_validator(mode="after")
    def require_paths(self) -> Self:
        _require_relative_posix(self.receiver_original_path, label="Receiver path")
        _require_relative_posix(self.target_relative_path, label="Target path")
        return self


class ConnectedChangeMatchReport(StrictFrozenConnectedModel):
    """Deterministic receiver match result and its non-self fingerprint."""

    schema_version: Literal["connected-change-match-report.v1"] = (
        "connected-change-match-report.v1"
    )
    status: Literal["matched", "blocked"]
    core_fingerprint: str = Field(pattern=SHA256_PATTERN)
    receiver_source_commitment: str = Field(pattern=SHA256_PATTERN)
    refinement_rounds: int = Field(ge=0, le=500)
    mappings: tuple[ConnectedChangeMatchMapping, ...] = ()
    blocker_code: str | None = Field(default=None, pattern=r"^[a-z0-9_:-]{1,128}$")
    detail: str = Field(min_length=1, max_length=2_000)
    match_report_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_status_shape(self) -> Self:
        logical_ids = tuple(mapping.logical_member_id for mapping in self.mappings)
        if logical_ids != tuple(sorted(logical_ids)) or len(logical_ids) != len(
            set(logical_ids)
        ):
            raise ValueError("Match mappings must be logical-ID sorted and unique.")
        receiver_ids = tuple(mapping.receiver_file_id for mapping in self.mappings)
        if len(receiver_ids) != len(set(receiver_ids)):
            raise ValueError("A receiver file cannot satisfy two logical members.")
        if self.status == "matched":
            if self.blocker_code is not None or not self.mappings:
                raise ValueError("A matched report requires mappings and no blocker.")
        elif self.blocker_code is None or self.mappings:
            raise ValueError("A blocked report requires one blocker and no mappings.")
        if self.match_report_fingerprint != connected_change_match_report_fingerprint(
            self
        ):
            raise ValueError("Connected Change match-report fingerprint mismatch.")
        return self


class GptPlannedExecutionOrigin(StrictFrozenConnectedModel):
    """Truthful observable authority for an origin planned with GPT or replay."""

    schema_version: Literal["folder-execution-origin.v1"] = "folder-execution-origin.v1"
    kind: Literal["gpt_planned"] = "gpt_planned"
    planner_kind: Literal["live", "deterministic_development", "recorded_replay"]
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    returned_model_id: str | None = None
    observable_transcript: tuple[JsonValue, ...]
    clarification_question: str | None = None
    clarification_answer: str | None = None
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    provider_call_count: int = Field(ge=0, le=8)
    api_used: bool
    store_false: bool | None = None
    external_network_used: bool

    @model_validator(mode="after")
    def require_truthful_planner_origin(self) -> Self:
        if (self.clarification_question is None) != (self.clarification_answer is None):
            raise ValueError("Clarification question and answer must appear together.")
        if self.planner_kind == "live":
            if (
                not self.api_used
                or not self.external_network_used
                or self.store_false is not True
                or self.returned_model_id is None
                or self.provider_call_count < 1
            ):
                raise ValueError("A live origin requires truthful API metadata.")
        elif (
            self.api_used or self.external_network_used or self.store_false is not None
        ):
            raise ValueError("A non-live origin cannot claim live API behavior.")
        return self


class CapsuleAppliedExecutionOrigin(StrictFrozenConnectedModel):
    """Truthful keyless and provider-free receiver execution authority."""

    schema_version: Literal["folder-execution-origin.v1"] = "folder-execution-origin.v1"
    kind: Literal["capsule_applied"] = "capsule_applied"
    change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)
    originating_receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    match_report_fingerprint: str = Field(pattern=SHA256_PATTERN)
    receiver_accepted_plan_fingerprint: str = Field(pattern=SHA256_PATTERN)
    provider_call_count: Literal[0] = 0
    api_used: Literal[False] = False
    external_network_used: Literal[False] = False


GptExecutionOrigin = GptPlannedExecutionOrigin | GptPlannedExecutionOriginV2
FolderExecutionOrigin = (
    GptPlannedExecutionOrigin
    | GptPlannedExecutionOriginV2
    | CapsuleAppliedExecutionOrigin
)


def connected_change_member_id(member: ConnectedChangeMember) -> str:
    """Return the opaque logical role ID without using an origin path."""

    intrinsic = (
        {
            "byte_size": member.byte_size,
            "payload_sha256": member.payload_sha256,
        }
        if member.descriptor_kind == "ordinary"
        else {
            "markdown_non_destination_sha256": (member.markdown_non_destination_sha256)
        }
    )
    return canonical_sha256(
        {
            "domain": "name-atlas:connected-change-member-id:v1",
            "descriptor_kind": member.descriptor_kind,
            "intrinsic": intrinsic,
            "member_kind": "regular_file",
            "protected": member.protected,
            "protected_suffix": member.protected_suffix,
            "target_relative_path": member.target_relative_path,
        }
    )


def connected_change_core_fingerprint(core: ConnectedChangeCore) -> str:
    """Return the canonical immutable Core fingerprint."""

    return canonical_sha256(core)


def connected_change_file_fingerprint(change_file: ConnectedChangeFile) -> str:
    """Hash the envelope while excluding its own fingerprint field."""

    payload = change_file.model_dump(
        mode="json",
        exclude={"change_file_fingerprint"},
    )
    return canonical_sha256(payload)


def connected_change_match_report_fingerprint(
    report: ConnectedChangeMatchReport,
) -> str:
    """Hash a match report while excluding its own fingerprint field."""

    return canonical_sha256(
        report.model_dump(mode="json", exclude={"match_report_fingerprint"})
    )


def _require_relative_posix(value: str, *, label: str) -> None:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{label} must be valid UTF-8.") from exc
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise ValueError(f"{label} must be a relative POSIX path.")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError(f"{label} cannot contain empty or dot segments.")
    if PurePosixPath(value).as_posix() != value:
        raise ValueError(f"{label} must use normalized POSIX syntax.")
