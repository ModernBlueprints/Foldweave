"""Process-local opaque capabilities for native Foldweave path selection."""

from __future__ import annotations

import os
import secrets
import threading
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import Field, model_validator

from name_atlas.folder_refactor.contracts import StrictFrozenModel
from name_atlas.foldweave_companion import current_trusted_public_invocation
from name_atlas.native_bridge import NativePathRole

oslo_tz = ZoneInfo("Europe/Oslo")
LocalHandleChannel = Literal["chatgpt_hosted", "codex_hosted", "local_mcp"]
HANDLE_LIFETIME = timedelta(minutes=30)


class OpaqueLocalItemHandle(StrictFrozenModel):
    """Public, path-free identity for one locally selected item."""

    schema_version: Literal["foldweave-local-item-handle.v1"] = (
        "foldweave-local-item-handle.v1"
    )
    handle: str = Field(pattern=r"^fw_[A-Za-z0-9_-]{43}$")
    role: NativePathRole
    display_name: str = Field(min_length=1, max_length=255)
    expires_at: datetime

    @model_validator(mode="after")
    def require_oslo_expiry(self):
        if self.expires_at.tzinfo is None:
            raise ValueError("Opaque handle expiry must be timezone aware.")
        normalized = self.expires_at.astimezone(oslo_tz)
        if normalized.utcoffset() != self.expires_at.utcoffset():
            raise ValueError("Opaque handle expiry must use Europe/Oslo.")
        return self


class FoldweaveLocalHandleError(RuntimeError):
    """A local capability cannot be resolved within its exact authority."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(frozen=True, slots=True)
class _LocalHandleRecord:
    public: OpaqueLocalItemHandle
    path: Path
    channel: LocalHandleChannel
    public_invocation_binding: tuple[str, str, str] | None


class FoldweaveLocalHandleStore:
    """Keep paths inside the trusted Python process behind expiring handles."""

    def __init__(
        self,
        *,
        clock: Callable[[], datetime] | None = None,
        token_factory: Callable[[], str] | None = None,
    ) -> None:
        self._clock = clock or (lambda: datetime.now(tz=oslo_tz))
        self._token_factory = token_factory or (lambda: secrets.token_urlsafe(32))
        self._records: dict[str, _LocalHandleRecord] = {}
        self._lock = threading.Lock()

    def register(
        self,
        *,
        role: NativePathRole,
        path: Path,
        channel: LocalHandleChannel,
    ) -> OpaqueLocalItemHandle:
        """Register one selected local item without exposing its path."""

        return self._register(
            role=role,
            path=path,
            channel=channel,
            reuse_existing=False,
        )

    def register_or_reuse(
        self,
        *,
        role: NativePathRole,
        path: Path,
        channel: LocalHandleChannel,
    ) -> OpaqueLocalItemHandle:
        """Return the current capability for one trusted path or mint one."""

        return self._register(
            role=role,
            path=path,
            channel=channel,
            reuse_existing=True,
        )

    def _register(
        self,
        *,
        role: NativePathRole,
        path: Path,
        channel: LocalHandleChannel,
        reuse_existing: bool,
    ) -> OpaqueLocalItemHandle:
        """Register one exact role/channel-bound local capability."""

        resolved = _validate_selected_path(role=role, path=path)
        public_invocation_binding = _current_public_binding(channel)
        now = self._now()
        with self._lock:
            self._purge_expired(now)
            if reuse_existing:
                for record in self._records.values():
                    if (
                        record.public.role is role
                        and record.channel == channel
                        and record.path == resolved
                        and record.public_invocation_binding
                        == public_invocation_binding
                    ):
                        return record.public
            token = f"fw_{self._token_factory()}"
            if token in self._records:
                raise FoldweaveLocalHandleError(
                    "handle_collision",
                    "Generated local-item capability already exists.",
                )
            public = OpaqueLocalItemHandle(
                handle=token,
                role=role,
                display_name=resolved.name or "Selected item",
                expires_at=now + HANDLE_LIFETIME,
            )
            record = _LocalHandleRecord(
                public=public,
                path=resolved,
                channel=channel,
                public_invocation_binding=public_invocation_binding,
            )
            self._records[token] = record
        return public

    def resolve(
        self,
        handle: str,
        *,
        role: NativePathRole,
        channel: LocalHandleChannel,
    ) -> Path:
        """Resolve one exact role/channel-bound capability locally."""

        public_invocation_binding = _current_public_binding(channel)
        now = self._now()
        with self._lock:
            record = self._records.get(handle)
            if record is None:
                raise FoldweaveLocalHandleError(
                    "local_handle_unknown",
                    "Local item handle is unknown or expired.",
                )
            if record.public.expires_at <= now:
                del self._records[handle]
                raise FoldweaveLocalHandleError(
                    "local_handle_expired",
                    "Local item handle has expired; choose the item again.",
                )
            if record.public.role is not role:
                raise FoldweaveLocalHandleError(
                    "local_handle_role_mismatch",
                    "Local item handle was issued for another role.",
                )
            if record.channel != channel:
                raise FoldweaveLocalHandleError(
                    "local_handle_channel_mismatch",
                    "Local item handle belongs to another integration channel.",
                )
            if record.public_invocation_binding != public_invocation_binding:
                raise FoldweaveLocalHandleError(
                    "local_handle_public_binding_mismatch",
                    "Local item handle belongs to another paired ChatGPT session.",
                )
            path = record.path
        return _validate_selected_path(role=role, path=path)

    def _now(self) -> datetime:
        value = self._clock()
        if value.tzinfo is None:
            raise ValueError("Local-handle clock must be timezone aware.")
        return value.astimezone(oslo_tz)

    def _purge_expired(self, now: datetime) -> None:
        expired = tuple(
            token
            for token, record in self._records.items()
            if record.public.expires_at <= now
        )
        for token in expired:
            del self._records[token]


def _current_public_binding(
    channel: LocalHandleChannel,
) -> tuple[str, str, str] | None:
    invocation = current_trusted_public_invocation()
    if invocation is None:
        return None
    if channel != "chatgpt_hosted":
        raise FoldweaveLocalHandleError(
            "local_handle_public_channel_invalid",
            "Public ChatGPT authority cannot issue another integration channel.",
        )
    return invocation.handle_binding()


def _validate_selected_path(*, role: NativePathRole, path: Path) -> Path:
    candidate = path.expanduser()
    if not candidate.is_absolute() or not os.path.lexists(candidate):
        raise FoldweaveLocalHandleError(
            "local_item_unavailable",
            "Selected local item is no longer available.",
        )
    resolved = candidate.resolve(strict=True)
    directory_role = role in {
        NativePathRole.SOURCE_FOLDER,
        NativePathRole.OUTPUT_PARENT,
        NativePathRole.RESTORE_DESTINATION,
    }
    if directory_role and not resolved.is_dir():
        raise FoldweaveLocalHandleError(
            "local_item_type_mismatch",
            "Selected local item must be a directory for this role.",
        )
    if role is NativePathRole.CHANGE_FILE and not resolved.is_file():
        raise FoldweaveLocalHandleError(
            "local_item_type_mismatch",
            "Selected local item must be a regular Change File.",
        )
    return resolved
