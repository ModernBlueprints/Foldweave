"""Packaged-app ownership tests for the Foldweave ChatGPT companion."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from name_atlas.folder_app import DeterministicFolderRunService, create_folder_app
from name_atlas.foldweave_companion_client import (
    CompanionGatewayProfileV1,
    CompanionGatewayStatusV1,
    CompanionPairingRegistrationV1,
    CompanionPairingStateStore,
    CompanionPairingStateV1,
    CompanionTransportError,
)
from name_atlas.foldweave_companion_supervisor import (
    FoldweaveCompanionSupervisor,
    PairingConnectionState,
)
from name_atlas.foldweave_pairing_service import (
    FoldweavePairingService,
    PairingPageStatus,
    PairingPageView,
)


def _pairing_state() -> CompanionPairingStateV1:
    return CompanionPairingStateV1(
        gateway=CompanionGatewayProfileV1(base_url="https://foldweave-gateway.example"),
        device_id="fwd_" + "a" * 32,
        session_id="s" * 43,
        pairing_code_expires_at=2_000_000,
        next_device_sequence=2,
    )


async def _wait_until(predicate, *, attempts: int = 100) -> None:
    for _ in range(attempts):
        if predicate():
            return
        await asyncio.sleep(0)
    raise AssertionError("Expected asynchronous supervisor state was not reached.")


@dataclass(slots=True)
class _BlockingRuntime:
    calls: int = 0
    active: int = 0
    peak_active: int = 0
    cancelled: int = 0
    wake_calls: int = 0
    started: asyncio.Event = field(default_factory=asyncio.Event)

    def wake(self) -> None:
        self.wake_calls += 1

    async def __call__(self, _state_store: CompanionPairingStateStore) -> None:
        self.calls += 1
        self.active += 1
        self.peak_active = max(self.peak_active, self.active)
        self.started.set()
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.cancelled += 1
            raise
        finally:
            self.active -= 1


@dataclass(slots=True)
class _LifecycleProbe:
    starts: int = 0
    changes: int = 0
    stops: int = 0
    shutdowns: int = 0

    async def start(self) -> None:
        self.starts += 1

    async def pairing_state_changed(self) -> None:
        self.changes += 1

    async def stop_companion(self) -> None:
        self.stops += 1

    async def shutdown(self) -> None:
        self.shutdowns += 1


@dataclass(slots=True)
class _PairingProbe:
    store: CompanionPairingStateStore
    approved: bool = False

    async def register(
        self,
        gateway: CompanionGatewayProfileV1,
        *,
        device_name: str,
    ) -> CompanionPairingRegistrationV1:
        assert device_name == "Foldweave Mac"
        state = _pairing_state().model_copy(update={"gateway": gateway})
        await self.store.write(state)
        return CompanionPairingRegistrationV1(
            session=state,
            pairing_code="23456789AB",
        )

    async def approve_locally(self) -> CompanionPairingStateV1:
        self.approved = True
        return await self.store.read()

    async def status(self) -> CompanionGatewayStatusV1:
        try:
            state = await self.store.read()
        except CompanionTransportError:
            raise
        return CompanionGatewayStatusV1(
            schema_version="foldweave-pairing-status.v1",
            request_id="r" * 24,
            device_id=state.device_id,
            session_id=state.session_id,
            pairing_state="local_approved" if self.approved else "pending",
            authorized=False,
            connected=False,
            revoked=False,
            expires_at=state.pairing_code_expires_at,
            last_seen_at=None,
        )

    async def revoke(self) -> None:
        await self.store.remove()


@dataclass(slots=True)
class _ApplicationPairingLifecycle:
    starts: int = 0
    stops: int = 0

    async def start_background_runtime(self) -> None:
        self.starts += 1

    async def stop_background_runtime(self) -> None:
        self.stops += 1

    async def view(self) -> PairingPageView:
        return PairingPageView(
            status=PairingPageStatus.NOT_CONFIGURED,
            status_label="Not paired",
            detail="No pairing exists.",
            configured=False,
            can_register=True,
        )

    async def register(self, **_: object) -> PairingPageView:
        return await self.view()

    async def approve_locally(self) -> PairingPageView:
        return await self.view()

    async def revoke(self) -> PairingPageView:
        return await self.view()


@pytest.mark.anyio
async def test_unpaired_app_start_is_nonblocking_and_starts_no_runtime(
    tmp_path: Path,
) -> None:
    runtime = _BlockingRuntime()
    supervisor = FoldweaveCompanionSupervisor(
        state_store=CompanionPairingStateStore(path=tmp_path / "pairing.json"),
        runtime=runtime,
    )

    await supervisor.start()

    assert runtime.calls == 0
    assert supervisor.connection_state() is PairingConnectionState.DISCONNECTED
    await supervisor.shutdown()


@pytest.mark.anyio
async def test_registration_or_approval_wakeup_starts_one_companion(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    runtime = _BlockingRuntime()
    supervisor = FoldweaveCompanionSupervisor(state_store=store, runtime=runtime)
    await supervisor.start()
    await store.write(_pairing_state())

    await supervisor.pairing_state_changed()
    await runtime.started.wait()

    assert runtime.calls == 1
    assert runtime.peak_active == 1
    assert supervisor.connection_state() is PairingConnectionState.RECONNECTING
    await supervisor.shutdown()
    assert runtime.cancelled == 1


@pytest.mark.anyio
async def test_pairing_service_wakes_on_register_and_approve_then_stops_on_revoke(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    lifecycle = _LifecycleProbe()
    service = FoldweavePairingService(
        state_store=store,
        pairing=_PairingProbe(store),
        runtime_lifecycle=lifecycle,
        now_ms=lambda: 1_000_000,
    )

    await service.start_background_runtime()
    await service.register(
        gateway_url="https://foldweave-gateway.example",
        device_name="Foldweave Mac",
    )
    await service.approve_locally()
    await service.revoke()
    await service.stop_background_runtime()

    assert lifecycle.starts == 1
    assert lifecycle.changes == 2
    assert lifecycle.stops == 1
    assert lifecycle.shutdowns == 1


def test_fastapi_lifespan_owns_companion_start_and_clean_shutdown() -> None:
    lifecycle = _ApplicationPairingLifecycle()
    app = create_folder_app(
        DeterministicFolderRunService(),
        pairing_service=lifecycle,
    )

    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
        assert lifecycle.starts == 1

    assert lifecycle.stops == 1


@pytest.mark.anyio
async def test_restart_with_existing_pairing_restarts_companion(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    await store.write(_pairing_state())
    first_runtime = _BlockingRuntime()
    first = FoldweaveCompanionSupervisor(state_store=store, runtime=first_runtime)
    await first.start()
    await first_runtime.started.wait()
    await first.shutdown()

    restarted_runtime = _BlockingRuntime()
    restarted = FoldweaveCompanionSupervisor(
        state_store=CompanionPairingStateStore(path=store.path),
        runtime=restarted_runtime,
    )
    await restarted.start()
    await restarted_runtime.started.wait()

    assert first_runtime.calls == 1
    assert first_runtime.cancelled == 1
    assert restarted_runtime.calls == 1
    await restarted.shutdown()


@pytest.mark.anyio
async def test_runtime_failure_retries_with_bounded_exponential_backoff(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    await store.write(_pairing_state())
    calls = 0
    blocked = asyncio.Event()
    observed_delays: list[float] = []

    async def runtime(_state_store: CompanionPairingStateStore) -> None:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("transient companion startup failure")
        blocked.set()
        await asyncio.Event().wait()

    async def retry_waiter(_wake: asyncio.Event, delay: float) -> bool:
        observed_delays.append(delay)
        return False

    supervisor = FoldweaveCompanionSupervisor(
        state_store=store,
        runtime=runtime,
        initial_retry_seconds=1.0,
        maximum_retry_seconds=2.0,
        retry_waiter=retry_waiter,
    )
    await supervisor.start()
    await blocked.wait()

    assert calls == 3
    assert observed_delays == [1.0, 2.0]
    assert max(observed_delays) <= supervisor.maximum_retry_seconds
    await supervisor.shutdown()


@pytest.mark.anyio
async def test_duplicate_lifecycle_events_never_start_a_second_runtime(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    await store.write(_pairing_state())
    runtime = _BlockingRuntime()
    supervisor = FoldweaveCompanionSupervisor(state_store=store, runtime=runtime)

    await asyncio.gather(*(supervisor.start() for _ in range(5)))
    await runtime.started.wait()
    await asyncio.gather(*(supervisor.pairing_state_changed() for _ in range(5)))
    await asyncio.sleep(0)

    assert runtime.calls == 1
    assert runtime.peak_active == 1
    assert runtime.wake_calls == 5
    await supervisor.shutdown()


@pytest.mark.anyio
async def test_revoke_stops_active_companion_and_allows_later_repairing(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    await store.write(_pairing_state())
    runtime = _BlockingRuntime()
    supervisor = FoldweaveCompanionSupervisor(state_store=store, runtime=runtime)
    await supervisor.start()
    await runtime.started.wait()

    assert await store.remove() is True
    await supervisor.pairing_state_changed()

    assert runtime.active == 0
    assert runtime.cancelled == 1
    assert supervisor.connection_state() is PairingConnectionState.DISCONNECTED

    runtime.started.clear()
    await store.write(_pairing_state())
    await supervisor.pairing_state_changed()
    await runtime.started.wait()
    assert runtime.calls == 2
    await supervisor.shutdown()


@pytest.mark.anyio
async def test_clean_shutdown_awaits_runtime_and_leaves_no_orphan_task(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "pairing.json")
    await store.write(_pairing_state())
    runtime = _BlockingRuntime()
    supervisor = FoldweaveCompanionSupervisor(state_store=store, runtime=runtime)
    await supervisor.start()
    await runtime.started.wait()

    await supervisor.shutdown()
    await _wait_until(lambda: runtime.active == 0)

    assert runtime.cancelled == 1
    assert runtime.active == 0
    assert supervisor.connection_state() is PairingConnectionState.DISCONNECTED
