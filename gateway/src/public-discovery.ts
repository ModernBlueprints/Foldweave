import { MAX_MCP_BODY_BYTES, SUPPORTED_SCOPES } from "./constants";
import { isPlainRecord } from "./contracts";
import generatedOutputContract from "./generated/foldweave-public-mcp-output-contract.v1.json";
import { HttpError, jsonResponse, readJsonBody } from "./http";
import type { FoldweaveScope } from "./public-invocation";

export const PUBLIC_MCP_PATH = "/mcp";
const WIDGET_MIME_TYPE = "text/html;profile=mcp-app";
const LATEST_PROTOCOL_VERSION = "2025-06-18";
const SUPPORTED_PROTOCOL_VERSIONS = new Set([
  "2024-11-05",
  "2025-03-26",
  LATEST_PROTOCOL_VERSION,
]);

type JsonRpcId = number | string | null;
type JsonSchema = Record<string, unknown>;

interface PublicMcpOutputContract {
  outputSchemaFamilies: Record<string, JsonSchema>;
  schemaVersion: "foldweave-public-mcp-output-contract.v1";
  toolOutputFamily: Record<string, string>;
  widgetResourceUri: string;
}

function parseOutputContract(value: unknown): PublicMcpOutputContract {
  if (!isPlainRecord(value)) {
    throw new Error("The generated public MCP output contract is invalid.");
  }
  const keys = Object.keys(value).sort();
  const expectedKeys = [
    "outputSchemaFamilies",
    "schemaVersion",
    "toolOutputFamily",
    "widgetResourceUri",
  ];
  if (JSON.stringify(keys) !== JSON.stringify(expectedKeys)) {
    throw new Error("The generated public MCP output contract has unexpected fields.");
  }
  if (
    value.schemaVersion !== "foldweave-public-mcp-output-contract.v1" ||
    typeof value.widgetResourceUri !== "string" ||
    !value.widgetResourceUri.startsWith("ui://foldweave/") ||
    !isPlainRecord(value.outputSchemaFamilies) ||
    !isPlainRecord(value.toolOutputFamily)
  ) {
    throw new Error("The generated public MCP output contract is malformed.");
  }
  return value as unknown as PublicMcpOutputContract;
}

const OUTPUT_CONTRACT = parseOutputContract(generatedOutputContract);
export const WIDGET_RESOURCE_URI = OUTPUT_CONTRACT.widgetResourceUri;
export const WIDGET_RESOURCE_COMPATIBILITY_URIS = [
  "ui://foldweave/review-v31.html",
  "ui://foldweave/review-v32.html",
] as const;
const READABLE_WIDGET_RESOURCE_URIS = new Set<string>([
  WIDGET_RESOURCE_URI,
  ...WIDGET_RESOURCE_COMPATIBILITY_URIS,
]);

interface PublicToolDescriptor {
  _meta: Record<string, unknown>;
  annotations: {
    destructiveHint: false;
    idempotentHint: boolean;
    openWorldHint: false;
    readOnlyHint: boolean;
  };
  description: string;
  inputSchema: JsonSchema;
  name: string;
  outputSchema: JsonSchema;
  securitySchemes: Array<{ scopes: FoldweaveScope[]; type: "oauth2" }>;
  title: string;
}

const SHA256 = { pattern: "^[a-f0-9]{64}$", type: "string" } as const;
const JOB_ID = { pattern: "^[a-f0-9]{32}$", type: "string" } as const;
const OPAQUE_HANDLE = {
  pattern: "^fw_[A-Za-z0-9_-]{43}$",
  type: "string",
} as const;
const LOCAL_SELECTION_ID = {
  pattern: "^fwsel_[A-Za-z0-9_-]{43}$",
  type: "string",
} as const;
const IDEMPOTENCY_KEY = {
  maxLength: 200,
  minLength: 1,
  type: "string",
} as const;
const CALL_ID = { maxLength: 128, minLength: 1, type: "string" } as const;
const NONNEGATIVE_INTEGER = { minimum: 0, type: "integer" } as const;
const NULLABLE_SHA256 = {
  anyOf: [SHA256, { type: "null" }],
} as const;

const TOOL_SCOPES = {
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
  submit_plan: "foldweave.plan",
  submit_compact_plan: "foldweave.plan",
  submit_plan_revision: "foldweave.plan",
  verify_result: "foldweave.review",
} as const satisfies Record<string, FoldweaveScope>;

type PublicToolName = keyof typeof TOOL_SCOPES;

function validateOutputContractToolSet(): void {
  const expectedTools = Object.keys(TOOL_SCOPES).sort();
  const actualTools = Object.keys(OUTPUT_CONTRACT.toolOutputFamily).sort();
  if (JSON.stringify(expectedTools) !== JSON.stringify(actualTools)) {
    throw new Error("The generated public MCP output contract has a stale tool set.");
  }
  for (const toolName of expectedTools) {
    const family = OUTPUT_CONTRACT.toolOutputFamily[toolName];
    const schema =
      family === undefined
        ? undefined
        : OUTPUT_CONTRACT.outputSchemaFamilies[family];
    if (
      typeof family !== "string" ||
      !isPlainRecord(schema) ||
      schema.type !== "object" ||
      schema.additionalProperties !== false
    ) {
      throw new Error(
        `The generated public MCP output schema for ${toolName} is invalid.`,
      );
    }
  }
}

validateOutputContractToolSet();

const READ_ONLY_TOOLS = new Set<PublicToolName>([
  "get_change_file",
  "get_compiler_failures",
  "get_plan_preview",
  "job_status",
  "recover_revision",
  "verify_result",
]);
const APP_ONLY_TOOLS = new Set<PublicToolName>([
  "accept_plan_and_create_copy",
  "get_change_file",
  "recreate_original",
  "recover_revision",
]);
const MODEL_AND_APP_TOOLS = new Set<PublicToolName>([
  "get_plan_preview",
  "job_status",
  "keep_previous_proposal",
  "revise_plan",
  "verify_result",
]);

function objectSchema(
  properties: Record<string, unknown>,
  required: readonly string[],
): JsonSchema {
  return {
    additionalProperties: false,
    properties,
    required: [...required],
    type: "object",
  };
}

function tool(
  name: PublicToolName,
  title: string,
  description: string,
  inputSchema: JsonSchema,
): PublicToolDescriptor {
  const scope = TOOL_SCOPES[name];
  const securitySchemes = [{ scopes: [scope], type: "oauth2" as const }];
  const visibility = APP_ONLY_TOOLS.has(name)
    ? ["app"]
    : MODEL_AND_APP_TOOLS.has(name)
      ? ["model", "app"]
      : ["model"];
  const ui: Record<string, unknown> = { visibility };
  const meta: Record<string, unknown> = {
    securitySchemes,
    ui,
  };
  if (name === "get_plan_preview") {
    ui.resourceUri = WIDGET_RESOURCE_URI;
    meta["openai/outputTemplate"] = WIDGET_RESOURCE_URI;
    meta["openai/toolInvocation/invoked"] = "Foldweave preview ready";
    meta["openai/toolInvocation/invoking"] = "Loading the exact Foldweave preview";
  }
  if (APP_ONLY_TOOLS.has(name) || MODEL_AND_APP_TOOLS.has(name)) {
    meta["openai/widgetAccessible"] = true;
  }
  return {
    _meta: meta,
    annotations: {
      destructiveHint: false,
      idempotentHint: name !== "choose_local_item",
      openWorldHint: false,
      readOnlyHint: READ_ONLY_TOOLS.has(name),
    },
    description,
    inputSchema,
    name,
    outputSchema:
      OUTPUT_CONTRACT.outputSchemaFamilies[
        OUTPUT_CONTRACT.toolOutputFamily[name]!
      ]!,
    securitySchemes,
    title,
  };
}

const START_JOB_SCHEMA = objectSchema(
  {
    evidence_disclosure_acknowledged: { type: "boolean" },
    idempotency_key: IDEMPOTENCY_KEY,
    output_handle: OPAQUE_HANDLE,
    request: { maxLength: 20_000, minLength: 1, type: "string" },
    source_handle: OPAQUE_HANDLE,
  },
  [
    "source_handle",
    "output_handle",
    "request",
    "evidence_disclosure_acknowledged",
    "idempotency_key",
  ],
);

const AUTHORIZATION_SCHEMA = objectSchema(
  {
    authorization_context_fingerprint: SHA256,
    candidate_fingerprint: SHA256,
    expected_revision: NONNEGATIVE_INTEGER,
    idempotency_key: IDEMPOTENCY_KEY,
    imported_change_file_fingerprint: NULLABLE_SHA256,
    job_id: JOB_ID,
    match_report_fingerprint: NULLABLE_SHA256,
    preview_fingerprint: SHA256,
    proposal_revision: { maximum: 2, minimum: 0, type: "integer" },
    source_commitment: SHA256,
  },
  [
    "job_id",
    "proposal_revision",
    "source_commitment",
    "imported_change_file_fingerprint",
    "match_report_fingerprint",
    "authorization_context_fingerprint",
    "expected_revision",
    "preview_fingerprint",
    "candidate_fingerprint",
    "idempotency_key",
  ],
);

const FOLDER_PLAN_SCHEMA: JsonSchema = {
  $defs: {
    FolderPlan: {
      additionalProperties: false,
      properties: {
        entries: {
          default: [],
          items: { $ref: "#/$defs/FolderPlanEntry" },
          type: "array",
        },
        evidence_fingerprint: SHA256,
        evidence_schema_version: {
          const: "folder-evidence-ledger.v1",
          default: "folder-evidence-ledger.v1",
          type: "string",
        },
        exclusions: { items: { type: "string" }, type: "array" },
        request_fingerprint: SHA256,
        request_scope: {
          const: "rename_and_move_every_file",
          type: "string",
        },
        result_folder_name: { maxLength: 240, minLength: 1, type: "string" },
        schema_version: {
          const: "folder-plan.v1",
          default: "folder-plan.v1",
          type: "string",
        },
        source_commitment: SHA256,
      },
      required: [
        "source_commitment",
        "request_fingerprint",
        "request_scope",
        "evidence_fingerprint",
        "result_folder_name",
        "exclusions",
      ],
      type: "object",
    },
    FolderPlanEntry: {
      additionalProperties: false,
      properties: {
        evidence_ids: {
          items: { type: "string" },
          minItems: 1,
          type: "array",
        },
        file_id: SHA256,
        original_path: { maxLength: 4_096, minLength: 1, type: "string" },
        proposed_target: { maxLength: 1_024, minLength: 1, type: "string" },
        rationale: { maxLength: 1_000, minLength: 1, type: "string" },
      },
      required: [
        "file_id",
        "original_path",
        "proposed_target",
        "rationale",
        "evidence_ids",
      ],
      type: "object",
    },
  },
  ...objectSchema(
    { call_id: CALL_ID, job_id: JOB_ID, plan: { $ref: "#/$defs/FolderPlan" } },
    ["job_id", "call_id", "plan"],
  ),
};

const COMPACT_FOLDER_PLAN_SCHEMA: JsonSchema = {
  $defs: {
    FolderHostCompactPlanEntryV1: {
      additionalProperties: false,
      properties: {
        relative_path: {
          maxLength: 4_096,
          minLength: 1,
          type: "string",
          description:
            "Exact origin-relative_path from the hosted job inventory. Foldweave resolves it against the immutable durable inventory and derives the authoritative file_id locally.",
        },
        proposed_target: { maxLength: 1_024, minLength: 1, type: "string" },
      },
      required: ["relative_path", "proposed_target"],
      type: "object",
    },
  },
  ...objectSchema(
    {
      call_id: CALL_ID,
      entries: {
        items: { $ref: "#/$defs/FolderHostCompactPlanEntryV1" },
        maxItems: 500,
        type: "array",
      },
      job_id: JOB_ID,
      result_folder_name: { maxLength: 240, minLength: 1, type: "string" },
    },
    ["job_id", "call_id", "result_folder_name", "entries"],
  ),
};

const HOST_REVISION_SCHEMA: JsonSchema = {
  $defs: {
    FolderHostPlanRevisionEntryV1: {
      additionalProperties: false,
      properties: {
        evidence_ids: {
          description:
            'Use exact permitted evidence IDs. For a path-only revision use ["initial_inventory"]; never use a file ID or call ID.',
          items: { type: "string" },
          minItems: 1,
          type: "array",
        },
        file_id: {
          ...SHA256,
          description:
            "The exact preview member identifier; this is never an evidence ID.",
        },
        rationale: { maxLength: 1_000, minLength: 1, type: "string" },
        replacement_target_path: {
          maxLength: 1_024,
          minLength: 1,
          type: "string",
        },
      },
      required: [
        "file_id",
        "replacement_target_path",
        "rationale",
        "evidence_ids",
      ],
      type: "object",
    },
    FolderHostPlanRevisionV1: {
      additionalProperties: false,
      properties: {
        base_candidate_fingerprint: SHA256,
        entries: {
          default: [],
          items: { $ref: "#/$defs/FolderHostPlanRevisionEntryV1" },
          maxItems: 500,
          type: "array",
        },
        replacement_result_folder_name: {
          anyOf: [
            { maxLength: 240, minLength: 1, type: "string" },
            { type: "null" },
          ],
          default: null,
        },
        schema_version: {
          const: "folder-host-plan-revision.v1",
          default: "folder-host-plan-revision.v1",
          type: "string",
        },
      },
      required: ["base_candidate_fingerprint"],
      type: "object",
    },
  },
  ...objectSchema(
    {
      call_id: CALL_ID,
      job_id: JOB_ID,
      revision: { $ref: "#/$defs/FolderHostPlanRevisionV1" },
    },
    ["job_id", "call_id", "revision"],
  ),
};

export const PUBLIC_TOOL_DESCRIPTORS: PublicToolDescriptor[] = [
  tool(
    "choose_local_item",
    "Choose an item",
    "Call without selection_id to open one fixed-role picker in the paired local app. Then poll this tool with the returned selection_id until the status is terminal. Returns only an opaque handle, never a path.",
    objectSchema(
      {
        role: {
          enum: [
            "source_folder",
            "output_parent",
            "change_file",
            "restore_destination",
          ],
          type: "string",
        },
        selection_id: {
          anyOf: [LOCAL_SELECTION_ID, { type: "null" }],
          default: null,
        },
      },
      ["role"],
    ),
  ),
  tool(
    "create_or_resume_planning_job",
    "Start or resume planning",
    "Create one consented durable ChatGPT-hosted planning job from opaque local handles without calling the direct Responses API.",
    START_JOB_SCHEMA,
  ),
  tool(
    "plan_change",
    "Plan a folder change",
    "Start the same durable hosted planning workflow; the host still inspects bounded evidence and submits a complete plan.",
    START_JOB_SCHEMA,
  ),
  tool(
    "prepare_change_application",
    "Review a shared change",
    "Verify one Change File, deterministically match the selected local project, and stop at receiver review without model, API, or direct-budget use.",
    objectSchema(
      {
        change_file_handle: OPAQUE_HANDLE,
        idempotency_key: IDEMPOTENCY_KEY,
        output_handle: OPAQUE_HANDLE,
        source_handle: OPAQUE_HANDLE,
      },
      ["change_file_handle", "source_handle", "output_handle", "idempotency_key"],
    ),
  ),
  tool(
    "list_inventory_page",
    "View folder contents",
    "Read one deterministic page of path-relative metadata and return exact evidence identifiers for plan citations.",
    objectSchema(
      {
        call_id: CALL_ID,
        cursor: {
          anyOf: [
            { pattern: "^inv:[a-f0-9]{16}:[0-9]+$", type: "string" },
            { type: "null" },
          ],
          default: null,
        },
        job_id: JOB_ID,
        page_size: { default: 50, maximum: 100, minimum: 1, type: "integer" },
      },
      ["job_id", "call_id"],
    ),
  ),
  tool(
    "read_text_excerpt",
    "Read text excerpt",
    "Read one counted UTF-8 excerpt for an eligible stable file ID in the exact hosted job.",
    objectSchema(
      {
        call_id: CALL_ID,
        file_id: SHA256,
        job_id: JOB_ID,
        max_bytes: { maximum: 16_384, minimum: 1, type: "integer" },
        start_byte: NONNEGATIVE_INTEGER,
      },
      ["job_id", "call_id", "file_id", "start_byte", "max_bytes"],
    ),
  ),
  tool(
    "inspect_markdown_links",
    "Inspect links",
    "Read one deterministic page of supported relative Markdown-link relationships for an eligible file ID.",
    objectSchema(
      {
        call_id: CALL_ID,
        cursor: {
          anyOf: [
            { pattern: "^links:[a-f0-9]{16}:[0-9]+$", type: "string" },
            { type: "null" },
          ],
          default: null,
        },
        file_id: SHA256,
        job_id: JOB_ID,
        page_size: { default: 50, maximum: 100, minimum: 1, type: "integer" },
      },
      ["job_id", "call_id", "file_id"],
    ),
  ),
  tool(
    "request_clarification",
    "Ask a question",
    "Persist the one model-originated question for missing user intent; mechanical compiler failures are not clarifications.",
    objectSchema(
      {
        expected_revision: NONNEGATIVE_INTEGER,
        idempotency_key: IDEMPOTENCY_KEY,
        job_id: JOB_ID,
        question: { maxLength: 1_000, minLength: 1, type: "string" },
      },
      ["job_id", "expected_revision", "question", "idempotency_key"],
    ),
  ),
  tool(
    "answer_clarification",
    "Answer question",
    "Persist the user's exact answer only when the expected revision and question fingerprint still match.",
    objectSchema(
      {
        answer: { maxLength: 2_000, minLength: 1, type: "string" },
        expected_revision: NONNEGATIVE_INTEGER,
        idempotency_key: IDEMPOTENCY_KEY,
        job_id: JOB_ID,
        question_fingerprint: SHA256,
      },
      [
        "job_id",
        "expected_revision",
        "question_fingerprint",
        "answer",
        "idempotency_key",
      ],
    ),
  ),
  tool(
    "submit_plan",
    "Submit plan",
    "Compile one complete host-model plan deterministically and stop at review without creating output.",
    FOLDER_PLAN_SCHEMA,
  ),
  tool(
    "submit_compact_plan",
    "Submit compact plan",
    "Submit one complete origin-relative-path-to-target mapping; Foldweave resolves every path against the immutable durable inventory, derives job-owned fields, and invokes the same deterministic compiler without creating output.",
    COMPACT_FOLDER_PLAN_SCHEMA,
  ),
  tool(
    "get_compiler_failures",
    "View plan issues",
    "Read all bounded deterministic plan-submission failures for the exact hosted job without changing it.",
    objectSchema({ job_id: JOB_ID }, ["job_id"]),
  ),
  tool(
    "revise_plan",
    "Start a revision",
    "Use this when the user requests changes to the visible Foldweave preview. Reserve the exact revision first; the returned job ID is the only job ID valid for revision submission.",
    objectSchema(
      {
        candidate_fingerprint: SHA256,
        expected_revision: NONNEGATIVE_INTEGER,
        idempotency_key: IDEMPOTENCY_KEY,
        instruction: { maxLength: 2_000, minLength: 1, type: "string" },
        job_id: JOB_ID,
        preview_fingerprint: SHA256,
      },
      [
        "job_id",
        "expected_revision",
        "candidate_fingerprint",
        "preview_fingerprint",
        "instruction",
        "idempotency_key",
      ],
    ),
  ),
  tool(
    "recover_revision",
    "Recover pending revision",
    "Read one exact hosted revision after the review widget remounts. Bind recovery to the visible parent job revision, candidate, preview, and source; return no continuation for zero matches and block rather than choose when explicit forks are ambiguous.",
    objectSchema(
      {
        job_id: JOB_ID,
        parent_candidate_fingerprint: SHA256,
        parent_job_revision: NONNEGATIVE_INTEGER,
        parent_preview_fingerprint: SHA256,
        source_commitment: SHA256,
      },
      [
        "job_id",
        "parent_job_revision",
        "parent_candidate_fingerprint",
        "parent_preview_fingerprint",
        "source_commitment",
      ],
    ),
  ),
  tool(
    "submit_plan_revision",
    "Submit revision",
    "Use this after a Foldweave revision has already been reserved. Submit one strict sparse replacement for the reserved job; never execute or accept it.",
    HOST_REVISION_SCHEMA,
  ),
  tool(
    "get_plan_preview",
    "Show structure preview",
    "Use this when durable status contains a preview fingerprint. Pass the returned job ID, job revision, and preview fingerprint to render the exact current-versus-proposed review.",
    objectSchema(
      {
        expected_revision: NONNEGATIVE_INTEGER,
        job_id: JOB_ID,
        preview_fingerprint: SHA256,
      },
      ["job_id", "expected_revision", "preview_fingerprint"],
    ),
  ),
  tool(
    "job_status",
    "Check status",
    "Use this after revision submission or while polling durable work. Read the latest checkpoint without resuming work, calling a model, or creating output.",
    objectSchema({ job_id: JOB_ID }, ["job_id"]),
  ),
  tool(
    "keep_previous_proposal",
    "Keep previous proposal",
    "Dismiss one failed revision and rebind the preserved complete proposal to a fresh exact review checkpoint.",
    AUTHORIZATION_SCHEMA,
  ),
  tool(
    "accept_plan_and_create_copy",
    "Accept and create copy",
    "Persist exact fingerprint-bound user authorization, create a separate copy, and independently verify it without direct API use.",
    AUTHORIZATION_SCHEMA,
  ),
  tool(
    "verify_result",
    "Verify result",
    "Run the source-free deterministic receipt verifier for the exact durable result without model or direct-budget use.",
    objectSchema(
      { job_id: JOB_ID, organized_tree_commitment: SHA256 },
      ["job_id", "organized_tree_commitment"],
    ),
  ),
  tool(
    "get_change_file",
    "Get Change File",
    "Return one expiring opaque local item handle plus exact verified Change File and receipt identities, never a local path.",
    objectSchema({ job_id: JOB_ID }, ["job_id"]),
  ),
  tool(
    "recreate_original",
    "Recreate original",
    "Create or reverify the transaction's fixed absent sibling reconstruction destination without overwriting or exposing a local path.",
    objectSchema({ job_id: JOB_ID }, ["job_id"]),
  ),
];

const WIDGET_RESOURCE = {
  _meta: {
    "openai/widgetCSP": { connect_domains: [], resource_domains: [] },
    "openai/widgetDescription":
      "Foldweave's exact current-versus-proposed folder review, revision, acceptance, and verification surface.",
    "openai/widgetPrefersBorder": true,
    ui: {
      csp: { connectDomains: [], resourceDomains: [] },
      prefersBorder: true,
    },
  },
  description:
    "Render one exact current-versus-proposed Foldweave plan before the user authorizes a separate copy.",
  mimeType: WIDGET_MIME_TYPE,
  name: "foldweave_review",
  title: "Structure review",
  uri: WIDGET_RESOURCE_URI,
};

function publicWidgetResource(origin: string) {
  return {
    ...WIDGET_RESOURCE,
    _meta: {
      ...WIDGET_RESOURCE._meta,
      "openai/widgetCSP": {
        connect_domains: [],
        resource_domains: [origin],
      },
      "openai/widgetDomain": origin,
      ui: {
        csp: { connectDomains: [], resourceDomains: [origin] },
        domain: origin,
        prefersBorder: true,
      },
    },
  };
}

function publicWidgetHtml(origin: string): string {
  // Cloudflare's static-asset edge can retain an earlier bundle at the stable
  // path after a Worker deployment. Keep the readable filename while changing
  // this cache key whenever the widget resource contract changes.
  const assetCacheKey = "review-v37";
  const stylesheet = `${origin}/foldweave-chatgpt-widget.css?asset=${assetCacheKey}`;
  const javascript = `${origin}/foldweave-chatgpt-widget.js?asset=${assetCacheKey}`;
  return (
    '<!doctype html><html lang="en"><head><meta charset="utf-8">' +
    '<meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<meta name="color-scheme" content="light dark">' +
    '<title>Structure review</title>' +
    `<link rel="stylesheet" href="${stylesheet}"></head><body>` +
    '<div id="foldweave-chatgpt-widget-root"></div>' +
    `<script type="module" src="${javascript}"></script>` +
    "</body></html>"
  );
}

function requestId(value: Record<string, unknown>): JsonRpcId | undefined {
  if (!Object.prototype.hasOwnProperty.call(value, "id")) {
    return undefined;
  }
  const id = value.id;
  if (id === null || typeof id === "string") {
    return id;
  }
  if (typeof id === "number" && Number.isFinite(id)) {
    return id;
  }
  throw new HttpError(400, "mcp_request_invalid", "The JSON-RPC identifier is invalid.");
}

function rpcResponse(id: JsonRpcId, result: unknown, status = 200): Response {
  return jsonResponse(
    { id, jsonrpc: "2.0", result } as never,
    { status },
  );
}

function rpcError(
  id: JsonRpcId,
  code: number,
  message: string,
  status = 200,
): Response {
  return jsonResponse(
    { error: { code, message }, id, jsonrpc: "2.0" } as never,
    { status },
  );
}

function oauthChallenge(origin: string, scope: FoldweaveScope): string {
  return (
    `Bearer resource_metadata="${origin}/.well-known/oauth-protected-resource${PUBLIC_MCP_PATH}", ` +
    `scope="${scope}", error="insufficient_scope", ` +
    'error_description="Connect ChatGPT to the paired Foldweave app to continue"'
  );
}

function toolCallChallenge(
  id: JsonRpcId,
  request: Record<string, unknown>,
  origin: string,
): Response {
  if (!isPlainRecord(request.params) || typeof request.params.name !== "string") {
    return rpcError(id, -32602, "The tool call parameters are invalid.");
  }
  const name = request.params.name;
  if (!(name in TOOL_SCOPES)) {
    return rpcError(id, -32602, "The requested Foldweave tool is unavailable.");
  }
  const scope = TOOL_SCOPES[name as PublicToolName];
  return rpcResponse(id, {
    _meta: { "mcp/www_authenticate": [oauthChallenge(origin, scope)] },
    content: [
      {
        text: "Connect ChatGPT to the paired Foldweave app before using this tool.",
        type: "text",
      },
    ],
    isError: true,
  });
}

function protocolVersion(request: Record<string, unknown>): string {
  const params = request.params;
  if (
    isPlainRecord(params) &&
    typeof params.protocolVersion === "string" &&
    SUPPORTED_PROTOCOL_VERSIONS.has(params.protocolVersion)
  ) {
    return params.protocolVersion;
  }
  return LATEST_PROTOCOL_VERSION;
}

export async function handlePublicMcpDiscovery(request: Request): Promise<Response> {
  if (request.method === "DELETE") {
    return new Response(null, {
      headers: { "cache-control": "no-store" },
      status: 204,
    });
  }
  if (request.method !== "POST") {
    throw new HttpError(405, "method_not_allowed", "Public MCP discovery requires POST.");
  }
  const parsed = await readJsonBody(request, MAX_MCP_BODY_BYTES);
  if (!isPlainRecord(parsed) || parsed.jsonrpc !== "2.0" || typeof parsed.method !== "string") {
    throw new HttpError(400, "mcp_request_invalid", "Expected one JSON-RPC 2.0 request object.");
  }
  const id = requestId(parsed);
  if (id === undefined) {
    return new Response(null, {
      headers: { "cache-control": "no-store" },
      status: 202,
    });
  }
  const origin = new URL(request.url).origin;
  switch (parsed.method) {
    case "initialize":
      return rpcResponse(id, {
        capabilities: {
          resources: { listChanged: false, subscribe: false },
          tools: { listChanged: false },
        },
        instructions:
          "Foldweave uses OAuth to reach one paired local app. The model proposes; deterministic local code compiles, previews, executes only after exact user acceptance, and verifies a separate copy.",
        protocolVersion: protocolVersion(parsed),
        serverInfo: { name: "Foldweave", version: "1.0.0" },
      });
    case "ping":
      return rpcResponse(id, {});
    case "tools/list":
      return rpcResponse(id, { tools: PUBLIC_TOOL_DESCRIPTORS });
    case "tools/call":
      return toolCallChallenge(id, parsed, origin);
    case "resources/list":
      return rpcResponse(id, { resources: [publicWidgetResource(origin)] });
    case "resources/templates/list":
      return rpcResponse(id, { resourceTemplates: [] });
    case "resources/read": {
      const requestedResourceUri = isPlainRecord(parsed.params)
        ? parsed.params.uri
        : null;
      if (
        typeof requestedResourceUri !== "string" ||
        !READABLE_WIDGET_RESOURCE_URIS.has(requestedResourceUri)
      ) {
        return rpcError(id, -32602, "The requested Foldweave resource is unavailable.");
      }
      return rpcResponse(id, {
        contents: [
          {
            _meta: publicWidgetResource(origin)._meta,
            mimeType: WIDGET_MIME_TYPE,
            text: publicWidgetHtml(origin),
            uri: requestedResourceUri,
          },
        ],
      });
    }
    default:
      return rpcError(id, -32601, "The requested public MCP discovery method is unavailable.");
  }
}

export function publicMcpScopes(): readonly string[] {
  return SUPPORTED_SCOPES;
}
