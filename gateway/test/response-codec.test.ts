import { describe, expect, it } from "vitest";

import {
  bytesToBase64Url,
  sha256Hex,
  utf8,
} from "../src/canonical";
import {
  MAX_MCP_RESPONSE_COMPRESSED_BYTES,
  MAX_MCP_RESPONSE_DECODED_BYTES,
  MAX_MCP_RESPONSE_WIRE_BYTES,
} from "../src/constants";
import {
  decodeCompanionRpcResponse,
  parseCompanionRpcResponseEnvelope,
} from "../src/response-codec";

function actualBuiltWidgetResource(): string {
  const safeJavaScript = __FOLDWEAVE_WIDGET_JAVASCRIPT__.replace(
    /<\/script/giu,
    "<\\/script",
  );
  const safeStylesheet = __FOLDWEAVE_WIDGET_CSS__.replace(
    /<\/style/giu,
    "<\\/style",
  );
  return (
    '<!doctype html><html lang="en"><head>' +
    '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    "<title>Foldweave structure review</title>" +
    `<style>${safeStylesheet}</style></head><body>` +
    '<div id="foldweave-chatgpt-widget-root"></div>' +
    `<script type="module">${safeJavaScript}</script>` +
    "</body></html>"
  );
}

async function gzip(value: Uint8Array): Promise<Uint8Array> {
  const reader = new Blob([Uint8Array.from(value)])
    .stream()
    .pipeThrough(new CompressionStream("gzip"))
    .getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;
  while (true) {
    const { done, value: chunk } = await reader.read();
    if (done) {
      break;
    }
    chunks.push(chunk);
    total += chunk.byteLength;
  }
  const output = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    output.set(chunk, offset);
    offset += chunk.byteLength;
  }
  return output;
}

async function encodedEnvelope(body: string): Promise<Record<string, unknown>> {
  const decoded = utf8(body);
  const compressed = await gzip(decoded);
  return {
    body: bytesToBase64Url(compressed),
    bodyDigest: await sha256Hex(decoded),
    bodyEncoding: "gzip+base64url",
    compressedSize: compressed.byteLength,
    decodedSize: decoded.byteLength,
    headers: { "content-type": "text/html;profile=mcp-app" },
    requestId: "widget_resource_0123456789abcdef",
    schemaVersion: "foldweave-mcp-response-envelope.v1",
    status: 200,
    type: "mcp_response",
  };
}

describe("companion response codec", () => {
  it("carries the actual built widget under the one-MiB signed boundary", async () => {
    const widget = actualBuiltWidgetResource();
    const decodedBytes = utf8(widget);
    expect(decodedBytes.byteLength).toBeGreaterThan(MAX_MCP_RESPONSE_WIRE_BYTES);

    const wire = await encodedEnvelope(widget);
    const serializedWireBytes = utf8(JSON.stringify(wire)).byteLength;
    expect(Number(wire.compressedSize)).toBeLessThanOrEqual(
      MAX_MCP_RESPONSE_COMPRESSED_BYTES,
    );
    expect(serializedWireBytes).toBeLessThanOrEqual(MAX_MCP_RESPONSE_WIRE_BYTES);

    const decoded = await decodeCompanionRpcResponse(
      parseCompanionRpcResponseEnvelope(wire),
    );
    expect(decoded.body).toBe(widget);
    expect(decoded.headers).toEqual({
      "content-type": "text/html;profile=mcp-app",
    });
  });

  it("refuses unknown encodings, decoded-size overruns, and digest mismatches", async () => {
    const valid = await encodedEnvelope("Foldweave response");
    expect(() =>
      parseCompanionRpcResponseEnvelope({
        ...valid,
        bodyEncoding: "identity",
      }),
    ).toThrow(/encoding is unsupported/u);
    expect(() =>
      parseCompanionRpcResponseEnvelope({
        ...valid,
        decodedSize: MAX_MCP_RESPONSE_DECODED_BYTES + 1,
      }),
    ).toThrow(/decoded_size is invalid/u);

    const parsed = parseCompanionRpcResponseEnvelope({
      ...valid,
      bodyDigest: "0".repeat(64),
    });
    await expect(decodeCompanionRpcResponse(parsed)).rejects.toThrow(
      /digest does not match/u,
    );
  });

  it("refuses compressed bodies above the fixed compressed limit", () => {
    const oversized = new Uint8Array(MAX_MCP_RESPONSE_COMPRESSED_BYTES + 1);
    expect(() =>
      parseCompanionRpcResponseEnvelope({
        body: bytesToBase64Url(oversized),
        bodyDigest: "0".repeat(64),
        bodyEncoding: "gzip+base64url",
        compressedSize: oversized.byteLength,
        decodedSize: 0,
        headers: { "content-type": "application/json" },
        requestId: "oversized_response_0123456789",
        schemaVersion: "foldweave-mcp-response-envelope.v1",
        status: 200,
        type: "mcp_response",
      }),
    ).toThrow(/too large/u);
  });
});
