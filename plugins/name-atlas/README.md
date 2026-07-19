# Reversible Name Atlas Codex plugin

This thin plugin exposes the same seven high-level Name Atlas operations used
by the browser and CLI. It contains no second planner, job store, receipt,
verifier, reconstruction engine, or generic filesystem tool.

The plugin runs the Name Atlas MCP server from the current clean repository
checkout. Use Python 3.11 and run `uv sync --frozen` in that checkout first.

## Install from a clean clone

From the repository root:

1. Run `uv sync --frozen`.
2. Set `CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"`.
3. Run `"$CODEX_BIN" plugin marketplace add .`.
4. Run `"$CODEX_BIN" plugin add name-atlas@personal`.
5. Refresh or restart Codex.
6. Start a new Codex task whose working directory is this repository clone.

The explicit path is the tested macOS binary bundled with ChatGPT desktop. It
avoids accidentally invoking an older `codex` shim on `PATH`. A bare `codex`
command is suitable only when `codex plugin --help` resolves successfully.

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

Every mutation uses a caller idempotency key: origin start, Change File
application, the clarification answer, and reconstruction. An identical retry
returns the same durable authority; conflicting reuse blocks. Reconstruction
reuses the job's originating start/application key and remains no-replace. Poll
the returned durable handle with `job_status`; if the job requests its single
clarification, send the exact displayed question fingerprint, expected
revision, answer, and answer idempotency key through `answer_clarification`,
then continue polling.

## Uninstall

Run `"$CODEX_BIN" plugin remove name-atlas@personal`. If this repository
marketplace is no longer needed, run
`"$CODEX_BIN" plugin marketplace remove personal`.
