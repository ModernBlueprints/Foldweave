import {
  MCP_OPERATION_SCHEMA,
  PUBLIC_INVOCATION_SCHEMA,
  PUBLIC_INVOCATION_SEED_SCHEMA,
  SUPPORTED_SCOPES,
} from "./constants";
import { canonicalSha256, type JsonValue } from "./canonical";
import {
  isPlainRecord,
  parseScopeList,
  requireDeviceId,
  requireExactKeys,
  requireOpaqueId,
  requireSessionId,
  requireSha256,
} from "./contracts";
import { HttpError } from "./http";

export type FoldweaveScope = (typeof SUPPORTED_SCOPES)[number];

export interface McpOperationDescriptor {
  bodyDigest: string;
  httpMethod: string;
  jobId: string | null;
  mcpSessionId: string | null;
  rpcMethod: string | null;
  schemaVersion: typeof MCP_OPERATION_SCHEMA;
  toolName: string | null;
}

export interface PublicInvocationSeed {
  authorizedAt: number;
  bodyDigest: string;
  channel: "chatgpt_hosted";
  deviceId: string;
  jobId: string | null;
  oauthGrantFingerprint: string;
  operationDigest: string;
  requestId: string;
  schemaVersion: typeof PUBLIC_INVOCATION_SEED_SCHEMA;
  scopes: FoldweaveScope[];
  sessionId: string;
}

export interface TrustedPublicInvocationContext {
  bodyDigest: string;
  channel: "chatgpt_hosted";
  deviceId: string;
  expiresAt: number;
  issuedAt: number;
  jobId: string | null;
  nonce: string;
  oauthGrantFingerprint: string;
  operationDigest: string;
  requestId: string;
  revokedAt: number | null;
  schemaVersion: typeof PUBLIC_INVOCATION_SCHEMA;
  scopes: FoldweaveScope[];
  sequence: number;
  sessionId: string;
}

const JOB_ID_PATTERN = /^[a-f0-9]{32}$/u;
const FORBIDDEN_PUBLIC_CAPABILITY_KEYS = [
  "capability_expires_at",
  "capability_id",
] as const;

const TOOL_SCOPES = {
  accept_plan_and_create_copy: "foldweave.execute",
  recreate_original: "foldweave.execute",
  get_change_file: "foldweave.review",
  get_plan_preview: "foldweave.review",
  job_status: "foldweave.review",
  verify_result: "foldweave.review",
  answer_clarification: "foldweave.plan",
  choose_local_item: "foldweave.plan",
  create_or_resume_planning_job: "foldweave.plan",
  get_compiler_failures: "foldweave.plan",
  inspect_markdown_links: "foldweave.plan",
  keep_previous_proposal: "foldweave.plan",
  list_inventory_page: "foldweave.plan",
  plan_change: "foldweave.plan",
  prepare_change_application: "foldweave.plan",
  read_text_excerpt: "foldweave.plan",
  request_clarification: "foldweave.plan",
  revise_plan: "foldweave.plan",
  submit_plan: "foldweave.plan",
  submit_plan_revision: "foldweave.plan",
} as const satisfies Record<string, FoldweaveScope>;

const JOBLESS_TOOLS = new Set([
  "choose_local_item",
  "create_or_resume_planning_job",
  "plan_change",
  "prepare_change_application",
]);

export function canonicalScopes(value: readonly string[]): FoldweaveScope[] {
  return [...parseScopeList([...value])].sort() as FoldweaveScope[];
}

export async function oauthGrantFingerprint(input: {
  authorizedAt: number;
  deviceId: string;
  scopes: readonly string[];
  sessionId: string;
}): Promise<string> {
  return canonicalSha256({
    authorizedAt: input.authorizedAt,
    deviceId: input.deviceId,
    schemaVersion: "foldweave-oauth-grant.v1",
    scopes: canonicalScopes(input.scopes),
    sessionId: input.sessionId,
  });
}

export async function describeMcpOperation(input: {
  body: string;
  bodyDigest: string;
  headers: Record<string, string>;
}): Promise<{
  descriptor: McpOperationDescriptor;
  digest: string;
  requiredScope: FoldweaveScope;
}> {
  const httpMethod = input.headers["x-foldweave-http-method"] ?? "POST";
  let rpcMethod: string | null = null;
  let toolName: string | null = null;
  let jobId: string | null = null;
  if (input.body.length > 0) {
    let value: unknown;
    try {
      value = JSON.parse(input.body) as unknown;
    } catch {
      throw new HttpError(400, "mcp_operation_invalid", "MCP request body is not valid JSON.");
    }
    if (!isPlainRecord(value)) {
      throw new HttpError(400, "mcp_operation_invalid", "MCP request body must be one JSON-RPC object.");
    }
    if (typeof value.method === "string" && value.method.length <= 128) {
      rpcMethod = value.method;
    }
    if (rpcMethod === "tools/call") {
      if (!isPlainRecord(value.params) || typeof value.params.name !== "string") {
        throw new HttpError(400, "mcp_operation_invalid", "MCP tool call is invalid.");
      }
      toolName = value.params.name;
      if (!(toolName in TOOL_SCOPES)) {
        throw new HttpError(403, "mcp_tool_not_authorized", "MCP tool is not authorized for public relay.");
      }
      if (!isPlainRecord(value.params.arguments)) {
        throw new HttpError(400, "mcp_operation_invalid", "MCP tool arguments are invalid.");
      }
      const argumentsValue = value.params.arguments;
      if (
        FORBIDDEN_PUBLIC_CAPABILITY_KEYS.some((key) =>
          Object.prototype.hasOwnProperty.call(argumentsValue, key),
        )
      ) {
        throw new HttpError(
          400,
          "mcp_public_capability_forbidden",
          "Public MCP tool calls cannot carry a job capability.",
        );
      }
      if (JOBLESS_TOOLS.has(toolName)) {
        if (Object.prototype.hasOwnProperty.call(argumentsValue, "job_id")) {
          throw new HttpError(
            400,
            "mcp_public_job_binding_unexpected",
            "This public MCP tool cannot receive a job identifier.",
          );
        }
      } else {
        const candidateJobId = argumentsValue.job_id;
        if (
          typeof candidateJobId !== "string" ||
          !JOB_ID_PATTERN.test(candidateJobId)
        ) {
          throw new HttpError(
            400,
            "mcp_public_job_binding_required",
            "This public MCP tool requires one exact job identifier.",
          );
        }
        jobId = candidateJobId;
      }
    }
  }
  const descriptor: McpOperationDescriptor = {
    bodyDigest: input.bodyDigest,
    httpMethod,
    jobId,
    mcpSessionId: input.headers["mcp-session-id"] ?? null,
    rpcMethod,
    schemaVersion: MCP_OPERATION_SCHEMA,
    toolName,
  };
  return {
    descriptor,
    digest: await canonicalSha256(descriptor as unknown as JsonValue),
    requiredScope:
      toolName === null
        ? "foldweave.review"
        : TOOL_SCOPES[toolName as keyof typeof TOOL_SCOPES],
  };
}

export function parsePublicInvocationSeed(value: unknown): PublicInvocationSeed {
  if (!isPlainRecord(value)) {
    throw new HttpError(400, "invocation_context_invalid", "Public invocation context is invalid.");
  }
  requireExactKeys(
    value,
    [
      "authorizedAt",
      "bodyDigest",
      "channel",
      "deviceId",
      "jobId",
      "oauthGrantFingerprint",
      "operationDigest",
      "requestId",
      "schemaVersion",
      "scopes",
      "sessionId",
    ],
    "invocation_context",
  );
  if (
    value.schemaVersion !== PUBLIC_INVOCATION_SEED_SCHEMA ||
    value.channel !== "chatgpt_hosted" ||
    !Number.isSafeInteger(value.authorizedAt) ||
    Number(value.authorizedAt) <= 0
  ) {
    throw new HttpError(400, "invocation_context_invalid", "Public invocation context is invalid.");
  }
  const hasJobId = value.jobId !== null;
  if (hasJobId && (typeof value.jobId !== "string" || !JOB_ID_PATTERN.test(value.jobId))) {
    throw new HttpError(400, "invocation_context_invalid", "Public invocation job binding is invalid.");
  }
  return {
    authorizedAt: Number(value.authorizedAt),
    bodyDigest: requireSha256(value.bodyDigest, "invocation_body_digest"),
    channel: "chatgpt_hosted",
    deviceId: requireDeviceId(value.deviceId),
    jobId: hasJobId ? String(value.jobId) : null,
    oauthGrantFingerprint: requireSha256(value.oauthGrantFingerprint, "oauth_grant_fingerprint"),
    operationDigest: requireSha256(value.operationDigest, "operation_digest"),
    requestId: requireOpaqueId(value.requestId, "invocation_request_id"),
    schemaVersion: PUBLIC_INVOCATION_SEED_SCHEMA,
    scopes: canonicalScopes(parseScopeList(value.scopes)),
    sessionId: requireSessionId(value.sessionId),
  };
}

export function requireInvocationScope(
  scopes: readonly string[],
  requiredScope: FoldweaveScope,
): void {
  if (!scopes.includes(requiredScope)) {
    throw new HttpError(403, "invocation_scope_missing", "OAuth grant does not authorize this Foldweave operation.");
  }
}
