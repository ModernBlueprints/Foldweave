"""Deterministic path-independent Connected Change receiver matching."""

from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from name_atlas.folder_refactor.connected_change.contracts import (
    ConnectedChangeCore,
    ConnectedChangeCoreV2,
    ConnectedChangeError,
    ConnectedChangeFile,
    ConnectedChangeFileV2,
    ConnectedChangeMatchMapping,
    ConnectedChangeMatchReport,
    ConnectedChangeMember,
    connected_change_core_fingerprint,
    connected_change_core_v2_fingerprint,
    connected_change_match_report_fingerprint,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    ReceiverDescriptor,
    build_receiver_descriptors,
)
from name_atlas.folder_refactor.contracts import FolderInventory
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.serialization import canonical_sha256


def match_connected_change(
    change_file_or_core: (
        ConnectedChangeFile
        | ConnectedChangeFileV2
        | ConnectedChangeCore
        | ConnectedChangeCoreV2
    ),
    receiver_inventory: FolderInventory,
    receiver_graph: FolderReferenceGraph,
    *,
    markdown_payloads: Mapping[str, bytes],
) -> ConnectedChangeMatchReport:
    """Match every logical role to one receiver file or return one blocker."""

    core = (
        change_file_or_core.core
        if isinstance(change_file_or_core, ConnectedChangeFile | ConnectedChangeFileV2)
        else change_file_or_core
    )
    core_fingerprint = _core_fingerprint(core)
    try:
        receiver_descriptors = build_receiver_descriptors(
            receiver_inventory,
            receiver_graph,
            markdown_payloads=markdown_payloads,
        )
    except ConnectedChangeError as exc:
        return _blocked_report(
            core_fingerprint=core_fingerprint,
            receiver_source_commitment=receiver_inventory.source_commitment,
            code=exc.code,
            detail=exc.message,
        )
    return _match_descriptors(
        core,
        receiver_descriptors,
        receiver_source_commitment=receiver_inventory.source_commitment,
        receiver_empty_directories=tuple(
            item.relative_path for item in receiver_inventory.empty_directories
        ),
    )


def _match_descriptors(
    core: ConnectedChangeCore | ConnectedChangeCoreV2,
    receiver_descriptors: Sequence[ReceiverDescriptor],
    *,
    receiver_source_commitment: str,
    receiver_empty_directories: Sequence[str],
) -> ConnectedChangeMatchReport:
    """Pure sequence-order-invariant matcher used by tests and the public adapter."""

    core_fingerprint = _core_fingerprint(core)
    origin = tuple(core.members)
    receiver = tuple(receiver_descriptors)
    blocker = _preflight_blocker(
        core,
        receiver,
        receiver_empty_directories=receiver_empty_directories,
    )
    if blocker is not None:
        code, detail = blocker
        return _blocked_report(
            core_fingerprint=core_fingerprint,
            receiver_source_commitment=receiver_source_commitment,
            code=code,
            detail=detail,
        )

    origin_by_id = {member.logical_member_id: member for member in origin}
    receiver_by_id = {member.file_id: member for member in receiver}
    if len(origin_by_id) != len(origin) or len(receiver_by_id) != len(receiver):
        return _blocked_report(
            core_fingerprint=core_fingerprint,
            receiver_source_commitment=receiver_source_commitment,
            code="receiver_relationship_changed",
            detail="Member identities are not unique.",
        )

    origin_colors = {
        member.logical_member_id: canonical_sha256(_origin_base(member))
        for member in origin
    }
    receiver_colors = {
        member.file_id: canonical_sha256(_receiver_base(member)) for member in receiver
    }
    if not _equal_color_cardinalities(origin_colors, receiver_colors):
        return _blocked_report(
            core_fingerprint=core_fingerprint,
            receiver_source_commitment=receiver_source_commitment,
            code="receiver_relationship_changed",
            detail="Receiver intrinsic descriptor classes differ from the Change File.",
        )

    origin_incoming = _origin_incoming(origin)
    receiver_incoming = _receiver_incoming(receiver)
    refinement_rounds = 0
    for round_number in range(1, len(origin) + 1):
        next_origin = {
            member.logical_member_id: canonical_sha256(
                _origin_refinement_signature(
                    member,
                    colors=origin_colors,
                    incoming=origin_incoming[member.logical_member_id],
                )
            )
            for member in origin
        }
        next_receiver = {
            member.file_id: canonical_sha256(
                _receiver_refinement_signature(
                    member,
                    colors=receiver_colors,
                    incoming=receiver_incoming[member.file_id],
                )
            )
            for member in receiver
        }
        refinement_rounds = round_number
        if not _equal_color_cardinalities(next_origin, next_receiver):
            return _blocked_report(
                core_fingerprint=core_fingerprint,
                receiver_source_commitment=receiver_source_commitment,
                code="receiver_relationship_changed",
                detail="Supported relationship structure differs from the Change File.",
                refinement_rounds=refinement_rounds,
            )
        stable = _same_partition(origin_colors, next_origin) and _same_partition(
            receiver_colors, next_receiver
        )
        origin_colors = next_origin
        receiver_colors = next_receiver
        if stable:
            break

    origin_classes = _color_classes(origin_colors)
    receiver_classes = _color_classes(receiver_colors)
    ambiguous_sizes = sorted(
        len(members) for members in origin_classes.values() if len(members) > 1
    )
    if ambiguous_sizes:
        return _blocked_report(
            core_fingerprint=core_fingerprint,
            receiver_source_commitment=receiver_source_commitment,
            code="receiver_ambiguous_duplicate_group",
            detail=(
                "Receiver matching remains symmetric after deterministic refinement; "
                f"ambiguous class sizes={ambiguous_sizes!r}."
            ),
            refinement_rounds=refinement_rounds,
        )

    mappings: list[ConnectedChangeMatchMapping] = []
    for color, logical_ids in origin_classes.items():
        receiver_ids = receiver_classes[color]
        logical_id = logical_ids[0]
        receiver_id = receiver_ids[0]
        logical_member = origin_by_id[logical_id]
        receiver_member = receiver_by_id[receiver_id]
        mappings.append(
            ConnectedChangeMatchMapping(
                logical_member_id=logical_id,
                receiver_file_id=receiver_id,
                receiver_original_path=receiver_member.relative_path,
                target_relative_path=logical_member.target_relative_path,
            )
        )
    return _matched_report(
        core_fingerprint=core_fingerprint,
        receiver_source_commitment=receiver_source_commitment,
        refinement_rounds=refinement_rounds,
        mappings=tuple(sorted(mappings, key=lambda item: item.logical_member_id)),
    )


def _preflight_blocker(
    core: ConnectedChangeCore,
    receiver: Sequence[ReceiverDescriptor],
    *,
    receiver_empty_directories: Sequence[str],
) -> tuple[str, str] | None:
    origin = core.members
    if len(receiver) < len(origin):
        return "receiver_member_missing", "Receiver project has fewer regular files."
    if len(receiver) > len(origin):
        return "receiver_member_extra", "Receiver project has extra regular files."
    if tuple(sorted(receiver_empty_directories)) != (core.empty_directory_requirements):
        return (
            "receiver_empty_directory_mismatch",
            "Receiver explicit empty directories differ from the Change File.",
        )

    origin_protected = Counter(
        (
            member.origin_relative_path,
            member.byte_size,
            member.payload_sha256,
            member.protected_suffix,
        )
        for member in origin
        if member.protected
    )
    receiver_protected = Counter(
        (
            member.relative_path,
            member.byte_size,
            member.payload_sha256,
            member.protected_suffix,
        )
        for member in receiver
        if member.protected
    )
    if origin_protected != receiver_protected:
        return (
            "receiver_protected_member_mismatch",
            "Receiver protected paths or exact bytes differ from the Change File.",
        )

    origin_shapes = Counter(
        (member.descriptor_kind, member.protected) for member in origin
    )
    receiver_shapes = Counter(
        (member.descriptor_kind, member.protected) for member in receiver
    )
    if origin_shapes != receiver_shapes:
        return (
            "receiver_payload_changed",
            "Receiver member kinds differ from the Change File.",
        )

    origin_suffixes = Counter(
        (member.descriptor_kind, member.protected, member.protected_suffix)
        for member in origin
    )
    receiver_suffixes = Counter(
        (member.descriptor_kind, member.protected, member.protected_suffix)
        for member in receiver
    )
    if origin_suffixes != receiver_suffixes:
        return (
            "receiver_suffix_mismatch",
            "Receiver protected suffixes differ from the Change File.",
        )

    origin_ordinary = Counter(
        (member.byte_size, member.payload_sha256, member.protected)
        for member in origin
        if member.descriptor_kind == "ordinary"
    )
    receiver_ordinary = Counter(
        (member.byte_size, member.payload_sha256, member.protected)
        for member in receiver
        if member.descriptor_kind == "ordinary"
    )
    if origin_ordinary != receiver_ordinary:
        return (
            "receiver_payload_changed",
            "Receiver ordinary payload bytes differ from the Change File.",
        )

    origin_markdown_content = Counter(
        member.markdown_non_destination_sha256
        for member in origin
        if member.descriptor_kind == "markdown"
    )
    receiver_markdown_content = Counter(
        member.markdown_non_destination_sha256
        for member in receiver
        if member.descriptor_kind == "markdown"
    )
    if origin_markdown_content != receiver_markdown_content:
        return (
            "receiver_markdown_content_changed",
            "Receiver Markdown bytes outside supported destinations differ.",
        )

    origin_link_shapes = Counter(
        (
            member.markdown_non_destination_sha256,
            tuple(
                (slot.slot_index, slot.is_image, slot.syntax_class, slot.fragment)
                for slot in member.link_slots
            ),
        )
        for member in origin
        if member.descriptor_kind == "markdown"
    )
    receiver_link_shapes = Counter(
        (
            member.markdown_non_destination_sha256,
            tuple(
                (slot.slot_index, slot.is_image, slot.syntax_class, slot.fragment)
                for slot in member.link_slots
            ),
        )
        for member in receiver
        if member.descriptor_kind == "markdown"
    )
    if origin_link_shapes != receiver_link_shapes:
        return (
            "receiver_relationship_changed",
            "Receiver supported link-slot structure differs from the Change File.",
        )
    return None


def _origin_base(member: ConnectedChangeMember) -> dict[str, Any]:
    return {
        "descriptor_kind": member.descriptor_kind,
        "protected": member.protected,
        "protected_path": member.origin_relative_path if member.protected else None,
        "protected_suffix": member.protected_suffix,
        "byte_size": member.byte_size,
        "payload_sha256": member.payload_sha256,
        "markdown_non_destination_sha256": member.markdown_non_destination_sha256,
        "link_shape": [
            {
                "slot_index": slot.slot_index,
                "is_image": slot.is_image,
                "syntax_class": slot.syntax_class,
                "fragment": slot.fragment,
            }
            for slot in member.link_slots
        ],
    }


def _receiver_base(member: ReceiverDescriptor) -> dict[str, Any]:
    return {
        "descriptor_kind": member.descriptor_kind,
        "protected": member.protected,
        "protected_path": member.relative_path if member.protected else None,
        "protected_suffix": member.protected_suffix,
        "byte_size": member.byte_size,
        "payload_sha256": member.payload_sha256,
        "markdown_non_destination_sha256": member.markdown_non_destination_sha256,
        "link_shape": [
            {
                "slot_index": slot.slot_index,
                "is_image": slot.is_image,
                "syntax_class": slot.syntax_class,
                "fragment": slot.fragment,
            }
            for slot in member.link_slots
        ],
    }


def _origin_incoming(
    members: Sequence[ConnectedChangeMember],
) -> dict[str, list[tuple[str, Any]]]:
    incoming: dict[str, list[tuple[str, Any]]] = defaultdict(list)
    for member in members:
        incoming.setdefault(member.logical_member_id, [])
        for slot in member.link_slots:
            incoming[slot.target_logical_member_id].append(
                (member.logical_member_id, slot)
            )
    return incoming


def _receiver_incoming(
    members: Sequence[ReceiverDescriptor],
) -> dict[str, list[tuple[str, Any]]]:
    incoming: dict[str, list[tuple[str, Any]]] = defaultdict(list)
    known = {member.file_id for member in members}
    for member in members:
        incoming.setdefault(member.file_id, [])
        for slot in member.link_slots:
            if slot.target_file_id not in known:
                raise AssertionError(
                    "Validated receiver graph targets an unknown file."
                )
            incoming[slot.target_file_id].append((member.file_id, slot))
    return incoming


def _origin_refinement_signature(
    member: ConnectedChangeMember,
    *,
    colors: Mapping[str, str],
    incoming: Iterable[tuple[str, Any]],
) -> dict[str, Any]:
    return _refinement_signature(
        base=_origin_base(member),
        outgoing=(
            (
                slot.slot_index,
                slot.is_image,
                slot.syntax_class,
                slot.fragment,
                colors[slot.target_logical_member_id],
            )
            for slot in member.link_slots
        ),
        incoming=(
            (
                colors[source_id],
                slot.slot_index,
                slot.is_image,
                slot.syntax_class,
                slot.fragment,
            )
            for source_id, slot in incoming
        ),
    )


def _receiver_refinement_signature(
    member: ReceiverDescriptor,
    *,
    colors: Mapping[str, str],
    incoming: Iterable[tuple[str, Any]],
) -> dict[str, Any]:
    return _refinement_signature(
        base=_receiver_base(member),
        outgoing=(
            (
                slot.slot_index,
                slot.is_image,
                slot.syntax_class,
                slot.fragment,
                colors[slot.target_file_id],
            )
            for slot in member.link_slots
        ),
        incoming=(
            (
                colors[source_id],
                slot.slot_index,
                slot.is_image,
                slot.syntax_class,
                slot.fragment,
            )
            for source_id, slot in incoming
        ),
    )


def _refinement_signature(
    *,
    base: Mapping[str, Any],
    outgoing: Iterable[tuple[Any, ...]],
    incoming: Iterable[tuple[Any, ...]],
) -> dict[str, Any]:
    incoming_hashes = sorted(canonical_sha256(list(item)) for item in incoming)
    return {
        "base": dict(base),
        "outgoing": [list(item) for item in outgoing],
        "incoming": incoming_hashes,
    }


def _equal_color_cardinalities(
    origin: Mapping[str, str],
    receiver: Mapping[str, str],
) -> bool:
    return Counter(origin.values()) == Counter(receiver.values())


def _same_partition(before: Mapping[str, str], after: Mapping[str, str]) -> bool:
    keys = tuple(before)
    return all(
        (before[left] == before[right]) == (after[left] == after[right])
        for left in keys
        for right in keys
    )


def _color_classes(colors: Mapping[str, str]) -> dict[str, list[str]]:
    classes: dict[str, list[str]] = defaultdict(list)
    for member_id, color in colors.items():
        classes[color].append(member_id)
    return classes


def _matched_report(
    *,
    core_fingerprint: str,
    receiver_source_commitment: str,
    refinement_rounds: int,
    mappings: tuple[ConnectedChangeMatchMapping, ...],
) -> ConnectedChangeMatchReport:
    return _report(
        status="matched",
        core_fingerprint=core_fingerprint,
        receiver_source_commitment=receiver_source_commitment,
        refinement_rounds=refinement_rounds,
        mappings=mappings,
        blocker_code=None,
        detail=f"Matched every logical member exactly once ({len(mappings)} files).",
    )


def _blocked_report(
    *,
    core_fingerprint: str,
    receiver_source_commitment: str,
    code: str,
    detail: str,
    refinement_rounds: int = 0,
) -> ConnectedChangeMatchReport:
    return _report(
        status="blocked",
        core_fingerprint=core_fingerprint,
        receiver_source_commitment=receiver_source_commitment,
        refinement_rounds=refinement_rounds,
        mappings=(),
        blocker_code=code,
        detail=detail,
    )


def _report(**values: Any) -> ConnectedChangeMatchReport:
    provisional = ConnectedChangeMatchReport.model_construct(
        schema_version="connected-change-match-report.v1",
        match_report_fingerprint="0" * 64,
        **values,
    )
    return ConnectedChangeMatchReport(
        **provisional.model_dump(mode="python", exclude={"match_report_fingerprint"}),
        match_report_fingerprint=connected_change_match_report_fingerprint(provisional),
    )


def _core_fingerprint(core: ConnectedChangeCore | ConnectedChangeCoreV2) -> str:
    """Dispatch the immutable fingerprint domain without weakening either schema."""

    if isinstance(core, ConnectedChangeCoreV2):
        return connected_change_core_v2_fingerprint(core)
    return connected_change_core_fingerprint(core)
