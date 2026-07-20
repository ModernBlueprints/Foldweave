"""Local companion identity, capability, signature, and replay tests."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from name_atlas.foldweave_companion import (
    CompanionContractError,
    CompanionReplayGuard,
    CompanionSignedEnvelopeV1,
    DeviceIdentityStore,
    GatewayRelayGuard,
    TrustedPublicInvocationContextV1,
    describe_mcp_operation,
    parse_companion_challenge,
    parse_companion_rpc_request,
    trusted_public_invocation,
)
from name_atlas.foldweave_local_handles import (
    FoldweaveLocalHandleError,
    FoldweaveLocalHandleStore,
)
from name_atlas.native_bridge import NativePathRole

oslo_tz = ZoneInfo("Europe/Oslo")


def _public_invocation(
    *,
    body: str,
    headers: dict[str, str],
    issued_at: int,
    expires_at: int,
    request_id: str,
    sequence: int,
    device_id: str = "fwd_" + "d" * 32,
    session_id: str = "s" * 43,
    scopes: tuple[str, ...] = (
        "foldweave.execute",
        "foldweave.plan",
        "foldweave.review",
    ),
    nonce: str = "invocation_nonce_1234567890",
    revoked_at: int | None = None,
) -> dict[str, object]:
    body_sha256 = hashlib.sha256(body.encode()).hexdigest()
    descriptor, operation_sha256, _required_scope = describe_mcp_operation(
        body=body,
        body_sha256=body_sha256,
        headers=headers,
    )
    return {
        "bodyDigest": body_sha256,
        "channel": "chatgpt_hosted",
        "deviceId": device_id,
        "expiresAt": expires_at,
        "issuedAt": issued_at,
        "jobId": descriptor["jobId"],
        "nonce": nonce,
        "oauthGrantFingerprint": "a" * 64,
        "operationDigest": operation_sha256,
        "requestId": request_id,
        "revokedAt": revoked_at,
        "schemaVersion": "foldweave-public-invocation.v1",
        "scopes": list(scopes),
        "sequence": sequence,
        "sessionId": session_id,
    }


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


def test_device_identity_is_stable_keychain_backed_and_signs_canonical_body() -> None:
    keychain = _MemoryKeychain()
    store = DeviceIdentityStore(adapter=keychain)

    first = store.load_or_create()
    second = DeviceIdentityStore(adapter=keychain).load_or_create()
    assert first == second
    stored_text = next(iter(keychain.items.values())).decode("utf-8")
    assert first.public_key not in stored_text
    assert "private_key" in json.loads(stored_text)

    envelope = store.sign_envelope(
        request_id="1" * 32,
        sequence=1,
        body={
            "body": "{}",
            "headers": {"content-type": "application/json"},
            "requestId": "1" * 32,
            "status": 200,
            "type": "mcp_response",
        },
        issued_at=1_000_000,
        nonce="2" * 32,
    )
    assert envelope.wire_payload()["schemaVersion"] == ("foldweave-device-envelope.v1")
    assert set(first.public_jwk()) == {"crv", "kty", "x"}
    assert first.registration_body(device_name="Nikolai's Mac")["deviceId"] == (
        first.device_id
    )
    CompanionReplayGuard().verify_and_record(
        envelope,
        device_id=first.device_id,
        public_key=first.public_key,
        now=1_001_000,
    )

    forged_payload = envelope.model_dump(mode="python")
    forged_payload["body"] = {"job_id": "a" * 32, "status": "verified"}
    with pytest.raises(ValueError, match="body digest"):
        CompanionSignedEnvelopeV1.model_validate(forged_payload, strict=True)


def test_public_job_capability_is_restart_stable_and_job_bound() -> None:
    keychain = _MemoryKeychain()
    store = DeviceIdentityStore(adapter=keychain)
    identity = store.load_or_create()
    inputs = {
        "job_id": "a" * 32,
        "device_id": identity.device_id,
        "oauth_grant_fingerprint": "b" * 64,
        "scopes": (
            "foldweave.execute",
            "foldweave.plan",
            "foldweave.review",
        ),
        "expires_at_ms": 8_800_000,
    }

    first = store.derive_public_job_capability_id(**inputs)
    restarted = DeviceIdentityStore(adapter=keychain)
    assert restarted.derive_public_job_capability_id(**inputs) == first
    assert first.startswith("fwjc_")
    assert len(first) == 91
    assert first not in next(iter(keychain.items.values())).decode("utf-8")
    assert (
        restarted.derive_public_job_capability_id(**{**inputs, "job_id": "c" * 32})
        != first
    )


def test_replay_guard_blocks_nonce_sequence_signature_and_time_failures() -> None:
    first_store = DeviceIdentityStore(adapter=_MemoryKeychain())
    first_identity = first_store.load_or_create()
    guard = CompanionReplayGuard()
    first = first_store.sign_envelope(
        request_id="3" * 32,
        sequence=1,
        body={"type": "heartbeat"},
        issued_at=2_000_000,
        nonce="4" * 32,
    )
    guard.verify_and_record(
        first,
        device_id=first_identity.device_id,
        public_key=first_identity.public_key,
        now=2_001_000,
    )

    with pytest.raises(CompanionContractError, match="nonce was already used"):
        guard.verify_and_record(
            first,
            device_id=first_identity.device_id,
            public_key=first_identity.public_key,
            now=2_001_000,
        )

    old_sequence = first_store.sign_envelope(
        request_id="5" * 32,
        sequence=1,
        body={"type": "heartbeat"},
        issued_at=2_001_000,
        nonce="6" * 32,
    )
    with pytest.raises(CompanionContractError, match="sequence is not monotonic"):
        guard.verify_and_record(
            old_sequence,
            device_id=first_identity.device_id,
            public_key=first_identity.public_key,
            now=2_002_000,
        )

    second_store = DeviceIdentityStore(adapter=_MemoryKeychain())
    second_store.load_or_create()
    wrong_key_envelope = second_store.sign_envelope(
        request_id="7" * 32,
        sequence=2,
        body={"type": "heartbeat"},
        issued_at=2_002_000,
        nonce="8" * 32,
    )
    with pytest.raises(CompanionContractError, match="signature is invalid"):
        guard.verify_and_record(
            wrong_key_envelope,
            device_id=first_identity.device_id,
            public_key=first_identity.public_key,
            now=2_003_000,
        )

    expired = first_store.sign_envelope(
        request_id="9" * 32,
        sequence=2,
        body={"type": "heartbeat"},
        issued_at=2_000_000,
        lifetime_ms=1,
        nonce="a" * 32,
    )
    with pytest.raises(CompanionContractError, match="has expired"):
        guard.verify_and_record(
            expired,
            device_id=first_identity.device_id,
            public_key=first_identity.public_key,
            now=2_002_000,
        )


def test_gateway_challenge_and_rpc_request_are_exact_digest_and_replay_bound() -> None:
    challenge = parse_companion_challenge(
        {
            "challenge": "c" * 43,
            "expiresAt": 4_060_000,
            "sessionId": "s" * 43,
            "type": "companion_challenge",
        }
    )
    assert challenge.session_id == "s" * 43

    body = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
    headers = {
        "accept": "application/json, text/event-stream",
        "content-type": "application/json",
        "x-foldweave-http-method": "POST",
    }
    request = parse_companion_rpc_request(
        {
            "body": body,
            "bodyDigest": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "expiresAt": 4_025_000,
            "headers": headers,
            "issuedAt": 4_000_000,
            "invocation": _public_invocation(
                body=body,
                headers=headers,
                issued_at=4_000_000,
                expires_at=4_025_000,
                request_id="r" * 32,
                sequence=12,
            ),
            "requestId": "r" * 32,
            "sequence": 12,
            "type": "mcp_request",
        }
    )
    guard = GatewayRelayGuard()
    guard.verify_and_record(
        request,
        expected_device_id="fwd_" + "d" * 32,
        expected_session_id="s" * 43,
        now=4_001_000,
    )
    with pytest.raises(CompanionContractError, match="sequence is not monotonic"):
        guard.verify_and_record(
            request,
            expected_device_id="fwd_" + "d" * 32,
            expected_session_id="s" * 43,
            now=4_001_000,
        )

    replayed_context = _public_invocation(
        body=body,
        headers=headers,
        issued_at=4_000_050,
        expires_at=4_025_050,
        request_id="n" * 32,
        sequence=13,
    )
    replayed_context["nonce"] = request.invocation.nonce
    nonce_replay = parse_companion_rpc_request(
        {
            "body": body,
            "bodyDigest": hashlib.sha256(body.encode()).hexdigest(),
            "expiresAt": 4_025_050,
            "headers": headers,
            "issuedAt": 4_000_050,
            "invocation": replayed_context,
            "requestId": "n" * 32,
            "sequence": 13,
            "type": "mcp_request",
        }
    )
    with pytest.raises(CompanionContractError, match="nonce was replayed"):
        guard.verify_and_record(
            nonce_replay,
            expected_device_id="fwd_" + "d" * 32,
            expected_session_id="s" * 43,
            now=4_001_000,
        )

    retry_headers = {"x-foldweave-http-method": "POST"}
    retried_request = parse_companion_rpc_request(
        {
            "body": body,
            "bodyDigest": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "expiresAt": 4_025_100,
            "headers": retry_headers,
            "issuedAt": 4_000_100,
            "invocation": _public_invocation(
                body=body,
                headers=retry_headers,
                issued_at=4_000_100,
                expires_at=4_025_100,
                request_id="r" * 32,
                sequence=14,
                nonce="invocation_nonce_abcdefghijk",
            ),
            "requestId": "r" * 32,
            "sequence": 14,
            "type": "mcp_request",
        }
    )
    guard.verify_and_record(
        retried_request,
        expected_device_id="fwd_" + "d" * 32,
        expected_session_id="s" * 43,
        now=4_001_000,
    )

    wrong_digest = {
        "body": body,
        "bodyDigest": "0" * 64,
        "expiresAt": 4_025_000,
        "headers": {"content-type": "application/json"},
        "issuedAt": 4_000_000,
        "invocation": _public_invocation(
            body=body,
            headers={"content-type": "application/json"},
            issued_at=4_000_000,
            expires_at=4_025_000,
            request_id="x" * 32,
            sequence=13,
        ),
        "requestId": "x" * 32,
        "sequence": 13,
        "type": "mcp_request",
    }
    with pytest.raises(ValueError, match="body digest"):
        parse_companion_rpc_request(wrong_digest)

    with pytest.raises(CompanionContractError, match="unsupported or missing"):
        parse_companion_challenge(
            {
                "challenge": "c" * 43,
                "expiresAt": 4_060_000,
                "sessionId": "s" * 43,
                "type": "companion_challenge",
                "path": "/private/project",
            }
        )


def test_typescript_operation_digest_vector_is_byte_identical() -> None:
    body = (
        '{"id":1,"jsonrpc":"2.0","method":"tools/call","params":'
        '{"arguments":{"job_id":"'
        + "a" * 32
        + '"},"name":"accept_plan_and_create_copy"}}'
    )
    body_sha256 = hashlib.sha256(body.encode()).hexdigest()
    descriptor, operation_sha256, required_scope = describe_mcp_operation(
        body=body,
        body_sha256=body_sha256,
        headers={
            "mcp-session-id": "mcp-session-1",
            "x-foldweave-http-method": "POST",
        },
    )

    assert body_sha256 == (
        "43413ebccc99358a3df383b31f65272f028c073a9147339ee3c8f572de46f0e8"
    )
    assert operation_sha256 == (
        "aaeb4e431ee0f8c93ede6e1bf34c9683891d5edc35d0ac9b73472c6dedb5b3ac"
    )
    assert descriptor["jobId"] == "a" * 32
    assert "capabilityId" not in descriptor
    assert "capabilityExpiresAt" not in descriptor
    assert required_scope == "foldweave.execute"


@pytest.mark.parametrize(
    "tool_name,arguments",
    [
        ("job_status", {}),
        (
            "job_status",
            {
                "capability_id": "fwjc_" + "C" * 86,
                "job_id": "a" * 32,
            },
        ),
        (
            "choose_local_item",
            {
                "capability_expires_at": 5_800_000,
                "capability_id": "fwjc_" + "C" * 86,
                "job_id": "a" * 32,
                "role": "source_folder",
            },
        ),
    ],
)
def test_public_operation_requires_job_identity_and_forbids_raw_capability(
    tool_name: str,
    arguments: dict[str, object],
) -> None:
    body = json.dumps(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"arguments": arguments, "name": tool_name},
        },
        separators=(",", ":"),
    )
    with pytest.raises(CompanionContractError):
        describe_mcp_operation(
            body=body,
            body_sha256=hashlib.sha256(body.encode()).hexdigest(),
            headers={"x-foldweave-http-method": "POST"},
        )


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ({"scopes": ["foldweave.review"]}, "gateway_invocation_scope_missing"),
        ({"deviceId": "fwd_" + "e" * 32}, "gateway_invocation_device_mismatch"),
        ({"expiresAt": 4_000_500}, "gateway_invocation_expired"),
        ({"revokedAt": 4_000_100}, "gateway_invocation_revoked"),
    ],
)
def test_public_invocation_blocks_wrong_scope_device_expiry_and_revocation(
    mutation: dict[str, object],
    expected_code: str,
) -> None:
    body = json.dumps(
        {
            "id": 1,
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "arguments": {
                    "job_id": "b" * 32,
                },
                "name": "accept_plan_and_create_copy",
            },
        },
        separators=(",", ":"),
    )
    headers = {"content-type": "application/json", "x-foldweave-http-method": "POST"}
    invocation = _public_invocation(
        body=body,
        headers=headers,
        issued_at=4_000_000,
        expires_at=4_025_000,
        request_id="q" * 32,
        sequence=1,
    )
    invocation.update(mutation)
    request = parse_companion_rpc_request(
        {
            "body": body,
            "bodyDigest": hashlib.sha256(body.encode()).hexdigest(),
            "expiresAt": invocation["expiresAt"],
            "headers": headers,
            "issuedAt": 4_000_000,
            "invocation": invocation,
            "requestId": "q" * 32,
            "sequence": 1,
            "type": "mcp_request",
        }
    )
    with pytest.raises(CompanionContractError) as exc_info:
        GatewayRelayGuard().verify_and_record(
            request,
            expected_device_id="fwd_" + "d" * 32,
            expected_session_id="s" * 43,
            now=4_001_000,
        )
    assert exc_info.value.code == expected_code


def test_public_local_handle_is_bound_to_exact_device_session_and_grant(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    store = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 20, 10, 0, tzinfo=oslo_tz),
        token_factory=lambda: "H" * 43,
    )
    body = '{"jsonrpc":"2.0","method":"tools/list","id":1}'
    headers = {"x-foldweave-http-method": "POST"}
    first = TrustedPublicInvocationContextV1.model_validate(
        {
            "body_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "channel": "chatgpt_hosted",
            "device_id": "fwd_" + "d" * 32,
            "expires_at": 4_025_000,
            "issued_at": 4_000_000,
            "job_id": None,
            "nonce": "handle_invocation_nonce_1234",
            "oauth_grant_fingerprint": "a" * 64,
            "operation_sha256": describe_mcp_operation(
                body=body,
                body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                headers=headers,
            )[1],
            "request_id": "h" * 32,
            "revoked_at": None,
            "scopes": ("foldweave.review",),
            "sequence": 1,
            "session_id": "s" * 43,
        },
        strict=True,
    )
    with trusted_public_invocation(first):
        handle = store.register(
            role=NativePathRole.SOURCE_FOLDER,
            path=source,
            channel="chatgpt_hosted",
        )
        assert (
            store.resolve(
                handle.handle,
                role=NativePathRole.SOURCE_FOLDER,
                channel="chatgpt_hosted",
            )
            == source.resolve()
        )
    for update in (
        {"device_id": "fwd_" + "e" * 32},
        {"session_id": "t" * 43},
        {"oauth_grant_fingerprint": "b" * 64},
    ):
        mismatched = first.model_copy(update=update)
        with (
            trusted_public_invocation(mismatched),
            pytest.raises(FoldweaveLocalHandleError) as exc_info,
        ):
            store.resolve(
                handle.handle,
                role=NativePathRole.SOURCE_FOLDER,
                channel="chatgpt_hosted",
            )
        assert exc_info.value.code == "local_handle_public_binding_mismatch"
    with pytest.raises(FoldweaveLocalHandleError) as unbound_error:
        store.resolve(
            handle.handle,
            role=NativePathRole.SOURCE_FOLDER,
            channel="chatgpt_hosted",
        )
    assert unbound_error.value.code == "local_handle_public_binding_mismatch"
