"""Planner-free, fail-closed filesystem primitives for durable v2 jobs."""

from __future__ import annotations

import fcntl
import hashlib
import os
import stat
import tempfile
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Self

_READ_CHUNK_BYTES = 1024 * 1024


class DurableJobIOError(RuntimeError):
    """A durable-job filesystem operation could not be completed safely."""


class DurableJobLoadError(DurableJobIOError):
    """A durable-job input is absent, unstable, unreadable, or unsupported."""


class DurableJobWriteError(DurableJobIOError):
    """A durable-job write could not be completed atomically."""


class DurableJobLockError(DurableJobWriteError):
    """Another process currently owns the durable-job mutation lock."""


@dataclass(frozen=True, slots=True)
class StableRegularFileRead:
    """Exact bytes and local identity from one stable no-follow regular-file read."""

    path: Path
    payload: bytes
    device: int
    inode: int
    size: int
    modified_ns: int
    sha256: str


def read_stable_regular_file(
    path: Path,
    *,
    max_bytes: int | None = None,
) -> StableRegularFileRead:
    """Read one regular file once and reject replacement during the read."""

    if not isinstance(path, Path):
        raise DurableJobLoadError("Durable input path must be a pathlib.Path.")
    if max_bytes is not None and max_bytes < 0:
        raise ValueError("max_bytes must be nonnegative when supplied.")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise DurableJobLoadError(
            f"Durable input cannot be opened as a regular file: {path}"
        ) from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise DurableJobLoadError("Durable input must be a regular file.")
        if max_bytes is not None and before.st_size > max_bytes:
            raise DurableJobLoadError(
                f"Durable input exceeds the {max_bytes}-byte limit."
            )
        chunks: list[bytes] = []
        digest = hashlib.sha256()
        observed_size = 0
        while True:
            chunk = os.read(descriptor, _READ_CHUNK_BYTES)
            if not chunk:
                break
            observed_size += len(chunk)
            if max_bytes is not None and observed_size > max_bytes:
                raise DurableJobLoadError(
                    f"Durable input exceeds the {max_bytes}-byte limit."
                )
            digest.update(chunk)
            chunks.append(chunk)
        after = os.fstat(descriptor)
    except OSError as exc:
        raise DurableJobLoadError(
            "Durable input could not be read completely."
        ) from exc
    finally:
        os.close(descriptor)

    stable_fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns")
    if any(getattr(before, name) != getattr(after, name) for name in stable_fields):
        raise DurableJobLoadError("Durable input changed while it was being read.")
    if observed_size != after.st_size:
        raise DurableJobLoadError("Durable input size changed while it was read.")
    try:
        path_state = path.lstat()
    except OSError as exc:
        raise DurableJobLoadError(
            "Durable input disappeared after it was read."
        ) from exc
    if stat.S_ISLNK(path_state.st_mode) or not stat.S_ISREG(path_state.st_mode):
        raise DurableJobLoadError("Durable input must remain a regular file.")
    if any(getattr(after, name) != getattr(path_state, name) for name in stable_fields):
        raise DurableJobLoadError("Durable input was replaced while it was read.")
    return StableRegularFileRead(
        path=path.resolve(strict=True),
        payload=b"".join(chunks),
        device=after.st_dev,
        inode=after.st_ino,
        size=after.st_size,
        modified_ns=after.st_mtime_ns,
        sha256=digest.hexdigest(),
    )


class DurableJobFileLock:
    """One process-held, non-blocking writer lock beside a job file."""

    def __init__(self, job_path: Path) -> None:
        self.job_path = job_path.resolve(strict=False)
        self.lock_path = self.job_path.with_suffix(f"{self.job_path.suffix}.lock")
        self._descriptor: int | None = None

    def __enter__(self) -> Self:
        _require_real_parent(self.job_path, create=True)
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(self.lock_path, flags, 0o600)
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise DurableJobLockError("Durable-job lock is not a regular file.")
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except DurableJobLockError:
            with suppress(UnboundLocalError, OSError):
                os.close(descriptor)
            raise
        except (BlockingIOError, OSError) as exc:
            with suppress(UnboundLocalError, OSError):
                os.close(descriptor)
            raise DurableJobLockError(
                "Durable job is already open for mutation."
            ) from exc
        self._descriptor = descriptor
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc_value, traceback
        descriptor = self._descriptor
        self._descriptor = None
        if descriptor is not None:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
            finally:
                os.close(descriptor)

    @property
    def held(self) -> bool:
        """Return whether this context currently owns the process lock."""

        return self._descriptor is not None


def atomic_write_regular_file(path: Path, payload: bytes) -> None:
    """Atomically replace one regular file and durably sync its parent directory."""

    if not isinstance(payload, bytes):
        raise DurableJobWriteError("Durable-job payload must be bytes.")
    parent = _require_real_parent(path, create=True)
    temporary_path: Path | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            dir=parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        )
        temporary_path = Path(temporary_name)
        try:
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
        except BaseException:
            with suppress(OSError):
                os.close(descriptor)
            raise
        if os.path.lexists(path):
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                raise DurableJobWriteError(
                    "Durable-job destination must remain a regular file."
                )
        os.replace(temporary_path, path)
        temporary_path = None
        _fsync_directory(parent)
    except DurableJobWriteError:
        raise
    except OSError as exc:
        raise DurableJobWriteError(
            "Durable job could not be written atomically."
        ) from exc
    finally:
        if temporary_path is not None:
            with suppress(OSError):
                temporary_path.unlink()


def _require_real_parent(path: Path, *, create: bool) -> Path:
    parent = path.resolve(strict=False).parent
    try:
        if create:
            parent.mkdir(parents=True, exist_ok=True)
        metadata = parent.lstat()
    except OSError as exc:
        raise DurableJobWriteError("Durable-job parent is unavailable.") from exc
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise DurableJobWriteError("Durable-job parent must be a real directory.")
    return parent


def _fsync_directory(path: Path) -> None:
    flags = os.O_RDONLY
    if hasattr(os, "O_DIRECTORY"):
        flags |= os.O_DIRECTORY
    descriptor = os.open(path, flags)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
