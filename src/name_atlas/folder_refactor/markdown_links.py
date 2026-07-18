"""Exact-span scanner and rewriter for the supported Markdown-link subset."""

from __future__ import annotations

import hashlib
import posixpath
import re
from array import array
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath
from urllib.parse import quote, unquote_to_bytes

from name_atlas.folder_refactor.contracts import (
    FolderAcceptedPlan,
    FolderFile,
    FolderInventory,
)
from name_atlas.folder_refactor.markdown_contracts import (
    FolderReferenceGraph,
    MarkdownIgnoredCounts,
    MarkdownReference,
    reference_fingerprint,
)

MARKDOWN_SUFFIXES = frozenset({".md", ".markdown"})
MAX_SUPPORTED_MARKDOWN_REFERENCES = 10_000
_URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
_PERCENT_ESCAPE = re.compile(r"%[0-9A-Fa-f]{2}")
_ENCODED_SEPARATOR = re.compile(r"%(?:2[fF]|5[cC])")
_REFERENCE_DEFINITION = re.compile(r" {0,3}\[([^]\r\n]+)\]:[ \t]*(.*)")
_FENCE_OPEN = re.compile(r" {0,3}(`{3,}|~{3,})")
_LINE_END = re.compile(r"\r\n?|\n")


class MarkdownLinkError(ValueError):
    """One source document or accepted rewrite is outside the frozen subset."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class _ParsedDestination:
    text: str
    start_character: int
    end_character: int
    closing_character: int
    style: str


@dataclass(frozen=True, slots=True)
class _ResolvedDestination:
    kind: str
    target: FolderFile | None = None
    fragment: str | None = None


@dataclass(frozen=True, slots=True)
class _BacktickRun:
    start: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.start


def build_reference_graph(
    inventory: FolderInventory,
    markdown_payloads: Mapping[str, bytes],
) -> FolderReferenceGraph:
    """Scan all and only Markdown source members into one portable graph.

    ``markdown_payloads`` is an explicit, read-only boundary. The function
    performs no filesystem access and requires exact bytes for every inventory
    member whose suffix is ``.md`` or ``.markdown`` (case-insensitively).
    """

    markdown_files = tuple(
        item
        for item in inventory.files
        if PurePosixPath(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
    )
    expected_paths = {item.relative_path for item in markdown_files}
    if any(not isinstance(path, str) for path in markdown_payloads):
        _reject(
            "invalid_markdown_payload_path",
            "Markdown payload keys must be relative-path strings.",
        )
    supplied_paths = set(markdown_payloads)
    missing = sorted(expected_paths - supplied_paths)
    extra = sorted(supplied_paths - expected_paths)
    if missing:
        _reject("missing_markdown_payload", f"Missing Markdown bytes: {missing!r}")
    if extra:
        _reject(
            "unexpected_markdown_payload",
            f"Bytes were supplied for non-Markdown inventory paths: {extra!r}",
        )

    return build_reference_graph_from_reader(
        inventory,
        lambda source_file: markdown_payloads[source_file.relative_path],
    )


def build_reference_graph_from_reader(
    inventory: FolderInventory,
    reader: Callable[[FolderFile], bytes],
) -> FolderReferenceGraph:
    """Scan Markdown sequentially through an identity-checking byte reader."""

    markdown_files = tuple(
        item
        for item in inventory.files
        if PurePosixPath(item.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
    )
    files_by_path = {item.relative_path: item for item in inventory.files}
    directories = _directory_paths(inventory)
    references: list[MarkdownReference] = []
    ignored_external = 0
    ignored_anchor = 0
    for source_file in markdown_files:
        payload = reader(source_file)
        if not isinstance(payload, bytes):
            _reject(
                "invalid_markdown_payload_type",
                f"Markdown bytes must be bytes: {source_file.relative_path}",
            )
        if len(payload) != source_file.size or hashlib.sha256(payload).hexdigest() != (
            source_file.sha256
        ):
            _reject(
                "markdown_payload_binding_mismatch",
                "Markdown bytes do not match the inventory: "
                f"{source_file.relative_path}",
            )
        document_references, ignored = _scan_document(
            source_file=source_file,
            payload=payload,
            files_by_path=files_by_path,
            directory_paths=directories,
            maximum_references=(MAX_SUPPORTED_MARKDOWN_REFERENCES - len(references)),
        )
        references.extend(document_references)
        ignored_external += ignored.external_schemes
        ignored_anchor += ignored.anchor_only

    references.sort(key=lambda item: (item.source_path, item.destination_start_byte))
    return FolderReferenceGraph(
        source_commitment=inventory.source_commitment,
        references=tuple(references),
        ignored=MarkdownIgnoredCounts(
            external_schemes=ignored_external,
            anchor_only=ignored_anchor,
        ),
    )


def derive_reference_rewrites(
    graph: FolderReferenceGraph,
    accepted_plan: FolderAcceptedPlan,
) -> FolderReferenceGraph:
    """Derive canonical relative destinations from one accepted complete map."""

    if graph.source_commitment != accepted_plan.source_commitment:
        _reject(
            "accepted_plan_binding_mismatch",
            "Reference graph and accepted plan target different source inventories.",
        )
    mappings = {mapping.file_id: mapping for mapping in accepted_plan.file_mappings}
    derived: list[MarkdownReference] = []
    for reference in graph.references:
        source_mapping = mappings.get(reference.source_file_id)
        target_mapping = mappings.get(reference.target_file_id)
        if source_mapping is None or target_mapping is None:
            _reject(
                "accepted_plan_missing_reference_member",
                f"Accepted plan omits reference {reference.reference_id}.",
            )
        if source_mapping.original_path != reference.source_path or (
            target_mapping.original_path != reference.target_path
        ):
            _reject(
                "accepted_plan_reference_path_mismatch",
                "Accepted plan paths disagree with reference "
                f"{reference.reference_id}.",
            )
        source_parent = posixpath.dirname(source_mapping.target_path) or "."
        relative_target = posixpath.relpath(
            target_mapping.target_path,
            start=source_parent,
        )
        encoded_target = _encode_relative_path(relative_target)
        proposed = encoded_target + (reference.fragment or "")
        status = (
            "unchanged"
            if proposed == reference.original_destination_text
            else "rewritten"
        )
        if source_mapping.protected and status == "rewritten":
            _reject(
                "protected_markdown_link_context_unsupported",
                "A protected Markdown member would need a content rewrite to "
                "preserve a supported local link.",
            )
        if ".." in PurePosixPath(relative_target).parts:
            _reject(
                "path_traversal_unsupported",
                "Accepted paths would require an unsupported parent-traversal "
                f"destination for reference {reference.reference_id}.",
            )
        derived.append(
            reference.model_copy(
                update={
                    "proposed_destination": proposed,
                    "verification_status": status,
                }
            )
        )
    return FolderReferenceGraph(
        source_commitment=graph.source_commitment,
        references=tuple(derived),
        ignored=graph.ignored,
    )


def apply_reference_rewrites(
    original_bytes: bytes,
    *,
    source_file_id: str,
    graph: FolderReferenceGraph,
) -> bytes:
    """Apply exact verified destination replacements from right to left."""

    _decode_utf8(original_bytes, "invalid_utf8_markdown")
    references = [
        reference
        for reference in graph.references
        if reference.source_file_id == source_file_id
    ]
    chunks: list[bytes] = []
    cursor = 0
    for reference in references:
        if reference.proposed_destination is None or (
            reference.verification_status == "pending"
        ):
            _reject(
                "rewrite_not_derived",
                f"Reference has no derived destination: {reference.reference_id}",
            )
        start = reference.destination_start_byte
        end = reference.destination_end_byte
        if start < cursor or end > len(original_bytes) or end < start:
            _reject(
                "invalid_reference_span",
                f"Reference span is outside or overlaps source bytes: "
                f"{reference.reference_id}",
            )
        expected = bytes.fromhex(reference.original_destination_bytes_hex)
        if original_bytes[start:end] != expected:
            _reject(
                "reference_span_binding_mismatch",
                f"Source bytes changed at reference {reference.reference_id}.",
            )
        chunks.append(original_bytes[cursor:start])
        chunks.append(reference.proposed_destination.encode("utf-8"))
        cursor = end
    chunks.append(original_bytes[cursor:])
    return b"".join(chunks)


def verify_reference_rewrites(
    original_bytes: bytes,
    staged_bytes: bytes,
    *,
    source_file_id: str,
    graph: FolderReferenceGraph,
) -> None:
    """Fail closed unless deterministic reapplication yields staged bytes exactly."""

    expected = apply_reference_rewrites(
        original_bytes,
        source_file_id=source_file_id,
        graph=graph,
    )
    if staged_bytes != expected:
        _reject(
            "staged_markdown_mismatch",
            "Staged Markdown does not equal deterministic exact-span reapplication.",
        )


def _scan_document(
    *,
    source_file: FolderFile,
    payload: bytes,
    files_by_path: Mapping[str, FolderFile],
    directory_paths: frozenset[str],
    maximum_references: int,
) -> tuple[list[MarkdownReference], MarkdownIgnoredCounts]:
    text = _decode_utf8(payload, "invalid_utf8_markdown")
    byte_offsets = _byte_offsets(text)
    eligible = _markdown_eligible_mask(text)
    bracket_matches = _matching_brackets(text, eligible)
    ignored_definitions = _reference_definitions(
        text=text,
        eligible=eligible,
        source_path=source_file.relative_path,
        files_by_path=files_by_path,
        directory_paths=directory_paths,
    )
    references: list[MarkdownReference] = []
    external_count = 0
    anchor_count = 0
    index = 0
    while index < len(text):
        if not eligible[index]:
            index += 1
            continue
        is_image = text.startswith("![", index) and not _is_escaped(text, index)
        if is_image:
            label_start = index + 1
        elif text[index] == "[" and not _is_escaped(text, index):
            if (
                index > 0
                and text[index - 1] == "!"
                and not _is_escaped(
                    text,
                    index - 1,
                )
            ):
                index += 1
                continue
            label_start = index
        else:
            index += 1
            continue
        label_end = bracket_matches.get(label_start)
        if label_end is None:
            index += 1
            continue
        following = label_end + 1
        if following < len(text) and text[following] == "[" and eligible[following]:
            reference_end = bracket_matches.get(following)
            if reference_end is None:
                _reject(
                    "unsupported_local_link_syntax",
                    f"Malformed reference-style link in {source_file.relative_path}.",
                )
            explicit_label = text[following + 1 : reference_end]
            if not explicit_label:
                explicit_label = text[label_start + 1 : label_end]
            normalized_label = _normalize_reference_label(explicit_label)
            definition_kind = ignored_definitions.get(normalized_label)
            if definition_kind is not None:
                if definition_kind == "external":
                    external_count += 1
                else:
                    anchor_count += 1
                index = reference_end + 1
                continue
            _reject(
                "reference_style_local_unsupported",
                f"Reference-style local links are unsupported: "
                f"{source_file.relative_path}.",
            )
        if (
            following >= len(text)
            or text[following] != "("
            or (not eligible[following])
        ):
            index = label_end + 1
            continue
        parsed = _parse_inline_destination(
            text=text,
            open_parenthesis=following,
            source_path=source_file.relative_path,
        )
        if not all(
            eligible[position]
            for position in range(following, parsed.closing_character + 1)
        ):
            index = parsed.closing_character + 1
            continue
        logical_text = (
            _unescape_token_path_preserving_fragment(parsed.text)
            if parsed.style == "token"
            else parsed.text
        )
        resolved = _resolve_destination(
            destination=logical_text,
            source_path=source_file.relative_path,
            files_by_path=files_by_path,
            directory_paths=directory_paths,
        )
        if resolved.kind == "external":
            external_count += 1
        elif resolved.kind == "anchor":
            anchor_count += 1
        else:
            target = resolved.target
            if target is None:
                raise AssertionError("Resolved local destination lacks a target.")
            if len(references) >= maximum_references:
                _reject(
                    "markdown_reference_limit_exceeded",
                    "Supported Markdown reference count exceeds the "
                    f"application limit of {MAX_SUPPORTED_MARKDOWN_REFERENCES}.",
                )
            start_byte = byte_offsets[parsed.start_character]
            end_byte = byte_offsets[parsed.end_character]
            original_bytes = payload[start_byte:end_byte]
            reference_id = reference_fingerprint(
                source_file_id=source_file.file_id,
                target_file_id=target.file_id,
                destination_start_byte=start_byte,
                destination_end_byte=end_byte,
                original_destination_bytes_hex=original_bytes.hex(),
            )
            references.append(
                MarkdownReference(
                    reference_id=reference_id,
                    source_file_id=source_file.file_id,
                    source_path=source_file.relative_path,
                    target_file_id=target.file_id,
                    target_path=target.relative_path,
                    destination_start_byte=start_byte,
                    destination_end_byte=end_byte,
                    original_destination_text=parsed.text,
                    original_destination_bytes_hex=original_bytes.hex(),
                    fragment=resolved.fragment,
                    destination_style=parsed.style,
                    is_image=is_image,
                )
            )
        index = parsed.closing_character + 1
    return references, MarkdownIgnoredCounts(
        external_schemes=external_count,
        anchor_only=anchor_count,
    )


def _parse_inline_destination(
    *,
    text: str,
    open_parenthesis: int,
    source_path: str,
) -> _ParsedDestination:
    start = open_parenthesis + 1
    if start >= len(text):
        _reject(
            "unsupported_local_link_syntax",
            f"Unclosed inline link in {source_path}.",
        )
    if text[start] == "<":
        destination_start = start + 1
        end = destination_start
        while end < len(text) and text[end] not in {">", "\n", "\r"}:
            end += 1
        if end >= len(text) or text[end] != ">":
            _reject(
                "unsupported_local_link_syntax",
                f"Malformed angle destination in {source_path}.",
            )
        closing = end + 1
        if closing >= len(text) or text[closing] != ")":
            _reject(
                "unsupported_local_link_syntax",
                f"Titles or trailing syntax are unsupported in {source_path}.",
            )
        destination = text[destination_start:end]
        if not destination:
            _reject(
                "unsupported_local_link_syntax",
                f"Empty link destination in {source_path}.",
            )
        return _ParsedDestination(
            text=destination,
            start_character=destination_start,
            end_character=end,
            closing_character=closing,
            style="angle",
        )

    end = start
    while end < len(text):
        character = text[end]
        if character == ")":
            break
        if character in {"\n", "\r"} or character.isspace():
            _reject(
                "unsupported_local_link_syntax",
                f"Unquoted destinations cannot contain whitespace: {source_path}.",
            )
        if character == "(":
            _reject(
                "unsupported_local_link_syntax",
                f"Unquoted parentheses must be escaped: {source_path}.",
            )
        if character == "\\":
            if end + 1 >= len(text) or text[end + 1] not in {"(", ")"}:
                _reject(
                    "unsupported_local_link_syntax",
                    f"Unsupported Markdown destination escape: {source_path}.",
                )
            end += 2
            continue
        end += 1
    if end >= len(text) or text[end] != ")" or end == start:
        _reject(
            "unsupported_local_link_syntax",
            f"Malformed or empty inline link in {source_path}.",
        )
    return _ParsedDestination(
        text=text[start:end],
        start_character=start,
        end_character=end,
        closing_character=end,
        style="token",
    )


def _resolve_destination(
    *,
    destination: str,
    source_path: str,
    files_by_path: Mapping[str, FolderFile],
    directory_paths: frozenset[str],
) -> _ResolvedDestination:
    if destination.startswith("#"):
        return _ResolvedDestination(kind="anchor")
    scheme = _URI_SCHEME.match(destination)
    if scheme:
        scheme_name = destination[: scheme.end() - 1].casefold()
        if scheme_name == "file":
            _reject("file_url_unsupported", f"file: URL in {source_path}.")
        if len(scheme_name) == 1 and destination[scheme.end() :].startswith(
            ("/", "\\")
        ):
            _reject("absolute_path_unsupported", f"Absolute path in {source_path}.")
        return _ResolvedDestination(kind="external")
    if destination.startswith(("/", "\\")):
        _reject("absolute_path_unsupported", f"Absolute path in {source_path}.")
    path_text, separator, fragment_text = destination.partition("#")
    fragment = f"#{fragment_text}" if separator else None
    if not path_text:
        return _ResolvedDestination(kind="anchor")
    if "?" in path_text:
        _reject("query_string_unsupported", f"Query string in {source_path}.")
    _validate_percent_escapes(path_text, source_path)
    if _ENCODED_SEPARATOR.search(path_text):
        _reject(
            "encoded_separator_ambiguity",
            f"Encoded slash or backslash in {source_path}.",
        )
    decoded_bytes = unquote_to_bytes(path_text)
    if b"\x00" in decoded_bytes:
        _reject("decoded_nul", f"Decoded NUL in {source_path}.")
    try:
        decoded_path = decoded_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise MarkdownLinkError(
            "invalid_utf8_destination",
            f"Link destination is not UTF-8 in {source_path}.",
        ) from exc
    if "\\" in decoded_path or decoded_path.startswith("/"):
        _reject("absolute_path_unsupported", f"Non-POSIX path in {source_path}.")
    if "?" in decoded_path:
        _reject(
            "query_string_unsupported", f"Encoded query ambiguity in {source_path}."
        )
    components = decoded_path.split("/")
    if any(component == "" for component in components):
        _reject(
            "unsupported_local_link_syntax", f"Empty path segment in {source_path}."
        )
    if ".." in components:
        if _traversal_escapes_root(source_path, components):
            _reject(
                "outside_root_path",
                f"Link escapes the source root: {source_path}.",
            )
        _reject("path_traversal_unsupported", f"Path traversal in {source_path}.")
    normalized_components = [component for component in components if component != "."]
    if not normalized_components:
        _reject("directory_target", f"Link targets a directory in {source_path}.")
    source_parent = PurePosixPath(source_path).parent
    combined = PurePosixPath(source_parent, *normalized_components).as_posix()
    if combined.startswith("../") or combined == "..":
        _reject("outside_root_path", f"Link escapes the source root: {source_path}.")
    if combined in directory_paths:
        _reject("directory_target", f"Link targets directory {combined!r}.")
    target = files_by_path.get(combined)
    if target is None:
        folded_matches = [
            candidate
            for candidate in files_by_path
            if candidate.casefold() == combined.casefold()
        ]
        if folded_matches:
            _reject(
                "case_mismatched_target",
                f"Case-sensitive target mismatch {combined!r}; candidates="
                f"{sorted(folded_matches)!r}.",
            )
        _reject("dangling_target", f"Link target does not exist: {combined!r}.")
    return _ResolvedDestination(
        kind="local",
        target=target,
        fragment=fragment,
    )


def _reference_definitions(
    *,
    text: str,
    eligible: Sequence[int],
    source_path: str,
    files_by_path: Mapping[str, FolderFile],
    directory_paths: frozenset[str],
) -> dict[str, str]:
    ignored_labels: dict[str, str] = {}
    for line_start, line_end in _line_ranges(text):
        if line_start >= len(text) or not eligible[line_start]:
            continue
        line = text[line_start:line_end].rstrip("\r\n")
        match = _REFERENCE_DEFINITION.fullmatch(line)
        if match is None:
            continue
        label = _normalize_reference_label(match.group(1))
        remainder = match.group(2).strip()
        if not remainder:
            _reject(
                "unsupported_local_link_syntax",
                f"Empty reference definition in {source_path}.",
            )
        if remainder.startswith("<"):
            closing = remainder.find(">", 1)
            if closing < 0:
                _reject(
                    "unsupported_local_link_syntax",
                    f"Malformed reference definition in {source_path}.",
                )
            destination = remainder[1:closing]
        else:
            destination = remainder.split(maxsplit=1)[0]
        logical = _unescape_token_destination(destination)
        resolved = _resolve_destination(
            destination=logical,
            source_path=source_path,
            files_by_path=files_by_path,
            directory_paths=directory_paths,
        )
        if resolved.kind in {"external", "anchor"}:
            ignored_labels[label] = resolved.kind
            continue
        _reject(
            "reference_style_local_unsupported",
            f"Reference-style local definition is unsupported: {source_path}.",
        )
    return ignored_labels


def _markdown_eligible_mask(text: str) -> bytearray:
    eligible = bytearray(b"\x01") * len(text)
    fence_character: str | None = None
    fence_length = 0
    for line_start, line_end in _line_ranges(text):
        line = text[line_start:line_end]
        body = line.rstrip("\r\n")
        if fence_character is not None:
            _mark_false(eligible, line_start, line_end)
            stripped = body.lstrip(" ")
            indentation = len(body) - len(stripped)
            if indentation <= 3:
                run = len(stripped) - len(stripped.lstrip(fence_character))
                trailing = stripped[run:]
                if run >= fence_length and not trailing.strip():
                    fence_character = None
                    fence_length = 0
            continue
        opening = _FENCE_OPEN.match(body)
        if opening is not None:
            run = opening.group(1)
            fence_character = run[0]
            fence_length = len(run)
            _mark_false(eligible, line_start, line_end)
            continue
        if body.startswith("\t") or body.startswith("    "):
            _mark_false(eligible, line_start, line_end)
            continue
    _mask_inline_code_spans(text, eligible)
    return eligible


def _mask_inline_code_spans(text: str, eligible: bytearray) -> None:
    """Mask matching backtick spans, including multiline code spans."""

    runs = _eligible_backtick_runs(text, eligible)
    next_run_with_length: dict[int, int] = {}
    latest_run_by_length: dict[int, int] = {}
    for run_index in range(len(runs) - 1, -1, -1):
        run = runs[run_index]
        following = latest_run_by_length.get(run.length)
        if following is not None:
            next_run_with_length[run_index] = following
        latest_run_by_length[run.length] = run_index

    masked_until = 0
    for run_index, run in enumerate(runs):
        if run.start < masked_until:
            continue
        closing_index = next_run_with_length.get(run_index)
        if closing_index is None:
            continue
        closing = runs[closing_index]
        _mark_false(eligible, run.start, closing.end)
        masked_until = closing.end


def _eligible_backtick_runs(
    text: str,
    eligible: Sequence[int],
) -> list[_BacktickRun]:
    """Tokenize eligible, unescaped backtick runs once in linear time."""

    runs: list[_BacktickRun] = []
    index = 0
    while index < len(text):
        if not eligible[index] or text[index] != "`" or _is_escaped(text, index):
            index += 1
            continue
        run_end = index
        while run_end < len(text) and eligible[run_end] and text[run_end] == "`":
            run_end += 1
        runs.append(_BacktickRun(start=index, end=run_end))
        index = run_end
    return runs


def _matching_brackets(
    text: str,
    eligible: Sequence[int],
) -> dict[int, int]:
    """Map eligible opening brackets to their line-local closes in one pass."""

    openings: list[int] = []
    matches: dict[int, int] = {}
    for index, character in enumerate(text):
        if not eligible[index]:
            continue
        if character in {"\n", "\r"}:
            openings.clear()
            continue
        if character not in {"[", "]"} or _is_escaped(text, index):
            continue
        if character == "[":
            openings.append(index)
        elif openings:
            matches[openings.pop()] = index
    return matches


def _validate_percent_escapes(value: str, source_path: str) -> None:
    index = 0
    while index < len(value):
        if value[index] != "%":
            index += 1
            continue
        match = _PERCENT_ESCAPE.match(value, index)
        if match is None:
            _reject(
                "malformed_percent_escape",
                f"Malformed percent escape in {source_path}.",
            )
        index = match.end()


def _unescape_token_destination(value: str) -> str:
    result: list[str] = []
    index = 0
    while index < len(value):
        if value[index] == "\\":
            if index + 1 >= len(value) or value[index + 1] not in {"(", ")"}:
                _reject(
                    "unsupported_local_link_syntax",
                    "Unsupported Markdown destination escape.",
                )
            result.append(value[index + 1])
            index += 2
        else:
            result.append(value[index])
            index += 1
    return "".join(result)


def _unescape_token_path_preserving_fragment(value: str) -> str:
    path, separator, fragment = value.partition("#")
    unescaped_path = _unescape_token_destination(path)
    return unescaped_path + (f"#{fragment}" if separator else "")


def _encode_relative_path(value: str) -> str:
    parts = value.split("/")
    return "/".join(
        part if part in {".", ".."} else quote(part, safe="-._~") for part in parts
    )


def _directory_paths(inventory: FolderInventory) -> frozenset[str]:
    directories: set[str] = set()
    for file in inventory.files:
        parts = PurePosixPath(file.relative_path).parts
        for index in range(1, len(parts)):
            directories.add(PurePosixPath(*parts[:index]).as_posix())
    for empty in inventory.empty_directories:
        parts = PurePosixPath(empty.relative_path).parts
        for index in range(1, len(parts) + 1):
            directories.add(PurePosixPath(*parts[:index]).as_posix())
    return frozenset(directories)


def _traversal_escapes_root(source_path: str, components: list[str]) -> bool:
    stack = list(PurePosixPath(source_path).parent.parts)
    if stack == ["."]:
        stack = []
    for component in components:
        if component in {"", "."}:
            continue
        if component == "..":
            if not stack:
                return True
            stack.pop()
        else:
            stack.append(component)
    return False


def _decode_utf8(payload: bytes, code: str) -> str:
    try:
        return payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise MarkdownLinkError(code, "Markdown content must be valid UTF-8.") from exc


def _byte_offsets(text: str) -> array[int]:
    offsets = array("I", [0])
    total = 0
    for character in text:
        total += len(character.encode("utf-8"))
        offsets.append(total)
    return offsets


def _line_ranges(text: str) -> Iterator[tuple[int, int]]:
    if not text:
        yield 0, 0
        return
    start = 0
    for match in _LINE_END.finditer(text):
        end = match.end()
        yield start, end
        start = end
    if start < len(text):
        yield start, len(text)


def _mark_false(values: bytearray, start: int, end: int) -> None:
    values[start:end] = b"\x00" * (end - start)


def _is_escaped(text: str, index: int) -> bool:
    backslashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _normalize_reference_label(value: str) -> str:
    return " ".join(value.split()).casefold()


def _reject(code: str, message: str) -> None:
    raise MarkdownLinkError(code, message)
