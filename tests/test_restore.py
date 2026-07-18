"""R5 bounded logical-restore transaction and CLI acceptance."""

from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from zoneinfo import ZoneInfo

import pytest
from pydantic import ValidationError

from name_atlas import cli
from name_atlas import restore as restore_module
from name_atlas.decision_cards import RecordedReplayDecisionCardProvider
from name_atlas.package_import import PackageImportError, import_package
from name_atlas.receipts import (
    CHANGE_RECEIPT_PATH,
    PORTABLE_SOURCE_SNAPSHOT_PATH,
    PortableSourceSnapshot,
    portable_snapshot_from_source,
    read_regular_bytes,
)
from name_atlas.receiver_verifier import (
    ReceiptVerificationStatus,
    verify_receipt,
)
from name_atlas.restore import RestoreError, RestoreReport, restore_receipt
from name_atlas.verification import BagItPackageValidator
from name_atlas.workflow import WorkflowSession

PROJECT_ROOT = Path(__file__).parents[1]
HERO_ROOT = PROJECT_ROOT / "sample_data" / "hero"
REPLAY_RECORD = (
    PROJECT_ROOT / "src" / "name_atlas" / "recordings" / "hero_decision_card.json"
)
oslo_tz = ZoneInfo("Europe/Oslo")


def _tree_state(root: Path) -> dict[str, tuple[str, bytes | str | None]]:
    """Capture path identity and bytes without following symbolic links."""

    if not root.exists():
        return {}
    state: dict[str, tuple[str, bytes | str | None]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            state[relative] = ("symlink", path.readlink().as_posix())
        elif path.is_dir():
            state[relative] = ("directory", None)
        else:
            state[relative] = ("file", path.read_bytes())
    return state


def _finalized_hero_handoff(tmp_path: Path) -> tuple[Path, Path]:
    """Create one real finalized hero handoff through the public workflow."""

    source = tmp_path / "sender" / "source"
    source.parent.mkdir()
    shutil.copytree(HERO_ROOT, source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "sender" / "stages",
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=tmp_path / "sender" / "cases" / "hero.case.json",
        case_name="R5 logical restore",
    )
    try:
        meaning_family = next(
            family
            for family in workflow.package.families
            if family.canonical_identifier == "NA-0001"
        )
        collision_family = next(
            family
            for family in workflow.package.families
            if family.canonical_identifier == "CASE-010"
        )
        asyncio.run(workflow.generate_card(meaning_family.family_id))
        workflow.approve(meaning_family.family_id)
        workflow.approve_low_risk()
        workflow.edit(collision_family.family_id, "harbor-map-north")
        workflow.approve_low_risk()
        stage = workflow.stage()
        assert stage.receiver_verification is not None
        assert stage.receiver_verification.status is ReceiptVerificationStatus.VERIFIED
        return source, stage.stage_root
    finally:
        workflow.close()


def _finalized_single_original_handoff(tmp_path: Path) -> tuple[Path, Path]:
    """Finalize one strict package whose optional normalization file is absent."""

    source = tmp_path / "single-sender" / "source"
    (source / "objects").mkdir(parents=True)
    (source / "metadata").mkdir()
    (source / "objects" / "photo-one.txt").write_bytes(b"single payload\n")
    (source / "metadata" / "metadata.csv").write_text(
        "filename,dc.identifier,dc.title\n"
        "objects/photo-one.txt,SINGLE-001,Single original\n",
        encoding="utf-8",
    )
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "single-sender" / "stages",
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=tmp_path / "single-sender" / "cases" / "single.case.json",
        case_name="R5 package without normalization",
    )
    try:
        workflow.approve_low_risk()
        assert workflow.view_model()["export_ready"] is True
        stage = workflow.stage()
        assert stage.receiver_verification is not None
        assert stage.receiver_verification.status is ReceiptVerificationStatus.VERIFIED
        return source, stage.stage_root
    finally:
        workflow.close()


def _committed_snapshot(handoff: Path) -> PortableSourceSnapshot:
    return PortableSourceSnapshot.model_validate_json(
        read_regular_bytes(handoff, PORTABLE_SOURCE_SNAPSHOT_PATH)
    )


def _assert_no_failed_transaction_exposure(
    restore_parent: Path,
    before: dict[str, tuple[str, bytes | str | None]],
    destination: Path,
) -> None:
    assert not destination.exists()
    assert _tree_state(restore_parent) == before


def test_restore_reconstructs_complete_hero_and_returns_strict_external_report(
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    expected_snapshot = _committed_snapshot(handoff)
    destination = tmp_path / "receiver" / "restored-source"
    destination.parent.mkdir()

    report = restore_receipt(handoff, destination)
    receiver_result = verify_receipt(handoff)

    assert isinstance(report, RestoreReport)
    assert report.schema_version == "restore-report.v1"
    assert report.status == "restored"
    assert report.receipt_fingerprint == receiver_result.receipt_fingerprint
    assert report.restored_at.tzinfo == oslo_tz
    assert report.destination == destination.resolve()
    assert report.source_snapshot_commitment == expected_snapshot.commitment
    assert report.restored_member_count == len(expected_snapshot.members)
    assert report.restored_bytes == sum(
        member.size for member in expected_snapshot.members
    )
    assert report.restored_snapshot == expected_snapshot
    assert report.checks
    assert all(check.passed for check in report.checks)

    serialized = report.model_dump(mode="json", exclude_none=False)
    assert RestoreReport.model_validate_json(report.model_dump_json()) == report
    with pytest.raises(ValidationError):
        RestoreReport.model_validate_json(
            json.dumps({**serialized, "unexpected": True})
        )
    first_check = report.checks[0]
    with pytest.raises(ValidationError):
        type(first_check).model_validate_json(
            json.dumps({**first_check.model_dump(mode="json"), "unexpected": True})
        )

    restored_package = import_package(destination)
    actual_snapshot = portable_snapshot_from_source(restored_package.snapshot)
    assert actual_snapshot == expected_snapshot
    assert tuple(
        (member.relative_path, member.size, member.sha256)
        for member in actual_snapshot.members
    ) == tuple(
        (member.relative_path, member.size, member.sha256)
        for member in expected_snapshot.members
    )
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before
    assert not tuple(destination.parent.glob("*restore-report*"))
    assert not tuple(
        path
        for path in destination.parent.iterdir()
        if path != destination and "pending" in path.name
    )


def test_restore_supports_strict_package_without_optional_normalization(
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_single_original_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    expected_snapshot = _committed_snapshot(handoff)
    destination = tmp_path / "single-receiver" / "restored-source"
    destination.parent.mkdir()

    report = restore_receipt(handoff, destination)

    assert report.restored_snapshot == expected_snapshot
    assert report.restored_member_count == 2
    assert {member.relative_path for member in expected_snapshot.members} == {
        "metadata/metadata.csv",
        "objects/photo-one.txt",
    }
    assert not (source / "normalization.csv").exists()
    assert not (destination / "normalization.csv").exists()
    assert portable_snapshot_from_source(import_package(destination).snapshot) == (
        expected_snapshot
    )
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_invalid_receipt_is_rejected_before_restore_writes(tmp_path: Path) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    invalid = tmp_path / "receiver" / "invalid-handoff"
    invalid.parent.mkdir()
    shutil.copytree(handoff, invalid)
    (invalid / CHANGE_RECEIPT_PATH).write_text("{}\n", encoding="utf-8")
    assert verify_receipt(invalid).status is ReceiptVerificationStatus.BLOCKED
    source_before = _tree_state(source)
    handoff_before = _tree_state(invalid)
    restore_parent = tmp_path / "invalid-restore"
    restore_parent.mkdir()
    restore_before = _tree_state(restore_parent)
    destination = restore_parent / "source"

    with pytest.raises(RestoreError):
        restore_receipt(invalid, destination)

    _assert_no_failed_transaction_exposure(
        restore_parent,
        restore_before,
        destination,
    )
    assert _tree_state(source) == source_before
    assert _tree_state(invalid) == handoff_before


def test_existing_destination_is_refused_after_verify_and_never_replaced(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "existing-restore"
    destination = restore_parent / "source"
    destination.mkdir(parents=True)
    (destination / "sentinel.txt").write_text("do not replace\n", encoding="utf-8")
    before = _tree_state(restore_parent)
    verification_calls = 0
    real_verify = restore_module.verify_receipt

    def verified_first(*args: Any, **kwargs: Any) -> Any:
        nonlocal verification_calls
        verification_calls += 1
        return real_verify(*args, **kwargs)

    monkeypatch.setattr(restore_module, "verify_receipt", verified_first)

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    assert verification_calls == 1
    assert _tree_state(restore_parent) == before
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


@pytest.mark.parametrize("destination_kind", ("file", "dangling_symlink"))
def test_existing_non_directory_destination_is_refused_without_replacement(
    destination_kind: str,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / f"existing-{destination_kind}"
    restore_parent.mkdir()
    destination = restore_parent / "source"
    if destination_kind == "file":
        destination.write_bytes(b"do not replace\n")
    else:
        destination.symlink_to("missing-target", target_is_directory=True)
    before = _tree_state(restore_parent)

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    assert destination.is_symlink() or destination.is_file()
    assert _tree_state(restore_parent) == before
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_destination_inside_received_bag_is_refused_without_creating_anything(
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    destination = handoff / "restored-source"

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    assert not destination.exists()
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_copy_failure_never_promotes_or_leaves_pending_tree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "copy-failure"
    restore_parent.mkdir()
    before = _tree_state(restore_parent)
    destination = restore_parent / "source"

    def fail_copy(*args: Any, **kwargs: Any) -> None:
        del args, kwargs
        raise OSError("injected restore copy failure")

    monkeypatch.setattr(restore_module, "_copy_verified_member", fail_copy)

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    _assert_no_failed_transaction_exposure(restore_parent, before, destination)
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_strict_reimport_failure_never_promotes_or_leaves_pending_tree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "import-failure"
    restore_parent.mkdir()
    before = _tree_state(restore_parent)
    destination = restore_parent / "source"

    def fail_import(_root: Path) -> Any:
        raise PackageImportError("injected strict reimport failure")

    monkeypatch.setattr(restore_module, "import_package", fail_import)

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    _assert_no_failed_transaction_exposure(restore_parent, before, destination)
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_snapshot_proof_failure_never_promotes_or_leaves_pending_tree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "proof-failure"
    restore_parent.mkdir()
    before = _tree_state(restore_parent)
    destination = restore_parent / "source"
    real_import = restore_module.import_package

    def mismatched_import(root: Path) -> Any:
        package = real_import(root)
        mismatched_snapshot = package.snapshot.model_copy(
            update={"commitment": "0" * 64}
        )
        return package.model_copy(update={"snapshot": mismatched_snapshot})

    monkeypatch.setattr(restore_module, "import_package", mismatched_import)

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    _assert_no_failed_transaction_exposure(restore_parent, before, destination)
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_promotion_failure_never_exposes_destination_or_pending_tree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "promotion-failure"
    restore_parent.mkdir()
    before = _tree_state(restore_parent)
    destination = restore_parent / "source"

    def fail_promotion(_pending: Path, _destination: Path) -> None:
        raise OSError("injected no-replace promotion failure")

    monkeypatch.setattr(
        restore_module,
        "promote_directory_no_replace",
        fail_promotion,
    )

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    _assert_no_failed_transaction_exposure(restore_parent, before, destination)
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_handoff_mutation_during_restore_blocks_before_promotion_and_cleans_pending(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    bag_info = handoff / "bag-info.txt"
    bag_info_before = bag_info.read_bytes()
    restore_parent = tmp_path / "handoff-mutation"
    restore_parent.mkdir()
    restore_before = _tree_state(restore_parent)
    destination = restore_parent / "source"
    real_verify = restore_module.verify_receipt
    verification_calls = 0
    mutation_injected = False
    promotion_called = False

    def verify_then_mutate(*args: Any, **kwargs: Any) -> Any:
        nonlocal mutation_injected, verification_calls
        verification_calls += 1
        if verification_calls == 2:
            bag_info.write_bytes(bag_info_before + b"Injected concurrent change.\n")
            mutation_injected = True
        return real_verify(*args, **kwargs)

    def record_promotion(_pending: Path, _destination: Path) -> None:
        nonlocal promotion_called
        promotion_called = True

    monkeypatch.setattr(restore_module, "verify_receipt", verify_then_mutate)
    monkeypatch.setattr(
        restore_module,
        "promote_directory_no_replace",
        record_promotion,
    )

    try:
        with pytest.raises(RestoreError):
            restore_receipt(handoff, destination)

        assert verification_calls == 2
        assert mutation_injected is True
        assert promotion_called is False
        _assert_no_failed_transaction_exposure(
            restore_parent,
            restore_before,
            destination,
        )
        assert _tree_state(source) == source_before
        assert _tree_state(handoff) != handoff_before
    finally:
        bag_info.write_bytes(bag_info_before)

    assert _tree_state(handoff) == handoff_before


def test_pending_intermediate_symlink_cannot_escape_restore_root(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "pending-symlink"
    restore_parent.mkdir()
    restore_before = _tree_state(restore_parent)
    destination = restore_parent / "source"
    external = tmp_path / "external-write-target"
    external.mkdir()
    (external / "sentinel.txt").write_bytes(b"external sentinel\n")
    external_before = _tree_state(external)
    real_create = restore_module._create_pending_root

    def create_with_intermediate_symlink(final_root: Path) -> Any:
        pending = real_create(final_root)
        (pending.path / "objects").symlink_to(external, target_is_directory=True)
        return pending

    monkeypatch.setattr(
        restore_module,
        "_create_pending_root",
        create_with_intermediate_symlink,
    )

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    _assert_no_failed_transaction_exposure(
        restore_parent,
        restore_before,
        destination,
    )
    assert _tree_state(external) == external_before
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_replaced_pending_path_preserves_replacement_and_cleans_owned_tree(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "pending-replacement"
    restore_parent.mkdir()
    destination = restore_parent / "source"
    replacement_sentinel: Path | None = None
    moved_owned_pending: Path | None = None

    def replace_pending_then_fail(**kwargs: Any) -> None:
        nonlocal moved_owned_pending, replacement_sentinel
        pending = kwargs["destination"]
        pending_root = pending.path
        moved_owned_pending = pending_root.with_name(
            f"{pending_root.name.removesuffix('.pending')}-moved.pending"
        )
        pending_root.rename(moved_owned_pending)
        pending_root.mkdir()
        replacement_sentinel = pending_root / "replacement-sentinel.txt"
        replacement_sentinel.write_bytes(b"attacker replacement; do not delete\n")
        raise RestoreError("injected failure after pending replacement")

    monkeypatch.setattr(
        restore_module,
        "_copy_verified_member",
        replace_pending_then_fail,
    )

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    assert replacement_sentinel is not None
    assert replacement_sentinel.read_bytes() == (
        b"attacker replacement; do not delete\n"
    )
    assert moved_owned_pending is not None
    assert not moved_owned_pending.exists()
    assert not destination.exists()
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_destination_race_preserves_new_destination_and_cleans_owned_pending(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / "destination-race"
    restore_parent.mkdir()
    destination = restore_parent / "source"
    real_promote = restore_module.promote_directory_no_replace
    destination_bytes = b"racing destination; do not replace\n"

    def create_destination_then_promote(pending: Path, final: Path) -> None:
        final.mkdir()
        (final / "sentinel.txt").write_bytes(destination_bytes)
        real_promote(pending, final)

    monkeypatch.setattr(
        restore_module,
        "promote_directory_no_replace",
        create_destination_then_promote,
    )

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    assert _tree_state(destination) == {
        "sentinel.txt": ("file", destination_bytes),
    }
    assert not tuple(
        path
        for path in restore_parent.iterdir()
        if path != destination and path.name.endswith(".pending")
    )
    assert _tree_state(source) == source_before
    assert _tree_state(handoff) == handoff_before


def test_handoff_removed_after_first_verification_raises_restore_error_without_writes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    restore_parent = tmp_path / "removed-handoff-api"
    restore_parent.mkdir()
    restore_before = _tree_state(restore_parent)
    destination = restore_parent / "source"
    real_verify = restore_module.verify_receipt
    verification_calls = 0

    def verify_then_remove(*args: Any, **kwargs: Any) -> Any:
        nonlocal verification_calls
        result = real_verify(*args, **kwargs)
        verification_calls += 1
        if verification_calls == 1:
            shutil.rmtree(handoff)
        return result

    monkeypatch.setattr(restore_module, "verify_receipt", verify_then_remove)

    with pytest.raises(RestoreError):
        restore_receipt(handoff, destination)

    assert verification_calls == 1
    _assert_no_failed_transaction_exposure(
        restore_parent,
        restore_before,
        destination,
    )
    assert _tree_state(source) == source_before


def test_cli_reports_blocked_when_handoff_disappears_after_first_verification(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    restore_parent = tmp_path / "removed-handoff-cli"
    restore_parent.mkdir()
    restore_before = _tree_state(restore_parent)
    destination = restore_parent / "source"
    real_verify = restore_module.verify_receipt
    verification_calls = 0

    def verify_then_remove(*args: Any, **kwargs: Any) -> Any:
        nonlocal verification_calls
        result = real_verify(*args, **kwargs)
        verification_calls += 1
        if verification_calls == 1:
            shutil.rmtree(handoff)
        return result

    monkeypatch.setattr(restore_module, "verify_receipt", verify_then_remove)

    exit_code = cli.run(
        ["restore-receipt", str(handoff), str(destination)],
        environ={},
    )
    output = capsys.readouterr()

    assert exit_code == 1
    assert "BLOCKED" in f"{output.out}{output.err}"
    assert "Traceback" not in f"{output.out}{output.err}"
    assert verification_calls == 1
    _assert_no_failed_transaction_exposure(
        restore_parent,
        restore_before,
        destination,
    )
    assert _tree_state(source) == source_before


@pytest.mark.parametrize("injection_kind", ("ordinary_tag", "empty_directory"))
def test_handoff_member_injected_after_second_verification_blocks_before_promotion(
    injection_kind: str,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    source, handoff = _finalized_hero_handoff(tmp_path)
    source_before = _tree_state(source)
    handoff_before = _tree_state(handoff)
    restore_parent = tmp_path / f"final-handoff-{injection_kind}"
    restore_parent.mkdir()
    restore_before = _tree_state(restore_parent)
    destination = restore_parent / "source"
    real_verify = restore_module.verify_receipt
    verification_calls = 0
    injected_path: Path | None = None
    promotion_called = False

    def verify_then_inject(*args: Any, **kwargs: Any) -> Any:
        nonlocal injected_path, verification_calls
        result = real_verify(*args, **kwargs)
        verification_calls += 1
        if verification_calls == 2:
            if injection_kind == "ordinary_tag":
                injected_path = handoff / "receiver-injected-tag.txt"
                injected_path.write_bytes(b"injected after receiver verification\n")
            else:
                injected_path = handoff / "receiver-injected-empty-directory"
                injected_path.mkdir()
        return result

    def record_promotion(_pending: Path, _destination: Path) -> None:
        nonlocal promotion_called
        promotion_called = True

    monkeypatch.setattr(restore_module, "verify_receipt", verify_then_inject)
    monkeypatch.setattr(
        restore_module,
        "promote_directory_no_replace",
        record_promotion,
    )

    try:
        with pytest.raises(RestoreError):
            restore_receipt(handoff, destination)

        assert verification_calls == 2
        assert injected_path is not None
        assert promotion_called is False
        _assert_no_failed_transaction_exposure(
            restore_parent,
            restore_before,
            destination,
        )
        assert _tree_state(source) == source_before
        assert _tree_state(handoff) != handoff_before
    finally:
        if injected_path is not None and injected_path.is_dir():
            injected_path.rmdir()
        elif injected_path is not None and injected_path.exists():
            injected_path.unlink()

    assert _tree_state(handoff) == handoff_before


def test_restore_cli_dispatches_before_demo_provider_and_prints_result(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    handoff = tmp_path / "received-bag"
    handoff.mkdir()
    destination = tmp_path / "restored-source"
    provider_initialized = False
    called: dict[str, Path] = {}

    def fail_if_provider_initializes(*args: Any, **kwargs: Any) -> None:
        nonlocal provider_initialized
        del args, kwargs
        provider_initialized = True

    def fake_restore(received_bag: Path, restore_destination: Path) -> Any:
        called["received_bag"] = received_bag
        called["destination"] = restore_destination
        return SimpleNamespace(
            receipt_fingerprint="a" * 64,
            destination=restore_destination.resolve(),
        )

    monkeypatch.setattr(
        cli.LiveDecisionCardProvider,
        "from_api_key",
        fail_if_provider_initializes,
    )
    monkeypatch.setattr(cli, "restore_receipt", fake_restore)

    exit_code = cli.run(
        ["restore-receipt", str(handoff), str(destination)],
        environ={},
    )

    assert exit_code == 0
    assert provider_initialized is False
    assert called == {
        "received_bag": handoff,
        "destination": destination,
    }
    assert capsys.readouterr().out == (f"RESTORED {'a' * 64} {destination.resolve()}\n")


def test_restore_cli_uses_distinct_input_and_transaction_exit_codes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    destination = tmp_path / "restored-source"
    missing = tmp_path / "missing-bag"

    input_exit = cli.run(
        ["restore-receipt", str(missing), str(destination)],
        environ={},
    )
    input_output = capsys.readouterr()

    candidate = tmp_path / "received-bag"
    candidate.mkdir()

    def fail_restore(_received_bag: Path, _destination: Path) -> Any:
        raise RestoreError("injected verified-transaction blocker")

    monkeypatch.setattr(cli, "restore_receipt", fail_restore)
    blocked_exit = cli.run(
        ["restore-receipt", str(candidate), str(destination)],
        environ={},
    )
    blocked_output = capsys.readouterr()

    assert input_exit == 2
    assert input_output.out == ""
    assert "input" in input_output.err.lower()
    assert blocked_exit == 1
    assert "BLOCKED" in f"{blocked_output.out}{blocked_output.err}"
