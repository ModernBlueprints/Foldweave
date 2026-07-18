"""Bounded planner Protocol and deterministic A1 development implementation."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from name_atlas.folder_refactor.contracts import (
    FolderInventory,
    FolderPlan,
    FolderPlanEntry,
    FolderPlannerOutcome,
    PlanOutcome,
)
from name_atlas.folder_refactor.serialization import (
    canonical_sha256,
    request_fingerprint,
)


@runtime_checkable
class FolderPlanner(Protocol):
    """Produce one bounded outcome without filesystem mutation authority."""

    async def plan(
        self,
        *,
        request: str,
        inventory: FolderInventory,
        evidence_fingerprint: str,
    ) -> FolderPlannerOutcome:
        """Return a strict plan, clarification, or blocker."""
        ...


class DeterministicDevelopmentPlanner:
    """A truthful no-API A1 planner used only for the walking transaction."""

    def __init__(
        self,
        *,
        result_folder_name: str = "name-atlas-organized-copy",
        target_prefix: str = "organized",
    ) -> None:
        self._result_folder_name = result_folder_name
        self._target_prefix = target_prefix
        self.invocation_count = 0

    async def plan(
        self,
        *,
        request: str,
        inventory: FolderInventory,
        evidence_fingerprint: str,
    ) -> FolderPlannerOutcome:
        """Return a deterministic complete map for the current A1 slice."""

        self.invocation_count += 1
        entries = tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=f"{self._target_prefix}/{item.relative_path}",
                rationale=(
                    "Deterministic A1 development plan; semantic GPT-5.6 "
                    "planning is introduced at A4."
                ),
                evidence_ids=(f"inventory:{item.file_id}",),
            )
            for item in inventory.files
            if not item.protected
        )
        plan = FolderPlan(
            source_commitment=inventory.source_commitment,
            request_fingerprint=request_fingerprint(request),
            request_scope="rename_and_move_every_file",
            evidence_fingerprint=evidence_fingerprint,
            result_folder_name=self._result_folder_name,
            entries=entries,
            exclusions=(),
        )
        return PlanOutcome(plan=plan)


def initial_evidence_fingerprint(inventory: FolderInventory) -> str:
    """Bind the exact path-and-metadata evidence available in A1."""

    records = [
        {
            "evidence_id": f"inventory:{item.file_id}",
            "member": item.model_dump(mode="json"),
        }
        for item in inventory.files
    ]
    return canonical_sha256(
        {
            "schema_version": "folder-evidence-ledger.v1",
            "source_commitment": inventory.source_commitment,
            "records": records,
        }
    )
