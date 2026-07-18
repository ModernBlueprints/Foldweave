"""Bounded, read-only evidence tools for folder planning."""

from __future__ import annotations

import codecs
import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol

from pydantic import JsonValue

from name_atlas.folder_refactor.contracts import FolderFile, FolderInventory
from name_atlas.folder_refactor.inventory import (
    HASH_CHUNK_SIZE,
    FolderScan,
    FolderScanError,
    scan_folder,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.planner_contracts import (
    MAX_AGGREGATE_RESULT_BYTES,
    MAX_EVIDENCE_RESULT_BYTES,
    MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES,
    EvidenceCallRecord,
    FolderEvidenceLedger,
    InspectMarkdownLinksCall,
    ListInventoryPageCall,
    PlannerInventoryFile,
    ReadTextExcerptCall,
    evidence_ledger_payload,
    evidence_record_payload,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)


class PlannerEvidenceError(RuntimeError):
    """Evidence cannot be supplied within the frozen authority boundary."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class EvidenceExecution:
    """One stable tool outcome before it is numbered in the ledger."""

    status: Literal["success", "rejected", "failed"]
    result: JsonValue | None
    error_code: str | None
    truncated: bool
    cache_hit: bool


class EvidenceService(Protocol):
    """Execute only declared read-only evidence calls."""

    def execute(
        self,
        call: ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
    ) -> EvidenceExecution:
        """Return one bounded result without filesystem mutation."""
        ...


def create_initial_evidence_ledger(
    inventory: FolderInventory,
    request: str,
) -> FolderEvidenceLedger:
    """Create the exact initial path-and-metadata evidence envelope."""

    request_id = request_fingerprint(request)
    initial_evidence: JsonValue = {
        "evidence_id": "initial_inventory",
        "empty_directories": [
            item.model_dump(mode="json") for item in inventory.empty_directories
        ],
        "files": [_planner_file_metadata(item) for item in inventory.files],
        "folder_contract": "name-atlas-ordinary-folder.v1",
        "profile": "name-atlas-cross-platform-safe.v1",
        "request": request,
        "request_fingerprint": request_id,
        "schema_version": "folder-planner-initial-evidence.v1",
        "source_commitment": inventory.source_commitment,
    }
    initial_bytes = len(canonical_json_bytes(initial_evidence))
    if initial_bytes > MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES:
        raise PlannerEvidenceError(
            "initial_evidence_limit_exceeded",
            "The complete initial inventory exceeds the outbound evidence limit.",
        )
    payload = {
        "aggregate_result_bytes": 0,
        "initial_evidence": initial_evidence,
        "initial_evidence_bytes": initial_bytes,
        "records": (),
        "request_fingerprint": request_id,
        "schema_version": "folder-evidence-ledger.v1",
        "source_commitment": inventory.source_commitment,
        "total_outbound_evidence_bytes": initial_bytes,
    }
    return FolderEvidenceLedger(
        **payload,
        evidence_fingerprint=canonical_sha256(payload),
    )


def append_evidence_execution(
    ledger: FolderEvidenceLedger,
    *,
    response_turn: int,
    call: ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
    execution: EvidenceExecution,
) -> FolderEvidenceLedger:
    """Number, bind, and append one counted evidence invocation."""

    arguments = _call_arguments(call)
    outcome: JsonValue = {
        "error_code": execution.error_code,
        "result": execution.result,
        "status": execution.status,
        "truncated": execution.truncated,
    }
    byte_count = len(canonical_json_bytes(outcome))
    if byte_count > MAX_EVIDENCE_RESULT_BYTES:
        raise PlannerEvidenceError(
            "evidence_result_limit_exceeded",
            "An evidence result exceeded its per-call byte limit.",
        )
    record_number = len(ledger.records) + 1
    record_payload: dict[str, JsonValue] = {
        "arguments": arguments,
        "cache_hit": execution.cache_hit,
        "call_id": call.call_id,
        "evidence_call_number": record_number,
        "outcome": outcome,
        "response_turn": response_turn,
        "tool_name": call.tool_name,
    }
    record = EvidenceCallRecord(
        response_turn=response_turn,
        evidence_call_number=record_number,
        call_id=call.call_id,
        tool_name=call.tool_name,
        arguments=arguments,
        status=execution.status,
        result=execution.result,
        error_code=execution.error_code,
        truncated=execution.truncated,
        cache_hit=execution.cache_hit,
        byte_count=byte_count,
        fingerprint=canonical_sha256(record_payload),
    )
    if record.fingerprint != canonical_sha256(evidence_record_payload(record)):
        raise AssertionError("Evidence record hash-domain construction diverged.")
    records = (*ledger.records, record)
    aggregate = sum(item.byte_count for item in records)
    total = ledger.initial_evidence_bytes + aggregate
    if aggregate > MAX_AGGREGATE_RESULT_BYTES:
        raise PlannerEvidenceError(
            "aggregate_evidence_limit_exceeded",
            "Aggregate evidence-tool results exceed the configured limit.",
        )
    if total > MAX_TOTAL_OUTBOUND_EVIDENCE_BYTES:
        raise PlannerEvidenceError(
            "outbound_evidence_limit_exceeded",
            "Total outbound evidence exceeds the configured limit.",
        )
    candidate_payload: dict[str, JsonValue] = {
        "aggregate_result_bytes": aggregate,
        "initial_evidence": ledger.initial_evidence,
        "initial_evidence_bytes": ledger.initial_evidence_bytes,
        "records": [item.model_dump(mode="json") for item in records],
        "request_fingerprint": ledger.request_fingerprint,
        "schema_version": ledger.schema_version,
        "source_commitment": ledger.source_commitment,
        "total_outbound_evidence_bytes": total,
    }
    candidate = FolderEvidenceLedger(
        aggregate_result_bytes=aggregate,
        initial_evidence=ledger.initial_evidence,
        initial_evidence_bytes=ledger.initial_evidence_bytes,
        records=records,
        request_fingerprint=ledger.request_fingerprint,
        source_commitment=ledger.source_commitment,
        total_outbound_evidence_bytes=total,
        evidence_fingerprint=canonical_sha256(candidate_payload),
    )
    if candidate.evidence_fingerprint != canonical_sha256(
        evidence_ledger_payload(candidate)
    ):
        raise AssertionError("Evidence ledger hash-domain construction diverged.")
    return candidate


class LocalFolderEvidenceService:
    """Read bounded evidence by stable ID from one immutable initial scan."""

    def __init__(
        self,
        scan: FolderScan,
        *,
        reference_graph: FolderReferenceGraph,
    ) -> None:
        if reference_graph.source_commitment != scan.inventory.source_commitment:
            raise PlannerEvidenceError(
                "reference_graph_mismatch",
                "Reference graph targets a different source inventory.",
            )
        self._scan = scan
        self._reference_graph = reference_graph
        self._files_by_id = {item.file_id: item for item in scan.inventory.files}
        self._cache: dict[str, EvidenceExecution] = {}

    def execute(
        self,
        call: ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
    ) -> EvidenceExecution:
        """Execute one source-equality-checked, content-bounded read."""

        cache_key = canonical_sha256(
            {"call": _call_arguments(call), "tool_name": call.tool_name}
        )
        try:
            self._require_source_unchanged()
            cached = self._cache.get(cache_key)
            if cached is not None:
                return EvidenceExecution(
                    status=cached.status,
                    result=cached.result,
                    error_code=cached.error_code,
                    truncated=cached.truncated,
                    cache_hit=True,
                )
            if isinstance(call, ListInventoryPageCall):
                execution = self._inventory_page(call)
            elif isinstance(call, ReadTextExcerptCall):
                execution = self._text_excerpt(call)
            else:
                execution = self._markdown_links(call)
            self._require_source_unchanged()
        except PlannerEvidenceError as exc:
            execution = EvidenceExecution(
                status="rejected",
                result=None,
                error_code=exc.code,
                truncated=False,
                cache_hit=False,
            )
        self._cache[cache_key] = execution
        return execution

    def _inventory_page(self, call: ListInventoryPageCall) -> EvidenceExecution:
        files = self._scan.inventory.files
        offset = _decode_cursor(
            call.cursor,
            domain="inv",
            binding=self._scan.inventory.source_commitment,
            upper_bound=len(files),
        )
        selected = list(files[offset : offset + call.page_size])
        bounded = _bounded_page(
            schema_version="folder-inventory-page.v1",
            key="items",
            values=[_planner_file_metadata(item) for item in selected],
            offset=offset,
            total=len(files),
            cursor_domain="inv",
            cursor_binding=self._scan.inventory.source_commitment,
            extra={},
        )
        truncated = bounded["next_cursor"] is not None
        return EvidenceExecution(
            status="success",
            result=bounded,
            error_code=None,
            truncated=truncated,
            cache_hit=False,
        )

    def _text_excerpt(self, call: ReadTextExcerptCall) -> EvidenceExecution:
        source_file = self._require_file(call.file_id)
        if source_file.protected:
            raise PlannerEvidenceError(
                "protected_content_denied",
                "Protected file contents cannot be sent as evidence.",
            )
        if not source_file.evidence_eligible:
            raise PlannerEvidenceError(
                "content_evidence_unsupported",
                "This file type is not eligible for text evidence.",
            )
        excerpt, end, file_size = _read_verified_utf8_window(
            self._scan.source_root / source_file.relative_path,
            source_file,
            start=call.start_byte,
            maximum=call.max_bytes,
        )
        result: JsonValue = {
            "content_is_untrusted": True,
            "end_byte": end,
            "file_id": source_file.file_id,
            "omitted_byte_count": file_size - end,
            "original_byte_count": file_size,
            "relative_path": source_file.relative_path,
            "returned_byte_count": end - call.start_byte,
            "schema_version": "folder-text-excerpt.v1",
            "start_byte": call.start_byte,
            "text": excerpt,
            "truncated": end < file_size,
        }
        bounded, truncated_by_size = _bound_text_result(result, "text")
        return EvidenceExecution(
            status="success",
            result=bounded,
            error_code=None,
            truncated=bool(bounded["truncated"]) or truncated_by_size,
            cache_hit=False,
        )

    def _markdown_links(
        self,
        call: InspectMarkdownLinksCall,
    ) -> EvidenceExecution:
        source_file = self._require_file(call.file_id)
        if source_file.protected:
            raise PlannerEvidenceError(
                "protected_content_denied",
                "Protected file link context cannot be sent as evidence.",
            )
        if Path(source_file.relative_path).suffix.casefold() not in {
            ".md",
            ".markdown",
        }:
            raise PlannerEvidenceError(
                "markdown_link_evidence_unsupported",
                "Only Markdown files have supported-link evidence.",
            )
        references = [
            item.model_dump(mode="json")
            for item in self._reference_graph.references
            if item.source_file_id == call.file_id
        ]
        cursor_binding = canonical_sha256(
            {
                "file_id": call.file_id,
                "source_commitment": self._scan.inventory.source_commitment,
            }
        )
        offset = _decode_cursor(
            call.cursor,
            domain="links",
            binding=cursor_binding,
            upper_bound=len(references),
        )
        bounded = _bounded_page(
            schema_version="folder-markdown-link-evidence.v1",
            key="references",
            values=references[offset : offset + call.page_size],
            offset=offset,
            total=len(references),
            cursor_domain="links",
            cursor_binding=cursor_binding,
            extra={
                "file_id": call.file_id,
                "ignored": self._reference_graph.ignored.model_dump(mode="json"),
            },
        )
        truncated = bounded["next_cursor"] is not None
        return EvidenceExecution(
            status="success",
            result=bounded,
            error_code=None,
            truncated=truncated,
            cache_hit=False,
        )

    def _require_file(self, file_id: str) -> FolderFile:
        source_file = self._files_by_id.get(file_id)
        if source_file is None:
            raise PlannerEvidenceError(
                "unknown_file_id",
                "Evidence call references an unknown file ID.",
            )
        return source_file

    def _require_source_unchanged(self) -> None:
        try:
            current = scan_folder(self._scan.source_root)
        except (FolderScanError, OSError) as exc:
            raise PlannerEvidenceError(
                "source_changed",
                "Source cannot be proven equal while collecting evidence.",
            ) from exc
        if (
            current.inventory.source_commitment
            != self._scan.inventory.source_commitment
            or current.local_file_identities != self._scan.local_file_identities
            or current.local_directory_identities
            != self._scan.local_directory_identities
        ):
            raise PlannerEvidenceError(
                "source_changed",
                "Source changed while collecting planner evidence.",
            )


def _planner_file_metadata(source_file: FolderFile) -> dict[str, JsonValue]:
    """Return the disclosed planner view without raw content digests."""

    return PlannerInventoryFile(
        evidence_eligible=source_file.evidence_eligible,
        file_id=source_file.file_id,
        protected=source_file.protected,
        relative_path=source_file.relative_path,
        size=source_file.size,
    ).model_dump(mode="json")


def _call_arguments(
    call: ListInventoryPageCall | ReadTextExcerptCall | InspectMarkdownLinksCall,
) -> JsonValue:
    raw = call.model_dump(mode="json")
    raw.pop("call_id")
    raw.pop("tool_name")
    return raw


def _read_verified_utf8_window(
    path: Path,
    expected: FolderFile,
    *,
    start: int,
    maximum: int,
) -> tuple[str, int, int]:
    """Stream-verify a UTF-8 file while retaining only one bounded byte window."""

    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if start > expected.size:
        raise PlannerEvidenceError(
            "excerpt_offset_out_of_range",
            "Text excerpt offset is beyond the file.",
        )
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise PlannerEvidenceError(
            "evidence_file_unreadable",
            "Evidence file cannot be opened safely.",
        ) from exc
    requested_end = min(expected.size, start + maximum)
    window = bytearray()
    digest = hashlib.sha256()
    decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    position = 0
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink > 1:
            raise PlannerEvidenceError(
                "source_changed",
                "Evidence member is no longer a supported regular file.",
            )
        while chunk := os.read(descriptor, HASH_CHUNK_SIZE):
            digest.update(chunk)
            try:
                decoder.decode(chunk, final=False)
            except UnicodeDecodeError as exc:
                raise PlannerEvidenceError(
                    "invalid_utf8_evidence",
                    "Eligible text evidence is not valid UTF-8.",
                ) from exc
            chunk_end = position + len(chunk)
            overlap_start = max(start, position)
            overlap_end = min(requested_end, chunk_end)
            if overlap_start < overlap_end:
                window.extend(chunk[overlap_start - position : overlap_end - position])
            position = chunk_end
        try:
            decoder.decode(b"", final=True)
        except UnicodeDecodeError as exc:
            raise PlannerEvidenceError(
                "invalid_utf8_evidence",
                "Eligible text evidence is not valid UTF-8.",
            ) from exc
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    identity_before = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    identity_after = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if (
        identity_before != identity_after
        or position != expected.size
        or digest.hexdigest() != expected.sha256
    ):
        raise PlannerEvidenceError(
            "source_changed",
            "Evidence file changed while being read.",
        )
    raw_window = bytes(window)
    end = requested_end
    for backtrack in range(0, min(4, len(raw_window) + 1)):
        candidate = raw_window[: len(raw_window) - backtrack]
        try:
            text = candidate.decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            continue
        return text, end - backtrack, expected.size
    raise PlannerEvidenceError(
        "excerpt_boundary_invalid",
        "Excerpt start must align with a UTF-8 character boundary.",
    )


def _bounded_page(
    *,
    schema_version: str,
    key: str,
    values: list[JsonValue],
    offset: int,
    total: int,
    cursor_domain: Literal["inv", "links"],
    cursor_binding: str,
    extra: dict[str, JsonValue],
) -> dict[str, JsonValue]:
    selected = list(values)
    while True:
        next_offset = offset + len(selected)
        complete = next_offset >= total
        candidate: dict[str, JsonValue] = {
            **extra,
            "complete": complete,
            key: selected,
            "next_cursor": (
                None
                if complete
                else _encode_cursor(cursor_domain, cursor_binding, next_offset)
            ),
            "offset": offset,
            "schema_version": schema_version,
            "total": total,
            "truncated": not complete,
        }
        if (
            _outcome_size(candidate, truncated=not complete)
            <= MAX_EVIDENCE_RESULT_BYTES
        ):
            return candidate
        if not selected:
            raise PlannerEvidenceError(
                "evidence_result_limit_exceeded",
                "Evidence-page metadata exceeds its per-call result limit.",
            )
        selected.pop()


def _bound_text_result(result: JsonValue, key: str) -> tuple[JsonValue, bool]:
    if _outcome_size(result, truncated=bool(result["truncated"])) <= (
        MAX_EVIDENCE_RESULT_BYTES
    ):
        return result, False
    if not isinstance(result, dict) or not isinstance(result.get(key), str):
        raise PlannerEvidenceError(
            "evidence_result_limit_exceeded",
            "Text evidence result cannot be bounded deterministically.",
        )
    text = result[key]
    low = 0
    high = len(text)
    best: dict[str, JsonValue] | None = None
    while low <= high:
        midpoint = (low + high) // 2
        shortened = text[:midpoint]
        returned_bytes = len(shortened.encode("utf-8"))
        start_byte = int(result["start_byte"])
        original_bytes = int(result["original_byte_count"])
        candidate = {
            **result,
            "end_byte": start_byte + returned_bytes,
            key: shortened,
            "returned_byte_count": returned_bytes,
            "omitted_byte_count": original_bytes - start_byte - returned_bytes,
            "truncated": True,
        }
        if _outcome_size(candidate, truncated=True) <= MAX_EVIDENCE_RESULT_BYTES:
            best = candidate
            low = midpoint + 1
        else:
            high = midpoint - 1
    if best is None:
        raise PlannerEvidenceError(
            "evidence_result_limit_exceeded",
            "Text evidence metadata exceeds its per-call result limit.",
        )
    return best, True


def _outcome_size(result: JsonValue, *, truncated: bool) -> int:
    return len(
        canonical_json_bytes(
            {
                "error_code": None,
                "result": result,
                "status": "success",
                "truncated": truncated,
            }
        )
    )


def _encode_cursor(
    domain: Literal["inv", "links"],
    binding: str,
    offset: int,
) -> str:
    return f"{domain}:{binding[:16]}:{offset}"


def _decode_cursor(
    cursor: str | None,
    *,
    domain: Literal["inv", "links"],
    binding: str,
    upper_bound: int,
) -> int:
    if cursor is None:
        return 0
    expected_prefix = f"{domain}:{binding[:16]}:"
    if not cursor.startswith(expected_prefix):
        raise PlannerEvidenceError(
            "invalid_evidence_cursor",
            "Evidence cursor is not bound to this immutable source.",
        )
    try:
        offset = int(cursor.removeprefix(expected_prefix))
    except ValueError as exc:
        raise PlannerEvidenceError(
            "invalid_evidence_cursor",
            "Evidence cursor is malformed.",
        ) from exc
    if offset < 0 or offset > upper_bound:
        raise PlannerEvidenceError(
            "invalid_evidence_cursor",
            "Evidence cursor is outside the available result set.",
        )
    return offset
