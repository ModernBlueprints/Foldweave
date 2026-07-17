"""Focused connected M1 transaction through Atlas, Decisions, and Proof."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
import pytest

from name_atlas import workflow as workflow_module
from name_atlas.app import create_app
from name_atlas.config import RuntimeConfig
from name_atlas.decision_cards import (
    BudgetLedgerError,
    DecisionCardCapExhaustedError,
    RecordedDecisionCard,
    RecordedReplayDecisionCardProvider,
    ReplayRecordWriteError,
    ReplayUsage,
    UnknownEvidenceIdError,
    evidence_fingerprint,
    load_recorded_decision_card,
)
from name_atlas.decisions import DecisionError, HumanAction
from name_atlas.domain import (
    CandidateExplanation,
    DecisionCard,
    EvidencePacket,
    LinkedObservation,
    RunMode,
)
from name_atlas.staging import StagingError
from name_atlas.verification import BagItPackageValidator
from name_atlas.workflow import WorkflowSession

HERO_ROOT = Path(__file__).parents[1] / "sample_data" / "hero"


class FakeDecisionCardProvider:
    """Deterministic test double that has no human or staging authority."""

    def __init__(self) -> None:
        self.packets: list[EvidencePacket] = []

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        self.packets.append(packet)
        evidence_id = packet.metadata_evidence[2].evidence_id
        observation = LinkedObservation(
            text="The source spelling may distinguish the intended Spanish term.",
            evidence_ids=(evidence_id,),
        )
        return DecisionCard(
            possible_interpretations=(observation,),
            possible_meaning_loss=(observation,),
            uncertainty="The bounded evidence cannot establish semantic intent.",
            why_the_distinction_matters=(
                "The descriptor remains visible after repository ingest."
            ),
            discriminating_question=(
                "Which supplied descriptor preserves the archivist's intended meaning?"
            ),
            candidate_explanations=(
                CandidateExplanation(
                    candidate_path=packet.candidate_paths[0],
                    explanation="This supplied candidate follows the fixed profile.",
                    evidence_ids=(evidence_id,),
                ),
            ),
        )


class FakeLiveDecisionCardProvider(FakeDecisionCardProvider):
    """Live-labelled test double for cap accounting without network I/O."""

    provider_kind = "live"

    def __init__(self) -> None:
        super().__init__()
        self.last_record: RecordedDecisionCard | None = None

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        card = await super().generate(packet)
        self.last_record = RecordedDecisionCard(
            model="gpt-5.6",
            schema_version="decision-card.v1",
            evidence_fingerprint=evidence_fingerprint(packet),
            generated_at=datetime.now(tz=ZoneInfo("Europe/Oslo")),
            decision_card=card,
            usage=ReplayUsage(
                input_tokens=100,
                cached_input_tokens=0,
                output_tokens=50,
                reasoning_tokens=10,
                total_tokens=150,
                latency_ms=25.0,
                estimated_cost_usd=0.002,
            ),
        )
        return card


class RecordingLiveDecisionCardProvider(FakeLiveDecisionCardProvider):
    """Live-labelled double that exposes the exact sanitized replay record."""


class MismatchedRecordingLiveProvider(FakeLiveDecisionCardProvider):
    """Expose a stale replay record despite returning a valid current card."""

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        card = await super().generate(packet)
        assert self.last_record is not None
        self.last_record = self.last_record.model_copy(
            update={"evidence_fingerprint": "f" * 64}
        )
        return card


class InvalidDecisionCardProvider(FakeDecisionCardProvider):
    """Return a typed card that violates the submitted evidence boundary."""

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        card = await super().generate(packet)
        invalid = LinkedObservation(
            text="This observation cites invented evidence.",
            evidence_ids=("metadata:invented",),
        )
        return card.model_copy(update={"possible_interpretations": (invalid,)})


def _write_low_risk_package(root: Path) -> None:
    (root / "objects").mkdir(parents=True)
    (root / "metadata").mkdir()
    (root / "objects" / "poster.svg").write_text("poster", encoding="utf-8")
    (root / "metadata" / "metadata.csv").write_text(
        "filename,dc.identifier,dc.title\n"
        "objects/poster.svg,LOW-0001,Ordinary poster\n",
        encoding="utf-8",
    )


def _write_meaning_risk_package(root: Path) -> None:
    (root / "objects").mkdir(parents=True)
    (root / "metadata").mkdir()
    (root / "objects" / "campaña.svg").write_text("campaign", encoding="utf-8")
    (root / "metadata" / "metadata.csv").write_text(
        "filename,dc.identifier,dc.title\nobjects/campaña.svg,MEAN-0001,Campaña\n",
        encoding="utf-8",
    )


def _write_long_metadata_package(root: Path) -> tuple[str, str]:
    (root / "objects").mkdir(parents=True)
    (root / "metadata").mkdir()
    (root / "objects" / "campaña.svg").write_text("campaign", encoding="utf-8")
    long_value = "description-" + "x" * 4_100
    long_header = "custom-" + "h" * 180
    (root / "metadata" / "metadata.csv").write_text(
        f"filename,dc.identifier,dc.title,dc.description,{long_header}\n"
        f"objects/campaña.svg,MEAN-0001,Campaña,{long_value},\n",
        encoding="utf-8",
    )
    return long_value, long_header


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_connected_walking_skeleton_requires_model_then_human_then_proof(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    shutil.copytree(HERO_ROOT, source)
    source_before = {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    }
    provider = FakeDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
    )
    family_id = next(
        family.family_id
        for family in workflow.package.families
        if family.canonical_identifier == "NA-0001"
    )
    collision_family_id = next(
        family.family_id
        for family in workflow.package.families
        if family.canonical_identifier == "CASE-010"
    )
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config, workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
        follow_redirects=True,
    ) as client:
        initial = await client.get("/")
        initial_view = workflow.view_model()
        missing_proof_artifact = await client.get(
            "/proof-artifacts/name-atlas/verification_report.json"
        )
        premature_stage = await client.post("/stage")
        generated = await client.post(f"/families/{family_id}/generate")
        approved = await client.post(f"/families/{family_id}/approve")
        first_batch = await client.post("/approve-low-risk")
        edited_collision = await client.post(
            f"/families/{collision_family_id}/edit",
            content=b"descriptor=harbor-map-north",
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        second_batch = await client.post("/approve-low-risk")
        staged = await client.post("/stage")
        proof_artifact = await client.get(
            "/proof-artifacts/name-atlas/verification_report.json"
        )
        unknown_artifact = await client.get(
            "/proof-artifacts/data/objects/NA-0001__campana__original.svg"
        )

    assert initial.status_code == 200
    assert "Campaña poster" in initial.text
    assert "Repository-ready identity profile" in initial.text
    assert "What GPT-5.6 will see" in initial.text
    assert "Mechanical blocker" in initial.text
    assert "Mechanical blocker; no model call" in initial.text
    assert "Transformation trace, risks, and affected links" in initial.text
    assert "Approve 9 eligible low-risk families" in initial.text
    assert initial_view["eligible_low_risk_count"] == 9
    assert {
        item["family"].canonical_identifier for item in initial_view["decision_items"]
    } == {"NA-0001", "CASE-010", "case-010"}
    assert missing_proof_artifact.status_code == 404
    assert "Blocked · action required" in premature_stage.text
    assert "GPT is advisory" in generated.text
    assert "Possible interpretations" in generated.text
    assert "The source spelling may distinguish the intended Spanish term." in (
        generated.text
    )
    assert "The descriptor remains visible after repository ingest." in generated.text
    assert provider.packets[0].candidate_paths[0] in generated.text
    assert provider.packets[0].metadata_evidence[2].evidence_id in generated.text
    assert len(provider.packets) == 1
    assert workflow.decisions[family_id].export_ready is True
    assert "Stored state:" in approved.text
    assert "low-risk families" in first_batch.text
    assert "Human descriptor stored" in edited_collision.text
    assert "low-risk families" in second_batch.text
    assert "Verified round-trip integrity within the supported package contract" in (
        staged.text
    )
    assert workflow.stage_result is not None
    assert workflow.stage_result.artifacts.report.map_row_count == 28
    resolved_view = workflow.view_model()
    assert resolved_view["eligible_low_risk_count"] == 0
    assert {
        item["family"].canonical_identifier for item in resolved_view["decision_items"]
    } == {"NA-0001", "CASE-010"}
    assert proof_artifact.status_code == 200
    assert proof_artifact.json()["claim"] == (
        "Verified round-trip integrity within the supported package contract"
    )
    assert unknown_artifact.status_code == 404
    assert "Proof artifacts" in staged.text
    assert "name-atlas/verification_report.json" in staged.text
    assert BagItPackageValidator().validate(workflow.stage_result.stage_root).valid
    assert {
        path.relative_to(source).as_posix(): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    } == source_before


@pytest.mark.anyio
async def test_low_risk_batch_approval_makes_no_provider_call(
    tmp_path: Path,
) -> None:
    source = tmp_path / "low-risk"
    _write_low_risk_package(source)
    provider = FakeDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
    )
    family_id = workflow.package.families[0].family_id

    view = workflow.view_model()
    item = view["families"][0]  # type: ignore[index]
    assert item["requires_card"] is False
    assert item["packet"] is None
    with pytest.raises(DecisionError, match="no mechanically flagged Meaning risk"):
        await workflow.generate_card(family_id)

    decisions = workflow.approve_low_risk()

    assert len(decisions) == 1
    assert decisions[0].export_ready
    assert provider.packets == []


@pytest.mark.anyio
async def test_low_risk_batch_never_overwrites_an_explicit_refusal(
    tmp_path: Path,
) -> None:
    source = tmp_path / "low-risk-refusal"
    _write_low_risk_package(source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=FakeDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
    )
    family_id = workflow.package.families[0].family_id
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config, workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
        follow_redirects=True,
    ) as client:
        initial = await client.get("/")
        refused = await client.post(f"/families/{family_id}/refuse")
        batch = await client.post("/approve-low-risk")

    assert "1 routine fixed-profile family still awaits" in initial.text
    assert workflow.view_model()["eligible_low_risk_count"] == 0
    assert workflow.decisions[family_id].action is HumanAction.REFUSED
    assert "Refused · export blocked" in refused.text
    assert "decision-state decision-state--red" in refused.text
    assert "Human refusal blocks the complete package" in refused.text
    assert "No unresolved low-risk families are eligible." in batch.text
    assert workflow.decisions[family_id].action is HumanAction.REFUSED


def test_supported_long_and_empty_metadata_is_visibly_bounded_for_gpt(
    tmp_path: Path,
) -> None:
    source = tmp_path / "long-metadata"
    long_value, long_header = _write_long_metadata_package(source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=FakeDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
    )
    family = workflow.package.families[0]

    packet = workflow.evidence_packet(family.family_id)
    rendered = workflow.view_model()
    description = next(
        item
        for item in packet.metadata_evidence
        if item.label.startswith("dc.description")
    )
    custom = next(
        item
        for item in packet.metadata_evidence
        if item.label.startswith(long_header[:30])
    )

    assert family.metadata_row.value("dc.description") == long_value
    assert len(description.value) == 4_000
    assert "truncated by Name Atlas" in description.value
    assert "visibly clipped" in description.label
    assert len(custom.label) <= 128
    assert custom.value == ""
    assert rendered["families"]


@pytest.mark.anyio
async def test_identical_evidence_hits_cache_and_changed_evidence_does_not(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning"
    _write_meaning_risk_package(source)
    provider = FakeDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
    )
    family_id = workflow.package.families[0].family_id

    first = await workflow.generate_card(family_id)
    repeated = await workflow.generate_card(family_id)
    decision = workflow.edit(family_id, "campana-reviewed")
    before_refresh = workflow.view_model()["families"][0]  # type: ignore[index]
    assert before_refresh["card_stale"] is True
    with pytest.raises(DecisionError, match="validated decision card"):
        workflow.approve(family_id)
    changed = await workflow.generate_card(family_id)

    assert first == repeated
    assert changed != first
    assert all(
        proposal.transformation_steps[-1].after
        == decision.resolved_targets[proposal.role]
        for proposal in workflow.proposals
    )
    assert len(provider.packets) == 2
    assert provider.packets[0] != provider.packets[1]
    metrics = workflow.view_model()["decision_metrics"]
    assert metrics["cards_requested"] == 3  # type: ignore[index]
    assert metrics["cache_hits"] == 1  # type: ignore[index]


@pytest.mark.anyio
async def test_live_call_cap_cannot_overwrite_human_decision(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning"
    _write_meaning_risk_package(source)
    provider = FakeLiveDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
        live_call_cap=1,
    )
    family_id = workflow.package.families[0].family_id

    await workflow.generate_card(family_id)
    workflow.edit(family_id, "campana-reviewed")
    with pytest.raises(DecisionCardCapExhaustedError, match="cap is exhausted"):
        await workflow.generate_card(family_id)

    assert len(provider.packets) == 1
    assert workflow.live_calls_made == 1
    assert workflow.decisions[family_id].action is HumanAction.EDITED


@pytest.mark.anyio
async def test_cost_cap_exhaustion_stays_unresolved(tmp_path: Path) -> None:
    source = tmp_path / "meaning-cost-cap"
    _write_meaning_risk_package(source)
    provider = FakeLiveDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
        cost_cap_usd=0.1,
    )
    family_id = workflow.package.families[0].family_id

    with pytest.raises(DecisionCardCapExhaustedError, match="cost cap"):
        await workflow.generate_card(family_id)

    assert provider.packets == []
    assert workflow.live_calls_made == 0
    assert workflow.decisions[family_id].action is HumanAction.UNRESOLVED


@pytest.mark.anyio
async def test_workflow_revalidates_provider_output_before_authority(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning-invalid-provider"
    _write_meaning_risk_package(source)
    provider = InvalidDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
    )
    family_id = workflow.package.families[0].family_id

    with pytest.raises(UnknownEvidenceIdError):
        await workflow.generate_card(family_id)

    assert family_id not in workflow.cards
    assert workflow.decisions[family_id].action is HumanAction.UNRESOLVED


@pytest.mark.anyio
async def test_live_budget_reservation_survives_workflow_restart(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning-restart"
    ledger_path = tmp_path / "api_budget.json"
    _write_meaning_risk_package(source)
    first_provider = FakeLiveDecisionCardProvider()
    first = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "first-output",
        decision_card_provider=first_provider,
        package_validator=BagItPackageValidator(),
        budget_ledger_path=ledger_path,
        live_call_cap=1,
    )
    family_id = first.package.families[0].family_id
    await first.generate_card(family_id)

    second_provider = FakeLiveDecisionCardProvider()
    restarted = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "second-output",
        decision_card_provider=second_provider,
        package_validator=BagItPackageValidator(),
        budget_ledger_path=ledger_path,
        live_call_cap=1,
    )

    with pytest.raises(DecisionCardCapExhaustedError, match="cap is exhausted"):
        await restarted.generate_card(family_id)

    assert first_provider.packets
    assert second_provider.packets == []
    assert restarted.committed_live_cost_usd > 0


@pytest.mark.anyio
async def test_replay_record_is_atomic_immutable_and_not_blocked_by_stale_temp(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning-record"
    _write_meaning_risk_package(source)
    record_path = tmp_path / "recordings" / "hero_decision_card.json"
    record_path.parent.mkdir()
    stale_legacy_temp = record_path.with_suffix(".json.tmp")
    stale_legacy_temp.write_text("interrupted old temporary", encoding="utf-8")
    provider = RecordingLiveDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
        replay_record_path=record_path,
    )
    family_id = workflow.package.families[0].family_id

    await workflow.generate_card(family_id)
    first_record_bytes = record_path.read_bytes()
    first_record = load_recorded_decision_card(first_record_bytes)
    await workflow.generate_card(family_id)

    assert first_record.evidence_fingerprint == evidence_fingerprint(
        provider.packets[0]
    )
    assert record_path.read_bytes() == first_record_bytes
    assert workflow.replay_record_error is None

    workflow.edit(family_id, "campana-reviewed")
    await workflow.generate_card(family_id)

    assert record_path.read_bytes() == first_record_bytes
    assert workflow.replay_record_error is None
    assert len(provider.packets) == 2


@pytest.mark.anyio
async def test_record_write_failure_retries_without_second_provider_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "meaning-record-retry"
    _write_meaning_risk_package(source)
    record_path = tmp_path / "recordings" / "hero_decision_card.json"
    provider = RecordingLiveDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
        replay_record_path=record_path,
    )
    family_id = workflow.package.families[0].family_id
    original_link = workflow_module.os.link

    def fail_link(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise OSError("injected replay promotion failure")

    monkeypatch.setattr(workflow_module.os, "link", fail_link)
    with pytest.raises(ReplayRecordWriteError, match="retrying"):
        await workflow.generate_card(family_id)

    assert len(provider.packets) == 1
    assert workflow.live_calls_made == 1
    assert family_id not in workflow.cards
    monkeypatch.setattr(workflow_module.os, "link", original_link)

    await workflow.generate_card(family_id)

    assert len(provider.packets) == 1
    assert workflow.live_calls_made == 1
    assert record_path.is_file()
    assert family_id in workflow.cards


@pytest.mark.anyio
async def test_live_baseline_record_replays_in_a_fresh_session(tmp_path: Path) -> None:
    source = tmp_path / "meaning-fresh-replay"
    _write_meaning_risk_package(source)
    record_path = tmp_path / "recordings" / "hero_decision_card.json"
    live_provider = RecordingLiveDecisionCardProvider()
    live = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "live-output",
        decision_card_provider=live_provider,
        package_validator=BagItPackageValidator(),
        replay_record_path=record_path,
    )
    family_id = live.package.families[0].family_id
    live_card = await live.generate_card(family_id)

    replay_provider = RecordedReplayDecisionCardProvider(record_path.read_bytes())
    replay = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "replay-output",
        decision_card_provider=replay_provider,
        package_validator=BagItPackageValidator(),
        replay_record_path=record_path,
    )
    replay.require_replay_record_compatible()

    assert await replay.generate_card(family_id) == live_card
    assert replay.replay_cards_used == 1


@pytest.mark.anyio
async def test_incompatible_existing_record_blocks_before_live_request(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning-incompatible-record"
    _write_meaning_risk_package(source)
    record_path = tmp_path / "recordings" / "hero_decision_card.json"
    record_path.parent.mkdir()
    packet_workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "temporary-output",
        decision_card_provider=FakeDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
    )
    packet = packet_workflow.evidence_packet(
        packet_workflow.package.families[0].family_id
    )
    packet_provider = FakeDecisionCardProvider()
    card = await packet_provider.generate(packet)
    mismatched = RecordedDecisionCard(
        model="gpt-5.6",
        schema_version="decision-card.v1",
        evidence_fingerprint="f" * 64,
        generated_at=datetime.now(tz=ZoneInfo("Europe/Oslo")),
        decision_card=card,
        usage=ReplayUsage(
            input_tokens=100,
            cached_input_tokens=0,
            output_tokens=50,
            reasoning_tokens=10,
            total_tokens=150,
            latency_ms=25.0,
            estimated_cost_usd=0.002,
        ),
    )
    record_path.write_text(mismatched.model_dump_json(), encoding="utf-8")
    provider = RecordingLiveDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
        replay_record_path=record_path,
    )
    family_id = workflow.package.families[0].family_id

    with pytest.raises(ReplayRecordWriteError, match="different evidence"):
        await workflow.generate_card(family_id)

    assert provider.packets == []
    assert workflow.live_calls_made == 0


@pytest.mark.anyio
async def test_live_record_must_match_the_current_packet_and_card(
    tmp_path: Path,
) -> None:
    source = tmp_path / "meaning-stale-live-record"
    _write_meaning_risk_package(source)
    provider = MismatchedRecordingLiveProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
    )
    family_id = workflow.package.families[0].family_id

    with pytest.raises(ReplayRecordWriteError, match="does not match"):
        await workflow.generate_card(family_id)

    assert family_id not in workflow.cards
    assert workflow.decisions[family_id].action is HumanAction.UNRESOLVED


@pytest.mark.anyio
async def test_reported_cost_failure_preserves_card_and_retries_without_api_call(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = tmp_path / "meaning-usage-retry"
    _write_meaning_risk_package(source)
    provider = RecordingLiveDecisionCardProvider()
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=provider,
        package_validator=BagItPackageValidator(),
    )
    family_id = workflow.package.families[0].family_id
    original_record_cost = workflow.budget_ledger.record_reported_cost

    def fail_reported_cost(value: float) -> object:
        del value
        raise BudgetLedgerError("injected usage ledger failure")

    monkeypatch.setattr(
        workflow.budget_ledger,
        "record_reported_cost",
        fail_reported_cost,
    )
    first = await workflow.generate_card(family_id)

    assert family_id in workflow.cards
    assert workflow.budget_reporting_error is not None
    assert len(provider.packets) == 1
    monkeypatch.setattr(
        workflow.budget_ledger,
        "record_reported_cost",
        original_record_cost,
    )

    repeated = await workflow.generate_card(family_id)

    assert repeated == first
    assert len(provider.packets) == 1
    assert workflow.budget_reporting_error is None


def test_failed_restage_clears_previous_green_proof(tmp_path: Path) -> None:
    source = tmp_path / "restage"
    _write_low_risk_package(source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=FakeDecisionCardProvider(),
        package_validator=BagItPackageValidator(),
    )
    workflow.approve_low_risk()
    workflow.stage()
    assert workflow.view_model()["proof"] is not None
    (source / "objects" / "poster.svg").write_text("changed", encoding="utf-8")

    with pytest.raises(StagingError, match="changed after the initial snapshot"):
        workflow.stage()

    assert workflow.stage_result is None
    assert workflow.view_model()["proof"] is None
