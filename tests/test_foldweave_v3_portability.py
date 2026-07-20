"""Path-neutral Foldweave v3 producer and independent-verifier regressions."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Literal

import pytest
from test_foldweave_derivative_review_service import (
    _accept_parent_unchanged,
    _build_receiver_parent,
    _create_child,
)
from test_foldweave_host_service import _complete_host_plan, _start_host_job

from name_atlas.cli import run as run_cli
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderPortableExecutionAuthorizationV1,
    GptDerivativeJobAuthorityV3,
)
from name_atlas.folder_refactor.connected_change.receipt import (
    FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.portable_artifacts import CHANGE_RECEIPT_PATH
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)
from name_atlas.verification.bag_writer import BagItWriter


def test_origin_producer_blocks_absolute_host_call_id(tmp_path: Path) -> None:
    """Observable host metadata cannot leak a local path into origin proof."""

    fixture, output, service, planning = _start_host_job(tmp_path)
    reviewing = service.submit_plan(
        job_id=planning.job_id,
        call_id="/Users/example/private-origin",
        plan=_complete_host_plan(fixture, planning),
    )
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None

    blocked = service.accept_plan_and_create_copy(
        job_id=reviewing.job_id,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        result_folder_name=reviewing.candidate_plan.result_folder_name,
        idempotency_key="reject-pathful-host-origin",
        channel="chatgpt_hosted",
    )

    assert blocked.lifecycle is FolderJobLifecycleV3.BLOCKED
    assert blocked.blocker_message is not None
    assert "sender-local absolute path" in blocked.blocker_message
    assert tuple(output.iterdir()) == ()


@pytest.mark.anyio
async def test_derivative_producer_blocks_absolute_provider_call_id(
    tmp_path: Path,
) -> None:
    """Derivative observable metadata receives the same producer-side refusal."""

    context = _build_receiver_parent(tmp_path)
    child = _create_child(context, key="pathful-derivative-child")
    assert isinstance(child.authority, GptDerivativeJobAuthorityV3)
    parent = child.authority.parent_binding
    mapping = next(
        item for item in parent.parent_candidate.file_mappings if not item.protected
    )
    provider = _AbsolutePathDerivativeProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=parent.parent_candidate_fingerprint,
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=mapping.file_id,
                    replacement_target_path=(
                        f"portable-review/{Path(mapping.target_path).name}"
                    ),
                    rationale="Exercise derivative proof portability.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )
    reviewing = await context.service.submit_direct_derivative_revision(
        child.job_path,
        provider=provider,
    )
    assert reviewing.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None

    blocked = context.service.accept(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        output_parent=context.child_output,
        result_folder_name=reviewing.candidate_plan.result_folder_name,
        idempotency_key="reject-pathful-derivative",
        channel="native_app",
    )

    assert blocked.lifecycle is FolderJobLifecycleV3.BLOCKED
    assert blocked.blocker_message is not None
    assert "sender-local absolute path" in blocked.blocker_message
    assert tuple(context.child_output.iterdir()) == ()


def test_receiver_verifier_rejects_pathful_portable_authorization(
    tmp_path: Path,
) -> None:
    """Independent v3 verification repeats the path-neutral authority check."""

    context = _build_receiver_parent(tmp_path)
    verified_job = _accept_parent_unchanged(
        context,
        key="portable-receiver-accept",
    )
    assert verified_job.final_result_path is not None
    assert verified_job.execution_authorization is not None
    normal = verify_connected_result(verified_job.final_result_path)
    assert normal.status is ConnectedReceiptVerificationStatus.VERIFIED

    authorization_path = (
        verified_job.final_result_path / FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH
    )
    authorization_bytes = authorization_path.read_bytes()
    portable = FolderPortableExecutionAuthorizationV1.model_validate_json(
        authorization_bytes,
        strict=True,
    )
    assert portable.authorization_fingerprint == (
        verified_job.execution_authorization.authorization_fingerprint
    )
    assert b'"output_parent"' not in authorization_bytes
    assert str(context.output_parent).encode("utf-8") not in authorization_bytes

    forged = (tmp_path / "forged-pathful-receiver").resolve()
    shutil.copytree(verified_job.final_result_path, forged)
    _forge_pathful_portable_authorization(forged)

    blocked = verify_connected_result(forged)
    assert blocked.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert "portable_sender_path_detected" in blocked.failed_check_ids


def test_foldweave_cli_verifies_and_restores_v3_result(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The public provider-free CLI dispatches v3 verification and restore."""

    fixture, _output, service, planning = _start_host_job(tmp_path)
    reviewing = service.submit_plan(
        job_id=planning.job_id,
        call_id="portable-v3-plan",
        plan=_complete_host_plan(fixture, planning),
    )
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    verified = service.accept_plan_and_create_copy(
        job_id=reviewing.job_id,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        result_folder_name=reviewing.candidate_plan.result_folder_name,
        idempotency_key="portable-v3-accept",
        channel="chatgpt_hosted",
    )
    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert verified.final_result_path is not None
    assert verified.verified_artifacts is not None

    assert (
        run_cli(
            [
                "verify-receipt",
                str(verified.final_result_path),
                "--source",
                str(fixture.sofia_root),
            ],
            environ={},
        )
        == 0
    )
    assert capsys.readouterr().out == (
        f"VERIFIED {verified.verified_artifacts.receipt_fingerprint}\n"
    )

    destination = tmp_path / "restored-v3-source"
    assert (
        run_cli(
            [
                "restore-receipt",
                str(verified.final_result_path),
                str(destination),
            ],
            environ={},
        )
        == 0
    )
    assert capsys.readouterr().out.startswith(
        f"RESTORED {verified.verified_artifacts.receipt_fingerprint} "
    )
    assert (
        scan_folder(destination).inventory == scan_folder(fixture.sofia_root).inventory
    )


class _AbsolutePathDerivativeProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self, revision: FolderPlanRevisionV1) -> None:
        self._revision = revision

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        _turn_input: FolderDerivativeRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        return FolderRevisionProviderResponseV1(
            provider_kind="deterministic",
            call_id="/Users/example/private-derivative",
            revision=self._revision,
        )


def _forge_pathful_portable_authorization(result_root: Path) -> None:
    """Keep outer commitments valid while injecting one prohibited local path."""

    authorization_path = result_root / FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH
    authorization = json.loads(authorization_path.read_bytes())
    authorization["result_folder_name"] = "/Users/example/private-receiver"
    authorization["authorization_fingerprint"] = canonical_sha256(
        {
            key: value
            for key, value in authorization.items()
            if key != "authorization_fingerprint"
        }
    )
    authorization_bytes = canonical_json_bytes(authorization)
    FolderPortableExecutionAuthorizationV1.model_validate_json(
        authorization_bytes,
        strict=True,
    )
    authorization_path.write_bytes(authorization_bytes)

    receipt_path = result_root / CHANGE_RECEIPT_PATH
    receipt = json.loads(receipt_path.read_bytes())
    core = receipt["receipt"]
    core["execution_authorization_fingerprint"] = authorization[
        "authorization_fingerprint"
    ]
    for commitment in core["artifact_commitments"]:
        if commitment["path"] == FOLDWEAVE_EXECUTION_AUTHORIZATION_PATH:
            commitment["size"] = len(authorization_bytes)
            commitment["sha256"] = hashlib.sha256(authorization_bytes).hexdigest()
            break
    else:
        raise AssertionError("Receipt omitted portable execution authorization.")
    receipt["receipt_fingerprint"] = canonical_sha256(core)
    receipt_path.write_bytes(canonical_json_bytes(receipt))
    BagItWriter().finalize_tagmanifest(result_root)
