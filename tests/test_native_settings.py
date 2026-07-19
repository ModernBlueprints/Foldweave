from dataclasses import dataclass, field

import pytest

from name_atlas.native_settings import (
    CredentialStoreError,
    DirectEndpointProfile,
    MacOSKeychainCredentialStore,
    NativeSettingsService,
    SessionCredentialStore,
)


@dataclass
class FakeKeychainAdapter:
    value: bytes | None = field(default=None, repr=False)

    def exists(self, *, service: str, account: str) -> bool:
        assert service and account
        return self.value is not None

    def read(self, *, service: str, account: str) -> bytes:
        assert service and account
        if self.value is None:
            raise CredentialStoreError(
                "credential_not_configured",
                "No direct API credential is configured.",
            )
        return self.value

    def write(self, *, service: str, account: str, value: bytes) -> None:
        assert service and account
        self.value = value

    def remove(self, *, service: str, account: str) -> bool:
        assert service and account
        existed = self.value is not None
        self.value = None
        return existed


class ImmediateScheduler:
    def call(self, function, *, timeout_seconds: float):
        assert timeout_seconds > 0
        return function()


@dataclass
class FixedPrompt:
    value: str | None

    def prompt(self) -> str | None:
        return self.value


def test_keychain_store_add_read_update_remove_without_status_secret() -> None:
    adapter = FakeKeychainAdapter()
    store = MacOSKeychainCredentialStore(adapter=adapter)

    assert store.status().model_dump(mode="json") == {
        "configured": False,
        "status_code": None,
        "store_kind": "keychain",
    }
    store.write("qualification-secret-one")
    assert store.status().configured is True
    assert "qualification-secret-one" not in store.status().model_dump_json()
    assert store.read() == "qualification-secret-one"
    store.write("qualification-secret-two")
    assert store.read() == "qualification-secret-two"
    assert store.remove() is True
    assert store.remove() is False
    assert store.status().configured is False


def test_native_settings_configure_cancel_and_remove_are_status_only() -> None:
    store = SessionCredentialStore()
    service = NativeSettingsService(
        store=store,
        scheduler=ImmediateScheduler(),
        prompt=FixedPrompt("trusted-session-secret"),
    )

    configured = service.configure()
    assert configured.model_dump(mode="json") == {
        "configured": True,
        "status": "configured",
        "status_code": None,
    }
    assert "trusted-session-secret" not in configured.model_dump_json()
    assert "trusted-session-secret" not in service.view().model_dump_json()

    service.prompt = FixedPrompt(None)
    cancelled = service.configure()
    assert cancelled.status == "cancelled"
    assert store.read() == "trusted-session-secret"

    removed = service.remove()
    assert removed.status == "removed"
    assert store.status().configured is False


@pytest.mark.parametrize(
    "endpoint",
    (
        "http://api.openai.com/v1",
        "https://user@api.openai.com/v1",
        "https://api.openai.com/v1?debug=true",
        "https://api.openai.com/v1#fragment",
        "https://api.openai.com:443/v1",
        "https://api.openai.com/v1/",
    ),
)
def test_official_endpoint_rejects_noncanonical_or_expanded_authority(
    endpoint: str,
) -> None:
    with pytest.raises(ValueError):
        DirectEndpointProfile(
            profile_kind="openai_official",
            endpoint=endpoint,
            model_alias="gpt-5.6",
            store_false_claim=True,
            openai_pricing_claim=True,
        )


def test_compatible_endpoint_is_explicit_and_inherits_no_openai_claims() -> None:
    profile = DirectEndpointProfile.compatible(
        endpoint="https://models.example.test/v1/",
        model_alias="compatible-model",
    )
    assert profile.endpoint == "https://models.example.test/v1"
    assert profile.store_false_claim is False
    assert profile.openai_pricing_claim is False

    for invalid in (
        "http://models.example.test/v1",
        "https://user@models.example.test/v1",
        "https://models.example.test/v1?x=1",
        "https://models.example.test/v1#x",
    ):
        with pytest.raises(ValueError):
            DirectEndpointProfile.compatible(
                endpoint=invalid,
                model_alias="compatible-model",
            )
