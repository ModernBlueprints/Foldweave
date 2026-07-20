import {
  MAX_MCP_RESPONSE_COMPRESSED_BYTES,
  MAX_MCP_RESPONSE_DECODED_BYTES,
  MAX_MCP_RESPONSE_ENCODED_CHARACTERS,
  MCP_RESPONSE_BODY_ENCODING,
  MCP_RESPONSE_ENVELOPE_SCHEMA,
} from "./constants";
import {
  base64UrlToBytes,
  bytesToBase64Url,
  sha256Hex,
} from "./canonical";
import {
  isPlainRecord,
  requireExactKeys,
  requireOpaqueId,
  requireSha256,
  type CompanionRpcResponseEnvelope,
} from "./contracts";
import { HttpError } from "./http";

const RESPONSE_HEADER_ALLOWLIST = new Set([
  "content-type",
  "mcp-session-id",
  "retry-after",
]);

export interface DecodedCompanionRpcResponse {
  body: string;
  headers: Record<string, string>;
  requestId: string;
  status: number;
}

function requireBoundedSize(
  value: unknown,
  label: string,
  maximum: number,
): number {
  if (!Number.isSafeInteger(value) || Number(value) < 0 || Number(value) > maximum) {
    throw new HttpError(400, `${label}_invalid`, `${label} is invalid.`);
  }
  return Number(value);
}

export function parseCompanionRpcResponseEnvelope(
  value: unknown,
): CompanionRpcResponseEnvelope {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "rpc_response_invalid", "Companion response is invalid.");
  }
  requireExactKeys(
    value,
    [
      "body",
      "bodyDigest",
      "bodyEncoding",
      "compressedSize",
      "decodedSize",
      "headers",
      "requestId",
      "schemaVersion",
      "status",
      "type",
    ],
    "rpc_response",
  );
  if (value.schemaVersion !== MCP_RESPONSE_ENVELOPE_SCHEMA) {
    throw new HttpError(
      400,
      "rpc_response_schema_unsupported",
      "Companion response schema is unsupported.",
    );
  }
  if (value.bodyEncoding !== MCP_RESPONSE_BODY_ENCODING) {
    throw new HttpError(
      400,
      "rpc_response_encoding_unsupported",
      "Companion response encoding is unsupported.",
    );
  }
  if (value.type !== "mcp_response") {
    throw new HttpError(400, "rpc_response_invalid", "Companion response type is invalid.");
  }
  if (
    typeof value.body !== "string" ||
    value.body.length === 0 ||
    value.body.length > MAX_MCP_RESPONSE_ENCODED_CHARACTERS
  ) {
    throw new HttpError(413, "rpc_response_too_large", "Companion response is too large.");
  }
  let compressed: Uint8Array;
  try {
    compressed = base64UrlToBytes(value.body);
  } catch {
    throw new HttpError(400, "rpc_response_invalid", "Companion response body is invalid.");
  }
  if (bytesToBase64Url(compressed) !== value.body) {
    throw new HttpError(400, "rpc_response_invalid", "Companion response body is invalid.");
  }
  const compressedSize = requireBoundedSize(
    value.compressedSize,
    "rpc_response_compressed_size",
    MAX_MCP_RESPONSE_COMPRESSED_BYTES,
  );
  if (compressedSize === 0 || compressed.byteLength !== compressedSize) {
    throw new HttpError(400, "rpc_response_invalid", "Companion response size is invalid.");
  }
  const decodedSize = requireBoundedSize(
    value.decodedSize,
    "rpc_response_decoded_size",
    MAX_MCP_RESPONSE_DECODED_BYTES,
  );
  if (!Number.isInteger(value.status) || Number(value.status) < 100 || Number(value.status) > 599) {
    throw new HttpError(400, "rpc_response_invalid", "Companion response status is invalid.");
  }
  if (!isPlainRecord(value.headers)) {
    throw new HttpError(400, "rpc_response_invalid", "Companion response headers are invalid.");
  }
  const headers: Record<string, string> = {};
  for (const [name, headerValue] of Object.entries(value.headers)) {
    const normalized = name.toLowerCase();
    if (
      !RESPONSE_HEADER_ALLOWLIST.has(normalized) ||
      typeof headerValue !== "string" ||
      headerValue.length > 512 ||
      /[\r\n]/u.test(headerValue)
    ) {
      throw new HttpError(400, "rpc_response_invalid", "Companion response headers are invalid.");
    }
    headers[normalized] = headerValue;
  }
  return {
    body: value.body,
    bodyDigest: requireSha256(value.bodyDigest, "rpc_response_body_digest"),
    bodyEncoding: MCP_RESPONSE_BODY_ENCODING,
    compressedSize,
    decodedSize,
    headers,
    requestId: requireOpaqueId(value.requestId, "request_id"),
    schemaVersion: MCP_RESPONSE_ENVELOPE_SCHEMA,
    status: Number(value.status),
    type: "mcp_response",
  };
}

export async function decodeCompanionRpcResponse(
  envelope: CompanionRpcResponseEnvelope,
): Promise<DecodedCompanionRpcResponse> {
  const compressed = base64UrlToBytes(envelope.body);
  if (
    compressed.byteLength !== envelope.compressedSize ||
    compressed.byteLength > MAX_MCP_RESPONSE_COMPRESSED_BYTES
  ) {
    throw new HttpError(502, "rpc_response_invalid", "Companion response size is invalid.");
  }
  const bodyBytes = await gunzipBounded(compressed, envelope.decodedSize);
  if ((await sha256Hex(bodyBytes)) !== envelope.bodyDigest) {
    throw new HttpError(
      502,
      "rpc_response_digest_mismatch",
      "Companion response digest does not match.",
    );
  }
  let body: string;
  try {
    body = new TextDecoder("utf-8", { fatal: true }).decode(bodyBytes);
  } catch {
    throw new HttpError(502, "rpc_response_invalid", "Companion response is not UTF-8.");
  }
  return {
    body,
    headers: envelope.headers,
    requestId: envelope.requestId,
    status: envelope.status,
  };
}

async function gunzipBounded(
  compressed: Uint8Array,
  declaredDecodedSize: number,
): Promise<Uint8Array> {
  let reader: ReadableStreamDefaultReader<Uint8Array>;
  try {
    const stream = new Blob([Uint8Array.from(compressed)]).stream().pipeThrough(
      new DecompressionStream("gzip"),
    );
    reader = stream.getReader();
  } catch {
    throw new HttpError(502, "rpc_response_invalid", "Companion response compression is invalid.");
  }
  const chunks: Uint8Array[] = [];
  let total = 0;
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      total += value.byteLength;
      if (total > declaredDecodedSize || total > MAX_MCP_RESPONSE_DECODED_BYTES) {
        await reader.cancel();
        throw new HttpError(413, "rpc_response_decoded_too_large", "Companion response expands beyond its limit.");
      }
      chunks.push(value);
    }
  } catch (error) {
    if (error instanceof HttpError) {
      throw error;
    }
    throw new HttpError(502, "rpc_response_invalid", "Companion response compression is invalid.");
  }
  if (total !== declaredDecodedSize) {
    throw new HttpError(502, "rpc_response_invalid", "Companion response decoded size is invalid.");
  }
  const decoded = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    decoded.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return decoded;
}
