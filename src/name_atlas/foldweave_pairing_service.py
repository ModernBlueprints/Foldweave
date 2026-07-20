"""Truthful native/browser presentation for Foldweave ChatGPT pairing."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Protocol, runtime_checkable
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from name_atlas.foldweave_companion import (
    CompanionContractError,
    DeviceIdentityStore,
)
from name_atlas.foldweave_companion_client import (
    CompanionGatewayProfileV1,
    CompanionGatewayStatusV1,
    CompanionPairingClient,
    CompanionPairingRegistrationV1,
    CompanionPairingStateStore,
    CompanionPairingStateV1,
    CompanionTransportError,
)
from name_atlas.foldweave_companion_supervisor import PairingConnectionState

oslo_tz = ZoneInfo("Europe/Oslo")


class PairingPageStatus(StrEnum):
    """Path-free statuses that the pairing page may display."""

    NOT_CONFIGURED = "not_configured"
    AWAITING_LOCAL_APPROVAL = "awaiting_local_approval"
    LOCAL_ONLY = "local_only"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"
    REVOKED = "revoked"
    EXPIRED = "expired"
    LOCAL_STATE_INVALID = "local_state_invalid"


class PairingClientOperations(Protocol):
    """The narrow companion operations used by the presentation service."""

    async def register(
        self,
        gateway: CompanionGatewayProfileV1,
        *,
        device_name: str,
    ) -> CompanionPairingRegistrationV1: ...

    async def approve_locally(self) -> CompanionPairingStateV1: ...

    async def status(self) -> CompanionGatewayStatusV1: ...

    async def revoke(self) -> None: ...


class PairingRuntimeStatus(Protocol):
    """Optional exact local companion reconnect evidence."""

    def connection_state(self) -> PairingConnectionState: ...


class PairingRuntimeLifecycle(Protocol):
    """App-owned companion lifecycle triggered by durable pairing changes."""

    async def start(self) -> None: ...

    async def pairing_state_changed(self) -> None: ...

    async def stop_companion(self) -> None: ...

    async def shutdown(self) -> None: ...


@runtime_checkable
class PairingApplicationLifecycle(Protocol):
    """Optional lifespan hooks exposed by the concrete pairing service."""

    async def start_background_runtime(self) -> None: ...

    async def stop_background_runtime(self) -> None: ...


class PairingLifecycleOperations(Protocol):
    """Injected renderer-facing pairing lifecycle."""

    async def view(self) -> PairingPageView: ...

    async def register(
        self,
        *,
        gateway_url: str,
        device_name: str,
    ) -> PairingPageView: ...

    async def approve_locally(self) -> PairingPageView: ...

    async def revoke(self) -> PairingPageView: ...


@dataclass(frozen=True, slots=True)
class PairingPageView:
    """Renderer-safe pairing state with no device or session identifiers."""

    status: PairingPageStatus
    status_label: str
    detail: str
    configured: bool
    gateway_url: str | None = None
    pairing_code: str | None = None
    expires_at: str | None = None
    can_register: bool = False
    can_approve: bool = False
    can_revoke: bool = False


class PairingLifecycleError(RuntimeError):
    """One stable and disclosure-safe pairing-page failure."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


@dataclass(slots=True)
class FoldweavePairingService:
    """Coordinate pairing UI actions without becoming transport authority."""

    state_store: CompanionPairingStateStore
    pairing: PairingClientOperations
    runtime_status: PairingRuntimeStatus | None = None
    runtime_lifecycle: PairingRuntimeLifecycle | None = None
    now_ms: Callable[[], int] = field(
        default=lambda: int(time.time() * 1_000),
        repr=False,
    )
    _registration: CompanionPairingRegistrationV1 | None = field(
        default=None,
        init=False,
        repr=False,
    )
    _local_approval_observed: bool = field(default=False, init=False, repr=False)

    async def view(self) -> PairingPageView:
        """Return the strongest truthful status supported by current evidence."""

        try:
            local = await self.state_store.read()
        except CompanionTransportError as exc:
            if exc.code == "pairing_not_configured":
                return _not_configured_view()
            return PairingPageView(
                status=PairingPageStatus.LOCAL_STATE_INVALID,
                status_label="Local pairing state unavailable",
                detail=(
                    "Foldweave could not validate the saved pairing state. "
                    "No ChatGPT authorization or connection is being claimed."
                ),
                configured=False,
                can_register=False,
            )

        registration = self._current_registration(local)
        try:
            gateway = await self.pairing.status()
        except (
            CompanionContractError,
            CompanionTransportError,
            OSError,
            ValidationError,
        ):
            return self._local_only_view(local, registration)
        return self._gateway_view(local, registration, gateway)

    async def start_background_runtime(self) -> None:
        """Start packaged-app ownership without requiring a configured pairing."""

        if self.runtime_lifecycle is not None:
            await self.runtime_lifecycle.start()

    async def stop_background_runtime(self) -> None:
        """Stop and await the packaged-app-owned companion runtime."""

        if self.runtime_lifecycle is not None:
            await self.runtime_lifecycle.shutdown()

    async def register(
        self,
        *,
        gateway_url: str,
        device_name: str,
    ) -> PairingPageView:
        """Register one device and retain its one-time code only in memory."""

        current = await self.view()
        if not current.can_register:
            raise PairingLifecycleError(
                "pairing_already_configured",
                "Revoke the current pairing before registering another.",
            )
        try:
            gateway = CompanionGatewayProfileV1(base_url=gateway_url)
            registration = await self.pairing.register(
                gateway,
                device_name=device_name,
            )
        except (CompanionContractError, CompanionTransportError) as exc:
            raise _safe_lifecycle_error(exc.code) from exc
        except (ValidationError, OSError, RuntimeError, ValueError) as exc:
            raise PairingLifecycleError(
                "pairing_registration_invalid",
                "The gateway URL or device name is invalid, or registration failed.",
            ) from exc
        self._registration = registration
        self._local_approval_observed = False
        if self.runtime_lifecycle is not None:
            await self.runtime_lifecycle.pairing_state_changed()
        return await self.view()

    async def approve_locally(self) -> PairingPageView:
        """Sign local approval without claiming that OAuth has completed."""

        current = await self.view()
        if not current.can_approve:
            raise PairingLifecycleError(
                "pairing_local_approval_unavailable",
                "No current one-time pairing is available for local approval.",
            )
        try:
            await self.pairing.approve_locally()
        except (CompanionContractError, CompanionTransportError) as exc:
            raise _safe_lifecycle_error(exc.code) from exc
        except (OSError, RuntimeError, ValueError) as exc:
            raise PairingLifecycleError(
                "pairing_local_approval_failed",
                "Local approval could not be confirmed.",
            ) from exc
        self._local_approval_observed = True
        if self.runtime_lifecycle is not None:
            await self.runtime_lifecycle.pairing_state_changed()
        return await self.view()

    async def revoke(self) -> PairingPageView:
        """Revoke gateway authorization before removing local pairing state."""

        try:
            await self.pairing.revoke()
        except (CompanionContractError, CompanionTransportError) as exc:
            raise _safe_lifecycle_error(exc.code) from exc
        except (OSError, RuntimeError, ValueError) as exc:
            raise PairingLifecycleError(
                "pairing_revocation_failed",
                "The Foldweave pairing could not be revoked.",
            ) from exc
        self._registration = None
        self._local_approval_observed = False
        if self.runtime_lifecycle is not None:
            await self.runtime_lifecycle.stop_companion()
        return _not_configured_view()

    def _current_registration(
        self,
        local: CompanionPairingStateV1,
    ) -> CompanionPairingRegistrationV1 | None:
        registration = self._registration
        if registration is None:
            return None
        if registration.session.session_id != local.session_id:
            self._registration = None
            return None
        return registration

    def _local_only_view(
        self,
        local: CompanionPairingStateV1,
        registration: CompanionPairingRegistrationV1 | None,
    ) -> PairingPageView:
        now = self.now_ms()
        if registration is not None and now >= local.pairing_code_expires_at:
            return PairingPageView(
                status=PairingPageStatus.EXPIRED,
                status_label="Pairing expired",
                detail=(
                    "The locally recorded pairing window expired. Register again "
                    "to create a new one-time code."
                ),
                configured=True,
                gateway_url=local.gateway.base_url,
                expires_at=_format_oslo_timestamp(local.pairing_code_expires_at),
                can_register=True,
                can_revoke=True,
            )
        if registration is not None and not self._local_approval_observed:
            return PairingPageView(
                status=PairingPageStatus.AWAITING_LOCAL_APPROVAL,
                status_label="Waiting for local approval",
                detail=(
                    "The gateway issued this one-time code. Confirm this installation "
                    "locally, then complete authorization in ChatGPT."
                ),
                configured=True,
                gateway_url=local.gateway.base_url,
                pairing_code=registration.pairing_code,
                expires_at=_format_oslo_timestamp(local.pairing_code_expires_at),
                can_approve=True,
                can_revoke=True,
            )
        detail = (
            "This installation is approved locally, but Foldweave cannot currently "
            "confirm OAuth authorization or a companion connection."
            if self._local_approval_observed
            else "A local pairing record exists, but gateway authorization and the "
            "companion connection could not be confirmed."
        )
        return PairingPageView(
            status=PairingPageStatus.LOCAL_ONLY,
            status_label="Local pairing only",
            detail=detail,
            configured=True,
            gateway_url=local.gateway.base_url,
            pairing_code=(None if registration is None else registration.pairing_code),
            expires_at=_format_oslo_timestamp(local.pairing_code_expires_at),
            can_revoke=True,
        )

    def _gateway_view(
        self,
        local: CompanionPairingStateV1,
        registration: CompanionPairingRegistrationV1 | None,
        gateway: CompanionGatewayStatusV1,
    ) -> PairingPageView:
        common = {
            "configured": True,
            "gateway_url": local.gateway.base_url,
            "expires_at": _format_oslo_timestamp(gateway.expires_at),
            "can_revoke": True,
        }
        if gateway.revoked or gateway.pairing_state == "revoked":
            return PairingPageView(
                status=PairingPageStatus.REVOKED,
                status_label="Pairing revoked",
                detail="The gateway confirms that this pairing has been revoked.",
                can_register=True,
                **common,
            )
        if gateway.pairing_state == "expired" or self.now_ms() >= gateway.expires_at:
            return PairingPageView(
                status=PairingPageStatus.EXPIRED,
                status_label="Pairing expired",
                detail="The gateway confirms that this pairing has expired.",
                can_register=True,
                **common,
            )
        if not gateway.authorized:
            if gateway.pairing_state == "pending":
                if registration is None:
                    return PairingPageView(
                        status=PairingPageStatus.LOCAL_ONLY,
                        status_label="Pairing code unavailable",
                        detail=(
                            "The gateway still has a pending pairing, but its "
                            "one-time code was intentionally not saved across restart. "
                            "Register again to create a new code."
                        ),
                        can_register=True,
                        **common,
                    )
                return PairingPageView(
                    status=PairingPageStatus.AWAITING_LOCAL_APPROVAL,
                    status_label="Waiting for local approval",
                    detail=(
                        "The gateway is waiting for this installation to confirm "
                        "the one-time pairing. This is not ChatGPT authorization."
                    ),
                    pairing_code=(
                        None if registration is None else registration.pairing_code
                    ),
                    can_approve=True,
                    **common,
                )
            return PairingPageView(
                status=PairingPageStatus.LOCAL_ONLY,
                status_label="Locally approved; finish in ChatGPT",
                detail=(
                    "The gateway confirms local approval, but OAuth authorization "
                    "has not completed. Enter the one-time code in ChatGPT."
                ),
                pairing_code=(
                    None if registration is None else registration.pairing_code
                ),
                **common,
            )
        if gateway.connected:
            return PairingPageView(
                status=PairingPageStatus.CONNECTED,
                status_label="Configured and connected",
                detail=(
                    "The gateway confirms OAuth authorization and a currently "
                    "authenticated Foldweave companion connection."
                ),
                **common,
            )
        if (
            self.runtime_status is not None
            and self.runtime_status.connection_state()
            is PairingConnectionState.RECONNECTING
        ):
            return PairingPageView(
                status=PairingPageStatus.RECONNECTING,
                status_label="Configured; reconnecting",
                detail=(
                    "OAuth authorization is active. The local companion reports "
                    "that it is reconnecting to the gateway."
                ),
                **common,
            )
        return PairingPageView(
            status=PairingPageStatus.DISCONNECTED,
            status_label="Configured; companion disconnected",
            detail=(
                "OAuth authorization is active, but the gateway does not currently "
                "observe an authenticated companion connection."
            ),
            **common,
        )


def create_default_pairing_service() -> FoldweavePairingService:
    """Compose the real pairing service without reading Keychain or using network."""

    state_store = CompanionPairingStateStore()
    pairing = CompanionPairingClient(
        identity_store=DeviceIdentityStore(),
        state_store=state_store,
    )
    return FoldweavePairingService(state_store=state_store, pairing=pairing)


def _not_configured_view() -> PairingPageView:
    return PairingPageView(
        status=PairingPageStatus.NOT_CONFIGURED,
        status_label="Not paired",
        detail=(
            "This Foldweave installation is not paired with ChatGPT. Direct API "
            "mode remains separately available in Secure settings."
        ),
        configured=False,
        can_register=True,
    )


def _format_oslo_timestamp(timestamp_ms: int) -> str:
    instant = datetime.fromtimestamp(timestamp_ms / 1_000, tz=oslo_tz)
    return f"{instant.day} {instant.strftime('%B %Y at %H:%M %Z')}"


def _safe_lifecycle_error(code: str) -> PairingLifecycleError:
    messages = {
        "device_name_invalid": "The device name is invalid.",
        "gateway_unavailable": "The Foldweave gateway is unavailable.",
        "gateway_request_rejected": "The Foldweave gateway rejected the request.",
        "gateway_response_invalid": "The Foldweave gateway response was invalid.",
        "gateway_response_too_large": "The Foldweave gateway response was too large.",
        "pairing_not_configured": "No Foldweave gateway pairing is configured.",
        "pairing_approval_failed": "Local pairing approval failed.",
        "pairing_revocation_failed": "The Foldweave pairing could not be revoked.",
        "pairing_state_invalid": "The saved Foldweave pairing state is invalid.",
    }
    return PairingLifecycleError(
        code if code in messages else "pairing_operation_failed",
        messages.get(code, "The pairing operation failed without exposing details."),
    )
