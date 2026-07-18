"""Strict portable contracts for supported Markdown-link evidence."""

from __future__ import annotations

from collections import defaultdict
from pathlib import PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from name_atlas.folder_refactor.serialization import canonical_sha256

SHA256_PATTERN = r"^[a-f0-9]{64}$"
HEX_BYTES_PATTERN = r"^(?:[a-f0-9]{2})+$"


class StrictFrozenMarkdownModel(BaseModel):
    """Immutable fail-closed base for Markdown reference records."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


class MarkdownIgnoredCounts(StrictFrozenMarkdownModel):
    """Supported syntax that is intentionally left unchanged."""

    external_schemes: int = Field(ge=0)
    anchor_only: int = Field(ge=0)

    @property
    def total(self) -> int:
        """Return the complete ignored-link count."""

        return self.external_schemes + self.anchor_only


class MarkdownReference(StrictFrozenMarkdownModel):
    """One exact supported local-link destination span."""

    reference_id: str = Field(pattern=SHA256_PATTERN)
    source_file_id: str = Field(pattern=SHA256_PATTERN)
    source_path: str = Field(min_length=1, max_length=4_096)
    target_file_id: str = Field(pattern=SHA256_PATTERN)
    target_path: str = Field(min_length=1, max_length=4_096)
    destination_start_byte: int = Field(ge=0)
    destination_end_byte: int = Field(gt=0)
    original_destination_text: str = Field(min_length=1, max_length=8_192)
    original_destination_bytes_hex: str = Field(pattern=HEX_BYTES_PATTERN)
    fragment: str | None
    destination_style: Literal["angle", "token"]
    is_image: bool
    target_resolution: Literal["resolved"] = "resolved"
    proposed_destination: str | None = None
    verification_status: Literal["pending", "unchanged", "rewritten"] = "pending"

    @model_validator(mode="after")
    def validate_binding(self) -> MarkdownReference:
        """Bind IDs, paths, spans, bytes, and rewrite state."""

        _require_portable_path(self.source_path)
        _require_portable_path(self.target_path)
        if self.destination_end_byte <= self.destination_start_byte:
            raise ValueError("Markdown destination byte span must be nonempty.")
        original_bytes = bytes.fromhex(self.original_destination_bytes_hex)
        try:
            original_text = original_bytes.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise ValueError("Markdown destination bytes must be valid UTF-8.") from exc
        if original_text != self.original_destination_text:
            raise ValueError("Markdown destination text does not match its bytes.")
        if len(original_bytes) != (
            self.destination_end_byte - self.destination_start_byte
        ):
            raise ValueError(
                "Markdown destination span length does not match its bytes."
            )
        if self.fragment is not None and not self.fragment.startswith("#"):
            raise ValueError("Markdown fragments must retain their leading '#'.")
        expected_id = reference_fingerprint(
            source_file_id=self.source_file_id,
            target_file_id=self.target_file_id,
            destination_start_byte=self.destination_start_byte,
            destination_end_byte=self.destination_end_byte,
            original_destination_bytes_hex=self.original_destination_bytes_hex,
        )
        if self.reference_id != expected_id:
            raise ValueError("Markdown reference ID does not match its exact binding.")
        if self.verification_status == "pending":
            if self.proposed_destination is not None:
                raise ValueError(
                    "A pending reference cannot have a proposed destination."
                )
        elif self.proposed_destination is None:
            raise ValueError("A derived reference requires a proposed destination.")
        elif (
            self.verification_status == "unchanged"
            and self.proposed_destination != self.original_destination_text
        ):
            raise ValueError(
                "An unchanged reference must retain its exact destination."
            )
        elif (
            self.verification_status == "rewritten"
            and self.proposed_destination == self.original_destination_text
        ):
            raise ValueError("A rewritten reference must change its destination bytes.")
        return self


class FolderReferenceGraph(StrictFrozenMarkdownModel):
    """Complete path-neutral supported-link graph for one source inventory."""

    schema_version: Literal["folder-reference-graph.v1"] = "folder-reference-graph.v1"
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    references: tuple[MarkdownReference, ...] = ()
    ignored: MarkdownIgnoredCounts

    @model_validator(mode="after")
    def validate_graph(self) -> FolderReferenceGraph:
        """Require deterministic order, unique IDs, and disjoint spans."""

        sort_keys = [
            (reference.source_path, reference.destination_start_byte)
            for reference in self.references
        ]
        if sort_keys != sorted(sort_keys):
            raise ValueError("Markdown references must be deterministically ordered.")
        reference_ids = [reference.reference_id for reference in self.references]
        if len(reference_ids) != len(set(reference_ids)):
            raise ValueError("Markdown reference IDs must be unique.")
        by_source: dict[str, list[MarkdownReference]] = defaultdict(list)
        for reference in self.references:
            by_source[reference.source_file_id].append(reference)
        for references in by_source.values():
            prior_end = -1
            for reference in references:
                if reference.destination_start_byte < prior_end:
                    raise ValueError("Markdown destination spans cannot overlap.")
                prior_end = reference.destination_end_byte
        return self


def reference_fingerprint(
    *,
    source_file_id: str,
    target_file_id: str,
    destination_start_byte: int,
    destination_end_byte: int,
    original_destination_bytes_hex: str,
) -> str:
    """Return the stable identity of one exact source destination span."""

    return canonical_sha256(
        {
            "domain": "name-atlas:markdown-reference:v1",
            "destination_end_byte": destination_end_byte,
            "destination_start_byte": destination_start_byte,
            "original_destination_bytes_hex": original_destination_bytes_hex,
            "source_file_id": source_file_id,
            "target_file_id": target_file_id,
        }
    )


def _require_portable_path(value: str) -> None:
    if not value or value.startswith("/") or "\\" in value or "\x00" in value:
        raise ValueError("Markdown reference paths must be portable relative paths.")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value:
        raise ValueError("Markdown reference paths must use normalized POSIX syntax.")
    if any(part in {"", ".", ".."} for part in value.split("/")):
        raise ValueError("Markdown reference paths cannot contain dot segments.")
