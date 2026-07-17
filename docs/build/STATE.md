# Reversible Name Atlas — Current Build State

Checkpoint: **Friday 17 July 2026 at 21:15:30 CEST**

Phase: **M7 — RELEASE CANDIDATE**

Production goal: **ACTIVE**

H+0: **Friday 17 July 2026 at 17:16:25 CEST**

## Schedule at this checkpoint

- Recording-ready boundary: Tuesday 21 July 2026 at 02:00 CEST
- Submission boundary: Wednesday 22 July 2026 at 02:00 CEST
- Product time remaining: 76 hours 44 minutes 29 seconds
- Total time to submission: 100 hours 44 minutes 29 seconds
- Protected submission reserve: 24 hours
- Compression: not required; ordinary H+ targets remain in force

Targets force integration and scope control. They are not cancellation timers.

## Verified repository state

- Repository: `/Users/nikolai/Desktop/Repos/reversible-name-atlas`
- Branch: `main`
- Scaffold baseline:
  `f1c519d215790d9e9949c5991c96826e5a2e295b`
- Feature-freeze product commit:
  `819e674ba74fb86d981f390d52214de5b4e4f7a7`
- M6 live/replay release commit:
  `d71b0b903a8259b158e1d674c5735edb88a6c665`
- No Git remote or public repository exists yet.
- The working tree was clean immediately after the M6 release commit. This
  synchronized plan/state checkpoint is the only current change.

## Verified release evidence

- M0 through M6: **COMPLETE**. Feature freeze remains active.
- Hero: 12 stable families, 28 content objects, 30 source-package members, one
  Meaning-risk family, and one casefold collision pair.
- One explicit live request used the exact `gpt-5.6` alias and the complete
  visible hero evidence packet. The returned card passed schema, evidence-ID,
  candidate-path, and advisory-authority validation.
- Canonical replay record:
  `src/name_atlas/recordings/hero_decision_card.json`; SHA-256
  `2fe0da43fe57e72043effcf13dc3a3084b8a262295e132b00109bf767f06ae00`;
  evidence fingerprint
  `0f0b0b7cf923432431e7d184c6881cb34d61a0e5caf578f87cc029494b97d830`.
- Provider-reported usage: 1,676 input tokens, 994 output tokens, and 2,670
  total tokens. Application-measured end-to-end latency: 14.645 seconds.
  Application-estimated model cost: USD 0.0382. Conservative committed budget
  reservation: USD 0.6790 of the USD 10 cap.
- The live transaction reached 12/12 explicit human resolutions, including the
  human-entered `campaign-poster` descriptor, then passed copy-only staging,
  source equality, 28 complete forward/reverse map rows, reverse dry run, every
  deterministic proof check, and Library of Congress `bagit` validation.
- Two subsequent complete replay transactions ran with `OPENAI_API_KEY` absent,
  displayed **Recorded GPT-5.6 response**, made no provider request, and reached
  the same verified result. Their staged data trees and deterministic artifacts
  are byte-identical except for the expected run location/time fields and the
  corresponding verification-report tag hash.
- The tiny negative fixture visibly and mechanically blocks staging while its
  Meaning decision is unresolved.
- Current automation: `uv lock --check`; `uv sync --frozen`; 116 pytest tests;
  Ruff lint and format; `git diff --check`; source/wheel build; local Markdown
  link scan; canonical-record validation; and repository secret scan all pass.
- Six 1280×720 product captures were visually inspected. Their captions now
  describe only visible evidence; the Atlas capture exposes no personal path.
- Two bounded M6 audits found no remaining product, record, claim, secret, or
  documented source-checkout judge-path blocker after one correction pass.

## Credential and release readiness

- A replacement restricted project API key is configured only in ignored local
  `.env`, whose mode is 600. Its value has never been committed or included in
  a release artifact.
- The first accidentally exposed one-time key was revoked before use. It is not
  the active replacement key and no request was made with it.
- Exactly one provider request has been made with the replacement key. M7 may
  use it only for a startup smoke that does not generate another card.
- After the clean-clone live-startup smoke, revoke the replacement key and
  remove local `.env`, then verify both facts without exposing the key.
- M7: **IN_PROGRESS**.
- Live GPT-5.6 implementation and recorded replay: **COMPLETE**.
- Public repository: **PENDING**.
- Recording package, public video, and Devpost submission: **PENDING**.
- Current M7 blocker: **NONE**.

## Compact recovery capsule

- Phase: M7 release candidate; M0–M6 complete; feature freeze active.
- Release commit: `d71b0b903a8259b158e1d674c5735edb88a6c665`.
- Product evidence: one real `gpt-5.6` call, one sanitized exact-fingerprint
  record, one verified live transaction, two verified keyless replay
  transactions, 116 tests, clean lint/format/build/link/secret checks.
- Budget: one request; USD 0.0382 estimated model cost; USD 0.6790 conservative
  reservation; USD 10 cap.
- Prohibitions: no discovery/tournament/harness loop; no new features; no second
  provider request; no secret exposure; no unsupported claim; no silent model
  substitution; no consumption of the final 24-hour reserve for product work.
- Credential cleanup: perform one no-request clean-clone live-startup smoke,
  then revoke the replacement key and remove ignored `.env`.
- Next operation: **Commit this synchronized M6 checkpoint, create a fresh clone
  outside the working tree at the release commit, and execute every M7 clean-
  environment check including a complete keyless replay transaction.**
