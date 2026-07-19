"""Adversarial checks for the independent Connected Change verifier."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from connected_change_fixtures import make_connected_change_fixture

from name_atlas.folder_refactor.connected_change.descriptors import (
    create_connected_change_file,
    parse_connected_change_file,
)
from name_atlas.folder_refactor.connected_change.proof import (
    render_connected_proof_html,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_MATCH_REPORT_PATH,
    CONNECTED_CHANGE_PATH,
    EXECUTION_ORIGIN_PATH,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptCoreV2,
    FolderReceiptEnvelopeV2,
)
from name_atlas.folder_refactor.connected_change.service import (
    apply_connected_change,
    create_connected_change_origin,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.contracts import FolderVerificationReport
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    EVIDENCE_LEDGER_PATH,
    PROOF_AND_RESTORE_HTML_PATH,
    VERIFICATION_REPORT_PATH,
    canonical_portable_json_bytes,
    parse_portable_model,
    read_regular_bytes,
    regular_file_measurement,
)
from name_atlas.folder_refactor.receipt_contracts import FolderArtifactCommitment
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.verification.bagit_validator import BagItPackageValidator


def test_portable_proof_is_responsive_and_wraps_long_identifiers() -> None:
    payload = render_connected_proof_html("a" * 64, "b" * 64).decode()

    assert 'name="viewport"' in payload
    assert "width=device-width,initial-scale=1" in payload
    assert "box-sizing:border-box" in payload
    assert "overflow-wrap:anywhere" in payload
    assert "word-break:break-word" in payload
    assert f"<code>{'a' * 64}</code>" in payload
    assert f"<code>{'b' * 64}</code>" in payload


def test_role_artifacts_and_optional_source_are_independently_checked(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    receiver = apply_connected_change(
        change_file_path=origin.change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
    )

    origin_paths = _receipt_artifact_paths(origin.folder_run.result_root)
    receiver_paths = _receipt_artifact_paths(receiver.folder_run.result_root)
    assert EVIDENCE_LEDGER_PATH in origin_paths
    assert CONNECTED_CHANGE_MATCH_REPORT_PATH not in origin_paths
    assert CONNECTED_CHANGE_MATCH_REPORT_PATH in receiver_paths
    assert EVIDENCE_LEDGER_PATH not in receiver_paths

    matching = verify_connected_result(
        origin.folder_run.result_root,
        source_root=fixture.sofia_root,
    )
    assert matching.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert matching.failed_check_ids == ()
    mismatching = verify_connected_result(
        origin.folder_run.result_root,
        source_root=fixture.martin_root,
    )
    assert mismatching.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert mismatching.failed_check_ids == ("supplied_source_mismatch",)


def test_verifier_rejects_retagged_human_proof_tamper(tmp_path: Path) -> None:
    result_root = _create_origin_result(tmp_path)
    (result_root / PROOF_AND_RESTORE_HTML_PATH).write_bytes(b"forged proof\n")
    BagItWriter().finalize_tagmanifest(result_root)

    assert BagItPackageValidator().validate(result_root).valid is True
    verification = verify_connected_result(result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("offline_proof_mismatch",)


def test_verifier_rejects_retagged_extra_portable_artifact(tmp_path: Path) -> None:
    result_root = _create_origin_result(tmp_path)
    (result_root / "name-atlas" / "uncommitted.json").write_bytes(b"{}")
    BagItWriter().finalize_tagmanifest(result_root)

    assert BagItPackageValidator().validate(result_root).valid is True
    verification = verify_connected_result(result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("artifact_set_mismatch",)


def test_verifier_rejects_self_consistent_false_verification_report(
    tmp_path: Path,
) -> None:
    result_root = _create_origin_result(tmp_path)
    report = parse_portable_model(
        read_regular_bytes(result_root, VERIFICATION_REPORT_PATH),
        FolderVerificationReport,
    )
    altered_report = report.model_copy(
        update={"path_change_count": report.path_change_count + 1}
    )
    (result_root / VERIFICATION_REPORT_PATH).write_bytes(
        canonical_portable_json_bytes(altered_report)
    )
    _reissue_receipt(result_root, verification_report=altered_report)

    assert BagItPackageValidator().validate(result_root).valid is True
    verification = verify_connected_result(result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("verification_report_mismatch",)


@pytest.mark.parametrize(
    "field_name",
    (
        "source_directory_count",
        "source_bytes",
        "path_change_count",
        "supported_link_count",
        "rewritten_link_count",
        "producer_bagit_messages",
    ),
)
def test_verifier_rejects_reissued_false_receipt_summary(
    tmp_path: Path,
    field_name: str,
) -> None:
    result_root = _create_origin_result(tmp_path)
    envelope = parse_portable_model(
        read_regular_bytes(result_root, CHANGE_RECEIPT_PATH),
        FolderReceiptEnvelopeV2,
    )
    current = getattr(envelope.receipt, field_name)
    if field_name == "producer_bagit_messages":
        replacement: Any = ("fabricated producer validation",)
    elif field_name in {
        "source_directory_count",
        "source_bytes",
        "supported_link_count",
    }:
        replacement = current + 1
    else:
        assert current > 0
        replacement = current - 1
    _reissue_receipt(
        result_root,
        receipt_updates={field_name: replacement},
        reissue_change_file=field_name != "supported_link_count",
    )

    assert BagItPackageValidator().validate(result_root).valid is True
    verification = verify_connected_result(result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("receipt_summary_mismatch",)


def test_verifier_requires_canonical_portable_json(tmp_path: Path) -> None:
    result_root = _create_origin_result(tmp_path)
    origin_path = result_root / EXECUTION_ORIGIN_PATH
    origin_path.write_bytes(
        json.dumps(
            json.loads(origin_path.read_bytes()),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        ).encode()
    )
    _reissue_receipt(result_root)

    assert BagItPackageValidator().validate(result_root).valid is True
    verification = verify_connected_result(result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("portable_artifact_schema_invalid",)


def _create_origin_result(tmp_path: Path) -> Path:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "origin-output"
    output.mkdir()
    return create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    ).folder_run.result_root


def _receipt_artifact_paths(result_root: Path) -> set[str]:
    envelope = parse_portable_model(
        read_regular_bytes(result_root, CHANGE_RECEIPT_PATH),
        FolderReceiptEnvelopeV2,
    )
    return {item.path for item in envelope.receipt.artifact_commitments}


def _reissue_receipt(
    result_root: Path,
    *,
    verification_report: FolderVerificationReport | None = None,
    receipt_updates: dict[str, Any] | None = None,
    reissue_change_file: bool = True,
) -> None:
    envelope = parse_portable_model(
        read_regular_bytes(result_root, CHANGE_RECEIPT_PATH),
        FolderReceiptEnvelopeV2,
    )
    commitments = tuple(
        (
            FolderArtifactCommitment(
                path=commitment.path,
                size=regular_file_measurement(result_root, commitment.path)[0],
                sha256=regular_file_measurement(result_root, commitment.path)[1],
            )
            if commitment.path in {EXECUTION_ORIGIN_PATH, VERIFICATION_REPORT_PATH}
            else commitment
        )
        for commitment in envelope.receipt.artifact_commitments
    )
    update = {
        **envelope.receipt.model_dump(
            mode="python",
            exclude={
                "artifact_commitments",
                "verification_report_fingerprint",
            },
        ),
        "artifact_commitments": commitments,
        "verification_report_fingerprint": (
            envelope.receipt.verification_report_fingerprint
            if verification_report is None
            else canonical_sha256(verification_report)
        ),
    }
    if any(item.path == EXECUTION_ORIGIN_PATH for item in commitments):
        origin_payload = json.loads(
            read_regular_bytes(result_root, EXECUTION_ORIGIN_PATH)
        )
        update["execution_origin_fingerprint"] = canonical_sha256(origin_payload)
    update.update(receipt_updates or {})
    altered_core = FolderReceiptCoreV2(**update)
    altered_envelope = FolderReceiptEnvelopeV2(
        receipt=altered_core,
        receipt_fingerprint=canonical_sha256(altered_core),
    )
    (result_root / CHANGE_RECEIPT_PATH).write_bytes(
        canonical_portable_json_bytes(altered_envelope)
    )
    if reissue_change_file:
        current_change_file = parse_connected_change_file(
            read_regular_bytes(result_root, CONNECTED_CHANGE_PATH)
        )
        altered_change_file = create_connected_change_file(
            current_change_file.core,
            originating_receipt=altered_envelope,
        )
        (result_root / CONNECTED_CHANGE_PATH).write_bytes(
            canonical_portable_json_bytes(altered_change_file)
        )
    (result_root / PROOF_AND_RESTORE_HTML_PATH).write_bytes(
        render_connected_proof_html(
            altered_envelope.receipt_fingerprint,
            altered_core.organized_tree.commitment,
        )
    )
    BagItWriter().finalize_tagmanifest(result_root)
