"""Outbound gateway companion, state, and loopback relay tests."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI, Response

from name_atlas.foldweave_companion import (
    MAX_MCP_RESPONSE_WIRE_BYTES,
    CompanionContractError,
    CompanionRpcRequestV1,
    CompanionRpcResponseBodyV1,
    CompanionRpcResponseEnvelopeV1,
    DeviceIdentityStore,
    current_trusted_public_invocation,
    describe_mcp_operation,
    parse_companion_rpc_request,
)
from name_atlas.foldweave_companion_client import (
    CompanionGatewayProfileV1,
    CompanionGatewayStatusV1,
    CompanionPairingClient,
    CompanionPairingStateStore,
    CompanionPairingStateV1,
    CompanionTransportError,
    FoldweaveCompanionSession,
    InProcessMcpProxy,
    LoopbackMcpProxy,
    _NoRedirectWebSocketConnect,
    _wait_for_reconnect,
)


class _MemoryKeychain:
    def __init__(self) -> None:
        self.items: dict[tuple[str, str], bytes] = {}

    def exists(self, *, service: str, account: str) -> bool:
        return (service, account) in self.items

    def read(self, *, service: str, account: str) -> bytes:
        return self.items[(service, account)]

    def write(self, *, service: str, account: str, value: bytes) -> None:
        self.items[(service, account)] = value

    def remove(self, *, service: str, account: str) -> bool:
        return self.items.pop((service, account), None) is not None


class _ScriptedSocket:
    def __init__(self, inbound: list[str]) -> None:
        self.inbound = inbound
        self.sent: list[bytes | str] = []

    async def recv(self) -> str:
        if not self.inbound:
            raise RuntimeError("test_complete")
        return self.inbound.pop(0)

    async def send(self, message: str | bytes) -> None:
        self.sent.append(message)


class _EchoProxy:
    def __init__(self) -> None:
        self.requests: list[CompanionRpcRequestV1] = []
        self.invocations_seen = []

    async def relay(self, request: CompanionRpcRequestV1):
        from name_atlas.foldweave_companion import CompanionRpcResponseBodyV1

        self.requests.append(request)
        self.invocations_seen.append(current_trusted_public_invocation())
        return CompanionRpcResponseBodyV1(
            body='{"jsonrpc":"2.0","id":1,"result":{}}',
            headers={"content-type": "application/json"},
            request_id=request.request_id,
            status=200,
        )


def _public_rpc_wire(
    *,
    body: str,
    issued_at: int,
    expires_at: int,
    request_id: str,
    sequence: int,
    device_id: str,
    session_id: str,
    headers: dict[str, str] | None = None,
    scopes: list[str] | None = None,
) -> dict[str, object]:
    request_headers = headers or {
        "content-type": "application/json",
        "x-foldweave-http-method": "POST",
    }
    body_sha256 = hashlib.sha256(body.encode()).hexdigest()
    descriptor, operation_sha256, _required_scope = describe_mcp_operation(
        body=body,
        body_sha256=body_sha256,
        headers=request_headers,
    )
    return {
        "body": body,
        "bodyDigest": body_sha256,
        "expiresAt": expires_at,
        "headers": request_headers,
        "issuedAt": issued_at,
        "invocation": {
            "bodyDigest": body_sha256,
            "channel": "chatgpt_hosted",
            "deviceId": device_id,
            "expiresAt": expires_at,
            "issuedAt": issued_at,
            "jobId": descriptor["jobId"],
            "nonce": f"invocation_nonce_{sequence:016d}",
            "oauthGrantFingerprint": "a" * 64,
            "operationDigest": operation_sha256,
            "requestId": request_id,
            "revokedAt": None,
            "schemaVersion": "foldweave-public-invocation.v1",
            "scopes": scopes
            or [
                "foldweave.execute",
                "foldweave.plan",
                "foldweave.review",
            ],
            "sequence": sequence,
            "sessionId": session_id,
        },
        "requestId": request_id,
        "sequence": sequence,
        "type": "mcp_request",
    }


def _public_rpc_request(**kwargs: object) -> CompanionRpcRequestV1:
    return parse_companion_rpc_request(_public_rpc_wire(**kwargs))


@pytest.mark.anyio
async def test_pairing_state_sequence_is_persisted_before_use(tmp_path: Path) -> None:
    path = tmp_path / "state" / "companion.json"
    store = CompanionPairingStateStore(path=path)
    state = CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id="fwd_" + "a" * 32,
        session_id="s" * 43,
        pairing_code_expires_at=1_000_000,
        next_device_sequence=2,
    )
    await store.write(state)

    advanced, sequence = await store.allocate_sequence()
    assert sequence == 2
    assert advanced.next_device_sequence == 3
    assert (await CompanionPairingStateStore(path=path).read()) == advanced
    assert path.stat().st_mode & 0o777 == 0o600


@pytest.mark.anyio
async def test_companion_challenge_relays_without_claiming_oauth_authorization(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    state_store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    state = CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id=identity.device_id,
        session_id="s" * 43,
        pairing_code_expires_at=8_000_000,
        next_device_sequence=3,
    )
    await state_store.write(state)
    monkeypatch.setattr("time.time", lambda: 7_000.0)
    body = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
    request = _public_rpc_wire(
        body=body,
        issued_at=7_000_000,
        expires_at=7_025_000,
        request_id="r" * 64,
        sequence=1,
        device_id=identity.device_id,
        session_id=state.session_id,
    )
    socket = _ScriptedSocket(
        [
            json.dumps(
                {
                    "challenge": "c" * 43,
                    "expiresAt": 7_060_000,
                    "sessionId": state.session_id,
                    "type": "companion_challenge",
                }
            ),
            json.dumps({"sessionId": state.session_id, "type": "companion_ready"}),
            json.dumps(request),
        ]
    )
    proxy = _EchoProxy()
    session = FoldweaveCompanionSession(
        identity_store=identity_store,
        state_store=state_store,
        mcp_proxy=proxy,
    )

    with pytest.raises(RuntimeError, match="test_complete"):
        await session.run_connection(socket)

    assert len(proxy.requests) == 1
    assert proxy.invocations_seen == [proxy.requests[0].invocation]
    assert current_trusted_public_invocation() is None
    assert len(socket.sent) == 2
    challenge_response = json.loads(socket.sent[0])
    response = json.loads(socket.sent[1])
    assert challenge_response["body"]["type"] == "challenge_response"
    assert response["body"]["type"] == "mcp_response"
    assert response["body"]["requestId"] == request["requestId"]
    assert response["body"]["schemaVersion"] == ("foldweave-mcp-response-envelope.v1")
    assert response["body"]["bodyEncoding"] == "gzip+base64url"
    transported = CompanionRpcResponseEnvelopeV1(
        body=response["body"]["body"],
        body_encoding=response["body"]["bodyEncoding"],
        body_sha256=response["body"]["bodyDigest"],
        compressed_size=response["body"]["compressedSize"],
        decoded_size=response["body"]["decodedSize"],
        headers=response["body"]["headers"],
        request_id=response["body"]["requestId"],
        schema_version=response["body"]["schemaVersion"],
        status=response["body"]["status"],
        message_type=response["body"]["type"],
    )
    assert json.loads(transported.decoded_body()) == {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {},
    }
    assert response["requestId"] == request["requestId"]
    persisted = await state_store.read()
    assert persisted.next_device_sequence == 5
    assert persisted.last_gateway_sequence == 1
    assert "authorized_at" not in persisted.model_dump()
    assert "grant_expires_at" not in persisted.model_dump()


@pytest.mark.anyio
async def test_reconnect_rejects_a_gateway_sequence_already_persisted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    state_store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    state = CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id=identity.device_id,
        session_id="s" * 43,
        pairing_code_expires_at=8_000_000,
        next_device_sequence=3,
        last_gateway_sequence=5,
    )
    await state_store.write(state)
    monkeypatch.setattr("time.time", lambda: 7_000.0)
    body = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
    socket = _ScriptedSocket(
        [
            json.dumps(
                {
                    "challenge": "c" * 43,
                    "expiresAt": 7_060_000,
                    "sessionId": state.session_id,
                    "type": "companion_challenge",
                }
            ),
            json.dumps({"sessionId": state.session_id, "type": "companion_ready"}),
            json.dumps(
                _public_rpc_wire(
                    body=body,
                    issued_at=7_000_000,
                    expires_at=7_025_000,
                    request_id="r" * 64,
                    sequence=5,
                    device_id=identity.device_id,
                    session_id=state.session_id,
                )
            ),
        ]
    )
    proxy = _EchoProxy()

    with pytest.raises(CompanionTransportError, match="gateway_request_replayed"):
        await FoldweaveCompanionSession(
            identity_store=identity_store,
            state_store=state_store,
            mcp_proxy=proxy,
        ).run_connection(socket)

    assert proxy.requests == []
    assert (await state_store.read()).last_gateway_sequence == 5
    assert len(socket.sent) == 1


@pytest.mark.anyio
async def test_wrong_scope_stops_before_local_mcp_dispatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    state_store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    state = CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id=identity.device_id,
        session_id="s" * 43,
        pairing_code_expires_at=8_000_000,
        next_device_sequence=3,
    )
    await state_store.write(state)
    monkeypatch.setattr("time.time", lambda: 7_000.0)
    body = json.dumps(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "arguments": {
                    "job_id": "a" * 32,
                },
                "name": "accept_plan_and_create_copy",
            },
        },
        separators=(",", ":"),
    )
    request = _public_rpc_wire(
        body=body,
        issued_at=7_000_000,
        expires_at=7_025_000,
        request_id="scope_rejected_request_12345",
        sequence=1,
        device_id=identity.device_id,
        session_id=state.session_id,
        scopes=["foldweave.review"],
    )
    socket = _ScriptedSocket(
        [
            json.dumps(
                {
                    "challenge": "c" * 43,
                    "expiresAt": 7_060_000,
                    "sessionId": state.session_id,
                    "type": "companion_challenge",
                }
            ),
            json.dumps({"sessionId": state.session_id, "type": "companion_ready"}),
            json.dumps(request),
        ]
    )
    proxy = _EchoProxy()

    with pytest.raises(CompanionContractError) as exc_info:
        await FoldweaveCompanionSession(
            identity_store=identity_store,
            state_store=state_store,
            mcp_proxy=proxy,
        ).run_connection(socket)

    assert exc_info.value.code == "gateway_invocation_scope_missing"
    assert proxy.requests == []
    assert (await state_store.read()).last_gateway_sequence == 0
    assert len(socket.sent) == 1


@pytest.mark.anyio
async def test_loopback_proxy_forwards_only_bounded_headers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    async def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["url"] = str(request.url)
        captured["authorization"] = request.headers.get("authorization")
        return httpx.Response(
            200,
            content=b'{"jsonrpc":"2.0","id":1,"result":{}}',
            headers={
                "content-type": "application/json",
                "mcp-session-id": "session-1",
                "x-internal": "/private/project",
            },
        )

    transport = httpx.MockTransport(handler)
    original_client = httpx.AsyncClient

    def client_factory(*args, **kwargs):
        return original_client(transport=transport, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)
    body = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
    request = _public_rpc_request(
        body=body,
        issued_at=9_000_000,
        expires_at=9_025_000,
        request_id="r" * 64,
        sequence=1,
        device_id="fwd_" + "d" * 32,
        session_id="s" * 43,
        headers={
            "content-type": "application/json",
            "x-foldweave-http-method": "POST",
        },
    )
    response = await LoopbackMcpProxy("http://127.0.0.1:8123/mcp").relay(request)

    assert captured == {
        "authorization": None,
        "method": "POST",
        "url": "http://127.0.0.1:8123/mcp",
    }
    assert response.headers == {
        "content-type": "application/json",
        "mcp-session-id": "session-1",
    }
    assert "/private/project" not in response.model_dump_json()


@pytest.mark.anyio
async def test_embedded_proxy_runs_mcp_without_a_second_loopback_listener() -> None:
    app = FastAPI()

    @app.post("/mcp")
    async def mcp() -> Response:
        return Response(
            content='{"jsonrpc":"2.0","id":1,"result":{"tools":[]}}',
            media_type="application/json",
            headers={"mcp-session-id": "embedded-session"},
        )

    body = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
    request = _public_rpc_request(
        body=body,
        issued_at=9_000_000,
        expires_at=9_025_000,
        request_id="r" * 64,
        sequence=1,
        device_id="fwd_" + "d" * 32,
        session_id="s" * 43,
        headers={
            "content-type": "application/json",
            "x-foldweave-http-method": "POST",
        },
    )

    response = await InProcessMcpProxy(app).relay(request)

    assert response.status == 200
    assert response.headers == {
        "content-type": "application/json",
        "mcp-session-id": "embedded-session",
    }
    assert json.loads(response.body)["result"] == {"tools": []}


def test_actual_built_widget_uses_deterministic_bounded_response_envelope() -> None:
    from name_atlas.folder_refactor.serialization import canonical_json_bytes
    from name_atlas.foldweave_chatgpt_mcp import _load_widget_html

    widget = _load_widget_html(None)
    widget_size = len(widget.encode("utf-8"))
    assert widget_size > MAX_MCP_RESPONSE_WIRE_BYTES
    response = CompanionRpcResponseBodyV1(
        body=widget,
        headers={"content-type": "text/html;profile=mcp-app"},
        request_id="widget_resource_0123456789abcdef",
        status=200,
    )

    first = CompanionRpcResponseEnvelopeV1.from_response(response)
    second = CompanionRpcResponseEnvelopeV1.from_response(response)

    assert first == second
    assert first.body_encoding == "gzip+base64url"
    assert first.decoded_size == widget_size
    assert first.compressed_size < first.decoded_size
    assert first.decoded_body() == widget
    identity_store = DeviceIdentityStore(adapter=_MemoryKeychain())
    identity_store.load_or_create()
    signed = identity_store.sign_envelope(
        request_id=response.request_id,
        sequence=1,
        body=first.wire_payload(),
        issued_at=10_000_000,
        nonce="widget_response_nonce_1234567890",
    )
    assert len(canonical_json_bytes(signed.wire_payload())) <= (
        MAX_MCP_RESPONSE_WIRE_BYTES
    )


def test_gateway_and_loopback_profiles_reject_redirectable_or_nonlocal_urls() -> None:
    with pytest.raises(ValueError, match="canonical HTTPS origin"):
        CompanionGatewayProfileV1(base_url="https://user@example.com")
    with pytest.raises(ValueError, match="loopback HTTP"):
        LoopbackMcpProxy("https://example.com/mcp")


def test_websocket_connector_rejects_redirects() -> None:
    connector = _NoRedirectWebSocketConnect(
        "wss://foldweave-gateway.example/companion?session=" + "s" * 43,
        proxy=None,
    )
    redirect = RuntimeError("redirect")
    assert connector.process_redirect(redirect) is redirect
    assert connector.proxy is None


@pytest.mark.anyio
async def test_pairing_wake_interrupts_companion_reconnect_delay() -> None:
    stop = asyncio.Event()
    wake = asyncio.Event()
    waiting = asyncio.create_task(_wait_for_reconnect(stop, wake, timeout_seconds=60.0))
    await asyncio.sleep(0)

    wake.set()

    assert await waiting is True
    assert wake.is_set() is False


@pytest.mark.anyio
async def test_authoritative_pairing_status_is_exact_bound_and_persists_sequence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    state_store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    state = CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id=identity.device_id,
        session_id="s" * 43,
        pairing_code_expires_at=8_000_000,
        next_device_sequence=4,
    )
    await state_store.write(state)

    async def handler(request: httpx.Request) -> httpx.Response:
        sent = json.loads(request.content)
        assert sent["sequence"] == 4
        assert sent["body"] == {
            "deviceId": identity.device_id,
            "intent": "pairing_status",
            "sessionId": state.session_id,
        }
        return httpx.Response(
            200,
            json={
                "authorized": True,
                "connected": True,
                "deviceId": identity.device_id,
                "expiresAt": 9_000_000,
                "lastSeenAt": 7_500_000,
                "pairingState": "authorized",
                "requestId": sent["requestId"],
                "revoked": False,
                "schemaVersion": "foldweave-pairing-status.v1",
                "sessionId": state.session_id,
            },
            headers={"content-type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    original_client = httpx.AsyncClient

    def client_factory(*args, **kwargs):
        return original_client(transport=transport, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)
    status = await CompanionPairingClient(
        identity_store=identity_store,
        state_store=state_store,
    ).status()

    assert status == CompanionGatewayStatusV1(
        schema_version="foldweave-pairing-status.v1",
        request_id=status.request_id,
        device_id=identity.device_id,
        session_id=state.session_id,
        pairing_state="authorized",
        authorized=True,
        connected=True,
        revoked=False,
        expires_at=9_000_000,
        last_seen_at=7_500_000,
    )
    assert (await state_store.read()).next_device_sequence == 5
    assert "/private/" not in status.model_dump_json()


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("mutation", "expected_error"),
    [
        ({"deviceId": "fwd_" + "f" * 32}, "pairing_status_binding_invalid"),
        ({"sessionId": "x" * 43}, "pairing_status_binding_invalid"),
        ({"requestId": "wrong_request_123456789"}, "pairing_status_binding_invalid"),
        ({"extra": "unsupported"}, "gateway_response_invalid"),
        ({"authorized": False}, "gateway_response_invalid"),
        (
            {"connected": True, "pairingState": "expired"},
            "gateway_response_invalid",
        ),
        (
            {"pairingState": "expired", "revoked": True},
            "gateway_response_invalid",
        ),
    ],
)
async def test_pairing_status_fails_closed_on_wrong_binding_or_schema(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: dict[str, object],
    expected_error: str,
) -> None:
    keychain = _MemoryKeychain()
    identity_store = DeviceIdentityStore(adapter=keychain)
    identity = identity_store.load_or_create()
    state_store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    state = CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id=identity.device_id,
        session_id="s" * 43,
        pairing_code_expires_at=8_000_000,
        next_device_sequence=2,
    )
    await state_store.write(state)

    async def handler(request: httpx.Request) -> httpx.Response:
        sent = json.loads(request.content)
        payload: dict[str, object] = {
            "authorized": True,
            "connected": False,
            "deviceId": identity.device_id,
            "expiresAt": 9_000_000,
            "lastSeenAt": None,
            "pairingState": "authorized",
            "requestId": sent["requestId"],
            "revoked": False,
            "schemaVersion": "foldweave-pairing-status.v1",
            "sessionId": state.session_id,
        }
        payload.update(mutation)
        return httpx.Response(
            200,
            json=payload,
            headers={"content-type": "application/json"},
        )

    transport = httpx.MockTransport(handler)
    original_client = httpx.AsyncClient

    def client_factory(*args, **kwargs):
        return original_client(transport=transport, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)
    with pytest.raises(CompanionTransportError) as exc_info:
        await CompanionPairingClient(
            identity_store=identity_store,
            state_store=state_store,
        ).status()
    assert exc_info.value.code == expected_error
    assert (await state_store.read()).next_device_sequence == 3
