# Reversible Name Atlas — Integrated Implementation Plan

Status: **ACTIVE**

Production goal: **ACTIVE**

Plan authority: **the only product implementation plan**

This document controls dependency order, integration targets, acceptance
evidence, scope cuts, and current delivery status. Product truth and acceptance
requirements live only in `docs/build/BUILD_SPEC.md`. Execution authority lives
only in `docs/build/GOAL.md`. Current observed state lives only in
`docs/build/STATE.md`.

H+0 is **Friday 17 July 2026 at 17:16:25 CEST**, the active-goal creation
timestamp in this primary Codex task. M0 through M6 are complete and M7 is in
progress.

## Operating rules

1. Build vertical, continuously runnable product slices in milestone order.
2. The primary Codex task is the sole integrator and owns architecture,
   cross-module contracts, repository state, integration, acceptance, claims,
   release state, and submission closure.
3. A bounded subagent may own a non-overlapping implementation or review task,
   but its output is an unverified claim until the primary integrator inspects,
   integrates, and runs the relevant checks.
4. A clean command exit is not completion. Each milestone requires the exact
   evidence in its delivery record plus inspection of user-visible output.
5. Keep the application runnable after every integration. Do not accumulate
   disconnected components for a late merge.
6. Required behavior in the specification is not cut merely because a target
   time is missed. Targets force integration and simplification; they are not
   cancellation timers.
7. Complete M5 triggers mandatory feature freeze. After that point, work is
   limited to defects, proof integrity, replay/live reliability, accessibility,
   judge setup, claims, release, recording, and submission.
8. Update the Actual status and Actual verification fields below only from fresh
   evidence. Keep `STATE.md` short and synchronized with the active milestone.

Status vocabulary: `PENDING`, `IN_PROGRESS`, `COMPLETE`, or `BLOCKED`. A milestone
is `COMPLETE` only when its user-visible outcome, automated checks, visual checks,
and downstream handoff all pass.

When an early milestone references a parent requirement that is hardened later,
the reference means only the explicit vertical slice stated in that milestone's
Outcome, Responsibilities, Checks, and Evidence fields. It does not claim the
entire parent requirement complete. Full specification acceptance is established
only by M6 and independently reproduced in M7.

## Timing model

Absolute protected boundaries:

- Recording-ready product: **Tuesday 21 July 2026 at 02:00 CEST**
- Submission confirmed: **Wednesday 22 July 2026 at 02:00 CEST**

A full 80-hour product window requires activation no later than Friday 17 July
2026 at 18:00 CEST.

At activation calculate:

`available_product_hours = hours from H+0 to 21 July 2026 02:00 CEST`

When `available_product_hours >= 80`, use the ordinary H+ targets. When it is
less than 80, apply every already-frozen exclusion immediately and set these
completion anchors:

| Anchor | Compressed completion target |
|---|---:|
| M1 | 15% of available product hours |
| M4 | 55% of available product hours |
| M5 | 70% of available product hours |
| M7 | 90% of available product hours |
| M8 | 100% of available product hours |

Pull M0, M2, M3, and M6 forward inside the next anchor while preserving the
dependency order. Never consume the final 24-hour reserve to restore an optional
feature.

If a milestone slips:

1. measure verified completion rather than effort spent;
2. identify the blocking dependency and root cause;
3. select the simplest route to the same user-visible outcome;
4. apply the next pre-authorized optional cut;
5. restore the continuously runnable product;
6. update this plan and `STATE.md` with evidence; and
7. continue.

After two serious failed corrections of the same problem, reassess the
abstraction or integration boundary instead of applying a third symptom patch.

## Non-negotiable delivery spine

The following remain required throughout compression:

- the strict supported package contract and fixed transformation profile;
- stable family identity and identity-level propagation;
- fail-closed parsing, collisions, decisions, and source-change handling;
- a real validated GPT-5.6 decision card with bounded authority;
- truthful, deterministic, visibly labeled replay;
- copy-only staging and unchanged source proof;
- complete forward/reverse maps, reverse dry run, and BagIt validation;
- connected Atlas, Decisions, and Proof states;
- the hero transaction plus one blocking negative transaction;
- a clean judge path, public repository, public video, and confirmed Devpost
  submission; and
- every claim boundary in `CLAIM-001` and `CLAIM-002`.

Pre-authorized optional cuts, in order:

1. animation and decorative motion;
2. a second visual theme;
3. extra profile or semantic-risk variants;
4. hero objects beyond what makes the required story clear;
5. metrics beyond measured judge-facing facts;
6. secondary pages;
7. CLI conveniences; and
8. nonessential documentation beyond judge, provenance, limitations, build
   disclosure, and submission needs.

`path_plan.csv` is already excluded by `IO-004` and is never reconsidered.

## Vertical delivery records

### M0 — Product foundation

| Field | Binding value |
|---|---|
| Requirement references | `PRD-004`, `AI-001`, `AI-006`, `REL-001`, `REL-002`, `REL-003` |
| Dependencies | Activated production goal and clean scaffold baseline |
| Target window | H+0–3 |
| User-visible outcome | The documented local command opens a minimal loopback application shell; replay and live provider boundaries are selectable and live mode reports credential absence clearly |
| Implementation responsibilities | Create the Python 3.11 project, lock dependencies, CLI and server entry points, modular package shell, configuration boundary, provider and validator protocols, and startup diagnostics; confirm API-access status without exposing secrets |
| Automated checks | `uv sync --frozen`; CLI help/start smoke test; configuration tests; initial pytest and Ruff pass |
| Visual checks | Browser shell opens at loopback only; mode and credential status are legible |
| Exact completion evidence | Commit ID; lockfile; successful command transcripts; browser screenshot; test/lint results; recorded API-access status |
| Downstream consumer | M1 walking skeleton and every later judge command |
| Owner | Primary integrator; bounded dependency/configuration review may be delegated |
| Allowed scope cut | Decorative shell styling only |
| Actual status | **COMPLETE** |
| Actual verification | **PASSED at commit `c177663c59efb22fb85f18d021f850fe396b08b6`: `uv sync --frozen`; Python 3.11; CLI/help and missing-credential behavior; 8 pytest tests; Ruff lint/format; SDK `responses.parse` surface; HTTP health smoke; `127.0.0.1`-only listener; safe diagnostics; in-app-browser DOM, console, and full-page visual inspection.** |

### M1 — Walking skeleton

| Field | Binding value |
|---|---|
| Requirement references | Walking-skeleton slices only of `PRD-001`, `PRD-005`, `TX-001`–`TX-004`, `TX-006`–`TX-008`, `AI-001`–`AI-004`, `UX-001`–`UX-004`, `VER-001`, and `VER-002`; no complete parent-requirement claim |
| Dependencies | M0 |
| Target window | H+3–12 |
| User-visible outcome | A small hero subset completes scan → family → proposal → deterministic Meaning risk → real GPT-5.6 card → human decision → identity propagation → copy-only stage → one proof result |
| Implementation responsibilities | Implement the thinnest complete transaction through real module boundaries, using one original and required linked derivatives/metadata; capture a sanitized real response suitable for later replay |
| Automated checks | Focused end-to-end happy path; GPT schema/authority rejection checks; source-before/after equality; one staged hash and one reverse mapping assertion |
| Visual checks | The same family can be followed coherently through Atlas, Decisions, and Proof; GPT content remains neutral and cannot approve |
| Exact completion evidence | End-to-end transcript; real model metadata and sanitized response; screenshots of the minimum three connected states; focused test results; one content-object source/stage hash equality; one rewritten control-field diff; one inverse logical-path map row |
| Downstream consumer | M2–M5; proves the architecture before hardening |
| Owner | Primary integrator; one bounded UI or GPT-schema task may be delegated without owning integration |
| Allowed scope cut | Use the minimum hero subset and plain styling; do not cut the real GPT call or complete transaction |
| Actual status | **COMPLETE** |
| Actual verification | **PASSED through release commit `d71b0b903a8259b158e1d674c5735edb88a6c665`: the connected 12-family/28-object hero transaction completed with the exact live `gpt-5.6` provider, one visible bounded evidence packet, one schema-valid advisory card, an explicit human edit to `campaign-poster`, family-wide propagation, copy-only staging, inverse maps, reverse dry run, unchanged source, and valid BagIt proof. The sanitized canonical response has SHA-256 `2fe0da43fe57e72043effcf13dc3a3084b8a262295e132b00109bf767f06ae00`; two subsequent complete keyless replay transactions independently reached the same proof without another provider request.** |

### M2 — Contract and graph hardening

| Field | Binding value |
|---|---|
| Requirement references | `IO-001`–`IO-005`, `TX-001`–`TX-005`, `TX-007`, `VER-003` scenarios 1–3 and 9–14, `REL-002` |
| Dependencies | M1 walking transaction remains runnable |
| Target window | H+12–24 |
| User-visible outcome | The complete supported package imports into stable object families, shows every declared relationship, creates the exact fixed-profile proposals, and explains mechanical blockers |
| Implementation responsibilities | Finish strict UTF-8 CSV/path/package validation, streamed snapshots, stable IDs, object-family graph, profile trace, Policy/Collision/Links/Meaning risks, and exact/NFC/casefold collision detection |
| Automated checks | Required parser, graph, identity, profile, collision, source-change, symlink/special-file, path-traversal, malformed CSV, and derivative-reference scenarios |
| Visual checks | Hero package structure and blocker messages agree with serialized domain objects; errors identify the exact member/invariant |
| Exact completion evidence | Focused suite results; stable-ID repeatability output; representative serialized family/proposal; screenshots of valid import and one blocker |
| Downstream consumer | M3 decision transaction and M4 staging |
| Owner | Primary integrator; bounded parser/fixture tests may be delegated |
| Allowed scope cut | Extra diagnostic prose and non-required risk variants |
| Actual status | **COMPLETE** |
| Actual verification | **PASSED at commit `1cce39d8c46c62eef96b9baa64b83d16765d5c03`: the complete strict package-contract matrix contains 41 focused import scenarios covering identifiers, UTF-8/CSV shape, supported tree, reciprocal metadata and derivative relationships, traversal, symlinks, special files, stable identities, and optional normalization behavior. Fixed-profile traces, Meaning signals, exact/NFC/casefold collisions, collision editing/recomputation, and source-change blocking are integrated. The 12-family/28-object Atlas and exact blocker states were inspected in-browser at 1440×1000. Full repository verification: 111 passed; Ruff and frozen sync passed.** |

### M3 — Decision transaction

| Field | Binding value |
|---|---|
| Requirement references | `TX-004`, `TX-006`–`TX-007`, `AI-001`–`AI-006`, `UX-002`, `UX-004`, `VER-003` scenarios 2–8 and 13 |
| Dependencies | M2 evidence addresses, proposals, and stable identities |
| Target window | H+24–34 |
| User-visible outcome | The user sees the exact outbound evidence, requests a live or recorded card, receives a neutral evidence-linked question, and explicitly approves, edits, refuses, or leaves unresolved; one decision propagates to the family |
| Implementation responsibilities | Complete evidence fingerprinting, structured live/replay/test providers, response validation, cache and cap metrics, decision-state machine, edit revalidation, low-risk batch approval, and stable-identity propagation |
| Automated checks | Unknown evidence/candidate rejection; malformed/API/cap failure; cache hit/invalidation; GPT authority denial; all human states; edited-path validation; family-wide propagation |
| Visual checks | Outbound packet is visible before generation; replay label is exact; neutral GPT card cannot alter status; human decision visibly controls readiness |
| Exact completion evidence | Live and replay response records; decision-ledger sample; metric output; focused tests; browser screenshots of pending, card, and resolved states |
| Downstream consumer | M4 export gate and M5 final Decisions experience |
| Owner | Primary integrator; bounded prompt/schema adversarial review may be delegated |
| Allowed scope cut | Extra card layouts, extra semantic-risk variants, and nonessential metrics |
| Actual status | **COMPLETE** |
| Actual verification | **PASSED through release commit `d71b0b903a8259b158e1d674c5735edb88a6c665`: complete evidence fingerprints, bounded live/replay/test providers, coordinator-side output revalidation, stale-card invalidation, exact cache behavior, explicit human states, identity-level propagation, write-once atomic replay capture, retry-without-second-call, pristine-evidence replay validation, and persistent conservative budget accounting are integrated. The real `gpt-5.6` card used the exact hero fingerprint, 14 supplied evidence references, and only mechanically supplied candidate paths; it remained advisory. Provider usage was 1,676 input and 994 output tokens. The application measured 14.645 seconds end-to-end latency, estimated USD 0.0382 cost, and retained a USD 0.6790 conservative reservation. Two keyless replay runs displayed the exact `Recorded GPT-5.6 response` label and made no live request.** |

### M4 — Staging and complete proof

| Field | Binding value |
|---|---|
| Requirement references | `TX-005`–`TX-008`, `VER-001`–`VER-004`, `VER-003` scenarios 8–20, `REL-002` |
| Dependencies | M2 hardened graph and M3 completed human decisions |
| Target window | H+34–44 |
| User-visible outcome | A resolved hero package stages atomically without touching the source, rewrites only declared references, generates complete proof artifacts and a valid BagIt package, and exposes a failed negative transaction as non-exportable |
| Implementation responsibilities | Implement pending-directory transaction, pre-stage rescan, copy and reference rewrite, complete maps and reverse dry run, proof serialization, human summary, BagIt creation/validator boundary, failure preservation, and final promotion |
| Automated checks | Copy failure; source mutation/change; payload equality; declared reference resolution; profile/collision checks; map inverse and reverse dry run; report/UI data equality; BagIt validation; whole-package blockers |
| Visual checks | Proof state shows every invariant, artifact path, blocker, and staged location with correct authority colors |
| Exact completion evidence | Successful and blocked transaction reports; source/stage hashes; forward/reverse maps; reverse-dry-run result; BagIt validation output; proof screenshot; focused suite |
| Downstream consumer | M5 product experience, M6 claims/docs, and demo recording |
| Owner | Primary integrator; bounded BagIt/transaction failure review may be delegated |
| Allowed scope cut | Extra proof charts or artifact viewers; never a proof invariant |
| Actual status | **COMPLETE** |
| Actual verification | **PASSED at commit `1cce39d8c46c62eef96b9baa64b83d16765d5c03`: atomic no-replace pending promotion; pre/post/final source checks; authority-specific decision validation; byte-copy and complete data-member accounting; strict staged control, source-snapshot, decision-ledger, and forward/reverse-map read-back; declared-reference resolution; exact reverse dry run; profile/collision checks; final post-BagIt deterministic rerun; BagIt validation; blocked failure-report preservation; and stale-proof clearing are implemented. Regression tests prove copy failure, extra payload, post-proof payload mutation, map/control/ledger tampering, source change, crafted authority records, and promotion collision cannot produce the green claim. The full 12-family package reached the Proof UI at 1440×1000 with all checks and no console errors.** |

### M5 — Product experience and feature freeze

| Field | Binding value |
|---|---|
| Requirement references | `UX-001`–`UX-005`, `PRD-001`–`PRD-003`, `VER-002`, `CLAIM-001`–`CLAIM-002` |
| Dependencies | Complete M1–M4 transaction |
| Target window | H+44–56 |
| User-visible outcome | One coherent, responsive Atlas → Decisions → Proof story explains the linked collection, the exception requiring judgment, and the verified staged result using the final hero package |
| Implementation responsibilities | Finish connected navigation/state, information hierarchy, accessible visual authority, understandable failures, recording-resolution layout, polished hero data and provenance, and one tiny negative fixture |
| Automated checks | UI smoke and state consistency; hero counts/ranges; negative fixture block; no hidden product path bypasses required decisions |
| Visual checks | Full browser walkthrough at recording dimensions; collision and `campaña → campana` stories are legible; no neutral GPT prose appears verified |
| Exact completion evidence | Final fixture inventory/provenance; screenshots of all three states and negative block; smoke results; feature-freeze checkpoint |
| Downstream consumer | M6 hardening and M8 demonstration |
| Owner | Primary integrator; bounded visual/accessibility critique may be delegated |
| Allowed scope cut | Cuts 1–6 from the frozen optional list as necessary |
| Actual status | **COMPLETE — FEATURE-FROZEN** |
| Actual verification | **PASSED through release commit `d71b0b903a8259b158e1d674c5735edb88a6c665`: commit `819e674ba74fb86d981f390d52214de5b4e4f7a7` froze the selected-root CLI, compact Atlas, exception-only Decisions queue, exact evidence and transformation presentation, separate GPT/human authority, blocker-specific Proof, proof-artifact controls, responsive layout, and one tiny unresolved-Meaning fixture. Browser QA completed the hero at desktop and mobile sizes and confirmed the negative fixture creates no stage. Final judge-facing captures now show the Atlas counts and risks, actual live request metrics, the neutral live card and human controls, exact recorded-replay labeling, verified deterministic Proof, and the blocked negative state. Feature freeze remains active.** |

**Feature freeze is mandatory when M5 is complete.**

### M6 — Release hardening

| Field | Binding value |
|---|---|
| Requirement references | `VER-003`, `REL-001`–`REL-004`, `CLAIM-001`–`CLAIM-002`, `AI-006` |
| Dependencies | M5 feature-frozen product |
| Target window | H+56–68 |
| User-visible outcome | The complete acceptance suite passes, replay is deterministic, live GPT-5.6 is freshly verified, and a judge can understand setup, supported scope, limitations, provenance, and Codex/GPT use |
| Implementation responsibilities | Close defects only; complete tests, README, MIT license, limitations, troubleshooting, pre-existing-work updates, build disclosure, sanitized replay record, screenshots, and factual metrics |
| Automated checks | Full pytest, Ruff check/format, replay repeats, live provider check, fixture and proof consistency, secret scan |
| Visual checks | Final cross-browser-size walkthrough; README and screenshots match current UI and commands |
| Exact completion evidence | Full check logs; live model record; replay-repeat comparison; docs/claim review; secret scan; screenshot set |
| Downstream consumer | M7 release candidate |
| Owner | Primary integrator; bounded documentation/claims audit may be delegated |
| Allowed scope cut | Cuts 5–8 only; no new feature work |
| Actual status | **COMPLETE** |
| Actual verification | **PASSED at release commit `d71b0b903a8259b158e1d674c5735edb88a6c665`: one live `gpt-5.6` transaction and two complete keyless replays passed; the canonical record is model/schema/evidence-bound and sanitized; live, replay, proof, Atlas, and blocked-negative captures were visually inspected; README, MIT license, limitations, provenance, troubleshooting, and factual Codex build disclosure are present. `uv lock --check`, `uv sync --frozen`, 116 pytest tests, Ruff lint and format, `git diff --check`, source and wheel builds, local Markdown links, canonical-record validation, and a repository secret scan passed. Two bounded release audits found no remaining product, claim, record, or source-checkout packaging blocker after correction of latency attribution and screenshot captions.** |

### M7 — Release candidate

| Field | Binding value |
|---|---|
| Requirement references | `REL-003`–`REL-004`, `VER-002`–`VER-003`, `AI-006`, `CLAIM-001`–`CLAIM-002` |
| Dependencies | M6 full local release checks |
| Target window | H+68–72 |
| User-visible outcome | A fresh judge environment can install and run replay; live mode is verified; the exact hero transaction, UI, proof, and commands are stable |
| Implementation responsibilities | Test a clean clone outside the working tree, run all judge commands, verify final Git state and public-repository readiness, repeat visual and secret checks, and select the release-candidate commit |
| Automated checks | Clean clone; frozen sync; replay; live smoke; full tests; lint/format; secret scan; Git cleanliness |
| Visual checks | Clean-clone UI and hero story match the working tree at recording dimensions |
| Exact completion evidence | Clone path and commit; exact command results; selected commit; final screenshots; repository-state report |
| Downstream consumer | M8 recording package and M9 public submission |
| Owner | Primary integrator; independent release-candidate review may be delegated |
| Allowed scope cut | No feature cuts remain; fix blockers or simplify implementation behind the same contract |
| Actual status | **IN_PROGRESS** |
| Actual verification | **M6 release commit selected as `d71b0b903a8259b158e1d674c5735edb88a6c665`. Clean-clone install, keyless replay transaction, judge commands, live-startup-only smoke, final secret/Git checks, and public-repository readiness remain to be reproduced outside the working tree.** |

### M8 — Recording readiness

| Field | Binding value |
|---|---|
| Requirement references | `REL-004` and all requirements referenced by its Definition of Done |
| Dependencies | Verified M7 release candidate |
| Target window | H+72–80; absolute deadline Tuesday 21 July 2026 at 02:00 CEST |
| User-visible outcome | The public repository and exact demonstration are finished; no code, feature, or design work remains; narration, shot list, copy, screenshots, and proof artifacts are ready for recording |
| Implementation responsibilities | Publish the MIT repository, verify final URLs and commit, rehearse the exact demo, time a 2:35–2:45 English narration draft, prepare shot list/Devpost copy/screenshots, and perform final rules/claims review |
| Automated checks | Public clean clone and judge commands; final acceptance suite; final secret scan; repository URL/commit verification |
| Visual checks | Timed rehearsal; capture-resolution walkthrough; screenshots and Devpost copy match the release candidate |
| Exact completion evidence | Public URL and commit; clean-clone log; rehearsal duration; narration/shot-list/Devpost drafts; final screenshot and proof-artifact set |
| Downstream consumer | M9 protected submission reserve |
| Owner | Primary integrator; user handles no recording yet unless they elect to start early |
| Allowed scope cut | Only nonessential copy polish; recording readiness itself is not cut |
| Actual status | **PENDING** |
| Actual verification | **NOT RUN** |

### M9 — Protected submission reserve

| Field | Binding value |
|---|---|
| Requirement references | `REL-004`, official Build Week rules and FAQ, `CLAIM-001`–`CLAIM-002` |
| Dependencies | M8 complete at the protected boundary |
| Target window | Tuesday 21 July 2026 02:00 CEST through Wednesday 22 July 2026 02:00 CEST |
| User-visible outcome | A public sub-three-minute English demo video and complete Devpost entry accurately demonstrate the working release and the submission receipt is confirmed |
| Implementation responsibilities | Support user voice-over; capture/edit; upload and verify public playback; obtain `/feedback` from the primary build task; re-run due diligence; create, review, and submit Devpost; capture confirmation |
| Automated checks | Final clean run at submitted commit; repository/video URL accessibility; required-field and claim checklist |
| Visual checks | Full public video playback with audio; Devpost preview; submitted page/receipt |
| Exact completion evidence | Public video URL; `/feedback` Session ID; final repository commit; Devpost URL; submission timestamp in Europe/Oslo; receipt screenshot or equivalent confirmation |
| Downstream consumer | Final Build Week delivery closeout |
| Owner | Primary integrator coordinates; user owns voice recording, MFA/CAPTCHA, account actions, and personal attestations |
| Allowed scope cut | No required submission element; cut only redundant polish |
| Actual status | **PENDING** |
| Actual verification | **NOT RUN** |

## Completion and checkpoint protocol

At each milestone boundary:

1. run the milestone's checks;
2. inspect the actual artifacts and UI;
3. record exact commands, results, paths, and commit;
4. update this milestone's Actual fields;
5. update `STATE.md` with the current phase, evidence, margin, blocker, and next
   exact operation; and
6. commit an integrated, runnable state before beginning the next milestone.

Do not mark the overall production goal complete until every completion surface
in `BUILD_SPEC.md` is complete and the Devpost submission is confirmed.
