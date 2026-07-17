"""Focused copy-only stage and proof transaction tests."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from name_atlas import staging as staging_module
from name_atlas.artifacts import ArtifactReadError, parse_path_map
from name_atlas.decisions import (
    HumanAction,
    HumanDecision,
    approve_family,
    edit_family,
    unresolved_family,
)
from name_atlas.domain import ContentRole
from name_atlas.package_import import import_package
from name_atlas.proposals import build_proposals
from name_atlas.staging import VERIFIED_CLAIM, StagingError, stage_package
from name_atlas.verification import BagItPackageValidator
from name_atlas.verification.staged_proof import verify_staged_artifacts


def _copy_hero(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    (source / "objects").mkdir(parents=True)
    (source / "manualNormalization" / "access").mkdir(parents=True)
    (source / "manualNormalization" / "preservation").mkdir(parents=True)
    (source / "metadata").mkdir()
    (source / "objects" / "campaña-poster.svg").write_text("original", encoding="utf-8")
    (source / "manualNormalization" / "access" / "campaña-access.svg").write_text(
        "access", encoding="utf-8"
    )
    (
        source / "manualNormalization" / "preservation" / "campaña-preservation.svg"
    ).write_text("preservation", encoding="utf-8")
    (source / "metadata" / "metadata.csv").write_text(
        "filename,dc.identifier,dc.title\n"
        "objects/campaña-poster.svg,NA-0001,Campaña poster\n",
        encoding="utf-8",
    )
    (source / "normalization.csv").write_text(
        "objects/campaña-poster.svg,"
        "manualNormalization/access/campaña-access.svg,"
        "manualNormalization/preservation/campaña-preservation.svg\n",
        encoding="utf-8",
    )
    return source


def _read_tree(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def test_resolved_hero_stages_copy_only_with_complete_proof(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    before = _read_tree(source)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )

    result = stage_package(
        package,
        (decision,),
        output_root=tmp_path / "output",
        package_validator=BagItPackageValidator(),
    )

    assert _read_tree(source) == before
    assert result.stage_root.is_dir()
    assert BagItPackageValidator().validate(result.stage_root).valid is True
    assert result.artifacts.report.claim == VERIFIED_CLAIM
    assert result.artifacts.report.source_unchanged is True
    assert result.artifacts.report.map_row_count == 3
    assert all(check.passed for check in result.artifacts.report.checks)
    assert result.artifacts.report.bagit_validation.valid is True
    checks = {check.check_id: check.passed for check in result.artifacts.report.checks}
    assert checks["control_file_semantics_preserved"] is True
    assert checks["declared_references_resolve"] is True
    assert checks["forward_reverse_inverse"] is True
    assert checks["reverse_dry_run"] is True

    forward = result.artifacts.forward_map
    assert {row.role for row in forward} == {
        ContentRole.ORIGINAL,
        ContentRole.ACCESS,
        ContentRole.PRESERVATION,
    }
    for row in forward:
        assert (result.stage_root / "data" / row.target_path).read_bytes() == (
            source / row.source_path
        ).read_bytes()

    metadata_path = result.stage_root / "data" / "metadata" / "metadata.csv"
    with metadata_path.open(newline="", encoding="utf-8") as stream:
        metadata_rows = list(csv.DictReader(stream))
    assert (
        metadata_rows[0]["filename"] == decision.resolved_targets[ContentRole.ORIGINAL]
    )
    assert metadata_rows[0]["dc.title"] == "Campaña poster"

    control_proofs = {
        proof.logical_path: proof for proof in result.artifacts.report.control_files
    }
    metadata_proof = control_proofs["metadata/metadata.csv"]
    assert metadata_proof.rewritten_fields == ("row:2:filename",)
    assert metadata_proof.non_path_fields_unchanged is True
    assert (
        metadata_proof.staged_sha256
        == hashlib.sha256(metadata_path.read_bytes()).hexdigest()
    )
    normalization_proof = control_proofs["normalization.csv"]
    assert normalization_proof.rewritten_fields == (
        "row:1:original",
        "row:1:access",
        "row:1:preservation",
    )
    assert normalization_proof.non_path_fields_unchanged is True

    report_path = result.stage_root / "name-atlas" / "verification_report.json"
    assert json.loads(report_path.read_text(encoding="utf-8")) == (
        result.artifacts.report.model_dump(mode="json")
    )


def test_unresolved_family_blocks_before_output_creation(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    output = tmp_path / "output"

    with pytest.raises(StagingError, match="no complete resolved target"):
        stage_package(
            package,
            (unresolved_family(package.families[0].family_id),),
            output_root=output,
            package_validator=BagItPackageValidator(),
        )

    assert not output.exists()


def test_changed_source_blocks_before_copy(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )
    payload = source / "objects" / "campaña-poster.svg"
    payload.write_text(payload.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(StagingError, match="changed after the initial snapshot"):
        stage_package(
            package,
            (decision,),
            output_root=tmp_path / "output",
            package_validator=BagItPackageValidator(),
        )


def test_copy_failure_preserves_blocked_report_without_promotion(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _copy_hero(tmp_path)
    before = _read_tree(source)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )
    output = tmp_path / "output"

    def fail_copy(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise StagingError("Injected copy failure.")

    monkeypatch.setattr(staging_module, "_copy_content_member", fail_copy)

    with pytest.raises(StagingError, match="Injected copy failure"):
        stage_package(
            package,
            (decision,),
            output_root=output,
            package_validator=BagItPackageValidator(),
        )

    pending = tuple(output.glob(".*.pending"))
    assert len(pending) == 1
    assert not any(
        path.is_dir() and not path.name.startswith(".") for path in output.iterdir()
    )
    report = json.loads(
        (pending[0] / "name-atlas" / "verification_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "blocked"
    assert report["claim"] is None
    assert report["source_unchanged"] is None
    assert report["checks"][0]["passed"] is False
    assert "copy_content_objects" in report["blockers"][0]
    assert _read_tree(source) == before


def test_output_inside_source_is_rejected_without_mutation(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )
    before = _read_tree(source)

    with pytest.raises(StagingError, match="outside the immutable source"):
        stage_package(
            package,
            (decision,),
            output_root=source / "staging",
            package_validator=BagItPackageValidator(),
        )

    assert _read_tree(source) == before
    assert not (source / "staging").exists()


def test_crafted_escaping_resolved_target_blocks_before_output(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )
    targets = dict(decision.resolved_targets)
    targets[ContentRole.ORIGINAL] = "../../outside.svg"
    crafted = HumanDecision(
        family_id=decision.family_id,
        action=decision.action,
        human_input=None,
        resolved_targets=targets,
    )
    output = tmp_path / "output"

    with pytest.raises(StagingError, match="authority record"):
        stage_package(
            package,
            (crafted,),
            output_root=output,
            package_validator=BagItPackageValidator(),
        )

    assert not output.exists()
    assert not (tmp_path / "outside.svg").exists()


def test_crafted_decision_cannot_mislabel_edited_target_as_approved(
    tmp_path: Path,
) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    decision = approve_family(
        package.families[0],
        build_proposals(package.families),
        semantic_card_available=True,
    )
    targets = dict(decision.resolved_targets)
    targets[ContentRole.ORIGINAL] = "objects/NA-0001__never-proposed__original.svg"
    crafted = HumanDecision(
        family_id=decision.family_id,
        action=HumanAction.APPROVED,
        human_input=None,
        resolved_targets=targets,
    )

    with pytest.raises(StagingError, match="approved authority record"):
        stage_package(
            package,
            (crafted,),
            output_root=tmp_path / "output",
            package_validator=BagItPackageValidator(),
        )


def test_crafted_edited_decision_must_match_its_exact_human_input(
    tmp_path: Path,
) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    proposals = build_proposals(package.families)
    valid_edit = edit_family(
        package.families[0],
        proposals,
        descriptor="campaign-reviewed",
        semantic_card_available=True,
    )
    crafted = valid_edit.model_copy(update={"human_input": "different-descriptor"})

    with pytest.raises(StagingError, match="edited authority record"):
        stage_package(
            package,
            (crafted,),
            output_root=tmp_path / "output",
            package_validator=BagItPackageValidator(),
        )


def test_unaccounted_staged_payload_blocks_the_final_claim(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    decision = approve_family(
        package.families[0],
        build_proposals(package.families),
        semantic_card_available=True,
    )
    original_write_controls = staging_module._write_control_files

    def write_controls_with_extra(*args: object, **kwargs: object) -> None:
        original_write_controls(*args, **kwargs)
        pending_root = kwargs["pending_root"]
        assert isinstance(pending_root, Path)
        extra = pending_root / "data" / "objects" / "undeclared.bin"
        extra.write_bytes(b"not part of the transaction")

    monkeypatch.setattr(
        staging_module,
        "_write_control_files",
        write_controls_with_extra,
    )

    with pytest.raises(StagingError, match="deterministic proof checks failed"):
        stage_package(
            package,
            (decision,),
            output_root=tmp_path / "output",
            package_validator=BagItPackageValidator(),
        )

    pending = next((tmp_path / "output").glob(".*.pending"))
    report = json.loads(
        (pending / "name-atlas" / "verification_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "blocked"
    assert report["claim"] is None


def test_payload_changed_during_bag_creation_blocks_the_final_claim(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    decision = approve_family(
        package.families[0],
        build_proposals(package.families),
        semantic_card_available=True,
    )
    target = decision.resolved_targets[ContentRole.ORIGINAL]
    original_bag_write = staging_module.BagItWriter.write

    def tampering_bag_write(
        writer: object,
        bag_root: Path,
        *,
        bagging_date: object,
    ) -> None:
        (bag_root / "data" / target).write_bytes(b"changed after first proof")
        original_bag_write(writer, bag_root, bagging_date=bagging_date)  # type: ignore[arg-type]

    monkeypatch.setattr(staging_module.BagItWriter, "write", tampering_bag_write)

    with pytest.raises(StagingError, match="Final deterministic"):
        stage_package(
            package,
            (decision,),
            output_root=tmp_path / "output",
            package_validator=BagItPackageValidator(),
        )

    pending = next((tmp_path / "output").glob(".*.pending"))
    report = json.loads(
        (pending / "name-atlas" / "verification_report.json").read_text(
            encoding="utf-8"
        )
    )
    assert report["status"] == "blocked"
    assert report["claim"] is None


def test_actual_control_file_tampering_fails_semantic_proof(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )
    result = stage_package(
        package,
        (decision,),
        output_root=tmp_path / "output",
        package_validator=BagItPackageValidator(),
    )
    metadata_path = result.stage_root / "data" / "metadata" / "metadata.csv"
    metadata_path.write_text(
        metadata_path.read_text(encoding="utf-8").replace(
            "Campaña poster",
            "Tampered title",
        ),
        encoding="utf-8",
    )

    proof = verify_staged_artifacts(
        package,
        result.artifacts.forward_map,
        {decision.family_id: decision},
        pending_root=result.stage_root,
    )
    checks = {check.check_id: check.passed for check in proof.checks}

    assert checks["control_file_semantics_preserved"] is False
    assert checks["declared_references_resolve"] is True
    assert checks["reverse_dry_run"] is True
    metadata_proof = next(
        item
        for item in proof.control_files
        if item.logical_path == "metadata/metadata.csv"
    )
    assert metadata_proof.non_path_fields_unchanged is False
    assert (
        metadata_proof.staged_sha256
        == hashlib.sha256(metadata_path.read_bytes()).hexdigest()
    )


def test_actual_map_and_reference_tampering_fails_reverse_proof(tmp_path: Path) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    proposals = build_proposals(package.families)
    decision = approve_family(
        package.families[0],
        proposals,
        semantic_card_available=True,
    )
    result = stage_package(
        package,
        (decision,),
        output_root=tmp_path / "output",
        package_validator=BagItPackageValidator(),
    )
    metadata_path = result.stage_root / "data" / "metadata" / "metadata.csv"
    with metadata_path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.reader(stream, strict=True))
    rows[1][0] = decision.resolved_targets[ContentRole.ACCESS]
    with metadata_path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, lineterminator="\n").writerows(rows)

    reverse_path = result.stage_root / "name-atlas" / "reverse_path_map.csv"
    with reverse_path.open(newline="", encoding="utf-8") as stream:
        reverse_rows = list(csv.reader(stream, strict=True))
    reverse_rows[1][4] = "objects/not-the-recorded-source.svg"
    with reverse_path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream, lineterminator="\n").writerows(reverse_rows)
    proof = verify_staged_artifacts(
        package,
        result.artifacts.forward_map,
        {decision.family_id: decision},
        pending_root=result.stage_root,
    )
    checks = {check.check_id: check.passed for check in proof.checks}

    assert checks["control_file_semantics_preserved"] is False
    assert checks["declared_references_resolve"] is True
    assert checks["forward_reverse_inverse"] is False
    assert checks["reverse_dry_run"] is False


def test_source_snapshot_and_decision_ledger_are_read_back_exactly(
    tmp_path: Path,
) -> None:
    source = _copy_hero(tmp_path)
    package = import_package(source)
    decision = approve_family(
        package.families[0],
        build_proposals(package.families),
        semantic_card_available=True,
    )
    result = stage_package(
        package,
        (decision,),
        output_root=tmp_path / "output",
        package_validator=BagItPackageValidator(),
    )
    ledger_path = result.stage_root / "name-atlas" / "decision_ledger.json"
    ledger_path.write_text(
        '{"schema_version":"decision-ledger.v1","decisions":[]}',
        encoding="utf-8",
    )

    proof = verify_staged_artifacts(
        package,
        result.artifacts.forward_map,
        {decision.family_id: decision},
        pending_root=result.stage_root,
    )
    checks = {check.check_id: check.passed for check in proof.checks}

    assert checks["state_artifacts_exact"] is False


def test_path_map_parser_rejects_a_changed_schema() -> None:
    malformed = (
        "family_id,canonical_identifier,role,unexpected_source,target_path,size,"
        "sha256\n"
        f"{'a' * 64},NA-0001,original,objects/source.svg,objects/target.svg,1,"
        f"{'b' * 64}\n"
    ).encode()

    with pytest.raises(ArtifactReadError, match="invalid schema header"):
        parse_path_map(malformed, reverse=False)
