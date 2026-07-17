"""Pure, read-only verification of one portable Name Atlas handoff."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import stat
import unicodedata
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from name_atlas.artifacts import ArtifactReadError, PathMapRow, parse_path_map
from name_atlas.domain import ContentRole
from name_atlas.ports import PackageValidator
from name_atlas.proposals import DESCRIPTOR_PATTERN, EXTENSION_PATTERN
from name_atlas.receipts import (
    CHANGE_RECEIPT_HTML_PATH,
    CHANGE_RECEIPT_PATH,
    DECISION_LEDGER_PATH,
    FORWARD_PATH_MAP_PATH,
    ORIGINAL_METADATA_PATH,
    ORIGINAL_NORMALIZATION_PATH,
    PORTABLE_SOURCE_SNAPSHOT_PATH,
    REVERSE_PATH_MAP_PATH,
    VERIFICATION_REPORT_PATH,
    DecisionLedgerV2,
    PortableSourceMember,
    PortableSourceSnapshot,
    ReceiptContractError,
    ReceiptCore,
    ReceiptEnvelope,
    StagedDataMember,
    VerificationReportV2,
    artifact_commitment,
    contains_sender_local_path,
    portable_snapshot_from_source,
    read_regular_bytes,
    receipt_fingerprint,
    staged_data_commitment,
    staged_data_members,
)
from name_atlas.source import ControlRole, snapshot_tree, validate_relative_path
from name_atlas.verification.bagit_validator import (
    BagItAdapterError,
    BagItPackageValidator,
)

_Model = TypeVar("_Model", bound=BaseModel)
_DIGEST_PATTERN = re.compile(r"[a-f0-9]{64}\Z")


class ReceiptVerificationStatus(StrEnum):
    """Receiver-facing deterministic verdict."""

    VERIFIED = "verified"
    BLOCKED = "blocked"


class ReceiptVerificationCheck(BaseModel):
    """One stable receiver check with path-neutral detail."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    check_id: str = Field(min_length=1, max_length=160)
    passed: bool
    detail: str = Field(min_length=1, max_length=1_000)


class ReceiptVerificationResult(BaseModel):
    """Non-persisted result returned by the receiver verifier."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    schema_version: str = Field(pattern=r"^receipt-verification\.v1$")
    status: ReceiptVerificationStatus
    receipt_fingerprint: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{64}$",
    )
    checks: tuple[ReceiptVerificationCheck, ...] = Field(min_length=1)
    failed_check_ids: tuple[str, ...]


class ReceiptCandidateError(ValueError):
    """The CLI input cannot be opened as a candidate handoff directory."""


def verify_receipt(
    bag_root: Path,
    *,
    source_root: Path | None = None,
    package_validator: PackageValidator | None = None,
) -> ReceiptVerificationResult:
    """Verify a finalized handoff without a case, provider, network, or writes."""

    root = _require_candidate_directory(bag_root)
    validator = package_validator or BagItPackageValidator()
    checks: list[ReceiptVerificationCheck] = []

    try:
        bagit_result = validator.validate(root)
    except BagItAdapterError:
        _record_failure(
            checks,
            "bagit_validation_error",
            "BagIt validation could not complete safely.",
        )
    else:
        if bagit_result.valid:
            _record_success(checks, "bagit_valid", "BagIt validation passed.")
        else:
            _record_failure(
                checks,
                "bagit_validation_failed",
                "BagIt fixity or completeness validation failed.",
            )

    try:
        receipt_bytes = read_regular_bytes(root, CHANGE_RECEIPT_PATH)
        receipt_value = _strict_json_object(receipt_bytes)
        if set(receipt_value) != {"receipt", "receipt_fingerprint"}:
            raise ValueError("Receipt envelope fields are not exact.")
        core_json = json.dumps(
            receipt_value["receipt"],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
        core = ReceiptCore.model_validate_json(core_json)
        fingerprint_value = receipt_value["receipt_fingerprint"]
        if (
            not isinstance(fingerprint_value, str)
            or _DIGEST_PATTERN.fullmatch(fingerprint_value) is None
        ):
            raise ValueError("Receipt fingerprint syntax is invalid.")
    except (ReceiptContractError, UnicodeError, ValueError, ValidationError):
        _record_failure(
            checks,
            "receipt_schema_invalid",
            "The machine receipt does not satisfy portable-change-receipt.v1.",
        )
        return _result(checks)

    expected_fingerprint = receipt_fingerprint(core)
    if fingerprint_value != expected_fingerprint:
        _record_failure(
            checks,
            "receipt_fingerprint_mismatch",
            "ReceiptCore canonical bytes do not match the envelope fingerprint.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    ReceiptEnvelope(receipt=core, receipt_fingerprint=fingerprint_value)
    _record_success(
        checks,
        "receipt_fingerprint_valid",
        "ReceiptCore canonical fingerprint matches.",
    )

    artifact_failures = _verify_artifact_commitments(root, core)
    if artifact_failures:
        checks.extend(artifact_failures)
        return _result(checks, fingerprint=fingerprint_value)
    _record_success(
        checks,
        "artifact_commitments_valid",
        f"All {len(core.artifact_commitments)} raw artifact digests match.",
    )

    try:
        snapshot = _parse_artifact_model(
            root,
            PORTABLE_SOURCE_SNAPSHOT_PATH,
            PortableSourceSnapshot,
        )
        ledger = _parse_artifact_model(
            root,
            DECISION_LEDGER_PATH,
            DecisionLedgerV2,
        )
        report = _parse_artifact_model(
            root,
            VERIFICATION_REPORT_PATH,
            VerificationReportV2,
        )
        forward_rows = parse_path_map(
            read_regular_bytes(root, FORWARD_PATH_MAP_PATH), reverse=False
        )
        reverse_rows = parse_path_map(
            read_regular_bytes(root, REVERSE_PATH_MAP_PATH), reverse=True
        )
    except (ArtifactReadError, ReceiptContractError, ValidationError, ValueError):
        _record_failure(
            checks,
            "portable_artifact_schema_invalid",
            "A receipt-bound portable artifact does not satisfy its exact schema.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    _record_success(
        checks,
        "portable_artifact_schemas_valid",
        "Snapshot, ledger, report, and both maps parsed strictly.",
    )

    if any(
        contains_sender_local_path(value) for value in (snapshot, ledger, report, core)
    ):
        _record_failure(
            checks,
            "portable_artifact_contains_local_path",
            "A portable machine artifact contains a sender-local absolute path.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    _record_success(
        checks,
        "portable_artifacts_path_neutral",
        "Portable machine artifacts contain no absolute path or file URI.",
    )

    try:
        data_members = staged_data_members(root)
    except ReceiptContractError:
        _record_failure(
            checks,
            "staged_data_unreadable",
            "The staged data tree is not a complete ordinary-file tree.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    if (
        staged_data_commitment(data_members) != core.staged_data_commitment
        or len(data_members) != core.staged_data_file_count
        or sum(member.size for member in data_members) != core.staged_data_bytes
    ):
        _record_failure(
            checks,
            "staged_data_commitment_mismatch",
            "The complete data/ member commitment or counts differ from the receipt.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    _record_success(
        checks,
        "staged_data_commitment_valid",
        f"Committed {len(data_members)} staged data members match.",
    )

    cross_failures = _cross_artifact_failures(
        root=root,
        core=core,
        snapshot=snapshot,
        ledger=ledger,
        report=report,
        forward_rows=forward_rows,
        reverse_rows=reverse_rows,
        data_members=data_members,
    )
    if cross_failures:
        checks.extend(cross_failures)
        return _result(checks, fingerprint=fingerprint_value)
    _record_success(
        checks,
        "transaction_consistency_valid",
        "Snapshot, controls, ledger, maps, payloads, report, and receipt agree.",
    )

    try:
        receipt_html = read_regular_bytes(root, CHANGE_RECEIPT_HTML_PATH).decode(
            "utf-8", errors="strict"
        )
    except (ReceiptContractError, UnicodeError):
        _record_failure(
            checks,
            "offline_receipt_invalid",
            "The offline receipt is missing or is not valid UTF-8.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    if (
        fingerprint_value not in receipt_html
        or core.case_id not in receipt_html
        or "portable-change-receipt.v1" not in receipt_html
    ):
        _record_failure(
            checks,
            "offline_receipt_disagrees",
            "The offline receipt omits a central machine-receipt identity.",
        )
        return _result(checks, fingerprint=fingerprint_value)
    _record_success(
        checks,
        "offline_receipt_consistent",
        "The offline view identifies the machine receipt and case.",
    )

    if source_root is not None:
        try:
            supplied = portable_snapshot_from_source(snapshot_tree(source_root))
        except (OSError, ValueError):
            _record_failure(
                checks,
                "supplied_source_unreadable",
                "The optional source cannot be compared under the package contract.",
            )
            return _result(checks, fingerprint=fingerprint_value)
        if supplied != snapshot:
            _record_failure(
                checks,
                "supplied_source_mismatch",
                "The optional source differs from the committed source description.",
            )
            return _result(checks, fingerprint=fingerprint_value)
        _record_success(
            checks,
            "supplied_source_matches",
            "The optional source exactly matches the portable snapshot.",
        )

    return _result(checks, fingerprint=fingerprint_value)


def _verify_artifact_commitments(
    root: Path, core: ReceiptCore
) -> tuple[ReceiptVerificationCheck, ...]:
    failures: list[ReceiptVerificationCheck] = []
    for expected in core.artifact_commitments:
        slug = _artifact_slug(expected.path)
        try:
            actual = artifact_commitment(root, expected.path)
        except ReceiptContractError:
            failures.append(
                ReceiptVerificationCheck(
                    check_id=f"artifact_missing_or_unreadable:{slug}",
                    passed=False,
                    detail=f"Receipt-bound artifact is unavailable: {expected.path}.",
                )
            )
            continue
        if actual != expected:
            failures.append(
                ReceiptVerificationCheck(
                    check_id=f"artifact_digest_mismatch:{slug}",
                    passed=False,
                    detail=(
                        "Raw artifact digest or size no longer equals the receipt "
                        f"commitment: {expected.path}."
                    ),
                )
            )
    return tuple(failures)


def _cross_artifact_failures(
    *,
    root: Path,
    core: ReceiptCore,
    snapshot: PortableSourceSnapshot,
    ledger: DecisionLedgerV2,
    report: VerificationReportV2,
    forward_rows: tuple[PathMapRow, ...],
    reverse_rows: tuple[PathMapRow, ...],
    data_members: tuple[StagedDataMember, ...],
) -> tuple[ReceiptVerificationCheck, ...]:
    failures: list[ReceiptVerificationCheck] = []
    content_members: dict[str, PortableSourceMember] = {
        member.relative_path: member
        for member in snapshot.members
        if member.role in set(ContentRole)
    }
    controls: dict[ControlRole, PortableSourceMember] = {
        member.role: member
        for member in snapshot.members
        if isinstance(member.role, ControlRole)
    }
    data_by_path = {member.path: member for member in data_members}
    committed_paths = {item.path for item in core.artifact_commitments}
    normalization_committed = ORIGINAL_NORMALIZATION_PATH in committed_paths
    normalization_present = ControlRole.NORMALIZATION in controls

    snapshot_consistent = (
        snapshot.commitment == core.source_snapshot_commitment
        and len(snapshot.members) == core.source_member_count
        and sum(member.size for member in snapshot.members) == core.source_bytes
        and set(controls)
        in (
            {ControlRole.METADATA},
            {ControlRole.METADATA, ControlRole.NORMALIZATION},
        )
        and normalization_committed == normalization_present
    )
    if not snapshot_consistent:
        failures.append(
            _failed(
                "source_snapshot_receipt_mismatch",
                "Portable source description and receipt summary differ.",
            )
        )

    maps_consistent = _maps_are_consistent(
        forward_rows,
        reverse_rows,
        content_members=content_members,
        data_by_path=data_by_path,
    )
    if not maps_consistent:
        failures.append(
            _failed(
                "path_maps_inconsistent",
                "Forward/reverse maps do not completely bind source and staged data.",
            )
        )

    decisions_consistent = _decisions_match_maps(ledger, forward_rows)
    if not decisions_consistent:
        failures.append(
            _failed(
                "decision_ledger_inconsistent",
                "Decision authority does not match the complete path maps.",
            )
        )

    controls_consistent = False
    if maps_consistent:
        try:
            controls_consistent = _controls_match_transaction(
                root,
                controls=controls,
                forward_rows=forward_rows,
            )
        except ReceiptContractError:
            controls_consistent = False
    if not controls_consistent:
        failures.append(
            _failed(
                "declared_controls_inconsistent",
                "Original and staged declared controls do not match the path maps.",
            )
        )

    gpt_count = sum(
        decision.meaning_review is not None for decision in ledger.decisions
    )
    receipt_counts_consistent = (
        ledger.case_id == core.case_id
        and len(forward_rows) == core.map_row_count
        and len(ledger.decisions) == core.decision_count
        and len(ledger.decisions) == core.human_decision_count
        and gpt_count == core.gpt_assisted_decision_count
    )
    if not receipt_counts_consistent:
        failures.append(
            _failed(
                "receipt_counts_inconsistent",
                "Case, map, decision, or GPT-assisted counts differ.",
            )
        )

    report_consistent = (
        report.status.value == "verified"
        and report.claim is not None
        and report.generated_at.tzinfo is not None
        and report.source_snapshot_commitment == snapshot.commitment
        and report.prestaging_snapshot_commitment == snapshot.commitment
        and report.postcopy_snapshot_commitment == snapshot.commitment
        and report.source_unchanged is True
        and report.content_object_count == len(forward_rows)
        and report.content_bytes == sum(row.size for row in forward_rows)
        and report.map_row_count == len(forward_rows)
        and all(check.passed for check in report.checks)
        and report.bagit_validation == core.producer_bagit_validation
        and not report.blockers
        and core.producer_bagit_validation.valid
        and _report_control_hashes_match(root, report, controls)
        and set(report.artifact_paths)
        == committed_paths
        | {
            CHANGE_RECEIPT_PATH,
            CHANGE_RECEIPT_HTML_PATH,
            "tagmanifest-sha256.txt",
        }
    )
    if not report_consistent:
        failures.append(
            _failed(
                "producer_report_inconsistent",
                "Producer findings disagree with recomputed receipt facts.",
            )
        )

    return tuple(failures)


def _maps_are_consistent(
    forward_rows: tuple[PathMapRow, ...],
    reverse_rows: tuple[PathMapRow, ...],
    *,
    content_members: dict[str, PortableSourceMember],
    data_by_path: dict[str, StagedDataMember],
) -> bool:
    if (
        not forward_rows
        or forward_rows != reverse_rows
        or len({row.source_path for row in forward_rows}) != len(forward_rows)
        or len({row.target_path for row in forward_rows}) != len(forward_rows)
        or set(content_members) != {row.source_path for row in forward_rows}
    ):
        return False
    targets = tuple(row.target_path for row in forward_rows)
    if not _targets_unique(targets):
        return False
    for row in forward_rows:
        source = content_members.get(row.source_path)
        target = data_by_path.get(row.target_path)
        if (
            source is None
            or target is None
            or source.role != row.role
            or source.size != row.size
            or source.sha256 != row.sha256
            or target.size != row.size
            or target.sha256 != row.sha256
            or not _target_profile_valid(row)
        ):
            return False
    control_paths = {"metadata/metadata.csv"}
    if "normalization.csv" in data_by_path:
        control_paths.add("normalization.csv")
    return set(data_by_path) == set(targets) | control_paths


def _decisions_match_maps(
    ledger: DecisionLedgerV2,
    rows: tuple[PathMapRow, ...],
) -> bool:
    rows_by_family: dict[str, dict[ContentRole, PathMapRow]] = {}
    for row in rows:
        family_rows = rows_by_family.setdefault(row.family_id, {})
        if row.role in family_rows:
            return False
        family_rows[row.role] = row
    if set(rows_by_family) != {entry.family_id for entry in ledger.decisions}:
        return False
    for entry in ledger.decisions:
        family_rows = rows_by_family[entry.family_id]
        proposals = {proposal.role: proposal for proposal in entry.initial_proposals}
        if set(proposals) != set(family_rows):
            return False
        for role, row in family_rows.items():
            proposal = proposals[role]
            if (
                proposal.original_relative_path != row.source_path
                or proposal.canonical_identifier != row.canonical_identifier
                or entry.human_decision.resolved_targets[role] != row.target_path
            ):
                return False
    return True


def _controls_match_transaction(
    root: Path,
    *,
    controls: dict[ControlRole, PortableSourceMember],
    forward_rows: tuple[PathMapRow, ...],
) -> bool:
    metadata_member = controls.get(ControlRole.METADATA)
    if metadata_member is None:
        return False
    original_metadata_bytes = read_regular_bytes(root, ORIGINAL_METADATA_PATH)
    if (
        len(original_metadata_bytes) != metadata_member.size
        or hashlib.sha256(original_metadata_bytes).hexdigest() != metadata_member.sha256
    ):
        return False
    staged_metadata_bytes = read_regular_bytes(root, "data/metadata/metadata.csv")
    original_metadata = _parse_csv(original_metadata_bytes)
    staged_metadata = _parse_csv(staged_metadata_bytes)
    if not original_metadata or not staged_metadata:
        return False
    if original_metadata[0] != staged_metadata[0]:
        return False
    if not original_metadata[0] or original_metadata[0][0] != "filename":
        return False
    if len(original_metadata) != len(staged_metadata):
        return False
    target_by_source = {row.source_path: row.target_path for row in forward_rows}
    for original_row, staged_row in zip(
        original_metadata[1:], staged_metadata[1:], strict=True
    ):
        if (
            len(original_row) != len(original_metadata[0])
            or len(staged_row) != len(staged_metadata[0])
            or staged_row[1:] != original_row[1:]
            or staged_row[0] != target_by_source.get(original_row[0])
        ):
            return False

    normalization_member = controls.get(ControlRole.NORMALIZATION)
    if normalization_member is None:
        try:
            read_regular_bytes(root, "data/normalization.csv")
        except ReceiptContractError:
            return True
        return False

    original_normalization_bytes = read_regular_bytes(root, ORIGINAL_NORMALIZATION_PATH)
    if (
        len(original_normalization_bytes) != normalization_member.size
        or hashlib.sha256(original_normalization_bytes).hexdigest()
        != normalization_member.sha256
    ):
        return False
    original_normalization = _parse_csv(original_normalization_bytes)
    staged_normalization = _parse_csv(
        read_regular_bytes(root, "data/normalization.csv")
    )
    if len(original_normalization) != len(staged_normalization):
        return False
    for original_row, staged_row in zip(
        original_normalization, staged_normalization, strict=True
    ):
        if len(original_row) != 3 or len(staged_row) != 3:
            return False
        expected = tuple(
            "" if not value else target_by_source.get(value) for value in original_row
        )
        if staged_row != expected:
            return False
    return True


def _report_control_hashes_match(
    root: Path,
    report: VerificationReportV2,
    controls: dict[ControlRole, PortableSourceMember],
) -> bool:
    proofs = {proof.logical_path: proof for proof in report.control_files}
    expected_paths = {"metadata/metadata.csv"}
    if ControlRole.NORMALIZATION in controls:
        expected_paths.add("normalization.csv")
    if set(proofs) != expected_paths:
        return False
    for role, logical_path in (
        (ControlRole.METADATA, "metadata/metadata.csv"),
        (ControlRole.NORMALIZATION, "normalization.csv"),
    ):
        member = controls.get(role)
        if member is None:
            continue
        proof = proofs[logical_path]
        try:
            staged = read_regular_bytes(root, f"data/{logical_path}")
        except ReceiptContractError:
            return False
        if (
            proof.source_sha256 != member.sha256
            or proof.staged_sha256 != hashlib.sha256(staged).hexdigest()
            or not proof.non_path_fields_unchanged
        ):
            return False
    return True


def _parse_csv(data: bytes) -> tuple[tuple[str, ...], ...]:
    try:
        text = data.decode("utf-8", errors="strict")
        return tuple(
            tuple(row) for row in csv.reader(io.StringIO(text, newline=""), strict=True)
        )
    except (UnicodeError, csv.Error) as exc:
        raise ReceiptContractError("Declared control is not strict UTF-8 CSV.") from exc


def _target_profile_valid(row: PathMapRow) -> bool:
    expected_directory = {
        ContentRole.ORIGINAL: "objects",
        ContentRole.ACCESS: "manualNormalization/access",
        ContentRole.PRESERVATION: "manualNormalization/preservation",
    }[row.role]
    try:
        validate_relative_path(row.target_path)
    except ValueError:
        return False
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


def _targets_unique(targets: tuple[str, ...]) -> bool:
    comparisons = (
        targets,
        tuple(unicodedata.normalize("NFC", target) for target in targets),
        tuple(unicodedata.normalize("NFC", target).casefold() for target in targets),
    )
    return all(len(values) == len(set(values)) for values in comparisons)


def _parse_artifact_model(
    root: Path,
    relative_path: str,
    model_type: type[_Model],
) -> _Model:
    data = read_regular_bytes(root, relative_path)
    _strict_json_object(data)
    return model_type.model_validate_json(data)


def _strict_json_object(data: bytes) -> dict[str, Any]:
    try:
        text = data.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=lambda constant: _raise_invalid_constant(constant),
        )
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Artifact is not strict JSON.") from exc
    if not isinstance(value, dict):
        raise ValueError("Artifact JSON root must be an object.")
    return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("Artifact JSON contains a duplicate object key.")
        value[key] = item
    return value


def _raise_invalid_constant(constant: str) -> None:
    raise ValueError(f"Unsupported JSON constant: {constant}")


def _require_candidate_directory(value: Path) -> Path:
    if not isinstance(value, Path):
        raise ReceiptCandidateError("Received bag must be a pathlib.Path.")
    try:
        metadata = value.lstat()
    except OSError as exc:
        raise ReceiptCandidateError("Received bag cannot be inspected.") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ReceiptCandidateError("Received bag must be a real directory.")
    try:
        return value.resolve(strict=True)
    except OSError as exc:
        raise ReceiptCandidateError("Received bag cannot be resolved.") from exc


def _artifact_slug(relative_path: str) -> str:
    names = {
        PORTABLE_SOURCE_SNAPSHOT_PATH: "source_snapshot",
        ORIGINAL_METADATA_PATH: "original_metadata",
        ORIGINAL_NORMALIZATION_PATH: "original_normalization",
        DECISION_LEDGER_PATH: "decision_ledger",
        FORWARD_PATH_MAP_PATH: "forward_path_map",
        REVERSE_PATH_MAP_PATH: "reverse_path_map",
        VERIFICATION_REPORT_PATH: "verification_report",
        "name-atlas/verification_summary.md": "verification_summary",
        "bagit.txt": "bagit",
        "bag-info.txt": "bag_info",
        "manifest-sha256.txt": "payload_manifest",
    }
    return names[relative_path]


def _record_success(
    checks: list[ReceiptVerificationCheck], check_id: str, detail: str
) -> None:
    checks.append(
        ReceiptVerificationCheck(check_id=check_id, passed=True, detail=detail)
    )


def _record_failure(
    checks: list[ReceiptVerificationCheck], check_id: str, detail: str
) -> None:
    checks.append(
        ReceiptVerificationCheck(check_id=check_id, passed=False, detail=detail)
    )


def _failed(check_id: str, detail: str) -> ReceiptVerificationCheck:
    return ReceiptVerificationCheck(check_id=check_id, passed=False, detail=detail)


def _result(
    checks: list[ReceiptVerificationCheck],
    *,
    fingerprint: str | None = None,
) -> ReceiptVerificationResult:
    failed = tuple(check.check_id for check in checks if not check.passed)
    return ReceiptVerificationResult(
        schema_version="receipt-verification.v1",
        status=(
            ReceiptVerificationStatus.BLOCKED
            if failed
            else ReceiptVerificationStatus.VERIFIED
        ),
        receipt_fingerprint=fingerprint,
        checks=tuple(checks),
        failed_check_ids=failed,
    )
