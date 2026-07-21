import { env, exports } from "cloudflare:workers";
import { beforeEach, describe, expect, it } from "vitest";

import {
  bytesToBase64Url,
  canonicalSha256,
  sha256Hex,
  type JsonValue,
} from "../src/canonical";
import {
  DEVICE_ENVELOPE_SCHEMA,
  DEVICE_REGISTRATION_SCHEMA,
  OAUTH_PROPS_SCHEMA,
} from "../src/constants";
import { signaturePayload } from "../src/device-crypto";
import { initializeDeviceSequenceDomains } from "../src/device-session";
import { McpApiHandler } from "../src/gateway";
import generatedOutputContract from "../src/generated/foldweave-public-mcp-output-contract.v1.json";
import {
  canonicalScopes,
  describeMcpOperation,
  oauthGrantFingerprint,
} from "../src/public-invocation";
import {
  PUBLIC_MCP_PATH,
  PUBLIC_TOOL_DESCRIPTORS,
  WIDGET_RESOURCE_COMPATIBILITY_URIS,
  WIDGET_RESOURCE_URI,
} from "../src/public-discovery";

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

function nextSocketClose(
  webSocket: WebSocket,
): Promise<{ code: number; reason: string; wasClean: boolean }> {
  return new Promise((resolve) => {
    const onClose = (event: CloseEvent) => {
      webSocket.removeEventListener("close", onClose);
      resolve({ code: event.code, reason: event.reason, wasClean: event.wasClean });
    };
    webSocket.addEventListener("close", onClose);
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

  it("discovers the bounded MCP surface before OAuth", async () => {
    const initialized = await workerFetch(`https://gateway.example${PUBLIC_MCP_PATH}`, {
      body: JSON.stringify({
        id: 1,
        jsonrpc: "2.0",
        method: "initialize",
        params: { protocolVersion: "2025-06-18" },
      }),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    expect(initialized.status).toBe(200);
    await expect(initialized.json()).resolves.toMatchObject({
      id: 1,
      jsonrpc: "2.0",
      result: {
        capabilities: {
          resources: { listChanged: false, subscribe: false },
          tools: { listChanged: false },
        },
        protocolVersion: "2025-06-18",
        serverInfo: { name: "Foldweave" },
      },
    });

    const listed = await workerFetch(`https://gateway.example${PUBLIC_MCP_PATH}`, {
      body: JSON.stringify({ id: "tools", jsonrpc: "2.0", method: "tools/list" }),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    expect(listed.status).toBe(200);
    const listing = (await listed.json()) as {
      result: { tools: Array<Record<string, unknown>> };
    };
    expect(listing.result.tools).toHaveLength(PUBLIC_TOOL_DESCRIPTORS.length);
    expect(new Set(listing.result.tools.map((tool) => tool.name))).toEqual(
      new Set(PUBLIC_TOOL_DESCRIPTORS.map((tool) => tool.name)),
    );
    const scopeByTool = Object.fromEntries(
      listing.result.tools.map((tool) => [
        String(tool.name),
        ((tool.securitySchemes as Array<{ scopes: string[] }>)[0]?.scopes ?? [])[0],
      ]),
    );
    expect(scopeByTool).toEqual({
      accept_plan_and_create_copy: "foldweave.execute",
      answer_clarification: "foldweave.plan",
      choose_local_item: "foldweave.plan",
      create_or_resume_planning_job: "foldweave.plan",
      get_change_file: "foldweave.review",
      get_compiler_failures: "foldweave.plan",
      get_plan_preview: "foldweave.review",
      inspect_markdown_links: "foldweave.plan",
      job_status: "foldweave.review",
      keep_previous_proposal: "foldweave.plan",
      list_inventory_page: "foldweave.plan",
      plan_change: "foldweave.plan",
      prepare_change_application: "foldweave.plan",
      read_text_excerpt: "foldweave.plan",
      recreate_original: "foldweave.execute",
      recover_revision: "foldweave.review",
      request_clarification: "foldweave.plan",
      revise_plan: "foldweave.plan",
      submit_compact_plan: "foldweave.plan",
      submit_plan: "foldweave.plan",
      submit_plan_revision: "foldweave.plan",
      verify_result: "foldweave.review",
    });
    for (const tool of listing.result.tools) {
      const schemes = tool.securitySchemes as Array<Record<string, unknown>>;
      const meta = tool._meta as Record<string, unknown>;
      expect(schemes).toHaveLength(1);
      expect(schemes[0]).toMatchObject({ type: "oauth2" });
      expect((schemes[0]?.scopes as unknown[])).toHaveLength(1);
      expect(meta.securitySchemes).toEqual(schemes);
      expect(tool.inputSchema).toMatchObject({
        additionalProperties: false,
        type: "object",
      });
      const family = generatedOutputContract.toolOutputFamily[
        String(tool.name) as keyof typeof generatedOutputContract.toolOutputFamily
      ];
      expect(family).toBeDefined();
      expect(tool.outputSchema).toEqual(
        generatedOutputContract.outputSchemaFamilies[
          family as keyof typeof generatedOutputContract.outputSchemaFamilies
        ],
      );
    }
    const previewTool = listing.result.tools.find(
      (tool) => tool.name === "get_plan_preview",
    );
    expect(previewTool?._meta).toMatchObject({
      "openai/outputTemplate": WIDGET_RESOURCE_URI,
      ui: { resourceUri: WIDGET_RESOURCE_URI },
    });
    const compactPlanTool = listing.result.tools.find(
      (tool) => tool.name === "submit_compact_plan",
    );
    expect(compactPlanTool?.inputSchema).toMatchObject({
      $defs: {
        FolderHostCompactPlanEntryV1: {
          additionalProperties: false,
          properties: {
            proposed_target: { maxLength: 1024, minLength: 1, type: "string" },
            relative_path: { maxLength: 4096, minLength: 1, type: "string" },
          },
          required: ["relative_path", "proposed_target"],
          type: "object",
        },
      },
    });
    expect(
      (
        compactPlanTool?.inputSchema as {
          $defs: { FolderHostCompactPlanEntryV1: { properties: object } };
        }
      ).$defs.FolderHostCompactPlanEntryV1.properties,
    ).not.toHaveProperty("file_id");
    const reviseTool = listing.result.tools.find(
      (tool) => tool.name === "revise_plan",
    );
    expect(reviseTool?._meta).toMatchObject({
      "openai/widgetAccessible": true,
      ui: { visibility: ["model", "app"] },
    });
    const recoverRevisionTool = listing.result.tools.find(
      (tool) => tool.name === "recover_revision",
    );
    expect(recoverRevisionTool).toMatchObject({
      annotations: {
        idempotentHint: true,
        readOnlyHint: true,
      },
      inputSchema: {
        additionalProperties: false,
        required: [
          "job_id",
          "parent_job_revision",
          "parent_candidate_fingerprint",
          "parent_preview_fingerprint",
          "source_commitment",
        ],
        type: "object",
      },
    });
    expect(recoverRevisionTool?._meta).toMatchObject({
      "openai/widgetAccessible": true,
      ui: { visibility: ["app"] },
    });
    const submitRevisionTool = listing.result.tools.find(
      (tool) => tool.name === "submit_plan_revision",
    );
    expect(submitRevisionTool?._meta).toMatchObject({
      ui: { visibility: ["model"] },
    });
    expect(submitRevisionTool?._meta).not.toHaveProperty(
      "openai/widgetAccessible",
    );
    const selectionTool = listing.result.tools.find(
      (tool) => tool.name === "choose_local_item",
    );
    expect(selectionTool?.inputSchema).toMatchObject({
      additionalProperties: false,
      properties: {
        selection_id: {
          anyOf: [
            { pattern: "^fwsel_[A-Za-z0-9_-]{43}$", type: "string" },
            { type: "null" },
          ],
          default: null,
        },
      },
      required: ["role"],
    });
    expect(String(selectionTool?.description)).toContain("poll this tool");
  });

  it("returns a per-tool OAuth challenge without invoking local work", async () => {
    const response = await workerFetch(`https://gateway.example${PUBLIC_MCP_PATH}`, {
      body: JSON.stringify({
        id: 2,
        jsonrpc: "2.0",
        method: "tools/call",
        params: { arguments: {}, name: "plan_change" },
      }),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toMatchObject({
      id: 2,
      jsonrpc: "2.0",
      result: {
        _meta: {
          "mcp/www_authenticate": [
            expect.stringMatching(
              /resource_metadata="https:\/\/gateway\.example\/\.well-known\/oauth-protected-resource\/mcp".*scope="foldweave\.plan".*error="insufficient_scope".*error_description="Connect ChatGPT to the paired Foldweave app to continue"/,
            ),
          ],
        },
        isError: true,
      },
    });
  });

  it("advertises the widget bootstrap without project state", async () => {
    const listed = await workerFetch(`https://gateway.example${PUBLIC_MCP_PATH}`, {
      body: JSON.stringify({ id: 3, jsonrpc: "2.0", method: "resources/list" }),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    const listedResource = (await listed.json()) as {
      result: { resources: Array<Record<string, unknown>> };
    };
    expect(listedResource).toMatchObject({
      result: {
        resources: [
          {
            mimeType: "text/html;profile=mcp-app",
            uri: WIDGET_RESOURCE_URI,
          },
        ],
      },
    });
    expect(listedResource.result.resources[0]?._meta).toMatchObject({
      "openai/widgetDomain": "https://gateway.example",
      ui: { domain: "https://gateway.example" },
    });
    const read = await workerFetch(`https://gateway.example${PUBLIC_MCP_PATH}`, {
      body: JSON.stringify({
        id: 4,
        jsonrpc: "2.0",
        method: "resources/read",
        params: { uri: WIDGET_RESOURCE_URI },
      }),
      headers: { "content-type": "application/json" },
      method: "POST",
    });
    const resource = (await read.json()) as {
      result: { contents: Array<Record<string, unknown>> };
    };
    expect(resource.result.contents[0]).toMatchObject({
      mimeType: "text/html;profile=mcp-app",
      uri: WIDGET_RESOURCE_URI,
    });
    expect(String(resource.result.contents[0]?.text)).toContain(
      'id="foldweave-chatgpt-widget-root"',
    );
    expect(String(resource.result.contents[0]?.text)).toContain(
      "https://gateway.example/foldweave-chatgpt-widget.js?asset=review-v37",
    );
    expect(resource.result.contents[0]?._meta).toMatchObject({
      "openai/widgetCSP": {
        connect_domains: [],
        resource_domains: ["https://gateway.example"],
      },
      "openai/widgetDomain": "https://gateway.example",
      ui: {
        csp: {
          connectDomains: [],
          resourceDomains: ["https://gateway.example"],
        },
        domain: "https://gateway.example",
      },
    });
    expect(JSON.stringify(resource)).not.toContain("/Users/");
    expect(JSON.stringify(resource)).not.toContain("fw_");

    for (const compatibilityUri of WIDGET_RESOURCE_COMPATIBILITY_URIS) {
      const compatibilityRead = await workerFetch(
        `https://gateway.example${PUBLIC_MCP_PATH}`,
        {
          body: JSON.stringify({
            id: `compatibility-${compatibilityUri}`,
            jsonrpc: "2.0",
            method: "resources/read",
            params: { uri: compatibilityUri },
          }),
          headers: { "content-type": "application/json" },
          method: "POST",
        },
      );
      const compatibilityResource = (await compatibilityRead.json()) as {
        result: { contents: Array<Record<string, unknown>> };
      };
      expect(compatibilityResource.result.contents[0]).toMatchObject({
        mimeType: "text/html;profile=mcp-app",
        uri: compatibilityUri,
      });
      expect(String(compatibilityResource.result.contents[0]?.text)).toContain(
        "https://gateway.example/foldweave-chatgpt-widget.js?asset=review-v37",
      );
    }
  });

  it("routes bearer traffic directly to the canonical OAuth-protected endpoint", async () => {
    const response = await workerFetch(`https://gateway.example${PUBLIC_MCP_PATH}`, {
      body: JSON.stringify({ id: 5, jsonrpc: "2.0", method: "tools/list" }),
      headers: {
        authorization: "Bearer invalid-test-token",
        "content-type": "application/json",
      },
      method: "POST",
      redirect: "manual",
    });
    expect(response.status).toBe(401);
    expect(response.headers.get("location")).toBeNull();
    expect(response.headers.get("www-authenticate")).toContain(
      `/.well-known/oauth-protected-resource${PUBLIC_MCP_PATH}`,
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
  it("serves stale widget compatibility resources through authenticated OAuth MCP", async () => {
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const deviceId = "fwd_31313131313131313131313131313131";
    const sessionId = "stale_widget_auth_session_1234567890";
    const now = Date.now();
    const session = env.DEVICE_SESSIONS.get(
      env.DEVICE_SESSIONS.idFromName(`foldweave-device-session:${sessionId}`),
    );
    expect(
      (
        await postJson(session, "/register", {
          activeCodeHash: "a".repeat(64),
          createdAt: now,
          deviceId,
          deviceName: "Stale Widget Compatibility Mac",
          expiresAt: now + 10 * 60 * 1000,
          initialNonceHash: "b".repeat(64),
          initialSequence: 1,
          publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
          sessionId,
        })
      ).status,
    ).toBe(200);
    const approval = await createSignedEnvelope(
      keyPair.privateKey,
      { intent: "approve_pairing", sessionId },
      2,
      "approval_stale_widget_compatibility",
      "nonce_approval_stale_widget_compatibility",
    );
    expect((await postJson(session, "/approve", approval)).status).toBe(200);
    const authorizedAt = Date.now();
    const scopes = canonicalScopes([
      "foldweave.plan",
      "foldweave.review",
      "foldweave.execute",
    ]);
    expect(
      (
        await postJson(session, "/oauth-authorized", {
          authorizedAt,
          scopes,
          sessionId,
        })
      ).status,
    ).toBe(200);

    const compatibilityUris = [
      "ui://foldweave/review-v31.html",
      "ui://foldweave/review-v32.html",
    ] as const;
    for (const uri of compatibilityUris) {
      expect(WIDGET_RESOURCE_COMPATIBILITY_URIS).toContain(uri);
      const response = await McpApiHandler.prototype.fetch.call(
        {
          ctx: {
            props: {
              authorizedAt,
              deviceId,
              schemaVersion: OAUTH_PROPS_SCHEMA,
              scopes,
              sessionId,
            },
          },
          env,
        } as unknown as McpApiHandler,
        new Request(`https://gateway.example${PUBLIC_MCP_PATH}`, {
          body: JSON.stringify({
            id: `authenticated-${uri}`,
            jsonrpc: "2.0",
            method: "resources/read",
            params: { uri },
          }),
          headers: { "content-type": "application/json" },
          method: "POST",
        }),
      );
      expect(response.status).toBe(200);
      const body = (await response.json()) as {
        result: { contents: Array<Record<string, unknown>> };
      };
      expect(body.result.contents[0]).toMatchObject({
        _meta: {
          "openai/widgetDomain": "https://gateway.example",
          ui: { domain: "https://gateway.example" },
        },
        mimeType: "text/html;profile=mcp-app",
        uri,
      });
      expect(String(body.result.contents[0]?.text)).toContain(
        "https://gateway.example/foldweave-chatgpt-widget.js?asset=review-v37",
      );
    }
  });

  it("seeds both sequence domains from a legacy combined checkpoint", () => {
    const legacy = { lastSequence: 17 };

    expect(initializeDeviceSequenceDomains(legacy)).toEqual({
      companion: 17,
      control: 17,
    });
    expect(legacy).toEqual({
      lastCompanionSequence: 17,
      lastControlSequence: 17,
      lastSequence: 17,
    });
  });

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
    const approvalResult = (await approved.json()) as Record<string, unknown>;
    expect(approvalResult.approved).toBe(true);
    expect(approvalResult.approvedAt).toEqual(expect.any(Number));
    expect(approvalResult.codeHash).toMatch(/^[a-f0-9]{64}$/u);
    expect(approvalResult.sessionId).toBe(result.sessionId);

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

  it("revokes stale OAuth grants across client registrations before issuing a new pairing", async () => {
    await workerFetch("https://gateway.example/healthz");
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const deviceId = "fwd_88888888888888888888888888888888";
    const userId = `device-${await sha256Hex(
      `foldweave-oauth-user.v1\u0000${deviceId}`,
    )}`;
    const scopes = [
      "foldweave.plan",
      "foldweave.review",
      "foldweave.execute",
    ];
    const oldSessions = [
      "stale_oauth_session_1111111111111111",
      "stale_oauth_session_2222222222222222",
    ];

    for (const [index, oldSessionId] of oldSessions.entries()) {
      const redirectUri = `https://chatgpt.com/connector/oauth/stale-${index}`;
      const client = await env.OAUTH_PROVIDER.createClient({
        clientName: `Stale ChatGPT app ${index}`,
        grantTypes: ["authorization_code", "refresh_token"],
        redirectUris: [redirectUri],
        responseTypes: ["code"],
        tokenEndpointAuthMethod: "none",
      });
      await env.OAUTH_PROVIDER.completeAuthorization({
        metadata: { deviceId, sessionId: oldSessionId },
        props: {
          authorizedAt: Date.now() + index,
          deviceId,
          schemaVersion: OAUTH_PROPS_SCHEMA,
          scopes,
          sessionId: oldSessionId,
        },
        request: {
          clientId: client.clientId,
          codeChallenge: "A".repeat(43),
          codeChallengeMethod: "S256",
          redirectUri,
          resource: "https://gateway.example/mcp",
          responseType: "code",
          scope: scopes,
          state: `stale-state-${index}`,
        },
        revokeExistingGrants: false,
        scope: scopes,
        userId,
      });
    }

    const before = await env.OAUTH_PROVIDER.listUserGrants(userId);
    expect(before.items).toHaveLength(2);
    expect(
      new Set(before.items.map((grant) => grant.metadata.sessionId)),
    ).toEqual(new Set(oldSessions));

    const registration = await createSignedEnvelope(
      keyPair.privateKey,
      {
        deviceId,
        deviceName: "Replacement Pairing Mac",
        publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
        schemaVersion: DEVICE_REGISTRATION_SCHEMA,
      },
      1,
      "registration_replaces_stale_oauth",
      "nonce_registration_replaces_stale_oauth",
    );
    const registered = await workerFetch(
      "https://gateway.example/pairing/register",
      {
        body: JSON.stringify(registration),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(registered.status).toBe(201);
    expect(
      (await env.OAUTH_PROVIDER.listUserGrants(userId)).items,
    ).toEqual([]);
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

    const codeIssuedStatus = await session.fetch(
      "https://foldweave.internal/status",
    );
    await expect(codeIssuedStatus.json()).resolves.toMatchObject({
      authorized: true,
      clientAccessObserved: false,
      clientAccessObservedAt: null,
    });
    const unsupportedStream = await McpApiHandler.prototype.fetch.call(
      {
        ctx: {
          props: {
            authorizedAt,
            deviceId: registrationBody.deviceId,
            schemaVersion: OAUTH_PROPS_SCHEMA,
            scopes: authorizedScopes,
            sessionId,
          },
        },
        env,
      } as unknown as McpApiHandler,
      new Request(`https://gateway.example${PUBLIC_MCP_PATH}`, {
        headers: { accept: "text/event-stream" },
        method: "GET",
      }),
    );
    expect(unsupportedStream.status).toBe(405);
    expect(unsupportedStream.headers.get("allow")).toBe("POST, DELETE");
    expect(unsupportedStream.headers.get("cache-control")).toBe("no-store");
    await expect(unsupportedStream.text()).resolves.toBe("");
    await expect(
      (await session.fetch("https://foldweave.internal/status")).json(),
    ).resolves.toMatchObject({ clientAccessObserved: false });
    const invalidAuthenticatedResponse = await McpApiHandler.prototype.fetch.call(
      {
        ctx: {
          props: {
            authorizedAt,
            deviceId: registrationBody.deviceId,
            schemaVersion: OAUTH_PROPS_SCHEMA,
            scopes: authorizedScopes,
            sessionId,
          },
        },
        env,
      } as unknown as McpApiHandler,
      new Request(`https://gateway.example${PUBLIC_MCP_PATH}`, {
        body: JSON.stringify({
          id: "invalid-client-access",
          jsonrpc: "2.0",
          method: "tools/call",
          params: { arguments: {}, name: "job_status" },
        }),
        headers: { "content-type": "application/json" },
        method: "POST",
      }),
    );
    expect(invalidAuthenticatedResponse.status).toBe(400);
    await expect(
      (await session.fetch("https://foldweave.internal/status")).json(),
    ).resolves.toMatchObject({ clientAccessObserved: false });
    const authenticatedWidgetResource = await McpApiHandler.prototype.fetch.call(
      {
        ctx: {
          props: {
            authorizedAt,
            deviceId: registrationBody.deviceId,
            schemaVersion: OAUTH_PROPS_SCHEMA,
            scopes: authorizedScopes,
            sessionId,
          },
        },
        env,
      } as unknown as McpApiHandler,
      new Request(`https://gateway.example${PUBLIC_MCP_PATH}`, {
        body: JSON.stringify({
          id: "authenticated-widget-resource",
          jsonrpc: "2.0",
          method: "resources/read",
          params: { uri: WIDGET_RESOURCE_URI },
        }),
        headers: { "content-type": "application/json" },
        method: "POST",
      }),
    );
    expect(authenticatedWidgetResource.status).toBe(200);
    const authenticatedWidgetBody = (await authenticatedWidgetResource.json()) as {
      result: { contents: Array<Record<string, unknown>> };
    };
    expect(authenticatedWidgetBody.result.contents[0]).toMatchObject({
      _meta: {
        "openai/widgetDomain": "https://gateway.example",
        ui: { domain: "https://gateway.example" },
      },
      mimeType: "text/html;profile=mcp-app",
      uri: WIDGET_RESOURCE_URI,
    });
    expect(String(authenticatedWidgetBody.result.contents[0]?.text)).toContain(
      "https://gateway.example/foldweave-chatgpt-widget.js?asset=review-v37",
    );
    const authenticatedInitializedNotification =
      await McpApiHandler.prototype.fetch.call(
        {
          ctx: {
            props: {
              authorizedAt,
              deviceId: registrationBody.deviceId,
              schemaVersion: OAUTH_PROPS_SCHEMA,
              scopes: authorizedScopes,
              sessionId,
            },
          },
          env,
        } as unknown as McpApiHandler,
        new Request(`https://gateway.example${PUBLIC_MCP_PATH}`, {
          body: JSON.stringify({
            jsonrpc: "2.0",
            method: "notifications/initialized",
          }),
          headers: { "content-type": "application/json" },
          method: "POST",
        }),
      );
    expect(authenticatedInitializedNotification.status).toBe(202);
    await expect(authenticatedInitializedNotification.text()).resolves.toBe("");
    const authenticatedRequest = new Request(
      `https://gateway.example${PUBLIC_MCP_PATH}`,
      {
        body: JSON.stringify({
          id: "first-client-access",
          jsonrpc: "2.0",
          method: "tools/call",
          params: {
            arguments: { job_id: "a".repeat(32) },
            name: "job_status",
          },
        }),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    const authenticatedResponse = await McpApiHandler.prototype.fetch.call(
      {
        ctx: {
          props: {
            authorizedAt,
            deviceId: registrationBody.deviceId,
            schemaVersion: OAUTH_PROPS_SCHEMA,
            scopes: authorizedScopes,
            sessionId,
          },
        },
        env,
      } as unknown as McpApiHandler,
      authenticatedRequest,
    );
    expect(authenticatedResponse.status).toBe(503);
    const observedStatus = await session.fetch("https://foldweave.internal/status");
    const observedStatusBody = (await observedStatus.json()) as Record<
      string,
      unknown
    >;
    expect(observedStatusBody).toMatchObject({
      authorized: true,
      clientAccessObserved: true,
    });
    expect(observedStatusBody.clientAccessObservedAt).toEqual(expect.any(Number));
    const firstObservedAt = observedStatusBody.clientAccessObservedAt;
    const repeatedObservation = await postJson(
      session,
      "/client-access-observed",
      {
        authorizedAt,
        deviceId: registrationBody.deviceId,
        scopes: authorizedScopes,
        sessionId,
      },
    );
    await expect(repeatedObservation.json()).resolves.toEqual({
      clientAccessObserved: true,
      clientAccessObservedAt: firstObservedAt,
    });

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
      2,
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
      50,
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
      authorizationCodeIssued: true,
      clientAccessObserved: true,
      connected: true,
      pairingState: "client_access_observed",
    });

    const challengerResponse = await session.fetch(
      "https://foldweave.internal/websocket",
      {
        headers: { upgrade: "websocket" },
        method: "GET",
      },
    );
    expect(challengerResponse.status).toBe(101);
    const challengerSocket = challengerResponse.webSocket!;
    challengerSocket.accept();
    const challengerChallenge = await nextSocketMessage(challengerSocket);
    expect(challengerChallenge).toMatchObject({ type: "companion_challenge" });

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
      3,
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
    const challengerProof = await createSignedEnvelope(
      keyPair.privateKey,
      {
        challenge: String(challengerChallenge.challenge),
        sessionId,
        type: "challenge_response",
      },
      4,
      "challenge_replacement_123456",
      "nonce_challenge_replacement_123456",
    );
    challengerSocket.send(JSON.stringify(challengerProof));
    await expect(nextSocketMessage(challengerSocket)).resolves.toMatchObject({
      type: "companion_ready",
    });
    const replacementStatusEnvelope = await createSignedEnvelope(
      keyPair.privateKey,
      {
        deviceId: registrationBody.deviceId,
        intent: "pairing_status",
        sessionId,
      },
      51,
      "status_replacement_123456789",
      "nonce_status_replacement_123456789",
    );
    const replacementStatus = await workerFetch(
      `https://gateway.example/pairing/status?session=${sessionId}`,
      {
        body: JSON.stringify(replacementStatusEnvelope),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    await expect(replacementStatus.json()).resolves.toMatchObject({
      authorizationCodeIssued: true,
      clientAccessObserved: true,
      connected: true,
      pairingState: "client_access_observed",
    });
    const replayedResponseSequence = await createSignedEnvelope(
      keyPair.privateKey,
      responseEnvelope.body!,
      3,
      relayInput.requestId,
      "nonce_response_replay_fedcba9876",
    );
    challengerSocket.send(JSON.stringify(replayedResponseSequence));
    await expect(nextSocketMessage(challengerSocket)).resolves.toMatchObject({
      error: "device_request_replayed",
      type: "companion_error",
    });
    challengerSocket.close(1000, "test complete");
    webSocket.close(1000, "test complete");
  });

  it("keeps the socket open for persisted duplicate responses and closes unknown responses", async () => {
    const keyPair = (await crypto.subtle.generateKey(
      { name: "Ed25519" },
      true,
      ["sign", "verify"],
    )) as CryptoKeyPair;
    const exported = await crypto.subtle.exportKey("jwk", keyPair.publicKey);
    const deviceId = "fwd_44444444444444444444444444444444";
    const sessionId = "late_response_session_0123456789abcdef";
    const now = Date.now();
    const session = env.DEVICE_SESSIONS.get(
      env.DEVICE_SESSIONS.idFromName(`foldweave-device-session:${sessionId}`),
    );
    expect(
      (
        await postJson(session, "/register", {
          activeCodeHash: "a".repeat(64),
          createdAt: now,
          deviceId,
          deviceName: "Late Response Test Mac",
          expiresAt: now + 10 * 60 * 1000,
          initialNonceHash: "b".repeat(64),
          initialSequence: 1,
          publicKeyJwk: { crv: "Ed25519", kty: "OKP", x: exported.x! },
          sessionId,
        })
      ).status,
    ).toBe(200);
    const approval = await createSignedEnvelope(
      keyPair.privateKey,
      { intent: "approve_pairing", sessionId },
      2,
      "approval_late_response_123456",
      "nonce_approval_late_response_123456",
    );
    expect((await postJson(session, "/approve", approval)).status).toBe(200);
    const authorizedAt = Date.now();
    const scopes = canonicalScopes([
      "foldweave.plan",
      "foldweave.review",
      "foldweave.execute",
    ]);
    expect(
      (
        await postJson(session, "/oauth-authorized", {
          authorizedAt,
          scopes,
          sessionId,
        })
      ).status,
    ).toBe(200);

    const socketResponse = await session.fetch(
      "https://foldweave.internal/websocket",
      {
        headers: { upgrade: "websocket" },
        method: "GET",
      },
    );
    expect(socketResponse.status).toBe(101);
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
          2,
          "challenge_late_response_12345",
          "nonce_challenge_late_response_12345",
        ),
      ),
    );
    await expect(nextSocketMessage(webSocket)).resolves.toMatchObject({
      type: "companion_ready",
    });
    let controlSequence = 3;
    const readPublicStatus = async (label: string) => {
      const sequence = controlSequence;
      controlSequence += 1;
      const statusResponse = await postJson(
        session,
        "/public-status",
        await createSignedEnvelope(
          keyPair.privateKey,
          { deviceId, intent: "pairing_status", sessionId },
          sequence,
          `status_late_${label}_${sequence}_request`,
          `nonce_status_late_${label}_${sequence}_request`,
        ),
      );
      expect(statusResponse.status).toBe(200);
      return (await statusResponse.json()) as Record<string, unknown>;
    };

    const relayHeaders = {
      accept: "application/json, text/event-stream",
      "content-type": "application/json",
      "x-foldweave-http-method": "POST",
    };
    const grantFingerprint = await oauthGrantFingerprint({
      authorizedAt,
      deviceId,
      scopes,
      sessionId,
    });
    const makeRelayInput = async (
      requestId: string,
      jsonRpcId: number,
      jobId: string,
    ) => {
      const body = JSON.stringify({
        id: jsonRpcId,
        jsonrpc: "2.0",
        method: "tools/call",
        params: {
          arguments: { job_id: jobId },
          name: "job_status",
        },
      });
      const bodyDigest = await sha256Hex(body);
      const operation = await describeMcpOperation({
        body,
        bodyDigest,
        headers: relayHeaders,
      });
      return {
        body,
        bodyDigest,
        headers: relayHeaders,
        invocation: {
          authorizedAt,
          bodyDigest,
          channel: "chatgpt_hosted",
          deviceId,
          jobId,
          oauthGrantFingerprint: grantFingerprint,
          operationDigest: operation.digest,
          requestId,
          schemaVersion: "foldweave-public-invocation-seed.v1",
          scopes,
          sessionId,
        },
        requestId,
      } as const;
    };
    const makeResponseEnvelope = async (
      requestId: string,
      sequence: number,
      nonce: string,
      jsonRpcId: number,
    ) => {
      const responseBody = JSON.stringify({
        id: jsonRpcId,
        jsonrpc: "2.0",
        result: { connected: true },
      });
      const encoded = await gzipBase64Url(responseBody);
      return createSignedEnvelope(
        keyPair.privateKey,
        {
          body: encoded.body,
          bodyDigest: await sha256Hex(responseBody),
          bodyEncoding: "gzip+base64url",
          compressedSize: encoded.compressedSize,
          decodedSize: new TextEncoder().encode(responseBody).byteLength,
          headers: { "content-type": "application/json" },
          requestId,
          schemaVersion: "foldweave-mcp-response-envelope.v1",
          status: 200,
          type: "mcp_response",
        },
        sequence,
        requestId,
        nonce,
      );
    };

    const firstRequestId = "relay_late_known_0123456789";
    const firstInput = await makeRelayInput(
      firstRequestId,
      1,
      "c".repeat(32),
    );
    const firstOutboundPromise = nextSocketMessage(webSocket);
    const firstRelay = postJson(session, "/relay", firstInput);
    await expect(firstOutboundPromise).resolves.toMatchObject({
      requestId: firstRequestId,
      type: "mcp_request",
    });
    const firstResponse = await makeResponseEnvelope(
      firstRequestId,
      3,
      "nonce_late_response_first_123456",
      1,
    );
    webSocket.send(JSON.stringify(firstResponse));
    expect((await firstRelay).status).toBe(200);

    const statusBeforeDuplicate = await readPublicStatus("before");
    const lastSeenBeforeDuplicate = Number(statusBeforeDuplicate.lastSeenAt);
    await new Promise((resolve) => setTimeout(resolve, 5));
    const duplicateResponse = await makeResponseEnvelope(
      firstRequestId,
      4,
      "nonce_late_response_duplicate_123",
      1,
    );
    webSocket.send(JSON.stringify(duplicateResponse));
    let lastSeenAfterDuplicate = lastSeenBeforeDuplicate;
    for (let attempt = 0; attempt < 20; attempt += 1) {
      const status = await readPublicStatus(`after_${attempt}`);
      lastSeenAfterDuplicate = Number(status.lastSeenAt);
      if (lastSeenAfterDuplicate > lastSeenBeforeDuplicate) {
        break;
      }
      await new Promise((resolve) => setTimeout(resolve, 5));
    }
    expect(lastSeenAfterDuplicate).toBeGreaterThan(lastSeenBeforeDuplicate);

    const secondRequestId = "relay_after_late_0123456789";
    const secondInput = await makeRelayInput(
      secondRequestId,
      2,
      "d".repeat(32),
    );
    const secondOutboundPromise = nextSocketMessage(webSocket);
    const secondRelay = postJson(session, "/relay", secondInput);
    await expect(secondOutboundPromise).resolves.toMatchObject({
      requestId: secondRequestId,
      type: "mcp_request",
    });
    webSocket.send(
      JSON.stringify(
        await makeResponseEnvelope(
          secondRequestId,
          5,
          "nonce_after_late_response_123456",
          2,
        ),
      ),
    );
    const secondRelayResponse = await secondRelay;
    expect(secondRelayResponse.status).toBe(200);
    await expect(secondRelayResponse.json()).resolves.toMatchObject({
      requestId: secondRequestId,
      type: "mcp_response",
    });

    const unknownRequestId = "relay_never_issued_0123456789";
    const errorMessage = nextSocketMessage(webSocket);
    const closeEvent = nextSocketClose(webSocket);
    webSocket.send(
      JSON.stringify(
        await makeResponseEnvelope(
          unknownRequestId,
          6,
          "nonce_unknown_response_123456789",
          3,
        ),
      ),
    );
    await expect(errorMessage).resolves.toMatchObject({
      error: "rpc_response_unexpected",
      type: "companion_error",
    });
    await expect(closeEvent).resolves.toMatchObject({
      code: 1008,
      reason: "Invalid companion message",
    });
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
      authorizationCodeIssued: false,
      clientAccessObserved: false,
      clientAccessObservedAt: null,
      connected: false,
      deviceId,
      expiresAt: result.expiresAt,
      lastSeenAt: null,
      pairingState: "pending",
      requestId: "status_pending_1234567890",
      revoked: false,
      schemaVersion: "foldweave-pairing-status.v2",
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
      authorizationCodeIssued: false,
      clientAccessObserved: false,
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
      authorizationCodeIssued: false,
      clientAccessObserved: false,
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
      authorizationCodeIssued: true,
      clientAccessObserved: false,
      connected: true,
      pairingState: "authorization_code_issued",
    });

    const revocation = await createSignedEnvelope(
      keyPair.privateKey,
      { intent: "revoke_pairing", sessionId },
      7,
      "revoke_authority_1234567890",
      "nonce_revoke_authority_1234567890",
    );
    const revocationResponse = await workerFetch(
      `https://gateway.example/pairing/revoke?session=${sessionId}`,
      {
        body: JSON.stringify(revocation),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    expect(revocationResponse.status).toBe(200);
    await expect(revocationResponse.json()).resolves.toEqual({
      codeHash: expect.stringMatching(/^[a-f0-9]{64}$/u),
      deviceId,
      revoked: true,
      revokedAt: expect.any(Number),
      sessionId,
    });
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
      authorizationCodeIssued: false,
      clientAccessObserved: false,
      pairingState: "expired",
      revoked: false,
    });
  });
});
