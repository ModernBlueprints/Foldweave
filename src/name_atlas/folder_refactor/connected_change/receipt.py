"""Strict acyclic v2 receipts for Connected Change origin and receiver results."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from name_atlas.domain import PackageValidationResult
from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.connected_change.contracts import (
    CapsuleAppliedExecutionOrigin,
    FolderExecutionOrigin,
    GptExecutionOrigin,
    GptPlannedExecutionOrigin,
)
from name_atlas.folder_refactor.connected_change.organized_tree import (
    OrganizedTreeSnapshot,
)
from name_atlas.folder_refactor.connected_change.receipt_contracts import (
    FolderReceiptCoreV2,
    FolderReceiptEnvelopeV2,
    connected_required_receipt_artifact_paths,
)
from name_atlas.folder_refactor.contracts import (
    FolderInventory,
    FolderVerificationReport,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderEvidenceLedgerV2,
    GptPlannedExecutionOriginV2,
)
from name_atlas.folder_refactor.markdown_contracts import FolderReferenceGraph
from name_atlas.folder_refactor.portable_artifacts import regular_file_measurement
from name_atlas.folder_refactor.receipt_contracts import (
    FolderArtifactCommitment,
    FolderChangeLedger,
    FolderEvidenceLedger,
    FolderPathMapRow,
    FolderStagedDataMember,
    FolderUserRequestArtifact,
)
from name_atlas.folder_refactor.serialization import canonical_sha256

EXECUTION_ORIGIN_PATH = "name-atlas/execution_origin.json"
CONNECTED_CHANGE_PATH = "name-atlas/connected_change_capsule.json"
CONNECTED_CHANGE_MATCH_REPORT_PATH = "name-atlas/connected_change_match_report.json"

_REQUIRED_REPORT_CHECK_IDS = frozenset(
    {
        "bagit_validation",
        "complete_file_bijection",
        "empty_directories_preserved",
        "payload_hashes_preserved",
        "protected_paths_preserved",
        "result_is_separate",
        "source_unchanged",
        "supported_markdown_links_resolve",
    }
)


def build_connected_artifact_commitments(
    pending_root: Path,
    *,
    original_content_file_ids: tuple[str, ...],
    include_match_report: bool,
) -> tuple[FolderArtifactCommitment, ...]:
    """Measure the exact pre-receipt portable authority set."""

    if not isinstance(pending_root, Path):
        raise ValueError("Pending result root must be a pathlib.Path.")
    execution_role: Literal["origin", "receiver"] = (
        "receiver" if include_match_report else "origin"
    )
    paths = set(connected_required_receipt_artifact_paths(execution_role))
    paths.update(
        f"name-atlas/original-content/{file_id}.bin"
        for file_id in original_content_file_ids
    )
    commitments = []
    for relative_path in sorted(paths):
        size, digest = regular_file_measurement(pending_root, relative_path)
        commitments.append(
            FolderArtifactCommitment(
                path=relative_path,
                size=size,
                sha256=digest,
            )
        )
    return tuple(commitments)


def build_connected_receipt(
    *,
    execution_role: Literal["origin", "receiver"],
    job_id: str,
    inventory: FolderInventory,
    user_request: FolderUserRequestArtifact,
    accepted_plan: FolderAcceptedPlanV2,
    reference_graph: FolderReferenceGraph,
    path_rows: tuple[FolderPathMapRow, ...],
    change_ledger: FolderChangeLedger,
    report: FolderVerificationReport,
    execution_origin: FolderExecutionOrigin,
    evidence_ledger: FolderEvidenceLedger | FolderEvidenceLedgerV2 | None = None,
    artifact_commitments: tuple[FolderArtifactCommitment, ...],
    staged_members: tuple[FolderStagedDataMember, ...],
    staged_data_commitment: str,
    organized_tree: OrganizedTreeSnapshot,
    producer_bagit_validation: PackageValidationResult,
    connected_change_core_fingerprint: str,
    imported_change_file_fingerprint: str | None = None,
    imported_change_file_sha256: str | None = None,
    originating_receipt_fingerprint: str | None = None,
    match_report_fingerprint: str | None = None,
    match_report_sha256: str | None = None,
) -> FolderReceiptEnvelopeV2:
    """Build a strict role-aware receipt after independently binding authorities."""

    plan_fingerprint = canonical_sha256(accepted_plan)
    graph_fingerprint = canonical_sha256(reference_graph)
    if not producer_bagit_validation.valid:
        raise ValueError("Producer BagIt validation must pass before receipt creation.")
    if not (
        inventory.source_commitment
        == accepted_plan.source_commitment
        == reference_graph.source_commitment
        == report.source_commitment
        == change_ledger.source_commitment
    ):
        raise ValueError("Receipt authorities target different source commitments.")
    if not (
        user_request.request_fingerprint
        == accepted_plan.request_fingerprint
        == report.request_fingerprint
        == change_ledger.request_fingerprint
    ):
        raise ValueError("Receipt authorities target different requests.")
    if change_ledger.accepted_plan_fingerprint != plan_fingerprint:
        raise ValueError("Change ledger does not bind the v2 accepted plan.")
    if change_ledger.reference_graph_fingerprint != graph_fingerprint:
        raise ValueError("Change ledger does not bind the derived reference graph.")
    if report.accepted_plan_fingerprint != plan_fingerprint:
        raise ValueError("Verification report does not bind the v2 accepted plan.")
    if change_ledger.evidence_fingerprint != accepted_plan.evidence_fingerprint:
        raise ValueError("Change ledger does not bind the origin evidence identity.")
    if execution_role == "origin":
        if not isinstance(
            execution_origin,
            GptPlannedExecutionOrigin | GptPlannedExecutionOriginV2,
        ):
            raise ValueError("An origin receipt requires gpt_planned authority.")
        if evidence_ledger is None:
            raise ValueError("An origin receipt requires its exact evidence ledger.")
        validate_connected_evidence_ledger(
            job_id=job_id,
            inventory=inventory,
            user_request=user_request,
            accepted_plan=accepted_plan,
            execution_origin=execution_origin,
            evidence_ledger=evidence_ledger,
        )
    elif not isinstance(execution_origin, CapsuleAppliedExecutionOrigin):
        raise ValueError("A receiver receipt requires capsule_applied authority.")
    elif evidence_ledger is not None:
        raise ValueError("A receiver receipt cannot fabricate a GPT evidence ledger.")
    execution_plan_fingerprint = (
        execution_origin.accepted_plan_fingerprint
        if isinstance(
            execution_origin,
            GptPlannedExecutionOrigin | GptPlannedExecutionOriginV2,
        )
        else execution_origin.receiver_accepted_plan_fingerprint
    )
    if execution_plan_fingerprint != plan_fingerprint:
        raise ValueError("Execution origin does not bind the accepted plan.")
    if staged_data_commitment != report.staged_data_commitment:
        raise ValueError("Staged commitment differs from the verification report.")
    validate_connected_verification_report(
        inventory=inventory,
        accepted_plan=accepted_plan,
        reference_graph=reference_graph,
        change_ledger=change_ledger,
        report=report,
        organized_tree=organized_tree,
    )
    core = FolderReceiptCoreV2(
        execution_role=execution_role,
        job_id=job_id,
        source_commitment=inventory.source_commitment,
        source_file_count=len(inventory.files),
        source_directory_count=inventory.directory_count,
        source_bytes=inventory.total_bytes,
        request_fingerprint=user_request.request_fingerprint,
        evidence_fingerprint=accepted_plan.evidence_fingerprint,
        accepted_plan_fingerprint=plan_fingerprint,
        reference_graph_fingerprint=graph_fingerprint,
        execution_origin_fingerprint=canonical_sha256(execution_origin),
        change_ledger_fingerprint=canonical_sha256(change_ledger),
        verification_report_fingerprint=canonical_sha256(report),
        connected_change_core_fingerprint=connected_change_core_fingerprint,
        imported_change_file_fingerprint=imported_change_file_fingerprint,
        imported_change_file_sha256=imported_change_file_sha256,
        originating_receipt_fingerprint=originating_receipt_fingerprint,
        match_report_fingerprint=match_report_fingerprint,
        match_report_sha256=match_report_sha256,
        artifact_commitments=artifact_commitments,
        staged_data_members=staged_members,
        staged_data_commitment=staged_data_commitment,
        organized_tree=organized_tree,
        map_row_count=len(path_rows),
        path_change_count=change_ledger.path_change_count,
        supported_link_count=change_ledger.supported_link_count,
        rewritten_link_count=change_ledger.rewritten_link_count,
        producer_bagit_messages=producer_bagit_validation.messages,
    )
    return FolderReceiptEnvelopeV2(
        receipt=core,
        receipt_fingerprint=canonical_sha256(core),
    )


def validate_connected_evidence_ledger(
    *,
    job_id: str,
    inventory: FolderInventory,
    user_request: FolderUserRequestArtifact,
    accepted_plan: FolderAcceptedPlanV2,
    execution_origin: GptExecutionOrigin,
    evidence_ledger: FolderEvidenceLedger | FolderEvidenceLedgerV2,
) -> None:
    """Require one origin ledger and execution-origin record to agree exactly."""

    if isinstance(execution_origin, GptPlannedExecutionOriginV2):
        if not isinstance(evidence_ledger, FolderEvidenceLedgerV2):
            raise ValueError("V2 execution origin requires composite v2 evidence.")
        expected_provider_calls = (
            evidence_ledger.response_turn_count
            if evidence_ledger.model_transport == "responses_api"
            else 0
        )
        expected_api_use = evidence_ledger.model_transport == "responses_api"
        expected_network_use = evidence_ledger.model_transport in {
            "responses_api",
            "chatgpt_hosted",
            "codex_hosted",
        }
        if not (
            evidence_ledger.job_id == job_id
            and evidence_ledger.source_commitment == inventory.source_commitment
            and evidence_ledger.request_fingerprint == user_request.request_fingerprint
            and evidence_ledger.request_scope == accepted_plan.request_scope
            and evidence_ledger.evidence_fingerprint
            == accepted_plan.evidence_fingerprint
            and evidence_ledger.accepted_plan_fingerprint
            == canonical_sha256(accepted_plan)
            and execution_origin.evidence_fingerprint
            == evidence_ledger.evidence_fingerprint
            and execution_origin.evidence_transcript_fingerprint
            == evidence_ledger.transcript_fingerprint
            and execution_origin.accepted_plan_fingerprint
            == evidence_ledger.accepted_plan_fingerprint
            and execution_origin.provider_call_count == expected_provider_calls
            and execution_origin.returned_model_ids
            == evidence_ledger.returned_model_ids
            and execution_origin.store_false == evidence_ledger.store_false
            and execution_origin.planning_basis == evidence_ledger.planning_basis
            and execution_origin.model_transport == evidence_ledger.model_transport
            and execution_origin.clarification_question
            == evidence_ledger.initial_ledger.clarification_question
            and execution_origin.clarification_answer
            == evidence_ledger.initial_ledger.clarification_answer
            and execution_origin.api_used == expected_api_use
            and execution_origin.external_network_used == expected_network_use
            and execution_origin.observable_transcript
            == tuple(
                record
                for segment in evidence_ledger.segments
                for record in segment.observable_records
            )
        ):
            raise ValueError(
                "Composite evidence, accepted plan, and v2 execution origin "
                "do not agree."
            )
        if accepted_plan.evidence_schema_version != "folder-evidence-ledger.v2":
            raise ValueError("Composite evidence requires accepted-plan v2 dispatch.")
        return
    if not isinstance(evidence_ledger, FolderEvidenceLedger):
        raise ValueError("Historical execution origin requires v1 evidence.")

    expected_provider_kind = {
        "deterministic_development": "deterministic",
        "live": "live",
        "recorded_replay": "recorded_replay",
    }[execution_origin.planner_kind]
    observable_transcript = tuple(
        turn.model_dump(mode="json") for turn in evidence_ledger.observable_turns
    )
    if not (
        evidence_ledger.job_id == job_id
        and evidence_ledger.source_commitment == inventory.source_commitment
        and evidence_ledger.request_fingerprint == user_request.request_fingerprint
        and evidence_ledger.evidence_fingerprint == accepted_plan.evidence_fingerprint
        and evidence_ledger.accepted_plan_fingerprint == canonical_sha256(accepted_plan)
        and evidence_ledger.request_scope == accepted_plan.request_scope
        and evidence_ledger.provider_kind == expected_provider_kind
        and evidence_ledger.clarification_question
        == execution_origin.clarification_question
        and evidence_ledger.clarification_answer
        == execution_origin.clarification_answer
        and execution_origin.evidence_fingerprint
        == evidence_ledger.evidence_fingerprint
        and execution_origin.accepted_plan_fingerprint
        == evidence_ledger.accepted_plan_fingerprint
        and execution_origin.observable_transcript == observable_transcript
    ):
        raise ValueError(
            "Origin evidence ledger, accepted plan, execution origin, and receipt "
            "identity do not agree."
        )
    if execution_origin.planner_kind == "live":
        if not (
            execution_origin.provider_call_count == evidence_ledger.response_turn_count
            and execution_origin.returned_model_id is not None
            and execution_origin.returned_model_id in evidence_ledger.returned_model_ids
            and execution_origin.store_false is True
            and evidence_ledger.store_false is True
        ):
            raise ValueError("Live evidence ledger metadata is not truthful.")
    elif not (
        execution_origin.provider_call_count == 0
        and execution_origin.store_false is None
        and evidence_ledger.store_false is None
    ):
        raise ValueError("Keyless evidence ledger metadata is not truthful.")
    elif execution_origin.planner_kind == "deterministic_development":
        if execution_origin.returned_model_id is not None or (
            evidence_ledger.returned_model_ids
        ):
            raise ValueError("Deterministic evidence cannot claim a returned model.")
    elif evidence_ledger.returned_model_ids and (
        execution_origin.returned_model_id not in evidence_ledger.returned_model_ids
    ):
        raise ValueError("Replay evidence does not bind its returned model identity.")


def validate_connected_verification_report(
    *,
    inventory: FolderInventory,
    accepted_plan: FolderAcceptedPlanV2,
    reference_graph: FolderReferenceGraph,
    change_ledger: FolderChangeLedger,
    report: FolderVerificationReport,
    organized_tree: OrganizedTreeSnapshot,
) -> None:
    """Require the human-facing verification report to equal derived facts."""

    check_ids = tuple(check.check_id for check in report.checks)
    if len(check_ids) != len(set(check_ids)) or set(check_ids) != (
        _REQUIRED_REPORT_CHECK_IDS
    ):
        raise ValueError("Verification report check IDs are not exact.")
    expected = {
        "source_commitment": inventory.source_commitment,
        "request_fingerprint": accepted_plan.request_fingerprint,
        "accepted_plan_fingerprint": canonical_sha256(accepted_plan),
        "result_folder_name": accepted_plan.result_folder_name,
        "file_count": len(inventory.files),
        "path_change_count": change_ledger.path_change_count,
        "protected_file_count": change_ledger.protected_file_count,
        "empty_directory_count": len(accepted_plan.empty_directories),
        "supported_link_count": len(reference_graph.references),
        "rewritten_link_count": change_ledger.rewritten_link_count,
        "rewritten_markdown_file_count": (change_ledger.rewritten_markdown_file_count),
    }
    if any(
        getattr(report, field_name) != value for field_name, value in expected.items()
    ):
        raise ValueError("Verification report fields differ from derived facts.")
    if not (
        organized_tree.file_count == len(inventory.files)
        and organized_tree.empty_directory_count == len(accepted_plan.empty_directories)
    ):
        raise ValueError("Organized-tree counts differ from verified report facts.")
