"""Local-only identity, capability, and signed transport authority for Foldweave."""

from __future__ import annotations

import base64
import gzip
import hashlib
import json
import secrets
import threading
import time
import zlib
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Literal

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from pydantic import Field, JsonValue, model_validator

from name_atlas.folder_refactor.contracts import SHA256_PATTERN, StrictFrozenModel
from name_atlas.folder_refactor.serialization import canonical_json_bytes
from name_atlas.native_settings import (
    CredentialStoreError,
    PyObjCKeychainAdapter,
    SecurityKeychainAdapter,
)

DEVICE_KEYCHAIN_SERVICE = "com.modernblueprints.foldweave.device-identity"
DEVICE_KEYCHAIN_ACCOUNT = "default"
DEVICE_ID_PREFIX = "fwd_"
MAX_SIGNED_REQUEST_LIFETIME_MS = 30 * 60 * 1_000
PUBLIC_JOB_CAPABILITY_LIFETIME_MS = 30 * 60 * 1_000
MAX_CLOCK_SKEW_MS = 60 * 1_000
MAX_TRACKED_NONCES = 4_096
MAX_MCP_BODY_BYTES = 1_024 * 1_024
MAX_MCP_RESPONSE_WIRE_BYTES = 1_024 * 1_024
MAX_MCP_RESPONSE_COMPRESSED_BYTES = 768 * 1_024
MAX_MCP_RESPONSE_DECODED_BYTES = 4 * 1_024 * 1_024
MAX_MCP_RESPONSE_ENCODED_CHARACTERS = (MAX_MCP_RESPONSE_COMPRESSED_BYTES * 4 + 2) // 3
COMPANION_RPC_TIMEOUT_MS = 25 * 1_000
MCP_RESPONSE_ENVELOPE_SCHEMA = "foldweave-mcp-response-envelope.v1"
MCP_RESPONSE_BODY_ENCODING = "gzip+base64url"
_SIGNATURE_DOMAIN = b"foldweave-device-envelope-signature.v1\x00"
_PUBLIC_JOB_CAPABILITY_DOMAIN = b"foldweave-public-job-capability.v1\x00"
PUBLIC_JOB_CAPABILITY_PREFIX = "fwjc_"
_MCP_REQUEST_HEADER_ALLOWLIST = frozenset(
    {
        "accept",
        "content-type",
        "last-event-id",
        "mcp-protocol-version",
        "mcp-session-id",
        "x-foldweave-http-method",
    }
)
_MCP_RESPONSE_HEADER_ALLOWLIST = frozenset(
    {"content-type", "mcp-session-id", "retry-after"}
)
_SUPPORTED_PUBLIC_SCOPES = (
    "foldweave.execute",
    "foldweave.plan",
    "foldweave.review",
)
_PUBLIC_TOOL_SCOPES = {
    "accept_plan_and_create_copy": "foldweave.execute",
    "recreate_original": "foldweave.execute",
    "get_change_file": "foldweave.review",
    "get_plan_preview": "foldweave.review",
    "job_status": "foldweave.review",
    "verify_result": "foldweave.review",
    "answer_clarification": "foldweave.plan",
    "choose_local_item": "foldweave.plan",
    "create_or_resume_planning_job": "foldweave.plan",
    "get_compiler_failures": "foldweave.plan",
    "inspect_markdown_links": "foldweave.plan",
    "keep_previous_proposal": "foldweave.plan",
    "list_inventory_page": "foldweave.plan",
    "plan_change": "foldweave.plan",
    "prepare_change_application": "foldweave.plan",
    "read_text_excerpt": "foldweave.plan",
    "request_clarification": "foldweave.plan",
    "revise_plan": "foldweave.plan",
    "submit_plan": "foldweave.plan",
    "submit_plan_revision": "foldweave.plan",
}
_PUBLIC_JOBLESS_TOOLS = frozenset(
    {
        "choose_local_item",
        "create_or_resume_planning_job",
        "plan_change",
        "prepare_change_application",
    }
)
_PUBLIC_JOB_BOUND_TOOLS = frozenset(_PUBLIC_TOOL_SCOPES) - _PUBLIC_JOBLESS_TOOLS


class CompanionContractError(RuntimeError):
    """One stable local companion boundary failure without secret material."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class CompanionDeviceIdentityV1(StrictFrozenModel):
    """Public, gateway-safe identity for one verified Foldweave installation."""

    schema_version: Literal["foldweave-device-identity.v1"] = (
        "foldweave-device-identity.v1"
    )
    device_id: str = Field(pattern=r"^fwd_[a-f0-9]{32}$")
    public_key: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")

    def public_jwk(self) -> dict[str, str]:
        """Return the exact public-only JWK accepted by the gateway."""

        return {"crv": "Ed25519", "kty": "OKP", "x": self.public_key}

    def registration_body(self, *, device_name: str) -> dict[str, JsonValue]:
        """Return one strict path-free registration body."""

        normalized = device_name.strip()
        if (
            not normalized
            or len(normalized) > 80
            or any(
                ord(character) < 32 or ord(character) == 127 for character in normalized
            )
        ):
            raise CompanionContractError(
                "device_name_invalid",
                "The Foldweave device name is invalid.",
            )
        return {
            "deviceId": self.device_id,
            "deviceName": normalized,
            "publicKeyJwk": self.public_jwk(),
            "schemaVersion": "foldweave-device-registration.v1",
        }


class _StoredDeviceIdentityV1(StrictFrozenModel):
    """Keychain-only serialization of the device identity."""

    schema_version: Literal["foldweave-device-key.v1"] = "foldweave-device-key.v1"
    device_id: str = Field(pattern=r"^fwd_[a-f0-9]{32}$")
    private_key: str = Field(pattern=r"^[A-Za-z0-9_-]{43}$")


class CompanionSignedEnvelopeV1(StrictFrozenModel):
    """Canonical device-signed request or response forwarded by the gateway."""

    schema_version: Literal["foldweave-device-envelope.v1"] = (
        "foldweave-device-envelope.v1"
    )
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    issued_at: int = Field(ge=0)
    expires_at: int = Field(ge=0)
    sequence: int = Field(ge=1)
    nonce: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    body: dict[str, JsonValue]
    body_sha256: str = Field(pattern=SHA256_PATTERN)
    signature: str = Field(pattern=r"^[A-Za-z0-9_-]{86}$")

    @model_validator(mode="after")
    def require_canonical_body_and_lifetime(self) -> CompanionSignedEnvelopeV1:
        lifetime = self.expires_at - self.issued_at
        if lifetime <= 0 or lifetime > MAX_SIGNED_REQUEST_LIFETIME_MS:
            raise ValueError("Signed companion envelope lifetime is invalid.")
        if hashlib.sha256(canonical_json_bytes(self.body)).hexdigest() != (
            self.body_sha256
        ):
            raise ValueError("Signed companion envelope body digest is invalid.")
        return self

    def unsigned_wire_payload(self) -> dict[str, JsonValue]:
        """Return the exact camel-case gateway signature domain payload."""

        return {
            "body": self.body,
            "bodyDigest": self.body_sha256,
            "expiresAt": self.expires_at,
            "issuedAt": self.issued_at,
            "nonce": self.nonce,
            "requestId": self.request_id,
            "schemaVersion": self.schema_version,
            "sequence": self.sequence,
        }

    def wire_payload(self) -> dict[str, JsonValue]:
        """Return the exact gateway JSON envelope without local-only fields."""

        return {**self.unsigned_wire_payload(), "signature": self.signature}


class CompanionChallengeV1(StrictFrozenModel):
    """One short-lived challenge sent by the paired gateway session."""

    message_type: Literal["companion_challenge"] = "companion_challenge"
    challenge: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    expires_at: int = Field(ge=0)
    session_id: str = Field(pattern=r"^[A-Za-z0-9_-]{32,128}$")


class TrustedPublicInvocationContextV1(StrictFrozenModel):
    """OAuth- and paired-device-bound authority for one public MCP operation."""

    schema_version: Literal["foldweave-public-invocation.v1"] = (
        "foldweave-public-invocation.v1"
    )
    channel: Literal["chatgpt_hosted"] = "chatgpt_hosted"
    device_id: str = Field(pattern=r"^fwd_[a-f0-9]{32}$")
    session_id: str = Field(pattern=r"^[A-Za-z0-9_-]{32,128}$")
    oauth_grant_fingerprint: str = Field(pattern=SHA256_PATTERN)
    scopes: tuple[str, ...]
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    issued_at: int = Field(ge=0)
    expires_at: int = Field(ge=0)
    sequence: int = Field(ge=1)
    nonce: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    body_sha256: str = Field(pattern=SHA256_PATTERN)
    operation_sha256: str = Field(pattern=SHA256_PATTERN)
    job_id: str | None = Field(default=None, pattern=r"^[a-f0-9]{32}$")
    revoked_at: int | None = Field(default=None, ge=0)

    @model_validator(mode="after")
    def require_bounded_authority(self) -> TrustedPublicInvocationContextV1:
        if self.scopes != tuple(sorted(set(self.scopes))) or any(
            scope not in _SUPPORTED_PUBLIC_SCOPES for scope in self.scopes
        ):
            raise ValueError("Trusted public invocation scopes are invalid.")
        lifetime = self.expires_at - self.issued_at
        if lifetime <= 0 or lifetime > COMPANION_RPC_TIMEOUT_MS:
            raise ValueError("Trusted public invocation lifetime is invalid.")
        return self

    def handle_binding(self) -> tuple[str, str, str]:
        """Return the exact identity tuple that may use public local handles."""

        return (
            self.device_id,
            self.session_id,
            self.oauth_grant_fingerprint,
        )


class CompanionRpcRequestV1(StrictFrozenModel):
    """One bounded MCP HTTP request delivered over the paired WebSocket."""

    message_type: Literal["mcp_request"] = "mcp_request"
    body: str
    body_sha256: str = Field(pattern=SHA256_PATTERN)
    expires_at: int = Field(ge=0)
    headers: dict[str, str]
    issued_at: int = Field(ge=0)
    invocation: TrustedPublicInvocationContextV1
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    sequence: int = Field(ge=1)

    @model_validator(mode="after")
    def require_bounded_rpc(self) -> CompanionRpcRequestV1:
        if len(self.body.encode("utf-8")) > MAX_MCP_BODY_BYTES:
            raise ValueError("Companion MCP request body is too large.")
        if hashlib.sha256(self.body.encode("utf-8")).hexdigest() != (self.body_sha256):
            raise ValueError("Companion MCP request body digest is invalid.")
        lifetime = self.expires_at - self.issued_at
        if lifetime <= 0 or lifetime > COMPANION_RPC_TIMEOUT_MS:
            raise ValueError("Companion MCP request lifetime is invalid.")
        _require_bounded_headers(
            self.headers,
            allowed=_MCP_REQUEST_HEADER_ALLOWLIST,
        )
        if (
            self.invocation.body_sha256 != self.body_sha256
            or self.invocation.request_id != self.request_id
            or self.invocation.issued_at != self.issued_at
            or self.invocation.expires_at != self.expires_at
            or self.invocation.sequence != self.sequence
        ):
            raise ValueError("Companion MCP invocation binding is invalid.")
        return self


class CompanionRpcResponseBodyV1(StrictFrozenModel):
    """One decoded local MCP response before bounded transport encoding."""

    message_type: Literal["mcp_response"] = "mcp_response"
    body: str
    headers: dict[str, str]
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    status: int = Field(ge=100, le=599)

    @model_validator(mode="after")
    def require_bounded_response(self) -> CompanionRpcResponseBodyV1:
        if len(self.body.encode("utf-8")) > MAX_MCP_RESPONSE_DECODED_BYTES:
            raise ValueError("Companion MCP response body is too large.")
        _require_bounded_headers(
            self.headers,
            allowed=_MCP_RESPONSE_HEADER_ALLOWLIST,
        )
        return self


class CompanionRpcResponseEnvelopeV1(StrictFrozenModel):
    """One deterministic compressed MCP response inside the signed envelope."""

    schema_version: Literal["foldweave-mcp-response-envelope.v1"] = (
        MCP_RESPONSE_ENVELOPE_SCHEMA
    )
    message_type: Literal["mcp_response"] = "mcp_response"
    body: str = Field(
        min_length=1,
        max_length=MAX_MCP_RESPONSE_ENCODED_CHARACTERS,
        pattern=r"^[A-Za-z0-9_-]+$",
    )
    body_encoding: Literal["gzip+base64url"] = MCP_RESPONSE_BODY_ENCODING
    body_sha256: str = Field(pattern=SHA256_PATTERN)
    compressed_size: int = Field(ge=1, le=MAX_MCP_RESPONSE_COMPRESSED_BYTES)
    decoded_size: int = Field(ge=0, le=MAX_MCP_RESPONSE_DECODED_BYTES)
    headers: dict[str, str]
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    status: int = Field(ge=100, le=599)

    @model_validator(mode="after")
    def require_exact_encoded_response(self) -> CompanionRpcResponseEnvelopeV1:
        compressed = _b64url_decode(self.body)
        if len(compressed) != self.compressed_size:
            raise ValueError("Companion MCP compressed response size is invalid.")
        if len(compressed) > MAX_MCP_RESPONSE_COMPRESSED_BYTES:
            raise ValueError("Companion MCP compressed response is too large.")
        decoded = _bounded_gzip_decompress(compressed)
        if len(decoded) != self.decoded_size:
            raise ValueError("Companion MCP decoded response size is invalid.")
        if hashlib.sha256(decoded).hexdigest() != self.body_sha256:
            raise ValueError("Companion MCP decoded response digest is invalid.")
        decoded.decode("utf-8", errors="strict")
        _require_bounded_headers(
            self.headers,
            allowed=_MCP_RESPONSE_HEADER_ALLOWLIST,
        )
        return self

    @classmethod
    def from_response(
        cls,
        response: CompanionRpcResponseBodyV1,
    ) -> CompanionRpcResponseEnvelopeV1:
        """Encode a local response into the sole deterministic wire profile."""

        decoded = response.body.encode("utf-8")
        compressed = bytearray(gzip.compress(decoded, compresslevel=9, mtime=0))
        if len(compressed) >= 10:
            compressed[9] = 255
        return cls(
            body=_b64url_encode(bytes(compressed)),
            body_sha256=hashlib.sha256(decoded).hexdigest(),
            compressed_size=len(compressed),
            decoded_size=len(decoded),
            headers=response.headers,
            request_id=response.request_id,
            status=response.status,
        )

    def decoded_body(self) -> str:
        """Return the exact verified UTF-8 MCP response body."""

        return _bounded_gzip_decompress(_b64url_decode(self.body)).decode(
            "utf-8",
            errors="strict",
        )

    def wire_payload(self) -> dict[str, JsonValue]:
        return {
            "body": self.body,
            "bodyDigest": self.body_sha256,
            "bodyEncoding": self.body_encoding,
            "compressedSize": self.compressed_size,
            "decodedSize": self.decoded_size,
            "headers": self.headers,
            "requestId": self.request_id,
            "schemaVersion": self.schema_version,
            "status": self.status,
            "type": self.message_type,
        }


@dataclass(slots=True)
class DeviceIdentityStore:
    """Generate and retain one Ed25519 installation key in macOS Keychain."""

    adapter: SecurityKeychainAdapter = field(default_factory=PyObjCKeychainAdapter)
    service: str = DEVICE_KEYCHAIN_SERVICE
    account: str = DEVICE_KEYCHAIN_ACCOUNT

    def load_or_create(self) -> CompanionDeviceIdentityV1:
        if self.adapter.exists(service=self.service, account=self.account):
            stored = self._read_stored()
            private_key = _private_key_from_text(stored.private_key)
        else:
            private_key = Ed25519PrivateKey.generate()
            stored = _StoredDeviceIdentityV1(
                device_id=DEVICE_ID_PREFIX + secrets.token_hex(16),
                private_key=_private_key_text(private_key),
            )
            self.adapter.write(
                service=self.service,
                account=self.account,
                value=canonical_json_bytes(stored),
            )
        return CompanionDeviceIdentityV1(
            device_id=stored.device_id,
            public_key=_public_key_text(private_key.public_key()),
        )

    def sign_envelope(
        self,
        *,
        request_id: str,
        sequence: int,
        body: dict[str, JsonValue],
        issued_at: int | None = None,
        lifetime_ms: int = MAX_SIGNED_REQUEST_LIFETIME_MS,
        nonce: str | None = None,
    ) -> CompanionSignedEnvelopeV1:
        if lifetime_ms <= 0 or lifetime_ms > MAX_SIGNED_REQUEST_LIFETIME_MS:
            raise CompanionContractError(
                "companion_envelope_lifetime_invalid",
                "Signed companion envelope lifetime exceeds the fixed limit.",
            )
        stored = self._read_stored()
        now = int(time.time() * 1_000) if issued_at is None else issued_at
        body_sha256 = hashlib.sha256(canonical_json_bytes(body)).hexdigest()
        unsigned_wire: dict[str, JsonValue] = {
            "body": body,
            "bodyDigest": body_sha256,
            "expiresAt": now + lifetime_ms,
            "issuedAt": now,
            "nonce": nonce or secrets.token_urlsafe(24),
            "requestId": request_id,
            "schemaVersion": "foldweave-device-envelope.v1",
            "sequence": sequence,
        }
        signature = _b64url_encode(
            _private_key_from_text(stored.private_key).sign(
                _SIGNATURE_DOMAIN + canonical_json_bytes(unsigned_wire)
            )
        )
        return CompanionSignedEnvelopeV1(
            request_id=request_id,
            issued_at=now,
            expires_at=now + lifetime_ms,
            sequence=sequence,
            nonce=str(unsigned_wire["nonce"]),
            body=body,
            body_sha256=body_sha256,
            signature=signature,
        )

    def derive_public_job_capability_id(
        self,
        *,
        job_id: str,
        device_id: str,
        oauth_grant_fingerprint: str,
        scopes: tuple[str, ...],
        expires_at_ms: int,
    ) -> str:
        """Derive one restart-stable, job-specific opaque public capability."""

        if len(job_id) != 32 or any(
            character not in "0123456789abcdef" for character in job_id
        ):
            raise CompanionContractError(
                "public_job_capability_input_invalid",
                "The public job capability job identity is invalid.",
            )
        if len(oauth_grant_fingerprint) != 64 or any(
            character not in "0123456789abcdef" for character in oauth_grant_fingerprint
        ):
            raise CompanionContractError(
                "public_job_capability_input_invalid",
                "The public job capability grant identity is invalid.",
            )
        if scopes != tuple(sorted(set(scopes))) or any(
            scope not in _SUPPORTED_PUBLIC_SCOPES for scope in scopes
        ):
            raise CompanionContractError(
                "public_job_capability_input_invalid",
                "The public job capability scopes are invalid.",
            )
        if expires_at_ms <= 0:
            raise CompanionContractError(
                "public_job_capability_input_invalid",
                "The public job capability expiry is invalid.",
            )
        stored = self._read_stored()
        if stored.device_id != device_id:
            raise CompanionContractError(
                "public_job_capability_device_mismatch",
                "The public job capability belongs to another installation.",
            )
        payload: dict[str, JsonValue] = {
            "deviceId": device_id,
            "expiresAt": expires_at_ms,
            "jobId": job_id,
            "oauthGrantFingerprint": oauth_grant_fingerprint,
            "schemaVersion": "foldweave-public-job-capability-derivation.v1",
            "scopes": list(scopes),
        }
        signature = _private_key_from_text(stored.private_key).sign(
            _PUBLIC_JOB_CAPABILITY_DOMAIN + canonical_json_bytes(payload)
        )
        return PUBLIC_JOB_CAPABILITY_PREFIX + _b64url_encode(signature)

    def remove(self) -> bool:
        return self.adapter.remove(service=self.service, account=self.account)

    def _read_stored(self) -> _StoredDeviceIdentityV1:
        try:
            raw = self.adapter.read(service=self.service, account=self.account)
            payload = json.loads(raw.decode("utf-8", errors="strict"))
            return _StoredDeviceIdentityV1.model_validate(payload, strict=True)
        except CredentialStoreError:
            raise
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise CompanionContractError(
                "device_identity_invalid",
                "The stored Foldweave device identity is invalid.",
            ) from exc


def parse_companion_challenge(value: object) -> CompanionChallengeV1:
    """Strictly parse one gateway challenge without accepting extra fields."""

    record = _require_record(value, "companion_challenge")
    _require_exact_keys(
        record,
        {"challenge", "expiresAt", "sessionId", "type"},
        "companion_challenge",
    )
    return CompanionChallengeV1(
        challenge=record["challenge"],
        expires_at=record["expiresAt"],
        session_id=record["sessionId"],
        message_type=record["type"],
    )


def _parse_trusted_public_invocation(
    value: object,
) -> TrustedPublicInvocationContextV1:
    record = _require_record(value, "trusted_public_invocation")
    _require_exact_keys(
        record,
        {
            "bodyDigest",
            "channel",
            "deviceId",
            "expiresAt",
            "issuedAt",
            "jobId",
            "nonce",
            "oauthGrantFingerprint",
            "operationDigest",
            "requestId",
            "revokedAt",
            "schemaVersion",
            "scopes",
            "sequence",
            "sessionId",
        },
        "trusted_public_invocation",
    )
    scopes = record["scopes"]
    if not isinstance(scopes, list):
        raise CompanionContractError(
            "trusted_public_invocation_invalid",
            "The trusted public invocation scopes are invalid.",
        )
    return TrustedPublicInvocationContextV1(
        body_sha256=record["bodyDigest"],
        channel=record["channel"],
        device_id=record["deviceId"],
        expires_at=record["expiresAt"],
        issued_at=record["issuedAt"],
        job_id=record["jobId"],
        nonce=record["nonce"],
        oauth_grant_fingerprint=record["oauthGrantFingerprint"],
        operation_sha256=record["operationDigest"],
        request_id=record["requestId"],
        revoked_at=record["revokedAt"],
        schema_version=record["schemaVersion"],
        scopes=tuple(scopes),
        sequence=record["sequence"],
        session_id=record["sessionId"],
    )


def parse_companion_rpc_request(value: object) -> CompanionRpcRequestV1:
    """Strictly parse one path-neutral request relayed by the gateway."""

    record = _require_record(value, "companion_rpc_request")
    _require_exact_keys(
        record,
        {
            "body",
            "bodyDigest",
            "expiresAt",
            "headers",
            "issuedAt",
            "invocation",
            "requestId",
            "sequence",
            "type",
        },
        "companion_rpc_request",
    )
    return CompanionRpcRequestV1(
        body=record["body"],
        body_sha256=record["bodyDigest"],
        expires_at=record["expiresAt"],
        headers=record["headers"],
        issued_at=record["issuedAt"],
        invocation=_parse_trusted_public_invocation(record["invocation"]),
        request_id=record["requestId"],
        sequence=record["sequence"],
        message_type=record["type"],
    )


@dataclass(slots=True)
class CompanionReplayGuard:
    """Reject expired, replayed, or non-monotonic device envelopes."""

    _last_sequence_by_device: dict[str, int] = field(default_factory=dict)
    _nonces: set[tuple[str, str]] = field(default_factory=set)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def verify_and_record(
        self,
        envelope: CompanionSignedEnvelopeV1,
        *,
        device_id: str,
        public_key: str,
        now: int | None = None,
    ) -> None:
        if not device_id.startswith(DEVICE_ID_PREFIX) or len(device_id) != 36:
            raise CompanionContractError(
                "device_identity_invalid",
                "The Foldweave device identity is invalid.",
            )
        current = int(time.time() * 1_000) if now is None else now
        if envelope.issued_at > current + MAX_CLOCK_SKEW_MS:
            raise CompanionContractError(
                "companion_envelope_not_yet_valid",
                "The signed companion envelope was issued in the future.",
            )
        if current >= envelope.expires_at:
            raise CompanionContractError(
                "companion_envelope_expired",
                "The signed companion envelope has expired.",
            )
        _verify_envelope_signature(envelope, public_key)
        nonce_key = (device_id, envelope.nonce)
        with self._lock:
            if nonce_key in self._nonces:
                raise CompanionContractError(
                    "companion_envelope_replayed",
                    "The signed companion envelope nonce was already used.",
                )
            previous = self._last_sequence_by_device.get(device_id, 0)
            if envelope.sequence <= previous:
                raise CompanionContractError(
                    "companion_sequence_replayed",
                    "The signed companion envelope sequence is not monotonic.",
                )
            if len(self._nonces) >= MAX_TRACKED_NONCES:
                raise CompanionContractError(
                    "companion_replay_window_full",
                    "The replay window is full and requires a fresh connection.",
                )
            self._nonces.add(nonce_key)
            self._last_sequence_by_device[device_id] = envelope.sequence

    def reset_device(self, device_id: str) -> None:
        with self._lock:
            self._last_sequence_by_device.pop(device_id, None)
            self._nonces = {
                nonce_key for nonce_key in self._nonces if nonce_key[0] != device_id
            }


@dataclass(slots=True)
class GatewayRelayGuard:
    """Reject stale or replayed gateway relay frames on one paired session."""

    _last_sequence: int = 0
    _nonces: set[str] = field(default_factory=set)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def verify_and_record(
        self,
        request: CompanionRpcRequestV1,
        *,
        expected_device_id: str,
        expected_session_id: str,
        now: int | None = None,
    ) -> None:
        current = int(time.time() * 1_000) if now is None else now
        invocation = request.invocation
        if (
            invocation.device_id != expected_device_id
            or invocation.session_id != expected_session_id
        ):
            raise CompanionContractError(
                "gateway_invocation_device_mismatch",
                "The gateway invocation targets another paired installation.",
            )
        if invocation.revoked_at is not None:
            raise CompanionContractError(
                "gateway_invocation_revoked",
                "The gateway invocation grant was revoked.",
            )
        if invocation.issued_at > current + MAX_CLOCK_SKEW_MS:
            raise CompanionContractError(
                "gateway_invocation_not_yet_valid",
                "The gateway invocation was issued in the future.",
            )
        if current >= invocation.expires_at:
            raise CompanionContractError(
                "gateway_invocation_expired",
                "The gateway invocation has expired.",
            )
        descriptor, operation_sha256, required_scope = describe_mcp_operation(
            body=request.body,
            body_sha256=request.body_sha256,
            headers=request.headers,
        )
        if (
            invocation.operation_sha256 != operation_sha256
            or invocation.job_id != descriptor["jobId"]
        ):
            raise CompanionContractError(
                "gateway_invocation_operation_mismatch",
                "The gateway invocation does not authorize this MCP operation.",
            )
        if required_scope not in invocation.scopes:
            raise CompanionContractError(
                "gateway_invocation_scope_missing",
                "The OAuth grant does not authorize this Foldweave operation.",
            )
        with self._lock:
            if (
                request.sequence <= self._last_sequence
                or invocation.nonce in self._nonces
            ):
                raise CompanionContractError(
                    "gateway_sequence_replayed",
                    "The gateway relay sequence is not monotonic or the invocation "
                    "nonce was replayed.",
                )
            if len(self._nonces) >= MAX_TRACKED_NONCES:
                raise CompanionContractError(
                    "gateway_replay_window_full",
                    "The gateway replay window requires a fresh connection.",
                )
            self._nonces.add(invocation.nonce)
            self._last_sequence = request.sequence

    def reset_connection(self) -> None:
        """Drop connection-local replay state after a verified new challenge."""

        with self._lock:
            self._last_sequence = 0
            self._nonces.clear()


_CURRENT_TRUSTED_PUBLIC_INVOCATION: ContextVar[
    TrustedPublicInvocationContextV1 | None
] = ContextVar("foldweave_trusted_public_invocation", default=None)


@contextmanager
def trusted_public_invocation(
    context: TrustedPublicInvocationContextV1,
) -> Iterator[None]:
    """Make one already verified public authority visible during local dispatch."""

    token = _CURRENT_TRUSTED_PUBLIC_INVOCATION.set(context)
    try:
        yield
    finally:
        _CURRENT_TRUSTED_PUBLIC_INVOCATION.reset(token)


def current_trusted_public_invocation() -> TrustedPublicInvocationContextV1 | None:
    """Return the current verified public authority, if dispatch is public."""

    return _CURRENT_TRUSTED_PUBLIC_INVOCATION.get()


def describe_mcp_operation(
    *,
    body: str,
    body_sha256: str,
    headers: dict[str, str],
) -> tuple[dict[str, JsonValue], str, str]:
    """Build the cross-runtime canonical public MCP operation descriptor."""

    http_method = headers.get("x-foldweave-http-method", "POST")
    rpc_method: str | None = None
    tool_name: str | None = None
    job_id: str | None = None
    if body:
        try:
            value = json.loads(body)
        except json.JSONDecodeError as exc:
            raise CompanionContractError(
                "mcp_operation_invalid",
                "The MCP request body is not valid JSON.",
            ) from exc
        if not isinstance(value, dict) or any(
            not isinstance(key, str) for key in value
        ):
            raise CompanionContractError(
                "mcp_operation_invalid",
                "The MCP request body must be one JSON-RPC object.",
            )
        method = value.get("method")
        if isinstance(method, str) and len(method) <= 128:
            rpc_method = method
        if rpc_method == "tools/call":
            params = value.get("params")
            if not isinstance(params, dict) or not isinstance(params.get("name"), str):
                raise CompanionContractError(
                    "mcp_operation_invalid",
                    "The MCP tool call is invalid.",
                )
            tool_name = params["name"]
            if tool_name not in _PUBLIC_TOOL_SCOPES:
                raise CompanionContractError(
                    "mcp_tool_not_authorized",
                    "The MCP tool is not authorized for public relay.",
                )
            arguments = params.get("arguments")
            if not isinstance(arguments, dict) or any(
                not isinstance(key, str) for key in arguments
            ):
                raise CompanionContractError(
                    "mcp_operation_invalid",
                    "The MCP tool arguments are invalid.",
                )
            job_binding_keys = {"job_id"}
            forbidden_capability_keys = {
                "capability_id",
                "capability_expires_at",
            }
            if forbidden_capability_keys.intersection(arguments):
                raise CompanionContractError(
                    "mcp_public_job_capability_forbidden",
                    "Public MCP input cannot contain a raw job capability.",
                )
            if tool_name in _PUBLIC_JOBLESS_TOOLS:
                if job_binding_keys.intersection(arguments):
                    raise CompanionContractError(
                        "mcp_public_job_binding_unexpected",
                        "This public MCP tool cannot receive a job identity.",
                    )
            elif tool_name in _PUBLIC_JOB_BOUND_TOOLS:
                candidate_job_id = arguments.get("job_id")
                if (
                    not isinstance(candidate_job_id, str)
                    or len(candidate_job_id) != 32
                    or any(
                        character not in "0123456789abcdef"
                        for character in candidate_job_id
                    )
                ):
                    raise CompanionContractError(
                        "mcp_public_job_binding_required",
                        "This public MCP tool requires one exact job identity.",
                    )
                job_id = candidate_job_id
    descriptor: dict[str, JsonValue] = {
        "bodyDigest": body_sha256,
        "httpMethod": http_method,
        "jobId": job_id,
        "mcpSessionId": headers.get("mcp-session-id"),
        "rpcMethod": rpc_method,
        "schemaVersion": "foldweave-mcp-operation.v1",
        "toolName": tool_name,
    }
    operation_sha256 = hashlib.sha256(canonical_json_bytes(descriptor)).hexdigest()
    required_scope = (
        "foldweave.review" if tool_name is None else _PUBLIC_TOOL_SCOPES[tool_name]
    )
    return descriptor, operation_sha256, required_scope


def _require_record(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise CompanionContractError(
            f"{label}_invalid",
            f"The {label.replace('_', ' ')} is invalid.",
        )
    return value


def _require_exact_keys(
    record: dict[str, object],
    expected: set[str],
    label: str,
) -> None:
    if set(record) != expected:
        raise CompanionContractError(
            f"{label}_invalid",
            f"The {label.replace('_', ' ')} has unsupported or missing fields.",
        )


def _require_bounded_headers(
    headers: dict[str, str],
    *,
    allowed: frozenset[str],
) -> None:
    for name, value in headers.items():
        if (
            name not in allowed
            or name != name.casefold()
            or not isinstance(value, str)
            or len(value) > 512
            or "\r" in value
            or "\n" in value
        ):
            raise ValueError("Companion MCP headers are invalid.")


def _verify_envelope_signature(
    envelope: CompanionSignedEnvelopeV1,
    public_key: str,
) -> None:
    try:
        Ed25519PublicKey.from_public_bytes(_b64url_decode(public_key)).verify(
            _b64url_decode(envelope.signature),
            _SIGNATURE_DOMAIN + canonical_json_bytes(envelope.unsigned_wire_payload()),
        )
    except (InvalidSignature, ValueError) as exc:
        raise CompanionContractError(
            "companion_signature_invalid",
            "The signed companion envelope signature is invalid.",
        ) from exc


def _private_key_text(private_key: Ed25519PrivateKey) -> str:
    return _b64url_encode(
        private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )


def _private_key_from_text(value: str) -> Ed25519PrivateKey:
    try:
        return Ed25519PrivateKey.from_private_bytes(_b64url_decode(value))
    except ValueError as exc:
        raise CompanionContractError(
            "device_identity_invalid",
            "The stored Foldweave device identity is invalid.",
        ) from exc


def _public_key_text(public_key: Ed25519PublicKey) -> str:
    return _b64url_encode(
        public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
    )


def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("ascii")


def _b64url_decode(value: str) -> bytes:
    try:
        raw = value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("Value is not base64url ASCII.") from exc
    padding = b"=" * ((4 - len(raw) % 4) % 4)
    decoded = base64.b64decode(raw + padding, altchars=b"-_", validate=True)
    if _b64url_encode(decoded) != value:
        raise ValueError("Value is not canonical base64url.")
    return decoded


def _bounded_gzip_decompress(compressed: bytes) -> bytes:
    if not compressed or len(compressed) > MAX_MCP_RESPONSE_COMPRESSED_BYTES:
        raise ValueError("Companion MCP compressed response size is invalid.")
    try:
        decompressor = zlib.decompressobj(wbits=16 + zlib.MAX_WBITS)
        decoded = decompressor.decompress(
            compressed,
            MAX_MCP_RESPONSE_DECODED_BYTES + 1,
        )
        if (
            len(decoded) > MAX_MCP_RESPONSE_DECODED_BYTES
            or decompressor.unconsumed_tail
        ):
            raise ValueError("Companion MCP decoded response is too large.")
        decoded += decompressor.flush(MAX_MCP_RESPONSE_DECODED_BYTES - len(decoded) + 1)
    except zlib.error as exc:
        raise ValueError("Companion MCP compressed response is invalid.") from exc
    if len(decoded) > MAX_MCP_RESPONSE_DECODED_BYTES:
        raise ValueError("Companion MCP decoded response is too large.")
    if not decompressor.eof or decompressor.unused_data:
        raise ValueError("Companion MCP compressed response is invalid.")
    return decoded
