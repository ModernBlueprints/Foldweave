"""Atomic no-replace directory promotion on supported judge platforms."""

from __future__ import annotations

import ctypes
import errno
import os
import sys
from pathlib import Path

DARWIN_AT_FDCWD = -2
DARWIN_RENAME_EXCL = 0x00000004
LINUX_AT_FDCWD = -100
LINUX_RENAME_NOREPLACE = 1


def promote_directory_no_replace(source: Path, destination: Path) -> None:
    """Atomically rename a pending directory only when destination is absent."""

    library = ctypes.CDLL(None, use_errno=True)
    source_bytes = os.fsencode(source)
    destination_bytes = os.fsencode(destination)
    if sys.platform == "darwin":
        rename = library.renameatx_np
        rename.argtypes = (
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        )
        rename.restype = ctypes.c_int
        result = rename(
            DARWIN_AT_FDCWD,
            source_bytes,
            DARWIN_AT_FDCWD,
            destination_bytes,
            DARWIN_RENAME_EXCL,
        )
    elif sys.platform.startswith("linux"):
        try:
            rename = library.renameat2
        except AttributeError as exc:
            raise OSError("Atomic no-replace promotion is unavailable.") from exc
        rename.argtypes = (
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        )
        rename.restype = ctypes.c_int
        result = rename(
            LINUX_AT_FDCWD,
            source_bytes,
            LINUX_AT_FDCWD,
            destination_bytes,
            LINUX_RENAME_NOREPLACE,
        )
    else:
        raise OSError("Atomic no-replace promotion is unsupported on this platform.")

    if result == 0:
        return
    error_number = ctypes.get_errno()
    if error_number in {errno.EEXIST, errno.ENOTEMPTY}:
        raise FileExistsError(
            error_number,
            "Final stage destination already exists.",
            destination,
        )
    raise OSError(error_number, os.strerror(error_number), destination)
