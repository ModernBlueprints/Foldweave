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
