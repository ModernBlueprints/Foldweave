# Codex and GPT-5.6 build log

This is the factual development record for Reversible Name Atlas. Codex with
GPT-5.6 was the primary development environment and integrator. The user chose
the product direction, authorized the frozen build contracts, retained human
authority over semantic decisions, and owns the submission voice-over,
eligibility attestations, `/feedback`, and final submission-hold release.

The runtime use of GPT-5.6 is separate and deliberately narrower: it may create
one bounded, evidence-linked advisory card for a mechanically detected Meaning
risk. It cannot approve, edit, verify, select a final path, stage a collection,
or make a handoff exportable.

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

### Current verified checkpoint

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

## How Codex contributed

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

## Provenance and claim boundary

Selected mechanical ideas from a pre-Build-Week feasibility spike were adapted
under the disclosures in [`PREEXISTING_WORK.md`](PREEXISTING_WORK.md). Its
tournament semantic/evaluator machinery was rejected, and the product has no
runtime dependency on the ephemeral spike.

This log does not claim semantic correctness, sender authentication,
compliance, production readiness, universal archival support, universal
reversibility, or measured time savings. The recording-ready release commit and
public-repository alignment are complete. Video, `/feedback` ID, personal
attestations, explicit hold release, and Devpost submission remain pending.
The submission hold remains active.

## Devpost pre-submission preparation — 18 July 2026

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

## Video-capture preflight — 18 July 2026

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
