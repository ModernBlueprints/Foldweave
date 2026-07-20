"""Build and parse payload-free Connected Change descriptors."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any

from pydantic import ValidationError

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    MAX_CHANGE_FILE_BYTES,
    MAX_CONNECTED_CHANGE_GENERATION,
    ConnectedChangeCore,
    ConnectedChangeCoreV2,
    ConnectedChangeError,
    ConnectedChangeFile,
    ConnectedChangeFileAny,
    ConnectedChangeFileV2,
    ConnectedChangeLineageV1,
    ConnectedChangeLinkSlot,
    ConnectedChangeMember,
    ConnectedChangeMemberBindingV1,
    connected_change_core_fingerprint,
    connected_change_core_v2_fingerprint,
    connected_change_file_fingerprint,
    connected_change_file_v2_fingerprint,
    connected_change_member_id,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptEnvelopeV2,
    FolderReceiptEnvelopeV3,
)
from name_atlas.folder_refactor.contracts import (
    FolderAcceptedPlan,
    FolderFile,
    FolderInventory,
)
from name_atlas.folder_refactor.markdown_contracts import (
    FolderReferenceGraph,
    MarkdownReference,
)
from name_atlas.folder_refactor.markdown_links import MARKDOWN_SUFFIXES
from name_atlas.folder_refactor.naming import (
    TargetPathError,
    protected_suffix,
    validate_complete_target_tree,
    validate_result_folder_name,
    validate_target_path,
)
from name_atlas.folder_refactor.portable_artifacts import (
    FolderPortableArtifactError,
    strict_json_object,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)


@dataclass(frozen=True, slots=True)
class ReceiverLinkSlot:
    """One receiver-local supported relationship used only by the matcher."""

    slot_index: int
    is_image: bool
    syntax_class: str
    fragment: str | None
    target_file_id: str


@dataclass(frozen=True, slots=True)
class ReceiverDescriptor:
    """One receiver member described without using its path as match evidence."""

    file_id: str
    relative_path: str
    descriptor_kind: str
    protected_suffix: str
    protected: bool
    byte_size: int | None
    payload_sha256: str | None
    markdown_non_destination_sha256: str | None
    link_slots: tuple[ReceiverLinkSlot, ...]


def build_connected_change_core(
    inventory: FolderInventory,
    graph: FolderReferenceGraph,
    accepted_plan: FolderAcceptedPlan | FolderAcceptedPlanV2,
    *,
    request: str,
    markdown_payloads: Mapping[str, bytes],
    expected_organized_tree_commitment: str,
    origin_proof_identifiers: Sequence[str] = (),
) -> ConnectedChangeCore:
    """Build one immutable payload-free Core from independently bound inputs."""

    _require_common_commitment(inventory, graph, accepted_plan)
    if accepted_plan.request_fingerprint != request_fingerprint(request):
        _reject("change_file_schema_invalid", "Accepted plan targets another request.")
    inventory_by_id = {item.file_id: item for item in inventory.files}
    mappings_by_id = {item.file_id: item for item in accepted_plan.file_mappings}
    if set(mappings_by_id) != set(inventory_by_id):
        _reject(
            "change_file_schema_invalid",
            "Accepted plan does not account for every source file exactly once.",
        )
    expected_empty_directories = tuple(
        item.relative_path for item in inventory.empty_directories
    )
    if accepted_plan.empty_directories != expected_empty_directories:
        _reject(
            "change_file_schema_invalid",
            "Accepted plan empty directories differ from the source inventory.",
        )
    references_by_source = _validated_references_by_source(inventory, graph)

    provisional: dict[str, ConnectedChangeMember] = {}
    for source_file in inventory.files:
        mapping = mappings_by_id[source_file.file_id]
        if mapping.original_path != source_file.relative_path:
            _reject(
                "change_file_schema_invalid",
                f"Accepted mapping path differs for {source_file.relative_path!r}.",
            )
        if mapping.protected != source_file.protected:
            _reject(
                "change_file_schema_invalid",
                "Accepted protection authority differs for "
                f"{source_file.relative_path!r}.",
            )
        suffix = protected_suffix(PurePosixPath(source_file.relative_path).name)
        references = references_by_source.get(source_file.file_id, ())
        if source_file.protected:
            if mapping.target_path != source_file.relative_path:
                _reject(
                    "change_file_schema_invalid",
                    f"Protected member moved: {source_file.relative_path!r}.",
                )
            _require_protected_reference_stability(
                source_file=source_file,
                references=references,
                mappings_by_id=mappings_by_id,
            )
            descriptor_kind = "ordinary"
            non_destination = None
            byte_size = source_file.size
            payload_sha256 = source_file.sha256
        elif _is_markdown(source_file):
            descriptor_kind = "markdown"
            non_destination = _markdown_non_destination_sha256(
                source_file,
                references,
                markdown_payloads,
            )
            byte_size = None
            payload_sha256 = None
        else:
            if references:
                _reject(
                    "change_file_schema_invalid",
                    "Non-Markdown member owns link records: "
                    f"{source_file.relative_path!r}.",
                )
            descriptor_kind = "ordinary"
            non_destination = None
            byte_size = source_file.size
            payload_sha256 = source_file.sha256

        skeleton = ConnectedChangeMember.model_construct(
            logical_member_id="0" * 64,
            descriptor_kind=descriptor_kind,
            origin_relative_path=source_file.relative_path,
            target_relative_path=mapping.target_path,
            protected_suffix=suffix,
            protected=source_file.protected,
            byte_size=byte_size,
            payload_sha256=payload_sha256,
            markdown_non_destination_sha256=non_destination,
            link_slots=(),
        )
        member_id = connected_change_member_id(skeleton)
        provisional[source_file.file_id] = skeleton.model_copy(
            update={"logical_member_id": member_id}
        )

    members: list[ConnectedChangeMember] = []
    for source_file in inventory.files:
        skeleton = provisional[source_file.file_id]
        link_slots = tuple(
            ConnectedChangeLinkSlot(
                slot_index=index,
                is_image=reference.is_image,
                syntax_class=reference.destination_style,
                fragment=reference.fragment,
                target_logical_member_id=provisional[
                    reference.target_file_id
                ].logical_member_id,
            )
            for index, reference in enumerate(
                references_by_source.get(source_file.file_id, ())
            )
            if skeleton.descriptor_kind == "markdown"
        )
        members.append(
            ConnectedChangeMember(
                **skeleton.model_dump(mode="python", exclude={"link_slots"}),
                link_slots=link_slots,
            )
        )

    return ConnectedChangeCore(
        request=request,
        request_fingerprint=request_fingerprint(request),
        requested_result_folder_name=accepted_plan.result_folder_name,
        origin_source_commitment=inventory.source_commitment,
        members=tuple(sorted(members, key=lambda item: item.logical_member_id)),
        empty_directory_requirements=tuple(expected_empty_directories),
        expected_file_count=len(members),
        expected_empty_directory_count=len(inventory.empty_directories),
        expected_supported_link_count=sum(len(member.link_slots) for member in members),
        expected_organized_tree_commitment=expected_organized_tree_commitment,
        origin_proof_identifiers=tuple(sorted(origin_proof_identifiers)),
    )


def build_connected_change_core_v2(
    complete_core: ConnectedChangeCore,
    *,
    lineage: ConnectedChangeLineageV1,
) -> ConnectedChangeCoreV2:
    """Promote one complete generated Core into the versioned lineage family."""

    if not isinstance(complete_core, ConnectedChangeCore):
        _reject(
            "change_file_schema_invalid",
            "A v2 Core requires one complete validated v1-compatible Core.",
        )
    return ConnectedChangeCoreV2(
        **complete_core.model_dump(mode="python", exclude={"schema_version"}),
        lineage=lineage,
    )


def build_connected_change_lineage(
    *,
    parent_change_file: ConnectedChangeFileAny,
    parent_candidate_fingerprint: str,
    revision_instruction_fingerprint: str,
    member_bindings: Sequence[ConnectedChangeMemberBindingV1],
    parent_candidate: FolderAcceptedPlanV2 | None = None,
) -> ConnectedChangeLineageV1:
    """Build one complete immediate-parent binding without embedding the parent."""

    if not isinstance(parent_change_file, ConnectedChangeFile | ConnectedChangeFileV2):
        _reject(
            "change_file_lineage_invalid",
            "Lineage parent must be a verified Connected Change File.",
        )
    parent_generation = (
        parent_change_file.core.lineage.generation
        if isinstance(parent_change_file, ConnectedChangeFileV2)
        else 0
    )
    generation = parent_generation + 1
    if generation > MAX_CONNECTED_CHANGE_GENERATION:
        _reject(
            "change_file_lineage_generation_exceeded",
            "A Foldweave Change File cannot exceed lineage generation "
            f"{MAX_CONNECTED_CHANGE_GENERATION}.",
        )
    parent_member_ids = tuple(
        member.logical_member_id for member in parent_change_file.core.members
    )
    ordered_bindings = tuple(
        sorted(member_bindings, key=lambda item: item.parent_logical_member_id)
    )
    bound_parent_ids = tuple(
        binding.parent_logical_member_id for binding in ordered_bindings
    )
    if len(bound_parent_ids) != len(parent_member_ids) or set(bound_parent_ids) != set(
        parent_member_ids
    ):
        _reject(
            "change_file_lineage_invalid",
            "Immediate-parent lineage must bind every parent logical member once.",
        )
    if parent_candidate is None:
        # Historical callers only had the producer-side plan committed by the
        # parent Change File. Keep that strict behavior for compatibility.
        finalized_parent_candidate = (
            parent_change_file.originating_receipt.receipt.compiled_candidate_fingerprint
            if isinstance(parent_change_file, ConnectedChangeFileV2)
            else (
                parent_change_file.originating_receipt.receipt.accepted_plan_fingerprint
            )
        )
        if finalized_parent_candidate != parent_candidate_fingerprint:
            _reject(
                "change_file_lineage_invalid",
                "Parent candidate fingerprint differs from the finalized parent "
                "receipt.",
            )
    elif not (
        canonical_sha256(parent_candidate) == parent_candidate_fingerprint
        and parent_candidate.request_fingerprint
        == parent_change_file.core.request_fingerprint
        and parent_candidate.result_folder_name
        == parent_change_file.core.requested_result_folder_name
    ):
        _reject(
            "change_file_lineage_invalid",
            "Receiver-parent candidate does not bind the imported proposal.",
        )
    return ConnectedChangeLineageV1(
        generation=generation,
        parent_generation=parent_generation,
        parent_change_file_schema_version=parent_change_file.schema_version,
        parent_core_schema_version=parent_change_file.core.schema_version,
        parent_change_file_fingerprint=(parent_change_file.change_file_fingerprint),
        parent_core_fingerprint=parent_change_file.core_fingerprint,
        parent_originating_receipt_fingerprint=(
            parent_change_file.originating_receipt.receipt_fingerprint
        ),
        parent_organized_tree_commitment=(
            parent_change_file.originating_receipt.receipt.organized_tree.commitment
        ),
        parent_candidate_fingerprint=parent_candidate_fingerprint,
        revision_instruction_fingerprint=revision_instruction_fingerprint,
        member_bindings=ordered_bindings,
    )


def create_connected_change_file(
    core: ConnectedChangeCore,
    *,
    originating_receipt: FolderReceiptEnvelopeV2 | Mapping[str, Any],
) -> ConnectedChangeFile:
    """Create an acyclic transferable envelope around a finalized receipt."""

    receipt = _validated_originating_receipt(
        originating_receipt,
        core=core,
    )
    provisional = ConnectedChangeFile.model_construct(
        schema_version="connected-change-file.v1",
        core=core,
        core_fingerprint=connected_change_core_fingerprint(core),
        originating_receipt=receipt,
        change_file_fingerprint="0" * 64,
    )
    change_file = ConnectedChangeFile(
        **provisional.model_dump(mode="python", exclude={"change_file_fingerprint"}),
        change_file_fingerprint=connected_change_file_fingerprint(provisional),
    )
    if len(canonical_json_bytes(change_file)) > MAX_CHANGE_FILE_BYTES:
        _reject(
            "change_file_too_large",
            f"Change File exceeds {MAX_CHANGE_FILE_BYTES} bytes.",
        )
    return change_file


def create_connected_change_file_v2(
    core: ConnectedChangeCoreV2,
    *,
    originating_receipt: FolderReceiptEnvelopeV3 | Mapping[str, Any],
) -> ConnectedChangeFileV2:
    """Finalize one self-contained Foldweave envelope around a v3 receipt."""

    receipt = _validated_originating_receipt_v3(
        originating_receipt,
        core=core,
    )
    provisional = ConnectedChangeFileV2.model_construct(
        schema_version="connected-change-file.v2",
        core=core,
        core_fingerprint=connected_change_core_v2_fingerprint(core),
        originating_receipt=receipt,
        change_file_fingerprint="0" * 64,
    )
    change_file = ConnectedChangeFileV2(
        **provisional.model_dump(mode="python", exclude={"change_file_fingerprint"}),
        change_file_fingerprint=connected_change_file_v2_fingerprint(provisional),
    )
    if len(canonical_json_bytes(change_file)) > MAX_CHANGE_FILE_BYTES:
        _reject(
            "change_file_too_large",
            f"Change File exceeds {MAX_CHANGE_FILE_BYTES} bytes.",
        )
    return change_file


def parse_connected_change_file(data: bytes) -> ConnectedChangeFile:
    """Strictly parse and verify a bounded Connected Change File envelope."""

    if not isinstance(data, bytes):
        _reject("change_file_schema_invalid", "Change File input must be bytes.")
    if len(data) > MAX_CHANGE_FILE_BYTES:
        _reject(
            "change_file_too_large",
            f"Change File exceeds {MAX_CHANGE_FILE_BYTES} bytes.",
        )
    try:
        raw = strict_json_object(data)
    except FolderPortableArtifactError as exc:
        _reject("change_file_schema_invalid", str(exc))
    if set(raw) != {
        "schema_version",
        "core",
        "core_fingerprint",
        "originating_receipt",
        "change_file_fingerprint",
    }:
        _reject("change_file_schema_invalid", "Change File fields are not exact.")
    core_raw = raw.get("core")
    if not isinstance(core_raw, dict):
        _reject("change_file_schema_invalid", "Change File Core must be an object.")
    expected_core = canonical_sha256(core_raw)
    envelope_payload = {
        key: value for key, value in raw.items() if key != "change_file_fingerprint"
    }
    expected_envelope = canonical_sha256(envelope_payload)
    if (
        raw.get("core_fingerprint") != expected_core
        or raw.get("change_file_fingerprint") != expected_envelope
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Change File canonical fingerprint does not match its contents.",
        )
    try:
        change_file = ConnectedChangeFile.model_validate_json(data, strict=True)
    except ValidationError as exc:
        if _raw_receiver_targets_are_invalid(core_raw):
            _reject("receiver_target_invalid", str(exc))
        _reject("change_file_schema_invalid", str(exc))
    _validated_originating_receipt(
        change_file.originating_receipt,
        core=change_file.core,
    )
    if canonical_json_bytes(change_file) != data:
        _reject(
            "change_file_schema_invalid",
            "Change File must use exact canonical JSON serialization.",
        )
    return change_file


def parse_connected_change_file_v2(data: bytes) -> ConnectedChangeFileV2:
    """Strictly parse and verify one bounded Foldweave Change File envelope."""

    raw = _strict_bounded_change_file_object(data)
    if raw.get("schema_version") != "connected-change-file.v2":
        _reject(
            "change_file_schema_invalid",
            "Change File does not declare connected-change-file.v2.",
        )
    _require_exact_envelope_fields(raw)
    core_raw = raw.get("core")
    if not isinstance(core_raw, dict):
        _reject("change_file_schema_invalid", "Change File Core must be an object.")
    _require_raw_fingerprints(raw, core_raw)
    try:
        change_file = ConnectedChangeFileV2.model_validate_json(data, strict=True)
    except ValidationError as exc:
        if _raw_receiver_targets_are_invalid(core_raw):
            _reject("receiver_target_invalid", str(exc))
        _reject("change_file_schema_invalid", str(exc))
    _validated_originating_receipt_v3(
        change_file.originating_receipt,
        core=change_file.core,
    )
    if canonical_json_bytes(change_file) != data:
        _reject(
            "change_file_schema_invalid",
            "Change File must use exact canonical JSON serialization.",
        )
    return change_file


def parse_connected_change_file_any(data: bytes) -> ConnectedChangeFileAny:
    """Strictly dispatch canonical Change File bytes across v1 and v2."""

    raw = _strict_bounded_change_file_object(data)
    schema_version = raw.get("schema_version")
    if schema_version == "connected-change-file.v1":
        return parse_connected_change_file(data)
    if schema_version == "connected-change-file.v2":
        return parse_connected_change_file_v2(data)
    _reject(
        "change_file_schema_invalid",
        "Change File schema version is unsupported.",
    )


def _strict_bounded_change_file_object(data: bytes) -> dict[str, Any]:
    if not isinstance(data, bytes):
        _reject("change_file_schema_invalid", "Change File input must be bytes.")
    if len(data) > MAX_CHANGE_FILE_BYTES:
        _reject(
            "change_file_too_large",
            f"Change File exceeds {MAX_CHANGE_FILE_BYTES} bytes.",
        )
    try:
        return strict_json_object(data)
    except FolderPortableArtifactError as exc:
        _reject("change_file_schema_invalid", str(exc))


def _require_exact_envelope_fields(raw: Mapping[str, Any]) -> None:
    if set(raw) != {
        "schema_version",
        "core",
        "core_fingerprint",
        "originating_receipt",
        "change_file_fingerprint",
    }:
        _reject("change_file_schema_invalid", "Change File fields are not exact.")


def _require_raw_fingerprints(
    raw: Mapping[str, Any],
    core_raw: Mapping[str, Any],
) -> None:
    expected_core = canonical_sha256(core_raw)
    envelope_payload = {
        key: value for key, value in raw.items() if key != "change_file_fingerprint"
    }
    expected_envelope = canonical_sha256(envelope_payload)
    if (
        raw.get("core_fingerprint") != expected_core
        or raw.get("change_file_fingerprint") != expected_envelope
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Change File canonical fingerprint does not match its contents.",
        )


def _raw_receiver_targets_are_invalid(core_raw: Mapping[str, Any]) -> bool:
    """Classify only well-shaped receiver targets through the frozen path profile."""

    result_folder_name = core_raw.get("requested_result_folder_name")
    members = core_raw.get("members")
    empty_directories = core_raw.get("empty_directory_requirements")
    if (
        not isinstance(result_folder_name, str)
        or not isinstance(members, list)
        or not isinstance(empty_directories, list)
    ):
        return False

    file_targets: list[str] = []
    try:
        validate_result_folder_name(result_folder_name)
        for member in members:
            if not isinstance(member, dict):
                return False
            original_path = member.get("origin_relative_path")
            target_path = member.get("target_relative_path")
            protected = member.get("protected")
            if (
                not isinstance(original_path, str)
                or not isinstance(target_path, str)
                or not isinstance(protected, bool)
            ):
                return False
            validate_target_path(
                target_path,
                original_path=original_path,
                protected=protected,
            )
            file_targets.append(target_path)
        if not all(isinstance(path, str) for path in empty_directories):
            return False
        for path in empty_directories:
            validate_target_path(path, original_path=path, protected=True)
        validate_complete_target_tree(file_targets, empty_directories)
    except TargetPathError:
        return True
    return False


def build_receiver_descriptors(
    inventory: FolderInventory,
    graph: FolderReferenceGraph,
    *,
    markdown_payloads: Mapping[str, bytes],
) -> tuple[ReceiverDescriptor, ...]:
    """Build receiver-local intrinsic descriptors without matching by path."""

    if graph.source_commitment != inventory.source_commitment:
        _reject(
            "receiver_relationship_changed",
            "Receiver graph targets another source inventory.",
        )
    references_by_source = _validated_references_by_source(inventory, graph)
    descriptors: list[ReceiverDescriptor] = []
    for source_file in inventory.files:
        suffix = protected_suffix(PurePosixPath(source_file.relative_path).name)
        references = references_by_source.get(source_file.file_id, ())
        if source_file.protected or not _is_markdown(source_file):
            descriptor_kind = "ordinary"
            byte_size = source_file.size
            payload_sha256 = source_file.sha256
            non_destination = None
            slots: tuple[ReceiverLinkSlot, ...] = ()
        else:
            descriptor_kind = "markdown"
            byte_size = None
            payload_sha256 = None
            non_destination = _markdown_non_destination_sha256(
                source_file,
                references,
                markdown_payloads,
            )
            slots = tuple(
                ReceiverLinkSlot(
                    slot_index=index,
                    is_image=reference.is_image,
                    syntax_class=reference.destination_style,
                    fragment=reference.fragment,
                    target_file_id=reference.target_file_id,
                )
                for index, reference in enumerate(references)
            )
        descriptors.append(
            ReceiverDescriptor(
                file_id=source_file.file_id,
                relative_path=source_file.relative_path,
                descriptor_kind=descriptor_kind,
                protected_suffix=suffix,
                protected=source_file.protected,
                byte_size=byte_size,
                payload_sha256=payload_sha256,
                markdown_non_destination_sha256=non_destination,
                link_slots=slots,
            )
        )
    return tuple(descriptors)


def _require_common_commitment(
    inventory: FolderInventory,
    graph: FolderReferenceGraph,
    accepted_plan: FolderAcceptedPlan | FolderAcceptedPlanV2,
) -> None:
    commitments = {
        inventory.source_commitment,
        graph.source_commitment,
        accepted_plan.source_commitment,
    }
    if len(commitments) != 1:
        _reject(
            "change_file_schema_invalid",
            "Inventory, graph, and accepted plan target different sources.",
        )


def _validated_references_by_source(
    inventory: FolderInventory,
    graph: FolderReferenceGraph,
) -> dict[str, tuple[MarkdownReference, ...]]:
    by_id = {item.file_id: item for item in inventory.files}
    grouped: dict[str, list[MarkdownReference]] = defaultdict(list)
    for reference in graph.references:
        source = by_id.get(reference.source_file_id)
        target = by_id.get(reference.target_file_id)
        if source is None or target is None:
            _reject(
                "receiver_relationship_changed",
                "Reference graph names a member outside the inventory.",
            )
        if (
            source.relative_path != reference.source_path
            or target.relative_path != reference.target_path
        ):
            _reject(
                "receiver_relationship_changed",
                "Reference graph paths disagree with the bound inventory.",
            )
        grouped[source.file_id].append(reference)
    return {
        file_id: tuple(sorted(items, key=lambda item: item.destination_start_byte))
        for file_id, items in grouped.items()
    }


def _markdown_non_destination_sha256(
    source_file: FolderFile,
    references: Sequence[MarkdownReference],
    markdown_payloads: Mapping[str, bytes],
) -> str:
    payload = markdown_payloads.get(source_file.relative_path)
    if not isinstance(payload, bytes):
        _reject(
            "receiver_markdown_content_changed",
            f"Exact Markdown bytes are missing for {source_file.relative_path!r}.",
        )
    if (
        len(payload) != source_file.size
        or hashlib.sha256(payload).hexdigest() != source_file.sha256
    ):
        _reject(
            "receiver_markdown_content_changed",
            f"Markdown bytes do not match {source_file.relative_path!r}.",
        )
    digest = hashlib.sha256()
    cursor = 0
    for reference in references:
        start = reference.destination_start_byte
        end = reference.destination_end_byte
        if start < cursor or end > len(payload) or start >= end:
            _reject(
                "receiver_relationship_changed",
                f"Markdown span is invalid for {source_file.relative_path!r}.",
            )
        if payload[start:end] != bytes.fromhex(
            reference.original_destination_bytes_hex
        ):
            _reject(
                "receiver_relationship_changed",
                f"Markdown destination bytes changed in {source_file.relative_path!r}.",
            )
        digest.update(payload[cursor:start])
        cursor = end
    digest.update(payload[cursor:])
    return digest.hexdigest()


def _require_protected_reference_stability(
    *,
    source_file: FolderFile,
    references: Sequence[MarkdownReference],
    mappings_by_id: Mapping[str, Any],
) -> None:
    for reference in references:
        target_mapping = mappings_by_id.get(reference.target_file_id)
        if (
            target_mapping is None
            or target_mapping.target_path != reference.target_path
        ):
            _reject(
                "change_file_schema_invalid",
                "A protected Markdown member would need a content rewrite: "
                f"{source_file.relative_path!r}.",
            )


def _validated_originating_receipt(
    receipt: FolderReceiptEnvelopeV2 | Mapping[str, Any],
    *,
    core: ConnectedChangeCore,
) -> FolderReceiptEnvelopeV2:
    try:
        parsed = (
            receipt
            if isinstance(receipt, FolderReceiptEnvelopeV2)
            else FolderReceiptEnvelopeV2.model_validate_json(
                canonical_json_bytes(dict(receipt)),
                strict=True,
            )
        )
    except (TypeError, ValueError, ValidationError) as exc:
        _reject(
            "change_file_schema_invalid",
            f"Originating receipt is not a strict v2 receipt: {exc}",
        )
    if parsed.receipt.execution_role != "origin":
        _reject(
            "change_file_schema_invalid",
            "Originating receipt must declare the origin execution role.",
        )
    if (
        parsed.receipt.connected_change_core_fingerprint
        != connected_change_core_fingerprint(core)
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Originating receipt does not commit this Change File Core.",
        )
    receipt_core = parsed.receipt
    if not (
        receipt_core.source_commitment == core.origin_source_commitment
        and receipt_core.request_fingerprint == core.request_fingerprint
        and receipt_core.source_file_count == core.expected_file_count
        and receipt_core.map_row_count == core.expected_file_count
        and receipt_core.supported_link_count == core.expected_supported_link_count
        and receipt_core.organized_tree.commitment
        == core.expected_organized_tree_commitment
        and receipt_core.evidence_fingerprint in core.origin_proof_identifiers
        and receipt_core.accepted_plan_fingerprint in core.origin_proof_identifiers
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Originating receipt authorities do not match the Change File Core.",
        )
    return parsed


def _validated_originating_receipt_v3(
    receipt: FolderReceiptEnvelopeV3 | Mapping[str, Any],
    *,
    core: ConnectedChangeCoreV2,
) -> FolderReceiptEnvelopeV3:
    try:
        parsed = (
            receipt
            if isinstance(receipt, FolderReceiptEnvelopeV3)
            else FolderReceiptEnvelopeV3.model_validate_json(
                canonical_json_bytes(dict(receipt)),
                strict=True,
            )
        )
    except (TypeError, ValueError, ValidationError) as exc:
        _reject(
            "change_file_schema_invalid",
            f"Originating receipt is not a strict v3 receipt: {exc}",
        )
    receipt_core = parsed.receipt
    if receipt_core.execution_role not in {"origin", "derivative"}:
        _reject(
            "change_file_schema_invalid",
            "Originating receipt must declare origin or derivative execution.",
        )
    if not (
        receipt_core.connected_change_core_schema_version == "connected-change-core.v2"
        and receipt_core.connected_change_core_fingerprint
        == connected_change_core_v2_fingerprint(core)
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Originating receipt does not commit this v2 Change File Core.",
        )
    if receipt_core.execution_role == "derivative" and not (
        receipt_core.imported_change_file_fingerprint
        == core.lineage.parent_change_file_fingerprint
        and receipt_core.originating_receipt_fingerprint
        == core.lineage.parent_originating_receipt_fingerprint
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Derivative receipt does not bind the immediate parent lineage.",
        )
    if not (
        receipt_core.source_commitment == core.origin_source_commitment
        and receipt_core.request_fingerprint == core.request_fingerprint
        and receipt_core.source_file_count == core.expected_file_count
        and receipt_core.map_row_count == core.expected_file_count
        and receipt_core.supported_link_count == core.expected_supported_link_count
        and receipt_core.organized_tree.commitment
        == core.expected_organized_tree_commitment
        and receipt_core.lineage_generation == core.lineage.generation
        and receipt_core.evidence_fingerprint in core.origin_proof_identifiers
        and receipt_core.accepted_plan_fingerprint in core.origin_proof_identifiers
    ):
        _reject(
            "change_file_fingerprint_mismatch",
            "Originating receipt authorities do not match the v2 Change File Core.",
        )
    return parsed


def _is_markdown(source_file: FolderFile) -> bool:
    return (
        PurePosixPath(source_file.relative_path).suffix.casefold() in MARKDOWN_SUFFIXES
    )


def _reject(code: str, message: str) -> None:
    raise ConnectedChangeError(code, message)
