# Foldweave Codex plugin

This thin plugin exposes Foldweave's bounded host-planning and reviewed
workflow tools to Codex. It contains no second planner, job store, receipt,
verifier, reconstruction engine, budget ledger, or generic filesystem tool.
Every operation dispatches into the same local deterministic engine used by the
native application, browser fallback, and CLI.

## Install from a clean clone

From the repository root:

1. Run `uv sync --frozen`.
2. Set `CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"`.
3. Run `"$CODEX_BIN" plugin marketplace add .`.
4. Run `"$CODEX_BIN" plugin add foldweave@personal`.
5. Refresh or restart Codex.
6. Start a new Codex task whose working directory is this clean repository
   clone.

The explicit path is the tested macOS binary bundled with ChatGPT desktop. It
avoids accidentally invoking an older `codex` shim on `PATH`. A bare `codex`
command is suitable only when `codex plugin --help` resolves successfully.

The installed plugin copy contributes only the manifest and relative MCP
configuration. The MCP command launches
`uv run --frozen foldweave mcp --transport stdio` from the task's clean
checkout; it contains no absolute developer path and requires no runtime Node
process.

## Use

The shared server provides two bounded tool families.

Host-planning tools let Codex create or resume a durable planning job, inspect
only the job-bound inventory and supported evidence, submit a complete plan or
sparse revision, inspect deterministic compiler failures, and retrieve the one
immutable preview. The family includes:

- `create_or_resume_planning_job`
- `list_inventory_page`
- `read_text_excerpt`
- `inspect_markdown_links`
- `request_clarification`
- `submit_plan`
- `submit_plan_revision`
- `get_compiler_failures`
- `get_plan_preview`

Reviewed workflow tools prepare origin or receiver work, expose durable status,
preserve a valid proposal after a failed revision, bind exact acceptance to the
visible preview, and use the existing proof services. The family includes:

- `plan_change`
- `prepare_change_application`
- `job_status`
- `answer_clarification`
- `revise_plan`
- `keep_previous_proposal`
- `accept_plan_and_create_copy`
- `get_change_file`
- `verify_result`
- `recreate_original`

Codex supplies model inference for Codex-hosted planning. That mode does not
read a direct Responses API key and does not reserve or mutate Foldweave's
direct-API budget ledger. Deterministic Change File preparation and unchanged
application, preview rendering, verification, and reconstruction remain
model-free.

No result is created while a job is under review. Execution requires acceptance
of the exact candidate and preview fingerprints. Mutation tools bind an
idempotency key and expected job revision so a retry cannot create duplicate
work. Poll the durable handle with `job_status`; if the job requests its sole
clarification, answer the exact displayed question before continuing. The
selected source is never modified in place.

## Uninstall

Run `"$CODEX_BIN" plugin remove foldweave@personal`. If this repository
marketplace is no longer needed, run
`"$CODEX_BIN" plugin marketplace remove personal`.
