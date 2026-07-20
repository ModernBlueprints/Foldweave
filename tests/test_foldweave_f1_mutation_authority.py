"""F1 retry-history and cross-job destination-reservation regressions."""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Barrier
from typing import Literal

import pytest
from connected_change_fixtures import make_connected_change_fixture

from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    evolve_job_v3,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
    FoldweaveReviewServiceError,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionEntryV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
)
from name_atlas.folder_refactor.planner_provider import (
    DETERMINISTIC_DEVELOPMENT_REQUEST,
    DeterministicDevelopmentPlannerProvider,
)
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage


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
            call_id=f"f1-revision-{len(self.inputs)}",
            revision=self._revision,
        )


@pytest.mark.anyio
async def test_old_revision_retry_after_second_revision_is_provider_free(
    tmp_path: Path,
) -> None:
    """An old exact retry resolves from append-only history after job advance."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    initial = await service.prepare_planned_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "revision-history.json",
        request=DETERMINISTIC_DEVELOPMENT_REQUEST,
        idempotency_key="f1-initial-plan",
        provider=DeterministicDevelopmentPlannerProvider(),
    )
    assert initial.preview is not None
    assert initial.candidate_plan is not None

    first_entry = next(
        entry for entry in initial.candidate_plan.file_mappings if not entry.protected
    )
    first_instruction = "Move the selected member into the first review section."
    first_key = "f1-first-revision"
    first = await service.revise(
        initial.job_path,
        expected_revision=initial.revision,
        preview_fingerprint=initial.preview.preview_fingerprint,
        candidate_fingerprint=initial.preview.compiled_candidate_fingerprint,
        instruction=first_instruction,
        idempotency_key=first_key,
        provider=_ScriptedRevisionProvider(
            FolderPlanRevisionV1(
                base_candidate_fingerprint=(
                    initial.preview.compiled_candidate_fingerprint
                ),
                entries=(
                    FolderPlanRevisionEntryV1(
                        file_id=first_entry.file_id,
                        replacement_target_path=(
                            f"first/{Path(first_entry.target_path).name}"
                        ),
                        rationale="Place this member in the first section.",
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            )
        ),
    )
    assert first.preview is not None
    assert first.candidate_plan is not None

    second_entry = next(
        entry
        for entry in first.candidate_plan.file_mappings
        if not entry.protected and entry.file_id != first_entry.file_id
    )
    second = await service.revise(
        first.job_path,
        expected_revision=first.revision,
        preview_fingerprint=first.preview.preview_fingerprint,
        candidate_fingerprint=first.preview.compiled_candidate_fingerprint,
        instruction="Move another member into the second review section.",
        idempotency_key="f1-second-revision",
        provider=_ScriptedRevisionProvider(
            FolderPlanRevisionV1(
                base_candidate_fingerprint=(
                    first.preview.compiled_candidate_fingerprint
                ),
                entries=(
                    FolderPlanRevisionEntryV1(
                        file_id=second_entry.file_id,
                        replacement_target_path=(
                            f"second/{Path(second_entry.target_path).name}"
                        ),
                        rationale="Place this member in the second section.",
                        evidence_ids=("initial_inventory",),
                    ),
                ),
            )
        ),
    )
    assert second.proposal_revision == 2
    assert [
        binding.terminal_outcome for binding in second.revision_mutation_bindings
    ] == ["proposal_replaced", "proposal_replaced"]

    factory_calls = 0

    def forbidden_provider_factory() -> _ScriptedRevisionProvider:
        nonlocal factory_calls
        factory_calls += 1
        raise AssertionError("Historical exact retry must not construct a provider.")

    retried = await service.revise(
        second.job_path,
        expected_revision=initial.revision,
        preview_fingerprint=initial.preview.preview_fingerprint,
        candidate_fingerprint=initial.preview.compiled_candidate_fingerprint,
        instruction=first_instruction,
        idempotency_key=first_key,
        provider_factory=forbidden_provider_factory,
    )
    assert retried == second
    assert factory_calls == 0

    with pytest.raises(
        FolderJobV3IdempotencyConflict,
        match="another exact request",
    ):
        await service.revise(
            second.job_path,
            expected_revision=initial.revision,
            preview_fingerprint=initial.preview.preview_fingerprint,
            candidate_fingerprint=initial.preview.compiled_candidate_fingerprint,
            instruction="Conflicting reuse of the first durable retry key.",
            idempotency_key=first_key,
            provider_factory=forbidden_provider_factory,
        )
    assert factory_calls == 0


def test_destination_reservation_has_one_race_winner_and_releases_on_block(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Sibling jobs cannot both reserve one result, including after restart."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    jobs = tmp_path / "jobs"
    service = FoldweaveReviewService()
    reviews = tuple(
        service.prepare_deterministic_origin_review(
            source_root=fixture.sofia_root,
            output_parent=output,
            job_path=jobs / f"contender-{index}.json",
            request=fixture.request,
            result_folder_name=fixture.result_name,
            target_by_original_path=fixture.target_paths,
            idempotency_key=f"f1-contender-{index}",
        )
        for index in range(2)
    )
    assert all(review.preview is not None for review in reviews)

    def stop_before_copy(
        _service: FoldweaveReviewService,
        _writer,
        job: FolderRefactorJobV3,
        *,
        progress_callback,
    ) -> FolderRefactorJobV3:
        del progress_callback
        return job

    monkeypatch.setattr(FoldweaveReviewService, "_execute_locked", stop_before_copy)
    barrier = Barrier(2)

    def accept(review: FolderRefactorJobV3) -> FolderRefactorJobV3:
        assert review.preview is not None
        assert review.candidate_plan is not None
        barrier.wait(timeout=5)
        return service.accept(
            review.job_path,
            expected_revision=review.revision,
            preview_fingerprint=review.preview.preview_fingerprint,
            candidate_fingerprint=review.preview.compiled_candidate_fingerprint,
            output_parent=output,
            result_folder_name=review.candidate_plan.result_folder_name,
            idempotency_key=f"accept-{review.job_id}",
            channel="native_app",
        )

    outcomes: list[FolderRefactorJobV3] = []
    failures: list[FoldweaveReviewServiceError] = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = tuple(executor.submit(accept, review) for review in reviews)
        for future in futures:
            try:
                outcomes.append(future.result(timeout=10))
            except FoldweaveReviewServiceError as exc:
                failures.append(exc)

    assert len(outcomes) == 1
    assert outcomes[0].lifecycle is FolderJobLifecycleV3.EXECUTING
    assert outcomes[0].destination_reservation is not None
    assert outcomes[0].destination_reservation.output_parent == output.resolve()
    assert (
        outcomes[0].destination_reservation.final_result_path
        == (output / fixture.result_name).resolve()
    )
    assert [failure.code for failure in failures] == ["destination_already_reserved"]
    assert tuple(output.iterdir()) == ()

    winner = outcomes[0]
    restarted = FoldweaveReviewService().resume_authorized_execution(winner.job_path)
    assert restarted == winner

    winner_store = FolderRefactorJobV3Store(winner.job_path)
    with winner_store.writer() as writer:
        current = writer.rehydrate()
        blocked = evolve_job_v3(
            current,
            revision=current.revision + 1,
            lifecycle=FolderJobLifecycleV3.BLOCKED,
            blocker_code="test_release",
            blocker_message="Release the reservation without creating a result.",
        )
        writer.save(blocked, expected_current=current)

    loser = next(review for review in reviews if review.job_id != winner.job_id)
    assert loser.preview is not None
    assert loser.candidate_plan is not None
    accepted_after_release = service.accept(
        loser.job_path,
        expected_revision=loser.revision,
        preview_fingerprint=loser.preview.preview_fingerprint,
        candidate_fingerprint=loser.preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=loser.candidate_plan.result_folder_name,
        idempotency_key=f"accept-{loser.job_id}",
        channel="native_app",
    )
    assert accepted_after_release.lifecycle is FolderJobLifecycleV3.EXECUTING
    assert accepted_after_release.destination_reservation is not None
    assert tuple(output.iterdir()) == ()


def test_accept_and_revision_race_has_one_authority_winner(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Acceptance and revision cannot both advance the same visible preview."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    review = asyncio.run(
        service.prepare_planned_origin_review(
            source_root=fixture.sofia_root,
            output_parent=output,
            job_path=tmp_path / "jobs" / "accept-revise-race.json",
            request=DETERMINISTIC_DEVELOPMENT_REQUEST,
            idempotency_key="f1-accept-revise-race",
            provider=DeterministicDevelopmentPlannerProvider(),
        )
    )
    assert review.preview is not None
    assert review.candidate_plan is not None
    mapping = next(
        item for item in review.candidate_plan.file_mappings if not item.protected
    )

    def stop_before_copy(
        _service: FoldweaveReviewService,
        _writer,
        job: FolderRefactorJobV3,
        *,
        progress_callback,
    ) -> FolderRefactorJobV3:
        del progress_callback
        return job

    monkeypatch.setattr(FoldweaveReviewService, "_execute_locked", stop_before_copy)
    barrier = Barrier(2)

    def accept_visible_preview() -> FolderRefactorJobV3:
        barrier.wait(timeout=5)
        return service.accept(
            review.job_path,
            expected_revision=review.revision,
            preview_fingerprint=review.preview.preview_fingerprint,
            candidate_fingerprint=review.preview.compiled_candidate_fingerprint,
            output_parent=output,
            result_folder_name=review.candidate_plan.result_folder_name,
            idempotency_key="f1-race-accept",
            channel="native_app",
        )

    def revise_visible_preview() -> FolderRefactorJobV3:
        barrier.wait(timeout=5)
        return asyncio.run(
            service.revise(
                review.job_path,
                expected_revision=review.revision,
                preview_fingerprint=review.preview.preview_fingerprint,
                candidate_fingerprint=review.preview.compiled_candidate_fingerprint,
                instruction="Move one member into the race-test section.",
                idempotency_key="f1-race-revise",
                provider=_ScriptedRevisionProvider(
                    FolderPlanRevisionV1(
                        base_candidate_fingerprint=(
                            review.preview.compiled_candidate_fingerprint
                        ),
                        entries=(
                            FolderPlanRevisionEntryV1(
                                file_id=mapping.file_id,
                                replacement_target_path=(
                                    f"race/{Path(mapping.target_path).name}"
                                ),
                                rationale="Apply the exact visible revision.",
                                evidence_ids=("initial_inventory",),
                            ),
                        ),
                    )
                ),
            )
        )

    outcomes: list[FolderRefactorJobV3] = []
    failures: list[Exception] = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = (
            executor.submit(accept_visible_preview),
            executor.submit(revise_visible_preview),
        )
        for future in futures:
            try:
                outcomes.append(future.result(timeout=10))
            except Exception as exc:  # test captures the losing authority path
                failures.append(exc)

    durable = service.status(review.job_path)
    assert len(outcomes) == 1
    assert len(failures) == 1
    assert durable == outcomes[0]
    assert durable.lifecycle in {
        FolderJobLifecycleV3.EXECUTING,
        FolderJobLifecycleV3.REVIEWING,
    }
    assert (durable.execution_authorization is None) != (durable.proposal_revision == 0)
    assert tuple(output.iterdir()) == ()


def test_executing_job_rehydrates_stale_with_historical_reservation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Staleness clears execution authority without corrupting reservation history."""

    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    review = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "stale-after-authorization.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="f1-stale-reservation",
    )
    assert review.preview is not None
    assert review.candidate_plan is not None

    def stop_before_copy(
        _service: FoldweaveReviewService,
        _writer,
        job: FolderRefactorJobV3,
        *,
        progress_callback,
    ) -> FolderRefactorJobV3:
        del progress_callback
        return job

    monkeypatch.setattr(FoldweaveReviewService, "_execute_locked", stop_before_copy)
    executing = service.accept(
        review.job_path,
        expected_revision=review.revision,
        preview_fingerprint=review.preview.preview_fingerprint,
        candidate_fingerprint=review.preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=review.candidate_plan.result_folder_name,
        idempotency_key="f1-stale-reservation-accept",
        channel="native_app",
    )
    assert executing.lifecycle is FolderJobLifecycleV3.EXECUTING
    assert executing.destination_reservation is not None

    (fixture.sofia_root / "changed-after-authorization.txt").write_text(
        "changed\n",
        encoding="utf-8",
    )
    stale = FolderRefactorJobV3Store(executing.job_path).load()

    assert stale.lifecycle is FolderJobLifecycleV3.STALE
    assert stale.staleness is not None
    assert stale.staleness.code == "source_changed"
    assert stale.execution_authorization is None
    assert stale.pending_result_path is None
    assert stale.final_result_path is None
    assert stale.destination_reservation == executing.destination_reservation
    assert tuple(output.iterdir()) == ()
