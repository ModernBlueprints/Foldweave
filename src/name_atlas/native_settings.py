"""Trusted native credential and endpoint settings for Foldweave."""

from __future__ import annotations

import os
import sys
import threading
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Literal, Protocol, TypeVar
from urllib.parse import urlsplit, urlunsplit

from pydantic import Field, model_validator

from name_atlas.folder_refactor.contracts import StrictFrozenModel

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OFFICIAL_OPENAI_ENDPOINT = "https://api.openai.com/v1"
OFFICIAL_OPENAI_MODEL = "gpt-5.6"
KEYCHAIN_SERVICE = "com.modernblueprints.foldweave.openai-api"
KEYCHAIN_ACCOUNT = "default"
MAX_CREDENTIAL_BYTES = 16 * 1024
SECURE_PROMPT_TIMEOUT_SECONDS = 300.0


class CredentialStoreError(RuntimeError):
    """One stable trusted-store failure that never includes credential data."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class DirectEndpointProfile(StrictFrozenModel):
    """One validated direct-provider destination and truthful claim profile."""

    profile_kind: Literal["openai_official", "compatible"]
    endpoint: str = Field(min_length=1, max_length=2_048)
    model_alias: str = Field(min_length=1, max_length=200)
    store_false_claim: bool
    openai_pricing_claim: bool

    @model_validator(mode="after")
    def require_bounded_endpoint(self) -> DirectEndpointProfile:
        parsed = urlsplit(self.endpoint)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(
                "Direct endpoint requires HTTPS without userinfo, query, or fragment."
            )
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Direct endpoint port is invalid.") from exc
        canonical_host = parsed.hostname.casefold()
        canonical_netloc = (
            canonical_host if port is None else f"{canonical_host}:{port}"
        )
        canonical_path = parsed.path.rstrip("/") or "/"
        canonical = urlunsplit(("https", canonical_netloc, canonical_path, "", ""))
        if self.endpoint != canonical:
            raise ValueError("Direct endpoint must use its canonical HTTPS form.")
        if self.profile_kind == "openai_official":
            if (
                self.endpoint != OFFICIAL_OPENAI_ENDPOINT
                or port is not None
                or self.model_alias != OFFICIAL_OPENAI_MODEL
                or self.store_false_claim is not True
                or self.openai_pricing_claim is not True
            ):
                raise ValueError("Official OpenAI profile fields are fixed.")
        elif self.store_false_claim or self.openai_pricing_claim:
            raise ValueError(
                "Compatible endpoints cannot inherit OpenAI retention or pricing "
                "claims."
            )
        return self

    @classmethod
    def official(cls) -> DirectEndpointProfile:
        return cls(
            profile_kind="openai_official",
            endpoint=OFFICIAL_OPENAI_ENDPOINT,
            model_alias=OFFICIAL_OPENAI_MODEL,
            store_false_claim=True,
            openai_pricing_claim=True,
        )

    @classmethod
    def compatible(
        cls,
        *,
        endpoint: str,
        model_alias: str,
    ) -> DirectEndpointProfile:
        parsed = urlsplit(endpoint.strip())
        if (
            parsed.scheme.casefold() != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(
                "Compatible endpoint requires HTTPS without userinfo, query, or "
                "fragment."
            )
        try:
            port = parsed.port
        except ValueError as exc:
            raise ValueError("Compatible endpoint port is invalid.") from exc
        netloc = parsed.hostname.casefold()
        if port is not None:
            netloc = f"{netloc}:{port}"
        path = parsed.path.rstrip("/") or "/"
        canonical = urlunsplit((parsed.scheme.casefold(), netloc, path, "", ""))
        return cls(
            profile_kind="compatible",
            endpoint=canonical,
            model_alias=model_alias.strip(),
            store_false_claim=False,
            openai_pricing_claim=False,
        )


class CredentialStatus(StrictFrozenModel):
    """Renderer-safe credential state with no secret-derived material."""

    configured: bool
    store_kind: Literal["keychain", "environment", "session"]
    status_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )


class CredentialStore(Protocol):
    """Trusted secret storage boundary used only by Python."""

    def status(self) -> CredentialStatus:
        """Return existence state without reading secret data."""
        ...

    def read(self) -> str:
        """Return the credential only to a trusted provider factory."""
        ...

    def write(self, value: str) -> None:
        """Add or replace the credential without exposing it."""
        ...

    def remove(self) -> bool:
        """Delete the credential and return whether an item existed."""
        ...


@dataclass(slots=True)
class EnvironmentCredentialStore:
    """Read-only qualification credential from an explicitly injected mapping."""

    environ: Mapping[str, str] = field(default_factory=lambda: os.environ)

    def status(self) -> CredentialStatus:
        configured = bool(self.environ.get(OPENAI_API_KEY_ENV, "").strip())
        return CredentialStatus(configured=configured, store_kind="environment")

    def read(self) -> str:
        value = self.environ.get(OPENAI_API_KEY_ENV, "")
        return _validate_credential(value)

    def write(self, value: str) -> None:
        del value
        raise CredentialStoreError(
            "credential_store_read_only",
            "The qualification environment is read-only.",
        )

    def remove(self) -> bool:
        raise CredentialStoreError(
            "credential_store_read_only",
            "The qualification environment is read-only.",
        )


@dataclass(slots=True)
class SessionCredentialStore:
    """Ephemeral trusted store for development and automated verification."""

    _value: str | None = field(default=None, repr=False)

    def status(self) -> CredentialStatus:
        return CredentialStatus(
            configured=self._value is not None,
            store_kind="session",
        )

    def read(self) -> str:
        if self._value is None:
            raise CredentialStoreError(
                "credential_not_configured",
                "No direct API credential is configured.",
            )
        return self._value

    def write(self, value: str) -> None:
        self._value = _validate_credential(value)

    def remove(self) -> bool:
        existed = self._value is not None
        self._value = None
        return existed


class SecurityKeychainAdapter(Protocol):
    """Narrow testable projection of macOS Keychain generic-password calls."""

    def exists(self, *, service: str, account: str) -> bool: ...

    def read(self, *, service: str, account: str) -> bytes: ...

    def write(self, *, service: str, account: str, value: bytes) -> None: ...

    def remove(self, *, service: str, account: str) -> bool: ...


class PyObjCKeychainAdapter:
    """Call Security.framework without backend discovery or shell execution."""

    @staticmethod
    def _security():
        if sys.platform != "darwin":
            raise CredentialStoreError(
                "keychain_unavailable",
                "macOS Keychain is unavailable on this platform.",
            )
        try:
            import Security
        except ImportError as exc:
            raise CredentialStoreError(
                "keychain_unavailable",
                "macOS Keychain support is unavailable.",
            ) from exc
        return Security

    def _query(self, *, service: str, account: str) -> dict[object, object]:
        security = self._security()
        return {
            security.kSecClass: security.kSecClassGenericPassword,
            security.kSecAttrService: service,
            security.kSecAttrAccount: account,
        }

    def exists(self, *, service: str, account: str) -> bool:
        security = self._security()
        query = {
            **self._query(service=service, account=account),
            security.kSecReturnAttributes: True,
            security.kSecMatchLimit: security.kSecMatchLimitOne,
        }
        status, _result = security.SecItemCopyMatching(query, None)
        if status == security.errSecSuccess:
            return True
        if status == security.errSecItemNotFound:
            return False
        raise _keychain_error(status)

    def read(self, *, service: str, account: str) -> bytes:
        security = self._security()
        query = {
            **self._query(service=service, account=account),
            security.kSecReturnData: True,
            security.kSecMatchLimit: security.kSecMatchLimitOne,
        }
        status, result = security.SecItemCopyMatching(query, None)
        if status == security.errSecItemNotFound:
            raise CredentialStoreError(
                "credential_not_configured",
                "No direct API credential is configured.",
            )
        if status != security.errSecSuccess or result is None:
            raise _keychain_error(status)
        return bytes(result)

    def write(self, *, service: str, account: str, value: bytes) -> None:
        security = self._security()
        query = self._query(service=service, account=account)
        if self.exists(service=service, account=account):
            status = security.SecItemUpdate(
                query,
                {security.kSecValueData: value},
            )
        else:
            status, _result = security.SecItemAdd(
                {**query, security.kSecValueData: value},
                None,
            )
        if status != security.errSecSuccess:
            raise _keychain_error(status)

    def remove(self, *, service: str, account: str) -> bool:
        security = self._security()
        status = security.SecItemDelete(self._query(service=service, account=account))
        if status == security.errSecSuccess:
            return True
        if status == security.errSecItemNotFound:
            return False
        raise _keychain_error(status)


@dataclass(slots=True)
class MacOSKeychainCredentialStore:
    """Product-user credential in one fixed Keychain generic-password item."""

    adapter: SecurityKeychainAdapter = field(default_factory=PyObjCKeychainAdapter)
    service: str = KEYCHAIN_SERVICE
    account: str = KEYCHAIN_ACCOUNT

    def status(self) -> CredentialStatus:
        try:
            configured = self.adapter.exists(
                service=self.service,
                account=self.account,
            )
        except CredentialStoreError as exc:
            return CredentialStatus(
                configured=False,
                store_kind="keychain",
                status_code=exc.code,
            )
        return CredentialStatus(configured=configured, store_kind="keychain")

    def read(self) -> str:
        raw = self.adapter.read(service=self.service, account=self.account)
        try:
            value = raw.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise CredentialStoreError(
                "credential_invalid",
                "The stored direct API credential is invalid.",
            ) from exc
        return _validate_credential(value)

    def write(self, value: str) -> None:
        validated = _validate_credential(value)
        self.adapter.write(
            service=self.service,
            account=self.account,
            value=validated.encode("utf-8"),
        )

    def remove(self) -> bool:
        return self.adapter.remove(service=self.service, account=self.account)


T = TypeVar("T")


class MainThreadScheduler(Protocol):
    """Run one bounded native UI closure on the Cocoa main thread."""

    def call(self, function: Callable[[], T], *, timeout_seconds: float) -> T: ...


class CocoaMainThreadScheduler:
    """Synchronously await one AppKit closure without moving secrets to HTTP."""

    def call(self, function: Callable[[], T], *, timeout_seconds: float) -> T:
        if threading.current_thread() is threading.main_thread():
            return function()
        try:
            from PyObjCTools import AppHelper
        except ImportError as exc:
            raise CredentialStoreError(
                "native_settings_unavailable",
                "Native settings are unavailable.",
            ) from exc
        completed = threading.Event()
        result: list[T] = []
        failure: list[BaseException] = []

        def invoke() -> None:
            try:
                result.append(function())
            except BaseException as exc:  # noqa: BLE001 - re-raised on caller
                failure.append(exc)
            finally:
                completed.set()

        AppHelper.callAfter(invoke)
        if not completed.wait(timeout_seconds):
            raise CredentialStoreError(
                "native_settings_timeout",
                "Native credential entry timed out.",
            )
        if failure:
            error = failure[0]
            if isinstance(error, CredentialStoreError):
                raise error
            raise CredentialStoreError(
                "native_settings_failed",
                "Native credential entry failed.",
            ) from error
        return result[0]


class SecureCredentialPrompt(Protocol):
    def prompt(self) -> str | None:
        """Return trusted secret input or None when the user cancels."""
        ...


class CocoaSecureCredentialPrompt:
    """Collect a credential with NSSecureTextField on the main thread."""

    def prompt(self) -> str | None:
        if threading.current_thread() is not threading.main_thread():
            raise CredentialStoreError(
                "native_settings_thread_invalid",
                "Secure credential entry must run on the main thread.",
            )
        try:
            from AppKit import (
                NSAlert,
                NSAlertFirstButtonReturn,
                NSMakeRect,
                NSSecureTextField,
            )
        except ImportError as exc:
            raise CredentialStoreError(
                "native_settings_unavailable",
                "Native credential entry is unavailable.",
            ) from exc
        alert = NSAlert.alloc().init()
        alert.setMessageText_("Configure OpenAI API key")
        alert.setInformativeText_(
            "The key is stored in macOS Keychain and never enters the Foldweave "
            "web view."
        )
        alert.addButtonWithTitle_("Save key")
        alert.addButtonWithTitle_("Cancel")
        field = NSSecureTextField.alloc().initWithFrame_(
            NSMakeRect(0.0, 0.0, 420.0, 24.0)
        )
        field.setPlaceholderString_("OpenAI API key")
        alert.setAccessoryView_(field)
        response = alert.runModal()
        try:
            if response != NSAlertFirstButtonReturn:
                return None
            return _validate_credential(str(field.stringValue()))
        finally:
            field.setStringValue_("")


class NativeSettingsResult(StrictFrozenModel):
    """Renderer-safe result of a configure or remove action."""

    status: Literal["configured", "removed", "cancelled", "failed"]
    configured: bool
    status_code: str | None = Field(
        default=None,
        pattern=r"^[a-z0-9_:-]{1,128}$",
    )


class NativeSettingsView(StrictFrozenModel):
    """Complete renderer-safe settings projection."""

    credential: CredentialStatus
    endpoint: str
    endpoint_profile: Literal["openai_official", "compatible"]


@dataclass(slots=True)
class NativeSettingsService:
    """Keep secure entry and trusted storage behind status-only operations."""

    store: CredentialStore
    endpoint: DirectEndpointProfile = field(
        default_factory=DirectEndpointProfile.official
    )
    scheduler: MainThreadScheduler = field(default_factory=CocoaMainThreadScheduler)
    prompt: SecureCredentialPrompt = field(default_factory=CocoaSecureCredentialPrompt)

    def view(self) -> NativeSettingsView:
        return NativeSettingsView(
            credential=self.store.status(),
            endpoint=self.endpoint.endpoint,
            endpoint_profile=self.endpoint.profile_kind,
        )

    def configure(self) -> NativeSettingsResult:
        def collect_and_store() -> bool:
            value = self.prompt.prompt()
            if value is None:
                return False
            self.store.write(value)
            return True

        try:
            configured = self.scheduler.call(
                collect_and_store,
                timeout_seconds=SECURE_PROMPT_TIMEOUT_SECONDS,
            )
        except CredentialStoreError as exc:
            return NativeSettingsResult(
                status="failed",
                configured=self.store.status().configured,
                status_code=exc.code,
            )
        if not configured:
            return NativeSettingsResult(
                status="cancelled",
                configured=self.store.status().configured,
            )
        return NativeSettingsResult(status="configured", configured=True)

    def remove(self) -> NativeSettingsResult:
        try:
            self.store.remove()
        except CredentialStoreError as exc:
            return NativeSettingsResult(
                status="failed",
                configured=self.store.status().configured,
                status_code=exc.code,
            )
        return NativeSettingsResult(status="removed", configured=False)


def _validate_credential(value: str) -> str:
    if not isinstance(value, str):
        raise CredentialStoreError(
            "credential_invalid",
            "The direct API credential is invalid.",
        )
    encoded = value.encode("utf-8", errors="strict")
    if (
        not value
        or value != value.strip()
        or len(encoded) > MAX_CREDENTIAL_BYTES
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise CredentialStoreError(
            "credential_invalid",
            "The direct API credential is invalid.",
        )
    return value


def _keychain_error(status: int) -> CredentialStoreError:
    del status
    return CredentialStoreError(
        "keychain_operation_failed",
        "macOS Keychain could not complete the credential operation.",
    )
