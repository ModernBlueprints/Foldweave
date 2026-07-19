# Pre-existing Work Disclosure

Status: **SELECTIVE MECHANICAL ADAPTATION DISCLOSED; NO WHOLESALE CODE OR RUNTIME DEPENDENCY**

This file records the boundary between Reversible Name Atlas and an earlier
Build Week feasibility spike. The spike is evidence about selected mechanical
behaviors, not the foundation, architecture, runtime dependency, or product
implementation for this repository.

## Source identity

Spike root:

`/tmp/openai-build-week-tournament/20260715T134849CEST-5685c739/spike_results/P3-CAN-ARCH-PATHMAP-001/candidate`

The active 22-entry `SHA256SUMS` inventory at that root was verified 22/22 on
17 July 2026 before scaffold creation.

| Source module | SHA-256 |
|---|---|
| `pathatlas/contracts.py` | `69e4ee549bd4a7289ff7deda82bdcbe9200d021ebad0c667186a0ef590a7ca97` |
| `pathatlas/bundle.py` | `59bc11400cda7ba939a6e13874498f9ae1fc7fec3d02ab1e54e01bbe221cec56` |
| `pathatlas/graph.py` | `347475dd1cdaa27b2fbe0b57d0d1fcf65922c0a6dedf303619fdc7bb52679aa7` |
| `pathatlas/projection.py` | `f49e5c4c2acaceb0a51dc2d563a13e3812319f073f32dcf0556660dcefd2db73` |
| `pathatlas/transaction.py` | `bca2c560dde8e3612124b8b40598d62a2e7bcdf2fb8d0d3a5fab140dce640ef3` |
| `pathatlas/semantic.py` — excluded | `1c654220fe73846fed683c5c303a266c70fd7dc0c096930edd1590c248772ea8` |

The scaffold-time ledger used the package label `name_atlas_spike/`. A bounded
17 July 2026 provenance inspection established that the live candidate package
is actually `pathatlas/`; the five eligible file hashes still match the
scaffold-time values exactly. The table above records the observed source paths.

The `/tmp` path is ephemeral. The new product must build, test, run, and disclose
provenance without that path existing. No source import, package dependency,
symbolic link, runtime lookup, test lookup, or judge command may depend on it.

## Disposition

`ADAPT` means a small behavior or focused algorithm may be reimplemented or
carefully ported into the new contract. `REWRITE` means use the behavioral lesson
only and create a fresh bounded implementation. `REJECT` means do not carry the
material into the product.

| Spike material | Eligible behavior or lesson | Disposition | Required treatment |
|---|---|---|---|
| `contracts.py` | Canonical JSON, strict relative-path checks, duplicate/non-finite rejection, exclusive-create behavior | **ADAPT** | Select only focused helpers that match the new Pydantic and path contracts |
| `bundle.py` snapshot | Inventory, regular-file enforcement, symlink/special-file rejection, size and SHA-256 snapshot | **ADAPT** | Use streamed hashing and the new ordinary Unicode-visible package contract |
| `bundle.py` CSV parsing | Exact UTF-8 and strict row/column validation | **ADAPT** | Implement only for `metadata.csv` and `normalization.csv` |
| `graph.py` | Metadata and derivative relationship modeling; unresolved-reference blockers | **REWRITE** | Build around the new `ObjectFamily` identity and supported package contract |
| `projection.py` | Transformation trace, bounded target validation, collision alternatives, edited-target validation | **ADAPT** | Implement the fixed new profile and separate exact/NFC/casefold comparisons |
| `transaction.py` staging behavior | Pre-stage re-snapshot, copy-only pending stage, no overwrite, payload verification, final promotion | **REWRITE** | Decompose into bounded staging, artifact, verification, and validator modules |
| `transaction.py` mapping behavior | One identity propagates through references and complete forward/reverse maps | **ADAPT** | Port focused algorithms only after matching `TX-007` and `VER-002` |
| Spike test scenarios | Path escape, collision, copy-only staging, overwrite refusal, reverse proof, prepare/commit/verify | **ADAPT** | Recreate behavioral scenarios in the new acceptance suite; do not copy the old harness wholesale |
| `semantic.py` | Frozen executable, prompt/compiler hashes, tournament batch transport, scoring review | **REJECT** | Never import, execute, adapt, or use as the GPT provider |
| Old CLI and bundle schema | Arm/attempt controls, raw hexadecimal path identities, fixture/evaluator contracts | **REJECT** | Do not expose in product commands, fixtures, or domain contracts |
| Evidence, scorer, repair, evaluator, and pilot machinery | Tournament validation and certification surfaces | **REJECT** | Do not copy or recreate |

The old `transaction.py` is a 2,017-line tournament-coupled monolith. It is not
eligible for wholesale transplantation. The old semantic path is pinned to a
specific local executable and tournament identity; it is incompatible with the
official Responses API provider required by `docs/build/BUILD_SPEC.md`.

## Actual-reuse disclosure rule

No fragment has been copied into this repository during scaffold creation.

Whenever implementation actually reuses a fragment or closely translates a
focused algorithm, update this file in the same product commit with:

- source module and SHA-256 from the table above;
- source symbol or exact source line range;
- destination repository path and symbol;
- `ADAPT` or `REWRITE` disposition;
- what changed to satisfy the new contract;
- relevant acceptance scenario; and
- destination commit.

Behavioral inspiration without copied code must still be described when it
materially shaped an implementation. Tournament semantic/evaluator machinery
remains excluded even if adapting it appears faster.

## Actual M1 mechanical adaptations

The M1 vertical transaction was written in the new repository rather than
copied wholesale. The bounded source inspection nevertheless materially shaped
the following implementations. All rows belong to the product commit with
subject `feat: deliver deterministic M1 walking transaction`; its exact hash is
recorded in `docs/build/STATE.md` after the commit exists.

| Verified source behavior | Destination | Disposition and contract change | Acceptance evidence |
|---|---|---|---|
| `pathatlas/contracts.py:70-75` and `pathatlas/bundle.py:49-89`; source hashes above | `src/name_atlas/source.py` — `_read_regular_file`, `snapshot_tree` | **ADAPT** — retained streamed SHA-256, deterministic ordering, and regular-file classification; added descriptor-level `fstat`, no-follow open, raw supported-tree classification, and change-during-read checks | `tests/test_package_import.py` stable snapshot, symlink, and source-change cases |
| `pathatlas/bundle.py:92-108` | `src/name_atlas/package_import.py` — `_csv_rows`, `_parse_metadata`, `_parse_normalization` | **ADAPT** — rebuilt only for the frozen UTF-8 metadata/normalization contracts and corrected the old missing-trailing-cell predicate by requiring exact row cardinality | malformed-row and reciprocal-accounting tests in `tests/test_package_import.py` |
| `pathatlas/graph.py:10-93` | `src/name_atlas/package_import.py` — `_reconcile` and `ObjectFamily` | **REWRITE** — retained the invariant that every reference resolves to one stable identity; rejected the old bundle, raw-byte, and evaluator schemas | hero family/derivative import and orphan-reference tests |
| `pathatlas/projection.py:81-189` | `src/name_atlas/proposals.py` — `project_descriptor`, `build_family_proposals` | **ADAPT** — recast the ordered projection as the fixed identifier/descriptor/role profile with structured steps and separate Meaning signals; did not reuse old encoding claims or collision keys | `campaña` to `campana` proposal and human-decision tests |
| Focused `pathatlas/transaction.py:1050-1206` copy-only lessons | `src/name_atlas/staging.py` — `stage_package`, `_copy_content_member`, control propagation | **REWRITE** — decomposed the monolith into import, decision, staging, artifact, BagIt writer, and validator boundaries; omitted every tournament arm/review/evaluator protocol | `tests/test_staging.py` and connected `tests/test_workflow.py` |
| Focused mapping/reverse invariants in `pathatlas/transaction.py:1582-1791` | `src/name_atlas/artifacts.py`, `src/name_atlas/staging.py`, and `src/name_atlas/verification/staged_proof.py` | **ADAPT** — retained complete forward/reverse map coverage and hash equality while replacing raw hexadecimal identity with stable `ObjectFamily` identity and ordinary logical paths; commit `1cce39d8c46c62eef96b9baa64b83d16765d5c03` adds independent serialized-map, control-file, source-snapshot, decision-ledger, exact data-member, and reverse-reference read-back under the new contract | map/control/state-artifact tampering, extra-payload, post-BagIt payload-change, staged-hash, source-equality, report, reverse-dry-run, and BagIt assertions |

No code, prompt, executable, scoring rule, or transport behavior from
`pathatlas/semantic.py` was inspected, imported, executed, or adapted. The
product has no runtime, test, or judge-path dependency on the ephemeral spike
root.

## Current release provenance

The table above is the complete adaptation record for the disclosed feasibility
spike. No additional source fragment, prompt, executable, scoring rule,
evaluation harness, or transport implementation from that spike was copied or
imported during the later product cycles.

The current Connected Change release evolved from work already written in this
same repository during Build Week. That internal evolution is disclosed here so
the final product is not presented as if every subsystem appeared for the first
time in the last revision.

| Build Week checkpoint | Reused repository-owned foundation | New or materially rewritten work at that checkpoint |
|---|---|---|
| Public archive baseline `4baec1e` | Source scanning and hashing; copy-only pending/final promotion; canonical JSON; BagIt packaging; receiver receipt verification; reconstruction; FastAPI/Jinja shell; locally packaged Blueprint assets | Archive-specific Migration Case, portable receipt, verifier, five-state workbench, and release infrastructure |
| A1 `5609ca6` | The mechanical scanner, hashing, copy, BagIt, browser, and packaging lessons already implemented in the repository | Generic ordinary-folder inventory and identities; protected-member classification; complete-file planner schema; deterministic compiler; separate result transaction; Start/Working/Done surface |
| A2 `04f6b89` | A1 generic-folder contracts and repository persistence patterns | Exact-span Markdown parser and link graph; bounded evidence tools; planner turn/repair/clarification authority; source-staleness and restart-safe browser transaction |
| A3 `e3803d2` | Existing BagIt, atomic-write, receipt, verification, and reconstruction mechanics, adapted to the generic folder schemas | Strict `FolderRefactorJob.v1`; complete path-neutral folder artifact family; preserved original Markdown bytes; source-free verifier; exact altered-result refusal; exact folder reconstruction |
| Connected Change C0 `a5ea342` and C1 `c94c26b` | A1–A3 scanner, compiler, link rewriter, copy transaction, job, receipt, verifier, and reconstruction services | Name Atlas Change File; path-independent member descriptors; deterministic fixed-point receiver matcher; safe in-root parent links; `gpt_planned`/`capsule_applied` provenance; v2 job/plan/receipt contracts; receiver-specific result, receipt, verification, convergence, and reconstruction |
| C2 `852fc55` | The same server-owned job and transaction services | Home/Organize/Apply/Working/Done release surface; bounded native macOS picker; verified Finder bridge; truthful receiver progress and Change File download/application experience |
| C3 `9e8d3db` | The bounded planner/provider and fixture machinery created in A1–A3 | Final 24-file Sofia/Martin fixtures; two new real GPT-5.6 planner records; exact sanitized replays; final convergence and refusal evidence; monotonic migration of the sole budget ledger |
| C4 `bc1898e` | The existing browser/CLI domain services and durable v2 job | One shared seven-tool STDIO MCP server, consent and job-bound idempotency, restart recovery, and actual Codex tool qualification |
| C5 `7314c58` / feature-freeze checkpoint `0dc4776` | The verified shared MCP server | Thin Codex plugin and repository marketplace metadata; clean-clone installation, fresh-task discovery/invocation, installed-cache proof, and uninstall instructions |

The Connected Change matcher, Change File contracts, v2 provenance and receipt
semantics, receiver application, current browser journeys, shared MCP server,
and Codex plugin were implemented in this repository for the current Build Week
submission. They are not wrappers around the old spike and do not import it at
runtime or during tests.

The Codex plugin's initial manifest structure was created through OpenAI's
official plugin-creator workflow after its product gate returned `GO`. The
committed plugin contains only marketplace metadata and a relative MCP
configuration around the same Name Atlas server; it contains no copied product
implementation.

The historical archive release and A1–A3 checkpoints remain in ordinary Git
history as traceable predecessors. The selected release-facing product is the
feature-frozen `CONNECTED_CHANGE_GO` profile, and the public documentation must
not present the superseded archive workflow as its current experience.
