# Foldweave build state

Observed: **Sunday 19 July 2026 at 22:01:53 CEST** using
`oslo_tz = ZoneInfo("Europe/Oslo")`.

Phase: **F0C_CHATGPT_DEVELOPER_MODE_IN_PROGRESS**

Submission hold: **ACTIVE**

Blocker: **NONE**

## Activation and repository

| Field | Observed state |
|---|---|
| Historical H+0 | Friday 17 July 2026 at 17:16:25 CEST — `PRESERVED` |
| Historical R+0 | Saturday 18 July 2026 at 00:51:51 CEST — `PRESERVED` |
| Historical A+0 | Saturday 18 July 2026 at 15:37:55 CEST — `PRESERVED` |
| Historical C+0 | Saturday 18 July 2026 at 23:31:39 CEST — `PRESERVED` |
| Preceding Connected Change goal | `COMPLETED THROUGH C7; SUPERSEDED FOR FUTURE EXECUTION` |
| Amended Foldweave goal | `ACTIVE` |
| Foldweave F+0 | Sunday 19 July 2026 at 17:18:14 CEST |
| Current branch | `revision/foldweave-native-review` |
| Exact predecessor | `1023999f2acc7b806775b407dc01a15af3447e90` |
| Governance commit locator | Parent `1023999f2acc7b806775b407dc01a15af3447e90`; subject `docs: establish Foldweave native-review scaffold`; exact SHA belongs in the handoff |
| `main` | `1023999f2acc7b806775b407dc01a15af3447e90` — unchanged |
| `origin/main` | `1023999f2acc7b806775b407dc01a15af3447e90` — unchanged |
| Previous local revision | `revision/ai-first-folder-refactor` at `1023999f2acc7b806775b407dc01a15af3447e90` — unchanged |
| Previous remote revision | `origin/revision/ai-first-folder-refactor` at `1023999f2acc7b806775b407dc01a15af3447e90` — unchanged |
| Historical portable branch | local and remote `revision/portable-change-receipt` at `4baec1ed7b8553775527e3be506edab584b2b8b3` — unchanged |

The exact governance commit SHA, clean post-commit state, and remote Foldweave
branch SHA cannot be asserted by the file contained in that commit. They must be
reported from fresh post-commit evidence in the scaffold handoff.

## Remaining fixed windows at the observed time

| Boundary | Absolute Oslo time | Remaining |
|---|---|---:|
| Feature freeze | Tuesday 21 July 2026 at 01:00 CEST | 26 hours, 58 minutes, 6 seconds |
| Release candidate | Tuesday 21 July 2026 at 06:00 CEST | 31 hours, 58 minutes, 6 seconds |
| Recording readiness | Tuesday 21 July 2026 at 10:00 CEST | 35 hours, 58 minutes, 6 seconds |
| Submission | Wednesday 22 July 2026 at 02:00 CEST | 51 hours, 58 minutes, 6 seconds |

These windows continue to elapse. F+0 recorded activation and the scaled
targets; it did not reset the 44-hour envelope. The effective F0a target is
Sunday 19 July 2026 at 21:55:42 CEST.

## Observed implementation status

| Surface | Status |
|---|---|
| A1–A3 and C0–C7 inherited foundation | `VERIFIED COMPLETE` |
| Foldweave branding | `F0A REVIEW SURFACE COMPLETE`; full active-surface rename remains F3 |
| Job v3 and immutable preview | `F0A VERIFIED COMPLETE` |
| Review and exact acceptance | `F0A VERIFIED COMPLETE` |
| Bounded revision | `F0B LIVE ORIGIN PATH VERIFIED`; complete multi-surface engine remains F1 |
| Change File v2 and receipt/verifier v3 | `NOT STARTED` |
| Serial derivative collaboration | `NOT STARTED` |
| Native Foldweave app | `F0B VERIFIED COMPLETE — GO` |
| Keychain settings | `F0B PACKAGED CONFIGURE/STATUS/REMOVE VERIFIED`; final state not configured |
| New direct GPT planner evidence | `F0B LIVE ORIGIN REVIEW/REVISION/ACCEPTANCE VERIFIED`; F4 evidence matrix remains |
| ChatGPT developer integration | `F0C IN PROGRESS` |
| Consumer gateway and companion | `NOT STARTED` |
| ChatGPT distribution states | `NOT STARTED` |
| Reviewed MCP and Codex update | `NOT STARTED` |
| Budget migration | `COMPLETE`; sole USD 40 ledger preserved, current call cap 13 fully reserved; F4 may set the final count cap |
| Feature freeze | `PENDING`; absolute boundary Tuesday 21 July 2026 at 01:00 CEST |
| Foldweave release materials | `STALE FOR THE FOLDWEAVE RELEASE — PRESERVED VERIFIED NAME ATLAS PREDECESSOR MATERIAL; MUST BE REGENERATED AFTER FOLDWEAVE FEATURE FREEZE` |
| Devpost submission | `NOT PERFORMED` |

## Current environment and budget facts

- The process environment contains no `OPENAI_API_KEY`; no value was read or
  exposed.
- Ignored `.env.local` exists with owner-only mode `0600`; its contents were not
  read.
- The sole ledger remains `.name-atlas/api_budget.json`, schema
  `gpt-budget.v1`, model `gpt-5.6`, SHA-256
  `7f4142aaee9bc6bb14f88c91541d9d611ef5abd1d7f4f958cd3434d401f75f0a`.
- The ledger is monotonically migrated to USD 40 monetary authority while
  preserving the cumulative call cap 13. It records 13 requests reserved, 13
  provider attempts reserved, USD 12.734470 conservative committed exposure,
  and USD 0.874860 reported estimated cost. The current call cap is exhausted;
  only F4 may set its final count after the complete remaining call graph is
  frozen.
- Cloudflare CLI, verified account credentials, deployment, gateway URL, and
  pairing evidence are absent.
- No Apple Developer ID code-signing identity is installed.
- The macOS ChatGPT application and the current Codex desktop environment are
  present. A standalone `/Applications/Codex.app` is absent, and the discovered
  legacy `codex` shell executable fails to start; this is an implementation-time
  Codex installation/qualification risk, not a scaffold blocker.
- The installed personal plugin is still branded Name Atlas.
- The packaged Keychain qualification ended with no Foldweave item configured.
- There is no observed active Name Atlas/Foldweave server process.

## Latest verified commands

- `uv lock --check` — passed; 62 packages resolved.
- `PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest -p no:cacheprovider` —
  passed; 918 tests in 69.30 seconds with one existing Starlette warning.
- Focused independent F0b/native/provider suites — passed; 60 tests and 45
  tests in the two bounded audits.
- `npm run typecheck` — passed with strict library checking.
- `npm test` — passed; 8 Vitest tests.
- `npm run build` — passed; production review assets regenerated.
- `uv run --no-sync ruff check .` — passed.
- `uv run --no-sync ruff format --check .` — passed; 181 files already
  formatted.
- PyInstaller production build, arm64/file checks, and strict ad-hoc
  `codesign` verification — passed; unrelated-location launch passed.
- Product-native receipt verification returned `VERIFIED` for receipt
  `116616c0b6fd857c9885177ef80e02e4e574f82d5ec82e00ef2b773ffa005fdd`;
  source/reconstruction comparison was exact.
- The actual packaged picker timeout/selection and Keychain
  configure/status/remove paths passed without provider or output mutation.
- Restart preserved job SHA-256
  `c8320d759aa39000a05f221509defa0aff708c2d80edb1439488e2a793a0284d`
  and the ledger SHA above; final quit left no process.
- Sensitive-value/path scan, `git diff --check`, and
  `git diff --cached --check` — passed.
- The independent adversarial audit returned F0b `COMPLETE — GO`.

## Exact next operation

`Implement and qualify F0c through the currently documented official ChatGPT developer route: connect the bounded Foldweave host-planning MCP and local companion to a fresh task in the actual macOS ChatGPT app, render the shared preview widget, send one revision back through the host model loop, accept the exact preview, verify the local result, and prove that the direct ledger remains unchanged.`

## Compact recovery capsule

- **Phase:** `F0C_CHATGPT_DEVELOPER_MODE_IN_PROGRESS`
- **Branch / predecessor:** `revision/foldweave-native-review` /
  `1023999f2acc7b806775b407dc01a15af3447e90`
- **Current F milestone:** F0c ChatGPT developer mode; F0a and F0b returned
  verified `GO`; F+0 is Sunday 19 July 2026 at 17:18:14 CEST
- **Latest verified commands:** lock passed; 918 Python tests, 8 frontend tests,
  strict TypeScript, Vite build, Ruff lint/format, and Git diff checks passed
- **Job / preview:** F0a authority and F0b direct native
  review/revision/acceptance `VERIFIED COMPLETE`
- **Change File / receipt / verifier / reconstruction:** predecessor evidence
  complete; Foldweave v2/v3 work `NOT STARTED`
- **Native / browser:** packaged F0b native gate `VERIFIED COMPLETE — GO`;
  browser fallback remains available
- **Direct / live / replay:** live F0b origin transaction `VERIFIED COMPLETE`;
  broader F4 evidence remains
- **ChatGPT / gateway / companion:** F0c `IN PROGRESS`; consumer gateway remains
  `NOT STARTED`
- **MCP / Codex:** predecessor installed plugin complete; Foldweave update
  `NOT STARTED`
- **Budget:** sole ledger migrated to USD 40; call cap 13 fully reserved; F4
  retains authority to set the final count cap
- **Feature freeze:** pending; absolute boundary Tuesday 21 July 2026 at 01:00
  CEST; 26 hours, 58 minutes, 6 seconds remained at this checkpoint
- **Release materials:** stale for Foldweave; predecessor materials preserved
- **Submission hold:** `ACTIVE`
- **Blockers:** none
- **Next operation:** qualify the official ChatGPT developer path through the
  actual macOS ChatGPT app with the shared host-planning tools, widget,
  companion, exact acceptance, local proof, and unchanged direct ledger
