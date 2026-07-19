# Reversible Name Atlas — Current Build State

Checkpoint: **Sunday 19 July 2026 at 06:24:53 CEST**

Phase: **C4_REQUIRED_SHARED_MCP**

Submission hold: **ACTIVE**

## Activation and fixed boundaries

- Historical H+0: **Friday 17 July 2026 at 17:16:25 CEST — PRESERVED**.
- Historical R+0: **Saturday 18 July 2026 at 00:51:51 CEST — PRESERVED**.
- Historical A+0: **Saturday 18 July 2026 at 15:37:55 CEST — PRESERVED**.
- Connected Change C+0: **Saturday 18 July 2026 at 23:31:39 CEST**.
- Previous AI-first goal: **COMPLETED THROUGH A3; SUPERSEDED FOR FUTURE
  EXECUTION**.
- Amended Connected Change goal: **ACTIVE**.
- Selected profile: **CONNECTED_CHANGE_GO**.
- Feature freeze: **Monday 20 July 2026 at 14:00 CEST**; **1 day, 7 hours,
  35 minutes, 7 seconds remaining at checkpoint**.
- Release candidate: **Monday 20 July 2026 at 20:00 CEST**; **1 day, 13 hours,
  35 minutes, 7 seconds remaining at checkpoint**.
- Recording ready: **Tuesday 21 July 2026 at 02:00 CEST**; **1 day, 19 hours,
  35 minutes, 7 seconds remaining at checkpoint**.
- Submission deadline: **Wednesday 22 July 2026 at 02:00 CEST**; **2 days,
  19 hours, 35 minutes, 7 seconds remaining at checkpoint**.
- Submission hold: **ACTIVE**.

## Repository checkpoint

- Repository: `/Users/nikolai/Desktop/Repos/reversible-name-atlas`.
- Branch: `revision/ai-first-folder-refactor`.
- Immutable A3 fallback: `e3803d26d342f5c128f4e9876a7b7e35c35bde3c`.
- Governance baseline: `4d4f07814a24ed2e28b015cecb1655e5c414632c`.
- Pre-activation preservation checkpoint:
  `121789a71d6f493a2c10e9503e6bc63db526fb7c`.
- C0 checkpoint: `a5ea34216962946f8abfc5db0ec6b5f1f0f07fb8`.
- C1 checkpoint: `c94c26bc66936be0bb87bf51e5381acfb2b4d300`.
- C2 checkpoint: `852fc55b6e3f8291e011d9102b0e132ea851a3d1`.
- C3 checkpoint locator: subject `feat: complete connected-change C3 evidence`
  on parent `852fc55b`; use fresh Git for the exact SHA after this state is
  committed.
- Local `main`, `origin/main`, and local/remote
  `revision/portable-change-receipt`: **PRESERVED AT `4baec1e`**.
- New branch/worktree, promotion, merge, rebase, force-push: **NOT PERFORMED**.

This file does not contain its own future commit SHA or claim its own post-commit
cleanliness. Fresh Git controls current repository facts.

## Observed product state

- A1–A3 foundation: **COMPLETE AND VERIFIED**.
- C0 cross-layout gate: **COMPLETE — CONNECTED_CHANGE_GO**.
- C1 Connected Change engine: **COMPLETE AND VERIFIED**.
- C2 Home/Organize/Apply browser and bounded macOS bridge: **COMPLETE AND
  VERIFIED**.
- C3 final GPT-5.6 evidence, exact replays, fixtures, receiver convergence,
  release refusal matrix, and browser replay: **COMPLETE AND VERIFIED**.
- Sole budget migration: **COMPLETE; HISTORY PRESERVED**.
- Required shared MCP: **NOT STARTED**.
- Codex plugin gate: **NOT REACHED**.
- Feature freeze: **PENDING; ABSOLUTE BOUNDARY ACTIVE**.
- Release materials: **STALE — PRESERVED SECOND-CYCLE RELEASE MATERIAL; MUST BE
  REGENERATED AFTER THE SELECTED PRODUCT PROFILE REACHES FEATURE FREEZE**.
- Current blocker: **NONE**.

## C3 evidence and verification

- Live hero root: `.name-atlas/c3-live-20260719T054119+0200`; exact
  `gpt-5.6`, returned `gpt-5.6-sol`, `store=false`, three turns, 16 evidence
  calls, zero questions, receipt
  `e3e15fb57f396760a53aecf1549cd3ecb0937cf85039e90113d29b4b1f88f9b1`,
  organized tree
  `a11ab49b9b48151aae4343c189c2eecae8c0a67a91cac45144656eb0ece02f7e`.
- Live ambiguity root:
  `.name-atlas/c3-live-ambiguity-retry-20260719T055030+0200`; exact
  `gpt-5.6`, returned `gpt-5.6-sol`, `store=false`, three turns, four evidence
  calls, exactly one question and one answer, receipt
  `9eba5c8d670106641dec8d6f6dc4366ea12454db2bd7eb8a86f27c2ca7c3b2a7`,
  organized tree
  `80d9bee46958fe996fb837c618534d29f3f0d90aad531ee18ce29ffbc1b639f6`.
- The first ambiguity attempt is preserved as failed evidence: its correct
  question cited tool-call IDs not yet accepted by the clarification evidence
  binder. A narrow correction accepts only unique observed call IDs for the one
  question; plan evidence remains content-addressed. The fresh retry passed.
- Exact sanitized recordings:
  `src/name_atlas/recordings/folder_hero_zero_question.json` SHA-256
  `75a4ab5f6bc41068c666659fb671bfbd1dcee6a24dcbbe67ba16250dca81d6a1`;
  `src/name_atlas/recordings/folder_ambiguity_one_question.json` SHA-256
  `cf8dc1ad3ad99ed99a2a10d273c713245584c89a34cf547d0a5dd9c23fdd623f`.
- Keyless proof root: `.name-atlas/c3-keyless-proof-20260719T055219+0200`.
  The hero replay, Martin receiver, and ambiguity replay all verified; Martin
  used zero provider/API/budget/external-network authority, converged to the hero
  organized tree, and reconstructed its own source exactly.
- Bundled browser replay: `.name-atlas/connected-demo/replay`; Home → Organize →
  Working → Done is truthful, 24/24 files and 23 supported links are accounted
  for, Verify again passes, and reconstruction compares exactly with the source.
  Desktop 1280×720 and narrow 390×844 have no horizontal overflow. A persisted
  job now refuses a mismatched live/replay invocation label before provider or
  budget setup.
- The final hero refusal matrix returns exact blockers for changed payload,
  changed non-destination Markdown, changed supported relationship, protected
  disagreement, and Change File fingerprint mismatch. The symmetric fixture
  blocks without guessing. A retagged BagIt-valid accepted-plan alteration is
  blocked by `artifact_digest_mismatch:accepted_plan`.
- Final focused C3/CLI correction suite: **13 passed in 12.87 seconds**.
- Complete regression: **795 passed in 46.48 seconds**.
- `uv lock --check`: **PASSED; 32 packages resolved**.
- Ruff lint: **PASSED**.
- Ruff format: **PASSED; 146 files already formatted**.
- `git diff --check`: **PASSED**.
- Independent C3 replay/privacy audit: **GO**.
- Independent C3 end-to-end/downstream audit: **GO**.

## Credentials, budget, and inactive later surfaces

- Process `OPENAI_API_KEY`: **ABSENT; NO VALUE READ**.
- Ignored owner-only `.env.local`: **PRESENT; VALUE NOT READ OR LOADED**.
- Sole ledger: `.name-atlas/api_budget.json`, SHA-256
  `c76f578db7d571b8297b9ba48467b8680e5759979370a81c978b0d72d31edecb`.
- Ledger authority: **9/13 requests and provider attempts; USD 9.736060
  conservative committed exposure; USD 0.605515 reported estimated cost; USD 10
  cumulative cap; no second ledger**.
- Further live GPT calls: **NOT REQUIRED OR PLANNED**.
- Browser/native QA servers: **STOPPED**.
- MCP, plugin, promotion, public-release, video, and submission operations:
  **NOT STARTED**.

## Compact recovery capsule

- Phase: `C4_REQUIRED_SHARED_MCP`.
- Branch/A3/C0: `revision/ai-first-folder-refactor` / `e3803d2` / `a5ea342`.
- Active profile/current milestone: `CONNECTED_CHANGE_GO / C3 COMPLETE; C4 NEXT`.
- Latest checks: `13 focused; 795 full; lock; Ruff lint; Ruff format; diff;
  five source-free verifications; exact receiver reconstruction; browser and
  responsive proof; two independent audits GO`.
- Change File/matcher/job/provenance: `C1 COMPLETE AND VERIFIED`.
- Receipt/verifier/reconstruction: `C1/C3 COMPLETE AND VERIFIED`.
- Browser/native picker: `C2/C3 COMPLETE AND VERIFIED`.
- GPT live/replay: `TWO NEW LIVE TRANSACTIONS AND TWO EXACT REPLAYS COMPLETE`.
- MCP/plugin: `NOT STARTED / GATE NOT REACHED`.
- Feature freeze/release materials: `ABSOLUTE BOUNDARY ACTIVE / STALE`.
- Submission hold: `ACTIVE`.
- Blockers: `NONE`.
- Next operation: add the stable official MCP v1 dependency and implement one
  shared STDIO server with exactly the seven frozen high-level tools, durable
  idempotent job handles, consent, protocol-only STDOUT, and actual Codex proof.

## Exact next operation

`Begin C4 by adding mcp>=1.27,<2 through the normal lock workflow, then implement and verify the required shared seven-tool STDIO server before making the one-time plugin decision.`
