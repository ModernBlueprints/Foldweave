# Reversible Name Atlas — revised Build Week submission package

Status: **R7 DRAFT — RELEASE CANDIDATE, REHEARSAL, SCREENSHOTS, AND THUMBNAIL
COMPLETE; PUBLIC ALIGNMENT, VIDEO, USER ACTIONS, AND SUBMISSION PENDING**

Submission hold: **ACTIVE — DO NOT SUBMIT UNTIL THE USER EXPLICITLY RELEASES
THE HOLD**

This is the one working package for the revised demo, Devpost draft, screenshot
set, and final due-diligence pass. It is not a product specification or a claim
of final release readiness. Product truth and claim authority remain in
[`build/BUILD_SPEC.md`](build/BUILD_SPEC.md) and
[`LIMITATIONS.md`](LIMITATIONS.md).

## Official requirement snapshot

Rechecked Saturday 18 July 2026 against the
[Official Rules](https://openai.devpost.com/rules) and
[FAQ](https://openai.devpost.com/details/faqs):

- the submission period closes Wednesday 22 July 2026 at 02:00 CEST;
- the entry must be a working project built with Codex and GPT-5.6 and fit one
  selected track;
- the text must explain the project's features and functionality;
- the demonstration video must be public on YouTube, include a clear working
  demo with audio, cover what was built plus specific Codex and GPT-5.6 use,
  and remain under three minutes;
- the submission must provide a repository URL for judging and testing;
- the README must include setup, sample/testing guidance, specific Codex
  contributions, key decisions, and GPT-5.6 use;
- the primary Codex build task's `/feedback` Session ID is required; and
- the equally weighted judging criteria are Technological Implementation,
  Design, Potential Impact, and Quality of the Idea.

The official rules, not this package or any plugin, remain authoritative. The
user must personally confirm eligibility, entrant type, country, ownership,
representative authority when applicable, and every other personal attestation.

## Submission identity and pending release fields

| Field | Draft or status |
|---|---|
| Project | **Reversible Name Atlas** |
| Tagline | **Refactor the collection. Hand over the proof.** |
| Track | **Work & Productivity** |
| One-line summary | A local migration workbench that turns a risky change to a linked digital collection into a persistent human-reviewed case and a portable receipt another person can independently verify. |
| Public repository | <https://github.com/ModernBlueprints/reversible-name-atlas> |
| License | MIT |
| Current known-good public baseline | `827b0f6f93174d3c34aedfd98d8467a299ab2669`; revised release not yet promoted at this draft checkpoint |
| Accepted R6 product candidate | `eb54f3a2b3ab60bc690d3151e7f5bce0ad28aa0c` |
| Final revised release SHA | `[PENDING: fill only after the recording-ready release checkpoint is committed and public alignment passes]` |
| Final demo receipt fingerprint | `2ba5d8316f970d0a8f220a57fef1b7f77c167213146eeef2639284f251f0509a` |
| Final screenshot hashes | Recorded in the revised screenshot inventory below; recheck only after a deliberate recapture |
| Devpost thumbnail | `docs/submission-thumbnail.png` — 1500×1000 PNG, 3:2, 210,124 bytes, SHA-256 `1eee93fe81037843ca80453574d9f488a8aef97c0ad542ea615cfcd045a78ca0` |
| Public YouTube URL | `[USER ACTION REQUIRED: record/approve voice-over, upload as Public, and supply verified URL]` |
| `/feedback` Session ID | `[USER ACTION REQUIRED: run /feedback in the primary Codex build task and supply the generated ID]` |
| Entrant type and country | `[USER ACTION REQUIRED: confirm; do not infer]` |
| Eligibility and ownership attestations | `[USER ACTION REQUIRED: read and personally attest]` |
| Submission-hold release | `[USER ACTION REQUIRED: explicitly release only after product, video, due diligence, and form are complete]` |
| Devpost submission | **NOT PERFORMED** |

## Crisp product case

### The problem

A linked digital object is not one filename. Its identity can also appear in an
access derivative, a preservation derivative, a metadata row, a relationship
file, paths, and manifests. A bulk rename can produce a cleaner-looking tree
while leaving those declared relationships inconsistent. Even a mechanically
valid normalization can flatten language that carried meaning.

For the supported package contract, a preservation specialist therefore needs
more than a rename preview. They need a durable record of what was reviewed,
proof that the staged package matches those decisions, and a handoff that a
receiver can verify without trusting the sender's running application.

### The solution

Reversible Name Atlas is a loopback-only migration workbench for a digital-
preservation specialist or processing archivist preparing a linked collection
for preservation or repository ingest. It converts one risky structural change
into a complete bounded transaction:

`linked source → persistent Migration Case → mechanical proposals → bounded GPT evidence where needed → human decisions → copy-only BagIt handoff → Portable Change Receipt → independent receiver verification → bounded logical restore`

The application supports one strict package shape and one fixed repository-
ready profile. That deliberate boundary makes the proof inspectable: every
source member, declared relationship, proposal, human action, staged target,
map row, and committed artifact must agree or the complete handoff blocks.

### Why the revised version matters

The proof no longer ends inside Name Atlas. The completed bag contains an
immutable path-neutral receipt, exact original control files, a complete
decision ledger, forward and reverse maps, producer verification, and an
offline human-readable receipt. A separate receiver command requires no source,
Migration Case, browser, API key, GPT, or network. It recomputes the receipt
fingerprint, committed artifact digests, staged-data commitment, package graph,
decisions, paths, references, maps, deterministic findings, and BagIt result.

The sharp demonstration is a controlled counterfactual: alter one resolved
target in the decision ledger, rebuild the ordinary BagIt tag manifest, and
standard BagIt validation still passes. Name Atlas blocks because the altered
ledger no longer matches the immutable receipt commitment. This demonstrates
receipt-bound transaction consistency. It is not a signature, sender
authentication, or protection against someone who deliberately rewrites every
artifact and issues a new internally consistent receipt.

### Potential impact

For the initial user, the value is a reviewable change-control and handoff
boundary around a consequential but bounded collection migration. The sender
can stop treating a successful batch rename as proof. A receiver can inspect the
human decisions, verify the transferred bytes and declared relationships, and,
for this supported contract, reconstruct the original logical package into a
new destination.

The Build Week release demonstrates that exact transaction. It does not claim
measured time savings, practitioner prevalence, production readiness, semantic
correctness, institutional adoption, universal archive support, or universal
reversibility.

## How the product works

### 1. Persistent Migration Case

`demo` creates or resumes a strict `migration-case.v1`. The case preserves the
source snapshot, object families, proposals, evidence packet, exact card,
human decisions, resolved targets, lifecycle, handoff pointer, and receipt
fingerprint across process restart. Every mutation reloads and revalidates the
durable case. An added, removed, renamed, resized, or content-changed source
member makes the case stale, records the exact difference, and blocks decision,
staging, and receipt mutation.

### 2. Five-state human workbench

- **Atlas** shows exceptions first while keeping every family, relationship,
  before/after path, risk, and affected reference inspectable.
- **Decide** lets the human batch-approve routine proposals, mechanically edit
  collisions without GPT, and review one Meaning exception at a time.
- **Stage** shows readiness and performs one all-or-nothing copy-only
  transaction; the source stays untouched.
- **Verify** presents one truthful verdict across Source, Payloads, References,
  Paths, Decisions, Package, and Receipt.
- **Handoff** exposes the receipt fingerprint, offline receipt, keyless verifier
  command, receiver rerun, and bounded restore command.

The shell uses locally packaged Blueprint core `6.17.2` and Blueprint icons
`6.13.0` in a dark visual system. It is server-rendered FastAPI/Jinja and
requires no client-side JavaScript; it does not use React, Vite, a CDN, or a
Node judge path.

### 3. Deterministic mechanics, bounded GPT-5.6, human authority

Deterministic code owns import, stable identity, proposals, collisions,
reference checks, decision propagation, staging, receipts, and verification.
GPT-5.6 is called only for a mechanically flagged Meaning risk and only after
the user sees and requests the bounded outbound text. The included replay is an
exact sanitized record from one real `gpt-5.6` response, bound to its model,
schema, and complete evidence fingerprint. No second provider call was made for
the revised case, receipt, verifier, interface, or restore work.

The card can present possible interpretations, possible meaning loss,
uncertainty, evidence links, and one discriminating question. It cannot approve,
edit, resolve a collision, set a final target, verify, stage, or turn anything
green. The human supplies the only semantic action.

### 4. Portable receipt and receiver verification

The sender stages copies, rewrites only declared path fields, preserves exact
original control files as receipt-bound tag files, creates inverse maps and the
complete decision ledger, runs source-aware proof, validates BagIt, finalizes a
non-circular receipt, and runs the independent receiver verifier before
no-replace promotion. Portable artifacts contain relative POSIX paths, not the
sender's local source, case, checkout, temporary, or home paths.

The receiver runs:

`uv run name-atlas verify-receipt RECEIVED_BAG`

`VERIFIED <fingerprint>` means the received transaction is internally
consistent with its committed source description. Supplying `--source` adds a
comparison to that source. Source-free verification does not prove historical
source authenticity or sender identity.

### 5. Bounded logical restore

The admitted restore verifies the handoff first, refuses an existing
destination, reconstructs content through the reverse map, restores byte-exact
original declared controls, strictly reimports the pending package, proves every
in-scope path, size, and SHA-256 against the portable snapshot, and promotes
no-replace only after every check passes:

`uv run name-atlas restore-receipt RECEIVED_BAG RESTORE_DESTINATION`

The exact permitted claim is that it reconstructs every in-scope source-package
member byte-for-byte within the supported Name Atlas package contract. It does
not restore ACLs, ownership, timestamps, extended attributes, resource forks,
undeclared references, embedded links, or arbitrary filesystem state.

## Working evidence at this draft checkpoint

- 12 hero object families;
- 28 content objects and 30 source-package members;
- original, access, and preservation derivative propagation;
- one casefold collision resolved by a human descriptor edit;
- one `campaña` → `campana` Meaning review using the exact recorded GPT-5.6
  card and a human-owned action;
- 12 explicit human decisions, including one GPT-assisted review;
- 28 complete forward/reverse map rows;
- a persistent restart-safe case and exact source-staleness blockers;
- a 30-member receipt-bound BagIt handoff;
- source-free and exact-source receiver verification after copying the bag;
- the exact BagIt-valid altered-ledger failure blocked on
  `artifact_digest_mismatch:decision_ledger`;
- verify-first logical reconstruction of all 30 source members and 23,621 bytes
  in the R5 acceptance transaction, with source and handoff unchanged; and
- 265 tests plus lock, Ruff lint/format, isolated wheel, browser, and Git
  whitespace checks on exact candidate `eb54f3a`;
- a fresh detached Python 3.11 clean clone, installed 85-entry wheel, complete
  durable transaction, copied-bag verification, controlled failure, and
  30-member restore independently returned `GO`; and
- a complete R7 browser/terminal rehearsal produced selected receipt
  `2ba5d8316f970d0a8f220a57fef1b7f77c167213146eeef2639284f251f0509a`.

Public revised SHA and unauthenticated public-clone alignment remain pending.
The selected recording receipt is fixed above. No product code, feature, or
design work remains planned.

## Technology list

- Codex with GPT-5.6 as the primary development environment;
- GPT-5.6 through the OpenAI Responses API for the bounded runtime card;
- Python 3.11;
- FastAPI and Uvicorn;
- Jinja2 server-rendered HTML;
- Pydantic v2 strict external and serialized contracts;
- Blueprint core `6.17.2` compiled CSS and Blueprint icons `6.13.0`, packaged
  locally under Apache-2.0 attribution;
- Name Atlas CSS with no client-side JavaScript requirement;
- Library of Congress `bagit`;
- SHA-256 and standard-library filesystem primitives;
- `uv` and a committed lockfile;
- pytest and Ruff; and
- Git and GitHub.

## Exact judge path

Prerequisites: macOS, Python 3.11, and `uv`. macOS is the tested Build Week judge
platform; Linux and Windows are not release-test claims.

From the repository root:

1. `uv sync --frozen`
2. `uv run name-atlas demo --mode replay`
3. Open <http://127.0.0.1:8000>

Replay is the stable keyless path. It uses the included synthetic hero package
and visibly labels the exact evidence-bound record **Recorded GPT-5.6
response**. It makes no API request. The application reports its case path in
the terminal and resumes that case on restart.

After producing a handoff from Stage, copy its path from Handoff and run:

- `uv run name-atlas verify-receipt RECEIVED_BAG`
- `uv run name-atlas verify-receipt RECEIVED_BAG --source sample_data/hero`
- `uv run name-atlas restore-receipt RECEIVED_BAG RESTORE_DESTINATION`

`RESTORE_DESTINATION` must not already exist.

Project checks:

- `uv run pytest`
- `uv run ruff check .`
- `uv run ruff format --check .`

Optional live startup:

- configure `OPENAI_API_KEY` only in the launching environment; then
- run `uv run name-atlas demo --mode live`.

Live mode uses exact `gpt-5.6`, substitutes no fallback, and still makes no
request until the user presses Generate on the Meaning item. Judges do not need
a key to run the complete recorded-replay transaction or either receiver
command.

## Devpost description draft

### Inspiration

A preservation migration can look successful because every renamed file exists,
while its metadata, derivatives, decision history, or receiver handoff no longer
agree. We wanted to treat the change as a reviewable transaction rather than a
batch command—and to make the proof survive after the sender closes the app.

### What it does

Reversible Name Atlas turns one strict linked digital collection into a
persistent, human-reviewed Migration Case. It previews identifier-based path
changes, keeps originals and derivatives together, exposes collisions and
possible meaning loss, and blocks the whole package until each required human
decision and deterministic invariant is complete.

It then creates a copy-only BagIt handoff with an immutable Portable Change
Receipt, exact original controls, complete decision provenance, two-way path
maps, and producer proof. A separate keyless receiver command verifies the bag
without the sender's source, case, browser, network, GPT, or API key. A bounded
restore can reconstruct every in-scope source member into a new destination.

### How we built it

The application is Python 3.11 with FastAPI, Jinja2, Pydantic v2, the official
OpenAI SDK, Library of Congress `bagit`, and locally packaged Blueprint assets.
The five-state interface is server-rendered; deterministic and human authority
never moves into browser JavaScript.

The Migration Case uses strict versioned records, atomic replace, `fsync`, a
process lock, optimistic revision matching, and exact source rehydration. The
receipt uses an acyclic canonical hash domain, raw artifact commitments, and a
complete staged-data commitment. The independent verifier strictly parses and
recomputes the transaction instead of trusting the sender's UI report.

### How GPT-5.6 is used

Deterministic mechanics first identify a Meaning risk. After the user inspects
and explicitly sends a bounded evidence packet, GPT-5.6 returns a structured
neutral card containing possible interpretations, possible meaning loss,
uncertainty, evidence links, and one discriminating question. The model cannot
approve, select a path, verify, or stage.

The repository includes one sanitized record from a real `gpt-5.6` response to
the exact hero evidence. Replay validates the model, schema, and complete
evidence fingerprint, is visibly labeled, and requires no API key. No new model
call was needed for the portable-handoff revision.

### How Codex was used

Codex with GPT-5.6 was the primary development environment and integrator. In
one primary task it translated frozen product contracts into vertical slices,
kept the application runnable, integrated bounded parallel reviews, exercised
the browser and CLI, reproduced adversarial proof failures, and converted valid
failures into regression tests.

The key decisions made explicit through that collaboration were one strict
package contract instead of a generic adapter platform; a persistent local case
as workflow authority; an immutable receipt as the handoff boundary; GPT as
advisory and the human as semantic authority; a source-free receiver verifier;
and verify-first no-overwrite restore. The dated chronology and commit evidence
are in `docs/CODEX_BUILD_LOG.md`.

### Challenges and accomplishments

The hardest problem was preventing a plausible green result. We had to separate
four authorities: the local mutable case, the complete decision ledger, the
producer verification report, and the immutable receipt. We also had to remove
receipt self-reference, keep sender-local paths out of portable artifacts,
verify a copied bag without sender state, and make restore safe against partial
promotion and path races.

The clearest accomplishment is the controlled failure: after altering the
decision ledger and rebuilding the BagIt tag manifest, ordinary BagIt still
passes, but Name Atlas identifies the exact receipt-commitment mismatch. That is
the difference between validating transferred bytes and verifying this declared
change transaction.

### What we learned

AI authority should shrink as a claim becomes more consequential. GPT-5.6 is
useful for organizing bounded ambiguity into a precise human question. It is
not the right authority for approval or proof. Human judgment and deterministic
verification complement each other only when their roles remain explicit in
the product and artifacts.

### What's next

After Build Week, the honest next work is practitioner testing, measured
workflow studies, scale characterization, and evidence-based selection of any
additional package adapter. Direct repository integration, generic policy
builders, signatures, collaboration, and AI-training-data adapters are not part
of this release.

## Devpost field draft

| Field | Draft value |
|---|---|
| Project name | `Reversible Name Atlas` |
| Tagline | `Refactor the collection. Hand over the proof.` |
| Category | `Work & Productivity` |
| Repository | `https://github.com/ModernBlueprints/reversible-name-atlas` — confirm it resolves to the selected revised release before submission |
| Thumbnail | `docs/submission-thumbnail.png` — upload the exact hash recorded above |
| Technologies | `Codex, GPT-5.6, OpenAI Responses API, Python 3.11, FastAPI, Jinja2, Pydantic v2, Blueprint, BagIt, uv, pytest, Ruff, CSS, GitHub` |
| Testing instructions | `On macOS with Python 3.11 and uv: run uv sync --frozen, then uv run name-atlas demo --mode replay and open http://127.0.0.1:8000. The included hero data and recorded GPT-5.6 card need no API key. Run uv run pytest for the full suite. After staging, use the copyable verify-receipt and restore-receipt commands on the Handoff page.` |
| Video URL | `[USER ACTION REQUIRED: PUBLIC YOUTUBE URL]` |
| `/feedback` Session ID | `[USER ACTION REQUIRED]` |
| Submitter type | `[USER CONFIRM: Individual / Team of Individuals / Organization]` |
| Country | `[USER CONFIRM; do not infer]` |
| Plugin/developer-tool fields | `Not applicable — Work & Productivity standalone local browser application.` |
| Final release SHA | `[PENDING PUBLIC ALIGNMENT]` |
| Submission hold | `ACTIVE — final submit prohibited until explicit user release` |

## Three-minute demo storyboard

Target exported duration: **2:43–2:45**, leaving at least 15 seconds below the
three-minute limit. Do not accelerate unreadable UI footage to hit the target.

| Time | Visual and action | Narration purpose |
|---:|---|---|
| 0:00–0:08 | Title, linked original/derivative/metadata montage, then Atlas | One identity spans multiple declared records; a rename is a transaction. |
| 0:08–0:22 | Atlas exception-first summary; 12 families, 28 objects, Collision and Meaning signals | Complete change and relationships are visible before copying. |
| 0:22–0:37 | Decide: batch routine families; edit the casefold collision mechanically | Human action is explicit; deterministic problems do not call GPT. |
| 0:37–1:02 | Meaning evidence packet, visibly labeled recorded GPT-5.6 card, human enters `campaign-poster` | GPT frames bounded ambiguity; the human selects the outcome. |
| 1:02–1:14 | Stage readiness and **Stage copies and verify handoff** | One copy-only, all-or-nothing transaction; source untouched. |
| 1:14–1:29 | Verify: seven green groups and receipt fingerprint | Deterministic source-to-receipt verdict. |
| 1:29–1:44 | Handoff: offline receipt, copyable verifier, restore command | Proof becomes a receiver artifact, not a sender-screen opinion. |
| 1:44–1:54 | Open offline receipt after copying the bag to an unrelated path | Human-readable handoff remains inspectable without the app. |
| 1:54–2:06 | Terminal: keyless `verify-receipt` prints `VERIFIED <fingerprint>` | Independent verification needs no source, case, browser, network, GPT, or key. |
| 2:06–2:18 | Controlled copy: show BagIt pass, then Name Atlas `BLOCKED artifact_digest_mismatch:decision_ledger` | Standard package validation passes; the receipt detects inconsistent decision provenance. |
| 2:18–2:25 | Terminal: successful bounded restore summary or Handoff restore command plus verified report | Supported original logical package can be reconstructed into an absent destination. |
| 2:25–2:43 | Concise commit/test overlay, product end card, repository URL | Specific Codex workflow, 265-test checkpoint, closing value proposition. |
| 2:43–2:45 | Silent two-second end card | Leave a clean visual landing frame. |

R7 visual rehearsal status: **PASS**. The complete application sequence was
rehearsed at a 1280×720 capture viewport with the specified shot holds and no
horizontal overflow. The selected receipt, copied-bag verifier, controlled
failure, and restore commands were then rerun from the exact candidate. The
visual schedule totals 2:45. This is timing evidence for the shot plan, not a
substitute for the user's final narrated recording.

## Timed English voice-over draft

Target: **2:35–2:45** with natural pauses. The final recording must be timed
against the selected visuals; do not assume a words-per-minute estimate is
proof of duration.

> One collection identity can span an original, derivatives, metadata,
> relationship files, and manifests. Rename only one path, and a cleaner-looking
> collection can become inconsistent.
>
> Reversible Name Atlas turns that risk into a persistent, human-reviewed
> Migration Case and a portable receipt another person can verify.
>
> Atlas shows twelve families, twenty-eight content objects, proposals, and
> links before copying. Routine families need explicit batch approval. This
> collision is mechanical, so GPT is skipped; I edit its descriptor and the
> family map updates.
>
> The final exception is campaña becoming campana. Removing the Spanish ñ
> may change meaning. Name Atlas first shows the bounded outbound packet: exact
> paths, transformation trace, metadata, derivative links, candidates, and
> evidence IDs. No payload bytes or approval fields leave the app.
>
> This recorded GPT-5.6 response is visibly labeled and bound to the exact
> evidence fingerprint. It presents interpretations, uncertainty, and one
> discriminating question. It cannot approve, verify, or choose a path. I enter
> campaign-poster; the human action is stored with the evidence and card.
>
> The case survives restart and blocks if the source changes. With every family
> resolved, Name Atlas stages copies, rewrites only declared path fields,
> preserves the source, and creates a BagIt handoff.
>
> Verify turns green only after source, payload, reference, path, decision,
> package, and receipt checks pass. The handoff includes original controls,
> two-way maps, complete decision provenance, a machine receipt, and this
> offline view.
>
> After copying the bag, the receiver runs one keyless command. It needs no
> source, case, browser, network, GPT, or API key. It recomputes the transaction
> and returns the same receipt fingerprint.
>
> Now the counterfactual: I alter one resolved target and rebuild the BagIt tag
> manifest. BagIt still passes. Name Atlas blocks because the changed decision
> ledger no longer matches the receipt. A verified restore can also reconstruct
> every in-scope source member into a new destination.
>
> Codex with GPT-5.6 was the primary development environment. One main task
> turned frozen contracts into vertical slices, parallelized bounded reviews,
> reproduced proof failures, and made them two hundred sixty-five passing tests.
> Runtime GPT-5.6 only frames one ambiguity; authority stays human, and proof
> stays deterministic.
>
> Reversible Name Atlas. Refactor the collection. Hand over the proof.

### Voice-over ownership and acceptance

- Final narrator/voice recording: `[USER ACTION REQUIRED]`
- Final recorded duration: `[PENDING; must be 2:35–2:45 target and video must be under 3:00]`
- Audio intelligibility check: `[PENDING]`
- Spoken claims checked against the selected release: `[PENDING]`
- User approval of final audio: `[PENDING]`

## Capture shot list

1. Use a neutral recording workspace and the final release checkout. No personal
   paths, browser notifications, account identifiers, secrets, or private tabs.
2. Record the browser at 1920×1080 or 2560×1440 and export 1920×1080. Use the
   visually verified desktop width and a zoom level readable at normal YouTube
   playback.
3. Use replay mode. Show **Recorded GPT-5.6 response** and the model contract.
   Do not make another provider request for the recording.
4. Use one fresh hero Migration Case for the narrated transaction. Rehearse the
   exact batch approval, collision edit, Meaning card, human edit, Stage,
   Verify, and Handoff sequence before capture.
5. Prepare the copied successful handoff, controlled altered-ledger copy, and
   absent restore destination in a neutral temporary path before recording.
6. Capture terminal commands at a readable font size with no shell history or
   unrelated filesystem output. Show exact command/result pairs, not a
   prewritten imitation.
7. Show the offline receipt from the copied bag. Make clear that it is a derived
   human view and that the machine receipt/artifact commitments are authority.
8. Use a concise Codex/commit/test overlay during the final narration. The FAQ
   does not require the Codex interface on screen, but the narration must name
   concrete contributions.
9. Use no copyrighted music or third-party footage. Blueprint is part of the
   licensed product UI, not external promotional footage; retain its notices in
   the repository.
10. Export under three minutes, watch the complete local file with audio, upload
    it as Public on YouTube, then watch the complete public playback before
    adding its URL to Devpost.

## Revised screenshot inventory and specification

The first-cycle screenshots were replaced by the exact revised set below. Each
capture was produced from synthetic data under a neutral temporary path and
inspected at the stated 1440×900 recording viewport; the Handoff frame is
deliberately scrolled so its receiver commands remain visible.

| Path | Required frame | Acceptance criteria | Status |
|---|---|---|---|
| `docs/screenshots/01-atlas.png` | Atlas exception-first overview | Case identity, source commitment, family/object counts, Collision and Meaning signals, and before/after relationship context readable; no personal path | `PASS — SHA-256 4bf00ff8dbdfaf9c3a23c5741d105d582ac3afe88a48ee3a7846b1d97f86699b` |
| `docs/screenshots/02-decide.png` | Meaning decision | Bounded evidence, **Recorded GPT-5.6 response**, neutral card, and separate human-authority action all visible; no model-approval implication | `PASS — SHA-256 b256618090e4b8b69bda2c3f1d9a7102a1166cd3ce895a127dbba8817230fa8e` |
| `docs/screenshots/03-stage.png` | Ready-to-stage transaction | Source untouched, neutral temporary source/destination, resolved count, and one copy-and-verify action readable | `PASS — SHA-256 85ef920b8b880b0b053114f86eea25d2a5ba721df53dc5605569a613f3da96a0` |
| `docs/screenshots/04-verify.png` | Verified handoff | Fresh receiver verdict, all seven green proof groups, and receipt fingerprint readable | `PASS — SHA-256 3519348d70ed78451abad5db39caa0467ef35071413c2474ed82b245e2e437d8` |
| `docs/screenshots/05-handoff.png` | Receiver handoff | Offline receipt action, keyless verifier and restore commands, current receiver verdict, dependencies, and fingerprint readable | `PASS — SHA-256 379ac8e5516d77902e13a6a5da4af4f03b733f5176306050bdb26bdfff79c905` |
| `docs/screenshots/06-offline-receipt.png` | Copied bag's offline receipt | Receipt identity, source/staged commitments, counts, producer BagIt pass, and non-authoritative label readable outside the app | `PASS — SHA-256 315631397d3c2d332e3397f65591389ced2ff91be0163871d21c577045374b3a` |
| `docs/screenshots/07-negative-block.png` | Controlled receipt inconsistency | Exact Name Atlas `artifact_digest_mismatch:decision_ledger` blocker shown against a disposable altered handoff; the separately executed command evidence establishes ordinary BagIt pass | `PASS — SHA-256 abff85e54f475befdce275c92bea5c517d93f1f006744aaf3cb2214b871bc683` |

All final captures must use synthetic fixture data, avoid secrets and sender-
local personal paths, preserve truthful status colors, contain no clipping or
horizontal document overflow, and match the selected release behavior.

### Devpost gallery thumbnail

Use [`submission-thumbnail.png`](submission-thumbnail.png), a code-native
1500×1000 PNG in the established dark visual system. It is 3:2, 210,124 bytes,
and has SHA-256
`1eee93fe81037843ca80453574d9f488a8aef97c0ad542ea615cfcd045a78ca0`.
The editable vector source is
[`submission-thumbnail.svg`](submission-thumbnail.svg), SHA-256
`91e1f7eff0159df6417913d3493a330ffef718857839b12e928a9cf8df1b4836`.
It contains only project-native text and vector shapes; no generated or
third-party promotional imagery is embedded. The visible `2ba5…f0509a`
fragment is the actual selected recording receipt, not illustrative evidence.

## Limitations and claim boundaries for public copy

The public description and video may say that the verified release:

- persists a human-reviewed Migration Case across restart;
- binds GPT evidence, the exact card presented, and the human's explicit action
  in the complete decision ledger;
- creates a copy-only BagIt handoff with a path-neutral Portable Change Receipt;
- independently verifies a copied receipt without source, case, browser,
  network, GPT, or API key;
- detects the exact BagIt-valid but receipt-inconsistent altered-ledger copy; and
- reconstructs every in-scope source-package member byte-for-byte within the
  supported Name Atlas package contract.

Do not claim:

- measured or percentage time savings, recurring speed, or practitioner
  prevalence;
- semantic correctness, AI safety verification, or that GPT chose the correct
  name;
- sender identity, human authorship, institutional authorization, signatures,
  or cryptographic authentication;
- historical-source authenticity from source-free verification;
- compliance, production readiness, or downstream repository acceptance;
- preservation or restoration of ACLs, ownership, timestamps, extended
  attributes, resource forks, undeclared links, embedded links, or arbitrary
  filesystem state;
- universal archival-workflow support, arbitrary schemas, universal safety, or
  universal reversibility;
- Archivematica certification, compatibility, or live integration;
- AI-training-data readiness, institutional adoption, proven superiority over
  ordinary Codex, absence of competitors, or a proven probability of winning.

## Claim-to-evidence audit

| Public claim | Required evidence before use | Draft status |
|---|---|---|
| Persistent restart-safe case | Restart test and exact case/card/decision rehydration | Verified at R2 and in the 265-test R6 suite |
| Source change blocks | Added/removed/renamed/resized/content-changed matrix and UI blocker | Verified at R2 and in the 265-test R6 suite |
| Portable path-neutral receipt | Artifact schema/path scan, fingerprint, raw digest and staged-data recomputation | Verified at R3 and in the R6 candidate path scan |
| Independent keyless verification | Copied-bag subprocess with API key absent and bag byte snapshot | Verified at R3/R5 and twice from exact detached `eb54f3a` clean clones |
| BagIt-valid altered ledger blocks | BagIt pass plus exit `1` and exact `artifact_digest_mismatch:decision_ledger` | Verified at R1/R3 and reverified in R6; final screenshot records the exact Name Atlas blocker |
| Five-state coherent experience | Route/guard matrix and browser QA at recording and narrow widths | Verified at R4/R5 and final R6 screenshot/narrow QA |
| Bounded restore | Verify-first unmocked restore, exact 30-member snapshot equality, no overwrite, source/handoff unchanged | Verified at R5 and twice from exact detached `eb54f3a` clean clones |
| Real GPT-5.6 card | Canonical record SHA, evidence fingerprint, usage, and live/replay build evidence | Verified; no new call made or needed |
| 265 passing tests | Fresh R6 release-hardening full-suite output | Verified by the primary integrator after the final path-selection correction |
| Final public release | Selected SHA, clean branch, public alignment, unauthenticated clone | `[PENDING PUBLIC ALIGNMENT]` |
| Final video and submission | Public playback, `/feedback`, personal attestations, explicit hold release, Devpost receipt | `[USER ACTIONS AND FINAL CLOSURE PENDING]` |

## Due-diligence checklist

### Product and repository

- [ ] Recording-ready release SHA selected and recorded above
- [ ] Revision fast-forward promoted only after release acceptance
- [ ] Public repository resolves to the selected SHA
- [ ] Public repository is MIT-licensed and third-party notices are present
- [x] `uv sync --frozen` passes in an exact detached clean clone
- [x] Complete keyless hero replay passes from that clean clone
- [x] Copied-bag `verify-receipt` passes from that clean clone
- [x] Admitted `restore-receipt` passes from that clean clone
- [x] Final pytest, Ruff lint, Ruff format, build, wheel, link, secret,
      absolute-path, license/asset, and Git-clean checks pass
- [x] Replay label/model/evidence fingerprint remain exact
- [x] Live startup remains truthful without making an unnecessary provider call
- [x] README, limitations, provenance, build log, and sample-data guidance match
      the selected release

### Claims, media, and intellectual property

- [ ] Every sentence in the final video and Devpost description maps to the
      claim-to-evidence table or is removed
- [ ] No personal path, credential, account identifier, private notification,
      or unrelated content appears in screenshots or video
- [ ] Synthetic fixture provenance remains documented
- [ ] Blueprint and all other third-party licenses/notices remain included
- [ ] No unlicensed music, third-party footage, or unsupported trademark use
- [x] All seven revised screenshots pass final visual QA and their hashes are
      recorded
- [x] Final 3:2 project-gallery thumbnail is rendered, visually inspected, and
      hash-recorded
- [ ] Final narration matches the selected product and is approved by the user
- [ ] Final video duration is strictly under 3:00
- [ ] Final video has intelligible English audio covering the product, concrete
      Codex work, and runtime GPT-5.6 role
- [ ] Final video is Public on YouTube and complete public playback is verified

### Devpost and user-owned attestations

- [ ] User confirms entrant type
- [ ] User confirms country of residence and eligibility
- [ ] User confirms ownership, representative authority when applicable, and
      all personal/legal attestations after reading the form and rules
- [ ] Work & Productivity is selected
- [ ] Repository URL and testing instructions are exact
- [ ] Public YouTube URL is added
- [ ] User runs `/feedback` in the primary build task and adds the exact Session
      ID
- [ ] Project description, technologies, screenshots, thumbnail, and required
      custom fields are complete
- [ ] Due date is reconfirmed against the official rules immediately before
      submission
- [ ] User explicitly releases the active submission hold
- [ ] Only after release: final Devpost submission is performed
- [ ] Submitted project page, repository, and video resolve correctly
- [ ] Devpost submission/receipt confirmation is captured before Wednesday
      22 July 2026 at 02:00 CEST

## Final stop rule

Preparing or committing this draft does not authorize submission. If every
independent product and media requirement is complete while the submission hold
remains active, the correct state is
`WAITING_FOR_SUBMISSION_HOLD_RELEASE`. Final Devpost submission remains
prohibited until the user explicitly releases that hold.
