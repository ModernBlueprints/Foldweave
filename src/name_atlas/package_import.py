"""Strict import of the supported linked-collection package contract."""

from __future__ import annotations

import csv
import hashlib
import io
import re
import unicodedata
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from name_atlas.domain import ContentRole, MemberKind
from name_atlas.source import (
    SourceError,
    SourceMember,
    SourceSnapshot,
    read_member_bytes,
    snapshot_tree,
    validate_relative_path,
)

IDENTIFIER_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")


class PackageImportError(ValueError):
    """The package does not satisfy the frozen supported input contract."""


class MetadataRow(BaseModel):
    """One metadata row with exact column order and values preserved."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    row_number: int = Field(ge=2)
    header: tuple[str, ...] = Field(min_length=2)
    values: tuple[str, ...] = Field(min_length=2)

    def value(self, column: str) -> str:
        """Return one named value from the exact ordered row."""

        return self.values[self.header.index(column)]


class NormalizationRow(BaseModel):
    """One exact no-header derivative relationship row."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    row_number: int = Field(ge=1)
    original_path: str
    access_path: str | None
    preservation_path: str | None


class ObjectFamily(BaseModel):
    """One stable original identity plus its optional declared derivatives."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    family_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    canonical_identifier: str = Field(min_length=1, max_length=64)
    original: SourceMember
    access: SourceMember | None
    preservation: SourceMember | None
    metadata_row: MetadataRow
    normalization_row_number: int | None

    @property
    def members(self) -> tuple[SourceMember, ...]:
        """Return present members in canonical role order."""

        return (
            self.original,
            *((self.access,) if self.access is not None else ()),
            *((self.preservation,) if self.preservation is not None else ()),
        )


class SourcePackage(BaseModel):
    """A fully reconciled package ready for deterministic proposals."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    root: Path
    snapshot: SourceSnapshot
    metadata_header: tuple[str, ...]
    metadata_rows: tuple[MetadataRow, ...] = Field(min_length=1)
    normalization_rows: tuple[NormalizationRow, ...]
    normalization_present: bool
    families: tuple[ObjectFamily, ...] = Field(min_length=1)

    @property
    def content_members(self) -> tuple[SourceMember, ...]:
        """Return every reciprocally accounted content object."""

        return tuple(member for family in self.families for member in family.members)


def import_package(root: Path) -> SourcePackage:
    """Import one complete package or fail before any copying occurs."""

    try:
        snapshot = snapshot_tree(root)
        members = {member.relative_path: member for member in snapshot.members}
        metadata_member = members.get("metadata/metadata.csv")
        if metadata_member is None:
            raise PackageImportError("Required metadata/metadata.csv is missing.")
        metadata_header, metadata_rows = _parse_metadata(
            read_member_bytes(snapshot.source_root, metadata_member)
        )
        normalization_member = members.get("normalization.csv")
        normalization_rows = (
            _parse_normalization(
                read_member_bytes(snapshot.source_root, normalization_member)
            )
            if normalization_member is not None
            else ()
        )
        return _reconcile(
            snapshot=snapshot,
            metadata_header=metadata_header,
            metadata_rows=metadata_rows,
            normalization_rows=normalization_rows,
            normalization_present=normalization_member is not None,
        )
    except PackageImportError:
        raise
    except SourceError as exc:
        raise PackageImportError(str(exc)) from exc


def _decode_utf8(data: bytes, *, label: str) -> str:
    if not data:
        raise PackageImportError(f"{label} is empty.")
    try:
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise PackageImportError(f"{label} is not valid UTF-8.") from exc


def _csv_rows(data: bytes, *, label: str) -> list[list[str]]:
    text = _decode_utf8(data, label=label)
    try:
        return list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        raise PackageImportError(f"{label} is malformed CSV: {exc}") from exc


def _parse_metadata(data: bytes) -> tuple[tuple[str, ...], tuple[MetadataRow, ...]]:
    rows = _csv_rows(data, label="metadata/metadata.csv")
    if not rows:
        raise PackageImportError("metadata/metadata.csv has no header.")
    header = tuple(rows[0])
    if not header or header[0] != "filename":
        raise PackageImportError("filename must be the first metadata column.")
    if any(not column for column in header) or len(header) != len(set(header)):
        raise PackageImportError("Metadata headers must be nonblank and unique.")
    if header.count("filename") != 1 or header.count("dc.identifier") != 1:
        raise PackageImportError(
            "Metadata must contain filename and exactly one dc.identifier column."
        )
    parsed: list[MetadataRow] = []
    for row_number, values in enumerate(rows[1:], start=2):
        if len(values) != len(header):
            raise PackageImportError(
                f"Metadata row {row_number} has {len(values)} fields; "
                f"expected {len(header)}."
            )
        parsed.append(
            MetadataRow(
                row_number=row_number,
                header=header,
                values=tuple(values),
            )
        )
    if not parsed:
        raise PackageImportError("metadata/metadata.csv contains no object rows.")
    return header, tuple(parsed)


def _parse_normalization(data: bytes) -> tuple[NormalizationRow, ...]:
    rows = _csv_rows(data, label="normalization.csv")
    parsed: list[NormalizationRow] = []
    for row_number, values in enumerate(rows, start=1):
        if len(values) != 3:
            raise PackageImportError(
                f"Normalization row {row_number} has {len(values)} fields; expected 3."
            )
        original, access, preservation = values
        if not original:
            raise PackageImportError(
                f"Normalization row {row_number} has a blank original path."
            )
        if not access and not preservation:
            raise PackageImportError(
                f"Normalization row {row_number} declares no derivative."
            )
        parsed.append(
            NormalizationRow(
                row_number=row_number,
                original_path=validate_relative_path(original),
                access_path=validate_relative_path(access) if access else None,
                preservation_path=(
                    validate_relative_path(preservation) if preservation else None
                ),
            )
        )
    if not parsed:
        raise PackageImportError("normalization.csv is present but empty.")
    return tuple(parsed)


def _reconcile(
    *,
    snapshot: SourceSnapshot,
    metadata_header: tuple[str, ...],
    metadata_rows: tuple[MetadataRow, ...],
    normalization_rows: tuple[NormalizationRow, ...],
    normalization_present: bool,
) -> SourcePackage:
    members = {member.relative_path: member for member in snapshot.members}
    actual_by_role = {
        role: {
            member.relative_path
            for member in snapshot.members
            if member.kind is MemberKind.CONTENT_OBJECT and member.role is role
        }
        for role in ContentRole
    }

    metadata_by_original: dict[str, MetadataRow] = {}
    identifiers: set[str] = set()
    for row in metadata_rows:
        original_path = validate_relative_path(row.value("filename"))
        if not original_path.startswith("objects/"):
            raise PackageImportError(
                f"Metadata row {row.row_number} filename must begin with objects/."
            )
        if original_path in metadata_by_original:
            raise PackageImportError(f"Duplicate original reference: {original_path}")
        identifier = row.value("dc.identifier")
        if (
            IDENTIFIER_PATTERN.fullmatch(identifier) is None
            or unicodedata.normalize("NFC", identifier) != identifier
        ):
            raise PackageImportError(
                f"Invalid dc.identifier at metadata row {row.row_number}: "
                f"{identifier!r}"
            )
        if identifier in identifiers:
            raise PackageImportError(f"Duplicate dc.identifier: {identifier}")
        identifiers.add(identifier)
        metadata_by_original[original_path] = row

    if set(metadata_by_original) != actual_by_role[ContentRole.ORIGINAL]:
        missing = sorted(
            actual_by_role[ContentRole.ORIGINAL] - set(metadata_by_original)
        )
        orphaned = sorted(
            set(metadata_by_original) - actual_by_role[ContentRole.ORIGINAL]
        )
        raise PackageImportError(
            "Metadata/original accounting mismatch; "
            f"unreferenced={missing}, unresolved={orphaned}."
        )

    normalization_by_original: dict[str, NormalizationRow] = {}
    seen_derivatives: dict[ContentRole, set[str]] = {
        ContentRole.ACCESS: set(),
        ContentRole.PRESERVATION: set(),
    }
    if not normalization_present and any(
        actual_by_role[role] for role in seen_derivatives
    ):
        raise PackageImportError(
            "normalization.csv is required when derivative roots contain files."
        )
    for row in normalization_rows:
        if row.original_path not in metadata_by_original:
            raise PackageImportError(
                f"Normalization row {row.row_number} references unknown original: "
                f"{row.original_path}"
            )
        if row.original_path in normalization_by_original:
            raise PackageImportError(
                f"Original has more than one normalization row: {row.original_path}"
            )
        for role, path, prefix in (
            (ContentRole.ACCESS, row.access_path, "manualNormalization/access/"),
            (
                ContentRole.PRESERVATION,
                row.preservation_path,
                "manualNormalization/preservation/",
            ),
        ):
            if path is None:
                continue
            if not path.startswith(prefix):
                raise PackageImportError(
                    f"Normalization row {row.row_number} has {role.value} path "
                    f"outside {prefix}: {path}"
                )
            if path in seen_derivatives[role]:
                raise PackageImportError(
                    f"Derivative belongs to more than one family: {path}"
                )
            if path not in actual_by_role[role]:
                raise PackageImportError(
                    f"Normalization row {row.row_number} references missing "
                    f"{role.value}: {path}"
                )
            seen_derivatives[role].add(path)
        normalization_by_original[row.original_path] = row

    for role in (ContentRole.ACCESS, ContentRole.PRESERVATION):
        if seen_derivatives[role] != actual_by_role[role]:
            orphaned = sorted(actual_by_role[role] - seen_derivatives[role])
            missing = sorted(seen_derivatives[role] - actual_by_role[role])
            raise PackageImportError(
                f"{role.value.title()} derivative accounting mismatch; "
                f"unreferenced={orphaned}, unresolved={missing}."
            )
    families: list[ObjectFamily] = []
    for original_path, row in metadata_by_original.items():
        identifier = row.value("dc.identifier")
        normalization = normalization_by_original.get(original_path)
        family_id = hashlib.sha256(
            f"family\0{identifier}\0{original_path}".encode()
        ).hexdigest()
        families.append(
            ObjectFamily(
                family_id=family_id,
                canonical_identifier=identifier,
                original=members[original_path],
                access=(
                    members[normalization.access_path]
                    if normalization is not None and normalization.access_path
                    else None
                ),
                preservation=(
                    members[normalization.preservation_path]
                    if normalization is not None and normalization.preservation_path
                    else None
                ),
                metadata_row=row,
                normalization_row_number=(
                    normalization.row_number if normalization is not None else None
                ),
            )
        )
    families.sort(key=lambda family: family.metadata_row.row_number)
    return SourcePackage(
        root=snapshot.source_root,
        snapshot=snapshot,
        metadata_header=metadata_header,
        metadata_rows=metadata_rows,
        normalization_rows=normalization_rows,
        normalization_present=normalization_present,
        families=tuple(families),
    )
