import {
  DEVICE_ENVELOPE_SCHEMA,
  DEVICE_REGISTRATION_SCHEMA,
  MCP_RESPONSE_BODY_ENCODING,
  MCP_RESPONSE_ENVELOPE_SCHEMA,
  MAX_CONTROL_BODY_BYTES,
  PAIRING_CODE_LENGTH,
  SUPPORTED_SCOPES,
} from "./constants";
import type { JsonValue } from "./canonical";
import type { TrustedPublicInvocationContext } from "./public-invocation";
import { HttpError } from "./http";

export interface Ed25519PublicJwk extends JsonWebKey {
  crv: "Ed25519";
  kty: "OKP";
  x: string;
}

export interface SignedDeviceEnvelope<T extends JsonValue = JsonValue> {
  body: T;
  bodyDigest: string;
  expiresAt: number;
  issuedAt: number;
  nonce: string;
  requestId: string;
  schemaVersion: typeof DEVICE_ENVELOPE_SCHEMA;
  sequence: number;
  signature: string;
}

export interface DeviceRegistrationBody {
  deviceId: string;
  deviceName: string;
  publicKeyJwk: Ed25519PublicJwk;
  schemaVersion: typeof DEVICE_REGISTRATION_SCHEMA;
}

export interface DeviceSessionRecord {
  activeCodeHash: string;
  authorizedAt: number | null;
  createdAt: number;
  deviceId: string;
  deviceName: string;
  expiresAt: number;
  lastRelaySequence: number;
  lastSequence: number;
  localApprovedAt: number | null;
  lastSeenAt: number | null;
  publicKeyJwk: Ed25519PublicJwk;
  recentNonces: Array<{ expiresAt: number; hash: string }>;
  recentRelays: Array<{
    expiresAt: number;
    fingerprint: string;
    requestId: string;
  }>;
  revokedAt: number | null;
  scopes: string[];
  sessionId: string;
}

export interface PairingDirectoryRecord {
  codeHash: string;
  consumedAt: number | null;
  expiresAt: number;
  failedAttempts: number;
  localApprovedAt: number | null;
  revokedAt: number | null;
  sessionId: string;
}

export interface CompanionRpcRequest {
  body: string;
  bodyDigest: string;
  expiresAt: number;
  headers: Record<string, string>;
  issuedAt: number;
  invocation: TrustedPublicInvocationContext;
  requestId: string;
  sequence: number;
  type: "mcp_request";
}

export interface CompanionRpcResponseEnvelope {
  [key: string]: JsonValue;
  body: string;
  bodyDigest: string;
  bodyEncoding: typeof MCP_RESPONSE_BODY_ENCODING;
  compressedSize: number;
  decodedSize: number;
  headers: Record<string, string>;
  requestId: string;
  schemaVersion: typeof MCP_RESPONSE_ENVELOPE_SCHEMA;
  status: number;
  type: "mcp_response";
}

export interface CompanionChallengeBody {
  challenge: string;
  sessionId: string;
  type: "challenge_response";
}

const DEVICE_ID_PATTERN = /^fwd_[a-f0-9]{32}$/u;
const SESSION_ID_PATTERN = /^[A-Za-z0-9_-]{32,128}$/u;
const OPAQUE_ID_PATTERN = /^[A-Za-z0-9_-]{16,128}$/u;
const SHA256_PATTERN = /^[0-9a-f]{64}$/u;
const BASE64URL_PATTERN = /^[A-Za-z0-9_-]+$/u;
const PAIRING_CODE_PATTERN = new RegExp(`^[0-9A-HJKMNP-TV-Z]{${PAIRING_CODE_LENGTH}}$`, "u");

export function isPlainRecord(value: unknown): value is Record<string, unknown> {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value) &&
    Object.getPrototypeOf(value) === Object.prototype
  );
}

export function requireExactKeys(
  value: Record<string, unknown>,
  keys: readonly string[],
  label: string,
): void {
  const actual = Object.keys(value).sort();
  const expected = [...keys].sort();
  if (actual.length !== expected.length || actual.some((key, index) => key !== expected[index])) {
    throw new HttpError(400, `${label}_schema_invalid`, `${label} has unsupported or missing fields.`);
  }
}

function requireString(
  value: unknown,
  label: string,
  maximumLength: number,
): string {
  if (typeof value !== "string" || value.length === 0 || value.length > maximumLength) {
    throw new HttpError(400, `${label}_invalid`, `${label} is invalid.`);
  }
  return value;
}

export function requireDeviceId(value: unknown): string {
  const deviceId = requireString(value, "device_id", 128);
  if (!DEVICE_ID_PATTERN.test(deviceId)) {
    throw new HttpError(400, "device_id_invalid", "deviceId must be an opaque identifier.");
  }
  return deviceId;
}

export function requireSessionId(value: unknown): string {
  const sessionId = requireString(value, "session_id", 128);
  if (!SESSION_ID_PATTERN.test(sessionId)) {
    throw new HttpError(400, "session_id_invalid", "sessionId must be an opaque identifier.");
  }
  return sessionId;
}

export function requireOpaqueId(value: unknown, label: string): string {
  const identifier = requireString(value, label, 128);
  if (!OPAQUE_ID_PATTERN.test(identifier)) {
    throw new HttpError(400, `${label}_invalid`, `${label} must be an opaque identifier.`);
  }
  return identifier;
}

export function requireSha256(value: unknown, label: string): string {
  const digest = requireString(value, label, 64);
  if (!SHA256_PATTERN.test(digest)) {
    throw new HttpError(400, `${label}_invalid`, `${label} must be a lowercase SHA-256 digest.`);
  }
  return digest;
}

export function requireBase64Url(value: unknown, label: string): string {
  const encoded = requireString(value, label, MAX_CONTROL_BODY_BYTES);
  if (!BASE64URL_PATTERN.test(encoded)) {
    throw new HttpError(400, `${label}_invalid`, `${label} must be unpadded base64url.`);
  }
  return encoded;
}

export function normalizePairingCode(value: unknown): string {
  if (typeof value !== "string") {
    throw new HttpError(400, "pairing_code_invalid", "Pairing code is invalid.");
  }
  const normalized = value.replace(/[\s-]/gu, "").toUpperCase();
  if (!PAIRING_CODE_PATTERN.test(normalized)) {
    throw new HttpError(400, "pairing_code_invalid", "Pairing code is invalid.");
  }
  return normalized;
}

export function parsePublicJwk(value: unknown): Ed25519PublicJwk {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "public_key_invalid", "publicKeyJwk is invalid.");
  }
  requireExactKeys(value, ["crv", "kty", "x"], "public_key");
  if (value.kty !== "OKP" || value.crv !== "Ed25519") {
    throw new HttpError(400, "public_key_invalid", "Only Ed25519 public keys are supported.");
  }
  const x = requireBase64Url(value.x, "public_key_x");
  if (x.length !== 43) {
    throw new HttpError(400, "public_key_invalid", "Ed25519 public key length is invalid.");
  }
  return { crv: "Ed25519", kty: "OKP", x };
}

export function parseRegistrationBody(value: unknown): DeviceRegistrationBody {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "registration_schema_invalid", "Registration body is invalid.");
  }
  requireExactKeys(
    value,
    ["deviceId", "deviceName", "publicKeyJwk", "schemaVersion"],
    "registration",
  );
  if (value.schemaVersion !== DEVICE_REGISTRATION_SCHEMA) {
    throw new HttpError(400, "registration_schema_invalid", "Registration schema is unsupported.");
  }
  const deviceName = requireString(value.deviceName, "device_name", 80).trim();
  if (deviceName.length === 0 || /[\u0000-\u001f\u007f]/u.test(deviceName)) {
    throw new HttpError(400, "device_name_invalid", "deviceName is invalid.");
  }
  return {
    deviceId: requireDeviceId(value.deviceId),
    deviceName,
    publicKeyJwk: parsePublicJwk(value.publicKeyJwk),
    schemaVersion: DEVICE_REGISTRATION_SCHEMA,
  };
}

export function parseSignedEnvelope<T extends JsonValue>(
  value: unknown,
  parseBody: (body: unknown) => T,
): SignedDeviceEnvelope<T> {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "device_envelope_invalid", "Signed device envelope is invalid.");
  }
  requireExactKeys(
    value,
    [
      "body",
      "bodyDigest",
      "expiresAt",
      "issuedAt",
      "nonce",
      "requestId",
      "schemaVersion",
      "sequence",
      "signature",
    ],
    "device_envelope",
  );
  if (value.schemaVersion !== DEVICE_ENVELOPE_SCHEMA) {
    throw new HttpError(400, "device_envelope_invalid", "Signed envelope schema is unsupported.");
  }
  if (!Number.isSafeInteger(value.issuedAt) || !Number.isSafeInteger(value.expiresAt)) {
    throw new HttpError(400, "device_envelope_invalid", "Signed envelope timestamps are invalid.");
  }
  if (!Number.isSafeInteger(value.sequence) || Number(value.sequence) < 1) {
    throw new HttpError(400, "device_envelope_invalid", "Signed envelope sequence is invalid.");
  }
  const signature = requireBase64Url(value.signature, "signature");
  if (signature.length !== 86) {
    throw new HttpError(400, "signature_invalid", "Ed25519 signature length is invalid.");
  }
  return {
    body: parseBody(value.body),
    bodyDigest: requireSha256(value.bodyDigest, "body_digest"),
    expiresAt: Number(value.expiresAt),
    issuedAt: Number(value.issuedAt),
    nonce: requireOpaqueId(value.nonce, "nonce"),
    requestId: requireOpaqueId(value.requestId, "request_id"),
    schemaVersion: DEVICE_ENVELOPE_SCHEMA,
    sequence: Number(value.sequence),
    signature,
  };
}

export function parseScopeList(value: unknown): string[] {
  if (!Array.isArray(value) || value.some((scope) => typeof scope !== "string")) {
    throw new HttpError(400, "scopes_invalid", "Scopes are invalid.");
  }
  const unique = [...new Set(value)];
  if (
    unique.length !== value.length ||
    unique.some((scope) => !SUPPORTED_SCOPES.includes(scope as (typeof SUPPORTED_SCOPES)[number]))
  ) {
    throw new HttpError(400, "scopes_invalid", "Scopes are invalid.");
  }
  return unique;
}

export function recordAsJson(value: Record<string, unknown>): JsonValue {
  return value as JsonValue;
}
