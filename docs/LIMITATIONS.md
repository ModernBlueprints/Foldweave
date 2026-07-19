# Limitations and claim boundaries

Reversible Name Atlas is a local-first Build Week project for one precise job:
rename and reorganize files in a connected project folder while accounting for
every admitted file, preserve the supported relative Markdown links between
those files, and create a separate result that can be checked and reconstructed.
It is not a universal file manager, content-understanding system,
synchronization service, or production backup product.

## What Name Atlas changes

Name Atlas can:

- rename files;
- move files into a new folder structure;
- preserve every admitted source file exactly once;
- preserve protected members at their original relative paths;
- update the supported relative Markdown links when a note, its target, or both
  move; and
- create a separate verified result while leaving the selected source folder
  unchanged.

It does not delete, omit, merge, deduplicate, extract, convert, or edit the
general contents of files. It does not refactor source code or repair imports,
configuration, databases, application references, spreadsheets, Office/PDF
links, or media-library catalogs. A request that requires those operations is
outside the supported contract and must not produce an accepted result.

The demonstrated JPG, PNG, WAV, MP3, PDF, XLSX, and other opaque formats are
copied byte-for-byte. GPT-5.6 does not inspect or semantically understand their
contents; it can use only their admitted path and basic metadata as planning
evidence.

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
Empty directories are preserved explicitly at the same relative path.

This release defines a conservative Name Atlas naming profile: Unicode NFC,
bounded component/path lengths, no Windows-reserved basenames or forbidden
characters, exact/NFC/casefold uniqueness, and no file/directory ancestor
conflicts. That is an application rule set, not a claim of native operation on
every filesystem or a tested native Windows runtime.

A Name Atlas Change File is limited to 16 MiB of strict UTF-8 JSON. Invalid
UTF-8, duplicate JSON keys, non-finite values, unknown fields, unsupported
schema versions, and invalid canonical fingerprints block before the receiver
folder is scanned.

## Protected members

Dotfiles, members below dot-directories or version-control directories, and
common credential/key filenames are protected. They remain in the complete
inventory and result, keep their exact original relative paths, and their
contents are not offered to GPT-5.6 as planning evidence.

A protected Markdown file containing a supported local link is outside this
release contract, because preserving the relationship could require exposing or
rewriting content that the product deliberately keeps out of planning.

## Supported Markdown links

Name Atlas handles a deliberately narrow, testable Markdown subset:

- UTF-8 `.md` and `.markdown` files;
- inline links and inline images;
- a destination inside angle brackets, or an unquoted destination without
  literal whitespace or unescaped parentheses;
- relative local file targets, including lexically safe in-root `../` paths;
- optional fragments; and
- UTF-8 percent encoding.

It preserves every byte outside the exact accepted destination spans and proves
that a rewritten link still resolves to the same logical file.

External schemes and anchor-only links are left unchanged. Root-relative or
absolute paths, `file:` URLs, query strings, root escape, malformed escapes,
encoded slash/backslash ambiguity, directory or dangling targets,
case-mismatched targets, and local reference-style links/definitions are not
supported. Name Atlas does not claim to preserve arbitrary links embedded in
Office documents, PDFs, source code, databases, design files, or media catalogs.

## GPT-5.6 planning boundary

GPT-5.6 is used only for the origin planning transaction. It receives the
plain-English instruction, relative names and folder structure, basic file
metadata needed to bind the plan, selected excerpts from eligible text and
Markdown files, and supported-link context. It does not receive absolute local
paths, protected contents, or arbitrary opaque file bytes.

GPT-5.6 proposes a complete rename/move plan. Fixed code then requires every
eligible file exactly once, injects protected files and empty directories,
checks names and relationships, derives link rewrites, copies the data, and
verifies the result. GPT-5.6 cannot directly write, rename, delete, promote, or
verify files. A mechanical defect may be repaired within a fixed limit; genuinely
missing user intent can produce at most one question and one answer.

The live integration uses exact model alias `gpt-5.6`, the Responses API,
strict tools, no model fallback, no provider retry, and `store=false`.
`store=false` means the application does not ask OpenAI to retain the generated
response for later API retrieval. Standard abuse-monitoring and prompt-caching
retention may still apply. The project does not claim zero retention, complete
privacy, or that nothing leaves the computer during an origin planning run.

The recorded demonstration replays two exact successful GPT-5.6 planning runs
and makes no provider call. Its interface labels that mode **Recorded GPT-5.6
planning run**.

## Name Atlas Change File boundary

A Name Atlas Change File records a verified change so another person can apply
it to a differently arranged equivalent copy without another GPT call.

It contains no project payload bytes. It does contain sensitive project
metadata: names and structure, file sizes and hashes, supported link
relationships, the original instruction, target names, and proof identifiers.
“No project payload bytes are transferred” is accurate; “nothing about the
project is shared” is not.

Receiver matching is deterministic and intentionally conservative. Ordinary
files must match exact size and SHA-256 descriptors. Markdown prose, labels,
line endings, fragments, link count/order, and supported relationship structure
must match; only the supported destination text may differ. Protected files
also require the same original relative path and bytes. Empty-directory
requirements must agree.

An extra or missing member, changed payload, changed Markdown prose, changed
supported relationship, incompatible suffix, protected-member disagreement,
empty-directory disagreement, invalid Change File, or unresolved symmetric
duplicate group blocks instead of being guessed. Name Atlas does not reconcile
independently edited copies, infer semantic equivalence, or solve general graph
isomorphism.

Applying a Change File initializes no GPT provider, requires no API key, makes
no budget reservation, and makes no external network request. The local browser
still uses loopback HTTP between the browser and the application, so the project
does not make the broader claim that the browser uses no networking at all.

## What verification proves

`name-atlas verify-receipt` is read-only, keyless, source-free, and independent
of the live job, browser, GPT provider, and network. It validates the portable
result, strict artifact schemas, exact recorded commitments, complete file
accounting, accepted paths, supported link rewrites, inverse maps, preserved
original Markdown bytes, and reported findings.

Without `--source`, verification proves internal consistency against the source
description committed inside the result. It does not prove that the producer's
historical source was authentic. With `--source`, it additionally compares the
supplied current folder with that committed description.

The receipt and Change File are not signatures. They do not authenticate a
sender, establish authorship or institutional authorization, prevent a party
from deliberately issuing a wholly new self-consistent receipt, or provide
compliance certification. The controlled altered-result example demonstrates
receipt-bound inconsistency detection, not tamper-proofing.

## Reconstruction boundary

`name-atlas restore-receipt` and **Recreate original layout** verify the result
first, refuse an existing destination, and create another folder matching that
job's admitted original relative paths and bytes. A receiver result reconstructs
the receiver's own starting layout, not the producer's different layout.

The reconstruction does not change the source, organized result, or Change
File. It does not preserve timestamps, ownership, access-control lists,
extended attributes, resource forks, hard-link or symlink identity, undeclared
references, or arbitrary filesystem state. “Recreates every in-scope source
member's relative path and bytes within the supported Name Atlas folder
contract” is the complete supported claim.

## Browser, macOS bridge, CLI, MCP, and plugin

The standard product is a loopback FastAPI/Jinja browser application. Manual
absolute path fields work on every supported judge path. On macOS, fixed
application-controlled AppleScript opens native folder/file selection and
Finder for verified job-owned results. The product is not a native desktop or
mobile application and does not provide remote phone file access.

The shared STDIO MCP server exposes exactly seven high-level Name Atlas tools.
It does not expose arbitrary file reads/writes, shell commands, direct compiler
bypass, receipt construction, or proof override. Mutation retries use the
existing durable job authority so an identical request returns the same job or
result instead of duplicating work.

The Codex plugin is a thin package around that same MCP server. It was qualified
through a clean-clone marketplace installation, a fresh Codex task, real tool
discovery and invocation, keyless replay/verification/reconstruction, and clear
missing-key live behavior. Codex is the tested plugin client. The project does
not claim tested compatibility with Claude, Cursor, OpenCode, Grok, or other
hosts that were not exercised.

## Release status

This is a hackathon release, not a production-readiness claim. The evidence
demonstrates the exact bundled fixtures and supported contract. It does not
establish universal zero-question behavior, measured time savings, market
adoption, native Windows support, legal compliance, or a universal organizer
for every file format and relationship.
