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

## D-056 — In-place Connected Change revision

- Date: 18 July 2026
- Decision: Revise the existing five-document scaffold on
  `revision/ai-first-folder-refactor` rather than create another branch or
  governance authority.
- Rationale: The current branch already contains the exact completed A1–A3
  foundation; another branch would fragment integration and recovery.

## D-057 — Exact A3 fallback preservation

- Date: 18 July 2026
- Decision: Preserve `e3803d2` as the immutable completed A3 fallback.
- Rationale: The existential extension can fail without endangering the verified
  job, proof, receipt, verifier, and reconstruction transaction.

## D-058 — Change File as central differentiator

- Date: 18 July 2026
- Decision: Center the revised product on a transferable Name Atlas Change File.
- Rationale: Planning once and deterministically reapplying the same connected
  change is the clearest novel user transaction and strongest extension of A3.

## D-059 — Payload-free but metadata-disclosing transfer

- Date: 18 July 2026
- Decision: Transfer no project payload bytes while disclosing that paths,
  structure, sizes, hashes, link relationships, instruction, targets, and proof
  identifiers remain sensitive metadata.
- Rationale: This is the strongest truthful privacy boundary supported by the
  artifact; a broader secrecy claim would be false.

## D-060 — Deterministic partition refinement

- Date: 18 July 2026
- Decision: Match path-independent intrinsic descriptors and refine by ordered
  outgoing and sorted incoming relationship colors to a fixed point.
- Rationale: It supports differently arranged equivalent copies without semantic
  guesses, path shortcuts, or general graph-isomorphism scope.

## D-061 — Symmetric duplicates block

- Date: 18 July 2026
- Decision: Accept singleton refined classes only and block any unresolved
  duplicate symmetry.
- Rationale: An arbitrary tie-break could apply the right content to the wrong
  intended role while appearing mechanically successful.

## D-062 — Safe in-root parent links

- Date: 18 July 2026
- Decision: Permit decoded `..` only when lexical normalization remains inside
  the selected root and resolves uniquely to a regular logical member.
- Rationale: Real connected folders use sibling/parent-relative links; bounded
  normalization broadens usefulness without allowing traversal escape.

## D-063 — Truthful execution origins

- Date: 18 July 2026
- Decision: Record strict `gpt_planned` and `capsule_applied` origins.
- Rationale: Receiver execution must prove zero provider/API/budget use and must
  not fabricate model evidence or planning progress.

## D-064 — Versioned v2 authority with strict v1 evidence support

- Date: 18 July 2026
- Decision: Introduce v2 job, accepted-plan, and receipt contracts while keeping
  finalized A3 v1 receipts verifiable and v1 jobs read-only.
- Rationale: New provenance and receiver semantics cannot be silently imposed on
  historical artifacts.

## D-065 — Acyclic Core, receipt, and envelope

- Date: 18 July 2026
- Decision: Have the origin receipt commit the Change File Core fingerprint,
  then embed that finalized receipt in the self-fingerprinted envelope.
- Rationale: This produces a portable bidirectional binding without any artifact
  hashing itself.

## D-066 — Receiver-specific proof and convergence

- Date: 18 July 2026
- Decision: Give the receiver its own plan, receipt, reverse map,
  reconstruction, and one path-sensitive organized-tree commitment shared with
  the producer result.
- Rationale: The receiver must prove convergence while retaining the ability to
  recreate its own different starting layout.

## D-067 — Home, Organize, and Apply surface

- Date: 18 July 2026
- Decision: Use one Home with separate Organize and Apply journeys feeding shared
  Working and Done states.
- Rationale: The split makes the two product promises understandable and keeps
  GPT progress out of keyless receiver execution.

## D-068 — Bounded macOS picker and Finder bridge

- Date: 18 July 2026
- Decision: Add fixed-script `osascript` selection and verified-path `open`
  actions while retaining manual path fields.
- Rationale: Native selection removes the main local-browser usability problem
  without introducing a second desktop architecture or arbitrary command input.

## D-069 — One required shared STDIO MCP server

- Date: 18 July 2026
- Decision: Under Connected Change, expose seven high-level tools through one
  stable-v1 Python MCP server backed by the browser/CLI services.
- Rationale: MCP makes the product reusable from Codex and compatible hosts
  without duplicating the planner or filesystem authority.

## D-070 — MCP consent and idempotency

- Date: 18 July 2026
- Decision: Require explicit planning disclosure acknowledgement and persist
  canonical request/idempotency bindings in the existing job.
- Rationale: Model-driven retries must not duplicate provider calls, jobs,
  results, or clarification answers, and MCP must not bypass user disclosure.

## D-071 — Plugin behind installed-copy proof

- Date: 18 July 2026
- Decision: Gate plugin packaging after shared MCP and require marketplace
  installation, restart, new task, discovery, real invocation, and cache-copy
  evidence.
- Rationale: Repository files or a standalone server are not proof of an
  installable Codex plugin experience.

## D-072 — Existential C0 and exact A3 fallback

- Date: 18 July 2026
- Decision: Decide the whole cross-layout transaction before UI, provider, MCP,
  or plugin work, with two corrections maximum and mutually exclusive Connected
  or A3 fallback profiles.
- Rationale: The matching premise is the product's existential risk and must not
  consume release time if it cannot be proven end to end.

## D-073 — C+0 and absolute feature freeze

- Date: 18 July 2026
- Decision: Scale only pre-freeze milestones from actual C+0 while keeping
  feature freeze, release candidate, recording readiness, and submission fixed.
- Rationale: Remaining time changes, but the release reserve cannot be borrowed
  for continued feature work.

## D-074 — Sole budget ledger and delayed provider evidence

- Date: 18 July 2026
- Decision: Preserve one cumulative USD 10 ledger and make new provider calls
  only after C0 plus prompt/schema/evidence/fixture stabilization.
- Rationale: Calls before the existential and replay contracts stabilize create
  cost and unusable evidence without reducing core risk.

## D-075 — Connected Change claim and privacy boundaries

- Date: 18 July 2026
- Decision: Claim deterministic application to a differently arranged
  equivalent copy and no transferred payload bytes, while explicitly excluding
  semantic reconciliation, authentication, and metadata secrecy.
- Rationale: The demonstrated invariant is valuable only when stated more
  narrowly than universal equivalence, privacy, or trust.

## D-076 — Explicit C+0 activation

- Date: 18 July 2026
- Decision: Make the amended Connected Change goal inactive until the user
  explicitly activates its complete text in the current primary task.
- Rationale: Scaffold implementation freezes authority but must not consume the
  product clock or resume product mutation automatically.

## D-077 — Submission hold continues

- Date: 18 July 2026
- Decision: Keep final Devpost submission prohibited until the selected product,
  renewed materials, public video, `/feedback`, due diligence, and draft are
  complete and the user explicitly releases the hold.
- Rationale: Irreversible submission remains a user-owned gate and must reflect
  the final selected profile rather than an intermediate build.

## D-078 — Pre-activation remote preservation

- Date: 18 July 2026
- Decision: Under the user's explicit instruction, publish the existing
  `revision/ai-first-folder-refactor` history to the matching remote branch,
  then commit and push this factual checkpoint before C+0.
- Rationale: A remote copy protects the completed A1–A3 implementation and the
  inactive Connected Change scaffold before the next sprint. This ordinary
  branch backup does not activate the goal, select a product profile, alter
  `main`, open a pull request, promote a release, or release the submission
  hold.

## D-079 — C0 selects `CONNECTED_CHANGE_GO`

- Date: 19 July 2026
- Decision: Select `CONNECTED_CHANGE_GO` after the complete Sofia/Martin
  transaction, convergence, receiver reconstruction, exact refusal matrix,
  provider/API/budget/network isolation, and adversarial source-free verifier
  cases passed following the two allowed corrections.
- Rationale: The existential cross-layout premise is proven end to end before
  the C0 deadline. The final independent re-audit found no remaining material
  C0 defect; C1 now owns the separately classified engine-hardening work.

## D-080 — Exact sibling-result and native-picker browser authority

- Date: 19 July 2026
- Decision: Permit a selected output parent that is a strict source ancestor
  while requiring the exact pending and final result trees to remain disjoint
  from the source and each other, and include bounded native-picker invocation
  in the existing minimal-JavaScript authority.
- Rationale: The required default result next to the source necessarily uses the
  source's parent, and the required native selection route necessarily needs a
  small browser invocation. The previous literal wording contradicted those two
  required behaviors even though the exact result trees, native scripts, and
  server-side validators remain bounded.

## D-081 — Mandatory MCP inventory preflight before the durable handle

- Date: 19 July 2026
- Decision: Complete the bounded local path and inventory preflight before
  persisting and returning an MCP job handle, then run provider planning,
  matching, copying, and result creation behind that durable handle.
- Rationale: The strict v2 job identity requires the complete committed source
  inventory. A provisional handle or sidecar would be undurable or create a
  second workflow authority. The hero returns after preflight in 0.033628
  seconds, while the product now explicitly makes no fixed-latency claim for
  arbitrarily large admitted payloads.

## D-082 — Shared MCP restart and idempotency authority

- Date: 19 July 2026
- Decision: Keep scheduling process-local but recover every unfinished durable
  job at MCP server startup, retry overlapping writer ownership, preserve
  read-only status polling, and store all mutation-key bindings inside the sole
  v2 job.
- Rationale: A client can survive STDIO process replacement without creating a
  second job, ledger, provider call, or result, while lock contention remains a
  coordination event rather than a false product blocker.

## D-083 — Optional Codex plugin gate returns `GO`

- Date: 19 July 2026
- Decision: Admit one thin Codex plugin around the verified shared MCP server.
- Rationale: C1–C4 browser, CLI, live/replay, Change File, receipt, verifier,
  reconstruction, refusal, and shared-MCP surfaces pass; the actual Codex tool
  invocation passes; no required defect remains; more than twelve hours remain
  before recording readiness; and the plugin reuses the same server with a
  conservative implementation estimate below four hours.

## D-084 — Accept the clean-clone plugin and enter feature freeze

- Date: 19 July 2026
- Decision: Accept the thin Codex plugin after public clean-clone installation,
  isolated-cache equality, new-task tool invocation, keyless replay,
  verification, reconstruction, missing-key behavior, and uninstall all pass;
  enter selected-profile feature freeze immediately.
- Rationale: The optional plugin now satisfies its complete installed-copy gate.
  Freezing early protects the remaining release, documentation, visual,
  rehearsal, and packaging interval from new feature scope.

## D-085 — User-authorized Foldweave native-review cycle

- Date: 19 July 2026
- Decision: Begin no new product work until the user explicitly activates the
  refrozen Foldweave goal after this bounded governance revision.
- Rationale: Review-before-execution, native packaging, dual live planning, and
  derivative collaboration materially change the release contract and require
  one coherent new execution epoch.

## D-086 — Preserve `1023999` and use one new branch

- Date: 19 July 2026
- Decision: Preserve commit `1023999` and all predecessor refs, and perform the
  future cycle only on `revision/foldweave-native-review`.
- Rationale: One child branch protects the verified release without fragmenting
  architecture, history, or implementation authority.

## D-087 — Foldweave name, casing, tagline, and no conflict search

- Date: 19 July 2026
- Decision: Use **Foldweave**, exact casing, with **Change the structure. Keep
  the connections.**, and perform no brand-conflict search in this cycle.
- Rationale: The user selected the identity and expressly excluded further name
  investigation from the time-bounded implementation scope.

## D-088 — One deterministic engine and four mandatory execution modes

- Date: 19 July 2026
- Decision: Retain one deterministic engine while requiring native direct API,
  ChatGPT-hosted, recorded replay, and unchanged Change File application modes.
- Rationale: The modes differ in model transport, not in execution, proof, or
  job authority; sharing the engine prevents divergent safety semantics.

## D-089 — Review before execution and one immutable preview DTO

- Date: 19 July 2026
- Decision: Make a complete `folder-plan-preview.v1` the only renderer- and
  authorization-facing representation, use the explicit branching v3 lifecycle,
  and prohibit output before review.
- Rationale: Every surface must show and authorize the same mechanically valid
  proposal rather than reconstructing a plan from partial responses.

## D-090 — Job v3 and exact fingerprint-bound acceptance

- Date: 19 July 2026
- Decision: Use `folder-refactor-job.v3` for new jobs and bind acceptance to the
  exact job revision, source, imported file, candidate, preview, destination,
  channel, and idempotency key.
- Rationale: Transactional binding prevents stale tabs, changed inputs, races,
  duplicate retries, and restart ambiguity from executing an unseen proposal.

## D-091 — Bounded sparse revisions preserve the prior valid preview

- Date: 19 July 2026
- Decision: Permit at most two user revisions, apply only strict sparse deltas,
  rebuild and recheck the complete candidate, and retain the prior valid preview
  after failure.
- Rationale: This gives useful iteration without allowing partial plans,
  unchecked model authority, counter resets, or destructive failure recovery.

## D-092 — Immutable receiver parent and derivative child jobs

- Date: 19 July 2026
- Decision: Keep the model-free imported proposal in an immutable parent review
  job and create a separate child when the receiver asks a model to revise it.
- Rationale: The unchanged acceptance route and its provenance must survive a
  derivative attempt, while any model use must be truthfully attributable.

## D-093 — Change File v2, receipt v3, and strict historical compatibility

- Date: 19 July 2026
- Decision: Use the new v2/v3 schema family for Foldweave output and strict
  schema dispatch for historical jobs, receipts, Change Files, and fingerprints;
  keep application-capable v1 files applicable unchanged and derive only
  complete self-contained v2 children from v1 parents.
- Rationale: New review and lineage semantics require versioned contracts;
  global renaming would corrupt immutable predecessor evidence.

## D-094 — Immediate-parent lineage, explicit forks, and no merge

- Date: 19 July 2026
- Decision: Record one immediate parent per derivative, permit explicit forks,
  embed no recursive ancestor envelopes, implement no automatic merge, cap
  generation at 32 inclusive, and cap canonical lineage metadata at 1,048,576
  bytes inclusive.
- Rationale: Bounded lineage supports serial collaboration without introducing
  live collaborative state, unbounded metadata, or ambiguous merge authority.

## D-095 — Sofia/Martin/Sofia serial collaboration proof

- Date: 19 July 2026
- Decision: Require the complete T1/CF1 to Martin T2/CF2 and back-to-Sofia
  transaction, including unchanged application, both live revision transports,
  convergence, and participant-specific reconstruction.
- Rationale: This single proof demonstrates the product's core portable and
  iterative value across differently arranged equivalent sources.

## D-096 — Purpose-built accessible tree and focused React review island

- Date: 19 July 2026
- Decision: Use a shared React/TypeScript/Blueprint folder-tree component for
  native, browser, and ChatGPT review rather than Mermaid or static diagrams;
  require its exact 500-file/1,000-directory acceptance fixture.
- Rationale: Operational review needs scalable navigation, filtering, stable
  state, exact member detail, shared DTO semantics, and accessibility.

## D-097 — pywebview shell with one FastAPI control plane

- Date: 19 July 2026
- Decision: Package a narrow pywebview 6.x shell around the existing FastAPI
  engine and keep durable product state server-owned.
- Rationale: A small native shell supplies macOS integration without creating a
  second backend, duplicating the app, or undertaking a full frontend rewrite.

## D-098 — PyInstaller onedir profile and bounded py2app fallback

- Date: 19 July 2026
- Decision: Use a checked-in PyInstaller 6.x `onedir --windowed` specification;
  switch to py2app only after two serious PyInstaller corrections fail.
- Rationale: The primary profile is inspectable and time-bounded while the
  preauthorized fallback prevents indefinite packaging repair.

## D-099 — Keychain credential store and strict endpoint policy

- Date: 19 July 2026
- Decision: Keep API credentials in macOS Keychain behind a Python protocol,
  expose only configured state to renderers, and validate direct endpoints and
  redirects fail-closed; keep user runtime and development-qualification keys
  as distinct roles; store new production v3 state under
  `~/Library/Application Support/Foldweave/` with explicit alternate-root
  injection and read-only legacy stores.
- Rationale: Model credentials must remain outside React, browser persistence,
  jobs, MCP, artifacts, and logs while still supporting local direct mode.

## D-100 — Exact direct Responses API mode remains mandatory

- Date: 19 July 2026
- Decision: Preserve exact `gpt-5.6`, Responses API, strict tools,
  `store=false`, no model fallback, and no provider retry for direct planning.
- Rationale: Direct API operation is an explicit product requirement and its
  evidence and cost authority must remain bounded and reproducible.

## D-101 — ChatGPT-hosted mode is mandatory and billing-separate

- Date: 19 July 2026
- Decision: Require actual ChatGPT-supplied model inference with no hidden
  Foldweave Responses API request or direct-ledger mutation.
- Rationale: ChatGPT subscriptions and API billing are separate; only a genuine
  host-model workflow provides the required subscription-backed experience.

## D-102 — Public Cloudflare MCP gateway and outbound companion

- Date: 19 July 2026
- Decision: Use Cloudflare Workers Free on `workers.dev` with
  `@cloudflare/workers-oauth-provider`, its required `OAUTH_KV` binding, a
  SQLite Durable Object relay, and a paired outbound local companion.
- Rationale: ChatGPT needs a stable public authenticated MCP endpoint while the
  local-first engine must remain behind an outbound-only connection.

## D-103 — OAuth/PKCE/CIMD pairing with local-device identity

- Date: 19 July 2026
- Decision: Use authorization code OAuth 2.1 with PKCE S256, CIMD and DCR
  fallback, a Keychain-held Ed25519 device key, and bounded one-time-code
  pairing, expiry, rate limits, rotation, and revocation.
- Rationale: Foldweave has no account system; the verified local installation is
  the narrow identity root while the library owns standards-sensitive OAuth.

## D-104 — Durable Object relay, replay defense, and local job authority

- Date: 19 July 2026
- Decision: Let the Durable Object accept the companion's outbound WSS with
  hibernation and bounded correlation state, but keep every product operation
  and idempotency record in the local v3 job.
- Rationale: Signed requests, nonces, sequences, digests, expiry, and reconnect
  can protect transport without turning Cloudflare into a second engine or job
  database; large correlation state must not rely on the 16,384-byte WebSocket
  attachment limit.

## D-105 — Secure MCP Tunnel is developer qualification only

- Date: 19 July 2026
- Decision: Require the official tunnel for F0c developer-mode proof but never
  use it as the consumer distribution architecture or proof of consumer no-key
  access; substitution requires a user instruction or official-rule change.
- Rationale: Tunnel setup depends on separate Platform configuration and does
  not replace the selected paired public gateway.

## D-106 — Two-layer shared MCP and reviewed Codex workflow

- Date: 19 July 2026
- Decision: Expose bounded host-planning and high-level reviewed-workflow tools
  through local STDIO and authenticated HTTP transports over one domain service.
- Rationale: Host models need evidence and submission tools, while callers need
  durable workflows; neither layer may bypass review or gain arbitrary file or
  shell authority.

## D-107 — Orthogonal planning, transport, and execution provenance

- Date: 19 July 2026
- Decision: Record planning basis, model transport, and execution origin as
  separate strict fields.
- Rationale: Fresh versus derivative planning, API versus host transport, and
  planned versus capsule execution answer different truth claims and must not
  be collapsed.

## D-108 — Replay and unchanged application remain model-free

- Date: 19 July 2026
- Decision: Keep recorded replay and exact unchanged Change File application
  free of model calls, credentials, external model requests, and budget use.
- Rationale: These modes are essential keyless evidence and deterministic
  portability paths, not degraded live planning.

## D-109 — Sole budget ledger migrates monotonically to USD 40

- Date: 19 July 2026
- Decision: After F+0 and the required contract freeze, but before any F0b live
  call, preserve `.name-atlas/api_budget.json` and all history, raise only its
  monetary ceiling to USD 40, retain call cap 13, and finalize the call cap in
  F4 after the complete call graph is frozen.
- Rationale: One cumulative ledger prevents reset or double authority while the
  larger ceiling permits the required real direct qualification transactions.

## D-110 — Foldweave branding with strict legacy dispatch

- Date: 19 July 2026
- Decision: Rename every active release-facing surface to Foldweave while
  preserving historical schema identifiers, artifact paths, receipts, jobs,
  Git history, and a documented `name-atlas` CLI alias.
- Rationale: The new product needs one coherent identity without falsifying or
  breaking verified predecessor artifacts.

## D-111 — Separate ChatGPT distribution states

- Date: 19 July 2026
- Decision: Track developer verification, consumer pairing, publication
  readiness, review submission, approval, and publication independently.
- Rationale: Implementation and developer connection do not prove directory
  approval or public listing, which require external observed evidence.

## D-112 — Four opening existential gates

- Date: 19 July 2026
- Decision: Prove review authority, packaged native operation, actual ChatGPT
  developer mode, and the consumer gateway before broad polish or release work;
  give each persistent failure an exact no-go or external-wait state and prevent
  later milestones from passing while a mandatory gate is unverified.
- Rationale: The highest-risk integrations must fail or pass while there is
  still time to correct architecture rather than after surface polish.

## D-113 — Fixed 44-hour scaling and absolute boundaries

- Date: 19 July 2026
- Decision: Scale F0–F7 from the actual remaining portion of the fixed envelope,
  with feature freeze at 01:00, release candidate at 06:00, and recording
  readiness at 10:00 CEST on 21 July 2026.
- Rationale: F+0 records activation but cannot manufacture time or move the
  user's protected video and submission reserve.

## D-114 — Fixed scope cuts and prohibited expansion

- Date: 19 July 2026
- Decision: Apply only the ordered optional cuts and prohibit new platforms,
  backends, collaboration systems, discovery, and validation machinery.
- Rationale: Predetermined cuts preserve required product value and prevent
  reactive architecture expansion under deadline pressure.

## D-115 — Explicit F+0 activation boundary

- Date: 19 July 2026
- Decision: Create F+0 only when the user explicitly activates the complete
  amended goal in the current primary task.
- Rationale: Governance preparation and remote preservation must not
  accidentally authorize product, credential, API, or external-service work.

## D-116 — Continuing final-submission hold

- Date: 19 July 2026
- Decision: Prohibit final Devpost submission until all product, release, video,
  `/feedback`, due-diligence, and package requirements pass and the user
  explicitly releases the hold.
- Rationale: Submission includes user-owned voice, attestations, and final
  authority that implementation progress cannot replace.

## D-117 — Separate the defensive lineage byte ceiling from valid v2 shape acceptance

- Date: 20 July 2026
- Decision: Retain the inclusive 1,048,576-byte lineage parser ceiling and its
  one-byte-over refusal, but test valid current-schema acceptance with the
  maximum 500 fixed-shape member bindings rather than requiring an unreachable
  one-MiB v2 lineage object. Do not add padding or enlarge the product member
  boundary to manufacture that size.
- Rationale: The maximum valid 500-binding v2 lineage serializes far below one
  MiB, so the earlier exact-valid-object boundary requirement contradicted the
  frozen 500-member schema. This correction preserves the defensive limit while
  making product acceptance semantically possible.

## D-118 — Keep the public job capability inside the trusted local authority

- Date: 20 July 2026
- Decision: Persist only the local device-key-derived job-capability hash and
  binding metadata in JobV3, and validate that capability inside the companion/
  host after verified device, OAuth-grant, scope, request, and job binding. Never
  return or accept the raw capability through MCP, `structuredContent`, `_meta`,
  the model, the widget, gateway state, browser state, or logs.
- Rationale: A raw bearer capability in an Apps SDK tool result is visible to
  the model and conversation transcript, contradicting UX-022's strict secret
  boundary. Server-side derivation preserves the thirty-minute per-job
  authority without exposing a secret to an untrusted presentation surface.
