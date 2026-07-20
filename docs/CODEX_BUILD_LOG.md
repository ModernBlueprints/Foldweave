# Codex and GPT-5.6 build log

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
inspection. The authoritative paths and SHA-256 values are recorded in
`docs/SUBMISSION_PACKAGE.md`. Final responsive QA at 390×844 traversed all five
routes with zero horizontal document overflow; the Handoff page retained
readable receipt identity, verifier command, and restore action.

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

An independent HTTPS clone at `/tmp/name-atlas-c6-audit.6Oy7Ak/repo` passed
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
invoked installed `verify_result` successfully. The final seven screenshots,
PNG/SVG thumbnail, and then-current 346-word C6 narration draft passed independent media,
metadata, path, secret, and claim review.

The release-media replacement removed seven superseded second-cycle PNGs from
the current gallery because they showed the archive workflow rather than the
selected Connected Change product: `01-atlas.png` (345,430 bytes),
`02-decide.png` (422,841), `03-stage.png` (200,943), `04-verify.png` (348,416),
`05-handoff.png` (341,384), `06-offline-receipt.png` (334,009), and
`07-negative-block.png` (365,283), for 2,358,306 bytes total. They remain
byte-for-byte recoverable from feature-freeze commit `0dc4776`; the current
release replaces them with the visually audited seven-frame Connected Change
gallery and Sofia→Change File→Martin thumbnail recorded in the submission
package.

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
`e10b09a` at
`/Users/Shared/NameAtlas-C7-Fix-Clone-e10b09a.opfllx/repo` reproduced 822/822
and 249/249 tests. Its 563,894-byte, 205-member wheel has SHA-256
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

The audited `docs/submission-thumbnail.png` was then streamed through Devpost's
direct file-upload path. The processed public thumbnail returned HTTP 200 as a
51,109-byte PNG. A first non-mutating upload command retained the connector's
literal `<FILE_PATH>` placeholder and exited 26 before reading or uploading any
file; the corrected command used the fixed audited local path and succeeded
once. No duplicate project or thumbnail mutation was created.

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

### Current implementation after `2322076`

The active working branch continues to integrate the proof-carrying derivative
transaction and shared host surfaces. Current source and tests cover:

- complete `connected-change-file.v2` children with immediate-parent lineage;
- receipt/verifier v3 and transaction-specific reconstruction authority;
- immutable receiver parent jobs and explicit derivative children;
- direct, ChatGPT-hosted, Codex-hosted, replay, and model-free provenance;
- a local STDIO MCP profile for Codex and a ChatGPT Streamable HTTP profile;
- a purpose-built current/proposed React tree shared by the native review island
  and ChatGPT widget;
- an outbound-only paired companion and a checked-in Cloudflare gateway profile;
  and
- a renamed thin Foldweave Codex plugin around the same MCP and deterministic
  engine.

Those source surfaces are not release evidence by themselves. At this
documentation checkpoint, public Cloudflare deployment, consumer pairing,
ChatGPT directory approval/public listing, a final ChatGPT origin-revision
transaction, and a final fresh-task Foldweave Codex installed-copy transaction
must not be claimed unless separately observed and recorded.

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

The ChatGPT developer qualification has demonstrated real tool discovery,
opaque local selection, deterministic receiver matching, and a rendered
receiver-local current/shared preview without loading a direct API key. The
consumer gateway and complete final host qualification remain separate gates;
developer-mode evidence is not a public-distribution claim.

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

### Release and submission status

The Connected Change predecessor remains the last complete public release. The
Foldweave branch has not yet been declared a release candidate in this build
log. No Cloudflare public deployment, ChatGPT directory approval, signed or
notarized app, final Foldweave video, `/feedback`, eligibility/ownership
attestation, final submission-hold release, or Devpost submission is asserted
here. The submission hold remains active.
