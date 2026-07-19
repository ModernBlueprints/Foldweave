"""Copy-only exact reconstruction from a verified generic-folder receipt."""

from __future__ import annotations

import hashlib
import os
import stat
import uuid
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from zoneinfo import ZoneInfo

from name_atlas.folder_refactor.contracts import (
    FolderAcceptedPlan,
    FolderInventory,
)
from name_atlas.folder_refactor.inventory import (
    HASH_CHUNK_SIZE,
    FolderScanError,
    scan_folder,
)
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
    FolderReceiptEnvelope,
    FolderReceiptVerificationStatus,
    FolderRestoreCheck,
    FolderRestoreReport,
)
from name_atlas.folder_refactor.receipt_verifier import verify_folder_receipt
from name_atlas.verification.promotion import promote_directory_no_replace

oslo_tz = ZoneInfo("Europe/Oslo")

_DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
)
_FILE_READ_FLAGS = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
_FILE_WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)


class FolderReconstructionError(RuntimeError):
    """A verified result cannot be reconstructed at the requested destination."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        failed_check_ids: tuple[str, ...] = (),
    ) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.failed_check_ids = failed_check_ids


@dataclass(frozen=True, slots=True)
class _OwnedPendingDirectory:
    path: Path
    parent: Path
    identity: tuple[int, int]
    parent_identity: tuple[int, int]


def restore_folder_receipt(
    result_root: Path,
    destination: Path,
) -> FolderRestoreReport:
    """Verify first, then recreate every committed source path and byte."""

    verification = verify_folder_receipt(result_root)
    if verification.status is not FolderReceiptVerificationStatus.VERIFIED:
        raise FolderReconstructionError(
            "receipt_verification_blocked",
            "The result must pass independent verification before reconstruction.",
            failed_check_ids=verification.failed_check_ids,
        )
    if verification.receipt_fingerprint is None:
        raise AssertionError("Verified receipt result lacks its fingerprint.")

    root = result_root.resolve(strict=True)
    final_destination = _resolve_absent_destination(
        destination,
        result_root=root,
    )
    try:
        inventory_bytes = read_regular_bytes(root, SOURCE_SNAPSHOT_PATH)
        accepted_plan_bytes = read_regular_bytes(root, ACCEPTED_PLAN_PATH)
        receipt_bytes = read_regular_bytes(root, CHANGE_RECEIPT_PATH)
        forward_bytes = read_regular_bytes(root, FORWARD_PATH_MAP_PATH)
        reverse_bytes = read_regular_bytes(root, REVERSE_PATH_MAP_PATH)
        inventory = parse_portable_model(
            inventory_bytes,
            FolderInventory,
        )
        accepted_plan = parse_portable_model(
            accepted_plan_bytes,
            FolderAcceptedPlan,
        )
        envelope = parse_portable_model(
            receipt_bytes,
            FolderReceiptEnvelope,
        )
        forward_rows = parse_folder_path_map(
            forward_bytes,
            reverse=False,
        )
        reverse_rows = parse_folder_path_map(
            reverse_bytes,
            reverse=True,
        )
    except (FolderPortableArtifactError, ValueError) as exc:
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Verified portable authorities could not be reopened safely.",
        ) from exc
    if (
        envelope.receipt_fingerprint != verification.receipt_fingerprint
        or forward_rows != reverse_rows
        or accepted_plan.source_commitment != inventory.source_commitment
        or not _reparsed_authorities_match_receipt(
            envelope,
            {
                SOURCE_SNAPSHOT_PATH: inventory_bytes,
                ACCEPTED_PLAN_PATH: accepted_plan_bytes,
                FORWARD_PATH_MAP_PATH: forward_bytes,
                REVERSE_PATH_MAP_PATH: reverse_bytes,
            },
        )
    ):
        raise FolderReconstructionError(
            "receipt_reparse_failed",
            "Verified portable authorities changed before reconstruction.",
        )

    pending: _OwnedPendingDirectory | None = None
    promoted = False
    try:
        pending = _create_owned_pending(final_destination)
        for row in forward_rows:
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
        for empty_directory in inventory.empty_directories:
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
                "The pending reconstruction is outside the supported folder contract.",
            ) from exc
        if restored_inventory != inventory:
            raise FolderReconstructionError(
                "reconstructed_inventory_mismatch",
                "Reconstructed paths, bytes, or empty directories differ "
                "from the source snapshot.",
            )

        report = FolderRestoreReport(
            receipt_fingerprint=verification.receipt_fingerprint,
            source_commitment=inventory.source_commitment,
            destination=final_destination,
            completed_at=datetime.now(oslo_tz),
            restored_file_count=len(inventory.files),
            restored_bytes=inventory.total_bytes,
            restored_empty_directory_count=len(inventory.empty_directories),
            checks=(
                FolderRestoreCheck(
                    check_id="receipt_verified",
                    detail="Independent source-free receipt verification passed first.",
                ),
                FolderRestoreCheck(
                    check_id="complete_original_paths_recreated",
                    detail="Every in-scope source path was recreated exactly once.",
                ),
                FolderRestoreCheck(
                    check_id="original_bytes_recreated",
                    detail=(
                        "Every reconstructed file size and SHA-256 matches "
                        "the source snapshot."
                    ),
                ),
                FolderRestoreCheck(
                    check_id="empty_directories_recreated",
                    detail="Every explicit source empty directory was recreated.",
                ),
                FolderRestoreCheck(
                    check_id="destination_promoted_no_replace",
                    detail=(
                        "The completed folder was promoted only while the "
                        "destination was absent."
                    ),
                ),
            ),
        )
        _fsync_directory(pending.parent)
        try:
            promote_directory_no_replace(pending.path, final_destination)
        except (FileExistsError, OSError) as exc:
            raise FolderReconstructionError(
                "promotion_failed",
                "The reconstruction destination could not be promoted "
                "without replacement.",
            ) from exc
        promoted = True
        return report
    except FolderReconstructionError:
        raise
    except Exception as exc:
        raise FolderReconstructionError(
            "reconstruction_copy_failed",
            "Copy-only reconstruction failed before promotion.",
        ) from exc
    finally:
        if pending is not None and not promoted:
            try:
                _remove_owned_pending(pending)
            except OSError as cleanup_error:
                raise FolderReconstructionError(
                    "pending_cleanup_failed",
                    "The exact product-owned pending reconstruction could "
                    "not be removed.",
                ) from cleanup_error


def _reparsed_authorities_match_receipt(
    envelope: FolderReceiptEnvelope,
    authorities: dict[str, bytes],
) -> bool:
    commitments = {item.path: item for item in envelope.receipt.artifact_commitments}
    for path, payload in authorities.items():
        commitment = commitments.get(path)
        if commitment is None:
            return False
        if commitment.size != len(payload):
            return False
        if commitment.sha256 != hashlib.sha256(payload).hexdigest():
            return False
    return True


def _resolve_absent_destination(
    destination: Path,
    *,
    result_root: Path,
    source_root: Path | None = None,
    require_result_sibling: bool = True,
) -> Path:
    if not isinstance(destination, Path):
        raise FolderReconstructionError(
            "destination_type_invalid",
            "Reconstruction destination must be a pathlib.Path.",
        )
    if not destination.is_absolute():
        raise FolderReconstructionError(
            "destination_must_be_absolute",
            "Reconstruction destination must be an absolute path.",
        )
    if destination.name in {"", ".", ".."} or "\x00" in destination.name:
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "Reconstruction destination has an invalid final component.",
        )
    try:
        destination_exists = os.path.lexists(destination)
    except (OSError, ValueError) as exc:
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "Reconstruction destination cannot be inspected.",
        ) from exc
    if destination_exists:
        raise FolderReconstructionError(
            "destination_exists",
            "Reconstruction refuses an existing destination.",
        )
    parent = destination.parent
    try:
        metadata = parent.lstat()
    except OSError as exc:
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "Reconstruction destination parent must already exist.",
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "Reconstruction destination parent must be a real directory.",
        )
    if metadata.st_mode & 0o222 == 0 or metadata.st_mode & 0o111 == 0:
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "Reconstruction destination parent is not writable and searchable.",
        )
    try:
        resolved_parent = parent.resolve(strict=True)
    except OSError as exc:
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "Reconstruction destination parent cannot be resolved.",
        ) from exc
    resolved = resolved_parent / destination.name
    if _contains(result_root, resolved) or _contains(resolved, result_root):
        raise FolderReconstructionError(
            "destination_overlaps_result",
            "Reconstruction destination and received result cannot contain "
            "one another.",
        )
    if source_root is not None:
        try:
            source_metadata = source_root.lstat()
            resolved_source = source_root.resolve(strict=True)
        except OSError as exc:
            raise FolderReconstructionError(
                "source_root_invalid",
                "Known reconstruction source root cannot be inspected safely.",
            ) from exc
        if stat.S_ISLNK(source_metadata.st_mode) or not stat.S_ISDIR(
            source_metadata.st_mode
        ):
            raise FolderReconstructionError(
                "source_root_invalid",
                "Known reconstruction source root must be a real directory.",
            )
        if _contains(resolved_source, resolved) or _contains(resolved, resolved_source):
            raise FolderReconstructionError(
                "destination_overlaps_source",
                "Reconstruction destination and known source cannot contain "
                "one another.",
            )
    if require_result_sibling and resolved_parent != result_root.parent.resolve(
        strict=True
    ):
        raise FolderReconstructionError(
            "destination_must_share_result_parent",
            "Reconstruction destination must be next to the received result.",
        )
    return resolved


def _create_owned_pending(destination: Path) -> _OwnedPendingDirectory:
    parent = destination.parent
    pending = parent / f".{destination.name}.pending-{uuid.uuid4().hex}"
    try:
        pending.mkdir(mode=0o700, exist_ok=False)
        metadata = pending.lstat()
        parent_metadata = parent.lstat()
    except FileExistsError as exc:
        raise FolderReconstructionError(
            "pending_destination_conflict",
            "The unique pending reconstruction path already exists.",
        ) from exc
    except OSError as exc:
        raise FolderReconstructionError(
            "destination_parent_invalid",
            "The pending reconstruction directory could not be created.",
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise FolderReconstructionError(
            "pending_destination_conflict",
            "The pending reconstruction path is not a real directory.",
        )
    return _OwnedPendingDirectory(
        path=pending,
        parent=parent,
        identity=(metadata.st_dev, metadata.st_ino),
        parent_identity=(parent_metadata.st_dev, parent_metadata.st_ino),
    )


def _copy_verified_member(
    *,
    source_root: Path,
    source_relative_path: str,
    destination: _OwnedPendingDirectory,
    destination_relative_path: str,
    expected_size: int,
    expected_sha256: str,
) -> None:
    source_descriptor = _open_source_member(source_root, source_relative_path)
    destination_parent: int | None = None
    output_descriptor: int | None = None
    digest = hashlib.sha256()
    copied_size = 0
    try:
        destination_parent, destination_name = _open_destination_parent(
            destination,
            destination_relative_path,
        )
        before = os.fstat(source_descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise OSError("Reconstruction source is not regular.")
        output_descriptor = os.open(
            destination_name,
            _FILE_WRITE_FLAGS,
            0o600,
            dir_fd=destination_parent,
        )
        while chunk := os.read(source_descriptor, HASH_CHUNK_SIZE):
            copied_size += len(chunk)
            digest.update(chunk)
            view = memoryview(chunk)
            while view:
                written = os.write(output_descriptor, view)
                if written <= 0:
                    raise OSError("Reconstruction write made no progress.")
                view = view[written:]
        os.fsync(output_descriptor)
        after = os.fstat(source_descriptor)
    finally:
        if output_descriptor is not None:
            os.close(output_descriptor)
        if destination_parent is not None:
            os.close(destination_parent)
        os.close(source_descriptor)
    before_identity = _file_identity(before)
    after_identity = _file_identity(after)
    if before_identity != after_identity:
        raise FolderReconstructionError(
            "reconstruction_copy_failed",
            f"Receipt member changed while copying: {source_relative_path}.",
        )
    if copied_size != expected_size or digest.hexdigest() != expected_sha256:
        raise FolderReconstructionError(
            "reconstruction_copy_failed",
            "Receipt member differs from original-byte authority: "
            f"{source_relative_path}.",
        )


def _open_source_member(root: Path, relative_path: str) -> int:
    parts = _portable_parts(relative_path)
    current = os.open(root, _DIRECTORY_OPEN_FLAGS)
    try:
        for part in parts[:-1]:
            child = os.open(part, _DIRECTORY_OPEN_FLAGS, dir_fd=current)
            os.close(current)
            current = child
        descriptor = os.open(parts[-1], _FILE_READ_FLAGS, dir_fd=current)
    except OSError:
        os.close(current)
        raise
    os.close(current)
    return descriptor


def _open_destination_parent(
    pending: _OwnedPendingDirectory,
    relative_path: str,
) -> tuple[int, str]:
    parts = _portable_parts(relative_path)
    current = os.open(pending.path, _DIRECTORY_OPEN_FLAGS)
    try:
        root_metadata = os.fstat(current)
        if (root_metadata.st_dev, root_metadata.st_ino) != pending.identity:
            raise OSError("Pending reconstruction identity changed.")
        for part in parts[:-1]:
            with suppress(FileExistsError):
                os.mkdir(part, mode=0o700, dir_fd=current)
            child = os.open(part, _DIRECTORY_OPEN_FLAGS, dir_fd=current)
            os.close(current)
            current = child
    except OSError:
        os.close(current)
        raise
    return current, parts[-1]


def _ensure_destination_directory(
    pending: _OwnedPendingDirectory,
    relative_path: str,
) -> None:
    parts = _portable_parts(relative_path)
    current = os.open(pending.path, _DIRECTORY_OPEN_FLAGS)
    try:
        root_metadata = os.fstat(current)
        if (root_metadata.st_dev, root_metadata.st_ino) != pending.identity:
            raise OSError("Pending reconstruction identity changed.")
        for part in parts:
            with suppress(FileExistsError):
                os.mkdir(part, mode=0o700, dir_fd=current)
            child = os.open(part, _DIRECTORY_OPEN_FLAGS, dir_fd=current)
            os.close(current)
            current = child
    finally:
        os.close(current)


def _portable_parts(value: str) -> tuple[str, ...]:
    if (
        not isinstance(value, str)
        or not value
        or value.startswith("/")
        or "\\" in value
        or "\x00" in value
    ):
        raise OSError("Receipt path is not portable relative POSIX syntax.")
    parts = PurePosixPath(value).parts
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise OSError("Receipt path contains an empty or dot segment.")
    if PurePosixPath(*parts).as_posix() != value:
        raise OSError("Receipt path is not normalized POSIX syntax.")
    return parts


def _remove_owned_pending(pending: _OwnedPendingDirectory) -> None:
    parent_descriptor = os.open(pending.parent, _DIRECTORY_OPEN_FLAGS)
    directory_descriptor: int | None = None
    try:
        parent_metadata = os.fstat(parent_descriptor)
        if (parent_metadata.st_dev, parent_metadata.st_ino) != (
            pending.parent_identity
        ):
            raise OSError("Pending parent identity changed.")
        directory_descriptor = os.open(
            pending.path.name,
            _DIRECTORY_OPEN_FLAGS,
            dir_fd=parent_descriptor,
        )
        directory_metadata = os.fstat(directory_descriptor)
        if (directory_metadata.st_dev, directory_metadata.st_ino) != pending.identity:
            raise OSError("Pending reconstruction identity changed.")
        _clear_directory(directory_descriptor)
        os.close(directory_descriptor)
        directory_descriptor = None
        os.rmdir(pending.path.name, dir_fd=parent_descriptor)
        os.fsync(parent_descriptor)
    finally:
        if directory_descriptor is not None:
            os.close(directory_descriptor)
        os.close(parent_descriptor)


def _clear_directory(descriptor: int) -> None:
    with os.scandir(descriptor) as entries:
        names = sorted(entry.name for entry in entries)
    for name in names:
        metadata = os.stat(name, dir_fd=descriptor, follow_symlinks=False)
        if stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode):
            child = os.open(name, _DIRECTORY_OPEN_FLAGS, dir_fd=descriptor)
            try:
                _clear_directory(child)
            finally:
                os.close(child)
            os.rmdir(name, dir_fd=descriptor)
        else:
            os.unlink(name, dir_fd=descriptor)


def _file_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int]:
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        metadata.st_nlink,
    )


def _fsync_directory(path: Path) -> None:
    descriptor: int | None = None
    try:
        descriptor = os.open(path, _DIRECTORY_OPEN_FLAGS)
        os.fsync(descriptor)
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _contains(parent: Path, child: Path) -> bool:
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True
