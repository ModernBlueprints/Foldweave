# Sample-data provenance

The files below `hero/` are synthetic demonstration assets created specifically
for Reversible Name Atlas during OpenAI Build Week. They contain no personal or
third-party source data and are distributed under the repository's MIT license.

The single hero package contains 12 synthetic object families and 30 regular
files: 12 originals, 16 declared derivatives, `metadata/metadata.csv`, and
`normalization.csv`. Every SVG was authored for this fixture from geometric
shapes and text; no external artwork, personal data, or third-party payload was
used.

The fixture demonstrates the complete supported package contract:

- `campaña-poster.svg` has access and preservation derivatives and deliberately
  projects `campaña` to `campana`, producing the one human Meaning decision in
  the hero story;
- `Harbor_Map.svg` (`CASE-010`) and `harbor-map.svg` (`case-010`) are distinct
  source families whose descriptor and identifier combinations produce target
  paths that differ exactly but collide under Unicode casefold comparison; a
  human descriptor edit resolves the collision;
- the remaining families exercise originals with both, one, or no declared
  derivatives, exact metadata linkage, canonical identifier adoption,
  role-bearing targets, structural moves, and synchronized family propagation.

All titles, descriptions, dates, identifiers, names, and depicted events are
fictional. The files are distributed under the repository's MIT license. This
directory is the only polished hero collection; it was expanded in place from
the walking-skeleton family rather than creating a second fixture.

The SVG source was authored directly in this repository with Codex on 17 July
2026. It uses only XML text, basic geometric paths, and locally chosen colors;
there are no downloaded, traced, or embedded external assets.

## Tiny negative fixture

The separate `negative_unresolved_meaning/` package is the single intentionally
negative fixture. It is a valid minimal supported package containing one
synthetic original and its required metadata row, with no derivatives. The
fixed profile projects `campaña` to `campana`, so the family has a mechanically
flagged Meaning risk. With that human decision left unresolved, whole-package
export must stop before creating any staged output.

Its SVG was authored directly in this repository with Codex on 17 July 2026
from basic geometric shapes and text. It contains no personal, third-party, or
downloaded source data and is distributed under the repository's MIT license.

| Original family | Declared derivatives | Intended demonstration role |
|---|---|---|
| `campaña-poster.svg` | access + preservation | One bounded Meaning-risk card and human resolution propagated to the full family |
| `river-festival-program.svg` | access + preservation | Ordinary three-member family and canonical identifier adoption |
| `oral-history-session-01.svg` | preservation | Preservation-only family |
| `neighborhood-map-1978.svg` | access + preservation | Metadata and derivative-reference propagation |
| `botanical-survey-sheet.svg` | none | Valid original-only family |
| `harbor-correspondence.svg` | access | Access-only family |
| `winter-market-photograph.svg` | access + preservation | Structural moves for a complete three-member family |
| `community-radio-log.svg` | none | Second valid original-only family |
| `textile-workshop-notes.svg` | preservation | Second preservation-only family |
| `Harbor_Map.svg` | access + preservation | Casefold-collision family A (`CASE-010`) |
| `harbor-map.svg` | access + preservation | Casefold-collision family B (`case-010`) and human edit counterpart |
| `conservation-report-final.svg` | access | Second access-only family |
