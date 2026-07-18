"""AI-first planner schema, authority, and deterministic compiler tests."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from name_atlas.folder_refactor.compiler import PlanCompilationError, compile_plan
from name_atlas.folder_refactor.contracts import (
    FolderAcceptedPlan,
    FolderPlan,
    FolderPlanEntry,
    FolderPlannerOutcome,
    PlanOutcome,
)
from name_atlas.folder_refactor.inventory import (
    FolderScan,
    inventory_evidence_ids,
    scan_folder,
)
from name_atlas.folder_refactor.markdown_links import build_reference_graph
from name_atlas.folder_refactor.naming import protected_suffix
from name_atlas.folder_refactor.planner import (
    DeterministicDevelopmentPlanner,
    FolderPlanner,
    initial_evidence_fingerprint,
)
from name_atlas.folder_refactor.serialization import request_fingerprint

REQUEST = "Organize this folder for a colleague and keep every file."


def _write(root: Path, relative_path: str, payload: bytes = b"payload") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)


def _scan(tmp_path: Path, *, collision_sources: bool = False) -> FolderScan:
    source = tmp_path / "source"
    source.mkdir()
    _write(source, "notes.md")
    _write(source, "brief.md" if collision_sources else "draft.txt")
    _write(source, "archive.tar.GZ")
    _write(source, "README")
    _write(source, ".env")
    _write(source, "credentials.txt")
    (source / "empty").mkdir()
    return scan_folder(source)


def _complete_plan(
    scan: FolderScan,
    *,
    targets: dict[str, str] | None = None,
    result_folder_name: str = "organized-result",
) -> FolderPlan:
    overrides = targets or {}
    entries = tuple(
        FolderPlanEntry(
            file_id=item.file_id,
            original_path=item.relative_path,
            proposed_target=overrides.get(
                item.relative_path,
                f"organized/{item.relative_path}",
            ),
            rationale="Required by the user's organization request.",
            evidence_ids=(f"inventory:{item.file_id}",),
        )
        for item in scan.inventory.files
        if not item.protected
    )
    return FolderPlan(
        source_commitment=scan.inventory.source_commitment,
        request_fingerprint=request_fingerprint(REQUEST),
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=initial_evidence_fingerprint(scan.inventory),
        result_folder_name=result_folder_name,
        entries=entries,
        exclusions=(),
    )


def _compile(scan: FolderScan, plan: FolderPlan) -> FolderAcceptedPlan:
    return compile_plan(
        scan.inventory,
        REQUEST,
        plan,
        known_evidence_ids=inventory_evidence_ids(scan.inventory),
        evidence_fingerprint=initial_evidence_fingerprint(scan.inventory),
        reference_graph=build_reference_graph(
            scan.inventory,
            {
                item.relative_path: (scan.source_root / item.relative_path).read_bytes()
                for item in scan.inventory.files
                if Path(item.relative_path).suffix.casefold() in {".md", ".markdown"}
            },
        ),
    )


def _replace_plan(plan: FolderPlan, **updates: Any) -> FolderPlan:
    values = plan.model_dump(mode="python")
    values.update(updates)
    return FolderPlan.model_validate(values, strict=True)


def _replace_entry(entry: FolderPlanEntry, **updates: Any) -> FolderPlanEntry:
    values = entry.model_dump(mode="python")
    values.update(updates)
    return FolderPlanEntry.model_validate(values, strict=True)


def test_complete_plan_compiles_to_exact_file_bijection(tmp_path: Path) -> None:
    scan = _scan(tmp_path)

    accepted = _compile(scan, _complete_plan(scan))

    assert accepted.schema_version == "folder-accepted-plan.v1"
    assert len(accepted.file_mappings) == len(scan.inventory.files)
    assert {item.file_id for item in accepted.file_mappings} == {
        item.file_id for item in scan.inventory.files
    }
    assert {item.original_path for item in accepted.file_mappings} == {
        item.relative_path for item in scan.inventory.files
    }
    assert accepted.empty_directories == ("empty",)
    assert accepted.source_commitment == scan.inventory.source_commitment
    assert accepted.request_fingerprint == request_fingerprint(REQUEST)
    assert accepted.evidence_fingerprint == initial_evidence_fingerprint(scan.inventory)

    by_source = {item.original_path: item for item in accepted.file_mappings}
    assert by_source[".env"].target_path == ".env"
    assert by_source[".env"].protected is True
    assert by_source[".env"].planner_supplied is False
    assert by_source["credentials.txt"].target_path == "credentials.txt"
    assert by_source["credentials.txt"].planner_supplied is False
    assert by_source["notes.md"].target_path == "organized/notes.md"
    assert by_source["notes.md"].planner_supplied is True


@pytest.mark.parametrize(
    ("mutation", "error_code"),
    [
        ("missing", "missing_file_ids"),
        ("duplicate", "duplicate_file_id"),
        ("unknown", "unknown_file_id"),
        ("protected", "protected_file_in_plan"),
        ("path_mismatch", "original_path_mismatch"),
        ("unknown_evidence", "unknown_evidence_id"),
    ],
)
def test_compiler_rejects_incomplete_or_unauthorized_entries(
    tmp_path: Path,
    mutation: str,
    error_code: str,
) -> None:
    scan = _scan(tmp_path)
    plan = _complete_plan(scan)
    entries = list(plan.entries)
    if mutation == "missing":
        entries.pop()
    elif mutation == "duplicate":
        entries.append(entries[0])
    elif mutation == "unknown":
        entries.append(
            FolderPlanEntry(
                file_id="f" * 64,
                original_path="invented.txt",
                proposed_target="organized/invented.txt",
                rationale="Invented entry must never be accepted.",
                evidence_ids=(next(iter(inventory_evidence_ids(scan.inventory))),),
            )
        )
    elif mutation == "protected":
        protected = next(item for item in scan.inventory.files if item.protected)
        entries.append(
            FolderPlanEntry(
                file_id=protected.file_id,
                original_path=protected.relative_path,
                proposed_target=protected.relative_path,
                rationale="GPT cannot control a protected member.",
                evidence_ids=(f"inventory:{protected.file_id}",),
            )
        )
    elif mutation == "path_mismatch":
        entries[0] = _replace_entry(entries[0], original_path="wrong-path.md")
    else:
        entries[0] = _replace_entry(
            entries[0],
            evidence_ids=("excerpt:unknown",),
        )

    candidate = _replace_plan(plan, entries=tuple(entries))

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == error_code


@pytest.mark.parametrize(
    ("mutation", "error_code"),
    [
        ({"source_commitment": "f" * 64}, "source_commitment_mismatch"),
        ({"request_fingerprint": "f" * 64}, "request_fingerprint_mismatch"),
        ({"evidence_fingerprint": "f" * 64}, "evidence_fingerprint_mismatch"),
        ({"exclusions": ("draft.txt",)}, "plan_exclusions_forbidden"),
    ],
)
def test_compiler_enforces_source_request_evidence_and_no_exclusion_bindings(
    tmp_path: Path,
    mutation: dict[str, object],
    error_code: str,
) -> None:
    scan = _scan(tmp_path)
    candidate = _replace_plan(_complete_plan(scan), **mutation)

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == error_code


@pytest.mark.parametrize(
    "result_folder_name",
    [
        "nested/result",
        "nested\\result",
        ".",
        "..",
        ".hidden",
        "trailing.",
        " leading",
        "CON",
        "bad?name",
        "cafe\u0301",
        "é" * 121,
    ],
)
def test_result_folder_name_is_exactly_one_safe_component(
    tmp_path: Path,
    result_folder_name: str,
) -> None:
    scan = _scan(tmp_path)
    candidate = _replace_plan(
        _complete_plan(scan),
        result_folder_name=result_folder_name,
    )

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_result_folder_name"


@pytest.mark.parametrize(
    "target",
    [
        "/absolute/notes.md",
        "bad\\notes.md",
        "bad//notes.md",
        "bad/../notes.md",
        "bad/notes.txt",
        "bad/CON.md",
        "bad/ notes.md",
        "bad?/notes.md",
        "cafe\u0301/notes.md",
        "bad\nname/notes.md",
        f"{'é' * 119}.md",
        f"{'é' * 100}/{'é' * 100}/{'é' * 100}/"
        f"{'é' * 100}/{'é' * 100}/{'é' * 100}/notes.md",
    ],
)
def test_target_profile_and_exact_suffix_are_enforced(
    tmp_path: Path,
    target: str,
) -> None:
    scan = _scan(tmp_path)
    candidate = _complete_plan(scan, targets={"notes.md": target})

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_target_path"


def test_multidot_suffix_case_and_extensionless_status_are_preserved(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    assert protected_suffix("archive.tar.GZ") == ".tar.GZ"
    assert protected_suffix("README") == ""

    wrong_multidot = _complete_plan(
        scan,
        targets={"archive.tar.GZ": "organized/archive.tar.gz"},
    )
    with pytest.raises(PlanCompilationError) as first:
        _compile(scan, wrong_multidot)
    assert first.value.code == "invalid_target_path"

    added_suffix = _complete_plan(
        scan,
        targets={"README": "organized/README.txt"},
    )
    with pytest.raises(PlanCompilationError) as second:
        _compile(scan, added_suffix)
    assert second.value.code == "invalid_target_path"


def test_file_targets_are_unique_under_casefold(tmp_path: Path) -> None:
    scan = _scan(tmp_path, collision_sources=True)
    candidate = _complete_plan(
        scan,
        targets={
            "notes.md": "A/item.md",
            "brief.md": "a/item.md",
        },
    )

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_target_tree"


def test_directory_prefix_spelling_is_consistent_under_casefold(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    candidate = _complete_plan(
        scan,
        targets={
            "notes.md": "Working/notes.md",
            "draft.txt": "working/draft.txt",
        },
    )

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_target_tree"


def test_file_cannot_also_be_a_required_directory(tmp_path: Path) -> None:
    scan = _scan(tmp_path)
    candidate = _complete_plan(
        scan,
        targets={
            "README": "documents",
            "notes.md": "documents/notes.md",
        },
    )

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_target_tree"


@pytest.mark.parametrize("target", ["empty", "empty/README"])
def test_fixed_empty_directory_cannot_become_a_file_or_gain_members(
    tmp_path: Path,
    target: str,
) -> None:
    scan = _scan(tmp_path)
    candidate = _complete_plan(scan, targets={"README": target})

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_target_tree"


def test_collision_with_injected_protected_target_is_rejected(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    candidate = _complete_plan(
        scan,
        targets={"draft.txt": "credentials.txt"},
    )

    with pytest.raises(PlanCompilationError) as raised:
        _compile(scan, candidate)
    assert raised.value.code == "invalid_target_tree"


def test_accepted_plan_contract_rejects_forged_authority_and_collisions(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path, collision_sources=True)
    accepted = _compile(scan, _complete_plan(scan))
    raw = accepted.model_dump(mode="python")
    protected_index = next(
        index for index, item in enumerate(raw["file_mappings"]) if item["protected"]
    )
    markdown_indexes = [
        index
        for index, item in enumerate(raw["file_mappings"])
        if not item["protected"] and item["original_path"].endswith(".md")
    ]
    eligible_index = markdown_indexes[0]

    moved_protected = list(raw["file_mappings"])
    moved_protected[protected_index] = {
        **moved_protected[protected_index],
        "target_path": "moved/secret.txt",
    }
    with pytest.raises(ValidationError, match="Protected file|Protected mappings"):
        FolderAcceptedPlan.model_validate(
            {**raw, "file_mappings": tuple(moved_protected)},
            strict=True,
        )

    injected_eligible = list(raw["file_mappings"])
    injected_eligible[eligible_index] = {
        **injected_eligible[eligible_index],
        "planner_supplied": False,
    }
    with pytest.raises(ValidationError, match="Eligible mappings"):
        FolderAcceptedPlan.model_validate(
            {**raw, "file_mappings": tuple(injected_eligible)},
            strict=True,
        )

    duplicated_target = list(raw["file_mappings"])
    other_index = markdown_indexes[1]
    first_target = duplicated_target[eligible_index]["target_path"]
    duplicated_target[other_index] = {
        **duplicated_target[other_index],
        "target_path": f"{first_target[:-3].swapcase()}.md",
    }
    with pytest.raises(ValidationError, match="Conflicting file target|not unique"):
        FolderAcceptedPlan.model_validate(
            {**raw, "file_mappings": tuple(duplicated_target)},
            strict=True,
        )


def test_planner_outcome_schema_is_discriminated_versioned_and_strict(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    plan = _complete_plan(scan)
    adapter = TypeAdapter(FolderPlannerOutcome)

    parsed = adapter.validate_python(
        {
            "schema_version": "folder-planner-outcome.v1",
            "kind": "plan",
            "plan": plan.model_dump(mode="python"),
        },
        strict=True,
    )

    assert isinstance(parsed, PlanOutcome)
    assert parsed.schema_version == "folder-planner-outcome.v1"
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        adapter.validate_python(
            {
                "schema_version": "folder-planner-outcome.v1",
                "kind": "blocked",
                "blocker_code": "unsupported_request",
                "message": "Unsupported.",
                "unexpected": True,
            },
            strict=True,
        )


def test_development_planner_respects_the_read_only_bounded_protocol(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    planner = DeterministicDevelopmentPlanner()
    evidence_fingerprint = initial_evidence_fingerprint(scan.inventory)

    assert isinstance(planner, FolderPlanner)
    outcome = asyncio.run(
        planner.plan(
            request=REQUEST,
            inventory=scan.inventory,
            evidence_fingerprint=evidence_fingerprint,
        )
    )

    assert isinstance(outcome, PlanOutcome)
    assert planner.invocation_count == 1
    assert outcome.plan.source_commitment == scan.inventory.source_commitment
    assert outcome.plan.request_fingerprint == request_fingerprint(REQUEST)
    assert outcome.plan.evidence_fingerprint == evidence_fingerprint
    assert {entry.file_id for entry in outcome.plan.entries} == {
        item.file_id for item in scan.inventory.files if not item.protected
    }
    assert all(
        entry.evidence_ids == (f"inventory:{entry.file_id}",)
        for entry in outcome.plan.entries
    )
    assert not {item.file_id for item in scan.inventory.files if item.protected} & {
        entry.file_id for entry in outcome.plan.entries
    }


def test_plan_contract_is_immutable_and_forbids_unexpected_authority(
    tmp_path: Path,
) -> None:
    scan = _scan(tmp_path)
    plan = _complete_plan(scan)

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        FolderPlan.model_validate(
            {
                **plan.model_dump(mode="python"),
                "absolute_output_path": "/tmp/result",
            },
            strict=True,
        )
    with pytest.raises(ValidationError, match="Instance is frozen"):
        plan.result_folder_name = "mutated"  # type: ignore[misc]
