import {
  CLOCK_SKEW_MS,
  DEVICE_ENVELOPE_SCHEMA,
  SIGNED_REQUEST_MAX_LIFETIME_MS,
} from "./constants";
import {
  base64UrlToBytes,
  canonicalJson,
  canonicalSha256,
  utf8,
  type JsonValue,
} from "./canonical";
import type { Ed25519PublicJwk, SignedDeviceEnvelope } from "./contracts";
import { HttpError } from "./http";

const SIGNATURE_DOMAIN = "foldweave-device-envelope-signature.v1\u0000";

export function signaturePayload<T extends JsonValue>(
  envelope: Omit<SignedDeviceEnvelope<T>, "signature">,
): Uint8Array {
  return utf8(
    `${SIGNATURE_DOMAIN}${canonicalJson({
      body: envelope.body,
      bodyDigest: envelope.bodyDigest,
      expiresAt: envelope.expiresAt,
      issuedAt: envelope.issuedAt,
      nonce: envelope.nonce,
      requestId: envelope.requestId,
      schemaVersion: DEVICE_ENVELOPE_SCHEMA,
      sequence: envelope.sequence,
    })}`,
  );
}

export async function importEd25519PublicKey(
  publicKeyJwk: Ed25519PublicJwk,
): Promise<CryptoKey> {
  try {
    return await crypto.subtle.importKey(
      "jwk",
      publicKeyJwk,
      { name: "Ed25519" },
      false,
      ["verify"],
    );
  } catch {
    throw new HttpError(400, "public_key_invalid", "Ed25519 public key cannot be imported.");
  }
}

export async function verifyDeviceEnvelope<T extends JsonValue>(
  envelope: SignedDeviceEnvelope<T>,
  publicKeyJwk: Ed25519PublicJwk,
  now = Date.now(),
): Promise<void> {
  if (envelope.issuedAt > now + CLOCK_SKEW_MS) {
    throw new HttpError(401, "device_signature_invalid", "Signed request was issued in the future.");
  }
  if (envelope.expiresAt <= now - CLOCK_SKEW_MS) {
    throw new HttpError(401, "device_signature_expired", "Signed request has expired.");
  }
  if (
    envelope.expiresAt <= envelope.issuedAt ||
    envelope.expiresAt - envelope.issuedAt > SIGNED_REQUEST_MAX_LIFETIME_MS
  ) {
    throw new HttpError(401, "device_signature_invalid", "Signed request lifetime is invalid.");
  }
  const expectedDigest = await canonicalSha256(envelope.body);
  if (expectedDigest !== envelope.bodyDigest) {
    throw new HttpError(401, "body_digest_mismatch", "Signed request body digest does not match.");
  }
  const publicKey = await importEd25519PublicKey(publicKeyJwk);
  const verified = await crypto.subtle.verify(
    { name: "Ed25519" },
    publicKey,
    Uint8Array.from(base64UrlToBytes(envelope.signature)).buffer,
    Uint8Array.from(signaturePayload({
      body: envelope.body,
      bodyDigest: envelope.bodyDigest,
      expiresAt: envelope.expiresAt,
      issuedAt: envelope.issuedAt,
      nonce: envelope.nonce,
      requestId: envelope.requestId,
      schemaVersion: envelope.schemaVersion,
      sequence: envelope.sequence,
    })).buffer,
  );
  if (!verified) {
    throw new HttpError(401, "device_signature_invalid", "Device signature is invalid.");
  }
}
