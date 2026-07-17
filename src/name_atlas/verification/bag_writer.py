"""Product-owned, deterministic BagIt 1.0 tag-file writer."""

from __future__ import annotations

import hashlib
import os
import stat
from contextlib import suppress
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path, PurePosixPath
from zoneinfo import ZoneInfo

oslo_tz = ZoneInfo("Europe/Oslo")

_BAGIT_VERSION = "1.0"
_TAG_FILE_ENCODING = "UTF-8"
_SOFTWARE_AGENT = "Reversible Name Atlas 0.1.0"
_HASH_CHUNK_SIZE = 1024 * 1024
_PAYLOAD_DIRECTORY = "data"
_PROOF_DIRECTORY = "name-atlas"
_BAGIT_FILE = "bagit.txt"
_BAG_INFO_FILE = "bag-info.txt"
_PAYLOAD_MANIFEST = "manifest-sha256.txt"
_TAG_MANIFEST = "tagmanifest-sha256.txt"
_INITIAL_ROOT_ENTRIES = frozenset({_PAYLOAD_DIRECTORY, _PROOF_DIRECTORY})
_COMPLETED_ROOT_ENTRIES = frozenset(
    {
        *_INITIAL_ROOT_ENTRIES,
        _BAGIT_FILE,
        _BAG_INFO_FILE,
        _PAYLOAD_MANIFEST,
        _TAG_MANIFEST,
    }
)
_REFRESHABLE_TAG_PATH = PurePosixPath(_PROOF_DIRECTORY, "verification_report.json")


class BagItWriterError(RuntimeError):
    """The pending stage cannot safely be turned into or refreshed as a bag."""


@dataclass(frozen=True, slots=True)
class BagItWriteResult:
    """Measurements from one successful BagIt tag-file write."""

    bag_root: Path
    payload_file_count: int
    payload_bytes: int
    tag_file_count: int


class BagItWriter:
    """Write BagIt metadata inside a fresh, product-owned pending stage."""

    def write(
        self,
        pending_root: Path,
        *,
        bagging_date: date | None = None,
    ) -> BagItWriteResult:
        """Create deterministic SHA-256 BagIt tag files without moving payloads."""

        root = _require_pending_directory(pending_root)
        _require_root_entries(root, _INITIAL_ROOT_ENTRIES)
        payload_files = _regular_files_under(root, _PAYLOAD_DIRECTORY)
        proof_files = _regular_files_under(root, _PROOF_DIRECTORY)
        if not payload_files:
            raise BagItWriterError("Pending stage data/ contains no payload files.")
        if not proof_files:
            raise BagItWriterError(
                "Pending stage name-atlas/ contains no proof tag files."
            )

        payload_bytes = sum(path.stat().st_size for path in payload_files)
        selected_date = bagging_date or datetime.now(oslo_tz).date()
        if isinstance(selected_date, datetime) or not isinstance(selected_date, date):
            raise BagItWriterError("Bagging date must be a datetime.date.")

        payload_manifest = _render_manifest(root, payload_files)
        bagit_text = (
            f"BagIt-Version: {_BAGIT_VERSION}\n"
            f"Tag-File-Character-Encoding: {_TAG_FILE_ENCODING}\n"
        )
        bag_info = (
            f"Bagging-Date: {selected_date.isoformat()}\n"
            f"Bag-Software-Agent: {_SOFTWARE_AGENT}\n"
            f"Payload-Oxum: {payload_bytes}.{len(payload_files)}\n"
        )

        _write_new_utf8(root / _BAGIT_FILE, bagit_text)
        _write_new_utf8(root / _BAG_INFO_FILE, bag_info)
        _write_new_utf8(root / _PAYLOAD_MANIFEST, payload_manifest)

        tag_files = _tag_files(root)
        _write_new_utf8(root / _TAG_MANIFEST, _render_manifest(root, tag_files))
        return BagItWriteResult(
            bag_root=root,
            payload_file_count=len(payload_files),
            payload_bytes=payload_bytes,
            tag_file_count=len(tag_files),
        )

    def refresh_tagmanifest(self, pending_root: Path) -> BagItWriteResult:
        """Atomically refresh only this writer's tag manifest after proof mutation."""

        root = _require_pending_directory(pending_root)
        _require_root_entries(root, _COMPLETED_ROOT_ENTRIES)
        payload_files = _regular_files_under(root, _PAYLOAD_DIRECTORY)
        proof_files = _regular_files_under(root, _PROOF_DIRECTORY)
        if not payload_files or not proof_files:
            raise BagItWriterError(
                "Completed pending bag is missing payload or proof files."
            )

        _require_writer_owned_metadata(root, payload_files)
        _require_current_payload_manifest(root, payload_files)
        tag_files = _tag_files(root)
        _require_refreshable_existing_tagmanifest(root, tag_files)

        replacement = _render_manifest(root, tag_files)
        _atomic_replace_utf8(root / _TAG_MANIFEST, replacement)
        payload_bytes = sum(path.stat().st_size for path in payload_files)
        return BagItWriteResult(
            bag_root=root,
            payload_file_count=len(payload_files),
            payload_bytes=payload_bytes,
            tag_file_count=len(tag_files),
        )

    def finalize_tagmanifest(self, pending_root: Path) -> BagItWriteResult:
        """Bind the complete final tag-file set after receipt finalization.

        The staging transaction calls this exactly once after every immutable
        receipt-bound artifact and the derived offline receipt exist. Payload
        metadata must still match the writer's initial BagIt output.
        """

        root = _require_pending_directory(pending_root)
        _require_root_entries(root, _COMPLETED_ROOT_ENTRIES)
        payload_files = _regular_files_under(root, _PAYLOAD_DIRECTORY)
        proof_files = _regular_files_under(root, _PROOF_DIRECTORY)
        if not payload_files or not proof_files:
            raise BagItWriterError(
                "Completed pending bag is missing payload or proof files."
            )

        _require_writer_owned_metadata(root, payload_files)
        _require_current_payload_manifest(root, payload_files)
        tag_files = _tag_files(root)
        replacement = _render_manifest(root, tag_files)
        _atomic_replace_utf8(root / _TAG_MANIFEST, replacement)
        payload_bytes = sum(path.stat().st_size for path in payload_files)
        return BagItWriteResult(
            bag_root=root,
            payload_file_count=len(payload_files),
            payload_bytes=payload_bytes,
            tag_file_count=len(tag_files),
        )


def _require_pending_directory(pending_root: Path) -> Path:
    if not isinstance(pending_root, Path):
        raise BagItWriterError("Pending stage root must be a pathlib.Path.")
    try:
        root_stat = pending_root.lstat()
    except FileNotFoundError as exc:
        raise BagItWriterError("Pending stage root does not exist.") from exc
    except OSError as exc:
        raise BagItWriterError("Pending stage root could not be inspected.") from exc
    if stat.S_ISLNK(root_stat.st_mode):
        raise BagItWriterError("Pending stage root must not be a symlink.")
    if not stat.S_ISDIR(root_stat.st_mode):
        raise BagItWriterError("Pending stage root is not a directory.")
    return pending_root.resolve(strict=True)


def _require_root_entries(root: Path, expected: frozenset[str]) -> None:
    try:
        actual = frozenset(entry.name for entry in os.scandir(root))
    except OSError as exc:
        raise BagItWriterError("Pending stage root could not be enumerated.") from exc
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise BagItWriterError(
            "Pending stage root structure is invalid; "
            f"missing={missing}, extra={extra}."
        )

    for directory_name in (_PAYLOAD_DIRECTORY, _PROOF_DIRECTORY):
        directory = root / directory_name
        try:
            mode = directory.lstat().st_mode
        except OSError as exc:
            raise BagItWriterError(
                f"Pending stage {directory_name}/ could not be inspected."
            ) from exc
        if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
            raise BagItWriterError(
                f"Pending stage {directory_name}/ must be a real directory."
            )

    for file_name in expected - _INITIAL_ROOT_ENTRIES:
        candidate = root / file_name
        try:
            mode = candidate.lstat().st_mode
        except OSError as exc:
            raise BagItWriterError(
                f"Pending stage root file {file_name} could not be inspected."
            ) from exc
        if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
            raise BagItWriterError(
                f"Pending stage root file {file_name} must be a regular file."
            )


def _regular_files_under(root: Path, directory_name: str) -> tuple[Path, ...]:
    directory = root / directory_name
    files: list[Path] = []

    def visit(current: Path) -> None:
        try:
            entries = sorted(os.scandir(current), key=lambda entry: entry.name)
        except OSError as exc:
            raise BagItWriterError(
                f"Pending stage {directory_name}/ could not be enumerated."
            ) from exc
        for entry in entries:
            candidate = Path(entry.path)
            try:
                mode = entry.stat(follow_symlinks=False).st_mode
            except OSError as exc:
                raise BagItWriterError(
                    f"Pending stage member could not be inspected: "
                    f"{_relative_posix(root, candidate)}."
                ) from exc
            relative = _relative_posix(root, candidate)
            if stat.S_ISLNK(mode):
                raise BagItWriterError(f"Pending stage contains a symlink: {relative}.")
            if stat.S_ISDIR(mode):
                visit(candidate)
            elif stat.S_ISREG(mode):
                files.append(candidate)
            else:
                raise BagItWriterError(
                    f"Pending stage contains a special file: {relative}."
                )

    visit(directory)
    return tuple(sorted(files, key=lambda path: _relative_posix(root, path)))


def _tag_files(root: Path) -> tuple[Path, ...]:
    proof_files = _regular_files_under(root, _PROOF_DIRECTORY)
    root_tag_files = tuple(
        root / name for name in (_BAGIT_FILE, _BAG_INFO_FILE, _PAYLOAD_MANIFEST)
    )
    return tuple(
        sorted(
            (*root_tag_files, *proof_files),
            key=lambda path: _relative_posix(root, path),
        )
    )


def _render_manifest(root: Path, files: tuple[Path, ...]) -> str:
    return "".join(
        f"{_stream_sha256(path)}  {_relative_posix(root, path)}\n" for path in files
    )


def _stream_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(_HASH_CHUNK_SIZE), b""):
                digest.update(chunk)
    except OSError as exc:
        raise BagItWriterError("A staged file could not be hashed.") from exc
    return digest.hexdigest()


def _relative_posix(root: Path, path: Path) -> str:
    try:
        relative = path.relative_to(root)
        rendered = relative.as_posix()
        rendered.encode("utf-8", errors="strict")
    except (UnicodeEncodeError, ValueError) as exc:
        raise BagItWriterError(
            "A staged path is not a valid in-scope UTF-8 path."
        ) from exc
    if PurePosixPath(rendered).is_absolute() or ".." in PurePosixPath(rendered).parts:
        raise BagItWriterError("A staged path escapes the pending stage.")
    return rendered


def _write_new_utf8(path: Path, content: str) -> None:
    try:
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
    except FileExistsError as exc:
        raise BagItWriterError(f"Refusing to overwrite existing {path.name}.") from exc
    except OSError as exc:
        raise BagItWriterError(f"Could not create {path.name}.") from exc


def _atomic_replace_utf8(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    try:
        with temporary.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except FileExistsError as exc:
        raise BagItWriterError(
            "A tag-manifest refresh is already in progress."
        ) from exc
    except OSError as exc:
        raise BagItWriterError(
            "Tag manifest could not be atomically refreshed."
        ) from exc
    finally:
        with suppress(OSError):
            temporary.unlink(missing_ok=True)


def _require_writer_owned_metadata(root: Path, payload_files: tuple[Path, ...]) -> None:
    expected_bagit = (
        f"BagIt-Version: {_BAGIT_VERSION}\n"
        f"Tag-File-Character-Encoding: {_TAG_FILE_ENCODING}\n"
    )
    try:
        bagit_text = (root / _BAGIT_FILE).read_text(encoding="utf-8")
        bag_info = (root / _BAG_INFO_FILE).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise BagItWriterError("Existing BagIt metadata could not be read.") from exc
    if bagit_text != expected_bagit:
        raise BagItWriterError("Existing bagit.txt was not produced by this writer.")
    lines = bag_info.splitlines()
    if len(lines) != 3:
        raise BagItWriterError("Existing bag-info.txt was not produced by this writer.")
    try:
        date.fromisoformat(lines[0].removeprefix("Bagging-Date: "))
    except ValueError as exc:
        raise BagItWriterError(
            "Existing bag-info.txt was not produced by this writer."
        ) from exc
    payload_bytes = sum(path.stat().st_size for path in payload_files)
    expected_lines = (
        f"Bag-Software-Agent: {_SOFTWARE_AGENT}",
        f"Payload-Oxum: {payload_bytes}.{len(payload_files)}",
    )
    if (
        not lines[0].startswith("Bagging-Date: ")
        or tuple(lines[1:]) != expected_lines
        or not bag_info.endswith("\n")
    ):
        raise BagItWriterError("Existing bag-info.txt was not produced by this writer.")


def _require_current_payload_manifest(
    root: Path, payload_files: tuple[Path, ...]
) -> None:
    expected = _render_manifest(root, payload_files)
    try:
        actual = (root / _PAYLOAD_MANIFEST).read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise BagItWriterError("Existing payload manifest could not be read.") from exc
    if actual != expected:
        raise BagItWriterError(
            "Payload manifest or staged payload changed before refresh."
        )


def _require_refreshable_existing_tagmanifest(
    root: Path, tag_files: tuple[Path, ...]
) -> None:
    manifest_path = root / _TAG_MANIFEST
    try:
        existing = manifest_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise BagItWriterError("Existing tag manifest could not be read.") from exc

    expected_paths = tuple(_relative_posix(root, path) for path in tag_files)
    existing_entries = _parse_sha256_manifest(existing)
    if tuple(path for path, _digest in existing_entries) != expected_paths:
        raise BagItWriterError(
            "Existing tag manifest does not describe this writer's complete tag set."
        )

    current_digests = {
        _relative_posix(root, path): _stream_sha256(path) for path in tag_files
    }
    changed_paths = {
        PurePosixPath(path)
        for path, digest in existing_entries
        if current_digests[path] != digest
    }
    if not changed_paths.issubset({_REFRESHABLE_TAG_PATH}):
        raise BagItWriterError(
            "Only name-atlas/verification_report.json may change before refresh."
        )


def _parse_sha256_manifest(content: str) -> tuple[tuple[str, str], ...]:
    entries: list[tuple[str, str]] = []
    for line in content.splitlines():
        try:
            digest, path = line.split("  ", maxsplit=1)
        except ValueError as exc:
            raise BagItWriterError("Existing tag manifest is malformed.") from exc
        invalid_digest = len(digest) != 64 or any(
            character not in "0123456789abcdef" for character in digest
        )
        if invalid_digest:
            raise BagItWriterError(
                "Existing tag manifest contains an invalid SHA-256 digest."
            )
        invalid_path = (
            not path
            or PurePosixPath(path).is_absolute()
            or ".." in PurePosixPath(path).parts
        )
        if invalid_path:
            raise BagItWriterError("Existing tag manifest contains an invalid path.")
        entries.append((path, digest))
    if len(entries) != len({path for path, _digest in entries}):
        raise BagItWriterError("Existing tag manifest contains duplicate paths.")
    return tuple(entries)
