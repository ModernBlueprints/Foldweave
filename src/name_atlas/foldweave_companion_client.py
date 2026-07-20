"""Outbound Foldweave gateway companion and loopback MCP relay."""

from __future__ import annotations

import asyncio
import json
import os
import secrets
import time
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Protocol
from urllib.parse import urlencode, urlsplit, urlunsplit

import httpx
from pydantic import Field, model_validator
from starlette.types import ASGIApp
from websockets.asyncio.client import connect

from name_atlas.folder_refactor.contracts import StrictFrozenModel
from name_atlas.folder_refactor.serialization import canonical_json_bytes
from name_atlas.foldweave_companion import (
    COMPANION_RPC_TIMEOUT_MS,
    MAX_MCP_BODY_BYTES,
    MAX_MCP_RESPONSE_DECODED_BYTES,
    MAX_MCP_RESPONSE_WIRE_BYTES,
    CompanionChallengeV1,
    CompanionContractError,
    CompanionRpcRequestV1,
    CompanionRpcResponseBodyV1,
    CompanionRpcResponseEnvelopeV1,
    DeviceIdentityStore,
    GatewayRelayGuard,
    parse_companion_challenge,
    parse_companion_rpc_request,
    trusted_public_invocation,
)

PAIRING_STATE_SCHEMA = "foldweave-companion-pairing.v1"
MAX_GATEWAY_CONTROL_RESPONSE_BYTES = 16 * 1_024
DEFAULT_PAIRING_STATE_PATH = (
    Path.home()
    / "Library"
    / "Application Support"
    / "Foldweave"
    / "companion-pairing.json"
)
_RESPONSE_HEADERS = frozenset({"content-type", "mcp-session-id", "retry-after"})


class CompanionTransportError(RuntimeError):
    """One stable companion transport failure without payload or credential data."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


class CompanionGatewayProfileV1(StrictFrozenModel):
    """One canonical public gateway destination."""

    schema_version: Literal["foldweave-gateway-profile.v1"] = (
        "foldweave-gateway-profile.v1"
    )
    base_url: str = Field(min_length=1, max_length=2_048)

    @model_validator(mode="after")
    def require_canonical_https(self) -> CompanionGatewayProfileV1:
        parsed = urlsplit(self.base_url)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.port is not None
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Foldweave gateway requires one canonical HTTPS origin.")
        canonical = f"https://{parsed.hostname.casefold()}"
        if self.base_url != canonical:
            raise ValueError("Foldweave gateway URL is not canonical.")
        return self

    def http_url(self, path: str, *, query: dict[str, str] | None = None) -> str:
        if not path.startswith("/") or "?" in path or "#" in path:
            raise ValueError("Gateway path is invalid.")
        suffix = path
        if query:
            suffix += "?" + urlencode(query)
        return self.base_url + suffix

    def websocket_url(self, session_id: str) -> str:
        parsed = urlsplit(self.http_url("/companion", query={"session": session_id}))
        return urlunsplit(("wss", parsed.netloc, parsed.path, parsed.query, ""))


class CompanionPairingStateV1(StrictFrozenModel):
    """Non-secret local pairing and transport sequence checkpoint."""

    schema_version: Literal["foldweave-companion-pairing.v1"] = PAIRING_STATE_SCHEMA
    gateway: CompanionGatewayProfileV1
    device_id: str = Field(pattern=r"^fwd_[a-f0-9]{32}$")
    session_id: str = Field(pattern=r"^[A-Za-z0-9_-]{32,128}$")
    pairing_code_expires_at: int = Field(ge=0)
    next_device_sequence: int = Field(ge=2)
    last_gateway_sequence: int = Field(default=0, ge=0)


class CompanionPairingRegistrationV1(StrictFrozenModel):
    """One path-free local presentation of a newly registered pairing."""

    session: CompanionPairingStateV1
    pairing_code: str = Field(pattern=r"^[0-9A-HJKMNP-TV-Z]{10}$")


class CompanionGatewayStatusV1(StrictFrozenModel):
    """Authoritative, path-free pairing state returned by the public gateway."""

    schema_version: Literal["foldweave-pairing-status.v1"]
    request_id: str = Field(pattern=r"^[A-Za-z0-9_-]{16,128}$")
    device_id: str = Field(pattern=r"^fwd_[a-f0-9]{32}$")
    session_id: str = Field(pattern=r"^[A-Za-z0-9_-]{32,128}$")
    pairing_state: Literal[
        "pending",
        "local_approved",
        "authorized",
        "revoked",
        "expired",
    ]
    authorized: bool
    connected: bool
    revoked: bool
    expires_at: int = Field(gt=0)
    last_seen_at: int | None = Field(default=None, gt=0)

    @model_validator(mode="after")
    def require_consistent_authority(self) -> CompanionGatewayStatusV1:
        if self.pairing_state == "pending" and (self.authorized or self.revoked):
            raise ValueError("Pending pairing status is inconsistent.")
        if self.pairing_state == "local_approved" and (self.authorized or self.revoked):
            raise ValueError("Locally approved pairing status is inconsistent.")
        if self.pairing_state == "authorized" and (not self.authorized or self.revoked):
            raise ValueError("Authorized pairing status is inconsistent.")
        if self.pairing_state == "revoked" and not self.revoked:
            raise ValueError("Revoked pairing status is inconsistent.")
        if self.revoked and self.pairing_state != "revoked":
            raise ValueError("Pairing revocation status is inconsistent.")
        if self.connected and self.pairing_state in {"revoked", "expired"}:
            raise ValueError("Connected pairing status is inconsistent.")
        return self


@dataclass(slots=True)
class CompanionPairingStateStore:
    """Atomically persist non-secret session identity and outbound sequence."""

    path: Path = DEFAULT_PAIRING_STATE_PATH
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock, repr=False)

    async def write(self, state: CompanionPairingStateV1) -> None:
        async with self._lock:
            await asyncio.to_thread(self._write_sync, state)

    async def read(self) -> CompanionPairingStateV1:
        async with self._lock:
            return await asyncio.to_thread(self._read_sync)

    async def allocate_sequence(self) -> tuple[CompanionPairingStateV1, int]:
        """Persist sequence consumption before a signed request can leave."""

        async with self._lock:
            state = await asyncio.to_thread(self._read_sync)
            sequence = state.next_device_sequence
            advanced = state.model_copy(update={"next_device_sequence": sequence + 1})
            await asyncio.to_thread(self._write_sync, advanced)
            return advanced, sequence

    async def record_gateway_sequence(self, sequence: int) -> None:
        """Persist an inbound relay sequence before dispatching local work."""

        async with self._lock:
            state = await asyncio.to_thread(self._read_sync)
            if sequence <= state.last_gateway_sequence:
                raise CompanionTransportError(
                    "gateway_request_replayed",
                    "The gateway relay sequence was already used.",
                )
            advanced = state.model_copy(update={"last_gateway_sequence": sequence})
            await asyncio.to_thread(self._write_sync, advanced)

    async def remove(self) -> bool:
        async with self._lock:
            return await asyncio.to_thread(self._remove_sync)

    def _read_sync(self) -> CompanionPairingStateV1:
        try:
            raw = self.path.read_bytes()
            payload = json.loads(raw.decode("utf-8", errors="strict"))
            return CompanionPairingStateV1.model_validate(payload, strict=True)
        except FileNotFoundError as exc:
            raise CompanionTransportError(
                "pairing_not_configured",
                "No Foldweave gateway pairing is configured.",
            ) from exc
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise CompanionTransportError(
                "pairing_state_invalid",
                "The local Foldweave pairing state is invalid.",
            ) from exc

    def _write_sync(self, state: CompanionPairingStateV1) -> None:
        parent = self.path.parent
        parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if parent.is_symlink() or not parent.is_dir():
            raise CompanionTransportError(
                "pairing_state_parent_invalid",
                "The Foldweave pairing state directory is invalid.",
            )
        temporary = parent / f".{self.path.name}.{secrets.token_hex(8)}.tmp"
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
        try:
            with os.fdopen(descriptor, "wb", closefd=True) as stream:
                stream.write(canonical_json_bytes(state))
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        finally:
            with suppress(FileNotFoundError):
                temporary.unlink()
        os.chmod(self.path, 0o600)

    def _remove_sync(self) -> bool:
        try:
            self.path.unlink()
            return True
        except FileNotFoundError:
            return False


@dataclass(slots=True)
class CompanionPairingClient:
    """Register, locally approve, and revoke one device-bound pairing."""

    identity_store: DeviceIdentityStore
    state_store: CompanionPairingStateStore
    timeout_seconds: float = 15.0

    async def register(
        self,
        gateway: CompanionGatewayProfileV1,
        *,
        device_name: str,
    ) -> CompanionPairingRegistrationV1:
        identity = self.identity_store.load_or_create()
        request_id = secrets.token_urlsafe(24)
        envelope = self.identity_store.sign_envelope(
            request_id=request_id,
            sequence=1,
            body=identity.registration_body(device_name=device_name),
            lifetime_ms=10 * 60 * 1_000,
        )
        payload = await self._post_json(
            gateway.http_url("/pairing/register"),
            envelope.wire_payload(),
            expected_status=201,
        )
        _require_exact_response_keys(
            payload,
            {"expiresAt", "pairingCode", "sessionId"},
        )
        session = CompanionPairingStateV1(
            gateway=gateway,
            device_id=identity.device_id,
            session_id=payload["sessionId"],
            pairing_code_expires_at=payload["expiresAt"],
            next_device_sequence=2,
        )
        registration = CompanionPairingRegistrationV1(
            session=session,
            pairing_code=payload["pairingCode"],
        )
        await self.state_store.write(session)
        return registration

    async def approve_locally(self) -> CompanionPairingStateV1:
        advanced, sequence = await self.state_store.allocate_sequence()
        envelope = self.identity_store.sign_envelope(
            request_id=secrets.token_urlsafe(24),
            sequence=sequence,
            body={
                "intent": "approve_pairing",
                "sessionId": advanced.session_id,
            },
        )
        payload = await self._post_json(
            advanced.gateway.http_url(
                "/pairing/approve",
                query={"session": advanced.session_id},
            ),
            envelope.wire_payload(),
            expected_status=200,
        )
        _require_exact_response_keys(
            payload,
            {"approved", "approvedAt", "codeHash", "sessionId"},
        )
        if not (
            payload["approved"] is True
            and isinstance(payload["approvedAt"], int)
            and payload["approvedAt"] > 0
            and _is_sha256(payload["codeHash"])
            and payload["sessionId"] == advanced.session_id
        ):
            raise CompanionTransportError(
                "pairing_approval_failed",
                "The Foldweave pairing was not approved.",
            )
        return advanced

    async def revoke(self) -> None:
        advanced, sequence = await self.state_store.allocate_sequence()
        envelope = self.identity_store.sign_envelope(
            request_id=secrets.token_urlsafe(24),
            sequence=sequence,
            body={
                "intent": "revoke_pairing",
                "sessionId": advanced.session_id,
            },
        )
        payload = await self._post_json(
            advanced.gateway.http_url(
                "/pairing/revoke",
                query={"session": advanced.session_id},
            ),
            envelope.wire_payload(),
            expected_status=200,
        )
        _require_exact_response_keys(
            payload,
            {"codeHash", "deviceId", "revoked", "revokedAt", "sessionId"},
        )
        if not (
            payload["revoked"] is True
            and isinstance(payload["revokedAt"], int)
            and payload["revokedAt"] > 0
            and _is_sha256(payload["codeHash"])
            and payload["deviceId"] == advanced.device_id
            and payload["sessionId"] == advanced.session_id
        ):
            raise CompanionTransportError(
                "pairing_revocation_failed",
                "The Foldweave pairing was not revoked.",
            )
        await self.state_store.remove()

    async def status(self) -> CompanionGatewayStatusV1:
        """Read signed-request, device-bound status from gateway authority."""

        advanced, sequence = await self.state_store.allocate_sequence()
        request_id = secrets.token_urlsafe(24)
        envelope = self.identity_store.sign_envelope(
            request_id=request_id,
            sequence=sequence,
            body={
                "deviceId": advanced.device_id,
                "intent": "pairing_status",
                "sessionId": advanced.session_id,
            },
        )
        payload = await self._post_json(
            advanced.gateway.http_url(
                "/pairing/status",
                query={"session": advanced.session_id},
            ),
            envelope.wire_payload(),
            expected_status=200,
        )
        _require_exact_response_keys(
            payload,
            {
                "authorized",
                "connected",
                "deviceId",
                "expiresAt",
                "lastSeenAt",
                "pairingState",
                "requestId",
                "revoked",
                "schemaVersion",
                "sessionId",
            },
        )
        try:
            status = CompanionGatewayStatusV1.model_validate(
                {
                    "authorized": payload["authorized"],
                    "connected": payload["connected"],
                    "device_id": payload["deviceId"],
                    "expires_at": payload["expiresAt"],
                    "last_seen_at": payload["lastSeenAt"],
                    "pairing_state": payload["pairingState"],
                    "request_id": payload["requestId"],
                    "revoked": payload["revoked"],
                    "schema_version": payload["schemaVersion"],
                    "session_id": payload["sessionId"],
                },
                strict=True,
            )
        except ValueError as exc:
            raise CompanionTransportError(
                "gateway_response_invalid",
                "The Foldweave gateway returned an invalid pairing status.",
            ) from exc
        if (
            status.request_id != request_id
            or status.device_id != advanced.device_id
            or status.session_id != advanced.session_id
        ):
            raise CompanionTransportError(
                "pairing_status_binding_invalid",
                "The Foldweave gateway returned status for another pairing.",
            )
        return status

    async def _post_json(
        self,
        url: str,
        payload: dict[str, object],
        *,
        expected_status: int,
    ) -> dict[str, object]:
        async with httpx.AsyncClient(
            follow_redirects=False,
            timeout=self.timeout_seconds,
            trust_env=False,
        ) as client:
            try:
                response = await client.post(url, json=payload)
            except httpx.HTTPError as exc:
                raise CompanionTransportError(
                    "gateway_unavailable",
                    "The Foldweave gateway is unavailable.",
                ) from exc
        if response.status_code != expected_status:
            raise CompanionTransportError(
                "gateway_request_rejected",
                f"The Foldweave gateway rejected the request ({response.status_code}).",
            )
        if len(response.content) > MAX_GATEWAY_CONTROL_RESPONSE_BYTES:
            raise CompanionTransportError(
                "gateway_response_too_large",
                "The Foldweave gateway response is too large.",
            )
        content_type = (
            response.headers.get("content-type", "")
            .partition(";")[0]
            .strip()
            .casefold()
        )
        if content_type != "application/json":
            raise CompanionTransportError(
                "gateway_response_invalid",
                "The Foldweave gateway returned an invalid response.",
            )
        try:
            result = response.json()
        except ValueError as exc:
            raise CompanionTransportError(
                "gateway_response_invalid",
                "The Foldweave gateway returned an invalid response.",
            ) from exc
        if not isinstance(result, dict) or any(
            not isinstance(key, str) for key in result
        ):
            raise CompanionTransportError(
                "gateway_response_invalid",
                "The Foldweave gateway returned an invalid response.",
            )
        return result


class CompanionMcpProxy(Protocol):
    """One narrow MCP HTTP relay into the existing local control plane."""

    async def relay(
        self,
        request: CompanionRpcRequestV1,
    ) -> CompanionRpcResponseBodyV1: ...


@dataclass(slots=True)
class LoopbackMcpProxy:
    """Forward bounded gateway MCP requests only to the loopback MCP endpoint."""

    endpoint: str
    timeout_seconds: float = COMPANION_RPC_TIMEOUT_MS / 1_000

    def __post_init__(self) -> None:
        parsed = urlsplit(self.endpoint)
        if (
            parsed.scheme != "http"
            or parsed.hostname not in {"127.0.0.1", "::1", "localhost"}
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path != "/mcp"
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("Companion MCP endpoint must be exact loopback HTTP.")

    async def relay(
        self,
        request: CompanionRpcRequestV1,
    ) -> CompanionRpcResponseBodyV1:
        try:
            async with httpx.AsyncClient(
                follow_redirects=False,
                timeout=self.timeout_seconds,
                trust_env=False,
            ) as client:
                return await _relay_mcp_request(client, self.endpoint, request)
        except httpx.HTTPError as exc:
            raise CompanionTransportError(
                "local_mcp_unavailable",
                "The local Foldweave MCP service is unavailable.",
            ) from exc


@dataclass(slots=True)
class InProcessMcpProxy:
    """Relay gateway MCP requests into the packaged app without another listener."""

    app: ASGIApp
    endpoint_path: str = "/mcp"
    timeout_seconds: float = COMPANION_RPC_TIMEOUT_MS / 1_000

    def __post_init__(self) -> None:
        if self.endpoint_path != "/mcp":
            raise ValueError("Embedded companion MCP path must be exact.")

    async def relay(
        self,
        request: CompanionRpcRequestV1,
    ) -> CompanionRpcResponseBodyV1:
        transport = httpx.ASGITransport(app=self.app, raise_app_exceptions=False)
        try:
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://foldweave.internal",
                follow_redirects=False,
                timeout=self.timeout_seconds,
                trust_env=False,
            ) as client:
                return await _relay_mcp_request(client, self.endpoint_path, request)
        except httpx.HTTPError as exc:
            raise CompanionTransportError(
                "local_mcp_unavailable",
                "The embedded Foldweave MCP service is unavailable.",
            ) from exc


async def _relay_mcp_request(
    client: httpx.AsyncClient,
    endpoint: str,
    request: CompanionRpcRequestV1,
) -> CompanionRpcResponseBodyV1:
    headers = dict(request.headers)
    method = headers.pop("x-foldweave-http-method", "POST")
    if method not in {"GET", "POST", "DELETE"}:
        raise CompanionTransportError(
            "mcp_method_invalid",
            "The relayed MCP HTTP method is invalid.",
        )
    response = await client.request(
        method,
        endpoint,
        content=request.body.encode("utf-8"),
        headers=headers,
    )
    if len(response.content) > MAX_MCP_RESPONSE_DECODED_BYTES:
        raise CompanionTransportError(
            "local_mcp_response_too_large",
            "The local Foldweave MCP response is too large.",
        )
    try:
        body = response.content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise CompanionTransportError(
            "local_mcp_response_invalid",
            "The local Foldweave MCP response is not UTF-8.",
        ) from exc
    response_headers = {
        name.casefold(): value
        for name, value in response.headers.items()
        if name.casefold() in _RESPONSE_HEADERS
    }
    return CompanionRpcResponseBodyV1(
        body=body,
        headers=response_headers,
        request_id=request.request_id,
        status=response.status_code,
    )


class CompanionSocket(Protocol):
    async def recv(self) -> str | bytes: ...

    async def send(self, message: str | bytes) -> None: ...


class _NoRedirectWebSocketConnect(connect):
    """Disable websocket redirects while retaining the stable client API."""

    def process_redirect(self, exc: Exception) -> Exception:
        return exc


@dataclass(slots=True)
class FoldweaveCompanionSession:
    """Run one authenticated outbound relay against the single local MCP."""

    identity_store: DeviceIdentityStore
    state_store: CompanionPairingStateStore
    mcp_proxy: CompanionMcpProxy
    _relay_guard: GatewayRelayGuard = field(
        default_factory=GatewayRelayGuard,
        repr=False,
    )

    async def run_connection(self, socket: CompanionSocket) -> None:
        state = await self.state_store.read()
        challenge = _decode_challenge(await socket.recv())
        if challenge.session_id != state.session_id:
            raise CompanionTransportError(
                "companion_session_mismatch",
                "The gateway challenge targets another pairing session.",
            )
        now = int(time.time() * 1_000)
        if now >= challenge.expires_at:
            raise CompanionTransportError(
                "companion_challenge_expired",
                "The gateway challenge has expired.",
            )
        advanced, sequence = await self.state_store.allocate_sequence()
        challenge_response = self.identity_store.sign_envelope(
            request_id=secrets.token_urlsafe(24),
            sequence=sequence,
            body={
                "challenge": challenge.challenge,
                "sessionId": challenge.session_id,
                "type": "challenge_response",
            },
            lifetime_ms=min(
                challenge.expires_at - now,
                COMPANION_RPC_TIMEOUT_MS,
            ),
        )
        await socket.send(canonical_json_bytes(challenge_response.wire_payload()))
        ready = _decode_record(await socket.recv(), "companion_ready")
        if set(ready) != {"sessionId", "type"} or not (
            ready.get("type") == "companion_ready"
            and ready.get("sessionId") == advanced.session_id
        ):
            raise CompanionTransportError(
                "companion_ready_invalid",
                "The gateway did not confirm the paired companion.",
            )
        self._relay_guard.reset_connection()
        while True:
            message = await socket.recv()
            request = parse_companion_rpc_request(
                _decode_record(message, "companion_rpc_request")
            )
            self._relay_guard.verify_and_record(
                request,
                expected_device_id=state.device_id,
                expected_session_id=state.session_id,
            )
            await self.state_store.record_gateway_sequence(request.sequence)
            with trusted_public_invocation(request.invocation):
                response = await self._relay_or_error(request)
            transport_response = CompanionRpcResponseEnvelopeV1.from_response(response)
            _advanced, response_sequence = await self.state_store.allocate_sequence()
            envelope = self.identity_store.sign_envelope(
                request_id=request.request_id,
                sequence=response_sequence,
                body=transport_response.wire_payload(),
                lifetime_ms=COMPANION_RPC_TIMEOUT_MS,
            )
            wire_bytes = canonical_json_bytes(envelope.wire_payload())
            if len(wire_bytes) > MAX_MCP_RESPONSE_WIRE_BYTES:
                raise CompanionTransportError(
                    "companion_response_envelope_too_large",
                    "The encoded Foldweave companion response is too large.",
                )
            await socket.send(wire_bytes)

    async def _relay_or_error(
        self,
        request: CompanionRpcRequestV1,
    ) -> CompanionRpcResponseBodyV1:
        try:
            return await self.mcp_proxy.relay(request)
        except CompanionTransportError:
            body = canonical_json_bytes(
                {
                    "error": {
                        "code": -32603,
                        "message": "The local Foldweave MCP service is unavailable.",
                    },
                    "id": None,
                    "jsonrpc": "2.0",
                }
            ).decode("utf-8")
            return CompanionRpcResponseBodyV1(
                body=body,
                headers={"content-type": "application/json"},
                request_id=request.request_id,
                status=502,
            )

    async def run_forever(
        self,
        stop: asyncio.Event,
        *,
        retry_wake: asyncio.Event | None = None,
        initial_delay_seconds: float = 0.5,
        maximum_delay_seconds: float = 30.0,
    ) -> None:
        delay = initial_delay_seconds
        while not stop.is_set():
            state = await self.state_store.read()
            try:
                async with _NoRedirectWebSocketConnect(
                    state.gateway.websocket_url(state.session_id),
                    compression=None,
                    proxy=None,
                    open_timeout=10,
                    ping_interval=20,
                    ping_timeout=20,
                    close_timeout=5,
                    max_size=MAX_MCP_BODY_BYTES + 16 * 1_024,
                ) as socket:
                    delay = initial_delay_seconds
                    await self.run_connection(socket)
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001 - bounded reconnect boundary
                jitter = secrets.randbelow(251) / 1_000
                woke = await _wait_for_reconnect(
                    stop,
                    retry_wake,
                    timeout_seconds=delay + jitter,
                )
                delay = (
                    initial_delay_seconds
                    if woke
                    else min(maximum_delay_seconds, delay * 2)
                )


async def _wait_for_reconnect(
    stop: asyncio.Event,
    retry_wake: asyncio.Event | None,
    *,
    timeout_seconds: float,
) -> bool:
    """Return true only when an explicit pairing event wakes reconnect."""

    if retry_wake is None:
        with suppress(TimeoutError):
            await asyncio.wait_for(stop.wait(), timeout=timeout_seconds)
        return False
    if retry_wake.is_set():
        retry_wake.clear()
        return True
    stop_wait = asyncio.create_task(stop.wait())
    retry_wait = asyncio.create_task(retry_wake.wait())
    try:
        done, pending = await asyncio.wait(
            {stop_wait, retry_wait},
            timeout=timeout_seconds,
            return_when=asyncio.FIRST_COMPLETED,
        )
    finally:
        for task in (stop_wait, retry_wait):
            if not task.done():
                task.cancel()
        await asyncio.gather(stop_wait, retry_wait, return_exceptions=True)
    woke = retry_wait in done and retry_wait.result()
    if woke:
        retry_wake.clear()
    return bool(woke)


def _decode_record(value: str | bytes, label: str) -> dict[str, object]:
    if isinstance(value, bytes):
        try:
            text = value.decode("utf-8", errors="strict")
        except UnicodeDecodeError as exc:
            raise CompanionTransportError(
                f"{label}_invalid",
                "The gateway message is not UTF-8.",
            ) from exc
    else:
        text = value
    if len(text.encode("utf-8")) > MAX_MCP_BODY_BYTES + 16 * 1_024:
        raise CompanionTransportError(
            f"{label}_too_large",
            "The gateway message is too large.",
        )
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CompanionTransportError(
            f"{label}_invalid",
            "The gateway message is invalid JSON.",
        ) from exc
    if not isinstance(payload, dict) or any(
        not isinstance(key, str) for key in payload
    ):
        raise CompanionTransportError(
            f"{label}_invalid",
            "The gateway message is not a JSON object.",
        )
    return payload


def _decode_challenge(value: str | bytes) -> CompanionChallengeV1:
    try:
        return parse_companion_challenge(_decode_record(value, "companion_challenge"))
    except (CompanionContractError, ValueError) as exc:
        raise CompanionTransportError(
            "companion_challenge_invalid",
            "The gateway challenge is invalid.",
        ) from exc


def _require_exact_response_keys(
    payload: dict[str, object],
    expected: set[str],
) -> None:
    if set(payload) != expected:
        raise CompanionTransportError(
            "gateway_response_invalid",
            "The Foldweave gateway returned an invalid response.",
        )


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
