"""C0 origin and provider-free receiver transactions over the shared copy engine."""

from __future__ import annotations

import hashlib
import os
import stat
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import cast

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
    build_connected_accepted_plan,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CHANGE_FILE_BYTES,
    CapsuleAppliedExecutionOrigin,
    ConnectedChangeError,
    ConnectedChangeFile,
    ConnectedChangeMatchReport,
    FolderExecutionOrigin,
    GptPlannedExecutionOrigin,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    build_connected_change_core,
    create_connected_change_file,
    parse_connected_change_file,
)
from name_atlas.folder_refactor.connected_change.evidence import (
    build_deterministic_origin_evidence,
)
from name_atlas.folder_refactor.connected_change.matcher import (
    match_connected_change,
)
from name_atlas.folder_refactor.connected_change.organized_tree import (
    OrganizedTreeCommitmentMismatch,
    OrganizedTreeSnapshot,
    require_organized_tree_commitment,
    scan_organized_tree,
)
from name_atlas.folder_refactor.connected_change.proof import (
    render_connected_proof_html,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_MATCH_REPORT_PATH,
    CONNECTED_CHANGE_PATH,
    EXECUTION_ORIGIN_PATH,
    build_connected_artifact_commitments,
    build_connected_receipt,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.inventory import FolderScan, scan_folder
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.markdown_links import MARKDOWN_SUFFIXES
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    EVIDENCE_LEDGER_PATH,
    PROOF_AND_RESTORE_HTML_PATH,
    canonical_portable_json_bytes,
    write_new_portable_json,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderChangeLedger,
    FolderEvidenceLedger,
    FolderPathMapRow,
    FolderStagedDataMember,
    FolderUserRequestArtifact,
)
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.folder_refactor.transaction import (
    FolderBagWriter,
    FolderProofFinalizer,
    FolderRunResult,
    FolderTransactionError,
    FolderTransactionPaths,
    _write_portable_bytes,
    execute_accepted_folder_plan,
    scan_folder_with_references,
)
from name_atlas.ports import PackageValidator
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.verification.bagit_validator import BagItPackageValidator


@dataclass(frozen=True, slots=True)
class ConnectedChangeRunResult:
    """One promoted result and its portable Connected Change identities."""

    folder_run: FolderRunResult
    change_file_path: Path
    change_file_fingerprint: str
    receipt_fingerprint: str
    organized_tree_commitment: str
    execution_origin: FolderExecutionOrigin
    match_report: ConnectedChangeMatchReport | None


@dataclass(frozen=True, slots=True)
class PreparedConnectedChangeOrigin:
    """Source-bound origin plan prepared before any result write occurs."""

    initial_scan: FolderScan
    reference_graph: FolderReferenceGraph
    request: str
    accepted_plan: FolderAcceptedPlanV2
    execution_origin: GptPlannedExecutionOrigin
    evidence_ledger: FolderEvidenceLedger
    markdown_payloads: Mapping[str, bytes]


@dataclass(frozen=True, slots=True)
class PreparedConnectedChangeApplication:
    """Source- and Change-File-bound receiver plan prepared before execution."""

    initial_scan: FolderScan
    reference_graph: FolderReferenceGraph
    request: str
    accepted_plan: FolderAcceptedPlanV2
    execution_origin: CapsuleAppliedExecutionOrigin
    external_change_file: _StableExternalFile
    change_file: ConnectedChangeFile
    match_report: ConnectedChangeMatchReport


PreparedConnectedChange = (
    PreparedConnectedChangeOrigin | PreparedConnectedChangeApplication
)


@dataclass(frozen=True, slots=True)
class _StableExternalFile:
    path: Path
    bytes: bytes
    identity: tuple[int, int, int, int]
    sha256: str


class _OriginFinalizer(FolderProofFinalizer):
    def __init__(
        self,
        *,
        job_id: str,
        execution_origin: GptPlannedExecutionOrigin,
        evidence_ledger: FolderEvidenceLedger,
        markdown_payloads: Mapping[str, bytes],
    ) -> None:
        self.job_id = job_id
        self.execution_origin = execution_origin
        self.evidence_ledger = evidence_ledger
        self.markdown_payloads = dict(markdown_payloads)
        self.change_file: ConnectedChangeFile | None = None
        self.organized_tree: OrganizedTreeSnapshot | None = None

    def finalize(self, **values: object) -> str:
        pending_root = cast(Path, values["pending_root"])
        initial_scan = cast(FolderScan, values["initial_scan"])
        user_request = cast(FolderUserRequestArtifact, values["user_request"])
        accepted_plan = _require_v2_plan(values["accepted_plan"])
        reference_graph = values["reference_graph"]
        path_rows = cast(tuple[FolderPathMapRow, ...], values["path_rows"])
        change_ledger = cast(FolderChangeLedger, values["change_ledger"])
        staged_members = cast(
            tuple[FolderStagedDataMember, ...], values["staged_members"]
        )
        organized = scan_organized_tree(pending_root / "data")
        core = build_connected_change_core(
            initial_scan.inventory,
            reference_graph,
            accepted_plan,
            request=user_request.request,
            markdown_payloads=self.markdown_payloads,
            expected_organized_tree_commitment=organized.commitment,
            origin_proof_identifiers=(
                self.execution_origin.evidence_fingerprint,
                self.execution_origin.accepted_plan_fingerprint,
            ),
        )
        write_new_portable_json(
            pending_root,
            EXECUTION_ORIGIN_PATH,
            self.execution_origin,
        )
        write_new_portable_json(
            pending_root,
            EVIDENCE_LEDGER_PATH,
            self.evidence_ledger,
        )
        rewritten_ids = tuple(
            sorted(
                entry.file_id
                for entry in change_ledger.entries
                if entry.markdown_rewritten
            )
        )
        commitments = build_connected_artifact_commitments(
            pending_root,
            original_content_file_ids=rewritten_ids,
            include_match_report=False,
        )
        envelope = build_connected_receipt(
            execution_role="origin",
            job_id=self.job_id,
            inventory=initial_scan.inventory,
            user_request=user_request,
            accepted_plan=accepted_plan,
            reference_graph=reference_graph,
            path_rows=path_rows,
            change_ledger=change_ledger,
            report=values["report"],
            execution_origin=self.execution_origin,
            evidence_ledger=self.evidence_ledger,
            artifact_commitments=commitments,
            staged_members=staged_members,
            staged_data_commitment=cast(str, values["staged_data_commitment"]),
            organized_tree=organized,
            producer_bagit_validation=values["producer_bagit_validation"],
            connected_change_core_fingerprint=canonical_sha256(core),
        )
        write_new_portable_json(pending_root, CHANGE_RECEIPT_PATH, envelope)
        change_file = create_connected_change_file(
            core,
            originating_receipt=envelope,
        )
        write_new_portable_json(pending_root, CONNECTED_CHANGE_PATH, change_file)
        _write_portable_bytes(
            Path(PROOF_AND_RESTORE_HTML_PATH),
            render_connected_proof_html(
                envelope.receipt_fingerprint,
                organized.commitment,
            ),
            pending_root,
        )
        _finalize_and_verify(
            pending_root=pending_root,
            bag_writer=values["bag_writer"],
            package_validator=values["package_validator"],
            receipt_fingerprint=envelope.receipt_fingerprint,
        )
        self.change_file = change_file
        self.organized_tree = organized
        return envelope.receipt_fingerprint

    def validate_before_promotion(self) -> None:
        """The origin has no non-source external authority to revalidate."""


class _ReceiverFinalizer(FolderProofFinalizer):
    def __init__(
        self,
        *,
        job_id: str,
        external_change_file: _StableExternalFile,
        change_file: ConnectedChangeFile,
        match_report: ConnectedChangeMatchReport,
        execution_origin: CapsuleAppliedExecutionOrigin,
    ) -> None:
        self.job_id = job_id
        self.external_change_file = external_change_file
        self.change_file = change_file
        self.match_report = match_report
        self.execution_origin = execution_origin
        self.organized_tree: OrganizedTreeSnapshot | None = None

    def finalize(self, **values: object) -> str:
        pending_root = cast(Path, values["pending_root"])
        initial_scan = cast(FolderScan, values["initial_scan"])
        user_request = cast(FolderUserRequestArtifact, values["user_request"])
        accepted_plan = _require_v2_plan(values["accepted_plan"])
        reference_graph = values["reference_graph"]
        path_rows = cast(tuple[FolderPathMapRow, ...], values["path_rows"])
        change_ledger = cast(FolderChangeLedger, values["change_ledger"])
        staged_members = cast(
            tuple[FolderStagedDataMember, ...], values["staged_members"]
        )
        organized = require_organized_tree_commitment(
            scan_organized_tree(pending_root / "data"),
            self.change_file.core.expected_organized_tree_commitment,
        )
        write_new_portable_json(
            pending_root,
            EXECUTION_ORIGIN_PATH,
            self.execution_origin,
        )
        _write_portable_bytes(
            Path(CONNECTED_CHANGE_PATH),
            self.external_change_file.bytes,
            pending_root,
        )
        match_bytes = canonical_portable_json_bytes(self.match_report)
        _write_portable_bytes(
            Path(CONNECTED_CHANGE_MATCH_REPORT_PATH),
            match_bytes,
            pending_root,
        )
        rewritten_ids = tuple(
            sorted(
                entry.file_id
                for entry in change_ledger.entries
                if entry.markdown_rewritten
            )
        )
        commitments = build_connected_artifact_commitments(
            pending_root,
            original_content_file_ids=rewritten_ids,
            include_match_report=True,
        )
        origin_receipt_fingerprint = _origin_receipt_fingerprint(self.change_file)
        envelope = build_connected_receipt(
            execution_role="receiver",
            job_id=self.job_id,
            inventory=initial_scan.inventory,
            user_request=user_request,
            accepted_plan=accepted_plan,
            reference_graph=reference_graph,
            path_rows=path_rows,
            change_ledger=change_ledger,
            report=values["report"],
            execution_origin=self.execution_origin,
            artifact_commitments=commitments,
            staged_members=staged_members,
            staged_data_commitment=cast(str, values["staged_data_commitment"]),
            organized_tree=organized,
            producer_bagit_validation=values["producer_bagit_validation"],
            connected_change_core_fingerprint=self.change_file.core_fingerprint,
            imported_change_file_fingerprint=(self.change_file.change_file_fingerprint),
            imported_change_file_sha256=self.external_change_file.sha256,
            originating_receipt_fingerprint=origin_receipt_fingerprint,
            match_report_fingerprint=self.match_report.match_report_fingerprint,
            match_report_sha256=hashlib.sha256(match_bytes).hexdigest(),
        )
        write_new_portable_json(pending_root, CHANGE_RECEIPT_PATH, envelope)
        _write_portable_bytes(
            Path(PROOF_AND_RESTORE_HTML_PATH),
            render_connected_proof_html(
                envelope.receipt_fingerprint,
                organized.commitment,
            ),
            pending_root,
        )
        _finalize_and_verify(
            pending_root=pending_root,
            bag_writer=values["bag_writer"],
            package_validator=values["package_validator"],
            receipt_fingerprint=envelope.receipt_fingerprint,
        )
        _require_external_unchanged(self.external_change_file)
        self.organized_tree = organized
        return envelope.receipt_fingerprint

    def validate_before_promotion(self) -> None:
        """Require the imported Change File to remain byte-identical."""

        _require_external_unchanged(self.external_change_file)


def create_connected_change_origin(
    *,
    source_root: Path,
    output_parent: Path,
    request: str,
    result_folder_name: str,
    target_by_original_path: Mapping[str, str],
    bag_writer: FolderBagWriter | None = None,
    package_validator: PackageValidator | None = None,
) -> ConnectedChangeRunResult:
    """Create one deterministic-development origin result and Change File."""

    job_id = uuid.uuid4().hex
    prepared = prepare_connected_change_origin(
        job_id=job_id,
        source_root=source_root,
        request=request,
        result_folder_name=result_folder_name,
        target_by_original_path=target_by_original_path,
    )
    return execute_prepared_connected_change(
        prepared=prepared,
        output_parent=output_parent,
        job_id=job_id,
        bag_writer=bag_writer,
        package_validator=package_validator,
    )


def prepare_connected_change_origin(
    *,
    job_id: str,
    source_root: Path,
    request: str,
    result_folder_name: str,
    target_by_original_path: Mapping[str, str],
) -> PreparedConnectedChangeOrigin:
    """Compile one deterministic-development origin without writing a result."""

    initial_scan, graph = scan_folder_with_references(source_root)
    expected_paths = {item.relative_path for item in initial_scan.inventory.files}
    if set(target_by_original_path) != expected_paths:
        raise ConnectedChangeError(
            "origin_target_map_incomplete",
            "Origin targets must account for every source file exactly once.",
        )
    protected_target_changes = tuple(
        item.relative_path
        for item in initial_scan.inventory.files
        if item.protected
        and target_by_original_path[item.relative_path] != item.relative_path
    )
    if protected_target_changes:
        raise ConnectedChangeError(
            "origin_protected_target_invalid",
            "Origin targets must preserve every protected member at its exact "
            f"relative path: {protected_target_changes!r}.",
        )
    target_by_id = {
        item.file_id: target_by_original_path[item.relative_path]
        for item in initial_scan.inventory.files
        if not item.protected
    }
    from name_atlas.folder_refactor.planner_evidence import (
        create_initial_evidence_ledger,
    )

    evidence_fingerprint = create_initial_evidence_ledger(
        initial_scan.inventory,
        request,
    ).evidence_fingerprint
    plan = build_connected_accepted_plan(
        inventory=initial_scan.inventory,
        request=request,
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name=result_folder_name,
        target_by_file_id=target_by_id,
        execution_authority="gpt_plan",
    )
    origin, evidence_ledger = build_deterministic_origin_evidence(
        job_id=job_id,
        inventory=initial_scan.inventory,
        request=request,
        accepted_plan=plan,
    )
    return PreparedConnectedChangeOrigin(
        initial_scan=initial_scan,
        reference_graph=graph,
        request=request,
        accepted_plan=plan,
        execution_origin=origin,
        evidence_ledger=evidence_ledger,
        markdown_payloads=_read_markdown_payloads(initial_scan),
    )


def rehydrate_prepared_connected_change_origin(
    *,
    source_root: Path,
    request: str,
    accepted_plan: FolderAcceptedPlanV2,
    execution_origin: GptPlannedExecutionOrigin,
    evidence_ledger: FolderEvidenceLedger,
) -> PreparedConnectedChangeOrigin:
    """Rebind one persisted accepted origin to its unchanged local source."""

    initial_scan, graph = scan_folder_with_references(source_root)
    from name_atlas.folder_refactor.connected_change.accepted_plan import (
        validate_connected_accepted_plan,
    )
    from name_atlas.folder_refactor.connected_change.receipt import (
        validate_connected_evidence_ledger,
    )
    from name_atlas.folder_refactor.receipt_builder import (
        build_folder_user_request_artifact,
    )

    validate_connected_accepted_plan(
        inventory=initial_scan.inventory,
        request=request,
        plan=accepted_plan,
    )
    validate_connected_evidence_ledger(
        job_id=evidence_ledger.job_id,
        inventory=initial_scan.inventory,
        user_request=build_folder_user_request_artifact(request),
        accepted_plan=accepted_plan,
        execution_origin=execution_origin,
        evidence_ledger=evidence_ledger,
    )
    return PreparedConnectedChangeOrigin(
        initial_scan=initial_scan,
        reference_graph=graph,
        request=request,
        accepted_plan=accepted_plan,
        execution_origin=execution_origin,
        evidence_ledger=evidence_ledger,
        markdown_payloads=_read_markdown_payloads(initial_scan),
    )


def apply_connected_change(
    *,
    change_file_path: Path,
    source_root: Path,
    output_parent: Path,
    bag_writer: FolderBagWriter | None = None,
    package_validator: PackageValidator | None = None,
) -> ConnectedChangeRunResult:
    """Apply one Change File deterministically without provider or budget access."""

    prepared = prepare_connected_change_application(
        change_file_path=change_file_path,
        source_root=source_root,
    )
    return execute_prepared_connected_change(
        prepared=prepared,
        output_parent=output_parent,
        job_id=uuid.uuid4().hex,
        bag_writer=bag_writer,
        package_validator=package_validator,
    )


def prepare_connected_change_application(
    *,
    change_file_path: Path,
    source_root: Path,
) -> PreparedConnectedChangeApplication:
    """Match one receiver without provider, budget, or result mutation."""

    external = _read_stable_external_file(change_file_path)
    change_file = parse_connected_change_file(external.bytes)
    if canonical_portable_json_bytes(change_file) != external.bytes:
        raise ConnectedChangeError(
            "change_file_schema_invalid",
            "Change File must use exact canonical JSON serialization.",
        )
    initial_scan, graph = scan_folder_with_references(source_root)
    markdown_payloads = _read_markdown_payloads(initial_scan)
    match_report = match_connected_change(
        change_file,
        initial_scan.inventory,
        graph,
        markdown_payloads=markdown_payloads,
    )
    if match_report.status != "matched":
        raise ConnectedChangeError(
            match_report.blocker_code or "receiver_match_blocked",
            match_report.detail,
        )
    unprotected_ids = {
        item.file_id for item in initial_scan.inventory.files if not item.protected
    }
    target_by_id = {
        item.receiver_file_id: item.target_relative_path
        for item in match_report.mappings
        if item.receiver_file_id in unprotected_ids
    }
    evidence_fingerprint = _origin_evidence_fingerprint(change_file)
    plan = build_connected_accepted_plan(
        inventory=initial_scan.inventory,
        request=change_file.core.request,
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name=change_file.core.requested_result_folder_name,
        target_by_file_id=target_by_id,
        execution_authority="change_file",
    )
    origin = CapsuleAppliedExecutionOrigin(
        change_file_fingerprint=change_file.change_file_fingerprint,
        originating_receipt_fingerprint=_origin_receipt_fingerprint(change_file),
        match_report_fingerprint=match_report.match_report_fingerprint,
        receiver_accepted_plan_fingerprint=canonical_sha256(plan),
    )
    return PreparedConnectedChangeApplication(
        initial_scan=initial_scan,
        reference_graph=graph,
        request=change_file.core.request,
        accepted_plan=plan,
        execution_origin=origin,
        external_change_file=external,
        change_file=change_file,
        match_report=match_report,
    )


def execute_prepared_connected_change(
    *,
    prepared: PreparedConnectedChange,
    output_parent: Path,
    job_id: str,
    transaction_paths: FolderTransactionPaths | None = None,
    bag_writer: FolderBagWriter | None = None,
    package_validator: PackageValidator | None = None,
) -> ConnectedChangeRunResult:
    """Execute one persisted preparation through the shared copy transaction."""

    if isinstance(prepared, PreparedConnectedChangeOrigin):
        finalizer: _OriginFinalizer | _ReceiverFinalizer = _OriginFinalizer(
            job_id=job_id,
            execution_origin=prepared.execution_origin,
            evidence_ledger=prepared.evidence_ledger,
            markdown_payloads=prepared.markdown_payloads,
        )
    else:
        finalizer = _ReceiverFinalizer(
            job_id=job_id,
            external_change_file=prepared.external_change_file,
            change_file=prepared.change_file,
            match_report=prepared.match_report,
            execution_origin=prepared.execution_origin,
        )
    try:
        run = execute_accepted_folder_plan(
            initial_scan=prepared.initial_scan,
            output_parent=output_parent,
            request=prepared.request,
            accepted_plan=prepared.accepted_plan,
            reference_graph=prepared.reference_graph,
            bag_writer=BagItWriter() if bag_writer is None else bag_writer,
            package_validator=(
                BagItPackageValidator()
                if package_validator is None
                else package_validator
            ),
            proof_finalizer=finalizer,
            transaction_paths=transaction_paths,
        )
    except FolderTransactionError as exc:
        connected_error = _project_connected_transaction_error(exc)
        if connected_error is not None:
            raise connected_error from exc
        raise
    if finalizer.organized_tree is None:
        raise AssertionError("Connected Change finalizer lacks convergence proof.")
    if isinstance(finalizer, _OriginFinalizer):
        if finalizer.change_file is None:
            raise AssertionError("Origin finalizer returned without a Change File.")
        change_file = finalizer.change_file
        match_report = None
    else:
        change_file = finalizer.change_file
        match_report = finalizer.match_report
    return ConnectedChangeRunResult(
        folder_run=run,
        change_file_path=run.result_root / CONNECTED_CHANGE_PATH,
        change_file_fingerprint=change_file.change_file_fingerprint,
        receipt_fingerprint=_require_receipt_fingerprint(run),
        organized_tree_commitment=finalizer.organized_tree.commitment,
        execution_origin=prepared.execution_origin,
        match_report=match_report,
    )


def _project_connected_transaction_error(
    error: FolderTransactionError,
) -> ConnectedChangeError | None:
    """Preserve stable Connected Change blockers across the shared transaction."""

    cause: BaseException | None = error.__cause__
    while cause is not None:
        if isinstance(cause, ConnectedChangeError):
            return cause
        if isinstance(cause, OrganizedTreeCommitmentMismatch):
            return ConnectedChangeError(
                OrganizedTreeCommitmentMismatch.blocker_id,
                str(cause),
            )
        cause = cause.__cause__
    return None


def _read_markdown_payloads(scan: FolderScan) -> dict[str, bytes]:
    payloads = {
        item.relative_path: (scan.source_root / item.relative_path).read_bytes()
        for item in scan.inventory.files
        if PurePosixPath(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
    }
    for item in scan.inventory.files:
        payload = payloads.get(item.relative_path)
        if payload is not None and (
            len(payload) != item.size
            or hashlib.sha256(payload).hexdigest() != item.sha256
        ):
            raise ConnectedChangeError(
                "source_changed",
                f"Markdown source changed: {item.relative_path}",
            )
    rescanned = scan_folder(scan.source_root)
    if (
        rescanned.inventory != scan.inventory
        or rescanned.local_file_identities != scan.local_file_identities
        or rescanned.local_directory_identities != scan.local_directory_identities
    ):
        raise ConnectedChangeError(
            "source_changed",
            "Source changed while Connected Change evidence was read.",
        )
    return payloads


def _read_stable_external_file(path: Path) -> _StableExternalFile:
    if not isinstance(path, Path) or not path.is_absolute():
        raise ConnectedChangeError(
            "change_file_schema_invalid",
            "Change File path must be an absolute pathlib.Path.",
        )
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise ConnectedChangeError(
            "change_file_schema_invalid",
            "Change File cannot be opened safely.",
        ) from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ConnectedChangeError(
                "change_file_schema_invalid",
                "Change File must be a regular file.",
            )
        if before.st_size > MAX_CHANGE_FILE_BYTES:
            raise ConnectedChangeError(
                "change_file_too_large",
                f"Change File exceeds {MAX_CHANGE_FILE_BYTES} bytes.",
            )
        chunks = []
        digest = hashlib.sha256()
        while chunk := os.read(descriptor, 1024 * 1024):
            chunks.append(chunk)
            digest.update(chunk)
        after = os.fstat(descriptor)
        identity = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        if identity != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise ConnectedChangeError(
                "change_file_changed",
                "Change File changed while being read.",
            )
    finally:
        os.close(descriptor)
    payload = b"".join(chunks)
    if len(payload) != before.st_size:
        raise ConnectedChangeError(
            "change_file_changed",
            "Change File size changed while being read.",
        )
    return _StableExternalFile(
        path=path,
        bytes=payload,
        identity=identity,
        sha256=digest.hexdigest(),
    )


def _require_external_unchanged(expected: _StableExternalFile) -> None:
    current = _read_stable_external_file(expected.path)
    if (
        current.identity != expected.identity
        or current.sha256 != expected.sha256
        or current.bytes != expected.bytes
    ):
        raise ConnectedChangeError(
            "change_file_changed",
            "Change File changed during receiver execution.",
        )


def _origin_receipt_fingerprint(change_file: ConnectedChangeFile) -> str:
    return change_file.originating_receipt.receipt_fingerprint


def _origin_evidence_fingerprint(change_file: ConnectedChangeFile) -> str:
    return change_file.originating_receipt.receipt.evidence_fingerprint


def _require_v2_plan(value: object) -> FolderAcceptedPlanV2:
    if not isinstance(value, FolderAcceptedPlanV2):
        raise ValueError("Connected Change finalization requires accepted-plan v2.")
    return value


def _require_receipt_fingerprint(run: FolderRunResult) -> str:
    if run.receipt_fingerprint is None:
        raise AssertionError("Connected Change result lacks its receipt fingerprint.")
    return run.receipt_fingerprint


def _finalize_and_verify(
    *,
    pending_root: Path,
    bag_writer: object,
    package_validator: object,
    receipt_fingerprint: str,
) -> None:
    cast(FolderBagWriter, bag_writer).finalize_tagmanifest(pending_root)
    package = cast(PackageValidator, package_validator).validate(pending_root)
    if not package.valid:
        raise ValueError("Final Connected Change BagIt validation failed.")
    verification = verify_connected_result(pending_root)
    if (
        verification.status is not ConnectedReceiptVerificationStatus.VERIFIED
        or verification.receipt_fingerprint != receipt_fingerprint
    ):
        failures = "; ".join(
            f"{check.check_id}: {check.detail}"
            for check in verification.checks
            if not check.passed
        )
        raise ValueError(
            "Independent Connected Change verification blocked: " + failures
        )
