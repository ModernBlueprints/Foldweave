"""Copy-only pending staging transaction and deterministic integrity proof."""

from __future__ import annotations

import csv
import hashlib
import io
import logging
import os
import stat
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Protocol
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict

from name_atlas.artifacts import (
    ControlFileProof,
    PathMapRow,
    ProofStatus,
    StageArtifacts,
    VerificationCheck,
    VerificationReport,
    replace_verification_report,
    write_decision_ledger,
    write_path_map,
    write_source_snapshot,
    write_summary,
    write_verification_report,
)
from name_atlas.decisions import HumanAction, HumanDecision
from name_atlas.domain import ContentRole, PackageValidationResult
from name_atlas.package_import import ObjectFamily, SourcePackage, import_package
from name_atlas.proposals import (
    DESCRIPTOR_PATTERN,
    EXTENSION_PATTERN,
    build_proposals,
    edited_targets,
)
from name_atlas.source import (
    HASH_CHUNK_SIZE,
    SourceMember,
    snapshot_tree,
    validate_relative_path,
)
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.verification.promotion import promote_directory_no_replace
from name_atlas.verification.staged_proof import (
    StagedProofError,
    targets_are_unique,
    verify_staged_artifacts,
)

oslo_tz = ZoneInfo("Europe/Oslo")
VERIFIED_CLAIM = "Verified round-trip integrity within the supported package contract"
LOGGER = logging.getLogger(__name__)


class _PackageValidator(Protocol):
    def validate(self, bag_root: Path) -> PackageValidationResult:
        """Validate a completed pending package without mutating it."""


class StagingError(RuntimeError):
    """The package could not be exposed as an exportable final stage."""


class StageResult(BaseModel):
    """Completed exportable stage and its exact proof artifact model."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    stage_root: Path
    artifacts: StageArtifacts


def stage_package(
    package: SourcePackage,
    decisions: tuple[HumanDecision, ...],
    *,
    output_root: Path,
    package_validator: _PackageValidator,
) -> StageResult:
    """Create, verify, and promote one new copy-only BagIt stage."""

    decision_by_family = _validate_decisions(package, decisions)
    prestaging = import_package(package.root)
    if prestaging.snapshot != package.snapshot:
        raise StagingError("Source package changed after the initial snapshot.")

    output_candidate = output_root.resolve(strict=False)
    if output_candidate == package.root or package.root in output_candidate.parents:
        raise StagingError("Stage output must be outside the immutable source package.")
    output_root.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(oslo_tz)
    final_root, pending_root = _allocate_stage_paths(
        output_root,
        generated_at=generated_at,
        snapshot_commitment=package.snapshot.commitment,
    )
    (pending_root / "data").mkdir(parents=True)
    (pending_root / "name-atlas").mkdir()

    map_rows: list[PathMapRow] = []
    report_path = pending_root / "name-atlas" / "verification_report.json"
    current_stage = "pending_allocation"
    write_verification_report(
        report_path,
        _failure_report(
            generated_at=generated_at,
            final_root=final_root,
            package=package,
            map_rows=(),
            stage=current_stage,
            reason="Staging transaction has not completed.",
        ),
    )
    try:
        current_stage = "copy_content_objects"
        for family in package.families:
            decision = decision_by_family[family.family_id]
            for member in family.members:
                target = decision.resolved_targets[member.role]
                _copy_content_member(
                    package.root / member.relative_path,
                    pending_root / "data" / target,
                    member,
                )
                map_rows.append(
                    PathMapRow(
                        family_id=family.family_id,
                        canonical_identifier=family.canonical_identifier,
                        role=member.role,
                        source_path=member.relative_path,
                        target_path=target,
                        size=member.size,
                        sha256=member.sha256,
                    )
                )

        current_stage = "write_declared_control_files"
        _write_control_files(
            package,
            decision_by_family,
            pending_root=pending_root,
        )
        current_stage = "postcopy_source_snapshot"
        postcopy = snapshot_tree(package.root)
        if postcopy != package.snapshot:
            raise StagingError("Source package changed during copy-only staging.")

        ordered_maps = tuple(
            sorted(map_rows, key=lambda row: (row.family_id, row.role.value))
        )
        proof_root = pending_root / "name-atlas"
        artifact_paths = (
            "name-atlas/source_snapshot.json",
            "name-atlas/decision_ledger.json",
            "name-atlas/forward_path_map.csv",
            "name-atlas/reverse_path_map.csv",
            "name-atlas/verification_report.json",
            "name-atlas/verification_summary.md",
            "bagit.txt",
            "bag-info.txt",
            "manifest-sha256.txt",
            "tagmanifest-sha256.txt",
        )
        current_stage = "write_proof_artifacts"
        write_source_snapshot(proof_root / "source_snapshot.json", package.snapshot)
        ordered_decisions = tuple(
            decision_by_family[family.family_id] for family in package.families
        )
        write_decision_ledger(proof_root / "decision_ledger.json", ordered_decisions)
        write_path_map(proof_root / "forward_path_map.csv", ordered_maps, reverse=False)
        write_path_map(proof_root / "reverse_path_map.csv", ordered_maps, reverse=True)
        write_summary(
            proof_root / "verification_summary.md",
            content_objects=len(ordered_maps),
            content_bytes=sum(row.size for row in ordered_maps),
        )
        current_stage = "deterministic_verification"
        try:
            deterministic_proof = verify_staged_artifacts(
                package,
                ordered_maps,
                decision_by_family,
                pending_root=pending_root,
            )
        except StagedProofError as exc:
            raise StagingError(str(exc)) from exc
        checks = deterministic_proof.checks
        control_proofs = deterministic_proof.control_files
        if not all(check.passed for check in checks):
            raise StagingError("One or more deterministic proof checks failed.")
        provisional_validation = PackageValidationResult(
            validator="bagit",
            valid=False,
            messages=("BagIt validation has not run yet.",),
        )
        report = _report(
            status=ProofStatus.BLOCKED,
            claim=None,
            generated_at=generated_at,
            final_root=final_root,
            package=package,
            postcopy_commitment=postcopy.commitment,
            maps=ordered_maps,
            control_proofs=control_proofs,
            checks=checks,
            bagit_validation=provisional_validation,
            artifact_paths=artifact_paths,
            blockers=("BagIt validation has not run yet.",),
        )
        current_stage = "write_provisional_report"
        replace_verification_report(report_path, report)

        current_stage = "bagit_creation"
        writer = BagItWriter()
        writer.write(pending_root, bagging_date=generated_at.date())
        current_stage = "bagit_validation"
        first_validation = package_validator.validate(pending_root)
        current_stage = "post_bagit_deterministic_verification"
        try:
            final_deterministic_proof = verify_staged_artifacts(
                package,
                ordered_maps,
                decision_by_family,
                pending_root=pending_root,
            )
        except StagedProofError as exc:
            raise StagingError(str(exc)) from exc
        checks = final_deterministic_proof.checks
        control_proofs = final_deterministic_proof.control_files
        deterministic_valid = all(check.passed for check in checks)
        final_status = (
            ProofStatus.VERIFIED
            if first_validation.valid and deterministic_valid
            else ProofStatus.BLOCKED
        )
        blockers = tuple(check.label for check in checks if not check.passed) + (
            () if first_validation.valid else first_validation.messages
        )
        report = _report(
            status=final_status,
            claim=VERIFIED_CLAIM if final_status is ProofStatus.VERIFIED else None,
            generated_at=generated_at,
            final_root=final_root,
            package=package,
            postcopy_commitment=postcopy.commitment,
            maps=ordered_maps,
            control_proofs=control_proofs,
            checks=checks,
            bagit_validation=first_validation,
            artifact_paths=artifact_paths,
            blockers=blockers,
        )
        replace_verification_report(report_path, report)
        writer.refresh_tagmanifest(pending_root)
        final_validation = package_validator.validate(pending_root)
        if final_status is ProofStatus.VERIFIED and not final_validation.valid:
            report = _report(
                status=ProofStatus.BLOCKED,
                claim=None,
                generated_at=generated_at,
                final_root=final_root,
                package=package,
                postcopy_commitment=postcopy.commitment,
                maps=ordered_maps,
                control_proofs=control_proofs,
                checks=checks,
                bagit_validation=final_validation,
                artifact_paths=artifact_paths,
                blockers=final_validation.messages,
            )
            replace_verification_report(report_path, report)
            writer.refresh_tagmanifest(pending_root)
        if (
            not deterministic_valid
            or not first_validation.valid
            or not final_validation.valid
        ):
            raise StagingError(
                "Final deterministic or BagIt verification failed; preserved "
                f"pending stage at {pending_root}."
            )
        current_stage = "final_source_snapshot"
        if snapshot_tree(package.root) != package.snapshot:
            raise StagingError("Source package changed before final promotion.")
        current_stage = "final_promotion"
        try:
            promote_directory_no_replace(pending_root, final_root)
        except FileExistsError as exc:
            raise StagingError("Final stage path appeared before promotion.") from exc
        except OSError as exc:
            raise StagingError("Atomic final-stage promotion failed.") from exc
    except Exception as exc:
        _preserve_failure_report(
            report_path=report_path,
            generated_at=generated_at,
            final_root=final_root,
            package=package,
            map_rows=tuple(map_rows),
            stage=current_stage,
            error=exc,
        )
        raise

    artifacts = StageArtifacts(
        forward_map=ordered_maps,
        reverse_map=ordered_maps,
        report=report,
    )
    return StageResult(stage_root=final_root, artifacts=artifacts)


def _validate_decisions(
    package: SourcePackage,
    decisions: tuple[HumanDecision, ...],
) -> dict[str, HumanDecision]:
    decision_by_family = {decision.family_id: decision for decision in decisions}
    if len(decision_by_family) != len(decisions):
        raise StagingError("A family has duplicate decision records.")
    expected_ids = {family.family_id for family in package.families}
    if set(decision_by_family) != expected_ids:
        raise StagingError("Every family must have exactly one decision record.")
    profile_proposals = build_proposals(package.families)
    for family in package.families:
        decision = decision_by_family[family.family_id]
        expected_roles = {member.role for member in family.members}
        if (
            not decision.export_ready
            or set(decision.resolved_targets) != expected_roles
        ):
            raise StagingError(
                f"Family {family.family_id} has no complete resolved target map."
            )
        if decision.action is HumanAction.APPROVED:
            expected_targets = {
                proposal.role: proposal.proposed_relative_path
                for proposal in profile_proposals
                if proposal.family_id == family.family_id
            }
        elif decision.action is HumanAction.EDITED:
            assert decision.human_input is not None
            try:
                expected_targets = dict(edited_targets(family, decision.human_input))
            except ValueError as exc:
                raise StagingError(
                    f"Family {family.family_id} has an invalid edited decision."
                ) from exc
        else:
            raise StagingError(f"Family {family.family_id} is not approved or edited.")
        if dict(decision.resolved_targets) != expected_targets:
            raise StagingError(
                f"Family {family.family_id} decision targets do not match its "
                f"{decision.action.value} authority record."
            )
        for member in family.members:
            _validate_resolved_target(
                family,
                member,
                decision.resolved_targets[member.role],
            )
    _require_globally_unique_targets(
        tuple(
            target
            for decision in decisions
            for target in decision.resolved_targets.values()
        )
    )
    return decision_by_family


def _validate_resolved_target(
    family: ObjectFamily,
    member: SourceMember,
    target: str,
) -> None:
    try:
        validate_relative_path(target)
    except ValueError as exc:
        raise StagingError(
            f"Resolved target is not a safe relative path: {target!r}"
        ) from exc
    path = PurePosixPath(target)
    expected_directory = {
        ContentRole.ORIGINAL: "objects",
        ContentRole.ACCESS: "manualNormalization/access",
        ContentRole.PRESERVATION: "manualNormalization/preservation",
    }[member.role]
    if path.parent.as_posix() != expected_directory:
        raise StagingError(
            f"Resolved {member.role.value} target uses the wrong directory: {target}"
        )
    source_extension = PurePosixPath(member.relative_path).suffix.lower()
    if (
        path.suffix != source_extension
        or EXTENSION_PATTERN.fullmatch(path.suffix) is None
    ):
        raise StagingError(
            f"Resolved target does not retain the lowercased final extension: {target}"
        )
    stem = path.name[: -len(path.suffix)]
    try:
        identifier, descriptor, role = stem.split("__")
    except ValueError as exc:
        raise StagingError(
            f"Resolved target does not match the fixed profile: {target}"
        ) from exc
    if (
        identifier != family.canonical_identifier
        or DESCRIPTOR_PATTERN.fullmatch(descriptor) is None
        or role != member.role.value
    ):
        raise StagingError(
            f"Resolved target does not match the fixed profile: {target}"
        )


def _allocate_stage_paths(
    output_root: Path,
    *,
    generated_at: datetime,
    snapshot_commitment: str,
) -> tuple[Path, Path]:
    prefix = generated_at.strftime("name-atlas-%Y%m%dT%H%M%S%z")
    base = f"{prefix}-{snapshot_commitment[:8]}"
    for counter in range(1_000):
        suffix = "" if counter == 0 else f"-{counter}"
        final_root = output_root / f"{base}{suffix}"
        pending_root = output_root / f".{base}{suffix}.pending"
        if not final_root.exists() and not pending_root.exists():
            pending_root.mkdir()
            return final_root, pending_root
    raise StagingError("No unused stage path is available.")


def _copy_content_member(source: Path, destination: Path, member: SourceMember) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    source_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    destination_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    source_descriptor: int | None = None
    destination_descriptor: int | None = None
    digest = hashlib.sha256()
    size = 0
    try:
        source_descriptor = os.open(source, source_flags)
        source_stat = os.fstat(source_descriptor)
        if not stat.S_ISREG(source_stat.st_mode):
            raise StagingError(f"Source is not a regular file: {member.relative_path}")
        destination_descriptor = os.open(destination, destination_flags, 0o600)
        while chunk := os.read(source_descriptor, HASH_CHUNK_SIZE):
            digest.update(chunk)
            size += len(chunk)
            view = memoryview(chunk)
            while view:
                written = os.write(destination_descriptor, view)
                view = view[written:]
        os.fsync(destination_descriptor)
    except OSError as exc:
        raise StagingError(f"Copy failed for {member.relative_path}.") from exc
    finally:
        if destination_descriptor is not None:
            os.close(destination_descriptor)
        if source_descriptor is not None:
            os.close(source_descriptor)
    if size != member.size or digest.hexdigest() != member.sha256:
        raise StagingError(
            f"Copied payload does not match source: {member.relative_path}"
        )


def _write_control_files(
    package: SourcePackage,
    decision_by_family: dict[str, HumanDecision],
    *,
    pending_root: Path,
) -> None:
    """Write declared control files from stored family target maps."""

    family_by_row = {
        family.metadata_row.row_number: family for family in package.families
    }
    metadata_rows = []
    for row in package.metadata_rows:
        values = list(row.values)
        family = family_by_row[row.row_number]
        values[0] = decision_by_family[family.family_id].resolved_targets[
            ContentRole.ORIGINAL
        ]
        metadata_rows.append(tuple(values))
    metadata_bytes = _render_csv((package.metadata_header, *metadata_rows))
    metadata_target = pending_root / "data" / "metadata" / "metadata.csv"
    _write_new_bytes(metadata_target, metadata_bytes)

    if package.normalization_present:
        family_by_normalization_row = {
            family.normalization_row_number: family
            for family in package.families
            if family.normalization_row_number is not None
        }
        normalization_values = []
        for row in package.normalization_rows:
            family = family_by_normalization_row[row.row_number]
            targets = decision_by_family[family.family_id].resolved_targets
            normalization_values.append(
                (
                    targets[ContentRole.ORIGINAL],
                    targets.get(ContentRole.ACCESS, ""),
                    targets.get(ContentRole.PRESERVATION, ""),
                )
            )
        normalization_bytes = _render_csv(tuple(normalization_values))
        _write_new_bytes(
            pending_root / "data" / "normalization.csv", normalization_bytes
        )


def _render_csv(rows: tuple[tuple[str, ...], ...]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerows(rows)
    return stream.getvalue().encode()


def _write_new_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def _require_globally_unique_targets(targets: tuple[str, ...]) -> None:
    if not targets_are_unique(targets):
        raise StagingError("Resolved targets collide under exact, NFC, or casefold.")


def _preserve_failure_report(
    *,
    report_path: Path,
    generated_at: datetime,
    final_root: Path,
    package: SourcePackage,
    map_rows: tuple[PathMapRow, ...],
    stage: str,
    error: Exception,
) -> None:
    reason = (
        str(error).strip()
        if isinstance(error, StagingError)
        else f"Unexpected {type(error).__name__} during {stage}."
    )
    if not reason:
        reason = f"Staging failed during {stage}."
    report = _failure_report(
        generated_at=generated_at,
        final_root=final_root,
        package=package,
        map_rows=map_rows,
        stage=stage,
        reason=reason[:800],
    )
    try:
        if report_path.exists():
            replace_verification_report(report_path, report)
        else:
            write_verification_report(report_path, report)
    except (OSError, ValueError):
        LOGGER.error("Could not preserve staging failure report at %s", report_path)


def _failure_report(
    *,
    generated_at: datetime,
    final_root: Path,
    package: SourcePackage,
    map_rows: tuple[PathMapRow, ...],
    stage: str,
    reason: str,
) -> VerificationReport:
    blocker = f"{stage}: {reason}"
    return VerificationReport(
        status=ProofStatus.BLOCKED,
        claim=None,
        generated_at=generated_at,
        staged_location=str(final_root),
        source_snapshot_commitment=package.snapshot.commitment,
        prestaging_snapshot_commitment=package.snapshot.commitment,
        postcopy_snapshot_commitment=None,
        source_unchanged=None,
        content_object_count=len(map_rows),
        content_bytes=sum(row.size for row in map_rows),
        control_files=(),
        map_row_count=len(map_rows),
        checks=(
            VerificationCheck(
                check_id="transaction_incomplete",
                label="Staging transaction did not complete",
                passed=False,
                detail=blocker,
            ),
        ),
        bagit_validation=PackageValidationResult(
            validator="bagit",
            valid=False,
            messages=("BagIt validation did not complete.",),
        ),
        artifact_paths=("name-atlas/verification_report.json",),
        blockers=(blocker,),
    )


def _report(
    *,
    status: ProofStatus,
    claim: str | None,
    generated_at: datetime,
    final_root: Path,
    package: SourcePackage,
    postcopy_commitment: str,
    maps: tuple[PathMapRow, ...],
    control_proofs: tuple[ControlFileProof, ...],
    checks: tuple[VerificationCheck, ...],
    bagit_validation: PackageValidationResult,
    artifact_paths: tuple[str, ...],
    blockers: tuple[str, ...],
) -> VerificationReport:
    return VerificationReport(
        status=status,
        claim=claim,
        generated_at=generated_at,
        staged_location=str(final_root),
        source_snapshot_commitment=package.snapshot.commitment,
        prestaging_snapshot_commitment=package.snapshot.commitment,
        postcopy_snapshot_commitment=postcopy_commitment,
        source_unchanged=postcopy_commitment == package.snapshot.commitment,
        content_object_count=len(maps),
        content_bytes=sum(row.size for row in maps),
        control_files=control_proofs,
        map_row_count=len(maps),
        checks=checks,
        bagit_validation=bagit_validation,
        artifact_paths=artifact_paths,
        blockers=blockers,
    )
