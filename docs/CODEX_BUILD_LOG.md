# Foldweave — Codex and GPT-5.6 build log

This is the factual development record for **Foldweave**, previously released
during Build Week as Reversible Name Atlas/Name Atlas. Codex with GPT-5.6 is the
primary development environment and integrator. The user chose the product
direction, authorized the frozen build contracts and plain-English requests,
supplies the sole clarification answer when required, and owns the submission
voice-over, eligibility attestations, `/feedback`, and final submission-hold
release. Historical names, commit descriptions, artifacts, and qualification
claims below remain unchanged because they describe the product that existed at
those checkpoints.

The current runtime use of model inference is central but bounded. In native
direct mode, exact `gpt-5.6` proposes a complete plan or sparse revision through
the Responses API. In ChatGPT-hosted and Codex-hosted modes, the host supplies
model inference through bounded Foldweave tools. Fixed code still requires every
admitted file exactly once, injects protected files, derives link rewrites,
renders one immutable preview, executes only after fingerprint-bound human
acceptance, copies into a separate result, and independently verifies the
outcome. No model has source-mutation, acceptance, promotion, receipt, or proof
authority. The older advisory-card and Connected Change roles below are
preserved as explicitly historical evidence; they do not by themselves qualify
the current Foldweave planner or review surfaces.

## First product cycle — 17 July 2026

| Commit | Outcome | Verified checkpoint |
|---|---|---|
| `f1c519d215790d9e9949c5991c96826e5a2e295b` | Established the initial frozen specification, vertical plan, goal, state checkpoint, decisions log, and pre-existing-work boundary. | Governance only; no product code yet. |
| `c177663c59efb22fb85f18d021f850fe396b08b6` | Added the Python 3.11/`uv` project, loopback FastAPI/Jinja shell, Pydantic contracts, CLI, provider boundary, and locked dependencies. | 8 tests plus frozen sync and Ruff checks. |
| `83d64fe361747faef4e340c76a2958736d754e5a` | Delivered the first vertical transaction: synthetic hero package, strict import, stable families, proposals, risk signals, human decisions, copy-only staging, maps, and BagIt proof. | 57 tests. Card behavior was still supplied by test doubles; no live-response claim. |
| `1cce39d8c46c62eef96b9baa64b83d16765d5c03` | Hardened the strict input matrix, budget ledger, evidence cache, atomic promotion, serialized proof read-back, complete map/reference checks, and reverse dry run. | 111 tests. Reproduced false-green paths became regression tests. |
| `819e674ba74fb86d981f390d52214de5b4e4f7a7` | Froze the first complete browser experience, selected-source/output paths, decision evidence, explicit human controls, proof blockers, responsive layout, and one negative fixture. | 116 tests and desktop/narrow browser QA. |
| `d71b0b903a8259b158e1d674c5735edb88a6c665` | Verified the real live card, exact replay, complete hero stage, and release artifacts. | One live provider request; subsequent keyless replays; 116 tests. |
| `79e2836019cc392a02ad0cf04971b091a5c8c8d9` | Completed the first clean-clone release candidate. | Frozen install, tests, Ruff, build, link, secret, replay, live-startup, and browser checks. |
| `827b0f6f93174d3c34aedfd98d8467a299ab2669` | Checkpointed and published the known-good first-cycle release on `main`. | Preserved as the public fallback for the revised cycle. |

### Real GPT-5.6 record

At 20:40:58 CEST on 17 July 2026, one explicit Generate action sent the
displayed bounded hero evidence to the exact `gpt-5.6` model alias through the
OpenAI Responses API. The schema-valid neutral card was generated from 1,676
input tokens and 994 output tokens, 2,670 tokens in total. The application
measured 14.645 seconds of end-to-end latency and estimated USD 0.0382 in model
cost while retaining a conservative USD 0.6790 budget reservation.

The sanitized write-once record has:

- SHA-256
  `2fe0da43fe57e72043effcf13dc3a3084b8a262295e132b00109bf767f06ae00`;
- evidence fingerprint
  `0f0b0b7cf923432431e7d184c6881cb34d61a0e5caf578f87cc029494b97d830`;
- model alias `gpt-5.6`; and
- a visible runtime label of **Recorded GPT-5.6 response** in replay mode.

The record contains possible interpretations, possible meaning loss, explicit
uncertainty, linked evidence IDs, and one discriminating question for the
`campaña` → `campana` projection. It contains no approval field or executable
authority. Two subsequent complete replay transactions ran with
`OPENAI_API_KEY` absent and used the record only after exact model, schema, and
evidence-fingerprint validation.

Exactly one OpenAI provider request was made for this project through this R6
documentation checkpoint. No provider request was made to add case persistence,
receipt binding, independent verification, the five-state interface, restore,
or this release documentation.

## Revised portable-handoff cycle — 18 July 2026

The user authorized an in-place revision whose goal is not another naming
screen, but a complete sender-to-receiver transaction:

`persistent Migration Case → human-reviewed change → Portable Change Receipt → independent keyless verification → bounded logical restore`

The public first-cycle `main` commit remained the known-good fallback while the
revision was built on `revision/portable-change-receipt`.

| Commit | Outcome | Verified evidence |
|---|---|---|
| `fbe6dea2e3755cc25c20202e254bf4f994ed2121` | Refroze the revised contract, delivery plan, goal, state, and decisions without product mutation. | Revised governance baseline with parent `827b0f6`. |
| `ccc5e7d6c50e7a5acc41c97cee8bb439fcc120f5` | Activated the revised build at 00:51:51 CEST. | R+0 and proportional milestone targets recorded. |
| `2495a6fabd38e2695d574c02ac8a8130717eb729` | Added a durable `migration-case.v1`, receipt-bound decisions, initial `portable-change-receipt.v1`, independent verifier dispatch, controlled altered-ledger failure, and the five route skeleton. | 144 tests. Restart preserved the case/card/decision; copied bags verified keylessly; the BagIt-valid altered ledger blocked on `artifact_digest_mismatch:decision_ledger`. |
| `5949a0f3255e181fdde46ca206d86a6c41bb5eb6` | Hardened the Migration Case as the sole mutable authority with strict rehydration, atomic writes, locking, optimistic revisions, source-staleness differences, and finalized immutability. | 184 tests. Added/removed/renamed/resized/content-changed matrices and restart browser QA passed; no API call. |
| `b59b9efd5752b4038c89db6e2b0fd6f19e1b5a47` | Completed path-neutral `v2` artifacts, byte-exact original controls, the non-circular receipt envelope, offline HTML, and the source-free receiver verifier. | 215 tests. Copied handoffs verified with and without the exact source; malformed and cross-artifact false-positive attacks failed closed; no bag byte changed during verification. |
| `0e7543af1f46e06a55ccd22d75c647b44b68d102` | Delivered the connected Atlas, Decide, Stage, Verify, and Handoff workbench with server-owned state and locally packaged Blueprint dark assets. | 241 tests. Browser QA passed at 1440×900, 1000×800, and 390×844; a clean wheel contained the required CSS, icons, license, and notices. |
| `b10445138baf47ee4156a5a5ed151d0cb7819d4e` | Added verify-first `restore-receipt`, strict `restore-report.v1`, exact original-control restoration, complete snapshot proof, and no-replace promotion. | 262 tests. An unmocked restore reconstructed 30 members and 23,621 bytes exactly; source and handoff remained unchanged; isolated-wheel execution and adversarial race/failure matrices passed. |
| `d034b27b8b47224c4f7bff5d8be4717241522618` | Closed R5 and began frozen R6 release hardening. | Feature freeze active; only proof integrity, release QA, documentation, screenshots, rehearsal, and submission preparation remain. |
| `eb54f3a2b3ab60bc690d3151e7f5bce0ad28aa0c` | Hardened the revised release candidate, packaged the hero in the wheel, corrected durable replay restart and installed-wheel source selection, replaced the first-cycle release copy, and installed the seven revised screenshots. | 265 tests; two final independent audits; exact detached clean-clone, build, installed-wheel, complete receipt, controlled-failure, restore, link, license, path, secret, and screenshot checks all returned `GO`. |
| `6591d57e254a21944fb0c4bdfb2f7a4eec18eda4` | Selected the recording-ready release checkpoint with the rehearsed transaction, final R7 package, seven screenshots, and 3:2 thumbnail. | Exact detached local clone and credential-disabled public HTTPS clone each passed frozen install, 265 tests, build, wheel, receipt verification, and keyless five-route replay startup. |

### Historical second-cycle verified checkpoint

Freshly rerun on the revision branch during R6 documentation work:

- `uv lock --check` — passed;
- `uv run --no-sync pytest -p no:cacheprovider` — **265 passed in 12.45s**;
- `uv run --no-sync ruff check .` — passed;
- `uv run --no-sync ruff format --check .` — 54 files already formatted; and
- Python compilation and `git diff --check` — passed.

R6 release hardening found and corrected three judge-path defects without
changing the product contract. The wheel now packages the 30-member hero
fixture; replay startup resumes a durable post-decision case from its already
validated evidence/card binding instead of incorrectly comparing that case with
the pristine pre-decision proposal; and an installed wheel now always selects
its packaged hero even when the invocation directory contains a shadowing
`sample_data/hero` path. One restart regression and two checkout-versus-wheel
path-selection regressions bring the suite to 265 tests.

The current R6 candidate wheel has SHA-256
`1ed641680a164196bf0fc07d894389713d0033ad28ffda27cba7253e2c0e266b`.
It contains 85 entries: all 30 hero members, the recorded GPT-5.6 response, six
templates, 12 static/Blueprint assets, the Blueprint Apache-2.0 license, and the
third-party notice. Scans of unpacked wheel bytes found no sender home or
temporary path, `file://` URI, or key-shaped value.

Installed into a fresh Python 3.11 environment and launched from an unrelated
working directory with `OPENAI_API_KEY` absent, that wheel selected its packaged
hero and recorded card, created a local case, reported exact model `gpt-5.6` and
**Recorded GPT-5.6 response**, and served `/`, `/atlas`, `/decide`, `/stage`,
`/verify`, and `/handoff` successfully. Live startup without a key exited `2`
with the documented local-configuration instruction. Live startup with a
non-secret placeholder exposed exact `gpt-5.6` readiness and the explicit
Generate action without a provider request or budget-ledger creation. A second
isolated-wheel launch from a directory containing a deliberately shadowing
`sample_data/hero` still selected the packaged fixture and reached `/decide`.

The current successful hero handoff verifies source-free and with its exact
source at receipt fingerprint
`1b7f34514a2d1fa390a55c54df89c597d6a33d9b8ef2059d7af55efaf078edc6`.
Its disposable altered-ledger copy remains ordinary-BagIt-valid while the Name
Atlas verifier exits `1` with exactly
`artifact_digest_mismatch:decision_ledger`.

### Exact-commit R6 acceptance and R7 rehearsal

The exact detached candidate `eb54f3a` was installed with Python 3.11 from a
fresh local clone. Its locked environment passed all 265 tests, Ruff
lint/format, compilation, build, and Git checks. The resulting 85-entry wheel
matched SHA-256
`1ed641680a164196bf0fc07d894389713d0033ad28ffda27cba7253e2c0e266b`,
contained the 30-member hero, replay record, templates, Blueprint assets, MIT
license, Apache-2.0 license, and third-party notice, and ran from an unrelated
working directory with no API key.

The primary exact-commit transaction survived process restart and produced
receipt `9279dd11742f73518bf6a27f6a2fa41d3a15659fc3fe27592c6bf8a0499334da`.
Its copied bag verified with and without its source, the exact altered ledger
remained BagIt-valid but blocked only on
`artifact_digest_mismatch:decision_ledger`, and restore reconstructed all 30
members. A separate independent clone reproduced the entire matrix with
receipt `e68229f3cc7d3cef736823a138c3099617e4a325aaaae016e91704141b8bf5f0`,
23,621 restored bytes, unchanged source and handoff, and overall verdict `GO`.

R7 then rehearsed the complete visual transaction at a 1280×720 capture
viewport: Atlas, low-risk batch approval, mechanical collision edit, the exact
recorded GPT-5.6 card, human Meaning edit, Stage, seven-group Verify, Handoff,
and offline receipt. The transaction had no horizontal document overflow and
produced selected recording receipt
`2ba5d8316f970d0a8f220a57fef1b7f77c167213146eeef2639284f251f0509a`.
The copied selected handoff verified in 0.95 seconds; the controlled altered
copy passed BagIt and produced the exact blocker; and restore completed in 0.74
seconds with all 30 source members byte-identical and the copied handoff
unchanged. The continuous visual storyboard remains 0:00–2:45. The actual
voice recording and its final timing remain user-owned.

The code-native Devpost thumbnail is a 1500×1000, 3:2, 210,124-byte PNG with
SHA-256 `1eee93fe81037843ca80453574d9f488a8aef97c0ad542ea615cfcd045a78ca0`.
Its SVG source has SHA-256
`91e1f7eff0159df6417913d3493a330ffef718857839b12e928a9cf8df1b4836`.
It uses only project-native text and vector shapes in the established dark
visual system, and its visible abbreviated digest is the selected recording
receipt `2ba5…f0509a`, not a decorative invented value.

### Public recording-ready release

The selected recording-ready checkpoint is
`6591d57e254a21944fb0c4bdfb2f7a4eec18eda4`, with parent `eb54f3a`. It was
tested first from an exact detached local clone and then fast-forward promoted
normally to both `revision/portable-change-receipt` and public `main`. No force
push, rebase, or history rewrite occurred.

A credential-disabled HTTPS clone from
<https://github.com/ModernBlueprints/reversible-name-atlas> resolved exactly to
`6591d57`. In that public clone:

- `uv sync --frozen --python 3.11` passed;
- all 265 pytest tests passed in 14.18 seconds;
- Ruff lint/format, compilation, and Git whitespace passed;
- the wheel retained SHA-256
  `1ed641680a164196bf0fc07d894389713d0033ad28ffda27cba7253e2c0e266b`;
- the selected receipt `2ba5…f0509a` verified source-free and against the
  exact hero source; and
- keyless replay truthfully reported exact `gpt-5.6`, **Recorded GPT-5.6
  response**, redirected `/` to `/decide`, and served all five workbench routes
  plus local Blueprint and Name Atlas CSS.

An earlier diagnostic invocation cloned the exact commit but did not change
its shell working directory before running the toolchain. No clean-clone gate
was claimed from that run. The complete check was rerun with the clone as the
explicit working directory and passed, followed by the independent public-clone
run above.

The R7 closure after `6591d57` changes only evidence and status in the build
log, submission package, implementation plan, and state checkpoint. It changes
no product code, screenshot, thumbnail, narration draft, or storyboard. Its
exact public HEAD is resolved from fresh Git and reported in the handoff because
a commit cannot contain its own hash.

### Revised screenshot replacement record

R6 regenerated one coherent seven-frame release set from the synthetic hero
transaction at 1440×900. Each final file was converted to genuine PNG bytes and
checked with file-type, pixel-dimension, metadata, personal-path, and secret
inspection. The authoritative paths and SHA-256 values are recorded at
`6591d57e254a21944fb0c4bdfb2f7a4eec18eda4:docs/SUBMISSION_PACKAGE.md`.
Final responsive QA at 390×844 traversed all five routes with zero horizontal
document overflow; the Handoff page retained readable receipt identity,
verifier command, and restore action.

The following five first-cycle captures were then removed from the release
directory because they depict the superseded interface and overlap the revised
set:

| Removed first-cycle path | Bytes | SHA-256 |
|---|---:|---|
| `docs/screenshots/02-decisions-live.png` | 482,121 | `d5b1f66907dcfea4c3c3e191bc0f057a35f6d775672eeafa4c30ff5e8832ba8e` |
| `docs/screenshots/02-live-metrics.png` | 232,533 | `504924debda2a6bd617fd3594e4351bf4f4d4de62c8856adada3ead689e44390` |
| `docs/screenshots/03-decisions-replay.png` | 272,388 | `10ee1acd17a32e4e3a182d8cf86728a49e64a7071ac72ca57f9eff87abb87e37` |
| `docs/screenshots/04-proof.png` | 328,646 | `a550d061e234c21237fa6bf182dad90c8b201e8fce70280efea20263704032ad` |
| `docs/screenshots/05-negative-block.png` | 198,589 | `ae3e876a44db844c70fbdb6066c336ee46f480f94b8e6e9c9ffb7bbb46fe8ab2` |

They remain recoverable byte-for-byte from Git history at the known-good
first-cycle release `827b0f6`; no product evidence or non-regenerable user data
was destroyed.

## Historical second-cycle Codex contribution

This section records the superseded archive-centered second cycle. The current
release division of work is documented later under **Division of work: GPT-5.6,
deterministic code, and Codex**.

The primary Codex task translated the frozen contracts into dependency-ordered
vertical slices, kept one integrated application runnable, delegated bounded
non-overlapping reviews, inspected their findings, exercised the browser and
CLI, reproduced adversarial failures, and converted valid failures into focused
regression tests. The most consequential collaborative decisions were:

- one strict linked-package contract rather than a generic adapter platform;
- a persistent local Migration Case as workflow authority;
- an immutable path-neutral receipt as the handoff boundary;
- deterministic mechanics and human semantic authority, with GPT-5.6 advisory
  only;
- a receiver verifier independent of the sender's case, source, browser,
  network, API key, and GPT;
- a BagIt-valid altered-ledger counterfactual that distinguishes package-byte
  validation from receipt-bound transaction consistency;
- a five-state server-rendered workbench instead of a client-side framework;
  and
- a bounded restore that verifies first and never overwrites a destination.

Codex accelerated implementation, integration, adversarial review, and
regression work. This is a qualitative development-process account. It is not a
percentage, recurring-speed, productivity, or superiority measurement.

## Historical second-cycle provenance and claim boundary

Selected mechanical ideas from a pre-Build-Week feasibility spike were adapted
under the disclosures in [`PREEXISTING_WORK.md`](PREEXISTING_WORK.md). Its
tournament semantic/evaluator machinery was rejected, and the product has no
runtime dependency on the ephemeral spike.

This historical checkpoint did not claim semantic correctness, sender
authentication, compliance, production readiness, universal archival support,
universal reversibility, or measured time savings. Its recording-ready state was
subsequently superseded by the AI-first and Connected Change cycles below. The
submission hold remained active.

## Historical Devpost pre-submission preparation — 18 July 2026

The authenticated Devpost connector identified the existing Reversible Name
Atlas project as software ID `1344382`, slug `reversible-name-atlas`. The
separate historical Preflight submission draft was inspected only as a list
entry and was not changed.

The Reversible Name Atlas project was updated from the first-cycle story to the
exact frozen revised Devpost copy in `docs/SUBMISSION_PACKAGE.md`, including the
new tagline, 4,715-character Markdown source, technology list, and public GitHub
repository link. Devpost rendered the accepted story as 4,676 characters. The
exact 210,124-byte frozen PNG thumbnail with SHA-256
`1eee93fe81037843ca80453574d9f488a8aef97c0ad542ea615cfcd045a78ca0`
was uploaded once through the connector's streamed-file path and its resulting
public image returned HTTP 200.

Post-update semantic verification reported:

- project name `Reversible Name Atlas`;
- tagline `Refactor the collection. Hand over the proof.`;
- public project URL <https://devpost.com/software/reversible-name-atlas>;
- project page state `published`;
- no attached hackathon;
- no video URL; and
- no OpenAI Build Week submission performed.

Both available browser sessions displayed Devpost as logged out, so no optional
gallery upload was attempted. The seven accepted local screenshots remain
ready. The connector independently returned the complete OpenAI Build Week
submission-field schema, but no Build Week category, repository/testing
custom-field answer, `/feedback`, video, country, submitter type, or personal
answer was written or submitted. The final-submit tool was not called.

Immediately before this documentation checkpoint, `uv lock --check`, all 265
pytest tests, Ruff lint, Ruff format, and `git diff --check` passed. This was
pre-submission preparation only. The user's voice recording, `/feedback`,
personal attestations, explicit submission-hold release, and final Devpost
submission remain pending; the hold remains active.

## Historical video-capture preflight — 18 July 2026

The protected submission-reserve work verified the final capture path without
creating or publishing a final video. FFmpeg `8.0.1` detected the macOS screen
capture device and successfully encoded a disposable 0.97-second H.264 test.
That full-display test was deleted immediately after codec, dimensions, frame
rate, and duration were verified so no incidental desktop content was retained.

The safer capture route records only the Name Atlas page viewport. A disposable
browser session produced 1920×1080 page-only frames with no Codex window,
browser chrome, account data, notification, credential, or personal path. A
three-second 30 fps H.264/yuv420p preflight encode passed with SHA-256
`b3f746fe0bf5a7b6a7da2d297f15be44863fda727c25aa19548ffdd7228dd688`.
The corresponding inspected frame has SHA-256
`4e4bf7310f6e92674b78f614f6b142e16c77901bac081896bb9f59c803b9aead`.
Both are retained only in the ignored local
`.name-atlas/video-production/preflight/` workspace.

The preflight rebuilt and installed the exact accepted wheel, whose SHA-256
remained
`1ed641680a164196bf0fc07d894389713d0033ad28ffda27cba7253e2c0e266b`,
from a neutral temporary directory. Keyless replay displayed **Recorded
GPT-5.6 response** and a scratch transaction exercised low-risk approval, the
collision edit, the exact evidence-bound card, the human Meaning edit, copy-only
staging, and the verified handoff. The 48 MB disposable workspace—wheel,
environment, case, stage, raw frames, and full-display test—was removed
afterward; the accepted release and selected receipt were unchanged.

This establishes capture and encoding readiness only. The final recording must
still be timed against the user's actual narration, checked with audio, exported
under three minutes, and watched locally and after public YouTube upload. No
video was uploaded, no provider call was made, and the submission hold remains
active.

## AI-first ordinary-folder cycle — 18 July 2026

The user replaced the manual archive workflow with an automatic ordinary-folder
transaction: describe the change, let GPT-5.6 plan a complete rename/move map,
compile it through fixed rules, ask at most one question, create a separate
result, preserve supported Markdown links, verify it independently, and recreate
the original layout.

| Commit | Outcome | Verified checkpoint |
|---|---|---|
| `ee66128` | Froze the AI-first folder specification and vertical A1–A7 operating scaffold on `revision/ai-first-folder-refactor`. | Governance only; the preceding release stayed intact at `4baec1e`. |
| `5609ca6` | Delivered A1 generic inventory, protected members, stable identities, complete-file compiler, separate copy transaction, and Start/Working/Done shell. | 108 focused and 359 full tests; desktop/narrow browser QA; source unchanged. |
| `04f6b89` | Delivered A2 exact-span Markdown relationships, bounded evidence tools, planner repair/clarification rules, staleness, restart, and one mutation-owning worker boundary. | 242 focused and 502 full tests; zero-question and one-question development transactions; no provider call. |
| `e3803d2` | Completed A3 durable `FolderRefactorJob.v1`, path-neutral artifacts, acyclic receipt, original Markdown bytes, source-free verifier, exact BagIt-valid alteration refusal, and reconstruction. | 129 focused and 590 full tests; receipt `52b4e3f5c15946d4c6940e585cdaec9264f11ab0dc4139afec2129716995f3ce`; exact reconstruction. |

A3 remains the immutable fallback. Its predecessor behavior was preserved rather
than reset or relabeled when the user authorized the Connected Change extension.

## Connected Change cycle — 18–19 July 2026

The final selected profile adds one transferable Name Atlas Change File. Sofia
can plan and verify a connected-folder reorganization once. Martin can apply the
same change to a differently arranged equivalent project without another GPT
call or transfer of project payload bytes. The Change File still discloses
project names and structure, sizes and hashes, supported relationships, the
instruction, targets, and proof identifiers.

| Commit | Outcome | Verified checkpoint |
|---|---|---|
| `4d4f078` | Established the inactive Connected Change operating scaffold. | Governance parent `e3803d2`; no product work. |
| `121789a` | Recorded and pushed the pre-activation preservation checkpoint. | Remote revision branch backed up; `main` remained at `4baec1e`. |
| `92ac783` | Activated C+0 at Saturday 18 July 2026 at 23:31:39 CEST. | Exact branch, timing, and C0 gate recorded. |
| `a5ea342` | Proved C0 and selected `CONNECTED_CHANGE_GO`. | Complete two-layout origin/receiver transaction, deterministic refusals, equal organized-tree commitment, receiver reconstruction, and zero receiver provider/API/budget/external-network use; 636 full tests. |
| `c94c26b` | Completed C1 strict Change File, deterministic matcher, v2 job/receipt provenance, receiver application, source-free verification, convergence, and receiver-specific reconstruction. | 707 full tests plus unrelated-location, restart, staleness, false-summary, and immutability proof. |
| `852fc55` | Completed C2 Home/Organize/Apply/Working/Done, bounded native macOS picker, verified Finder bridge, and truthful receiver journey. | 34 focused and 759 full tests; 1280×720 and 390×844 visual/accessibility QA. |
| `9e8d3db` | Completed C3 final fixtures, two real GPT-5.6 planner transactions, exact sanitized replays, Sofia/Martin convergence, and the final refusal matrix. | 13 focused and 795 full tests; exact live receipts and keyless replay/reconstruction. |
| `bc1898e` | Completed C4 shared seven-tool STDIO MCP server with consent, durable idempotency, restart recovery, and actual Codex invocation. | 12 focused and 807 full tests; Codex task `019f78e6-06d3-72f0-9258-be362118ea2f` invoked `verify_result`. |
| `7314c58` | Added the thin Codex plugin and repository marketplace around the same MCP server. | Clean-clone install, isolated cache equality, fresh-task discovery/invocation, keyless replay, verification, reconstruction, missing-key behavior, and uninstall passed. |
| `0dc4776` | Closed C5 and entered feature freeze early. | 16 focused and 811 full tests; installed-plugin task `019f7916-02e0-7910-a5a6-f190cd21ec21`; release materials marked for regeneration. |
| `20d5627` | Prepared and accepted the Connected Change release candidate. | Exact public HTTPS clone; 818 full and 245 release-matrix tests; wheel, isolated replay, source-free verification, exact reconstruction, final media, claims, and installed-plugin requalification all passed. |
| `e10b09a` | Corrected explicit named-job discovery and selected the recording-ready product. | Independent exact-public-clone qualification; 822 full and 249 release-matrix tests; installed-wheel replay, verification, reconstruction, and exact-path success/retry/corruption behavior passed. |

### Current real GPT-5.6 planner evidence

The final 24-file hero used exact model alias `gpt-5.6` and returned
`gpt-5.6-sol`. It completed in three response turns and 16 bounded evidence
calls without a question, with `store=false`, receipt
`e3e15fb57f396760a53aecf1549cd3ecb0937cf85039e90113d29b4b1f88f9b1`,
and organized-tree commitment
`a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.

The four-file ambiguity transaction completed in three turns and four evidence
calls, asked exactly one question, accepted exactly one answer, retained both
presentations, and produced receipt
`9eba5c8d670106641dec8d6f6dc4366ea12454db2bd7eb8a86f27c2ca7c3b2a7`.

The exact sanitized recordings are:

- `src/name_atlas/recordings/folder_hero_zero_question.json`, SHA-256
  `75a4ab5f6bc41068c666659fb671bfbd1dcee6a24dcbbe67ba16250dca81d6a1`;
- `src/name_atlas/recordings/folder_ambiguity_one_question.json`, SHA-256
  `cf8dc1ad3ad99ed99a2a10d273c713245584c89a34cf547d0a5dd9c23fdd623f`.

Neither recording contains a credential, provider response ID, absolute local
path, protected content, or hidden reasoning. Recorded mode makes no provider
call and fails closed if its fixture, request, schemas, evidence, or replay
fingerprint differs.

The sole cumulative budget ledger is at 9 of 13 provider requests/attempts, USD
9.736060 conservative committed exposure, USD 0.605515 reported estimated cost,
and the unchanged USD 10 cap. The earlier advisory-card request remains included
in those totals. No further live request is required for the release.

### Division of work

Codex was the primary implementation and integration environment. It read the
frozen contracts, implemented the Python modules and tests, maintained the one
branch and state checkpoint, ran the vertical transactions, performed browser
and clean-clone checks, coordinated bounded independent audits, corrected
adversarial findings, generated release documentation, and qualified the shared
MCP and installed plugin. Agent messages and passing unit tests were never used
as completion by themselves; each milestone required its specified
product-native and downstream evidence, relevant regression coverage, visual
checks where applicable, and a coherent commit.

Runtime GPT-5.6 planned the two exact demonstrated origin transactions from
bounded evidence. It did not mutate the source, decide whether its plan passed,
derive byte offsets, write the Change File, apply a receiver change, verify a
result, or reconstruct a folder. Those operations remained deterministic Name
Atlas services.

The receiver-side Change File transaction made no GPT call, required no API key,
made no budget reservation, and made no external network request. The browser
itself still uses loopback HTTP.

## C6 release status — 19 July 2026

Selected profile `CONNECTED_CHANGE_GO` entered feature freeze on Sunday 19 July
2026 at 08:36:26 CEST. C6 accepted exact public candidate
`20d56278d08128de410778b9c5a8f558ce677e29` on Sunday 19 July 2026 at
10:24:03 CEST after regenerating the README, limitations, provenance, build
log, screenshots, thumbnail, narration, Devpost copy, and submission package.

An independent HTTPS clone in an unrelated temporary directory passed
frozen Python 3.11 installation, **818 complete tests**, the separate **245-test
release matrix**, lock, Ruff lint, Ruff format over 154 files, and Git diff
checks. Its 563,515-byte wheel contains 205 members and exactly 53 Connected
Change fixture files; SHA-256 is
`6c976d8e8546d859d8d778c6aa2a9fe65d1c358799128ffc1954433166cbda0b`.
ZIP integrity, console metadata, browser assets, both exact recordings,
notices, licenses, cache exclusion, developer-path exclusion, and secret-pattern
scans passed. From an unrelated working directory, the isolated installed wheel
ran the keyless Home → Organize → Working → Done replay, downloaded
`northstar.nameatlas-change.json`, verified source-free with receipt
`d8419f9baca079d491a4253f6d0738b1def9d8670ab42ba5826714aa7cee1674`,
and reconstructed all 24 files plus one empty directory exactly.

The neutral final Sofia/Martin transaction used separate source commitments
`8afa2f86d2ed2fe5a5b7b935d107351887685310e8c225f3a7d161c20691df69`
and `a1968bf0dc63b8e14fee98c4d041faed385edefa2960b6b217cf48cec064fc3f`.
It produced origin receipt
`6b57e3fb62bed7b22b11912fa01e0b363e9e3e8472e57604f45abda5bb4f9ec1`,
receiver receipt
`15c010e97faf2fa1693abacdddffae86a8374d9bc6184b3a50e2c75a87ee288f`,
Change File fingerprint
`2edbbe336a9f665933c3324045c3da2be967aac668e337b0ad23a71ea56f30f0`,
and shared organized-tree commitment
`a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.
Both source-aware verifiers and exact reconstructions passed. Martin remained
`capsule_applied` with zero provider calls, false API use, false external-
network use, and a byte-identical project budget ledger.

The same candidate plugin was installed from another public clone, matched its
source manifest/config/README byte-for-byte, discovered exactly seven tools,
and passed keyless replay, verification, reconstruction, missing-key behavior,
and uninstall. Fresh Codex task `019f7976-0b6d-7461-ad63-c3519052b06b`
invoked installed `verify_result` successfully. The then-current seven-image
Connected Change gallery, PNG/SVG thumbnail, and 346-word C6 narration draft
passed independent media, metadata, path, secret, and claim review. That gallery
is preserved at immutable predecessor
`1023999f2acc7b806775b407dc01a15af3447e90`; its paths, dimensions, and hashes
are recorded at
`1023999f2acc7b806775b407dc01a15af3447e90:docs/SUBMISSION_PACKAGE.md`.

The release-media replacement removed seven superseded second-cycle PNGs from
the then-current gallery because they showed the archive workflow rather than
the selected Connected Change product: `01-atlas.png` (345,430 bytes),
`02-decide.png` (422,841), `03-stage.png` (200,943), `04-verify.png` (348,416),
`05-handoff.png` (341,384), `06-offline-receipt.png` (334,009), and
`07-negative-block.png` (365,283), for 2,358,306 bytes total. They remain
byte-for-byte recoverable from feature-freeze commit `0dc4776`; the then-current
release at immutable predecessor
`1023999f2acc7b806775b407dc01a15af3447e90` replaced them with the visually
audited seven-frame Connected Change gallery and Sofia→Change File→Martin
thumbnail recorded in that commit's submission package.

## C7 recording-readiness status — 19 July 2026

The complete 1280×720 Sofia-to-Martin recording rehearsal passed through Home,
Organize, recorded GPT-5.6 planning, Done, Change File download, Apply,
receiver-specific matching, independent verification, and reconstruction. The
origin receipt was
`8747992945a9ab6fad5d0dfe67158af2ed4fe78f31b023fd00627198faa3b460`;
the receiver receipt was
`59fd68c71a006d0ab53b07ff05ec85553cf08beeb2e1cc341bea9498345e8fc4`;
both results converged to organized-tree commitment
`a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.
The receiver remained `capsule_applied` with zero provider calls, false API use,
and false external-network use. The 390×844 Done view had no horizontal
overflow, and Martin's reconstruction matched all 24 source files plus the
explicit empty directory.

That rehearsal exposed one release-safe but material usability defect: an
explicit absent `--job` path inherited directory-wide idempotency discovery and
could treat unrelated sibling JSON in a general directory as a durable job.
The transaction failed before result mutation, but it violated the exact named-
path contract. Commit `e10b09a941567d3394c71dbb5dbc3a25c74f1a82`
separated `exact_path` discovery for browser/CLI from strict managed
`jobs_directory` discovery for MCP. Permanent tests now cover unrelated valid
and malformed siblings, byte-identical retry, corrupt and conflicting exact
jobs, browser origin/receiver completion, and managed-directory strictness.

The corrected local checkout passed 55 focused tests, 822 complete tests, the
249-test selected-release matrix, lock validation, Ruff lint, Ruff format over
154 files, and Git whitespace checks. An independent fresh HTTPS clone of exact
`e10b09a` in an unrelated temporary directory reproduced 822/822 and 249/249
tests. Its 563,894-byte, 205-member wheel has SHA-256
`ab055dfeab03b26856b7acb1fcc79baf8da6a328c318640d6aa821b3877112b7`.
An isolated installation ran the keyless replay, verified source-free and
source-aware with receipt
`0cd23b418541b7acad90a271ddaa9b9f2d603ac9f6f53c0b5825a438e652a598`,
reconstructed exactly, and proved the corrected explicit named-job behavior.
No qualification process remained; no credential was loaded, and no provider
call or budget mutation occurred.

The final frozen narration draft contains 344 lexical words (341 whitespace-
delimited tokens). A macOS `say` timing proxy at 130 words per minute lasted
155.120454 seconds (2:35.120), leaving 19.880 seconds inside the 2:55 storyboard
target. That proxy is not the user's final recording or exported video.

The accepted product commit was fast-forwarded without rebase or force-push to
both public `main` and the revision branch. The repository materials now
describe the selected product. No final video has been published, `/feedback`
and the user's voice remain user-owned, and the submission hold is active.

## Live Devpost draft synchronization — 19 July 2026

After the recording-ready checkpoint, the authenticated Devpost connector read
public project `1344382` and confirmed that it still contained the superseded
archive-oriented release story. The connector replaced only the mutable project
copy required for the selected release: final product name and tagline, the
4,568-character Connected Change description, final technology list, and the
public GitHub repository link. Devpost returned project version `3`.

The audited predecessor thumbnail at
`1023999f2acc7b806775b407dc01a15af3447e90:docs/submission-thumbnail.png`
(1500×1000; SHA-256
`0382fd0c9c15a89688b821496b7baad20633bb427cec74383735848327085515`)
was then streamed through Devpost's direct file-upload path. The processed
public thumbnail returned HTTP 200 as a 51,109-byte PNG. A first non-mutating
upload command retained the connector's literal `<FILE_PATH>` placeholder and
exited 26 before reading or uploading any file; the corrected command used the
fixed audited local path and succeeded once. No duplicate project or thumbnail
mutation was created.

A fresh project read confirmed the final tagline, a 4,568-character
description, public state `published`, `video_url: null`, and no hackathon
association. A separate public-page fetch confirmed the final tagline, core
Connected Change copy, repository link, technology list, and new Open Graph
thumbnail were actually rendered downstream. No submission, registration,
personal attestation, `/feedback`, hold release, or video mutation occurred.

## Live Build Week form and deadline readback — 19 July 2026

At Sunday 19 July 2026 at 12:05:52 CEST, read-only authenticated Devpost calls
confirmed that OpenAI Build Week remains open for submissions and the account
is already registered. The separate historical `Preflight` project remains a
Build Week `submission_draft`; Reversible Name Atlas project `1344382` remains
unassociated and unsubmitted. The official rules explicitly permit multiple
substantially different submissions, so the historical draft does not block the
Name Atlas entry.

The complete current submission-form readback requires submitter type (`27945`),
country (`27946`), category (`27947`), repository (`27948`), and primary-task
`/feedback` Session ID (`27950`), with optional judge instructions (`27949`)
and the applicable plugin/developer-tool instructions (`27951`). The frozen
draft maps the product to `Work & Productivity`, the public repository, the
keyless judge path, and the tested plugin instructions. Submitter type, country,
personal attestations, and `/feedback` remain user-owned.

The key-date readback and latest host announcement both confirm the deadline as
Wednesday 22 July 2026 at 02:00 CEST. The required YouTube demonstration remains
absent and must be publicly viewable, under three minutes, and include audio
covering the product, Codex, and GPT-5.6. These calls made no project,
registration, video, hackathon-association, submission, or hold mutation.

## Foldweave native-review cycle — 19–20 July 2026

The user authorized one new implementation branch from the verified Connected
Change predecessor `1023999f2acc7b806775b407dc01a15af3447e90`. The active
product identity is now **Foldweave**, with the tagline **Change the structure.
Keep the connections.** Historical Name Atlas artifacts and schema identifiers
remain strict compatibility surfaces rather than being rewritten.

The new product contract adds four explicit execution modes:

1. native direct `gpt-5.6` planning through the Responses API;
2. ChatGPT-hosted planning using the model supplied by the user's ChatGPT
   session, without a Foldweave Responses API key or direct-budget reservation;
3. exact recorded replay without model inference; and
4. unchanged Change File application without model inference.

Codex is a required access surface over the same host-planning tools and durable
domain services. It does not introduce a separate execution engine or model
provenance category.

### Published branch checkpoints

| Commit | Outcome | Verified checkpoint |
|---|---|---|
| `8eedb02` | Established the Foldweave native-review governance scaffold on `revision/foldweave-native-review`. | Governance only; parent `1023999` and the complete Connected Change release remained intact. |
| `ba37014` | Added review-before-execution for origin and receiver jobs. | Durable job v3, immutable preview DTO, current/proposed trees, no output in `reviewing`, stale/duplicate refusal, exact acceptance, separate verified result, browser/CLI review semantics. |
| `dfa85b4` | Qualified the packaged native direct transaction. | PyInstaller `onedir --windowed` Apple-Silicon app, one FastAPI control plane, focused React review island, native picker, Keychain configure/read/remove, exact live direct planning, one bounded revision, exact acceptance, receipt verification, reconstruction, restart, and clean shutdown. The app is unsigned/ad-hoc, not Developer-ID-signed or notarized. |
| `13fb54e` | Preserved the hosted-review implementation checkpoint. | Bounded host planning, shared ChatGPT widget contract, opaque local handles, truthful `chatgpt_hosted` provenance, provider-free hosted tools, and generated production widget assets. This checkpoint did not claim a completed consumer gateway or public listing. |
| `2322076` | Hardened the Foldweave review authority. | Append-only v3 mutation history, exact-request rehydration, destination reservation, bounded revision recovery, and additional stale, conflicting, retry, and race refusals. |
| `719fc18` | Delivered the integrated native-review and shared-planning checkpoint. | F0a review authority, F0b packaged native direct transaction, F0c actual macOS ChatGPT developer-mode transaction, complete F1 authority, deterministic F2 domain/portability/race matrices, shared MCP/companion/gateway code, and bounded independent authority corrections. The full checkpoint passed 1,102 Python tests, 54 frontend tests, 31 gateway tests, strict TypeScript and production builds; it did not claim live consumer deployment, final live derivative qualification, current Foldweave Codex installed-copy acceptance, or release readiness. |

### Verified implementation at `719fc182`

The checkpoint integrates one deterministic engine across the native app,
browser fallback, CLI, local STDIO MCP, ChatGPT-hosted MCP/widget, and paired
companion boundaries. It includes:

- strict `folder-refactor-job.v3` persistence, immutable
  `folder-plan-preview.v1`, no-output review, bounded sparse revision, exact
  fingerprint-bound acceptance, destination reservation, restart, and strict
  legacy dispatch;
- complete `connected-change-file.v2` derivative children with immediate-parent
  lineage, receipt/verifier v3, organized-tree convergence, and
  transaction-specific reconstruction authority;
- immutable receiver parent jobs and explicit derivative children, including
  deterministic Sofia → Martin → Sofia domain, portability, collision, race,
  compatibility, and reconstruction matrices;
- direct, ChatGPT-hosted, Codex-hosted, replay, and model-free provenance
  contracts that do not collapse planning transport into execution origin;
- one shared purpose-built current/proposed React tree for native/browser review
  and the ChatGPT widget;
- a local STDIO MCP profile for Codex, a loopback Streamable HTTP profile for
  ChatGPT developer qualification, an outbound-only paired companion, and a
  checked-in Cloudflare gateway implementation; and
- a renamed thin Foldweave Codex plugin around the same MCP and deterministic
  engine.

The public-authority implementation received an independent adversarial audit.
That audit reproduced a standalone companion context-loss defect and a raw
capability exposure through MCP results before deployment. The production
companion was changed to use the same in-process ASGI dispatch boundary as the
packaged app, and the raw bearer design was removed: public MCP and widget
surfaces carry only an opaque job ID while the trusted local host rederives and
validates the 30-minute job authority from the immutable device, grant, scope,
and job binding. The re-audit found no remaining HIGH or MEDIUM issue.

Checkpoint verification passed 1,102 Python tests, the 110-test integrated
public-authority subset, 54 frontend tests, 31 gateway tests, strict TypeScript,
the review/widget and gateway production builds, `uv lock --check`, Ruff lint,
Ruff format, and Git diff checks. These checks qualify the integrated code and
tested transactions; they do not substitute for a live consumer deployment.

At publication, the following were outside checkpoint `719fc182`'s claims:
live Cloudflare deployment and consumer OAuth pairing, public ChatGPT
approval/listing, the final real direct and ChatGPT-hosted derivative matrix,
current Foldweave clean-clone installed-copy Codex qualification,
release-candidate acceptance, recording readiness, video, `/feedback`, and
submission. Later evidence is recorded separately below and does not rewrite
what that immutable checkpoint proved.

### Native and browser boundary

The tested native profile is `Foldweave.app` on macOS Apple Silicon. The
pywebview window owns no durable product authority; it presents the existing
FastAPI control plane and a focused React/TypeScript review island. The direct
credential is stored in macOS Keychain and is never sent to the renderer. The
browser fallback and CLI remain supported. No Windows/Linux native, notarized,
Mac App Store, mobile, or remote-phone claim is made.

### ChatGPT and API boundary

ChatGPT subscription access and OpenAI API billing are separate. Native direct
mode uses a user-supplied OpenAI API key and the sole direct budget ledger.
ChatGPT-hosted mode uses the model supplied by ChatGPT and may not silently call
the direct API. Recorded replay and unchanged Change File application remain
model-free. A ChatGPT widget or tool invocation may use gateway networking even
when the underlying unchanged application is model-free.

The actual macOS ChatGPT developer qualification used the official Secure MCP
Tunnel, bounded hosted-planning tools, opaque local handles, and the visible
Foldweave widget. Hosted job `d8392e05e1e841c7850c28c7a6e4ce82` produced a
complete 24-file root proposal, accepted a path-only host revision, rendered
candidate
`5f96104f0c37825e21a389b0024cacd5af84908a9be8b443c1f801cf1319b83f`
and preview
`f9504c0e062cb7ab05b88fe9959f10b878d977e4a5df5b71f5f99f71f835c384`,
and stopped with no output. The visible widget action then persisted exact
`chatgpt_hosted` acceptance and produced a verified separate result with receipt
`e8acaa4b74db7722ff8d39de8bc7a28d8c1a34b9e16dc2eddef6c33d5c778fa7`,
Change File fingerprint
`0bf3caf6bdbbac5657db00af2eee8b7769dbf9d980feb4e3725f19b9abf5538b`,
and organized-tree commitment
`c234aabe97f7cccfaf6b8c025a2b34c2d4b50a4c350ba52245b8941ac8d6158e`.
Widget verification, Change File retrieval, reconstruction, independent CLI
verification, and exact source/reconstruction comparison passed. The sole
direct ledger remained byte-identical; no direct request, budget reservation,
hidden fallback, or fabricated direct metadata occurred.

This establishes `DEVELOPER_MODE_VERIFIED`, not consumer distribution. The
public gateway, consumer pairing, publication readiness, review submission,
approval, and public listing remain separate evidence gates.

### Post-checkpoint derivative, replay, and preflight evidence

After `719fc182`, the mandatory live derivative matrix completed without
changing the deterministic engine. Direct derivative job
`9ac2c69a75d44ba1b0a7f21a873dd342` and actual ChatGPT-hosted derivative job
`6af720f18400471098cb52e3e4af52e7` compiled the same candidate
`f4e79b7c377a73e3206049a8dccd40ce5334a201478d2d2be7067a23f24f793b`.
The direct job produced receipt
`a5f5eb43ae6889d56aaecef5a4464c7a1ed23a8db66d7b711899f954f77dc2e2`
and self-contained child Change File
`dcc3cc4d746564edc56cce28689e6e006541e2779dabf1166a9ffb83386e3b06`.
Its exact preview fingerprint was
`77d91a7e3fb28807bc9ea251fccd4baf593adc53f632e416b2bd15c6f19da628`,
and its receiver-specific reconstruction was path-and-byte identical to
Martin's selected source.

The actual macOS ChatGPT v17 widget rendered Martin's complete current tree
against the shared derivative proposal and executed only after the visible
**Accept this structure and create copy** action authorized preview
`668d613e6701b35d821a4a6dbde4da5d26cc6beb05ec9d41346d81865a43cb38`.
The immutable parent remained in `reviewing` without authorization or result.
The verified child records `gpt_revised_from_change_file`, planning basis
`derivative`, model transport `chatgpt_hosted`, provider-call count `0`, and
direct API use `false`. Its receipt is
`56468fd0d0a4c5dd715c5102f3b7d7fedae8e3a70077d3a0fd81f040e3fee0d3`;
its self-contained child Change File fingerprint is
`c54c20cd77d9386e9b52327fa88e84e2da87433fb437b520d02062c6098c06c6`.
Widget verification, opaque-handle Change File retrieval, and receiver-specific
reconstruction passed.

Both live transports converged to organized-tree commitment
`0ea8201ec6123615f9ab9028cb89a64027d63288f88041b4de209612623cc830`.
The hosted reconstruction is path-and-byte identical to Martin's selected
source. An independent read-only audit revalidated source immutability, BagIt
manifests, all 21 receipt artifact commitments, the acyclic
parent/Core/receipt/envelope proof graph, immediate-parent lineage,
self-contained CF2, and absence of payload bytes, absolute paths, and secrets in
the transferable artifact. No material defect remained.

A fresh keyless replay job `daeea1fc54c6472c8b74a0b027f04259` reached review,
accepted exact preview
`5e8729f9da5ae923fbc28d10d26d5604933dfa4329e62e02e9c89d97aa05d074`,
verified receipt
`c8020a10ef72fd4c5590fb09246427c69897cb6603448a6b850525b315548e10`,
correctly refused a relative reconstruction with
`destination_must_be_absolute`, and then recreated its selected source at a
valid absolute destination.

The sole direct ledger is schema `gpt-budget.v1`, model `gpt-5.6`, monetary cap
USD 40, call cap 16, 14 requests/attempts reserved, USD 13.057830 conservative
exposure, USD 0.895450 reported estimated cost, and SHA-256
`d76924e416de3e8a6f4cd7878399f9d54d711b1fadd6fa57dd524264ebd21af9`.
The ChatGPT-hosted derivative left those bytes unchanged.

At that F2 checkpoint the integrated preflight passed 1,176/1,176 Python tests, 80/80
frontend tests, 50/50 gateway tests, `uv lock --check` with 63 packages, Ruff
lint and formatting over 224 files, strict TypeScript, both frontend production
builds, exact generated review/widget asset parity, the Wrangler production dry
build, and Git diff checks.

Wrangler subsequently authenticated through the user-approved Cloudflare flow,
production and preview `OAUTH_KV` namespaces were bound, and public Worker
deployment version `fb97746a-8d6c-497c-aa48-29ecd798dff3` was created on Monday
20 July 2026 at 13:46:59 CEST with both SQLite Durable Object bindings and the
production KV binding. This proves deployment existence only. It does not yet
prove consumer OAuth, one-time pairing, outbound WSS, reconnect, complete
origin/receiver derivative transactions, `CONSUMER_PAIRING_VERIFIED`,
`PUBLICATION_READY`, approval, or public listing.

### Binding visual-acceptance correction

The user explicitly rejected the current gradient-heavy, cyber-like Foldweave
presentation as unacceptable. Functional UI implementation and automated
component checks are not visual acceptance. Before F3 can complete, every
active native, browser, review, settings, pairing, Done/proof, and ChatGPT
widget surface must use one restrained, minimal, recognizable macOS-native
visual system with native/Blueprint interaction patterns and no gradients,
neon glow, cyber styling, or decorative visual noise. The transformed surfaces
must then pass real 1280 x 720, approximately 1440 x 900, and 390 x 844
viewport inspection plus keyboard, focus, overflow, contrast, and accessibility
checks. No current screenshot or generated bundle is recorded as visually
accepted.

### Current primary commands

- `uv run foldweave app`
- `uv run foldweave app --browser`
- `uv run foldweave demo --mode replay`
- `uv run foldweave run --mode live|replay --source SOURCE [--output OUTPUT]
  [--job JOB]`
- `uv run foldweave apply-change CHANGE_FILE --source SOURCE [--output OUTPUT]
  [--job JOB]`
- `uv run foldweave preview JOB [--json]`
- `uv run foldweave revise JOB --instruction TEXT --idempotency-key KEY`
- `uv run foldweave accept JOB --preview-fingerprint SHA256
  --idempotency-key KEY`
- `uv run foldweave verify-receipt RESULT_BAG [--source SOURCE]`
- `uv run foldweave restore-receipt RESULT_BAG RESTORE_DESTINATION`
- `uv run foldweave mcp --transport stdio`
- `uv run foldweave mcp --transport streamable-http --surface
  chatgpt-hosted`
- `uv run foldweave companion register|approve|run|status|revoke`

`run` and `apply-change` prepare jobs for review. Neither command executes
without a later exact `accept` action. The legacy `name-atlas` command and
historical `*.nameatlas-change.json`/v1/v2 artifacts remain available through
strict legacy dispatch.

### Privacy and proof boundary

A Foldweave Change File contains no project payload bytes. It does disclose
names and structure, file sizes and hashes, supported-link relationships, the
instruction, targets, immediate-parent lineage, and proof identifiers. Live
planning sends bounded selected evidence. `store=false` is not a zero-retention
claim. A receipt proves internal consistency against its commitments; it is not
a signature, sender authentication, authorship proof, institutional approval,
or tamper-proofing claim.

### Historical release and submission status — superseded checkpoint

This paragraph records the pre-F3/F6 status that existed before the later
post-qualification record below. It is retained as historical evidence only and
must not be read as the current release state. At that superseded checkpoint,
the state was: product
release candidate `4e9ec44b02b25f515017ceb9922fff4fdf84ae46` accepted on the
published revision branch; technical ChatGPT state
`DEVELOPER_MODE_VERIFIED` / `CONSUMER_PAIRING_VERIFIED` /
`PUBLICATION_READY`; and no ChatGPT review submission, approval, publication,
public listing, final video, `/feedback`, personal attestation, hold release, or
Devpost submission was claimed.

### Historical post-checkpoint visual, native, gateway, and Codex qualification

The binding visual correction completed after the earlier rejection. Active
native, browser, review, settings, pairing, Done/proof, and ChatGPT widget
surfaces now use one restrained macOS dark utility language. Authored surfaces
contain no gradients, glow, text shadows, cyber palette, decorative full-width
rules, or card-grid ornament. Remaining separators are limited to functional
toolbar, split-view, Finder-row, disclosure, and settings-group boundaries. The
500-file/1,000-directory review fixture passed changed-only default, search,
selection, scroll retention, structure toggle, arrow-key navigation,
empty-directory filtering, and narrow acceptance. Measured contrast was 15.63:1
for primary text, 8.28–10.10:1 for muted text, and 5.57:1 for white action text
on system blue. The earlier visual-polish run passed 27 visual/native tests and
57/57 frontend tests; the later fresh release reproduction passed 80/80 frontend
tests. This is objective visual conformance, not a claim of any one person's
subjective final-pixel preference.

The earlier local rebuilt 55 MiB Apple-Silicon `Foldweave.app` had bundle ID
`com.modernblueprints.foldweave`, version `0.1.0`, minimum macOS `13.0`, and
executable SHA-256
`c999a68c82268d1fa40ba3c3c5e3cf327218c1502a8423fb0cadd1be48331032`.
It is retained as historical qualification evidence. The fresh clean-clone
release reproduction built the corresponding 55 MiB arm64 app with executable
SHA-256 `3a2bd5ed0eeca704fe8aed2c30652e18aedc088ebb65d5ec5a66d9d8031d1976`.
Strict deep ad-hoc signature verification, 30 focused native/package tests,
launch from an unrelated directory, ephemeral-loopback health, native picker
cancellation and selection, temporary Keychain roundtrip and removal, durable
review rehydration, exact acceptance, Done, Verify Again, CLI receipt
verification, no runtime Node, and no-orphan-process checks passed. Gatekeeper
rejection is expected because no Developer ID or notarization is claimed.

At that checkpoint the full integrated Python regression passed 1,176 tests with one
upstream warning. The frontend passed 80/80 and the gateway passed 50/50 tests;
strict TypeScript, production builds, lock validation, Ruff lint and format,
generated asset parity, and Git diff checks passed. The sole direct ledger remained
byte-identical at SHA-256
`d76924e416de3e8a6f4cd7878399f9d54d711b1fadd6fa57dd524264ebd21af9`:
USD 40 ceiling, 14 requests/provider attempts, USD 13.057830 conservative
exposure, and USD 0.895450 reported estimated cost.

The deployed public Worker at that checkpoint was deployment
`d14d051d-8920-44ea-b336-f3bbea2f6936`, version
`9ac88da8-9f85-4685-8a07-073d44b909b9`, at
<https://foldweave-gateway.skybert-ghostline.workers.dev>. Its health endpoint
reports ready with device-session, pairing-directory, and OAuth KV bindings.
It serves `review-v35`; the exact deployed/local widget asset identities are
CSS SHA-256
`666df057a85df92cfdd57228ef9fc1a8ece31cd65807720695d14dbd867ca173`
and JavaScript SHA-256
`3ac8e6c83350e1d88145d50470a90cb3b2763386aee816986139e611f3ac4bea`.
The Codex in-app Browser remains blocked at its client policy layer, but the
user-requested Google Chrome route completed the live consumer qualification
without weakening OAuth or changing the gateway.

Foldweave Codex plugin `0.1.0+codex.20260721091729` is installed and enabled
from the repository marketplace. The installed cache copy was inspected, and
the declared stdio MCP command initialized as `Foldweave` and returned 22
bounded tools through `tools/list`. This qualifies the current plugin bundle and
local MCP contract. Clean-clone plugin validation and stdio MCP discovery also
passed from release-candidate commit
`4e9ec44b02b25f515017ceb9922fff4fdf84ae46`.

The Foldweave branch remains pre-release. Release-candidate product commit
`4e9ec44b02b25f515017ceb9922fff4fdf84ae46` is selected and the revision branch
is published with release-state documentation. No ChatGPT review submission,
approval, publication, or public listing; Developer-ID/notarized distribution;
final video; `/feedback`; eligibility or ownership attestation;
submission-hold release; or Devpost submission is claimed. The submission hold
remains active.

### Live Google Chrome consumer qualification and widget compatibility

The Codex in-app Browser continued to reject the public `workers.dev` hostname
with `ERR_BLOCKED_BY_CLIENT` before Foldweave or ChatGPT could handle the
navigation. Google Chrome was therefore used as the user-requested supported
browser workaround; no browser-policy bypass, DevTools injection, alternate
gateway, or weakened OAuth control was introduced.

The existing ChatGPT consumer connector completed OAuth and reached the paired
outbound Foldweave companion. Native selection returned only opaque handles for
the 24-file Sofia source and an empty output parent. ChatGPT then used bounded
host-planning tools to create durable hosted root job
`976daca126a648a8bee4a5a4d62b6f8c`, inspect the complete eligible inventory and
supported links, and stop in `reviewing` before any output.

The first preview render exposed a separate product defect. ChatGPT had cached
`ui://foldweave/review-v31.html`, while the gateway at that qualification
checkpoint accepted only canonical `ui://foldweave/review-v33.html`. The
gateway then kept v33 as the
sole advertised template and admits only the explicit known v31 and v32 aliases
for `resources/read`, echoing the requested URI while serving the then-current
v33 assets. Unknown resource URIs remain fail-closed. Deployment
`ece68561-0740-47d3-9052-4e311cabf483` was live at the stable `workers.dev`
endpoint. Live ChatGPT retry rendered the Foldweave widget successfully.
Unauthenticated and authenticated OAuth-MCP regressions cover both aliases.
Gateway TypeScript, all 50 Worker tests, and the Wrangler production dry build
passed. Frontend TypeScript, all 76 component tests, and both production builds
also passed; the deployed v33 JavaScript and CSS bytes matched the then-current
local production assets exactly.

The widget submitted one revision instruction and the standard `ui/message`
request was acknowledged and visibly inserted into the ChatGPT transcript. The
observed host did not autonomously call `submit_plan_revision`, so Foldweave
does not claim seamless component-authored continuation. The exact continuation
was sent once through the same ChatGPT conversation; the host then called the
revision tool once. Job revision 9/proposal revision 1 returned to `reviewing`
with candidate
`70dc934a8f2b60089b24284712e7b6c22dc6e331c89ef52aa094a1b0148c3bef`
and preview
`b637ce35087b97fa60dd407351a6d0ddf28a4f6fc1a50be777bf6af4efe8dbca`.
The requested delivery-notes move is present and the complete candidate still
contains 24 mappings.

The live widget's **Accept this structure and create copy** action then persisted
exact `chatgpt_hosted` authorization for that candidate and preview. Job revision
11 is `verified`; the separate result contains all 24 source files and 23
changed paths. Its Change File fingerprint is
`84b7931453b1b6fb37796f9ccd6a0a7796a4554580e567b528e0cf3a19c1ab97`,
organized-tree commitment is
`2deba61e0aae9004f68e7b5ca185d5efc72f34e9dfa47407744766e4df7810ba`,
receipt fingerprint is
`9a0d4d0b67c7afbc6dcfc2837188263253e5979edbba946a241412b597d82d68`,
and verification fingerprint is
`0e5f5e519ce58a1a5f25d4f447372a8e108505ce5c21de4da4afaab6fd7fdfc6`.
Both source-free and source-aware CLI verification returned `VERIFIED`.
Reconstruction produced 24 files and `diff -qr` proved exact path-and-byte
equality with the selected source. Provenance records zero provider calls. The
sole direct ledger remained byte-identical at SHA-256
`d76924e416de3e8a6f4cd7878399f9d54d711b1fadd6fa57dd524264ebd21af9`.
This qualifies Chrome recovery, consumer OAuth/paired planning, widget
rendering, durable hosted revision, exact consumer-origin acceptance, verified
output, and reconstruction. It does not yet qualify automatic component-authored
continuation, receiver derivative, reconnect/refusal behavior,
`CONSUMER_PAIRING_VERIFIED`, or
`PUBLICATION_READY`.

### Live consumer receiver review and derivative acceptance

The verified consumer-origin Change File, Martin's differently arranged source,
and a new empty receiver output parent were selected through native pickers and
resolved to three opaque companion handles. The public gateway and ChatGPT saw
no absolute path. Deterministic receiver job
`c7ead78db18a4c84b6043006445050b0` matched all 24 files plus the protected
empty directory, stopped in `reviewing`, and rendered the required **Your current
folder / Shared proposal** widget. The trust strip reported source unchanged,
24 files, one protected file, one empty directory, 23 changed paths, 23 supported
links, 23 link updates, and output not created. Source commitment
`a1968bf0dc63b8e14fee98c4d041faed385edefa2960b6b217cf48cec064fc3f`
differs from Sofia's origin commitment, while match-report fingerprint
`8e91d21779d8d773ff42f7ad6fd755effc0143f8e62c873f23ccbcddddd51ac2`
binds the receiver-local bijection.

Martin requested that `Apollo-project-notes.md` move into
`01_project-brief`. The widget preserved the parent review and reserved immutable
child `90a548520b3e4672825de9ffcff0636a`. As in the consumer-origin case, the
component-authored `ui/message` was acknowledged but needed one explicit
same-conversation continuation. ChatGPT then called the derivative revision tool
exactly once. The complete replacement proposal returned to review with candidate
`ad1c86aa7044a4a4279b860d85b2a219b7ec0103c4b2750d5904f1b2df0073d3`
and preview
`e69bb1992a214352c0e0958bd830cc0ad8e7fb15124327771e7f23f6bcba3c5d`;
no output existed before acceptance.

The live widget's **Accept this structure and create copy** action persisted
exact `chatgpt_hosted` authorization and advanced the child to revision 3
`verified`. The separate result contains 24 files and 23 changed paths. Its
generation-one Change File fingerprint is
`ab28b4440ec976e337e567c5746e9d07ebe59faff270b8822421118f52e8ce2c`,
organized-tree commitment is
`20a71d110bcdedce603eacd1b69f517f88bac18d37fb702f1790c77430323b6e`,
receipt is
`6447e9d1a5a1afa49126dd6e8e673f3b757c37245638a4b444606022be5b484a`,
and verification is
`40b23f6fa6470acdfc886e6cc63f558302bed1d2152e6fcf752e1c2a6d09e1d5`.
Source-free and source-aware verification both returned `VERIFIED`; receiver
reconstruction produced 24 files and was path-and-byte identical to Martin's
selected source. The execution origin is `gpt_revised_from_change_file`, model
transport is `chatgpt_hosted`, provider call count is zero, and the direct ledger
remained byte-identical. The child Change File is self-contained and records
immediate-parent lineage to Sofia's origin Change File without embedding the
ancestor envelope.

This completed the positive live consumer origin and receiver-derivative
transactions. At this intermediate checkpoint, reconnect and live refusal
checks still gated `CONSUMER_PAIRING_VERIFIED` and `PUBLICATION_READY`; the
immediately following qualification closed those gates.

### Live consumer disconnect, reconnect, and refusal qualification

The standalone outbound companion was stopped at a quiescent boundary without
revoking the grant, changing the deployed Worker, or re-pairing the device. One
actual ChatGPT `job_status` call for verified derivative job
`90a548520b3e4672825de9ffcff0636a` while the companion was offline returned a
bounded upstream `502`. The consumer-root job, derivative job, 23-job inventory,
49-file result, and direct budget ledger remained unchanged.

Restarting the exact same companion established one authenticated outbound TLS
connection using the existing pairing. The same ChatGPT conversation re-read
the derivative as revision 3/proposal revision 1 `verified` with model transport
`chatgpt_hosted`. A post-reconnect `verify_result` returned `verified`, receipt
`6447e9d1a5a1afa49126dd6e8e673f3b757c37245638a4b444606022be5b484a`,
and organized-tree commitment
`20a71d110bcdedce603eacd1b69f517f88bac18d37fb702f1790c77430323b6e`;
local source-free verification returned `VERIFIED` for the same receipt.
Consumer-root SHA-256
`f2699251540b8fb0afefd53b19a582ff174f4b3219998ef4513bfd975465efcd`,
derivative-job SHA-256
`62f860e36ca1e3b2bae176de039cb38f1f7eaf80f171806c22ae1c6ab23ef848`,
and direct-ledger SHA-256
`d76924e416de3e8a6f4cd7878399f9d54d711b1fadd6fa57dd524264ebd21af9`
were byte-identical before, during, and after reconnect.

A deployed unauthenticated `tools/call` returned a bounded 471-byte MCP
`isError` result carrying the correct protected-resource challenge,
`foldweave.review` scope, and `insufficient_scope`. One authenticated
nonexistent-job request returned sanitized `job_status_unavailable`. The 50/50
gateway and 107/107 companion/hosted suites cover the destructive lockout,
rate-limit, expiry, replay, wrong-device, revocation, and duplicate-request
cases that were deliberately not induced against the sole live pairing.

This completes F0d and establishes `CONSUMER_PAIRING_VERIFIED` plus the narrow
`PUBLICATION_READY` technical state. It does not claim review submission,
approval, publication, public listing, or seamless automatic component-authored
revision continuation. The live `ui/message` acknowledgement still required
the explicitly documented same-conversation recovery, which completed one and
only one durable revision.

### Historical post-qualification release checkpoint

At this intermediate checkpoint, after the Chrome consumer transaction and
reconnect/refusal qualification, the
gateway was rebuilt and redeployed as deployment
`d14d051d-8920-44ea-b336-f3bbea2f6936`, version
`9ac88da8-9f85-4685-8a07-073d44b909b9`. The stable health endpoint reports
ready with all three required bindings. The deployed `review-v35` widget assets
match the local production bytes exactly: CSS SHA-256
`666df057a85df92cfdd57228ef9fc1a8ece31cd65807720695d14dbd867ca173`
and JavaScript SHA-256
`3ac8e6c83350e1d88145d50470a90cb3b2763386aee816986139e611f3ac4bea`.

The regression floor at that checkpoint was 1,176/1,176 Python tests with one upstream
warning, 80/80 frontend tests, and 50/50 gateway tests. A focused post-template
native/pairing/visual/package matrix passed 35/35; Ruff lint, Ruff format, and
Git diff checks also passed. The fresh clean-clone rebuilt arm64
`Foldweave.app` is an unsigned/ad-hoc judge artifact with executable SHA-256
`3a2bd5ed0eeca704fe8aed2c30652e18aedc088ebb65d5ec5a66d9d8031d1976`; its
installed wheel SHA-256 is
`c510b708c715aa59e1453a8ed5f7254372bc85d280fd490f339c6298732ad276`.

The Foldweave release-image and thumbnail evidence at that checkpoint was
captured and
hash-recorded:

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

Final release-artifact inspection found that the original bytes behind the
`.png` filename for `03-origin-review.png` were JPEG-encoded. The capture was
decoded and losslessly re-encoded as genuine PNG bytes; a decoded RGB
pixel-equivalence check preserved its 1728×940 rendered content exactly. The
table records the normalized asset's new size and SHA-256. No product state,
claim, or visual content changed.

The final gallery contact-sheet review confirmed that the nine UI captures, one
installed-copy Codex evidence card, and thumbnail retain the intended restrained
macOS dark visual language, readable controls, and no stale Name Atlas,
gradient, neon, or cyber-dashboard surface. The evidence card is not a literal
Codex UI screenshot.
The exact 317-word narration was also rendered through a local macOS
synthetic-speech preflight: 150.304 seconds at 125 words per minute and
148.652 seconds at 130. Those results validate the script's timing margin only;
they are not a substitute for the user's final voice, the final encoded video,
or public playback verification.

The official Build Week rules, FAQ, and dates page were rechecked during this
pass. They continue to require a working Codex/GPT-5.6 project, a public
repository, a public YouTube demonstration with audio below three minutes, the
primary `/feedback` Session ID, and no submission edits after the July 21 17:00
PDT deadline (Wednesday 22 July 2026 at 02:00 CEST). No Devpost or submission
state was modified by that recheck.

These were the published `main`/revision-branch and deployed-service identities
at that checkpoint. A fresh unrelated clean clone of the published revision branch
reproduced the accepted product candidate with `uv sync
--frozen`, 1,176 Python tests with one upstream warning, `uv lock --check`,
Ruff lint/format, Git diff checks, frontend TypeScript, 80 Vitest tests, both
frontend production builds, gateway TypeScript, 50 gateway tests, Wrangler
dry-run build, plugin validation, and stdio MCP initialization/tool discovery
with 22 bounded Foldweave tools.

The same clean clone built wheel SHA-256
`c510b708c715aa59e1453a8ed5f7254372bc85d280fd490f339c6298732ad276` and
the 55 MiB arm64 app executable SHA-256
`3a2bd5ed0eeca704fe8aed2c30652e18aedc088ebb65d5ec5a66d9d8031d1976`.
`codesign --verify --deep --strict --verbose=2` passed. The packaged app opened
from an unrelated directory, rendered its native Home and an existing review
job, correctly exposed the Original/Proposed toggle and exact acceptance
control, then shut down without its runtime lock or an orphaned clean-clone
process. The review job was not accepted in that visual check.

A fresh keyless origin replay and model-free Martin receiver application both
stopped in review, accepted the exact preview, verified source-free and
source-aware receipts, and reconstructed their respective selected sources.
The origin Change File fingerprint was
`940774830794366ce6c27bd6365629c6efed6a18461a3303298f295420efc214`, its
receipt fingerprint was
`f24ca69126ba56b8aa950fe0056b9494aab6bb11c945da256f867e6ea23f5fd8`, and
the receiver receipt fingerprint was
`b00296cbd83a5cf9daad1f00400e41ed9759dbda21bce797cc852967c0c37169`.
Both results committed organized tree
`a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.
The receiver provenance was `capsule_applied` with zero provider calls, API
use `false`, and external-network use `false`. An isolated environment with
only the built wheel repeated the keyless origin review, acceptance,
verification, and reconstruction.

The accepted release evidence is fast-forwarded to public `main`. Final media,
video, `/feedback`, personal attestations, explicit hold release, and submission
remain pending. No ChatGPT review submission, approval, publication, or public
listing is claimed. The submission hold remains active.

### Final agent-controlled recording-package closeout — 21 July 2026

The judge-facing documentation checkpoint
`d5702e1665c1ddb2b88ac68d902e9d6bc63304fd` was fast-forwarded without force to
both public `main` and `revision/foldweave-native-review`. A new unrelated public
`main` clone then installed with `uv sync --frozen` and ran the README's exact
keyless transaction. It materialized the disposable 24-file Sofia fixture,
stopped in `reviewing`, served the Foldweave review page on loopback, and exposed
the immutable preview endpoint. CLI exact acceptance of preview
`a361edc8f0f3e9a910481897c1ef8a3cac6ff293ace8e92f09bfcd918173d4b0` produced
a separate verified result with receipt
`eb328314e777c332754e27a538c9a16a159f8c571fbfcc0114786e385a1af257`.
Source-aware verification and `diff -qr` reconstruction proved the selected
synthetic source's paths and bytes exactly. The temporary loopback server shut
down cleanly after the inspection.

The final README now discloses the constrained project-selection tournament that
preceded product implementation. It is correctly described as a Build Week
decision aid that tested candidate directions against feasibility, user value,
track fit, and demonstrability. It is not Foldweave runtime code; its semantic,
scoring, evaluator, and transport machinery is excluded. The Foldweave demo
fixtures are also now described truthfully as synthetic predecessor material used
by the current release, with original Name Atlas labels retained only where
strict provenance or compatibility requires them.

The agent-controlled public project preparation is complete without a Build Week
submission: Devpost project record `1327974` now contains Foldweave project copy,
the public repository link, technology list, and the verified current thumbnail
(`b67e2f845857851fc31335ab85b9634a9f8acf9f65bdc6c95e547030876e7cb6`). Its
Devpost-provided `preflight-8s9awt` slug remains unchanged; no unsupported slug
mutation, category selection, personal form entry, or submission was attempted.
GitHub public metadata now identifies Foldweave as a review-and-verify connected
folder product and carries current product topics.

This established `RECORDING_READY` only in the narrow, governed sense: the
accepted Foldweave product, public repository, keyless judge path, release images,
frozen 317-word narration, 11-shot 2:55 capture plan, and timing-margin
preflight are ready for the user's recording work. It does not establish a user
voice recording, a public YouTube video, `/feedback` Session ID, personal or
legal attestation, release of the submission hold, or a Devpost submission. All
of those remain pending and the hold remains active.

### Primary `/feedback` Session ID captured — 21 July 2026

The user ran `/feedback` in the primary Codex build task and supplied the exact
Session ID. It is retained in an ignored, owner-only local submission record for
required Devpost field `27950`; public release files record its captured status
without duplicating the identifier. The authenticated Devpost connector updated
project `1327974` to version `6`, then a minimum-disclosure correction removed
the identifier from its public description in version `7` while preserving the
repository and keyless judge guidance. Connector readback retained an empty
`video_url` and a Build Week association with `submitted_at: null`. The public
video, personal form and legal attestations, explicit submission-hold release,
final Devpost submission, and confirmation remain pending. Capturing the Session
ID did not release the submission hold.

### Final UI, packaged-runtime, and release verification — 21 July 2026

The user identified concrete residual UI defects across Organize, Apply,
ChatGPT, Settings, and the hosted review widget: field legends intersected
their controls, manual-path labels lacked breathing room, pointer clicks drew
blue focus boxes or a stray line on empty space, and the closed/open Key storage
disclosure did not retain one alignment. The correction preserved keyboard
focus while removing pointer-only focus decoration. Fieldset surfaces now sit
inside their labelled containers, pointer and keyboard modality are tracked at
the document boundary, disclosure layout is stable in both states, and the
public ChatGPT widget uses the same focus-origin rule. No workflow or proof
authority moved into the renderer.

The packaged `/pairing` route exposed a second root cause during final QA:
noninteractive Keychain and companion probes could wait on an unavailable UI
credential surface. The Python runtime now fails closed and promptly in that
context while preserving normal native Keychain behavior. Product corrections
were committed as:

- `c84780fbab6da859352624e9e713a26ce385929c` — `fix: polish Foldweave native UI and runtime`;
- `68aba38a643d95f69e9aacd392904ef310f6994c` — `fix: remove hosted widget pointer focus outline`.

Rendered geometry and computed-style inspection at 1280×720 established zero
legend/control overlap on both Organize and Apply, a 7.6875-pixel manual-label
gap, no pointer outline or shadow on disclosures or blank-space clicks, stable
Key storage position across closed/open states, no horizontal overflow, and no
pointer outline on ChatGPT's How planning works or Advanced disclosures.
Keyboard-visible focus remains available. The rebuilt packaged app rendered
Home, Organize, ChatGPT, and Settings, returned every tested route in less than
20 milliseconds, exited with status zero, and left no server process or
listener.

The final public Worker version is
`77598fb6-72e4-48ee-919e-27488a60a515`. It serves `review-v37`; deployed bytes
match the checked-in production assets exactly: CSS SHA-256
`606dcee47981ac80cdb0a9bcbcc9f082d5bfb84087716ad8bbcbea5dd6b3b323` and JavaScript
SHA-256 `3ac8e6c83350e1d88145d50470a90cb3b2763386aee816986139e611f3ac4bea`.
The public health endpoint reports ready with all three required bindings.

A fresh unrelated clone at exact implementation checkpoint
`68aba38a643d95f69e9aacd392904ef310f6994c` passed `uv sync --frozen`,
`uv lock --check`, 1,184 Python tests with one upstream Starlette deprecation
warning, Ruff lint and format over 224 files, frontend typecheck, both production
builds and 80/80 tests, gateway typecheck, 50/50 tests, Wrangler dry-run,
generated-asset parity, and Git diff checks. It built a 55 MiB arm64
`Foldweave.app` whose executable SHA-256 is
`1c2316e26a23ecc9d3608e37d8a6ebf23ee2c128f468a9ec68018cf54cc606d4`, and a
wheel whose SHA-256 is
`7de05603f9be06627888f8369581a987693ad69b7e9ca1dd340cf78414c1df07`.
The app has bundle identifier `com.modernblueprints.foldweave`, version `0.1.0`,
minimum macOS `13.0`; strict deep ad-hoc signature verification passed. It is
still truthfully unsigned and unnotarized.

The same clean clone completed a fresh keyless origin and model-free receiver
transaction. Origin job `4aa71552bffa422c9b997724a713cfb1` produced Change
File fingerprint
`9cadf68fe3207e6de89a2fd3b1fd7ed3d97cb7a1d41dfba483911e4f507d79e0` and receipt
`0e33b16b6a7dc26cd171def18b0a01eaf0098315f32e154915373ff5cd6fcd1b`.
Receiver job `d4a8588ab2a843b9b3937a1885e9691d` produced receipt
`c0122b6ee7ed278c2aa7b18396bc8a35f628cbbbd0f3a0ab092f7ae0f24c77a8`.
Both source-free and source-aware verifiers passed; Sofia and Martin
reconstructions matched their selected source paths and bytes exactly; both
accepted results committed organized tree
`a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.

The release gallery remains ten image assets, accurately described as nine UI
captures plus one installed-copy Codex evidence card. Asset 09 is a truthful
summary derived from the recorded installed-copy qualification, not a literal
Codex UI screenshot. The unchanged gallery continues to represent the default
states shown; the final pointer-focus and noninteractive-Keychain corrections
are supported by the separate rendered-style, packaged-route, regression, and
clean-clone evidence above rather than by a false recapture claim.

The primary `/feedback` Session ID remains stored only in the ignored,
owner-only local submission record for Devpost field `27950`. Devpost project
`1327974`, version `7`, still has an empty video URL and `submitted_at: null`.
The final public YouTube video, user-owned eligibility and ownership entries,
explicit submission-hold release, final submission, and confirmation remain
pending. The submission hold remains active.

### Public Build Week video and Devpost-draft synchronization — 21 July 2026

The user authorized an AI-narrated final video because illness made a personal
voice recording impractical. The frozen 317-word evidence-checked script was
split into 27 timed cues and rendered with OpenAI Text-to-Speech model
`gpt-4o-mini-tts-2025-12-15`, voice `cedar`. The resulting narration is visibly
disclosed at the beginning and end of the video and in the YouTube description;
it is not represented as a live Foldweave model transaction.

The final master is exactly 175.000 seconds (`2:55`), 1920×1080 at 30 fps,
H.264 High / AAC-LC, with 5,250 frames, −16.3 LUFS integrated loudness, and
true peak −4.4 dBFS. Its SHA-256 is
`94ce318dca73f2c6af5ad6a0ec7e0d6316b162e9c77ac436bec4a6bd660b39a8`.
Full decode, frame-count, audio-level, visual, claim-to-evidence,
synchronization, and sensitive-data checks passed. An independent read-only
media audit returned `GO` for upload.

The video was uploaded and published Public on YouTube as **Foldweave — Change
the Structure. Keep the Connections. | OpenAI Build Week 2026**:

<https://youtu.be/aQgpK5z9OUQ>

YouTube reported **Checks complete. No issues found.** A 27-cue English caption
track with SHA-256
`b39b33f811b1ff65db7fb84646160fe3dd8f7b428c69096f2d43bb38cc07b8e6`
was published in YouTube Studio; public-player caption propagation may lag.
Google Chrome played the public upload from start to Replay at 2:55 with audio
enabled and autoplay disabled.

The official rules, dates, and latest announcements were rechecked. The live
Devpost connector reported `submissions_open` through Wednesday 22 July 2026 at
02:00 CEST. Devpost project `1327974` was updated to version `8`; connector
readback shows the exact public YouTube URL, public repository association, and
`submitted_at: null`. The private `/feedback` Session ID remains confined to
the ignored owner-only submission record and required field `27950`.

The remaining actions are user-owned submitter type, country, eligibility,
ownership, representative-authority where applicable, other personal/legal
attestations, and explicit release of the submission hold. Final Devpost
submission and confirmation have not occurred. The submission hold remains
active.
