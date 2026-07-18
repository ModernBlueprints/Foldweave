"""Copy-only logical restoration from one verified portable handoff."""

from __future__ import annotations

import hashlib
import os
import stat
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from name_atlas.artifacts import ArtifactReadError, PathMapRow, parse_path_map
from name_atlas.domain import MemberKind
from name_atlas.package_import import import_package
from name_atlas.ports import PackageValidator
from name_atlas.receipts import (
    FORWARD_PATH_MAP_PATH,
    ORIGINAL_METADATA_PATH,
    ORIGINAL_NORMALIZATION_PATH,
    PORTABLE_SOURCE_SNAPSHOT_PATH,
    REVERSE_PATH_MAP_PATH,
    PortableSourceMember,
    PortableSourceSnapshot,
    ReceiptContractError,
    portable_snapshot_from_source,
    read_regular_bytes,
)
from name_atlas.receiver_verifier import (
    ReceiptVerificationStatus,
    verify_receipt,
)
from name_atlas.source import HASH_CHUNK_SIZE, validate_relative_path
from name_atlas.verification.promotion import promote_directory_no_replace

oslo_tz = ZoneInfo("Europe/Oslo")

_RESTORE_CHECK_IDS = (
    "receipt_verified",
    "content_restored_through_reverse_map",
    "original_controls_restored",
    "strict_package_reimported",
    "portable_snapshot_equal",
    "handoff_unchanged",
    "promoted_no_replace",
)

_DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
)


@dataclass(frozen=True)
class _PendingDirectory:
    """One descriptor-anchored pending tree owned by this transaction."""

    path: Path
    parent: Path
    descriptor: int
    device: int
    inode: int

    @property
    def identity(self) -> tuple[int, int]:
        """Return the immutable filesystem identity captured at creation."""

        return self.device, self.inode


class RestoreStatus(StrEnum):
    """Terminal state of a successful restore report."""

    RESTORED = "restored"


class RestoreCheck(BaseModel):
    """One deterministic restore check."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    check_id: str = Field(min_length=1, max_length=128)
    passed: bool
    detail: str = Field(min_length=1, max_length=1_000)


class RestoreReport(BaseModel):
    """Strict external result for one successfully promoted logical restore."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)

    schema_version: Literal["restore-report.v1"] = "restore-report.v1"
    status: RestoreStatus = RestoreStatus.RESTORED
    receipt_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    restored_at: datetime
    destination: Path
    source_snapshot_commitment: str = Field(pattern=r"^[a-f0-9]{64}$")
    restored_member_count: int = Field(ge=1)
    restored_bytes: int = Field(ge=0)
    restored_snapshot: PortableSourceSnapshot
    checks: tuple[RestoreCheck, ...] = Field(min_length=1)

    @field_validator("restored_at")
    @classmethod
    def require_oslo_timestamp(cls, value: datetime) -> datetime:
        """Require an aware timestamp expressed with the Oslo offset."""

        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Restore timestamp must be timezone-aware.")
        oslo_value = value.astimezone(oslo_tz)
        if value.utcoffset() != oslo_value.utcoffset():
            raise ValueError("Restore timestamp must use the Europe/Oslo offset.")
        return value

    @field_validator("destination")
    @classmethod
    def require_absolute_destination(cls, value: Path) -> Path:
        """Keep the local result explicit without putting it in the handoff."""

        if not value.is_absolute():
            raise ValueError("Restore destination must be absolute.")
        return value

    @model_validator(mode="after")
    def require_complete_success_evidence(self) -> RestoreReport:
        """Bind counts and checks to the exact restored portable snapshot."""

        if self.source_snapshot_commitment != self.restored_snapshot.commitment:
            raise ValueError("Restore report commitment differs from its snapshot.")
        if self.restored_member_count != len(self.restored_snapshot.members):
            raise ValueError("Restore report member count differs from its snapshot.")
        if self.restored_bytes != sum(
            member.size for member in self.restored_snapshot.members
        ):
            raise ValueError("Restore report byte count differs from its snapshot.")
        check_ids = tuple(check.check_id for check in self.checks)
        if check_ids != _RESTORE_CHECK_IDS or not all(
            check.passed for check in self.checks
        ):
            raise ValueError("Restore report checks are incomplete or failed.")
        return self


class RestoreError(RuntimeError):
    """A verified handoff could not be restored without weakening the contract."""


def restore_receipt(
    received_bag: Path,
    destination: Path,
    *,
    package_validator: PackageValidator | None = None,
) -> RestoreReport:
    """Verify and restore one handoff into a new source-shaped directory.

    The received bag is read-only. The destination is promoted atomically from a
    sibling pending directory only after strict package import and exact portable
    snapshot equality pass.
    """

    verification = verify_receipt(
        received_bag,
        package_validator=package_validator,
    )
    if verification.status is not ReceiptVerificationStatus.VERIFIED:
        blocker_text = " ".join(verification.failed_check_ids)
        raise RestoreError(f"Receipt verification blocked restore: {blocker_text}")
    if verification.receipt_fingerprint is None:
        raise RestoreError("Verified receipt did not expose its fingerprint.")

    handoff_root = _resolve_verified_handoff_root(received_bag)
    handoff_before = _snapshot_read_only_tree(handoff_root)
    final_root = _resolve_absent_destination(destination, handoff_root=handoff_root)
    snapshot, reverse_rows = _read_restore_authority(handoff_root)
    pending = _create_pending_root(final_root)
    promoted = False

    try:
        _restore_content(
            handoff_root=handoff_root,
            pending=pending,
            snapshot=snapshot,
            reverse_rows=reverse_rows,
        )
        _restore_original_controls(
            handoff_root=handoff_root,
            pending=pending,
            snapshot=snapshot,
        )
        _require_pending_path_identity(pending)
        restored_package = import_package(pending.path)
        _require_pending_path_identity(pending)
        restored_snapshot = portable_snapshot_from_source(restored_package.snapshot)
        if restored_snapshot != snapshot:
            raise RestoreError(
                "Restored package paths, roles, sizes, or digests differ from the "
                "portable source snapshot."
            )

        final_verification = verify_receipt(
            handoff_root,
            package_validator=package_validator,
        )
        if (
            final_verification.status is not ReceiptVerificationStatus.VERIFIED
            or final_verification.receipt_fingerprint
            != verification.receipt_fingerprint
        ):
            raise RestoreError(
                "Received handoff no longer matches the verified receipt."
            )
        handoff_after_verification = _snapshot_read_only_tree(handoff_root)
        if handoff_after_verification != handoff_before:
            raise RestoreError("Received handoff changed during restoration.")

        checks = tuple(
            RestoreCheck(check_id=check_id, passed=True, detail=detail)
            for check_id, detail in (
                (
                    "receipt_verified",
                    "The keyless receiver verifier passed before copying and "
                    "again before promotion.",
                ),
                (
                    "content_restored_through_reverse_map",
                    f"Restored {len(reverse_rows)} content objects through the "
                    "reverse map.",
                ),
                (
                    "original_controls_restored",
                    "Restored byte-exact original declared control files.",
                ),
                (
                    "strict_package_reimported",
                    "The pending directory passed the strict supported-package "
                    "importer.",
                ),
                (
                    "portable_snapshot_equal",
                    "Every restored path, role, size, and SHA-256 matches the receipt.",
                ),
                (
                    "handoff_unchanged",
                    "The complete received directory/file layout and file bytes "
                    "remained unchanged through final receiver verification.",
                ),
                (
                    "promoted_no_replace",
                    "The complete pending restore was promoted without replacement.",
                ),
            )
        )
        success_report = RestoreReport(
            receipt_fingerprint=verification.receipt_fingerprint,
            restored_at=datetime.now(oslo_tz),
            destination=final_root,
            source_snapshot_commitment=snapshot.commitment,
            restored_member_count=len(snapshot.members),
            restored_bytes=sum(member.size for member in snapshot.members),
            restored_snapshot=restored_snapshot,
            checks=checks,
        )
        os.fsync(pending.descriptor)
        _require_pending_path_identity(pending)
        promote_directory_no_replace(pending.path, final_root)
        promoted = True
        _require_directory_identity(
            final_root,
            expected=pending.identity,
            label="Promoted restore destination",
        )
    except RestoreError:
        raise
    except (OSError, ValueError) as exc:
        raise RestoreError("Restore transaction failed before promotion.") from exc
    finally:
        try:
            if not promoted:
                _discard_pending(pending)
        finally:
            with suppress(OSError):
                os.close(pending.descriptor)

    return success_report


def _read_restore_authority(
    handoff_root: Path,
) -> tuple[PortableSourceSnapshot, tuple[PathMapRow, ...]]:
    """Read only receipt-bound authority needed to reconstruct source paths."""

    try:
        snapshot = PortableSourceSnapshot.model_validate_json(
            read_regular_bytes(handoff_root, PORTABLE_SOURCE_SNAPSHOT_PATH),
            strict=True,
        )
        forward_rows = parse_path_map(
            read_regular_bytes(handoff_root, FORWARD_PATH_MAP_PATH),
            reverse=False,
        )
        reverse_rows = parse_path_map(
            read_regular_bytes(handoff_root, REVERSE_PATH_MAP_PATH),
            reverse=True,
        )
    except (ArtifactReadError, ReceiptContractError, ValueError) as exc:
        raise RestoreError("Receipt-bound restore authority cannot be parsed.") from exc
    if forward_rows != reverse_rows:
        raise RestoreError("Forward and reverse maps are not exact inverses.")
    return snapshot, reverse_rows


def _restore_content(
    *,
    handoff_root: Path,
    pending: _PendingDirectory,
    snapshot: PortableSourceSnapshot,
    reverse_rows: tuple[PathMapRow, ...],
) -> None:
    """Copy every content object from its staged path to its original path."""

    content_members = {
        member.relative_path: member
        for member in snapshot.members
        if member.kind is MemberKind.CONTENT_OBJECT
    }
    restored_sources: set[str] = set()
    for row in reverse_rows:
        source_path = row.source_path
        target_path = row.target_path
        member = content_members.get(source_path)
        if (
            member is None
            or member.size != row.size
            or member.sha256 != row.sha256
            or member.role != row.role
            or source_path in restored_sources
        ):
            raise RestoreError("Reverse map does not match portable source authority.")
        _copy_verified_member(
            source_root=handoff_root,
            source_relative_path=f"data/{target_path}",
            destination=pending,
            destination_relative_path=source_path,
            expected=member,
        )
        restored_sources.add(source_path)
    if restored_sources != set(content_members):
        raise RestoreError("Reverse map does not cover every source content object.")


def _restore_original_controls(
    *,
    handoff_root: Path,
    pending: _PendingDirectory,
    snapshot: PortableSourceSnapshot,
) -> None:
    """Restore byte-exact declared controls from receipt-bound tag artifacts."""

    control_artifacts = {
        "metadata/metadata.csv": ORIGINAL_METADATA_PATH,
        "normalization.csv": ORIGINAL_NORMALIZATION_PATH,
    }
    controls = tuple(
        member
        for member in snapshot.members
        if member.kind is MemberKind.DECLARED_CONTROL_FILE
    )
    for member in controls:
        artifact_path = control_artifacts.get(member.relative_path)
        if artifact_path is None:
            raise RestoreError(
                "Portable snapshot contains an unsupported control file."
            )
        _copy_verified_member(
            source_root=handoff_root,
            source_relative_path=artifact_path,
            destination=pending,
            destination_relative_path=member.relative_path,
            expected=member,
        )


def _copy_verified_member(
    *,
    source_root: Path,
    source_relative_path: str,
    destination: _PendingDirectory,
    destination_relative_path: str,
    expected: PortableSourceMember,
) -> None:
    """Stream one regular member with no-follow, exclusivity, and digest proof."""

    validate_relative_path(source_relative_path)
    validate_relative_path(destination_relative_path)
    source_path = _require_regular_relative_path(source_root, source_relative_path)
    destination_parent_descriptor, destination_name = _open_destination_parent(
        destination,
        destination_relative_path,
    )

    source_descriptor: int | None = None
    destination_descriptor: int | None = None
    digest = hashlib.sha256()
    copied_size = 0
    try:
        source_descriptor = os.open(
            source_path,
            os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
        )
        source_before = os.fstat(source_descriptor)
        if not stat.S_ISREG(source_before.st_mode):
            raise RestoreError("Restore source is not a regular file.")
        destination_descriptor = os.open(
            destination_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
            dir_fd=destination_parent_descriptor,
        )
        while chunk := os.read(source_descriptor, HASH_CHUNK_SIZE):
            digest.update(chunk)
            copied_size += len(chunk)
            view = memoryview(chunk)
            while view:
                written = os.write(destination_descriptor, view)
                if written <= 0:
                    raise OSError("Restore destination write made no progress.")
                view = view[written:]
        os.fsync(destination_descriptor)
        source_after = os.fstat(source_descriptor)
    except RestoreError:
        raise
    except OSError as exc:
        raise RestoreError(
            f"Copy failed for restored member: {destination_relative_path}"
        ) from exc
    finally:
        if destination_descriptor is not None:
            os.close(destination_descriptor)
        if source_descriptor is not None:
            os.close(source_descriptor)
        os.close(destination_parent_descriptor)

    source_identity_before = (
        source_before.st_dev,
        source_before.st_ino,
        source_before.st_size,
        source_before.st_mtime_ns,
    )
    source_identity_after = (
        source_after.st_dev,
        source_after.st_ino,
        source_after.st_size,
        source_after.st_mtime_ns,
    )
    if source_identity_before != source_identity_after:
        raise RestoreError(
            f"Restore source changed while copying: {source_relative_path}"
        )
    if copied_size != expected.size or digest.hexdigest() != expected.sha256:
        raise RestoreError(
            f"Restored member differs from its receipt: {destination_relative_path}"
        )


def _require_regular_relative_path(root: Path, relative_path: str) -> Path:
    """Resolve one regular in-root path without following a symlink component."""

    resolved_root = _require_real_directory(root)
    current = resolved_root
    parts = PurePosixPath(relative_path).parts
    for part in parts[:-1]:
        current /= part
        try:
            metadata = current.lstat()
        except OSError as exc:
            raise RestoreError("Restore source parent cannot be inspected.") from exc
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RestoreError("Restore source parent is not a real directory.")
    candidate = current / parts[-1]
    try:
        metadata = candidate.lstat()
    except OSError as exc:
        raise RestoreError("Restore source member cannot be inspected.") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RestoreError("Restore source member is not a regular file.")
    return candidate


def _open_destination_parent(
    pending: _PendingDirectory,
    relative_path: str,
) -> tuple[int, str]:
    """Open one pending-tree parent without following any directory symlink."""

    parts = PurePosixPath(relative_path).parts
    current_descriptor = os.dup(pending.descriptor)
    try:
        root_metadata = os.fstat(current_descriptor)
        if (root_metadata.st_dev, root_metadata.st_ino) != pending.identity:
            raise RestoreError("Restore pending-directory identity changed.")
        for part in parts[:-1]:
            with suppress(FileExistsError):
                os.mkdir(part, mode=0o700, dir_fd=current_descriptor)
            child_descriptor = os.open(
                part,
                _DIRECTORY_OPEN_FLAGS,
                dir_fd=current_descriptor,
            )
            child_metadata = os.fstat(child_descriptor)
            if not stat.S_ISDIR(child_metadata.st_mode):
                os.close(child_descriptor)
                raise RestoreError(
                    "Restore destination parent is not a real directory."
                )
            os.close(current_descriptor)
            current_descriptor = child_descriptor
    except RestoreError:
        os.close(current_descriptor)
        raise
    except OSError as exc:
        os.close(current_descriptor)
        raise RestoreError(
            "Restore destination parent cannot be created safely."
        ) from exc
    return current_descriptor, parts[-1]


def _resolve_absent_destination(destination: Path, *, handoff_root: Path) -> Path:
    """Resolve a new destination under a present real parent."""

    candidate = destination.expanduser()
    if not candidate.is_absolute():
        candidate = Path.cwd() / candidate
    parent = _require_real_directory(candidate.parent)
    resolved = parent / candidate.name
    if os.path.lexists(resolved):
        raise RestoreError(f"Restore destination already exists: {resolved}")
    try:
        resolved.relative_to(handoff_root)
    except ValueError:
        pass
    else:
        raise RestoreError("Restore destination cannot be inside the received handoff.")
    return resolved


def _resolve_verified_handoff_root(received_bag: Path) -> Path:
    """Resolve a handoff that was openable when initial verification ran."""

    try:
        return received_bag.expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise RestoreError(
            "Received handoff became unavailable after initial verification."
        ) from exc


def _create_pending_root(final_root: Path) -> _PendingDirectory:
    """Create and pin one product-owned sibling pending directory."""

    pending_path: Path | None = None
    descriptor: int | None = None
    try:
        pending_path = Path(
            tempfile.mkdtemp(
                prefix=f".{final_root.name[:64]}.restore-",
                suffix=".pending",
                dir=final_root.parent,
            )
        )
        descriptor = os.open(pending_path, _DIRECTORY_OPEN_FLAGS)
        metadata = os.fstat(descriptor)
        if not stat.S_ISDIR(metadata.st_mode):
            raise OSError("Pending restore root is not a directory.")
        return _PendingDirectory(
            path=pending_path,
            parent=final_root.parent,
            descriptor=descriptor,
            device=metadata.st_dev,
            inode=metadata.st_ino,
        )
    except OSError as exc:
        if descriptor is not None:
            os.close(descriptor)
        if pending_path is not None:
            with suppress(OSError):
                pending_path.rmdir()
        raise RestoreError("Restore pending directory could not be created.") from exc


def _require_pending_path_identity(pending: _PendingDirectory) -> None:
    """Require the pending pathname to still identify the pinned directory."""

    _require_directory_identity(
        pending.path,
        expected=pending.identity,
        label="Restore pending directory",
    )


def _require_directory_identity(
    path: Path,
    *,
    expected: tuple[int, int],
    label: str,
) -> None:
    """Require one path to name the expected real directory identity."""

    try:
        metadata = path.lstat()
    except OSError as exc:
        raise RestoreError(f"{label} cannot be inspected.") from exc
    actual = (metadata.st_dev, metadata.st_ino)
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or actual != expected
    ):
        raise RestoreError(f"{label} no longer has its owned identity.")


def _discard_pending(pending: _PendingDirectory) -> None:
    """Remove only the pinned pending inode, even if its pathname was replaced."""

    try:
        _clear_directory_descriptor(pending.descriptor)
        parent_descriptor = os.open(pending.parent, _DIRECTORY_OPEN_FLAGS)
        try:
            owned_name = _find_owned_child_name(parent_descriptor, pending.identity)
            if owned_name is None:
                raise RestoreError(
                    "Restore failed and the owned pending directory cannot be located."
                )
            current = os.stat(
                owned_name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
            if (
                not stat.S_ISDIR(current.st_mode)
                or (current.st_dev, current.st_ino) != pending.identity
            ):
                raise RestoreError(
                    "Restore failed and pending-directory ownership changed."
                )
            os.rmdir(owned_name, dir_fd=parent_descriptor)
        finally:
            os.close(parent_descriptor)
    except RestoreError:
        raise
    except OSError as exc:
        raise RestoreError(
            f"Restore failed and owned pending cleanup also failed: {pending.path}"
        ) from exc


def _clear_directory_descriptor(directory_descriptor: int) -> None:
    """Clear one owned tree by descriptors without following symbolic links."""

    with os.scandir(directory_descriptor) as iterator:
        names = tuple(sorted(entry.name for entry in iterator))
    for name in names:
        try:
            metadata = os.stat(
                name,
                dir_fd=directory_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            continue
        if stat.S_ISDIR(metadata.st_mode):
            child_descriptor = os.open(
                name,
                _DIRECTORY_OPEN_FLAGS,
                dir_fd=directory_descriptor,
            )
            try:
                child_metadata = os.fstat(child_descriptor)
                child_identity = (child_metadata.st_dev, child_metadata.st_ino)
                if child_identity != (metadata.st_dev, metadata.st_ino):
                    raise RestoreError("Pending child identity changed during cleanup.")
                _clear_directory_descriptor(child_descriptor)
                current = os.stat(
                    name,
                    dir_fd=directory_descriptor,
                    follow_symlinks=False,
                )
                if (
                    not stat.S_ISDIR(current.st_mode)
                    or (current.st_dev, current.st_ino) != child_identity
                ):
                    raise RestoreError("Pending child identity changed during cleanup.")
                os.rmdir(name, dir_fd=directory_descriptor)
            finally:
                os.close(child_descriptor)
        else:
            os.unlink(name, dir_fd=directory_descriptor)


def _find_owned_child_name(
    parent_descriptor: int,
    identity: tuple[int, int],
) -> str | None:
    """Find the one sibling entry that still names an owned directory inode."""

    matches: list[str] = []
    with os.scandir(parent_descriptor) as iterator:
        names = tuple(sorted(entry.name for entry in iterator))
    for name in names:
        try:
            metadata = os.stat(
                name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            continue
        if (
            stat.S_ISDIR(metadata.st_mode)
            and (
                metadata.st_dev,
                metadata.st_ino,
            )
            == identity
        ):
            matches.append(name)
    if len(matches) > 1:
        raise RestoreError("Owned pending directory has ambiguous sibling names.")
    return matches[0] if matches else None


def _snapshot_read_only_tree(
    root: Path,
) -> tuple[tuple[str, str, int, str], ...]:
    """Hash complete file bytes and directory paths in one read-only tree."""

    resolved_root = _require_real_directory(root)
    members: list[tuple[str, str, int, str]] = []
    regular_file_count = 0
    for directory, directory_names, file_names in os.walk(
        resolved_root,
        topdown=True,
        followlinks=False,
    ):
        directory_path = Path(directory)
        for name in sorted(directory_names):
            child = directory_path / name
            try:
                metadata = child.lstat()
            except OSError as exc:
                raise RestoreError(
                    "Received handoff directory cannot be inspected."
                ) from exc
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
                raise RestoreError("Received handoff contains a non-directory link.")
            relative_path = child.relative_to(resolved_root).as_posix()
            members.append(("directory", relative_path, 0, ""))
        for name in sorted(file_names):
            child = directory_path / name
            relative_path = child.relative_to(resolved_root).as_posix()
            size, digest = _hash_stable_regular_file(child)
            members.append(("file", relative_path, size, digest))
            regular_file_count += 1
    if not regular_file_count:
        raise RestoreError("Received handoff contains no regular files.")
    return tuple(sorted(members))


def _hash_stable_regular_file(path: Path) -> tuple[int, str]:
    """Stream a no-follow regular file and reject change during the read."""

    descriptor: int | None = None
    digest = hashlib.sha256()
    size = 0
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise RestoreError("Received handoff contains a non-regular member.")
        while chunk := os.read(descriptor, HASH_CHUNK_SIZE):
            digest.update(chunk)
            size += len(chunk)
        after = os.fstat(descriptor)
    except RestoreError:
        raise
    except OSError as exc:
        raise RestoreError("Received handoff member cannot be hashed.") from exc
    finally:
        if descriptor is not None:
            os.close(descriptor)
    identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
    identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
    if identity_before != identity_after or size != after.st_size:
        raise RestoreError("Received handoff changed while it was hashed.")
    return size, digest.hexdigest()


def _require_real_directory(path: Path) -> Path:
    """Require a non-symlink directory and return its canonical path."""

    try:
        metadata = path.lstat()
    except OSError as exc:
        raise RestoreError(f"Directory cannot be inspected: {path}") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise RestoreError(f"Directory must be a non-symlink directory: {path}")
    return path.resolve(strict=True)
