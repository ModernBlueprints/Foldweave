# Limitations and claim boundaries

Reversible Name Atlas is a Build Week MVP with one deliberately strict package
contract and one repository-ready transformation profile. Its verification
claim applies only to the supported transaction described in
[`build/BUILD_SPEC.md`](build/BUILD_SPEC.md). It is not a production-readiness,
compliance, semantic-correctness, or universal-preservation claim.

## Live and replay evidence boundary

One real `gpt-5.6` card was generated from the exact visible hero packet and
persisted as the canonical sanitized replay record. The full hero transaction
then passed twice in replay mode with `OPENAI_API_KEY` absent. The record is
bound to its model alias, schema version, and complete evidence fingerprint; it
cannot be used for another source.

This proves one bounded live response and deterministic replay for the included
fixture. It does not establish general model reliability, semantic correctness,
workflow coverage, or scalability. Live mode still requires a separately
configured local credential and an explicit Generate action. Replay data must
come from a real validated response; a hand-authored or fabricated card is not
an acceptable substitute.

## Supported scope only

The MVP supports regular files inside one selected local root, required UTF-8
`metadata/metadata.csv`, optional UTF-8 `normalization.csv`, at most one access
and one preservation derivative per original, one fixed identifier-based path
profile, explicit whole-family human decisions, and all-or-nothing copy-only
BagIt staging.

The MVP does not support:

- `path_plan.csv`;
- arbitrary schema mapping;
- spreadsheets other than the two declared CSV contracts;
- many-to-many derivative relationships;
- external catalogs or databases;
- ArchivesSpace, AtoM, or live Archivematica integration;
- embedded-link discovery in PDFs, office files, databases, or media;
- legacy raw filename-byte recovery;
- source mutation;
- partial package export;
- accounts, collaboration, permissions, hosted deployment, or cloud storage;
- a Codex plugin or MCP runtime interface;
- Linux or Windows as tested judge platforms; or
- a general policy/profile builder.

Unsupported, malformed, ambiguous, orphaned, colliding, refused, unresolved,
or changed input blocks the complete package. The product does not attempt a
best-effort partial migration.

## What integrity verification does not prove

The product must not claim preservation of:

- filesystem access-control lists;
- extended attributes;
- file creation or modification timestamps;
- resource forks;
- undeclared external references;
- arbitrary embedded links;
- every filesystem's byte-level filename representation; or
- data or relationships outside the declared supported package.

Passing the in-scope checks and Library of Congress `bagit` validation does not
prove:

- semantic correctness;
- universal or mathematical reversibility;
- full filesystem preservation;
- live Archivematica acceptance;
- Archivematica certification, compatibility, or integration;
- archival, legal-record, regulatory, or compliance certification; or
- that a downstream repository will accept the package.

The exact phrase **Verified round-trip integrity within the supported package
contract** is permitted only when every requirement in `VER-002` passes. It
means that the source snapshot remained equal, content-object hashes match,
only declared reference fields changed, declared links resolve, targets satisfy
the one profile without exact/NFC/casefold collisions, forward and reverse maps
are complete inverses, reverse dry run succeeds, no decision or invariant
remains unresolved, `bagit` validation passes, and the UI agrees with the
serialized report.

## GPT-5.6 is advisory

GPT-5.6 receives only the bounded text evidence displayed before the request.
It does not receive source payload bytes. Its structured card can explain
possible interpretations, possible meaning loss, uncertainty, and a
discriminating question. It cannot:

- determine the correct name;
- establish semantic truth;
- approve or edit a family;
- set a final target;
- verify safety or correctness;
- make a package exportable; or
- override a deterministic blocker.

Missing credentials, unknown evidence, malformed output, API failure, model
unavailability, cost-cap exhaustion, or a mismatched replay record leaves the
family unresolved.

## Claims this project does not make

Reversible Name Atlas does not claim:

- that the problem is a critical or universal crisis;
- that archivists constantly experience it;
- 50% or any other unmeasured time saving;
- faster recurring work;
- that GPT-5.6 determines the correct name;
- that AI verifies semantic correctness or safety;
- that wrong transformations cannot occur;
- mathematical or universal reversibility;
- full filesystem preservation;
- compliance certification or legal-record assurance;
- Archivematica certification, compatibility, or live integration;
- that Archivematica expects clean input or lacks filename handling;
- that all bulk renamers break metadata;
- support for arbitrary schemas or every archival workflow;
- million-file scalability;
- production readiness;
- institutional acceptance or adoption;
- that OpenAI or another AI lab uses or needs this workflow;
- proven superiority over ordinary Codex;
- a proven high probability of winning; or
- that nothing else exists.

No practitioner-prevalence, institutional-adoption, time-saving, recurring-speed,
or large-scale performance claim has been measured by this project. Public
descriptions should report only observed transaction facts such as families,
objects, references, moves, decisions, risk triggers, calls, cache hits,
collisions, rewrites, validation outcomes, latency, reported token usage, and
estimated model cost.
