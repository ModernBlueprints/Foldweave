"""Complete public-service transaction and refusal matrix for the C0 gate."""

from __future__ import annotations

import builtins
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

import pytest
from connected_change_fixtures import (
    ConnectedChangeFixture,
    make_connected_change_fixture,
    make_symmetric_fixture,
    portable_tree,
    tree_state,
)

import name_atlas.folder_refactor.connected_change.service as connected_change_service
import name_atlas.folder_refactor.transaction as folder_transaction
from name_atlas.folder_refactor.connected_change.contracts import (
    CapsuleAppliedExecutionOrigin,
    ConnectedChangeError,
    ConnectedChangeMatchReport,
    GptPlannedExecutionOrigin,
    connected_change_match_report_fingerprint,
)
from name_atlas.folder_refactor.connected_change.descriptors import (
    create_connected_change_file,
    parse_connected_change_file,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    CONNECTED_CHANGE_MATCH_REPORT_PATH,
    EXECUTION_ORIGIN_PATH,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptCoreV2,
    FolderReceiptEnvelopeV2,
)
from name_atlas.folder_refactor.connected_change.reconstruction import (
    restore_connected_result,
)
from name_atlas.folder_refactor.connected_change.service import (
    apply_connected_change,
    create_connected_change_origin,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.markdown_contracts import (
    FolderReferenceGraph,
    MarkdownReference,
    reference_fingerprint,
)
from name_atlas.folder_refactor.portable_artifacts import (
    CHANGE_RECEIPT_PATH,
    canonical_portable_json_bytes,
    parse_portable_model,
    read_regular_bytes,
    regular_file_measurement,
)
from name_atlas.folder_refactor.receipt_contracts import FolderArtifactCommitment
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.verification.bagit_validator import BagItPackageValidator

_FORBIDDEN_RECEIVER_IMPORTS = (
    "name_atlas.decision_cards.budget",
    "name_atlas.decision_cards.providers",
    "name_atlas.folder_refactor.planner_provider",
)


def test_complete_c0_origin_receiver_convergence_and_reconstruction(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    sofia_output = tmp_path / "sofia-results"
    martin_output = tmp_path / "martin-results"
    sofia_output.mkdir()
    martin_output.mkdir()
    sofia_before = tree_state(fixture.sofia_root)
    martin_before = tree_state(fixture.martin_root)
    sofia_inventory = scan_folder(fixture.sofia_root).inventory
    martin_inventory = scan_folder(fixture.martin_root).inventory
    assert sofia_inventory.source_commitment != martin_inventory.source_commitment

    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=sofia_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    assert isinstance(origin.execution_origin, GptPlannedExecutionOrigin)
    assert origin.execution_origin.planner_kind == "deterministic_development"
    assert origin.execution_origin.provider_call_count == 0
    assert origin.execution_origin.api_used is False
    assert origin.execution_origin.external_network_used is False
    assert tree_state(fixture.sofia_root) == sofia_before
    change_file_before = _file_state(origin.change_file_path)
    change_bytes = origin.change_file_path.read_bytes()
    for source_file in sofia_inventory.files:
        assert (fixture.sofia_root / source_file.relative_path).read_bytes() not in (
            change_bytes
        )
    assert str(fixture.sofia_root).encode() not in change_bytes

    imported_before = _watched_imports()
    with monkeypatch.context() as guarded:
        guarded.setattr(builtins, "__import__", _guarded_receiver_import())
        receiver = apply_connected_change(
            change_file_path=origin.change_file_path,
            source_root=fixture.martin_root,
            output_parent=martin_output,
        )
    assert _watched_imports() == imported_before
    assert isinstance(receiver.execution_origin, CapsuleAppliedExecutionOrigin)
    assert receiver.execution_origin.provider_call_count == 0
    assert receiver.execution_origin.api_used is False
    assert receiver.execution_origin.external_network_used is False
    assert tree_state(fixture.martin_root) == martin_before
    assert _file_state(origin.change_file_path) == change_file_before
    assert receiver.change_file_path.read_bytes() == change_bytes

    origin_verification = verify_connected_result(origin.folder_run.result_root)
    receiver_verification = verify_connected_result(receiver.folder_run.result_root)
    assert origin_verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert receiver_verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert origin_verification.failed_check_ids == ()
    assert receiver_verification.failed_check_ids == ()
    assert origin.receipt_fingerprint != receiver.receipt_fingerprint
    assert origin_verification.receipt_fingerprint == origin.receipt_fingerprint
    assert receiver_verification.receipt_fingerprint == receiver.receipt_fingerprint
    assert (
        origin.organized_tree_commitment
        == receiver.organized_tree_commitment
        == origin_verification.organized_tree_commitment
        == receiver_verification.organized_tree_commitment
    )
    assert portable_tree(origin.folder_run.data_root) == portable_tree(
        receiver.folder_run.data_root
    )

    expected_client_note = (
        b"Approved item: [document](../deliverables/approved.txt#final)\r\n"
    )
    expected_research_note = (
        b"Research item: [document](../research/supporting.txt#draft)\r\n"
    )
    for data_root in (origin.folder_run.data_root, receiver.folder_run.data_root):
        assert (data_root / "notes/client-brief.md").read_bytes() == (
            expected_client_note
        )
        assert (data_root / "notes/research-log.md").read_bytes() == (
            expected_research_note
        )

    unrelated = tmp_path / "unrelated-location" / "received-result"
    unrelated.parent.mkdir()
    shutil.copytree(receiver.folder_run.result_root, unrelated)
    unrelated_verification = verify_connected_result(unrelated)
    assert unrelated_verification.status is ConnectedReceiptVerificationStatus.VERIFIED
    assert unrelated_verification.receipt_fingerprint == receiver.receipt_fingerprint

    from name_atlas.cli import run as run_cli

    assert run_cli(["verify-receipt", str(unrelated)], environ={}) == 0
    assert capsys.readouterr().out.strip() == (
        f"VERIFIED {receiver.receipt_fingerprint}"
    )
    assert (
        run_cli(
            [
                "verify-receipt",
                str(unrelated),
                "--source",
                str(fixture.martin_root),
            ],
            environ={},
        )
        == 0
    )
    assert capsys.readouterr().out.strip() == (
        f"VERIFIED {receiver.receipt_fingerprint}"
    )
    assert (
        run_cli(
            [
                "verify-receipt",
                str(unrelated),
                "--source",
                str(fixture.sofia_root),
            ],
            environ={},
        )
        == 1
    )
    assert capsys.readouterr().out.strip() == "BLOCKED supplied_source_mismatch"
    cli_restore_destination = (
        receiver.folder_run.result_root.parent / "martin-original-cli"
    )
    assert (
        run_cli(
            [
                "restore-receipt",
                str(receiver.folder_run.result_root),
                str(cli_restore_destination),
            ],
            environ={},
        )
        == 0
    )
    assert portable_tree(cli_restore_destination) == portable_tree(fixture.martin_root)
    assert capsys.readouterr().out.startswith(
        f"RESTORED {receiver.receipt_fingerprint} "
    )

    restore_destination = receiver.folder_run.result_root.parent / "martin-original"
    receiver_result_before_restore = tree_state(receiver.folder_run.result_root)
    report = restore_connected_result(
        receiver.folder_run.result_root,
        restore_destination,
    )
    assert report.receipt_fingerprint == receiver.receipt_fingerprint
    assert report.source_commitment == martin_inventory.source_commitment
    assert portable_tree(restore_destination) == portable_tree(fixture.martin_root)
    assert portable_tree(restore_destination) != portable_tree(fixture.sofia_root)
    assert tree_state(fixture.sofia_root) == sofia_before
    assert tree_state(fixture.martin_root) == martin_before
    assert tree_state(receiver.folder_run.result_root) == receiver_result_before_restore
    assert _file_state(origin.change_file_path) == change_file_before


@pytest.mark.parametrize(
    ("mutation", "expected_blocker"),
    [
        ("payload", "receiver_payload_changed"),
        ("markdown_prose", "receiver_markdown_content_changed"),
        ("relationship", "receiver_relationship_changed"),
        ("protected", "receiver_protected_member_mismatch"),
    ],
)
def test_receiver_refuses_changed_project_without_output(
    tmp_path: Path,
    mutation: str,
    expected_blocker: str,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    _mutate_martin(fixture, mutation)
    receiver_before = tree_state(fixture.martin_root)
    change_before = _file_state(change_file)
    output = tmp_path / "receiver-output"
    output.mkdir()

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=change_file,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == expected_blocker
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before
    assert _file_state(change_file) == change_before


def test_receiver_fresh_process_has_no_planner_provider_or_budget_authority(
    tmp_path: Path,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    output = tmp_path / "isolated-receiver-output"
    output.mkdir()
    budget_path = Path(".name-atlas/api_budget.json").resolve()
    script = r"""
import builtins
import hashlib
import json
import socket
import sys
from pathlib import Path

change_file = Path(sys.argv[1])
source = Path(sys.argv[2])
output = Path(sys.argv[3])
budget = Path(sys.argv[4])
forbidden = (
    "name_atlas.folder_refactor.planner",
    "name_atlas.folder_refactor.planner_provider",
    "name_atlas.decision_cards.budget",
    "name_atlas.decision_cards.providers",
    "openai",
)
before_modules = frozenset(
    name for name in sys.modules
    if any(name == item or name.startswith(item + ".") for item in forbidden)
)
if before_modules:
    raise AssertionError(f"forbidden authority loaded before service: {before_modules}")
def budget_digest():
    return hashlib.sha256(budget.read_bytes()).hexdigest() if budget.exists() else None

before_budget = budget_digest()
original_import = builtins.__import__
network_attempts = []

def blocked_connection(*args, **kwargs):
    network_attempts.append("create_connection")
    raise AssertionError("receiver attempted an external network connection")

class GuardedSocket(socket.socket):
    def connect(self, *args, **kwargs):
        network_attempts.append("socket.connect")
        raise AssertionError("receiver attempted an external network connection")

    def connect_ex(self, *args, **kwargs):
        network_attempts.append("socket.connect_ex")
        raise AssertionError("receiver attempted an external network connection")

socket.create_connection = blocked_connection
socket.socket = GuardedSocket

def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    if any(name == item or name.startswith(item + ".") for item in forbidden):
        raise AssertionError(f"receiver imported forbidden authority: {name}")
    return original_import(name, globals, locals, fromlist, level)

builtins.__import__ = guarded_import
from name_atlas.folder_refactor.connected_change.service import apply_connected_change

result = apply_connected_change(
    change_file_path=change_file,
    source_root=source,
    output_parent=output,
)
after_modules = frozenset(
    name for name in sys.modules
    if any(name == item or name.startswith(item + ".") for item in forbidden)
)
after_budget = budget_digest()
print(json.dumps({
    "forbidden_modules": sorted(after_modules),
    "budget_unchanged": before_budget == after_budget,
    "network_attempts": network_attempts,
    "provider_calls": result.execution_origin.provider_call_count,
    "api_used": result.execution_origin.api_used,
    "external_network_used": result.execution_origin.external_network_used,
    "result_root": str(result.folder_run.result_root),
}, sort_keys=True))
"""
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    environment.pop("OPENAI_API_KEY", None)

    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(change_file),
            str(fixture.martin_root),
            str(output),
            str(budget_path),
        ],
        cwd=Path.cwd(),
        env=environment,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )

    evidence = json.loads(completed.stdout)
    assert evidence == {
        "api_used": False,
        "budget_unchanged": True,
        "external_network_used": False,
        "forbidden_modules": [],
        "network_attempts": [],
        "provider_calls": 0,
        "result_root": str(output / fixture.result_name),
    }
    verification = verify_connected_result(Path(evidence["result_root"]))
    assert verification.status is ConnectedReceiptVerificationStatus.VERIFIED


def test_receiver_refuses_symmetric_duplicate_group_without_output(
    tmp_path: Path,
) -> None:
    fixture = make_symmetric_fixture(tmp_path / "projects")
    origin_inventory = scan_folder(fixture.origin_root).inventory
    targets = {
        item.relative_path: f"organized/{item.relative_path}"
        for item in origin_inventory.files
    }
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.origin_root,
        output_parent=origin_output,
        request="Organize every file and preserve every supported link.",
        result_folder_name="organized-copy",
        target_by_original_path=targets,
    )
    receiver_before = tree_state(fixture.receiver_root)
    change_before = _file_state(origin.change_file_path)

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=origin.change_file_path,
            source_root=fixture.receiver_root,
            output_parent=receiver_output,
        )

    assert raised.value.code == "receiver_ambiguous_duplicate_group"
    assert tuple(receiver_output.iterdir()) == ()
    assert tree_state(fixture.receiver_root) == receiver_before
    assert _file_state(origin.change_file_path) == change_before


def test_receiver_refuses_change_file_fingerprint_mismatch_without_output(
    tmp_path: Path,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    tampered_payload = json.loads(change_file.read_bytes())
    tampered_payload["core"]["request"] += " altered"
    tampered = tmp_path / "tampered.nameatlas-change.json"
    tampered.write_bytes(canonical_json_bytes(tampered_payload))
    output = tmp_path / "receiver-output"
    output.mkdir()
    receiver_before = tree_state(fixture.martin_root)

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=tampered,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == "change_file_fingerprint_mismatch"
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.martin_root) == receiver_before


def test_verifier_rejects_self_consistent_reissued_match_authority(
    tmp_path: Path,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    receiver_output = tmp_path / "receiver-output"
    receiver_output.mkdir()
    receiver = apply_connected_change(
        change_file_path=change_file,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
    )
    result_root = receiver.folder_run.result_root
    report = parse_portable_model(
        read_regular_bytes(result_root, CONNECTED_CHANGE_MATCH_REPORT_PATH),
        ConnectedChangeMatchReport,
    )
    first, second, *remaining = report.mappings
    altered_mappings = tuple(
        sorted(
            (
                first.model_copy(
                    update={"logical_member_id": second.logical_member_id}
                ),
                second.model_copy(
                    update={"logical_member_id": first.logical_member_id}
                ),
                *remaining,
            ),
            key=lambda item: item.logical_member_id,
        )
    )
    provisional_report = ConnectedChangeMatchReport.model_construct(
        **report.model_dump(
            mode="python",
            exclude={"mappings", "match_report_fingerprint"},
        ),
        mappings=altered_mappings,
        match_report_fingerprint="0" * 64,
    )
    altered_report = ConnectedChangeMatchReport(
        **provisional_report.model_dump(
            mode="python",
            exclude={"match_report_fingerprint"},
        ),
        match_report_fingerprint=(
            connected_change_match_report_fingerprint(provisional_report)
        ),
    )
    report_bytes = canonical_portable_json_bytes(altered_report)
    (result_root / CONNECTED_CHANGE_MATCH_REPORT_PATH).write_bytes(report_bytes)

    execution_origin = CapsuleAppliedExecutionOrigin.model_validate_json(
        read_regular_bytes(result_root, EXECUTION_ORIGIN_PATH),
        strict=True,
    )
    altered_origin = CapsuleAppliedExecutionOrigin(
        **execution_origin.model_dump(
            mode="python",
            exclude={"match_report_fingerprint"},
        ),
        match_report_fingerprint=altered_report.match_report_fingerprint,
    )
    (result_root / EXECUTION_ORIGIN_PATH).write_bytes(
        canonical_portable_json_bytes(altered_origin)
    )

    envelope = parse_portable_model(
        read_regular_bytes(result_root, CHANGE_RECEIPT_PATH),
        FolderReceiptEnvelopeV2,
    )
    changed_paths = {
        CONNECTED_CHANGE_MATCH_REPORT_PATH,
        EXECUTION_ORIGIN_PATH,
    }
    commitments = tuple(
        (
            FolderArtifactCommitment(
                path=commitment.path,
                size=regular_file_measurement(result_root, commitment.path)[0],
                sha256=regular_file_measurement(result_root, commitment.path)[1],
            )
            if commitment.path in changed_paths
            else commitment
        )
        for commitment in envelope.receipt.artifact_commitments
    )
    altered_core = FolderReceiptCoreV2(
        **envelope.receipt.model_dump(
            mode="python",
            exclude={
                "artifact_commitments",
                "execution_origin_fingerprint",
                "match_report_fingerprint",
                "match_report_sha256",
            },
        ),
        artifact_commitments=commitments,
        execution_origin_fingerprint=canonical_sha256(altered_origin),
        match_report_fingerprint=altered_report.match_report_fingerprint,
        match_report_sha256=hashlib.sha256(report_bytes).hexdigest(),
    )
    altered_envelope = FolderReceiptEnvelopeV2(
        receipt=altered_core,
        receipt_fingerprint=canonical_sha256(altered_core),
    )
    (result_root / CHANGE_RECEIPT_PATH).write_bytes(
        canonical_portable_json_bytes(altered_envelope)
    )
    BagItWriter().finalize_tagmanifest(result_root)

    assert BagItPackageValidator().validate(result_root).valid is True
    verification = verify_connected_result(result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("connected_receipt_invalid",)


def test_verifier_rejects_self_consistent_forged_reference_graph(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture, change_file = _create_origin_fixture(tmp_path)
    receiver_scan, actual_graph = folder_transaction.scan_folder_with_references(
        fixture.martin_root
    )
    forged_graph = _swap_reference_targets(actual_graph)
    assert forged_graph != actual_graph
    receiver_output = tmp_path / "receiver-output"
    receiver_output.mkdir()

    def forged_scan(_: Path) -> tuple[Any, FolderReferenceGraph]:
        return receiver_scan, forged_graph

    def forged_issuer_verification(result_root: Path) -> SimpleNamespace:
        envelope = parse_portable_model(
            read_regular_bytes(result_root, CHANGE_RECEIPT_PATH),
            FolderReceiptEnvelopeV2,
        )
        return SimpleNamespace(
            status=ConnectedReceiptVerificationStatus.VERIFIED,
            receipt_fingerprint=envelope.receipt_fingerprint,
            checks=(),
        )

    with monkeypatch.context() as forged:
        forged.setattr(
            connected_change_service,
            "scan_folder_with_references",
            forged_scan,
        )
        forged.setattr(
            folder_transaction,
            "_build_reference_graph_for_scan",
            lambda _: forged_graph,
        )
        forged.setattr(
            connected_change_service,
            "verify_connected_result",
            forged_issuer_verification,
        )
        receiver = apply_connected_change(
            change_file_path=change_file,
            source_root=fixture.martin_root,
            output_parent=receiver_output,
        )

    assert BagItPackageValidator().validate(receiver.folder_run.result_root).valid
    verification = verify_connected_result(receiver.folder_run.result_root)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("connected_receipt_invalid",)


def test_change_file_rejects_receiver_receipt_as_origin_authority(
    tmp_path: Path,
) -> None:
    fixture, change_file_path = _create_origin_fixture(tmp_path)
    receiver_output = tmp_path / "receiver-output"
    receiver_output.mkdir()
    receiver = apply_connected_change(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
    )
    change_file = parse_connected_change_file(change_file_path.read_bytes())
    receiver_envelope = parse_portable_model(
        read_regular_bytes(receiver.folder_run.result_root, CHANGE_RECEIPT_PATH),
        FolderReceiptEnvelopeV2,
    )

    with pytest.raises(ConnectedChangeError) as raised:
        create_connected_change_file(
            change_file.core,
            originating_receipt=receiver_envelope,
        )

    assert raised.value.code == "change_file_schema_invalid"


def test_origin_refuses_changed_protected_target_without_output(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    targets = {**fixture.target_paths, ".env.local": "moved/.env.local"}
    output = tmp_path / "origin-output"
    output.mkdir()
    source_before = tree_state(fixture.sofia_root)

    with pytest.raises(ConnectedChangeError) as raised:
        create_connected_change_origin(
            source_root=fixture.sofia_root,
            output_parent=output,
            request=fixture.request,
            result_folder_name=fixture.result_name,
            target_by_original_path=targets,
        )

    assert raised.value.code == "origin_protected_target_invalid"
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.sofia_root) == source_before


def _create_origin_fixture(
    tmp_path: Path,
) -> tuple[ConnectedChangeFixture, Path]:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "origin-output"
    output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    return fixture, origin.change_file_path


def _mutate_martin(fixture: ConnectedChangeFixture, mutation: str) -> None:
    root = fixture.martin_root
    if mutation == "payload":
        (root / "originals/a-copy.txt").write_bytes(b"changed presentation\n")
    elif mutation == "markdown_prose":
        (root / "working/research.md").write_bytes(
            b"Changed prose: [document](../originals/b-copy.txt#draft)\r\n"
        )
    elif mutation == "relationship":
        (root / "working/research.md").write_bytes(
            b"Research item: [document](../originals/a-copy.txt#draft)\r\n"
        )
    elif mutation == "protected":
        (root / ".env.local").write_bytes(b"DEMO_MODE=changed\n")
    else:
        raise AssertionError(f"Unhandled C0 mutation: {mutation}")


def _file_state(path: Path) -> tuple[int, int, int, int, bytes]:
    metadata = path.lstat()
    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_size,
        metadata.st_mtime_ns,
        path.read_bytes(),
    )


def _swap_reference_targets(graph: FolderReferenceGraph) -> FolderReferenceGraph:
    if len(graph.references) != 2:
        raise AssertionError("The C0 adversarial graph requires exactly two links.")
    first, second = graph.references

    def replace_target(
        reference: MarkdownReference,
        target: MarkdownReference,
    ) -> MarkdownReference:
        values = reference.model_dump(mode="python")
        values.update(
            target_file_id=target.target_file_id,
            target_path=target.target_path,
            reference_id=reference_fingerprint(
                source_file_id=reference.source_file_id,
                target_file_id=target.target_file_id,
                destination_start_byte=reference.destination_start_byte,
                destination_end_byte=reference.destination_end_byte,
                original_destination_bytes_hex=(
                    reference.original_destination_bytes_hex
                ),
            ),
        )
        return MarkdownReference.model_validate(values, strict=True)

    return FolderReferenceGraph(
        source_commitment=graph.source_commitment,
        references=(
            replace_target(first, second),
            replace_target(second, first),
        ),
        ignored=graph.ignored,
    )


def _watched_imports() -> frozenset[str]:
    return frozenset(
        name
        for name in sys.modules
        if any(
            name == forbidden or name.startswith(f"{forbidden}.")
            for forbidden in _FORBIDDEN_RECEIVER_IMPORTS
        )
    )


def _guarded_receiver_import() -> Any:
    original_import = builtins.__import__

    def guarded_import(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> ModuleType:
        if any(
            name == forbidden or name.startswith(f"{forbidden}.")
            for forbidden in _FORBIDDEN_RECEIVER_IMPORTS
        ):
            raise AssertionError(
                f"Receiver transaction imported forbidden authority: {name}"
            )
        return original_import(name, globals, locals, fromlist, level)

    return guarded_import
