"""F0c protocol and boundary acceptance for hosted Foldweave MCP Apps."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest
from connected_change_fixtures import make_connected_change_fixture, tree_state
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp.exceptions import ToolError
from mcp.types import CallToolResult

from name_atlas.folder_refactor.connected_change.descriptors import (
    parse_connected_change_file_any,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    CapsuleAppliedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    GptDerivativeJobAuthorityV3,
    GptHostedJobAuthorityV3,
)
from name_atlas.folder_refactor.contracts import FolderPlan, FolderPlanEntry
from name_atlas.folder_refactor.foldweave_host_contracts import (
    FolderHostPlanRevisionEntryV1,
    FolderHostPlanRevisionV1,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.serialization import canonical_sha256
from name_atlas.foldweave_chatgpt_mcp import (
    CODEX_SERVER_INSTRUCTIONS,
    SERVER_INSTRUCTIONS,
    WIDGET_MIME_TYPE,
    WIDGET_RESOURCE_URI,
    _assert_safe_boundary,
    build_foldweave_chatgpt_server,
    build_foldweave_mcp_parser,
    run_foldweave_mcp_server,
)
from name_atlas.foldweave_host_service import FoldweaveHostPlanningService
from name_atlas.foldweave_launcher import run as run_foldweave
from name_atlas.foldweave_local_handles import FoldweaveLocalHandleStore
from name_atlas.foldweave_native_cli import compose_foldweave_native_app
from name_atlas.foldweave_paths import FoldweavePaths
from name_atlas.native_bridge import (
    NativeOpenResult,
    NativeOpenStatus,
    NativePathRole,
    NativePathSelection,
    NativeSelectionStatus,
)

oslo_tz = ZoneInfo("Europe/Oslo")

EXPECTED_TOOLS = {
    "choose_local_item",
    "create_or_resume_planning_job",
    "plan_change",
    "prepare_change_application",
    "list_inventory_page",
    "read_text_excerpt",
    "inspect_markdown_links",
    "request_clarification",
    "answer_clarification",
    "submit_plan",
    "get_compiler_failures",
    "revise_plan",
    "submit_plan_revision",
    "get_plan_preview",
    "job_status",
    "keep_previous_proposal",
    "accept_plan_and_create_copy",
    "get_change_file",
    "verify_result",
    "recreate_original",
}
READ_ONLY_TOOLS = {
    "get_compiler_failures",
    "get_change_file",
    "get_plan_preview",
    "job_status",
    "verify_result",
}
WIDGET_CALLABLE_TOOLS = {
    "get_change_file",
    "get_plan_preview",
    "job_status",
    "keep_previous_proposal",
    "accept_plan_and_create_copy",
    "verify_result",
    "recreate_original",
}
MODEL_ONLY_TOOLS = {
    "choose_local_item",
    "create_or_resume_planning_job",
    "plan_change",
    "prepare_change_application",
    "list_inventory_page",
    "read_text_excerpt",
    "inspect_markdown_links",
    "request_clarification",
    "answer_clarification",
    "submit_plan",
    "get_compiler_failures",
    "revise_plan",
    "submit_plan_revision",
}
MODEL_AND_APP_TOOLS = {
    "get_plan_preview",
    "job_status",
    "keep_previous_proposal",
    "verify_result",
}
APP_ONLY_TOOLS = {
    "accept_plan_and_create_copy",
    "get_change_file",
    "recreate_original",
}


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def test_host_boundary_allows_relative_members_named_tmp() -> None:
    _assert_safe_boundary(
        {
            "relative_path": "drafts/tmp/layout.bin",
            "original_destination": "../drafts/tmp/layout.bin",
        }
    )


@dataclass(frozen=True, slots=True)
class HostedHarness:
    service: FoldweaveHostPlanningService
    server: Any
    handles: FoldweaveLocalHandleStore
    source_handle: str
    output_handle: str
    fixture: Any
    output_root: Path


def _harness(tmp_path: Path) -> HostedHarness:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    tokens = iter(tuple(character * 43 for character in "ABCDEFGHIJKL"))
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: next(tokens),
    )
    source_handle = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=fixture.sofia_root,
        channel="chatgpt_hosted",
    )
    output_handle = handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=output,
        channel="chatgpt_hosted",
    )
    service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        handle_store=handles,
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    return HostedHarness(
        service=service,
        server=build_foldweave_chatgpt_server(service),
        handles=handles,
        source_handle=source_handle.handle,
        output_handle=output_handle.handle,
        fixture=fixture,
        output_root=output,
    )


async def _call(server: Any, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = await server.call_tool(name, arguments)
    assert isinstance(result, CallToolResult)
    assert result.isError is False
    assert result.structuredContent is not None
    _assert_no_public_job_capability(result.model_dump(mode="json"))
    return result.structuredContent


def _assert_no_public_job_capability(value: Any) -> None:
    encoded = json.dumps(value, sort_keys=True, default=str)
    assert "fwjc_" not in encoded
    assert '"capability_id"' not in encoded
    assert '"capability_expires_at"' not in encoded
    assert "public_job_capability" not in encoded


def _plan_for(harness: HostedHarness, job_id: str) -> FolderPlan:
    job = harness.service.status(job_id)
    assert isinstance(job.authority, GptHostedJobAuthorityV3)
    return FolderPlan(
        source_commitment=job.source_inventory.source_commitment,
        request_fingerprint=job.authority.planning_state.request_fingerprint,
        request_scope="rename_and_move_every_file",
        evidence_fingerprint=(
            job.authority.planning_state.evidence_state.evidence_fingerprint
        ),
        result_folder_name=harness.fixture.result_name,
        entries=tuple(
            FolderPlanEntry(
                file_id=item.file_id,
                original_path=item.relative_path,
                proposed_target=harness.fixture.target_paths[item.relative_path],
                rationale="Organize the connected project for handoff.",
                evidence_ids=("initial_inventory",),
            )
            for item in job.source_inventory.files
            if not item.protected
        ),
        exclusions=(),
    )


async def _create_review(harness: HostedHarness, *, key: str) -> dict[str, Any]:
    started = await _call(
        harness.server,
        "plan_change",
        {
            "source_handle": harness.source_handle,
            "output_handle": harness.output_handle,
            "request": harness.fixture.request,
            "evidence_disclosure_acknowledged": True,
            "idempotency_key": key,
        },
    )
    plan = _plan_for(harness, started["job_id"])
    submitted = await _call(
        harness.server,
        "submit_plan",
        {
            "job_id": started["job_id"],
            "call_id": f"{key}-plan",
            "plan": plan.model_dump(mode="json"),
        },
    )
    assert submitted["lifecycle"] == "reviewing"
    return submitted


async def _accept_current_review(
    harness: HostedHarness,
    reviewed: dict[str, Any],
    *,
    key: str,
) -> dict[str, Any]:
    snapshot = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": reviewed["job_id"],
            "expected_revision": reviewed["job_revision"],
            "preview_fingerprint": reviewed["preview_fingerprint"],
        },
    )
    preview = snapshot["preview"]
    status = snapshot["status"]
    return await _call(
        harness.server,
        "accept_plan_and_create_copy",
        {
            "job_id": reviewed["job_id"],
            "proposal_revision": preview["proposal_revision"],
            "source_commitment": preview["source_commitment"],
            "imported_change_file_fingerprint": preview[
                "imported_change_file_fingerprint"
            ],
            "match_report_fingerprint": preview["match_report_fingerprint"],
            "authorization_context_fingerprint": status[
                "authorization_context_fingerprint"
            ],
            "expected_revision": status["job_revision"],
            "preview_fingerprint": status["preview_fingerprint"],
            "candidate_fingerprint": status["candidate_fingerprint"],
            "idempotency_key": key,
        },
    )


@pytest.mark.anyio
async def test_server_metadata_widget_resource_and_tool_bounds() -> None:
    server = build_foldweave_chatgpt_server()
    tools = await server.list_tools()
    assert {tool.name for tool in tools} == EXPECTED_TOOLS
    assert len(tools) == len(EXPECTED_TOOLS)
    assert MODEL_ONLY_TOOLS | MODEL_AND_APP_TOOLS | APP_ONLY_TOOLS == EXPECTED_TOOLS
    assert not MODEL_ONLY_TOOLS & MODEL_AND_APP_TOOLS
    assert not MODEL_ONLY_TOOLS & APP_ONLY_TOOLS
    assert not MODEL_AND_APP_TOOLS & APP_ONLY_TOOLS
    for tool in tools:
        assert tool.annotations is not None
        assert tool.annotations.readOnlyHint is (tool.name in READ_ONLY_TOOLS)
        assert tool.annotations.destructiveHint is False
        assert tool.annotations.idempotentHint is (tool.name != "choose_local_item")
        assert tool.annotations.openWorldHint is False
        assert tool.outputSchema is not None
        assert tool.outputSchema["additionalProperties"] is False
        assert tool.inputSchema["type"] == "object"
        assert "channel" not in tool.inputSchema.get("properties", {})
        input_properties = tool.inputSchema.get("properties", {})
        _assert_no_public_job_capability(
            {
                "description": tool.description,
                "input_schema": tool.inputSchema,
                "output_schema": tool.outputSchema,
                "meta": tool.meta,
            }
        )
        if tool.name == "recreate_original":
            assert set(input_properties) == {"job_id"}
            assert tool.inputSchema.get("required") == ["job_id"]
        if tool.name == "get_plan_preview":
            assert tool.meta is not None
            assert tool.meta["openai/outputTemplate"] == WIDGET_RESOURCE_URI
            assert tool.meta["ui"] == {
                "resourceUri": WIDGET_RESOURCE_URI,
                "visibility": ["model", "app"],
            }
        else:
            assert not tool.meta or "openai/outputTemplate" not in tool.meta
            assert tool.meta is not None
            if tool.name in MODEL_ONLY_TOOLS:
                assert tool.meta["ui"] == {"visibility": ["model"]}
                assert "openai/widgetAccessible" not in tool.meta
            elif tool.name in MODEL_AND_APP_TOOLS:
                assert tool.meta["ui"] == {"visibility": ["model", "app"]}
            else:
                assert tool.name in APP_ONLY_TOOLS
                assert tool.meta["ui"] == {"visibility": ["app"]}
        if tool.name in WIDGET_CALLABLE_TOOLS:
            assert tool.meta is not None
            assert tool.meta["openai/widgetAccessible"] is True

    resources = await server.list_resources()
    assert len(resources) == 1
    resource = resources[0]
    assert str(resource.uri) == WIDGET_RESOURCE_URI
    assert resource.mimeType == WIDGET_MIME_TYPE
    assert resource.meta["ui"] == {
        "csp": {"connectDomains": [], "resourceDomains": []},
        "prefersBorder": True,
    }
    assert resource.meta is not None
    assert resource.meta["openai/widgetCSP"] == {
        "connect_domains": [],
        "resource_domains": [],
    }
    contents = list(await server.read_resource(WIDGET_RESOURCE_URI))
    assert len(contents) == 1
    html = contents[0].content
    assert contents[0].mime_type == WIDGET_MIME_TYPE
    assert '<div id="foldweave-chatgpt-widget-root"></div>' in html
    assert '<script type="module">' in html
    assert "fw-chatgpt-widget" in html
    assert "ui/initialize" in html
    assert "ui/notifications/tool-result" in html
    assert '<script type="module" src=' not in html
    assert '<link rel="stylesheet"' not in html

    assert SERVER_INSTRUCTIONS.startswith("Foldweave never changes a selected source.")
    assert "Responses API" in SERVER_INSTRUCTIONS[:512]
    assert "receiver preparation" in SERVER_INSTRUCTIONS
    _assert_no_public_job_capability(SERVER_INSTRUCTIONS)
    _assert_no_public_job_capability(CODEX_SERVER_INSTRUCTIONS)
    assert "every inventory file whose protected flag is false" in SERVER_INSTRUCTIONS
    assert "even when evidence_eligible is false" in SERVER_INSTRUCTIONS
    assert "Omit protected files and explicit empty directories" in SERVER_INSTRUCTIONS
    assert "get_compiler_failures" in SERVER_INSTRUCTIONS
    assert "fresh call_id" in SERVER_INSTRUCTIONS
    assert "citation_evidence_id" in SERVER_INSTRUCTIONS
    assert "it can be initial_inventory or an evidence-record fingerprint" in (
        SERVER_INSTRUCTIONS
    )
    assert "Never use a call ID, file ID" in SERVER_INSTRUCTIONS
    assert "cite exactly initial_inventory" in SERVER_INSTRUCTIONS
    assert "unavailable after revise_plan" in SERVER_INSTRUCTIONS
    inventory_tool = next(tool for tool in tools if tool.name == "list_inventory_page")
    assert inventory_tool.outputSchema is not None
    assert "citation_evidence_id" in inventory_tool.outputSchema["required"]
    assert (
        "Exact evidence ID to copy into the current plan entry"
        in inventory_tool.outputSchema["properties"]["citation_evidence_id"][
            "description"
        ]
    )
    submit_plan_tool = next(tool for tool in tools if tool.name == "submit_plan")
    assert submit_plan_tool.description is not None
    assert "protected flag is false" in submit_plan_tool.description
    assert "evidence_eligible flag is false" in submit_plan_tool.description
    assert "Omit protected files" in submit_plan_tool.description
    assert "get_compiler_failures" in submit_plan_tool.description
    assert "fresh call_id" in submit_plan_tool.description
    revision_tool = next(tool for tool in tools if tool.name == "submit_plan_revision")
    assert revision_tool.description is not None
    assert "citation_evidence_id" in revision_tool.description
    assert "never substitute a file ID or call ID" in revision_tool.description
    assert '["initial_inventory"]' in revision_tool.description
    assert "Do not call evidence tools after" in revision_tool.description
    revision_schema = json.dumps(revision_tool.inputSchema, sort_keys=True)
    assert "identifies the member to revise and is never an evidence ID" in (
        revision_schema
    )
    assert 'use exactly [\\"initial_inventory\\"]' in revision_schema
    assert "never copy file_id or call_id" in revision_schema
    reserve_revision_tool = next(tool for tool in tools if tool.name == "revise_plan")
    assert reserve_revision_tool.description is not None
    assert '["initial_inventory"]' in reserve_revision_tool.description
    assert "Evidence tools become intentionally unavailable" in (
        reserve_revision_tool.description
    )


@pytest.mark.anyio
async def test_server_profiles_are_construction_owned_and_not_caller_selectable(
    tmp_path: Path,
) -> None:
    harness = _harness(tmp_path)
    chatgpt_server = build_foldweave_chatgpt_server(
        harness.service,
        surface="chatgpt_hosted",
    )
    codex_server = build_foldweave_chatgpt_server(
        harness.service,
        surface="codex_hosted",
    )

    assert chatgpt_server.instructions == SERVER_INSTRUCTIONS
    assert codex_server.instructions == CODEX_SERVER_INSTRUCTIONS
    assert "ChatGPT supplies model inference" in chatgpt_server.instructions
    assert "Codex supplies model inference" in codex_server.instructions

    for server in (chatgpt_server, codex_server):
        tools = await server.list_tools()
        for tool in tools:
            assert "channel" not in tool.inputSchema.get("properties", {})


@pytest.mark.anyio
async def test_public_job_capability_never_enters_mcp_outputs_or_projection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _harness(tmp_path)

    def fail_if_accessed(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("MCP must not access or project a raw job capability.")

    monkeypatch.setattr(
        harness.service,
        "public_job_capability",
        fail_if_accessed,
        raising=False,
    )

    started = await _call(
        harness.server,
        "plan_change",
        {
            "source_handle": harness.source_handle,
            "output_handle": harness.output_handle,
            "request": harness.fixture.request,
            "evidence_disclosure_acknowledged": True,
            "idempotency_key": "mcp-boundary-origin",
        },
    )
    _assert_no_public_job_capability(started)

    submitted = await _call(
        harness.server,
        "submit_plan",
        {
            "job_id": started["job_id"],
            "call_id": "mcp-boundary-plan",
            "plan": _plan_for(harness, started["job_id"]).model_dump(mode="json"),
        },
    )
    preview = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": started["job_id"],
            "expected_revision": submitted["job_revision"],
            "preview_fingerprint": submitted["preview_fingerprint"],
        },
    )
    status = await _call(
        harness.server,
        "job_status",
        {"job_id": started["job_id"]},
    )
    _assert_no_public_job_capability(preview)
    _assert_no_public_job_capability(status)


@pytest.mark.anyio
async def test_complete_hosted_origin_review_revision_accept_and_verify(
    tmp_path: Path,
) -> None:
    harness = _harness(tmp_path)
    source_before = tree_state(harness.fixture.sofia_root)
    start_arguments = {
        "source_handle": harness.source_handle,
        "output_handle": harness.output_handle,
        "request": harness.fixture.request,
        "evidence_disclosure_acknowledged": True,
        "idempotency_key": "f0c-origin",
    }
    started = await _call(harness.server, "plan_change", start_arguments)
    repeated = await _call(
        harness.server,
        "create_or_resume_planning_job",
        start_arguments,
    )
    assert repeated == started
    job_id = started["job_id"]
    assert started["lifecycle"] == "planning"
    assert started["direct_api_used"] is False
    assert started["direct_budget_reserved"] is False

    inventory = await _call(
        harness.server,
        "list_inventory_page",
        {"job_id": job_id, "call_id": "inventory-1", "page_size": 100},
    )
    assert inventory["result"]["items"]
    assert all("sha256" not in item for item in inventory["result"]["items"])
    assert inventory["evidence_fingerprint"] == (
        harness.service.status(
            job_id
        ).authority.planning_state.evidence_state.evidence_fingerprint
    )
    inventory_state = harness.service.status(
        job_id
    ).authority.planning_state.evidence_state
    assert inventory["permitted_evidence_ids"] == (
        "initial_inventory",
        *(record.fingerprint for record in inventory_state.records),
    )
    assert inventory["citation_evidence_id"] == "initial_inventory"
    assert inventory["citation_evidence_id"] in inventory["permitted_evidence_ids"]

    durable = harness.service.status(job_id)
    markdown = next(
        item
        for item in durable.source_inventory.files
        if item.relative_path == "notes/client-brief.md"
    )
    excerpt = await _call(
        harness.server,
        "read_text_excerpt",
        {
            "job_id": job_id,
            "call_id": "excerpt-1",
            "file_id": markdown.file_id,
            "start_byte": 0,
            "max_bytes": 16_384,
        },
    )
    assert excerpt["result"] is not None
    assert excerpt["evidence_fingerprint"] == (
        harness.service.status(
            job_id
        ).authority.planning_state.evidence_state.evidence_fingerprint
    )
    excerpt_state = harness.service.status(
        job_id
    ).authority.planning_state.evidence_state
    assert excerpt["permitted_evidence_ids"] == (
        "initial_inventory",
        *(record.fingerprint for record in excerpt_state.records),
    )
    assert excerpt["citation_evidence_id"] == excerpt_state.records[-1].fingerprint
    assert excerpt["citation_evidence_id"] in excerpt["permitted_evidence_ids"]
    links = await _call(
        harness.server,
        "inspect_markdown_links",
        {
            "job_id": job_id,
            "call_id": "links-1",
            "file_id": markdown.file_id,
            "page_size": 100,
        },
    )
    assert links["result"]["references"]
    assert links["evidence_fingerprint"] == (
        harness.service.status(
            job_id
        ).authority.planning_state.evidence_state.evidence_fingerprint
    )
    links_state = harness.service.status(job_id).authority.planning_state.evidence_state
    assert links["permitted_evidence_ids"] == (
        "initial_inventory",
        *(record.fingerprint for record in links_state.records),
    )
    assert links["citation_evidence_id"] == links_state.records[-1].fingerprint
    assert links["citation_evidence_id"] in links["permitted_evidence_ids"]

    clarification = await _call(
        harness.server,
        "request_clarification",
        {
            "job_id": job_id,
            "expected_revision": links["job_revision"],
            "question": "Should the approved material remain separate?",
            "idempotency_key": "clarification-question-1",
        },
    )
    assert clarification["lifecycle"] == "awaiting_clarification"
    clarification_again = await _call(
        harness.server,
        "request_clarification",
        {
            "job_id": job_id,
            "expected_revision": links["job_revision"],
            "question": "Should the approved material remain separate?",
            "idempotency_key": "clarification-question-1",
        },
    )
    assert clarification_again == clarification
    with pytest.raises(ToolError) as question_conflict:
        await harness.server.call_tool(
            "request_clarification",
            {
                "job_id": job_id,
                "expected_revision": links["job_revision"],
                "question": "Should all material be combined?",
                "idempotency_key": "clarification-question-1",
            },
        )
    assert "clarification_idempotency_conflict" in str(question_conflict.value)
    with pytest.raises(ToolError) as stale_answer:
        await harness.server.call_tool(
            "answer_clarification",
            {
                "job_id": job_id,
                "expected_revision": links["job_revision"],
                "question_fingerprint": clarification[
                    "clarification_question_fingerprint"
                ],
                "answer": "Yes, keep approved and research material separate.",
                "idempotency_key": "clarification-answer-stale",
            },
        )
    assert "clarification_binding_mismatch" in str(stale_answer.value)
    with pytest.raises(ToolError) as wrong_question:
        await harness.server.call_tool(
            "answer_clarification",
            {
                "job_id": job_id,
                "expected_revision": clarification["job_revision"],
                "question_fingerprint": "0" * 64,
                "answer": "Yes, keep approved and research material separate.",
                "idempotency_key": "clarification-answer-wrong-question",
            },
        )
    assert "clarification_binding_mismatch" in str(wrong_question.value)
    answered = await _call(
        harness.server,
        "answer_clarification",
        {
            "job_id": job_id,
            "expected_revision": clarification["job_revision"],
            "question_fingerprint": clarification["clarification_question_fingerprint"],
            "answer": "Yes, keep approved and research material separate.",
            "idempotency_key": "clarification-answer-1",
        },
    )
    assert answered["lifecycle"] == "planning"
    answered_again = await _call(
        harness.server,
        "answer_clarification",
        {
            "job_id": job_id,
            "expected_revision": clarification["job_revision"],
            "question_fingerprint": clarification["clarification_question_fingerprint"],
            "answer": "Yes, keep approved and research material separate.",
            "idempotency_key": "clarification-answer-1",
        },
    )
    assert answered_again == answered
    with pytest.raises(ToolError) as answer_conflict:
        await harness.server.call_tool(
            "answer_clarification",
            {
                "job_id": job_id,
                "expected_revision": clarification["job_revision"],
                "question_fingerprint": clarification[
                    "clarification_question_fingerprint"
                ],
                "answer": "No, combine all material.",
                "idempotency_key": "clarification-answer-1",
            },
        )
    assert "clarification_idempotency_conflict" in str(answer_conflict.value)

    status = await _call(harness.server, "job_status", {"job_id": job_id})
    assert status == answered
    plan = _plan_for(harness, job_id)
    submitted = await _call(
        harness.server,
        "submit_plan",
        {
            "job_id": job_id,
            "call_id": "plan-1",
            "plan": plan.model_dump(mode="json"),
        },
    )
    assert submitted["lifecycle"] == "reviewing"
    submitted_again = await _call(
        harness.server,
        "submit_plan",
        {
            "job_id": job_id,
            "call_id": "plan-1",
            "plan": plan.model_dump(mode="json"),
        },
    )
    assert submitted_again == submitted
    failures = await _call(
        harness.server,
        "get_compiler_failures",
        {"job_id": job_id},
    )
    assert failures["failures"] == ()

    review = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": job_id,
            "expected_revision": submitted["job_revision"],
            "preview_fingerprint": submitted["preview_fingerprint"],
        },
    )
    assert review["schema_version"] == "foldweave-chatgpt-review.v1"
    assert review["status"]["lifecycle"] == "reviewing"
    assert review["status"]["direct_api_used"] is False
    assert review["status"]["direct_budget_reserved"] is False
    assert not tuple(harness.output_root.iterdir())

    reviewed_job = harness.service.status(job_id)
    assert reviewed_job.candidate_plan is not None
    first = next(
        item for item in reviewed_job.candidate_plan.file_mappings if not item.protected
    )
    revision_reserved = await _call(
        harness.server,
        "revise_plan",
        {
            "job_id": job_id,
            "expected_revision": review["status"]["job_revision"],
            "candidate_fingerprint": review["status"]["candidate_fingerprint"],
            "preview_fingerprint": review["status"]["preview_fingerprint"],
            "instruction": "Place the first reviewed file in a revised folder.",
            "idempotency_key": "revision-1",
        },
    )
    assert revision_reserved["lifecycle"] == "revising"
    sparse = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=canonical_sha256(reviewed_job.candidate_plan),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=first.file_id,
                replacement_target_path=f"revised/{Path(first.target_path).name}",
                rationale="Apply the user's exact revision.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    revised = await _call(
        harness.server,
        "submit_plan_revision",
        {
            "job_id": job_id,
            "call_id": "revision-submit-1",
            "revision": sparse.model_dump(mode="json"),
        },
    )
    assert revised["lifecycle"] == "reviewing"
    assert revised["proposal_revision"] == 1
    revised_review = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": job_id,
            "expected_revision": revised["job_revision"],
            "preview_fingerprint": revised["preview_fingerprint"],
        },
    )
    assert revised_review["preview"]["proposal_revision"] == 1

    exact = revised_review["status"]
    preview = revised_review["preview"]
    acceptance_arguments = {
        "job_id": job_id,
        "proposal_revision": preview["proposal_revision"],
        "source_commitment": preview["source_commitment"],
        "imported_change_file_fingerprint": preview["imported_change_file_fingerprint"],
        "match_report_fingerprint": preview["match_report_fingerprint"],
        "authorization_context_fingerprint": exact["authorization_context_fingerprint"],
        "expected_revision": exact["job_revision"],
        "preview_fingerprint": exact["preview_fingerprint"],
        "candidate_fingerprint": exact["candidate_fingerprint"],
        "idempotency_key": "accept-1",
    }
    accepted = await _call(
        harness.server,
        "accept_plan_and_create_copy",
        acceptance_arguments,
    )
    assert accepted["status"]["lifecycle"] == "verified"
    assert accepted["result"]["source_unchanged"] is True
    accepted_retry = await _call(
        harness.server,
        "accept_plan_and_create_copy",
        acceptance_arguments,
    )
    assert accepted_retry == accepted
    conflicting_acceptance = {
        **acceptance_arguments,
        "candidate_fingerprint": "0" * 64,
    }
    with pytest.raises(ToolError):
        await harness.server.call_tool(
            "accept_plan_and_create_copy",
            conflicting_acceptance,
        )
    verification = await _call(
        harness.server,
        "verify_result",
        {
            "job_id": job_id,
            "organized_tree_commitment": accepted["result"][
                "organized_tree_commitment"
            ],
        },
    )
    assert verification["verification"] == "verified"
    assert verification["failed_check_ids"] == ()
    assert tree_state(harness.fixture.sofia_root) == source_before

    encoded = json.dumps(accepted, sort_keys=True)
    assert str(tmp_path) not in encoded
    assert "/Users/" not in encoded
    assert "api_key" not in encoded.lower()


@pytest.mark.anyio
async def test_receiver_prepare_and_reconstruct_are_model_free_and_retry_bound(
    tmp_path: Path,
) -> None:
    harness = _harness(tmp_path)
    sofia_before = tree_state(harness.fixture.sofia_root)
    martin_before = tree_state(harness.fixture.martin_root)

    origin_review = await _create_review(harness, key="shared-mcp-origin")
    origin = await _accept_current_review(
        harness,
        origin_review,
        key="shared-mcp-origin-accept",
    )
    assert origin["status"]["lifecycle"] == "verified"

    change_file = await _call(
        harness.server,
        "get_change_file",
        {"job_id": origin_review["job_id"]},
    )
    assert change_file["schema_version"] == "foldweave-change-file-result.v1"
    assert set(change_file) == {
        "schema_version",
        "job_id",
        "item",
        "change_file_fingerprint",
        "originating_receipt_fingerprint",
    }
    assert set(change_file["item"]) == {
        "schema_version",
        "handle",
        "role",
        "display_name",
        "expires_at",
    }
    assert change_file["item"]["role"] == "change_file"
    change_file_path = harness.handles.resolve(
        change_file["item"]["handle"],
        role=NativePathRole.CHANGE_FILE,
        channel="chatgpt_hosted",
    )
    parsed_change_file = parse_connected_change_file_any(change_file_path.read_bytes())
    assert (
        change_file["change_file_fingerprint"]
        == parsed_change_file.change_file_fingerprint
    )
    assert (
        change_file["originating_receipt_fingerprint"]
        == parsed_change_file.originating_receipt.receipt_fingerprint
    )
    assert str(change_file_path) not in json.dumps(change_file, default=str)

    receiver_output = tmp_path / "receiver-output"
    receiver_output.mkdir()
    martin_handle = harness.handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=harness.fixture.martin_root,
        channel="chatgpt_hosted",
    )
    receiver_output_handle = harness.handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=receiver_output,
        channel="chatgpt_hosted",
    )
    prepare_arguments = {
        "change_file_handle": change_file["item"]["handle"],
        "source_handle": martin_handle.handle,
        "output_handle": receiver_output_handle.handle,
        "idempotency_key": "shared-mcp-receiver",
    }
    receiver = await _call(
        harness.server,
        "prepare_change_application",
        prepare_arguments,
    )
    receiver_retry = await _call(
        harness.server,
        "prepare_change_application",
        prepare_arguments,
    )
    assert receiver_retry == receiver
    assert receiver["lifecycle"] == "reviewing"
    assert receiver["planning_basis"] == "none"
    assert receiver["model_transport"] == "none"
    assert receiver["execution_origin"] == "capsule_applied"
    assert receiver["direct_api_used"] is False
    assert receiver["direct_budget_reserved"] is False
    assert isinstance(
        harness.service.status(receiver["job_id"]).authority,
        CapsuleAppliedJobAuthorityV2,
    )
    assert not tuple(receiver_output.iterdir())

    receiver_review = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": receiver["job_id"],
            "expected_revision": receiver["job_revision"],
            "preview_fingerprint": receiver["preview_fingerprint"],
        },
    )
    assert receiver_review["journey"] == "apply"
    assert receiver_review["status"]["planning_basis"] == "none"
    assert receiver_review["status"]["model_transport"] == "none"
    assert receiver_review["status"]["execution_origin"] == "capsule_applied"
    assert (
        receiver_review["preview"]["source_commitment"]
        != (origin_review["source_commitment"])
    )

    accepted_receiver = await _accept_current_review(
        harness,
        receiver,
        key="shared-mcp-receiver-accept",
    )
    assert accepted_receiver["status"]["lifecycle"] == "verified"
    assert accepted_receiver["status"]["model_transport"] == "none"
    assert accepted_receiver["status"]["execution_origin"] == "capsule_applied"
    assert tree_state(harness.fixture.sofia_root) == sofia_before
    assert tree_state(harness.fixture.martin_root) == martin_before

    terminal_job = harness.service.status(receiver["job_id"])
    terminal_bytes = terminal_job.job_path.read_bytes()
    output_entries_before_restore = set(receiver_output.iterdir())
    restoration = await _call(
        harness.server,
        "recreate_original",
        {"job_id": receiver["job_id"]},
    )
    restored_path = harness.handles.resolve(
        restoration["item"]["handle"],
        role=NativePathRole.RESTORE_DESTINATION,
        channel="chatgpt_hosted",
    )
    assert restored_path.parent == receiver_output
    assert set(receiver_output.iterdir()) - output_entries_before_restore == {
        restored_path
    }
    assert (
        scan_folder(restored_path).inventory
        == scan_folder(harness.fixture.martin_root).inventory
    )
    assert (
        restoration["receipt_fingerprint"]
        == terminal_job.verified_artifacts.receipt_fingerprint
    )
    assert (
        restoration["source_commitment"]
        == terminal_job.source_inventory.source_commitment
    )
    assert restoration["restored_file_count"] == len(
        terminal_job.source_inventory.files
    )
    assert harness.service.status(receiver["job_id"]).job_path.read_bytes() == (
        terminal_bytes
    )

    restoration_retry = await _call(
        harness.server,
        "recreate_original",
        {"job_id": receiver["job_id"]},
    )
    assert restoration_retry == restoration
    assert set(receiver_output.iterdir()) - output_entries_before_restore == {
        restored_path
    }

    encoded = json.dumps(
        {
            "change_file": change_file,
            "receiver": receiver,
            "restoration": restoration,
        },
        default=str,
        sort_keys=True,
    )
    assert str(tmp_path) not in encoded
    assert "/Users/" not in encoded
    assert "api_key" not in encoded.lower()


@pytest.mark.anyio
async def test_mcp_receiver_hosted_derivative_rehydrates_and_verifies(
    tmp_path: Path,
) -> None:
    """MCP owns one complete hosted derivative while native rehydrates it."""

    harness = _harness(tmp_path)
    sofia_before = tree_state(harness.fixture.sofia_root)
    martin_before = tree_state(harness.fixture.martin_root)
    budget_ledger = tmp_path / "state" / "api_budget.json"
    budget_ledger.parent.mkdir(parents=True, exist_ok=True)
    budget_ledger.write_bytes(b'{"sentinel":"hosted-mcp-must-not-mutate"}\n')
    budget_before = budget_ledger.read_bytes()

    origin_review = await _create_review(harness, key="derivative-mcp-origin")
    origin = await _accept_current_review(
        harness,
        origin_review,
        key="derivative-mcp-origin-accept",
    )
    assert origin["status"]["lifecycle"] == "verified"
    origin_change = await _call(
        harness.server,
        "get_change_file",
        {"job_id": origin_review["job_id"]},
    )

    receiver_output = tmp_path / "receiver-derivative-output"
    receiver_output.mkdir()
    martin_handle = harness.handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=harness.fixture.martin_root,
        channel="chatgpt_hosted",
    )
    receiver_output_handle = harness.handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=receiver_output,
        channel="chatgpt_hosted",
    )
    receiver = await _call(
        harness.server,
        "prepare_change_application",
        {
            "change_file_handle": origin_change["item"]["handle"],
            "source_handle": martin_handle.handle,
            "output_handle": receiver_output_handle.handle,
            "idempotency_key": "derivative-mcp-receiver-parent",
        },
    )
    assert receiver["lifecycle"] == "reviewing"
    assert receiver["planning_basis"] == "none"
    assert receiver["model_transport"] == "none"
    assert receiver["direct_api_used"] is False
    assert receiver["direct_budget_reserved"] is False
    parent = harness.service.status(receiver["job_id"])
    parent_bytes = parent.job_path.read_bytes()
    assert not tuple(receiver_output.iterdir())

    revision_arguments = {
        "job_id": receiver["job_id"],
        "expected_revision": receiver["job_revision"],
        "candidate_fingerprint": receiver["candidate_fingerprint"],
        "preview_fingerprint": receiver["preview_fingerprint"],
        "instruction": "Move one matched file into Martin's hosted review folder.",
        "idempotency_key": "derivative-mcp-hosted-child",
    }
    child_pending = await _call(
        harness.server,
        "revise_plan",
        revision_arguments,
    )
    child_pending_retry = await _call(
        harness.server,
        "revise_plan",
        revision_arguments,
    )
    assert child_pending_retry == child_pending
    assert child_pending["job_id"] != receiver["job_id"]
    assert child_pending["lifecycle"] == "revising"
    assert child_pending["planning_basis"] == "derivative"
    assert child_pending["model_transport"] == "chatgpt_hosted"
    assert child_pending["execution_origin"] == "none"
    assert child_pending["direct_api_used"] is False
    assert child_pending["direct_budget_reserved"] is False
    assert parent.job_path.read_bytes() == parent_bytes

    pending_job = harness.service.status(child_pending["job_id"])
    assert isinstance(pending_job.authority, GptDerivativeJobAuthorityV3)
    editable = next(
        item
        for item in pending_job.authority.parent_binding.parent_candidate.file_mappings
        if not item.protected
    )
    sparse = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=(
            pending_job.authority.parent_binding.parent_candidate_fingerprint
        ),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=editable.file_id,
                replacement_target_path=(
                    "martin-hosted-review/"
                    f"{editable.file_id[:12]}-{Path(editable.target_path).name}"
                ),
                rationale="Apply Martin's exact hosted derivative instruction.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    submission_arguments = {
        "job_id": child_pending["job_id"],
        "call_id": "derivative-mcp-hosted-submission",
        "revision": sparse.model_dump(mode="json"),
    }
    revised = await _call(
        harness.server,
        "submit_plan_revision",
        submission_arguments,
    )
    revised_retry = await _call(
        harness.server,
        "submit_plan_revision",
        submission_arguments,
    )
    assert revised_retry == revised
    assert revised["lifecycle"] == "reviewing"
    assert revised["proposal_revision"] == 1
    assert revised["planning_basis"] == "derivative"
    assert revised["model_transport"] == "chatgpt_hosted"
    assert revised["execution_origin"] == "gpt_revised_from_change_file"
    assert revised["direct_api_used"] is False
    assert revised["direct_budget_reserved"] is False
    assert parent.job_path.read_bytes() == parent_bytes
    assert not tuple(receiver_output.iterdir())

    revised_job = harness.service.status(revised["job_id"])
    assert isinstance(revised_job.authority, GptDerivativeJobAuthorityV3)
    assert revised_job.authority.execution_origin is not None
    assert revised_job.authority.execution_origin.kind == "gpt_revised_from_change_file"
    assert revised_job.authority.execution_origin.model_transport == "chatgpt_hosted"
    assert revised_job.authority.execution_origin.api_used is False
    assert revised_job.authority.execution_origin.provider_call_count == 0
    assert revised_job.authority.execution_origin.store_false is None

    review = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": revised["job_id"],
            "expected_revision": revised["job_revision"],
            "preview_fingerprint": revised["preview_fingerprint"],
        },
    )
    assert (
        review["preview"]["compiled_candidate_fingerprint"]
        == (revised["candidate_fingerprint"])
    )
    assert review["preview"]["preview_fingerprint"] == (revised["preview_fingerprint"])
    assert (
        review["preview"]["imported_change_file_fingerprint"]
        == (origin_change["change_file_fingerprint"])
    )

    child_bytes_before_native = revised_job.job_path.read_bytes()
    native = compose_foldweave_native_app(
        source=None,
        output=None,
        job=None,
        job_id=revised["job_id"],
        mode="development",
        environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")},
    )
    assert native.job_path == revised_job.job_path
    native_service = native.app.state.folder_run_service
    native_checkpoint = native_service.rehydrate_web_checkpoint()
    assert native_checkpoint is not None
    assert native_checkpoint.lifecycle.value == "reviewing"
    assert native_checkpoint.review is not None
    assert native_checkpoint.review.job_id == revised["job_id"]
    assert native_checkpoint.review.job_revision == revised["job_revision"]
    assert (
        native_checkpoint.review.candidate_fingerprint
        == (revised["candidate_fingerprint"])
    )
    assert (
        native_checkpoint.review.preview_fingerprint == (revised["preview_fingerprint"])
    )
    assert revised_job.job_path.read_bytes() == child_bytes_before_native
    hosted_after_native = await _call(
        harness.server,
        "job_status",
        {"job_id": revised["job_id"]},
    )
    assert hosted_after_native == revised

    exact = review["status"]
    preview = review["preview"]
    acceptance_arguments = {
        "job_id": revised["job_id"],
        "proposal_revision": preview["proposal_revision"],
        "source_commitment": preview["source_commitment"],
        "imported_change_file_fingerprint": preview["imported_change_file_fingerprint"],
        "match_report_fingerprint": preview["match_report_fingerprint"],
        "authorization_context_fingerprint": exact["authorization_context_fingerprint"],
        "expected_revision": exact["job_revision"],
        "preview_fingerprint": exact["preview_fingerprint"],
        "candidate_fingerprint": exact["candidate_fingerprint"],
        "idempotency_key": "derivative-mcp-exact-acceptance",
    }
    accepted = await _call(
        harness.server,
        "accept_plan_and_create_copy",
        acceptance_arguments,
    )
    accepted_retry = await _call(
        harness.server,
        "accept_plan_and_create_copy",
        acceptance_arguments,
    )
    assert accepted_retry == accepted
    assert accepted["status"]["lifecycle"] == "verified"
    assert accepted["status"]["planning_basis"] == "derivative"
    assert accepted["status"]["model_transport"] == "chatgpt_hosted"
    assert accepted["status"]["execution_origin"] == "gpt_revised_from_change_file"
    assert accepted["result"] is not None

    verification = await _call(
        harness.server,
        "verify_result",
        {
            "job_id": revised["job_id"],
            "organized_tree_commitment": accepted["result"][
                "organized_tree_commitment"
            ],
        },
    )
    assert verification["verification"] == "verified"
    assert verification["failed_check_ids"] == ()
    assert (
        verification["organized_tree_commitment"]
        == (accepted["result"]["organized_tree_commitment"])
    )

    child_change = await _call(
        harness.server,
        "get_change_file",
        {"job_id": revised["job_id"]},
    )
    child_change_path = harness.handles.resolve(
        child_change["item"]["handle"],
        role=NativePathRole.CHANGE_FILE,
        channel="chatgpt_hosted",
    )
    parsed_child_change = parse_connected_change_file_any(
        child_change_path.read_bytes()
    )
    assert child_change["change_file_fingerprint"] == (
        parsed_child_change.change_file_fingerprint
    )
    assert (
        child_change["change_file_fingerprint"]
        == (accepted["result"]["change_file_fingerprint"])
    )
    assert (
        parsed_child_change.core.lineage.parent_change_file_fingerprint
        == (origin_change["change_file_fingerprint"])
    )

    terminal = harness.service.status(revised["job_id"])
    terminal_bytes = terminal.job_path.read_bytes()
    terminal_native_checkpoint = native_service.web_checkpoint()
    assert terminal_native_checkpoint is not None
    assert terminal_native_checkpoint.lifecycle.value == "verified"
    assert terminal_native_checkpoint.result is not None
    assert (
        terminal_native_checkpoint.result.receipt_fingerprint
        == (verification["receipt_fingerprint"])
    )
    assert (
        terminal_native_checkpoint.result.organized_tree_commitment
        == (verification["organized_tree_commitment"])
    )
    assert terminal.job_path.read_bytes() == terminal_bytes

    restoration = await _call(
        harness.server,
        "recreate_original",
        {"job_id": revised["job_id"]},
    )
    restoration_retry = await _call(
        harness.server,
        "recreate_original",
        {"job_id": revised["job_id"]},
    )
    assert restoration_retry == restoration
    restored_path = harness.handles.resolve(
        restoration["item"]["handle"],
        role=NativePathRole.RESTORE_DESTINATION,
        channel="chatgpt_hosted",
    )
    assert (
        scan_folder(restored_path).inventory
        == scan_folder(harness.fixture.martin_root).inventory
    )
    assert restoration["receipt_fingerprint"] == (verification["receipt_fingerprint"])
    assert restoration["source_commitment"] == (
        terminal.source_inventory.source_commitment
    )
    assert harness.service.status(revised["job_id"]).job_path.read_bytes() == (
        terminal_bytes
    )
    assert parent.job_path.read_bytes() == parent_bytes
    assert budget_ledger.read_bytes() == budget_before
    assert tree_state(harness.fixture.sofia_root) == sofia_before
    assert tree_state(harness.fixture.martin_root) == martin_before

    encoded = json.dumps(
        {
            "receiver": receiver,
            "revised": revised,
            "accepted": accepted,
            "verification": verification,
            "restoration": restoration,
        },
        default=str,
        sort_keys=True,
    )
    assert str(tmp_path) not in encoded
    assert "/Users/" not in encoded
    assert "api_key" not in encoded.lower()


@pytest.mark.anyio
async def test_native_receiver_rehydrates_into_hosted_mcp_derivative(
    tmp_path: Path,
) -> None:
    """A native receiver remains the exact parent continued through MCP."""

    harness = _harness(tmp_path)
    origin_review = await _create_review(
        harness,
        key="native-to-mcp-origin",
    )
    origin = await _accept_current_review(
        harness,
        origin_review,
        key="native-to-mcp-origin-accept",
    )
    assert origin["status"]["lifecycle"] == "verified"
    origin_change = await _call(
        harness.server,
        "get_change_file",
        {"job_id": origin_review["job_id"]},
    )
    change_file_path = harness.handles.resolve(
        origin_change["item"]["handle"],
        role=NativePathRole.CHANGE_FILE,
        channel="chatgpt_hosted",
    )

    receiver_output = tmp_path / "native-receiver-output"
    receiver_output.mkdir()
    receiver_job_path = tmp_path / "state" / "jobs" / "native-receiver.json"
    native = compose_foldweave_native_app(
        source=None,
        output=None,
        job=receiver_job_path,
        mode="development",
        environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")},
    )
    native_service = native.app.state.folder_run_service
    native_review = await native_service.apply_shared_change(
        change_file_path=change_file_path,
        source_root=harness.fixture.martin_root,
        output_parent=receiver_output,
    )
    native_preview = native_service.get_plan_preview(native_review.job_id)
    assert native.job_path == receiver_job_path.resolve(strict=True)
    assert native_review.job_revision == native_preview.expected_job_revision
    assert native_review.candidate_fingerprint == (
        native_preview.compiled_candidate_fingerprint
    )
    assert native_review.preview_fingerprint == native_preview.preview_fingerprint
    assert native_preview.source_commitment == (
        scan_folder(harness.fixture.martin_root).inventory.source_commitment
    )
    assert (
        native_preview.imported_change_file_fingerprint
        == (origin_change["change_file_fingerprint"])
    )
    parent_bytes = native.job_path.read_bytes()
    assert not tuple(receiver_output.iterdir())

    restarted_native = compose_foldweave_native_app(
        source=None,
        output=None,
        job=None,
        job_id=native_review.job_id,
        mode="development",
        environ={"FOLDWEAVE_STATE_ROOT": str(tmp_path / "state")},
    )
    restarted_checkpoint = (
        restarted_native.app.state.folder_run_service.rehydrate_web_checkpoint()
    )
    assert restarted_native.job_path == native.job_path
    assert restarted_checkpoint is not None
    assert restarted_checkpoint.lifecycle.value == "reviewing"
    assert restarted_checkpoint.review is not None
    assert restarted_checkpoint.review.job_revision == native_review.job_revision
    assert restarted_checkpoint.review.candidate_fingerprint == (
        native_review.candidate_fingerprint
    )
    assert restarted_checkpoint.review.preview_fingerprint == (
        native_review.preview_fingerprint
    )
    assert native.job_path.read_bytes() == parent_bytes

    restarted_host = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    restarted_server = build_foldweave_chatgpt_server(restarted_host)
    hosted_parent = await _call(
        restarted_server,
        "job_status",
        {"job_id": native_review.job_id},
    )
    hosted_preview = await _call(
        restarted_server,
        "get_plan_preview",
        {
            "job_id": native_review.job_id,
            "expected_revision": native_review.job_revision,
            "preview_fingerprint": native_review.preview_fingerprint,
        },
    )
    assert hosted_parent["lifecycle"] == "reviewing"
    assert hosted_parent["planning_basis"] == "none"
    assert hosted_parent["model_transport"] == "none"
    assert hosted_parent["job_revision"] == native_review.job_revision
    assert hosted_parent["candidate_fingerprint"] == (
        native_review.candidate_fingerprint
    )
    assert hosted_parent["preview_fingerprint"] == (native_review.preview_fingerprint)
    assert hosted_parent["source_commitment"] == native_preview.source_commitment
    assert hosted_preview["preview"]["compiled_candidate_fingerprint"] == (
        native_preview.compiled_candidate_fingerprint
    )
    assert hosted_preview["preview"]["preview_fingerprint"] == (
        native_preview.preview_fingerprint
    )
    assert hosted_preview["preview"]["source_commitment"] == (
        native_preview.source_commitment
    )
    assert hosted_preview["preview"]["imported_change_file_fingerprint"] == (
        native_preview.imported_change_file_fingerprint
    )
    assert native.job_path.read_bytes() == parent_bytes

    revision_arguments = {
        "job_id": native_review.job_id,
        "expected_revision": hosted_parent["job_revision"],
        "candidate_fingerprint": hosted_parent["candidate_fingerprint"],
        "preview_fingerprint": hosted_parent["preview_fingerprint"],
        "instruction": "Move one matched file into the continued hosted review.",
        "idempotency_key": "native-to-mcp-derivative",
    }
    child_pending = await _call(
        restarted_server,
        "revise_plan",
        revision_arguments,
    )
    child_pending_retry = await _call(
        restarted_server,
        "revise_plan",
        revision_arguments,
    )
    assert child_pending_retry == child_pending
    assert child_pending["job_id"] != native_review.job_id
    assert child_pending["lifecycle"] == "revising"
    assert child_pending["planning_basis"] == "derivative"
    assert child_pending["model_transport"] == "chatgpt_hosted"
    assert child_pending["source_commitment"] == native_preview.source_commitment
    assert native.job_path.read_bytes() == parent_bytes

    pending = restarted_host.status(child_pending["job_id"])
    assert isinstance(pending.authority, GptDerivativeJobAuthorityV3)
    assert pending.authority.parent_binding.parent_job_id == native_review.job_id
    assert pending.authority.parent_binding.parent_job_revision == (
        native_review.job_revision
    )
    assert pending.authority.parent_binding.parent_candidate_fingerprint == (
        native_review.candidate_fingerprint
    )
    assert pending.authority.parent_binding.parent_preview_fingerprint == (
        native_review.preview_fingerprint
    )
    assert pending.authority.parent_binding.imported_change_file_fingerprint == (
        native_preview.imported_change_file_fingerprint
    )
    editable = next(
        item
        for item in pending.authority.parent_binding.parent_candidate.file_mappings
        if not item.protected
    )
    sparse = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=(
            pending.authority.parent_binding.parent_candidate_fingerprint
        ),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=editable.file_id,
                replacement_target_path=(
                    "continued-hosted-review/"
                    f"{editable.file_id[:12]}-{Path(editable.target_path).name}"
                ),
                rationale="Continue the native receiver through hosted MCP.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    submission_arguments = {
        "job_id": child_pending["job_id"],
        "call_id": "native-to-mcp-derivative-submission",
        "revision": sparse.model_dump(mode="json"),
    }
    revised = await _call(
        restarted_server,
        "submit_plan_revision",
        submission_arguments,
    )
    revised_retry = await _call(
        restarted_server,
        "submit_plan_revision",
        submission_arguments,
    )
    assert revised_retry == revised
    assert revised["lifecycle"] == "reviewing"
    assert revised["planning_basis"] == "derivative"
    assert revised["model_transport"] == "chatgpt_hosted"
    assert revised["execution_origin"] == "gpt_revised_from_change_file"
    assert revised["source_commitment"] == native_preview.source_commitment
    assert revised["candidate_fingerprint"] != native_review.candidate_fingerprint
    assert revised["preview_fingerprint"] != native_review.preview_fingerprint
    assert native.job_path.read_bytes() == parent_bytes
    assert not tuple(receiver_output.iterdir())


@pytest.mark.anyio
async def test_fastmcp_polling_is_byte_read_only_after_source_mutation(
    tmp_path: Path,
) -> None:
    """All declared read-only hosted polling tools preserve durable job bytes."""

    harness = _harness(tmp_path)
    reviewed = await _create_review(harness, key="polling-read-only")
    job_id = reviewed["job_id"]
    job = harness.service.status(job_id)
    assert job.preview is not None
    job_bytes = job.job_path.read_bytes()

    changed_relative = next(
        item.relative_path for item in job.source_inventory.files if not item.protected
    )
    changed = harness.fixture.sofia_root / changed_relative
    changed.write_bytes(changed.read_bytes() + b"changed after review\n")

    status = await _call(harness.server, "job_status", {"job_id": job_id})
    assert status["lifecycle"] == "reviewing"
    preview = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": job_id,
            "expected_revision": reviewed["job_revision"],
            "preview_fingerprint": reviewed["preview_fingerprint"],
        },
    )
    assert preview["status"]["job_id"] == status["job_id"]
    assert preview["status"]["job_revision"] == status["job_revision"]
    assert preview["status"]["preview_fingerprint"] == status["preview_fingerprint"]
    failures = await _call(
        harness.server,
        "get_compiler_failures",
        {"job_id": job_id},
    )
    assert failures["failures"] == ()
    assert job.job_path.read_bytes() == job_bytes

    with pytest.raises(ToolError):
        await harness.server.call_tool(
            "revise_plan",
            {
                "job_id": job_id,
                "expected_revision": reviewed["job_revision"],
                "candidate_fingerprint": reviewed["candidate_fingerprint"],
                "preview_fingerprint": reviewed["preview_fingerprint"],
                "instruction": "Move the first file into a new folder.",
                "idempotency_key": "stale-mutation",
            },
        )
    stale = harness.service.status(job_id)
    assert stale.lifecycle.value == "stale"
    assert stale.staleness is not None
    assert stale.staleness.code == "source_changed"
    assert job.job_path.read_bytes() != job_bytes


@pytest.mark.anyio
async def test_failed_revision_keeps_and_rebinds_previous_preview(
    tmp_path: Path,
) -> None:
    harness = _harness(tmp_path)
    submitted = await _create_review(harness, key="failed-revision")
    job = harness.service.status(submitted["job_id"])
    assert job.candidate_plan is not None
    mutable = tuple(
        item for item in job.candidate_plan.file_mappings if not item.protected
    )
    first, second = mutable[:2]
    reserved = await _call(
        harness.server,
        "revise_plan",
        {
            "job_id": job.job_id,
            "expected_revision": submitted["job_revision"],
            "candidate_fingerprint": submitted["candidate_fingerprint"],
            "preview_fingerprint": submitted["preview_fingerprint"],
            "instruction": "Move the first file onto the second file's target.",
            "idempotency_key": "failed-revision-reserve",
        },
    )
    assert reserved["lifecycle"] == "revising"
    collision = FolderHostPlanRevisionV1(
        base_candidate_fingerprint=canonical_sha256(job.candidate_plan),
        entries=(
            FolderHostPlanRevisionEntryV1(
                file_id=first.file_id,
                replacement_target_path=second.target_path,
                rationale="Apply the requested target.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    failed = await _call(
        harness.server,
        "submit_plan_revision",
        {
            "job_id": job.job_id,
            "call_id": "failed-revision-submit",
            "revision": collision.model_dump(mode="json"),
        },
    )
    assert failed["lifecycle"] == "revision_failed"
    assert failed["revision_failure_code"] is not None
    failed_review = await _call(
        harness.server,
        "get_plan_preview",
        {
            "job_id": job.job_id,
            "expected_revision": failed["job_revision"],
            "preview_fingerprint": failed["preview_fingerprint"],
        },
    )
    assert failed_review["status"]["lifecycle"] == "revision_failed"
    assert failed_review["status"]["revision_failure"] is not None
    preview = failed_review["preview"]
    status = failed_review["status"]
    keep_arguments = {
        "job_id": job.job_id,
        "proposal_revision": preview["proposal_revision"],
        "source_commitment": preview["source_commitment"],
        "imported_change_file_fingerprint": preview["imported_change_file_fingerprint"],
        "match_report_fingerprint": preview["match_report_fingerprint"],
        "authorization_context_fingerprint": status[
            "authorization_context_fingerprint"
        ],
        "expected_revision": status["job_revision"],
        "preview_fingerprint": status["preview_fingerprint"],
        "candidate_fingerprint": status["candidate_fingerprint"],
        "idempotency_key": "keep-previous-1",
    }
    kept = await _call(
        harness.server,
        "keep_previous_proposal",
        keep_arguments,
    )
    assert kept["status"]["lifecycle"] == "reviewing"
    assert kept["status"]["revision_failure"] is None
    kept_retry = await _call(
        harness.server,
        "keep_previous_proposal",
        keep_arguments,
    )
    assert kept_retry == kept
    assert not tuple(harness.output_root.iterdir())


class _FixedNativeBridge:
    def __init__(self, selected: Path) -> None:
        self._selected = selected

    async def choose_path(self, role: NativePathRole) -> NativePathSelection:
        assert role is NativePathRole.SOURCE_FOLDER
        return NativePathSelection(
            status=NativeSelectionStatus.SELECTED,
            path=self._selected,
        )

    async def show_in_finder(self, path: Path) -> NativeOpenResult:
        del path
        return NativeOpenResult(status=NativeOpenStatus.OPENED)


@pytest.mark.anyio
async def test_local_selection_returns_only_an_opaque_handle(tmp_path: Path) -> None:
    selected = tmp_path / "private-project"
    selected.mkdir()
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: "Z" * 43,
    )
    service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        handle_store=handles,
        native_bridge=_FixedNativeBridge(selected),
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    result = await _call(
        build_foldweave_chatgpt_server(service),
        "choose_local_item",
        {"role": "source_folder"},
    )
    assert result["status"] == "selected"
    assert result["item"]["handle"] == f"fw_{'Z' * 43}"
    assert result["item"]["display_name"] == selected.name
    assert str(selected) not in json.dumps(result, default=str)


@pytest.mark.anyio
async def test_sensitive_excerpt_is_persisted_locally_but_not_returned(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    output.mkdir()
    fake_local_path = "/".join(("", "Users", "alice", "private.txt"))
    fake_project_key = "sk-proj-" + ("X" * 32)
    sensitive = f"Local {fake_local_path} and {fake_project_key}"
    (source / "note.md").write_text(sensitive, encoding="utf-8")
    tokens = iter(("X" * 43, "Y" * 43))
    handles = FoldweaveLocalHandleStore(
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
        token_factory=lambda: next(tokens),
    )
    source_handle = handles.register(
        role=NativePathRole.SOURCE_FOLDER,
        path=source,
        channel="chatgpt_hosted",
    )
    output_handle = handles.register(
        role=NativePathRole.OUTPUT_PARENT,
        path=output,
        channel="chatgpt_hosted",
    )
    service = FoldweaveHostPlanningService(
        paths=FoldweavePaths(state_root=tmp_path / "state"),
        handle_store=handles,
        clock=lambda: datetime(2026, 7, 19, 20, 0, tzinfo=oslo_tz),
    )
    server = build_foldweave_chatgpt_server(service)
    started = await _call(
        server,
        "plan_change",
        {
            "source_handle": source_handle.handle,
            "output_handle": output_handle.handle,
            "request": "Organize the note.",
            "evidence_disclosure_acknowledged": True,
            "idempotency_key": "sensitive-boundary",
        },
    )
    file_id = service.status(started["job_id"]).source_inventory.files[0].file_id
    with pytest.raises(ToolError) as error:
        await server.call_tool(
            "read_text_excerpt",
            {
                "job_id": started["job_id"],
                "call_id": "sensitive-excerpt",
                "file_id": file_id,
                "start_byte": 0,
                "max_bytes": 16_384,
            },
        )
    rendered = str(error.value)
    assert "local_path_disclosure_blocked" in rendered
    assert "/Users/alice" not in rendered
    assert "SUPERSECRETVALUE" not in rendered
    durable = service.status(started["job_id"])
    assert len(durable.authority.planning_state.evidence_state.records) == 1


def test_mcp_launcher_dispatch_and_loopback_transport(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import name_atlas.foldweave_chatgpt_mcp as module

    observed: dict[str, Any] = {}

    class _FakeServer:
        def run(self, *, transport: str) -> None:
            observed["transport"] = transport

    def build_fake(*, surface: str, host: str, port: int) -> _FakeServer:
        observed["surface"] = surface
        observed["host"] = host
        observed["port"] = port
        return _FakeServer()

    monkeypatch.setattr(module, "build_foldweave_chatgpt_server", build_fake)
    assert (
        run_foldweave_mcp_server(
            [
                "--transport",
                "streamable-http",
                "--host",
                "localhost",
                "--port",
                "8765",
            ]
        )
        == 0
    )
    assert observed == {
        "surface": "chatgpt_hosted",
        "host": "localhost",
        "port": 8765,
        "transport": "streamable-http",
    }
    observed.clear()
    assert run_foldweave_mcp_server(["--transport", "stdio"]) == 0
    assert observed == {
        "surface": "codex_hosted",
        "host": "127.0.0.1",
        "port": 8000,
        "transport": "stdio",
    }
    observed.clear()
    assert (
        run_foldweave_mcp_server(
            ["--transport", "stdio", "--surface", "chatgpt-hosted"]
        )
        == 0
    )
    assert observed == {
        "surface": "chatgpt_hosted",
        "host": "127.0.0.1",
        "port": 8000,
        "transport": "stdio",
    }
    monkeypatch.setattr(module, "run_foldweave_mcp_server", lambda argv: len(argv))
    assert run_foldweave(["mcp", "--transport", "stdio"]) == 2
    with pytest.raises(SystemExit):
        build_foldweave_mcp_parser().parse_args(["--host", "0.0.0.0"])


@pytest.mark.anyio
async def test_real_stdio_protocol_is_provider_free_and_path_safe(
    tmp_path: Path,
) -> None:
    environment = dict(os.environ)
    environment.pop("OPENAI_API_KEY", None)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    repository = Path(__file__).resolve().parents[1]
    stderr_path = tmp_path / "foldweave-mcp-stderr.log"
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "name_atlas.foldweave_launcher", "mcp"],
        cwd=str(repository),
        env=environment,
    )
    with stderr_path.open("w", encoding="utf-8") as stderr:
        async with stdio_client(parameters, errlog=stderr) as streams:
            read_stream, write_stream = streams
            async with ClientSession(read_stream, write_stream) as session:
                initialized = await session.initialize()
                assert initialized.instructions == CODEX_SERVER_INSTRUCTIONS
                listed = await session.list_tools()
                assert {tool.name for tool in listed.tools} == EXPECTED_TOOLS
                resources = await session.list_resources()
                assert len(resources.resources) == 1
                assert str(resources.resources[0].uri) == WIDGET_RESOURCE_URI
                widget = await session.read_resource(WIDGET_RESOURCE_URI)
                assert widget.contents[0].mimeType == WIDGET_MIME_TYPE
                assert "foldweave-chatgpt-widget-root" in widget.contents[0].text
                result = await session.call_tool(
                    "job_status",
                    {"job_id": "0" * 32},
                )
                assert result.isError is True
                text = " ".join(
                    item.text for item in result.content if hasattr(item, "text")
                )
                assert "job_handle_invalid" in text
                assert "/Users/" not in text
                assert "OPENAI_API_KEY" not in text

    assert stderr_path.read_text(encoding="utf-8") == ""


def test_mcp_module_has_no_direct_provider_or_budget_import() -> None:
    import name_atlas.foldweave_chatgpt_mcp as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    forbidden = (
        "foldweave_provider_factory",
        "api_budget",
        "OpenAI",
        "from openai",
        "import openai",
    )
    assert not tuple(item for item in forbidden if item in source)
