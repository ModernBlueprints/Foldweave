"""F0b provider-driven review, revision, and exact-execution evidence."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Literal

import pytest
from connected_change_fixtures import make_connected_change_fixture, tree_state

from name_atlas.decision_cards.budget import PersistentBudgetLedger
from name_atlas.folder_refactor.connected_change import (
    review_service as review_module,
)
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    GptPlannedJobAuthorityV3,
    canonical_job_v3_bytes,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FOLDWEAVE_F0B_CONTRACT_FREEZE,
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.demo_fixtures import (
    FOLDWEAVE_F0B_FIXTURE_FINGERPRINT,
    foldweave_f0b_fixture_fingerprint,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH,
    FolderEvidenceLedgerV2,
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
    build_execution_origin_v2,
)
from name_atlas.folder_refactor.live_planner_provider import (
    LiveFolderPlanRevisionProvider,
)
from name_atlas.folder_refactor.planner_provider import (
    DETERMINISTIC_DEVELOPMENT_REQUEST,
    DeterministicDevelopmentPlannerProvider,
    PlannerProviderResponseError,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
)


class _ScriptedRevisionProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self, revision: FolderPlanRevisionV1) -> None:
        self._revision = revision
        self.inputs: list[FolderPlannerRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.inputs.append(turn_input)
        return FolderRevisionProviderResponseV1(
            provider_kind="deterministic",
            call_id=f"revision-{len(self.inputs)}",
            revision=self._revision,
        )


class _FailingRevisionProvider:
    provider_kind: Literal["deterministic"] = "deterministic"

    def __init__(self) -> None:
        self.inputs: list[FolderPlannerRevisionTurnInputV1] = []

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return ()

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        self.inputs.append(turn_input)
        raise RuntimeError("The scripted provider did not return a revision.")


class _ForbiddenResponses:
    """Prove a missing contract binding fails before any client request."""

    def __init__(self) -> None:
        self.requests: list[object] = []

    async def create(self, **kwargs: object) -> object:
        self.requests.append(kwargs)
        raise AssertionError("The unbound revision must not reach the provider.")


@pytest.mark.anyio
async def test_f0b_scripted_initial_revision_accept_and_verify(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    job_path = tmp_path / "jobs" / "direct-review.json"
    source_before = tree_state(fixture.sofia_root)
    service = FoldweaveReviewService()

    reviewing = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=job_path,
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="f0b-scripted-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )

    assert reviewing.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert isinstance(reviewing.authority, GptPlannedJobAuthorityV3)
    assert reviewing.authority.evidence_ledger is not None
    assert reviewing.authority.execution_origin is not None
    assert reviewing.candidate_plan is not None
    assert reviewing.preview is not None
    assert reviewing.candidate_plan.evidence_schema_version == (
        "folder-evidence-ledger.v2"
    )
    assert reviewing.authority.evidence_ledger.contract_freeze_fingerprint == (
        FOLDWEAVE_F0B_CONTRACT_FREEZE.contract_freeze_fingerprint
    )
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.sofia_root) == source_before

    selected = next(
        item for item in reviewing.candidate_plan.file_mappings if not item.protected
    )
    revision = FolderPlanRevisionV1(
        base_candidate_fingerprint=(reviewing.preview.compiled_candidate_fingerprint),
        entries=(
            FolderPlanRevisionEntryV1(
                file_id=selected.file_id,
                replacement_target_path=f"reviewed/{Path(selected.target_path).name}",
                rationale="Place this member in the reviewed section.",
                evidence_ids=("initial_inventory",),
            ),
        ),
    )
    revision_provider = _ScriptedRevisionProvider(revision)
    revised = await service.revise(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction="Place the selected member in a reviewed section.",
        idempotency_key="f0b-scripted-revision",
        provider=revision_provider,
    )

    assert revised.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert revised.proposal_revision == 1
    assert revised.revision_attempt_count == 1
    assert revised.candidate_plan is not None
    assert revised.preview is not None
    assert revised.candidate_plan != reviewing.candidate_plan
    assert revision_provider.inputs[0].base_candidate == reviewing.candidate_plan
    assert revision_provider.inputs[0].turn_contract_freeze_fingerprint == (
        FOLDWEAVE_F0B_CONTRACT_FREEZE.contract_freeze_fingerprint
    )
    assert isinstance(revised.authority, GptPlannedJobAuthorityV3)
    assert revised.authority.evidence_ledger is not None
    assert (
        revised.authority.evidence_ledger.segments[-1].observable_records[0]["input"][
            "turn_contract_freeze_fingerprint"
        ]
        == FOLDWEAVE_F0B_CONTRACT_FREEZE.contract_freeze_fingerprint
    )
    assert tuple(output.iterdir()) == ()
    assert tree_state(fixture.sofia_root) == source_before

    verified = service.accept(
        revised.job_path,
        expected_revision=revised.revision,
        preview_fingerprint=revised.preview.preview_fingerprint,
        candidate_fingerprint=revised.preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=revised.candidate_plan.result_folder_name,
        idempotency_key="f0b-scripted-accept",
        channel="native_app",
    )

    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert verified.final_result_path is not None
    assert verified.final_result_path.is_dir()
    assert service.verify_result(verified.job_path).status.value == "verified"
    assert tree_state(fixture.sofia_root) == source_before


@pytest.mark.anyio
async def test_f0b_contract_correction_preserves_the_observed_prefix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    old_freeze = "a" * 64
    corrected_freeze = "b" * 64
    monkeypatch.setattr(
        review_module,
        "FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT",
        old_freeze,
    )
    reviewing = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "contract-correction.json",
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="f0b-contract-correction-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.candidate_plan is not None
    assert reviewing.preview is not None
    editable = tuple(
        item for item in reviewing.candidate_plan.file_mappings if not item.protected
    )
    failed_provider = _ScriptedRevisionProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=(
                reviewing.preview.compiled_candidate_fingerprint
            ),
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=editable[0].file_id,
                    replacement_target_path=editable[1].target_path,
                    rationale="Exercise a mechanically rejected old-contract turn.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )
    failed = await service.revise(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction="Attempt the old-contract placement.",
        idempotency_key="f0b-contract-correction-failed",
        provider=failed_provider,
    )
    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert isinstance(failed.authority, GptPlannedJobAuthorityV3)
    failed_ledger = failed.authority.evidence_ledger
    assert failed_ledger is not None
    assert len(failed.revision_rejections) == 1

    # Recreate the exact pre-binding representation: the nested field is absent,
    # and every enclosing fingerprint continues to validate in its old domain.
    legacy_payload = failed_ledger.model_dump(mode="json")
    legacy_segment = legacy_payload["segments"][-1]
    legacy_turn = legacy_segment["observable_records"][0]
    legacy_input = legacy_turn["input"]
    legacy_input.pop("turn_contract_freeze_fingerprint")
    legacy_turn["input_bytes"] = len(canonical_json_bytes(legacy_input))
    legacy_turn["input_fingerprint"] = canonical_sha256(legacy_input)
    legacy_turn["turn_fingerprint"] = canonical_sha256(
        {key: value for key, value in legacy_turn.items() if key != "turn_fingerprint"}
    )
    legacy_segment["segment_fingerprint"] = canonical_sha256(
        {
            key: value
            for key, value in legacy_segment.items()
            if key != "segment_fingerprint"
        }
    )
    legacy_payload["transcript_fingerprint"] = canonical_sha256(
        {
            key: value
            for key, value in legacy_payload.items()
            if key != "transcript_fingerprint"
        }
    )
    legacy = FolderEvidenceLedgerV2.model_validate_json(
        canonical_json_bytes(legacy_payload),
        strict=True,
    )
    legacy_turn_model = legacy.segments[-1].observable_records[0]
    assert "turn_contract_freeze_fingerprint" not in legacy_turn_model["input"]
    failed_prefix = legacy.transcript_fingerprint
    failed_segments = legacy.segments
    legacy_authority = failed.authority.model_copy(
        update={
            "evidence_ledger": legacy,
            "execution_origin": build_execution_origin_v2(legacy),
        }
    )
    legacy_job = failed.model_copy(
        update={
            "authority": legacy_authority,
            "revision_rejections": (),
        }
    )
    failed.job_path.write_bytes(canonical_job_v3_bytes(legacy_job))
    failed = legacy_job

    monkeypatch.setattr(
        review_module,
        "FOLDWEAVE_CONTRACT_FREEZE_FINGERPRINT",
        corrected_freeze,
    )
    successful_provider = _ScriptedRevisionProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=(failed.preview.compiled_candidate_fingerprint),
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=editable[0].file_id,
                    replacement_target_path=(
                        f"reviewed/{Path(editable[0].target_path).name}"
                    ),
                    rationale="Exercise a valid corrected-contract turn.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )
    revised = await service.revise(
        failed.job_path,
        expected_revision=failed.revision,
        preview_fingerprint=failed.preview.preview_fingerprint,
        candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
        instruction="Apply the corrected-contract placement.",
        idempotency_key="f0b-contract-correction-success",
        provider=successful_provider,
    )
    assert revised.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert isinstance(revised.authority, GptPlannedJobAuthorityV3)
    revised_ledger = revised.authority.evidence_ledger
    assert revised_ledger is not None
    assert revised_ledger.segments[: len(failed_segments)] == failed_segments
    assert revised_ledger.contract_freeze_fingerprint == old_freeze
    revised_turn = revised_ledger.segments[-1].observable_records[0]
    assert revised_turn["input"]["turn_contract_freeze_fingerprint"] == (
        corrected_freeze
    )
    assert revised_turn["input"]["prior_transcript_fingerprint"] == failed_prefix
    assert len(revised.revision_rejections) == 1
    rejection = revised.revision_rejections[0]
    assert rejection.segment_fingerprint == failed_segments[-1].segment_fingerprint
    assert rejection.turn_fingerprint == legacy_turn["turn_fingerprint"]
    assert rejection.contract_freeze_fingerprint == old_freeze
    assert rejection.code == failed.revision_failure.code
    assert rejection.detail == failed.revision_failure.detail

    explicit_null = dict(revised_turn["input"])
    explicit_null["turn_contract_freeze_fingerprint"] = None
    with pytest.raises(ValueError, match="omitted only by a historical record"):
        FolderPlannerRevisionTurnInputV1.model_validate_json(
            canonical_json_bytes(explicit_null),
            strict=True,
        )


@pytest.mark.anyio
async def test_live_revision_rejects_unbound_legacy_input_before_budget(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    reviewing = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "unbound-live-revision.json",
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="f0b-unbound-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.candidate_plan is not None
    assert reviewing.preview is not None
    selected = next(
        item for item in reviewing.candidate_plan.file_mappings if not item.protected
    )
    scripted = _ScriptedRevisionProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=(
                reviewing.preview.compiled_candidate_fingerprint
            ),
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=selected.file_id,
                    replacement_target_path=(
                        f"reviewed/{Path(selected.target_path).name}"
                    ),
                    rationale="Capture one otherwise valid revision input.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )
    await service.revise(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction="Capture a bounded revision input.",
        idempotency_key="f0b-unbound-capture",
        provider=scripted,
    )
    legacy_payload = scripted.inputs[0].model_dump(mode="json")
    legacy_payload["provider_kind"] = "live"
    legacy_payload.pop("turn_contract_freeze_fingerprint")
    legacy_input = FolderPlannerRevisionTurnInputV1.model_validate_json(
        canonical_json_bytes(legacy_payload),
        strict=True,
    )
    responses = _ForbiddenResponses()
    budget = PersistentBudgetLedger(path=None, live_call_cap=13, cost_cap_usd=40)
    provider = LiveFolderPlanRevisionProvider(
        SimpleNamespace(responses=responses),
        budget=budget,
    )

    with pytest.raises(
        PlannerProviderResponseError,
        match="exact contract-freeze binding",
    ):
        await provider.exchange(legacy_input)

    assert responses.requests == []
    assert budget.snapshot.live_requests_reserved == 0
    assert budget.snapshot.provider_attempts_reserved == 0


@pytest.mark.anyio
async def test_f0b_failed_revision_preserves_and_keeps_previous_proposal(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    reviewing = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "failed-revision.json",
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="f0b-failed-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.candidate_plan is not None
    assert reviewing.preview is not None
    editable = tuple(
        item for item in reviewing.candidate_plan.file_mappings if not item.protected
    )
    assert len(editable) >= 2
    collision_target = editable[1].target_path
    provider = _ScriptedRevisionProvider(
        FolderPlanRevisionV1(
            base_candidate_fingerprint=(
                reviewing.preview.compiled_candidate_fingerprint
            ),
            entries=(
                FolderPlanRevisionEntryV1(
                    file_id=editable[0].file_id,
                    replacement_target_path=collision_target,
                    rationale="Attempt a colliding placement.",
                    evidence_ids=("initial_inventory",),
                ),
            ),
        )
    )

    failed = await service.revise(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction="Put these two files at the same path.",
        idempotency_key="f0b-failed-revision",
        provider=provider,
    )

    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert failed.candidate_plan == reviewing.candidate_plan
    assert failed.preview is not None
    assert failed.revision_failure is not None
    assert tuple(output.iterdir()) == ()

    kept = service.keep_previous_proposal(
        failed.job_path,
        expected_revision=failed.revision,
        preview_fingerprint=failed.preview.preview_fingerprint,
        candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
        idempotency_key="f0b-keep-previous",
    )
    assert kept.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert kept.candidate_plan == reviewing.candidate_plan
    assert kept.preview is not None
    assert kept.preview.expected_job_revision == kept.revision
    assert kept.revision_failure is None
    assert tuple(output.iterdir()) == ()

    exact_retry = service.keep_previous_proposal(
        failed.job_path,
        expected_revision=failed.revision,
        preview_fingerprint=failed.preview.preview_fingerprint,
        candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
        idempotency_key="f0b-keep-previous",
    )
    assert exact_retry == kept
    with pytest.raises(FolderJobV3IdempotencyConflict):
        service.keep_previous_proposal(
            failed.job_path,
            expected_revision=failed.revision,
            preview_fingerprint="f" * 64,
            candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
            idempotency_key="f0b-keep-previous",
        )


@pytest.mark.anyio
async def test_f0b_provider_failure_is_recoverable_and_retry_is_provider_free(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    reviewing = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "provider-failure.json",
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="f0b-provider-failure-initial",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert reviewing.preview is not None
    provider = _FailingRevisionProvider()

    failed = await service.revise(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction="Keep the selected project material together.",
        idempotency_key="f0b-provider-failure-revision",
        provider=provider,
    )

    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED
    assert failed.candidate_plan == reviewing.candidate_plan
    assert failed.preview is not None
    assert failed.revision_failure is not None
    assert failed.revision_failure.code == "revision_provider_failed"
    assert len(failed.revision_provider_failures) == 1
    assert isinstance(failed.authority, GptPlannedJobAuthorityV3)
    assert failed.authority.pending_revision_turn is None
    assert tuple(output.iterdir()) == ()
    assert len(provider.inputs) == 1

    factory_calls = 0

    def forbidden_provider_factory():
        nonlocal factory_calls
        factory_calls += 1
        raise AssertionError("An exact retry must not construct another provider.")

    retried = await service.revise(
        failed.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        instruction="Keep the selected project material together.",
        idempotency_key="f0b-provider-failure-revision",
        provider_factory=forbidden_provider_factory,
    )
    assert retried == failed
    assert factory_calls == 0


def test_f0b_contract_freeze_binds_every_pre_call_surface() -> None:
    freeze = FOLDWEAVE_F0B_CONTRACT_FREEZE

    assert foldweave_f0b_fixture_fingerprint() == (FOLDWEAVE_F0B_FIXTURE_FINGERPRINT)
    assert freeze.fixture_fingerprint == FOLDWEAVE_F0B_FIXTURE_FINGERPRINT
    assert freeze.qualification_call_graph == (FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH)
    assert (
        freeze.initial_provider_attempts_min,
        freeze.initial_provider_attempts_max,
        freeze.revision_provider_attempts,
        freeze.total_provider_attempts_min,
        freeze.total_provider_attempts_max,
    ) == (2, 3, 1, 3, 4)
    assert freeze.model_dump(mode="json") == {
        "schema_version": "foldweave-f0b-contract-freeze.v1",
        "initial_prompt_fingerprint": (
            "c7386d195ba12701b2014d993c8af74056da6d05cb3c757bcf06acea423fd182"
        ),
        "initial_tools_fingerprint": (
            "e6b76ebd8ff37e5453530e91b7d87e10e49907663fb4c584e2061f19fb88bcf7"
        ),
        "revision_prompt_fingerprint": (
            "1df669dc2447a143a756c5dea86bd03443b77ae9fd04c0d6b8a73a7789799987"
        ),
        "revision_tools_fingerprint": (
            "5031313a0f8143c9906d058a31892a5356aecc8f9cebe6a647bb3db1282a1784"
        ),
        "preview_review_contract_fingerprint": (
            "f42a1f1f35c76cc4edff03c9b84c3465bdf53afc8c2603b9a07b2b2a240116cd"
        ),
        "derivative_planning_contract_fingerprint": (
            "60d87314acff0dfb9c0242bce68a47fe87940ee65f773980fe07d1aa73bc02a4"
        ),
        "qualification_provider_profile_fingerprint": (
            "9bcbd662c8165dfa0a5f914af27684aaf3e1165ed5230a66c555176a39e32727"
        ),
        "replay_schema_version": "folder-planner-replay.v2",
        "replay_envelope_identity_fingerprint": (
            "f666decaff4d31994c9a8d87eff19ff2fa1b52554bc3519265def2d1db5ce38f"
        ),
        "evidence_schema_version": "folder-evidence-ledger.v2",
        "evidence_envelope_contract_fingerprint": (
            "607abd69adcbf3e505868f7b8267f777576fc95d99a154a5d77297a6fe146343"
        ),
        "fixture_name": "sofia-apollo-native-root-review.v1",
        "fixture_fingerprint": (
            "fd2e57938875453d3eca99085bb80e266f44b9c8e2195453247373ec4e593fa7"
        ),
        "qualification_call_graph": list(FOLDWEAVE_F0B_QUALIFICATION_CALL_GRAPH),
        "initial_provider_attempts_min": 2,
        "initial_provider_attempts_max": 3,
        "revision_provider_attempts": 1,
        "total_provider_attempts_min": 3,
        "total_provider_attempts_max": 4,
        "qualification_call_graph_fingerprint": (
            "2aeb2cc40da44bb5e531bb75a2c8f428792fdce3bba1a76a5480be90e4161dd0"
        ),
        "contract_freeze_fingerprint": (
            "178aa4aa084ed459726e165acb51edc2c36c16aad9c4020cc49c7542e22feec9"
        ),
    }
