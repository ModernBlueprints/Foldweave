"""Bounded native macOS path selection and Finder integration."""

from __future__ import annotations

import asyncio
import os
import stat
import sys
import threading
from contextlib import suppress
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from types import MappingProxyType
from typing import Protocol

OSASCRIPT_PATH = Path("/usr/bin/osascript")
OPEN_PATH = Path("/usr/bin/open")
PICKER_TIMEOUT_SECONDS = 120.0
FINDER_TIMEOUT_SECONDS = 10.0
PROCESS_TERMINATION_GRACE_SECONDS = 1.0
MAX_PICKER_OUTPUT_BYTES = 16 * 1024
_SELECTED_MARKER = "NAME_ATLAS_SELECTED"
_CANCELLED_MARKER = "NAME_ATLAS_CANCELLED"


class NativePathRole(StrEnum):
    """The only browser-selectable native path roles."""

    SOURCE_FOLDER = "source_folder"
    OUTPUT_PARENT = "output_parent"
    CHANGE_FILE = "change_file"
    RESTORE_DESTINATION = "restore_destination"


class NativeSelectionStatus(StrEnum):
    """One explicit native chooser outcome."""

    SELECTED = "selected"
    CANCELLED = "cancelled"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    FAILED = "failed"


class NativeOpenStatus(StrEnum):
    """One explicit Finder-opening outcome."""

    OPENED = "opened"
    UNAVAILABLE = "unavailable"
    TIMEOUT = "timeout"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class NativePathSelection:
    """A native chooser result that carries a path only after selection."""

    status: NativeSelectionStatus
    path: Path | None = None
    reason_code: str | None = None

    def __post_init__(self) -> None:
        if self.status is NativeSelectionStatus.SELECTED:
            if self.path is None or not self.path.is_absolute():
                raise ValueError("A selected native path must be absolute.")
        elif self.path is not None:
            raise ValueError("A non-selection cannot carry a path.")


@dataclass(frozen=True, slots=True)
class NativeOpenResult:
    """The bounded result of opening one server-authorized Finder path."""

    status: NativeOpenStatus
    reason_code: str | None = None


class NativePathBridge(Protocol):
    """Select local paths and open one verified path without shell authority."""

    async def choose_path(self, role: NativePathRole) -> NativePathSelection:
        """Run at most one fixed native chooser and return no path on failure."""
        ...

    async def show_in_finder(self, path: Path) -> NativeOpenResult:
        """Open one caller-verified real directory through exact /usr/bin/open."""
        ...


class _AsyncProcess(Protocol):
    returncode: int | None

    async def communicate(self) -> tuple[bytes, bytes]: ...

    async def wait(self) -> int: ...

    def terminate(self) -> None: ...

    def kill(self) -> None: ...


class _AsyncProcessFactory(Protocol):
    async def __call__(
        self,
        program: str,
        *args: str,
        stdout: int | None,
        stderr: int | None,
    ) -> _AsyncProcess: ...


def _picker_script(*, chooser: str, prompt: str) -> str:
    return f'''try
    set pickedItem to {chooser} with prompt "{prompt}"
    return "{_SELECTED_MARKER}" & linefeed & POSIX path of pickedItem
on error errorMessage number errorNumber
    if errorNumber is -128 then
        return "{_CANCELLED_MARKER}"
    end if
    error errorMessage number errorNumber
end try'''


FIXED_PICKER_SCRIPTS = MappingProxyType(
    {
        NativePathRole.SOURCE_FOLDER: _picker_script(
            chooser="choose folder",
            prompt="Choose the folder to organize",
        ),
        NativePathRole.OUTPUT_PARENT: _picker_script(
            chooser="choose folder",
            prompt="Choose where Foldweave should create the result",
        ),
        NativePathRole.CHANGE_FILE: _picker_script(
            chooser="choose file",
            prompt="Choose a Foldweave Change File",
        ),
        NativePathRole.RESTORE_DESTINATION: _picker_script(
            chooser="choose folder",
            prompt="Choose where Foldweave should recreate the original layout",
        ),
    }
)

_PICKER_PROCESS_LOCK = threading.Lock()


@dataclass(slots=True)
class MacOSNativePathBridge:
    """Invoke only fixed macOS utilities through shell-free subprocess calls."""

    platform_name: str = field(default_factory=lambda: sys.platform)
    osascript_path: Path = field(default=OSASCRIPT_PATH, init=False)
    open_path: Path = field(default=OPEN_PATH, init=False)
    picker_timeout_seconds: float = PICKER_TIMEOUT_SECONDS
    finder_timeout_seconds: float = FINDER_TIMEOUT_SECONDS
    termination_grace_seconds: float = PROCESS_TERMINATION_GRACE_SECONDS
    process_factory: _AsyncProcessFactory = field(
        default=asyncio.create_subprocess_exec,
        repr=False,
    )

    async def choose_path(self, role: NativePathRole) -> NativePathSelection:
        """Run one immutable AppleScript selected only through a strict role enum."""

        if self.platform_name != "darwin" or not _is_executable(self.osascript_path):
            return NativePathSelection(
                status=NativeSelectionStatus.UNAVAILABLE,
                reason_code="picker_unavailable",
            )
        if not _PICKER_PROCESS_LOCK.acquire(blocking=False):
            return NativePathSelection(
                status=NativeSelectionStatus.FAILED,
                reason_code="picker_busy",
            )
        try:
            try:
                process = await self.process_factory(
                    str(self.osascript_path),
                    "-e",
                    FIXED_PICKER_SCRIPTS[role],
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
            except OSError:
                return NativePathSelection(
                    status=NativeSelectionStatus.FAILED,
                    reason_code="picker_failed",
                )
            try:
                stdout, _stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.picker_timeout_seconds,
                )
            except TimeoutError:
                await _terminate_and_reap(
                    process,
                    grace_seconds=self.termination_grace_seconds,
                )
                return NativePathSelection(
                    status=NativeSelectionStatus.TIMEOUT,
                    reason_code="picker_timeout",
                )
            except asyncio.CancelledError:
                await asyncio.shield(
                    _terminate_and_reap(
                        process,
                        grace_seconds=self.termination_grace_seconds,
                    )
                )
                raise
            except OSError:
                await _terminate_and_reap(
                    process,
                    grace_seconds=self.termination_grace_seconds,
                )
                return NativePathSelection(
                    status=NativeSelectionStatus.FAILED,
                    reason_code="picker_failed",
                )
            if process.returncode != 0:
                return NativePathSelection(
                    status=NativeSelectionStatus.FAILED,
                    reason_code="picker_failed",
                )
            return _parse_picker_output(stdout)
        finally:
            _PICKER_PROCESS_LOCK.release()

    async def show_in_finder(self, path: Path) -> NativeOpenResult:
        """Open one absolute real directory without accepting shell syntax."""

        if self.platform_name != "darwin" or not _is_executable(self.open_path):
            return NativeOpenResult(
                status=NativeOpenStatus.UNAVAILABLE,
                reason_code="finder_unavailable",
            )
        if not _is_real_directory(path):
            return NativeOpenResult(
                status=NativeOpenStatus.FAILED,
                reason_code="finder_path_invalid",
            )
        try:
            process = await self.process_factory(
                str(self.open_path),
                str(path),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.PIPE,
            )
        except OSError:
            return NativeOpenResult(
                status=NativeOpenStatus.FAILED,
                reason_code="finder_failed",
            )
        try:
            await asyncio.wait_for(
                process.communicate(),
                timeout=self.finder_timeout_seconds,
            )
        except TimeoutError:
            await _terminate_and_reap(
                process,
                grace_seconds=self.termination_grace_seconds,
            )
            return NativeOpenResult(
                status=NativeOpenStatus.TIMEOUT,
                reason_code="finder_timeout",
            )
        except asyncio.CancelledError:
            await asyncio.shield(
                _terminate_and_reap(
                    process,
                    grace_seconds=self.termination_grace_seconds,
                )
            )
            raise
        except OSError:
            await _terminate_and_reap(
                process,
                grace_seconds=self.termination_grace_seconds,
            )
            return NativeOpenResult(
                status=NativeOpenStatus.FAILED,
                reason_code="finder_failed",
            )
        if process.returncode != 0:
            return NativeOpenResult(
                status=NativeOpenStatus.FAILED,
                reason_code="finder_failed",
            )
        return NativeOpenResult(status=NativeOpenStatus.OPENED)


def _parse_picker_output(stdout: bytes) -> NativePathSelection:
    if not stdout or len(stdout) > MAX_PICKER_OUTPUT_BYTES:
        return _invalid_picker_output()
    try:
        text = stdout.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return _invalid_picker_output()
    if text.endswith("\r\n"):
        text = text[:-2]
    elif text.endswith(("\n", "\r")):
        text = text[:-1]
    if text == _CANCELLED_MARKER:
        return NativePathSelection(
            status=NativeSelectionStatus.CANCELLED,
            reason_code="picker_cancelled",
        )
    prefix = f"{_SELECTED_MARKER}\n"
    if not text.startswith(prefix):
        return _invalid_picker_output()
    path_text = text.removeprefix(prefix)
    if not path_text or "\x00" in path_text:
        return _invalid_picker_output()
    selected = Path(path_text)
    if not selected.is_absolute():
        return _invalid_picker_output()
    return NativePathSelection(
        status=NativeSelectionStatus.SELECTED,
        path=selected,
    )


def _invalid_picker_output() -> NativePathSelection:
    return NativePathSelection(
        status=NativeSelectionStatus.FAILED,
        reason_code="picker_output_invalid",
    )


async def _terminate_and_reap(
    process: _AsyncProcess,
    *,
    grace_seconds: float,
) -> None:
    try:
        process.terminate()
    except ProcessLookupError:
        await process.wait()
        return
    try:
        await asyncio.wait_for(process.wait(), timeout=grace_seconds)
        return
    except TimeoutError:
        pass
    with suppress(ProcessLookupError):
        process.kill()
    await process.wait()


def _is_executable(path: Path) -> bool:
    return path.is_file() and os.access(path, os.X_OK)


def _is_real_directory(path: Path) -> bool:
    if not path.is_absolute() or "\x00" in str(path):
        return False
    try:
        metadata = path.lstat()
    except (OSError, ValueError):
        return False
    return stat.S_ISDIR(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode)
