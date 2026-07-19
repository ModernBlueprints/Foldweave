# Reversible Name Atlas — Build Week submission package

Status: **C6 DRAFT — FEATURE-FROZEN `CONNECTED_CHANGE_GO`; RELEASE MATERIALS
ARE BEING REGENERATED; NOT RECORDING-READY; NOT SUBMITTED**

Submission hold: **ACTIVE — FINAL DEVPOST SUBMISSION IS PROHIBITED UNTIL THE
USER EXPLICITLY RELEASES THE HOLD**

This is the working C6 package for the final judge path, Devpost draft, media
plan, claim audit, and due-diligence pass. It is not product authority and does
not prove release acceptance. Product truth remains in
[`build/BUILD_SPEC.md`](build/BUILD_SPEC.md); execution evidence and status
remain in [`build/IMPLEMENTATION_PLAN.md`](build/IMPLEMENTATION_PLAN.md) and
[`build/STATE.md`](build/STATE.md).

No release SHA, wheel digest, screenshot digest, final receipt identity, public
video URL, or final test count may be added here until it has been reproduced
from the accepted C6/C7 checkpoint. The C5 evidence below is explicitly a
feature-freeze baseline, not a release-candidate claim.

## Official requirement snapshot

Rechecked Sunday 19 July 2026 against the
[Official Rules](https://openai.devpost.com/rules),
[FAQ](https://openai.devpost.com/details/faqs), and
[dates page](https://openai.devpost.com/details/dates):

- the submission period closes **Wednesday 22 July 2026 at 02:00 CEST**;
- the entry must be a working project built with Codex and GPT-5.6 and select
  one track;
- the selected track is **Work & Productivity**;
- the text description must explain the project's features and functionality;
- the repository must be available for judging and testing with relevant
  licensing;
- the README must provide setup, sample/testing guidance, specific Codex
  contributions, key decisions, and the role of GPT-5.6;
- the primary Codex task's `/feedback` Session ID is required;
- the public YouTube demonstration must include a clear working demo with
  audio, explain what was built and how Codex and GPT-5.6 were used, and remain
  under three minutes;
- plugin/developer-tool surfaces require installation instructions, supported
  platforms, and a judge path that does not require rebuilding the product from
  scratch;
- pre-existing and third-party work must be disclosed accurately; and
- the equally weighted judging criteria are Technological Implementation,
  Design, Potential Impact, and Quality of the Idea.

The official sources remain controlling. The user must personally confirm
eligibility, entrant type, country, ownership, representative authority when
applicable, and every other personal or legal attestation.

## Submission identity and pending fields

| Field | C6 draft value or status |
|---|---|
| Project | **Reversible Name Atlas** |
| Primary tagline | **Describe the change once. Apply it wherever the same project exists.** |
| Secondary line | **AI planning once. Deterministic execution everywhere.** |
| Track | **Work & Productivity** |
| Category | **AI refactoring for connected project folders** |
| One-line summary | GPT-5.6 plans a connected-folder reorganization once; Name Atlas can then apply and verify the same change on a differently arranged equivalent copy without another GPT call or transfer of project payload bytes. |
| Public repository | <https://github.com/ModernBlueprints/reversible-name-atlas> — final public release SHA pending C6/C7 acceptance |
| License | MIT; third-party notices and packaged licenses must pass final clean-clone inspection |
| Selected product profile | `CONNECTED_CHANGE_GO` |
| C5 feature-freeze checkpoint | `0dc4776495cd708278d835c8394dcd9529be981e` — baseline evidence only |
| C6 release-candidate SHA | `[PENDING C6 ACCEPTANCE]` |
| C7 recording-ready SHA | `[PENDING C7 ACCEPTANCE]` |
| Final origin receipt | `[PENDING FINAL C6/C7 TRANSACTION]` |
| Final receiver receipt | `[PENDING FINAL C6/C7 TRANSACTION]` |
| Final Change File fingerprint | `[PENDING FINAL C6/C7 TRANSACTION]` |
| Final organized-tree commitment | `[PENDING FINAL C6/C7 TRANSACTION]` |
| Final screenshot and thumbnail hashes | **RECORDED BELOW — independent media audit GO** |
| Devpost software page | <https://devpost.com/software/reversible-name-atlas> — existing public copy is stale and must be replaced before submission |
| Public YouTube URL | `[PENDING FINAL CAPTURE AND PUBLIC UPLOAD; USER ACTION ONLY IF LOGIN/MFA/CAPTCHA IS REQUIRED]` |
| `/feedback` Session ID | `[USER ACTION REQUIRED: run /feedback in the primary Codex build task]` |
| Entrant type and country | `[USER ACTION REQUIRED: confirm; do not infer]` |
| Eligibility and ownership attestations | `[USER ACTION REQUIRED: read and personally attest]` |
| Submission-hold release | `[USER ACTION REQUIRED: explicitly release only after every prerequisite passes]` |
| Devpost submission | **NOT PERFORMED** |

### Final media hashes

These are the visually accepted C6 assets. Exactly seven genuine PNGs remain
under `docs/screenshots/`; the superseded archive-oriented gallery is preserved
only in Git history.

| Asset | Dimensions | SHA-256 |
|---|---:|---|
| `docs/screenshots/01-home.png` | 1280×720 | `dfff82fdc558451b4d1c21d7cd6e9073831dc828ec9dc1436e9f61e8a54ad812` |
| `docs/screenshots/02-organize.png` | 1280×1492 | `8f860ec73e6279beb054b09b70229e2a6facae6b9f0a005b067a4844e8151ef6` |
| `docs/screenshots/03-planning.png` | 1280×720 | `9b1bc2d7e8f2d85a61918951d618767ae7f8ff078c7519586fd534c4f2baad47` |
| `docs/screenshots/04-origin-done.png` | 1280×1672 | `84ec5b7f0a69be3447c741ad44338cb8abad923b0004771cd41448663a54e650` |
| `docs/screenshots/05-apply.png` | 1280×1446 | `468d7ed73531b9c88900c85d23e78f8077ab12d3d8badd0d910b0a79f0131c0c` |
| `docs/screenshots/06-receiver-done.png` | 1280×1672 | `f0aa7b946bdd42b74d3d7696239d4351de2373231b58b14cf0c69ab2ddc01757` |
| `docs/screenshots/07-mcp-plugin.png` | 1280×720 | `314ac7f4135e7c0131190d508100a173d322efadabc4d3ae35ded9acbc70a725` |
| `docs/submission-thumbnail.svg` | 1500×1000 view box | `3a6b2e56bda6a5e5ce5a4a44d7561cbc7837bc46f6d2c61ee97e16cfe166c810` |
| `docs/submission-thumbnail.png` | 1500×1000 | `0382fd0c9c15a89688b821496b7baad20633bb427cec74383735848327085515` |

## Product case

### The problem

A project folder is often more than a pile of independent files. Notes link to
presentations, images, research, meeting records, and working material. A person
can ask an AI assistant to reorganize one copy, but another teammate may hold
the same logical project under different local names and folders. Repeating the
AI task can produce a different result, cost another model call, and silently
break supported links.

The hard part is not moving files. It is carrying one complete change across
equivalent copies without guessing which file is which, losing a file, changing
the source, or trusting an unverified AI-authored batch of filesystem actions.

### The solution

Reversible Name Atlas is a local-first application for connected project
folders. A user selects a folder and describes the desired organization in
plain English. GPT-5.6 investigates bounded path and selected text evidence and
returns a complete proposed plan. Fixed code requires every in-scope file to be
accounted for exactly once, validates every destination, rewrites the supported
relative Markdown links, creates a separate result, and independently verifies
the outcome.

The verified origin result includes a **Name Atlas Change File**. The Change
File contains no project payload bytes, but it does disclose project names and
structure, file sizes and hashes, supported link relationships, the original
instruction, target names, and proof identifiers.

Another person can combine that Change File with a differently arranged but
equivalent local copy. Name Atlas matches the files deterministically and
creates that person's separate verified result with:

- no GPT or provider call;
- no API key or budget reservation;
- no external network request; and
- no transfer of project payload bytes.

The browser still uses loopback HTTP on the local computer. The receiver claim
is therefore **no external network request**, not an unqualified “no network”
claim.

### The Sofia and Martin story

Sofia is preparing the Apollo client project for a Northstar handoff. Her
folder contains 24 regular files, an explicit empty directory, ordinary text
and Markdown notes, and opaque files such as images, audio, PDF, spreadsheet,
and binary material. Name Atlas understands only paths and selected eligible
text/Markdown evidence; opaque formats are carried byte-for-byte.

Sofia chooses her folder and asks:

> Prepare this Apollo client-project folder for handoff as Northstar. Keep every file. Use the briefing and project notes to organize approved deliverables, working material, research, and meeting notes into clear folders. Rename Apollo-labelled paths to Northstar and keep every supported link working.

GPT-5.6 plans the complete change without asking Sofia a question. Fixed code
compiles the plan, preserves the protected file, accounts for all 24 admitted
files exactly once, updates 23 supported links, leaves the source unchanged,
and creates a verified Northstar result plus a Change File.

Martin has the same logical project, but his copy begins with different local
paths. He selects Sofia's Change File and his own folder. Name Atlas matches the
equivalent content and supported relationship structure without using either
person's ordinary source paths as matching evidence. It creates a separate
verified result whose organized-tree commitment equals Sofia's result.

Martin can then recreate his own original paths and bytes. He does not recreate
Sofia's original layout. If a payload, Markdown prose, supported relationship,
protected member, Change File fingerprint, or symmetrical duplicate group does
not match, Name Atlas blocks instead of guessing.

### Why this is different

The core product is not another bulk renamer or chat wrapper. GPT-5.6 provides
bounded semantic planning once. Deterministic code owns complete file
accounting, target validation, matching, rewriting, copy-only execution,
receipts, verification, convergence, and reconstruction everywhere.

The portable Change File turns one successful plan into a repeatable,
inspectable change without moving the underlying project files between people
and without asking another model to reinterpret the request.

### Potential impact

The immediate audience is anyone preparing a complicated project folder for
handoff or reuse: consultants, researchers, educators, journalists, designers,
photographers, small agencies, preservation workers, and technically capable
enthusiasts.

The demonstrated benefit is specific: one person can define a connected-folder
reorganization in ordinary language, while another can reproduce the same
verified result on an equivalent differently arranged copy. The release does
not claim measured time savings, broad adoption, production readiness, or
support for independently edited copies.

## How the product works

### 1. Origin planning

The user selects an ordinary local folder, describes only renaming and folder
grouping, acknowledges the outbound-evidence disclosure, and chooses **Plan and
create copy**.

GPT-5.6 may receive the exact instruction, relative file names and folder
structure, basic metadata needed to bind the plan, selected excerpts from
eligible text and Markdown files, and supported link context. It does not
receive every file's bytes, protected contents, opaque binary/media/document
contents, raw payload hashes, or absolute local paths.

Name Atlas sets `store=false`; it does not ask OpenAI to retain the response as
retrievable Responses API application state. Standard abuse-monitoring and
prompt-caching retention may still apply.

### 2. Deterministic compilation and copy

GPT submits a structured plan, not shell commands or direct filesystem
operations. The compiler verifies that each planner-eligible file appears
exactly once, injects protected files and empty directories unchanged, checks
the naming and path tree, derives exact Markdown destination replacements, and
creates an immutable accepted plan.

The source is never renamed, edited, or deleted. Name Atlas copies into an
absent pending result, rewrites only accepted Markdown destination spans,
preserves the original bytes of every rewritten Markdown file, proves the
transaction, validates the BagIt container, and promotes the result without
replacement only after every required check passes.

### 3. Name Atlas Change File

The origin result stores the exact envelope at
`name-atlas/connected_change_capsule.json`. The browser streams those same
verified bytes as the standalone download `northstar.nameatlas-change.json`;
it does not claim a second copy inside the result. The file is strict,
fingerprinted JSON and contains the complete deterministic description needed
to match and reproduce the change, not the project files themselves.

### 4. Keyless receiver application

The receiver selects the Change File and an equivalent local project folder.
Name Atlas strictly verifies the file, scans the receiver source, refines
deterministic equivalence classes from payload descriptors and supported link
relationships, accepts only unique mappings, rebinds the plan to receiver-local
file identities, and runs the same compiler and copy transaction.

Extra, missing, changed, protected, incompatible, or ambiguous input is a
terminal blocker. A mismatch never invokes GPT or becomes a user clarification.

### 5. Proof and reconstruction

Origin and receiver results each have their own receipt. Their source
commitments differ, while their final organized-tree commitments agree. The
source-free verifier needs no job, browser, GPT, API key, external network, or
original source and writes nothing.

**Recreate original layout** verifies first and creates another absent folder
matching that receiver's own original relative paths and bytes. It does not
restore timestamps, ownership, permissions, ACLs, extended attributes,
resource forks, symlinks, hard-link identity, or undeclared references.

## Exact judge paths

### Fastest browser path — keyless recorded demonstration

Prerequisites: macOS, Python 3.11, and `uv`.

From a clean clone:

1. `git clone https://github.com/ModernBlueprints/reversible-name-atlas.git`
2. `cd reversible-name-atlas`
3. `uv sync --frozen`
4. `uv run name-atlas demo --mode replay`
5. Open <http://127.0.0.1:8000>.

Replay uses the bundled 24-file synthetic hero and the exact sanitized record
from a real GPT-5.6 planning run. It is labeled **Recorded GPT-5.6 planning
run**, needs no API key, and makes no provider request.

Use the browser journeys:

- **Organize a folder** → Working → Done to inspect the origin result and
  download the Change File.
- **Apply a shared change** with the downloaded Change File and the bundled
  differently arranged Martin fixture → Working → Done to inspect the keyless
  receiver result.
- On Done, use **Verify again** and **Recreate original layout**.

The product provides a bounded native macOS folder/file picker and keeps manual
editable paths as the judge-automation and unsupported-platform fallback.

### Live origin planning

Configure `OPENAI_API_KEY` only in the launching environment, never in source,
command arguments, screenshots, logs, chat, or committed files. Then run:

`uv run name-atlas demo --mode live`

or:

`uv run name-atlas run --mode live --source SOURCE_ROOT [--output OUTPUT_PARENT] [--job JOB_FILE] [--port PORT]`

Live mode uses exact alias `gpt-5.6`, records the returned model identity, sets
`store=false`, and has no fallback model or provider retry. The release judge
path does not require a live key because replay is complete and keyless.

### Direct Change File application

`uv run name-atlas apply-change CHANGE_FILE --source SOURCE_ROOT [--output OUTPUT_PARENT] [--job JOB_FILE]`

This command dispatches before planner, provider, credential, and budget
initialization. It creates a new separate result and never edits the selected
source or Change File.

### Independent verification and reconstruction

- `uv run name-atlas verify-receipt RESULT_BAG`
- `uv run name-atlas verify-receipt RESULT_BAG --source SOURCE_ROOT`
- `uv run name-atlas restore-receipt RESULT_BAG RESTORE_DESTINATION`

The verifier is source-free by default. `--source` adds a current comparison to
the committed source description; it does not authenticate historical origin.
The reconstruction destination must not already exist.

### Shared MCP server

Run:

`uv run name-atlas mcp`

The STDIO server exposes exactly:

- `plan_and_create_copy`
- `job_status`
- `answer_clarification`
- `get_change_file`
- `apply_change_file`
- `verify_result`
- `recreate_original`

It exposes no arbitrary file read/write/move/delete, shell, direct planner
evidence tools, compiler bypass, receipt construction, or proof override.
Planning requires literal acknowledgement of the outbound-evidence and
retention disclosure. Mutations use persisted idempotency keys and durable jobs;
polling status cannot trigger a provider call.

### Codex plugin

From the final clean clone:

1. `uv sync --frozen`
2. `CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"`
3. `"$CODEX_BIN" plugin marketplace add .`
4. `"$CODEX_BIN" plugin add name-atlas@personal`
5. Refresh or restart Codex.
6. Start a new Codex task whose working directory is the clean clone.
7. Ask Codex to use a Name Atlas tool, for example to verify an existing result
   or apply a Change File.

The plugin is a thin package around the same MCP server. It contains no second
planner, job store, receipt, verifier, reconstruction engine, budget ledger, or
generic filesystem tool.

Uninstall with:

`"$CODEX_BIN" plugin remove name-atlas@personal`

If the local marketplace is no longer needed:

`"$CODEX_BIN" plugin marketplace remove personal`

Codex on macOS is the tested plugin client. Other MCP hosts are not called
tested unless separately exercised. The explicit binary path is the tested
ChatGPT desktop bundle and avoids an unrelated or stale `codex` shim on `PATH`;
a bare command is equivalent only when `codex plugin --help` succeeds.

### Maintainer checks

- `uv lock --check`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .`
- `git diff --check`

Final C6 acceptance must run these commands from an unrelated clean clone and
must also inspect the built wheel, package assets, secrets, absolute paths,
browser viewports, Change File transaction, refusal matrix, MCP, and installed
plugin.

## Technology list

- Codex with GPT-5.6 as the primary development environment and integrator;
- GPT-5.6 through the OpenAI Responses API for bounded origin planning;
- strict OpenAI function calling and structured output schemas;
- Python 3.11;
- FastAPI and Uvicorn;
- Jinja2 server-rendered HTML;
- Pydantic v2 strict contracts;
- official Python MCP SDK `mcp>=1.27,<2`;
- one shared STDIO MCP server and one thin Codex plugin;
- locally packaged Blueprint core and icons under their included license;
- vanilla JavaScript and CSS;
- Library of Congress `bagit`;
- SHA-256 and standard-library filesystem primitives;
- macOS `osascript` and `open` for bounded local picker/Finder bridges;
- `uv` and a committed lockfile;
- pytest and Ruff; and
- Git and GitHub.

The browser product uses no React, Vite, Node judge step, native desktop wrapper,
hosted service, account system, or cloud synchronization.

## How GPT-5.6 is used

GPT-5.6 is central to the origin transaction. It receives bounded, observable
evidence through five read-only/terminal tools: inventory paging, eligible text
excerpts, supported Markdown-link inspection, plan submission, and one optional
clarification request.

It plans every planner-eligible file, proposes one result-folder name and one
target per file, explains each mapping, and cites evidence. It cannot write,
move, delete, approve, verify, omit a file, bypass the compiler, or promote a
result.

Current C5 qualification includes:

- one real zero-question `gpt-5.6` hero run;
- one real one-question `gpt-5.6` ambiguity run;
- exact returned model identity `gpt-5.6-sol` for both;
- three Responses API turns for each run;
- sixteen evidence calls for the hero and four for the ambiguity case;
- one exact answer in the ambiguity case and no second question;
- sanitized exact replays for both successful transactions; and
- no credential, response ID, absolute local path, hidden reasoning, or
  unrelated account data in the committed records.

The deterministic compiler, Change File matching, copy transaction, receipt,
verification, and reconstruction do not trust model confidence or hidden
reasoning.

## How Codex was used

Codex was the primary development environment for the project. The user chose
and repeatedly refined the product direction, accepted the frozen contracts,
and retained authority over the final voice, personal attestations, `/feedback`,
submission hold, and final submission.

In the primary Codex task, Codex:

- translated product decisions into one frozen specification and one vertical
  implementation sequence;
- built the ordinary-folder scanner, protected-member policy, exact Markdown
  parser, planner tool schemas, persistent jobs, copy transaction, receipts,
  source-free verifier, and reconstruction engine;
- implemented and corrected the path-independent Change File matcher against a
  complete Sofia/Martin transaction and refusal matrix;
- built the Home/Organize/Apply browser experience and bounded macOS bridge;
- integrated the real GPT-5.6 planner, one-question continuation, sanitized
  replays, and the sole budget ledger;
- implemented the seven-tool shared MCP server with consent, durable polling,
  and idempotency;
- used the official plugin workflow, installed the plugin from a public clean
  clone, refreshed into new Codex tasks, and invoked the installed copy;
- delegated bounded non-overlapping reviews, reproduced material findings, and
  converted valid defects into regression tests; and
- maintained a continuously runnable product while preserving immutable
  predecessor checkpoints and accurate claims.

This is a qualitative, evidence-backed account. It is not a percentage speedup,
measured productivity claim, or claim that Codex independently chose the
product direction.

## Current C5 evidence — baseline only

The following evidence was complete at feature freeze. It must be rerun or
consumed by the final C6 clean-clone acceptance before any release-candidate
claim:

- selected profile: `CONNECTED_CHANGE_GO`;
- 24-file zero-question origin transaction and one-question ambiguity
  transaction;
- 23 supported hero links accounted for;
- differently arranged Sofia/Martin receiver transaction with zero receiver
  provider/API/budget/external-network authority;
- identical origin/receiver organized-tree commitment;
- receiver-specific exact reconstruction;
- refusals for changed payload, changed Markdown prose, changed relationship,
  protected disagreement, symmetric duplicate, and Change File fingerprint;
- BagIt-valid accepted-plan alteration blocked by
  `artifact_digest_mismatch:accepted_plan`;
- shared MCP direct transaction and real Codex MCP invocation;
- admitted plugin installed and invoked from an isolated clean-clone cache;
- keyless installed-plugin replay, verification, Change File retrieval, and
  reconstruction;
- missing-live-key behavior `live_credential_missing` without budget change;
- **16 focused plugin/MCP tests**;
- **811 complete regression tests**;
- `uv lock --check` with 48 packages;
- Ruff lint, Ruff format over 153 files, and `git diff --check` passed; and
- C5 feature-freeze checkpoint
  `0dc4776495cd708278d835c8394dcd9529be981e`.

These numbers and fingerprints are C5 checkpoint evidence. The final public
copy must use only freshly accepted C6/C7 results.

## Devpost description draft

### Inspiration

Project folders contain connections: notes point to deliverables, research,
images, and meeting records. Reorganizing one copy with AI is easy. Reproducing
the same change on another teammate's differently arranged copy—without
guessing, breaking supported links, or asking the model again—is not.

We wanted a change that could travel without the project files themselves and
could still be checked independently.

### What it does

Reversible Name Atlas lets a user select an ordinary project folder and explain
the desired organization in plain English. GPT-5.6 investigates bounded paths,
selected eligible text, and supported Markdown-link context, then submits a
complete structured plan.

Deterministic code requires every in-scope file exactly once, keeps protected
files fixed, validates every target, updates the demonstrated relative Markdown
links, leaves the source unchanged, and creates a separate verified result.

The result includes a payload-free Name Atlas Change File. Another person can
apply that file to a differently arranged equivalent copy without GPT, an API
key, a budget reservation, an external network request, or transfer of project
payload bytes. Name Atlas blocks changed or ambiguous copies rather than
guessing. Both verified results converge to the same organized tree, while each
person can recreate their own original layout.

### How we built it

The local application uses Python 3.11, FastAPI, Jinja2, Pydantic v2, the
OpenAI Responses API, the official Python MCP SDK, Library of Congress `bagit`,
and locally packaged Blueprint assets.

Strict versioned records bind the source, observable planner transcript,
accepted plan, Change File, receiver match report, maps, rewritten Markdown,
verification, and reconstruction. Atomic writes, process locking, optimistic
revisions, repeated source scans, no-replace promotion, canonical SHA-256
fingerprints, and a separate source-free verifier keep the model outside proof
authority.

The same domain services power the browser, CLI, seven-tool STDIO MCP server,
and thin Codex plugin.

### How GPT-5.6 is used

GPT-5.6 performs bounded origin planning through strict tools. It can inspect
relative inventory, eligible text excerpts, and supported link context; submit
one complete plan; and ask at most one essential question. It cannot mutate the
source, omit a file, execute arbitrary operations, approve its own plan, or
override verification.

The repository includes exact sanitized replays from one real zero-question
run and one real one-question run. Replay is visibly labeled, keyless, and
fails closed if its fixture, request, schemas, evidence, or fingerprint differs.

### How Codex was used

Codex with GPT-5.6 was the primary development environment and integrator. One
primary task converted frozen product contracts into dependency-ordered
vertical slices, built and connected the planner, matcher, browser, receipt,
verifier, reconstruction, MCP, and plugin surfaces, ran the real GPT
transactions, exercised clean-clone and installed-copy paths, and turned
adversarial review findings into regression tests.

The user made the product and scope decisions. Codex made the implementation
coherent, continuously runnable, and evidence-backed.

### Challenges and accomplishments

The hardest problem was matching equivalent projects without using either
person's ordinary source path as evidence. Name Atlas builds deterministic
classes from exact payload descriptors, Markdown non-destination bytes, and
ordered link relationships, then refines them to a fixed point. It accepts only
unique matches. Symmetric duplicates block.

The strongest demonstration is convergence: Sofia and Martin begin with
different source commitments, use one GPT-planned Change File, keep both
sources unchanged, independently verify both results, reach the same organized
tree, and can each recreate their own original paths and bytes.

### What we learned

AI is most useful here when it plans intent but does not control proof. A
portable change becomes credible only when fixed code accounts for every
in-scope file, refuses ambiguity, and lets another person verify and reverse
their own transaction without another model call.

### What's next

After Build Week, honest next steps are user testing, measured scale and
workflow studies, and evidence-based support for additional narrowly specified
connection types. Independently edited-copy reconciliation, semantic similarity
matching, arbitrary code refactoring, cloud synchronization, and production
hardening are not part of this release.

## Devpost field draft

| Field | Draft value |
|---|---|
| Project name | `Reversible Name Atlas` |
| Tagline | `Describe the change once. Apply it wherever the same project exists.` |
| Category | `Work & Productivity` |
| Repository | `https://github.com/ModernBlueprints/reversible-name-atlas` — confirm final public HEAD after C7 |
| Technologies | `Codex, GPT-5.6, OpenAI Responses API, Python 3.11, FastAPI, Jinja2, Pydantic v2, MCP Python SDK, Codex Plugin, Blueprint, BagIt, uv, pytest, Ruff, CSS, GitHub` |
| Testing instructions | `On macOS with Python 3.11 and uv: run uv sync --frozen, then uv run name-atlas demo --mode replay and open http://127.0.0.1:8000. The bundled Sofia/Martin transaction and recorded GPT-5.6 planning run require no API key. The README also documents direct Change File, verifier, reconstruction, MCP, and Codex-plugin paths.` |
| Supported platform | `Local browser/CLI/MCP on tested macOS; manual path fields support judge automation. No native Windows test claim.` |
| Public YouTube URL | `[PENDING FINAL CAPTURE AND PUBLIC UPLOAD; USER ACTION ONLY IF LOGIN/MFA/CAPTCHA IS REQUIRED]` |
| `/feedback` Session ID | `[USER ACTION REQUIRED]` |
| Submitter type | `[USER CONFIRM: Individual / Team of Individuals / Organization]` |
| Country | `[USER CONFIRM; DO NOT INFER]` |
| Selected release SHA | `[PENDING C7]` |
| Submission hold | `ACTIVE — FINAL SUBMIT PROHIBITED UNTIL EXPLICIT USER RELEASE` |

## Three-minute demonstration storyboard

Target exported duration: **2:55**. The final file must remain strictly below
3:00 after audio, transitions, and encoding. Do not speed unreadable footage to
meet the limit.

| Time | Visual and action | Narration purpose |
|---:|---|---|
| 0:00–0:12 | Title and a project note linking to several files | A project folder contains relationships, not just filenames. |
| 0:12–0:30 | Home → **Organize a folder**; native picker selects Sofia's folder | The user chooses a normal folder and describes the change. |
| 0:30–0:52 | Sofia's exact Northstar request and bounded evidence disclosure; press **Plan and create copy** | GPT-5.6 receives only the declared bounded planning evidence. |
| 0:52–1:10 | Working: **Recorded GPT-5.6 planning run** and deterministic checking stages | The exact recorded AI plan is shown; fixed code checks every in-scope file and destination. |
| 1:10–1:25 | Origin Done: 24 files, 23 links, source unchanged, verification passed | Sofia receives a separate verified result. |
| 1:25–1:45 | Download `northstar.nameatlas-change.json`; show the plain disclosure | The transferable file contains proof metadata, not project payload bytes. |
| 1:45–2:05 | Home → **Apply a shared change**; select Change File and Martin's differently arranged folder | Martin applies the same change without GPT, key, or external request. |
| 2:05–2:22 | Receiver Working → Done; show matching, verification, and equal organized-tree identity | Different starting paths converge without guessing. |
| 2:22–2:40 | **Verify again**, **Recreate original layout**, then one refusal or proof detail | Proof is independent; Martin can recreate his own original and ambiguity blocks. |
| 2:40–2:55 | Codex plugin tool result, test/commit overlay, repository end card | Specific Codex, GPT-5.6, MCP, and implementation contribution. |

## Timed plain-English voice-over draft

Target spoken duration: **approximately 2:35–2:50** with natural pauses. The
actual recording and exported video must be timed; word-count estimates are not
acceptance evidence.

> A project folder is more than filenames. Notes connect reports, research,
> meetings, and working files. A teammate may hold the same project under
> different local paths.
>
> Reversible Name Atlas lets us describe the change once and apply it wherever
> that same supported project exists.
>
> Sofia selects her Apollo folder and requests a Northstar handoff: keep all
> twenty-four admitted files, separate approved work, research, and drafts, and
> preserve supported Markdown links.
>
> Name Atlas first discloses the bounded evidence: instruction, relative
> structure, metadata, selected eligible text, and supported links—not protected
> content, opaque payloads, or absolute paths.
>
> This recorded GPT-5.6 run shows the plan from that evidence. The model proposes
> destinations but cannot move or verify anything. Fixed code requires all
> twenty-four files once, preserves the protected member, validates destinations,
> and derives link updates.
>
> Name Atlas creates a separate verified result. Sofia's source is unchanged and
> all twenty-three supported links still reach the same logical files.
>
> She downloads a Name Atlas Change File. It contains no project payload bytes,
> but it does disclose names, structure, sizes, hashes, link relationships, the
> instruction, target names, and proof identifiers.
>
> Martin has the same supported project under different local paths. He selects
> Sofia's Change File and his folder. This step makes no GPT call, needs no API
> key, reserves no model budget, and makes no external network request.
>
> Ordinary files match by exact bytes. Markdown notes match by unchanged text and
> supported link relationships, though destinations may differ. Ordinary matches
> never use Sofia's path, Martin's path, or arbitrary order. Protected files and
> explicit empty directories keep required paths. Changed or ambiguous copies
> block.
>
> Martin's new folder verifies independently and reaches the same organized
> tree as Sofia's. He can recreate his own original paths and bytes without
> changing either source or result.
>
> Codex with GPT-5.6 was the primary development environment. One main task
> integrated the planner, matcher, browser, receipts, verifier, reconstruction,
> MCP server, and installed plugin, turning adversarial findings into tests.
> GPT-5.6 plans once; deterministic execution and proof travel everywhere.
>
> Reversible Name Atlas. Describe the change once. Apply it wherever the same
> project exists.

### Voice-over ownership and acceptance

- Final narrator/voice recording: `[USER ACTION REQUIRED]`
- Final recorded duration: `[PENDING; EXPORTED VIDEO MUST BE UNDER 3:00]`
- Audio intelligibility: `[PENDING]`
- Every spoken claim checked against the selected release: `[PENDING]`
- User approval of final audio: `[PENDING]`

## Capture shot list

1. Use the final accepted clean-clone checkout and a neutral working directory.
2. Record the browser at the final 1280×720 product viewport or a larger clean
   capture that exports readably to 1920×1080.
3. Use the final keyless replay for the narrated origin. Show the exact label
   **Recorded GPT-5.6 planning run**; do not make another provider call for
   recording.
4. Use the bundled 24-file Sofia/Martin fixture and the final accepted Change
   File, receipts, verifier result, and reconstruction.
5. Show the disclosure before planning. Do not say that no project content is
   sent to GPT; selected eligible excerpts are part of the bounded evidence.
6. Show true origin-specific stages. The receiver Apply flow must never display
   a GPT-planning stage.
7. Prepare the receiver result and one truthful refusal/proof surface before
   capture so the terminal does not reveal shell history or unrelated paths.
8. Show only synthetic data. Exclude personal paths, account identifiers,
   notifications, secrets, response IDs, private tabs, and unrelated files.
9. If the plugin is shown, use the accepted installed-copy path in a new Codex
   task and display one real high-level Name Atlas tool result.
10. Keep technical hashes collapsed unless one is needed to demonstrate
    convergence or independent proof.
11. Use no copyrighted music, third-party footage, or unlicensed promotional
    asset. Retain required notices in the repository.
12. Export under three minutes, watch the complete local file with audio, upload
    it as Public on YouTube, and watch the complete public playback before
    entering the URL in Devpost.

## Final screenshot replacement specification

The existing archive-oriented images are stale and cannot ship as current
product evidence. Replace them with this final Connected Change set from the
accepted C6/C7 release:

| Final path | Required frame | Acceptance requirement |
|---|---|---|
| `docs/screenshots/01-home.png` | Home at 1280×720 | **Organize a folder** and **Apply a shared change**, exact tagline, no active job, no personal path |
| `docs/screenshots/02-organize.png` | Sofia Organize form | Native picker/manual fallback, exact request, source-untouched statement, evidence disclosure control, **Plan and create copy** |
| `docs/screenshots/03-planning.png` | Origin Working | Visible **Recorded GPT-5.6 planning run** label, truthful recorded planning and deterministic checking stages; no fake live call or completion |
| `docs/screenshots/04-origin-done.png` | Sofia Done | 24 files, changed-path/link counts, source unchanged, verification passed, Change File download and proof/reconstruction actions |
| `docs/screenshots/05-apply.png` | Martin Apply | Change File and project folder selection, derived result, exact no-GPT/no-key/no-external-request statement |
| `docs/screenshots/06-receiver-done.png` | Martin Done | Verified receiver result, Change File identity, source unchanged, convergence and receiver-specific reconstruction |
| `docs/screenshots/07-mcp-plugin.png` | Recorded installed-plugin acceptance evidence | Evidence card derived from the preserved real installed-copy task: discovered Name Atlas tool, one invocation, verified result, no developer absolute path or secret; explicitly not a reconstruction of Codex UI |

Each final PNG must be genuine image bytes, visually inspected, hash-recorded,
free of personal metadata/paths/secrets, and readable at the recording viewport.
The Home, Organize, Apply, Working, and Done UI must also pass the final
390×844 no-overflow, keyboard, focus, and contrast review.

### Final gallery thumbnail

Regenerate both:

- `docs/submission-thumbnail.svg`
- `docs/submission-thumbnail.png`

Required design:

- 1500×1000, 3:2;
- established dark Name Atlas visual system;
- title **Reversible Name Atlas**;
- headline **Describe the change once. Apply it wherever the same project exists.**;
- secondary line **AI planning once. Deterministic execution everywhere.**;
- simple Sofia folder → Name Atlas Change File → Martin folder visual;
- no Migration Case, archive-family, derivative, decision-ledger, or old receipt
  imagery;
- no invented digest presented as product evidence;
- no third-party promotional imagery; and
- final PNG/SVG hashes recorded only after visual and file inspection.

## Limitations and public claim boundaries

Public copy may claim only what the selected release demonstrates:

- GPT-5.6 plans one bounded connected-folder change from paths and selected
  eligible text/Markdown evidence;
- deterministic checks account for every in-scope file exactly once;
- protected files stay at their original relative paths;
- the source remains unchanged and a separate result is created;
- demonstrated supported relative Markdown links are rewritten and verified;
- the Name Atlas Change File carries no project payload bytes;
- another equivalent differently arranged copy can apply the Change File
  without GPT, an API key, a budget reservation, or an external network request;
- changed or ambiguous copies block;
- origin and receiver results converge to the same organized-tree commitment;
- source-free keyless verification checks internal consistency; and
- each receiver can recreate its own original layout and bytes within the
  supported contract.

The release does not claim:

- semantic equivalence or semantic correctness;
- reconciliation of independently edited, extra-file, or missing-file copies;
- general graph isomorphism or semantic-similarity matching;
- universal file-format understanding;
- image, audio, video, PDF, Office, or spreadsheet semantic understanding;
- code-aware refactoring or preservation of arbitrary imports/configuration;
- arbitrary connection preservation;
- universal filesystem portability or reversibility;
- native Windows testing, a mobile application, or remote phone file access;
- zero API retention, full privacy, or that nothing about the project is
  disclosed;
- sender identity, authorship, institutional authorization, signatures,
  historical authenticity, or tamper-proofing;
- compliance, production readiness, broad adoption, or measured time savings;
- universal zero-question behavior;
- tested support for MCP clients not actually exercised;
- absence of competitors, proven superiority, or probability of winning.

Important supported-scope boundaries:

- 1–500 regular files and at most 1,000 directories;
- at most 16 MiB per `.md`/`.markdown` file and 10,000 supported local Markdown
  references;
- regular files/directories only; symlinks, special files, hard-linked regular
  files, unsupported paths, unreadable members, overlap, insufficient capacity,
  and source change block;
- rename/move-only complete-file transaction; no deletion, omission, merge,
  deduplication, extraction, conversion, or arbitrary body editing;
- exact inline Markdown link/image subset, including lexically safe in-root
  parent-relative targets; reference-style links and unsupported local-looking
  syntax block;
- matching requires exact supported content/relationship agreement and unique
  deterministic classes; symmetrical duplicates block; and
- reconstruction covers in-scope relative paths and bytes, not arbitrary
  filesystem metadata or undeclared state.

## Claim-to-evidence audit

| Public claim | Required evidence | C6 draft status |
|---|---|---|
| GPT-5.6 plans the origin change | New real zero-question transcript, exact alias/returned model, observable tools, accepted plan, replay binding | `C5 VERIFIED; FINAL C6 REPLAY/RUN PENDING` |
| One essential clarification works | Real one-question transcript, one answer, accepted plan, replay, no second question | `C5 VERIFIED; FINAL C6 REPLAY PENDING` |
| Every in-scope file is present once | Inventory/accepted-plan/result bijection and source equality | `C5 VERIFIED; FINAL C6 TRANSACTION PENDING` |
| Supported links survive | Exact-span proof, same logical target IDs, final staged bytes | `C5 VERIFIED FOR 23 HERO LINKS; FINAL C6 PROOF PENDING` |
| Change File transfers no project payload bytes | Strict schema/content audit and raw file inspection | `C5 VERIFIED; FINAL C6 ARTIFACT AUDIT PENDING` |
| Receiver uses no GPT/API/budget/external network | `capsule_applied` provenance, zero counts, unchanged budget, dependency isolation | `C5 VERIFIED; FINAL C6 RECEIVER RUN PENDING` |
| Differently arranged copies converge | Different source commitments and identical organized-tree commitment | `C5 VERIFIED; FINAL C6 SOFIA/MARTIN RUN PENDING` |
| Changed or ambiguous copies block | Complete payload/Markdown/relationship/protected/duplicate/fingerprint refusal matrix | `C5 VERIFIED; FINAL C6 MATRIX PENDING` |
| Result verifies without source or key | Unrelated-location source-free verifier, no writes, exact receipt | `C5 VERIFIED; FINAL C6 RESULT PENDING` |
| Each receiver recreates its own original | Verify-first no-replace reconstruction and exact receiver snapshot equality | `C5 VERIFIED; FINAL C6 RECONSTRUCTION PENDING` |
| Shared MCP is the same product engine | Seven-tool direct run, consent/idempotency, durable polling, no duplicated core | `C4/C5 VERIFIED; FINAL CLEAN-CLONE CHECK PENDING` |
| Codex plugin is installed and usable | Public clean clone, install, refresh/new task, discovery, installed-copy invocation, uninstall | `C5 VERIFIED; FINAL C6 CLEAN-CLONE CHECK PENDING` |
| Complete regression passes | Fresh final suite, lock, lint, format, build, wheel, paths/secrets, Git | `C5 BASELINE 811; FINAL C6 COUNT PENDING` |
| Public release is judge-ready | Selected SHA, public alignment, clean HTTPS clone, exact commands and media | `PENDING C6/C7` |
| Video and submission are complete | Public playback, `/feedback`, attestations, hold release, Devpost confirmation | `USER ACTIONS AND FINAL CLOSURE PENDING` |

## Due-diligence checklist

### Product and repository

- [x] `CONNECTED_CHANGE_GO` selected and feature-frozen
- [x] C5 shared MCP and admitted plugin acceptance preserved
- [ ] C6 release-candidate SHA selected
- [ ] Final branch and public repository alignment verified
- [ ] Exact public HTTPS clone checked from an unrelated path
- [ ] `uv sync --frozen` passes in that clone
- [ ] Final keyless Sofia origin replay passes
- [ ] Final Martin Change File application passes
- [ ] Final source-free and source-aware verifier passes
- [ ] Final receiver-specific reconstruction passes
- [ ] Complete refusal matrix passes
- [ ] Shared MCP direct path and actual Codex invocation pass
- [ ] Plugin clean install, refresh/new task, installed-copy invocation, and
      uninstall pass
- [ ] Final pytest, Ruff lint, Ruff format, lock, build, wheel, Git, link,
      license, asset, secret, and absolute-path checks pass
- [ ] README, limitations, provenance, build log, sample guidance, and plugin
      instructions match the selected release

### Claims, privacy, media, and intellectual property

- [ ] Every sentence in the final README, Devpost copy, narration, screenshots,
      and thumbnail maps to this claim audit or is removed
- [ ] GPT outbound evidence says selected eligible excerpts may be sent
- [ ] Change File disclosure says no payload bytes but lists disclosed metadata
- [ ] `store=false` wording retains the standard-retention caveat
- [ ] Receiver “no external network” wording is not expanded into an
      unqualified browser “no network” claim
- [x] No personal path, credential, response ID, account identifier,
      notification, or unrelated content appears in committed or public media
- [ ] Synthetic fixture provenance is current
- [ ] Blueprint, MCP, BagIt, and all other third-party licensing obligations are
      satisfied
- [ ] No unlicensed music, third-party footage, or unsupported trademark use
- [x] Seven Connected Change screenshots pass final visual QA and hashes are
      recorded
- [x] Connected Change thumbnail PNG/SVG passes visual/file QA and hashes are
      recorded
- [ ] Final narration matches the selected release and is approved by the user
- [ ] Final video duration is strictly under 3:00
- [ ] Final video has intelligible English audio covering the product, concrete
      Codex work, and runtime GPT-5.6 integration
- [ ] Final video is Public on YouTube and complete public playback is verified

### Devpost and user-owned actions

- [ ] Stale public Devpost copy and thumbnail replaced with final material
- [ ] Work & Productivity selected
- [ ] Repository URL, technology list, supported platform, and testing
      instructions verified
- [ ] Public YouTube URL added
- [ ] User runs `/feedback` in the primary Codex build task and supplies the
      exact Session ID
- [ ] User confirms entrant type
- [ ] User confirms country and eligibility
- [ ] User confirms ownership, representative authority where applicable, and
      every personal/legal attestation after reading the form and rules
- [ ] Deadline rechecked against official sources immediately before submission
- [ ] User explicitly releases the active submission hold
- [ ] Only after release: final Devpost submission performed
- [ ] Submitted project page, repository, video, and testing instructions resolve
- [ ] Devpost receipt/confirmation captured before Wednesday 22 July 2026 at
      02:00 CEST

## Final stop rule

Creating, editing, committing, pushing, publishing, rehearsing, or uploading
this C6 draft does not authorize final submission and does not release the hold.

If every independently actionable product, release, media, due-diligence,
`/feedback`, and Devpost-draft requirement is complete while the hold remains
active, the correct state is `WAITING_FOR_SUBMISSION_HOLD_RELEASE`.

Final Devpost submission remains prohibited until the user explicitly releases
the submission hold. After release, submission is complete only when the final
entry and its receipt/confirmation have been verified.
