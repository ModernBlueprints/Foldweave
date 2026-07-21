# Sample-data provenance

All release-facing sample content is synthetic and was created for Foldweave
during OpenAI Build Week. It contains no personal project data and no
third-party project payload. Unless a subdirectory says otherwise, the samples
are distributed under the repository's MIT license. Historical files may retain
their original Name Atlas identity where that is necessary for provenance or
compatibility.

## Primary release fixtures: `connected_change/`

[`connected_change/`](connected_change) is the only current polished product
fixture family. It demonstrates Foldweave's review-before-execution workflow:
bounded model planning creates an immutable proposal for Sofia, and fixed code
can apply the resulting Foldweave Change File to Martin's differently arranged
equivalent project without another model call or transfer of project payload
bytes.

Its exact local provenance notes are in
[`connected_change/README.md`](connected_change/README.md).

### `connected_change/sofia_apollo/`

Sofia's source is the origin hero. It contains exactly 24 regular files under a
plausible client-project layout:

- five Markdown project and meeting notes;
- TXT and CSV research material;
- JPG and PNG images;
- WAV and MP3 audio;
- PDF documents;
- one XLSX workbook;
- one opaque binary cache file; and
- one protected `.env.example`.

The opaque formats are tiny synthetic examples. They demonstrate byte-preserving
carriage, not semantic understanding of images, media, PDFs, spreadsheets, or
binary formats.

The exact hero request is:

> Prepare this Apollo client-project folder for handoff as Northstar. Keep every file. Use the briefing and project notes to organize approved deliverables, working material, research, and meeting notes into clear folders. Rename Apollo-labelled paths to Northstar and keep every supported link working.

The final recorded hero keeps all 24 admitted files exactly once, changes 23
paths, rewrites and verifies 23 supported relative Markdown links, leaves the
protected `.env.example` fixed, preserves the explicit empty directory, and
creates a separate verified Northstar result and Foldweave Change File. Sofia's
source remains unchanged.

### `connected_change/martin_apollo/`

Martin's source contains the same 24 logical files under a genuinely different
starting layout. Ordinary corresponding files have identical payload bytes.
The five Markdown documents preserve the same prose, labels, fragments, link
order, and logical relationships, but their destination text reflects Martin's
different local paths.

For ordinary files, the deterministic receiver matcher does not use Sofia's or
Martin's source path or arbitrary lexical/iteration order. It matches ordinary
payload descriptors; for Markdown it matches all non-destination bytes and
iteratively refines the supported link-relationship graph. Protected members
and explicit empty directories retain their exact-path requirements. A
successful application produces a receiver-specific plan and receipt, an
independently verified result, and the same organized-tree commitment as
Sofia's result. Martin's reconstruction recreates Martin's own original paths
and bytes, not Sofia's layout.

### Explicit empty directory

Both hero copies logically contain `working/templates/empty`. Git cannot retain
an empty directory without adding a file, which would violate the exact 24-file
contract. The production fixture materializer therefore creates the empty
directory deterministically when it materializes the bundled demonstration.

### `connected_change/ambiguity/`

The ambiguity fixture is a separate four-file textual qualification case:

- `notes/client-approval.md` says that exactly one candidate was approved;
- `notes/internal-review.md` says that the other candidate remains internal;
- two synthetic PDF candidates are both retained; and
- neither note identifies which candidate is approved.

The request asks Foldweave to place the approved presentation in final
deliverables and the other in working material while preserving both files and
their supported links. The real GPT-5.6 qualification run asked exactly one
question:

> Which presentation is the client-approved final: Candidate A or Candidate B? The other will be placed in working material as the internal-review version.

The recorded answer identifies Candidate A as approved and Candidate B as
internal review. The same durable job then completes; no per-file review queue or
second clarification is used.

### Refusal cases

The release refusal matrix derives controlled disposable variants from the same
fixture family rather than creating more polished projects. It proves that
Foldweave blocks instead of guessing when there is:

- a changed ordinary payload;
- changed Markdown prose outside a supported destination span;
- a changed supported relationship;
- a symmetric duplicate group with no deterministic unique match;
- protected-member disagreement;
- an invalid Change File fingerprint; or
- a BagIt-valid artifact alteration inconsistent with its Foldweave receipt.

These variants are test/evidence products, not additional user-facing sample
collections. Canonical sources and accepted results are not mutated to create
them.

## Historical fixtures

The remaining sample directories are preserved as historical implementation
evidence. They are not the current judge path and must not be presented as
alternative release workflows.

### `folder_a1/`

`folder_a1/` is the small ordinary-folder walking fixture used to establish the
first AI-first vertical transaction. It helped verify complete file accounting,
protected-member handling, deterministic planning, copy-only output, and one
visible proof before the full Connected Change product existed.

### `hero/`

`hero/` is the earlier archive-specific collection fixture from the first and
second product cycles. It contains 12 synthetic object families, 30 regular
files, declared access/preservation relationships, `metadata/metadata.csv`, and
`normalization.csv`. It demonstrated the former Atlas/Decide/Stage/Verify/
Handoff workflow and remains useful only for historical regression coverage and
provenance.

Its SVGs were authored directly in the repository from XML text, geometric
shapes, and locally chosen colors. No external artwork was downloaded, traced,
or embedded.

### `negative_unresolved_meaning/`

`negative_unresolved_meaning/` is the matching historical one-family negative
fixture for the archive-specific workflow. It proved that the old human-review
transaction would not export while a Meaning decision remained unresolved. It
does not qualify the current GPT planner, Change File, receiver matcher, shared
MCP, or plugin.

## Provenance and reuse boundary

The exact boundary between the earlier feasibility spike and the repository
implementation is recorded in
[`../docs/PREEXISTING_WORK.md`](../docs/PREEXISTING_WORK.md). The current product
does not depend on the spike at runtime or in tests, and the spike's semantic,
scoring, evaluator, and tournament machinery was excluded.

The chronological Codex/GPT implementation record is
[`../docs/CODEX_BUILD_LOG.md`](../docs/CODEX_BUILD_LOG.md). The frozen selected
product contract and its claim limits are
[`../docs/build/BUILD_SPEC.md`](../docs/build/BUILD_SPEC.md).
