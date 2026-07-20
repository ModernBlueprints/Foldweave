"""Immutable renderer-facing plan previews for Foldweave review jobs."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Literal, Self

from pydantic import Field, model_validator

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.contracts import (
    SHA256_PATTERN,
    FolderInventory,
    StrictFrozenModel,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.markdown_links import derive_reference_rewrites
from name_atlas.folder_refactor.serialization import canonical_sha256

FOLDER_PLAN_PREVIEW_SCHEMA_VERSION = "folder-plan-preview.v1"


class FolderPlanTreeMember(StrictFrozenModel):
    """One member in either complete side of the review tree."""

    member_id: str = Field(pattern=SHA256_PATTERN)
    member_kind: Literal["regular_file", "empty_directory"]
    relative_path: str = Field(min_length=1, max_length=4_096)
    directory_prefixes: tuple[str, ...]
    protected: bool


class FolderPlanLinkEffect(StrictFrozenModel):
    """One supported Markdown connection derived for the proposed tree."""

    reference_id: str = Field(pattern=SHA256_PATTERN)
    source_member_id: str = Field(pattern=SHA256_PATTERN)
    target_member_id: str = Field(pattern=SHA256_PATTERN)
    current_source_path: str = Field(min_length=1, max_length=4_096)
    current_target_path: str = Field(min_length=1, max_length=4_096)
    proposed_source_path: str = Field(min_length=1, max_length=4_096)
    proposed_target_path: str = Field(min_length=1, max_length=4_096)
    original_destination: str = Field(min_length=1, max_length=8_192)
    proposed_destination: str = Field(min_length=1, max_length=8_192)
    status: Literal["unchanged", "rewritten"]


class FolderPlanMemberChange(StrictFrozenModel):
    """The path and authority comparison for one local source member."""

    member_id: str = Field(pattern=SHA256_PATTERN)
    member_kind: Literal["regular_file", "empty_directory"]
    current_relative_path: str = Field(min_length=1, max_length=4_096)
    proposed_relative_path: str = Field(min_length=1, max_length=4_096)
    change_classification: Literal[
        "unchanged",
        "renamed",
        "moved",
        "moved_and_renamed",
        "protected",
        "empty_directory",
    ]
    protected: bool
    authority_source: Literal["gpt_plan", "change_file", "protected"]
    rationale: str = Field(min_length=1, max_length=1_000)
    link_updated: bool = False
    supported_link_effect_ids: tuple[str, ...] = ()


class FolderPlanFinding(StrictFrozenModel):
    """One deterministic collision or blocker surfaced to the reviewer."""

    finding_id: str = Field(pattern=r"^[a-z0-9_:-]{1,128}$")
    severity: Literal["collision", "blocker"]
    detail: str = Field(min_length=1, max_length=2_000)
    member_ids: tuple[str, ...] = ()


class FolderPlanPreviewCounts(StrictFrozenModel):
    """Exact bounded counts shown in every review surface."""

    file_count: int = Field(ge=1, le=500)
    empty_directory_count: int = Field(ge=0, le=1_000)
    changed_path_count: int = Field(ge=0, le=500)
    renamed_count: int = Field(ge=0, le=500)
    moved_count: int = Field(ge=0, le=500)
    link_count: int = Field(ge=0)
    link_updated_count: int = Field(ge=0)
    protected_count: int = Field(ge=0, le=500)
    blocker_count: int = Field(ge=0)


class FolderPlanPreviewV1(StrictFrozenModel):
    """The sole complete DTO rendered and accepted by every Foldweave surface."""

    schema_version: Literal["folder-plan-preview.v1"] = (
        FOLDER_PLAN_PREVIEW_SCHEMA_VERSION
    )
    job_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    expected_job_revision: int = Field(ge=0)
    proposal_revision: int = Field(ge=0, le=2)
    proposal_basis: Literal[
        "fresh_gpt_plan",
        "imported_change_file",
        "gpt_derivative",
    ]
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    imported_change_file_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    match_report_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    immediate_parent_candidate_fingerprint: str | None = Field(
        default=None,
        pattern=SHA256_PATTERN,
    )
    current_tree_members: tuple[FolderPlanTreeMember, ...]
    proposed_tree_members: tuple[FolderPlanTreeMember, ...]
    member_changes: tuple[FolderPlanMemberChange, ...]
    supported_link_effects: tuple[FolderPlanLinkEffect, ...]
    collision_findings: tuple[FolderPlanFinding, ...] = ()
    blocker_findings: tuple[FolderPlanFinding, ...] = ()
    counts: FolderPlanPreviewCounts
    compiled_candidate_fingerprint: str = Field(pattern=SHA256_PATTERN)
    preview_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_complete_preview(self) -> Self:
        current_ids = tuple(item.member_id for item in self.current_tree_members)
        proposed_ids = tuple(item.member_id for item in self.proposed_tree_members)
        change_ids = tuple(item.member_id for item in self.member_changes)
        if len(current_ids) != len(set(current_ids)):
            raise ValueError("Current preview members must have unique IDs.")
        if len(proposed_ids) != len(set(proposed_ids)):
            raise ValueError("Proposed preview members must have unique IDs.")
        if len(change_ids) != len(set(change_ids)):
            raise ValueError("Preview changes must have unique member IDs.")
        if set(current_ids) != set(proposed_ids) or set(current_ids) != set(change_ids):
            raise ValueError("Both preview trees must account for every member once.")
        current_paths = tuple(item.relative_path for item in self.current_tree_members)
        proposed_paths = tuple(
            item.relative_path for item in self.proposed_tree_members
        )
        if len(current_paths) != len(set(current_paths)) or len(proposed_paths) != len(
            set(proposed_paths)
        ):
            raise ValueError("Each preview tree path must identify one member.")
        if self.current_tree_members != tuple(
            sorted(self.current_tree_members, key=lambda item: item.relative_path)
        ):
            raise ValueError("Current preview tree must be path sorted.")
        if self.proposed_tree_members != tuple(
            sorted(self.proposed_tree_members, key=lambda item: item.relative_path)
        ):
            raise ValueError("Proposed preview tree must be path sorted.")
        if self.member_changes != tuple(
            sorted(self.member_changes, key=lambda item: item.current_relative_path)
        ):
            raise ValueError("Preview changes must use current-path order.")
        if self.supported_link_effects != tuple(
            sorted(
                self.supported_link_effects,
                key=lambda item: (item.current_source_path, item.reference_id),
            )
        ):
            raise ValueError("Preview link effects must be deterministically ordered.")
        self._require_projection_consistency()
        portable_bindings = (
            self.imported_change_file_fingerprint,
            self.match_report_fingerprint,
            self.immediate_parent_candidate_fingerprint,
        )
        if self.proposal_basis == "imported_change_file":
            if (
                self.imported_change_file_fingerprint is None
                or self.match_report_fingerprint is None
                or self.immediate_parent_candidate_fingerprint is not None
            ):
                raise ValueError(
                    "An imported proposal requires only Change File and match "
                    "fingerprints."
                )
        elif self.proposal_basis == "gpt_derivative":
            if any(value is None for value in portable_bindings):
                raise ValueError(
                    "A derivative proposal requires Change File, match, and "
                    "immediate-parent candidate fingerprints."
                )
        elif any(value is not None for value in portable_bindings):
            raise ValueError("A fresh proposal cannot retain derivative authority.")
        expected = canonical_sha256(
            self.model_dump(mode="json", exclude={"preview_fingerprint"})
        )
        if self.preview_fingerprint != expected:
            raise ValueError(
                "Preview fingerprint does not match its complete contents."
            )
        return self

    def _require_projection_consistency(self) -> None:
        current_by_id = {item.member_id: item for item in self.current_tree_members}
        proposed_by_id = {item.member_id: item for item in self.proposed_tree_members}
        change_by_id = {item.member_id: item for item in self.member_changes}
        for member_id, change in change_by_id.items():
            current = current_by_id[member_id]
            proposed = proposed_by_id[member_id]
            if (
                current.member_kind != change.member_kind
                or proposed.member_kind != change.member_kind
                or current.relative_path != change.current_relative_path
                or proposed.relative_path != change.proposed_relative_path
                or current.protected != change.protected
                or proposed.protected != change.protected
                or current.directory_prefixes
                != _directory_prefixes(current.relative_path)
                or proposed.directory_prefixes
                != _directory_prefixes(proposed.relative_path)
            ):
                raise ValueError(
                    "Preview member changes must exactly reconcile both trees."
                )
            expected_classification = (
                "empty_directory"
                if change.member_kind == "empty_directory"
                else _classify_change(
                    current_path=change.current_relative_path,
                    proposed_path=change.proposed_relative_path,
                    protected=change.protected,
                )
            )
            if change.change_classification != expected_classification:
                raise ValueError(
                    "Preview change classification differs from its exact paths."
                )
            if change.member_kind == "empty_directory" and (
                not change.protected
                or change.authority_source != "protected"
                or change.current_relative_path != change.proposed_relative_path
            ):
                raise ValueError(
                    "Explicit empty directories must remain protected and unchanged."
                )
            if change.protected != (change.authority_source == "protected"):
                raise ValueError("Preview protection and member authority must agree.")

        effect_ids = tuple(item.reference_id for item in self.supported_link_effects)
        if len(effect_ids) != len(set(effect_ids)):
            raise ValueError("Preview link effects must have unique reference IDs.")
        effects_by_source: dict[str, list[FolderPlanLinkEffect]] = {}
        for effect in self.supported_link_effects:
            if (
                effect.source_member_id not in current_by_id
                or effect.target_member_id not in current_by_id
            ):
                raise ValueError("Preview link effects must target visible members.")
            source_current = current_by_id[effect.source_member_id]
            source_proposed = proposed_by_id[effect.source_member_id]
            target_current = current_by_id[effect.target_member_id]
            target_proposed = proposed_by_id[effect.target_member_id]
            if (
                effect.current_source_path != source_current.relative_path
                or effect.proposed_source_path != source_proposed.relative_path
                or effect.current_target_path != target_current.relative_path
                or effect.proposed_target_path != target_proposed.relative_path
            ):
                raise ValueError("Preview link paths must reconcile both trees.")
            effects_by_source.setdefault(effect.source_member_id, []).append(effect)

        for member_id, change in change_by_id.items():
            outgoing = effects_by_source.get(member_id, [])
            expected_ids = tuple(sorted(item.reference_id for item in outgoing))
            if change.supported_link_effect_ids != expected_ids or (
                change.link_updated
                != any(item.status == "rewritten" for item in outgoing)
            ):
                raise ValueError(
                    "Preview member link summaries differ from complete link effects."
                )

        for finding in self.collision_findings:
            if finding.severity != "collision" or any(
                member_id not in current_by_id for member_id in finding.member_ids
            ):
                raise ValueError("Collision findings must name visible members.")
        for finding in self.blocker_findings:
            if finding.severity != "blocker" or any(
                member_id not in current_by_id for member_id in finding.member_ids
            ):
                raise ValueError("Blocker findings must name visible members.")

        regular_changes = tuple(
            item for item in self.member_changes if item.member_kind == "regular_file"
        )
        changed = tuple(
            item
            for item in regular_changes
            if item.current_relative_path != item.proposed_relative_path
        )
        expected_counts = FolderPlanPreviewCounts(
            file_count=len(regular_changes),
            empty_directory_count=len(self.member_changes) - len(regular_changes),
            changed_path_count=len(changed),
            renamed_count=sum(
                PurePosixPath(item.current_relative_path).name
                != PurePosixPath(item.proposed_relative_path).name
                for item in changed
            ),
            moved_count=sum(
                PurePosixPath(item.current_relative_path).parent
                != PurePosixPath(item.proposed_relative_path).parent
                for item in changed
            ),
            link_count=len(self.supported_link_effects),
            link_updated_count=sum(
                item.status == "rewritten" for item in self.supported_link_effects
            ),
            protected_count=sum(item.protected for item in regular_changes),
            blocker_count=len(self.blocker_findings),
        )
        if self.counts != expected_counts:
            raise ValueError("Preview counts differ from its complete contents.")


def build_folder_plan_preview(
    *,
    job_id: str,
    expected_job_revision: int,
    proposal_revision: int,
    proposal_basis: Literal[
        "fresh_gpt_plan",
        "imported_change_file",
        "gpt_derivative",
    ],
    inventory: FolderInventory,
    reference_graph: FolderReferenceGraph,
    accepted_plan: FolderAcceptedPlanV2,
    imported_change_file_fingerprint: str | None = None,
    match_report_fingerprint: str | None = None,
    immediate_parent_candidate_fingerprint: str | None = None,
) -> FolderPlanPreviewV1:
    """Build one complete path-neutral review DTO from compiled authority."""

    if accepted_plan.source_commitment != inventory.source_commitment:
        raise ValueError("Preview plan targets another source inventory.")
    candidate_fingerprint = canonical_sha256(accepted_plan)
    by_id = {mapping.file_id: mapping for mapping in accepted_plan.file_mappings}
    derived_graph = derive_reference_rewrites(reference_graph, accepted_plan)
    link_effects = tuple(
        sorted(
            (
                FolderPlanLinkEffect(
                    reference_id=reference.reference_id,
                    source_member_id=reference.source_file_id,
                    target_member_id=reference.target_file_id,
                    current_source_path=reference.source_path,
                    current_target_path=reference.target_path,
                    proposed_source_path=by_id[reference.source_file_id].target_path,
                    proposed_target_path=by_id[reference.target_file_id].target_path,
                    original_destination=reference.original_destination_text,
                    proposed_destination=_require_proposed_destination(reference),
                    status=reference.verification_status,
                )
                for reference in derived_graph.references
            ),
            key=lambda item: (item.current_source_path, item.reference_id),
        )
    )
    links_by_source: dict[str, list[str]] = {}
    for effect in link_effects:
        links_by_source.setdefault(effect.source_member_id, []).append(
            effect.reference_id
        )

    current: list[FolderPlanTreeMember] = []
    proposed: list[FolderPlanTreeMember] = []
    changes: list[FolderPlanMemberChange] = []
    for item in inventory.files:
        mapping = by_id[item.file_id]
        current.append(
            _tree_member(
                member_id=item.file_id,
                member_kind="regular_file",
                relative_path=item.relative_path,
                protected=item.protected,
            )
        )
        proposed.append(
            _tree_member(
                member_id=item.file_id,
                member_kind="regular_file",
                relative_path=mapping.target_path,
                protected=item.protected,
            )
        )
        classification = _classify_change(
            current_path=item.relative_path,
            proposed_path=mapping.target_path,
            protected=item.protected,
        )
        changes.append(
            FolderPlanMemberChange(
                member_id=item.file_id,
                member_kind="regular_file",
                current_relative_path=item.relative_path,
                proposed_relative_path=mapping.target_path,
                change_classification=classification,
                protected=item.protected,
                authority_source=mapping.authority,
                rationale=_change_rationale(
                    current_path=item.relative_path,
                    proposed_path=mapping.target_path,
                    protected=item.protected,
                    authority=mapping.authority,
                ),
                link_updated=any(
                    effect.status == "rewritten"
                    for effect in link_effects
                    if effect.source_member_id == item.file_id
                ),
                supported_link_effect_ids=tuple(
                    sorted(links_by_source.get(item.file_id, ()))
                ),
            )
        )
    for item in inventory.empty_directories:
        member_id = canonical_sha256(
            {
                "domain": "foldweave:empty-directory-member:v1",
                "source_commitment": inventory.source_commitment,
                "relative_path": item.relative_path,
            }
        )
        current.append(
            _tree_member(
                member_id=member_id,
                member_kind="empty_directory",
                relative_path=item.relative_path,
                protected=True,
            )
        )
        proposed.append(
            _tree_member(
                member_id=member_id,
                member_kind="empty_directory",
                relative_path=item.relative_path,
                protected=True,
            )
        )
        changes.append(
            FolderPlanMemberChange(
                member_id=member_id,
                member_kind="empty_directory",
                current_relative_path=item.relative_path,
                proposed_relative_path=item.relative_path,
                change_classification="empty_directory",
                protected=True,
                authority_source="protected",
                rationale="Keep this explicit empty directory unchanged.",
            )
        )
    current_members = tuple(sorted(current, key=lambda item: item.relative_path))
    proposed_members = tuple(sorted(proposed, key=lambda item: item.relative_path))
    member_changes = tuple(sorted(changes, key=lambda item: item.current_relative_path))
    changed = tuple(
        item
        for item in member_changes
        if item.member_kind == "regular_file"
        and item.current_relative_path != item.proposed_relative_path
    )
    renamed = tuple(
        item
        for item in changed
        if PurePosixPath(item.current_relative_path).name
        != PurePosixPath(item.proposed_relative_path).name
    )
    moved = tuple(
        item
        for item in changed
        if PurePosixPath(item.current_relative_path).parent
        != PurePosixPath(item.proposed_relative_path).parent
    )
    counts = FolderPlanPreviewCounts(
        file_count=len(inventory.files),
        empty_directory_count=len(inventory.empty_directories),
        changed_path_count=len(changed),
        renamed_count=len(renamed),
        moved_count=len(moved),
        link_count=len(link_effects),
        link_updated_count=sum(item.status == "rewritten" for item in link_effects),
        protected_count=sum(item.protected for item in inventory.files),
        blocker_count=0,
    )
    payload = {
        "schema_version": FOLDER_PLAN_PREVIEW_SCHEMA_VERSION,
        "job_id": job_id,
        "expected_job_revision": expected_job_revision,
        "proposal_revision": proposal_revision,
        "proposal_basis": proposal_basis,
        "source_commitment": inventory.source_commitment,
        "imported_change_file_fingerprint": imported_change_file_fingerprint,
        "match_report_fingerprint": match_report_fingerprint,
        "immediate_parent_candidate_fingerprint": (
            immediate_parent_candidate_fingerprint
        ),
        "current_tree_members": current_members,
        "proposed_tree_members": proposed_members,
        "member_changes": member_changes,
        "supported_link_effects": link_effects,
        "collision_findings": (),
        "blocker_findings": (),
        "counts": counts,
        "compiled_candidate_fingerprint": candidate_fingerprint,
    }
    fingerprint_payload = {
        **payload,
        "current_tree_members": tuple(
            item.model_dump(mode="json") for item in current_members
        ),
        "proposed_tree_members": tuple(
            item.model_dump(mode="json") for item in proposed_members
        ),
        "member_changes": tuple(
            item.model_dump(mode="json") for item in member_changes
        ),
        "supported_link_effects": tuple(
            item.model_dump(mode="json") for item in link_effects
        ),
        "counts": counts.model_dump(mode="json"),
    }
    return FolderPlanPreviewV1(
        **payload,
        preview_fingerprint=canonical_sha256(fingerprint_payload),
    )


def _tree_member(
    *,
    member_id: str,
    member_kind: Literal["regular_file", "empty_directory"],
    relative_path: str,
    protected: bool,
) -> FolderPlanTreeMember:
    return FolderPlanTreeMember(
        member_id=member_id,
        member_kind=member_kind,
        relative_path=relative_path,
        directory_prefixes=_directory_prefixes(relative_path),
        protected=protected,
    )


def _directory_prefixes(relative_path: str) -> tuple[str, ...]:
    parent = PurePosixPath(relative_path).parent
    if parent.as_posix() == ".":
        return ()
    parts = parent.parts
    return tuple(
        PurePosixPath(*parts[:index]).as_posix() for index in range(1, len(parts) + 1)
    )


def _classify_change(
    *, current_path: str, proposed_path: str, protected: bool
) -> Literal[
    "unchanged",
    "renamed",
    "moved",
    "moved_and_renamed",
    "protected",
]:
    if protected:
        return "protected"
    if current_path == proposed_path:
        return "unchanged"
    current = PurePosixPath(current_path)
    proposed = PurePosixPath(proposed_path)
    renamed = current.name != proposed.name
    moved = current.parent != proposed.parent
    if renamed and moved:
        return "moved_and_renamed"
    if renamed:
        return "renamed"
    return "moved"


def _change_rationale(
    *,
    current_path: str,
    proposed_path: str,
    protected: bool,
    authority: Literal["gpt_plan", "change_file", "protected"],
) -> str:
    if protected:
        return "Keep this protected file at its exact source path."
    if authority == "change_file":
        return "Target prescribed by the imported Foldweave Change File."
    if current_path == proposed_path:
        return "Keep this file at its current relative path."
    return f"Place {current_path} at {proposed_path}."


def _require_proposed_destination(reference: object) -> str:
    proposed = getattr(reference, "proposed_destination", None)
    if not isinstance(proposed, str) or not proposed:
        raise ValueError("Derived preview reference lacks a destination.")
    return proposed
