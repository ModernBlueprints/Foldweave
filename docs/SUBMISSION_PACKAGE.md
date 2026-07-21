# Foldweave — Build Week release and submission package

Status: **FOLDWEAVE PRODUCT RELEASE CANDIDATE ACCEPTED — FRESH CLEAN-CLONE
PACKAGE, REPLAY, ORIGIN/RECEIVER, AND NATIVE-REVIEW EVIDENCE ARE RECORDED;
PUBLIC-`main` PROMOTION IS COMPLETE; FINAL MEDIA, USER-OWNED ATTESTATIONS,
AND FINAL SUBMISSION REMAIN PENDING**

Submission hold: **ACTIVE — FINAL DEVPOST SUBMISSION IS PROHIBITED UNTIL THE
USER EXPLICITLY RELEASES THE HOLD**

This document is the current Foldweave release narrative, judge path, Devpost
draft, media plan, claim boundary, and due-diligence checklist. It deliberately
separates verified implementation evidence from evidence that must still be
produced at release.

Product truth remains in
[`build/BUILD_SPEC.md`](build/BUILD_SPEC.md). Dependency order and observed
milestone evidence remain in
[`build/IMPLEMENTATION_PLAN.md`](build/IMPLEMENTATION_PLAN.md), while
[`build/STATE.md`](build/STATE.md) records the latest operational checkpoint.
This package cannot promote a working-tree build to a release candidate, infer
external approval, release the submission hold, or authorize final submission.

## Submission-control status

| Decision surface | Current evidence-backed state |
|---|---|
| Product identity | **Foldweave** |
| Tagline | **Change the structure. Keep the connections.** |
| Track | **Work & Productivity** |
| Category | **AI refactoring for connected project folders** |
| Clean-clone reproduction checkout | Documentation checkpoint `53fa3206c505292f4204d25a7fd8552093ed41fb` on `revision/foldweave-native-review`; it follows accepted product release-candidate commit `4e9ec44b02b25f515017ceb9922fff4fdf84ae46`. The current documentation-branch SHA is reported only in the release handoff. |
| Review-before-execution authority | **VERIFIED** for origin and receiver jobs |
| Packaged macOS application | **VERIFIED** as an Apple-Silicon unsigned/ad-hoc judge build; not notarized or Developer-ID signed |
| Native direct API mode | **VERIFIED** with exact `gpt-5.6`, bounded revision, exact acceptance, verification, and reconstruction |
| ChatGPT developer mode | `DEVELOPER_MODE_VERIFIED` in the actual macOS ChatGPT application |
| Public consumer gateway | `CONSUMER_PAIRING_VERIFIED`; deployment `d14d051d-8920-44ea-b336-f3bbea2f6936`, version `9ac88da8-9f85-4685-8a07-073d44b909b9`, is live at <https://foldweave-gateway.skybert-ghostline.workers.dev> and its health endpoint reports ready |
| Consumer pairing | `CONSUMER_PAIRING_VERIFIED`; live OAuth/PKCE, one-time pairing, outbound WSS, opaque local selection, origin and receiver-derivative transactions, disconnect/reconnect, verification, reconstruction, and bounded refusal behavior passed in Google Chrome |
| ChatGPT publication | `PUBLICATION_READY` in the narrow technical sense required to prepare an external review submission; `SUBMITTED_FOR_REVIEW`, `APPROVED`, `PUBLISHED`, and public listing are **NOT ESTABLISHED** |
| Codex plugin | Version `0.1.0+codex.20260721091729` is installed and enabled from the repository marketplace; installed cache inspection and stdio MCP initialization/tool discovery passed; clean-clone plugin validation and stdio MCP discovery passed from commit `4e9ec44b02b25f515017ceb9922fff4fdf84ae46` |
| Visual system | Objective macOS-style visual, responsive, component, accessibility, screenshot, and thumbnail checks pass |
| Release candidate | Product commit `4e9ec44b02b25f515017ceb9922fff4fdf84ae46` is selected and accepted; a fresh unrelated clean clone of the later documentation checkpoint rebuilt and exercised the same product code successfully |
| Final public `main` | Contains the accepted Foldweave release evidence through an ordinary no-force fast-forward; the exact current SHA is reported in the release handoff rather than embedded self-referentially |
| Final screenshots and thumbnail | Captured against the accepted product release candidate, visually reviewed, hash-recorded, and published in the current public release-evidence history |
| Final public video | **NOT CREATED OR UPLOADED** |
| `/feedback` Session ID | **USER ACTION PENDING** |
| Personal eligibility and ownership attestations | **USER ACTION PENDING** |
| Submission-hold release | **USER ACTION PENDING** |
| Final Devpost submission | **NOT PERFORMED** |

## Official Build Week requirement snapshot

The current release process must remain aligned with the
[official rules](https://openai.devpost.com/rules),
[FAQ](https://openai.devpost.com/details/faqs), and
[dates page](https://openai.devpost.com/details/dates). The binding submission
deadline is **Wednesday 22 July 2026 at 02:00 CEST**.

Those official sources were rechecked on Tuesday 21 July 2026 during the final
recording-readiness pass. They still state a July 21, 2026 17:00 PDT submission
deadline, which is Wednesday 22 July 2026 at 02:00 CEST; require a public
YouTube video with audio below three minutes; require clear Codex and GPT-5.6
use; require the primary `/feedback` Session ID; and prohibit changing a
submission after the period closes. No Devpost field or submission state was
mutated by that recheck.

The final package must include:

- a working project built with Codex and GPT-5.6;
- one selected track, **Work & Productivity**;
- a public repository available to judges, with relevant licensing and clear
  installation and testing instructions;
- a description of the product's features and functionality;
- an accurate explanation of the specific contributions of Codex and GPT-5.6;
- accurate disclosure of pre-existing and third-party work;
- the primary Codex task's `/feedback` Session ID;
- a publicly viewable YouTube demonstration with intelligible audio, a clear
  working product demonstration, and an exported duration strictly below three
  minutes; and
- the user's personal confirmation of entrant type, country, eligibility,
  ownership, representative authority where applicable, and every other legal
  attestation on the final form.

Official sources and the live submission form control if either changes. The
user must personally review and make every personal or legal attestation.

## Submission identity and draft fields

| Field | Foldweave draft or current status |
|---|---|
| Project name | `Foldweave` |
| Exact casing | `Foldweave`, never `FoldWeave` |
| Tagline | `Change the structure. Keep the connections.` |
| Track/category | `Work & Productivity` / `AI refactoring for connected project folders` |
| One-line summary | `Foldweave shows a complete connected-folder reorganization before execution, lets the user refine the proposal, and applies or extends the same verified structure on an equivalent copy while preserving supported Markdown links.` |
| Public repository | <https://github.com/ModernBlueprints/reversible-name-atlas> — repository slug may remain historical; the accepted Foldweave release evidence is public on `main` and the revision branch |
| License | MIT, subject to final package and third-party-notice inspection |
| Tested native platform | macOS Apple Silicon only |
| Native distribution statement | Unsigned/ad-hoc judge build; no notarization, Developer ID, or warning-free public installation claim |
| Direct AI path | User-supplied OpenAI API key; exact `gpt-5.6` through the Responses API |
| ChatGPT path | ChatGPT supplies model inference; no hidden Foldweave Responses API call or direct-ledger reservation |
| Recorded path | Keyless, provider-free, clearly labelled **Recorded GPT planning run** |
| Unchanged Change File path | Keyless and model-free deterministic review and application |
| Final release commit | Product release-candidate commit `4e9ec44b02b25f515017ceb9922fff4fdf84ae46`; reconciled release evidence is fast-forwarded to public `main` and the revision branch, with the current SHA verified in the handoff rather than embedded self-referentially |
| Fresh clean-clone native app digest | 55 MiB Apple-Silicon `Foldweave.app`; executable SHA-256 `3a2bd5ed0eeca704fe8aed2c30652e18aedc088ebb65d5ec5a66d9d8031d1976`; `codesign --verify --deep --strict` passed; unsigned/ad-hoc only |
| Fresh clean-clone wheel digest | `foldweave-0.1.0-py3-none-any.whl`; SHA-256 `c510b708c715aa59e1453a8ed5f7254372bc85d280fd490f339c6298732ad276` |
| Fresh clean-clone Change File, receipt, and verifier identities | Origin Change File fingerprint `940774830794366ce6c27bd6365629c6efed6a18461a3303298f295420efc214`, receipt `f24ca69126ba56b8aa950fe0056b9494aab6bb11c945da256f867e6ea23f5fd8`; receiver receipt `b00296cbd83a5cf9daad1f00400e41ed9759dbda21bce797cc852967c0c37169`; equal organized-tree commitment `a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`; source-free/source-aware verification and both reconstructions passed |
| Final screenshots and thumbnail | Current ten-image Foldweave gallery and thumbnail are captured against the accepted product candidate, visually reviewed, hash-recorded, and published in current release-evidence history |
| Devpost project copy | Foldweave draft below is synchronized to the accepted product candidate; final user review, form entry, video URL, and personal attestations remain pending |
| Public video URL | `[PENDING FINAL CAPTURE, USER VOICE, EDIT, PUBLIC UPLOAD, AND PLAYBACK VERIFICATION]` |
| `/feedback` Session ID | `[USER ACTION REQUIRED IN THE PRIMARY CODEX TASK]` |
| Entrant type and country | `[USER ACTION REQUIRED; DO NOT INFER]` |
| Eligibility/ownership attestations | `[USER ACTION REQUIRED; READ AND PERSONALLY ATTEST]` |
| Submission-hold release | `[USER ACTION REQUIRED AFTER EVERY PREREQUISITE PASSES]` |
| Final submission | `NOT PERFORMED` |

## Product case

### The problem

A project folder is not merely a list of filenames. Notes link to reports,
research, images, presentations, meeting records, and working material. A model
can suggest a better structure, but an unreviewed batch of filesystem changes
can omit a file, create a collision, break a supported link, or produce a
different structure when a teammate repeats the request.

The difficult transaction is broader than renaming files:

1. understand the requested structure from bounded evidence;
2. show exactly what would change before anything is copied;
3. let the user refine the complete proposal without silently changing other
   mappings;
4. execute only the exact proposal the user reviewed;
5. preserve every supported file and relative Markdown connection;
6. prove the separate result independently; and
7. carry that reviewed structure to a differently arranged but strictly
   equivalent copy without guessing.

### The solution

Foldweave is a packaged local-first macOS application for connected project
folders. A user chooses a folder and describes the desired organization. A live
host or a recorded planner proposes one complete structure. Deterministic code
then accounts for every admitted member, validates every destination, derives
supported Markdown-link rewrites, and renders one immutable preview.

The product stops before execution. The user toggles between the current and
proposed structures, inspects changed files and link effects, and either:

- selects **Accept this structure and create copy**; or
- enters a bounded revision instruction and selects **Send changes**.

Only acceptance of the exact visible preview authorizes Foldweave to create a
separate result. The selected source is not renamed, edited, or deleted.

The verified result can include a payload-free **Foldweave Change File**.
Another person can combine that file with a differently arranged but strictly
equivalent copy, see their own current structure against the shared proposal,
and either accept it unchanged without a model or build the next reviewed
proposal through an authorized live planning host.

### What makes Foldweave distinct

Foldweave separates four authorities that are often collapsed in an AI file
tool:

- **The model proposes.** It can inspect only bounded, eligible, job-scoped
  evidence and submit a complete plan or strict sparse revision.
- **Deterministic code compiles.** It owns file accounting, path validation,
  matching, supported-link derivation, copy execution, receipts, verification,
  and reconstruction.
- **The user authorizes.** Execution binds the exact job revision, candidate,
  preview, source, imported Change File, destination, and idempotency key.
- **Independent proof verifies.** A result can be checked without trusting the
  planner, UI, original job, API key, or original source.

That split makes the review a real execution boundary rather than an
illustration placed in front of an already-running transaction.

### Potential impact

The initial audience is anyone preparing a connected project folder for handoff
or reuse: consultants, researchers, educators, journalists, designers,
photographers, small agencies, preservation workers, and technically capable
enthusiasts.

The demonstrated value is concrete: one person can design and review a folder
structure in ordinary language; another can inspect that structure against
their own equivalent copy, apply it without a model, or extend it into a new
reviewed change. Foldweave does not claim broad adoption, measured time savings,
support for independently edited copies, or production readiness.

## Four required execution modes

| Mode | Who supplies model inference | Foldweave API credential | Direct budget ledger | Required behavior |
|---|---|---|---|---|
| Native direct API | Exact `gpt-5.6` through the OpenAI Responses API | User-supplied API key | Yes | Complete origin or derivative planning, review, bounded revision, exact acceptance, proof, and reconstruction in `Foldweave.app` |
| ChatGPT-hosted | The model supplied by the user's ChatGPT session | None | No | Complete planning and revision through the Foldweave widget and paired local companion, with no hidden direct API call |
| Recorded replay | None | None | No | Exact, labelled, keyless replay that stops for review before acceptance |
| Unchanged Change File application | None | None | No | Deterministic receiver matching, review, exact acceptance, proof, and reconstruction |

Codex is a required access surface over the same bounded MCP and deterministic
domain services. It supplies host inference in Codex-hosted planning, but it is
not a fifth model-provenance mode and does not create another engine.

ChatGPT subscription access and OpenAI API billing are separate. OAuth and
pairing authorize ChatGPT to use Foldweave; they do not convert a ChatGPT
subscription into Responses API credit.

## Journey A — Create a new Foldweave

1. Choose a local source folder through the native picker or validated manual
   path.
2. Describe the desired folder reorganization.
3. Choose native direct API or ChatGPT-hosted planning, or use the recorded
   replay for a keyless demonstration.
4. Choose or confirm the result location.
5. Acknowledge the bounded evidence and retention disclosure.
6. Foldweave scans and commits the source, then the selected host proposes a
   complete structure.
7. Deterministic code compiles the proposal and stops in `reviewing`.
8. Toggle between **Original structure** and **Proposed structure**; inspect
   changes, protected members, supported-link effects, counts, and rationale.
9. Accept the exact preview, or request one of at most two bounded user
   revisions.
10. If a revision fails, keep the prior valid proposal or try another change
    within the remaining limit.
11. Exact acceptance durably binds the visible candidate and preview.
12. Foldweave creates a separate copy, rewrites only supported Markdown
    destination spans, verifies the result, produces its receipt and applicable
    Change File, rescans the source, and promotes only if every check passes.

No result, receipt, reconstruction authority, or new Change File exists while
the job is merely under review.

## Journey B — Apply or build on a shared change

1. Choose a Foldweave Change File.
2. Choose the local differently arranged but strictly equivalent project.
3. Foldweave verifies the Change File, scans the complete source, performs
   deterministic matching, and compiles a receiver-local candidate.
4. The job stops in `reviewing` without creating output.
5. Toggle between **Your current folder** and **Shared proposal**. Every local
   file, explicit empty directory, protected member, and supported link is
   represented from deterministic evidence; no GPT request is needed to render
   the comparison.
6. Choose one branch:

   - **Accept unchanged.** The exact imported proposal executes as
     `capsule_applied` with no GPT call, API request, direct-budget reservation,
     or external model request.
   - **Build the next proposal.** A new immutable derivative child uses native
     direct API, ChatGPT, or Codex-hosted planning. The complete T2 proposal is
     reviewed and must be accepted separately.

7. The verified receiver result has its own receipt, verifier output, and
   reconstruction authority.
8. A derivative result may export one complete, self-contained child Foldweave
   Change File. It is not a sparse patch and does not require possession of its
   parent at application time.

Changed payload, changed Markdown prose, changed supported relationships,
protected disagreement, extra or missing members, ambiguous symmetric groups,
invalid fingerprints, source mutation, and convergence failure block instead
of triggering semantic guessing.

## The Sofia → Martin → Sofia story

Sofia has a 24-file Apollo project with supported Markdown links, an explicit
empty directory, protected material, ordinary text, and opaque formats that
Foldweave carries byte-for-byte. She requests a Northstar handoff structure.

Foldweave shows Sofia her original and proposed trees. She asks for one focused
revision, reviews the replacement preview, and accepts it. Foldweave creates
the verified T1 result and CF1 while leaving her source unchanged.

Martin has the same supported logical project under different local paths. He
selects CF1 and his own folder. Foldweave deterministically renders **Your
current folder** against **Shared proposal**. Martin can accept T1 unchanged
without a model, or use a live host to create a complete T2 child. The parent
review and its unchanged-acceptance route remain intact while the derivative is
reviewed.

After Martin accepts T2, Foldweave produces self-contained CF2. Sofia can apply
CF2 to her unchanged equivalent source or to a verified prior T1 `data/`
directory without possessing CF1. The accepted T2 results converge to the same
organized-tree commitment, while each transaction reconstructs the source
selected when that transaction began.

This is serial collaboration with explicit forks. Foldweave does not claim
live collaboration, automatic merge, accounts, participant authentication, or
reconciliation of independently edited copies.

## Architecture and technology

### One local deterministic authority

One Python 3.11 engine and one durable `FolderRefactorJobV3` authority serve:

- the packaged macOS application;
- browser fallback;
- CLI;
- local STDIO MCP and Codex;
- authenticated public HTTP MCP and the ChatGPT widget;
- recorded replay;
- Change File application;
- receipt verification; and
- reconstruction.

The deterministic engine owns inventory, hashing, matching, compilation,
supported-link rewriting, destination reservation, copy execution, receipts,
verification, and reconstruction. Frontends and hosts do not own durable
product state.

### Technology list

- Codex and GPT-5.6 as the primary development and direct-planning environment;
- OpenAI Responses API with strict function schemas and `store=false` for
  native direct mode;
- OpenAI Apps SDK/MCP Apps bridge for the ChatGPT widget;
- Python 3.11;
- Pydantic v2 strict versioned contracts;
- FastAPI, Uvicorn, and Jinja2 as the single local control plane;
- React 18, TypeScript, BlueprintJS v6, and Vite for the focused review tree and
  shared ChatGPT widget;
- pywebview 6 and Cocoa/WebKit for the narrow native shell;
- macOS Keychain Services and a native secure credential sheet;
- PyInstaller 6 `onedir --windowed` packaging for Apple Silicon;
- official Python MCP SDK v1 for local STDIO and Streamable HTTP MCP;
- Cloudflare Workers, `@cloudflare/workers-oauth-provider`, Workers KV,
  SQLite-backed Durable Objects, OAuth 2.1/PKCE, and outbound companion WSS for
  the consumer ChatGPT transport;
- Ed25519 device identity and signed transport envelopes;
- Library of Congress `bagit`, canonical SHA-256 fingerprints, and standard
  filesystem primitives;
- `uv` with a committed lockfile;
- pytest, Ruff, Vitest, TypeScript, and Wrangler build checks; and
- Git and GitHub.

Node.js is required to build the focused frontend and gateway. It is not a
runtime dependency inside the packaged native application.

### Native application boundary

The tested native profile is `Foldweave.app` on macOS Apple Silicon. It starts
one ephemeral loopback FastAPI server, waits for health, opens the system
webview on the main thread, and exposes a narrow bridge only for fixed-role
pickers, Keychain-backed settings, Finder reveal, and lifecycle.

The current qualified app is an unsigned/ad-hoc judge build. It is not
Developer-ID signed or notarized. Gatekeeper may warn or reject normal public
launch without the documented judge action. Foldweave does not claim native
Windows or Linux support, warning-free installation on every Mac, or public
distribution readiness from the existence of a local `.app` alone.

### ChatGPT consumer topology

The intended consumer topology is:

`ChatGPT + Foldweave widget → authenticated public MCP gateway → paired outbound companion → local deterministic engine`

The widget cannot access the filesystem. Selection happens locally and returns
opaque, device-bound handles; absolute local paths do not cross the public
gateway. The gateway transports bounded requests and OAuth/device authority but
does not become a second job store, planner, idempotency ledger, receipt,
verifier, or repository for project payloads.

Developer-mode qualification in the macOS ChatGPT app is verified. The stable
`workers.dev` gateway and paired outbound companion are also consumer-qualified:
live OAuth/PKCE, opaque local selection, root and receiver-derivative review,
bounded revision, exact acceptance, disconnect/reconnect, verification,
reconstruction, refusal behavior, and no-ledger-mutation checks passed in
Google Chrome. Standard component-authored `ui/message` was acknowledged but
required one explicit same-conversation continuation; Foldweave does not claim
that continuation is automatic. This evidence establishes
`CONSUMER_PAIRING_VERIFIED` and the narrow technical `PUBLICATION_READY` state.
It does not establish review submission, approval, publication, public listing,
or general availability in ChatGPT.

## How GPT-5.6 and ChatGPT are used

### Direct Responses API mode

Direct mode uses exact alias `gpt-5.6`, strict tools and schemas,
`store=false`, no fallback model, no Chat Completions fallback, and no provider
retry. The trusted Python process reads the user-supplied key. The key never
enters React, the DOM, browser storage, jobs, receipts, replays, Change Files,
MCP traffic, ChatGPT, screenshots, or committed files.

The planner may inspect relative inventory, bounded eligible text excerpts, and
supported Markdown-link evidence. It may submit one complete plan, ask at most
one essential clarification, and respond to at most two user-requested
revisions within the shared bounded counters. It cannot mutate the source,
execute a plan, approve its own proposal, construct proof, or override a
deterministic blocker.

Foldweave sets `store=false`, which means it does not ask the Responses API to
retain the response for later application retrieval. This is not a zero-
retention or zero-logging claim; standard abuse-monitoring and prompt-caching
retention may still apply.

### ChatGPT-hosted mode

In ChatGPT-hosted mode, the model supplied by the user's ChatGPT session calls
Foldweave's bounded host-planning tools. Foldweave does not read a direct API
key, initialize the Responses API provider, reserve direct budget, or fabricate
direct model identity, usage, cost, response IDs, or `store=false` metadata.

The visible widget renders the same immutable preview DTO as the native review
surface. **Send changes** re-enters the host-model loop; deterministic refresh,
exact acceptance, Change File retrieval, verification, and reconstruction call
bounded product tools.

### Recorded and model-free modes

Recorded replay is exact, sanitized, keyless, provider-free, and visibly
labelled **Recorded GPT planning run**. It fails closed when its fixture,
request, evidence, schemas, or fingerprints drift.

Unchanged Change File preparation, review, acceptance, verification, and
reconstruction use no model. A deterministic mismatch never invokes a model as
a fallback.

## How Codex was used

Codex was the primary implementation and integration environment. The user
selected and refined the product direction, approved the frozen contracts, and
retained authority over the final voice, personal attestations, `/feedback`,
submission hold, and final submission.

In the primary task, Codex:

- converted successive product decisions into one frozen specification, one
  dependency-ordered plan, one execution goal, and one observed state;
- preserved the complete earlier scanner, compiler, Change File, matcher,
  receipt, verifier, and reconstruction foundation while adding strict
  historical dispatch;
- built JobV3, the immutable preview DTO, review-before-execution, bounded
  revisions, exact authorization, destination reservation, and restart/race
  protections;
- built the focused React/TypeScript review tree and the restrained macOS-style
  native/browser/widget visual system;
- packaged the pywebview macOS application and integrated native pickers,
  Keychain settings, Finder reveal, health-gated startup, and clean shutdown;
- implemented direct, ChatGPT-hosted, Codex-hosted, replay, and model-free
  provenance through one engine;
- implemented Change File v2, receipt/verifier v3, immediate-parent lineage,
  self-contained derivative Change Files, convergence, and participant-specific
  reconstruction;
- implemented local and public MCP transports, the thin Codex plugin, the
  Cloudflare gateway, OAuth/pairing, and outbound companion; and
- used bounded independent reviewers, reproduced material findings, and turned
  valid findings into normal regression tests.

This is an evidence-backed account of work performed, not a measured
productivity percentage or a claim that Codex independently chose the product.

## Proof and trust boundaries

### What Foldweave proves

For an accepted transaction, Foldweave can prove within its supported contract:

- the selected source commitment;
- complete in-scope member accounting;
- the exact candidate and preview the user authorized;
- path, suffix, protection, collision, and source-stability checks;
- supported Markdown-link rewrites and target identity;
- separate-result creation without source mutation;
- artifact, receipt, Change File, and BagIt consistency;
- the path-sensitive organized-tree commitment, including explicit empty
  directories;
- receiver-specific deterministic matching and convergence; and
- reconstruction of the selected transaction source's in-scope relative paths
  and bytes.

### Foldweave Change File disclosure

A Foldweave Change File contains no project payload bytes. It does contain
project names and structure, file sizes and hashes, supported-link
relationships, the instruction, target names, immediate-parent lineage where
applicable, and proof identifiers.

The file proves its internal fingerprints and receipt binding. It does not
prove sender identity, authorship, participant identity, institutional
authorization, signature validity, or historical authenticity.

### Reconstruction boundary

**Recreate original** verifies first and creates an absent destination. It
restores the selected transaction source's in-scope relative paths and exact
bytes, including preserved original Markdown bytes and explicit empty
directories.

It does not restore timestamps, ownership, permissions, ACLs, extended
attributes, resource forks, symlink or hard-link identity, undeclared
references, or the first ancestor of an entire collaboration chain.

## Judge paths

The judge path was reproduced from a fresh unrelated clone of the published
revision-branch documentation checkpoint, whose product source is unchanged
from accepted product commit `4e9ec44b02b25f515017ceb9922fff4fdf84ae46`.
It passed the full Python suite, frontend and gateway builds, an installed-wheel
replay, origin/receiver acceptance, source-free and source-aware verification,
and reconstruction. The same commands are now the public judge path; no claim
is made that a final Devpost submission has occurred.

### Fastest keyless path

Prerequisites: macOS Apple Silicon, Python 3.11, and `uv`.

1. Clone the final accepted Foldweave revision.
2. Run `uv sync --frozen`.
3. Run `uv run foldweave demo --mode replay`.
4. Review **Original structure** and **Proposed structure**.
5. Optionally inspect the preview through `uv run foldweave preview JOB_FILE`.
6. Accept the exact displayed preview through the application or the documented
   `foldweave accept` command.
7. Inspect the separate verified result, receipt, Change File, and
   reconstruction.

Replay needs no API key and makes no provider call.

### Build and open the tested macOS application

Run:

`uv run pyinstaller --noconfirm --clean packaging/Foldweave.spec`

Then:

`open dist/Foldweave.app`

The final README must state the exact unsigned/ad-hoc launch behavior observed
from the accepted clean clone. It must not imply notarization or Developer-ID
signing.

### Browser fallback

Run:

`uv run foldweave app --browser`

This uses loopback HTTP on the same Mac. It is not a hosted web service.

### Direct live planning

Provide `OPENAI_API_KEY` only through the trusted local environment or the
native Keychain settings surface. Then prepare a review job:

`uv run foldweave run --mode live --source SOURCE_ROOT --output OUTPUT_PARENT --job JOB_FILE --request "Prepare this project for handoff. Keep every file and every supported link working."`

Inspect the immutable preview:

`uv run foldweave preview JOB_FILE`

Optionally request a bounded revision:

`uv run foldweave revise JOB_FILE --instruction "Move only the approved budget into an approved finance folder." --idempotency-key judge-revision-20260720-01`

Accept only the exact displayed preview:

`uv run foldweave accept JOB_FILE --preview-fingerprint PREVIEW_SHA256 --idempotency-key judge-accept-20260720-01`

### Unchanged Change File review and application

Prepare a receiver-local review:

`uv run foldweave apply-change CHANGE_FILE --source RECEIVER_SOURCE --output OUTPUT_PARENT --job RECEIVER_JOB`

Then inspect and accept the exact preview:

`uv run foldweave preview RECEIVER_JOB`

`uv run foldweave accept RECEIVER_JOB --preview-fingerprint PREVIEW_SHA256 --idempotency-key receiver-accept-20260720-01`

Preparation and review are model-free. No result is created before acceptance.

### Independent verification and reconstruction

- `uv run foldweave verify-receipt RESULT_BAG`
- `uv run foldweave verify-receipt RESULT_BAG --source SOURCE_ROOT`
- `uv run foldweave restore-receipt RESULT_BAG RESTORE_DESTINATION`

The source-free verifier requires no job, model, API key, browser, or original
source and writes nothing.

### Local MCP and Codex plugin

Start the shared local MCP server:

`uv run foldweave mcp --transport stdio`

From the final clean clone, install the thin plugin:

1. `CODEX_BIN="/Applications/ChatGPT.app/Contents/Resources/codex"`
2. `"$CODEX_BIN" plugin marketplace add .`
3. `"$CODEX_BIN" plugin add foldweave@personal`
4. Refresh or restart Codex.
5. Open a new Codex task whose working directory is the clean clone.
6. Discover and invoke Foldweave's reviewed workflow tools.

Uninstall with:

- `"$CODEX_BIN" plugin remove foldweave@personal`
- `"$CODEX_BIN" plugin marketplace remove personal`

The plugin is a thin relative MCP package around the same repository engine. It
contains no copied product implementation or developer-specific absolute path.

### ChatGPT-hosted judge path

Developer-mode qualification through the official Secure MCP Tunnel has passed
in the actual macOS ChatGPT application. The consumer topology has also passed
live OAuth/pairing/companion qualification in Google Chrome, including complete
origin and receiver-derivative transactions plus reconnect and refusal checks.
The qualified path may be documented with its explicit same-conversation
revision-recovery limitation. Do not say the app is submitted for review,
approved, published, publicly listed, or generally available in ChatGPT, and do
not substitute a hidden direct API request.

## Current verified implementation evidence

The following combines earlier qualification with a fresh unrelated clean-clone
release reproduction. The product-source evidence is release-candidate evidence
now fast-forwarded to public `main`; video, user-owned `/feedback`, legal
attestations, and submission remain intentionally separate gates.

| Surface | Latest verified evidence |
|---|---|
| Python regression | **1,176 passed**, one upstream warning |
| Frontend | **80/80** tests; strict TypeScript and both production builds pass |
| Public gateway | **50/50** Worker tests; strict TypeScript and Wrangler production dry build pass |
| Native/package focus | **30** focused tests; unrelated-directory launch, picker, temporary Keychain round trip/removal, rehydration, exact acceptance, verification, and no-orphan checks pass |
| Visual focus | **27** visual/pairing/proof/native tests; 500-file/1,000-directory review fixture passes required interaction and narrow-layout checks |
| Codex plugin focus | **21** focused checks plus official cachebuster, validator, reinstall, installed-cache identity, fresh-session tool use, exact acceptance, verification, reconstruction, and duplicate retry |
| Fresh clean-clone packaged app | Approximately 55 MiB, arm64, bundle ID `com.modernblueprints.foldweave`, version `0.1.0`, minimum macOS `13.0`, executable SHA-256 `3a2bd5ed0eeca704fe8aed2c30652e18aedc088ebb65d5ec5a66d9d8031d1976`; strict deep signature verification, unrelated-directory launch, Home and immutable review rendering, Original/Proposed toggle, and clean shutdown pass; unsigned/ad-hoc only |
| Direct budget authority | Sole ledger remains capped at cumulative USD 40; current qualified state records 14 attempts and no hosted-ledger mutation |
| ChatGPT developer flow | Actual macOS ChatGPT root and derivative review/revision/acceptance/verification/reconstruction evidence exists without direct-ledger mutation |
| F2 collaboration | Direct and ChatGPT-hosted derivatives converge; self-contained child Change Files, v3 receipts, verification, and transaction-specific reconstruction pass |
| Consumer gateway | `CONSUMER_PAIRING_VERIFIED`; deployment `d14d051d-8920-44ea-b336-f3bbea2f6936`, version `9ac88da8-9f85-4685-8a07-073d44b909b9`, serves `review-v35`; CSS SHA-256 `666df057a85df92cfdd57228ef9fc1a8ece31cd65807720695d14dbd867ca173`, JavaScript SHA-256 `3ac8e6c83350e1d88145d50470a90cb3b2763386aee816986139e611f3ac4bea`; `PUBLICATION_READY` is technical readiness only |

The clean-clone artifact hashes above identify the reproduced package, not a
notarized or externally hosted distribution. The no-force public `main`
promotion is complete; final media, user-owned form actions, and final submission
remain separate controlled steps.

## Devpost description draft

### Inspiration

Project folders contain relationships. Notes point to deliverables, research,
images, and meeting records. A model can propose a cleaner hierarchy, but an
unreviewed change can omit a file, break a supported link, or give each
teammate a different result.

We wanted a folder change that a person could inspect before execution, refine
without losing the valid proposal, carry to an equivalent copy without sending
the project payload, and verify independently.

### What it does

Foldweave lets a user select a connected project folder and describe a complete
reorganization in plain English. A direct GPT-5.6 planner, ChatGPT or Codex
host, or exact recorded replay proposes the structure. Deterministic code
accounts for every admitted member, validates every destination, derives
supported Markdown-link rewrites, and renders the original and proposed trees.

Nothing is copied while the proposal is under review. The user can accept the
exact preview or request a bounded revision. Acceptance creates a separate
verified result and can produce a payload-free Foldweave Change File.

Another person can combine that Change File with a differently arranged but
strictly equivalent copy. Foldweave deterministically shows their current tree
against the shared proposal. They can accept it unchanged without a model or
create a complete derivative proposal through an authorized live host. Changed
or ambiguous input blocks instead of being guessed.

### How we built it

One Python 3.11 engine owns scanning, hashing, deterministic compilation,
matching, exact Markdown rewriting, copy execution, versioned receipts,
verification, and reconstruction. FastAPI is the single local control plane.
React, TypeScript, BlueprintJS, and Vite implement the focused review tree and
shared ChatGPT widget. pywebview and PyInstaller package the Apple-Silicon app;
Keychain Services protect the direct credential.

The same domain services power the browser fallback, CLI, local STDIO MCP,
Codex plugin, and ChatGPT transport. The consumer ChatGPT architecture uses a
Cloudflare Workers OAuth gateway and an outbound paired companion so the remote
widget receives opaque handles rather than filesystem paths.

### How GPT-5.6 and host models are used

Native direct mode uses exact `gpt-5.6` through the Responses API with strict
tools, `store=false`, no fallback model, and no provider retry. The model sees
only bounded eligible evidence and proposes a complete plan or strict revision.
It cannot mutate files, accept its own proposal, build a receipt, or override
proof.

In ChatGPT-hosted and Codex-hosted modes, the host supplies model inference and
calls the same bounded planning tools. Foldweave does not make a hidden direct
API request or reserve the direct budget. Recorded replay and unchanged Change
File application are model-free.

### Challenges and accomplishments

The central implementation challenge was not drawing a folder tree. It was
making the rendered proposal the exact execution authority across native,
browser, ChatGPT, Codex, CLI, retries, restarts, and races.

The other difficult boundary was carrying one structure across different local
layouts. Foldweave matches complete equivalent projects from exact payload
descriptors and supported-link relationships, accepts only unique mappings,
and blocks symmetric ambiguity. A derivative Change File is complete and
self-contained while committing only one immediate parent.

The Sofia → Martin → Sofia proof demonstrates review, revision, unchanged
model-free application, derivative collaboration, convergence, independent
verification, and source-specific reconstruction through one engine.

### What we learned

AI is most useful here when it proposes intent but does not control execution or
proof. A preview is trustworthy only when acceptance binds the exact candidate
the user saw, and a portable change is credible only when deterministic code
accounts for every member and refuses ambiguity.

### What's next

After Build Week, honest next steps are user testing, measured workflow studies,
signed/notarized distribution, and evidence-based support for additional narrow
connection types. Independently edited-copy reconciliation, general semantic
matching, automatic merge, arbitrary code refactoring, cloud project sync, and
production hardening are outside this release.

## Devpost field draft

| Devpost field | Draft value or remaining authority |
|---|---|
| Project name | `Foldweave` |
| Tagline | `Change the structure. Keep the connections.` |
| Category | `Work & Productivity` |
| Repository | `https://github.com/ModernBlueprints/reversible-name-atlas` — accepted Foldweave release evidence is fast-forwarded to public `main`; exact current SHA is recorded in the release handoff |
| Technologies | `Codex, GPT-5.6, OpenAI Responses API, OpenAI Apps SDK, MCP, Python 3.11, Pydantic, FastAPI, Uvicorn, Jinja2, React, TypeScript, BlueprintJS, Vite, pywebview, PyInstaller, macOS Keychain, Cloudflare Workers, OAuth 2.1/PKCE, Durable Objects, Workers KV, WebSockets, BagIt, uv, pytest, Ruff, Vitest, GitHub` |
| Tested platform | `macOS Apple Silicon; unsigned/ad-hoc judge build. Browser fallback and CLI use the same local engine.` |
| Judge instructions | `Use the final README from the accepted release. The fastest keyless path is uv sync --frozen followed by uv run foldweave demo --mode replay. Review the proposed structure, accept the exact preview, verify the separate result, and recreate the selected source. No API key is required for replay.` |
| Plugin/developer-tool instructions | `Use the final plugins/foldweave/README.md from the accepted clean clone. Install foldweave@personal, restart or refresh Codex, open a fresh task, and invoke the installed Foldweave tools. Installed-copy release qualification is verified evidence for the accepted release candidate.` |
| ChatGPT availability | `DEVELOPER_MODE_VERIFIED; CONSUMER_PAIRING_VERIFIED; technically PUBLICATION_READY. Not submitted for review, approved, published, publicly listed, or generally available.` |
| Public video URL | `[PENDING]` |
| `/feedback` Session ID | `[USER ACTION REQUIRED]` |
| Submitter type | `[USER CONFIRM: INDIVIDUAL / TEAM / ORGANIZATION]` |
| Country | `[USER CONFIRM; DO NOT INFER]` |
| Eligibility/ownership | `[USER READS AND PERSONALLY ATTESTS]` |
| Submission hold | `ACTIVE — FINAL SUBMISSION PROHIBITED UNTIL EXPLICIT USER RELEASE` |

## Under-three-minute demonstration plan

Target exported duration: **2:55**. The final encoded file must remain strictly
below 3:00 after narration, transitions, and upload processing. This plan is a
draft until the final release and media are accepted.

| Time | Visual and action | Purpose |
|---:|---|---|
| 0:00–0:12 | Foldweave title; one project note linking to several local files | Establish that a folder contains connections, not only filenames |
| 0:12–0:30 | Open `Foldweave.app`; choose Sofia's folder; enter the Northstar request | Show the native, local-first start and plain-language intent |
| 0:30–0:52 | Review **Original structure** and **Proposed structure**; search or select one changed member | Prove that the complete plan is visible before execution |
| 0:52–1:10 | Enter one focused revision; show the replacement preview and delta | Demonstrate bounded iteration while the prior valid preview remains safe |
| 1:10–1:26 | Select **Accept this structure and create copy**; show Done, source unchanged, and independent verification | Show exact authorization and separate verified output |
| 1:26–1:41 | Download the Foldweave Change File; briefly show the payload-free metadata disclosure | Explain what travels and what does not |
| 1:41–2:02 | Martin chooses CF1 and his differently arranged project; toggle **Your current folder** / **Shared proposal** | Show deterministic receiver-local review without GPT |
| 2:02–2:22 | Build and review one T2 derivative through the selected live host; accept exact preview | Show serial collaboration rather than blind replay |
| 2:22–2:38 | Apply CF2 to Sofia or a verified T1 result; show equal organized-tree proof and source-specific reconstruction | Demonstrate convergence and reversibility within the contract |
| 2:38–2:48 | Brief ChatGPT widget and Codex installed-tool evidence | Explain the shared host surfaces and model-authority split |
| 2:48–2:55 | Foldweave end card and repository | Close with the product promise |

F0d has passed, so the final video may show the qualified consumer ChatGPT path
with the explicit same-conversation revision-recovery limitation. Do not imply
review submission, approval, publication, public listing, or general
availability.

## Timed narration draft

This draft must be read aloud, timed, and corrected against the final release
before recording. It intentionally avoids a public-listing claim and may use
the verified developer-mode and consumer-pairing evidence with their exact
qualifications. The current draft contains **317 whitespace-delimited words**.
A local macOS synthetic-speech preflight of this exact text measured
**150.304 seconds (2:30.304)** at 125 words per minute and **148.652 seconds
(2:28.652)** at 130 words per minute. It confirms useful script margin inside
the 2:55 storyboard, but it is not the user's voice and does not substitute for
timing the final narration or the final encoded video.

> A project folder is more than filenames. Notes connect reports, research,
> meetings, images, and working files. Reorganizing that folder with AI is easy.
> Knowing exactly what will change, preserving the connections, and carrying the
> same structure to a teammate's differently arranged copy is harder.
>
> Foldweave separates planning, authorization, and proof.
>
> Sofia selects her Apollo project and asks for a Northstar handoff. A live host
> or this exact recorded planning run proposes one complete structure from
> bounded evidence. The model cannot move a file or approve its own work.
>
> Before Foldweave creates anything, Sofia sees her original folder and the
> proposed structure. Every admitted file appears once. She can inspect moved
> items and supported Markdown links, then request a focused revision. Fixed
> code applies only that sparse change, rebuilds the complete proposal, and
> checks every destination again.
>
> Sofia accepts the exact preview. Foldweave creates a separate result, updates
> supported link destinations, leaves her source unchanged, and verifies the
> result independently.
>
> The result includes a Foldweave Change File. It contains no project payload
> bytes, but it does disclose names, structure, sizes, hashes, link
> relationships, the instruction, targets, lineage, and proof identifiers.
>
> Martin has the same supported project under different local paths. Foldweave
> matches it deterministically and shows Martin's current folder against Sofia's
> shared proposal. He can accept it unchanged without GPT, or use ChatGPT,
> Codex, or direct GPT-5.6 planning to build the next complete proposal.
>
> Martin creates T2 and sends a self-contained Change File back. Sofia can apply
> it without the earlier file. Accepted T2 results converge to the same organized
> tree, while each transaction can recreate the source it actually began with.
>
> The native app, browser fallback, ChatGPT widget, Codex plugin, replay, and
> Change File workflows all use one deterministic engine. Codex was the primary
> development environment; GPT-5.6 plans intent, the user accepts the exact
> structure, and Foldweave proves the result.
>
> Foldweave. Change the structure. Keep the connections.

Narration acceptance remains pending until:

- the lexical word count and a real spoken timing are recorded;
- every sentence maps to the final accepted release evidence;
- the user's final voice is intelligible and approved;
- the complete exported video is strictly below 3:00; and
- the public upload is watched end to end with audio.

## Capture and media checklist

1. Use the final accepted clean-clone checkout and final packaged app.
2. Capture the native application at a readable macOS window size; keep the
   system menu bar, notifications, unrelated applications, and personal paths
   out of frame.
3. Use only synthetic Sofia/Martin fixtures and release-selected results.
4. Show **Recorded GPT planning run** if replay is used. Do not label it live.
5. Show the review barrier clearly: no result before acceptance, then the exact
   acceptance action.
6. Keep technical fingerprints collapsed except for one concise convergence or
   verification proof.
7. Do not show an API key, response ID, account identifier, pairing secret,
   authorization code, private callback URL, terminal history, or unrelated
   local path.
8. If ChatGPT is shown, use only the actually qualified distribution state and
   a real Foldweave tool/widget transaction.
9. If Codex is shown, use a fresh task and the installed plugin copy from the
   final clean clone.
10. Record Finder-style, native macOS dark surfaces only after final visual QA.
11. Use no unlicensed music, third-party footage, or unapproved promotional
    asset.
12. Export below three minutes, watch the complete local file with audio,
    upload it Public to YouTube, and watch the complete public playback before
    entering the URL in Devpost.

## Final screenshot and thumbnail specification

The predecessor Name Atlas gallery is not Foldweave release evidence. Replace
it only after release-candidate acceptance with genuine captures from the final
selected commit.

| Final asset | Required frame | Acceptance requirement |
|---|---|---|
| `docs/screenshots/01-home.png` | Foldweave native Home | Minimal macOS dark surface; Create and Apply choices; no personal path or stale name |
| `docs/screenshots/02-create.png` | Sofia Create form | Native selection, request, mode, destination, accurate source/evidence statement |
| `docs/screenshots/03-origin-review.png` | Original/Proposed review | Complete tree, changed-only/search, selected-member details, exact acceptance and revision controls |
| `docs/screenshots/04-origin-revision.png` | Revised proposal | Visible proposal delta, prior valid proposal preserved, no output before acceptance |
| `docs/screenshots/05-origin-done.png` | Verified Sofia result | Source unchanged, separate result, receipt/verifier, Change File and reconstruction actions |
| `docs/screenshots/06-receiver-review.png` | Martin current/shared review | Receiver-local current tree, shared proposal, model-free trust state, unchanged/derivative choice |
| `docs/screenshots/07-derivative-review.png` | T2 derivative | Immediate-parent relationship, complete child preview, exact acceptance |
| `docs/screenshots/08-chatgpt-widget.png` | Actual qualified ChatGPT widget | Real host transaction, accurate distribution label, no path/secret or invented public availability |
| `docs/screenshots/09-codex-plugin.png` | Actual installed-copy Codex evidence | Fresh task, discovered Foldweave tool, one real invocation from final clean clone |
| `docs/screenshots/10-proof.png` | Verifier/convergence/reconstruction | Readable proof with no fabricated identity or authentication claim |

Every PNG must be genuine image bytes, readable at the intended viewport,
visually inspected, hash-recorded, and scanned for secrets, personal metadata,
paths, response IDs, stale branding, and unsupported claims.

Regenerate `docs/submission-thumbnail.svg` and
`docs/submission-thumbnail.png` with:

- a 1500×1000, 3:2 frame;
- the Foldweave name and exact tagline;
- the restrained macOS-native graphite visual language;
- one simple current structure → reviewed proposal → equivalent copy story;
- no cyber, gradient, neon, glass, or developer-dashboard styling;
- no predecessor Name Atlas release identity;
- no invented digest presented as evidence; and
- no third-party promotional imagery.

Current screenshot and thumbnail hashes:

| Asset | Pixels or kind | Bytes | SHA-256 |
|---|---:|---:|---|
| `docs/screenshots/01-home.png` | 1229×768 | 49,102 | `dd1d3aedce87630f05ac7ea11662ab78ff8f3c4cf473221c490b946de5788d78` |
| `docs/screenshots/02-create.png` | 1440×900 | 96,013 | `31b43b0f55c08da4a883614b0a8bc612bd7efdd5c79de8c027024cdcd1fce842` |
| `docs/screenshots/03-origin-review.png` | 1728×940 | 421,008 | `36fc1998d28f574337616a944eeaa90dd019f9e4f302e5b3933d493595cbdc27` |
| `docs/screenshots/04-origin-revision.png` | 1440×900 | 172,864 | `aabb9b11534d6caa96fdaadd102f31f72828c4f735dd0f2084730ccba5ba2e30` |
| `docs/screenshots/05-origin-done.png` | 3456×1880 | 136,825 | `30deed3a7618e42dd2a7589763fcfe7ac6d93cded51e3f6d2db740dc14e0fa25` |
| `docs/screenshots/06-receiver-review.png` | 1440×900 | 199,274 | `4511b7f22171d50d8bc4c89ad4cd5f09e0d834bca20d8d44c68b772de8964bc9` |
| `docs/screenshots/07-derivative-review.png` | 1440×900 | 207,760 | `f5a3a01f4beb241578a10db9cfe268e7b4c06b12467bd3e51ccd7b700a9ecc37` |
| `docs/screenshots/08-chatgpt-widget.png` | 1536×800 | 114,880 | `18b15bb3a86c7be46760e675b2d29ede4318e9bcd4cff017468b2fcb241b35bc` |
| `docs/screenshots/09-codex-plugin.png` | 1280×720 | 100,281 | `78a18e7f568787e2a78fca62a70e4f1d4de75665ada2c70034adf82e0be7ea70` |
| `docs/screenshots/10-proof.png` | 3456×1880 | 174,124 | `1cbab91b471abb5d65b2a8f9b07ea1f5d889dcbae6253fb8d1fd6c829c5c2f3f` |
| `docs/submission-thumbnail.png` | 1500×1000 | 136,792 | `b67e2f845857851fc31335ab85b9634a9f8acf9f65bdc6c95e547030876e7cb6` |
| `docs/submission-thumbnail.svg` | SVG source | 8,994 | `6f4b2b87c55ddf0b0d3c029261df581782901c555e0aae9d22a7d80ac280637d` |

These hashes are accepted release-candidate evidence for commit
`4e9ec44b02b25f515017ceb9922fff4fdf84ae46`.

## Claims and limitations

### Permitted only when demonstrated by the selected release

Foldweave may say that it:

- shows current and proposed folder structures before changing anything;
- supports bounded proposal revision before exact acceptance;
- represents every admitted member exactly once;
- keeps protected members fixed;
- updates and verifies supported relative Markdown links;
- leaves the selected source unchanged and creates a separate result;
- produces a Foldweave Change File containing no project payload bytes;
- deterministically matches and reviews a differently arranged but strictly
  equivalent copy;
- accepts an unchanged proposal without GPT or uses a live host to derive the
  next complete proposal;
- blocks changed or ambiguous input instead of guessing;
- converges accepted equivalent sources to one organized-tree commitment;
- independently verifies results and reconstructs each transaction's selected
  source paths and bytes within the supported contract;
- uses exact `gpt-5.6` in native direct mode;
- uses ChatGPT-supplied inference without a hidden Foldweave Responses API call
  in verified hosted mode; and
- uses the same local engine from the tested macOS, ChatGPT, and Codex surfaces.

### Required qualifications

- “Connections” means only the supported relative Markdown links inside the
  selected folder.
- A Change File has no payload bytes but discloses names, structure, sizes,
  hashes, supported-link relationships, instructions, targets, lineage, and
  proof identifiers.
- Live AI planning sends bounded selected evidence after disclosure.
- `store=false` is not proof of zero retention.
- ChatGPT subscription access and API billing are separate.
- ChatGPT-hosted model identity is not claimed unless authoritative host
  metadata supplies it.
- “Local-first” does not mean every mode is networkless: the browser uses
  loopback HTTP and ChatGPT uses gateway networking.
- Only macOS Apple Silicon is tested natively.
- The app is unsigned/ad-hoc, not notarized or Developer-ID signed.
- Public ChatGPT availability is claimed only from observed publication
  evidence.

### Prohibited claims

Do not claim:

- universal safety or semantic correctness;
- universal file-format, code, or reference understanding;
- code-aware refactoring;
- arbitrary connection preservation;
- general graph isomorphism or semantic-similarity matching;
- reconciliation of independently edited, extra-file, or missing-file copies;
- sender identity, participant authentication, authorship, signatures,
  institutional authorization, or historical authenticity;
- tamper-proofing, compliance, full privacy, zero retention, or no metadata
  disclosure;
- universal portability or reversibility;
- native Windows/Linux support, a mobile app, or remote-phone access;
- live collaboration, accounts, automatic merge, or cloud project sync;
- public ChatGPT listing before actual publication;
- notarized or signed distribution without evidence;
- production readiness, broad adoption, or unmeasured time savings;
- universal zero-question behavior;
- tested support for clients not actually exercised;
- absence of competitors, proven uniqueness, or probability of winning.

### Supported transaction boundary

- 1–500 regular files and at most 1,000 directories;
- at most 16 MiB per `.md`/`.markdown` member and at most 10,000 supported
  local Markdown references;
- regular files and directories only;
- symlinks, special files, hard-linked regular files, unsupported paths,
  unreadable members, overlap, insufficient capacity, and source change block;
- rename/move-only complete-file transactions;
- no deletion, omission, merge, deduplication, extraction, conversion, or
  arbitrary body editing;
- exact supported inline Markdown link/image syntax, including lexically safe
  in-root parent-relative targets;
- reference-style links and unsupported local-looking syntax block;
- deterministic complete matching only; unresolved symmetric duplicates block;
  and
- reconstruction covers admitted relative paths and bytes, not arbitrary
  filesystem metadata.

## Pre-existing and third-party work disclosure

The full disclosure is maintained in
[`PREEXISTING_WORK.md`](PREEXISTING_WORK.md). Foldweave evolved during Build
Week from earlier implementations in this repository:

- a disclosed feasibility spike informed a small set of mechanical scanning,
  canonicalization, path, copy-only staging, and forward/reverse-map behaviors;
- archive-specific tournament, evaluator, semantic-provider, scoring, and
  certification machinery was rejected and is not a runtime or test
  dependency;
- the earlier Reversible Name Atlas/Name Atlas cycles built the scanner,
  compiler, supported Markdown adapter, Change File v1, deterministic matcher,
  receipt/verifier, reconstruction, browser, MCP, and release foundation; and
- the Foldweave cycle added review-before-execution, JobV3, immutable previews,
  bounded revision, Change File v2, derivative lineage, the packaged native app,
  focused React tree, ChatGPT widget, gateway/companion, dual live planning, and
  refreshed Codex plugin.

Historical names, schemas, fingerprint domains, receipts, artifact paths, and
Git history are preserved for compatibility and provenance. Active
release-facing identity is Foldweave. Final release acceptance must verify the
MIT license, packaged notices, Blueprint, MCP, BagIt, Cloudflare, React,
pywebview, PyInstaller, and every other dependency or asset obligation.

## Claim-to-evidence audit

| Proposed public claim | Required release evidence | Current status |
|---|---|---|
| The proposal is visible before execution | Origin and receiver jobs stop at immutable review with no output | `VERIFIED — fresh clean-clone origin and receiver transactions reached review before exact acceptance` |
| The user can revise and still accept only the exact visible structure | Sparse revision, prior-preview preservation, stale/race/duplicate refusal, exact authorization | `VERIFIED — direct, ChatGPT, Codex, browser, CLI, and native qualification; fresh clean-clone replay acceptance uses the exact preview fingerprint` |
| Every admitted file appears once and supported links remain connected | Complete accounting and exact supported-link proof | `VERIFIED — fresh clean-clone origin and receiver proof: 24 files, 23 changed paths, 23 rewritten links` |
| The source remains unchanged and result is separate | Before/after source commitment and no-replace result transaction | `VERIFIED — fresh clean-clone origin and receiver source-aware verification and reconstruction pass` |
| Change Files contain no payload bytes | Strict schema/content audit and transferable-artifact scan | `VERIFIED — fresh clean-clone v2 origin Change File and receiver import pass strict verification` |
| Martin sees his own current structure | Receiver inventory/match report/preview DTO with no GPT render fallback | `VERIFIED` |
| Unchanged application uses no model | `capsule_applied` provenance and no provider/API/budget use | `VERIFIED` |
| Direct mode uses exact GPT-5.6 | Exact alias, returned model evidence, `store=false`, usage/cost, ledger | `VERIFIED in live qualification; no direct API call was made during the keyless clean-clone reproduction` |
| ChatGPT-hosted mode uses no hidden direct API call | Actual host tool traffic, no key/provider initialization, ledger byte equality | `DEVELOPER_MODE_VERIFIED; CONSUMER_PAIRING_VERIFIED` |
| Serial derivatives converge | CF1→CF2 proof, self-contained child, raw/T1 application, equal organized tree | `VERIFIED IN DIRECT AND CHATGPT DEVELOPER PATHS` |
| Results verify without source or key | Unrelated-location source-free verifier | `VERIFIED` |
| Each transaction reconstructs its own selected source | Verify-first no-replace reconstruction and exact snapshot equality | `VERIFIED` |
| Native macOS app works | Clean built `.app`, unrelated-path launch, picker, Keychain, live review/revision/accept, proof, restart, shutdown | `VERIFIED AS UNSIGNED/AD-HOC APP — fresh clean-clone build, launch, Home/review/toggle, and clean shutdown pass; no notarization or Developer ID claim` |
| Codex plugin is installed and uses the same engine | Final clean-clone install, cache identity, fresh task, discovery, invocation, complete reviewed path, uninstall | `CLEAN-CLONE PLUGIN VALIDATION AND STDIO MCP DISCOVERY PASSED; FULL INSTALLED-COPY UI INVOCATION EVIDENCE REMAINS CURRENT LOCAL QUALIFICATION` |
| Consumer ChatGPT pairing works | Real OAuth/PKCE, pairing, WSS, reconnect, bounded refusal/revocation coverage, origin and receiver derivative, unchanged ledger | `CONSUMER_PAIRING_VERIFIED`; standard `ui/message` continuation still requires the documented explicit same-conversation recovery |
| Foldweave is public in ChatGPT | Observed approval and publication | `NOT ESTABLISHED — DO NOT CLAIM` |
| Foldweave is recording-ready | Accepted release commit, clean clone, all mandatory modes, final media package, no planned product/design work | `NOT YET ESTABLISHED` |
| Video and submission are complete | Public playback, `/feedback`, attestations, hold release, Devpost confirmation | `PENDING USER AND FINAL CLOSURE ACTIONS` |

## Due-diligence checklist

### Product and release

- [x] Foldweave name, casing, tagline, product promise, and four modes are
      frozen.
- [x] Review-before-execution and exact preview-bound acceptance are implemented.
- [x] Origin and receiver revisions preserve the prior valid proposal.
- [x] Deterministic receiver rendering uses Martin's own source and needs no
      GPT merely to display the comparison.
- [x] Change File v2, receipt/verifier v3, immediate-parent lineage,
      self-contained derivative children, convergence, and transaction-specific
      reconstruction are implemented.
- [x] Packaged Apple-Silicon app, native picker, Keychain state, direct live
      planning, restart, and clean shutdown are qualified.
- [x] ChatGPT developer-mode root and derivative transactions are qualified in
      the actual macOS ChatGPT application.
- [x] Current Codex installed-copy qualification evidence exists.
- [x] Current objective macOS-style visual, maximum-shape, accessibility,
      responsive, and native-package checks pass.
- [x] Stable public `workers.dev` gateway deployment exists.
- [x] Complete live consumer OAuth/PKCE, pairing, outbound WSS, opaque local
      selection, reconnect, origin, receiver derivative, deployed refusal, and
      no-ledger-mutation qualification, with automated revocation, replay,
      expiry, rate-limit, wrong-device, and duplicate-request coverage.
- [x] Record `CONSUMER_PAIRING_VERIFIED` only after that complete evidence.
- [x] Establish and record `PUBLICATION_READY` without inferring review,
      approval, publication, or public listing.
- [x] Enter feature freeze with every mandatory path continuously runnable;
      the absolute feature-freeze boundary is active and only release-safe work
      remains.
- [x] Select one Foldweave release-candidate commit:
      `4e9ec44b02b25f515017ceb9922fff4fdf84ae46`.
- [x] Reproduce the full Python, frontend, gateway, native, replay,
      unchanged-apply, origin/receiver, verifier, and reconstruction release
      paths from a fresh unrelated clone of the published release branch. The
      direct and ChatGPT live matrices remain preserved from their earlier
      qualified evidence; they were not repeated as new paid or host calls.
- [x] Build and launch the final `.app` from an unrelated clean clone; inspect
      Home, the immutable review, Original/Proposed switching, and clean
      shutdown.
- [x] Record fresh clean-clone app, wheel, Change File, receipt, verifier,
      reconstruction, and organized-tree identities above.
- [x] Run final lock, Ruff lint/format, TypeScript, Vite, Vitest, Wrangler,
      package, diff, secret/response-ID/path, and active-brand scans. Historical
      compatibility/provenance records retain their original names and paths.
- [x] Fast-forward accepted Foldweave release to public `main` without rebase or
      force-push.

### Documentation, claims, and media

- [x] Current Foldweave product case, journeys, technologies, claims, and judge
      paths are consolidated in this package.
- [x] Pre-existing and repository-evolution disclosure is current.
- [x] Direct API, ChatGPT billing, `store=false`, metadata disclosure, native
      signing, and public-listing qualifications are explicit.
- [x] Reconcile and independently review README, limitations, provenance,
      build log, package metadata, installation guide, plugin guide, and this
      package against the accepted product candidate and fresh clean-clone
      evidence.
- [x] Capture the genuine Foldweave screenshot set from the current release
      worktree and visually review it.
- [x] Regenerate the Foldweave thumbnail and record all current media hashes.
- [x] Confirm no stale active Name Atlas branding survives outside historical
      and compatibility contexts.
- [x] Confirm no secret, response ID, personal path, account identifier,
      notification, pairing secret, authorization code, or private callback
      appears in current public-facing release material. Historical evidence is
      retained only where provenance requires it.
- [ ] Confirm every screenshot, narration sentence, README claim, Devpost field,
      and video statement maps to accepted evidence.
- [ ] Confirm every third-party license and asset obligation.
- [ ] Confirm no unlicensed music or footage.
- [ ] Perform a real spoken narration timing and revise for comfortable pacing.
- [ ] Record the user's voice.
- [ ] Export a complete video strictly below 3:00 with intelligible audio.
- [ ] Watch the complete local video.
- [ ] Upload the video Public to YouTube.
- [ ] Watch the complete public playback and verify the URL.

### Devpost and user-owned actions

- [ ] Recheck official rules, FAQ, deadline, and current form immediately before
      submission.
- [ ] Replace predecessor Devpost identity and copy with the accepted Foldweave
      release only after release acceptance.
- [ ] Select **Work & Productivity**.
- [ ] Verify repository, judge, plugin, platform, and ChatGPT-state instructions
      against the final public clone.
- [ ] Add the verified public YouTube URL.
- [ ] User runs `/feedback` in the primary Codex task and supplies the exact
      Session ID.
- [ ] User confirms entrant type and country.
- [ ] User reads and personally confirms eligibility, ownership, representative
      authority where applicable, and every legal attestation.
- [ ] User reviews and approves the final project description in their own
      voice.
- [ ] User explicitly releases the submission hold only after every prerequisite
      passes.
- [ ] Only after release: perform final Devpost submission.
- [ ] Verify the submitted project page, repository, video, and testing
      instructions.
- [ ] Capture the final submission receipt or confirmation before Wednesday
      22 July 2026 at 02:00 CEST.

## Final stop rule

Creating, editing, committing, pushing, publishing, packaging, deploying,
rehearsing, capturing, or uploading this release does not release the
submission hold.

If every independently actionable product, release, media, due-diligence,
`/feedback`, and Devpost-draft requirement is complete while the hold remains
active, the correct phase is:

`WAITING_FOR_SUBMISSION_HOLD_RELEASE`

Final Devpost submission remains prohibited until the user explicitly releases
the hold. After release, submission is complete only when the final entry and
its receipt or confirmation have been independently verified.
