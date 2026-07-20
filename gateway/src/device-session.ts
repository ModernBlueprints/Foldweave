import {
  CAPABILITY_TTL_MS,
  COMPANION_CHALLENGE_TTL_MS,
  COMPANION_RPC_TIMEOUT_MS,
  DEVICE_AUTHORIZATION_TTL_MS,
  MAX_CONTROL_BODY_BYTES,
  MAX_MCP_BODY_BYTES,
  MAX_MCP_RESPONSE_WIRE_BYTES,
  MAX_RECENT_NONCES,
  MAX_RECENT_RELAYS,
  NONCE_RETENTION_MS,
} from "./constants";
import {
  bytesToBase64Url,
  canonicalSha256,
  sha256Hex,
  type JsonValue,
} from "./canonical";
import {
  isPlainRecord,
  parsePublicJwk,
  parseScopeList,
  parseSignedEnvelope,
  requireDeviceId,
  requireExactKeys,
  requireOpaqueId,
  requireSessionId,
  requireSha256,
  type CompanionChallengeBody,
  type CompanionRpcRequest,
  type CompanionRpcResponseEnvelope,
  type DeviceSessionRecord,
  type SignedDeviceEnvelope,
} from "./contracts";
import { verifyDeviceEnvelope } from "./device-crypto";
import type { Env } from "./env";
import { errorResponse, HttpError, jsonResponse, readJsonBody } from "./http";
import { parseCompanionRpcResponseEnvelope } from "./response-codec";
import {
  canonicalScopes,
  describeMcpOperation,
  oauthGrantFingerprint,
  parsePublicInvocationSeed,
  requireInvocationScope,
  type PublicInvocationSeed,
  type TrustedPublicInvocationContext,
} from "./public-invocation";

interface SocketAttachment {
  authenticated: boolean;
  challenge: string;
  challengeExpiresAt: number;
  deviceId: string;
  sessionId: string;
}

interface PendingRpc {
  fingerprint: string;
  promise: Promise<CompanionRpcResponseEnvelope>;
  reject: (error: Error) => void;
  resolve: (response: CompanionRpcResponseEnvelope) => void;
  timeout: ReturnType<typeof setTimeout>;
}

interface InternalRelayRequest {
  body: string;
  bodyDigest: string;
  headers: Record<string, string>;
  invocation: PublicInvocationSeed;
  requestId: string;
}

const SESSION_STORAGE_KEY = "device-session";
export class PendingRelayRegistry {
  private readonly entries = new Map<string, PendingRpc>();

  public begin(
    requestId: string,
    fingerprint: string,
    timeoutMs: number,
  ): {
    created: boolean;
    promise: Promise<CompanionRpcResponseEnvelope>;
  } {
    const existing = this.entries.get(requestId);
    if (existing !== undefined) {
      if (existing.fingerprint !== fingerprint) {
        throw new HttpError(
          409,
          "relay_request_conflict",
          "Request identifier was reused for different relay content.",
        );
      }
      return { created: false, promise: existing.promise };
    }
    let resolvePromise!: (response: CompanionRpcResponseEnvelope) => void;
    let rejectPromise!: (error: Error) => void;
    const promise = new Promise<CompanionRpcResponseEnvelope>((resolve, reject) => {
      resolvePromise = resolve;
      rejectPromise = reject;
    });
    const timeout = setTimeout(() => {
      this.entries.delete(requestId);
      rejectPromise(
        new HttpError(
          504,
          "companion_timeout",
          "Foldweave companion did not respond in time.",
        ),
      );
    }, timeoutMs);
    this.entries.set(requestId, {
      fingerprint,
      promise,
      reject: rejectPromise,
      resolve: resolvePromise,
      timeout,
    });
    return { created: true, promise };
  }

  public resolve(requestId: string, response: CompanionRpcResponseEnvelope): boolean {
    const pending = this.entries.get(requestId);
    if (pending === undefined) {
      return false;
    }
    clearTimeout(pending.timeout);
    this.entries.delete(requestId);
    pending.resolve(response);
    return true;
  }

  public cancel(requestId: string, error: Error): void {
    const pending = this.entries.get(requestId);
    if (pending === undefined) {
      return;
    }
    clearTimeout(pending.timeout);
    this.entries.delete(requestId);
    pending.reject(error);
  }

  public rejectAll(error: Error): void {
    for (const requestId of [...this.entries.keys()]) {
      this.cancel(requestId, error);
    }
  }
}

export function authorizedSessionExpiresAt(authorizedAt: number): number {
  return authorizedAt + DEVICE_AUTHORIZATION_TTL_MS;
}

export function sessionIsActiveAt(
  record: Pick<DeviceSessionRecord, "expiresAt" | "revokedAt">,
  now = Date.now(),
): boolean {
  return record.revokedAt === null && record.expiresAt > now;
}

function nowTimestamp(value: unknown, label: string): number {
  if (!Number.isSafeInteger(value) || Number(value) <= 0) {
    throw new HttpError(400, `${label}_invalid`, `${label} is invalid.`);
  }
  return Number(value);
}

function parseActionBody(
  value: unknown,
  expectedIntent: "approve_pairing" | "revoke_pairing",
): JsonValue {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "device_action_invalid", "Device action is invalid.");
  }
  requireExactKeys(value, ["intent", "sessionId"], "device_action");
  if (value.intent !== expectedIntent) {
    throw new HttpError(400, "device_action_invalid", "Device action intent is invalid.");
  }
  return { intent: expectedIntent, sessionId: requireSessionId(value.sessionId) };
}

function parseStatusBody(value: unknown): JsonValue {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "pairing_status_invalid", "Pairing status request is invalid.");
  }
  requireExactKeys(value, ["deviceId", "intent", "sessionId"], "pairing_status");
  if (value.intent !== "pairing_status") {
    throw new HttpError(400, "pairing_status_invalid", "Pairing status intent is invalid.");
  }
  return {
    deviceId: requireDeviceId(value.deviceId),
    intent: "pairing_status",
    sessionId: requireSessionId(value.sessionId),
  };
}

function parseChallengeBody(value: unknown): JsonValue {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "challenge_response_invalid", "Challenge response is invalid.");
  }
  requireExactKeys(value, ["challenge", "sessionId", "type"], "challenge_response");
  if (value.type !== "challenge_response") {
    throw new HttpError(400, "challenge_response_invalid", "Challenge response type is invalid.");
  }
  return {
    challenge: requireOpaqueId(value.challenge, "challenge"),
    sessionId: requireSessionId(value.sessionId),
    type: "challenge_response",
  } satisfies CompanionChallengeBody;
}

function parseInternalRelay(value: unknown): InternalRelayRequest {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "relay_request_invalid", "Relay request is invalid.");
  }
  requireExactKeys(
    value,
    ["body", "bodyDigest", "headers", "invocation", "requestId"],
    "relay_request",
  );
  if (typeof value.body !== "string" || new TextEncoder().encode(value.body).byteLength > MAX_MCP_BODY_BYTES) {
    throw new HttpError(413, "relay_request_too_large", "Relay request is too large.");
  }
  if (!isPlainRecord(value.headers)) {
    throw new HttpError(400, "relay_request_invalid", "Relay request headers are invalid.");
  }
  const headers: Record<string, string> = {};
  for (const [name, headerValue] of Object.entries(value.headers)) {
    if (typeof headerValue !== "string" || headerValue.length > 512 || /[\r\n]/u.test(headerValue)) {
      throw new HttpError(400, "relay_request_invalid", "Relay request headers are invalid.");
    }
    headers[name.toLowerCase()] = headerValue;
  }
  return {
    body: value.body,
    bodyDigest: requireSha256(value.bodyDigest, "body_digest"),
    headers,
    invocation: parsePublicInvocationSeed(value.invocation),
    requestId: requireOpaqueId(value.requestId, "request_id"),
  };
}

export class DeviceSession implements DurableObject {
  private readonly state: DurableObjectState;
  private readonly pending = new PendingRelayRegistry();

  public constructor(state: DurableObjectState, _env: Env) {
    this.state = state;
  }

  public async fetch(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      if (request.method === "POST" && url.pathname === "/register") {
        return await this.register(request);
      }
      if (request.method === "POST" && url.pathname === "/approve") {
        return await this.approve(request);
      }
      if (request.method === "POST" && url.pathname === "/oauth-authorized") {
        return await this.markAuthorized(request);
      }
      if (request.method === "POST" && url.pathname === "/revoke") {
        return await this.revoke(request);
      }
      if (request.method === "GET" && url.pathname === "/status") {
        return await this.status();
      }
      if (request.method === "POST" && url.pathname === "/public-status") {
        return await this.publicStatus(request);
      }
      if (request.method === "GET" && url.pathname === "/websocket") {
        return await this.openWebSocket(request);
      }
      if (request.method === "POST" && url.pathname === "/relay") {
        return await this.relay(request);
      }
      return jsonResponse({ error: "not_found" }, { status: 404 });
    } catch (error) {
      return errorResponse(error);
    }
  }

  public async webSocketMessage(webSocket: WebSocket, message: string | ArrayBuffer): Promise<void> {
    try {
      const text = typeof message === "string" ? message : new TextDecoder("utf-8", { fatal: true }).decode(message);
      if (new TextEncoder().encode(text).byteLength > MAX_MCP_RESPONSE_WIRE_BYTES) {
        throw new HttpError(413, "websocket_message_too_large", "Companion message is too large.");
      }
      const attachment = webSocket.deserializeAttachment() as SocketAttachment | null;
      if (attachment === null) {
        throw new HttpError(401, "companion_state_invalid", "Companion socket state is invalid.");
      }
      const parsed = JSON.parse(text) as unknown;
      const record = await this.requireRecord();
      if (!attachment.authenticated) {
        const envelope = parseSignedEnvelope(parsed, parseChallengeBody);
        await this.verifyAndAdvance(envelope, record);
        const body = envelope.body as unknown as CompanionChallengeBody;
        if (
          body.challenge !== attachment.challenge ||
          body.sessionId !== attachment.sessionId ||
          attachment.challengeExpiresAt <= Date.now()
        ) {
          throw new HttpError(401, "challenge_response_invalid", "Companion challenge response is invalid.");
        }
        attachment.authenticated = true;
        webSocket.serializeAttachment(attachment);
        webSocket.send(JSON.stringify({ type: "companion_ready", sessionId: record.sessionId }));
        return;
      }

      const envelope = parseSignedEnvelope(parsed, parseCompanionRpcResponseEnvelope);
      await this.verifyAndAdvance(envelope, record);
      const body = envelope.body as unknown as CompanionRpcResponseEnvelope;
      if (envelope.requestId !== body.requestId) {
        throw new HttpError(400, "rpc_response_invalid", "Companion response request binding is invalid.");
      }
      if (!this.pending.resolve(body.requestId, body)) {
        throw new HttpError(409, "rpc_response_unexpected", "Companion response is not expected.");
      }
    } catch (error) {
      const code = error instanceof HttpError ? error.code : "companion_message_invalid";
      webSocket.send(JSON.stringify({ error: code, type: "companion_error" }));
      webSocket.close(1008, "Invalid companion message");
    }
  }

  public webSocketClose(
    _webSocket: WebSocket,
    _code: number,
    _reason: string,
    _wasClean: boolean,
  ): void {
    this.rejectPending("Companion disconnected before responding.");
  }

  public webSocketError(_webSocket: WebSocket, _error: unknown): void {
    this.rejectPending("Companion transport failed before responding.");
  }

  private async register(request: Request): Promise<Response> {
    const body = await readJsonBody(request);
    if (!isPlainRecord(body)) {
      throw new HttpError(400, "session_registration_invalid", "Session registration is invalid.");
    }
    requireExactKeys(
      body,
      [
        "activeCodeHash",
        "createdAt",
        "deviceId",
        "deviceName",
        "expiresAt",
        "initialNonceHash",
        "initialSequence",
        "publicKeyJwk",
        "sessionId",
      ],
      "session_registration",
    );
    const createdAt = nowTimestamp(body.createdAt, "created_at");
    const expiresAt = nowTimestamp(body.expiresAt, "expires_at");
    const initialSequence = nowTimestamp(body.initialSequence, "initial_sequence");
    if (expiresAt <= createdAt) {
      throw new HttpError(400, "session_registration_invalid", "Session expiry is invalid.");
    }
    if (typeof body.deviceName !== "string" || body.deviceName.length === 0 || body.deviceName.length > 80) {
      throw new HttpError(400, "device_name_invalid", "Device name is invalid.");
    }
    const record: DeviceSessionRecord = {
      activeCodeHash: requireSha256(body.activeCodeHash, "active_code_hash"),
      authorizedAt: null,
      createdAt,
      deviceId: requireDeviceId(body.deviceId),
      deviceName: body.deviceName,
      expiresAt,
      lastRelaySequence: 0,
      lastSeenAt: null,
      lastSequence: initialSequence,
      localApprovedAt: null,
      publicKeyJwk: parsePublicJwk(body.publicKeyJwk),
      recentNonces: [
        {
          expiresAt: createdAt + NONCE_RETENTION_MS,
          hash: requireSha256(body.initialNonceHash, "initial_nonce_hash"),
        },
      ],
      recentRelays: [],
      revokedAt: null,
      scopes: [],
      sessionId: requireSessionId(body.sessionId),
    };
    const created = await this.state.storage.transaction(async (transaction) => {
      const existing = await transaction.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
      if (existing !== undefined) {
        return false;
      }
      await transaction.put(SESSION_STORAGE_KEY, record);
      return true;
    });
    if (!created) {
      throw new HttpError(409, "session_already_registered", "Session is already registered.");
    }
    return jsonResponse({ registered: true });
  }

  private async approve(request: Request): Promise<Response> {
    const parsed = await readJsonBody(request);
    const envelope = parseSignedEnvelope(parsed, (body) => parseActionBody(body, "approve_pairing"));
    const record = await this.requireRecord();
    await this.verifyAndAdvance(envelope, record);
    if ((envelope.body as Record<string, JsonValue>).sessionId !== record.sessionId) {
      throw new HttpError(401, "session_binding_invalid", "Signed request targets another session.");
    }
    const approvedAt = Date.now();
    await this.state.storage.transaction(async (transaction) => {
      const current = await transaction.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
      if (current === undefined || current.revokedAt !== null || current.expiresAt <= approvedAt) {
        throw new HttpError(409, "session_inactive", "Session is no longer active.");
      }
      current.localApprovedAt = approvedAt;
      await transaction.put(SESSION_STORAGE_KEY, current);
    });
    return jsonResponse({
      approved: true,
      approvedAt,
      codeHash: record.activeCodeHash,
      sessionId: record.sessionId,
    });
  }

  private async markAuthorized(request: Request): Promise<Response> {
    const body = await readJsonBody(request);
    if (!isPlainRecord(body)) {
      throw new HttpError(400, "oauth_authorization_invalid", "OAuth authorization is invalid.");
    }
    requireExactKeys(body, ["authorizedAt", "scopes", "sessionId"], "oauth_authorization");
    const sessionId = requireSessionId(body.sessionId);
    const authorizedAt = nowTimestamp(body.authorizedAt, "authorized_at");
    const scopes = parseScopeList(body.scopes);
    await this.state.storage.transaction(async (transaction) => {
      const record = await transaction.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
      if (
        record === undefined ||
        record.sessionId !== sessionId ||
        record.revokedAt !== null ||
        record.expiresAt <= authorizedAt ||
        record.localApprovedAt === null
      ) {
        throw new HttpError(409, "session_inactive", "Session cannot be authorized.");
      }
      record.authorizedAt = authorizedAt;
      record.expiresAt = authorizedSessionExpiresAt(authorizedAt);
      record.scopes = scopes;
      await transaction.put(SESSION_STORAGE_KEY, record);
    });
    return jsonResponse({ authorized: true });
  }

  private async revoke(request: Request): Promise<Response> {
    const parsed = await readJsonBody(request);
    const envelope = parseSignedEnvelope(parsed, (body) => parseActionBody(body, "revoke_pairing"));
    const record = await this.requireRecord();
    await this.verifyAndAdvance(envelope, record);
    if ((envelope.body as Record<string, JsonValue>).sessionId !== record.sessionId) {
      throw new HttpError(401, "session_binding_invalid", "Signed request targets another session.");
    }
    const revokedAt = Date.now();
    await this.state.storage.transaction(async (transaction) => {
      const current = await transaction.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
      if (current !== undefined) {
        current.revokedAt = revokedAt;
        await transaction.put(SESSION_STORAGE_KEY, current);
      }
    });
    for (const webSocket of this.state.getWebSockets("companion")) {
      webSocket.close(1008, "Pairing revoked");
    }
    this.rejectPending("Pairing was revoked.");
    return jsonResponse({
      codeHash: record.activeCodeHash,
      deviceId: record.deviceId,
      revoked: true,
      revokedAt,
      sessionId: record.sessionId,
    });
  }

  private async status(): Promise<Response> {
    const record = await this.state.storage.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
    if (record === undefined) {
      return jsonResponse({ exists: false });
    }
    const now = Date.now();
    return jsonResponse({
      active: sessionIsActiveAt(record, now),
      authorized: record.authorizedAt !== null,
      codeHash: record.activeCodeHash,
      deviceId: record.deviceId,
      exists: true,
      expiresAt: record.expiresAt,
      localApproved: record.localApprovedAt !== null,
      revoked: record.revokedAt !== null,
      scopes: record.scopes,
      sessionId: record.sessionId,
    });
  }

  private async publicStatus(request: Request): Promise<Response> {
    const parsed = await readJsonBody(request);
    const envelope = parseSignedEnvelope(parsed, parseStatusBody);
    const record = await this.requireRecord();
    await this.verifyAndAdvance(envelope, record, false, true);
    const body = envelope.body as Record<string, JsonValue>;
    if (
      body.sessionId !== record.sessionId ||
      body.deviceId !== record.deviceId
    ) {
      throw new HttpError(401, "pairing_status_binding_invalid", "Pairing status binding is invalid.");
    }
    const current = await this.requireRecord();
    const now = Date.now();
    const expired = current.expiresAt <= now;
    const connected =
      current.revokedAt === null &&
      !expired &&
      this.state.getWebSockets("companion").some((candidate) => {
        const attachment = candidate.deserializeAttachment() as SocketAttachment | null;
        return (
          attachment?.authenticated === true &&
          attachment.deviceId === current.deviceId &&
          attachment.sessionId === current.sessionId
        );
      });
    const pairingState = current.revokedAt !== null
      ? "revoked"
      : expired
        ? "expired"
        : current.authorizedAt !== null
          ? "authorized"
          : current.localApprovedAt !== null
            ? "local_approved"
            : "pending";
    return jsonResponse({
      authorized: current.authorizedAt !== null,
      connected,
      deviceId: current.deviceId,
      expiresAt: current.expiresAt,
      lastSeenAt: current.lastSeenAt ?? null,
      pairingState,
      requestId: envelope.requestId,
      revoked: current.revokedAt !== null,
      schemaVersion: "foldweave-pairing-status.v1",
      sessionId: current.sessionId,
    });
  }

  private async openWebSocket(request: Request): Promise<Response> {
    if (request.headers.get("upgrade")?.toLowerCase() !== "websocket") {
      throw new HttpError(426, "websocket_upgrade_required", "WebSocket upgrade is required.");
    }
    const record = await this.requireActiveRecord();
    for (const existing of this.state.getWebSockets("companion")) {
      existing.close(1012, "Companion reconnected");
    }
    const pair = new WebSocketPair();
    const client = pair[0];
    const server = pair[1];
    const challenge = bytesToBase64Url(crypto.getRandomValues(new Uint8Array(32)));
    const attachment: SocketAttachment = {
      authenticated: false,
      challenge,
      challengeExpiresAt: Date.now() + COMPANION_CHALLENGE_TTL_MS,
      deviceId: record.deviceId,
      sessionId: record.sessionId,
    };
    server.serializeAttachment(attachment);
    this.state.acceptWebSocket(server, ["companion"]);
    server.send(
      JSON.stringify({
        challenge,
        expiresAt: attachment.challengeExpiresAt,
        sessionId: record.sessionId,
        type: "companion_challenge",
      }),
    );
    return new Response(null, { status: 101, webSocket: client });
  }

  private async relay(request: Request): Promise<Response> {
    const input = parseInternalRelay(await readJsonBody(request, MAX_MCP_BODY_BYTES + MAX_CONTROL_BODY_BYTES));
    const record = await this.requireActiveRecord(true);
    if ((await sha256Hex(input.body)) !== input.bodyDigest) {
      throw new HttpError(400, "relay_body_digest_mismatch", "Relay body digest does not match.");
    }
    const scopes = canonicalScopes(record.scopes);
    const invocation = input.invocation;
    if (
      invocation.deviceId !== record.deviceId ||
      invocation.sessionId !== record.sessionId ||
      invocation.authorizedAt !== record.authorizedAt ||
      invocation.requestId !== input.requestId ||
      invocation.bodyDigest !== input.bodyDigest ||
      JSON.stringify(invocation.scopes) !== JSON.stringify(scopes)
    ) {
      throw new HttpError(401, "invocation_binding_invalid", "Public invocation binding is invalid.");
    }
    const expectedGrantFingerprint = await oauthGrantFingerprint({
      authorizedAt: invocation.authorizedAt,
      deviceId: record.deviceId,
      scopes,
      sessionId: record.sessionId,
    });
    if (invocation.oauthGrantFingerprint !== expectedGrantFingerprint) {
      throw new HttpError(401, "invocation_grant_invalid", "Public invocation grant is invalid.");
    }
    const operation = await describeMcpOperation({
      body: input.body,
      bodyDigest: input.bodyDigest,
      headers: input.headers,
    });
    if (
      invocation.operationDigest !== operation.digest ||
      invocation.jobId !== operation.descriptor.jobId
    ) {
      throw new HttpError(401, "invocation_operation_invalid", "Public invocation operation binding is invalid.");
    }
    requireInvocationScope(scopes, operation.requiredScope);
    const relayFingerprint = await canonicalSha256({
      bodyDigest: input.bodyDigest,
      headers: input.headers,
      invocation: invocation as unknown as JsonValue,
      requestId: input.requestId,
      schemaVersion: "foldweave-relay-correlation.v1",
    });
    const webSocket = this.state
      .getWebSockets("companion")
      .find((candidate) => {
        const attachment = candidate.deserializeAttachment() as SocketAttachment | null;
        return attachment?.authenticated === true;
      });
    if (webSocket === undefined) {
      throw new HttpError(503, "companion_offline", "Foldweave companion is not connected.");
    }
    const sequence = await this.claimRelay(
      input.requestId,
      relayFingerprint,
      invocation,
    );
    const now = Date.now();
    const trustedInvocation: TrustedPublicInvocationContext = {
      bodyDigest: input.bodyDigest,
      channel: "chatgpt_hosted",
      deviceId: record.deviceId,
      expiresAt: now + COMPANION_RPC_TIMEOUT_MS,
      issuedAt: now,
      jobId: invocation.jobId,
      nonce: bytesToBase64Url(crypto.getRandomValues(new Uint8Array(24))),
      oauthGrantFingerprint: invocation.oauthGrantFingerprint,
      operationDigest: invocation.operationDigest,
      requestId: input.requestId,
      revokedAt: record.revokedAt,
      schemaVersion: "foldweave-public-invocation.v1",
      scopes,
      sequence,
      sessionId: record.sessionId,
    };
    const outbound: CompanionRpcRequest = {
      body: input.body,
      bodyDigest: input.bodyDigest,
      expiresAt: now + COMPANION_RPC_TIMEOUT_MS,
      headers: input.headers,
      issuedAt: now,
      invocation: trustedInvocation,
      requestId: input.requestId,
      sequence,
      type: "mcp_request",
    };
    const pending = this.pending.begin(
      input.requestId,
      relayFingerprint,
      COMPANION_RPC_TIMEOUT_MS,
    );
    if (!pending.created) {
      const response = await pending.promise;
      return jsonResponse(response as unknown as JsonValue);
    }
    try {
      webSocket.send(JSON.stringify(outbound));
    } catch {
      const error = new HttpError(
        503,
        "companion_offline",
        "Foldweave companion is not connected.",
      );
      this.pending.cancel(input.requestId, error);
      throw error;
    }
    const response = await pending.promise;
    return jsonResponse(response as unknown as JsonValue);
  }

  private async requireRecord(): Promise<DeviceSessionRecord> {
    const record = await this.state.storage.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
    if (record === undefined) {
      throw new HttpError(404, "session_not_found", "Pairing session was not found.");
    }
    return record;
  }

  private async requireActiveRecord(requireAuthorized = false): Promise<DeviceSessionRecord> {
    const record = await this.requireRecord();
    if (!sessionIsActiveAt(record)) {
      throw new HttpError(401, "session_inactive", "Pairing session is not active.");
    }
    if (requireAuthorized && record.authorizedAt === null) {
      throw new HttpError(401, "session_not_authorized", "Pairing session is not authorized.");
    }
    return record;
  }

  private async verifyAndAdvance<T extends JsonValue>(
    envelope: SignedDeviceEnvelope<T>,
    record: DeviceSessionRecord,
    requireActive = true,
    preserveLastSeen = false,
  ): Promise<void> {
    await verifyDeviceEnvelope(envelope, record.publicKeyJwk);
    const nonceHash = await sha256Hex(envelope.nonce);
    const now = Date.now();
    await this.state.storage.transaction(async (transaction) => {
      const current = await transaction.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
      if (
        current === undefined ||
        (requireActive && (current.revokedAt !== null || current.expiresAt <= now))
      ) {
        throw new HttpError(401, "session_inactive", "Pairing session is not active.");
      }
      current.recentNonces = current.recentNonces.filter((nonce) => nonce.expiresAt > now);
      if (
        envelope.sequence <= current.lastSequence ||
        current.recentNonces.some((nonce) => nonce.hash === nonceHash)
      ) {
        throw new HttpError(409, "device_request_replayed", "Signed device request was replayed.");
      }
      current.lastSequence = envelope.sequence;
      if (!preserveLastSeen) {
        current.lastSeenAt = now;
      }
      current.recentNonces.push({ expiresAt: now + NONCE_RETENTION_MS, hash: nonceHash });
      current.recentNonces = current.recentNonces.slice(-MAX_RECENT_NONCES);
      await transaction.put(SESSION_STORAGE_KEY, current);
    });
  }

  private async claimRelay(
    requestId: string,
    fingerprint: string,
    invocation: PublicInvocationSeed,
  ): Promise<number> {
    const now = Date.now();
    return this.state.storage.transaction(async (transaction) => {
      const record = await transaction.get<DeviceSessionRecord>(SESSION_STORAGE_KEY);
      if (
        record === undefined ||
        !sessionIsActiveAt(record, now) ||
        record.authorizedAt === null ||
        record.authorizedAt !== invocation.authorizedAt ||
        record.deviceId !== invocation.deviceId ||
        record.sessionId !== invocation.sessionId ||
        JSON.stringify(canonicalScopes(record.scopes)) !==
          JSON.stringify(invocation.scopes)
      ) {
        throw new HttpError(
          401,
          "session_inactive",
          "Pairing session is no longer authorized for this invocation.",
        );
      }
      record.recentRelays = (record.recentRelays ?? []).filter(
        (correlation) => correlation.expiresAt > now,
      );
      const existing = record.recentRelays.find(
        (correlation) => correlation.requestId === requestId,
      );
      if (existing !== undefined && existing.fingerprint !== fingerprint) {
        throw new HttpError(
          409,
          "relay_request_conflict",
          "Request identifier was reused for different relay content.",
        );
      }
      if (existing === undefined) {
        record.recentRelays.push({
          expiresAt: now + CAPABILITY_TTL_MS,
          fingerprint,
          requestId,
        });
        record.recentRelays = record.recentRelays.slice(-MAX_RECENT_RELAYS);
      }
      record.lastRelaySequence += 1;
      await transaction.put(SESSION_STORAGE_KEY, record);
      return record.lastRelaySequence;
    });
  }

  private rejectPending(message: string): void {
    this.pending.rejectAll(new HttpError(503, "companion_offline", message));
  }
}
