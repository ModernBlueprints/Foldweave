# Reversible Name Atlas — Revised Frozen Build Specification

Status: **REVISED / FROZEN**

Amended production goal: **INACTIVE — AWAITING EXPLICIT USER ACTIVATION**

Historical first-cycle goal: **SUPERSEDED FOR REVISED FUTURE EXECUTION**

Revision R+0: **NOT STARTED**

Submission hold: **ACTIVE**

Track: **Work & Productivity**

Tagline: **Refactor the collection. Hand over the proof.**

This document is the sole authority for what the Build Week product is, what it
supports, what it must prove, and what "finished" means. The implementation plan
controls sequence; the production goal controls execution authority; `STATE.md`
reports current facts. Neither of those may silently redefine this specification.

## Source precedence and read certificate

Apply sources in this order:

1. The user's current instructions.
2. The revised product-direction attachment certified below.
3. The revised operating-model attachment certified below.
4. This revised frozen specification.
5. The amended production goal in `docs/build/GOAL.md`, but only after the user
   explicitly activates its complete text; it then controls execution rather
   than product truth.
6. The current official OpenAI Build Week rules and FAQ.
7. Verified repository state and fresh product evidence.
8. The implementation plan and material-decisions history.
9. Earlier research, tournament artifacts, and model opinions.

Revised product-direction record:

- Path: `/Users/nikolai/.codex/attachments/4d8a7392-b014-4a35-b68c-e74f0aaf1e22/pasted-text.txt`
- Logical lines: `849`; newline characters: `848`; bytes: `40,106`.
- SHA-256: `5515c49cbdd316b3e0f36b822272602de721141e636a052178bb306edb94de1f`
- Read-through-EOF certificate: complete and revalidated on 18 July 2026; the
  source has no final newline.
- Authority role: revised product direction and acceptance surface.

Revised operating-model record:

- Path: `/Users/nikolai/.codex/attachments/845959d4-c96b-47e8-b814-f4320f499599/pasted-text.txt`
- Logical lines: `599`; newline characters: `598`; bytes: `26,026`.
- SHA-256: `985cbeadb98a0ef7c6b45a1128b033819669abd9065cdf2d5a154789c8d9bd73`
- Read-through-EOF certificate: complete and revalidated on 18 July 2026; the
  source has no final newline.
- Authority role: revised operating model, timing, activation, and stop
  conditions.

Historical first-cycle conversation record:

- Path: `/Users/nikolai/.codex/attachments/77c587ad-c9d0-435e-a91c-be2f2115c38d/pasted-text.txt`
- Lines: `1,944`
- Bytes: `108,954`
- SHA-256: `1e0cc189e75a95d7f5e504799b4bbc14cc03696880ceb96db3201decc518f8b9`
- Read-through-EOF certificate: complete and validated on 17 July 2026.

Each certificate may substitute for rereading only while its hash matches.
Reread through EOF if a hash changes, the applicable certificate is absent, an
earlier read was incomplete, exact source language controls the immediate
decision, or current state conflicts with the source. Never qualify evidence
from a truncated read or use a summary where the underlying source is required.

Official sources rechecked on 18 July 2026:

- Rules: <https://openai.devpost.com/rules>
- FAQ: <https://openai.devpost.com/details/faqs>
- GPT-5.6 Sol: <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
- Archivematica 1.18 manual normalization:
  <https://www.archivematica.org/en/docs/archivematica-1.18/user-manual/ingest/manual-normalization/>
- BagIt RFC 8493: <https://www.rfc-editor.org/rfc/rfc8493>

The official submission deadline is Wednesday 22 July 2026 at 02:00 CEST.
The protected recording-ready boundary is Tuesday 21 July 2026 at 02:00 CEST.

## Product contract

### PRD-001 — Product

Reversible Name Atlas is a local migration workbench that turns a risky
structural change to a linked digital collection into a persistent,
human-reviewed Migration Case and then produces a Portable Change Receipt that
another person can independently verify.

The required transaction is:

`linked source package → persistent case → mechanical proposals → bounded GPT evidence where needed → human decisions → copy-only staged bag → portable receipt → independent verification → handoff`

The first-cycle preview, collision/reference detection, human judgment,
identity-level propagation, copy-only staging, forward/reverse maps, reverse dry
run, and BagIt proof remain required components of that transaction.

The dangerous operation is not merely changing a filename. It is migrating an
identity shared by files, metadata, derivatives, paths, and manifests.

### PRD-002 — Initial user and job

The initial user is a digital-preservation specialist or processing archivist
preparing a linked born-digital or digitized collection for preservation or
repository ingest.

Job to be done:

> When I must rename or reorganize a digital collection before it enters another
> system, show me the complete change, preserve every declared relationship,
> isolate the exceptions that need judgment, and verify the staged result before
> I commit it.

Workflow position:

`source export or characterization → Reversible Name Atlas → BagIt, Archivematica, or repository ingest`

Name Atlas complements characterization tools, bulk renamers, OpenRefine, BagIt,
and Archivematica. It does not replace or integrate with them in this MVP.

### PRD-003 — Product breadth

The primary transaction is verified migration of a linked collection:

- canonical identifier adoption;
- role-bearing filenames;
- structural moves into repository-ready directories;
- original/derivative synchronization;
- declared metadata-reference propagation;
- target collision prevention;
- original path preservation as provenance; and
- deterministic staging and proof.

Transliteration is one amber Meaning exception demonstrating why a mechanically
valid migration may still require human judgment. It is not the product category.

### PRD-004 — Interface

Build one standalone, loopback-only local browser application with a conventional
Python CLI. Do not build a Codex plugin, MCP server, hosted SaaS, Electron or
Tauri wrapper, accounts, collaboration, permissions, or cloud hosting.

Codex is the development environment and must remain the primary build record for
`/feedback`. Codex is not a runtime dependency.

### PRD-005 — Authority model

| Actor | Authority |
|---|---|
| Deterministic engine | Discovers declared structure, proposes paths, detects mechanical risk, propagates decisions, stages copies, and verifies invariants |
| GPT-5.6 | Converts bounded, mechanically flagged evidence into an evidence-linked human question with explicit uncertainty |
| Human archivist | Supplies semantic truth and the only approval or edited target decision |

GPT prose can never approve a proposal, make a package exportable, or turn an
item green.

### PRD-006 — Persistent case and portable handoff

The Migration Case is the sole mutable workflow authority. It is local and may
contain operational absolute paths. The Portable Change Receipt is an immutable,
path-neutral handoff artifact inside the completed bag. BagIt validates the
package's declared bytes; the independent Name Atlas verifier validates the
receipt-bound transaction. These are separate responsibilities and neither the
receipt nor BagIt replaces the local case while work is in progress.

The initial user remains a digital-preservation specialist or processing
archivist. This revision does not reposition the MVP as an AI-training-data,
generic data-cleaning, or repository-integration product.

## Supported input

The contract uses these terms consistently:

- **logical collection path**: a POSIX-style path relative to the selected source
  root, such as `objects/example.tif`; it never begins with `data/`;
- **content object**: a regular file referenced exactly once as an original,
  access derivative, or preservation derivative;
- **declared control file**: `metadata/metadata.csv` or the optional
  `normalization.csv`; and
- **source-package member**: either a content object or a declared control file.

Product proof files and BagIt tag files are generated output, not source-package
members.

### IO-001 — Package root

Support one selected local directory containing ordinary Unicode-visible regular
files. Apart from the two declared control files, every regular file below
`objects/`, `manualNormalization/access/`, or
`manualNormalization/preservation/` is a content object and must be accounted
for reciprocally by the declared CSV references. The supported structure is:

```text
<root>/
├── objects/
│   └── ... originals ...
├── manualNormalization/
│   ├── access/
│   │   └── ... optional access derivatives ...
│   └── preservation/
│       └── ... optional preservation derivatives ...
├── metadata/
│   └── metadata.csv
└── normalization.csv  # optional when no derivative mapping is required
```

The selected root may contain only the shown control files, content roots, and
ordinary directories needed to contain referenced content objects. Unexpected
regular files or directories block import; empty content directories are
permitted.

Every source-package member must be a regular file. Symbolic links, sockets,
devices, FIFOs, resource forks treated as separate special files, and source
paths outside the selected root are unsupported and block the transaction.

### IO-002 — `metadata/metadata.csv`

The metadata CSV must:

- be UTF-8;
- contain a header;
- have `filename` as the first column exactly once;
- contain `dc.identifier` exactly once;
- contain no duplicate or blank header;
- contain exactly one row for every regular file below `objects/`, with no row
  referring outside `objects/`;
- use relative `filename` values beginning with `objects/`;
- resolve each `filename` to exactly one in-scope original; and
- contain no duplicate original reference or unreferenced file below `objects/`.

`dc.identifier` must be:

- non-empty;
- Unicode NFC-normalized;
- unique across original object families; and
- matched by `[A-Za-z0-9][A-Za-z0-9._-]{0,63}`.

`dc.title`, `dc.description`, `dc.language`, and other uniquely named UTF-8
columns may be present. All extra columns and values are preserved exactly as
parsed and serialized. Only the declared `filename` field may be rewritten in
the staged CSV.

### IO-003 — `normalization.csv`

The optional root-level `normalization.csv` is case-sensitive, UTF-8, has no
header, and has exactly three fields per row:

1. original path;
2. access-derivative path, possibly blank; and
3. preservation-derivative path, possibly blank.

Rules:

- the original must resolve to exactly one metadata-declared original;
- each nonblank access derivative must resolve to exactly one regular file below
  `manualNormalization/access/`;
- each nonblank preservation derivative must resolve to exactly one regular file
  below `manualNormalization/preservation/`;
- each original may have at most one access and one preservation derivative;
- one derivative may belong to only one original family;
- every regular file below either derivative root must appear exactly once in
  the matching derivative field;
- duplicate rows, duplicate roles, many-to-many relationships, and orphaned
  references block the transaction; and
- every path is relative, normalized, inside the selected root, and free of `.`
  and `..` segments.

`normalization.csv` may be absent only when both derivative roots contain no
regular files. If it is present, every row must declare at least one derivative.

The hero package must contain this file and exercise both derivative roles or at
least one derivative role across multiple families.

### IO-004 — Explicit exclusions

The MVP does not support:

- `path_plan.csv`;
- arbitrary schema mapping;
- spreadsheet import other than the two declared CSV contracts;
- many-to-many derivative relationships;
- external catalogs or databases;
- ArchivesSpace, AtoM, or live Archivematica integration;
- embedded-link discovery in PDFs, office files, databases, or media;
- legacy raw filename-byte recovery;
- source mutation; or
- partial package export.

### IO-005 — Fail-closed input behavior

Block before copying when any required input is missing, empty, malformed,
non-UTF-8, ambiguous, duplicated, outside the root, unsupported, unresolved, or
not reciprocally accounted for by the CSV graph. Errors must identify the
offending path, row, column, relationship, or invariant. No source-package
member may be silently omitted.

## Deterministic transformation

### TX-001 — Source snapshot

At scan time, inventory every source-package member with:

- original POSIX-style relative path;
- role;
- byte size;
- streamed SHA-256 payload digest; and
- member kind (`content_object` or `declared_control_file`).

Re-scan immediately before staging. Any added, removed, renamed, resized, or
content-changed source member blocks staging. Never retain the API key or source
payload bytes in product artifacts.

### TX-002 — Stable object family

Create one `ObjectFamily` per metadata-declared original. The stable internal
family ID is the lowercase SHA-256 hex digest of canonical UTF-8 bytes:

`"family\0" + dc.identifier + "\0" + original_relative_path`

The ID is deterministic across repeated scans of the unchanged package and does
not change when a proposed or staged path changes. Identical payloads remain
distinct when their identifiers or original paths differ.

### TX-003 — Repository-ready profile

Use exactly one profile named **Repository-ready identity profile**.

For each family:

1. Take the final filename stem of the original path as the descriptor source.
2. Normalize it with Unicode NFKD.
3. Remove Unicode combining marks and record every removed mark as a Meaning
   risk signal.
4. Lowercase ASCII letters.
5. Preserve ASCII digits.
6. Map whitespace, ASCII `.`, `_`, `-`, and unsupported punctuation to `-`.
7. Remove remaining non-ASCII code points from the projected descriptor while
   recording each removal as a Meaning risk signal.
8. Collapse repeated `-` characters and trim leading/trailing `-`.
9. Reject an empty descriptor.
10. Lowercase each file's existing final extension and require it to match
    `\.[a-z0-9]{1,16}`.

This intentionally projects `campaña` to `campana` and records removal of the
combining tilde as a Meaning risk.

Target leaves are:

`{dc.identifier}__{descriptor}__{role}{lowercase_extension}`

Target directories are:

- original: `objects/`;
- access: `manualNormalization/access/`; and
- preservation: `manualNormalization/preservation/`.

All members of a family use the descriptor derived from the original. Each member
retains its own lowercased extension. The profile changes only staged paths and
declared staged references.

### TX-004 — `PathProposal`

Each serialized proposal is role-specific and contains:

- stable family ID;
- canonical identifier;
- role;
- original relative path;
- proposed relative path;
- proposal source (`repository_ready_profile` or `human_edit`);
- ordered transformation steps;
- affected declared references;
- Policy, Collision, Links, and Meaning risk signals;
- human-resolution state;
- verification state; and
- evidence addresses.

All proposals remain visible. Low-risk proposals may be grouped, but batch
approval is an explicit human action. Nothing passes silently.

### TX-005 — Collision and profile comparison

Before any copy, prove target uniqueness independently under:

- exact Unicode scalar comparison;
- NFC-normalized comparison; and
- NFC-normalized Unicode `casefold()` comparison.

Any duplicate under any comparison is a red blocker. Also block a target that is
absolute, escapes the package, contains empty/`.`/`..` segments, violates the
profile, or collides with a product-generated metadata or BagIt path.

### TX-006 — Human decisions

`HumanDecision` is a family-level record containing the stable family ID, action,
human input, and a complete `resolved_targets` map keyed by every role present in
that family. Decision states are:

- `pending`;
- `approved`;
- `edited`;
- `refused`; and
- `unresolved`.

`approved` atomically copies every role-specific proposed target for the family
into `resolved_targets`.

`edited` accepts one human-entered family descriptor matching
`[a-z0-9]+(?:-[a-z0-9]+)*`. The decision service derives a complete target for
every present role using the fixed identifier, directory, role, and extension
rules in `TX-003`, validates the complete family and global target set under
`TX-005`, and then stores that immutable role-to-target map in
`resolved_targets`. It never silently normalizes the human input.

`refused` records an explicit refusal and has no resolved targets.
`pending` and `unresolved` also have no resolved targets. All three block the
complete package. A decision cannot be partially resolved by role.

### TX-007 — Identity-level propagation

Apply an approved or edited family decision from its stored
`resolved_targets` map to:

- original staged path;
- access and preservation staged paths;
- the metadata row's `filename` field;
- all three fields of the applicable `normalization.csv` row;
- the decision ledger;
- the forward map; and
- the reverse map.

No downstream consumer independently recomputes a final target from strings
after the decision service stores the complete map.

### TX-008 — Copy-only staging

Staging is an all-or-nothing local transaction whose final directory is a BagIt
1.0 bag. Logical collection paths remain the product and reference namespace.
Physical BagIt payload paths are exactly `data/{logical_collection_path}`.
Metadata values and forward/reverse maps never include the physical `data/`
prefix.

The transaction:

1. Refuse a pre-existing destination unless the user explicitly selects a new
   empty destination.
2. Create a new pending directory.
3. Re-scan and compare the source snapshot.
4. Copy every content object to its resolved physical BagIt payload path without
   editing its bytes.
5. Write rewritten declared control files below `data/`, changing only their
   declared logical path-reference fields.
6. Generate product proof artifacts as BagIt tag files below
   `name-atlas/`, outside `data/`.
7. Write `bagit.txt`, `bag-info.txt`, SHA-256 payload manifests, and SHA-256 tag
   manifests.
8. Run all product checks and the package validator.
9. Promote the pending directory only after every invariant passes.
10. Preserve a failure report and do not expose a failed stage as exportable.

`TX-008` remains the first-cycle behavioral foundation. The revised transaction
must use the more specific acyclic finalization order in `VER-006`; where the
two sequences differ, `VER-006` controls.

## Persistent Migration Case

### CASE-001 — Storage, identity, and command binding

Use the strict schema identifier `migration-case.v1`. The default ignored local
case directory is `.name-atlas/cases/`. The default filename is the first 16
lowercase hexadecimal characters of SHA-256 over these canonical UTF-8 bytes:

`"case-root\0" + resolved_source_root_posix`

followed by `.json`. The exact CLI override is `--case CASE_FILE`. Starting a
fresh case for the same source requires an explicitly different absent case
path; there is no destructive reset command.

`case_id` is a lowercase UUID4 hexadecimal value created once and preserved.
The local case may contain absolute source, output, case, and stage paths. No
portable artifact may contain those absolute paths.

### CASE-002 — Complete case contract and lifecycle

Persist with strict Pydantic v2 contracts using `extra="forbid"`:

- schema version and monotonically increasing revision;
- case ID and user-visible case name;
- package-contract ID `name-atlas-linked-package.v1`;
- profile ID `repository-ready-identity.v1`;
- created and updated Europe/Oslo timestamps;
- absolute local source root;
- immutable portable source snapshot;
- object families, deterministic proposals, risk signals, and transformation
  traces;
- exact evidence packets and evidence fingerprints;
- exact validated decision cards, model/schema metadata, display origin, and
  card fingerprints;
- human decisions and complete resolved-target maps;
- decision-to-evidence/card bindings;
- local staging and handoff pointers;
- receipt fingerprint when finalized; and
- current lifecycle state.

The only lifecycle values are `review`, `ready_to_stage`, `handoff_ready`,
`stale`, and `blocked`. A `handoff_ready` case is read-only in this MVP. A
revised decision requires a new case and a new receipt; a receipt is never
edited in place. Pending, unresolved, or refused required decisions remain in
the local case and block staging and completed-receipt generation.

### CASE-003 — Atomicity and writer exclusion

Save the complete case to a sibling temporary file, flush and `fsync` that file,
atomically replace the canonical file, and `fsync` the parent directory where
supported. Persist only when the expected prior revision matches. Hold a
process-level case lock for mutation; a second writer fails closed.

Corrupt JSON, an unsupported schema, revision mismatch, lock contention, or
incomplete required fields blocks loading or mutation. Never silently rebuild
authority from an in-memory browser session. The existing `WorkflowSession` may
become a façade over a rehydrated case aggregate, but its dictionaries and stage
result may not remain an independent authority.

### CASE-004 — Rehydration and source staleness

On load and before every mutation:

1. parse the case strictly;
2. rescan the configured source;
3. rebuild deterministic families and proposals;
4. compare the portable snapshot and derived deterministic records;
5. revalidate evidence, card, candidate, and decision bindings; and
6. reuse only state whose bindings remain exact.

An added, removed, renamed, resized, or content-changed source member makes the
case `stale`, reports the exact differences, and blocks decision mutation,
staging, and receipt generation. Preserve the stale case. The supported
recovery is a fresh case at a different explicit case path. Do not implement
case rebasing, automatic reconciliation, or decision carry-forward.

### CASE-005 — Authority and spending separation

The Migration Case is the only mutable workflow authority, but it is not a
project-wide API spending ledger. The existing project budget ledger remains the
sole spending authority. Card-specific usage may be copied into the case for
provenance without creating a second budget or call counter.

## GPT-5.6 decision cards

### AI-001 — Model and provider boundary

Use the official OpenAI Responses API with model alias `gpt-5.6`. At scaffold
time the alias routes to GPT-5.6 Sol and supports structured outputs. Do not
silently substitute another model.

Define a structural `DecisionCardProvider` protocol equivalent in behavior to:

`generate(packet: EvidencePacket) -> DecisionCard`

Implementations:

- live GPT-5.6 provider;
- recorded GPT-5.6 replay provider; and
- deterministic test double.

Model transport and prompting must not be coupled to source scanning, decisions,
staging, or verification.

### AI-002 — Bounded evidence packet

The packet may contain only:

- stable family ID;
- original and proposed relative paths;
- exact transformation steps;
- mechanically supplied candidate paths;
- selected neighboring relative paths;
- linked metadata values with evidence IDs;
- derivative relationships with evidence IDs;
- deterministic risk signals; and
- profile description.

Do not upload payload bytes. Before a live call, display the complete outbound
text to the user and require an explicit Generate action.

### AI-003 — Structured output

`DecisionCard` contains only:

- possible interpretations;
- possible meaning loss;
- evidence IDs supporting each observation;
- explicit uncertainty;
- why the distinction matters;
- one discriminating human question; and
- explanations of supplied candidate paths.

The schema contains no field or executable authority for `safe`, `correct`,
`verified`, `approved`, `final_target`, `exportable`, or semantic truth.

### AI-004 — Validation and failure

Validate that:

- every evidence ID exists in the submitted packet;
- every referenced candidate path was mechanically supplied;
- required fields and cardinalities match the Pydantic contract; and
- the response is bound to the complete evidence fingerprint.

Unknown evidence, unknown candidates, malformed output, API failure, model
unavailability, or cap exhaustion leaves the item explicitly unresolved. Never
fabricate a card or approve a proposal after failure.

### AI-005 — Calls, cache, and cost

Call GPT only for mechanically flagged Meaning risk. Cache only by SHA-256 of the
complete canonical evidence packet plus model and schema version. Changed evidence
invalidates the cache. Expose:

- cards requested;
- live calls made;
- replay cards used;
- cache hits;
- calls avoided by deterministic triage;
- model;
- tokens when reported;
- latency;
- estimated cost; and
- configured call/cost cap.

The activated goal caps total project OpenAI API spend at USD 10. Reaching the cap
leaves manual-review states and never changes authority.

### AI-006 — Replay truthfulness

Replay data must originate from a real, validated `gpt-5.6` response generated
during this build. The UI and README display **Recorded GPT-5.6 response**. The
record includes model, evidence fingerprint, response schema version, generation
timestamp in Europe/Oslo, and a sanitized response. It contains no API key or
sensitive source data.

### AI-007 — Receipt-bound evidence and human action

For every Meaning-risk decision, persist in the case and export in
`decision-ledger.v2`:

- the exact canonical evidence packet and its fingerprint;
- the exact validated card presented and its fingerprint;
- model alias and card schema;
- whether the displayed card came from live generation or recorded replay;
- the explicit human action and complete resolved targets; and
- the Europe/Oslo decision timestamp.

Every binding must be revalidated before staging and by the receiver verifier.
GPT still cannot approve, verify, select a final path, resolve a collision, make
an item exportable, or produce green status. Low-risk batch approvals and
mechanical collision edits contain no fabricated GPT provenance.

The inherited real GPT-5.6 record remains valid while its evidence packet,
model, card schema, and hero Meaning case remain exact. The revised walking
transaction must reuse that validated replay and must not make a second provider
call merely to add persistence or receipt binding. A new call is justified only
if the evidence/card contract changes materially or the inherited record becomes
invalid.

## User experience

### UX-001 — Atlas

Show collection and family counts, source structure, canonical identifiers,
original/access/preservation relationships, metadata links, profile, proposal
counts, structural moves, and risk counts across Policy, Collision, Links, and
Meaning.

### UX-002 — Decisions

Show before/after paths, exact transformation steps, affected links, evidence,
outbound GPT packet preview, neutral decision card, human approve/edit/refuse
controls, explicit unresolved state, low-risk batch approval, and export-readiness
progress.

### UX-003 — Proof

Show source snapshot status, staged location, content-object byte equality,
declared-reference resolution, target uniqueness, profile validity,
forward/reverse-map status,
reverse dry run, BagIt validation, unresolved/failed items, and open/download
controls for proof artifacts.

### UX-004 — Visual authority

- Green: deterministic fact verified after required human resolution.
- Amber: human judgment is still required.
- Red: mechanical blocker or failed invariant.
- Neutral: GPT explanation and uncertainty.

GPT prose alone never changes status color.

### UX-005 — Hero and negative fixtures

Create one redistributable synthetic hero package with approximately 12 object
families and 25–35 regular files. It must demonstrate canonical renaming,
directory moves, metadata rewrites, original/derivative propagation, one collision
that is resolved, `campaña → campana` resolved by the human after a live GPT card,
and a successful staged package.

Create one tiny negative fixture proving that an unresolved semantic decision,
collision, malformed input, or orphaned reference blocks export. Do not create
multiple polished collections. Record sample provenance.

`UX-001` through `UX-005` preserve the required information and fixture story.
The revised navigation and presentation contract is more specifically fixed by
`UX-006` through `UX-008`.

### UX-006 — Five-state server-rendered workbench

Expose these GET routes:

- `/atlas`;
- `/decide`;
- `/stage`;
- `/verify`; and
- `/handoff`.

`GET /` redirects to the server-computed next state: a stale or import-blocked
case goes to `/atlas`; an unresolved or refused required decision goes to
`/decide`; complete decisions without a verified handoff go to `/stage`; and a
verified handoff goes to `/handoff`.

`POST /stage` creates the complete bag, receipt, and receiver-verified handoff
atomically, then redirects to `/verify`. Verify explains the proof; Handoff is
the receiver-oriented surface. Every route remains directly inspectable and
shows `INCOMPLETE` or `BLOCKED` when prerequisites are absent.

The persistent shell shows the Name Atlas mark, case name and abbreviated case
ID, source commitment, live/replay mode, five-step navigation with
`aria-current`, resolved/unresolved count, and deterministic status.

### UX-007 — Page contracts and server authority

- **Atlas:** exception-first list and inspector, object-family relationships,
  before/after paths, risks, and affected references.
- **Decide:** one unresolved exception by default; collision controls without
  GPT; Meaning evidence, a neutral GPT card, and visually authoritative human
  action.
- **Stage:** readiness, blockers, source/destination, source-untouched statement,
  and one stage action.
- **Verify:** one `VERIFIED`, `BLOCKED`, or `INCOMPLETE` verdict with Source,
  Payloads, References, Paths, Decisions, Package, and Receipt groups.
- **Handoff:** receipt summary and fingerprint, local handoff path, offline
  receipt action, copyable verifier command, rerun-verifier action, and a restore
  action only if restore passes its gate.

Use semantic forms, tables, headings, links, and `<details>`. Collapse technical
evidence by default. JavaScript is limited to local filtering, clipboard, and
disclosure behavior. All state and transition authority remains server-side.

### UX-008 — Blueprint visual layer

Use `@blueprintjs/core` version `6.17.2` and `@blueprintjs/icons` version
`6.13.0` as locally vendored visual assets. Include Apache-2.0 attribution and a
third-party notice. Package compiled CSS and only the selected local icon assets
in the Python wheel; load `bp6-dark` on the application shell and Name Atlas
layout CSS after Blueprint. Use no CDN, React, Vite, client router, state store,
or Node runtime/build step in the judge path.

The icon vocabulary is: Atlas `diagram-tree`, Decide `help`, Stage `database`,
Verify `tick-circle`, Handoff `export`, plus `warning-sign`, `clipboard`,
`history`, and `chevron-right`. Icons accompany visible text, use
`aria-hidden`, and never carry status alone.

The product may say it uses Blueprint's dark visual system and locally packaged
visual assets. It may not claim to be a Blueprint React application.

## Verification and product artifacts

### VER-001 — Generated artifacts

Generate at least:

- `name-atlas/source_snapshot.json`;
- `name-atlas/decision_ledger.json`;
- `name-atlas/forward_path_map.csv`;
- `name-atlas/reverse_path_map.csv`;
- `name-atlas/verification_report.json`;
- a human-readable summary below `name-atlas/`; and
- `bagit.txt`, `bag-info.txt`, `manifest-sha256.txt`, and
  `tagmanifest-sha256.txt`.

The complete transformed logical collection, including content objects and
rewritten declared control files, is below `data/`. Forward and reverse maps have
one inverse row per content object and use logical collection paths. The fixed
control-file paths are not map rows; their source and staged hashes plus
field-level changes are recorded in `verification_report.json`.

### VER-002 — Integrity claim

The product may display **Verified round-trip integrity within the supported
package contract** only when all are true:

- the fresh pre-staging snapshot equals the initial snapshot;
- the application did not mutate any source-package member;
- every staged content object's SHA-256 equals its corresponding source content
  object's SHA-256;
- declared control files retain all rows, columns, non-path values, and ordering,
  and only declared path-reference fields change;
- every declared staged metadata and derivative reference resolves;
- every target satisfies the profile;
- every target is unique under all declared comparisons;
- forward and reverse maps are complete and exact inverses over the complete
  content-object logical path set;
- a reverse dry run reconstructs the original content-object logical paths and
  declared reference values;
- no required decision, unsupported input, or failed invariant remains;
- the Library of Congress `bagit` validator passes; and
- the Proof UI and serialized verification report agree.

### VER-003 — Required automated scenarios

Automate these scenarios, with UI-level verification where appropriate:

1. Valid hero-package import creates stable object families and declared edges.
2. A non-lossy proposal stays visible, supports explicit batch approval, and
   makes no GPT call.
3. `campaña → campana` creates a Meaning-risk evidence packet.
4. GPT can explain interpretations and ask a question but cannot approve or set a
   final target.
5. Unknown GPT evidence IDs and candidate paths are rejected.
6. Malformed output, API absence, model failure, or cap exhaustion remains
   unresolved.
7. Identical complete evidence reuses a cached card; changed evidence does not.
8. An unresolved, pending, or refused required decision blocks the whole export.
9. Exact, NFC, or casefold target collision blocks before copying.
10. Invalid/duplicate/missing `dc.identifier` blocks import.
11. Malformed/non-UTF-8 CSV, path traversal, symlink, or special file fails closed.
12. Orphaned, duplicated, or many-to-many derivative/reference data fails closed.
13. One family decision rewrites original, derivatives, metadata, and normalization
    data from the same stable identity.
14. A changed source tree blocks at the pre-staging re-scan.
15. Copy failure never promotes an exportable stage.
16. All source-package members and logical paths remain unchanged.
17. Staged content-object hashes equal source content-object hashes, while
    control-file changes are limited to declared path-reference fields.
18. Forward/reverse maps round-trip the complete content-object logical path set
    and reconstruct the declared reference values without a `data/` prefix.
19. BagIt validation succeeds for the resolved hero package.
20. The Proof UI equals `verification_report.json`.
21. Replay mode launches without an API key and is visibly labeled.
22. Live mode generates and displays a real validated `gpt-5.6` card.
23. A clean clone can run the documented replay judge path.

### VER-004 — Unsupported proof claims

Do not claim preservation of filesystem ACLs, extended attributes, creation or
modification timestamps, resource forks, undeclared external references,
arbitrary embedded links, every filesystem's byte-level filename representation,
live Archivematica acceptance, universal reversibility, or semantic correctness.

### VER-005 — Portable artifacts and original controls

The completed bag uses these versioned artifacts and paths:

| Artifact | Schema and path |
|---|---|
| Path-neutral source snapshot | `portable-source-snapshot.v1` at `name-atlas/source_snapshot.json` |
| Complete decision provenance | `decision-ledger.v2` at `name-atlas/decision_ledger.json` |
| Forward map | `name-atlas/forward_path_map.csv` |
| Reverse map | `name-atlas/reverse_path_map.csv` |
| Producer report | `verification-report.v2` at `name-atlas/verification_report.json` |
| Human summary | `name-atlas/verification_summary.md` |
| Machine receipt | `portable-change-receipt.v1` at `name-atlas/change_receipt.json` |
| Offline receipt | `name-atlas/change_receipt.html` |
| Original metadata control | `name-atlas/original-control/metadata/metadata.csv` |
| Original normalization control | `name-atlas/original-control/normalization.csv`, when present |
| Receiver result | `receipt-verification.v1`, returned but not written into the finalized bag |
| Restore result | `restore-report.v1`, only if restore is admitted |

The portable source snapshot contains only contract version, sorted relative
POSIX member path, role, member kind, size, SHA-256, and the existing
path-neutral aggregate commitment. It contains no `source_root`.

`decision-ledger.v2` is the complete decision authority: every initial proposal,
transformation/risk trace, human action, resolved-target map, decision method,
and exact Meaning-review record where applicable. The receipt commits the raw
ledger digest and summarizes counts; it does not duplicate the ledger.

`verification-report.v2` contains no absolute `staged_location`. Local stage
location remains only in the case and browser view model. All portable artifacts
use relative POSIX paths and contain no source, case, checkout, home, temporary,
or verifier-input absolute path and no `file://` URI.

Authority is domain-specific: `decision-ledger.v2` controls decision provenance,
`verification-report.v2` controls the producer's deterministic findings, and the
machine receipt controls its envelope, commitments, counts, and claim boundaries.
The Markdown summary and offline HTML are byte-bound, non-authoritative derived
views that must agree with those machine records.

Byte-exact original declared control files are always copied to the listed tag
paths and bound by the receipt and BagIt tag manifest. They are not payload
members under `data/`. They support independent original-versus-staged reference
comparison and any conditionally admitted logical restore.

### VER-006 — Non-circular receipt and immutable finalization

The machine receipt is an envelope with exactly:

- `receipt`: one complete immutable `ReceiptCore`; and
- `receipt_fingerprint`: lowercase SHA-256 of the canonical `ReceiptCore`
  bytes.

The fingerprint field is outside its own hash domain. Canonical `ReceiptCore`
bytes use Pydantic JSON-mode values, every declared field including explicit
`null`, UTF-8, `ensure_ascii=False`, sorted keys, separators `(",", ":")`,
`allow_nan=False`, and no trailing newline. Raw artifact digests are SHA-256 over
exact on-disk bytes, including a final newline when present.

`staged_data_commitment` is SHA-256 over the canonical sorted list of every
regular member below `data/`, each represented by its path relative to `data/`,
byte size, and SHA-256.

The receipt core commits raw digests for the portable source snapshot, each
original control copy, decision ledger, forward map, reverse map, final
verification report, retained human-readable summary, `bagit.txt`,
`bag-info.txt`, and `manifest-sha256.txt`. It explicitly excludes `change_receipt.json`,
`change_receipt.html`, `tagmanifest-sha256.txt`, and any later receiver result.
The final tag manifest protects the receipt JSON and HTML as ordinary tag files.

The receipt core records schema, package-contract and profile versions; case ID
but no case path; source and staged-data commitments and counts; authoritative
artifact commitments; map, decision, GPT-assisted, and human-decision counts;
producer BagIt-validator identity and result; claim boundaries; and paths to the
non-authoritative HTML and summary views.

Use this acyclic generation order:

1. rescan and prove the source equals the case snapshot;
2. copy content and write rewritten staged controls;
3. write portable source snapshot, byte-exact original controls, decision
   ledger, maps, summary, and provisional report;
4. run the existing source-aware deterministic proof;
5. write initial BagIt metadata and manifests;
6. run initial BagIt validation;
7. write the final path-neutral verification report;
8. calculate authoritative artifact hashes and staged-data commitment;
9. write the immutable receipt envelope;
10. render offline HTML from the finalized receipt and committed ledger/report
    information;
11. rebuild the complete tag manifest over the final tag-file set;
12. run final BagIt validation;
13. run the receiver verifier against the pending bag;
14. rescan the source again; and
15. promote no-replace only if source-aware proof, final BagIt validation,
    receiver verification, and final source equality all pass.

After receipt finalization no receipt-bound artifact may change. Preserve a
later failure as a sibling failure record outside the pending bag; never rewrite
the receipt or final report and create an undisclosed digest mismatch.

### VER-007 — Independent receiver verifier

The required command is:

`uv run name-atlas verify-receipt RECEIVED_BAG [--source SOURCE_ROOT]`

- Exit `0`: print `VERIFIED` and the receipt fingerprint.
- Exit `1`: print `BLOCKED` and stable failed check IDs.
- Exit `2`: usage error or the input cannot be opened as a candidate handoff.

The verifier performs no writes and requires no API key, GPT call, network,
browser, local Migration Case, `WorkflowSession`, or original source. It works
after the bag is copied to an unrelated absolute path. It reruns BagIt
validation; strictly parses every versioned artifact; validates the receipt-core
fingerprint and raw commitments; recomputes staged data; compares the portable
snapshot, original controls, ledger, proposals, decisions, maps, staged controls,
and payloads; recomputes profile, uniqueness, reference, inverse-map,
reverse-dry-run, evidence/card/decision, and unresolved-decision checks; compares
actual findings with `verification-report.v2`; and returns exact blockers.

With `--source`, additionally compare the supplied original source to the
portable snapshot. Without `--source`, prove only internal transaction
consistency against the committed source description; do not claim historical
source authenticity. The browser may call the same pure receiver service, but
acceptance requires a separate keyless subprocess. Shared strict parsers and
pure deterministic helpers are allowed; the verifier may not call the live
workflow/session proof path. No additional public verifier output format is
supported in this release: specifically, there is no `--json` or other
output-format option.

### VER-008 — Controlled BagIt-valid counterfactual

Create one disposable copy of the successful hero handoff. Change one resolved
target in `name-atlas/decision_ledger.json` to another syntactically valid path,
regenerate the ordinary BagIt tag manifest so BagIt validation passes, do not
alter the receipt, and run `verify-receipt`.

The required result is ordinary BagIt validation passing while Name Atlas exits
`1`, prints `BLOCKED`, and names the decision-ledger raw-digest mismatch against
the receipt commitment. Never alter the canonical successful handoff or source.
This proves receipt-bound transaction consistency, not cryptographic sender
authentication or resistance to a party that rewrites all artifacts and issues
a new internally consistent receipt.

### VER-009 — Revised acceptance matrix

In addition to `VER-003`, automate and inspect:

1. a case, card, human action, and targets survive process restart;
2. reopening unchanged evidence makes no provider call;
3. corrupt JSON, unknown schema, revision mismatch, and lock contention block;
4. added, removed, renamed, resized, and content-changed source members each make
   a case stale and preserve its file;
5. mismatched evidence, card, candidate, or decision binding blocks;
6. low-risk and collision decisions contain no fabricated GPT provenance;
7. receipt fingerprint and every committed raw digest recompute exactly;
8. copying a bag to a different absolute path preserves verification;
9. a portable-artifact scan finds no sender-local absolute path;
10. offline HTML agrees with parsed machine receipt and remains non-authoritative;
11. source snapshot, original controls, ledger, maps, staged controls, payloads,
    report, and receipt agree;
12. a separate keyless source-free verifier returns `0` and changes no bag byte;
13. optional `--source` passes for the exact source and blocks for a different
    source;
14. malformed/unknown receipts and each material commitment or invariant failure
    return stable blockers;
15. the exact `VER-008` counterfactual passes BagIt and is blocked by Name Atlas;
16. all five routes, root redirects, prerequisite guards, and post-stage redirect
    work without JavaScript authority; and
17. Blueprint assets, icons, license notice, and wheel contents work in a clean
    uv-only installation with no CDN or Node runtime.

## Architecture and judge contract

### REL-001 — Technology

Use:

- Python 3.11;
- `uv` and a committed lockfile;
- FastAPI;
- Jinja2;
- small, dependency-light vanilla JavaScript and CSS;
- Pydantic v2 at serialized/external boundaries;
- official OpenAI Python SDK;
- pytest;
- Ruff;
- Library of Congress `bagit`; and
- standard-library hashing and filesystem primitives where sufficient.

Support and test the judge path on macOS with Python 3.11. Keep POSIX/Linux
compatibility where ordinary `pathlib` behavior permits it. Windows support is
not an MVP claim.

### REL-002 — Modules

Keep bounded modules for:

- source snapshot and identity;
- strict package import;
- object-family graph;
- path proposals and risk detection;
- GPT decision cards;
- human decisions;
- staging transaction;
- verification and BagIt validation;
- product artifacts; and
- web presentation.

Use `Protocol` at the GPT provider and package-validator boundaries. Avoid a God
transaction module, circular dependencies, ceremonial abstractions, and a new
framework.

### REL-003 — Judge commands

The final repository must support:

```text
uv sync --frozen
uv run name-atlas demo --mode replay
uv run name-atlas demo --mode live
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Replay must require no API key. Live mode must fail clearly when the key is
absent and must never substitute another model.

The listed first-cycle commands remain supported. `REL-005` adds the revised
case, receiver-verifier, and conditional restore contracts.

### REL-004 — Recording-ready definition

By Tuesday 21 July 2026 at 02:00 CEST:

- every required product behavior works end to end;
- a real GPT-5.6 card has been generated, validated, displayed, and recorded;
- GPT has no approval or verification authority;
- the source remains unmodified;
- hero staging and all proof invariants pass;
- live and visibly labeled replay modes work;
- the full required automated suite, lint, and formatting pass;
- the UI has been visually verified at recording resolution;
- the hero and negative fixtures and provenance are final;
- the repository is public, MIT-licensed, clean, and points to the final commit;
- a clean clone runs from the README;
- README, limitations, pre-existing-work disclosure, Codex build log, screenshots,
  setup, judge commands, and troubleshooting are complete;
- the exact demonstration has been rehearsed;
- a 2:35–2:45 English narration draft and shot list are timed;
- Devpost title, track, description, technologies, repository URL, screenshots,
  Codex/GPT explanation, and claim language are drafted;
- the `/feedback` path is known;
- current submission requirements have been checked; and
- no code, design, or feature work remains planned.

The following 24 hours are reserved for the user's voice-over, final capture and
editing, upload/playback verification, `/feedback`, due diligence, final clean
run, Devpost submission, and receipt confirmation.

This first-cycle definition remains historical evidence. The revised release is
recording-ready only when `REL-007` also passes.

### REL-005 — Revised CLI and dispatch

The release must support:

```text
uv sync --frozen
uv run name-atlas demo --mode replay [--source SOURCE] [--output STAGING_PARENT] [--case CASE_FILE] [--port PORT]
uv run name-atlas demo --mode live [--source SOURCE] [--output STAGING_PARENT] [--case CASE_FILE] [--port PORT]
uv run name-atlas verify-receipt RECEIVED_BAG [--source SOURCE_ROOT]
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

`demo` creates an absent case and resumes an existing case, reports the exact
local case path, and blocks a stale case. Verifier and conditional restore
dispatch before provider, budget, demo-source, or web initialization. Replay is
keyless and visibly recorded; live uses exact `gpt-5.6` with no silent fallback.

The following command exists only if `REL-006` admits restore:

`uv run name-atlas restore-receipt RECEIVED_BAG RESTORE_DESTINATION`

### REL-006 — Conditional logical restore

Adjudicate restore exactly once at the R4/R+52 gate. Admit it only when case
persistence and restart, receipt JSON and offline HTML, positive and controlled
negative receiver verification, all five routes, inherited and new core tests,
and absence of material cross-artifact defects all pass, and at least 18 actual
hours remain before Tuesday 21 July 2026 at 02:00 CEST.

If any condition fails, record `CUT_BY_PREAUTHORIZED_GATE` and omit the command,
UI action, README instruction, and restore claim. A correctly gate-cut restore
is not a missing required feature and does not block the release.

The gate decision is monotonic. Before the verdict, the plan may pre-authorize
cutting restore, which yields `CUT_BY_PREAUTHORIZED_GATE`. Once the gate records
`GO`, the restore command is required and may not later be relabeled as a gate
cut; failure to complete it is a blocking R5 implementation defect. The restore
UI remains independently cuttable without changing the admitted command's
status.

If admitted, the command must verify the handoff first, refuse an existing
destination, create a sibling pending directory, copy content through the
reverse map to original logical paths, restore byte-exact declared controls from
`name-atlas/original-control/`, leave the handoff and source untouched, validate
the reconstructed directory through the strict importer, prove every in-scope
path, size, and SHA-256 equals the portable snapshot, and promote no-replace only
after proof passes. Its `restore-report.v1` result is external to the immutable
received bag.

The only permitted restore claim is:

> Reconstructs every in-scope source-package member byte-for-byte within the
> supported Name Atlas package contract.

Do not claim restoration of ACLs, ownership, timestamps, extended attributes,
resource forks, undeclared references, embedded links, or arbitrary filesystem
state.

### REL-007 — Revised recording-ready definition

By Tuesday 21 July 2026 at 02:00 CEST, all inherited requirements still apply
and the revised release must additionally have:

- persistent restart-safe Migration Cases with fail-closed staleness;
- exact evidence/card/human-decision provenance bindings;
- path-neutral `v2` proof artifacts, byte-exact original controls, an immutable
  machine receipt, and offline HTML;
- one independently verified copied handoff and the exact BagIt-valid but
  receipt-inconsistent controlled failure;
- connected, visually inspected Atlas, Decide, Stage, Verify, and Handoff routes
  in the locally packaged dark Blueprint visual system;
- a clean keyless subprocess verifier and truthfully labeled replay/live paths;
- the restore gate objectively recorded as shipped or
  `CUT_BY_PREAUTHORIZED_GATE`;
- passing inherited and revised tests, lint, format, portability/path scans,
  builds, clean-clone installation, and wheel-asset checks;
- refreshed README, limitations where necessary, provenance/notices, screenshots,
  narration, shot list, Devpost draft, and claim audit for the revised product;
- a selected release commit and rehearsed three-minute transaction; and
- no planned code, design, or optional feature work.

The first-cycle README, screenshots, narration, thumbnail, and Devpost copy are
preserved but stale until regenerated after revised feature freeze. The final 24
hours remain protected for user voice-over, capture/edit/upload, `/feedback`,
due diligence, explicit submission-hold release, submission, and confirmation.

## Claims

### CLAIM-001 — Permitted only after implementation and verification

- Makes mechanically risky collection-path transformations visible and reviewable.
- One human decision propagates through supported declared links.
- Creates a copy-only staged package.
- Verifies content-object hashes, declared references, collisions, profile
  compliance, and in-scope logical-path round trips.
- GPT-5.6 synthesizes bounded linked context into an evidence-linked human
  decision card.
- Supports one documented package shape and one repository-ready profile.
- Keeps the source untouched by the staging transaction.
- In the tools reviewed, this exact bounded transaction was not found.

### CLAIM-002 — Forbidden

Do not claim:

- a critical or universal crisis;
- that archivists constantly experience the problem;
- 50% or any other unmeasured time saving;
- faster recurring work;
- GPT-5.6 determines the correct name;
- AI verifies semantic correctness or safety;
- no wrong transformations;
- mathematical or universal reversibility;
- sender identity, human authorship, institutional authorization, signatures,
  or cryptographic authentication;
- full filesystem preservation;
- compliance certification or legal-record assurance;
- Archivematica certification, compatibility, or live integration;
- that Archivematica expects clean input or lacks filename handling;
- all bulk renamers break metadata;
- arbitrary schemas or every archival workflow are supported;
- million-file scalability;
- production readiness;
- institutional acceptance;
- OpenAI or another AI lab uses or needs the workflow;
- AI-training-data or model-curation readiness;
- proven superiority over ordinary Codex;
- a high probability of winning; or
- nothing else exists.

Record actual demonstration facts instead: objects, families, references,
proposals, moves, risk triggers, calls avoided/made, cache hits, collisions,
rewrites, unresolved decisions, validation outcomes, latency, and measured API
cost.

### CLAIM-003 — Revised permitted claims after proof

Only after the corresponding acceptance evidence passes, the revised release
may say that it:

- persists a human-reviewed Migration Case across restart;
- binds GPT evidence, the exact card presented, and the human's explicit action
  in a complete decision ledger;
- creates a portable, path-neutral Change Receipt for the supported transaction;
- permits independent, keyless receiver verification without the original case,
  source, browser, network, or GPT;
- detects the specified BagIt-valid but receipt-inconsistent altered handoff; and
- performs the bounded logical restore in `REL-006` only if that feature ships.

These are integrity and consistency claims within the supported contract, not
semantic correctness, historical-source authenticity, signer authentication,
compliance, production readiness, universal safety, or universal reversibility.

## Explicit product exclusions

Do not build during Build Week:

- another project-discovery process, tournament, benchmark, or validation harness;
- a general archive-management, DAM, ETL, data-catalog, or enterprise file tool;
- a naming-policy language or drag-and-drop schema builder;
- arbitrary input adapters or `path_plan.csv`;
- executable `apply-case` or cross-machine case application;
- source reconciliation, rebasing, or decision carry-forward;
- a repository connector platform;
- direct repository or Archivematica integration;
- cloud synchronization, hosting, accounts, collaboration, or permissions;
- signing, sender authentication, or institutional authorization;
- automatic source renaming;
- automatic semantic approval or AI-generated canonical identifiers;
- general deduplication or entity resolution;
- NER, ReFinED, or another entity-linking subsystem;
- Hugging Face, JSONL, Parquet, AI-training-data, generic adapter, or generic
  policy-builder work;
- live Archivematica integration;
- RO-Crate or another metadata platform;
- React, Vite, a client-side application state framework, or a Node judge path;
- multiple polished collections;
- AI-lab-specific workflow; or
- functionality unrelated to the complete three-minute submission story.

## Final completion surfaces

After explicit activation, the amended production goal may be marked complete
only when every required surface is complete, the user has explicitly released
the submission hold, and the Devpost submission is confirmed:

- Product implementation: `COMPLETE` or `PARTIAL`.
- Deterministic integrity proof: `COMPLETE` or `PARTIAL`.
- GPT-5.6 integration: `COMPLETE` or `PARTIAL`.
- Persistent Migration Case: `COMPLETE` or `PARTIAL`.
- Portable Change Receipt: `COMPLETE` or `PARTIAL`.
- Independent receiver verification: `COMPLETE` or `PARTIAL`.
- Five-state workbench: `COMPLETE` or `PARTIAL`.
- Conditional restore applicability: `COMPLETE` when shipped or correctly
  `CUT_BY_PREAUTHORIZED_GATE`.
- Judge execution path: `COMPLETE` or `PARTIAL`.
- Recording-ready package: `COMPLETE` or `PARTIAL`.
- Submission materials: `COMPLETE` or `PARTIAL`.
- Devpost submission: `COMPLETE` or `BLOCKED`.
- Overall Build Week delivery: `COMPLETE` only when all required surfaces and the
  confirmed submission are complete.

Time exhaustion, substantial code, or a nearly complete project is not completion.
While every independent requirement is complete but the submission hold remains
active, the correct state is `WAITING_FOR_SUBMISSION_HOLD_RELEASE`, not complete.
