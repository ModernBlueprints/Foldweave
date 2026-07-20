"""Independent source-free verification for Connected Change receipt families."""

from __future__ import annotations

import hashlib
import os
import stat
import uuid
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Literal, Self, TypeVar

from pydantic import (
    BaseModel,
    Field,
    TypeAdapter,
    ValidationError,
    field_validator,
    model_validator,
)

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
    build_connected_accepted_plan,
    validate_connected_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    CapsuleAppliedExecutionOrigin,
    ConnectedChangeFileV2,
    ConnectedChangeLineageV1,
    ConnectedChangeMatchReport,
    ConnectedChangeMemberBindingV1,
    FolderExecutionOrigin,
    GptExecutionOrigin,
    connected_change_core_v2_fingerprint,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    build_connected_change_core,
    build_connected_change_core_v2,
    parse_connected_change_file,
    parse_connected_change_file_any,
    parse_connected_change_file_v2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderPortableExecutionAuthorizationV1,
)
from name_atlas.folder_refactor.connected_change.matcher import (
    match_connected_change,
)
from name_atlas.folder_refactor.connected_change.organized_tree import (
    scan_organized_tree,
)
from name_atlas.folder_refactor.connected_change.preview import (
    FolderPlanPreviewV1,
    build_folder_plan_preview,
)
from name_atlas.folder_refactor.connected_change.proof import (
    render_connected_proof_html,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_MATCH_REPORT_PATH,
    CONNECTED_CHANGE_PATH,
    EXECUTION_ORIGIN_PATH,
    FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH,
    FOLDWEAVE_PLAN_PREVIEW_PATH,
    build_connected_artifact_commitments,
    build_foldweave_artifact_commitments,
    validate_connected_evidence_ledger,
    validate_connected_verification_report,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV2,
    FolderReceiptEnvelopeV3,
    parse_folder_receipt_envelope_any,
)
from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderInventory,
    FolderVerificationReport,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeEvidenceLedgerV1,
    FolderEvidenceLedgerV2,
    GptPlannedExecutionOriginV2,
)
from name_atlas.folder_refactor.inventory import FolderScanError, scan_folder
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.markdown_links import (
    MARKDOWN_SUFFIXES,
    build_reference_graph,
    derive_reference_rewrites,
    verify_reference_rewrites,
)
from name_atlas.folder_refactor.portable_artifacts import (
    ACCEPTED_PLAN_PATH,
    CHANGE_LEDGER_PATH,
    CHANGE_RECEIPT_PATH,
    EVIDENCE_LEDGER_PATH,
    FORWARD_PATH_MAP_PATH,
    ORIGINAL_CONTENT_ROOT,
    PROOF_AND_RESTORE_HTML_PATH,
    REFERENCE_GRAPH_PATH,
    REVERSE_PATH_MAP_PATH,
    SOURCE_SNAPSHOT_PATH,
    USER_REQUEST_PATH,
    VERIFICATION_REPORT_PATH,
    FolderPortableArtifactError,
    canonical_portable_json_bytes,
    parse_folder_path_map,
    parse_portable_model,
    read_regular_bytes,
    regular_file_measurement,
    staged_data_commitment,
    staged_data_members,
    strict_json_object,
)
from name_atlas.folder_refactor.receipt_builder import (
    ObservedResultFile,
    build_folder_path_rows_and_change_ledger,
    contains_sender_local_path,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderChangeLedger,
    FolderEvidenceLedger,
    FolderReceiptVerificationCheck,
    FolderUserRequestArtifact,
)
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.verification.bagit_validator import (
    BagItAdapterError,
    BagItPackageValidator,
)

_EXECUTION_ORIGIN_ADAPTER = TypeAdapter(FolderExecutionOrigin)
_EVIDENCE_LEDGER_ADAPTER = TypeAdapter(FolderEvidenceLedger | FolderEvidenceLedgerV2)
_Model = TypeVar("_Model", bound=BaseModel)


class _VerificationBlocked(ValueError):
    """One stable independent-verifier refusal."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class ConnectedReceiptVerificationStatus(StrEnum):
    """Independent v2 verification outcome."""

    VERIFIED = "verified"
    BLOCKED = "blocked"


class ConnectedReceiptVerification(StrictFrozenModel):
    """Write-free historical `folder-receipt-verification.v2` result."""

    schema_version: Literal["folder-receipt-verification.v2"] = (
        "folder-receipt-verification.v2"
    )
    status: ConnectedReceiptVerificationStatus
    job_id: str | None = Field(default=None, pattern=r"^[a-f0-9]{32}$")
    receipt_fingerprint: str | None = Field(default=None, pattern=SHA256_PATTERN)
    organized_tree_commitment: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
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
        failed = tuple(check.check_id for check in self.checks if not check.passed)
        if failed != self.failed_check_ids:
            raise ValueError("Failed check IDs do not match verification checks.")
        if self.status is ConnectedReceiptVerificationStatus.VERIFIED:
            if (
                self.job_id is None
                or self.receipt_fingerprint is None
                or self.organized_tree_commitment is None
                or self.failed_check_ids
            ):
                raise ValueError("A verified result requires complete identities.")
        elif not self.failed_check_ids:
            raise ValueError("A blocked result requires at least one failure.")
        return self


class FoldweaveReceiptVerificationV3(ConnectedReceiptVerification):
    """Strict write-free verification result emitted only for v3 receipts."""

    schema_version: Literal["folder-receipt-verification.v3"] = (
        "folder-receipt-verification.v3"
    )


def verify_connected_result(
    result_root: Path,
    *,
    source_root: Path | None = None,
) -> ConnectedReceiptVerification:
    """Strictly dispatch source-free verification across receipt v2 and v3."""

    try:
        receipt_bytes = read_regular_bytes(result_root, CHANGE_RECEIPT_PATH)
        raw = strict_json_object(receipt_bytes)
        core = raw.get("receipt")
        schema_version = core.get("schema_version") if isinstance(core, dict) else None
    except (FolderPortableArtifactError, OSError, ValueError):
        # Preserve the historical verifier's precise blocked result for every
        # malformed or missing v2-family artifact.
        schema_version = None
    if schema_version == "folder-change-receipt.v3":
        return _verify_foldweave_result_v3(result_root, source_root=source_root)
    return _verify_connected_result_v2(result_root, source_root=source_root)


def _verify_connected_result_v2(
    result_root: Path,
    *,
    source_root: Path | None = None,
) -> ConnectedReceiptVerification:
    """Verify v2 proof, optionally comparing one currently available source."""

    checks: list[FolderReceiptVerificationCheck] = []
    envelope: FolderReceiptEnvelopeV2 | None = None
    try:
        root = _require_candidate_root(result_root)
        bagit = BagItPackageValidator().validate(root)
        if not bagit.valid:
            return _blocked(
                checks,
                "bagit_validation_failed",
                "; ".join(bagit.messages),
            )
        _passed(checks, "bagit_valid", "BagIt validation passed.")

        receipt_bytes = read_regular_bytes(root, CHANGE_RECEIPT_PATH)
        envelope = parse_portable_model(receipt_bytes, FolderReceiptEnvelopeV2)
        if canonical_portable_json_bytes(envelope) != receipt_bytes:
            return _blocked(
                checks,
                "receipt_serialization_invalid",
                "The v2 receipt is not canonical JSON.",
                envelope=envelope,
            )
        _passed(
            checks,
            "receipt_fingerprint_valid",
            "The v2 receipt fingerprint matches.",
        )
        core = envelope.receipt
        if tuple(bagit.messages) != core.producer_bagit_messages:
            return _blocked(
                checks,
                "receipt_summary_mismatch",
                "The receipt's BagIt summary differs from independent validation.",
                envelope=envelope,
            )

        for commitment in core.artifact_commitments:
            size, digest = regular_file_measurement(root, commitment.path)
            if size != commitment.size or digest != commitment.sha256:
                slug = commitment.path.rsplit("/", 1)[-1].split(".", 1)[0]
                return _blocked(
                    checks,
                    f"artifact_digest_mismatch:{slug}",
                    f"Receipt-bound bytes changed: {commitment.path}",
                    envelope=envelope,
                )
        _passed(
            checks,
            "artifact_commitments_valid",
            f"All {len(core.artifact_commitments)} raw commitments match.",
        )

        artifacts = _parse_authorities(root, execution_role=core.execution_role)
        _validate_authorities(root, envelope, artifacts)
        _validate_exact_artifact_family(root, envelope, artifacts)
        _passed(
            checks,
            "portable_authorities_valid",
            "Every v2 authority is strict, canonical, complete, and mutually bound.",
        )

        actual_staged = staged_data_members(root)
        if actual_staged != core.staged_data_members or (
            staged_data_commitment(actual_staged) != core.staged_data_commitment
        ):
            raise ValueError("Staged data commitment differs from the receipt.")
        _verify_payloads(root, artifacts)
        _passed(
            checks,
            "complete_file_bijection",
            "Every committed source file appears exactly once with verified bytes.",
        )

        organized = scan_organized_tree(root / "data")
        if organized != core.organized_tree:
            raise ValueError("Organized tree differs from the receipt commitment.")
        _passed(
            checks,
            "organized_tree_commitment_valid",
            "Files, paths, bytes, and explicit empty directories match.",
        )

        _validate_connected_authority(root, envelope, artifacts)
        _passed(
            checks,
            "connected_change_authority_valid",
            "Change File, execution origin, and receiver bindings are exact.",
        )
        expected_proof = render_connected_proof_html(
            envelope.receipt_fingerprint,
            organized.commitment,
        )
        if read_regular_bytes(root, PROOF_AND_RESTORE_HTML_PATH) != expected_proof:
            raise _VerificationBlocked(
                "offline_proof_mismatch",
                "The human-readable proof differs from verified machine facts.",
            )
        _passed(
            checks,
            "offline_proof_valid",
            "The human-readable proof is exactly derived from verified facts.",
        )
        if source_root is not None:
            _compare_supplied_source(source_root, artifacts.inventory)
            _passed(
                checks,
                "supplied_source_matches",
                "The optional source exactly matches every committed path and byte.",
            )
        return _result(
            checks,
            envelope=envelope,
            organized_tree_commitment=organized.commitment,
        )
    except _VerificationBlocked as exc:
        return _blocked(
            checks,
            exc.code,
            exc.message,
            envelope=envelope,
        )
    except (FolderPortableArtifactError, ValidationError, ValueError, OSError) as exc:
        return _blocked(
            checks,
            "connected_receipt_invalid",
            str(exc),
            envelope=envelope,
        )
    except BagItAdapterError as exc:
        return _blocked(checks, "bagit_validation_error", str(exc))


def _verify_foldweave_result_v3(
    result_root: Path,
    *,
    source_root: Path | None = None,
) -> ConnectedReceiptVerification:
    """Verify one review- and lineage-aware Foldweave result without its source."""

    checks: list[FolderReceiptVerificationCheck] = []
    envelope: FolderReceiptEnvelopeV3 | None = None
    try:
        root = _require_candidate_root(result_root)
        bagit = BagItPackageValidator().validate(root)
        if not bagit.valid:
            return _blocked(
                checks,
                "bagit_validation_failed",
                "; ".join(bagit.messages),
                verification_schema_version="folder-receipt-verification.v3",
            )
        _passed(checks, "bagit_valid", "BagIt validation passed.")

        receipt_bytes = read_regular_bytes(root, CHANGE_RECEIPT_PATH)
        parsed = parse_folder_receipt_envelope_any(receipt_bytes)
        if not isinstance(parsed, FolderReceiptEnvelopeV3):
            raise _VerificationBlocked(
                "receipt_schema_mismatch",
                "Foldweave verification requires a v3 receipt.",
            )
        envelope = parsed
        core = envelope.receipt
        _passed(
            checks,
            "receipt_fingerprint_valid",
            "The v3 receipt fingerprint matches its immutable core.",
        )
        if tuple(bagit.messages) != core.producer_bagit_messages:
            raise _VerificationBlocked(
                "receipt_summary_mismatch",
                "The receipt's BagIt summary differs from independent validation.",
            )
        for commitment in core.artifact_commitments:
            size, digest = regular_file_measurement(root, commitment.path)
            if size != commitment.size or digest != commitment.sha256:
                slug = commitment.path.rsplit("/", 1)[-1].split(".", 1)[0]
                raise _VerificationBlocked(
                    f"artifact_digest_mismatch:{slug}",
                    f"Receipt-bound bytes changed: {commitment.path}",
                )
        _passed(
            checks,
            "artifact_commitments_valid",
            f"All {len(core.artifact_commitments)} v3 commitments match.",
        )

        artifacts = _parse_foldweave_authorities(root, core.execution_role)
        _validate_foldweave_authorities(root, envelope, artifacts)
        _validate_exact_foldweave_artifact_family(root, envelope, artifacts)
        _passed(
            checks,
            "portable_authorities_valid",
            "Preview, authorization, evidence, and result authorities are exact.",
        )

        actual_staged = staged_data_members(root)
        if actual_staged != core.staged_data_members or (
            staged_data_commitment(actual_staged) != core.staged_data_commitment
        ):
            raise ValueError("Staged data commitment differs from the v3 receipt.")
        _verify_payloads(root, artifacts)
        _passed(
            checks,
            "complete_file_bijection",
            "Every transaction-source file appears once with verified bytes.",
        )
        organized = scan_organized_tree(root / "data")
        if organized != core.organized_tree:
            raise ValueError("Organized tree differs from the v3 receipt.")
        _passed(
            checks,
            "organized_tree_commitment_valid",
            "Files, paths, bytes, and explicit empty directories match.",
        )

        _validate_foldweave_change_authority(root, envelope, artifacts)
        _passed(
            checks,
            "foldweave_change_authority_valid",
            "The role-specific Change File, provenance, match, and lineage are exact.",
        )
        expected_proof = render_connected_proof_html(
            envelope.receipt_fingerprint,
            organized.commitment,
            release_profile="foldweave",
        )
        if read_regular_bytes(root, PROOF_AND_RESTORE_HTML_PATH) != expected_proof:
            raise _VerificationBlocked(
                "offline_proof_mismatch",
                "The human-readable proof differs from verified machine facts.",
            )
        _passed(
            checks,
            "offline_proof_valid",
            "The human-readable proof is exactly derived from verified facts.",
        )
        if source_root is not None:
            _compare_supplied_source(source_root, artifacts.inventory)
            _passed(
                checks,
                "supplied_source_matches",
                "The optional source matches this transaction's source snapshot.",
            )
        return _result(
            checks,
            envelope=envelope,
            organized_tree_commitment=organized.commitment,
            verification_schema_version="folder-receipt-verification.v3",
        )
    except _VerificationBlocked as exc:
        return _blocked(
            checks,
            exc.code,
            exc.message,
            envelope=envelope,
            verification_schema_version="folder-receipt-verification.v3",
        )
    except (FolderPortableArtifactError, ValidationError, ValueError, OSError) as exc:
        return _blocked(
            checks,
            "foldweave_receipt_invalid",
            str(exc),
            envelope=envelope,
            verification_schema_version="folder-receipt-verification.v3",
        )
    except BagItAdapterError as exc:
        return _blocked(
            checks,
            "bagit_validation_error",
            str(exc),
            verification_schema_version="folder-receipt-verification.v3",
        )


class _Authorities:
    def __init__(
        self,
        *,
        inventory: FolderInventory,
        request: FolderUserRequestArtifact,
        plan: FolderAcceptedPlanV2,
        graph: FolderReferenceGraph,
        rows: tuple,
        ledger: FolderChangeLedger,
        report: FolderVerificationReport,
        execution_origin: FolderExecutionOrigin,
        evidence_ledger: FolderEvidenceLedger | FolderEvidenceLedgerV2 | None,
        plan_preview: FolderPlanPreviewV1 | None = None,
        execution_authorization: FolderPortableExecutionAuthorizationV1 | None = None,
    ) -> None:
        self.inventory = inventory
        self.request = request
        self.plan = plan
        self.graph = graph
        self.rows = rows
        self.ledger = ledger
        self.report = report
        self.execution_origin = execution_origin
        self.evidence_ledger = evidence_ledger
        self.plan_preview = plan_preview
        self.execution_authorization = execution_authorization


def _parse_authorities(
    root: Path,
    *,
    execution_role: Literal["origin", "receiver"],
) -> _Authorities:
    origin_bytes = read_regular_bytes(root, EXECUTION_ORIGIN_PATH)
    strict_json_object(origin_bytes)
    origin = _EXECUTION_ORIGIN_ADAPTER.validate_json(origin_bytes, strict=True)
    if canonical_portable_json_bytes(origin) != origin_bytes:
        raise _VerificationBlocked(
            "portable_artifact_schema_invalid",
            "Execution-origin JSON is not canonical.",
        )
    evidence_ledger = (
        _parse_canonical_evidence_ledger(root) if execution_role == "origin" else None
    )
    return _Authorities(
        inventory=_parse_canonical_model(root, SOURCE_SNAPSHOT_PATH, FolderInventory),
        request=_parse_canonical_model(
            root,
            USER_REQUEST_PATH,
            FolderUserRequestArtifact,
        ),
        plan=_parse_canonical_model(root, ACCEPTED_PLAN_PATH, FolderAcceptedPlanV2),
        graph=_parse_canonical_model(
            root,
            REFERENCE_GRAPH_PATH,
            FolderReferenceGraph,
        ),
        rows=parse_folder_path_map(
            read_regular_bytes(root, FORWARD_PATH_MAP_PATH), reverse=False
        ),
        ledger=_parse_canonical_model(
            root,
            CHANGE_LEDGER_PATH,
            FolderChangeLedger,
        ),
        report=_parse_canonical_model(
            root,
            VERIFICATION_REPORT_PATH,
            FolderVerificationReport,
        ),
        execution_origin=origin,
        evidence_ledger=evidence_ledger,
    )


def _parse_foldweave_authorities(
    root: Path,
    execution_role: Literal["origin", "receiver", "derivative"],
) -> _Authorities:
    origin_bytes = read_regular_bytes(root, EXECUTION_ORIGIN_PATH)
    strict_json_object(origin_bytes)
    origin = _EXECUTION_ORIGIN_ADAPTER.validate_json(origin_bytes, strict=True)
    if canonical_portable_json_bytes(origin) != origin_bytes:
        raise _VerificationBlocked(
            "portable_artifact_schema_invalid",
            "Execution-origin JSON is not canonical.",
        )
    evidence_ledger = (
        _parse_canonical_evidence_ledger(root)
        if execution_role in {"origin", "derivative"}
        else None
    )
    return _Authorities(
        inventory=_parse_canonical_model(root, SOURCE_SNAPSHOT_PATH, FolderInventory),
        request=_parse_canonical_model(
            root,
            USER_REQUEST_PATH,
            FolderUserRequestArtifact,
        ),
        plan=_parse_canonical_model(root, ACCEPTED_PLAN_PATH, FolderAcceptedPlanV2),
        graph=_parse_canonical_model(
            root,
            REFERENCE_GRAPH_PATH,
            FolderReferenceGraph,
        ),
        rows=parse_folder_path_map(
            read_regular_bytes(root, FORWARD_PATH_MAP_PATH),
            reverse=False,
        ),
        ledger=_parse_canonical_model(
            root,
            CHANGE_LEDGER_PATH,
            FolderChangeLedger,
        ),
        report=_parse_canonical_model(
            root,
            VERIFICATION_REPORT_PATH,
            FolderVerificationReport,
        ),
        execution_origin=origin,
        evidence_ledger=evidence_ledger,
        plan_preview=_parse_canonical_model(
            root,
            FOLDWEAVE_PLAN_PREVIEW_PATH,
            FolderPlanPreviewV1,
        ),
        execution_authorization=_parse_canonical_model(
            root,
            FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH,
            FolderPortableExecutionAuthorizationV1,
        ),
    )


def _parse_canonical_model(
    root: Path,
    relative_path: str,
    model_type: type[_Model],
) -> _Model:
    payload = read_regular_bytes(root, relative_path)
    parsed = parse_portable_model(payload, model_type)
    if canonical_portable_json_bytes(parsed) != payload:
        raise _VerificationBlocked(
            "portable_artifact_schema_invalid",
            f"Portable JSON is not canonical: {relative_path}.",
        )
    return parsed


def _parse_canonical_evidence_ledger(
    root: Path,
) -> FolderEvidenceLedger | FolderEvidenceLedgerV2:
    payload = read_regular_bytes(root, EVIDENCE_LEDGER_PATH)
    strict_json_object(payload)
    parsed = _EVIDENCE_LEDGER_ADAPTER.validate_json(payload, strict=True)
    if canonical_portable_json_bytes(parsed) != payload:
        raise _VerificationBlocked(
            "portable_artifact_schema_invalid",
            "Evidence-ledger JSON is not canonical.",
        )
    return parsed


def _validate_authorities(
    root: Path,
    envelope: FolderReceiptEnvelopeV2,
    artifacts: _Authorities,
) -> None:
    core = envelope.receipt
    reverse = parse_folder_path_map(
        read_regular_bytes(root, REVERSE_PATH_MAP_PATH), reverse=True
    )
    if reverse != artifacts.rows:
        raise ValueError("Forward and reverse maps are not exact inverses.")
    validate_connected_accepted_plan(
        inventory=artifacts.inventory,
        request=artifacts.request.request,
        plan=artifacts.plan,
    )
    derived = derive_reference_rewrites(artifacts.graph, artifacts.plan)
    if derived != artifacts.graph:
        raise ValueError("Reference graph does not equal deterministic derivation.")
    observed = {
        row.file_id: ObservedResultFile(
            relative_path=row.result_path,
            size=row.result_size,
            sha256=row.result_sha256,
        )
        for row in artifacts.rows
    }
    expected_rows, expected_ledger = build_folder_path_rows_and_change_ledger(
        inventory=artifacts.inventory,
        accepted_plan=artifacts.plan,
        reference_graph=artifacts.graph,
        observed_result_files=observed,
    )
    if expected_rows != artifacts.rows or expected_ledger != artifacts.ledger:
        raise ValueError("Maps or change ledger do not recompute exactly.")
    expected_summary = {
        "source_file_count": len(artifacts.inventory.files),
        "source_directory_count": artifacts.inventory.directory_count,
        "source_bytes": artifacts.inventory.total_bytes,
        "map_row_count": len(artifacts.rows),
        "path_change_count": artifacts.ledger.path_change_count,
        "supported_link_count": len(artifacts.graph.references),
        "rewritten_link_count": artifacts.ledger.rewritten_link_count,
    }
    if any(
        getattr(core, field_name) != value
        for field_name, value in expected_summary.items()
    ):
        raise _VerificationBlocked(
            "receipt_summary_mismatch",
            "Receipt summary counts differ from independently derived facts.",
        )
    if not (
        core.source_commitment == artifacts.inventory.source_commitment
        and core.request_fingerprint == artifacts.request.request_fingerprint
        and core.evidence_fingerprint == artifacts.plan.evidence_fingerprint
        and core.accepted_plan_fingerprint == canonical_sha256(artifacts.plan)
        and core.reference_graph_fingerprint == canonical_sha256(artifacts.graph)
        and core.execution_origin_fingerprint
        == canonical_sha256(artifacts.execution_origin)
        and core.change_ledger_fingerprint == canonical_sha256(artifacts.ledger)
        and core.verification_report_fingerprint == canonical_sha256(artifacts.report)
        and artifacts.report.staged_data_commitment == core.staged_data_commitment
    ):
        raise ValueError("Receipt fingerprints do not bind the parsed authorities.")
    try:
        validate_connected_verification_report(
            inventory=artifacts.inventory,
            accepted_plan=artifacts.plan,
            reference_graph=artifacts.graph,
            change_ledger=artifacts.ledger,
            report=artifacts.report,
            organized_tree=core.organized_tree,
        )
    except ValueError as exc:
        raise _VerificationBlocked(
            "verification_report_mismatch",
            "The verification report differs from independently derived facts.",
        ) from exc
    if core.execution_role == "origin":
        if not isinstance(artifacts.execution_origin, GptExecutionOrigin):
            raise ValueError("Origin result lacks gpt_planned execution authority.")
        if artifacts.evidence_ledger is None:
            raise ValueError("Origin result lacks its exact evidence ledger.")
        try:
            validate_connected_evidence_ledger(
                job_id=core.job_id,
                inventory=artifacts.inventory,
                user_request=artifacts.request,
                accepted_plan=artifacts.plan,
                execution_origin=artifacts.execution_origin,
                evidence_ledger=artifacts.evidence_ledger,
            )
        except ValueError as exc:
            raise _VerificationBlocked(
                "origin_evidence_mismatch",
                "Origin evidence differs from its accepted plan or execution origin.",
            ) from exc
    elif artifacts.evidence_ledger is not None:
        raise ValueError("Receiver result contains fabricated GPT evidence.")
    if contains_sender_local_path(
        (
            envelope,
            artifacts.inventory,
            artifacts.request,
            artifacts.plan,
            artifacts.graph,
            artifacts.ledger,
            artifacts.report,
            artifacts.execution_origin,
            artifacts.evidence_ledger,
        )
    ):
        raise ValueError("Portable v2 proof contains a sender-local absolute path.")


def _validate_foldweave_authorities(
    root: Path,
    envelope: FolderReceiptEnvelopeV3,
    artifacts: _Authorities,
) -> None:
    core = envelope.receipt
    preview = artifacts.plan_preview
    authorization = artifacts.execution_authorization
    if preview is None or authorization is None:
        raise ValueError("Foldweave result lacks preview or execution authorization.")
    _require_path_neutral_v3_authorities(
        envelope,
        artifacts.inventory,
        artifacts.request,
        artifacts.plan,
        artifacts.graph,
        artifacts.rows,
        artifacts.ledger,
        artifacts.report,
        artifacts.execution_origin,
        artifacts.evidence_ledger,
        preview,
        authorization,
    )
    reverse = parse_folder_path_map(
        read_regular_bytes(root, REVERSE_PATH_MAP_PATH),
        reverse=True,
    )
    if reverse != artifacts.rows:
        raise ValueError("Forward and reverse maps are not exact inverses.")
    validate_connected_accepted_plan(
        inventory=artifacts.inventory,
        request=artifacts.request.request,
        plan=artifacts.plan,
    )
    if derive_reference_rewrites(artifacts.graph, artifacts.plan) != artifacts.graph:
        raise ValueError("Reference graph does not equal deterministic derivation.")
    observed = {
        row.file_id: ObservedResultFile(
            relative_path=row.result_path,
            size=row.result_size,
            sha256=row.result_sha256,
        )
        for row in artifacts.rows
    }
    expected_rows, expected_ledger = build_folder_path_rows_and_change_ledger(
        inventory=artifacts.inventory,
        accepted_plan=artifacts.plan,
        reference_graph=artifacts.graph,
        observed_result_files=observed,
    )
    if expected_rows != artifacts.rows or expected_ledger != artifacts.ledger:
        raise ValueError("Maps or change ledger do not recompute exactly.")
    expected_summary = {
        "source_file_count": len(artifacts.inventory.files),
        "source_directory_count": artifacts.inventory.directory_count,
        "source_bytes": artifacts.inventory.total_bytes,
        "map_row_count": len(artifacts.rows),
        "path_change_count": artifacts.ledger.path_change_count,
        "supported_link_count": len(artifacts.graph.references),
        "rewritten_link_count": artifacts.ledger.rewritten_link_count,
    }
    if any(
        getattr(core, field_name) != value
        for field_name, value in expected_summary.items()
    ):
        raise _VerificationBlocked(
            "receipt_summary_mismatch",
            "V3 receipt summary differs from independently derived facts.",
        )
    candidate_fingerprint = canonical_sha256(artifacts.plan)
    rebuilt_preview = build_folder_plan_preview(
        job_id=preview.job_id,
        expected_job_revision=preview.expected_job_revision,
        proposal_revision=preview.proposal_revision,
        proposal_basis=preview.proposal_basis,
        inventory=artifacts.inventory,
        reference_graph=artifacts.graph,
        accepted_plan=artifacts.plan,
        imported_change_file_fingerprint=(preview.imported_change_file_fingerprint),
        match_report_fingerprint=preview.match_report_fingerprint,
        immediate_parent_candidate_fingerprint=(
            preview.immediate_parent_candidate_fingerprint
        ),
    )
    if rebuilt_preview != preview:
        raise _VerificationBlocked(
            "plan_preview_mismatch",
            "The reviewed preview differs from the deterministic candidate projection.",
        )
    if not (
        core.source_commitment == artifacts.inventory.source_commitment
        and core.request_fingerprint == artifacts.request.request_fingerprint
        and core.evidence_fingerprint == artifacts.plan.evidence_fingerprint
        and core.accepted_plan_fingerprint == candidate_fingerprint
        and core.compiled_candidate_fingerprint == candidate_fingerprint
        and core.reference_graph_fingerprint == canonical_sha256(artifacts.graph)
        and core.execution_origin_fingerprint
        == canonical_sha256(artifacts.execution_origin)
        and core.execution_authorization_fingerprint
        == authorization.authorization_fingerprint
        and core.plan_preview_fingerprint == preview.preview_fingerprint
        and core.change_ledger_fingerprint == canonical_sha256(artifacts.ledger)
        and core.verification_report_fingerprint == canonical_sha256(artifacts.report)
        and artifacts.report.staged_data_commitment == core.staged_data_commitment
        and preview.compiled_candidate_fingerprint == candidate_fingerprint
        and authorization.candidate_fingerprint == candidate_fingerprint
        and authorization.preview_fingerprint == preview.preview_fingerprint
        and authorization.job_id == core.job_id == preview.job_id
        and authorization.expected_job_revision == preview.expected_job_revision
        and authorization.proposal_revision == preview.proposal_revision
        and authorization.result_folder_name == artifacts.plan.result_folder_name
        and authorization.source_commitment
        == preview.source_commitment
        == artifacts.inventory.source_commitment
    ):
        raise ValueError("V3 receipt does not bind the exact reviewed authorities.")
    try:
        validate_connected_verification_report(
            inventory=artifacts.inventory,
            accepted_plan=artifacts.plan,
            reference_graph=artifacts.graph,
            change_ledger=artifacts.ledger,
            report=artifacts.report,
            organized_tree=core.organized_tree,
        )
    except ValueError as exc:
        raise _VerificationBlocked(
            "verification_report_mismatch",
            "The verification report differs from independently derived facts.",
        ) from exc
    if core.execution_role in {"origin", "derivative"}:
        if not isinstance(artifacts.execution_origin, GptPlannedExecutionOriginV2):
            raise ValueError("Model-planned v3 result lacks v2 provenance.")
        if not isinstance(artifacts.evidence_ledger, FolderEvidenceLedgerV2):
            raise ValueError("Model-planned v3 result lacks composite evidence.")
        validate_connected_evidence_ledger(
            job_id=core.job_id,
            inventory=artifacts.inventory,
            user_request=artifacts.request,
            accepted_plan=artifacts.plan,
            execution_origin=artifacts.execution_origin,
            evidence_ledger=artifacts.evidence_ledger,
        )
    elif artifacts.evidence_ledger is not None:
        raise ValueError("Model-free receiver result contains GPT evidence.")


def _require_path_neutral_v3_authorities(*values: object) -> None:
    """Reject any sender-local absolute path in v3 portable proof authority."""

    if contains_sender_local_path(values):
        raise _VerificationBlocked(
            "portable_sender_path_detected",
            "Foldweave portable v3 proof contains a sender-local absolute path.",
        )


def _verify_payloads(root: Path, artifacts: _Authorities) -> None:
    plan_by_id = {item.file_id: item for item in artifacts.plan.file_mappings}
    inventory_by_id = {item.file_id: item for item in artifacts.inventory.files}
    if set(plan_by_id) != set(inventory_by_id) or len(artifacts.rows) != len(
        inventory_by_id
    ):
        raise ValueError("Source-to-result file accounting is incomplete.")
    for row in artifacts.rows:
        mapping = plan_by_id[row.file_id]
        source = inventory_by_id[row.file_id]
        if not (
            row.original_path == source.relative_path == mapping.original_path
            and row.result_path == mapping.target_path
            and row.original_size == source.size
            and row.original_sha256 == source.sha256
        ):
            raise ValueError("A path-map row differs from source or accepted plan.")
        size, digest = regular_file_measurement(root, f"data/{row.result_path}")
        if size != row.result_size or digest != row.result_sha256:
            raise ValueError("Observed result bytes differ from the complete map.")
        if row.markdown_rewritten:
            original = read_regular_bytes(
                root,
                f"{ORIGINAL_CONTENT_ROOT}/{row.file_id}.bin",
            )
            if (
                len(original) != row.original_size
                or hashlib.sha256(original).hexdigest() != row.original_sha256
            ):
                raise ValueError("Original rewritten Markdown bytes differ.")
            staged = read_regular_bytes(root, f"data/{row.result_path}")
            verify_reference_rewrites(
                original,
                staged,
                source_file_id=row.file_id,
                graph=artifacts.graph,
            )
        elif row.result_sha256 != row.original_sha256:
            raise ValueError("An unchanged payload differs from its source bytes.")


def _validate_connected_authority(
    root: Path,
    envelope: FolderReceiptEnvelopeV2,
    artifacts: _Authorities,
) -> None:
    core = envelope.receipt
    change_bytes = read_regular_bytes(root, CONNECTED_CHANGE_PATH)
    change_file = (
        parse_connected_change_file(change_bytes)
        if core.execution_role == "origin"
        else parse_connected_change_file_any(change_bytes)
    )
    if change_file.core_fingerprint != core.connected_change_core_fingerprint:
        raise ValueError("Receipt and Change File Core fingerprints differ.")
    if (
        change_file.core.expected_organized_tree_commitment
        != core.organized_tree.commitment
    ):
        raise ValueError("Result does not converge to the Change File organized tree.")
    markdown_payloads = _original_markdown_payloads(root, artifacts)
    source_graph = build_reference_graph(artifacts.inventory, markdown_payloads)
    expected_result_graph = derive_reference_rewrites(source_graph, artifacts.plan)
    if expected_result_graph != artifacts.graph:
        raise ValueError(
            "Reference graph does not recompute from original Markdown bytes."
        )
    if core.execution_role == "origin":
        if (
            artifacts.plan.execution_authority != "gpt_plan"
            or not isinstance(artifacts.execution_origin, GptExecutionOrigin)
            or change_file.originating_receipt != envelope
        ):
            raise ValueError("Origin receipt, plan, or embedded receipt is untruthful.")
        expected_core = build_connected_change_core(
            artifacts.inventory,
            source_graph,
            artifacts.plan,
            request=artifacts.request.request,
            markdown_payloads=markdown_payloads,
            expected_organized_tree_commitment=core.organized_tree.commitment,
            origin_proof_identifiers=(
                artifacts.execution_origin.evidence_fingerprint,
                artifacts.execution_origin.accepted_plan_fingerprint,
            ),
        )
        if expected_core != change_file.core:
            raise ValueError(
                "Change File Core does not recompute from the origin authorities."
            )
        return
    if artifacts.plan.execution_authority != "change_file" or not isinstance(
        artifacts.execution_origin, CapsuleAppliedExecutionOrigin
    ):
        raise ValueError("Receiver result does not declare capsule authority.")
    if (
        hashlib.sha256(change_bytes).hexdigest() != core.imported_change_file_sha256
        or change_file.change_file_fingerprint != core.imported_change_file_fingerprint
        or change_file.originating_receipt.receipt_fingerprint
        != core.originating_receipt_fingerprint
    ):
        raise ValueError("Imported Change File receiver bindings differ.")
    report_bytes = read_regular_bytes(root, CONNECTED_CHANGE_MATCH_REPORT_PATH)
    report = _parse_canonical_model(
        root,
        CONNECTED_CHANGE_MATCH_REPORT_PATH,
        ConnectedChangeMatchReport,
    )
    if (
        hashlib.sha256(report_bytes).hexdigest() != core.match_report_sha256
        or report.match_report_fingerprint != core.match_report_fingerprint
        or report.status != "matched"
        or report.receiver_source_commitment != artifacts.inventory.source_commitment
        or report.core_fingerprint != change_file.core_fingerprint
    ):
        raise ValueError("Receiver match report differs from the receipt.")
    recomputed_report = match_connected_change(
        change_file,
        artifacts.inventory,
        source_graph,
        markdown_payloads=markdown_payloads,
    )
    if recomputed_report != report:
        raise ValueError(
            "Receiver match report does not recompute from committed source evidence."
        )
    expected = {
        item.receiver_file_id: (item.receiver_original_path, item.target_relative_path)
        for item in report.mappings
    }
    actual = {
        item.file_id: (item.original_path, item.target_path)
        for item in artifacts.plan.file_mappings
    }
    if expected != actual:
        raise ValueError("Receiver plan does not exactly rebind the match report.")
    origin = artifacts.execution_origin
    if not (
        origin.change_file_fingerprint == change_file.change_file_fingerprint
        and origin.originating_receipt_fingerprint
        == core.originating_receipt_fingerprint
        and origin.match_report_fingerprint == report.match_report_fingerprint
        and origin.receiver_accepted_plan_fingerprint
        == canonical_sha256(artifacts.plan)
    ):
        raise ValueError("capsule_applied provenance differs from receiver proof.")


def _validate_foldweave_change_authority(
    root: Path,
    envelope: FolderReceiptEnvelopeV3,
    artifacts: _Authorities,
) -> None:
    """Recompute the exact role-specific Change File and execution authority."""

    role = envelope.receipt.execution_role
    if role == "origin":
        _validate_foldweave_origin_change_authority(root, envelope, artifacts)
    elif role == "receiver":
        _validate_foldweave_receiver_change_authority(root, envelope, artifacts)
    else:
        _validate_foldweave_derivative_change_authority(root, envelope, artifacts)


def _validate_foldweave_origin_change_authority(
    root: Path,
    envelope: FolderReceiptEnvelopeV3,
    artifacts: _Authorities,
) -> None:
    """Rebuild one reviewed root Change File from source-free proof authorities."""

    core = envelope.receipt
    preview = artifacts.plan_preview
    authorization = artifacts.execution_authorization
    if preview is None or authorization is None:
        raise ValueError("Foldweave origin lacks reviewed authorization.")
    change_bytes = read_regular_bytes(root, CONNECTED_CHANGE_PATH)
    change_file = parse_connected_change_file_v2(change_bytes)
    _require_path_neutral_v3_authorities(change_file)
    root_core = change_file.core
    if not (
        change_file.originating_receipt == envelope
        and root_core.lineage == ConnectedChangeLineageV1(generation=0)
        and change_file.core_fingerprint == core.connected_change_core_fingerprint
        and change_file.core_fingerprint
        == connected_change_core_v2_fingerprint(root_core)
        and core.connected_change_core_schema_version == "connected-change-core.v2"
        and core.lineage_generation == 0
        and root_core.expected_organized_tree_commitment
        == core.organized_tree.commitment
    ):
        raise ValueError("Root Change File and v3 receipt do not form one proof.")
    if not (
        artifacts.plan.execution_authority == "gpt_plan"
        and isinstance(artifacts.execution_origin, GptPlannedExecutionOriginV2)
        and artifacts.execution_origin.kind == "gpt_planned"
        and artifacts.execution_origin.accepted_plan_fingerprint
        == canonical_sha256(artifacts.plan)
        and preview.proposal_basis == "fresh_gpt_plan"
        and preview.imported_change_file_fingerprint is None
        and preview.match_report_fingerprint is None
        and authorization.imported_change_file_fingerprint is None
        and authorization.match_report_fingerprint is None
    ):
        raise ValueError("Root Foldweave execution provenance is untruthful.")

    markdown_payloads = _original_markdown_payloads(root, artifacts)
    source_graph = build_reference_graph(artifacts.inventory, markdown_payloads)
    if derive_reference_rewrites(source_graph, artifacts.plan) != artifacts.graph:
        raise ValueError("Origin graph does not recompute from original bytes.")
    complete_core = build_connected_change_core(
        artifacts.inventory,
        source_graph,
        artifacts.plan,
        request=artifacts.request.request,
        markdown_payloads=markdown_payloads,
        expected_organized_tree_commitment=core.organized_tree.commitment,
        origin_proof_identifiers=(
            artifacts.execution_origin.evidence_fingerprint,
            canonical_sha256(artifacts.plan),
        ),
    )
    expected_root = build_connected_change_core_v2(
        complete_core,
        lineage=ConnectedChangeLineageV1(generation=0),
    )
    if expected_root != root_core:
        raise ValueError("Root Core does not recompute from transaction authorities.")


def _validate_foldweave_receiver_change_authority(
    root: Path,
    envelope: FolderReceiptEnvelopeV3,
    artifacts: _Authorities,
) -> None:
    """Recompute one model-free receiver from its exact imported Change File."""

    core = envelope.receipt
    preview = artifacts.plan_preview
    authorization = artifacts.execution_authorization
    if preview is None or authorization is None:
        raise ValueError("Foldweave receiver lacks reviewed authorization.")
    change_bytes = read_regular_bytes(root, CONNECTED_CHANGE_PATH)
    change_file = parse_connected_change_file_any(change_bytes)
    _require_path_neutral_v3_authorities(change_file)
    lineage_generation = (
        change_file.core.lineage.generation
        if isinstance(change_file, ConnectedChangeFileV2)
        else 0
    )
    if not (
        hashlib.sha256(change_bytes).hexdigest() == core.imported_change_file_sha256
        and change_file.change_file_fingerprint == core.imported_change_file_fingerprint
        and change_file.core_fingerprint == core.connected_change_core_fingerprint
        and change_file.core.schema_version == core.connected_change_core_schema_version
        and lineage_generation == core.lineage_generation
        and change_file.originating_receipt.receipt_fingerprint
        == core.originating_receipt_fingerprint
        and change_file.originating_receipt.receipt.organized_tree.commitment
        == change_file.core.expected_organized_tree_commitment
        and change_file.core.expected_organized_tree_commitment
        == core.organized_tree.commitment
        and preview.imported_change_file_fingerprint
        == authorization.imported_change_file_fingerprint
        == change_file.change_file_fingerprint
    ):
        raise ValueError("Imported Change File receiver bindings differ.")

    report_bytes = read_regular_bytes(root, CONNECTED_CHANGE_MATCH_REPORT_PATH)
    report = _parse_canonical_model(
        root,
        CONNECTED_CHANGE_MATCH_REPORT_PATH,
        ConnectedChangeMatchReport,
    )
    _require_path_neutral_v3_authorities(report)
    if not (
        hashlib.sha256(report_bytes).hexdigest() == core.match_report_sha256
        and report.match_report_fingerprint == core.match_report_fingerprint
        and report.match_report_fingerprint
        == preview.match_report_fingerprint
        == authorization.match_report_fingerprint
        and report.status == "matched"
        and report.receiver_source_commitment == artifacts.inventory.source_commitment
        and report.core_fingerprint == change_file.core_fingerprint
    ):
        raise ValueError("Receiver match report differs from the v3 receipt.")

    markdown_payloads = _original_markdown_payloads(root, artifacts)
    source_graph = build_reference_graph(artifacts.inventory, markdown_payloads)
    recomputed_report = match_connected_change(
        change_file,
        artifacts.inventory,
        source_graph,
        markdown_payloads=markdown_payloads,
    )
    if recomputed_report != report:
        raise ValueError(
            "Receiver match report does not recompute from committed source evidence."
        )
    if derive_reference_rewrites(source_graph, artifacts.plan) != artifacts.graph:
        raise ValueError("Receiver graph does not recompute from original bytes.")

    unprotected_ids = {
        member.file_id for member in artifacts.inventory.files if not member.protected
    }
    target_by_file_id = {
        mapping.receiver_file_id: mapping.target_relative_path
        for mapping in report.mappings
        if mapping.receiver_file_id in unprotected_ids
    }
    expected_plan = build_connected_accepted_plan(
        inventory=artifacts.inventory,
        request=change_file.core.request,
        evidence_fingerprint=(
            change_file.originating_receipt.receipt.evidence_fingerprint
        ),
        result_folder_name=change_file.core.requested_result_folder_name,
        target_by_file_id=target_by_file_id,
        execution_authority="change_file",
    )
    if artifacts.request.request != change_file.core.request or artifacts.plan != (
        expected_plan
    ):
        raise ValueError("Receiver-local accepted plan does not rebind the match.")
    origin = artifacts.execution_origin
    if not (
        isinstance(origin, CapsuleAppliedExecutionOrigin)
        and preview.proposal_basis == "imported_change_file"
        and origin.change_file_fingerprint == change_file.change_file_fingerprint
        and origin.originating_receipt_fingerprint
        == change_file.originating_receipt.receipt_fingerprint
        and origin.match_report_fingerprint == report.match_report_fingerprint
        and origin.receiver_accepted_plan_fingerprint
        == canonical_sha256(artifacts.plan)
        and origin.provider_call_count == 0
        and origin.api_used is False
        and origin.external_network_used is False
    ):
        raise ValueError("capsule_applied provenance differs from receiver proof.")


def _validate_foldweave_derivative_change_authority(
    root: Path,
    envelope: FolderReceiptEnvelopeV3,
    artifacts: _Authorities,
) -> None:
    """Recompute a derivative child without requiring its absent parent payload."""

    core = envelope.receipt
    preview = artifacts.plan_preview
    authorization = artifacts.execution_authorization
    if preview is None or authorization is None:
        raise ValueError("Derivative result lacks reviewed authorization.")
    change_bytes = read_regular_bytes(root, CONNECTED_CHANGE_PATH)
    change_file = parse_connected_change_file_v2(change_bytes)
    _require_path_neutral_v3_authorities(change_file)
    child_core = change_file.core
    if not (
        change_file.originating_receipt == envelope
        and child_core.lineage.generation >= 1
        and change_file.core_fingerprint == core.connected_change_core_fingerprint
        and change_file.core_fingerprint
        == connected_change_core_v2_fingerprint(child_core)
        and child_core.expected_organized_tree_commitment
        == core.organized_tree.commitment
        and core.lineage_generation == child_core.lineage.generation
    ):
        raise ValueError("Child Change File and v3 receipt do not form one proof.")

    report_bytes = read_regular_bytes(root, CONNECTED_CHANGE_MATCH_REPORT_PATH)
    report = _parse_canonical_model(
        root,
        CONNECTED_CHANGE_MATCH_REPORT_PATH,
        ConnectedChangeMatchReport,
    )
    _require_path_neutral_v3_authorities(report)
    lineage = child_core.lineage
    derivative_evidence = artifacts.evidence_ledger
    if not (
        isinstance(derivative_evidence, FolderEvidenceLedgerV2)
        and isinstance(
            derivative_evidence.initial_ledger,
            FolderDerivativeEvidenceLedgerV1,
        )
        and derivative_evidence.initial_ledger.revision_instruction_fingerprint
        == lineage.revision_instruction_fingerprint
        and derivative_evidence.initial_ledger.imported_change_file_fingerprint
        == lineage.parent_change_file_fingerprint
        and derivative_evidence.initial_ledger.match_report_fingerprint
        == report.match_report_fingerprint
        and derivative_evidence.initial_ledger.immediate_parent_candidate_fingerprint
        == lineage.parent_candidate_fingerprint
    ):
        raise ValueError("Derivative evidence differs from immediate-parent lineage.")
    if not (
        report.status == "matched"
        and report.receiver_source_commitment == artifacts.inventory.source_commitment
        and report.match_report_fingerprint == core.match_report_fingerprint
        and hashlib.sha256(report_bytes).hexdigest() == core.match_report_sha256
        and report.core_fingerprint == lineage.parent_core_fingerprint
        and core.imported_change_file_fingerprint
        == lineage.parent_change_file_fingerprint
        == preview.imported_change_file_fingerprint
        == authorization.imported_change_file_fingerprint
        and core.originating_receipt_fingerprint
        == lineage.parent_originating_receipt_fingerprint
        and preview.match_report_fingerprint
        == authorization.match_report_fingerprint
        == report.match_report_fingerprint
        and preview.immediate_parent_candidate_fingerprint
        == lineage.parent_candidate_fingerprint
    ):
        raise ValueError("Immediate-parent lineage differs from receiver review proof.")

    markdown_payloads = _original_markdown_payloads(root, artifacts)
    source_graph = build_reference_graph(artifacts.inventory, markdown_payloads)
    if derive_reference_rewrites(source_graph, artifacts.plan) != artifacts.graph:
        raise ValueError("Derivative graph does not recompute from original bytes.")
    complete_core = build_connected_change_core(
        artifacts.inventory,
        source_graph,
        artifacts.plan,
        request=artifacts.request.request,
        markdown_payloads=markdown_payloads,
        expected_organized_tree_commitment=core.organized_tree.commitment,
        origin_proof_identifiers=(
            artifacts.execution_origin.evidence_fingerprint,
            canonical_sha256(artifacts.plan),
        ),
    )
    expected_child = build_connected_change_core_v2(
        complete_core,
        lineage=lineage,
    )
    if expected_child != child_core:
        raise ValueError("Child Core does not recompute from transaction authorities.")

    inventory_by_id = {item.file_id: item for item in artifacts.inventory.files}
    child_by_origin = {
        item.origin_relative_path: item.logical_member_id for item in child_core.members
    }
    expected_bindings_list: list[ConnectedChangeMemberBindingV1] = []
    for mapping in report.mappings:
        receiver_member = inventory_by_id.get(mapping.receiver_file_id)
        if receiver_member is None:
            raise ValueError("Match report names an unknown transaction-source member.")
        child_member_id = child_by_origin.get(receiver_member.relative_path)
        if child_member_id is None:
            raise ValueError("Child Core omits a matched transaction-source member.")
        expected_bindings_list.append(
            ConnectedChangeMemberBindingV1(
                parent_logical_member_id=mapping.logical_member_id,
                child_logical_member_id=child_member_id,
            )
        )
    expected_bindings = tuple(
        sorted(
            expected_bindings_list,
            key=lambda item: item.parent_logical_member_id,
        )
    )
    if expected_bindings != lineage.member_bindings:
        raise ValueError("Lineage member bindings differ from the committed match.")
    if not (
        artifacts.plan.execution_authority == "gpt_plan"
        and isinstance(artifacts.execution_origin, GptPlannedExecutionOriginV2)
        and artifacts.execution_origin.kind == "gpt_revised_from_change_file"
        and artifacts.execution_origin.imported_change_file_fingerprint
        == core.imported_change_file_fingerprint
        and artifacts.execution_origin.match_report_fingerprint
        == core.match_report_fingerprint
        and artifacts.execution_origin.accepted_plan_fingerprint
        == canonical_sha256(artifacts.plan)
    ):
        raise ValueError("Derivative execution provenance is untruthful.")


def _original_markdown_payloads(
    root: Path,
    artifacts: _Authorities,
) -> dict[str, bytes]:
    """Recover exact receiver-source Markdown bytes from portable proof."""

    rows_by_id = {row.file_id: row for row in artifacts.rows}
    payloads: dict[str, bytes] = {}
    for source_file in artifacts.inventory.files:
        if PurePosixPath(source_file.relative_path).suffix.casefold() not in (
            MARKDOWN_SUFFIXES
        ):
            continue
        row = rows_by_id.get(source_file.file_id)
        if row is None:
            raise ValueError("Markdown source has no complete path-map row.")
        relative_path = (
            f"{ORIGINAL_CONTENT_ROOT}/{source_file.file_id}.bin"
            if row.markdown_rewritten
            else f"data/{row.result_path}"
        )
        payload = read_regular_bytes(root, relative_path)
        if (
            len(payload) != source_file.size
            or hashlib.sha256(payload).hexdigest() != source_file.sha256
        ):
            raise ValueError("Recovered Markdown source bytes differ from snapshot.")
        payloads[source_file.relative_path] = payload
    return payloads


def _validate_exact_artifact_family(
    root: Path,
    envelope: FolderReceiptEnvelopeV2,
    artifacts: _Authorities,
) -> None:
    rewritten_ids = tuple(
        sorted(
            entry.file_id
            for entry in artifacts.ledger.entries
            if entry.markdown_rewritten
        )
    )
    expected_commitments = build_connected_artifact_commitments(
        root,
        original_content_file_ids=rewritten_ids,
        include_match_report=envelope.receipt.execution_role == "receiver",
    )
    if expected_commitments != envelope.receipt.artifact_commitments:
        raise _VerificationBlocked(
            "artifact_set_mismatch",
            "The exact role-specific raw artifact set differs from the receipt.",
        )
    expected_name_atlas_files = {
        commitment.path
        for commitment in expected_commitments
        if commitment.path.startswith("name-atlas/")
    } | {
        CHANGE_RECEIPT_PATH,
        CONNECTED_CHANGE_PATH,
        PROOF_AND_RESTORE_HTML_PATH,
    }
    actual_name_atlas_files = _scan_name_atlas_files(root)
    if actual_name_atlas_files != expected_name_atlas_files:
        raise _VerificationBlocked(
            "artifact_set_mismatch",
            "The portable Name Atlas artifact family contains missing or extra files.",
        )


def _validate_exact_foldweave_artifact_family(
    root: Path,
    envelope: FolderReceiptEnvelopeV3,
    artifacts: _Authorities,
) -> None:
    rewritten_ids = tuple(
        sorted(
            entry.file_id
            for entry in artifacts.ledger.entries
            if entry.markdown_rewritten
        )
    )
    expected_commitments = build_foldweave_artifact_commitments(
        root,
        original_content_file_ids=rewritten_ids,
        execution_role=envelope.receipt.execution_role,
    )
    if expected_commitments != envelope.receipt.artifact_commitments:
        raise _VerificationBlocked(
            "artifact_set_mismatch",
            "The exact Foldweave v3 raw authority set differs from the receipt.",
        )
    expected_name_atlas_files = {
        commitment.path
        for commitment in expected_commitments
        if commitment.path.startswith("name-atlas/")
    } | {
        CHANGE_RECEIPT_PATH,
        CONNECTED_CHANGE_PATH,
        PROOF_AND_RESTORE_HTML_PATH,
    }
    if _scan_name_atlas_files(root) != expected_name_atlas_files:
        raise _VerificationBlocked(
            "artifact_set_mismatch",
            "The Foldweave portable artifact family has missing or extra files.",
        )


def _scan_name_atlas_files(root: Path) -> set[str]:
    proof_root = root / "name-atlas"
    files: set[str] = set()

    def visit(directory: Path) -> None:
        try:
            entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        except OSError as exc:
            raise _VerificationBlocked(
                "artifact_set_mismatch",
                "The portable Name Atlas artifact directory cannot be enumerated.",
            ) from exc
        for entry in entries:
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise _VerificationBlocked(
                    "artifact_set_mismatch",
                    "A portable Name Atlas artifact cannot be inspected.",
                ) from exc
            path = Path(entry.path)
            relative_path = path.relative_to(root).as_posix()
            if stat.S_ISLNK(metadata.st_mode):
                raise _VerificationBlocked(
                    "artifact_set_mismatch",
                    f"A portable artifact is a symlink: {relative_path}.",
                )
            if stat.S_ISDIR(metadata.st_mode):
                visit(path)
            elif stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1:
                files.add(relative_path)
            else:
                raise _VerificationBlocked(
                    "artifact_set_mismatch",
                    f"A portable artifact is linked or special: {relative_path}.",
                )

    visit(proof_root)
    return files


def _compare_supplied_source(source_root: Path, expected: FolderInventory) -> None:
    try:
        supplied = scan_folder(source_root).inventory
    except (FolderScanError, OSError, ValueError) as exc:
        raise _VerificationBlocked(
            "supplied_source_unreadable",
            "The optional source cannot be read under the supported folder contract.",
        ) from exc
    if supplied != expected:
        raise _VerificationBlocked(
            "supplied_source_mismatch",
            "The optional source differs from the committed source description.",
        )


def _require_candidate_root(value: Path) -> Path:
    if not isinstance(value, Path):
        raise ValueError("Result root must be a pathlib.Path.")
    metadata = value.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError("Result root must be a non-symlink directory.")
    return value.resolve(strict=True)


def _passed(
    checks: list[FolderReceiptVerificationCheck],
    check_id: str,
    detail: str,
) -> None:
    checks.append(
        FolderReceiptVerificationCheck(check_id=check_id, passed=True, detail=detail)
    )


def _blocked(
    checks: list[FolderReceiptVerificationCheck],
    check_id: str,
    detail: str,
    *,
    envelope: FolderReceiptEnvelopeV2 | FolderReceiptEnvelopeV3 | None = None,
    verification_schema_version: Literal[
        "folder-receipt-verification.v2",
        "folder-receipt-verification.v3",
    ]
    | None = None,
) -> ConnectedReceiptVerification:
    checks.append(
        FolderReceiptVerificationCheck(
            check_id=check_id,
            passed=False,
            detail=detail or "Verification blocked.",
        )
    )
    return _result(
        checks,
        envelope=envelope,
        verification_schema_version=verification_schema_version,
    )


def _result(
    checks: list[FolderReceiptVerificationCheck],
    *,
    envelope: FolderReceiptEnvelopeV2 | FolderReceiptEnvelopeV3 | None = None,
    organized_tree_commitment: str | None = None,
    verification_schema_version: Literal[
        "folder-receipt-verification.v2",
        "folder-receipt-verification.v3",
    ]
    | None = None,
) -> ConnectedReceiptVerification:
    failed = tuple(check.check_id for check in checks if not check.passed)
    is_v3 = (
        verification_schema_version == "folder-receipt-verification.v3"
        or isinstance(envelope, FolderReceiptEnvelopeV3)
    )
    result_type = (
        FoldweaveReceiptVerificationV3 if is_v3 else ConnectedReceiptVerification
    )
    return result_type(
        status=(
            ConnectedReceiptVerificationStatus.BLOCKED
            if failed
            else ConnectedReceiptVerificationStatus.VERIFIED
        ),
        job_id=None if envelope is None else envelope.receipt.job_id,
        receipt_fingerprint=(
            None if envelope is None else envelope.receipt_fingerprint
        ),
        organized_tree_commitment=organized_tree_commitment,
        checks=tuple(checks),
        failed_check_ids=failed,
    )
