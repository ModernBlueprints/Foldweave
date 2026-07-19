# Reversible Name Atlas Codex plugin

This thin plugin exposes the same seven high-level Name Atlas operations used
by the browser and CLI. It contains no second planner, job store, receipt,
verifier, reconstruction engine, or generic filesystem tool.

The plugin runs the Name Atlas MCP server from the current clean repository
checkout. Use Python 3.11 and run `uv sync --frozen` in that checkout first.

## Install from a clean clone

From the repository root:

1. Run `uv sync --frozen`.
2. Run `codex plugin marketplace add .`.
3. Run `codex plugin add name-atlas@personal`.
4. Refresh or restart Codex.
5. Start a new Codex task whose working directory is this repository clone.

The installed plugin copy contributes the manifest and relative MCP
configuration. The MCP command then launches `uv run --frozen name-atlas mcp`
from the task's clean Name Atlas checkout.

## Use

The plugin exposes:

- `plan_and_create_copy`
- `job_status`
- `answer_clarification`
- `get_change_file`
- `apply_change_file`
- `verify_result`
- `recreate_original`

Planning requires literal acknowledgement of the plugin's outbound-evidence
and retention disclosure. Live planning reads `OPENAI_API_KEY` only from the
local process environment. Keyless replay, Change File application,
verification, and reconstruction do not require that key.

Every mutating start or answer uses a caller idempotency key. Poll the returned
durable handle with `job_status`; if the job requests its single clarification,
send the exact displayed question fingerprint, expected revision, and answer
through `answer_clarification`, then continue polling.

## Uninstall

Run `codex plugin remove name-atlas@personal`. If this repository marketplace
is no longer needed, run `codex plugin marketplace remove personal`.
