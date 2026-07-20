"""Strict immutable authority for one Foldweave derivative child."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Literal, Self

from pydantic import Field, field_validator, model_validator

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CONNECTED_CHANGE_GENERATION,
    ConnectedChangeError,
    ConnectedChangeFile,
    ConnectedChangeFileAny,
    ConnectedChangeFileV2,
    ConnectedChangeMatchReport,
)
from name_atlas.folder_refactor.connected_change.job_v2 import ChangeFileInputBindingV2
from name_atlas.folder_refactor.connected_change.preview import FolderPlanPreviewV1
from name_atlas.folder_refactor.contracts import SHA256_PATTERN, StrictFrozenModel
from name_atlas.folder_refactor.serialization import canonical_sha256

FOLDER_DERIVATIVE_PARENT_BINDING_SCHEMA_VERSION = "folder-derivative-parent-binding.v1"
FOLDER_DERIVATIVE_CREATION_BINDING_SCHEMA_VERSION = (
    "folder-derivative-creation-binding.v1"
)

DerivativeModelTransport = Literal[
    "responses_api",
    "chatgpt_hosted",
    "codex_hosted",
    "recorded_replay",
    "deterministic_development",
]
DerivativeCreationChannel = Literal[
    "native_app",
    "browser",
    "chatgpt_hosted",
    "codex_mcp",
    "local_mcp",
    "cli",
]


class FolderDerivativeParentBindingV1(StrictFrozenModel):
    """Complete immutable receiver review from which one child is derived."""

    schema_version: Literal["folder-derivative-parent-binding.v1"] = (
        FOLDER_DERIVATIVE_PARENT_BINDING_SCHEMA_VERSION
    )
    parent_job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    parent_job_path: Path
    parent_source_root: Path
    parent_job_revision: int = Field(ge=0)
    parent_proposal_revision: int = Field(ge=0, le=2)
    parent_source_commitment: str = Field(pattern=SHA256_PATTERN)
    parent_candidate: FolderAcceptedPlanV2
    parent_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    parent_preview: FolderPlanPreviewV1
    parent_preview_fingerprint: str = Field(pattern=SHA256_PATTERN)
    change_file_binding: ChangeFileInputBindingV2
    match_report: ConnectedChangeMatchReport
    imported_change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_core_fingerprint: str = Field(pattern=SHA256_PATTERN)
    originating_receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    organized_tree_commitment: str = Field(pattern=SHA256_PATTERN)
    generation: int = Field(ge=1, le=32)
    binding_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("parent_job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("Derivative parent job ID must be lowercase UUID4 hex.")
        return value

    @field_validator("parent_job_path", "parent_source_root")
    @classmethod
    def require_canonical_absolute_path(cls, value: Path) -> Path:
        if not value.is_absolute() or value.resolve(strict=False) != value:
            raise ValueError(
                "Derivative parent paths must be canonical absolute paths."
            )
        return value

    @model_validator(mode="after")
    def require_exact_parent_review(self) -> Self:
        change_file = self.change_file_binding.change_file
        core = change_file.core
        receipt = change_file.originating_receipt
        preview = self.parent_preview
        if self.match_report.status != "matched":
            raise ValueError("A derivative parent requires a matched receiver review.")
        if not (
            self.parent_candidate_fingerprint
            == canonical_sha256(self.parent_candidate)
            == preview.compiled_candidate_fingerprint
            and self.parent_preview_fingerprint == preview.preview_fingerprint
            and preview.job_id == self.parent_job_id
            and preview.expected_job_revision == self.parent_job_revision
            and preview.proposal_revision == self.parent_proposal_revision
            and preview.proposal_basis == "imported_change_file"
            and preview.source_commitment == self.parent_source_commitment
            and self.parent_candidate.source_commitment
            == self.parent_source_commitment
            == self.match_report.receiver_source_commitment
            and self.parent_candidate.request_fingerprint == core.request_fingerprint
            and self.parent_candidate.result_folder_name
            == core.requested_result_folder_name
        ):
            raise ValueError(
                "Derivative parent candidate and preview do not identify one review."
            )
        if not (
            self.imported_change_file_fingerprint
            == change_file.change_file_fingerprint
            == preview.imported_change_file_fingerprint
            and self.imported_change_file_core_fingerprint
            == change_file.core_fingerprint
            == self.match_report.core_fingerprint
            and self.match_report.match_report_fingerprint
            == preview.match_report_fingerprint
            and preview.immediate_parent_candidate_fingerprint is None
            and self.originating_receipt_fingerprint == receipt.receipt_fingerprint
            and self.organized_tree_commitment
            == core.expected_organized_tree_commitment
            == receipt.receipt.organized_tree.commitment
        ):
            raise ValueError(
                "Derivative parent portable, match, and proof bindings disagree."
            )
        if self.generation != _next_derivative_generation(change_file):
            raise ValueError(
                "Derivative parent generation must be derived from its exact "
                "Change File."
            )
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"binding_fingerprint"})
        )
        if self.binding_fingerprint != expected:
            raise ValueError("Derivative parent binding fingerprint is invalid.")
        return self


class FolderDerivativeCreationBindingV1(StrictFrozenModel):
    """Idempotent creation request for one child before any model response."""

    schema_version: Literal["folder-derivative-creation-binding.v1"] = (
        FOLDER_DERIVATIVE_CREATION_BINDING_SCHEMA_VERSION
    )
    parent_binding_fingerprint: str = Field(pattern=SHA256_PATTERN)
    child_job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    child_job_path: Path
    source_root: Path
    output_parent: Path
    revision_instruction_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    contract_freeze_fingerprint: str = Field(pattern=SHA256_PATTERN)
    model_transport: DerivativeModelTransport
    channel: DerivativeCreationChannel
    idempotency_key_sha256: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    binding_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @field_validator("child_job_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("Derivative child job ID must be lowercase UUID4 hex.")
        return value

    @field_validator("child_job_path", "source_root", "output_parent")
    @classmethod
    def require_canonical_absolute_path(cls, value: Path) -> Path:
        if not value.is_absolute() or value.resolve(strict=False) != value:
            raise ValueError(
                "Derivative creation paths must be canonical absolute paths."
            )
        return value

    @model_validator(mode="after")
    def require_exact_creation_request(self) -> Self:
        request_payload = {
            "domain": "foldweave:derivative-child-creation-request:v1",
            "parent_binding_fingerprint": self.parent_binding_fingerprint,
            "source_root": self.source_root.as_posix(),
            "output_parent": self.output_parent.as_posix(),
            "revision_instruction_fingerprint": (self.revision_instruction_fingerprint),
            "evidence_fingerprint": self.evidence_fingerprint,
            "contract_freeze_fingerprint": self.contract_freeze_fingerprint,
            "model_transport": self.model_transport,
            "channel": self.channel,
        }
        if self.request_fingerprint != canonical_sha256(request_payload):
            raise ValueError("Derivative creation request fingerprint is invalid.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"binding_fingerprint"})
        )
        if self.binding_fingerprint != expected:
            raise ValueError("Derivative creation binding fingerprint is invalid.")
        return self


def build_derivative_parent_binding(
    *,
    parent_job_id: str,
    parent_job_path: Path,
    parent_source_root: Path,
    parent_job_revision: int,
    parent_proposal_revision: int,
    parent_source_commitment: str,
    parent_candidate: FolderAcceptedPlanV2,
    parent_preview: FolderPlanPreviewV1,
    change_file_binding: ChangeFileInputBindingV2,
    match_report: ConnectedChangeMatchReport,
    generation: int | None = None,
) -> FolderDerivativeParentBindingV1:
    """Build one self-validating immutable receiver-parent binding."""

    change_file = change_file_binding.change_file
    derived_generation = _next_derivative_generation(change_file)
    if generation is not None and generation != derived_generation:
        raise ValueError(
            "Caller-supplied derivative generation differs from the exact parent "
            "Change File."
        )
    values = {
        "parent_job_id": parent_job_id,
        "parent_job_path": parent_job_path,
        "parent_source_root": parent_source_root,
        "parent_job_revision": parent_job_revision,
        "parent_proposal_revision": parent_proposal_revision,
        "parent_source_commitment": parent_source_commitment,
        "parent_candidate": parent_candidate,
        "parent_candidate_fingerprint": canonical_sha256(parent_candidate),
        "parent_preview": parent_preview,
        "parent_preview_fingerprint": parent_preview.preview_fingerprint,
        "change_file_binding": change_file_binding,
        "match_report": match_report,
        "imported_change_file_fingerprint": change_file.change_file_fingerprint,
        "imported_change_file_core_fingerprint": change_file.core_fingerprint,
        "originating_receipt_fingerprint": (
            change_file.originating_receipt.receipt_fingerprint
        ),
        "organized_tree_commitment": (
            change_file.core.expected_organized_tree_commitment
        ),
        "generation": derived_generation,
    }
    draft = FolderDerivativeParentBindingV1.model_construct(
        **values,
        binding_fingerprint="0" * 64,
    )
    return FolderDerivativeParentBindingV1(
        **values,
        binding_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"binding_fingerprint"})
        ),
    )


def _next_derivative_generation(
    parent_change_file: ConnectedChangeFileAny,
) -> int:
    """Derive the child generation from the exact imported parent envelope."""

    if isinstance(parent_change_file, ConnectedChangeFile):
        parent_generation = 0
    elif isinstance(parent_change_file, ConnectedChangeFileV2):
        parent_generation = parent_change_file.core.lineage.generation
    else:  # pragma: no cover - strict contract typing makes this defensive only.
        raise ConnectedChangeError(
            "change_file_lineage_invalid",
            "Derivative parent must be a verified Foldweave Change File.",
        )
    generation = parent_generation + 1
    if generation > MAX_CONNECTED_CHANGE_GENERATION:
        raise ConnectedChangeError(
            "change_file_lineage_generation_exceeded",
            "A Foldweave Change File cannot exceed lineage generation "
            f"{MAX_CONNECTED_CHANGE_GENERATION}.",
        )
    return generation


def build_derivative_creation_binding(
    *,
    parent_binding: FolderDerivativeParentBindingV1,
    child_job_id: str,
    child_job_path: Path,
    source_root: Path,
    output_parent: Path,
    revision_instruction_fingerprint: str,
    evidence_fingerprint: str,
    contract_freeze_fingerprint: str,
    model_transport: DerivativeModelTransport,
    channel: DerivativeCreationChannel,
    idempotency_key_sha256: str,
) -> FolderDerivativeCreationBindingV1:
    """Build one exact idempotent child-creation binding."""

    values = {
        "parent_binding_fingerprint": parent_binding.binding_fingerprint,
        "child_job_id": child_job_id,
        "child_job_path": child_job_path,
        "source_root": source_root,
        "output_parent": output_parent,
        "revision_instruction_fingerprint": revision_instruction_fingerprint,
        "evidence_fingerprint": evidence_fingerprint,
        "contract_freeze_fingerprint": contract_freeze_fingerprint,
        "model_transport": model_transport,
        "channel": channel,
    }
    request_fingerprint = canonical_sha256(
        {
            "domain": "foldweave:derivative-child-creation-request:v1",
            "parent_binding_fingerprint": values["parent_binding_fingerprint"],
            "source_root": source_root.as_posix(),
            "output_parent": output_parent.as_posix(),
            "revision_instruction_fingerprint": revision_instruction_fingerprint,
            "evidence_fingerprint": evidence_fingerprint,
            "contract_freeze_fingerprint": contract_freeze_fingerprint,
            "model_transport": model_transport,
            "channel": channel,
        }
    )
    bound_values = {
        **values,
        "idempotency_key_sha256": idempotency_key_sha256,
        "request_fingerprint": request_fingerprint,
    }
    draft = FolderDerivativeCreationBindingV1.model_construct(
        **bound_values,
        binding_fingerprint="0" * 64,
    )
    return FolderDerivativeCreationBindingV1(
        **bound_values,
        binding_fingerprint=canonical_sha256(
            draft.model_dump(mode="json", exclude={"binding_fingerprint"})
        ),
    )
