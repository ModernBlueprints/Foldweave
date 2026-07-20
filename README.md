# Reversible Name Atlas

**Describe the change once. Apply it wherever the same project exists.**

*AI planning once. Deterministic execution everywhere.*

Reversible Name Atlas is a local-first application for reorganizing connected
project folders. You describe the result you want in plain English. GPT-5.6
plans the complete rename and folder move once; fixed code checks that every
file admitted by the supported folder contract is accounted for, creates a
separate verified result, and keeps the supported Markdown links working.

Name Atlas then creates a **Name Atlas Change File**. Another person who has an
equivalent copy of the same project—even if their copy starts under different
local names and folders—can apply that file without another GPT call, without
an API key, and without transferring the project files themselves.

## The problem

A project folder is often more than a pile of unrelated files. Notes link to
presentations, briefings link to research, and delivery instructions point to
approved material. A normal bulk rename can move the files while silently
breaking those connections. Asking an AI assistant to perform the same cleanup
twice can also produce two different arrangements.

Consider a small agency handing a project from Sofia to Martin:

- Sofia has the Apollo project organized around `approved/`, `working/`,
  `research/`, and `notes/`.
- Martin has the same logical files, but his local copy uses different names
  such as `ready/`, `drafts/`, `evidence/`, and `conversations/`.
- Both copies contain Markdown notes whose relative links reflect their own
  starting layouts.
- They want one consistent Northstar handoff without uploading the project to
  each other or asking AI to reinterpret the task twice.

A list of shell moves is not enough: it is tied to one starting layout. A copy
of Sofia's finished folder is also not enough when Martin must keep and verify
his own local source. Name Atlas records the *logical change* and the proof
needed to apply it to an equivalent copy within the supported contract, without
guessing.

## The Sofia-to-Martin story

### 1. Sofia organizes the project

Sofia opens the local browser application, chooses **Organize a folder**, and
enters:

> Prepare this Apollo client-project folder for handoff as Northstar. Keep every file. Use the briefing and project notes to organize approved deliverables, working material, research, and meeting notes into clear folders. Rename Apollo-labelled paths to Northstar and keep every supported link working.

The origin transaction is:

```text
local folder
  → plain-English request
  → bounded GPT-5.6 investigation
  → complete proposed plan
  → deterministic compilation
  → optional one-question clarification
  → separate verified result
  → Name Atlas Change File
```

GPT-5.6 may inspect only the bounded relative-path and eligible text evidence
made available by Name Atlas. It cannot write, move, delete, verify, or approve
files. Fixed code rejects incomplete, duplicate, invented, stale, colliding, or
otherwise invalid plans before any final result is accepted.

For the included hero, Name Atlas keeps all 24 files exactly once, changes 23
paths, rewrites and verifies 23 supported Markdown links, keeps the protected
`.env.example` at its original relative path, and creates a separate Northstar
result. Sofia's original folder remains unchanged.

### 2. Sofia shares the Change File

The generated `northstar.nameatlas-change.json` is a strict, fingerprinted JSON
file containing the change and its originating proof—not a copy of the project.

> The Change File contains no project payload bytes. It does contain project names and structure, file sizes and hashes, supported link relationships, the original instruction, target names, and proof identifiers.

Therefore the accurate privacy statement is **No project payload bytes are
transferred.** Name Atlas does not claim that nothing about the project is
shared.

### 3. Martin applies the same change

Martin chooses **Apply a shared change**, selects Sofia's Change File and his
differently arranged equivalent project folder, then chooses **Apply change and
create copy**.

The receiver transaction is:

```text
Name Atlas Change File
  + differently arranged equivalent local project
  → keyless deterministic matching
  → receiver-local complete plan
  → separate verified result
  → independent verification
  → receiver-specific reconstruction
```

This receiver path makes no GPT or provider call, reads no API key, reserves no
AI budget, makes no external network request, and transfers no project payload
bytes. The browser still communicates with its own loopback server on the same
computer.

Name Atlas matches ordinary files from intrinsic payload facts and the
supported Markdown relationship graph, never by guessing from Sofia's or
Martin's ordinary source path or from arbitrary filesystem order. Protected
members and explicit empty directories keep their exact-path requirements. If
duplicates remain indistinguishable, a payload changed, a relationship changed,
or any file is extra or missing, the entire application blocks. When it
succeeds, Sofia and Martin receive the same organized-tree commitment while
each original folder remains unchanged.

## What the application looks like

The standard release is a server-rendered FastAPI/Jinja application on the
local loopback interface. It uses locally packaged Blueprint assets and minimal
JavaScript.

- **Home** offers **Organize a folder** and **Apply a shared change**.
- **Organize** provides a macOS native folder picker, editable path fallback,
  plain-English request, derived result location, exact GPT evidence disclosure,
  and **Plan and create copy**.
- **Apply** provides Change File and project pickers, editable path fallback,
  result location, the no-GPT/no-key/no-external-network statement, and **Apply
  change and create copy**.
- **Working** shows truthful origin-specific stages. Organize identifies live or
  recorded GPT-5.6 planning; Apply shows deterministic matching and never a fake
  GPT stage.
- **Done** leads with **Your new folder is ready**, plain counts and verification
  facts, then offers **Show in Finder**, **Download Change File**, **See
  changes**, **View proof**, **Verify again**, and **Recreate original layout**.

The native picker and Finder bridge are bounded macOS conveniences. Manual paths
remain the supported fallback and judge-automation path. Responsive narrow
layout does not mean that Name Atlas is a mobile application or provides remote
phone access.

## Quick start: bundled keyless demonstration

Prerequisites:

- Python 3.11; and
- [`uv`](https://docs.astral.sh/uv/).

The tested Build Week judge path is macOS with Python 3.11. Native Windows is not
a tested release claim.

From a clean clone:

```text
git clone https://github.com/ModernBlueprints/reversible-name-atlas.git
cd reversible-name-atlas
uv sync --frozen
uv run name-atlas demo --mode replay
```

Open <http://127.0.0.1:8000>. The first clean run opens Home with the bundled
Sofia/Martin fixture. Choose **Organize a folder** to run the exact recorded hero
planning transaction. Replay mode needs no API key and makes no provider call.
The UI labels it **Recorded GPT-5.6 planning run**.

The replay is bound to the exact fixture, request, schemas, evidence, tool
sequence, and accepted plan. It fails closed for another source. The durable job
is stored under `.name-atlas/connected-demo/replay`; restarting the same command
resumes that exact job and may open directly on its current or completed state.

## Live planning for another local folder

Live origin planning requires `OPENAI_API_KEY` in the launching environment. Do
not place a key in this repository, shell history, screenshots, logs, receipts,
Change Files, MCP arguments, or chat.

Run the bundled live hero:

```text
uv run name-atlas demo --mode live
```

Or prepopulate a local folder, output parent, and durable job:

```text
uv run name-atlas run \
  --mode live \
  --source "/absolute/path/to/project" \
  --output "/absolute/path/to/output-parent" \
  --job "/absolute/path/to/jobs/project.json" \
  --port 8000
```

Live mode uses the exact `gpt-5.6` alias through the Responses API, strict tool
schemas, `store=false`, no provider retry, and no fallback model. `store=false`
means Name Atlas does not ask the Responses API to retain the response for later
application retrieval; OpenAI's standard abuse-monitoring and prompt-caching
retention may still apply.

Name Atlas sends only the disclosed instruction, relative paths and folder
structure, local-binding metadata, selected excerpts from eligible UTF-8 text
and Markdown files, and supported Markdown-link context. It does not send every
file's bytes, absolute local paths, protected contents, opaque binary contents,
or hidden reasoning.

## Apply a Change File from the CLI

Change File application dispatches before planner, credential, provider, and AI
budget initialization:

```text
uv run name-atlas apply-change \
  "/absolute/path/northstar.nameatlas-change.json" \
  --source "/absolute/path/to/martin-project" \
  --output "/absolute/path/to/result-parent" \
  --job "/absolute/path/to/jobs/martin.json"
```

`--output` and `--job` are optional. The default output is
`.name-atlas/folder-results`, and the default job is a new UUID-named file below
`.name-atlas/jobs/`. An identical retry against the same job returns the same
durable result; conflicting reuse blocks.

A successful command prints:

```text
VERIFIED <receiver-receipt-fingerprint>
JOB <durable-job-path>
RESULT <verified-result-path>
CHANGE_FILE <verified-change-file-path>
CHANGE_FILE_FINGERPRINT <fingerprint>
ORIGINATING_RECEIPT <origin-receipt-fingerprint>
```

## Verify a result independently

Verify an origin or receiver result without its local job, browser, source
folder, GPT, API key, or external network:

```text
uv run name-atlas verify-receipt RESULT_BAG
```

The verifier writes nothing. Exit `0` prints `VERIFIED <receipt-fingerprint>`;
exit `1` prints `BLOCKED <stable-failed-check-ids>`; exit `2` indicates usage or
candidate-input failure.

If the corresponding source is available, add a current byte-and-path
comparison:

```text
uv run name-atlas verify-receipt RESULT_BAG \
  --source "/absolute/path/to/source-root"
```

Source-free verification proves internal consistency against the source
description committed by the receipt. It does not prove historical
authenticity, sender identity, authorship, or institutional authorization.

## Recreate the original layout

Reconstruction first verifies the result and requires an absent destination:

```text
uv run name-atlas restore-receipt \
  RESULT_BAG \
  "/absolute/path/to/absent-original-layout"
```

The origin result reconstructs Sofia's source layout. A receiver result
reconstructs that receiver's own original paths and exact in-scope bytes—so
Martin gets Martin's starting layout, not Sofia's. The command leaves the source,
verified result, and Change File unchanged and promotes only after complete
proof.

The bounded claim covers in-scope relative paths and bytes. It does not restore
timestamps, ownership, ACLs, extended attributes, resource forks, symlink or
hard-link identity, undeclared references, or arbitrary filesystem state.

## What is supported

The selected folder must contain 1–500 readable regular files and at most 1,000
directories. Name Atlas includes hidden files and explicit empty directories,
but blocks before planning on symlinks, special files, unreadable members,
hard-linked regular files, changing input, unsafe overlap, or inadequate free
space.

Every admitted source file maps to exactly one result file:

- no deletion or omission;
- no merge or deduplication;
- no duplicate output copy;
- no invented user file;
- no extraction or conversion; and
- no direct source mutation.

Dotfiles, members below dot-directories or version-control directories, common
credential filenames, and key/certificate/password-vault suffixes are protected.
They remain in the complete inventory, stay at their exact original relative
path, and never expose their contents to GPT.

Name Atlas uses a bounded cross-platform-safe naming profile, not a claim of
universal filesystem portability. Renameable files keep their exact protected
suffix. Exact, NFC, and Unicode-casefold collisions and file/directory ancestor
conflicts block.

### Supported Markdown connections

The release rewrites only a narrow, testable subset in UTF-8 `.md` and
`.markdown` files:

- inline links and inline images;
- relative local file targets, including lexically safe in-root `../` paths;
- optional fragments; and
- UTF-8 percent encoding.

It ignores external URLs and anchor-only links. It blocks unsupported local
constructs, reference-style local links, query strings, absolute/root-relative
paths, root escape, dangling or case-mismatched targets, malformed escapes,
directory targets, and ambiguous relationships. Exact-span rewriting preserves
all bytes outside accepted destination spans.

PDF, Office, spreadsheet, image, audio, video, archive, and other opaque files
can be carried byte-for-byte, but Name Atlas does not claim to understand their
content or update embedded references inside them.

## Portable verified result

An accepted result is a BagIt-backed portable folder:

```text
<verified-result>/
├── data/          # the reorganized project the user opens
└── name-atlas/    # plan, Change File, maps, proof, receipt, and restore data
```

Portable artifacts use relative paths only. They include the complete source
description, request, observable planning or capsule-application origin,
accepted plan, supported relationship graph, forward/reverse maps, change
ledger, verification report, receipt, offline proof page, exact original bytes
for rewritten Markdown files, and the Change File. Receiver results also contain
their deterministic match report.

Origin and receiver receipts are different because they prove different local
transactions. Their final organized-tree commitments are identical when the
same Change File is successfully applied to an equivalent project.

The Change File and receipt use canonical SHA-256 fingerprints and acyclic
commitments. This supports integrity and internal-consistency checks. It is not a
digital signature, sender authentication, tamper-proofing, or proof that the
producer's historical source was authentic.

## Shared MCP server

Start the required local STDIO MCP server with:

```text
uv run foldweave mcp --transport stdio
```

STDOUT is MCP protocol only; diagnostics go to STDERR. One shared server exposes
two bounded tool families backed by the same durable job, compiler, copy,
receipt, verifier, and reconstruction services as the native application,
browser fallback, and CLI:

- host-planning tools for bounded inventory and evidence inspection, complete
  plan submission, sparse revision, compiler feedback, and immutable preview;
- reviewed workflow tools for origin planning, receiver preparation, durable
  status, clarification, revision recovery, exact fingerprint-bound acceptance,
  Change File retrieval, verification, and reconstruction.

Codex supplies model inference for Codex-hosted planning, so that mode neither
reads a direct Responses API key nor reserves Foldweave's direct-API budget.
Unchanged Change File preparation and application, preview rendering,
verification, and reconstruction remain model-free. Mutations require caller
idempotency keys and expected revisions. The server exposes no arbitrary
filesystem read/write/move/delete, shell, compiler bypass, receipt construction,
proof override, or provider credential tool.

## Codex plugin

The thin Foldweave Codex plugin packages the same shared MCP server; it does not
copy or replace the product implementation.

Install from a clean clone:

```text
uv sync --frozen
CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"
"$CODEX_BIN" plugin marketplace add .
"$CODEX_BIN" plugin add foldweave@personal
```

Refresh or restart Codex, then open a **new Codex task whose working directory
is that clean repository clone**. The discovered Foldweave tools use
`uv run --frozen foldweave mcp --transport stdio` from the task checkout. Codex
hosted planning uses Codex's model inference; deterministic unchanged Change
File application, verification, and reconstruction remain model-free.

The explicit `CODEX_BIN` is the tested macOS command from the ChatGPT desktop
bundle and avoids an unrelated or stale `codex` shim earlier on `PATH`. A bare
`codex` command is equivalent only when `codex plugin --help` resolves to a
current installation that supports the plugin subcommand.

Uninstall with:

```text
"$CODEX_BIN" plugin remove foldweave@personal
"$CODEX_BIN" plugin marketplace remove personal
```

Codex is the tested plugin/MCP client for this release. Other MCP hosts are not
called tested unless separately exercised.

## Exact judge and maintainer commands

Run from the repository root:

```text
uv sync --frozen
uv run name-atlas demo --mode replay
uv run name-atlas demo --mode live
uv run name-atlas run --mode live --source SOURCE_ROOT --output OUTPUT_PARENT --job JOB_FILE --port 8000
uv run name-atlas apply-change CHANGE_FILE --source SOURCE_ROOT --output OUTPUT_PARENT --job JOB_FILE
uv run name-atlas verify-receipt RESULT_BAG
uv run name-atlas verify-receipt RESULT_BAG --source SOURCE_ROOT
uv run name-atlas restore-receipt RESULT_BAG RESTORE_DESTINATION
uv run name-atlas mcp
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## Recording-ready product evidence

At selected product commit
`e10b09a941567d3394c71dbb5dbc3a25c74f1a82`, published on both `main` and
`revision/ai-first-folder-refactor`:

- the selected profile is `CONNECTED_CHANGE_GO`;
- the 24-file zero-question hero used one real exact `gpt-5.6` planning run,
  returned `gpt-5.6-sol`, used three response turns and 16 bounded evidence
  calls, and produced an exact sanitized replay;
- the four-file ambiguity case used one real exact `gpt-5.6` planning run,
  asked exactly one concise question, accepted one answer, and produced an exact
  sanitized replay;
- the keyless Sofia-to-Martin transaction verified both results, made zero
  receiver provider/API/budget/external-network calls, converged to organized
  tree `a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`,
  and reconstructed Martin's source exactly;
- the refusal matrix blocked changed payload, changed Markdown prose, changed
  supported relationship, protected-member disagreement, symmetric duplicates,
  invalid Change File fingerprint, and a BagIt-valid receipt inconsistency;
- the shared MCP server passed direct integration and a real Codex invocation;
- the thin plugin passed official validation, clean-clone install, fresh-task
  discovery, real `verify_result` invocation from the installed copy, keyless
  replay, reconstruction, missing-live-key behavior, and uninstall;
- the final **249-test release matrix** and complete **822-test** regression
  suite passed from a fresh public HTTPS clone; lock, Ruff lint, Ruff format
  over 154 files, Git whitespace checks, an isolated installed-wheel replay,
  source-free and source-aware verification, exact reconstruction, and the
  explicit named-job regression also passed; and
- the cumulative project ledger remained under its USD 10 authority: 9 of 13
  request attempts, USD 9.736060 conservative committed exposure, and USD
  0.605515 reported estimated cost.

These are checkpoint facts, not claims of production readiness, universal model
reliability, or performance on every admitted folder.

## Claim boundaries

The demonstrated central claim is:

> GPT-5.6 plans the connected-folder change once, and Name Atlas can deterministically apply and verify the same change on a differently arranged equivalent copy without another GPT call or transfer of project payload bytes.

Name Atlas may also state, for the demonstrated supported contract, that every
in-scope file is accounted for exactly once, protected files remain fixed,
supported Markdown links reach the same logical files, originals remain
unchanged, ambiguous duplicates block instead of being guessed, origin and
receiver results converge, and each receiver can reconstruct its own starting
layout.

Name Atlas does **not** claim:

- semantic equivalence or reconciliation of independently edited copies;
- reconciliation when a receiver has extra or missing files;
- general graph isomorphism or semantic-similarity matching;
- universal format understanding, connection preservation, portability, or
  reversibility;
- image, audio, video, PDF, Office, or spreadsheet semantic understanding;
- source-code, import, database, or application-aware refactoring;
- native Windows testing, a mobile application, or remote phone access;
- zero API retention, full privacy, or that nothing about the project is
  disclosed;
- sender identity, authorship, signatures, institutional authorization,
  historical authenticity, tamper-proofing, compliance, or production
  readiness;
- universal zero-question behavior, unmeasured time savings, broad adoption,
  support for untested MCP clients, competitor nonexistence, or a probability of
  winning.

The complete frozen contract is [docs/build/BUILD_SPEC.md](docs/build/BUILD_SPEC.md),
and the public limitation surface is [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

## How GPT-5.6 and Codex are used

Runtime GPT-5.6 is central to origin planning. It investigates bounded evidence,
submits a complete structured plan, repairs mechanically rejected plans within
fixed limits, and may ask one tightly scoped clarification when user intent is
genuinely missing. It never mutates files, approves its own result, bypasses
fixed checks, or participates in receiver application and verification.

Deterministic Name Atlas code owns scanning, stable identities, protected-file
rules, exact Markdown parsing and rewriting, complete plan compilation, naming
and collision checks, persistent jobs, copy-only staging, Change Files,
receipts, independent verification, and reconstruction.

Codex with GPT-5.6 was the primary development environment and integrator. One
primary task translated frozen contracts into vertical product slices, built and
tested the application, reproduced proof failures, delegated bounded independent
reviews, inspected browser behavior, and qualified the shared MCP server and
installed plugin. This is a factual development account, not an unmeasured speed
claim. See [docs/CODEX_BUILD_LOG.md](docs/CODEX_BUILD_LOG.md) for the chronological
record.

## Fixtures, provenance, and licenses

The primary release fixtures are under
[sample_data/connected_change](sample_data/connected_change). Sofia and Martin
contain synthetic equivalent 24-file projects in different layouts; the
ambiguity fixture is a separate four-file one-question case. Opaque examples
are synthetic and demonstrate byte-preserving carriage only.

Fixture provenance is recorded in [sample_data/README.md](sample_data/README.md).
The boundary between pre-existing feasibility work and this implementation is
recorded in [docs/PREEXISTING_WORK.md](docs/PREEXISTING_WORK.md). The application
has no runtime or test dependency on the earlier ephemeral spike and does not
reuse its semantic/evaluator machinery.

Reversible Name Atlas is distributed under the [MIT License](LICENSE). Locally
packaged Blueprint assets retain their Apache-2.0 notice and exact provenance in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
