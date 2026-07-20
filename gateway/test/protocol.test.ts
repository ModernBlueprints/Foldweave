import { describe, expect, it, vi } from "vitest";

import type { JsonValue } from "../src/canonical";
import { extractRegistrationEnvelope, validateClientRegistration } from "../src/gateway";
import { verifyDeviceEnvelope } from "../src/device-crypto";
import {
  authorizedSessionExpiresAt,
  PendingRelayRegistry,
  sessionIsActiveAt,
} from "../src/device-session";
import {
  canonicalScopes,
  describeMcpOperation,
  oauthGrantFingerprint,
  parsePublicInvocationSeed,
  requireInvocationScope,
} from "../src/public-invocation";

const PYTHON_COMPANION_VECTOR = {
  envelope: {
    body: {
      deviceId: "fwd_0123456789abcdef0123456789abcdef",
      deviceName: "Foldweave Test Mac",
      publicKeyJwk: {
        crv: "Ed25519",
        kty: "OKP",
        x: "ebVWLo_mVPlAeLES6KmLp5AfhTrmlb7X4OORC60ElmQ",
      },
      schemaVersion: "foldweave-device-registration.v1",
    },
    bodyDigest: "03cc10430c445056d7012ae1f94667c9517256b342fac0954d92d21c3a63738c",
    expiresAt: 2_000_000_300_000,
    issuedAt: 2_000_000_000_000,
    nonce: "nonce_0123456789abcdef0123456789abcdef",
    requestId: "request_0123456789abcdef0123456789abcdef",
    schemaVersion: "foldweave-device-envelope.v1",
    sequence: 1,
    signature:
      "ul5iSl9IS4Diz_q2qXbd25Hhdm7emjsd9AV4Kkm-KQ0uLYzMDGq42Sk-s9UCxP-c-fJFtRguDKKBHEREl0wpBg",
  },
  publicKeyJwk: {
    crv: "Ed25519",
    kty: "OKP",
    x: "ebVWLo_mVPlAeLES6KmLp5AfhTrmlb7X4OORC60ElmQ",
  },
} as const;

describe("Python companion interoperability", () => {
  it("accepts the deterministic Python-produced Ed25519 envelope", async () => {
    const envelope = extractRegistrationEnvelope(PYTHON_COMPANION_VECTOR.envelope);
    await expect(
      verifyDeviceEnvelope(
        envelope,
        PYTHON_COMPANION_VECTOR.publicKeyJwk,
        2_000_000_001_000,
      ),
    ).resolves.toBeUndefined();
  });

  it("rejects a body changed after Python signed it", async () => {
    const changed = structuredClone(PYTHON_COMPANION_VECTOR.envelope) as unknown as Record<
      string,
      JsonValue
    >;
    (changed.body as Record<string, JsonValue>).deviceName = "Changed";
    expect(() => extractRegistrationEnvelope(changed)).not.toThrow();
    const envelope = extractRegistrationEnvelope(changed);
    await expect(
      verifyDeviceEnvelope(
        envelope,
        PYTHON_COMPANION_VECTOR.publicKeyJwk,
        2_000_000_001_000,
      ),
    ).rejects.toThrow(/digest does not match/u);
  });
});

describe("dynamic client registration policy", () => {
  it("accepts public PKCE clients with HTTPS redirects", () => {
    expect(
      validateClientRegistration({
        clientMetadata: {
          redirect_uris: ["https://chatgpt.com/connector/oauth/callback"],
          token_endpoint_auth_method: "none",
        },
        request: new Request("https://gateway.example/oauth/register"),
      }),
    ).toBeUndefined();
  });

  it("rejects credentialed clients and unsafe redirects", () => {
    expect(
      validateClientRegistration({
        clientMetadata: {
          redirect_uris: ["http://public.example/callback"],
          token_endpoint_auth_method: "client_secret_post",
        },
        request: new Request("https://gateway.example/oauth/register"),
      }),
    ).toMatchObject({ status: 400 });
  });
});

describe("authorized device-session lifetime", () => {
  it("expires the code-era session at ten minutes but keeps an authorized grant for thirty days", () => {
    const start = 2_000_000_000_000;
    vi.useFakeTimers();
    try {
      vi.setSystemTime(start);
      const pairingOnly = { expiresAt: start + 10 * 60 * 1000, revokedAt: null };
      expect(sessionIsActiveAt(pairingOnly)).toBe(true);
      vi.setSystemTime(start + 10 * 60 * 1000 + 1);
      expect(sessionIsActiveAt(pairingOnly)).toBe(false);

      const authorized = {
        expiresAt: authorizedSessionExpiresAt(start),
        revokedAt: null,
      };
      vi.setSystemTime(start + 31 * 60 * 1000);
      expect(sessionIsActiveAt(authorized)).toBe(true);
      vi.setSystemTime(authorized.expiresAt);
      expect(sessionIsActiveAt(authorized)).toBe(false);
      expect(sessionIsActiveAt({ ...authorized, revokedAt: start + 1 }, start + 2)).toBe(
        false,
      );
    } finally {
      vi.useRealTimers();
    }
  });
});

describe("concurrent relay retries", () => {
  it("coalesces identical concurrent retries onto one pending response", async () => {
    const registry = new PendingRelayRegistry();
    const first = registry.begin("request_0123456789", "a".repeat(64), 10_000);
    const retry = registry.begin("request_0123456789", "a".repeat(64), 10_000);
    expect(first.created).toBe(true);
    expect(retry.created).toBe(false);
    expect(retry.promise).toBe(first.promise);
    const response = {
      body: "H4sIAAAAAAACAwMAAAAAAAAAAAA",
      bodyDigest: "b".repeat(64),
      bodyEncoding: "gzip+base64url" as const,
      compressedSize: 20,
      decodedSize: 0,
      headers: { "content-type": "application/json" },
      requestId: "request_0123456789",
      schemaVersion: "foldweave-mcp-response-envelope.v1" as const,
      status: 200,
      type: "mcp_response" as const,
    };
    expect(registry.resolve("request_0123456789", response)).toBe(true);
    await expect(Promise.all([first.promise, retry.promise])).resolves.toEqual([
      response,
      response,
    ]);
  });

  it("blocks conflicting content under the same request identifier", () => {
    const registry = new PendingRelayRegistry();
    const first = registry.begin("request_abcdef012345", "a".repeat(64), 10_000);
    expect(() =>
      registry.begin("request_abcdef012345", "b".repeat(64), 10_000),
    ).toThrow(/reused for different relay content/u);
    registry.cancel("request_abcdef012345", new Error("test cleanup"));
    void first.promise.catch(() => undefined);
  });
});

describe("trusted public invocation authority", () => {
  it("canonicalizes the OAuth grant and binds the exact MCP operation", async () => {
    const body = JSON.stringify({
      id: 1,
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        arguments: {
          job_id: "a".repeat(32),
        },
        name: "accept_plan_and_create_copy",
      },
    });
    const bodyDigest = await crypto.subtle.digest(
      "SHA-256",
      new TextEncoder().encode(body),
    );
    const bodyDigestHex = Array.from(new Uint8Array(bodyDigest), (byte) =>
      byte.toString(16).padStart(2, "0"),
    ).join("");
    const operation = await describeMcpOperation({
      body,
      bodyDigest: bodyDigestHex,
      headers: {
        "mcp-session-id": "mcp-session-1",
        "x-foldweave-http-method": "POST",
      },
    });
    expect(operation.requiredScope).toBe("foldweave.execute");
    expect(operation.descriptor.jobId).toBe("a".repeat(32));
    expect(bodyDigestHex).toBe(
      "43413ebccc99358a3df383b31f65272f028c073a9147339ee3c8f572de46f0e8",
    );
    expect(operation.digest).toBe(
      "aaeb4e431ee0f8c93ede6e1bf34c9683891d5edc35d0ac9b73472c6dedb5b3ac",
    );

    const scopes = canonicalScopes([
      "foldweave.review",
      "foldweave.execute",
      "foldweave.plan",
    ]);
    expect(scopes).toEqual([
      "foldweave.execute",
      "foldweave.plan",
      "foldweave.review",
    ]);
    await expect(
      oauthGrantFingerprint({
        authorizedAt: 2_000_000_000_000,
        deviceId: "fwd_" + "a".repeat(32),
        scopes,
        sessionId: "s".repeat(43),
      }),
    ).resolves.toBe(
      "c34ba69706c2484d3b430d1377685c77c21d536d79b3a0a85f7acd29f812e98d",
    );
  });

  it("rejects a tool when the OAuth grant lacks its required scope", async () => {
    const body = JSON.stringify({
      id: 1,
      jsonrpc: "2.0",
      method: "tools/call",
      params: {
        arguments: {
          job_id: "a".repeat(32),
        },
        name: "accept_plan_and_create_copy",
      },
    });
    const operation = await describeMcpOperation({
      body,
      bodyDigest: "a".repeat(64),
      headers: { "x-foldweave-http-method": "POST" },
    });
    expect(() =>
      requireInvocationScope(["foldweave.review"], operation.requiredScope),
    ).toThrow(/does not authorize/u);
  });

  it("requires only a job identifier for job-bound tools and rejects client capabilities", async () => {
    const bodyFor = (name: string, argumentsValue: Record<string, unknown>) =>
      JSON.stringify({
        id: 1,
        jsonrpc: "2.0",
        method: "tools/call",
        params: { arguments: argumentsValue, name },
      });
    await expect(
      describeMcpOperation({
        body: bodyFor("job_status", { job_id: "a".repeat(32) }),
        bodyDigest: "a".repeat(64),
        headers: {},
      }),
    ).resolves.toMatchObject({
      descriptor: { jobId: "a".repeat(32) },
    });
    await expect(
      describeMcpOperation({
        body: bodyFor("job_status", {}),
        bodyDigest: "a".repeat(64),
        headers: {},
      }),
    ).rejects.toMatchObject({ code: "mcp_public_job_binding_required" });
    await expect(
      describeMcpOperation({
        body: bodyFor("choose_local_item", {
          job_id: "a".repeat(32),
          role: "source_folder",
        }),
        bodyDigest: "a".repeat(64),
        headers: {},
      }),
    ).rejects.toMatchObject({ code: "mcp_public_job_binding_unexpected" });
    for (const forbidden of [
      { capability_id: "fwjc_" + "C".repeat(86), job_id: "a".repeat(32) },
      { capability_expires_at: 5_800_000, job_id: "a".repeat(32) },
    ]) {
      await expect(
        describeMcpOperation({
          body: bodyFor("job_status", forbidden),
          bodyDigest: "a".repeat(64),
          headers: {},
        }),
      ).rejects.toMatchObject({ code: "mcp_public_capability_forbidden" });
    }
  });

  it("parses a nullable job binding and rejects legacy capability fields", () => {
    const base = {
      authorizedAt: 5_000_000,
      bodyDigest: "a".repeat(64),
      channel: "chatgpt_hosted",
      deviceId: "fwd_" + "d".repeat(32),
      jobId: null,
      oauthGrantFingerprint: "b".repeat(64),
      operationDigest: "c".repeat(64),
      requestId: "request_0123456789",
      schemaVersion: "foldweave-public-invocation-seed.v1",
      scopes: ["foldweave.review"],
      sessionId: "s".repeat(43),
    };
    expect(parsePublicInvocationSeed(base)).toMatchObject({ jobId: null });
    const jobBound = parsePublicInvocationSeed({
      ...base,
      jobId: "a".repeat(32),
    });
    expect(jobBound).toMatchObject({ jobId: "a".repeat(32) });
    expect(JSON.stringify(jobBound)).not.toContain("fwjc_");
    expect(jobBound).not.toHaveProperty("capabilityId");
    expect(jobBound).not.toHaveProperty("capabilityExpiresAt");
    expect(() =>
      parsePublicInvocationSeed({
        ...base,
        capabilityId: "fwjc_" + "C".repeat(86),
      }),
    ).toThrow(/unsupported or missing fields/u);
  });
});
