import { env, exports } from "cloudflare:workers";
import { beforeEach, describe, expect, it } from "vitest";

import {
  bytesToBase64Url,
  canonicalSha256,
  sha256Hex,
  type JsonValue,
} from "../src/canonical";
import { DEVICE_ENVELOPE_SCHEMA, DEVICE_REGISTRATION_SCHEMA } from "../src/constants";
import { signaturePayload } from "../src/device-crypto";
import {
  canonicalScopes,
  describeMcpOperation,
  oauthGrantFingerprint,
} from "../src/public-invocation";

const DIRECTORY_NAME = "foldweave-pairing-directory-v1";

function workerFetch(input: string, init?: RequestInit): Promise<Response> {
  return (exports as unknown as { default: Fetcher }).default.fetch(input, init);
}

async function postJson(stub: DurableObjectStub, path: string, body: JsonValue): Promise<Response> {
  return stub.fetch(`https://foldweave.internal${path}`, {
    body: JSON.stringify(body),
    headers: { "content-type": "application/json" },
    method: "POST",
  });
}

async function createSignedEnvelope(
  privateKey: CryptoKey,
  body: JsonValue,
  sequence: number,
  requestId: string,
  nonce: string,
  issuedAtOverride?: number,
): Promise<Record<string, JsonValue>> {
  const issuedAt = issuedAtOverride ?? Date.now();
  const unsigned = {
    body,
    bodyDigest: await canonicalSha256(body),
    expiresAt: issuedAt + 60_000,
    issuedAt,
    nonce,
    requestId,
    schemaVersion: DEVICE_ENVELOPE_SCHEMA,
    sequence,
  } as const;
  const signature = new Uint8Array(
    await crypto.subtle.sign(
      { name: "Ed25519" },
      privateKey,
      Uint8Array.from(signaturePayload(unsigned)).buffer,
    ),
  );
  return { ...unsigned, signature: bytesToBase64Url(signature) };
}

async function gzipBase64Url(
  value: string,
): Promise<{ body: string; compressedSize: number }> {
  const writer = new Blob([new TextEncoder().encode(value)])
    .stream()
    .pipeThrough(new CompressionStream("gzip"))
    .getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  while (true) {
    const { done, value: chunk } = await writer.read();
    if (done) {
      break;
    }
    chunks.push(chunk);
    total += chunk.byteLength;
  }
  const compressed = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    compressed.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return {
    body: bytesToBase64Url(compressed),
    compressedSize: compressed.byteLength,
  };
}

function nextSocketMessage(webSocket: WebSocket): Promise<Record<string, unknown>> {
  return new Promise((resolve, reject) => {
    const onMessage = (event: MessageEvent) => {
      cleanup();
      try {
        const value = JSON.parse(String(event.data)) as unknown;
        if (typeof value !== "object" || value === null || Array.isArray(value)) {
          throw new TypeError("WebSocket message is not an object.");
        }
        resolve(value as Record<string, unknown>);
      } catch (error) {
        reject(error);
      }
    };
    const onError = () => {
      cleanup();
      reject(new Error("WebSocket failed before the next message."));
    };
    const cleanup = () => {
      webSocket.removeEventListener("message", onMessage);
      webSocket.removeEventListener("error", onError);
    };
    webSocket.addEventListener("message", onMessage);
    webSocket.addEventListener("error", onError);
  });
}

describe("public worker metadata", () => {
  it("reports only non-sensitive readiness", async () => {
    const response = await workerFetch("https://gateway.example/healthz");
    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({
      bindings: {
        deviceSessions: true,
        oauthKv: true,
        pairingDirectory: true,
      },
      ready: true,
      service: "foldweave-gateway",
    });
  });

  it("advertises PKCE S256, CIMD, DCR, and no RFC 8693 grant", async () => {
    const response = await workerFetch(
      "https://gateway.example/.well-known/oauth-authorization-server",
    );
    expect(response.status).toBe(200);
    const metadata = (await response.json()) as Record<string, unknown>;
    expect(metadata.code_challenge_methods_supported).toEqual(["S256"]);
    expect(metadata.client_id_metadata_document_supported).toBe(true);
    expect(metadata.registration_endpoint).toBe("https://gateway.example/oauth/register");
    expect(metadata.grant_types_supported).not.toContain(
      "urn:ietf:params:oauth:grant-type:token-exchange",
    );
  });

  it("challenges unauthenticated MCP traffic", async () => {
    const response = await workerFetch("https://gateway.example/mcp", {
      body: JSON.stringify({ id: 1, jsonrpc: "2.0", method: "initialize" }),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    expect(response.status).toBe(401);
    expect(response.headers.get("www-authenticate")).toContain(
      "/.well-known/oauth-protected-resource",
    );
  });
});

describe("pairing directory", () => {
  let directory: DurableObjectStub;

  beforeEach(() => {
    directory = env.PAIRING_DIRECTORY.get(
      env.PAIRING_DIRECTORY.idFromName(DIRECTORY_NAME),
    );
  });

  it("requires local approval and atomically consumes one valid code", async () => {
    const now = Date.now();
    const codeHash = "a".repeat(64);
    const sessionId = "s".repeat(43);
    expect(
      (
        await postJson(directory, "/register", {
          codeHash,
          expiresAt: now + 600_000,
          sessionId,
        })
      ).status,
    ).toBe(200);
    expect(
      (
        await postJson(directory, "/authorize", {
          attemptedAt: now + 1,
          codeHash,
          ipHash: "b".repeat(64),
        })
      ).status,
    ).toBe(400);
    expect(
      (
        await postJson(directory, "/approve", {
          approvedAt: now + 2,
          codeHash,
          sessionId,
        })
      ).status,
    ).toBe(200);
    const authorized = await postJson(directory, "/authorize", {
      attemptedAt: now + 3,
      codeHash,
      ipHash: "b".repeat(64),
    });
    expect(authorized.status).toBe(200);
    await expect(authorized.json()).resolves.toEqual({ authorized: true, sessionId });
    expect(
      (
        await postJson(directory, "/authorize", {
          attemptedAt: now + 4,
          codeHash,
          ipHash: "b".repeat(64),
        })
      ).status,
    ).toBe(400);
  });

  it("locks one supplied code after five failures", async () => {
    const attemptedAt = Date.now();
    const codeHash = "c".repeat(64);
    const ipHash = "d".repeat(64);
    for (let attempt = 0; attempt < 4; attempt += 1) {
      const response = await postJson(directory, "/authorize", {
        attemptedAt: attemptedAt + attempt,
        codeHash,
        ipHash,
      });
      expect(response.status).toBe(400);
    }
    const fifth = await postJson(directory, "/authorize", {
      attemptedAt: attemptedAt + 4,
      codeHash,
      ipHash,
    });
    expect(fifth.status).toBe(429);
    await expect(fifth.json()).resolves.toMatchObject({ error: "pairing_code_locked" });
  });

  it("limits one source bucket to twenty attempts per fifteen minutes", async () => {
    const attemptedAt = Date.now();
    const ipHash = "e".repeat(64);
    for (let attempt = 0; attempt < 20; attempt += 1) {
      const codeHash = await sha256Hex(`missing-${attempt}`);
      const response = await postJson(directory, "/authorize", {
        attemptedAt: attemptedAt + attempt,
        codeHash,
        ipHash,
      });
      expect(response.status).toBe(400);
    }
    const limited = await postJson(directory, "/authorize", {
      attemptedAt: attemptedAt + 20,
      codeHash: await sha256Hex("missing-final"),
      ipHash,
    });
    expect(limited.status).toBe(429);
    await expect(limited.json()).resolves.toMatchObject({ error: "pairing_rate_limited" });
  });
});

describe("device registration and signed local approval", () => {
  it("accepts a self-signed Ed25519 registration and rejects replayed approval", async () => {
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const body = {
      deviceId: "fwd_0123456789abcdef0123456789abcdef",
      deviceName: "Test Mac",
      publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
      schemaVersion: DEVICE_REGISTRATION_SCHEMA,
    } as const;
    const registration = await createSignedEnvelope(
      keyPair.privateKey,
      body,
      1,
      "registration_0123456789abcdef",
      "nonce_registration_0123456789abcdef",
    );
    const registered = await workerFetch("https://gateway.example/pairing/register", {
      body: JSON.stringify(registration),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    expect(registered.status).toBe(201);
    const result = (await registered.json()) as Record<string, unknown>;
    expect(result.pairingCode).toMatch(/^[0-9A-HJKMNP-TV-Z]{10}$/u);
    expect(result.sessionId).toMatch(/^[A-Za-z0-9_-]{43}$/u);

    const approval = await createSignedEnvelope(
      keyPair.privateKey,
      {
        intent: "approve_pairing",
        sessionId: String(result.sessionId),
      },
      2,
      "approval_0123456789abcdef",
      "nonce_approval_0123456789abcdef",
    );
    const approved = await workerFetch(
      `https://gateway.example/pairing/approve?session=${result.sessionId}`,
      {
        body: JSON.stringify(approval),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(approved.status).toBe(200);

    const replayed = await workerFetch(
      `https://gateway.example/pairing/approve?session=${result.sessionId}`,
      {
        body: JSON.stringify(approval),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(replayed.status).toBe(409);
    await expect(replayed.json()).resolves.toMatchObject({
      error: "device_request_replayed",
    });
  });

  it("authenticates a companion socket and coalesces one signed relay response", async () => {
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const registrationBody = {
      deviceId: "fwd_fedcba9876543210fedcba9876543210",
      deviceName: "Relay Test Mac",
      publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
      schemaVersion: DEVICE_REGISTRATION_SCHEMA,
    } as const;
    const registration = await createSignedEnvelope(
      keyPair.privateKey,
      registrationBody,
      1,
      "registration_fedcba9876543210",
      "nonce_registration_fedcba9876543210",
    );
    const registered = await workerFetch("https://gateway.example/pairing/register", {
      body: JSON.stringify(registration),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    const registrationResult = (await registered.json()) as Record<string, unknown>;
    const sessionId = String(registrationResult.sessionId);
    const session = env.DEVICE_SESSIONS.get(
      env.DEVICE_SESSIONS.idFromName(`foldweave-device-session:${sessionId}`),
    );
    const approval = await createSignedEnvelope(
      keyPair.privateKey,
      { intent: "approve_pairing", sessionId },
      2,
      "approval_fedcba9876543210",
      "nonce_approval_fedcba9876543210",
    );
    expect((await postJson(session, "/approve", approval)).status).toBe(200);
    const authorizedAt = Date.now();
    const authorizedScopes = [
      "foldweave.plan",
      "foldweave.review",
      "foldweave.execute",
    ];
    expect(
      (
        await postJson(session, "/oauth-authorized", {
          authorizedAt,
          scopes: authorizedScopes,
          sessionId,
        })
      ).status,
    ).toBe(200);

    const socketResponse = await session.fetch("https://foldweave.internal/websocket", {
      headers: { upgrade: "websocket" },
      method: "GET",
    });
    expect(socketResponse.status).toBe(101);
    const webSocket = socketResponse.webSocket!;
    webSocket.accept();
    const challenge = await nextSocketMessage(webSocket);
    expect(challenge.type).toBe("companion_challenge");
    const challengeResponse = await createSignedEnvelope(
      keyPair.privateKey,
      {
        challenge: String(challenge.challenge),
        sessionId,
        type: "challenge_response",
      },
      3,
      "challenge_fedcba9876543210",
      "nonce_challenge_fedcba9876543210",
    );
    webSocket.send(JSON.stringify(challengeResponse));
    await expect(nextSocketMessage(webSocket)).resolves.toMatchObject({
      type: "companion_ready",
    });

    const connectedStatusEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      {
        deviceId: registrationBody.deviceId,
        intent: "pairing_status",
        sessionId,
      },
      4,
      "status_connected_fedcba9876",
      "nonce_status_connected_fedcba9876",
    );
    const connectedStatus = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(connectedStatusEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(connectedStatus.json()).resolves.toMatchObject({
      authorized: true,
      connected: true,
      pairingState: "authorized",
    });

    const mcpBody = JSON.stringify({
      id: 1,
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        arguments: { job_id: "a".repeat(32) },
        name: "job_status",
      },
    });
    const bodyDigest = await sha256Hex(mcpBody);
    const requestId = "relay_fedcba9876543210";
    const relayHeaders = {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "x-foldweave-http-method": "POST",
    };
    const operation = await describeMcpOperation({
      body: mcpBody,
      bodyDigest,
      headers: relayHeaders,
    });
    const scopes = canonicalScopes(authorizedScopes);
    const relayInput = {
      body: mcpBody,
      bodyDigest,
      headers: relayHeaders,
      invocation: {
        authorizedAt,
        bodyDigest,
        channel: "chatgpt_hosted",
        deviceId: registrationBody.deviceId,
        jobId: "a".repeat(32),
        oauthGrantFingerprint: await oauthGrantFingerprint({
          authorizedAt,
          deviceId: registrationBody.deviceId,
          scopes,
          sessionId,
        }),
        operationDigest: operation.digest,
        requestId,
        schemaVersion: "foldweave-public-invocation-seed.v1",
        scopes,
        sessionId,
      },
      requestId,
    };
    const wrongDeviceRelay = await postJson(session, "/relay", {
      ...relayInput,
      invocation: {
        ...relayInput.invocation,
        deviceId: "fwd_" + "0".repeat(32),
      },
    });
    expect(wrongDeviceRelay.status).toBe(401);
    await expect(wrongDeviceRelay.json()).resolves.toMatchObject({
      error: "invocation_binding_invalid",
    });
    const firstRelay = postJson(session, "/relay", relayInput);
    const identicalRetry = postJson(session, "/relay", relayInput);
    const outbound = await nextSocketMessage(webSocket);
    expect(outbound).toMatchObject({
      body: mcpBody,
      invocation: {
        bodyDigest,
        channel: "chatgpt_hosted",
        deviceId: registrationBody.deviceId,
        jobId: "a".repeat(32),
        oauthGrantFingerprint: relayInput.invocation.oauthGrantFingerprint,
        operationDigest: operation.digest,
        requestId,
        revokedAt: null,
        schemaVersion: "foldweave-public-invocation.v1",
        scopes,
        sessionId,
      },
      requestId: relayInput.requestId,
      type: "mcp_request",
    });
    const outboundInvocation = outbound.invocation as Record<string, unknown>;
    expect(outboundInvocation.issuedAt).toBe(outbound.issuedAt);
    expect(outboundInvocation.expiresAt).toBe(outbound.expiresAt);
    expect(outboundInvocation.sequence).toBe(outbound.sequence);
    expect(outboundInvocation.nonce).toMatch(/^[A-Za-z0-9_-]{16,128}$/u);
    expect(outboundInvocation).not.toHaveProperty("capabilityId");
    expect(outboundInvocation).not.toHaveProperty("capabilityExpiresAt");
    expect(outboundInvocation).not.toHaveProperty("capability_id");
    expect(outboundInvocation).not.toHaveProperty("capability_expires_at");
    expect(JSON.stringify(outbound)).not.toContain("fwjc_");
    const responseBody = '{"jsonrpc":"2.0","id":1,"result":{"tools":[]}}';
    const encodedResponse = await gzipBase64Url(responseBody);
    const responseEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      {
        body: encodedResponse.body,
        bodyDigest: await sha256Hex(responseBody),
        bodyEncoding: "gzip+base64url",
        compressedSize: encodedResponse.compressedSize,
        decodedSize: new TextEncoder().encode(responseBody).byteLength,
        headers: { "content-type": "application/json" },
        requestId: relayInput.requestId,
        schemaVersion: "foldweave-mcp-response-envelope.v1",
        status: 200,
        type: "mcp_response",
      },
      5,
      relayInput.requestId,
      "nonce_response_fedcba9876543210",
    );
    webSocket.send(JSON.stringify(responseEnvelope));
    const [firstResponse, retryResponse] = await Promise.all([
      firstRelay,
      identicalRetry,
    ]);
    expect(firstResponse.status).toBe(200);
    expect(retryResponse.status).toBe(200);
    await expect(firstResponse.json()).resolves.toMatchObject({
      requestId: relayInput.requestId,
      type: "mcp_response",
    });
    await expect(retryResponse.json()).resolves.toMatchObject({
      requestId: relayInput.requestId,
      type: "mcp_response",
    });
    webSocket.close(1000, "test complete");
  });

  it("reports device-bound authoritative status and rejects replay, wrong device, and bad signatures", async () => {
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const deviceId = "fwd_11111111111111111111111111111111";
    const registration = await createSignedEnvelope(
      keyPair.privateKey,
      {
        deviceId,
        deviceName: "Status Test Mac",
        publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
        schemaVersion: DEVICE_REGISTRATION_SCHEMA,
      },
      1,
      "registration_status_12345678",
      "nonce_registration_status_12345678",
    );
    const registered = await workerFetch("https://gateway.example/pairing/register", {
      body: JSON.stringify(registration),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    const result = (await registered.json()) as Record<string, unknown>;
    const sessionId = String(result.sessionId);
    const makeStatus = (sequence: number, requestId: string, requestDeviceId = deviceId) =>
      createSignedEnvelope(
        keyPair.privateKey,
        { deviceId: requestDeviceId, intent: "pairing_status", sessionId },
        sequence,
        requestId,
        `nonce_${requestId}`,
      );

    const pendingEnvelope = await makeStatus(2, "status_pending_1234567890");
    const pending = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(pendingEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(pending.status).toBe(200);
    await expect(pending.json()).resolves.toEqual({
      authorized: false,
      connected: false,
      deviceId,
      expiresAt: result.expiresAt,
      lastSeenAt: null,
      pairingState: "pending",
      requestId: "status_pending_1234567890",
      revoked: false,
      schemaVersion: "foldweave-pairing-status.v1",
      sessionId,
    });

    const replay = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(pendingEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(replay.status).toBe(409);
    await expect(replay.json()).resolves.toMatchObject({ error: "device_request_replayed" });

    const wrongDevice = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(
          await makeStatus(3, "status_wrong_device_123456", "fwd_22222222222222222222222222222222"),
        ),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(wrongDevice.status).toBe(401);
    await expect(wrongDevice.json()).resolves.toMatchObject({
      error: "pairing_status_binding_invalid",
    });

    const forged = await makeStatus(4, "status_forged_123456789012");
    forged.signature = `${String(forged.signature).startsWith("A") ? "B" : "A"}${String(forged.signature).slice(1)}`;
    const badSignature = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(forged),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(badSignature.status).toBe(401);
    await expect(badSignature.json()).resolves.toMatchObject({ error: "device_signature_invalid" });

    const expiredEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId },
      4,
      "status_expired_request_12345",
      "nonce_status_expired_request_12345",
      Date.now() - 180_000,
    );
    const expiredRequest = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(expiredEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(expiredRequest.status).toBe(401);
    await expect(expiredRequest.json()).resolves.toMatchObject({
      error: "device_signature_expired",
    });

    const wrongSessionEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId: "w".repeat(43) },
      4,
      "status_wrong_session_123456",
      "nonce_status_wrong_session_123456",
    );
    const wrongSession = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(wrongSessionEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(wrongSession.status).toBe(401);
    await expect(wrongSession.json()).resolves.toMatchObject({
      error: "pairing_status_binding_invalid",
    });
  });

  it("reports authorized, revoked, and expired states without treating local approval as OAuth", async () => {
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const deviceId = "fwd_33333333333333333333333333333333";
    const registration = await createSignedEnvelope(
      keyPair.privateKey,
      {
        deviceId,
        deviceName: "Authority Test Mac",
        publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
        schemaVersion: DEVICE_REGISTRATION_SCHEMA,
      },
      1,
      "registration_authority_12345",
      "nonce_registration_authority_12345",
    );
    const registered = await workerFetch("https://gateway.example/pairing/register", {
      body: JSON.stringify(registration),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    const result = (await registered.json()) as Record<string, unknown>;
    const sessionId = String(result.sessionId);
    const session = env.DEVICE_SESSIONS.get(
      env.DEVICE_SESSIONS.idFromName(`foldweave-device-session:${sessionId}`),
    );
    const approval = await createSignedEnvelope(
      keyPair.privateKey,
      { intent: "approve_pairing", sessionId },
      2,
      "approval_authority_12345678",
      "nonce_approval_authority_12345678",
    );
    expect((await postJson(session, "/approve", approval)).status).toBe(200);

    const localStatusEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId },
      3,
      "status_local_approved_123456",
      "nonce_status_local_approved_123456",
    );
    const localStatus = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(localStatusEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(localStatus.json()).resolves.toMatchObject({
      authorized: false,
      pairingState: "local_approved",
    });

    const socketResponse = await session.fetch("https://foldweave.internal/websocket", {
      headers: { upgrade: "websocket" },
      method: "GET",
    });
    const webSocket = socketResponse.webSocket!;
    webSocket.accept();
    const challenge = await nextSocketMessage(webSocket);
    webSocket.send(
      JSON.stringify(
        await createSignedEnvelope(
          keyPair.privateKey,
          {
            challenge: String(challenge.challenge),
            sessionId,
            type: "challenge_response",
          },
          4,
          "challenge_authority_1234567",
          "nonce_challenge_authority_1234567",
        ),
      ),
    );
    await expect(nextSocketMessage(webSocket)).resolves.toMatchObject({
      type: "companion_ready",
    });
    const connectedBeforeOAuthEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId },
      5,
      "status_connected_no_oauth_1234",
      "nonce_status_connected_no_oauth_1234",
    );
    const connectedBeforeOAuth = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(connectedBeforeOAuthEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(connectedBeforeOAuth.json()).resolves.toMatchObject({
      authorized: false,
      connected: true,
      pairingState: "local_approved",
    });

    expect(
      (
        await postJson(session, "/oauth-authorized", {
          authorizedAt: Date.now(),
          scopes: ["foldweave.plan", "foldweave.review", "foldweave.execute"],
          sessionId,
        })
      ).status,
    ).toBe(200);
    const authorizedEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId },
      6,
      "status_authorized_123456789",
      "nonce_status_authorized_123456789",
    );
    const authorized = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(authorizedEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(authorized.json()).resolves.toMatchObject({
      authorized: true,
      connected: true,
      pairingState: "authorized",
    });

    const revocation = await createSignedEnvelope(
      keyPair.privateKey,
      { intent: "revoke_pairing", sessionId },
      7,
      "revoke_authority_1234567890",
      "nonce_revoke_authority_1234567890",
    );
    expect((await postJson(session, "/revoke", revocation)).status).toBe(200);
    const revokedEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId },
      8,
      "status_revoked_12345678901",
      "nonce_status_revoked_12345678901",
    );
    const revoked = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(revokedEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(revoked.json()).resolves.toMatchObject({
      pairingState: "revoked",
      revoked: true,
    });

    const expiredSessionId = "expired_status_session_1234567890";
    const expiredSession = env.DEVICE_SESSIONS.get(
      env.DEVICE_SESSIONS.idFromName(`foldweave-device-session:${expiredSessionId}`),
    );
    const now = Date.now();
    expect(
      (
        await postJson(expiredSession, "/register", {
          activeCodeHash: "a".repeat(64),
          createdAt: now - 120_000,
          deviceId,
          deviceName: "Expired Test Mac",
          expiresAt: now - 60_000,
          initialNonceHash: "b".repeat(64),
          initialSequence: 1,
          publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
          sessionId: expiredSessionId,
        })
      ).status,
    ).toBe(200);
    const expiredEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      { deviceId, intent: "pairing_status", sessionId: expiredSessionId },
      2,
      "status_expired_12345678901",
      "nonce_status_expired_12345678901",
    );
    const expired = await workerFetch(
      `https://gateway.example/pairing/status?session=${expiredSessionId}`,
      {
        body: JSON.stringify(expiredEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(expired.json()).resolves.toMatchObject({
      authorized: false,
      pairingState: "expired",
      revoked: false,
    });
  });
});
