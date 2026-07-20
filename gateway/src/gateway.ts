import type {
  AuthRequest,
  ClientInfo,
  ClientRegistrationCallbackOptions,
  ClientRegistrationCallbackResult,
} from "@cloudflare/workers-oauth-provider";
import { WorkerEntrypoint } from "cloudflare:workers";

import {
  MAX_CONTROL_BODY_BYTES,
  MAX_MCP_BODY_BYTES,
  OAUTH_PROPS_SCHEMA,
  PAIRING_CODE_TTL_MS,
  SUPPORTED_SCOPES,
} from "./constants";
import {
  bytesToBase64Url,
  canonicalJson,
  constantTimeEqual,
  sha256Hex,
  type JsonValue,
} from "./canonical";
import {
  isPlainRecord,
  normalizePairingCode,
  parseRegistrationBody,
  parseScopeList,
  parseSignedEnvelope,
  requireDeviceId,
  requireExactKeys,
  requireSessionId,
  requireSha256,
  type SignedDeviceEnvelope,
} from "./contracts";
import { verifyDeviceEnvelope } from "./device-crypto";
import type { Env, OAuthProps } from "./env";
import {
  errorResponse,
  HttpError,
  jsonResponse,
  readJsonBody,
  requireMethod,
  securityHeaders,
} from "./http";
import { generatePairingCode } from "./pairing-code";
import {
  decodeCompanionRpcResponse,
  parseCompanionRpcResponseEnvelope,
} from "./response-codec";
import {
  canonicalScopes,
  describeMcpOperation,
  oauthGrantFingerprint,
  requireInvocationScope,
  type PublicInvocationSeed,
} from "./public-invocation";

const DIRECTORY_NAME = "foldweave-pairing-directory-v1";
const MCP_REQUEST_HEADER_ALLOWLIST = new Set([
  "accept",
  "content-type",
  "last-event-id",
  "mcp-protocol-version",
  "mcp-session-id",
]);

interface SessionStatus {
  active: boolean;
  authorized: boolean;
  codeHash: string;
  deviceId: string;
  exists: true;
  expiresAt: number;
  localApproved: boolean;
  revoked: boolean;
  scopes: string[];
  sessionId: string;
}

function directoryStub(env: Env): DurableObjectStub {
  return env.PAIRING_DIRECTORY.get(env.PAIRING_DIRECTORY.idFromName(DIRECTORY_NAME));
}

function deviceSessionStub(env: Env, sessionId: string): DurableObjectStub {
  return env.DEVICE_SESSIONS.get(
    env.DEVICE_SESSIONS.idFromName(`foldweave-device-session:${sessionId}`),
  );
}

function randomOpaqueId(byteLength = 32): string {
  return bytesToBase64Url(crypto.getRandomValues(new Uint8Array(byteLength)));
}

function htmlEscape(value: string): string {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function oauthUserId(deviceId: string): Promise<string> {
  return sha256Hex(`foldweave-oauth-user.v1\u0000${deviceId}`).then(
    (digest) => `device-${digest}`,
  );
}

function requireSecureRequest(request: Request): void {
  const url = new URL(request.url);
  const isLoopback = url.hostname === "localhost" || url.hostname === "127.0.0.1";
  if (url.protocol !== "https:" && !isLoopback) {
    throw new HttpError(400, "https_required", "HTTPS is required.");
  }
}

async function responseJson(response: Response): Promise<Record<string, unknown>> {
  const value = (await response.json()) as unknown;
  if (!isPlainRecord(value)) {
    throw new HttpError(502, "internal_response_invalid", "Gateway state response is invalid.");
  }
  return value;
}

async function requireSessionStatus(
  env: Env,
  sessionId: string,
): Promise<SessionStatus> {
  const response = await deviceSessionStub(env, sessionId).fetch(
    "https://foldweave.internal/status",
  );
  const value = await responseJson(response);
  if (
    !response.ok ||
    value.exists !== true ||
    typeof value.active !== "boolean" ||
    typeof value.authorized !== "boolean" ||
    typeof value.localApproved !== "boolean" ||
    typeof value.revoked !== "boolean" ||
    !Array.isArray(value.scopes)
  ) {
    throw new HttpError(401, "session_inactive", "Pairing session is not active.");
  }
  return value as unknown as SessionStatus;
}

function clientDisplayName(client: ClientInfo | null): string {
  if (client?.clientName && client.clientName.length <= 100) {
    return client.clientName;
  }
  return "ChatGPT";
}

function renderAuthorizationPage(
  request: Request,
  oauthRequest: AuthRequest,
  client: ClientInfo | null,
  csrfToken: string,
  errorMessage?: string,
): Response {
  const url = new URL(request.url);
  const scopes = oauthRequest.scope.length > 0 ? oauthRequest.scope : [...SUPPORTED_SCOPES];
  const error = errorMessage
    ? `<p class="error" role="alert">${htmlEscape(errorMessage)}</p>`
    : "";
  const scopeItems = scopes
    .map((scope) => `<li>${htmlEscape(scope)}</li>`)
    .join("");
  const body = `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Pair Foldweave</title>
  <style>
    :root{color-scheme:dark;font-family:ui-sans-serif,system-ui,sans-serif;background:#071426;color:#e7f7ff}
    body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px}
    main{width:min(520px,100%);box-sizing:border-box;border:1px solid #1f6380;border-radius:16px;background:#0b1c31;padding:28px;box-shadow:0 20px 70px #0008}
    h1{font-size:1.65rem;margin:0 0 8px}p{color:#b8cad8;line-height:1.5}label{display:block;font-weight:700;margin:22px 0 8px}
    input{width:100%;box-sizing:border-box;border:1px solid #3d7897;border-radius:9px;background:#071426;color:#fff;padding:13px;font:inherit;letter-spacing:.12em;text-transform:uppercase}
    button{width:100%;margin-top:18px;border:0;border-radius:9px;background:#38c8ff;color:#05101c;padding:13px;font:inherit;font-weight:800;cursor:pointer}
    ul{color:#b8cad8}.error{border-left:3px solid #ffb454;padding-left:12px;color:#ffd6a4}.muted{font-size:.88rem}
  </style>
</head>
<body>
  <main>
    <h1>Pair Foldweave with ${htmlEscape(clientDisplayName(client))}</h1>
    <p>Enter the ten-character code shown by your local Foldweave companion. Confirm the pairing locally before continuing.</p>
    ${error}
    <form method="post" action="${htmlEscape(url.pathname + url.search)}">
      <input type="hidden" name="csrf" value="${htmlEscape(csrfToken)}">
      <label for="pairing-code">Pairing code</label>
      <input id="pairing-code" name="pairing_code" inputmode="text" autocomplete="one-time-code" minlength="10" maxlength="12" required autofocus>
      <button type="submit">Authorize Foldweave</button>
    </form>
    <p class="muted">Requested permissions:</p>
    <ul>${scopeItems}</ul>
    <p class="muted">No local path, project payload, API key, or planning excerpt is sent to this authorization page.</p>
  </main>
</body>
</html>`;
  const headers = securityHeaders(new Headers({ "content-type": "text/html; charset=utf-8" }));
  headers.append(
    "set-cookie",
    `__Host-fw_oauth_csrf=${csrfToken}; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=600`,
  );
  return new Response(body, { headers });
}

function readCookie(request: Request, name: string): string | null {
  const cookies = request.headers.get("cookie")?.split(";") ?? [];
  for (const cookie of cookies) {
    const [key, ...parts] = cookie.trim().split("=");
    if (key === name) {
      return parts.join("=");
    }
  }
  return null;
}

async function readAuthorizationForm(
  request: Request,
): Promise<{ csrf: string; pairingCode: string }> {
  const contentType = request.headers.get("content-type")?.split(";", 1)[0]?.trim();
  if (contentType !== "application/x-www-form-urlencoded") {
    throw new HttpError(415, "content_type_invalid", "Expected a form submission.");
  }
  const declaredLength = request.headers.get("content-length");
  if (declaredLength !== null && Number(declaredLength) > MAX_CONTROL_BODY_BYTES) {
    throw new HttpError(413, "request_too_large", "Form is too large.");
  }
  const bytes = new Uint8Array(await request.arrayBuffer());
  if (bytes.byteLength > MAX_CONTROL_BODY_BYTES) {
    throw new HttpError(413, "request_too_large", "Form is too large.");
  }
  const form = new URLSearchParams(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  const keys: string[] = [];
  form.forEach((_value, key) => keys.push(key));
  keys.sort();
  if (keys.length !== 2 || keys[0] !== "csrf" || keys[1] !== "pairing_code") {
    throw new HttpError(400, "authorization_form_invalid", "Authorization form is invalid.");
  }
  const csrf = form.get("csrf");
  const pairingCode = form.get("pairing_code");
  if (csrf === null || pairingCode === null) {
    throw new HttpError(400, "authorization_form_invalid", "Authorization form is invalid.");
  }
  return { csrf, pairingCode };
}

async function handleRegistration(request: Request, env: Env): Promise<Response> {
  requireSecureRequest(request);
  requireMethod(request, "POST");
  const parsed = await readJsonBody(request);
  const envelope = parseSignedEnvelope(parsed, (body) =>
    parseRegistrationBody(body) as unknown as JsonValue,
  );
  const registration = envelope.body as unknown as ReturnType<typeof parseRegistrationBody>;
  await verifyDeviceEnvelope(envelope, registration.publicKeyJwk);
  const initialNonceHash = await sha256Hex(envelope.nonce);

  for (let attempt = 0; attempt < 3; attempt += 1) {
    const now = Date.now();
    const sessionId = randomOpaqueId();
    const pairingCode = generatePairingCode();
    const codeHash = await sha256Hex(pairingCode);
    const expiresAt = now + PAIRING_CODE_TTL_MS;
    const sessionResponse = await deviceSessionStub(env, sessionId).fetch(
      "https://foldweave.internal/register",
      {
        body: JSON.stringify({
          activeCodeHash: codeHash,
          createdAt: now,
          deviceId: registration.deviceId,
          deviceName: registration.deviceName,
          expiresAt,
          initialNonceHash,
          initialSequence: envelope.sequence,
          publicKeyJwk: registration.publicKeyJwk,
          sessionId,
        }),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    if (!sessionResponse.ok) {
      continue;
    }
    const directoryResponse = await directoryStub(env).fetch(
      "https://foldweave.internal/register",
      {
        body: JSON.stringify({ codeHash, expiresAt, sessionId }),
        headers: { "content-type": "application/json" },
        method: "POST",
      },
    );
    if (directoryResponse.ok) {
      return jsonResponse(
        {
          expiresAt,
          pairingCode,
          sessionId,
        },
        { status: 201 },
      );
    }
  }
  throw new HttpError(503, "pairing_registration_failed", "Could not allocate a pairing code.");
}

async function handleApproval(request: Request, env: Env): Promise<Response> {
  requireSecureRequest(request);
  requireMethod(request, "POST");
  const url = new URL(request.url);
  const sessionId = requireSessionId(url.searchParams.get("session"));
  const bodyBytes = await request.arrayBuffer();
  if (bodyBytes.byteLength > MAX_CONTROL_BODY_BYTES) {
    throw new HttpError(413, "request_too_large", "Request body is too large.");
  }
  const sessionResponse = await deviceSessionStub(env, sessionId).fetch(
    "https://foldweave.internal/approve",
    {
      body: bodyBytes,
      headers: { "content-type": request.headers.get("content-type") ?? "" },
      method: "POST",
    },
  );
  if (!sessionResponse.ok) {
    return sessionResponse;
  }
  const result = await responseJson(sessionResponse);
  const codeHash = requireSha256(result.codeHash, "code_hash");
  const approvedAt = Number(result.approvedAt);
  const directoryResponse = await directoryStub(env).fetch(
    "https://foldweave.internal/approve",
    {
      body: JSON.stringify({ approvedAt, codeHash, sessionId }),
      headers: { "content-type": "application/json" },
      method: "POST",
    },
  );
  if (!directoryResponse.ok) {
    return directoryResponse;
  }
  return jsonResponse({ approved: true });
}

async function revokeOAuthGrants(env: Env, deviceId: string): Promise<void> {
  const userId = await oauthUserId(deviceId);
  let cursor: string | undefined;
  const grantIds: string[] = [];
  do {
    const page = await env.OAUTH_PROVIDER.listUserGrants(userId, { cursor, limit: 100 });
    for (const grant of page.items) {
      grantIds.push(grant.id);
    }
    cursor = page.cursor;
  } while (cursor !== undefined);
  for (const grantId of grantIds) {
    await env.OAUTH_PROVIDER.revokeGrant(grantId, userId);
  }
}

async function handleRevocation(request: Request, env: Env): Promise<Response> {
  requireSecureRequest(request);
  requireMethod(request, "POST");
  const url = new URL(request.url);
  const sessionId = requireSessionId(url.searchParams.get("session"));
  const bodyBytes = await request.arrayBuffer();
  if (bodyBytes.byteLength > MAX_CONTROL_BODY_BYTES) {
    throw new HttpError(413, "request_too_large", "Request body is too large.");
  }
  const sessionResponse = await deviceSessionStub(env, sessionId).fetch(
    "https://foldweave.internal/revoke",
    {
      body: bodyBytes,
      headers: { "content-type": request.headers.get("content-type") ?? "" },
      method: "POST",
    },
  );
  if (!sessionResponse.ok) {
    return sessionResponse;
  }
  const result = await responseJson(sessionResponse);
  const codeHash = requireSha256(result.codeHash, "code_hash");
  const deviceId = requireDeviceId(result.deviceId);
  const revokedAt = Number(result.revokedAt);
  await directoryStub(env).fetch("https://foldweave.internal/revoke", {
    body: JSON.stringify({ codeHash, revokedAt, sessionId }),
    headers: { "content-type": "application/json" },
    method: "POST",
  });
  await revokeOAuthGrants(env, deviceId);
  return jsonResponse({ revoked: true });
}

async function handlePairingStatus(request: Request, env: Env): Promise<Response> {
  requireSecureRequest(request);
  requireMethod(request, "POST");
  const sessionId = requireSessionId(new URL(request.url).searchParams.get("session"));
  const bodyBytes = await request.arrayBuffer();
  if (bodyBytes.byteLength > MAX_CONTROL_BODY_BYTES) {
    throw new HttpError(413, "request_too_large", "Request body is too large.");
  }
  return deviceSessionStub(env, sessionId).fetch(
    "https://foldweave.internal/public-status",
    {
      body: bodyBytes,
      headers: { "content-type": request.headers.get("content-type") ?? "" },
      method: "POST",
    },
  );
}

async function handleCompanionSocket(request: Request, env: Env): Promise<Response> {
  requireSecureRequest(request);
  requireMethod(request, "GET");
  const sessionId = requireSessionId(new URL(request.url).searchParams.get("session"));
  return deviceSessionStub(env, sessionId).fetch(
    new Request("https://foldweave.internal/websocket", {
      headers: request.headers,
      method: "GET",
    }),
  );
}

async function handleAuthorize(request: Request, env: Env): Promise<Response> {
  requireSecureRequest(request);
  const oauthRequest = await env.OAUTH_PROVIDER.parseAuthRequest(
    new Request(request.url, { headers: request.headers, method: "GET" }),
  );
  if (oauthRequest.responseType !== "code" || oauthRequest.codeChallengeMethod !== "S256") {
    throw new HttpError(400, "oauth_request_invalid", "Authorization requires code flow with PKCE S256.");
  }
  const unsupportedScope = oauthRequest.scope.find(
    (scope) => !SUPPORTED_SCOPES.includes(scope as (typeof SUPPORTED_SCOPES)[number]),
  );
  if (unsupportedScope !== undefined) {
    throw new HttpError(400, "oauth_scope_invalid", "Authorization requested an unsupported scope.");
  }
  const client = await env.OAUTH_PROVIDER.lookupClient(oauthRequest.clientId);
  if (request.method === "GET") {
    const csrfToken = randomOpaqueId(24);
    return renderAuthorizationPage(request, oauthRequest, client, csrfToken);
  }
  requireMethod(request, "POST");
  const { csrf, pairingCode: rawPairingCode } = await readAuthorizationForm(request);
  const csrfCookie = readCookie(request, "__Host-fw_oauth_csrf");
  if (csrfCookie === null || !constantTimeEqual(csrf, csrfCookie)) {
    throw new HttpError(403, "authorization_csrf_invalid", "Authorization form expired. Start again.");
  }
  const pairingCode = normalizePairingCode(rawPairingCode);
  const codeHash = await sha256Hex(pairingCode);
  const sourceIp = request.headers.get("cf-connecting-ip") ?? "unavailable";
  const ipHash = await sha256Hex(`foldweave-pairing-ip.v1\u0000${sourceIp}`);
  const attemptedAt = Date.now();
  const directoryResponse = await directoryStub(env).fetch(
    "https://foldweave.internal/authorize",
    {
      body: JSON.stringify({ attemptedAt, codeHash, ipHash }),
      headers: { "content-type": "application/json" },
      method: "POST",
    },
  );
  if (!directoryResponse.ok) {
    const csrfToken = randomOpaqueId(24);
    return renderAuthorizationPage(
      request,
      oauthRequest,
      client,
      csrfToken,
      directoryResponse.status === 429
        ? "Pairing attempts are temporarily limited. Generate a new code and try later."
        : "The code is invalid, expired, already used, or not yet confirmed locally.",
    );
  }
  const directoryResult = await responseJson(directoryResponse);
  const sessionId = requireSessionId(directoryResult.sessionId);
  const status = await requireSessionStatus(env, sessionId);
  if (!status.active || !status.localApproved || status.authorized || status.codeHash !== codeHash) {
    throw new HttpError(409, "pairing_state_invalid", "Pairing session cannot be authorized.");
  }
  const scopes = parseScopeList(
    oauthRequest.scope.length > 0 ? oauthRequest.scope : [...SUPPORTED_SCOPES],
  );
  const authorizedAt = Date.now();
  const userId = await oauthUserId(status.deviceId);
  const { redirectTo } = await env.OAUTH_PROVIDER.completeAuthorization({
    metadata: {
      deviceId: status.deviceId,
      sessionId,
    },
    props: {
      authorizedAt,
      deviceId: status.deviceId,
      schemaVersion: OAUTH_PROPS_SCHEMA,
      scopes,
      sessionId,
    } satisfies OAuthProps,
    request: oauthRequest,
    scope: scopes,
    userId,
  });
  const authorizedResponse = await deviceSessionStub(env, sessionId).fetch(
    "https://foldweave.internal/oauth-authorized",
    {
      body: JSON.stringify({ authorizedAt, scopes, sessionId }),
      headers: { "content-type": "application/json" },
      method: "POST",
    },
  );
  if (!authorizedResponse.ok) {
    throw new HttpError(409, "pairing_state_invalid", "Pairing session could not be finalized.");
  }
  const headers = securityHeaders(new Headers({ location: redirectTo }));
  headers.append(
    "set-cookie",
    "__Host-fw_oauth_csrf=; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=0",
  );
  return new Response(null, { headers, status: 302 });
}

function validateOAuthProps(value: unknown): OAuthProps {
  if (!isPlainRecord(value)) {
    throw new HttpError(401, "oauth_props_invalid", "OAuth authorization is invalid.");
  }
  requireExactKeys(
    value,
    ["authorizedAt", "deviceId", "schemaVersion", "scopes", "sessionId"],
    "oauth_props",
  );
  if (value.schemaVersion !== OAUTH_PROPS_SCHEMA || !Number.isSafeInteger(value.authorizedAt)) {
    throw new HttpError(401, "oauth_props_invalid", "OAuth authorization is invalid.");
  }
  return {
    authorizedAt: Number(value.authorizedAt),
    deviceId: requireDeviceId(value.deviceId),
    schemaVersion: OAUTH_PROPS_SCHEMA,
    scopes: parseScopeList(value.scopes),
    sessionId: requireSessionId(value.sessionId),
  };
}

function mcpError(
  request: Request,
  status: number,
  code: number,
  message: string,
): Response {
  const requestId = (() => {
    try {
      const value = JSON.parse(request.headers.get("x-foldweave-jsonrpc-id") ?? "null") as JsonValue;
      return value;
    } catch {
      return null;
    }
  })();
  return jsonResponse(
    { error: { code, message }, id: requestId, jsonrpc: "2.0" },
    { status },
  );
}

export class McpApiHandler extends WorkerEntrypoint<Env, OAuthProps> {
  public override async fetch(request: Request): Promise<Response> {
    try {
      requireSecureRequest(request);
      const url = new URL(request.url);
      if (url.pathname !== "/mcp") {
        return jsonResponse({ error: "not_found" }, { status: 404 });
      }
      if (!["GET", "POST", "DELETE"].includes(request.method)) {
        throw new HttpError(405, "method_not_allowed", "Method not allowed.");
      }
      const props = validateOAuthProps(this.ctx.props);
      const status = await requireSessionStatus(this.env, props.sessionId);
      if (
        !status.active ||
        !status.authorized ||
        status.deviceId !== props.deviceId ||
        status.sessionId !== props.sessionId ||
        canonicalJson(canonicalScopes(status.scopes)) !==
          canonicalJson(canonicalScopes(props.scopes))
      ) {
        const resourceMetadata = `${url.origin}/.well-known/oauth-protected-resource`;
        const response = mcpError(request, 401, -32001, "Foldweave pairing is inactive or expired.");
        response.headers.set(
          "www-authenticate",
          `Bearer resource_metadata="${resourceMetadata}", scope="${SUPPORTED_SCOPES.join(" ")}"`,
        );
        return response;
      }
      const declaredLength = request.headers.get("content-length");
      if (declaredLength !== null && Number(declaredLength) > MAX_MCP_BODY_BYTES) {
        throw new HttpError(413, "request_too_large", "MCP request is too large.");
      }
      const bodyBytes = new Uint8Array(await request.arrayBuffer());
      if (bodyBytes.byteLength > MAX_MCP_BODY_BYTES) {
        throw new HttpError(413, "request_too_large", "MCP request is too large.");
      }
      const body = new TextDecoder("utf-8", { fatal: true }).decode(bodyBytes);
      const bodyDigest = await sha256Hex(body);
      const headers: Record<string, string> = {
        "x-foldweave-http-method": request.method,
      };
      request.headers.forEach((value, name) => {
        if (MCP_REQUEST_HEADER_ALLOWLIST.has(name.toLowerCase())) {
          headers[name.toLowerCase()] = value;
        }
      });
      const requestId = await sha256Hex(
        canonicalJson({
          bodyDigest,
          deviceId: props.deviceId,
          method: request.method,
          mcpSessionId: headers["mcp-session-id"] ?? null,
          schemaVersion: "foldweave-mcp-correlation.v1",
        }),
      );
      const scopes = canonicalScopes(props.scopes);
      const operation = await describeMcpOperation({ body, bodyDigest, headers });
      requireInvocationScope(scopes, operation.requiredScope);
      const invocation: PublicInvocationSeed = {
        authorizedAt: props.authorizedAt,
        bodyDigest,
        channel: "chatgpt_hosted",
        deviceId: props.deviceId,
        jobId: operation.descriptor.jobId,
        oauthGrantFingerprint: await oauthGrantFingerprint({
          authorizedAt: props.authorizedAt,
          deviceId: props.deviceId,
          scopes,
          sessionId: props.sessionId,
        }),
        operationDigest: operation.digest,
        requestId,
        schemaVersion: "foldweave-public-invocation-seed.v1",
        scopes,
        sessionId: props.sessionId,
      };
      const relayResponse = await deviceSessionStub(this.env, props.sessionId).fetch(
        "https://foldweave.internal/relay",
        {
          body: JSON.stringify({ body, bodyDigest, headers, invocation, requestId }),
          headers: { "content-type": "application/json" },
          method: "POST",
        },
      );
      const relay = await responseJson(relayResponse);
      if (!relayResponse.ok) {
        return mcpError(
          request,
          relayResponse.status,
          -32002,
          typeof relay.message === "string" ? relay.message : "Foldweave companion is unavailable.",
        );
      }
      const decoded = await decodeCompanionRpcResponse(
        parseCompanionRpcResponseEnvelope(relay),
      );
      const responseHeaders = new Headers();
      for (const [name, value] of Object.entries(decoded.headers)) {
        responseHeaders.set(name, value);
      }
      responseHeaders.set("cache-control", "no-store");
      return new Response(decoded.body, {
        headers: responseHeaders,
        status: decoded.status,
      });
    } catch (error) {
      if (error instanceof HttpError) {
        return mcpError(request, error.status, -32600, error.message);
      }
      return mcpError(request, 500, -32603, "The gateway could not complete the request.");
    }
  }
}

export const defaultHandler: ExportedHandler<Env> = {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      if (url.pathname === "/healthz") {
        requireMethod(request, "GET");
        return jsonResponse({
          bindings: {
            deviceSessions: env.DEVICE_SESSIONS !== undefined,
            oauthKv: env.OAUTH_KV !== undefined,
            pairingDirectory: env.PAIRING_DIRECTORY !== undefined,
          },
          ready: true,
          service: "foldweave-gateway",
        });
      }
      if (url.pathname === "/authorize") {
        return await handleAuthorize(request, env);
      }
      if (url.pathname === "/pairing/register") {
        return await handleRegistration(request, env);
      }
      if (url.pathname === "/pairing/approve") {
        return await handleApproval(request, env);
      }
      if (url.pathname === "/pairing/revoke") {
        return await handleRevocation(request, env);
      }
      if (url.pathname === "/pairing/status") {
        return await handlePairingStatus(request, env);
      }
      if (url.pathname === "/companion") {
        return await handleCompanionSocket(request, env);
      }
      return jsonResponse({ error: "not_found" }, { status: 404 });
    } catch (error) {
      return errorResponse(error);
    }
  },
};

function isValidRedirectUri(value: unknown): boolean {
  if (typeof value !== "string" || value.length > 2048) {
    return false;
  }
  try {
    const url = new URL(value);
    if (url.username !== "" || url.password !== "" || url.hash !== "") {
      return false;
    }
    if (url.protocol === "https:") {
      return true;
    }
    return (
      url.protocol === "http:" &&
      (url.hostname === "127.0.0.1" || url.hostname === "localhost")
    );
  } catch {
    return false;
  }
}

export function validateClientRegistration(
  options: ClientRegistrationCallbackOptions,
): ClientRegistrationCallbackResult | void {
  const metadata = options.clientMetadata;
  const redirectUris = metadata.redirect_uris;
  if (
    !Array.isArray(redirectUris) ||
    redirectUris.length === 0 ||
    redirectUris.length > 10 ||
    !redirectUris.every(isValidRedirectUri)
  ) {
    return {
      code: "invalid_redirect_uri",
      description: "redirect_uris must contain bounded HTTPS or loopback callback URLs.",
      status: 400,
    };
  }
  const authenticationMethod = metadata.token_endpoint_auth_method;
  if (authenticationMethod !== undefined && authenticationMethod !== "none") {
    return {
      code: "invalid_client_metadata",
      description: "Foldweave accepts public PKCE clients only.",
      status: 400,
    };
  }
  return undefined;
}

export function extractRegistrationEnvelope(
  value: unknown,
): SignedDeviceEnvelope<JsonValue> {
  return parseSignedEnvelope(value, (body) =>
    parseRegistrationBody(body) as unknown as JsonValue,
  );
}
