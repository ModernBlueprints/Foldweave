"""Truthful mechanically accepted plans for Connected Change execution."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal, Self

from pydantic import Field, model_validator

from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderAcceptedPlan,
    FolderInventory,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.naming import (
    validate_complete_target_tree,
    validate_result_folder_name,
    validate_target_path,
)
from name_atlas.folder_refactor.serialization import request_fingerprint


class ConnectedAcceptedFileMapping(StrictFrozenModel):
    """One source-local mapping with an explicit non-fabricated authority."""

    file_id: str = Field(pattern=SHA256_PATTERN)
    original_path: str = Field(min_length=1, max_length=4_096)
    target_path: str = Field(min_length=1, max_length=1_024)
    protected: bool
    authority: Literal["gpt_plan", "change_file", "protected"]

    @model_validator(mode="after")
    def require_truthful_authority(self) -> Self:
        validate_target_path(
            self.target_path,
            original_path=self.original_path,
            protected=self.protected,
        )
        if self.protected:
            if self.authority != "protected" or self.target_path != self.original_path:
                raise ValueError(
                    "Protected mappings require protected authority and an "
                    "unchanged path."
                )
        elif self.authority == "protected":
            raise ValueError("An unprotected mapping cannot use protected authority.")
        return self


class FolderAcceptedPlanV2(StrictFrozenModel):
    """Complete immutable map for GPT-planned or Change-File-applied execution."""

    schema_version: Literal["folder-accepted-plan.v2"] = "folder-accepted-plan.v2"
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    request_scope: Literal["rename_and_move_every_file"] = "rename_and_move_every_file"
    evidence_schema_version: Literal[
        "folder-evidence-ledger.v1",
        "folder-evidence-ledger.v2",
    ] = "folder-evidence-ledger.v1"
    evidence_fingerprint: str = Field(pattern=SHA256_PATTERN)
    execution_authority: Literal["gpt_plan", "change_file"]
    result_folder_name: str = Field(min_length=1, max_length=240)
    file_mappings: tuple[ConnectedAcceptedFileMapping, ...] = Field(
        min_length=1,
        max_length=500,
    )
    empty_directories: tuple[str, ...] = ()

    @model_validator(mode="after")
    def require_complete_shape(self) -> Self:
        validate_result_folder_name(self.result_folder_name)
        originals = tuple(mapping.original_path for mapping in self.file_mappings)
        file_ids = tuple(mapping.file_id for mapping in self.file_mappings)
        targets = tuple(mapping.target_path for mapping in self.file_mappings)
        if originals != tuple(sorted(originals)) or len(originals) != len(
            set(originals)
        ):
            raise ValueError("Accepted mappings must be sorted and source-path unique.")
        if len(file_ids) != len(set(file_ids)):
            raise ValueError("Accepted mappings must contain unique file IDs.")
        for mapping in self.file_mappings:
            expected_authority = (
                "protected" if mapping.protected else self.execution_authority
            )
            if mapping.authority != expected_authority:
                raise ValueError(
                    "Mapping authority does not match the plan execution authority."
                )
        if self.empty_directories != tuple(sorted(set(self.empty_directories))):
            raise ValueError("Accepted empty directories must be sorted and unique.")
        for path in self.empty_directories:
            validate_target_path(path, original_path=path, protected=True)
        validate_complete_target_tree(targets, self.empty_directories)
        return self


def build_connected_accepted_plan(
    *,
    inventory: FolderInventory,
    request: str,
    evidence_fingerprint: str,
    result_folder_name: str,
    target_by_file_id: Mapping[str, str],
    execution_authority: Literal["gpt_plan", "change_file"],
    evidence_schema_version: Literal[
        "folder-evidence-ledger.v1",
        "folder-evidence-ledger.v2",
    ] = "folder-evidence-ledger.v1",
) -> FolderAcceptedPlanV2:
    """Build and independently rebind one complete v2 accepted map."""

    expected_ids = {item.file_id for item in inventory.files if not item.protected}
    supplied_ids = set(target_by_file_id)
    if supplied_ids != expected_ids:
        missing = sorted(expected_ids - supplied_ids)
        unexpected = sorted(supplied_ids - expected_ids)
        raise ValueError(
            "accepted_plan_file_accounting_mismatch: "
            f"missing={missing!r}, unexpected={unexpected!r}"
        )
    mappings = []
    for source_file in inventory.files:
        if source_file.protected:
            target = source_file.relative_path
            authority: Literal["gpt_plan", "change_file", "protected"] = "protected"
        else:
            target = target_by_file_id[source_file.file_id]
            authority = execution_authority
        mappings.append(
            ConnectedAcceptedFileMapping(
                file_id=source_file.file_id,
                original_path=source_file.relative_path,
                target_path=target,
                protected=source_file.protected,
                authority=authority,
            )
        )
    plan = FolderAcceptedPlanV2(
        source_commitment=inventory.source_commitment,
        request_fingerprint=request_fingerprint(request),
        evidence_schema_version=evidence_schema_version,
        evidence_fingerprint=evidence_fingerprint,
        execution_authority=execution_authority,
        result_folder_name=result_folder_name,
        file_mappings=tuple(sorted(mappings, key=lambda item: item.original_path)),
        empty_directories=tuple(
            item.relative_path for item in inventory.empty_directories
        ),
    )
    validate_connected_accepted_plan(inventory=inventory, request=request, plan=plan)
    return plan


def convert_planner_accepted_plan(
    *,
    inventory: FolderInventory,
    request: str,
    plan: FolderAcceptedPlan,
    evidence_schema_version: Literal[
        "folder-evidence-ledger.v1",
        "folder-evidence-ledger.v2",
    ] = "folder-evidence-ledger.v1",
) -> FolderAcceptedPlanV2:
    """Convert one mechanically accepted v1 planner map into v2 authority."""

    if (
        plan.source_commitment != inventory.source_commitment
        or plan.request_fingerprint != request_fingerprint(request)
    ):
        raise ValueError(
            "planner_accepted_plan_binding_mismatch: plan targets another job"
        )
    target_by_file_id = {
        mapping.file_id: mapping.target_path
        for mapping in plan.file_mappings
        if not mapping.protected
    }
    converted = build_connected_accepted_plan(
        inventory=inventory,
        request=request,
        evidence_fingerprint=plan.evidence_fingerprint,
        result_folder_name=plan.result_folder_name,
        target_by_file_id=target_by_file_id,
        execution_authority="gpt_plan",
        evidence_schema_version=evidence_schema_version,
    )
    before = {
        mapping.file_id: (
            mapping.original_path,
            mapping.target_path,
            mapping.protected,
        )
        for mapping in plan.file_mappings
    }
    after = {
        mapping.file_id: (
            mapping.original_path,
            mapping.target_path,
            mapping.protected,
        )
        for mapping in converted.file_mappings
    }
    if before != after or plan.empty_directories != converted.empty_directories:
        raise ValueError(
            "planner_accepted_plan_conversion_mismatch: v2 map changed planner output"
        )
    return converted


def validate_connected_accepted_plan(
    *,
    inventory: FolderInventory,
    request: str,
    plan: FolderAcceptedPlanV2,
) -> None:
    """Rebind a serialized v2 plan to an independently scanned source."""

    if plan.source_commitment != inventory.source_commitment:
        raise ValueError("source_commitment_mismatch: plan targets another source")
    if plan.request_fingerprint != request_fingerprint(request):
        raise ValueError("request_fingerprint_mismatch: plan targets another request")
    by_id = {item.file_id: item for item in inventory.files}
    mappings = {item.file_id: item for item in plan.file_mappings}
    if set(mappings) != set(by_id):
        raise ValueError(
            "accepted_plan_file_accounting_mismatch: every source file is required"
        )
    for file_id, source_file in by_id.items():
        mapping = mappings[file_id]
        if (
            mapping.original_path != source_file.relative_path
            or mapping.protected != source_file.protected
        ):
            raise ValueError(
                "accepted_plan_source_binding_mismatch: "
                f"mapping differs for {source_file.relative_path}"
            )
        expected_authority = (
            "protected" if source_file.protected else plan.execution_authority
        )
        if mapping.authority != expected_authority:
            raise ValueError(
                "accepted_plan_authority_mismatch: "
                f"mapping authority differs for {source_file.relative_path}"
            )
        validate_target_path(
            mapping.target_path,
            original_path=source_file.relative_path,
            protected=source_file.protected,
        )
    expected_empty = tuple(item.relative_path for item in inventory.empty_directories)
    if plan.empty_directories != expected_empty:
        raise ValueError(
            "accepted_plan_empty_directory_mismatch: explicit empty directories differ"
        )
