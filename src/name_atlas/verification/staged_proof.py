"""Independent read-back proof for staged controls and logical path maps."""

from __future__ import annotations

import csv
import hashlib
import io
import os
import stat
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from name_atlas.artifacts import (
    ArtifactReadError,
    ControlFileProof,
    PathMapRow,
    VerificationCheck,
    canonical_json_bytes,
    parse_path_map,
)
from name_atlas.decisions import HumanDecision
from name_atlas.domain import ContentRole
from name_atlas.package_import import SourcePackage
from name_atlas.proposals import DESCRIPTOR_PATTERN, EXTENSION_PATTERN
from name_atlas.source import HASH_CHUNK_SIZE, SourceMember, validate_relative_path


class StagedProofError(RuntimeError):
    """A staged proof artifact cannot be safely inspected."""


@dataclass(frozen=True)
class ControlVerification:
    """Verification derived from the actual staged control-file bytes."""

    proofs: tuple[ControlFileProof, ...]
    semantics_preserved: bool
    references_resolve: bool
    metadata_references: tuple[str, ...]
    normalization_references: tuple[tuple[str, str, str], ...]


@dataclass(frozen=True)
class DeterministicProof:
    """Deterministic checks and control proofs derived from staged artifacts."""

    control_files: tuple[ControlFileProof, ...]
    checks: tuple[VerificationCheck, ...]


def verify_staged_artifacts(
    package: SourcePackage,
    maps: tuple[PathMapRow, ...],
    decisions: dict[str, HumanDecision],
    *,
    pending_root: Path,
) -> DeterministicProof:
    """Read staged artifacts back and derive every deterministic proof check."""

    staged_hashes_match = all(
        _stream_sha256(pending_root / "data" / row.target_path) == row.sha256
        for row in maps
    )
    target_paths = tuple(row.target_path for row in maps)
    expected_data_members = {
        *(row.target_path for row in maps),
        "metadata/metadata.csv",
        *({"normalization.csv"} if package.normalization_present else set()),
    }
    try:
        actual_data_members = _enumerate_regular_members(pending_root / "data")
        data_members_exact = actual_data_members == expected_data_members
        data_members_detail = (
            f"Accounted for exactly {len(actual_data_members)} staged data files."
            if data_members_exact
            else (
                "Staged data members differ from the mapped content objects and "
                "declared control files."
            )
        )
    except StagedProofError as exc:
        data_members_exact = False
        data_members_detail = str(exc)

    ordered_decisions = tuple(
        decisions[family.family_id] for family in package.families
    )
    expected_ledger = {
        "schema_version": "decision-ledger.v1",
        "decisions": [
            decision.model_dump(mode="json") for decision in ordered_decisions
        ],
    }
    try:
        source_snapshot_exact = _read_regular_bytes(
            pending_root / "name-atlas" / "source_snapshot.json",
            label="Staged source snapshot artifact",
        ) == canonical_json_bytes(package.snapshot)
        decision_ledger_exact = _read_regular_bytes(
            pending_root / "name-atlas" / "decision_ledger.json",
            label="Staged decision ledger artifact",
        ) == canonical_json_bytes(expected_ledger)
        state_artifacts_exact = source_snapshot_exact and decision_ledger_exact
        state_artifacts_detail = (
            "Canonical source snapshot and ordered decision ledger match the "
            "transaction state."
            if state_artifacts_exact
            else "Source snapshot or decision ledger differs from transaction state."
        )
    except StagedProofError as exc:
        state_artifacts_exact = False
        state_artifacts_detail = str(exc)
    map_error: str | None = None
    try:
        forward_rows = parse_path_map(
            _read_regular_bytes(
                pending_root / "name-atlas" / "forward_path_map.csv",
                label="Staged forward path map",
            ),
            reverse=False,
        )
        reverse_rows = parse_path_map(
            _read_regular_bytes(
                pending_root / "name-atlas" / "reverse_path_map.csv",
                label="Staged reverse path map",
            ),
            reverse=True,
        )
    except (ArtifactReadError, StagedProofError) as exc:
        forward_rows = ()
        reverse_rows = ()
        map_error = str(exc)
    maps_are_exact_inverses = (
        map_error is None
        and forward_rows == maps
        and reverse_rows == maps
        and forward_rows == reverse_rows
        and len({row.source_path for row in forward_rows}) == len(forward_rows)
        and len({row.target_path for row in forward_rows}) == len(forward_rows)
        and {row.source_path for row in forward_rows}
        == {member.relative_path for member in package.content_members}
    )
    control_verification = _verify_control_files(
        package,
        decisions,
        pending_root=pending_root,
        mapped_targets=frozenset(row.target_path for row in forward_rows),
    )
    reverse_dry_run = _reverse_dry_run(
        package,
        control_verification,
        reverse_rows,
        maps_are_exact_inverses=maps_are_exact_inverses,
    )
    checks = (
        VerificationCheck(
            check_id="source_snapshot_equal",
            label="Source snapshot unchanged before staging",
            passed=True,
            detail=package.snapshot.commitment,
        ),
        VerificationCheck(
            check_id="payload_hashes_equal",
            label="Every staged content-object hash equals its source",
            passed=staged_hashes_match,
            detail=f"{len(maps)} content objects compared by SHA-256.",
        ),
        VerificationCheck(
            check_id="data_members_accounted",
            label="Every staged data member has a declared transaction identity",
            passed=data_members_exact,
            detail=data_members_detail,
        ),
        VerificationCheck(
            check_id="state_artifacts_exact",
            label="Source snapshot and decision ledger match transaction state",
            passed=state_artifacts_exact,
            detail=state_artifacts_detail,
        ),
        VerificationCheck(
            check_id="control_file_semantics_preserved",
            label="Declared control-file semantics are preserved",
            passed=control_verification.semantics_preserved,
            detail=(
                "Actual staged UTF-8 CSV bytes retain exact headers, row and "
                "column order, and every non-path value."
            ),
        ),
        VerificationCheck(
            check_id="declared_references_resolve",
            label="Every rewritten declared reference resolves",
            passed=control_verification.references_resolve,
            detail=(
                "Actual staged metadata and normalization references map to "
                "regular staged content objects."
            ),
        ),
        VerificationCheck(
            check_id="target_profile_valid",
            label="Every target satisfies the repository-ready profile",
            passed=all(_target_profile_valid(row) for row in maps),
            detail="Identifier, descriptor, role, directory, and extension checked.",
        ),
        VerificationCheck(
            check_id="forward_reverse_inverse",
            label="Forward and reverse logical maps are complete inverses",
            passed=maps_are_exact_inverses,
            detail=(
                map_error
                or (
                    f"Strictly parsed {len(forward_rows)} forward and reverse "
                    "rows with exact schemas, order, and fields."
                )
            ),
        ),
        VerificationCheck(
            check_id="reverse_dry_run",
            label="Reverse dry run reconstructs original declared references",
            passed=reverse_dry_run,
            detail=(
                "The actual staged control references were reverse-applied through "
                "the serialized reverse map."
            ),
        ),
        VerificationCheck(
            check_id="target_uniqueness",
            label="Targets are unique under exact, NFC, and casefold comparison",
            passed=targets_are_unique(target_paths),
            detail="Three independent target comparison sets evaluated.",
        ),
    )
    return DeterministicProof(
        control_files=control_verification.proofs,
        checks=checks,
    )


def targets_are_unique(targets: tuple[str, ...]) -> bool:
    """Check exact, NFC, and NFC-casefold target uniqueness."""

    comparisons = (
        targets,
        tuple(unicodedata.normalize("NFC", target) for target in targets),
        tuple(unicodedata.normalize("NFC", target).casefold() for target in targets),
    )
    return all(len(values) == len(set(values)) for values in comparisons)


def _read_regular_bytes(path: Path, *, label: str) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor: int | None = None
    chunks: list[bytes] = []
    try:
        descriptor = os.open(path, flags)
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise StagedProofError(f"{label} is not a regular file.")
        size = 0
        while chunk := os.read(descriptor, HASH_CHUNK_SIZE):
            chunks.append(chunk)
            size += len(chunk)
        after = os.fstat(descriptor)
        identity_before = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        )
        identity_after = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        )
        if identity_before != identity_after or size != after.st_size:
            raise StagedProofError(f"{label} changed while being verified.")
    except OSError as exc:
        raise StagedProofError(f"{label} cannot be read safely.") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return b"".join(chunks)


def _parse_staged_csv(
    path: Path, *, label: str
) -> tuple[bytes, tuple[tuple[str, ...], ...]]:
    data = _read_regular_bytes(path, label=label)
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise StagedProofError(f"{label} is not valid UTF-8.") from exc
    try:
        rows = tuple(
            tuple(row) for row in csv.reader(io.StringIO(text, newline=""), strict=True)
        )
    except csv.Error as exc:
        raise StagedProofError(f"{label} is malformed CSV: {exc}") from exc
    return data, rows


def _expected_metadata_rows(
    package: SourcePackage,
    decisions: dict[str, HumanDecision],
) -> tuple[tuple[str, ...], ...]:
    family_by_row = {
        family.metadata_row.row_number: family for family in package.families
    }
    expected: list[tuple[str, ...]] = []
    for row in package.metadata_rows:
        values = list(row.values)
        family = family_by_row[row.row_number]
        values[0] = decisions[family.family_id].resolved_targets[ContentRole.ORIGINAL]
        expected.append(tuple(values))
    return tuple(expected)


def _expected_normalization_rows(
    package: SourcePackage,
    decisions: dict[str, HumanDecision],
) -> tuple[tuple[str, str, str], ...]:
    family_by_row = {
        family.normalization_row_number: family
        for family in package.families
        if family.normalization_row_number is not None
    }
    expected: list[tuple[str, str, str]] = []
    for row in package.normalization_rows:
        family = family_by_row[row.row_number]
        targets = decisions[family.family_id].resolved_targets
        expected.append(
            (
                targets[ContentRole.ORIGINAL],
                targets.get(ContentRole.ACCESS, ""),
                targets.get(ContentRole.PRESERVATION, ""),
            )
        )
    return tuple(expected)


def _verify_control_files(
    package: SourcePackage,
    decisions: dict[str, HumanDecision],
    *,
    pending_root: Path,
    mapped_targets: frozenset[str],
) -> ControlVerification:
    data_root = pending_root / "data"
    metadata_bytes, metadata_csv = _parse_staged_csv(
        data_root / "metadata" / "metadata.csv",
        label="Staged metadata/metadata.csv",
    )
    expected_metadata = _expected_metadata_rows(package, decisions)
    actual_header = metadata_csv[0] if metadata_csv else ()
    actual_metadata = metadata_csv[1:] if metadata_csv else ()
    metadata_shape = (
        actual_header == package.metadata_header
        and len(actual_metadata) == len(package.metadata_rows)
        and all(
            len(values) == len(package.metadata_header) for values in actual_metadata
        )
    )
    metadata_non_path_unchanged = metadata_shape and all(
        actual[1:] == source.values[1:]
        for actual, source in zip(
            actual_metadata,
            package.metadata_rows,
            strict=True,
        )
    )
    metadata_semantics = (
        metadata_shape
        and actual_metadata == expected_metadata
        and metadata_non_path_unchanged
    )
    metadata_references = tuple(
        values[0] for values in actual_metadata if len(values) >= 1
    )
    metadata_rewrites = tuple(
        f"row:{source.row_number}:filename"
        for actual, source in zip(
            actual_metadata,
            package.metadata_rows,
            strict=False,
        )
        if actual and actual[0] != source.values[0]
    )
    metadata_source = _member_by_path(package, "metadata/metadata.csv")
    proofs = [
        ControlFileProof(
            logical_path="metadata/metadata.csv",
            source_sha256=metadata_source.sha256,
            staged_sha256=hashlib.sha256(metadata_bytes).hexdigest(),
            rewritten_fields=metadata_rewrites,
            non_path_fields_unchanged=metadata_non_path_unchanged,
        )
    ]

    normalization_path = data_root / "normalization.csv"
    normalization_references: tuple[tuple[str, str, str], ...] = ()
    normalization_semantics = not package.normalization_present
    if package.normalization_present:
        normalization_bytes, normalization_csv = _parse_staged_csv(
            normalization_path,
            label="Staged normalization.csv",
        )
        expected_normalization = _expected_normalization_rows(package, decisions)
        normalization_shape = len(normalization_csv) == len(
            package.normalization_rows
        ) and all(len(values) == 3 for values in normalization_csv)
        normalization_references = tuple(
            (values[0], values[1], values[2])
            for values in normalization_csv
            if len(values) == 3
        )
        normalization_semantics = (
            normalization_shape and normalization_references == expected_normalization
        )
        source_values = tuple(
            (
                row.original_path,
                row.access_path or "",
                row.preservation_path or "",
            )
            for row in package.normalization_rows
        )
        field_names = ("original", "access", "preservation")
        normalization_rewrites = tuple(
            f"row:{row_number}:{field_names[column]}"
            for row_number, (actual, source) in enumerate(
                zip(normalization_references, source_values, strict=False),
                start=1,
            )
            for column in range(3)
            if actual[column] != source[column]
        )
        normalization_source = _member_by_path(package, "normalization.csv")
        proofs.append(
            ControlFileProof(
                logical_path="normalization.csv",
                source_sha256=normalization_source.sha256,
                staged_sha256=hashlib.sha256(normalization_bytes).hexdigest(),
                rewritten_fields=normalization_rewrites,
                non_path_fields_unchanged=normalization_shape,
            )
        )
    elif os.path.lexists(normalization_path):
        normalization_semantics = False

    declared_references = (
        *metadata_references,
        *(
            reference
            for row in normalization_references
            for reference in row
            if reference
        ),
    )
    references_resolve = bool(declared_references) and all(
        reference in mapped_targets
        and _staged_reference_is_regular(data_root, reference)
        for reference in declared_references
    )
    return ControlVerification(
        proofs=tuple(proofs),
        semantics_preserved=metadata_semantics and normalization_semantics,
        references_resolve=references_resolve,
        metadata_references=metadata_references,
        normalization_references=normalization_references,
    )


def _staged_reference_is_regular(data_root: Path, reference: str) -> bool:
    try:
        validate_relative_path(reference)
    except ValueError:
        return False
    current = data_root
    for segment in PurePosixPath(reference).parts:
        current = current / segment
        try:
            metadata = current.lstat()
        except OSError:
            return False
        if stat.S_ISLNK(metadata.st_mode):
            return False
    return stat.S_ISREG(metadata.st_mode)


def _reverse_dry_run(
    package: SourcePackage,
    controls: ControlVerification,
    reverse_rows: tuple[PathMapRow, ...],
    *,
    maps_are_exact_inverses: bool,
) -> bool:
    if not maps_are_exact_inverses:
        return False
    reverse_by_target = {row.target_path: row.source_path for row in reverse_rows}
    if len(reverse_by_target) != len(reverse_rows):
        return False
    reconstructed_metadata = tuple(
        reverse_by_target.get(reference) for reference in controls.metadata_references
    )
    source_metadata = tuple(row.value("filename") for row in package.metadata_rows)
    reconstructed_normalization = tuple(
        tuple(
            "" if not reference else reverse_by_target.get(reference)
            for reference in row
        )
        for row in controls.normalization_references
    )
    source_normalization = tuple(
        (
            row.original_path,
            row.access_path or "",
            row.preservation_path or "",
        )
        for row in package.normalization_rows
    )
    return (
        reconstructed_metadata == source_metadata
        and reconstructed_normalization == source_normalization
        and set(reverse_by_target.values())
        == {member.relative_path for member in package.content_members}
    )


def _target_profile_valid(row: PathMapRow) -> bool:
    expected_directory = {
        ContentRole.ORIGINAL: "objects",
        ContentRole.ACCESS: "manualNormalization/access",
        ContentRole.PRESERVATION: "manualNormalization/preservation",
    }[row.role]
    path = PurePosixPath(row.target_path)
    if path.parent.as_posix() != expected_directory:
        return False
    extension = path.suffix
    if EXTENSION_PATTERN.fullmatch(extension) is None:
        return False
    stem = path.name[: -len(extension)]
    try:
        identifier, descriptor, role = stem.split("__")
    except ValueError:
        return False
    return (
        identifier == row.canonical_identifier
        and DESCRIPTOR_PATTERN.fullmatch(descriptor) is not None
        and role == row.role.value
    )


def _member_by_path(package: SourcePackage, path: str) -> SourceMember:
    return next(
        member for member in package.snapshot.members if member.relative_path == path
    )


def _stream_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(HASH_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _enumerate_regular_members(root: Path) -> set[str]:
    """Return every regular data member without following symbolic links."""

    try:
        root_metadata = root.lstat()
    except OSError as exc:
        raise StagedProofError("Staged data root cannot be inspected.") from exc
    if not stat.S_ISDIR(root_metadata.st_mode) or stat.S_ISLNK(root_metadata.st_mode):
        raise StagedProofError("Staged data root is not an ordinary directory.")

    members: set[str] = set()
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = tuple(os.scandir(directory))
        except OSError as exc:
            raise StagedProofError("Staged data tree cannot be enumerated.") from exc
        for entry in entries:
            path = Path(entry.path)
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise StagedProofError(
                    "A staged data member cannot be inspected."
                ) from exc
            if stat.S_ISDIR(metadata.st_mode):
                pending.append(path)
            elif stat.S_ISREG(metadata.st_mode):
                relative = path.relative_to(root).as_posix()
                if relative in members:
                    raise StagedProofError("A staged data path is duplicated.")
                members.add(relative)
            else:
                raise StagedProofError(
                    "Staged data contains a symbolic link or special file."
                )
    return members
