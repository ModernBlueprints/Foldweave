# Foldweave build state

Observed: **Tuesday 21 July 2026 at 21:38:04 CEST** using
`oslo_tz = ZoneInfo("Europe/Oslo")`.

Phase: **WAITING_FOR_SUBMISSION_HOLD_RELEASE**

Submission hold: **ACTIVE**

Global blocker: **NONE**. Every independently actionable product, release,
public-video, due-diligence, `/feedback`, and Devpost-draft requirement is
complete. The remaining gates are the user's personal/legal attestations and
explicit release of the submission hold. Final Devpost submission has not
occurred.

## History and repository

| Field | Observed state |
|---|---|
| Historical H+0 / R+0 / A+0 / C+0 | `PRESERVED` — exact timestamps remain in the sole plan |
| Foldweave F+0 | Sunday 19 July 2026 at 17:18:14 CEST — `ACTIVE` |
| Current branch | `revision/foldweave-native-review` |
| Preserved product release baseline | `4e9ec44b02b25f515017ceb9922fff4fdf84ae46` |
| Final implementation checkpoint | `68aba38a643d95f69e9aacd392904ef310f6994c` — final UI focus and fail-closed packaged-runtime corrections included |
| Final release-documentation locator | subject `docs: record final Foldweave release verification`, parent `68aba38a643d95f69e9aacd392904ef310f6994c`; the resulting SHA belongs in the handoff, not this file |
| Previous revision / portable branch | `1023999f2acc7b806775b407dc01a15af3447e90` and `revision/portable-change-receipt` at `4baec1ed7b8553775527e3be506edab584b2b8b3` — preserved |

## Remaining fixed window

| Boundary | Absolute Oslo time | State at observation |
|---|---|---:|
| Feature freeze | Tuesday 21 July 2026 at 01:00 CEST | passed by 20 hours, 38 minutes, 4 seconds |
| Release candidate | Tuesday 21 July 2026 at 06:00 CEST | passed by 15 hours, 38 minutes, 4 seconds |
| Recording readiness | Tuesday 21 July 2026 at 10:00 CEST | passed by 11 hours, 38 minutes, 4 seconds |
| Submission | Wednesday 22 July 2026 at 02:00 CEST | 4 hours, 21 minutes, 56 seconds remained |

F+0 did not reset the 44-hour envelope. Only release-safe work is now
permitted.

## Current verified status

| Surface | Status |
|---|---|
| A1–A3 and C0–C7 foundation; F0a–F0d and F1–F7 | `VERIFIED COMPLETE — RECORDING_READY` |
| Product and proof | review-before-execution, job v3, exact acceptance, bounded revision, Change File v2, receipt/verifier v3, lineage, convergence, and selected-source reconstruction `VERIFIED COMPLETE` |
| Native macOS app | `VERIFIED COMPLETE` — unsigned/ad-hoc Apple-Silicon judge build; no Developer ID or notarization claim |
| Direct GPT-5.6 | `VERIFIED COMPLETE` — live root and derivative evidence; sole USD 40 ledger preserved |
| ChatGPT | `DEVELOPER_MODE_VERIFIED`; `CONSUMER_PAIRING_VERIFIED`; technical `PUBLICATION_READY`; not submitted for review, approved, published, or publicly listed |
| Replay, unchanged application, MCP, and Codex | `VERIFIED COMPLETE` — model-free replay, `capsule_applied` receiver path, shared bounded MCP, installed-copy qualification, and clean-clone plugin/MCP validation |
| Gateway and companion | `VERIFIED COMPLETE` — deployed `workers.dev` gateway, OAuth/pairing, outbound companion, reconnect, and refusal matrix |
| Regression and source checks | 1,184 Python tests, 80 frontend tests, 50 gateway tests; lock, lint, format, packaging, visual, and claim scans pass as recorded in the plan and build log |
| Public clone judge path | `VERIFIED COMPLETE` — public `main` clone installed with `uv sync --frozen`; keyless replay reached review, served `/review`, accepted the exact preview, verified, and reconstructed source paths and bytes exactly |
| Public video | `VERIFIED COMPLETE` — Public at <https://youtu.be/aQgpK5z9OUQ>; exact 175.000-second master, disclosed OpenAI Text-to-Speech narration, no-music/repository-owned visuals, YouTube checks passed, English captions published in Studio, and public playback reached Replay at 2:55 with audio enabled |
| `/feedback` | `CAPTURED PRIVATELY` — exact primary Codex Session ID reserved for Devpost field `27950` |
| Devpost project preparation | `COMPLETE WITHOUT SUBMISSION` — public project `1327974`, version `8`, has Foldweave project copy, public repository, technology list, thumbnail, verified public video, keyless judge guidance, and captured-status `/feedback` evidence without exposing the identifier; the exact value is ready for field `27950`, **Work & Productivity** is frozen for field `27947`, and only user-owned fields, hold release, and submission remain pending |
| Devpost submission | `NOT PERFORMED` |

The category decision is complete: **Work & Productivity** will be supplied as
Devpost submission field `27947` only with the final submission, after the video
exists and the user explicitly releases the hold. Its current absence from an
unsubmitted project record is not a missing product decision.

## Latest verified commands

- Final clean clone at exact implementation checkpoint `68aba38`: `uv sync
  --frozen`, `uv lock --check`, **1,184** Python tests with one upstream
  deprecation warning, Ruff lint/format, frontend typecheck/build and **80/80**
  tests, gateway typecheck/dry build and **50/50** tests: passed.
- Final clean-clone package: 55 MiB arm64 app executable SHA-256
  `1c2316e26a23ecc9d3608e37d8a6ebf23ee2c128f468a9ec68018cf54cc606d4`;
  wheel SHA-256
  `7de05603f9be06627888f8369581a987693ad69b7e9ca1dd340cf78414c1df07`;
  strict deep signature verification, unrelated-directory launch, responsive
  routes, and clean shutdown passed.
- Final clean-clone origin and receiver: immutable review, exact acceptance,
  source-free/source-aware verification, and both exact reconstructions passed;
  both results commit organized tree
  `a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.
- Public gateway Worker version
  `77598fb6-72e4-48ee-919e-27488a60a515` serves byte-matched `review-v37`
  assets and reports ready with all required bindings.
- Final public media: 175.000-second H.264/AAC master SHA-256
  `94ce318dca73f2c6af5ad6a0ec7e0d6316b162e9c77ac436bec4a6bd660b39a8`;
  full decode, 5,250-frame count, −16.3 LUFS audio, visual/claim/privacy audit,
  YouTube checks, and complete public playback passed. The 27-cue English SRT
  SHA-256 is
  `b39b33f811b1ff65db7fb84646160fe3dd8f7b428c69096f2d43bb38cc07b8e6`.
- Devpost connector readback: project `1327974`, version `8`, video URL
  `https://youtu.be/aQgpK5z9OUQ`, Build Week `submitted_at: null`; live key-date
  state `submissions_open` through Wednesday 22 July 2026 at 02:00 CEST.

## User-owned work still pending

1. Complete submitter type, country, eligibility, ownership, representative, and
   other personal/legal Devpost entries.
2. Reread the final Devpost form and explicitly release the submission hold only
   after every prerequisite is complete.

## Exact next operation

`User completes the personal form and legal attestation fields, rereads the
final Devpost entry, and explicitly releases the submission hold. The public
video, repository, project description, judge path, and /feedback Session ID are
already prepared. Do not submit before that explicit release.`

## Compact recovery capsule

- **Phase:** `WAITING_FOR_SUBMISSION_HOLD_RELEASE`.
- **Branch / checkpoint:** `revision/foldweave-native-review`; product
  baseline `4e9ec44b02b25f515017ceb9922fff4fdf84ae46`; final implementation
  `68aba38a643d95f69e9aacd392904ef310f6994c`; final documentation SHA is
  reported in the handoff.
- **Evidence:** job/preview, Change File/receipt/verifier/reconstruction,
  native/browser, direct/hosted/replay, gateway, MCP/Codex, release visuals,
  final 2:55 public video, Devpost project version 8, and the Codex evidence
  card are verified; detailed fingerprints remain in the sole plan and build
  log.
- **Budget:** sole USD 40 ledger; no further direct call is needed for the
  recording package.
- **Release materials:** Foldweave-current and public; the tournament and
  predecessor-fixture provenance are explicitly disclosed.
- **Submission hold:** `ACTIVE`.
- **Blockers:** none globally; remaining prerequisites are user-owned personal
  and legal attestations plus explicit submission-hold release. Agent-controlled
  final submission resumes only after that release.
