"""Fail-closed generic-folder inventory and stable identity generation."""

from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from name_atlas.folder_refactor.contracts import (
    MAX_MARKDOWN_ADAPTER_BYTES,
    FolderEmptyDirectory,
    FolderFile,
    FolderInventory,
    compute_inventory_commitment,
)
from name_atlas.folder_refactor.naming import (
    TargetPathError,
    protected_suffix,
    validate_complete_target_tree,
    validate_target_path,
)
from name_atlas.folder_refactor.serialization import canonical_sha256

HASH_CHUNK_SIZE = 1024 * 1024
MAX_FILE_COUNT = 500
MAX_DIRECTORY_COUNT = 1_000
TEXT_EVIDENCE_SUFFIXES = frozenset({".csv", ".markdown", ".md", ".txt"})
SENSITIVE_BASENAMES = frozenset(
    {
        ".npmrc",
        ".pypirc",
        "id_dsa",
        "id_ecdsa",
        "id_ed25519",
        "id_rsa",
    }
)
SENSITIVE_SUFFIXES = (".kdbx", ".key", ".p12", ".pem", ".pfx")


class FolderScanError(ValueError):
    """The selected folder is outside the supported source contract."""


@dataclass(frozen=True, slots=True)
class FolderScan:
    """Local source root plus its path-neutral portable inventory."""

    source_root: Path
    inventory: FolderInventory
    local_file_identities: tuple[LocalFileIdentity, ...]
    local_directory_identities: tuple[LocalDirectoryIdentity, ...]


@dataclass(frozen=True, slots=True)
class LocalFileIdentity:
    """Nonportable identity used only to detect local member replacement."""

    relative_path: str
    device: int
    inode: int
    size: int
    modified_ns: int


@dataclass(frozen=True, slots=True)
class LocalDirectoryIdentity:
    """Nonportable identity used only to detect directory replacement."""

    relative_path: str
    device: int
    inode: int
    modified_ns: int


def scan_folder(root: Path) -> FolderScan:
    """Inventory every supported file and explicit empty directory."""

    source_root = _require_root(root)
    files: list[FolderFile] = []
    local_identities: list[LocalFileIdentity] = []
    local_directory_identities: list[LocalDirectoryIdentity] = []
    empty_directories: list[FolderEmptyDirectory] = []
    directory_count = 0

    def fail_walk(error: OSError) -> None:
        raise FolderScanError(f"Source directory cannot be read: {error.filename}")

    for directory, directory_names, file_names in os.walk(
        source_root,
        topdown=True,
        followlinks=False,
        onerror=fail_walk,
    ):
        directory_path = Path(directory)
        directory_relative_path = (
            "."
            if directory_path == source_root
            else directory_path.relative_to(source_root).as_posix()
        )
        local_directory_identities.append(
            _directory_identity(directory_path, directory_relative_path)
        )
        directory_names.sort()
        file_names.sort()
        for name in directory_names:
            child = directory_path / name
            relative_path = child.relative_to(source_root).as_posix()
            _validate_source_relative_path(relative_path)
            _require_directory(child, relative_path)
            directory_count += 1
            if directory_count > MAX_DIRECTORY_COUNT:
                raise FolderScanError(
                    f"Source contains more than {MAX_DIRECTORY_COUNT} directories."
                )

        if directory_path != source_root and not directory_names and not file_names:
            relative_path = directory_path.relative_to(source_root).as_posix()
            _validate_source_relative_path(relative_path)
            _validate_fixed_path(relative_path)
            empty_directories.append(FolderEmptyDirectory(relative_path=relative_path))

        for name in file_names:
            path = directory_path / name
            relative_path = path.relative_to(source_root).as_posix()
            _validate_source_relative_path(relative_path)
            source_file, local_identity = _scan_file(path, relative_path)
            files.append(source_file)
            local_identities.append(local_identity)
            if len(files) > MAX_FILE_COUNT:
                raise FolderScanError(
                    f"Source contains more than {MAX_FILE_COUNT} regular files."
                )

    if not files:
        raise FolderScanError("Selected source folder contains no regular files.")

    files.sort(key=lambda item: item.relative_path)
    local_identities.sort(key=lambda item: item.relative_path)
    local_directory_identities.sort(key=lambda item: item.relative_path)
    empty_directories.sort(key=lambda item: item.relative_path)
    _validate_fixed_target_tree(files, empty_directories)
    total_bytes = sum(item.size for item in files)
    file_tuple = tuple(files)
    empty_tuple = tuple(empty_directories)
    source_commitment = compute_inventory_commitment(
        files=file_tuple,
        empty_directories=empty_tuple,
        directory_count=directory_count,
        total_bytes=total_bytes,
    )
    inventory = FolderInventory(
        files=file_tuple,
        empty_directories=empty_tuple,
        directory_count=directory_count,
        total_bytes=total_bytes,
        source_commitment=source_commitment,
    )
    return FolderScan(
        source_root=source_root,
        inventory=inventory,
        local_file_identities=tuple(local_identities),
        local_directory_identities=tuple(local_directory_identities),
    )


def inventory_evidence_ids(inventory: FolderInventory) -> frozenset[str]:
    """Return stable IDs for the initial path-and-metadata evidence records."""

    return frozenset(f"inventory:{item.file_id}" for item in inventory.files)


def _require_root(root: Path) -> Path:
    if not isinstance(root, Path):
        raise FolderScanError("Source root must be a pathlib.Path.")
    try:
        metadata = root.lstat()
    except OSError as exc:
        raise FolderScanError(f"Source root cannot be inspected: {root}") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise FolderScanError(
            f"Source root must be an existing non-symlink directory: {root}"
        )
    try:
        return root.resolve(strict=True)
    except OSError as exc:
        raise FolderScanError(f"Source root cannot be resolved: {root}") from exc


def _require_directory(path: Path, relative_path: str) -> None:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise FolderScanError(
            f"Source directory cannot be inspected: {relative_path}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise FolderScanError(f"Symlink directories are unsupported: {relative_path}")
    if not stat.S_ISDIR(metadata.st_mode):
        raise FolderScanError(
            f"Special filesystem member is unsupported: {relative_path}"
        )


def _directory_identity(path: Path, relative_path: str) -> LocalDirectoryIdentity:
    """Capture one directory identity after ``os.walk`` enumerates it."""

    try:
        metadata = path.lstat()
    except OSError as exc:
        raise FolderScanError(
            f"Source directory cannot be inspected: {relative_path}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise FolderScanError(
            f"Source directory was replaced while scanning: {relative_path}"
        )
    return LocalDirectoryIdentity(
        relative_path=relative_path,
        device=metadata.st_dev,
        inode=metadata.st_ino,
        modified_ns=metadata.st_mtime_ns,
    )


def _scan_file(
    path: Path,
    relative_path: str,
) -> tuple[FolderFile, LocalFileIdentity]:
    try:
        metadata = path.lstat()
    except OSError as exc:
        raise FolderScanError(
            f"Source member cannot be inspected: {relative_path}"
        ) from exc
    if stat.S_ISLNK(metadata.st_mode):
        raise FolderScanError(f"Symlink files are unsupported: {relative_path}")
    if not stat.S_ISREG(metadata.st_mode):
        raise FolderScanError(
            f"Special filesystem member is unsupported: {relative_path}"
        )
    if metadata.st_nlink > 1:
        raise FolderScanError(f"Hard-linked files are unsupported: {relative_path}")

    size, digest, stable_metadata = _hash_regular_file(path, relative_path)
    reasons = _protection_reasons(relative_path)
    protected = bool(reasons)
    if protected:
        _validate_fixed_path(relative_path)
    else:
        _validate_eligible_suffix(relative_path)
    suffix = PurePosixPath(relative_path).suffix.casefold()
    if suffix in {".md", ".markdown"} and size > MAX_MARKDOWN_ADAPTER_BYTES:
        raise FolderScanError(
            "Markdown adapter byte limit exceeded: "
            f"{relative_path!r} is {size} bytes; maximum "
            f"{MAX_MARKDOWN_ADAPTER_BYTES} bytes."
        )
    evidence_eligible = not protected and suffix in TEXT_EVIDENCE_SUFFIXES
    identity_payload = {
        "domain": "name-atlas:folder-file-id:v1",
        "original_relative_path": relative_path,
        "payload_sha256": digest,
        "size": size,
    }
    source_file = FolderFile(
        file_id=canonical_sha256(identity_payload),
        relative_path=relative_path,
        size=size,
        sha256=digest,
        protected=protected,
        evidence_eligible=evidence_eligible,
        protection_reasons=reasons,
    )
    local_identity = LocalFileIdentity(
        relative_path=relative_path,
        device=stable_metadata.st_dev,
        inode=stable_metadata.st_ino,
        size=stable_metadata.st_size,
        modified_ns=stable_metadata.st_mtime_ns,
    )
    return source_file, local_identity


def _hash_regular_file(
    path: Path,
    relative_path: str,
) -> tuple[int, str, os.stat_result]:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise FolderScanError(
            f"Source file cannot be opened safely: {relative_path}"
        ) from exc

    digest = hashlib.sha256()
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise FolderScanError(f"Source member is not regular: {relative_path}")
        if before.st_nlink > 1:
            raise FolderScanError(f"Hard-linked files are unsupported: {relative_path}")
        size = 0
        while chunk := os.read(descriptor, HASH_CHUNK_SIZE):
            digest.update(chunk)
            size += len(chunk)
        after = os.fstat(descriptor)
        identity_before = (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
            before.st_nlink,
        )
        identity_after = (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_nlink,
        )
        if identity_before != identity_after or size != after.st_size:
            raise FolderScanError(
                f"Source file changed while being read: {relative_path}"
            )
    finally:
        os.close(descriptor)
    return size, digest.hexdigest(), after


def _validate_source_relative_path(value: str) -> None:
    try:
        value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise FolderScanError(f"Source path is not valid UTF-8: {value!r}") from exc
    if not value or value.startswith("/") or "\x00" in value or "\\" in value:
        raise FolderScanError(f"Unsupported source path: {value!r}")
    if any(ord(character) < 32 or 127 <= ord(character) <= 159 for character in value):
        raise FolderScanError(f"Source path contains a control character: {value!r}")
    raw_segments = value.split("/")
    if any(segment in {"", ".", ".."} for segment in raw_segments):
        raise FolderScanError(f"Unsupported source path: {value!r}")
    normalized = PurePosixPath(value)
    if normalized.is_absolute() or normalized.as_posix() != value:
        raise FolderScanError(f"Unsupported source path: {value!r}")


def _validate_fixed_path(relative_path: str) -> None:
    try:
        validate_target_path(
            relative_path,
            original_path=relative_path,
            protected=True,
        )
    except TargetPathError as exc:
        raise FolderScanError(
            f"Fixed source path cannot satisfy the result profile: {relative_path!r}"
        ) from exc


def _validate_eligible_suffix(relative_path: str) -> None:
    """Prove at scan time that one required exact suffix has a valid target."""

    suffix = protected_suffix(PurePosixPath(relative_path).name)
    candidate = f"x{suffix}"
    try:
        validate_target_path(
            candidate,
            original_path=relative_path,
            protected=False,
        )
    except TargetPathError as exc:
        raise FolderScanError(
            "Source file suffix cannot satisfy the result naming profile: "
            f"{relative_path!r}"
        ) from exc


def _validate_fixed_target_tree(
    files: list[FolderFile],
    empty_directories: list[FolderEmptyDirectory],
) -> None:
    fixed_file_paths = [item.relative_path for item in files if item.protected]
    fixed_empty_paths = [item.relative_path for item in empty_directories]
    try:
        validate_complete_target_tree(fixed_file_paths, fixed_empty_paths)
    except TargetPathError as exc:
        raise FolderScanError(
            "Fixed source members cannot satisfy the result path profile."
        ) from exc


def _protection_reasons(relative_path: str) -> tuple[str, ...]:
    segments = PurePosixPath(relative_path).parts
    basename = segments[-1].casefold()
    reasons: list[str] = []
    if any(segment.startswith(".") for segment in segments):
        reasons.append("dot_path")
    if basename in SENSITIVE_BASENAMES:
        reasons.append("sensitive_basename")
    if basename.startswith(("credentials", "secrets")):
        reasons.append("sensitive_prefix")
    if basename.startswith(".env"):
        reasons.append("environment_file")
    if basename.endswith(SENSITIVE_SUFFIXES):
        reasons.append("sensitive_suffix")
    return tuple(dict.fromkeys(reasons))
