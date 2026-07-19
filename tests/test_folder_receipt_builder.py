"""Focused pure generic-folder receipt construction and view tests."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

import pytest

from name_atlas.domain import PackageValidationResult
from name_atlas.folder_refactor.contracts import (
    AcceptedFileMapping,
    FolderAcceptedPlan,
    FolderEmptyDirectory,
    FolderFile,
    FolderInventory,
    FolderPlan,
    FolderPlanEntry,
    FolderVerificationCheck,
    FolderVerificationReport,
    compute_inventory_commitment,
)
from name_atlas.folder_refactor.markdown_contracts import (
    FolderReferenceGraph,
    MarkdownIgnoredCounts,
    MarkdownReference,
    reference_fingerprint,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    PlannerEvidenceState,
    PlannerObservableTurn,
    SubmitPlanCall,
    observable_turn_payload,
)
from name_atlas.folder_refactor.portable_artifacts import (
    ACCEPTED_PLAN_PATH,
    BAG_INFO_PATH,
    BAGIT_PATH,
    CHANGE_LEDGER_PATH,
    EVIDENCE_LEDGER_PATH,
    FORWARD_PATH_MAP_PATH,
    PAYLOAD_MANIFEST_PATH,
    REFERENCE_GRAPH_PATH,
    REVERSE_PATH_MAP_PATH,
    SOURCE_SNAPSHOT_PATH,
    USER_REQUEST_PATH,
    VERIFICATION_REPORT_PATH,
    canonical_portable_json_bytes,
    parse_folder_path_map,
)
from name_atlas.folder_refactor.receipt_builder import (
    FolderReceiptBuilderError,
    ObservedResultFile,
    build_folder_path_rows_and_change_ledger,
    build_folder_receipt,
    build_folder_user_request_artifact,
    compute_folder_staged_data_commitment,
    render_folder_proof_html,
    render_forward_path_map_csv,
    render_reverse_path_map_csv,
)
from name_atlas.folder_refactor.receipt_contracts import (
    PROOF_HTML_PATH,
    RECEIPT_JSON_PATH,
    FolderArtifactCommitment,
    FolderChangeLedger,
    FolderEvidenceLedger,
    FolderPathMapRow,
    FolderPlannerUsage,
    FolderReceiptEnvelope,
    FolderStagedDataMember,
    FolderUserRequestArtifact,
    folder_receipt_fingerprint,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)

JOB_ID = "123e4567e89b42d3a456426614174000"
MODEL_ID = "gpt-5.6-sol-2026-07-17"
REQUEST = (
    "Prepare this project for handoff. Keep every file and keep supported "
    "Markdown links working."
)
CHECK_IDS = (
    "source_unchanged",
    "complete_file_bijection",
    "payload_hashes_preserved",
    "supported_markdown_links_resolve",
    "protected_paths_preserved",
    "empty_directories_preserved",
    "result_is_separate",
    "bagit_validation",
)


@dataclass(frozen=True)
class ReceiptFixture:
    inventory: FolderInventory
    user_request: FolderUserRequestArtifact
    evidence_ledger: FolderEvidenceLedger
    accepted_plan: FolderAcceptedPlan
    reference_graph: FolderReferenceGraph
    path_rows: tuple[FolderPathMapRow, ...]
    change_ledger: FolderChangeLedger
    verification_report: FolderVerificationReport
    artifact_commitments: tuple[FolderArtifactCommitment, ...]
    staged_data_members: tuple[FolderStagedDataMember, ...]
    staged_data_commitment: str
    bagit_validation: PackageValidationResult
    envelope: FolderReceiptEnvelope


def test_builds_complete_sorted_change_authority_and_acyclic_receipt() -> None:
    fixture = _receipt_fixture()

    assert tuple(row.original_path for row in fixture.path_rows) == (
        ".env",
        "assets/guide.txt",
        "notes/index.md",
    )
    assert fixture.change_ledger.file_count == 3
    assert fixture.change_ledger.path_change_count == 2
    assert fixture.change_ledger.rewritten_link_count == 1
    assert fixture.change_ledger.rewritten_markdown_file_count == 1
    assert fixture.envelope.receipt.map_row_count == 3
    assert fixture.envelope.receipt.staged_data_file_count == 3

    committed_paths = {
        item.path for item in fixture.envelope.receipt.artifact_commitments
    }
    assert RECEIPT_JSON_PATH not in committed_paths
    assert PROOF_HTML_PATH not in committed_paths
    assert "tagmanifest-sha256.txt" not in committed_paths

    forward = render_forward_path_map_csv(fixture.path_rows)
    reverse = render_reverse_path_map_csv(fixture.path_rows)
    assert parse_folder_path_map(forward, reverse=False) == fixture.path_rows
    assert parse_folder_path_map(reverse, reverse=True) == fixture.path_rows
    assert reverse.splitlines()[0] == (
        b"file_id,result_path,original_path,original_size,original_sha256,"
        b"result_size,result_sha256,protected,markdown_rewritten"
    )


def test_receipt_rejects_cross_binding_and_count_disagreement() -> None:
    fixture = _receipt_fixture()
    bad_report = fixture.verification_report.model_copy(update={"file_count": 2})

    with pytest.raises(
        FolderReceiptBuilderError,
        match="Verification report file_count differs",
    ):
        _rebuild_receipt(fixture, verification_report=bad_report)

    shortened_members = fixture.staged_data_members[:-1]
    shortened_commitment = compute_folder_staged_data_commitment(shortened_members)
    matching_commitment_report = fixture.verification_report.model_copy(
        update={"staged_data_commitment": shortened_commitment}
    )
    with pytest.raises(
        FolderReceiptBuilderError,
        match="Staged-data members do not equal",
    ):
        _rebuild_receipt(
            fixture,
            staged_data_members=shortened_members,
            staged_data_commitment=shortened_commitment,
            verification_report=matching_commitment_report,
        )


def test_receipt_rejects_circular_or_post_finalization_commitment() -> None:
    fixture = _receipt_fixture()
    circular = _commitment(RECEIPT_JSON_PATH, b"not-the-receipt")
    commitments = tuple(
        sorted((*fixture.artifact_commitments, circular), key=lambda item: item.path)
    )

    with pytest.raises(
        FolderReceiptBuilderError,
        match="circular or post-finalization",
    ):
        _rebuild_receipt(fixture, artifact_commitments=commitments)


def test_offline_proof_is_deterministic_escaped_and_self_contained() -> None:
    fixture = _receipt_fixture(check_detail='<proof & "evidence">')

    first = render_folder_proof_html(
        fixture.envelope,
        fixture.change_ledger,
        fixture.verification_report,
    )
    second = render_folder_proof_html(
        fixture.envelope,
        fixture.change_ledger,
        fixture.verification_report,
    )
    text = first.decode("utf-8")

    assert first == second
    assert first.startswith(b"<!doctype html>\n")
    assert first.endswith(b"</body></html>\n")
    assert "Recorded GPT-5.6 planning run" in text
    assert "Live GPT-5.6 planning run" not in text
    assert MODEL_ID in text
    assert "&lt;proof &amp; &quot;evidence&quot;&gt;" in text
    assert '<proof & "evidence">' not in text
    assert "<script" not in text.casefold()
    assert "http://" not in text.casefold()
    assert "https://" not in text.casefold()
    assert "file://" not in text.casefold()
    assert "/Users/" not in text
    assert "uv run name-atlas verify-receipt RESULT_BAG" in text
    assert "uv run name-atlas restore-receipt RESULT_BAG RESTORE_DESTINATION" in text


def test_sender_local_paths_are_rejected_before_portable_construction() -> None:
    with pytest.raises(
        FolderReceiptBuilderError,
        match="sender-local absolute path",
    ):
        build_folder_user_request_artifact(
            "Move /Users/alice/private/project into a handoff folder."
        )

    fixture = _receipt_fixture()
    first_check = fixture.verification_report.checks[0].model_copy(
        update={"detail": "Source was read from C:\\Users\\alice\\project."}
    )
    bad_report = fixture.verification_report.model_copy(
        update={"checks": (first_check, *fixture.verification_report.checks[1:])}
    )
    with pytest.raises(
        FolderReceiptBuilderError,
        match="sender-local absolute path",
    ):
        _rebuild_receipt(fixture, verification_report=bad_report)


def test_provider_origin_is_truthful_for_live_replay_and_deterministic() -> None:
    replay = _receipt_fixture(provider_kind="recorded_replay")
    replay_html = render_folder_proof_html(
        replay.envelope,
        replay.change_ledger,
        replay.verification_report,
    ).decode("utf-8")
    assert replay.envelope.receipt.returned_model_ids == (MODEL_ID,)
    assert replay.envelope.receipt.store_false is None
    assert "Recorded GPT-5.6 planning run" in replay_html
    assert "makes no new API call" in replay_html
    assert "Live GPT-5.6 planning run" not in replay_html

    replay_without_origin = replay.envelope.receipt.model_copy(
        update={"returned_model_ids": ()}
    )
    malformed_replay_envelope = FolderReceiptEnvelope(
        receipt=replay_without_origin,
        receipt_fingerprint=folder_receipt_fingerprint(replay_without_origin),
    )
    with pytest.raises(
        FolderReceiptBuilderError,
        match="Recorded receipt evidence requires preserved model IDs",
    ):
        render_folder_proof_html(
            malformed_replay_envelope,
            replay.change_ledger,
            replay.verification_report,
        )

    live = _receipt_fixture(provider_kind="live")
    live_html = render_folder_proof_html(
        live.envelope,
        live.change_ledger,
        live.verification_report,
    ).decode("utf-8")
    assert live.envelope.receipt.returned_model_ids == (MODEL_ID,)
    assert live.envelope.receipt.store_false is True
    assert "Live GPT-5.6 planning run" in live_html
    assert "store=false" in live_html

    invalid_live = live.evidence_ledger.model_copy(update={"store_false": False})
    with pytest.raises(
        FolderReceiptBuilderError,
        match="Live planner evidence requires store=false",
    ):
        _rebuild_receipt(live, evidence_ledger=invalid_live)

    deterministic = _receipt_fixture(provider_kind="deterministic")
    deterministic_html = render_folder_proof_html(
        deterministic.envelope,
        deterministic.change_ledger,
        deterministic.verification_report,
    ).decode("utf-8")
    assert deterministic.envelope.receipt.returned_model_ids == ()
    assert "Deterministic local planning run" in deterministic_html
    assert "Live GPT-5.6 planning run" not in deterministic_html
    assert "Recorded GPT-5.6 planning run" not in deterministic_html


def test_receipt_rejects_transcript_plan_that_differs_from_accepted_plan() -> None:
    fixture = _receipt_fixture()
    original_turn = fixture.evidence_ledger.observable_turns[0]
    original_call = original_turn.tool_calls[0]
    assert isinstance(original_call, SubmitPlanCall)
    changed_entries = tuple(
        entry.model_copy(
            update={"proposed_target": "docs/review.md"}
            if entry.original_path == "notes/index.md"
            else {}
        )
        for entry in original_call.plan.entries
    )
    changed_plan = original_call.plan.model_copy(update={"entries": changed_entries})
    changed_call = original_call.model_copy(update={"plan": changed_plan})
    turn_values = original_turn.model_dump(mode="python")
    turn_values["tool_calls"] = (changed_call,)
    turn_values["response_fingerprint"] = "0" * 64
    draft_turn = PlannerObservableTurn.model_construct(**turn_values)
    turn_values["response_fingerprint"] = canonical_sha256(
        observable_turn_payload(draft_turn)
    )
    changed_turn = PlannerObservableTurn.model_validate(turn_values, strict=True)

    ledger_values = fixture.evidence_ledger.model_dump(mode="python")
    ledger_values["observable_turns"] = (changed_turn,)
    ledger_values["transcript_fingerprint"] = "0" * 64
    draft_ledger = FolderEvidenceLedger.model_construct(**ledger_values)
    ledger_values["transcript_fingerprint"] = canonical_sha256(
        draft_ledger.model_dump(
            mode="json",
            exclude={"transcript_fingerprint"},
        )
    )
    changed_ledger = FolderEvidenceLedger.model_validate(ledger_values, strict=True)

    with pytest.raises(
        FolderReceiptBuilderError,
        match="Accepted plan is not the compiled final observable submission",
    ):
        _rebuild_receipt(fixture, evidence_ledger=changed_ledger)


def test_offline_proof_rejects_disagreeing_committed_authorities() -> None:
    fixture = _receipt_fixture()
    bad_report = fixture.verification_report.model_copy(update={"path_change_count": 1})

    with pytest.raises(
        FolderReceiptBuilderError,
        match="one finalized transaction: path_change_count",
    ):
        render_folder_proof_html(
            fixture.envelope,
            fixture.change_ledger,
            bad_report,
        )


def _receipt_fixture(
    *,
    provider_kind: str = "recorded_replay",
    check_detail: str = "The exact deterministic check passed.",
) -> ReceiptFixture:
    source_bytes = {
        ".env": b"TOKEN=not-a-real-secret\n",
        "assets/guide.txt": b"Project guide\n",
        "notes/index.md": b"[Guide](../assets/guide.txt)\n",
    }
    files = tuple(
        sorted(
            (
                _folder_file(
                    ".env",
                    source_bytes[".env"],
                    protected=True,
                ),
                _folder_file("assets/guide.txt", source_bytes["assets/guide.txt"]),
                _folder_file("notes/index.md", source_bytes["notes/index.md"]),
            ),
            key=lambda item: item.relative_path,
        )
    )
    empty_directories = (FolderEmptyDirectory(relative_path="unused"),)
    inventory = FolderInventory(
        files=files,
        empty_directories=empty_directories,
        directory_count=3,
        total_bytes=sum(item.size for item in files),
        source_commitment=compute_inventory_commitment(
            files=files,
            empty_directories=empty_directories,
            directory_count=3,
            total_bytes=sum(item.size for item in files),
        ),
    )
    user_request = build_folder_user_request_artifact(REQUEST)

    initial_evidence = {
        "instruction": REQUEST,
        "paths": [item.relative_path for item in files],
    }
    initial_evidence_bytes = len(canonical_json_bytes(initial_evidence))
    evidence_fingerprint = canonical_sha256(
        {
            "aggregate_result_bytes": 0,
            "initial_evidence": initial_evidence,
            "initial_evidence_bytes": initial_evidence_bytes,
            "records": [],
            "request_fingerprint": user_request.request_fingerprint,
            "schema_version": "folder-planner-evidence-state.v1",
            "source_commitment": inventory.source_commitment,
            "total_outbound_evidence_bytes": initial_evidence_bytes,
        }
    )
    mapping_by_path = {
        ".env": ".env",
        "assets/guide.txt": "docs/guide.txt",
        "notes/index.md": "docs/index.md",
    }
    accepted_plan = FolderAcceptedPlan(
        source_commitment=inventory.source_commitment,
        request_fingerprint=user_request.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name="Northstar",
        file_mappings=tuple(
            AcceptedFileMapping(
                file_id=item.file_id,
                original_path=item.relative_path,
                target_path=mapping_by_path[item.relative_path],
                protected=item.protected,
                planner_supplied=not item.protected,
            )
            for item in files
        ),
        empty_directories=("unused",),
    )
    planner_plan = FolderPlan(
        source_commitment=inventory.source_commitment,
        request_fingerprint=user_request.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=evidence_fingerprint,
        result_folder_name="Northstar",
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=mapping_by_path[item.relative_path],
                rationale="Place this file in the requested handoff structure.",
                evidence_ids=("initial_inventory",),
            )
            for item in files
            if not item.protected
        ),
        exclusions=(),
    )
    evidence_ledger = _folder_evidence_ledger(
        provider_kind=provider_kind,
        inventory=inventory,
        user_request=user_request,
        accepted_plan=accepted_plan,
        planner_plan=planner_plan,
        initial_evidence=initial_evidence,
        initial_evidence_bytes=initial_evidence_bytes,
        evidence_fingerprint=evidence_fingerprint,
    )

    source_by_path = {item.relative_path: item for item in files}
    source_markdown = source_by_path["notes/index.md"]
    destination = "../assets/guide.txt"
    destination_start = len(b"[Guide](")
    destination_end = destination_start + len(destination.encode("utf-8"))
    target = source_by_path["assets/guide.txt"]
    reference = MarkdownReference(
        reference_id=reference_fingerprint(
            source_file_id=source_markdown.file_id,
            target_file_id=target.file_id,
            destination_start_byte=destination_start,
            destination_end_byte=destination_end,
            original_destination_bytes_hex=destination.encode("utf-8").hex(),
        ),
        source_file_id=source_markdown.file_id,
        source_path=source_markdown.relative_path,
        target_file_id=target.file_id,
        target_path=target.relative_path,
        destination_start_byte=destination_start,
        destination_end_byte=destination_end,
        original_destination_text=destination,
        original_destination_bytes_hex=destination.encode("utf-8").hex(),
        fragment=None,
        destination_style="token",
        is_image=False,
        proposed_destination="guide.txt",
        verification_status="rewritten",
    )
    reference_graph = FolderReferenceGraph(
        source_commitment=inventory.source_commitment,
        references=(reference,),
        ignored=MarkdownIgnoredCounts(external_schemes=0, anchor_only=0),
    )
    result_markdown = b"[Guide](guide.txt)\n"
    observed = {
        source_by_path[".env"].file_id: ObservedResultFile(
            relative_path=".env",
            size=source_by_path[".env"].size,
            sha256=source_by_path[".env"].sha256,
        ),
        target.file_id: ObservedResultFile(
            relative_path="docs/guide.txt",
            size=target.size,
            sha256=target.sha256,
        ),
        source_markdown.file_id: ObservedResultFile(
            relative_path="docs/index.md",
            size=len(result_markdown),
            sha256=_sha256(result_markdown),
        ),
    }
    path_rows, change_ledger = build_folder_path_rows_and_change_ledger(
        inventory=inventory,
        accepted_plan=accepted_plan,
        reference_graph=reference_graph,
        observed_result_files=observed,
    )
    staged_data_members = tuple(
        sorted(
            (
                FolderStagedDataMember(
                    path=row.result_path,
                    size=row.result_size,
                    sha256=row.result_sha256,
                )
                for row in path_rows
            ),
            key=lambda item: item.path,
        )
    )
    staged_commitment = compute_folder_staged_data_commitment(staged_data_members)
    checks = tuple(
        FolderVerificationCheck(
            check_id=check_id,
            passed=True,
            detail=check_detail if index == 0 else "The deterministic check passed.",
        )
        for index, check_id in enumerate(CHECK_IDS)
    )
    report = FolderVerificationReport(
        source_commitment=inventory.source_commitment,
        request_fingerprint=user_request.request_fingerprint,
        accepted_plan_fingerprint=canonical_sha256(accepted_plan),
        result_folder_name=accepted_plan.result_folder_name,
        staged_data_commitment=staged_commitment,
        file_count=change_ledger.file_count,
        path_change_count=change_ledger.path_change_count,
        protected_file_count=change_ledger.protected_file_count,
        empty_directory_count=len(inventory.empty_directories),
        supported_link_count=change_ledger.supported_link_count,
        rewritten_link_count=change_ledger.rewritten_link_count,
        rewritten_markdown_file_count=(change_ledger.rewritten_markdown_file_count),
        checks=checks,
    )
    bagit_validation = PackageValidationResult(
        validator="bagit",
        valid=True,
        messages=('BagIt <passed & "checked">.',),
    )
    artifact_commitments = _artifact_commitments(
        inventory=inventory,
        user_request=user_request,
        evidence_ledger=evidence_ledger,
        accepted_plan=accepted_plan,
        reference_graph=reference_graph,
        path_rows=path_rows,
        change_ledger=change_ledger,
        report=report,
        source_markdown=source_markdown,
    )
    envelope = build_folder_receipt(
        job_id=JOB_ID,
        inventory=inventory,
        user_request=user_request,
        evidence_ledger=evidence_ledger,
        accepted_plan=accepted_plan,
        reference_graph=reference_graph,
        path_rows=path_rows,
        change_ledger=change_ledger,
        verification_report=report,
        artifact_commitments=artifact_commitments,
        staged_data_members=staged_data_members,
        staged_data_commitment=staged_commitment,
        producer_bagit_validation=bagit_validation,
    )
    return ReceiptFixture(
        inventory=inventory,
        user_request=user_request,
        evidence_ledger=evidence_ledger,
        accepted_plan=accepted_plan,
        reference_graph=reference_graph,
        path_rows=path_rows,
        change_ledger=change_ledger,
        verification_report=report,
        artifact_commitments=artifact_commitments,
        staged_data_members=staged_data_members,
        staged_data_commitment=staged_commitment,
        bagit_validation=bagit_validation,
        envelope=envelope,
    )


def _folder_file(path: str, data: bytes, *, protected: bool = False) -> FolderFile:
    digest = _sha256(data)
    return FolderFile(
        file_id=canonical_sha256(
            {
                "domain": "name-atlas:folder-file-id:v1",
                "original_relative_path": path,
                "payload_sha256": digest,
                "size": len(data),
            }
        ),
        relative_path=path,
        size=len(data),
        sha256=digest,
        protected=protected,
        evidence_eligible=not protected,
        protection_reasons=("dotfile",) if protected else (),
    )


def _folder_evidence_ledger(
    *,
    provider_kind: str,
    inventory: FolderInventory,
    user_request: FolderUserRequestArtifact,
    accepted_plan: FolderAcceptedPlan,
    planner_plan: FolderPlan,
    initial_evidence: dict[str, object],
    initial_evidence_bytes: int,
    evidence_fingerprint: str,
) -> FolderEvidenceLedger:
    submit_plan = SubmitPlanCall(call_id="submit-1", plan=planner_plan)
    evidence_state = PlannerEvidenceState(
        source_commitment=inventory.source_commitment,
        request_fingerprint=user_request.request_fingerprint,
        initial_evidence=initial_evidence,
        initial_evidence_bytes=initial_evidence_bytes,
        records=(),
        aggregate_result_bytes=0,
        total_outbound_evidence_bytes=initial_evidence_bytes,
        evidence_fingerprint=evidence_fingerprint,
    )
    turn_input = FolderPlannerTurnInput(
        job_id=JOB_ID,
        response_turn=1,
        provider_kind=provider_kind,
        request=user_request.request,
        request_fingerprint=user_request.request_fingerprint,
        source_commitment=inventory.source_commitment,
        evidence_ledger=evidence_state,
        prior_turns=(),
        compiler_failures=(),
    )
    input_payload = turn_input.model_dump(mode="json")
    returned_model = MODEL_ID if provider_kind in {"live", "recorded_replay"} else None
    turn_values = {
        "response_turn": 1,
        "provider_kind": provider_kind,
        "returned_model": returned_model,
        "observable_output_items": (),
        "tool_calls": (submit_plan,),
        "blocker_code": None,
        "input_bytes": len(canonical_json_bytes(input_payload)),
        "input_fingerprint": canonical_sha256(input_payload),
        "input_payload": input_payload,
    }
    response_payload = {
        "blocker_code": None,
        "input_bytes": turn_values["input_bytes"],
        "input_fingerprint": turn_values["input_fingerprint"],
        "input_payload": input_payload,
        "observable_output_items": [],
        "provider_kind": provider_kind,
        "response_turn": 1,
        "returned_model": returned_model,
        "tool_calls": [submit_plan.model_dump(mode="json")],
    }
    turn = PlannerObservableTurn(
        **turn_values,
        response_fingerprint=canonical_sha256(response_payload),
    )
    assert turn.response_fingerprint == canonical_sha256(observable_turn_payload(turn))

    values = {
        "schema_version": "folder-evidence-ledger.v1",
        "job_id": JOB_ID,
        "source_commitment": inventory.source_commitment,
        "request_fingerprint": user_request.request_fingerprint,
        "request_scope": accepted_plan.request_scope,
        "model_alias": "gpt-5.6",
        "provider_kind": provider_kind,
        "returned_model_ids": (returned_model,) if returned_model else (),
        "store_false": True if provider_kind == "live" else None,
        "initial_evidence": initial_evidence,
        "initial_evidence_bytes": initial_evidence_bytes,
        "evidence_records": (),
        "aggregate_result_bytes": 0,
        "total_outbound_evidence_bytes": initial_evidence_bytes,
        "evidence_fingerprint": evidence_fingerprint,
        "observable_turns": (turn,),
        "compiler_failures": (),
        "response_turn_count": 1,
        "evidence_call_count": 0,
        "plan_submission_count": 1,
        "clarification_question": None,
        "clarification_answer": None,
        "accepted_plan_fingerprint": canonical_sha256(accepted_plan),
        "usage": (
            (
                FolderPlannerUsage(
                    response_turn=1,
                    input_tokens=100,
                    output_tokens=20,
                    cached_input_tokens=0,
                    reasoning_tokens=5,
                    total_tokens=120,
                    latency_ms=25.0,
                    estimated_cost_microusd=1_100,
                ),
            )
            if provider_kind == "live"
            else ()
        ),
    }
    draft = FolderEvidenceLedger.model_construct(
        **values,
        transcript_fingerprint="0" * 64,
    )
    transcript_payload = draft.model_dump(
        mode="json",
        exclude={"transcript_fingerprint"},
    )
    return FolderEvidenceLedger(
        **values,
        transcript_fingerprint=canonical_sha256(transcript_payload),
    )


def _artifact_commitments(
    *,
    inventory: FolderInventory,
    user_request: FolderUserRequestArtifact,
    evidence_ledger: FolderEvidenceLedger,
    accepted_plan: FolderAcceptedPlan,
    reference_graph: FolderReferenceGraph,
    path_rows: tuple[FolderPathMapRow, ...],
    change_ledger: FolderChangeLedger,
    report: FolderVerificationReport,
    source_markdown: FolderFile,
) -> tuple[FolderArtifactCommitment, ...]:
    exact_bytes = {
        ACCEPTED_PLAN_PATH: canonical_portable_json_bytes(accepted_plan),
        BAG_INFO_PATH: b"Bag-Software-Agent: Reversible Name Atlas\n",
        BAGIT_PATH: (b"BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n"),
        CHANGE_LEDGER_PATH: canonical_portable_json_bytes(change_ledger),
        EVIDENCE_LEDGER_PATH: canonical_portable_json_bytes(evidence_ledger),
        FORWARD_PATH_MAP_PATH: render_forward_path_map_csv(path_rows),
        PAYLOAD_MANIFEST_PATH: b"0" * 64 + b"  data/.env\n",
        REFERENCE_GRAPH_PATH: canonical_portable_json_bytes(reference_graph),
        REVERSE_PATH_MAP_PATH: render_reverse_path_map_csv(path_rows),
        SOURCE_SNAPSHOT_PATH: canonical_portable_json_bytes(inventory),
        USER_REQUEST_PATH: canonical_portable_json_bytes(user_request),
        VERIFICATION_REPORT_PATH: canonical_portable_json_bytes(report),
    }
    commitments = [_commitment(path, data) for path, data in exact_bytes.items()]
    commitments.append(
        FolderArtifactCommitment(
            path=f"name-atlas/original-content/{source_markdown.file_id}.bin",
            size=source_markdown.size,
            sha256=source_markdown.sha256,
        )
    )
    return tuple(sorted(commitments, key=lambda item: item.path))


def _rebuild_receipt(
    fixture: ReceiptFixture,
    **updates: object,
) -> FolderReceiptEnvelope:
    values = {
        "job_id": JOB_ID,
        "inventory": fixture.inventory,
        "user_request": fixture.user_request,
        "evidence_ledger": fixture.evidence_ledger,
        "accepted_plan": fixture.accepted_plan,
        "reference_graph": fixture.reference_graph,
        "path_rows": fixture.path_rows,
        "change_ledger": fixture.change_ledger,
        "verification_report": fixture.verification_report,
        "artifact_commitments": fixture.artifact_commitments,
        "staged_data_members": fixture.staged_data_members,
        "staged_data_commitment": fixture.staged_data_commitment,
        "producer_bagit_validation": fixture.bagit_validation,
    }
    values.update(updates)
    return build_folder_receipt(**values)  # type: ignore[arg-type]


def _commitment(path: str, data: bytes) -> FolderArtifactCommitment:
    return FolderArtifactCommitment(
        path=path,
        size=len(data),
        sha256=_sha256(data),
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
