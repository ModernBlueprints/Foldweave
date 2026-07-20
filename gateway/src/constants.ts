export const ACCESS_TOKEN_TTL_SECONDS = 60 * 60;
export const REFRESH_TOKEN_TTL_SECONDS = 30 * 24 * 60 * 60;
export const CLIENT_REGISTRATION_TTL_SECONDS = 90 * 24 * 60 * 60;
export const CAPABILITY_TTL_MS = 30 * 60 * 1000;
export const DEVICE_AUTHORIZATION_TTL_MS = REFRESH_TOKEN_TTL_SECONDS * 1000;

export const PAIRING_CODE_LENGTH = 10;
export const PAIRING_CODE_TTL_MS = 10 * 60 * 1000;
export const PAIRING_CODE_MAX_FAILURES = 5;
export const PAIRING_IP_MAX_ATTEMPTS = 20;
export const PAIRING_IP_WINDOW_MS = 15 * 60 * 1000;

export const CLOCK_SKEW_MS = 60 * 1000;
export const SIGNED_REQUEST_MAX_LIFETIME_MS = 30 * 60 * 1000;
export const NONCE_RETENTION_MS = 35 * 60 * 1000;
export const MAX_RECENT_NONCES = 128;
export const MAX_RECENT_RELAYS = 256;
export const COMPANION_CHALLENGE_TTL_MS = 60 * 1000;
export const COMPANION_RPC_TIMEOUT_MS = 25 * 1000;

export const MAX_CONTROL_BODY_BYTES = 16 * 1024;
export const MAX_MCP_BODY_BYTES = 1024 * 1024;
export const MAX_MCP_RESPONSE_WIRE_BYTES = 1024 * 1024;
export const MAX_MCP_RESPONSE_COMPRESSED_BYTES = 768 * 1024;
export const MAX_MCP_RESPONSE_DECODED_BYTES = 4 * 1024 * 1024;
export const MAX_MCP_RESPONSE_ENCODED_CHARACTERS = Math.ceil(
  (MAX_MCP_RESPONSE_COMPRESSED_BYTES * 4) / 3,
);

export const SUPPORTED_SCOPES = [
  "foldweave.plan",
  "foldweave.review",
  "foldweave.execute",
] as const;

export const DEVICE_ENVELOPE_SCHEMA = "foldweave-device-envelope.v1" as const;
export const DEVICE_REGISTRATION_SCHEMA =
  "foldweave-device-registration.v1" as const;
export const OAUTH_PROPS_SCHEMA = "foldweave-oauth-props.v1" as const;
export const MCP_RESPONSE_ENVELOPE_SCHEMA =
  "foldweave-mcp-response-envelope.v1" as const;
export const MCP_RESPONSE_BODY_ENCODING = "gzip+base64url" as const;
export const PUBLIC_INVOCATION_SCHEMA =
  "foldweave-public-invocation.v1" as const;
export const PUBLIC_INVOCATION_SEED_SCHEMA =
  "foldweave-public-invocation-seed.v1" as const;
export const MCP_OPERATION_SCHEMA = "foldweave-mcp-operation.v1" as const;
