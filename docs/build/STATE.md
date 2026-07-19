# Foldweave build state

Observed: **Sunday 19 July 2026 at 18:46:52 CEST** using
`oslo_tz = ZoneInfo("Europe/Oslo")`.

Phase: **F0B_NATIVE_APPLICATION_IN_PROGRESS**

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
| Feature freeze | Tuesday 21 July 2026 at 01:00 CEST | 30 hours, 13 minutes, 7 seconds |
| Release candidate | Tuesday 21 July 2026 at 06:00 CEST | 35 hours, 13 minutes, 7 seconds |
| Recording readiness | Tuesday 21 July 2026 at 10:00 CEST | 39 hours, 13 minutes, 7 seconds |
| Submission | Wednesday 22 July 2026 at 02:00 CEST | 55 hours, 13 minutes, 7 seconds |

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
| Bounded revision | `NOT STARTED` |
| Change File v2 and receipt/verifier v3 | `NOT STARTED` |
| Serial derivative collaboration | `NOT STARTED` |
| Native Foldweave app | `F0B IN PROGRESS` |
| Keychain settings | `F0B IN PROGRESS`; implementation not yet qualified |
| New direct GPT planner evidence | `NOT STARTED` |
| ChatGPT developer integration | `NOT STARTED` |
| Consumer gateway and companion | `NOT STARTED` |
| ChatGPT distribution states | `NOT STARTED` |
| Reviewed MCP and Codex update | `NOT STARTED` |
| Budget migration | `NOT STARTED` |
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
  `c76f578db7d571b8297b9ba48467b8680e5759979370a81c978b0d72d31edecb`.
- The ledger remains unchanged at USD 10 monetary authority, call cap 13, 9
  requests reserved, 9 provider attempts reserved, USD 9.736060 conservative
  committed exposure, and USD 0.605515 reported estimated cost.
- Cloudflare CLI, verified account credentials, deployment, gateway URL, and
  pairing evidence are absent.
- No Apple Developer ID code-signing identity is installed.
- The macOS ChatGPT application and the current Codex desktop environment are
  present. A standalone `/Applications/Codex.app` is absent, and the discovered
  legacy `codex` shell executable fails to start; this is an implementation-time
  Codex installation/qualification risk, not a scaffold blocker.
- The installed personal plugin is still branded Name Atlas.
- There is no observed active Name Atlas/Foldweave server process.

## Latest verified commands

- `uv lock --check` — passed; 48 packages resolved.
- `PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest -p no:cacheprovider` —
  passed; 855 tests in 64.18 seconds.
- Focused F0a Python review/authority/browser/launcher suite — passed; 33 tests.
- `npm run typecheck` — passed with strict library checking.
- `npm test` — passed; 6 Vitest tests.
- `npm run build` — passed; production review assets regenerated.
- `uv run --no-sync ruff check .` — passed.
- `uv run --no-sync ruff format --check .` — passed; 164 files already
  formatted.
- `git diff --check` and `git diff --cached --check` — passed.
- Independent corrected-bypass reproduction — `BYPASS_REJECTED`; durable
  checkpoint unchanged; output empty; unchanged exact acceptance verified.

## Exact next operation

`Freeze the exact F0b direct-planning and native-shell qualification contracts, verify and monotonically migrate the sole budget ledger to USD 40 before any call, then implement the smallest packaged Foldweave.app origin review/revision/accept/verify transaction.`

## Compact recovery capsule

- **Phase:** `F0B_NATIVE_APPLICATION_IN_PROGRESS`
- **Branch / predecessor:** `revision/foldweave-native-review` /
  `1023999f2acc7b806775b407dc01a15af3447e90`
- **Current F milestone:** F0b native application; F0a returned verified `GO`;
  F+0 is Sunday 19 July 2026 at 17:18:14 CEST
- **Latest verified commands:** lock passed; 855 Python tests, 6 frontend tests,
  strict TypeScript, Vite build, Ruff lint/format, and Git diff checks passed
- **Job / preview:** F0a review/acceptance authority `VERIFIED COMPLETE`
- **Change File / receipt / verifier / reconstruction:** predecessor evidence
  complete; Foldweave v2/v3 work `NOT STARTED`
- **Native / browser:** Foldweave browser review gate complete; native F0b
  `IN PROGRESS`
- **Direct / live / replay:** predecessor direct/replay evidence complete; new
  Foldweave qualification `NOT STARTED`
- **ChatGPT / gateway / companion:** `NOT STARTED`
- **MCP / Codex:** predecessor installed plugin complete; Foldweave update
  `NOT STARTED`
- **Budget:** unchanged sole USD 10 ledger; USD 40 migration `NOT STARTED`
- **Feature freeze:** pending; absolute boundary Tuesday 21 July 2026 at 01:00
  CEST; 30 hours, 13 minutes, 7 seconds remained at this checkpoint
- **Release materials:** stale for Foldweave; predecessor materials preserved
- **Submission hold:** `ACTIVE`
- **Blockers:** none
- **Next operation:** freeze F0b contracts, perform the verified monotonic USD 40
  ledger migration before any direct call, and build the packaged native
  transaction
