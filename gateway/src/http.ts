import { MAX_CONTROL_BODY_BYTES } from "./constants";
import type { JsonValue } from "./canonical";

export class HttpError extends Error {
  public readonly status: number;
  public readonly code: string;

  public constructor(status: number, code: string, message: string) {
    super(message);
    this.name = "HttpError";
    this.status = status;
    this.code = code;
  }
}

export function jsonResponse(
  value: JsonValue,
  init: ResponseInit = {},
): Response {
  const headers = new Headers(init.headers);
  headers.set("content-type", "application/json; charset=utf-8");
  headers.set("cache-control", "no-store");
  headers.set("x-content-type-options", "nosniff");
  return new Response(JSON.stringify(value), { ...init, headers });
}

export function errorResponse(error: unknown): Response {
  if (error instanceof HttpError) {
    return jsonResponse(
      { error: error.code, message: error.message },
      { status: error.status },
    );
  }
  console.error("Unhandled gateway failure", {
    errorName: error instanceof Error ? error.name : "unknown",
  });
  return jsonResponse(
    { error: "internal_error", message: "The gateway could not complete the request." },
    { status: 500 },
  );
}

export async function readJsonBody(
  request: Request,
  maximumBytes = MAX_CONTROL_BODY_BYTES,
): Promise<unknown> {
  const contentType = request.headers.get("content-type")?.split(";", 1)[0]?.trim();
  if (contentType !== "application/json") {
    throw new HttpError(415, "content_type_invalid", "Expected application/json.");
  }
  const declaredLength = request.headers.get("content-length");
  if (declaredLength !== null && Number(declaredLength) > maximumBytes) {
    throw new HttpError(413, "request_too_large", "Request body is too large.");
  }
  const bytes = new Uint8Array(await request.arrayBuffer());
  if (bytes.byteLength > maximumBytes) {
    throw new HttpError(413, "request_too_large", "Request body is too large.");
  }
  try {
    return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes)) as unknown;
  } catch {
    throw new HttpError(400, "json_invalid", "Request body is not strict UTF-8 JSON.");
  }
}

export function requireMethod(request: Request, ...methods: string[]): void {
  if (!methods.includes(request.method)) {
    throw new HttpError(405, "method_not_allowed", "Method not allowed.");
  }
}

export function securityHeaders(headers = new Headers()): Headers {
  headers.set("cache-control", "no-store");
  headers.set("content-security-policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'");
  headers.set("referrer-policy", "no-referrer");
  headers.set("x-content-type-options", "nosniff");
  headers.set("x-frame-options", "DENY");
  return headers;
}
