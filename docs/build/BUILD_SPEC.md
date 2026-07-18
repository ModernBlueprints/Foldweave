# Reversible Name Atlas — AI-first Build Specification

Status: **AI-FIRST THIRD-CYCLE PRODUCT CONTRACT FROZEN; AMENDED GOAL INACTIVE**

This document is the sole authority for what the AI-first Reversible Name Atlas
product is, what it supports, what it proves, and what must exist at recording
readiness. `IMPLEMENTATION_PLAN.md` controls sequence, `GOAL.md` controls
execution authority, `STATE.md` records observed current state, and
`DECISIONS.md` records rationale only.

No AI-first implementation is active merely because this specification exists
or is committed. Only the user's later explicit activation of the complete
amended `docs/build/GOAL.md` creates A+0.

## 1. Controlling sources and fixed boundaries

### Source certificates

| Authority | Path | Logical lines | Newlines | Bytes | SHA-256 | EOF |
|---|---|---:|---:|---:|---|---|
| AI-first product direction | `/Users/nikolai/.codex/attachments/d9b8d3f0-8b24-4715-a744-5eef576e91e9/pasted-text.txt` | 971 | 970 | 45,569 | `7777dd7fd322cebe1deb0ff12e03c13c7a18cf2e5769ad71a7a2fef807d1d76b` | Complete; no final newline; final byte `.` |
| Third-cycle operating model | `/Users/nikolai/.codex/attachments/47308821-f8b9-4101-b3cb-fff36b725471/pasted-text.txt` | 912 | 911 | 34,068 | `c6b18835cc0c63fa6be6fc7013ed498f72d4ed8133935a743c20cabedbf2d4b3` | Complete; no final newline; final byte `*` |

Authority precedence is: current user instruction; the first attachment for
product direction; the second attachment for operating structure; historical
repository governance where it does not conflict; then observed state for
facts.

### Official sources

- [Official Build Week rules](https://openai.devpost.com/rules)
- [Build Week FAQ](https://openai.devpost.com/details/faqs)
- [GPT-5.6 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
- [OpenAI function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI API data controls](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint)
- [Codex plugin documentation](https://developers.openai.com/codex/plugins/build)

The official deadline is Tuesday 21 July 2026 at 17:00 Pacific time, which is
**Wednesday 22 July 2026 at 02:00 CEST**. The protected recording-ready
boundary is **Tuesday 21 July 2026 at 02:00 CEST**.

The submission hold is active. Final Devpost submission is prohibited until the
AI-first product, renewed release materials, video, due diligence, and
submission package are complete and the user explicitly releases the hold.

## 2. Historical requirement disposition

The first- and second-cycle requirement text remains available in Git history at
known-good predecessor `4baec1ed7b8553775527e3be506edab584b2b8b3`.
Archive-specific contracts are not reinterpreted as generic folder contracts.
Every prior requirement identifier has the following explicit disposition.

| Historical IDs | Disposition | Third-cycle treatment |
|---|---|---|
| `PRD-001`–`PRD-005` | `SUPERSEDED_FOR_AI_FIRST_RELEASE` | Archive user, linked-package product identity, and archive-first surface are not active release requirements. |
| `PRD-006` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Portable, independently checkable handoff principle is restated under `PRD-009`, `VER-010`–`VER-014`. |
| `IO-001`–`IO-004` | `SUPERSEDED_FOR_AI_FIRST_RELEASE` | CSV package shape, normalization table, and archive profile are not accepted AI-first inputs. |
| `IO-005` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Fail-closed input behavior is restated under `IO-006`–`IO-011`. |
| `TX-001`–`TX-005` | `HISTORICAL_ONLY` | Archive family/proposal/identifier transformations do not control generic folder planning. |
| `TX-006`–`TX-008` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Copy-only staging, complete proof, and fail-closed promotion are restated under `TX-009`–`TX-013`. |
| `CASE-001`–`CASE-005` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Atomic persistence, revision checks, locks, rehydration, staleness, and immutable completion are restated under `CASE-006`–`CASE-009` for a new job schema. |
| `AI-001`–`AI-006` | `SUPERSEDED_FOR_AI_FIRST_RELEASE` | Decision-card-only GPT behavior is replaced by bounded complete folder planning. |
| `AI-007` | `HISTORICAL_ONLY` | The validated archive card remains historical evidence and cannot qualify the new planner. |
| `UX-001`–`UX-005` | `SUPERSEDED_FOR_AI_FIRST_RELEASE` | Archive Atlas/Decisions/Proof experience and old fixtures are not release-facing. |
| `UX-006`–`UX-008` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Server authority, progressive disclosure, Blueprint assets, and responsive visual foundations are restated under `UX-009`–`UX-012`. |
| `VER-001`–`VER-004` | `HISTORICAL_ONLY` | Archive-specific family/reference checks do not qualify generic folders. |
| `VER-005`–`VER-009` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Portable receipts, acyclic commitments, keyless verification, controlled failure, and restore mechanics are restated under `VER-010`–`VER-014`. |
| `REL-001`–`REL-004` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Python/uv packaging, tests, replay, documentation, and clean-release mechanics are restated under `REL-008`–`REL-011`. |
| `REL-005`–`REL-007` | `HISTORICAL_ONLY` | Second-cycle release, optional-restore gate, and recording evidence remain historical baseline facts. |
| `CLAIM-001`–`CLAIM-003` | `MECHANICALLY_REUSED_UNDER_NEW_ID` | Their cautionary boundaries are restated and expanded under `CLAIM-004`–`CLAIM-005`; they are not current product claims by themselves. |

The predecessor release is an inherited verified baseline, not evidence that any
new requirement below is implemented.

## 3. Product identity

### PRD-007 — Product, audience, and track

- Name: **Reversible Name Atlas**.
- Tagline: **Describe the change. Keep every connection. Prove the result.**
- Every primary use of “connection” must immediately qualify it as a supported
  relative Markdown link inside the selected folder.
- Track: **Work & Productivity**.
- Category: **AI refactoring for connected project folders**.
- Initial audience: people preparing a complicated project folder for another
  person to use, including consultants, researchers, designers, educators,
  photographers, journalists, small agencies, preservation workers, and
  enthusiasts.
- Core differentiator: “An ordinary AI organizer can move the files. Name Atlas
  can move the project without silently breaking the supported links that
  connect it.”

### PRD-008 — Required automatic transaction

The product accepts an ordinary local folder and plain-English request, lets
GPT-5.6 inspect bounded path and selected text evidence, compiles the proposed
plan with fixed code, asks one concise question only when essential information
is missing, and automatically creates a separate verified result.

Required transaction:

`local folder → request → bounded GPT investigation → structured plan → fixed compilation → optional one-question clarification → separate result → supported-link rewrite → proof → keyless verification → original-layout reconstruction`

The primary action is **Plan and create copy**. There is no per-file approval
queue. Clicking that action after the required disclosure authorizes the bounded
planning and copy transaction. GPT never directly mutates the source.

### PRD-009 — Proof-bearing usable result

The usable reorganized project lives under `data/`. The surrounding BagIt root
is a portable verified handoff whose `name-atlas/` directory contains the exact
request, observable evidence, accepted plan, maps, change ledger, verification,
receipt, and reconstruction material. Primary UI wording is “new folder” or
“verified result,” not BagIt terminology.

### PRD-010 — Required and optional surfaces

- The required product is one local, server-rendered browser application.
- Start, Working/Clarification, and Done are its only standard release-facing
  states.
- Old Atlas/Decide/Stage/Verify/Handoff routes are not registered in the normal
  release surface.
- The core browser product does not require Codex at runtime.
- One installable Codex plugin is optional behind the objective `REL-010` gate.
- A hosted ChatGPT app, SaaS, accounts, collaboration, and remote mobile access
  are excluded.

## 4. Input and path contract

### IO-006 — Supported ordinary folder

- Source is an existing readable local directory.
- Require at least 1 and at most 500 regular files.
- Permit at most 1,000 directories.
- Include every readable regular file, including hidden regular files.
- Directories are structural members; empty directories are explicit members
  fixed to their original relative paths.
- GPT cannot move or rename empty directories.
- Support only regular files and directories.
- Before any API call, block on a symlink, special file, unreadable member,
  unsupported path, member-limit breach, or regular file with `st_nlink > 1`.
- Never silently skip an unsupported member.
- Use streaming hashing and copying.
- There is no total folder-byte or opaque-payload-byte cap beyond the capacity
  rule in `IO-008`. Each `.md` or `.markdown` member is limited to 16 MiB
  because the exact semantic adapter must decode and index it in memory. A
  larger Markdown member blocks during inventory, before any provider call.
- Permit at most 10,000 supported local Markdown references across the complete
  folder. The scanner counts before retaining the next reference and blocks
  with `markdown_reference_limit_exceeded` during scanning, before provider use.

### IO-007 — Protected and evidence-denied members

Protect every dotfile, every member below any dot-directory, and every member
below `.git/`, `.hg/`, or `.svn/`.

Also protect basenames matched case-insensitively by `.env*`, `.npmrc`,
`.pypirc`, `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `credentials*`, or
`secrets*`, and suffixes `.pem`, `.key`, `.p12`, `.pfx`, or `.kdbx`.

Protected members:

- remain in the complete inventory and final result;
- stay at the exact original relative path;
- are injected mechanically into the accepted map;
- never expose content through GPT evidence tools;
- block a request that requires their inspection or movement.

A protected Markdown member may be carried unchanged only when it contains no
supported local link. If one contains a supported local link, scanning blocks
before any provider call: preserving that relationship could require exposing
or rewriting evidence-denied content, so it is outside this release contract.

### IO-008 — Capacity, overlap, and source equality

Before planning and execution, calculate source bytes and require:

`required_free = source_bytes + rewritten_markdown_original_bytes + max(256 MiB, ceil(source_bytes × 0.10))`

No separate total-byte cap applies, but capacity must pass. The resolved source
and output-parent/result trees may not contain one another. Pending and final
results may be children of the selected output parent, but the job file and all
mutable local-state directories must be outside the source, pending result,
final result, and portable handoff. No mutable product state may become an
in-scope source member. Resolve every absent path through its nearest existing
ancestor. The output parent must be writable and the final result absent.

The default `.name-atlas/jobs/` directory is ignored local state. It is usable
only when its resolved location satisfies the separation rule above; otherwise
planning blocks and requires an explicit safe `--job` path.

Rescan before planning, before execution, and before no-replace promotion. An
added, removed, renamed, replaced, resized, or digest-changed member makes the
job stale or blocked and prevents promotion.

### IO-009 — Stable identity and source commitment

File identity is lowercase SHA-256 over canonical, domain-separated bytes that
bind schema, original relative POSIX path, byte size, and payload SHA-256.
Identical bytes at different paths remain distinct identities.

The source commitment hashes the canonical sorted inventory of regular files
and explicit empty directories, including relative path, member kind, size and
payload digest where applicable, and protection/evidence flags. Portable
artifacts never contain sender-local absolute paths.

### IO-010 — Name Atlas cross-platform-safe naming profile

Targets are NFC relative POSIX paths under `data/`. Components must be nonempty
and cannot be `.`, `..`, contain NUL/control characters or `< > : " / \\ | ? *`,
or begin/end with a space or dot.

Reject, case-insensitively and before the first period, `CON`, `PRN`, `AUX`,
`NUL`, `COM1`–`COM9`, and `LPT1`–`LPT9`. Enforce 240 UTF-8 bytes per component
and 1,024 UTF-8 bytes per complete relative path. Enforce exact, NFC, and
casefold uniqueness for complete targets and every directory prefix, including
file/directory ancestor conflicts and empty-directory conflicts.

For a renameable non-dotfile, preserve the exact substring from its first
non-leading period through the end, including case. Extensionless files may be
renamed without adding a suffix. Protected dotfiles remain unchanged.

This is an application profile, not a universal filesystem or native-Windows
guarantee.

`result_folder_name` is exactly one nonempty path component, never a path. It
must satisfy the component-level NFC, forbidden-character, `.`/`..`,
leading/trailing space-or-dot, reserved-basename, and 240-byte rules above; it
cannot contain `/` or `\\` and never determines the absolute output parent.

### IO-011 — Supported Markdown links

Only UTF-8 `.md` and `.markdown` files receive semantic link handling. Support
inline links and inline images whose destination is either inside `<...>` or an
unquoted token without literal whitespace or unescaped parentheses. Targets
must be relative local files and may have an optional `#fragment`.

Each Markdown member is limited to 16 MiB as specified by `IO-006`. The scanner
uses compact bounded auxiliary structures and streams line-range discovery; it
does not create an unbounded whole-folder text index. The complete folder may
contain at most 10,000 supported local Markdown references; exceeding that
limit blocks before provider use. Protected Markdown members follow the
fail-closed local-link rule in `IO-007`.

- Ignore fenced code, indented code, and inline code.
- Ignore and count external schemes and anchor-only links.
- Reject query strings, absolute/root-relative/file URLs, outside-root paths,
  directories, dangling targets, malformed escapes, invalid UTF-8, traversal,
  decoded NUL, encoded slash/backslash ambiguity, and unsupported local-looking
  syntax.
- Resolve once-decoded UTF-8 paths case-sensitively against the logical source
  inventory, regardless of host filesystem behavior.
- Preserve fragments exactly and use one canonical segment-wise percent
  encoding for rewritten destinations.
- Reference-style local links and local reference definitions block; they are
  not claimed as supported.

Use an exact-span scanner or equally precise parser, never global replacement.

## 5. Transaction contract

### TX-009 — Complete compiled plan

The GPT plan covers every planner-eligible file exactly once. It cannot exclude,
delete, merge, duplicate, invent, or directly operate on a file. The compiler
rejects unknown, duplicate, missing, protected, or stale IDs; injects exact
unchanged protected-file and empty-directory mappings; and produces one
immutable accepted plan accounting for every source file exactly once.

Every submitted and accepted plan carries the exact supported request scope
`rename_and_move_every_file`. This field is a structural declaration, not proof
that model prose is semantically correct. A live or replay planner must return a
structured `blocked` outcome when the request is outside that fixed scope. The
deterministic A2 development provider is bound to one exact declared request
and blocks every other request fingerprint; it cannot promote an arbitrary
plain-English request merely because the complete-file compiler is safe.

The exact A2 deterministic-development request is:

> Prepare this project for handoff. Keep every file and every supported
> Markdown link working.

Product-generated proof files under `name-atlas/` are outside the user-file
bijection. Requests to delete, discard, deduplicate, merge, retain only selected
files, or extract archives are unsupported and block before promotion.

### TX-010 — Supported change boundary

Support file renames, moves into a new directory structure, derived target
directories, one validated result-root name, protected-file preservation, and
supported Markdown-link rewriting.

Exclude arbitrary body editing, code refactoring, import/config/database
rewriting, spreadsheet-cell changes, embedded Office/PDF/InDesign/Lightroom
links, OCR, media understanding, archive extraction, conversion, deletion,
deduplication, merging, arbitrary commands, and direct source mutation.

The user chooses the absolute output parent. GPT may propose one validated
`result_folder_name` but never an absolute output path.

### TX-011 — Deterministic reference graph and rewriting

Before planning, deterministic code records each supported link's source file
ID, target file ID, exact original destination span, destination text/bytes,
fragment, and target resolution. After plan compilation, the same record adds
the proposed rewritten destination and verification status. GPT never provides
byte offsets or rewrite commands.

After the accepted map exists, derive new destinations. Apply replacements from
right to left and preserve every byte outside accepted destination spans,
including line endings. Preserve complete original bytes of each rewritten
Markdown file at `name-atlas/original-content/<file-id>.bin`.

Verification must prove deterministic reapplication produces the staged bytes
and every rewritten link still resolves to the same stable target ID.

### TX-012 — Copy-only staging and atomic promotion

The source is never renamed, edited, or deleted. Create an absent sibling
pending result, copy every source file once, create explicit empty directories,
rewrite only accepted Markdown spans, write all proof artifacts, complete
deterministic proof and BagIt validation, run the source-free verifier, rescan
the source, and promote no-replace only when every required check passes.

A failed transaction creates no accepted final result. Any failure record is a
sibling outside the finalized receipt hash domain.

### TX-013 — Original-layout reconstruction

`restore-receipt` verifies first, refuses an existing destination, creates a
sibling pending destination, uses reverse maps for unchanged/moved payloads,
uses preserved original bytes for rewritten Markdown, recreates empty
directories, and proves every original path, size, and SHA-256 before
no-replace promotion. It changes neither source nor organized result.

## 6. Persistent job authority

### CASE-006 — `FolderRefactorJob`

The sole mutable workflow authority is strict schema `folder-refactor-job.v1`
with lifecycle `planning`, `awaiting_clarification`, `executing`, `verified`,
`stale`, or `blocked`.

Default jobs are `.name-atlas/jobs/<lowercase-uuid4-hex>.json`. `--job` resumes
an exact existing path or creates an exact absent path. The CLI prints the local
job path. A fresh run creates a new job; there is no destructive reset.

Persist schema/revision, UUID4 ID, display name, Europe/Oslo timestamps, local
source/output paths, portable snapshot, request, evidence, observable response
items, plan attempts and rejections, clarification/answer, accepted plan,
change ledger, result pointers, receipt fingerprint, and lifecycle.

### CASE-007 — Atomicity and concurrency

Use Pydantic v2 with `extra="forbid"`. Save complete JSON to a sibling temporary
file, flush and `fsync`, atomically replace, and `fsync` the parent where
supported. Require expected prior revision. Hold a process lock. Corrupt JSON,
unsupported schema, incomplete state, lock contention, or revision mismatch
blocks without reconstruction from UI memory.

### CASE-008 — Rehydration and staleness

On load and before mutation, parse strictly, rescan, recompute inventory and
reference data, compare the source commitment, and validate evidence, response,
plan, clarification, and accepted-plan bindings. Reuse only exact state. A
source change sets `stale`, reports exact differences, and blocks continuation,
execution, and promotion.

### CASE-009 — Terminal immutability

`verified`, `stale`, and `blocked` jobs are terminal for this release. Completed
receipts are immutable. A correction starts a fresh job from the unchanged
source and never edits a prior receipt in place.

## 7. GPT-5.6 planner

### AI-008 — Provider and authority boundary

Use exact `gpt-5.6` through the Responses API, strict function schemas,
`store=false`, and `max_retries=0`. Record the returned model identifier. There
is no Chat Completions or substitute-model fallback.

Persist complete observable output items needed for local multi-turn
continuation, including returned reasoning items required by the API protocol,
without exposing or claiming hidden chain-of-thought.

Strict tools are `list_inventory_page`, `read_text_excerpt`,
`inspect_markdown_links`, `submit_plan`, and `request_clarification`.

GPT receives no shell, arbitrary file read, write/move/delete function,
promotion authority, verifier override, omission authority, or ability to mark
its plan safe/correct/verified. Fixed code executes only a compiled accepted
plan after the user's original action authorization.

### AI-009 — Evidence and planner outcome

Source text is untrusted evidence, never instruction authority. GPT may receive
the request; relative paths; member kind; stable file ID; byte size; protected
and evidence-eligible flags; selected eligible UTF-8 excerpts; supported-link
context; evidence IDs; and profile description. Raw payload digests and
detailed protection reasons remain local. GPT never receives absolute paths,
arbitrary payload bytes, protected contents, opaque binary/media/document
content, secrets, or unrelated files.

`folder-planner-outcome.v1` is the discriminated union `plan`,
`clarification`, or `blocked`. A plan binds source commitment, request
fingerprint, the exact `rename_and_move_every_file` request scope, schema
versions, and evidence fingerprint. It contains a validated result-folder name
and exactly one entry per planner-eligible file: ID, original path, proposed
target, concise rationale, and known evidence IDs. It contains no absolute path
or exclusion. Any defensive exclusions field must be present and empty. The
planner must use the terminal `blocked` outcome for requests outside the fixed
scope; model confidence or self-asserted scope never overrides the compiler.

The evidence ledger records exact outbound evidence, declared `tool_name`,
validated tool arguments, stable result or failure, explicit status, byte count,
fingerprint, response turn, and evidence-call number. Entries are ordered by
response turn and evidence-call number. Model confidence is never a compiler
input.

### AI-010 — Turn, evidence, repair, and clarification limits

A response turn is one budget-reserved `responses.create` or `responses.parse`
attempt, including timeout, transport failure, refusal, incomplete response, or
invalid output. Persist/count before request. Maximum eight turns per job; no
hidden ninth call and no provider retry.

An evidence call is each requested evidence-function invocation, including
invalid, stale, empty, duplicate, rejected, or parallel calls. Count before
execution. Maximum 24 per job, 16 KiB per result, 128 KiB aggregate tool result
bytes, and 512 KiB total outbound evidence including initial inventory.
Repeated identical calls may use cache but still count and remain visible.
Truncation is explicit and blocks when complete accounting is impossible.

Maximum model output is 32,768 tokens per response.

Allow one initial submitted plan and at most two mechanically prompted corrected
submissions. Rejection after repair 2 is terminal. Return only stable
machine-readable compiler failures; never shift them to the user.

Allow at most one structured clarification, one compact question, and one user
answer. Post-answer work uses remaining budgets and cannot ask again. Only
missing user intent qualifies. API/model failure, malformed output, exhausted
limits, unsupported syntax/request, invalid destination, protected movement, or
source change produces a system blocker, not a user question.

### AI-011 — New live evidence and replay

Third-cycle release requires one real zero-question `gpt-5.6` hero transaction
and one real one-clarification transaction, each with an exact sanitized
`folder-planner-replay.v1` derived from the successful observable run.

Bind request, source commitment, schemas, evidence calls/results, submitted
plans, compiler feedback, clarification/answer where present, accepted plan,
alias, returned model ID, usage, estimated cost, Europe/Oslo timestamps, and
`store=false`. Commit no API key, response ID, absolute path, hidden reasoning,
or unrelated account data.

Replay is keyless, makes no provider call, displays **Recorded GPT-5.6 planning
run**, and fails closed if fixture, instruction, planner/evidence schema, or
fingerprint differs. The normal hero should complete in approximately three to
five provider turns; eight is a ceiling, not a target.

The historical archive DecisionCard recording is preserved as historical
evidence only and cannot qualify this requirement.

### AI-012 — Retention disclosure and sole budget authority

Before **Plan and create copy**, display:

> Your original folder will not be changed. Name Atlas will create and verify a separate result. It sends GPT-5.6 your instruction, relative file names and folder structure, basic file metadata used to bind the plan, selected excerpts from eligible text and Markdown files, and supported Markdown-link context needed to plan the change. It does not send every file's bytes. Raw content hashes are kept local.

Also display:

> Name Atlas asks the Responses API not to retain the response as application state and keeps the working planning record locally. Standard OpenAI API data-retention policies may still apply.

Do not claim zero retention, full privacy, or that OpenAI stores nothing.

`.name-atlas/api_budget.json` remains the sole project budget authority. Migrate
it atomically and monotonically without resetting history: preserve historical
requests, attempts, exposure, actual estimates, and cumulative USD 10 cap;
increase the secondary cumulative provider-request cap from 8 to 13; never
create a planner-specific ledger. Monetary reservation wins over request
capacity. The cumulative cap includes the one preserved historical provider
request and therefore permits at most twelve additional third-cycle
qualification/provider attempts. It does not permit thirteen new attempts.
Missing, corrupt, locked, or incompatible historical state blocks.

Before each request, reserve conservative maximum exposure under current
official pricing. Verify the configured token/evidence envelope cannot exceed
USD 10; record reported usage and estimated cost after every attempt.

## 8. User experience

### UX-009 — Start

`GET /start` and `POST /start` show only folder path, plain-English request,
result location/output parent, exact source-untouched and outbound-evidence
disclosures, and **Plan and create copy**. `--source` prepopulates the local
path. Immediately beside the request, state that every source file is always
kept exactly once and that the field controls only renaming and folder grouping;
deletion, omission, merging, conversion, and document-body editing are not
supported. Never describe this as uploading. A native picker is excluded.

### UX-010 — Working and clarification

`GET /working`, `GET /status`, and `POST /clarify` show simple stages: Reading
folder; GPT-5.6 is planning; Checking every file and destination; Creating a
separate result; Updating supported links; Verifying result.

Expose sufficient observable planning/tool progress to demonstrate central GPT
use while hiding repair noise and technical manifests by default. When needed,
show one question, accept one plain answer, and resume the same persisted job.
Refresh and explicit restart with the same job path cannot duplicate provider
calls or output.

Scanning, planning, copying, link rewriting, and proof execute as one complete
worker-thread service operation so the loopback web event loop remains
responsive. The durable writer and transaction authority stay together for the
whole operation. Presentation-only phase callbacks cannot mutate the job or
transaction. Shutdown or task cancellation waits for the mutation-owning
operation to reach its safe result or blocker; it never abandons a detached
writer thread.

### UX-011 — Done

`GET /done`, `POST /verify-again`, and `POST /recreate-original` lead with
plain facts: all source files present once, paths changed, supported links
updated/resolved, no files removed or overwritten, source unchanged, independent
verification passed, and original layout reproducible within the contract.

Actions: **Open new folder** (or display/copy exact `data/` path if native open
is unavailable), **See changes**, **View proof**, **Verify again**, and
**Recreate original layout**. Technical hashes, manifests, BagIt terms, schema
versions, transcript, and receipt fingerprint are collapsed by default.

### UX-012 — Routing, visual system, and release identity

`GET /` redirects by server-owned state: no job to `/start`; planning/executing
to `/working`; awaiting clarification to `/working` with question; verified to
`/done`; stale/blocked to `/working` with exact blocker and fresh-job guidance.

Use FastAPI, Jinja2, locally packaged Blueprint dark assets, and minimal
JavaScript for polling, disclosure, clipboard, and local filtering. Standard
release/judge commands register no old archive navigation or routes.

Required visual checks: 1280×720 and 390×844, semantic forms/headings/tables,
keyboard/focus behavior, contrast, and progressive disclosure. Responsive
layout is not a mobile app or remote phone/file-access claim.

## 9. Verification and portable artifacts

### VER-010 — Versioned portable artifact family

Strict schemas are `folder-refactor-job.v1`, `folder-inventory.v1`,
`folder-planner-outcome.v1`, `folder-plan.v1`,
`folder-reference-graph.v1`, `folder-accepted-plan.v1`,
`folder-evidence-ledger.v1`, `folder-planner-replay.v1`,
`folder-change-ledger.v1`, `folder-verification-report.v1`,
`folder-change-receipt.v1`, `folder-receipt-verification.v1`, and
`folder-restore-report.v1`. Use Pydantic v2 `extra="forbid"` and structural
Protocols at scanner, provider, evidence, compiler, staging, receipt, verifier,
and reconstruction boundaries.

Required result paths:

- `name-atlas/source_snapshot.json`
- `name-atlas/user_request.json`
- `name-atlas/evidence_ledger.json`
- `name-atlas/accepted_plan.json`
- `name-atlas/reference_graph.json`
- `name-atlas/forward_path_map.csv`
- `name-atlas/reverse_path_map.csv`
- `name-atlas/change_ledger.json`
- `name-atlas/verification_report.json`
- `name-atlas/change_receipt.json`
- `name-atlas/proof_and_restore.html`
- `name-atlas/original-content/<file-id>.bin` for every rewritten Markdown file
- BagIt metadata and SHA-256 manifests.

All portable artifacts use relative paths only.

### VER-011 — Acyclic receipt and generation order

The receipt envelope contains immutable `ReceiptCore` plus
`receipt_fingerprint`, which is outside its own hash domain. The fingerprint is
lowercase SHA-256 over the canonical `ReceiptCore` bytes. Canonical core bytes
use every JSON-mode field including explicit null, UTF-8,
`ensure_ascii=False`, sorted keys, separators `(",", ":")`, `allow_nan=False`,
and no trailing newline. Raw artifact digests cover exact on-disk bytes.

`staged_data_commitment` is lowercase SHA-256 over canonical JSON bytes for the
list of every regular member below `data/`, sorted by relative POSIX path. Each
list item contains exactly `path`, byte `size`, and lowercase payload `sha256`.
The list uses the same UTF-8, `ensure_ascii=False`, sorted-key, compact-separator,
`allow_nan=False`, and no-trailing-newline rules as `ReceiptCore`.

The core records the source and staged-data commitments, model/schema identity,
clarification where used, bounded claims, and raw SHA-256 commitments over the
exact on-disk bytes of `source_snapshot.json`, `user_request.json`,
`evidence_ledger.json`, `accepted_plan.json`, `reference_graph.json`, both path
maps, `change_ledger.json`, every `original-content/<file-id>.bin`,
`verification_report.json`, `bagit.txt`, `bag-info.txt`, and
`manifest-sha256.txt`.

Exclude receipt JSON, HTML, tag manifest, and later receiver-verification output
from the core commitment set; the final tag manifest protects receipt and HTML.

Generation order: prove source equality; copy/rewrite; write artifacts and
original bytes; deterministic proof; initial BagIt/manifests and validation;
final report; commitments; receipt; HTML; final tag manifest; final BagIt
validation; independent verifier; final source equality; no-replace promotion.
Receipt-bound artifacts do not change after finalization.

### VER-012 — Independent receiver verifier

`uv run name-atlas verify-receipt RESULT_BAG [--source SOURCE_ROOT]` writes
nothing. Exit 0 prints `VERIFIED` and fingerprint; exit 1 prints `BLOCKED` and
stable check IDs; exit 2 is usage/unopenable candidate.

It requires no job, browser, GPT, API key, network, or source, and must pass
after copying the result to an unrelated path. It validates BagIt, strict
schemas, fingerprint/digests, staged data, file bijection, request/evidence/plan
bindings, naming/path rules, Markdown replacements and target identity, inverse
maps, payloads, original-content artifacts, and report agreement. `--source`
adds current-source comparison; source-free verification proves internal
consistency, not historical authenticity.

### VER-013 — Exact controlled negative

Copy the successful hero result, alter one syntactically valid target in
`accepted_plan.json`, rebuild the ordinary BagIt tag manifest, leave the
receipt unchanged, and prove BagIt passes while Name Atlas exits 1 with:

`artifact_digest_mismatch:accepted_plan`

Never alter canonical source/result. This is transaction-consistency evidence,
not signing, authentication, or tamper-proofing.

### VER-014 — Exact bounded reconstruction

`uv run name-atlas restore-receipt RESULT_BAG RESTORE_DESTINATION` verifies
first, refuses an existing destination, uses a sibling pending directory,
reconstructs paths through the reverse map, restores exact original rewritten
Markdown bytes, recreates empty directories, proves every path/size/SHA-256,
and promotes no-replace. UI label: **Recreate original layout**.

Permitted claim: “Recreates every in-scope source member's relative path and
bytes within the supported Name Atlas folder contract.” Do not claim timestamps,
ownership, ACLs, extended attributes, resource forks, hard-link/symlink identity,
undeclared references, or arbitrary filesystem state.

## 10. Release contract

### REL-008 — Stable commands and packaging

Required commands:

- `uv sync --frozen`
- `uv run name-atlas demo --mode replay`
- `uv run name-atlas demo --mode live`
- `uv run name-atlas run --mode live --source SOURCE_ROOT [--output OUTPUT_PARENT] [--job JOB_FILE] [--port PORT]`
- `uv run name-atlas verify-receipt RESULT_BAG [--source SOURCE_ROOT]`
- `uv run name-atlas restore-receipt RESULT_BAG RESTORE_DESTINATION`
- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .`

Replay uses the bundled hero and exact new recording, requires no key, and makes
no provider request. Live uses exact `gpt-5.6` with no fallback. Verifier and
restore dispatch before provider/budget/demo/web initialization. Missing live
credentials do not affect replay, verifier, or restore.

Use Python 3.11, `uv`, FastAPI, Jinja2, vanilla JavaScript/CSS, Pydantic v2,
the official OpenAI SDK, pytest, Ruff, existing locally packaged Blueprint
assets, and existing BagIt support. Build the new generic workflow beside—not
inside—the archive-specific workflow authority.

### REL-009 — Fixtures and live evidence

The hero has exactly 24 regular files and at least eight supported relative
Markdown links, using generated or safely licensed Markdown, TXT/CSV, JPG/PNG,
WAV/MP3, PDF, XLSX, and opaque binary files with provenance. Opaque files are
copied byte-for-byte; only paths and eligible text/Markdown are semantic
evidence.

Hero instruction:

> Prepare this Apollo client-project folder for handoff as Northstar. Keep every file. Use the briefing and project notes to organize approved deliverables, working material, research, and meeting notes into clear folders. Rename Apollo-labelled paths to Northstar and keep every supported link working.

Require a real zero-question plan where a note and target both move, links still
resolve to the same payload, every file appears once, source stays unchanged,
result verifies, reconstruction matches, and replay is exact.

One small ambiguity fixture has one Markdown note call a presentation approved
and another call a different presentation internal review. Its instruction
requires the approved presentation under final deliverables, while both
presentations must be retained. Require one real clarification, one answer, a
complete plan containing both files, a verified result, and an exact replay. No
deletion, image understanding, or per-file approval. One controlled negative
uses `VER-013`. Do not create multiple polished collections.

### REL-010 — Optional Codex plugin gate

Adjudicate once at scaled A4/standard A+42. Admit only after both GPT paths,
persistence/restart, Markdown preservation, receipt, verifier, controlled
negative, reconstruction, three-state UI, and cross-artifact consistency pass;
no required defect remains; at least 12 actual hours remain before recording
readiness; implementation/installation/docs/regression estimate is at most six
hours; and no core logic would be duplicated.

If any predicate fails, record `CUT_BY_PREAUTHORIZED_GATE` and omit all plugin
code/docs/screenshots/claims. This is not incomplete required scope.

If admitted, build one installable Codex plugin with required
`.codex-plugin/plugin.json`, relative `.mcp.json`, and thin local STDIO MCP over
the same core services. Expose only `plan_and_create_copy`, `job_status`,
`verify_receipt`, and `recreate_original`. No raw filesystem tools, second
planner, second persistence, second receipt, or second budget ledger.

Acceptance requires clean-clone installation, app refresh/restart, visibility
in a new Codex task, real tool invocation, keyless replay, clear missing-key
failure for live mode, install/uninstall instructions, honest platforms, and a
judge path. A repository-local MCP process merely starting is insufficient.

### REL-011 — Feature freeze and recording readiness

At actual A+0 calculate available hours to Tuesday 21 July 2026 at 02:00 CEST,
plan at most 60, and scale A1/A2/A3/A4/A5/A6/A7 at 10/24/34/42/48/54/60.
Freeze no later than scaled A5 or twelve actual hours before recording readiness,
whichever is earlier. Targets force integration and simplification, not false
completion or cancellation.

After freeze, allow only defects, proof integrity, accessibility, visual QA,
clean install, docs, screenshots, claims, demo rehearsal, and release readiness.

Regenerate README, limitations, provenance/pre-existing-work disclosure, Codex
build log, screenshots, narration, Devpost copy, submission package, thumbnail,
and hero artifacts. Until then they are:

`STALE — PRESERVED SECOND-CYCLE RELEASE MATERIAL; MUST BE REGENERATED AFTER AI-FIRST FEATURE FREEZE`

Recording readiness requires clean public repository/clone, selected commit,
final hero/result/receipt/verifier/restore, live and replay truthfulness, stable
UI, no secrets, full suites, timed narration, shot list, screenshots, Devpost
draft, documented Codex/GPT contribution, prior/new-work disclosure, known
`/feedback` path, no planned product changes, and active submission hold.

## 11. Claim boundaries

### CLAIM-004 — Permitted claims

The product may say that the user describes a folder reorganization in plain
English; GPT-5.6 creates a complete proposed plan from bounded paths and selected
text evidence; fixed checks account for every supported source file exactly
once; protected members stay fixed; source remains unchanged; a separate result
is created; demonstrated supported relative Markdown links are rewritten and
verified; the hero needs no question; the ambiguity example asks one question;
exact observable evidence, plan, answer, changes, and proof are recorded; a
keyless verifier checks internal consistency; the BagIt-valid controlled change
is rejected; original paths/bytes can be recreated within the contract; and
opaque files are carried byte-for-byte.

An optional Codex plugin may be claimed only if `REL-010` actually passes.

### CLAIM-005 — Prohibited or qualified claims and exclusions

Do not claim universal safety, semantic correctness, every file format without
the opaque-byte qualification, media/PDF/Office/spreadsheet understanding, code
refactoring, arbitrary connection preservation, typical zero-question frequency,
mobile/remote phone access, native Windows operation, universal portability or
reversibility, zero API retention, full privacy, authentication/signatures,
authorship, tamper-proofing, compliance, production readiness, unmeasured time
savings, adoption, AI-training-data readiness, Archivematica integration,
nonexistence of competitors, or proven winning probability.

Explicitly exclude CSV reference adapters, image evidence/OCR/media
understanding, reference-style Markdown, native picker, generic rule builders,
5,000-file planner language, hosted ChatGPT app, React/Vite, required plugin,
second GPT semantic review, post-completion conversational revision, code
refactoring, JSONL/Parquet/Hugging Face/AI-data adapters, NER/ReFinED,
signatures/authentication, accounts/collaboration/permissions, repository/cloud
storage/Archivematica integration, multiple polished collections, and further
product-discovery/tournament/benchmark/validation-harness work.

Remaining optional cut order is decorative motion, nonessential metrics,
advanced filters, extra evidence-viewer presentation, then the optional plugin.
Never cut automatic complete planning, source immutability, file accounting,
protected behavior, persistent job/staleness, bounded evidence, deterministic
compilation, clarification path, Markdown preservation, separate result,
receipt, verifier, controlled negative, reconstruction, live/replay truthfulness,
three-state browser, clean installation, or release hardening.

## 12. AI-first recording-readiness Definition of Done

The AI-first product is recording-ready only when every active requirement above
is integrated and verified through the final hero transaction; both real
GPT-5.6 records and exact replays pass; keyless verifier and controlled negative
pass; reconstruction matches paths and bytes; old archive UI is absent from the
release surface; clean clone and all stable commands pass; regenerated release
materials agree with actual behavior and claim limits; the optional plugin is
either fully accepted or exactly `CUT_BY_PREAUTHORIZED_GATE`; no planned code or
design work remains; and final Devpost submission is still held for the user's
voice, `/feedback`, due diligence, and explicit hold release.
