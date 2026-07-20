"""Transaction-specific reconstruction from a verified v2 or v3 result."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Protocol, cast
from zoneinfo import ZoneInfo

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    parse_folder_receipt_envelope_any,
)
from name_atlas.folder_refactor.contracts import FolderInventory
from name_atlas.folder_refactor.inventory import FolderScanError, scan_folder
from name_atlas.folder_refactor.portable_artifacts import (
    ACCEPTED_PLAN_PATH,
    CHANGE_RECEIPT_PATH,
    FORWARD_PATH_MAP_PATH,
    ORIGINAL_CONTENT_ROOT,
    REVERSE_PATH_MAP_PATH,
    SOURCE_SNAPSHOT_PATH,
    FolderPortableArtifactError,
    parse_folder_path_map,
    parse_portable_model,
    read_regular_bytes,
)
from name_atlas.folder_refactor.receipt_contracts import (
    FolderPathMapRow,
    FolderRestoreCheck,
    FolderRestoreReport,
)
from name_atlas.folder_refactor.reconstruction import (
    FolderReconstructionError,
    _copy_verified_member,
    _create_owned_pending,
    _ensure_destination_directory,
    _fsync_directory,
    _OwnedPendingDirectory,
    _remove_owned_pending,
    _resolve_absent_destination,
)
from name_atlas.verification.promotion import promote_directory_no_replace

oslo_tz = ZoneInfo("Europe/Oslo")


class _ArtifactCommitment(Protocol):
    path: str
    size: int
    sha256: str


class _ReceiptCore(Protocol):
    execution_role: str
    source_commitment: str
    artifact_commitments: tuple[_ArtifactCommitment, ...]


class _ReceiptEnvelope(Protocol):
    receipt: _ReceiptCore
    receipt_fingerprint: str


class _VerificationResult(Protocol):
    status: object
    receipt_fingerprint: str | None
    failed_check_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _LoadedReceiverAuthorities:
    inventory_bytes: bytes
    accepted_plan_bytes: bytes
    receipt_bytes: bytes
    forward_bytes: bytes
    reverse_bytes: bytes
    inventory: FolderInventory
    accepted_plan: FolderAcceptedPlanV2
    envelope: object
    path_rows: tuple[FolderPathMapRow, ...]


def restore_connected_result(
    result_root: Path,
    destination: Path,
    *,
    source_root: Path | None = None,
) -> FolderRestoreReport:
    """Verify a result and recreate that transaction's own original layout."""

    verification = _verify_connected_result(result_root)
    verification_fingerprint = _require_verified(verification)

    try:
        root = result_root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "The verified Connected Change result cannot be reopened safely.",
        ) from exc
    final_destination = _resolve_absent_destination(
        destination,
        result_root=root,
        source_root=source_root,
        require_result_sibling=False,
    )
    authorities = _load_receiver_authorities(root)
    execution_role = _validate_receiver_authorities(
        authorities,
        verification_fingerprint=verification_fingerprint,
    )

    pending: _OwnedPendingDirectory | None = None
    promoted = False
    try:
        pending = _create_owned_pending(final_destination)
        for row in authorities.path_rows:
            source_relative_path = (
                f"{ORIGINAL_CONTENT_ROOT}/{row.file_id}.bin"
                if row.markdown_rewritten
                else f"data/{row.result_path}"
            )
            _copy_verified_member(
                source_root=root,
                source_relative_path=source_relative_path,
                destination=pending,
                destination_relative_path=row.original_path,
                expected_size=row.original_size,
                expected_sha256=row.original_sha256,
            )
        for empty_directory in authorities.inventory.empty_directories:
            _ensure_destination_directory(
                pending,
                empty_directory.relative_path,
            )
        _fsync_directory(pending.path)

        try:
            restored_inventory = scan_folder(pending.path).inventory
        except (FolderScanError, OSError, ValueError) as exc:
            raise FolderReconstructionError(
                "reconstructed_inventory_mismatch",
                "The pending receiver reconstruction is outside the supported "
                "folder contract.",
            ) from exc
        if restored_inventory != authorities.inventory:
            raise FolderReconstructionError(
                "reconstructed_inventory_mismatch",
                "Reconstructed receiver paths, bytes, or empty directories differ "
                "from this result's own source snapshot.",
            )

        repeated_verification = _verify_connected_result(root)
        if _require_verified(repeated_verification) != verification_fingerprint:
            raise FolderReconstructionError(
                "receipt_changed",
                "The Connected Change result changed during reconstruction.",
            )
        _fsync_directory(pending.parent)
        try:
            promote_directory_no_replace(pending.path, final_destination)
        except (FileExistsError, OSError) as exc:
            raise FolderReconstructionError(
                "promotion_failed",
                "The receiver reconstruction could not be promoted without "
                "replacement.",
            ) from exc
        promoted = True
        role_label = {
            "origin": "origin",
            "receiver": "receiver",
            "derivative": "selected-source",
        }[execution_role]
        return FolderRestoreReport(
            receipt_fingerprint=verification_fingerprint,
            source_commitment=authorities.inventory.source_commitment,
            destination=final_destination,
            completed_at=datetime.now(oslo_tz),
            restored_file_count=len(authorities.inventory.files),
            restored_bytes=authorities.inventory.total_bytes,
            restored_empty_directory_count=len(authorities.inventory.empty_directories),
            checks=(
                FolderRestoreCheck(
                    check_id="connected_change_receipt_verified",
                    detail=(
                        "Independent source-free Connected Change verification "
                        "passed before and after reconstruction."
                    ),
                ),
                FolderRestoreCheck(
                    check_id=f"{role_label}_original_paths_recreated",
                    detail=(
                        f"Every {role_label}-local source path was recreated "
                        f"exactly once from the {role_label} receipt."
                    ),
                ),
                FolderRestoreCheck(
                    check_id=f"{role_label}_original_bytes_recreated",
                    detail=(
                        f"Every reconstructed file matches the {role_label} "
                        "snapshot's exact size and SHA-256."
                    ),
                ),
                FolderRestoreCheck(
                    check_id=f"{role_label}_empty_directories_recreated",
                    detail=(
                        f"Every explicit empty directory in the {role_label} snapshot "
                        "was recreated."
                    ),
                ),
                FolderRestoreCheck(
                    check_id="destination_promoted_no_replace",
                    detail=(
                        "The receiver reconstruction was promoted only while the "
                        "destination was absent."
                    ),
                ),
            ),
        )
    except FolderReconstructionError:
        raise
    except Exception as exc:
        raise FolderReconstructionError(
            "reconstruction_copy_failed",
            "Copy-only receiver reconstruction failed before promotion.",
        ) from exc
    finally:
        if pending is not None and not promoted:
            try:
                _remove_owned_pending(pending)
            except OSError as cleanup_error:
                raise FolderReconstructionError(
                    "pending_cleanup_failed",
                    "The product-owned pending receiver reconstruction could not "
                    "be removed.",
                ) from cleanup_error


def _verify_connected_result(result_root: Path) -> _VerificationResult:
    from name_atlas.folder_refactor.connected_change.verification import (
        verify_connected_result,
    )

    return verify_connected_result(result_root)


def _require_verified(verification: _VerificationResult) -> str:
    status = getattr(verification.status, "value", verification.status)
    if status != "verified":
        raise FolderReconstructionError(
            "receipt_verification_blocked",
            "The result must pass Connected Change verification before reconstruction.",
            failed_check_ids=verification.failed_check_ids,
        )
    if verification.receipt_fingerprint is None:
        raise FolderReconstructionError(
            "receipt_verification_blocked",
            "Verified Connected Change result lacks a receipt fingerprint.",
        )
    return verification.receipt_fingerprint


def _load_receiver_authorities(root: Path) -> _LoadedReceiverAuthorities:
    try:
        inventory_bytes = read_regular_bytes(root, SOURCE_SNAPSHOT_PATH)
        accepted_plan_bytes = read_regular_bytes(root, ACCEPTED_PLAN_PATH)
        receipt_bytes = read_regular_bytes(root, CHANGE_RECEIPT_PATH)
        forward_bytes = read_regular_bytes(root, FORWARD_PATH_MAP_PATH)
        reverse_bytes = read_regular_bytes(root, REVERSE_PATH_MAP_PATH)
        inventory = parse_portable_model(inventory_bytes, FolderInventory)
        accepted_plan = parse_portable_model(
            accepted_plan_bytes,
            FolderAcceptedPlanV2,
        )
        envelope = parse_folder_receipt_envelope_any(receipt_bytes)
        forward_rows = parse_folder_path_map(forward_bytes, reverse=False)
        reverse_rows = parse_folder_path_map(reverse_bytes, reverse=True)
    except (FolderPortableArtifactError, ValueError) as exc:
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Verified receiver authorities could not be reopened strictly.",
        ) from exc
    if forward_rows != reverse_rows:
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Receiver forward and reverse maps are not exact inverses.",
        )
    return _LoadedReceiverAuthorities(
        inventory_bytes=inventory_bytes,
        accepted_plan_bytes=accepted_plan_bytes,
        receipt_bytes=receipt_bytes,
        forward_bytes=forward_bytes,
        reverse_bytes=reverse_bytes,
        inventory=inventory,
        accepted_plan=accepted_plan,
        envelope=envelope,
        path_rows=forward_rows,
    )


def _validate_receiver_authorities(
    authorities: _LoadedReceiverAuthorities,
    *,
    verification_fingerprint: str,
) -> str:
    envelope = cast(_ReceiptEnvelope, authorities.envelope)
    inventory = authorities.inventory
    plan = authorities.accepted_plan
    expected_authority = {
        "origin": "gpt_plan",
        "receiver": "change_file",
        "derivative": "gpt_plan",
    }.get(envelope.receipt.execution_role)
    if (
        expected_authority is None
        or envelope.receipt_fingerprint != verification_fingerprint
        or envelope.receipt.source_commitment != inventory.source_commitment
        or plan.source_commitment != inventory.source_commitment
        or plan.execution_authority != expected_authority
    ):
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Result receipt, snapshot, plan authority, and verification are not bound.",
        )
    if not _authorities_match_receipt(envelope, authorities):
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Receiver portable authorities changed after verification.",
        )

    inventory_by_id = {item.file_id: item for item in inventory.files}
    plan_by_id = {item.file_id: item for item in plan.file_mappings}
    rows_by_id = {item.file_id: item for item in authorities.path_rows}
    if not (
        set(inventory_by_id) == set(plan_by_id) == set(rows_by_id)
        and len(authorities.path_rows) == len(inventory.files)
    ):
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Receiver snapshot, plan, and maps do not account for every file once.",
        )
    for file_id, source_file in inventory_by_id.items():
        mapping = plan_by_id[file_id]
        row = rows_by_id[file_id]
        if (
            mapping.original_path != source_file.relative_path
            or mapping.target_path != row.result_path
            or mapping.original_path != row.original_path
            or mapping.protected != source_file.protected
            or row.protected != source_file.protected
            or row.original_size != source_file.size
            or row.original_sha256 != source_file.sha256
        ):
            raise FolderReconstructionError(
                "receipt_reparse_failed",
                "Receiver-local map differs from its own source snapshot or plan: "
                f"{source_file.relative_path}.",
            )
    return envelope.receipt.execution_role


def _authorities_match_receipt(
    envelope: _ReceiptEnvelope,
    authorities: _LoadedReceiverAuthorities,
) -> bool:
    commitments = {item.path: item for item in envelope.receipt.artifact_commitments}
    payloads = {
        SOURCE_SNAPSHOT_PATH: authorities.inventory_bytes,
        ACCEPTED_PLAN_PATH: authorities.accepted_plan_bytes,
        FORWARD_PATH_MAP_PATH: authorities.forward_bytes,
        REVERSE_PATH_MAP_PATH: authorities.reverse_bytes,
    }
    for path, payload in payloads.items():
        commitment = commitments.get(path)
        if commitment is None:
            return False
        if commitment.size != len(payload):
            return False
        if commitment.sha256 != hashlib.sha256(payload).hexdigest():
            return False
    return True
