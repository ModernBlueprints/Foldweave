"""Companion CLI dispatch, redaction, and lifecycle tests."""

from __future__ import annotations

import asyncio
import hashlib
import io
import json
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from name_atlas import foldweave_companion_cli, foldweave_launcher
from name_atlas.foldweave_companion import (
    CompanionRpcRequestV1,
    DeviceIdentityStore,
    TrustedPublicInvocationContextV1,
    current_trusted_public_invocation,
    trusted_public_invocation,
)
from name_atlas.foldweave_companion_client import (
    CompanionGatewayProfileV1,
    CompanionPairingRegistrationV1,
    CompanionPairingStateStore,
    CompanionPairingStateV1,
    CompanionTransportError,
    InProcessMcpProxy,
)
from name_atlas.foldweave_host_service import FoldweaveHostPlanningService


def _pairing_state() -> CompanionPairingStateV1:
    return CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id="fwd_" + "a" * 32,
        session_id="s" * 43,
        pairing_code_expires_at=2_000_000,
        next_device_sequence=4,
        last_gateway_sequence=2,
    )


@dataclass(slots=True)
class _FakePairing:
    state: CompanionPairingStateV1
    revoked: bool = False
    fail_revoke: bool = False

    async def register(
        self,
        gateway: CompanionGatewayProfileV1,
        *,
        device_name: str,
    ) -> CompanionPairingRegistrationV1:
        assert gateway == self.state.gateway
        assert device_name == "Nikolai Mac"
        return CompanionPairingRegistrationV1(
            session=self.state,
            pairing_code="23456789AB",
        )

    async def approve_locally(self) -> CompanionPairingStateV1:
        return self.state

    async def revoke(self) -> None:
        if self.fail_revoke:
            raise CompanionTransportError(
                "gateway_request_rejected",
                "The gateway rejected the request.",
            )
        self.revoked = True


def test_register_and_approve_outputs_are_path_free_and_do_not_claim_oauth(
    tmp_path: Path,
) -> None:
    state = _pairing_state()
    pairing = _FakePairing(state)
    store = CompanionPairingStateStore(path=tmp_path / "state.json")
    output = io.StringIO()

    assert (
        foldweave_companion_cli.run_foldweave_companion(
            [
                "register",
                "--gateway",
                state.gateway.base_url,
                "--device-name",
                "Nikolai Mac",
            ],
            state_store=store,
            pairing=pairing,
            stdout=output,
        )
        == 0
    )
    registration = json.loads(output.getvalue())
    assert registration == {
        "device_id": state.device_id,
        "expires_at": state.pairing_code_expires_at,
        "gateway": state.gateway.base_url,
        "pairing_code": "23456789AB",
        "schema_version": "foldweave-companion-registration.v1",
        "session_id": state.session_id,
    }
    assert "/Users/" not in output.getvalue()
    assert "secret" not in output.getvalue().casefold()

    output = io.StringIO()
    assert (
        foldweave_companion_cli.run_foldweave_companion(
            ["approve"],
            state_store=store,
            pairing=pairing,
            stdout=output,
        )
        == 0
    )
    approval = json.loads(output.getvalue())
    assert approval == {
        "local_approval_confirmed": True,
        "schema_version": "foldweave-companion-approval.v1",
        "session_id": state.session_id,
    }
    assert "oauth" not in output.getvalue().casefold()
    assert "authorized" not in output.getvalue().casefold()


def test_status_is_local_renderer_safe_and_never_claims_oauth(
    tmp_path: Path,
) -> None:
    state = _pairing_state()
    store = CompanionPairingStateStore(path=tmp_path / "private" / "state.json")
    asyncio.run(store.write(state))
    output = io.StringIO()

    assert (
        foldweave_companion_cli.run_foldweave_companion(
            ["status"],
            state_store=store,
            pairing=_FakePairing(state),
            stdout=output,
        )
        == 0
    )
    status = json.loads(output.getvalue())
    assert status == {
        "configured": True,
        "device_id": state.device_id,
        "gateway": state.gateway.base_url,
        "last_gateway_sequence": 2,
        "next_device_sequence": 4,
        "pairing_code_expires_at": 2_000_000,
        "schema_version": "foldweave-companion-status.v1",
        "session_id": state.session_id,
    }
    assert str(tmp_path) not in output.getvalue()
    assert "oauth" not in output.getvalue().casefold()
    assert "authorized" not in output.getvalue().casefold()


def test_revoke_reports_success_only_after_confirmed_gateway_response(
    tmp_path: Path,
) -> None:
    state = _pairing_state()
    store = CompanionPairingStateStore(path=tmp_path / "state.json")
    failing = _FakePairing(state, fail_revoke=True)
    output = io.StringIO()
    errors = io.StringIO()

    assert (
        foldweave_companion_cli.run_foldweave_companion(
            ["revoke"],
            state_store=store,
            pairing=failing,
            stdout=output,
            stderr=errors,
        )
        == 2
    )
    assert output.getvalue() == ""
    assert not failing.revoked
    assert json.loads(errors.getvalue())["error"] == "gateway_request_rejected"

    confirmed = _FakePairing(state)
    output = io.StringIO()
    assert (
        foldweave_companion_cli.run_foldweave_companion(
            ["revoke"],
            state_store=store,
            pairing=confirmed,
            stdout=output,
        )
        == 0
    )
    assert confirmed.revoked
    assert json.loads(output.getvalue())["revoked"] is True


@dataclass(slots=True)
class _FakeServer:
    url: str = "http://127.0.0.1:49152"
    started: bool = False
    stopped: bool = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


@dataclass(slots=True)
class _WaitingSession:
    started: asyncio.Event = field(default_factory=asyncio.Event)
    cancelled: bool = False
    endpoint: str | None = None

    async def run_forever(self, stop: asyncio.Event) -> None:
        assert not stop.is_set()
        self.started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.cancelled = True
            raise


@pytest.mark.anyio
async def test_runtime_cancellation_stops_ephemeral_loopback_server(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "state.json")
    await store.write(_pairing_state())
    server = _FakeServer()
    session = _WaitingSession()

    def session_factory(endpoint: str) -> _WaitingSession:
        session.endpoint = endpoint
        return session

    task = asyncio.create_task(
        foldweave_companion_cli.run_companion_runtime(
            store,
            local_server_factory=lambda: server,
            session_factory=session_factory,
        )
    )
    await session.started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert server.started
    assert server.stopped
    assert session.cancelled
    assert session.endpoint == "http://127.0.0.1:49152/mcp"


@pytest.mark.anyio
async def test_embedded_runtime_uses_in_process_mcp_lifespan_and_cleans_up(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "state.json")
    await store.write(_pairing_state())
    lifecycle: list[str] = []
    started = asyncio.Event()
    observed: dict[str, object] = {}

    class _Router:
        @asynccontextmanager
        async def lifespan_context(self, _app: object):
            lifecycle.append("started")
            try:
                yield
            finally:
                lifecycle.append("stopped")

    class _App:
        router = _Router()

    class _Server:
        def streamable_http_app(self) -> _App:
            return _App()

    class _Session:
        def __init__(self, **kwargs: object) -> None:
            observed.update(kwargs)

        async def run_forever(
            self,
            stop: asyncio.Event,
            *,
            retry_wake: asyncio.Event | None = None,
        ) -> None:
            observed["stop"] = stop
            observed["retry_wake"] = retry_wake
            started.set()
            await asyncio.Event().wait()

    service = cast(FoldweaveHostPlanningService, object())
    identity = cast(DeviceIdentityStore, object())
    monkeypatch.setattr(
        foldweave_companion_cli,
        "build_foldweave_chatgpt_server",
        lambda selected: _Server() if selected is service else None,
    )
    monkeypatch.setattr(
        foldweave_companion_cli,
        "FoldweaveCompanionSession",
        _Session,
    )
    runtime = foldweave_companion_cli.EmbeddedCompanionRuntime(
        service=service,
        identity_store=identity,
    )

    task = asyncio.create_task(runtime(store))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert lifecycle == ["started", "stopped"]
    assert observed["state_store"] is store
    assert observed["identity_store"] is identity
    assert isinstance(observed["mcp_proxy"], InProcessMcpProxy)
    assert observed["stop"].is_set()
    assert observed["retry_wake"] is runtime._retry_wake


@pytest.mark.anyio
async def test_default_runtime_uses_one_identity_and_in_process_composition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "state.json")
    await store.write(_pairing_state())
    identity = cast(DeviceIdentityStore, object())
    service = cast(FoldweaveHostPlanningService, object())
    observed: dict[str, object] = {}

    class _Runtime:
        def __init__(self, **kwargs: object) -> None:
            observed.update(kwargs)

        async def __call__(self, selected_store: CompanionPairingStateStore) -> None:
            observed["state_store"] = selected_store

    monkeypatch.setattr(
        foldweave_companion_cli,
        "DeviceIdentityStore",
        lambda: identity,
    )
    monkeypatch.setattr(
        foldweave_companion_cli,
        "FoldweaveHostPlanningService",
        lambda *, identity_store: service if identity_store is identity else None,
    )
    monkeypatch.setattr(
        foldweave_companion_cli,
        "EmbeddedCompanionRuntime",
        _Runtime,
    )

    await foldweave_companion_cli.run_companion_runtime(store)

    assert observed == {
        "identity_store": identity,
        "service": service,
        "state_store": store,
    }


@pytest.mark.anyio
async def test_in_process_proxy_preserves_verified_invocation_context() -> None:
    app = FastAPI(docs_url=None, openapi_url=None, redoc_url=None)

    @app.post("/mcp")
    async def inspect_context() -> JSONResponse:
        invocation = current_trusted_public_invocation()
        return JSONResponse(
            {
                "device_id": invocation.device_id if invocation else None,
                "trusted": invocation is not None,
            }
        )

    body = "{}"
    body_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    invocation = TrustedPublicInvocationContextV1(
        device_id="fwd_" + "a" * 32,
        session_id="s" * 43,
        oauth_grant_fingerprint="b" * 64,
        scopes=("foldweave.review",),
        request_id="request_" + "r" * 24,
        issued_at=1_000_000,
        expires_at=1_010_000,
        sequence=1,
        nonce="nonce_" + "n" * 24,
        body_sha256=body_sha256,
        operation_sha256="c" * 64,
    )
    request = CompanionRpcRequestV1(
        body=body,
        body_sha256=body_sha256,
        headers={
            "content-type": "application/json",
            "x-foldweave-http-method": "POST",
        },
        request_id=invocation.request_id,
        issued_at=invocation.issued_at,
        expires_at=invocation.expires_at,
        sequence=invocation.sequence,
        invocation=invocation,
    )

    with trusted_public_invocation(invocation):
        response = await InProcessMcpProxy(app).relay(request)

    assert response.status == 200
    assert json.loads(response.body) == {
        "device_id": invocation.device_id,
        "trusted": True,
    }
    assert current_trusted_public_invocation() is None


def test_launcher_dispatches_companion_without_loading_other_commands(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[str] = []

    def fake_run(arguments: list[str]) -> int:
        observed.extend(arguments)
        return 17

    monkeypatch.setattr(
        foldweave_companion_cli,
        "run_foldweave_companion",
        fake_run,
    )
    assert foldweave_launcher.run(["companion", "status"]) == 17
    assert observed == ["status"]
