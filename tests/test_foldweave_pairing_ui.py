"""Focused native/browser acceptance for truthful ChatGPT pairing UX."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from pathlib import Path

import httpx
import pytest

from name_atlas.folder_app import (
    FolderJourney,
    FolderReviewHandle,
    create_folder_app,
)
from name_atlas.foldweave_companion_client import (
    CompanionGatewayProfileV1,
    CompanionGatewayStatusV1,
    CompanionPairingRegistrationV1,
    CompanionPairingStateStore,
    CompanionPairingStateV1,
    CompanionTransportError,
)
from name_atlas.foldweave_pairing_service import (
    FoldweavePairingService,
    PairingConnectionState,
    PairingPageStatus,
    PairingPageView,
)

NOW_MS = 1_784_500_000_000
EXPIRES_MS = NOW_MS + 600_000
DEVICE_ID = "fwd_" + "1" * 32
SESSION_ID = "s" * 32
PAIRING_CODE = "23456789AB"


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@dataclass(slots=True)
class _FakePairingClient:
    store: CompanionPairingStateStore
    gateway_evidence: CompanionGatewayStatusV1 | Exception
    registrations: int = 0
    approvals: int = 0
    revocations: int = 0

    async def register(
        self,
        gateway: CompanionGatewayProfileV1,
        *,
        device_name: str,
    ) -> CompanionPairingRegistrationV1:
        assert device_name == "Nikolai's Mac"
        self.registrations += 1
        session = _pairing_state(gateway=gateway)
        await self.store.write(session)
        self.gateway_evidence = _gateway_evidence(pairing_state="pending")
        return CompanionPairingRegistrationV1(
            session=session,
            pairing_code=PAIRING_CODE,
        )

    async def approve_locally(self) -> CompanionPairingStateV1:
        self.approvals += 1
        state = await self.store.read()
        self.gateway_evidence = _gateway_evidence(pairing_state="local_approved")
        return state

    async def status(self) -> CompanionGatewayStatusV1:
        if isinstance(self.gateway_evidence, Exception):
            raise self.gateway_evidence
        return self.gateway_evidence

    async def revoke(self) -> None:
        self.revocations += 1
        await self.store.remove()


@dataclass(frozen=True, slots=True)
class _RuntimeStatus:
    state: PairingConnectionState

    def connection_state(self) -> PairingConnectionState:
        return self.state


def _pairing_state(
    *,
    gateway: CompanionGatewayProfileV1 | None = None,
) -> CompanionPairingStateV1:
    return CompanionPairingStateV1(
        gateway=gateway
        or CompanionGatewayProfileV1(base_url="https://foldweave.example.workers.dev"),
        device_id=DEVICE_ID,
        session_id=SESSION_ID,
        pairing_code_expires_at=EXPIRES_MS,
        next_device_sequence=2,
    )


def _gateway_evidence(
    *,
    pairing_state: str,
    authorized: bool = False,
    connected: bool = False,
    revoked: bool = False,
    expires_at: int = EXPIRES_MS,
) -> CompanionGatewayStatusV1:
    return CompanionGatewayStatusV1(
        schema_version="foldweave-pairing-status.v1",
        request_id="request_id_for_pairing_status",
        device_id=DEVICE_ID,
        session_id=SESSION_ID,
        pairing_state=pairing_state,
        authorized=authorized,
        connected=connected,
        revoked=revoked,
        expires_at=expires_at,
        last_seen_at=None,
    )


@pytest.mark.anyio
async def test_pairing_service_keeps_local_approval_distinct_from_oauth(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "private" / "pairing.json")
    client = _FakePairingClient(
        store=store,
        gateway_evidence=CompanionTransportError(
            "pairing_not_configured",
            "No pairing exists.",
        ),
    )
    service = FoldweavePairingService(
        state_store=store,
        pairing=client,
        now_ms=lambda: NOW_MS,
    )

    assert (await service.view()).status is PairingPageStatus.NOT_CONFIGURED
    registered = await service.register(
        gateway_url="https://foldweave.example.workers.dev",
        device_name="Nikolai's Mac",
    )
    assert registered.status is PairingPageStatus.AWAITING_LOCAL_APPROVAL
    assert registered.pairing_code == PAIRING_CODE
    assert registered.expires_at is not None
    assert registered.expires_at.endswith("CEST")

    approved = await service.approve_locally()
    assert approved.status is PairingPageStatus.LOCAL_ONLY
    assert "OAuth authorization has not completed" in approved.detail
    assert client.approvals == 1


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("gateway", "runtime", "expected"),
    (
        (
            _gateway_evidence(
                pairing_state="authorized",
                authorized=True,
                connected=True,
            ),
            None,
            PairingPageStatus.CONNECTED,
        ),
        (
            _gateway_evidence(pairing_state="authorized", authorized=True),
            None,
            PairingPageStatus.DISCONNECTED,
        ),
        (
            _gateway_evidence(pairing_state="authorized", authorized=True),
            _RuntimeStatus(PairingConnectionState.RECONNECTING),
            PairingPageStatus.RECONNECTING,
        ),
        (
            _gateway_evidence(pairing_state="revoked", revoked=True),
            None,
            PairingPageStatus.REVOKED,
        ),
        (
            _gateway_evidence(
                pairing_state="expired",
                expires_at=NOW_MS - 1,
            ),
            None,
            PairingPageStatus.EXPIRED,
        ),
    ),
)
async def test_pairing_service_uses_only_authoritative_gateway_and_runtime_status(
    tmp_path: Path,
    gateway: CompanionGatewayStatusV1,
    runtime: _RuntimeStatus | None,
    expected: PairingPageStatus,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / expected / "pairing.json")
    await store.write(_pairing_state())
    service = FoldweavePairingService(
        state_store=store,
        pairing=_FakePairingClient(store=store, gateway_evidence=gateway),
        runtime_status=runtime,
        now_ms=lambda: NOW_MS,
    )

    view = await service.view()

    assert view.status is expected
    if expected in {
        PairingPageStatus.CONNECTED,
        PairingPageStatus.DISCONNECTED,
        PairingPageStatus.RECONNECTING,
    }:
        assert view.configured is True


@pytest.mark.anyio
async def test_restart_preserves_local_state_without_inventing_authorization(
    tmp_path: Path,
) -> None:
    path = tmp_path / "private" / "pairing.json"
    store = CompanionPairingStateStore(path=path)
    await store.write(_pairing_state())
    unavailable = CompanionTransportError(
        "gateway_unavailable",
        "The gateway is unavailable.",
    )

    restarted = FoldweavePairingService(
        state_store=CompanionPairingStateStore(path=path),
        pairing=_FakePairingClient(store=store, gateway_evidence=unavailable),
        now_ms=lambda: EXPIRES_MS + 1,
    )
    view = await restarted.view()

    assert view.status is PairingPageStatus.LOCAL_ONLY
    assert "could not be confirmed" in view.detail
    assert view.pairing_code is None


@dataclass(slots=True)
class _ConnectedReviewService:
    evidence_disclosure_required: bool = False
    planner_label: str = "Foldweave reviewed planning"
    planner_note: str = "Review before execution."

    async def plan_and_create_copy(self, **_: object) -> FolderReviewHandle:
        return _review_handle(FolderJourney.ORGANIZE)

    async def apply_shared_change(self, **_: object) -> FolderReviewHandle:
        return _review_handle(FolderJourney.APPLY)

    def get_plan_preview(self, job_id: str) -> object:
        del job_id
        raise AssertionError("Preview rendering is outside this focused test.")

    async def accept_review(self, **_: object) -> object:
        raise AssertionError("Acceptance is outside this focused test.")


def _review_handle(journey: FolderJourney) -> FolderReviewHandle:
    return FolderReviewHandle(
        job_id="a" * 32,
        job_revision=1,
        proposal_revision=0,
        candidate_fingerprint="b" * 64,
        preview_fingerprint="c" * 64,
        source_root=Path("/tmp/foldweave-source"),
        output_parent=Path("/tmp/foldweave-output"),
        result_folder_name="foldweave-result",
        journey=journey,
    )


def _csrf(response: httpx.Response) -> str:
    match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
    assert match is not None
    return match.group(1)


@pytest.mark.anyio
async def test_pairing_routes_are_csrf_bound_path_free_and_explain_both_live_modes(
    tmp_path: Path,
) -> None:
    store = CompanionPairingStateStore(path=tmp_path / "private" / "pairing.json")
    client = _FakePairingClient(
        store=store,
        gateway_evidence=CompanionTransportError(
            "pairing_not_configured",
            "No pairing exists.",
        ),
    )
    pairing = FoldweavePairingService(
        state_store=store,
        pairing=client,
        now_ms=lambda: NOW_MS,
    )
    app = create_folder_app(
        _ConnectedReviewService(),
        pairing_service=pairing,
    )

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as browser:
        home = await browser.get("/")
        initial = await browser.get("/pairing")
        rejected = await browser.post(
            "/pairing/register",
            data={
                "csrf_token": "wrong",
                "gateway_url": "https://foldweave.example.workers.dev",
                "device_name": "Nikolai's Mac",
            },
        )
        registered = await browser.post(
            "/pairing/register",
            data={
                "csrf_token": _csrf(initial),
                "gateway_url": "https://foldweave.example.workers.dev",
                "device_name": "Nikolai's Mac",
            },
            follow_redirects=True,
        )
        approved = await browser.post(
            "/pairing/approve",
            data={"csrf_token": _csrf(registered)},
            follow_redirects=True,
        )

    assert home.status_code == 200
    assert "Direct API" in home.text
    assert "ChatGPT-hosted" in home.text
    assert "Manage ChatGPT pairing" in home.text
    assert initial.status_code == 200
    assert "Not paired" in initial.text
    assert rejected.status_code == 422
    assert PAIRING_CODE in registered.text
    assert "Waiting for local approval" in registered.text
    assert "Locally approved; finish in ChatGPT" in approved.text
    assert "This alone does not authorize ChatGPT" in approved.text
    for forbidden in (DEVICE_ID, SESSION_ID, str(tmp_path), "privateKey", "signature"):
        assert forbidden not in registered.text
        assert forbidden not in approved.text


@pytest.mark.anyio
async def test_active_apply_uses_foldweave_change_file_wording() -> None:
    app = create_folder_app(
        _ConnectedReviewService(),
        pairing_service=_StaticPairingService(),
    )
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://testserver",
    ) as browser:
        page = await browser.get("/apply")
        started = await browser.post(
            "/apply",
            data={
                "csrf_token": _csrf(page),
                "change_file": "/tmp/change.foldweave-change.json",
                "source_root": "/tmp/foldweave-source",
                "output_parent": "/tmp/foldweave-output",
            },
        )
        await asyncio.sleep(0)

    assert page.status_code == 200
    assert "Choose a Foldweave Change File" in page.text
    assert started.status_code == 303
    assert app.state.folder_web_state.request_value == (
        "Applying the selected Foldweave Change File"
    )


class _StaticPairingService:
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
