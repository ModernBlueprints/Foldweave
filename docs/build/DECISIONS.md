# Reversible Name Atlas — Material Decisions

Status: **HISTORICAL RATIONALE ONLY**

This is an append-only-in-substance record of why material choices or deviations
occurred. It is not an active specification, plan, goal, or checkpoint. Current
truth must be written in `BUILD_SPEC.md` or `IMPLEMENTATION_PLAN.md`; current
facts must be verified and summarized in `STATE.md`. A record here never
overrides those artifacts.

## D-001 — Broader linked-collection migration

- Date: 17 July 2026
- Decision: Position the product around verified migration of linked collection
  identities, not transliteration.
- Rationale: Renames affect files, metadata, derivatives, paths, and manifests.
  Transliteration demonstrates one important ambiguity but does not express the
  complete user transaction.
- Active authority: `PRD-001`–`PRD-003`.

## D-002 — Standalone local browser interface

- Date: 17 July 2026
- Decision: Use a loopback-only standalone browser application; exclude a Codex
  plugin and MCP server.
- Rationale: The complete Atlas, Decisions, and Proof workflow needs a persistent
  visual state, and the official requirement is meaningful Codex use in building
  the project rather than a mandatory Codex runtime.
- Active authority: `PRD-004` and `UX-001`–`UX-004`.

## D-003 — Whole-package fail-closed export

- Date: 17 July 2026
- Decision: Any unsupported input, blocker, refused proposal, or unresolved
  required decision blocks the complete selected package.
- Rationale: A partial stage could sever declared identity relationships while
  appearing complete.
- Active authority: `IO-005`, `TX-006`, and `TX-008`.

## D-004 — One hero and one tiny negative fixture

- Date: 17 July 2026
- Decision: Build one polished synthetic hero package and one minimal blocking
  fixture, not multiple polished collections.
- Rationale: One complete judge-facing transaction is higher value within the
  schedule than several shallow demonstrations.
- Active authority: `UX-005`.

## D-005 — `path_plan.csv` excluded

- Date: 17 July 2026
- Decision: Exclude `path_plan.csv` from the MVP, required tests, hero flow, and
  video.
- Rationale: The fixed repository-ready profile already demonstrates canonical
  renaming and structural moves. A future adapter remains possible through
  `PathProposal` without consuming Build Week scope.
- Active authority: `IO-004` and `TX-004`.

## D-006 — Governance repository before activation

- Date: 17 July 2026
- Decision: Initialize the fresh repository and commit only the operating
  scaffold before activating product work.
- Rationale: This creates one canonical home for governance artifacts without
  starting H+0, dependencies, code, API use, or publication.
- Active authority: the user-approved meta-implementation plan and `GOAL.md`.

## D-007 — Absolute 80/24 timing model

- Date: 17 July 2026
- Decision: Protect Tuesday 21 July 2026 at 02:00 CEST as recording-ready and
  Wednesday 22 July 2026 at 02:00 CEST as submission-confirmed.
- Rationale: A full 80-hour product period plus 24-hour submission reserve fits
  only if activation occurs by Friday 17 July 2026 at 18:00 CEST. Later
  activation compresses targets and optional scope, not required outcomes or the
  final reserve.
- Active authority: `IMPLEMENTATION_PLAN.md` timing model.

## D-008 — Fixed identifier and profile

- Date: 17 July 2026
- Decision: Require one unique NFC `dc.identifier` per family and use it as the
  canonical target prefix with the original stem-derived descriptor and role.
- Rationale: This closes the identity source and transformation algorithm so the
  hero transaction, collision checks, and proof are implementable.
- Active authority: `IO-002` and `TX-002`–`TX-005`.

## D-009 — Selective spike adaptation

- Date: 17 July 2026
- Decision: Treat the earlier spike as a catalog of mechanical behaviors and
  focused scenarios, not as the new application's foundation.
- Rationale: Its snapshot, path, mapping, and transaction lessons are useful,
  while its monolithic transaction, raw-path bundle, semantic executable, and
  tournament evaluator are incompatible with the product.
- Active authority: `docs/PREEXISTING_WORK.md`.

## D-010 — Earlier enormous goal superseded

- Date: 17 July 2026
- Decision: The earlier comprehensive project-discovery/execution `/goal` is
  superseded and inactive. Only the concise committed `GOAL.md` may be activated.
- Rationale: Product truth, delivery sequence, authority, and current state need
  separate owners to prevent contradictions and validation-harness recursion.
- Active authority: `GOAL.md` after explicit activation.

## D-011 — Root-commit baseline locator

- Date: 17 July 2026
- Decision: Identify the governance baseline inside committed artifacts as the
  unique root commit on branch `main` with subject
  `chore: establish build operating scaffold`. Report its exact SHA-1 in the
  handoff and resolve it from Git after activation.
- Rationale: A commit cannot contain its own hash: inserting that hash changes
  the commit. This corrects the accepted plan's self-referential requirement
  while preserving exactly one scaffold commit and an unambiguous immutable
  baseline.
- Active authority: `GOAL.md` and fresh Git history.

## D-012 — User-authorized in-place revision

- Date: 18 July 2026
- Decision: Amend the five existing governance authorities in place instead of
  creating a V2 scaffold.
- Rationale: One authority owner per question preserves continuity and prevents
  competing plans or goals.
- Active authority: the revised frozen specification, sole plan, and sole goal.

## D-013 — Known-good fallback and revision branch

- Date: 18 July 2026
- Decision: Preserve `827b0f6` on local and remote `main`; create only
  `revision/portable-change-receipt`, commit the governance revision locally,
  and do not push during the meta-stage.
- Rationale: The working public first-cycle release remains an immutable fallback
  while the revised cycle is unstarted.
- Active authority: `GOAL.md`, Git state, and the scaffold handoff.

## D-014 — Bounded feature-freeze reopening

- Date: 18 July 2026
- Decision: Reopen the first-cycle feature freeze only for the approved
  persistent-case, receipt, verifier, five-state UI, Blueprint, and conditional
  restore scope.
- Rationale: The prior release remains evidence, but its handoff proof ends
  inside the producer application.
- Active authority: `BUILD_SPEC.md` and the R1–R7 plan.

## D-015 — Migration Case as sole mutable authority

- Date: 18 July 2026
- Decision: Use one strict atomic `migration-case.v1` aggregate; any
  `WorkflowSession` becomes a façade rather than a second source of truth.
- Rationale: Cards, human actions, targets, and stage state must survive restart
  without diverging authorities.
- Active authority: `CASE-001`–`CASE-005`.

## D-016 — Changed source means stale case and fresh case

- Date: 18 July 2026
- Decision: Any source-member change makes the case stale and blocks mutation or
  staging; recovery is a preserved old case plus a different explicit new case.
- Rationale: Automatic reconciliation would make decision provenance ambiguous.
- Active authority: `CASE-004`.

## D-017 — Local case versus portable receipt

- Date: 18 July 2026
- Decision: Keep operational absolute paths only in the mutable local case;
  publish an immutable path-neutral receipt inside the completed bag.
- Rationale: Receiver verification must survive moving the handoff to an
  unrelated machine or absolute directory.
- Active authority: `PRD-006`, `CASE-001`, and `VER-005`.

## D-018 — Original control preservation

- Date: 18 July 2026
- Decision: Export byte-exact original declared controls as receipt-bound BagIt
  tag files alongside the path-neutral source representation.
- Rationale: A receiver needs the original declared references to verify the
  bounded transformation and enable any admitted logical restore.
- Active authority: `VER-005`.

## D-019 — Acyclic receipt envelope

- Date: 18 July 2026
- Decision: Hash canonical `ReceiptCore` bytes in an envelope whose fingerprint
  is outside its own domain; exclude receipt, HTML, and tag manifest from core
  artifact commitments and protect them through the final tag manifest.
- Rationale: This removes receipt and manifest self-reference while retaining
  exact byte commitments.
- Active authority: `VER-006`.

## D-020 — Independent verification and bounded claim

- Date: 18 July 2026
- Decision: Require a read-only, keyless, networkless source-free receiver
  verifier; optional `--source` adds comparison but is not required for internal
  consistency proof.
- Rationale: The handoff must carry proof another person can rerun without the
  producer's case or session. It does not authenticate sender identity or
  historical source truth.
- Active authority: `VER-007` and `CLAIM-003`.

## D-021 — Exact BagIt-valid altered-ledger demonstration

- Date: 18 July 2026
- Decision: Alter one syntactically valid resolved target in a disposable
  decision ledger, rebuild the ordinary tag manifest, retain the original
  receipt, and require BagIt pass plus Name Atlas digest blocker.
- Rationale: This demonstrates the additional transaction-consistency proof
  without pretending it is a signature.
- Active authority: `VER-008`.

## D-022 — Five-state server-rendered workbench

- Date: 18 July 2026
- Decision: Use Atlas, Decide, Stage, Verify, and Handoff routes with
  server-computed next-state routing and server-side transition authority.
- Rationale: Separating review, action, proof, and receiver handoff makes the
  transaction legible without adding a client application framework.
- Active authority: `UX-006` and `UX-007`.

## D-023 — Locally packaged Blueprint visual layer

- Date: 18 July 2026
- Decision: Vendor Blueprint core `6.17.2`, icons `6.13.0`, selected assets, and
  Apache-2.0 notice; use no React, Vite, CDN, Node runtime, or Node judge step.
- Rationale: Blueprint supplies a coherent dark visual vocabulary while the
  existing FastAPI/Jinja architecture retains authority and a uv-only judge path.
- Active authority: `UX-008`.

## D-024 — Conditional logical restore

- Date: 18 July 2026
- Decision: Decide restore once at R4/R+52; admit it only after all core gates
  pass and at least 18 real hours remain, otherwise record
  `CUT_BY_PREAUTHORIZED_GATE` and omit every restore surface and claim.
- Rationale: Restore has real value only after portable proof is complete and
  must not endanger the required release.
- Active authority: `REL-006` and the restore gate in the sole plan.

## D-025 — Reuse inherited GPT evidence

- Date: 18 July 2026
- Decision: Reuse the validated first-cycle GPT-5.6 record while its evidence,
  model, schema, and hero Meaning case remain exact; do not call again merely for
  persistence or receipt binding.
- Rationale: The revision changes durable provenance and handoff proof, not the
  validated model judgment surface.
- Active authority: `AI-007` and `GOAL.md` after activation.

## D-026 — Approved exclusions remain hard

- Date: 18 July 2026
- Decision: Exclude executable cases, reconciliation, NER/ReFinED,
  AI-training-data and generic adapters, signatures/authentication,
  collaboration, React/Vite, and direct repository integrations.
- Rationale: These are separate products or infrastructure expansions and do
  not strengthen the frozen three-minute transaction enough to justify risk.
- Active authority: `BUILD_SPEC.md` explicit exclusions.

## D-027 — Explicit revised-goal activation

- Date: 18 July 2026
- Decision: Preserve historical H+0 and start R+0 only when the user explicitly
  activates the complete amended sole goal in this primary task.
- Rationale: Meta-plan acceptance, file creation, and governance commit do not
  authorize revised product execution.
- Active authority: `GOAL.md`.

## D-028 — Final submission hold

- Date: 18 July 2026
- Decision: Permit draft and release preparation after goal activation but
  prohibit final Devpost submission until the user explicitly releases the hold.
- Rationale: The revised product, video, due diligence, and submission package
  must be complete before the irreversible submission step.
- Active authority: `GOAL.md`, the sole plan, and current `STATE.md`.

## D-029 — Revised goal activated and targets fixed

- Date: 18 July 2026
- Decision: Activate the complete amended production goal at Saturday 18 July
  2026 at 00:51:51 CEST, preserve historical H+0, and calculate the revised
  milestone targets from the plan's 69-hour 8-minute 9-second product window.
- Rationale: The governance baseline, branch, locked dependencies, 116 inherited
  tests, Ruff checks, and Git whitespace check all passed before R1 began.
- Active authority: activated `GOAL.md`, the sole implementation plan, and
  current `STATE.md`.

## D-030 — Finalized handoff remains historical and immutable

- Date: 18 July 2026
- Decision: Apply mandatory source-staleness mutation only before
  `handoff_ready`; after finalization, later sender-source drift cannot rewrite
  the case or receipt and may be assessed only as a separate current-source
  comparison.
- Rationale: A finalized receipt must remain an immutable record of the proved
  transaction. Retroactively converting it to a mutable stale case would
  contradict the read-only lifecycle and destroy stable handoff provenance.
- Active authority: `CASE-002`, corrected `CASE-004`, and `VER-007 --source`.

## D-031 — Conditional restore admitted once

- Date: 18 July 2026
- Decision: Record the one-time restore gate as `GO` at Saturday 18 July 2026 at
  04:19:07 CEST. The `restore-receipt` command is now mandatory; its Handoff UI
  remains independently cuttable.
- Rationale: Case restart, receipt JSON/HTML, positive and exact controlled-
  negative receiver verification, all five routes, the 241-test final R4 tree,
  and the independent cross-artifact audit all pass, with 69 hours 40 minutes
  52 seconds remaining before recording readiness—well above the required 18
  hours.
- Active authority: `REL-006`, the sole implementation plan's recorded restore
  gate, and current `STATE.md`.

## D-032 — User-authorized AI-first in-place revision

- Date: 18 July 2026
- Decision: Supersede the archive-first release as the future product direction
  by amending the same five governance authorities in place.
- Rationale: The user requires a broader, automatic, AI-first product while one
  source of truth per governance question prevents competing scaffolds.
- Active authority: the frozen third-cycle specification and sole plan after
  explicit A+0 activation.

## D-033 — Preserve the current release on a new revision branch

- Date: 18 July 2026
- Decision: Preserve exact predecessor `4baec1e`, `main`, `origin/main`, and both
  portable-receipt refs; use only `revision/ai-first-folder-refactor` for the
  third cycle.
- Rationale: The complete second-cycle release remains an immutable fallback
  while the new product is unstarted and unverified.
- Active authority: `GOAL.md`, fresh Git, and the scaffold handoff.

## D-034 — Automatic planning with exception-only human input

- Date: 18 July 2026
- Decision: Replace per-file approval with one complete GPT plan, fixed
  compilation, automatic separate-copy execution, and at most one clarification
  when user intent is genuinely missing.
- Rationale: This makes GPT-5.6 central and reduces routine human work without
  giving the model destructive or verification authority.
- Active authority: `PRD-008`, `AI-008`–`AI-010`.

## D-035 — Ordinary-folder bijection

- Date: 18 July 2026
- Decision: Accept one bounded ordinary-folder contract and require every source
  file to appear exactly once under the result's `data/` tree.
- Rationale: Complete accounting is the simplest provable boundary against
  silent deletion, omission, merging, duplication, or invention.
- Active authority: `IO-006`, `TX-009`.

## D-036 — Protected members remain fixed and evidence-denied

- Date: 18 July 2026
- Decision: Include dotfiles, dot-directories, version-control internals, and
  named credential/key material while fixing their paths and denying their
  contents to GPT.
- Rationale: Preserving every file must not expose likely credentials or let the
  planner break project-control internals.
- Active authority: `IO-007`.

## D-037 — Bounded GPT evidence without mutation tools

- Date: 18 July 2026
- Decision: Give GPT only strict read-only inventory/text/link evidence tools and
  terminal planning/clarification tools; never a shell or file mutation API.
- Rationale: Semantic planning benefits from GPT-5.6, while deterministic code
  remains the sole authority for complete mapping, execution, and proof.
- Active authority: `AI-008`, `AI-009`.

## D-038 — Two repairs and one clarification round

- Date: 18 July 2026
- Decision: Permit one initial plan, at most two mechanically prompted repairs,
  and one compact user question/answer within fixed call/evidence limits.
- Rationale: This supports useful automatic correction without unbounded agent
  loops or shifting machine failures to the user.
- Active authority: `AI-010`.

## D-039 — Narrow inline Markdown adapter

- Date: 18 July 2026
- Decision: Rewrite only the frozen inline-link/image subset and cut reference-
  style Markdown links from this release.
- Rationale: Exact byte-span rewriting and same-target proof are deliverable and
  demonstrable; general Markdown grammar would endanger the core transaction.
- Active authority: `IO-011`, `TX-011`.

## D-040 — Bounded cross-platform-safe naming profile

- Date: 18 July 2026
- Decision: Enforce explicit NFC, character, reserved-name, length, suffix, and
  exact/NFC/casefold path-tree rules without claiming universal Windows or
  filesystem portability.
- Rationale: The fixed profile prevents demonstrable collisions and invalid
  targets while keeping claims technically honest.
- Active authority: `IO-010`, `CLAIM-005`.

## D-041 — New schema family and persistent job authority

- Date: 18 July 2026
- Decision: Create distinct generic `folder-*.v1` contracts and make
  `FolderRefactorJob` the sole mutable workflow authority.
- Rationale: Archive schemas cannot be safely reinterpreted, and planner state,
  evidence, clarification, execution, and proof must survive restart without a
  second in-memory authority.
- Active authority: `CASE-006`–`CASE-009`, `VER-010`.

## D-042 — Usable `data/` result inside path-neutral proof

- Date: 18 July 2026
- Decision: Put the reorganized folder under `data/` and portable request,
  evidence, plan, maps, proof, and original Markdown bytes under `name-atlas/`.
- Rationale: Ordinary users receive a directly usable folder while another
  person can move and inspect the surrounding verified handoff.
- Active authority: `PRD-009`, `VER-010`.

## D-043 — Acyclic receipt, keyless verifier, exact negative, and reconstruction

- Date: 18 July 2026
- Decision: Adapt the existing receipt DAG and source-free verifier, demonstrate
  a BagIt-valid altered accepted plan, and preserve exact original Markdown
  bytes for bounded reconstruction.
- Rationale: These mechanics distinguish Name Atlas from an ordinary organizer
  without claiming signatures, authenticity, or universal undo.
- Active authority: `VER-011`–`VER-014`.

## D-044 — One Start/Working/Done release experience

- Date: 18 July 2026
- Decision: Make the AI-first three-state browser the only normal release-facing
  UI and unregister the old archive workflow from judge commands.
- Rationale: One plain, automatic story is more coherent than exposing two
  incompatible product identities.
- Active authority: `UX-009`–`UX-012`.

## D-045 — One 24-file hero and one textual ambiguity case

- Date: 18 July 2026
- Decision: Use one mixed-format 24-file Northstar handoff hero, one small
  conflicting-text clarification fixture, and one exact controlled negative.
- Rationale: The fixtures demonstrate semantic planning, connected-file
  preservation, exception-only questions, and proof without claiming opaque
  media understanding or building multiple polished collections.
- Active authority: `REL-009`.

## D-046 — New planner recordings replace historical replay authority

- Date: 18 July 2026
- Decision: Require new real zero-question and one-clarification GPT-5.6 planner
  runs with exact sanitized replays; retain the old DecisionCard recording only
  as historical evidence.
- Rationale: The old bounded explanation card cannot prove the materially new
  central planning transaction.
- Active authority: `AI-011`.

## D-047 — One monotonic budget-ledger migration

- Date: 18 July 2026
- Decision: Preserve the sole ledger and USD 10 cap, migrate its secondary
  cumulative provider-request cap from 8 to 13, retain every historical count
  and exposure, and treat the one historical request as part of that cumulative
  total so at most twelve additional third-cycle attempts remain.
- Rationale: Two new qualification sessions need bounded request capacity, but
  resetting usage or creating a second ledger would destroy spending authority.
- Active authority: `AI-012`.

## D-048 — Optional installable Codex plugin behind one gate

- Date: 18 July 2026
- Decision: Consider only one thin STDIO-MCP Codex plugin at scaled A4 and admit
  it only after all core predicates, time, estimate, shared-architecture, and
  real install/new-task checks pass.
- Rationale: Codex integration can strengthen the demo only when it does not
  endanger or duplicate the mandatory browser product.
- Active authority: `REL-010` and the sole plan's plugin gate.

## D-049 — Pre-cut expansion and frozen claim boundaries

- Date: 18 July 2026
- Decision: Cut media/CSV/reference-style/code/AI-data/NER/hosted-app and other
  adjacent expansions before A+0, and limit claims to demonstrated mechanics.
- Rationale: A focused connected-folder transaction has greater completion and
  judging value than an incomplete universal organizer.
- Active authority: `CLAIM-004`, `CLAIM-005`.

## D-050 — Explicit AI-first activation

- Date: 18 July 2026
- Decision: Preserve H+0 and R+0 and create A+0 only when the user explicitly
  activates the complete amended sole goal in this primary task.
- Rationale: Governance revision does not authorize product, API, publication,
  or submission work by itself.
- Active authority: `GOAL.md`.

## D-051 — Submission hold continues

- Date: 18 July 2026
- Decision: Keep final Devpost submission prohibited through the AI-first build,
  release, video, and due diligence until explicit user release.
- Rationale: The irreversible submission must reflect the completed revised
  product rather than the preserved second-cycle release or an intermediate
  third-cycle state.
- Active authority: `GOAL.md`, the sole plan, and current `STATE.md`.

## D-052 — Bounded Markdown adapter and protected-link fail-closed rule

- Date: 18 July 2026
- Decision: Limit each `.md` or `.markdown` member to 16 MiB before provider
  use, cap the complete folder at 10,000 supported local Markdown references
  before provider use, keep the total opaque-payload contract governed by
  capacity rather than a new size cap, use compact per-document scanner
  structures, and block a protected Markdown member that contains a supported
  local link.
- Rationale: Exact span indexing is intentionally in-memory and therefore needs
  defensible per-document and aggregate graph bounds. Protected link context
  cannot be exposed or rewritten without violating the evidence-denial
  boundary.
- Active authority: `IO-006`, `IO-007`, `IO-011`.

## D-053 — Minimized disclosed inventory metadata

- Date: 18 July 2026
- Decision: Give the planner only relative path, member kind, stable file ID,
  byte size, and protected/evidence-eligible flags in inventory views; retain
  raw payload digests and detailed protection reasons locally and disclose the
  transmitted basic metadata before the Start action.
- Rationale: The planner needs stable identities and bounded structural facts,
  but raw hashes and internal protection diagnostics add no planning value.
- Active authority: `AI-009`, `AI-012`.

## D-054 — Structurally bounded request intent

- Date: 18 July 2026
- Decision: Bind every proposed and accepted plan to the one supported
  `rename_and_move_every_file` scope, require a structured planner blocker for
  outside-scope intent, bind the deterministic A2 provider to one exact
  demonstration request, and disclose before execution that every source file
  is retained exactly once.
- Rationale: A finite phrase classifier cannot exhaustively interpret arbitrary
  language. Complete-file mechanics prevent loss but cannot prove that an
  unrestricted request was semantically fulfilled. Exact development-request
  binding prevents a misleading success now, while A4 remains responsible for
  the bounded live planner and truthful unsupported-intent outcome.
- Active authority: `TX-009`, `AI-009`, `UX-009`, `CLAIM-005`.

## D-055 — Responsive browser with one mutation authority

- Date: 18 July 2026
- Decision: Run each complete durable scan/planner/copy/proof operation on one
  worker-thread event loop, keep its writer and transaction authority intact,
  return progress to the web loop through presentation-only phase callbacks,
  and defer task cancellation until the mutation-owning operation reaches a
  safe result or blocker.
- Rationale: A background asyncio task does not make synchronous filesystem
  work nonblocking. One operation-level worker boundary keeps `/working` and
  `/status` responsive without splitting the job across competing writers or
  leaving a detached mutation running during shutdown.
- Active authority: `UX-010`, `CASE-007`, `TX-012`.
