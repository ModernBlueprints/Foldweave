"""Bounded CLI composition root for the paired Foldweave companion."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Protocol, TextIO

from pydantic import ValidationError

from name_atlas.foldweave_chatgpt_mcp import build_foldweave_chatgpt_server
from name_atlas.foldweave_companion import DeviceIdentityStore
from name_atlas.foldweave_companion_client import (
    CompanionGatewayProfileV1,
    CompanionPairingClient,
    CompanionPairingRegistrationV1,
    CompanionPairingStateStore,
    CompanionPairingStateV1,
    CompanionTransportError,
    FoldweaveCompanionSession,
    InProcessMcpProxy,
)
from name_atlas.foldweave_host_service import FoldweaveHostPlanningService


class PairingOperations(Protocol):
    """The network-bearing pairing operations used by command dispatch."""

    async def register(
        self,
        gateway: CompanionGatewayProfileV1,
        *,
        device_name: str,
    ) -> CompanionPairingRegistrationV1: ...

    async def approve_locally(self) -> CompanionPairingStateV1: ...

    async def revoke(self) -> None: ...


class CompanionRuntime(Protocol):
    """Run the outbound companion until cancellation or terminal failure."""

    async def __call__(self, state_store: CompanionPairingStateStore) -> None: ...


class LocalMcpServer(Protocol):
    """Existing loopback lifecycle surface required by the companion."""

    @property
    def url(self) -> str: ...

    def start(self) -> None: ...

    def stop(self) -> None: ...


class CompanionSessionRunner(Protocol):
    """Outbound WSS session surface used by the runtime composition."""

    async def run_forever(self, stop: asyncio.Event) -> None: ...


LocalServerFactory = Callable[[], LocalMcpServer]
SessionFactory = Callable[[str], CompanionSessionRunner]


@dataclass(slots=True)
class EmbeddedCompanionRuntime:
    """Run the shared hosted-planning MCP without a second local listener."""

    service: FoldweaveHostPlanningService
    identity_store: DeviceIdentityStore
    _retry_wake: asyncio.Event = field(
        default_factory=asyncio.Event,
        init=False,
        repr=False,
    )

    def wake(self) -> None:
        """Interrupt the current reconnect wait after a pairing transition."""

        self._retry_wake.set()

    async def __call__(self, state_store: CompanionPairingStateStore) -> None:
        await state_store.read()
        mcp_server = build_foldweave_chatgpt_server(self.service)
        mcp_app = mcp_server.streamable_http_app()
        stop = asyncio.Event()
        session = FoldweaveCompanionSession(
            identity_store=self.identity_store,
            state_store=state_store,
            mcp_proxy=InProcessMcpProxy(mcp_app),
        )
        try:
            async with mcp_app.router.lifespan_context(mcp_app):
                await session.run_forever(stop, retry_wake=self._retry_wake)
        finally:
            stop.set()


def build_foldweave_companion_parser() -> argparse.ArgumentParser:
    """Build the complete provider-free companion command surface."""

    parser = argparse.ArgumentParser(
        prog="foldweave companion",
        description=(
            "Pair this Foldweave installation and run its outbound-only "
            "ChatGPT companion."
        ),
    )
    commands = parser.add_subparsers(dest="companion_command", required=True)

    register = commands.add_parser(
        "register",
        help="Register this installation and print its one-time pairing code.",
    )
    register.add_argument(
        "--gateway",
        required=True,
        help="Canonical public HTTPS Foldweave gateway origin.",
    )
    register.add_argument(
        "--device-name",
        required=True,
        help="Short device label displayed during pairing.",
    )

    commands.add_parser(
        "approve",
        help="Sign the local approval for the pending one-time pairing.",
    )
    commands.add_parser(
        "run",
        help="Run the loopback MCP and outbound WSS companion until stopped.",
    )
    commands.add_parser(
        "status",
        help="Show path-free locally observed pairing configuration.",
    )
    commands.add_parser(
        "revoke",
        help="Revoke the gateway pairing and then remove local pairing state.",
    )
    return parser


def run_foldweave_companion(
    argv: Sequence[str] | None = None,
    *,
    state_store: CompanionPairingStateStore | None = None,
    pairing: PairingOperations | None = None,
    runtime: CompanionRuntime | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Dispatch one companion operation without loading unrelated authorities."""

    output = sys.stdout if stdout is None else stdout
    errors = sys.stderr if stderr is None else stderr
    options = build_foldweave_companion_parser().parse_args(list(argv or ()))
    store = state_store or CompanionPairingStateStore()
    operations = pairing or CompanionPairingClient(
        identity_store=DeviceIdentityStore(),
        state_store=store,
    )

    try:
        if options.companion_command == "register":
            registration = asyncio.run(
                operations.register(
                    CompanionGatewayProfileV1(base_url=options.gateway),
                    device_name=options.device_name,
                )
            )
            _write_json(
                output,
                {
                    "device_id": registration.session.device_id,
                    "expires_at": registration.session.pairing_code_expires_at,
                    "gateway": registration.session.gateway.base_url,
                    "pairing_code": registration.pairing_code,
                    "schema_version": "foldweave-companion-registration.v1",
                    "session_id": registration.session.session_id,
                },
            )
            return 0
        if options.companion_command == "approve":
            approved = asyncio.run(operations.approve_locally())
            _write_json(
                output,
                {
                    "local_approval_confirmed": True,
                    "schema_version": "foldweave-companion-approval.v1",
                    "session_id": approved.session_id,
                },
            )
            return 0
        if options.companion_command == "status":
            _write_json(output, asyncio.run(_local_status(store)))
            return 0
        if options.companion_command == "revoke":
            asyncio.run(operations.revoke())
            _write_json(
                output,
                {
                    "revoked": True,
                    "schema_version": "foldweave-companion-revocation.v1",
                },
            )
            return 0
        if options.companion_command == "run":
            asyncio.run((runtime or run_companion_runtime)(store))
            return 0
    except KeyboardInterrupt:
        return 130
    except (
        CompanionTransportError,
        OSError,
        RuntimeError,
        ValidationError,
        ValueError,
    ) as exc:
        _write_json(
            errors,
            {
                "error": (
                    exc.code
                    if isinstance(exc, CompanionTransportError)
                    else "companion_command_failed"
                ),
                "schema_version": "foldweave-companion-error.v1",
            },
        )
        return 2

    raise AssertionError("Companion parser returned an unsupported command.")


async def _local_status(
    state_store: CompanionPairingStateStore,
) -> dict[str, object]:
    """Return only locally observed, non-secret, path-free configuration."""

    try:
        state = await state_store.read()
    except CompanionTransportError as exc:
        if exc.code != "pairing_not_configured":
            raise
        return {
            "configured": False,
            "schema_version": "foldweave-companion-status.v1",
        }
    return {
        "configured": True,
        "device_id": state.device_id,
        "gateway": state.gateway.base_url,
        "last_gateway_sequence": state.last_gateway_sequence,
        "next_device_sequence": state.next_device_sequence,
        "pairing_code_expires_at": state.pairing_code_expires_at,
        "schema_version": "foldweave-companion-status.v1",
        "session_id": state.session_id,
    }


async def run_companion_runtime(
    state_store: CompanionPairingStateStore,
    *,
    local_server_factory: LocalServerFactory | None = None,
    session_factory: SessionFactory | None = None,
) -> None:
    """Run one existing local MCP engine and one outbound companion cleanly."""

    await state_store.read()
    identity_store = DeviceIdentityStore()
    if local_server_factory is None and session_factory is None:
        await EmbeddedCompanionRuntime(
            service=FoldweaveHostPlanningService(identity_store=identity_store),
            identity_store=identity_store,
        )(state_store)
        return
    if local_server_factory is None or session_factory is None:
        raise ValueError("Companion runtime test factories must be supplied together.")
    server = local_server_factory()
    stop = asyncio.Event()
    try:
        server.start()
        endpoint = f"{server.url}/mcp"
        session = session_factory(endpoint)
        await session.run_forever(stop)
    finally:
        stop.set()
        await asyncio.to_thread(server.stop)


def _write_json(stream: TextIO, payload: dict[str, object]) -> None:
    stream.write(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    )


def main() -> None:
    """Console-compatible companion entry point."""

    raise SystemExit(run_foldweave_companion())


if __name__ == "__main__":
    main()
