"""Acceptance checks for the single tiny unresolved-Meaning fixture."""

from __future__ import annotations

from pathlib import Path

import pytest

from name_atlas.decisions import unresolved_family
from name_atlas.package_import import import_package
from name_atlas.proposals import RiskCategory, build_proposals
from name_atlas.staging import StagingError, stage_package
from name_atlas.verification import BagItPackageValidator

NEGATIVE_ROOT = (
    Path(__file__).parents[1] / "sample_data" / "negative_unresolved_meaning"
)


def test_negative_fixture_is_valid_and_flags_one_meaning_risk() -> None:
    package = import_package(NEGATIVE_ROOT)
    proposals = build_proposals(package.families)

    assert len(package.snapshot.members) == 2
    assert len(package.families) == 1
    assert len(package.content_members) == 1
    assert package.normalization_present is False
    assert package.families[0].canonical_identifier == "NEG-0001"
    assert len(proposals) == 1
    assert proposals[0].proposed_relative_path == (
        "objects/NEG-0001__campana__original.svg"
    )
    assert any(
        signal.category is RiskCategory.MEANING for signal in proposals[0].risk_signals
    )


def test_unresolved_meaning_fixture_blocks_whole_package_export(
    tmp_path: Path,
) -> None:
    package = import_package(NEGATIVE_ROOT)
    family = package.families[0]
    output_root = tmp_path / "stages"

    with pytest.raises(StagingError, match="no complete resolved target"):
        stage_package(
            package,
            (unresolved_family(family.family_id),),
            output_root=output_root,
            package_validator=BagItPackageValidator(),
        )

    assert not output_root.exists()
