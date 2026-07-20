# Foldweave build state

Observed: **Monday 20 July 2026 at 12:25:11 CEST** using
`oslo_tz = ZoneInfo("Europe/Oslo")`.

Phase: **F0D CONSUMER GATEWAY QUALIFICATION AND F2 LIVE-TRANSPORT CLOSURE**

Submission hold: **ACTIVE**

Global blocker: **NONE**. The remaining F0d Cloudflare login is a narrow
user-owned prerequisite; local authority, MCP, engine, test, and release work
continues independently.

## Activation and repository

| Field | Observed state |
|---|---|
| Historical H+0 | Friday 17 July 2026 at 17:16:25 CEST — `PRESERVED` |
| Historical R+0 | Saturday 18 July 2026 at 00:51:51 CEST — `PRESERVED` |
| Historical A+0 | Saturday 18 July 2026 at 15:37:55 CEST — `PRESERVED` |
| Historical C+0 | Saturday 18 July 2026 at 23:31:39 CEST — `PRESERVED` |
| Foldweave F+0 | Sunday 19 July 2026 at 17:18:14 CEST — `ACTIVE` |
| Current branch | `revision/foldweave-native-review` |
| Checkpoint parent and pre-commit remote branch | `23220768d26990cb8f980f77be41510bc2a7bfd7`; identify the resulting checkpoint by fresh Git rather than self-reference |
| Exact predecessor, `main`, `origin/main`, and previous revision | `1023999f2acc7b806775b407dc01a15af3447e90` — unchanged |
| Historical portable branch | local and remote `revision/portable-change-receipt` at `4baec1ed7b8553775527e3be506edab584b2b8b3` — unchanged |
| Working tree at observation | the complete integrated Foldweave checkpoint is staged; no unrelated work was discarded; verify post-commit cleanliness with fresh Git |

## Remaining fixed windows

| Boundary | Absolute Oslo time | Remaining at observation |
|---|---|---:|
| Feature freeze | Tuesday 21 July 2026 at 01:00 CEST | 12 hours, 34 minutes, 48 seconds |
| Release candidate | Tuesday 21 July 2026 at 06:00 CEST | 17 hours, 34 minutes, 48 seconds |
| Recording readiness | Tuesday 21 July 2026 at 10:00 CEST | 21 hours, 34 minutes, 48 seconds |
| Submission | Wednesday 22 July 2026 at 02:00 CEST | 37 hours, 34 minutes, 48 seconds |

These windows continue to elapse. F+0 did not reset the 44-hour envelope.

## Observed implementation status

| Surface | Status |
|---|---|
| A1–A3 and C0–C7 inherited foundation | `VERIFIED COMPLETE` |
| Foldweave F0a review authority | `VERIFIED COMPLETE — GO` |
| Foldweave F0b packaged native/direct path | `VERIFIED COMPLETE — GO` |
| Foldweave F0c ChatGPT developer integration | `VERIFIED COMPLETE — DEVELOPER_MODE_VERIFIED` |
| Foldweave F1 complete review/revision engine | `VERIFIED COMPLETE — 1,102-TEST REGRESSION GREEN` |
| Job v3 and immutable preview | `VERIFIED COMPLETE` |
| Review/revision/exact acceptance | origin, receiver, direct, hosted, CLI, browser, native, and MCP paths `VERIFIED COMPLETE` |
| Change File v2 and receipt/verifier v3 | deterministic domain, portability, lineage, race, compatibility, and product-native review matrices complete; live-transport qualification remains |
| Serial derivative collaboration | deterministic Sofia → Martin → Sofia, self-contained CF2, raw/T1 application, convergence, and participant reconstruction complete; mandatory live/packaged evidence remains |
| Native Foldweave app and Keychain | `F0B VERIFIED COMPLETE`; final F3/F6 active-brand and release polish remain |
| Direct GPT evidence | live root review/revision/acceptance verified; F4 direct derivative matrix remains |
| ChatGPT-hosted evidence | live root review/revision/acceptance/verification/Change File/reconstruction verified; live receiver derivative remains |
| Consumer gateway and companion | local device/grant/scope/per-job-capability authority implemented and regression-green; live Cloudflare/OAuth/WSS qualification pending |
| ChatGPT distribution | `DEVELOPER_MODE_VERIFIED`; consumer pairing/publication states not yet achieved |
| Reviewed MCP/Codex | shared MCP and predecessor plugin exist; Foldweave installed-copy F4 qualification remains |
| Budget migration | `COMPLETE`; sole USD 40 ledger preserved |
| Feature freeze | `PENDING` |
| Foldweave release materials | `STALE FOR THE FOLDWEAVE RELEASE`; predecessor evidence preserved |
| Devpost submission | `NOT PERFORMED`; hold active |

## F0c completion evidence

- Actual macOS ChatGPT task and visible Foldweave widget were used through the
  official Secure MCP Tunnel. No Chrome or Brave automation was used.
- Hosted job: `d8392e05e1e841c7850c28c7a6e4ce82`.
- Revised preview: job revision 24, proposal revision 1, candidate
  `5f96104f0c37825e21a389b0024cacd5af84908a9be8b443c1f801cf1319b83f`,
  preview
  `f9504c0e062cb7ab05b88fe9959f10b878d977e4a5df5b71f5f99f71f835c384`.
- The actual widget action **Accept this structure and create copy** persisted
  exact `chatgpt_hosted` authorization and advanced the job to revision 26
  `verified`.
- Verified artifacts: receipt
  `e8acaa4b74db7722ff8d39de8bc7a28d8c1a34b9e16dc2eddef6c33d5c778fa7`,
  verification
  `b8d20f23e5aba8d24a64ae8f2608e3de0398ce920a03c7c174c28d44e95dacde`,
  Change File
  `0bf3caf6bdbbac5657db00af2eee8b7769dbf9d980feb4e3725f19b9abf5538b`,
  organized tree
  `c234aabe97f7cccfaf6b8c025a2b34c2d4b50a4c350ba52245b8941ac8d6158e`.
- The widget's **Verify again**, **Get Change File**, and **Recreate original**
  actions passed. Only opaque handles crossed the widget boundary.
- Independent CLI verification passed and both independent reconstructions
  matched the selected source exactly by path and bytes.
- The v3 public-CLI dispatch defect found by this check was corrected and has a
  passing verify/restore regression.
- The sole direct ledger remained byte-identical at SHA-256
  `7f4142aaee9bc6bb14f88c91541d9d611ef5abd1d7f4f958cd3434d401f75f0a`.

## Current environment and budget

- The process environment contains no `OPENAI_API_KEY`; no value was exposed.
- Ignored `.env.local` exists with owner-only mode `0600`; its value has not
  been printed or committed.
- The sole ledger remains `.name-atlas/api_budget.json`, schema
  `gpt-budget.v1`, model `gpt-5.6`, monetary cap USD 40, call cap 13, 13
  requests/attempts reserved, USD 12.734470 conservative exposure, and USD
  0.874860 reported estimated cost.
- The Secure MCP Tunnel and hosted Foldweave MCP process remain active for
  current developer qualification; process IDs 32146/32157/32159 were observed.
- Wrangler 4.112.0 is installed but not authenticated. A keychain-backed OAuth
  login is pending in Codex's in-app browser. No KV namespace, Worker, custom
  domain, paid plan, or public gateway has been provisioned or deployed.
- No Apple Developer ID identity is installed; the tested unsigned/ad-hoc
  Apple-Silicon judge build remains the truthful release profile.

## Latest verified commands

- Complete Python regression after all public-authority corrections:
  **1,102 passed in 130.81 seconds**.
- Primary-integrator post-correction companion, public-capability, MCP, host,
  native, and derivative authority matrix: **110 passed**.
- The independent audit's reproduced standalone loopback ContextVar defect was
  corrected before deployment. The production companion now uses in-process
  ASGI dispatch with one shared identity and host service; the new context and
  composition regressions pass.
- The same audit found that the first capability propagation design exposed a
  raw bearer through MCP `structuredContent`, contrary to UX-022. That design
  was removed before deployment: MCP and widget surfaces carry no raw
  capability, while the local host rederives and validates the immutable
  30-minute JobV3 binding from the verified device/grant/scope/job context.
- The bounded independent re-audit found no HIGH or MEDIUM issue, independently
  passed **83** public-authority Python tests plus the complete frontend and
  gateway suites, and returned code-level public-deployment readiness `GO`.
- Deterministic F2 closure matrix: **67 passed**; adjacent real
  parent/child-race and product-native Martin T1→T2 matrix: **25 passed**.
- Frontend strict TypeScript passed; Vitest passed **54/54**; Vite review and
  ChatGPT-widget production builds passed.
- Gateway strict TypeScript passed; Worker tests passed **31/31**; Wrangler
  production dry build passed at 219.63 KiB raw / 47.13 KiB gzip. The subsequent
  accidental request for a nonexistent `deploy:dry-run` npm script failed after
  the real `build` script had already passed; `package.json` confirms `build`
  itself is the dry-run deployment command.
- `uv lock --check` resolved 63 packages; Ruff lint passed; Ruff format reports
  **220 files already formatted**; unstaged and cached `git diff --check` pass.

## Exact next operation

`Preserve and publish the independently audited, regression-green
F1/deterministic-F2 checkpoint; then authenticate Wrangler
through Codex's in-app browser, provision the real free-tier gateway resources,
deploy, and qualify OAuth, pairing, outbound WSS, reconnect, origin, and receiver
derivative transactions before beginning the remaining direct/ChatGPT live F2
matrix and F3/F4 release qualification.`

## Compact recovery capsule

- **Phase:** `F0D CONSUMER GATEWAY QUALIFICATION AND F2 LIVE-TRANSPORT CLOSURE`
- **Branch / checkpoint parent:** `revision/foldweave-native-review` /
  `23220768d26990cb8f980f77be41510bc2a7bfd7`; resolve the checkpoint commit
  from fresh Git
- **Current milestone:** F0c and F1 complete; deterministic F2 complete; F0d
  live public deployment and F2 live transports in progress
- **Job / preview:** hosted job `d8392e05e1e841c7850c28c7a6e4ce82`,
  revision 26 `verified`; candidate/preview fingerprints recorded above
- **Change File / receipt / verifier / reconstruction:** v2/v3 deterministic,
  portability, race, lineage, and product-native matrices complete; live direct
  and hosted derivative evidence remains
- **Native / browser:** F0b complete; browser fallback available
- **Direct / live / replay:** direct F0b complete; hosted F0c complete; F4 matrix
  remains
- **ChatGPT / gateway / companion:** `DEVELOPER_MODE_VERIFIED`; local public
  capability authority regression-green; Cloudflare login/deployment pending
- **MCP / Codex:** MCP derivative boundary implemented; Foldweave installed-copy
  Codex qualification remains
- **Budget:** sole USD 40 ledger unchanged; direct call cap 13 fully reserved
- **Feature freeze:** Tuesday 21 July 2026 at 01:00 CEST
- **Release materials:** stale for Foldweave; predecessor materials preserved
- **Submission hold:** `ACTIVE`
- **Blockers:** no global blocker; narrow user-owned Cloudflare login pending
- **Next operation:** publish the independently audited green checkpoint, then
  authenticate/deploy and qualify F0d through the in-app browser
