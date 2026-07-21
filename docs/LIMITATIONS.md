# Foldweave limitations and claim boundaries

**Foldweave — Change the structure. Keep the connections.**

Foldweave is a local-first Build Week application for one precise job: propose
and review a reorganization of a connected project folder, preserve every
admitted file and the supported relative Markdown links between those files,
and create a separate verified result only after the user accepts the exact
preview. It is not a universal file manager, content-understanding system,
synchronization service, real-time collaboration product, or production backup
system.

This document describes the current supported contract and the limits on public
claims. A checked-in implementation, passing unit test, or visible UI is not by
itself evidence that an external distribution surface is publicly available.

## Qualification status at the current checkpoint

Checkpoint `719fc182bbd91e88cd1fa1fd6142d3d061f2aa87` remains the verified
integrated implementation baseline. Product release baseline
`4e9ec44b02b25f515017ceb9922fff4fdf84ae46` is preserved; final UI/runtime
correction checkpoint `68aba38a643d95f69e9aacd392904ef310f6994c` passed
renewed clean-clone acceptance and is included in the release fast-forwarded to
public `main`.
Its product, capture package, and 2:55 public Build Week video are complete; the
Devpost entry remains unsubmitted. The following distinctions are part of the
claim boundary:

| Surface | Current evidence-backed state |
|---|---|
| Review-before-execution authority | Qualified for origin and receiver jobs, including exact preview acceptance and fail-closed stale/duplicate/substituted authority |
| Native direct mode | Qualified in the packaged Apple-Silicon app: Keychain configure/read/remove and a separately scoped bounded live transaction with revision, exact acceptance, verification, reconstruction, restart, and clean shutdown; the development credential was removed |
| Native visual system | Objective conformance passed for the restrained macOS dark utility language across native, browser, review, settings, pairing, Done/proof, and widget surfaces, including large/narrow fixtures, keyboard behavior, focus, overflow, and measured contrast; this is not a claim of every user's subjective preference |
| ChatGPT developer mode | `DEVELOPER_MODE_VERIFIED` in the actual macOS ChatGPT app through the Secure MCP Tunnel; this is not consumer distribution |
| Consumer gateway and pairing | `CONSUMER_PAIRING_VERIFIED` through the user-authorized Google Chrome route: ChatGPT connector OAuth, device pairing, outbound companion WSS, opaque local selection, consumer origin and receiver-derivative transactions, reconnect, refusal checks, verification, and reconstruction passed. Worker version `77598fb6-72e4-48ee-919e-27488a60a515` serves final `review-v37`; technical `PUBLICATION_READY` is achieved for review submission |
| Codex | Foldweave plugin `0.1.0+codex.20260721091729` is installed and enabled from the repository marketplace; installed cache inspection and stdio MCP initialization/tool discovery pass against the same local MCP server |
| Integrated regression | 1,184 Python tests passed with one upstream deprecation warning; frontend passed 80/80; gateway passed 50/50; the sole direct ledger remained byte-identical at SHA-256 `d76924e416de3e8a6f4cd7878399f9d54d711b1fadd6fa57dd524264ebd21af9` |
| Public ChatGPT availability | Not submitted for review, approved, published, publicly listed, or claimed |
| Foldweave product release candidate | Accepted and fast-forwarded to public `main`; public video verified at <https://youtu.be/aQgpK5z9OUQ>; `/feedback` Session ID captured privately for the required submission field; personal attestations and explicit hold release remain separate gates |

The operational checkpoint in `docs/build/STATE.md` changes as qualification
continues. This document intentionally states only the minimum durable boundary
needed to prevent an implementation surface from being described as an
available consumer product before its full transaction is observed.

## Review before execution

Every new Foldweave transaction stops in review before it can create a result.
The review shows the selected source structure and one complete proposed
structure from a single immutable `folder-plan-preview.v1` value. The preview
accounts for every admitted file, protected member, explicit empty directory,
and supported link effect.

The action **Accept this structure and create copy** binds the durable job
revision, source commitment, candidate fingerprint, preview fingerprint,
destination, channel, and idempotency key. Stale tabs, changed sources, changed
Change Files, changed destinations, concurrent revisions, duplicate clicks, and
conflicting retries block rather than authorizing a different proposal.

A user can request at most two model-assisted revisions for one planning job.
Each successful revision creates a complete replacement preview and fixed code
rechecks file accounting, protected members, paths, collisions, and supported
link rewrites. A failed revision leaves the preceding valid proposal intact;
the failed proposal cannot be accepted as if it succeeded. Mechanical checker
failures are not converted into open-ended model retries.

No source file is renamed, moved, edited, or deleted. No result, receipt, or
transferable Change File exists merely because a proposal reached review.

## What Foldweave changes

Within the supported contract, Foldweave can:

- rename files;
- move files into a new folder structure;
- preserve every admitted source file exactly once;
- preserve protected members at their original relative paths;
- update supported relative Markdown links when a note, its target, or both
  move;
- compare a receiver's differently arranged local tree with a shared proposal;
- revise a shared proposal into a new derivative proposal; and
- create a separate verified result while leaving the selected source unchanged.

Foldweave does not delete, omit, merge, deduplicate, extract, convert, or edit
the general contents of files. It does not refactor source code or repair
imports, configuration, databases, application references, spreadsheets,
Office/PDF links, or media-library catalogs. A request that requires those
operations is outside the supported contract and must not produce an accepted
result.

The demonstrated JPG, PNG, WAV, MP3, PDF, XLSX, and other opaque formats are
copied byte-for-byte. A planning model does not inspect or semantically
understand their contents; it can use only their admitted path and basic
metadata as planning evidence.

## Admitted folder boundary

One job accepts an existing readable local directory containing:

- 1 to 500 regular files;
- at most 1,000 directories;
- regular files and directories only; and
- at most 10,000 supported local Markdown references.

Each `.md` or `.markdown` file is limited to 16 MiB. Symlinks, hard-linked
regular files, special files, unreadable members, changing sources, overlapping
source/result locations, insufficient free space, or an existing final result
block the transaction. Hidden files are included rather than silently skipped.
Empty directories are represented explicitly.

Foldweave uses a conservative naming profile: Unicode NFC, bounded component
and path lengths, no Windows-reserved basenames or forbidden characters,
exact/NFC/casefold uniqueness, and no file/directory ancestor conflicts. That is
an application rule set, not a claim of native operation on every filesystem.

A Foldweave Change File is limited to 16 MiB of strict UTF-8 JSON. Invalid
UTF-8, duplicate JSON keys, non-finite values, unknown fields, unsupported
schema versions, oversized files, and invalid canonical fingerprints block
before receiver execution.

## Protected members

Dotfiles, members below dot-directories or version-control directories, and
common credential/key filenames are protected. They remain in the complete
inventory and result, keep their exact original relative paths, and their
contents are not offered to a planning model.

A protected Markdown file containing a supported local link is outside this
release contract because preserving the relationship could require exposing or
rewriting content that Foldweave deliberately keeps out of planning.

## Supported connections

“Connections” means only the supported relative Markdown links inside the
selected folder. Foldweave handles a deliberately narrow, testable subset:

- UTF-8 `.md` and `.markdown` files;
- inline links and inline images;
- a destination inside angle brackets, or an unquoted destination without
  literal whitespace or unescaped parentheses;
- relative local file targets, including lexically safe in-root `../` paths;
- optional fragments; and
- UTF-8 percent encoding.

Foldweave preserves every byte outside the exact accepted destination spans and
proves that each rewritten link still resolves to the same logical file.

External schemes and anchor-only links are left unchanged. Root-relative or
absolute paths, `file:` URLs, query strings, root escape, malformed escapes,
encoded slash/backslash ambiguity, directory or dangling targets,
case-mismatched targets, and local reference-style links/definitions are not
supported. Foldweave does not claim to preserve arbitrary links embedded in
Office documents, PDFs, source code, databases, design files, or media catalogs.

## Four execution modes

Foldweave keeps four model and credential modes separate:

| Mode | Model inference | Credential and billing boundary |
|---|---|---|
| Native direct API | Exact `gpt-5.6` through the OpenAI Responses API | Uses the user's OpenAI API key and the sole Foldweave direct-API budget ledger |
| ChatGPT-hosted | Model supplied by the user's ChatGPT session | Uses no Foldweave Responses API key and makes no Foldweave direct-API budget reservation |
| Recorded replay | None | Keyless, model-free replay of exact labelled planning evidence |
| Unchanged Change File application | None | Keyless and model-free deterministic preparation, review, and execution |

A ChatGPT subscription and OpenAI API billing are separate. Pairing Foldweave
with ChatGPT does not turn a ChatGPT subscription into Responses API credit. The
ChatGPT-hosted path is truthful only when the ChatGPT session supplies model
inference; it may not silently call the direct API.

Codex is an additional access surface over the same bounded MCP and deterministic
domain services. It does not create a fifth model-provenance category or a
second execution engine.

## Direct GPT-5.6 boundary

Direct live planning uses exact model alias `gpt-5.6`, the Responses API,
strict tools and schemas, `store=false`, no model fallback, and no provider
retry. The model receives the plain-English instruction, relative names and
folder structure, basic file metadata, selected excerpts from eligible text and
Markdown files, and supported-link context. It does not receive absolute local
paths, protected contents, credentials, or arbitrary opaque file bytes.

The model proposes a complete plan or a strict bounded revision. Fixed code
requires every eligible file exactly once, injects protected files and empty
directories, checks names and relationships, derives link rewrites, renders the
preview, copies the accepted data, and verifies the result. A model cannot
write, rename, delete, promote, approve, or verify files and cannot manufacture
receipt or verifier authority.

`store=false` means Foldweave does not ask the Responses API to retain the
generated response as retrievable application state. Standard abuse-monitoring
and prompt-caching retention may still apply. Foldweave does not claim zero
retention, complete privacy, or that nothing leaves the computer during direct
live planning.

The native application stores a direct API key in macOS Keychain. The key is
read by the trusted Python process only; it does not enter React, the DOM,
browser storage, jobs, receipts, replays, MCP traffic, ChatGPT, logs, or
screenshots. Development and automated qualification may use an environment
credential without copying it into the product Keychain item.

## ChatGPT-hosted and companion boundary

The ChatGPT architecture is:

`ChatGPT app and Foldweave widget -> authenticated public gateway -> paired outbound companion -> local deterministic engine`

The remote widget cannot inspect the local filesystem. Folder and Change File
selection occurs through the local companion, and the host receives opaque
handles rather than absolute local paths. The local durable job remains the
sole product-operation and idempotency authority; the gateway is not a second
planner, job store, receipt service, or filesystem authority.

ChatGPT-hosted planning uses bounded Foldweave evidence tools and returns a
complete proposal for deterministic compilation. Current-tree extraction,
receiver matching, preview construction, acceptance, execution, verification,
and reconstruction are deterministic. Martin's current tree can therefore be
rendered against a shared proposal without a GPT call.

The checked-in gateway and companion implementation is now deployed at
<https://foldweave-gateway.skybert-ghostline.workers.dev>, version
`77598fb6-72e4-48ee-919e-27488a60a515`, serving the `review-v37` widget. The
earlier
`ERR_BLOCKED_BY_CLIENT` occurred at the Codex in-app Browser policy layer. The
user-authorized Google Chrome route completed ChatGPT connector OAuth, device
pairing, outbound companion WSS, opaque local selection, complete consumer
origin and receiver-derivative transactions, disconnect/reconnect, deployed
refusal checks, verification, and reconstruction. This evidence establishes
`CONSUMER_PAIRING_VERIFIED` and narrow technical `PUBLICATION_READY` for review
submission.

Those states do not establish review submission, approval, publication,
directory availability, or public listing. Foldweave must not be described as
publicly listed or universally available inside ChatGPT. The standard
component-authored `ui/message` revision request was acknowledged and displayed
but did not automatically cause a host tool call; one explicit
same-conversation continuation was required and verified for each consumer
revision.

## Change File and collaboration boundary

New Foldweave output uses a complete `*.foldweave-change.json` file. It can be
applied unchanged to a strictly equivalent receiver source, or used as the
immutable parent of one model-assisted derivative job. An unchanged application
uses no model and does not touch the direct-API budget. A derivative revision
does use the selected live planning transport and therefore cannot be described
as `capsule_applied`.

A derivative child Change File is complete and self-contained. It records only
its immediate parent identity rather than recursively embedding every ancestor.
The workflow supports explicit serial forks; it does not implement automatic
merge, live co-editing, accounts, permissions, or cloud synchronization.

A Foldweave Change File contains no project payload bytes. It does contain
sensitive project metadata: names and structure, file sizes and hashes,
supported-link relationships, the original instruction, target names, lineage,
and proof identifiers. “No project payload bytes are transferred” is accurate;
“nothing about the project is shared” is not.

Receiver matching is deterministic and intentionally conservative. Ordinary
files must match exact size and SHA-256 descriptors. Markdown prose, labels,
line endings, fragments, link count/order, and supported relationship structure
must match; only supported destination text may differ. Protected files also
require the same original relative path and bytes. Empty-directory requirements
must agree.

An extra or missing member, changed payload, changed Markdown prose, changed
supported relationship, incompatible suffix, protected-member disagreement,
empty-directory disagreement, invalid Change File, or unresolved symmetric
duplicate group blocks instead of being guessed. Foldweave does not reconcile
independently edited copies, infer semantic equivalence, or solve general graph
isomorphism.

Local unchanged Change File application initializes no model provider, reads no
API key, and makes no direct-API budget reservation. The browser fallback still
uses loopback HTTP. The ChatGPT access surface also uses gateway networking even
when the underlying unchanged application is model-free, so “no networking” is
not a universal product claim.

## Verification and reconstruction

`foldweave verify-receipt` is read-only, keyless, source-free, and independent
of the live planning provider. It validates the portable result, strict artifact
schemas, exact recorded commitments, complete file accounting, accepted paths,
supported link rewrites, inverse maps, preserved original Markdown bytes, and
reported findings.

Without `--source`, verification proves internal consistency against the source
description committed inside the result. It does not prove that the producer's
historical source was authentic. With `--source`, it additionally compares the
supplied current folder with that committed description.

The receipt and Change File are not signatures. They do not authenticate a
sender, establish authorship or institutional authorization, prevent a party
from issuing a wholly new self-consistent artifact, or provide compliance
certification. Controlled altered-result examples demonstrate receipt-bound
inconsistency detection, not tamper-proofing.

`foldweave restore-receipt` and **Recreate original layout** verify the selected
result first, refuse an existing destination, and recreate the source chosen for
that particular transaction. A receiver result reconstructs the receiver's own
starting layout, not the producer's layout or the first ancestor in a
collaboration chain.

Reconstruction does not preserve timestamps, ownership, access-control lists,
extended attributes, resource forks, hard-link or symlink identity, undeclared
references, or arbitrary filesystem state. The supported claim is limited to
recreating every in-scope source member's relative path and bytes.

## Native application and platform boundary

The tested native profile is `Foldweave.app` on macOS Apple Silicon. It uses a
pywebview shell around one private FastAPI loopback control plane. React,
TypeScript, BlueprintJS, and Vite provide the focused review tree and ChatGPT
widget; they do not own durable product state or require Node.js at runtime.

The packaged app has been qualified as an unsigned/ad-hoc judge build. No Apple
Developer ID identity is available, so Foldweave does not claim notarization,
Developer ID signing, Mac App Store distribution, or warning-free Gatekeeper
launch on every machine. The fresh clean-clone 55 MiB arm64 bundle has identifier
`com.modernblueprints.foldweave`, version `0.1.0`, minimum macOS `13.0`, and
executable SHA-256
`1c2316e26a23ecc9d3608e37d8a6ebf23ee2c128f468a9ec68018cf54cc606d4`.
Strict deep ad-hoc validation, unrelated-directory launch, Home/review rendering,
Original/Proposed switching, and clean shutdown pass. The browser and CLI remain
supported fallback paths.

Foldweave does not claim a native Windows or Linux application, mobile access,
or remote phone file access. Only macOS Apple Silicon is included in the native
release claim.

## MCP, Codex, and public distribution

One MCP implementation exposes bounded host-planning and reviewed workflow tool
families through local STDIO for Codex and Streamable HTTP for ChatGPT. It does
not expose arbitrary filesystem reads/writes/moves/deletes, shell execution,
compiler bypass, receipt construction, verification override, arbitrary
companion RPC, or provider credentials.

Mutations bind durable job identity, expected revision, exact fingerprints,
idempotency, source and Change File commitments, and trusted channel. Status
polling and preview retrieval cannot trigger a provider call.

The Foldweave Codex plugin is a thin package around that same MCP server; it does
not contain a copied planner or product engine. Version
`0.1.0+codex.20260721091729` is installed and enabled from the repository
marketplace; installed cache inspection and stdio MCP initialization/tool
discovery pass against the same local MCP server. Earlier installed-copy
workflow evidence remains version-specific. Historical Name Atlas plugin
qualification does not automatically qualify another Foldweave plugin build.

Similarly, developer-mode ChatGPT qualification, consumer pairing, publication
readiness, submission for review, approval, and public listing are separate
states. A tunnel is a developer route, not proof of the consumer gateway, and
submission for review is not approval.

## Current command boundary

The primary commands are:

- `uv run foldweave app` — native macOS application;
- `uv run foldweave app --browser` — loopback browser fallback;
- `uv run foldweave demo --mode replay` — bundled keyless proposal replay;
- `uv run foldweave run --mode live|replay --source SOURCE` — prepare an origin
  proposal and stop for review;
- `uv run foldweave apply-change CHANGE_FILE --source SOURCE` — prepare a
  receiver-local proposal and stop for review;
- `uv run foldweave preview JOB [--json]` — inspect the immutable preview;
- `uv run foldweave revise JOB --instruction TEXT --idempotency-key KEY` —
  request a bounded revision;
- `uv run foldweave accept JOB --preview-fingerprint SHA256
  --idempotency-key KEY` — accept exactly one preview and create a copy;
- `uv run foldweave verify-receipt RESULT_BAG [--source SOURCE]`;
- `uv run foldweave restore-receipt RESULT_BAG RESTORE_DESTINATION`;
- `uv run foldweave mcp --transport stdio` — local Codex MCP;
- `uv run foldweave mcp --transport streamable-http --surface
  chatgpt-hosted` — loopback ChatGPT developer transport; and
- `uv run foldweave companion register|approve|run|status|revoke` — paired
  companion lifecycle.

`run` and `apply-change` prepare review jobs; neither command executes the
proposal without a later exact `accept` action.

## Legacy compatibility

The internal Python package remains `name_atlas`, and `name-atlas` remains a
documented legacy command alias for historical workflows. Historical schema
identifiers, fingerprint domains, receipt paths, job files, proof artifacts,
and `*.nameatlas-change.json` files retain their original names and strict
dispatch semantics. Foldweave does not globally rename history or silently
migrate nonterminal legacy jobs.

Old finalized v1/v2 jobs and receipts remain readable under their original
contracts. A nonterminal legacy job requires a fresh Foldweave job rather than
being reinterpreted as `folder-refactor-job.v3`.

## Release claim boundary

Foldweave is a hackathon release, not a production-readiness claim. The
evidence demonstrates the exact tested fixtures, current macOS Apple Silicon
build, and supported contract. It does not establish universal zero-question
behavior, semantic correctness, measured time savings, market adoption, legal
compliance, universal portability or reversibility, or a universal organizer
for every file format and relationship.

The primary `/feedback` Session ID is captured and the final public video is
verified. Eligibility and ownership attestations, submission-hold release, and
Devpost submission remain separate user-owned completion steps. No release
document may imply those remaining steps occurred until their evidence exists.
