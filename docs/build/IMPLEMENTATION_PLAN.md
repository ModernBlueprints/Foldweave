# Reversible Name Atlas — Revised Integrated Implementation Plan

Status: **READY / INACTIVE**

Amended production goal: **INACTIVE**

Revision R+0: **NOT STARTED**

Submission hold: **ACTIVE**

This is the only implementation plan. `BUILD_SPEC.md` defines product truth;
the complete amended `GOAL.md`, once explicitly activated by the user, defines
execution authority; `STATE.md` reports current observed state. This plan
defines dependency order, target signals, evidence, allowed cuts, and actual
results. Merely existing or being committed does not activate it.

## Known-good inherited baseline

The revision starts from public release commit
`827b0f6f93174d3c34aedfd98d8467a299ab2669` on `main`. The product cycle will
continue on `revision/portable-change-receipt`; `main` remains the immutable
fallback until a renewed release candidate passes and is fast-forward promoted.

Inherited evidence, not proof of any newly added requirement:

- M0–M7 completed in the first cycle.
- Decisive first-cycle commits include scaffold `f1c519d`, feature-freeze
  product `819e674`, live/replay release `d71b0b9`, clean-clone release candidate
  `b4a2dd0`, and public checkpoint `827b0f6`.
- The strict linked-package importer, deterministic family/proposal engine,
  collision/reference checks, human authority, copy-only staging, maps, reverse
  dry run, BagIt validation, replay mode, and one validated real `gpt-5.6`
  record are inherited.
- The inherited release passed 116 pytest tests, Ruff lint/format, builds,
  secret/link checks, replay/live truthfulness checks, clean-clone installation,
  and one complete verified hero transaction.
- The validated replay record has SHA-256
  `2fe0da43fe57e72043effcf13dc3a3084b8a262295e132b00109bf767f06ae00`
  and evidence fingerprint
  `0f0b0b7cf923432431e7d184c6881cb34d61a0e5caf578f87cc029494b97d830`.
  Reuse it unless the evidence/card contract materially changes.

Old M8 status:

`SUPERSEDED — FIRST-CYCLE RELEASE MATERIAL PRESERVED BUT STALE`

The first-cycle README, screenshots, narration, thumbnail, Devpost copy, and
submission package are not evidence of revised release readiness. Final
submission remains prohibited while the submission hold is active.

## Timing model fixed at activation

R+0 is the Europe/Oslo timestamp at which the user explicitly activates the
complete amended `docs/build/GOAL.md` in this primary Codex task.

At R+0 calculate:

`available_revision_hours = hours from R+0 to Tuesday 21 July 2026 at 02:00 CEST`

`planned_revision_hours = min(70, max(0, available_revision_hours - 4))`

The four hours immediately before recording readiness are contingency for
defects and release blockers, never new scope. The final 24 hours through
Wednesday 22 July 2026 at 02:00 CEST remain the submission reserve.

If `planned_revision_hours < 70`, multiply the standard anchors by
`planned_revision_hours / 70`:

| Milestone | Standard anchor |
|---|---:|
| R1 | 12/70 |
| R2 | 26/70 |
| R3 | 38/70 |
| R4 and restore gate | 52/70 |
| R5 when admitted | 60/70 |
| R6 | 68/70 |
| R7 | 70/70 |

Preserve milestone order and absolute boundaries. The restore gate separately
requires at least 18 actual hours remaining. Targets force integration and
simplification; they are not cancellation timers. A missed optional gate cuts
that optional feature. A missed target does not cancel required case,
staleness, binding, receipt, verifier, controlled failure, five-state flow,
proof, clean clone, or release outcomes.

## Operating rules

- The current primary Codex task is the sole primary integrator. Bounded
  subagents may handle non-overlapping work; their results require inspection
  and product-native verification.
- Build vertical outcomes. Keep the integrated application runnable after R1.
- Every milestone closes only with actual automated evidence and relevant
  visual/artifact inspection; a completion message is not proof.
- Update this plan and the short state checkpoint with observed results. Record
  only material specification deviations in `DECISIONS.md`.
- Do not reopen project discovery, adapters, a parallel scaffold, or generic
  validation infrastructure.
- After two serious failed corrections of the same defect, reassess and simplify
  the abstraction rather than applying a third symptom patch.

Pre-authorized optional cuts, in order:

1. decorative motion;
2. second theme;
3. advanced Atlas filters and nonessential metrics;
4. thumbnails and additional relationship visuals;
5. case list/rename/delete conveniences;
6. extra negative permutations; additional public verifier output formats are
   already excluded;
7. restore UI; and
8. `restore-receipt` itself, but only before the one-time restore verdict; taking
   this cut causes `CUT_BY_PREAUTHORIZED_GATE`, and a recorded `GO` makes the
   command mandatory.

Never cut case persistence, staleness detection, evidence/card/human binding,
receipt JSON, offline HTML, independent receiver verifier, the controlled
failure, five-state flow, live/replay truthfulness, clean clone, or release
hardening.

## Revised vertical delivery records

### R1 — Revision walking transaction

- **Requirements:** PRD-006, CASE-001–005, AI-007, VER-005–008, UX-006–007,
  REL-005.
- **Dependencies:** explicit goal activation; inherited `827b0f6` release and
  validated replay record.
- **Calculated target:** standard R+0–12; proportionally scaled at activation.
- **User-visible outcome:** the hero case survives a process restart, the
  inherited replay card binds to a human decision, staging emits a minimal
  receipt, a separate keyless verifier passes, the exact BagIt-valid altered
  copy blocks, and all five routes exist in plain integrated form.
- **Implementation responsibilities:** introduce one rehydratable case aggregate,
  minimal versioned persistence, decision/card binding, minimal receipt DAG,
  receiver-verifier dispatch, controlled counterfactual, and five server routes
  without visual redesign.
- **Automated checks:** focused restart/binding tests; inherited suite; valid
  bag verifier exit `0`; altered-ledger bag BagIt-pass plus verifier exit `1`;
  route and redirect tests; no provider call in replay.
- **Visual checks:** inspect one complete plain Atlas→Decide→Stage→Verify→Handoff
  transaction and truthful replay label.
- **Exact completion evidence:** committed integrated transaction; case revision
  before/after restart; receipt fingerprint; separate subprocess output; BagIt
  result and exact digest blocker for controlled failure; five route captures;
  actual test counts.
- **Downstream consumer:** R2 hardening and R3 final receipt/verifier contracts.
- **Owner:** primary integrator; bounded subagents only for frozen isolated tests
  or pure contracts.
- **Allowed cut:** styling, convenience controls, extra metrics, restore; not any
  named walking-transaction link.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT RUN`.

### R2 — Case and authority hardening

- **Requirements:** CASE-001–005, AI-004–007, TX-006–007, VER-009.
- **Dependencies:** verified R1 walking transaction.
- **Calculated target:** standard R+12–26; proportionally scaled at activation.
- **User-visible outcome:** restart-safe decisions behave as one durable case;
  corruption, conflicting writers, and source change produce precise blockers;
  finalized cases cannot silently change.
- **Implementation responsibilities:** strict complete schema, canonical naming,
  atomic fsync/replace, process lock, optimistic revision check, lifecycle,
  deterministic rehydration, exact staleness diff, invalidation, and global
  budget-ledger separation.
- **Automated checks:** corrupt/unknown/incomplete case; revision and lock
  conflict; all five source-change classes; binding mismatches; finalized-case
  immutability; low-risk/collision records without GPT provenance; unchanged
  reopen with zero provider requests; inherited suite.
- **Visual checks:** restart the server on the same case; inspect preserved
  decisions and exact stale-source blocker.
- **Exact completion evidence:** serialized schema examples, atomicity and lock
  tests, source-diff matrix, no-call evidence, restart capture, actual full-suite
  result.
- **Downstream consumer:** R3 immutable receipt finalization and R4 persistent UI.
- **Owner:** primary integrator; bounded persistence-test reviewer allowed.
- **Allowed cut:** case listing, rename/delete, destructive reset, reconciliation,
  and convenience UI.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT RUN`.

### R3 — Receipt and verifier completion

- **Requirements:** VER-005–009, AI-007, REL-005, CLAIM-003.
- **Dependencies:** verified R2 case authority and inherited deterministic proof.
- **Calculated target:** standard R+26–38; proportionally scaled at activation.
- **User-visible outcome:** the complete source-free receipt can be copied and
  independently verified offline; its HTML explains the transaction; the exact
  controlled alteration remains BagIt-valid but Name-Atlas-blocked.
- **Implementation responsibilities:** final strict schemas; path-neutral source
  and report; byte-exact original controls; canonical ReceiptCore and envelope;
  acyclic 15-step writer; offline HTML; pure source-free verifier; optional
  source comparison; stable check IDs and exit contract.
- **Automated checks:** fingerprint/raw-digest/staged-data recomputation;
  self-reference absence; moved-bag verification; sender-path scan; HTML-machine
  agreement; cross-artifact consistency; source-free and `--source` matrices;
  malformed/schema/invariant blockers; no-write verifier snapshot; controlled
  counterfactual; inherited suite.
- **Visual checks:** open offline HTML without server/network and compare its
  central facts to the machine receipt and CLI verdict.
- **Exact completion evidence:** finalized successful hero handoff, copied-bag
  subprocess result, artifact hash table, path scan, HTML capture, controlled
  failure transcript, and actual test counts.
- **Downstream consumer:** R4 workbench and restore applicability gate.
- **Owner:** primary integrator; independent bounded verifier reviewer allowed.
- **Allowed cut:** extra negative permutations only; no additional public output
  format is permitted.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT RUN`.

### R4 — Five-state product experience

- **Requirements:** UX-004, UX-006–008, CASE-002–004, VER-007–009.
- **Dependencies:** verified R3 case/receipt/verifier transaction.
- **Calculated target:** standard R+38–52; proportionally scaled at activation.
- **User-visible outcome:** a streamlined dark Atlas, Decide, Stage, Verify, and
  Handoff workbench makes exceptions, human authority, proof, and receiver
  action immediately understandable.
- **Implementation responsibilities:** server-computed routing and guards;
  persistent shell; exception-first inspectors; progressive disclosure;
  Blueprint core `6.17.2` and icons `6.13.0` vendoring, attribution, wheel
  packaging, semantic HTML, responsive Name Atlas CSS, limited local JS.
- **Automated checks:** all routes and root transitions in every prerequisite
  state; POST guards; accessibility landmarks/labels; asset/no-CDN checks; wheel
  contents; uv-only clean install; inherited and revised suites.
- **Visual checks:** desktop recording resolution and narrow viewport; each
  route in complete and blocked states; keyboard flow, focus, contrast, status
  text, collapsed evidence, and no sender-path leakage.
- **Exact completion evidence:** route matrix, five approved captures, clean-wheel
  asset list and notice, visual/accessibility findings, actual suite results.
- **Downstream consumer:** restore gate, R6 hardening, and three-minute demo.
- **Owner:** primary integrator; bounded visual QA reviewer allowed.
- **Allowed cut:** motion, second theme, advanced filters, thumbnails, extra
  relationship visuals, case conveniences.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT RUN`.

### Restore gate — one-time applicability decision

- **Requirements:** REL-006.
- **Dependencies:** R1–R4 complete and freshly passing.
- **Calculated target:** at R4, no later than standard R+52 or its scaled anchor.
- **User-visible outcome:** one objective decision: restore is admitted or is
  recorded `CUT_BY_PREAUTHORIZED_GATE` without ambiguity.
- **Checks:** case restart; receipt JSON/HTML; positive and controlled-negative
  receiver verification; all five routes; inherited/new core suites; no material
  cross-artifact defect; at least 18 actual hours before recording readiness.
- **Exact completion evidence:** timestamped gate table with every predicate and
  final `GO` or `CUT_BY_PREAUTHORIZED_GATE`.
- **Owner:** primary integrator; no delegation of the decision.
- **Allowed cut:** restore UI may be cut independently. Before the verdict, the
  restore command may be cut and the verdict becomes
  `CUT_BY_PREAUTHORIZED_GATE`. After a recorded `GO`, the command is mandatory
  and cannot be relabeled as a gate cut. A legitimate gate cut does not block R6
  or release.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT EVALUATED`.

### R5 — Conditional restore

- **Requirements:** REL-006 and only the applicable portions of VER-009 and
  CLAIM-003.
- **Dependencies:** restore-gate `GO`.
- **Calculated target:** standard R+52–60; proportionally scaled at activation.
- **User-visible outcome:** a verified receipt can reconstruct every in-scope
  logical source-package member into a new destination, or this entire milestone
  is correctly absent after a gate cut.
- **Implementation responsibilities:** verify-first CLI, absent-destination
  guard, pending directory, reverse-map copy, byte-exact control restoration,
  strict reimport, complete path/size/hash equality, no-replace promotion,
  `restore-report.v1`; UI action only if still admitted.
- **Automated checks:** successful restore, existing destination, invalid receipt,
  copy/reimport/proof failure, source and handoff immutability, complete snapshot
  equality, no partial promotion.
- **Visual checks:** command clarity and Handoff action only if shipped.
- **Exact completion evidence:** after gate `GO`, a restore report and equality
  matrix; if the gate instead records `CUT_BY_PREAUTHORIZED_GATE`, R5 is
  inapplicable and no command/UI/docs/claim is present.
- **Downstream consumer:** R6 hardening and optional demo claim.
- **Owner:** primary integrator.
- **Allowed cut:** restore UI only after gate `GO`; there is no post-`GO` command
  cut. An admitted-command failure blocks R5 and release until corrected.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT APPLICABLE UNTIL GATE`.

### R6 — Feature freeze and release hardening

- **Requirements:** all required specification IDs; REL-006 only if applicable;
  REL-007; CLAIM-001–003.
- **Dependencies:** R4 plus restore cut, or R5 when admitted.
- **Calculated target:** R+52–68 without restore or R+60–68 with restore,
  proportionally scaled; optional feature freeze occurs immediately before R6
  and no later than 12 hours before recording readiness.
- **User-visible outcome:** one truthful, portable, stable release candidate with
  a clear judge path and no planned features.
- **Implementation responsibilities:** defect repair only; full proof-integrity
  audit; replay/live truthfulness; portability/path and secret scans; clean clone;
  wheel/build/license checks; accessibility/visual QA; refreshed README,
  limitations, notices/provenance, screenshots, narration, Devpost draft, and
  claims.
- **Automated checks:** lock/sync; full pytest; Ruff lint/format; build; link,
  secret, absolute-path, asset-license, and wheel-content scans; fresh copied
  hero verification; conditional restore; clean-clone replay and verifier;
  live startup and card validity without an unnecessary call.
- **Visual checks:** every route, blocked states, offline receipt, recording
  viewport, clean clone, no secrets/personal paths, refreshed screenshots.
- **Exact completion evidence:** selected candidate SHA, command transcript,
  test counts, artifact fingerprints, clean-clone record, visual audit,
  refreshed release-material paths, and claim matrix.
- **Downstream consumer:** R7 recording readiness and submission reserve.
- **Owner:** primary integrator; bounded clean-clone, visual, README, and claim
  reviewers allowed.
- **Allowed cut:** only remaining optional presentation conveniences; no required
  integrity or release surface.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT RUN`.

### R7 — Recording readiness

- **Requirements:** REL-007 and all applicable completion surfaces.
- **Dependencies:** verified R6 release candidate.
- **Calculated target:** standard R+68–70; proportionally scaled, ending no later
  than Tuesday 21 July 2026 at 02:00 CEST.
- **User-visible outcome:** the exact three-minute case→decision→receipt→receiver
  story is stable, rehearsed, and ready to record.
- **Implementation responsibilities:** select release commit; final clean replay
  and verifier; confirm live evidence truthfulness; finalize proof artifacts,
  screenshots, narration, shot list, Devpost draft, and `/feedback` path; make no
  planned code or design changes.
- **Automated checks:** final clean-clone judge commands and artifact fingerprints;
  repository/public revision alignment only after release acceptance.
- **Visual checks:** timed full rehearsal at capture resolution and offline
  receipt/handoff readability.
- **Exact completion evidence:** release SHA, clean status, final verification
  fingerprint, timed rehearsal duration, final materials, and zero planned work.
- **Downstream consumer:** protected submission reserve.
- **Owner:** primary integrator; user owns voice recording and `/feedback`.
- **Allowed cut:** no required release surface; restore remains absent if already
  gate-cut.
- **Actual status:** `PENDING / INACTIVE`.
- **Actual verification:** `NOT RUN`.

## Protected submission reserve

The final 24 hours are for the user's voice-over, final capture/edit/upload,
playback verification, `/feedback`, final rule/claim/clean-run audit, and
submission. Codex may prepare and update the Devpost draft after revised-goal
activation, but final submission is prohibited until the user explicitly
releases the active submission hold.

If every independent requirement is complete while the hold remains active, set
the phase to `WAITING_FOR_SUBMISSION_HOLD_RELEASE`, request only that release,
and preserve the completed release unchanged.

## Milestone closure protocol

For each milestone: verify dependencies; calculate its actual target; implement
the smallest complete vertical outcome; run its automated and visual checks;
record actual results and artifact/commit evidence; update `STATE.md`; and commit
coherently. If late, measure the gap, diagnose its root cause, take the next
authorized cut, restore the integrated product, and continue. Never mark a
milestone complete from elapsed time, code volume, or an agent report.
