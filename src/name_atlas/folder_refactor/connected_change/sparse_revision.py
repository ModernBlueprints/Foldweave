"""Provider-neutral deterministic compilation of sparse Foldweave revisions."""

from __future__ import annotations

from collections.abc import Collection

from name_atlas.folder_refactor.compiler import PlanCompilationError, compile_plan
from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
    convert_planner_accepted_plan,
)
from name_atlas.folder_refactor.contracts import (
    FolderInventory,
    FolderPlan,
    FolderPlanEntry,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderPlanRevisionV1,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph


def compile_sparse_revision_from_base(
    *,
    inventory: FolderInventory,
    request: str,
    reference_graph: FolderReferenceGraph,
    base_candidate: FolderAcceptedPlanV2,
    revision: FolderPlanRevisionV1,
    evidence_fingerprint: str,
    known_evidence_ids: Collection[str],
) -> FolderAcceptedPlanV2:
    """Compile one sparse model response against an immutable complete candidate."""

    by_file_id = {item.file_id: item for item in revision.entries}
    mappings = {item.file_id: item for item in base_candidate.file_mappings}
    unknown = set(by_file_id) - set(mappings)
    protected = {
        file_id for file_id, mapping in mappings.items() if mapping.protected
    } & set(by_file_id)
    if unknown:
        raise PlanCompilationError(
            "revision_unknown_file_id",
            f"Sparse revision names unknown file IDs: {sorted(unknown)!r}.",
        )
    if protected:
        raise PlanCompilationError(
            "revision_protected_file",
            f"Sparse revision names protected file IDs: {sorted(protected)!r}.",
        )
    result_folder_name = (
        revision.replacement_result_folder_name or base_candidate.result_folder_name
    )
    changed_target = any(
        mappings[file_id].target_path != entry.replacement_target_path
        for file_id, entry in by_file_id.items()
    )
    if not changed_target and result_folder_name == base_candidate.result_folder_name:
        raise PlanCompilationError(
            "revision_no_change",
            "Sparse revision does not change the reviewed structure.",
        )
    entries = []
    for mapping in base_candidate.file_mappings:
        if mapping.protected:
            continue
        replacement = by_file_id.get(mapping.file_id)
        entries.append(
            FolderPlanEntry(
                file_id=mapping.file_id,
                original_path=mapping.original_path,
                proposed_target=(
                    replacement.replacement_target_path
                    if replacement is not None
                    else mapping.target_path
                ),
                rationale=(
                    replacement.rationale
                    if replacement is not None
                    else "Retained from the mechanically accepted base proposal."
                ),
                evidence_ids=(
                    replacement.evidence_ids
                    if replacement is not None
                    else ("initial_inventory",)
                ),
            )
        )
    complete = FolderPlan(
        source_commitment=base_candidate.source_commitment,
        request_fingerprint=base_candidate.request_fingerprint,
        request_scope=base_candidate.request_scope,
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name=result_folder_name,
        entries=tuple(entries),
        exclusions=(),
    )
    compiled = compile_plan(
        inventory,
        request,
        complete,
        known_evidence_ids=set(known_evidence_ids),
        evidence_fingerprint=evidence_fingerprint,
        reference_graph=reference_graph,
    )
    return convert_planner_accepted_plan(
        inventory=inventory,
        request=request,
        plan=compiled,
        evidence_schema_version="folder-evidence-ledger.v2",
    )
