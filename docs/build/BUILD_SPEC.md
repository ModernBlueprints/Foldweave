# Foldweave — Native Review and Dual-Live-Planning Build Specification

Status: **FOLDWEAVE PRODUCT CONTRACT FROZEN; AMENDED GOAL INACTIVE;
WAITING_FOR_FOLDWEAVE_GOAL_ACTIVATION**

This is the sole authority for what Foldweave is, what the next release must
support, what it may claim, which completed predecessor behavior remains
foundational, and what must be true at recording readiness.
`IMPLEMENTATION_PLAN.md` controls dependency order, targets, evidence, and cuts;
`GOAL.md` controls execution authority only after explicit activation;
`STATE.md` records observed state; and `DECISIONS.md` records rationale only.

Sections 1–14 preserve the completed Reversible Name Atlas/Name Atlas A1–A3 and
C0–C7 contracts and evidence. They are historical implemented foundation, not
proof of Foldweave native review, derivative revision, or dual live planning.
Section 15 is the controlling Foldweave extension and narrowly supersedes the
listed predecessor clauses. Historical names, schema identifiers, artifact
paths, fingerprints, and completed evidence are not globally renamed.

The preceding Connected Change goal completed C0–C7 and is superseded only for
future execution. This specification, its commit, its push, its reproduction,
or an activation-readiness verdict does not activate the amended goal. Only the
user's later explicit activation of the complete `docs/build/GOAL.md` in the
current primary Codex task creates F+0.

## 1. Controlling sources and fixed boundaries

### Source certificates

| Authority | Path | Logical lines | Newlines | Bytes | SHA-256 | EOF |
|---|---|---:|---:|---:|---|---|
| AI-first product direction | `/Users/nikolai/.codex/attachments/d9b8d3f0-8b24-4715-a744-5eef576e91e9/pasted-text.txt` | 971 | 970 | 45,569 | `7777dd7fd322cebe1deb0ff12e03c13c7a18cf2e5769ad71a7a2fef807d1d76b` | Complete; no final newline; final byte `.` |
| Third-cycle operating model | `/Users/nikolai/.codex/attachments/47308821-f8b9-4101-b3cb-fff36b725471/pasted-text.txt` | 912 | 911 | 34,068 | `c6b18835cc0c63fa6be6fc7013ed498f72d4ed8133935a743c20cabedbf2d4b3` | Complete; no final newline; final byte `*` |
| Connected Change File product direction | `/Users/nikolai/.codex/attachments/09e7eea4-1ab1-4c90-a200-52e6a8855f3b/pasted-text.txt` | 940 | 939 | 39,271 | `23e4717c1c9d90032428a7ce8552af52988bb3aa03746440514aa71b43960cad` | Complete; no final newline; final byte `*` |
| In-place Connected Change operating model | `/Users/nikolai/.codex/attachments/f8841180-bcaa-4c74-ace2-d989ca57b24e/pasted-text.txt` | 897 | 896 | 30,548 | `cdbba77b841ea2e35a565acb8ef86721a00dc066f91c5724b788b379fd733cee` | Complete; no final newline; final byte `.` |

Authority precedence is: current user instruction; the Connected Change File
product-direction attachment for product direction and accepted claims; its
paired operating-model attachment for governance, sequencing, timing,
activation, and stop conditions; completed A1–A3 governance where it does not
conflict; fresh repository and product evidence for current facts; then older
conversation or memory only when reverified. The earlier attachment pair remains
the source for the implemented A1–A3 foundation, not the future sequence.

### Official sources

- [Official Build Week rules](https://openai.devpost.com/rules)
- [Build Week FAQ](https://openai.devpost.com/details/faqs)
- [Build Week dates](https://openai.devpost.com/details/dates)
- [GPT-5.6 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-5.6-sol)
- [OpenAI function-calling documentation](https://developers.openai.com/api/docs/guides/function-calling)
- [OpenAI API data controls](https://platform.openai.com/docs/models/default-usage-policies-by-endpoint)
- [Codex MCP documentation](https://developers.openai.com/codex/mcp)
- [Codex plugin documentation](https://developers.openai.com/codex/plugins/build)
- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Apple native selection documentation](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/PromptforaFileorFolder.html)

The official deadline is Tuesday 21 July 2026 at 17:00 Pacific time, which is
**Wednesday 22 July 2026 at 02:00 CEST**. The protected recording-ready
boundary is **Tuesday 21 July 2026 at 02:00 CEST**. Feature freeze is **Monday
20 July 2026 at 14:00 CEST**, and the release-candidate boundary is **Monday 20
July 2026 at 20:00 CEST**.

The submission hold is active. Final Devpost submission is prohibited until the
final selected product profile, renewed release materials, public video,
`/feedback`, due diligence, and submission package are complete and the user
explicitly releases the hold.

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

No separate total-byte cap applies, but capacity must pass. The selected output
parent may be disjoint from the source or a strict ancestor of it; the default
result-next-to-source layout uses the source's parent. The output parent may not
equal the source or be inside it. The exact pending and final result trees must
be immediate children of the selected output parent, remain mutually disjoint,
and neither contain nor be contained by the source. The job file and all mutable
local-state directories must be outside the source, pending result, final
result, and portable handoff. No mutable product state may become an in-scope
source member. Resolve every absent path through its nearest existing ancestor.
The output parent must be writable and the final result absent.

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
`store=false`, and `max_retries=0`. Every tool sets `strict=true`; every object
schema sets `additionalProperties=false`; every declared property is required
and uses a nullable type when logically optional. Record the returned model
identifier. There is no Chat Completions or substitute-model fallback.

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

> Name Atlas sets `store=false`, so it does not ask OpenAI to store the generated response for later retrieval through the Responses API. OpenAI's standard abuse-monitoring and prompt-caching retention may still apply.

Do not claim zero retention, full privacy, that OpenAI stores nothing, or that
all processing records remain only on the user's computer.

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

All portable artifacts use relative paths only. For `capsule_applied`, the v2
artifact family omits `evidence_ledger.json` rather than fabricating GPT
evidence; `execution_origin.json`, the exact imported Change File, and the match
report are the receiver authority. The receiver still writes its local accepted
plan, reference graph, maps, change ledger, verification report, receipt,
offline proof, and required original Markdown bytes.

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

`STALE — PRESERVED SECOND-CYCLE RELEASE MATERIAL; MUST BE REGENERATED AFTER THE SELECTED PRODUCT PROFILE REACHES FEATURE FREEZE`

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

The preceding paragraph records the A3-derived fallback release contract. For
future execution it is controlled by the mutually exclusive profile decision
below. It does not authorize resumption of the former A4–A7 sequence.

## 13. Connected Change extension and narrow supersessions

The requirements in Sections 3–12 remain the implemented A1–A3 foundation
except for the exact narrow supersessions below. A1–A3 are completed verified
implementation, not proof of any Connected Change requirement in this section.

| Existing clause | New controlling clause |
|---|---|
| `PRD-010` Start/Working/Done-only release surface | `PRD-013` and `UX-013`–`UX-016` add Home/Organize/Apply under `CONNECTED_CHANGE_GO`; it remains unchanged under fallback. |
| `IO-011` blanket rejection of every `..` component | `IO-015` permits only lexically safe in-root parent-relative targets. |
| `CASE-006` v1 sole-job wording | `CASE-010` makes v2 authoritative for new Connected Change jobs while finalized v1 jobs remain read-only evidence. |
| `UX-009` exclusion of a native picker | `UX-015` requires a bounded macOS picker with a manual-path fallback. |
| `UX-010`–`UX-012` GPT-only progress and three-state routing | `UX-013`–`UX-016` extend routing and require origin-specific progress under `CONNECTED_CHANGE_GO`; fallback retains the prior behavior. |
| `VER-010`–`VER-011` v1-only artifact and receipt wording | `VER-015`–`VER-016` add strict v2 origin/receiver variants; v1 receipt verification remains supported. |
| `REL-010` plugin-only MCP and four-tool contract | `REL-013` requires one shared seven-tool MCP server under `CONNECTED_CHANGE_GO`; `REL-014` separately gates plugin packaging. |
| `REL-011` A-era future timing and release sequence | `REL-015` and the sole C plan control future timing; the old text remains fallback foundation only. |
| `CLAIM-005` native-picker exclusion | Superseded only for the bounded picker in `UX-015`; every unrelated exclusion remains. |
| Former A4–A7 sequence | `SUPERSEDED BEFORE START — REPLACED BY CONNECTED CHANGE OR EXACT A3 FALLBACK PROFILE`. |

Only one of the following profiles can become active after C0:

- `CONNECTED_CHANGE_GO`: every Connected Change requirement in this section is
  required, including Change File generation/application, safe in-root parent
  links, deterministic cross-layout matching, truthful provenance, native
  picker, Organize/Apply browser journeys, shared MCP, new live/replay evidence,
  convergence, verifier, receipt, and reconstruction. The Codex plugin remains
  separately gated.
- `A3_RELEASE_FALLBACK`: Change File, Apply flow, cross-layout matching,
  native-picker expansion, shared MCP, plugin, and all Connected Change claims
  are `CUT_BY_EXISTENTIAL_GATE`. The preserved A3 product follows the compact
  fallback sequence in the sole plan. It still requires the new zero-question
  and one-clarification GPT-5.6 planner records and replays before release.

No provider call, budget migration, final UI work, MCP work, or plugin work can
begin before C0 chooses one profile. The profiles cannot coexist.

### PRD-011 — Connected Change identity and promise

- Product: **Reversible Name Atlas**.
- Primary tagline: **Describe the change once. Apply it wherever the same
  project exists.**
- Secondary line: **AI planning once. Deterministic execution everywhere.**
- Track: **Work & Productivity**.
- Category: **AI refactoring for connected project folders**.
- Audience: people preparing complicated project folders for handoff or reuse,
  including consultants, researchers, educators, journalists, designers,
  photographers, small agencies, preservation workers, and technically capable
  enthusiasts.

Central definition:

> Reversible Name Atlas is a local-first application that lets GPT-5.6 plan a connected-folder reorganization once, verifies and executes that plan through fixed code, and creates a payload-free Name Atlas Change File that can reproduce the same organized result on another equivalent copy of the project—even when that copy begins with different local paths.

### PRD-012 — Origin and receiver transactions

Required origin transaction:

`local folder → plain-English request → bounded GPT-5.6 evidence → complete proposed plan → deterministic compilation → optional one-question clarification → separate verified result → Name Atlas Change File`

Required receiver transaction:

`Name Atlas Change File + differently arranged equivalent local project → keyless deterministic matching → receiver-local accepted plan → separate verified result → independent verification → receiver-specific reconstruction`

The receiver transaction makes exactly zero GPT/provider calls, zero API
requests, zero budget reservations, and zero external network connections, and
transfers no project payload bytes. The browser still uses loopback HTTP, so the
product cannot claim an unqualified absence of network activity.

### PRD-013 — Required surfaces and existential fallback

Under `CONNECTED_CHANGE_GO`, the browser Home, Organize, Apply, Working, and
Done journeys; CLI Change File application; shared STDIO MCP; receipt,
verification, convergence, and reconstruction; and live/replay planner evidence
are required. The Codex plugin remains optional under `REL-014`.

C0 is an existential product gate, not a unit-test gate. It permits the initial
implementation plus two material corrections. If the full two-layout positive
transaction and required refusal cases still do not pass, record exactly
`A3_RELEASE_FALLBACK`, preserve the failed work and evidence in ordinary Git
history, and exclude every Connected Change surface and claim from release.

### IO-012 — Strict Name Atlas Change File input

User-facing name: **Name Atlas Change File**. Technical name: **Connected Change
Capsule**. Standalone files use `*.nameatlas-change.json`; the hero uses
`northstar.nameatlas-change.json`; origin and receiver results store the exact
envelope at `name-atlas/connected_change_capsule.json`.

The raw file is at most 16 MiB and is strict UTF-8 JSON. Duplicate JSON keys,
non-finite values, unknown fields, unsupported versions, invalid canonical
fingerprints, invalid UTF-8, and oversize input block before scanning a receiver
source. Strict Pydantic v2 contracts use `extra="forbid"` and strict mode.

New schemas are:

- `connected-change-core.v1`;
- `connected-change-file.v1`;
- `connected-change-match-report.v1`;
- `folder-execution-origin.v1`;
- `folder-accepted-plan.v2`;
- `folder-refactor-job.v2`;
- `folder-change-receipt.v2`; and
- `folder-receipt-verification.v2`.

Existing `folder-inventory.v1`, `folder-reference-graph.v1`, exact Markdown
parsing, maps, and reconstruction mechanics remain reusable where their
semantics are unchanged. Existing A3 `folder-change-receipt.v1` results remain
verifiable and reconstructable by strict version dispatch. Existing verified
`folder-refactor-job.v1` jobs are read-only evidence. A nonterminal v1 job fails
with fresh-job guidance and is never silently migrated or reinterpreted.

### IO-013 — Payload-free member descriptors and disclosure

The immutable Change File Core contains schema and matching-rule versions; the
original request and fingerprint; requested result-root name; one unique opaque
Change File member ID per source file; origin relative paths as disclosed
provenance only; accepted target paths; ordinary-file size and SHA-256; exact
protected suffix and protected-member requirements; Markdown non-destination-
byte commitment; ordered supported-link slots, relationships, kinds, syntax
classes, fragments, and order; explicit empty-directory requirements; expected
source/member/link counts; expected organized-tree commitment; bounded claims;
and originating proof identifiers.

Origin relative paths do not participate in receiver matching except for
protected members and exact-path empty-directory requirements.

The Change File contains no project payload bytes, absolute local paths,
credentials, protected contents, arbitrary command or shell fragment, hidden
reasoning, filesystem mutation authority, output-promotion authority, or GPT
requirement.

Required disclosure:

> The Change File contains no project payload bytes. It does contain project names and structure, file sizes and hashes, supported link relationships, the original instruction, target names, and proof identifiers.

Permitted privacy statement: **No project payload bytes are transferred.** The
product must not say that nothing about the project is shared.

### IO-014 — Deterministic path-independent receiver matching

Each source member receives a deterministic opaque Change File member ID over a
domain separator, accepted target path, member kind, protected suffix, and its
ordinary payload descriptor or Markdown non-destination commitment. The ID can
distinguish intended target roles, but neither the ID's accepted target path nor
any origin path is matching evidence.

The ordinary-file base descriptor is member kind, exact byte size, exact
SHA-256, exact protected suffix, and protection status. Protected files also
require exact original relative path and bytes.

The Markdown base descriptor is the exact SHA-256 over ordered byte segments
outside supported destination spans plus ordered link-slot count, inline-link
or inline-image kind, syntax class, exact fragment, exact slot order, and
source/target relationship structure. Only supported relative destination text
can differ. Prose, labels, line endings, fragments, link order/count, and all
non-destination bytes must match exactly.

Matching uses this terminating fixed-point algorithm:

1. Scan the complete origin descriptors and complete receiver source.
2. Create initial equivalence classes from member kind and intrinsic descriptor.
3. Include Markdown non-destination commitment and ordered link-slot metadata in
   the Markdown base class.
4. Iteratively refine each class with ordered outgoing edges colored by the
   current target classes and sorted incoming-edge signatures colored by the
   current source classes.
5. Recompute canonical colors until a fixed point or at most `file_count`
   rounds.
6. Require equal origin and receiver class cardinalities.
7. Accept only singleton class mappings.
8. Block every remaining non-singleton class as ambiguous.

Matching ordinary members never uses an origin path, receiver path, accepted
target path, lexical ordering, filesystem iteration order, or arbitrary
tie-breaking. Protected members retain the exact-path requirement defined
above, and explicit empty-directory requirements retain their exact-path
agreement rule. Matching does not attempt general graph isomorphism or
semantic-similarity matching.

Receiver application blocks on any extra/missing member, ordinary payload
change, Markdown non-destination change, supported relationship change,
incompatible suffix, protected path/byte disagreement, empty-directory
disagreement, ambiguous duplicate group, unsupported version, invalid
fingerprint or target, source/output overlap, source or Change File change,
output collision, or organized-tree convergence failure.

Stable blocker IDs include:

- `change_file_too_large`;
- `change_file_schema_invalid`;
- `change_file_fingerprint_mismatch`;
- `receiver_member_missing`;
- `receiver_member_extra`;
- `receiver_payload_changed`;
- `receiver_markdown_content_changed`;
- `receiver_relationship_changed`;
- `receiver_suffix_mismatch`;
- `receiver_protected_member_mismatch`;
- `receiver_empty_directory_mismatch`;
- `receiver_ambiguous_duplicate_group`;
- `receiver_target_invalid`;
- `change_file_changed`; and
- `organized_tree_commitment_mismatch`.

A mismatch never invokes GPT and never becomes a user clarification.

### IO-015 — Safe in-root parent-relative Markdown links

This requirement supersedes only `IO-011`'s blanket traversal rejection. After
one strict UTF-8 percent decode, split the destination into POSIX components,
ignore `.`, process each `..` by popping one existing source-parent component,
block a pop above the selected root, append ordinary components, resolve the
normalized path case-sensitively against the logical inventory, and require
exactly one regular-file target.

Continue blocking root escape, absolute/root-relative paths, `file:` URLs,
backslashes, query strings, malformed escapes, encoded slash/backslash
ambiguity, decoded NUL, invalid UTF-8, directory or dangling targets, case
mismatch, unsupported local-looking syntax, and reference-style local links or
definitions. Exact-span scanning, right-to-left replacement, exact fragment
preservation, and byte preservation outside destination spans remain unchanged.

### TX-014 — Change File construction and canonical fingerprints

Use the existing compact canonical JSON rules: JSON-mode values, every field
including explicit null, UTF-8, `ensure_ascii=False`, sorted keys, separators
`(",", ":")`, `allow_nan=False`, and no trailing newline.

`core_fingerprint` is lowercase SHA-256 over canonical
`ConnectedChangeCore` bytes. The transferable envelope contains
`schema_version`, the complete `core`, `core_fingerprint`, the exact finalized
originating receipt envelope, and `change_file_fingerprint`.
`change_file_fingerprint` is lowercase SHA-256 over canonical envelope content
excluding that fingerprint field.

The standalone file proves its internal canonical fingerprint, its embedded
receipt fingerprint, and that the embedded receipt commits the same Core
fingerprint. It does not prove producer-source historical authenticity, sender
identity, authorship, institutional authorization, signature validity, or the
authenticity of absent payload artifacts.

### TX-015 — Receiver application and deterministic plan rebinding

Receiver application strictly verifies the Change File, scans the complete
receiver source, runs `IO-014`, creates a complete receiver-local accepted plan,
and reruns the existing compiler and all naming, overlap, source-stability,
reference, copy, and promotion checks. Every receiver file participates exactly
once. No file is invented, deleted, omitted, merged, or duplicated.

The receiver creates an absent separate result and never edits the receiver
source or Change File. It makes zero provider/API calls, zero budget
reservations, and zero external-network calls. It does not fall back to model
judgment or clarification when deterministic matching blocks.

### TX-016 — Truthful execution origins

`folder-execution-origin.v1` is a strict discriminated union:

- `gpt_planned`: live, deterministic-development, or recorded-replay kind;
  model alias and returned model identity where applicable; observable
  tool/evidence transcript; clarification/answer where applicable; evidence
  fingerprint; accepted plan; provider-call count; and API/store metadata where
  applicable.
- `capsule_applied`: Change File fingerprint; originating receipt fingerprint;
  exact match-report fingerprint; receiver-local accepted-plan fingerprint;
  provider-call count `0`; API use `false`; external-network use `false`; no
  planner progress, model identity, or fabricated evidence ledger.

Both origins use the same scanner, compiler, naming checks, reference rewriter,
copy transaction, job store, receipt builder, independent verifier,
reconstruction engine, and release proof. `FolderRefactorJob.v2` requires
planner progress only for `gpt_planned` and forbids it for `capsule_applied`.

### TX-017 — Origin and receiver result transactions

Origin order is fixed:

1. prove source equality;
2. copy/rewrite into pending result;
3. generate normal artifacts and preserved original Markdown bytes;
4. run deterministic proof;
5. compute organized-tree commitment;
6. build and fingerprint immutable Change File Core;
7. write final path-neutral verification report;
8. build `FolderReceiptCore.v2`, committing the Core fingerprint but not future
   envelope bytes;
9. finalize origin receipt envelope;
10. build/write the Change File envelope containing that receipt;
11. render offline proof;
12. rebuild tag manifest over receipt, Change File, and HTML;
13. run final BagIt validation;
14. run independent verifier;
15. rescan source; and
16. promote no-replace only after every check passes.

The origin receipt raw-artifact commitment set excludes Change File envelope,
receipt JSON, proof HTML, tag manifest, and later receiver-verification output.
It commits the Change File Core fingerprint; the final tag manifest protects the
completed envelope.

Receiver order is fixed:

1. strictly verify Change File and record raw digest/fingerprint;
2. scan complete receiver source;
3. build match report and receiver-local accepted plan;
4. rerun compiler;
5. copy/rewrite into absent pending result;
6. write receiver artifacts, receiver original Markdown bytes, execution
   origin, exact imported Change File, and match report;
7. run deterministic proof;
8. require organized-tree commitment equality;
9. create a receiver-specific receipt committing the incoming Change File and
   match report;
10. rebuild tag manifest and run final BagIt/source-free verification;
11. rescan receiver source and Change File; and
12. promote no-replace only after all checks pass.

Origin and receiver receipts differ. Their final organized-tree commitments are
identical.

### TX-018 — Receiver-specific reconstruction

Receiver reconstruction verifies the receiver result, refuses an existing
destination, uses receiver-specific reverse maps and original Markdown bytes,
recreates receiver-specific empty directories, proves every receiver-source
path/size/SHA-256, and promotes no-replace. It reconstructs the receiver's own
original layout, not the producer's, and changes none of the sources, results,
or Change File.

### CASE-010 — Versioned job origin authority

`folder-refactor-job.v2` is the sole mutable authority for both origin kinds and
persists the exact execution-origin union, Change File/match-report bindings,
receiver-local plan, result/receipt pointers, lifecycle, and every v1 persistence,
lock, expected-revision, restart, staleness, immutability, and no-replace
invariant. Terminal jobs remain immutable. Source or Change File change makes a
receiver job stale or blocked and prevents continuation/promotion.

### CASE-011 — Capsule job lifecycle and idempotent request binding

Capsule application uses the existing lifecycle without a clarification state:
planning/matching, executing, verified, stale, or blocked. It never initializes
the planner. Durable mutation requests bind a caller idempotency-key hash to an
exact canonical request fingerprint in the existing job authority. Identical
retry returns the same durable job/result; conflicting reuse blocks. No second
idempotency database or ledger is permitted.

### CASE-012 — Cross-surface service authority

Browser, CLI, shared MCP, and admitted plugin invoke the same domain services
and persistent job. They cannot duplicate planner, compiler, persistence,
receipt, verifier, reconstruction, or budget logic. A service/process restart
rehydrates the job; status reads never trigger provider, budget, copy, or
clarification work.

### AI-013 — Planner versus Change File authority

Only origin planning uses GPT-5.6. It preserves exact `gpt-5.6`, Responses API,
strict tools, `store=false`, no fallback, no provider retry, the existing turn/
evidence/repair/clarification bounds, and one cumulative budget ledger.

Capsule application is mechanically forbidden from importing or initializing a
planner/provider, credential, budget reservation, or external-network client.
It records `capsule_applied`; it cannot display GPT planning progress or copy
origin evidence as if generated on the receiver.

After C0 and contract stabilization, release qualification requires one new real
zero-question origin run and one new real one-clarification origin run, plus
sanitized exact replays. The historical DecisionCard cannot qualify them. The
sole budget ledger migrates monotonically from request cap 8 to 13 while
preserving the one historical request/attempt, USD 0.679 committed exposure,
USD 0.0382 reported estimated cost, every count, and the cumulative USD 10 cap.
No second ledger or reset is permitted.

### UX-013 — Home and Organize journey

`GET /` renders Home when no job is active and otherwise routes by persisted
state. Home offers **Organize a folder** and **Apply a shared change**.

Organize shows **Choose folder…**, **What should change?**, a derived result
next to the source, secondary **Change result location…**, and **Plan and create
copy**. It visibly states:

> Your original folder will not be changed. Name Atlas will create and verify a separate result.

The accurate outbound-evidence and retention disclosure from `AI-012` remains
collapsed but must be acknowledged before origin planning.

### UX-014 — Apply, Working, and Done journeys

Apply shows **Choose Change File…**, **Choose your project folder…**, derived
result location with optional override, and **Apply change and create copy**. It
visibly states:

> Applying a Change File makes no GPT call, requires no API key, makes no external network request, and does not change your selected project folder.

Working displays only true stages: Reading folder; GPT-5.6 is planning **or**
Matching the shared change; Checking every file and destination; Creating the
new folder; Updating supported links; Verifying the result. Apply never shows a
fake GPT stage.

Done leads with **Your new folder is ready** and shows file, changed-path, and
updated-link counts; unchanged source; independent verification; Change File
identity; and reconstruction statement. Actions are **Show in Finder**,
**Download Change File**, **See changes**, **View proof**, **Verify again**, and
**Recreate original layout**. Technical hashes, schemas, transcripts, BagIt,
and receipt details stay collapsed.

Required routes are `GET /`, `GET /start`, `POST /start`, `GET /apply`,
`POST /apply`, `POST /choose-path`, `GET /working`, `GET /status`,
`POST /clarify`, `GET /done`, `GET /download-change-file`,
`POST /show-in-finder`, `POST /verify-again`, and
`POST /recreate-original`.

### UX-015 — Bounded native macOS picker and Finder bridge

Keep the loopback FastAPI/Jinja/Blueprint application; do not introduce a native
wrapper, Electron, Tauri, Swift, pywebview, PyObjC, React, or Vite.

`POST /choose-path` is loopback-only and uses existing trusted-host,
same-origin, cross-site, and CSRF protections. It accepts only role
`source_folder`, `output_parent`, `change_file`, or `restore_destination`; maps
that enum to one fixed application-owned AppleScript; invokes exact
`/usr/bin/osascript` without a shell or browser-text interpolation; permits one
picker process; enforces 120 seconds; terminates/reaps on timeout; distinguishes
selected, cancelled, unavailable, timeout, and failed; returns no path on any
non-selection; and performs no scan, hash, job creation, provider call, or copy.
Directory roles use `choose folder`; Change File uses `choose file`. Because a
native folder dialog selects an existing directory while reconstruction requires
an absent destination, `restore_destination` treats the selected directory as
the parent, derives and displays one absent child destination, and validates
that derived path only when reconstruction is submitted. Every other selection
is likewise validated only when its main form is submitted.

Manual editable paths remain required on every platform and in judge
automation. Unsupported platforms use them.

`POST /show-in-finder` can invoke fixed `/usr/bin/open`, no shell, with a short
timeout, only for a verified terminal-job path already held server-side. It
cannot accept an arbitrary browser path. Unsupported platforms display/copy the
path.

### UX-016 — Responsive and truthful release experience

FastAPI/Jinja/locally packaged Blueprint remains server-authoritative. Minimal
JavaScript is limited to polling, disclosure, native-picker invocation,
clipboard, and local filtering.
Acceptance includes 1280×720 and 390×844, semantic/keyboard/focus/contrast
review, and truthful origin-specific progress. Responsive layout is not a
mobile app, remote phone access, or native-file-access claim.

### VER-015 — Change File and organized-tree commitments

Add `name-atlas/execution_origin.json`,
`name-atlas/connected_change_capsule.json`, and, on receiver results only,
`name-atlas/connected_change_match_report.json`.

The organized-tree commitment is lowercase SHA-256 over canonical JSON for the
sorted complete list of every regular member below `data/` with path, size, and
SHA-256, plus every explicit empty directory with path and member kind. It is
path-sensitive and is the cross-layout convergence authority. The A3 staged-
data commitment remains for v1 compatibility.

The acyclic dependency graph is:

`Change File Core → origin receipt commits Core fingerprint → Change File envelope embeds origin receipt → envelope fingerprint excludes itself → final tag manifest protects envelope`

No artifact commits its own bytes or fingerprint.

### VER-016 — Independent Change File and receiver verification

Strict source-free verification validates the incoming Change File fingerprints,
embedded receipt binding, raw imported Change File digest, execution origin,
match report, receiver-local accepted plan, complete bijection, naming,
reference relationships, original Markdown bytes, receipt, BagIt, organized-
tree commitment, and report agreement. It needs no GPT, API key, budget, job,
browser, network, or original source. Optional source comparison adds current
source equality only.

Origin and receiver receipts use distinct v2 semantics and strict dispatch.
Unrelated-location Change File application and result verification must pass.

### VER-017 — Required convergence and refusal matrix

Under `CONNECTED_CHANGE_GO`, release evidence includes exactly one polished
24-file zero-question origin, one one-question origin, one Sofia-to-Martin
differently arranged equivalent receiver, and refusals for changed payload,
changed non-destination Markdown, changed supported relationship, symmetric
duplicate, protected disagreement, invalid Change File fingerprint, and the
existing receipt-integrity alteration.

The Sofia/Martin transaction must prove different source commitments, the same
supported logical project, zero receiver provider/API/budget/external-network
use, both sources unchanged, both results independently verified, identical
organized-tree commitments, and receiver reconstruction equal to Martin's own
original paths and bytes.

### VER-018 — Reconstruction and immutable-input proof

Receiver reconstruction obeys `TX-018`. Origin and receiver source trees,
origin and receiver results, and the Change File are rescanned at the required
boundaries and remain unchanged. A failed match or transaction promotes no
accepted result. Failure evidence stays outside immutable receipt domains.

### REL-012 — Required CLI, fixtures, and profile dispatch

Preserve existing stable commands and add:

- `uv run name-atlas apply-change CHANGE_FILE --source SOURCE_ROOT [--output OUTPUT_PARENT] [--job JOB_FILE]`;
- `uv run name-atlas mcp`.

`apply-change` dispatches before planner, provider, credential, and budget
initialization. Replay, Change File application, verifier, and reconstruction
remain keyless. Missing live credentials cannot affect them. Live origin
planning uses exact `gpt-5.6` without fallback.

The final fixture surface is exactly the positive and refusal matrix in
`VER-017`; do not create multiple polished projects.

### REL-013 — Required shared STDIO MCP server

Under `CONNECTED_CHANGE_GO`, use stable official Python MCP v1 with
`mcp>=1.27,<2`. There is one STDIO server and one implementation of each domain
service. It exposes exactly:

- `plan_and_create_copy`;
- `job_status`;
- `answer_clarification`;
- `get_change_file`;
- `apply_change_file`;
- `verify_result`; and
- `recreate_original`.

It exposes no arbitrary read/write/rename/move/delete, shell, raw planner
evidence tool, compiler bypass, direct receipt creation, proof override, or
approval bypass.

`plan_and_create_copy` requires tool input
`evidence_disclosure_acknowledged=true` for the exact bounded outbound-evidence
and retention disclosure. Without literal boolean `true`, the server returns a
structured non-mutating requirement and performs no scan, job mutation,
provider call, or budget reservation.

Every mutation tool accepts a caller idempotency key matching
`^[A-Za-z0-9][A-Za-z0-9._:-]{15,127}$`, binds its SHA-256 to the canonical
request fingerprint inside the existing job, returns the same durable
job/result for an identical retry, and blocks conflicting reuse. Clarification
answers bind expected revision and question fingerprint. Reconstruction stays
no-replace. No second idempotency store exists.

Origin and receiver start tools first complete the required local inventory
preflight: validate paths and input shape, read the Change File where applicable,
and stream/hash the complete selected source. They then persist and return the
durable job handle before provider planning, matching, copying, or result
creation finishes; subsequent long work uses `job_status`. This preflight is
fast for the demonstrated 24-file hero but is not constant-time or promised to
return within a fixed interval for arbitrarily large admitted payloads. A
provisional undurable handle or second intake authority is prohibited.

Process restart rehydrates and schedules unfinished durable work. Status polling
itself is read-only. Logs use STDERR; STDOUT is MCP protocol only. Credentials
come only from local environment. Tool schemas reuse browser/CLI validation.
The server `instructions` first 512 characters self-contain start → status →
optional answer → status and fixed limits. An actual Codex invocation against
this shared server is required before the plugin decision.

### REL-014 — Optional Codex plugin gate

After every required browser, CLI, MCP, GPT, Change File, receipt, verifier,
reconstruction, C0-positive, and C0-negative surface passes with no material
defect, adjudicate once as `GO` or `CUT_BY_PREAUTHORIZED_GATE`. `GO` additionally
requires at least 12 actual hours before recording readiness, enough time before
feature freeze, conservative work estimate at most four hours, and no duplicate
core logic.

If admitted, use the official plugin-creator workflow only after the gate. The
plugin contains `.codex-plugin/plugin.json`, relative `.mcp.json`, no absolute
developer path, and the same MCP server. Acceptance requires a repository
marketplace entry in the clean public clone, `uv sync --frozen`, installation
from that marketplace, app restart/refresh, a new Codex task, discovered tools,
real invocation, keyless replay, clear missing-key live behavior, complete
result, proof that the installed cache copy—not the developer checkout—ran, and
working install/uninstall instructions. Codex is the mandatory tested client.
Claude is only an optional smoke test; other hosts are not called tested without
actual installation and invocation.

### REL-015 — Timing, feature freeze, and recording readiness

At C+0 calculate actual hours to feature freeze and recording readiness. The
sole plan scales pre-freeze C0–C5 anchors, but these absolute boundaries do not
move:

- feature freeze: Monday 20 July 2026 at 14:00 CEST;
- release candidate: Monday 20 July 2026 at 20:00 CEST;
- recording ready: Tuesday 21 July 2026 at 02:00 CEST;
- submission: Wednesday 22 July 2026 at 02:00 CEST.

C0's latest decision is the earliest of its scaled target, C+8 hours, or the
point when only 32 actual hours remain before feature freeze. If already past at
C+0, select `A3_RELEASE_FALLBACK` immediately. Targets drive integration and
cuts; they never prove completion.

After selected-profile feature freeze, only defects, proof integrity,
accessibility, visual QA, clean installation, documentation, screenshots,
claims, rehearsal, packaging, and release work continue. Regenerate every stale
release artifact. Recording readiness requires selected release commit, clean
public repo/clone, final live/replay evidence, selected-profile fixtures,
receipts, verifier, reconstruction, required shared MCP under Connected Change,
admitted plugin only if fully passed, responsive/browser proof, timed narration,
shot list, screenshots, Devpost drafts, Codex/GPT contribution, prior/new-work
disclosure, known `/feedback` path, a rehearsed public-video duration strictly
below three minutes, no planned code/design change, and the active submission
hold.

### CLAIM-006 — Permitted Connected Change claims

When demonstrated under `CONNECTED_CHANGE_GO`, the product may say:

> GPT-5.6 plans the connected-folder change once, and Name Atlas can deterministically apply and verify the same change on a differently arranged equivalent copy without another GPT call or transfer of project payload bytes.

It may also state that every in-scope file is accounted for once; protected
files remain fixed; demonstrated supported Markdown links reach the same
logical files; originals remain unchanged; another person can apply the change
without an API key; symmetric duplicates and changed relationships block; the
origin and receiver converge to the same organized tree; and each receiver can
reconstruct its own original layout.

### CLAIM-007 — Connected Change limitations and exclusions

Do not claim semantic equivalence, reconciliation of independently edited
copies, extra/missing-file reconciliation, general graph isomorphism, universal
format understanding, media/PDF/Office/spreadsheet semantic understanding,
code-aware refactoring, arbitrary connection preservation, universal
portability/reversibility, native Windows testing, mobile/remote phone access,
zero API retention, full privacy, absence of disclosed metadata, sender/authors
authentication, signatures, institutional authorization, historical
authenticity, tamper-proofing, compliance, production readiness, universal
zero-question behavior, unmeasured time savings, broad adoption, untested MCP
clients, competitor nonexistence, or winning probability.

Freeze out native desktop wrappers, hosted service/cloud sync,
accounts/collaboration database, arbitrary filesystem MCP, general semantic
matching, source reconciliation, independently modified copies,
application-specific or AI-training-data adapters, JSONL/Parquet/Hugging Face,
NER/ReFinED, repository/Archivematica integration, second planner/job/ledger/
receipt/verifier/reconstruction engine, multiple client-specific MCP servers,
multiple polished projects, further discovery, benchmark platform, or
validation harness.

Under `A3_RELEASE_FALLBACK`, only the implemented A3-derived AI-first claims in
`CLAIM-004`–`CLAIM-005` survive. Every Change File, Apply, cross-layout, shared
MCP, native-picker expansion, convergence, and plugin claim is excluded.

## 14. Selected-profile recording-readiness Definition of Done

The selected release profile is recording-ready only when C0 has an exact
terminal profile; every non-cut requirement of that profile is integrated and
semantically verified through its user-visible transactions and downstream
consumers; full suites and clean-clone commands pass; regenerated release
materials and claims match actual behavior; the optional plugin is either fully
accepted or exactly cut; no planned product or design work remains; and final
submission is still held for the user's voice, `/feedback`, due diligence, and
explicit release.

## 15. Foldweave native-review extension and narrow supersessions

### Controlling sources, boundaries, and inherited status

The complete Foldweave contract was refrozen from these attachments, each read
through EOF before this governance revision:

| Authority | Path | Logical lines | Newlines | Bytes | SHA-256 | EOF |
|---|---|---:|---:|---:|---|---|
| Detailed product, review, lineage, native-app, proof, and acceptance contract | `/Users/nikolai/.codex/attachments/fe25f08d-09df-477d-b5dc-899d6b1da370/pasted-text.txt` | 1,725 | 1,724 | 65,947 | `015d9ea56b6bcaac9d0eb6d7c6324a803d5a23429fcd652e9ad83474daf1289e` | Complete; no final newline; final byte `*` |
| Single-control governance and 44-hour operating model | `/Users/nikolai/.codex/attachments/d6568a9c-464c-46ff-a6e9-25c40f217126/pasted-text.txt` | 996 | 995 | 35,564 | `178f131a0423854c3a9a827bad0d66ba3e0ca590df9580689472eabad67459d0` | Complete; no final newline; final byte `.` |
| Foldweave, four modes, mandatory ChatGPT, gateway/companion, USD 40, and activation refinements | `/Users/nikolai/.codex/attachments/911f299e-7804-4ea5-aafe-67fb2eff1e0e/pasted-text.txt` | 1,453 | 1,452 | 55,479 | `78c94970191e9023e320abdf53ab017f7a4416e9db4d61ab59406193be1865ec` | Complete; no final newline; final byte `.` |

Authority order is current user instruction; the third attachment for Foldweave
identity, mandatory dual live planning, billing separation, gateway/companion,
USD 40, branch, and F+0; the first attachment for review, lineage, native app,
proof, acceptance, and claims; the second attachment for governance, timing,
sequencing, audit, feature freeze, and the submission hold; inherited
governance where it does not conflict; fresh evidence for facts; then verified
older context.

The following current official boundaries control this cycle:

- feature freeze: **Tuesday 21 July 2026 at 01:00 CEST**;
- release candidate: **Tuesday 21 July 2026 at 06:00 CEST**;
- recording ready: **Tuesday 21 July 2026 at 10:00 CEST**;
- submission deadline: **Wednesday 22 July 2026 at 02:00 CEST**.

The 44-hour envelope began with the user's decision and is not reset by delayed
F+0 activation. Earlier dates in Sections 1–14 are predecessor-cycle evidence,
not future Foldweave authority. Final submission remains prohibited until the
completed Foldweave release, renewed materials, final public video,
`/feedback`, due diligence, and submission package are complete and the user
explicitly releases the hold.

The official-source baseline for this extension is the current Build Week
rules/FAQ/dates; GPT-5.6 Sol, function-calling, and Your Data documentation;
Apps SDK MCP server, ChatGPT UI, authentication, connection, MCP Apps
compatibility, Secure MCP Tunnel, and submission documentation; current Codex
MCP and plugin documentation; official pywebview, PyInstaller, Apple Keychain,
Cloudflare OAuth-provider, Workers KV, Durable Objects, and WebSocket
Hibernation documentation. The current Codex MCP URL redirects to
`https://learn.chatgpt.com/docs/extend/mcp?surface=cli`; the current plugin guide
is `https://learn.chatgpt.com/docs/build-plugins`; the current pywebview API is
`https://pywebview.flowrl.com/api/`; and Apps are currently submitted and
published as plugins. Those redirects and terminology do not change the
product contract.

The inherited implementation is labelled:

`COMPLETED CONNECTED-CHANGE C0–C7 RELEASE BASELINE — VERIFIED IMPLEMENTATION, NOT PROOF OF FOLDWEAVE NATIVE REVIEW, DUAL LIVE TRANSPORTS, OR DERIVATIVE REVISION`

These narrow supersessions control future work:

| Existing authority | Foldweave authority |
|---|---|
| Reversible Name Atlas/Name Atlas active identity | `PRD-014` makes Foldweave the active identity. |
| Automatic execution immediately after mechanical acceptance | `TX-019`–`TX-020` require review and exact human authorization first. |
| `folder-refactor-job.v2` for new jobs | `CASE-013` makes `folder-refactor-job.v3` authoritative for new review-era jobs. |
| `connected-change-file.v1` for new output | `IO-020` and `TX-024` require v2 Foldweave output and preserve strict legacy import. |
| receipt v2 for new output | `VER-020` requires receipt/verifier v3 for new output. |
| optional ChatGPT visualization | `PRD-016`, `AI-016`, and `UX-022` require real ChatGPT-hosted planning and widget review. |
| Secure MCP Tunnel as a possible general route | `REL-020` limits it to developer qualification. |
| cumulative USD 10 / call-cap 13 authority | `AI-020` raises only the sole direct-API monetary ceiling to USD 40 after F+0. |
| browser-only primary product | `PRD-017` and `REL-018` require a packaged macOS app with browser fallback. |
| native wrapper, React, Vite, pywebview exclusions | `UX-017`, `UX-021`, and `REL-017` admit only a narrow pywebview shell and focused React review/widget island. |
| automatic high-level MCP execution | `REL-021` requires reviewed host-planning and exact-acceptance layers. |
| Name Atlas CLI and Change File branding | `REL-016` and `IO-020` make Foldweave primary while preserving strict compatibility. |

### PRD-014 — Foldweave identity, audience, and promise

- Product name: **Foldweave**; exact casing is `Foldweave`, never `FoldWeave`.
- Tagline: **Change the structure. Keep the connections.**
- Track: **Work & Productivity**.
- Category: **AI refactoring for connected project folders**.
- User-facing artifact: **Foldweave Change File**.
- Primary CLI: `foldweave`.
- Native application: `Foldweave.app`.
- Do not perform a brand, domain, trademark, or product-name conflict search in
  this cycle.

Definition:

> Foldweave is a packaged local-first macOS application that lets a user or a ChatGPT/Codex host propose a complete reorganization of a connected project folder, renders the current and proposed structures before execution, supports bounded iterative revision, and creates a separate verified result only after the user accepts the exact proposal. Foldweave preserves every supported file, rewrites supported Markdown links deterministically, produces a payload-free transferable Foldweave Change File, independently verifies the result, and can recreate the selected source layout and bytes for that transaction.

Primary differentiator:

> Change the structure of a connected project once, review it before execution, and apply or refine that verified structure wherever an equivalent copy exists.

“Connections” means only the supported relative Markdown links inside the
selected folder. It never implies arbitrary code, database, Office, PDF,
embedded, application, or cloud references.

### PRD-015 — Audience, origin review, and receiver review

The audience remains people preparing complicated connected project folders for
handoff or reuse. Journey A creates a new Foldweave: select source, describe the
change, select direct API or ChatGPT-hosted planning, acknowledge disclosure,
plan and compile, stop at review, compare original/proposed, revise or accept,
then create and verify a separate copy and Change File.

Journey B imports a verified Change File and a differently arranged but strictly
equivalent local source, deterministically matches every member, stops at review,
and renders **Your current folder** versus **Shared proposal** without GPT.
The receiver may accept unchanged with no model/API/budget/external model
request, or create an immutable derivative child through either live planning
transport and review that complete child proposal before acceptance.

### PRD-016 — Four mandatory execution modes and Codex surface

Exactly four model-provenance modes are required:

| Mode | Model inference | Foldweave credential | Direct ledger | Required outcome |
|---|---|---|---|---|
| Native direct API | exact `gpt-5.6` through Responses API | user-supplied OpenAI API key | yes | complete planning and revision in `Foldweave.app` |
| ChatGPT-hosted | model supplied by the user's ChatGPT session | no Foldweave Responses API key | no | complete planning and revision in macOS ChatGPT through the paired companion |
| Recorded replay | none | none | no | exact labelled keyless replay of committed planning evidence |
| Unchanged Change File application | none | none | no | deterministic receiver review and exact unchanged application |

Codex is an additional required access surface over the same MCP and domain
services; it is not a fifth model-provenance category or a second engine. Both
live transports are mandatory. OAuth authenticates and authorizes Foldweave
access; it does not convert a ChatGPT subscription into Responses API credit.
ChatGPT and API Platform billing remain separate.

### PRD-017 — Required surfaces and single authority

The required release surfaces are packaged macOS Apple Silicon application,
browser fallback, CLI, local STDIO MCP/Codex, authenticated public HTTP
MCP/ChatGPT widget and companion, recorded replay, Change File application,
proof, verifier, and reconstruction. One Python deterministic engine and one
durable job authority serve all surfaces. Python owns business and persistence
state; React, Jinja, widgets, pywebview, ChatGPT, and Codex are presentation or
transport clients only.

### PRD-018 — Serial collaboration and deliberate limits

Support explicit serial forks, not live collaboration or merge:

`Sofia original → CF1/T1 → Martin current review → unchanged T1 or revised T2 → CF2 → Sofia applies T2`

One derivative child has one immutable immediate parent. No automatic merge,
accounts, cloud project database, live shared state, recursive ancestor-envelope
embedding, or runtime dependency on older Change Files is permitted. A child
Change File is complete and self-contained. Each transaction reconstructs the
source selected when that transaction began, not the first ancestor of the
collaboration chain.

### IO-016 — Native credentials and direct endpoint

Define a `CredentialStore` Protocol with a Keychain implementation for the
packaged app and environment/session implementation for development and
automation. A small Cocoa/PyObjC `NSSecureTextField` sheet supplies secure native
entry because pywebview's public dialog API does not define a password field.
The key is readable only by trusted Python and never enters React, the DOM,
localStorage, Zustand, browser storage, logs, screenshots, jobs, receipts,
replays, MCP, ChatGPT, or Change Files. Expose only configured/not-configured
state and a visible **Remove key** action.

There are two non-interchangeable credential roles. The runtime product key is
supplied, controlled, and removable by the product user and is used only for
that user's native direct-API transactions. A development-qualification key is
a separate narrowly restricted project credential used only for bounded build
qualification. It is never bundled, distributed, copied into the product-user
Keychain item, persisted as a user key, or used as evidence that consumer
credential entry works. Neither role can be used to infer the presence of the
other.

Default endpoint is `https://api.openai.com/v1`. Require HTTPS; reject userinfo,
fragments, unexpected query parameters, and cross-origin redirects; display the
actual destination before save; and preserve exact `gpt-5.6` only for the
official endpoint. A compatible custom endpoint is a separate advanced profile
and inherits no OpenAI model, pricing, `store=false`, or retention claim without
evidence.

### IO-017 — Opaque handles and evidence boundaries

Absolute local paths never cross the public gateway. Folder and Change File
selection happens in the companion and returns opaque, device-bound, expiring
handles. Host evidence tools expose only the same bounded eligible inventory,
selected excerpts, and supported-link facts authorized by the job. Source text
is untrusted data and cannot expand tool authority. Protected content,
credentials, arbitrary payloads, absolute paths, and unrelated files remain
ineligible.

### IO-018 — Gateway and companion transport inputs

Every public request binds OAuth grant, paired device, scope, per-job
capability, request ID, issue/expiry time, canonical body digest, replay nonce or
monotonic sequence, and Ed25519 device signature. The companion opens the
outbound authenticated WSS connection; the Durable Object accepts it as the
server through the Hibernation API. Reject expired, replayed, revoked,
cross-device, cross-job, malformed, or scope-incompatible input. Reconnects bind
the same canonical request and cannot duplicate a provider call, job, answer,
result, or reconstruction.

The per-job capability is a local, device-key-derived authority whose hash,
device, grant, scope set, and expiry are immutable in JobV3. Public MCP input
binds only the opaque job ID; after the gateway and companion verify the exact
device/grant/scope/request envelope, the local host rederives and validates the
capability internally. Its raw bearer value never crosses the gateway, enters
an MCP tool schema or result, appears in `structuredContent` or `_meta`, reaches
the model/widget, or enters browser/widget state. The inclusive lifetime remains
thirty minutes, after which a fresh job is required.

### IO-019 — App and cross-surface state

Durable state is `FolderRefactorJobV3`, never localStorage, Zustand, widget
state, Cloudflare, or browser memory. Every surface rehydrates the same job by
opaque local authority and exact revision/fingerprints. Frontends may persist
window geometry and ephemeral presentation preferences only. Missing, corrupt,
unsupported, stale, or unauthorized state fails closed rather than being
reconstructed from UI memory.

New production v3 application state has one default root:

`~/Library/Application Support/Foldweave/`

Its `jobs/`, preferences, bounded diagnostics, and temporary application-owned
state are owned by the local Python control plane. The production native app,
paired companion, and its browser view use that same root. Development and
automation may inject one alternate `FOLDWEAVE_STATE_ROOT`; CLI `--job` may
select one exact job file. Once a transaction is created, its selected job file
is its sole authority and must never be mirrored into a second store.

Existing `~/Library/Application Support/Reversible Name Atlas/` state and
project-local `.name-atlas/jobs/` remain legacy stores. Finalized v1/v2 jobs
are read strictly under their historical schemas for verification,
reconstruction, and supported application. Nonterminal legacy jobs fail with
fresh-v3-job guidance. There is no automatic or in-place migration. Any future
explicit migration must create a new v3 transaction while leaving the legacy
record byte-for-byte unchanged.

### IO-020 — Foldweave Change File v2 and legacy dispatch

New artifacts use `connected-change-core.v2`,
`connected-change-file.v2`, suffix `*.foldweave-change.json`, hero
`northstar.foldweave-change.json`, and user-facing name **Foldweave Change
File**. Preserve the 16 MiB strict UTF-8 JSON boundary, duplicate-key/non-finite/
unknown-field/version/fingerprint checks, canonical JSON rules, payload-free
content, metadata disclosure, and deterministic matcher from v1.

Legacy `*.nameatlas-change.json`, v1/v2 jobs and receipts, schema IDs,
fingerprint domains, and `name-atlas/` artifact paths remain under strict
version dispatch. Finalized legacy jobs/artifacts remain readable, verifiable,
and reconstructable; nonterminal legacy jobs fail with fresh-job guidance and
are never silently rewritten.

Every valid, application-capable `connected-change-file.v1` /
`*.nameatlas-change.json` remains applicable unchanged under its exact
historical matching and execution semantics. Foldweave prepares a new v3
receiver review around that immutable v1 parent, preserves the imported bytes
on unchanged acceptance, and may create a derivative only as a complete,
self-contained v2 child. The v2 child references the immediate v1 parent by its
actual historical fingerprints, never mutates or embeds the parent, and must
apply without possession of the v1 file. An old artifact whose version never
supported application is refused rather than upgraded by inference.

### IO-021 — Complete deterministic receiver representation

Martin's current tree is derived from his complete scanned inventory, explicit
empty directories, protected members, and supported-link graph. The shared
proposal is derived from the verified Change File, deterministic match report,
and receiver-local complete candidate. Every local member is represented once.
No GPT call is required or permitted merely to prepare or render the current/
shared comparison. Match failures remain terminal blockers and never trigger
semantic guessing, lexical path selection, arbitrary iteration order, or GPT
fallback.

### TX-019 — Review barrier

Every new origin or receiver job must stop in `reviewing` with one immutable
complete candidate and preview. While reviewing, no result, receipt,
verification output, reconstruction authority, or new Change File exists.
Planning-provider reservations legitimately used to create or revise a proposal
may exist, but no copy transaction has started. `POST /start`, `POST /apply`,
CLI `run`, and CLI `apply-change` prepare review jobs and never execute
implicitly.

### TX-020 — Exact fingerprint-bound authorization

The action is **Accept this structure and create copy**. Authorization binds job
ID, expected job revision, proposal revision, source commitment, imported
Change File fingerprint, match-report fingerprint, exact candidate fingerprint,
exact preview fingerprint, output parent, result-folder name, caller
idempotency key, channel (`native_app`, `browser`, `chatgpt_hosted`,
`codex_mcp`, `local_mcp`, or `cli`), authorization timestamp, and schema
version. Persist authorization transactionally before execution.

Reject stale-tab acceptance, revise/accept races, double clicks, duplicate MCP
work, destination/source/Change File/job/candidate/preview changes, wrong
channel/capability, and restart ambiguity. Identical retries return the same
job/result; conflicting reuse blocks.

### TX-021 — Bounded sparse revision

Allow at most two user-requested revisions and one model-originated
clarification per planning job. Counters never reset. Direct mode preserves the
existing response/evidence/byte/repair/no-retry limits. ChatGPT-hosted mode uses
the same evidence/byte limits, one clarification, two user revisions, and at
most an initial submission plus two mechanically corrected submissions.

A sparse revision contains only the exact base-candidate fingerprint, optional
result-root replacement, affected file IDs, replacement target paths, concise
rationale, and cited evidence IDs. Deterministic code verifies the base,
rejects missing/unknown/duplicate IDs, changes only listed mappings, preserves
all unlisted mappings, rejects protected or forbidden empty-directory changes,
and rejects deletion, omission, merge, duplication, or invention. It rebuilds
the complete candidate, rederives every supported-link rewrite, and reruns all
file-accounting, naming, suffix, tree, collision, source, Change File, output,
and link checks before creating one complete replacement preview.

### TX-022 — Revision failure and parent preservation

A failed revision leaves the prior valid preview intact, records the exact
failure, creates no result or Change File, and cannot be accepted as successful.
Offer **Try another change** and **Keep previous proposal**; keeping the prior
proposal is a durable state transition. A receiver derivative creates an
immutable child job and never mutates or destroys the parent's deterministic
unchanged-acceptance route.

The parent and all derivative children share one destination-reservation
domain. Exact output parent and result-folder name are transactionally reserved
before execution. Simultaneous parent/child or sibling acceptance for the same
destination must produce one deterministic reservation winner and fail every
other contender closed before any copy, or fail all contenders without a
partial result. No job may silently overwrite, reuse, or race a related job's
pending or final destination.

### TX-023 — Receiver parent and derivative child

Unchanged receiver acceptance makes no GPT/direct-API/budget/external-model
request, executes as `capsule_applied`, and preserves the exact imported Change
File bytes. A requested next proposal creates a child bound to the parent
candidate and preview, uses direct API or ChatGPT-hosted planning, compiles a
complete T2 proposal, stops for review, and executes only after exact
acceptance as `gpt_revised_from_change_file`. The exported child is a complete,
self-contained v2 Change File, never a sparse transferable patch, and cannot be
exported before verified execution.

### TX-024 — Change File v2 lineage and acyclic proof graph

The self-contained child commits one immediate parent: parent Change File and
Core fingerprints, parent originating-receipt fingerprint, parent organized-
tree commitment, parent candidate fingerprint, generation, revision-instruction
fingerprint, and parent-to-child member bindings. It never recursively embeds
ancestor envelopes.

A root Change File has lineage generation `0`; a child is exactly its parent's
generation plus one. Generation `32` is the inclusive maximum, so creation of a
generation-33 child blocks before receipt or artifact construction. Canonical
UTF-8 bytes for the complete immediate-parent lineage object, including member
bindings, are limited to 1,048,576 bytes inclusive; 1,048,577 bytes blocks.
The byte ceiling is a defensive parser and future-schema limit: the current v2
schema permits at most 500 fixed-shape member bindings, so no valid current-v2
lineage can naturally reach one MiB. Acceptance therefore requires both the raw
size guard at 1,048,576/1,048,577 bytes and a canonical maximum-valid-current-
schema lineage containing all 500 bindings. Do not add padding or expand the
500-member product boundary merely to manufacture a one-MiB valid object. The
generation limit and the applicable byte/shape limits are verified before
execution authorization can yield an exportable child. The complete Change
File still remains within the inherited 16 MiB raw-file limit.

The fixed graph is:

`immutable parent Change File → child ConnectedChangeCoreV2 → ReceiptCoreV3 → finalized receipt envelope → child Change File envelope → final BagIt tag manifest`

The receipt commits the child Core fingerprint, never future envelope bytes.
The file proves internal consistency and identity, not sender identity,
authorship, institutional authorization, signature validity, or historical
authenticity.

### TX-025 — Convergence and round-specific reconstruction

Descendants may apply to a raw strictly equivalent source or a verified prior
Foldweave/Name Atlas result's `data/` directory. If a result root is selected,
verify it first and locate `data/` deterministically. Preserve every inherited
matching blocker and path-sensitive organized-tree commitment, including empty
directories. Every accepted T2 endpoint converges to the same organized-tree
commitment. Reconstruction first verifies the selected result and recreates
the exact paths and bytes of the source selected when that transaction began.

### CASE-013 — Review-era job v3 lifecycle

All new work uses strict `folder-refactor-job.v3`. Its allowed transitions are:

| From | Allowed next state | Condition |
|---|---|---|
| created origin job | `planning` | A live or replay planner is required. |
| created derivative child from a reviewed imported proposal | `revising` | The immutable parent preview is the bound base for the first complete derivative replacement. |
| created receiver-parent job | `matching` | An imported Change File is being verified and rebound. |
| `matching` | `reviewing` | Deterministic matching and compilation produce one complete valid receiver preview. |
| `planning` | `awaiting_clarification` | The sole permitted model clarification is required. |
| `planning` | `reviewing` | A complete submission compiles and passes every mechanical check. |
| `awaiting_clarification` | `planning` | The exact bound answer is accepted once. |
| `reviewing` | `revising` | One permitted user revision is durably bound to the visible preview. |
| `reviewing` | `executing` | Exact authorization for that preview is persisted. |
| `revising` | `reviewing` | The sparse revision recompiles to one complete valid replacement preview. |
| `revising` | `revision_failed` | Provider or deterministic replacement construction fails while the prior preview remains intact. |
| `revision_failed` | `revising` | The user selects **Try another change** within remaining limits. |
| `revision_failed` | `reviewing` | The user durably selects **Keep previous proposal**. |
| `executing` | `verified` | Separate result, receipt, independent verification, applicable Change File, and reconstruction authority are complete. |

Any nonterminal operational state may transition to `stale` when a committed
source or imported Change File changes, or to `blocked` on a terminal
job-specific failure. `stale`, `blocked`, and `verified` are terminal. An
unchanged receiver-parent transaction never enters `planning`,
`awaiting_clarification`, or `revising`; it follows
`matching → reviewing → executing → verified`.

Only a new origin job begins in `planning`. A derivative child created from an
already reviewed imported proposal begins in `revising` because its immutable
parent candidate and preview are the exact base of its first model turn; it
reaches `reviewing` only after the complete derivative proposal compiles.

### CASE-014 — Immutable preview DTO

Add `folder-plan-preview.v1` containing job ID, expected job revision, proposal
revision, basis (`fresh_gpt_plan`, `imported_change_file`, or
`gpt_derivative`), local source commitment, optional imported Change File and
match-report fingerprints, optional immediate-parent candidate fingerprint,
all current/proposed members, stable local member IDs, current/proposed paths
and directory prefixes, explicit empty directories, protection, change class,
supported-link effects, collision/blocker findings, exact counts, compiled-
candidate fingerprint, and preview fingerprint.

This is the only renderer- and authorization-facing DTO for native React,
browser fallback, ChatGPT widget, Codex, local STDIO MCP, and public HTTP MCP.
No renderer may infer or merge a proposal from multiple responses.

### CASE-015 — Idempotency, concurrency, and staleness

All modifying requests bind the canonical request fingerprint, caller
idempotency key, job ID, expected revision, relevant question/candidate/preview
fingerprints, source commitment, Change File commitment, and channel/capability
inside the sole job. Accept-versus-revise races serialize. Double clicks and
retries cannot create duplicate provider calls, answers, results, receipts, or
destinations. Source or imported-file changes invalidate review. Process locks,
expected revisions, atomic writes, no-replace promotion, and terminal
immutability remain mandatory.

Destination reservation participates in the same transaction authority and is
shared by an imported parent and every derivative child or sibling. A
simultaneous same-output acceptance has exactly one recorded winner or no
winner; every loser receives a stable fail-closed collision and no partial
pending tree.

### CASE-016 — Restart and cross-surface rehydration

Restart must recover `matching`, `planning`, `awaiting_clarification`,
`reviewing`, `revising`, `revision_failed`, `executing`, and `verified` from the
job without reconstructing authority from a renderer or duplicating work. A job
created in ChatGPT is inspectable in native Foldweave after pairing; a
compatible native job is inspectable through ChatGPT. Status polling remains
read-only.

### CASE-017 — Strict historical behavior

Finalized v1/v2 jobs remain historical evidence under their exact schemas.
Nonterminal legacy jobs fail with fresh-job guidance. No global rename,
in-place schema migration, or reinterpretation may change their provenance,
fingerprints, paths, receipts, or reconstruction meaning.

### AI-014 — Direct GPT-5.6 planning

Native direct mode remains exact `gpt-5.6` through the Responses API with strict
tools and schemas, `store=false`, no Chat Completions fallback, no model
substitution, no provider retry, bounded observable evidence, and no hidden-
reasoning claim. Strict schemas validate argument shape but never replace
deterministic source-stability, fingerprint, idempotency, authorization, or
mutation checks. Record actual returned model identity, usage, cost, and direct
transport provenance. `store=false` disables retained response retrieval but is
not zero-retention or zero-logging proof.

### AI-015 — Direct revisions and evidence limits

The direct provider can create a root proposal or complete derivative proposal
and can return only the strict initial or sparse-revision contracts. Preserve
the existing eight-turn maximum, 24 evidence calls, 16 KiB per result, 128 KiB
aggregate tool bytes, 512 KiB total outbound evidence, 32,768 output-token cap,
one clarification, initial submission plus at most two mechanical corrections,
and no hidden provider retry. User revisions are separately limited to two and
share rather than reset the job counters.

### AI-016 — ChatGPT-hosted planning

ChatGPT-hosted planning is real only when the model supplied by the user's
ChatGPT session calls Foldweave's bounded host-planning tools and submits a
complete proposal or sparse revision. Foldweave makes no hidden Responses API
call, reads no API key, and reserves or mutates no direct budget. The remote
widget uses the standard MCP Apps bridge as its portable baseline. Inside
ChatGPT, **Send changes** feature-detects and prefers the documented
`window.openai.sendFollowUpMessage` extension so the instruction re-enters the
host-model loop; when that extension is absent, it emits one standard
`ui/message` notification. It selects exactly one follow-up transport and never
retries through the other transport after dispatch or rejection. Deterministic
refresh, exact acceptance, verification, Change File retrieval, and
reconstruction remain standard-first `tools/call` operations, with
`window.openai.callTool` only as the compatibility fallback.

ChatGPT may inspect only bounded job-scoped inventory pages, eligible excerpts,
and supported-link facts. It cannot access the filesystem, paths, credentials,
compiler bypasses, proof overrides, or mutation authority. The direct evidence,
clarification, user-revision, and mechanical-correction ceilings apply.

### AI-017 — Host-planning tool authority

The shared host-planning layer exposes only:

- `create_or_resume_planning_job`;
- `list_inventory_page`;
- `read_text_excerpt`;
- `inspect_markdown_links`;
- `submit_plan`;
- `submit_plan_revision`;
- `request_clarification`;
- `get_plan_preview`; and
- `get_compiler_failures`.

Each call binds the job, device/channel capability, expected revision, bounded
evidence authority, and idempotency where mutating. The model never executes,
approves, writes, renames, deletes, shells, builds a receipt, or marks a result
verified.

### AI-018 — Orthogonal provenance

New strict provenance records these orthogonal dimensions:

- planning basis: `fresh`, `derivative`, `replay`, or `none`;
- model transport: `responses_api`, `chatgpt_hosted`, `codex_hosted`,
  `recorded_replay`, or `none`;
- execution origin: `gpt_planned`, `gpt_revised_from_change_file`, or
  `capsule_applied`.

`chatgpt_hosted` records only observable Foldweave tool traffic and
authoritative host metadata. It cannot fabricate a Responses API ID, direct
usage/cost, `store=false`, direct alias, provider attempt, budget reservation,
or hidden reasoning. Once a derivative invokes any model it can never claim
`capsule_applied`.

### AI-019 — Recorded replay and model-free application

Recorded replay is exact, sanitized, labelled, keyless, provider-free, and
fingerprint-bound. Unchanged Change File preparation, review, application,
verification, and reconstruction remain model-free. Historical planner records
prove only their original release and cannot be relabelled as proof of review or
derivative workflows.

The exact Foldweave user-facing replay label is **Recorded GPT planning run**.
It must never be labelled live. This narrowly supersedes the historical
**Recorded GPT-5.6 planning run** wording for active Foldweave surfaces; exact
provider alias and observed model identity remain available only in technical
provenance where supported by evidence.

### AI-020 — Sole USD 40 direct-API budget authority

After F+0, inspect the sole ledger and freeze the review, derivative, replay,
prompt, strict-tool, evidence-envelope, fixture, and exact F0b qualification
fingerprints. Only after those contracts have verified stable identities and
before any F0b reservation or provider call, atomically migrate
`.name-atlas/api_budget.json` in place. Preserve every historical request,
reservation, attempt, committed exposure, reported cost, timestamp, schema,
model record, and the existing cumulative call cap `13`; change only the
monetary ceiling from USD 10 to the hard cumulative USD 40. No second ledger or
reset is permitted. The monetary cap dominates the call cap.

F0b is prohibited until the contract-freeze evidence, atomic migration, and
post-migration byte/field verification have all passed. Set the final cumulative
call cap only in F4, after the complete qualification call graph stabilizes:

`historical provider attempts + required remaining calls and turns + two contingency attempts`

ChatGPT-hosted work never reads, reserves, or mutates the direct ledger. No new
direct call occurs before the required contract freeze and monetary migration.

### UX-017 — Packaged native shell and secure settings

Use pywebview stable 6.x as a narrow macOS shell over the one existing FastAPI
loopback control plane. The app starts Uvicorn on a safely selected ephemeral
loopback port, waits for health, starts Cocoa/WebKit on the main thread, and
shuts down without an orphan server. The narrow bridge exposes only fixed-role
open file/folder panels, Keychain-mediated secure settings, Finder reveal,
window lifecycle, and optional bounded notifications—never arbitrary
filesystem access or shell execution.

The secure settings surface shows only configured state, actual direct endpoint,
save/remove actions, and validation failures. Manual path entry remains for
automation and browser fallback. Durable jobs survive app restart. The app must
launch after being copied to an unrelated directory.

### UX-018 — Origin review

Journey A stops at `/review`. Show **Original structure** and **Proposed
structure**, one canonical trust strip, exact file/change/link/protected counts,
selected-member details, concise rationale, authority source, supported-link
effects, and prior/current delta after revision. Primary controls are **Accept
this structure and create copy**, a revision text area, and **Send changes**.
No output exists before exact acceptance.

### UX-019 — Receiver review and derivative choice

Journey B first renders **Your current folder** and **Shared proposal** from the
deterministic receiver preview. It must account for every local file, empty
directory, protected member, and supported link. Martin may accept the exact
shared proposal unchanged or request a new proposal through either live
transport. The unchanged route remains available on the immutable parent if a
child revision fails.

The receiver trust strip derives exclusively from deterministic job and matcher
state and displays: imported Change File verification status and fingerprint;
receiver source commitment; match-report commitment; complete-accounting state;
blocker, collision, and unresolved-ambiguity counts; source-unchanged state;
the explicit fact that no result exists while reviewing; and **0 GPT calls so
far** until a derivative child actually invokes a model. The release-facing
proposal label is exactly **Shared proposal**. Sofia and Martin are demo
personas, not authenticated identities; any sender or participant name carried
as metadata is visibly unverified and never treated as authorship.

### UX-020 — Review and revision states

Expose truthful `matching`, `planning`, clarification, `reviewing`, `revising`,
`revision_failed`, `executing`, verified, stale, and blocked states. A failed
revision states the exact issue and offers **Try another change** and **Keep
previous proposal**. Apply never shows a fake GPT stage. Done remains led by
**Your new folder is ready** and exposes Finder, Change File download, changes,
proof, verify again, and recreate-original actions.

### UX-021 — Purpose-built accessible visual tree

Do not use Mermaid, beautiful-mermaid, ASCII trees, or static images as the
operational renderer. Use one purpose-built React 18 + TypeScript + BlueprintJS
v6 folder-tree component, driven only by `folder-plan-preview.v1`, with a dark
navy/cyan/violet/amber/green/gray palette and no color-only meaning.

Required behavior: origin and receiver toggles; stable selection, expansion,
and scroll across toggles; changed branches initially expanded; changed-only
default for large trees; search; moved/renamed/link-updated/protected/
unchanged/empty-directory filters; explicit icons; details, rationale,
authority, link effects, revision delta, exact counts, and trust strip. Support
keyboard-only navigation, visible focus, meaningful screen-reader names,
correct toggle state, sufficient contrast, and no horizontal failure at
1280×720, approximately 1440×900, and 390×844. Rendering can never mutate or
override the candidate.

Acceptance includes one generated maximum-shape fixture with exactly 500 files
and 1,000 explicit directories. It must prove bounded initial render,
Original/Proposed and current/shared toggles, changed-only mode, search and every
filter, stable selection/expansion/scroll, keyboard operation, meaningful
screen-reader identity, and no horizontal overflow at all required viewports.
Use virtualization only if measured behavior on that fixture demonstrates it
is needed; its introduction cannot change deterministic order or accessibility.

### UX-022 — Shared ChatGPT widget and pairing UX

The native/browser review island and ChatGPT widget must compile from the same
purpose-built React review/tree component source and consume the same preview
DTO, deterministic ordering, state semantics, revision/acceptance bindings, and
MCP domain tools. No second renderer or independent tree interpretation is
permitted. Only the thin host adapter, Apps bridge, CSP/resource registration,
and pywebview-specific shell integration differ. The widget contains no
pywebview behavior or local path. Follow the interactive, decoupled Apps SDK
pattern: data/model tools return structured results; one render tool attaches
the widget; the standard MCP Apps bridge is primary. The widget handles missing
initial tool input while approval is pending, renders only structured content,
and never receives a secret through tool output, `structuredContent`, `_meta`,
widget state, or props.

Pairing surfaces show device name, ten-character Crockford Base32 one-time code,
expiry, local approval, failure/revocation state, and no local path. Native
Foldweave exposes paired-device status and revocation. Gateway loss is a
transport state, not proof that a durable local job failed.

### UX-023 — Native/browser routes and accessibility

Preserve existing routes and add `GET /review`,
`GET /api/jobs/{job_id}/preview`, `GET /api/jobs/{job_id}/status`,
`POST /api/jobs/{job_id}/revision`,
`POST /api/jobs/{job_id}/keep-proposal`, and
`POST /api/jobs/{job_id}/accept`. Every modifying request requires same-origin/
CSRF controls, expected revision, exact fingerprints, and idempotency key.
Native, browser, and widget review must pass the same semantics, viewport, and
accessibility acceptance.

### VER-019 — Preview and authorization proof

Tests and product-native evidence prove that the rendered preview DTO, compiled
candidate, job revision, source/Change File commitments, and acceptance record
agree. A stale browser tab/widget, changed destination, concurrent revision,
double click, duplicate retry, or restart ambiguity cannot execute a different
or unseen candidate. Artifact existence, screenshots, or unit tests alone do
not qualify this boundary.

### VER-020 — New schema and proof family

New work uses:

- `folder-plan-preview.v1`;
- `folder-refactor-job.v3`;
- `connected-change-core.v2`;
- `connected-change-file.v2`;
- `folder-evidence-ledger.v2`;
- `folder-execution-origin.v2`;
- `folder-change-receipt.v3`; and
- `folder-receipt-verification.v3`.

Preserve strict historical dispatch and fingerprint domains. The v3 verifier
recomputes preview authorization, execution origin, immediate-parent lineage,
complete member accounting, maps, supported-link rewrites, organized-tree
commitment, receipt/core/envelope DAG, BagIt, and report agreement without
trusting a job or UI.

### VER-021 — Serial collaboration convergence

The mandatory Sofia/Martin/Sofia proof establishes distinct source commitments,
strict supported equivalence, Martin's own current tree, model-free unchanged
CF1 acceptance, direct and ChatGPT-hosted derivative options, self-contained
CF2, application of CF2 without CF1, application of CF2 to Sofia's unchanged
source and to a verified T1 `data/` directory, identical T2 organized-tree
commitments, unchanged sources/artifacts, and participant-specific
reconstruction.

### VER-022 — Transport and ledger truth

Instrument and prove that ChatGPT-hosted root and derivative transactions do not
read `OPENAI_API_KEY`, initialize the direct provider, reserve budget, mutate
ledger bytes, or fabricate direct usage/model/store metadata. Direct mode proves
the opposite truthful provenance under the USD 40 ledger. Replay and unchanged
apply prove model-free operation. Gateway and widget output/log/state scans must
contain no credential or absolute path.

### VER-023 — Negative, race, and transport matrix

Require stale and duplicate acceptance; revise/accept races; failed revision
prior-preview preservation; restart in every nonterminal state; source and
Change File staleness; every existing matcher/receipt refusal; tampered lineage;
recursive-envelope rejection; wrong/expired/reused/revoked/cross-device/
cross-job OAuth or capabilities; pairing local-denial, expiry, attempt limit,
rate limit, and replay; companion disconnect/reconnect; duplicate gateway retry;
prompt-injection inability to expand tools; Keychain add/read/update/remove and
missing-key cases; safe endpoint/redirect behavior; picker cancellation and
invalid role; copied-app launch; shutdown/no-orphan; and strict legacy
verification/reconstruction.

Also require lineage generation `32` acceptance and `33` refusal; the defensive
lineage-size guard at 1,048,576 bytes acceptance and 1,048,577 refusal; one
canonical valid lineage containing the current-schema maximum of 500 member
bindings; valid v1 Change File unchanged application; immutable v1 parent to
self-contained v2 child revision; v2 child application without the v1 file;
incompatible legacy version refusal; and simultaneous parent/child same-output
acceptance proving one deterministic reservation winner or a fail-closed
no-winner result with no partial output. Native checks include port conflict and
second-launch behavior.

### VER-024 — Clean release and reconstruction matrix

Release proof combines focused and full Python tests, frontend component tests,
TypeScript typecheck, Vite build, lock/Ruff/diff checks, clean source install,
clean clone, copied `.app`, browser fallback, direct and hosted live
transactions, replay, unchanged apply, derivative collaboration, verifier,
reconstruction, gateway pairing/reconnect, installed-copy Codex invocation,
secret/response-ID/path/brand scans, wheel/app/gateway/widget asset inspection,
license/attribution, visual/accessibility review, and regenerated release
materials. Reconstruction always recreates the transaction's selected source.

### REL-016 — Foldweave CLI and compatibility

Required primary commands are:

- `uv run foldweave app [--browser]`;
- `uv run foldweave demo --mode replay`;
- `uv run foldweave run --mode live|replay --source SOURCE_ROOT [--output OUTPUT_PARENT] [--job JOB_FILE]`;
- `uv run foldweave apply-change CHANGE_FILE --source SOURCE_ROOT [--output OUTPUT_PARENT] [--job JOB_FILE]`;
- `uv run foldweave preview JOB_FILE [--json]`;
- `uv run foldweave revise JOB_FILE --instruction TEXT --idempotency-key KEY`;
- `uv run foldweave accept JOB_FILE --preview-fingerprint SHA256 --idempotency-key KEY`;
- `uv run foldweave verify-receipt RESULT_BAG [--source SOURCE_ROOT]`;
- `uv run foldweave restore-receipt RESULT_BAG RESTORE_DESTINATION`;
- `uv run foldweave mcp`;
- `uv run pytest`;
- `uv run ruff check .`; and
- `uv run ruff format --check .`.

`run` and `apply-change` only prepare review. Preserve `name-atlas` as a
documented legacy alias for this release; the internal `name_atlas` package may
remain. Do not rename immutable schemas, domains, paths, jobs, receipts, or Git
history.

### REL-017 — Focused frontend build

Use React 18, TypeScript, BlueprintJS v6 CSS-variable architecture, and Vite
only for the review island and shared widget components. Serve production
assets from the same loopback FastAPI origin. React performs no OpenAI or
gateway fetch and owns no durable product state. Node is a build-time
dependency only; packaged runtime has no Node requirement. Jinja/Blueprint
continues to own Home, forms, Working, Done, proof, verification, and
reconstruction outside the review island.

### REL-018 — Native packaging

Use Python 3.11, stable pywebview 6.x, and stable PyInstaller 6.x with a
checked-in macOS `onedir --windowed` spec and Apple Silicon target. Explicitly
collect/test the PyObjC Cocoa, Quartz, WebKit, and Security frameworks needed by
pywebview, secure input, and Keychain. After two serious PyInstaller
corrections, py2app is the preauthorized fallback. Do not add Electron, Tauri,
SwiftUI, a full React rewrite, or a second backend.

Test and claim only macOS Apple Silicon. With no Developer ID identity, require
a working ad-hoc/unsigned judge build and truthful launch instructions; do not
claim notarization, signed distribution, or frictionless public installation.

### REL-019 — Public gateway and paired companion

Use one checked-in TypeScript Cloudflare Workers Free gateway on its stable
`workers.dev` HTTPS hostname. Use `@cloudflare/workers-oauth-provider`, OAuth
2.1 authorization code with PKCE S256, CIMD enabled with DCR fallback, a
mandatory Workers KV binding named `OAUTH_KV`, SQLite-backed Durable Objects,
and Durable Object WebSocket Hibernation.

Configure `allowPlainPKCE: false`,
`clientIdMetadataDocumentEnabled: true`, and Cloudflare's
`global_fetch_strictly_public` compatibility flag for CIMD fetch protection.
OAuth token exchange is disabled in the selected profile.
Workers KV stores only OAuth clients, grants, and refresh/access-token records
or hashes required by the provider. One SQLite Durable Object per paired
device/session stores only public device identity, public key, scopes,
revocation/expiry, connection status, and bounded request correlation. The
local v3 job remains the sole product/idempotency authority. Apply the no-
payload, no-path, no-protected-content, no-planning-excerpt, no-credential, and
no-product-job-state boundary to both Cloudflare stores.

The gateway exposes `/mcp`, protected-resource and authorization-server
metadata, authorization/token/client-registration endpoints, widget resources,
pairing/revocation endpoints, companion WSS, and health/readiness. No custom
domain, paid plan, billing change, or alternate provider is required or
authorized.

### REL-020 — OAuth pairing, companion, and distribution states

The companion creates an Ed25519 device key pair, keeps the private key in
Keychain, registers only public key and opaque device ID, requests a ten-
character Crockford Base32 one-time code, and requires user confirmation plus
local approval. Code lifetime is ten minutes; maximum five failed attempts per
code; rate limit twenty attempts per source IP per fifteen minutes; successful
authorization binds the exact device key and atomically consumes the code.
Access tokens last one hour, rotating refresh grants thirty days, dynamic-client
metadata ninety days, and per-job capabilities thirty minutes. Revocation is
available in native Foldweave and the authorization surface.

The companion opens one outbound authenticated WSS connection and never a
public inbound listener. Require TLS, challenge-response device proof, request
ID, issue/expiry time, nonce/sequence, canonical body digest, Ed25519 signature,
replay rejection, bounded-jitter reconnect, and durable local recovery. The DO
accepts the companion socket through Hibernation; a DO-initiated outgoing
socket is prohibited. WebSocket attachment data stays within the platform's
16,384-byte limit; larger bounded correlation belongs in SQLite.

Track `DEVELOPER_MODE_VERIFIED`, `CONSUMER_PAIRING_VERIFIED`,
`PUBLICATION_READY`, `SUBMITTED_FOR_REVIEW`, `APPROVED`, and `PUBLISHED`
separately. Secure MCP Tunnel is required for early developer qualification but
requires separate Platform tunnel credentials/permissions and is not the
consumer topology. Developer mode may require workspace-admin approval.
Approval does not publish automatically; only observed `PUBLISHED` permits a
public-listing claim.

Secure MCP Tunnel is the mandatory F0c qualification transport. It may be
replaced only by a current user instruction or a documented official-rule
change that explicitly amends this frozen contract; implementation preference
alone cannot substitute another route.

If the complete gateway/companion transaction still fails after the initial
implementation and two material corrections, record `FOLDWEAVE_PROFILE_NO_GO`
and transition to `WAITING_FOR_GATEWAY_PROVISIONING_OR_USER_SCOPE_DECISION`.
Do not cut ChatGPT, hide a direct API call, relabel a tunnel as consumer access,
switch providers reactively, incur paid hosting, or relabel the predecessor as
completed Foldweave. Continue independent work until a genuine global impasse.

Every opening gate has an exact persistent-failure disposition after its
initial implementation and two material corrections:

| Gate | Recorded outcome and phase |
|---|---|
| F0a review authority | Record `FOLDWEAVE_PROFILE_NO_GO`; enter `WAITING_FOR_REVIEW_AUTHORITY_CORRECTION_OR_USER_SCOPE_DECISION`. |
| F0b native application | After the bounded PyInstaller/py2app policy is exhausted, record `FOLDWEAVE_PROFILE_NO_GO`; enter `WAITING_FOR_NATIVE_APPLICATION_CORRECTION_OR_USER_SCOPE_DECISION`. |
| F0c ChatGPT developer qualification | If the remaining cause is user-owned Platform/workspace access, enter `WAITING_FOR_CHATGPT_DEVELOPER_ACCESS`; otherwise record `FOLDWEAVE_PROFILE_NO_GO` and enter `WAITING_FOR_CHATGPT_DEVELOPER_INTEGRATION_CORRECTION_OR_USER_SCOPE_DECISION`. |
| F0d consumer gateway | Record `FOLDWEAVE_PROFILE_NO_GO`; enter `WAITING_FOR_GATEWAY_PROVISIONING_OR_USER_SCOPE_DECISION`. |

No later F milestone or release-readiness claim may pass while any mandatory
gate lacks verified positive evidence. Independent work with no dependency on
the failed premise may continue until the named user decision/access change is
the genuine global impasse; waiting is never relabelled as completion.

### REL-021 — Shared MCP and Codex

Use one domain implementation with local STDIO MCP for Codex and authenticated
Streamable HTTP MCP through the public gateway for ChatGPT. In addition to the
host-planning tools in `AI-017`, expose high-level workflow tools:

- `plan_change`;
- `prepare_change_application`;
- `job_status`;
- `answer_clarification`;
- `revise_plan`;
- `accept_plan_and_create_copy`;
- `get_change_file`;
- `verify_result`;
- `recreate_original`; and
- companion-only `choose_local_item`.

The two layers may use distinct server namespaces but dispatch to the same
engine/job. Every MCP tool has accurate required read/write/open-world/
destructive annotations, strict schemas, bounded output, and exact mutation
bindings. Never expose arbitrary file read/write/move/rename/delete, shell,
public raw paths, arbitrary companion RPC, receipt construction, compiler
bypass, verification override, or credentials.

Codex acceptance requires an updated Foldweave plugin with required
`.codex-plugin/plugin.json`, relative `.mcp.json`, clean-clone install,
cache/version proof, refresh/restart, fresh task, tool discovery, and real
installed-copy transactions covering origin planning, review, revision,
acceptance, polling, receiver preparation, derivative revision, keyless
unchanged apply, verification, reconstruction, and duplicate retry. A direct
Python call is not acceptance.

### REL-022 — Required live/replay qualification

After contracts stabilize, require one real direct root plan/review/revision/
accept transaction, one real direct imported-Change-File derivative, zero-
question and one-clarification coverage, one real ChatGPT-hosted root
review/revision/accept transaction, and one real ChatGPT-hosted receiver
derivative. Create exact sanitized replay records where required and one keyless
replay path. Commit no secret, response ID, absolute path, hidden reasoning, or
personal data. Labels must truthfully distinguish transport, returned model,
usage, cost, replay, and model-free execution.

### REL-023 — Branding, timing, and recording readiness

After F+0, active release-facing identity must be Foldweave across app bundle,
1024-pixel abstract folded-path/weave icon and iconset, title/menu/About/
settings/notifications, native/browser/review/widget UI, MCP and Codex plugin,
CLI, Change File, proof, reconstruction, README, limitations, provenance,
pre-existing-work disclosure, build log, installation guide, screenshots,
narration, submission package, Devpost, package metadata, GitHub description,
and release assets. Historical artifacts and compatibility labels keep their
names; the checkout directory may remain unchanged.

F+0 records activation but cannot reset the 44-hour envelope. The sole plan
scales relative F targets to actual time available and preserves the absolute
feature-freeze, release-candidate, recording-ready, and submission boundaries.
Recording readiness requires the completed mandatory profile, clean public
release/clone, stable `.app`, direct/ChatGPT/Codex/replay/unchanged/derivative
flows, final artifacts/proof/reconstruction, required gateway states, final
screenshots, under-three-minute rehearsed story, timed narration and shot list,
complete Devpost drafts/provenance, known `/feedback` path, no planned product
or design change, and active submission hold.

### CLAIM-008 — Permitted Foldweave claims

Only when demonstrated, Foldweave may say it shows current and proposed
structures before changing anything; allows bounded revision before exact
acceptance; represents each in-scope file once; keeps protected members fixed;
updates and verifies supported Markdown links; leaves sources unchanged;
creates separate results; transfers no project payload bytes in a Change File;
deterministically matches and reviews an equivalent copy; accepts unchanged
without GPT or derives a new proposal; converges accepted equivalent sources to
one organized tree; reconstructs the selected source per transaction; uses
exact `gpt-5.6` in native direct mode; uses ChatGPT-supplied inference without a
hidden Foldweave API call in hosted mode; and uses the same local engine from
the tested macOS, ChatGPT, and Codex surfaces.

### CLAIM-009 — Required qualifications

A Change File contains no payload bytes but discloses names, structure, sizes,
hashes, supported-link relationships, instructions, targets, lineage, and proof
identifiers. Live planning sends bounded selected evidence after disclosure.
`store=false` is not zero-retention proof. ChatGPT access and API billing are
separate. ChatGPT model identity is not claimed unless authoritative host
metadata supplies it. “Local-first” does not mean every mode is networkless:
browser uses loopback HTTP and ChatGPT uses gateway networking. Only supported
relative Markdown connections are preserved. Only macOS Apple Silicon is
tested natively. Public directory availability is claimed only when observed.

### CLAIM-010 — Prohibited claims and scope expansion

Prohibit universal safety or semantic correctness; universal format/code/
reference understanding; general graph isomorphism; independently edited-copy
or extra/missing-file reconciliation; sender authentication, authorship,
signatures, institutional authorization, historical authenticity,
tamper-proofing, compliance, production readiness, full privacy, zero
retention, no metadata disclosure, universal portability/reversibility,
Windows/Linux native support, mobile/remote-phone access, real-time
collaboration, public listing before publication, universal zero-question
behavior, unmeasured savings, adoption, uniqueness, or winning probability.

Do not add Electron, Tauri, SwiftUI, another backend, full React rewrite,
Windows/Linux packaging, accounts, permissions, cloud project sync, automatic
merge, semantic reconciliation, general graph isomorphism, sender
authentication, draft Change Files, another planner/engine/job/ledger/receipt/
verifier/reconstruction authority, market research, tournament, benchmark, or
custom validation bureaucracy.

Mandatory capabilities cannot be cut: Foldweave identity; packaged macOS app;
direct Responses API; ChatGPT-hosted mode; Codex/MCP; native selection; review
before execution; purpose-built visualization; origin and receiver revision;
exact acceptance; source immutability and file accounting; protected/link
behavior; separate results; persistent jobs; Change File v2; receipt/verifier
v3; immediate-parent lineage; Sofia/Martin/Sofia proof; reconstruction; replay;
legacy compatibility; truthful claims; and clean release. Optional cuts, in
order, are decorative animation, supplementary metrics, graph interactions
beyond the required tree/link inspector, extra themes, extra MCP-client
examples, nonessential notifications, expanded technical presentation, then
compatibility conveniences not needed for real historical artifacts.

## 16. Foldweave recording-readiness Definition of Done

Foldweave is recording-ready only when all four opening existential gates and
every non-cut requirement in Section 15 pass through complete integrated user
transactions; the serial derivative proof, native package, direct and
ChatGPT-hosted live modes, replay, unchanged apply, shared MCP/Codex, receipt,
verifier, reconstruction, negative/compatibility matrices, clean build/clone,
visual/accessibility checks, public gateway state, regenerated materials,
under-three-minute rehearsal, and truthful claims agree. External directory
approval is never inferred. Code volume, elapsed time, an agent message, a
static screenshot, artifact existence, or unit tests alone cannot satisfy this
definition. Final Devpost submission remains held for the user's voice,
`/feedback`, personal attestations, due diligence, and explicit hold release.
