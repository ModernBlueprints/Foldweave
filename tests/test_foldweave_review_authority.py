"""Adversarial F0a review authority and durable-recovery regression tests."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path, PurePosixPath
from typing import Any

import pytest
from connected_change_fixtures import make_connected_change_fixture, tree_state
from pydantic import ValidationError

from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderExecutionAuthorizationV1,
    FolderJobLifecycleV3,
    FolderJobV3IdempotencyConflict,
    FolderJobV3RevisionError,
    FolderJobV3WriteError,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    FolderRefactorJobV3Writer,
    build_execution_authorization,
    evolve_job_v3,
    expected_final_result_path_v3,
    expected_pending_result_path_v3,
)
from name_atlas.folder_refactor.connected_change.preview import (
    FolderPlanPreviewV1,
    build_folder_plan_preview,
)
from name_atlas.folder_refactor.connected_change.review_service import (
    FoldweaveReviewService,
)
from name_atlas.folder_refactor.serialization import canonical_sha256


def test_preview_rejects_duplicate_member_change_even_with_valid_fingerprint(
    tmp_path: Path,
) -> None:
    """Every current member must have exactly one corresponding change row."""

    reviewing, _service, _output, _fixture = _prepare_review(tmp_path)
    preview_payload = _preview_payload(reviewing)
    changes = list(preview_payload["member_changes"])
    changes.append(deepcopy(changes[0]))
    changes.sort(key=lambda item: item["current_relative_path"])
    preview_payload["member_changes"] = tuple(changes)
    _refresh_preview_fingerprint(preview_payload)

    with pytest.raises(ValidationError, match="exactly once|unique"):
        FolderPlanPreviewV1.model_validate(preview_payload, strict=True)


def test_job_rejects_preview_path_divergent_from_compiled_candidate(
    tmp_path: Path,
) -> None:
    """A self-consistent DTO cannot replace the persisted compiler authority."""

    reviewing, _service, _output, _fixture = _prepare_review(tmp_path)
    preview_payload = _preview_payload(reviewing)
    proposed = list(preview_payload["proposed_tree_members"])
    linked_member_ids = {
        member_id
        for effect in preview_payload["supported_link_effects"]
        for member_id in (effect["source_member_id"], effect["target_member_id"])
    }
    selected = next(
        item
        for item in proposed
        if item["member_kind"] == "regular_file"
        and not item["protected"]
        and item["member_id"] not in linked_member_ids
    )
    selected_id = selected["member_id"]
    selected["relative_path"] = (
        f"zzzz-divergent/renamed-{PurePosixPath(selected['relative_path']).name}"
    )
    selected["directory_prefixes"] = ("zzzz-divergent",)
    proposed.sort(key=lambda item: item["relative_path"])
    preview_payload["proposed_tree_members"] = tuple(proposed)
    changes = list(preview_payload["member_changes"])
    change = next(item for item in changes if item["member_id"] == selected_id)
    change["proposed_relative_path"] = selected["relative_path"]
    change["change_classification"] = "moved_and_renamed"
    preview_payload["member_changes"] = tuple(changes)
    _refresh_preview_counts(preview_payload)
    _refresh_preview_fingerprint(preview_payload)

    divergent_preview = FolderPlanPreviewV1.model_validate(
        preview_payload,
        strict=True,
    )
    job_payload = reviewing.model_dump(mode="python")
    job_payload["preview"] = divergent_preview.model_dump(mode="python")

    with pytest.raises(ValidationError, match="candidate|preview|tree|path"):
        FolderRefactorJobV3.model_validate(job_payload, strict=True)


@pytest.mark.parametrize(
    "count_field",
    [
        "file_count",
        "empty_directory_count",
        "changed_path_count",
        "link_count",
        "protected_count",
        "blocker_count",
    ],
)
def test_preview_rejects_incorrect_derived_count(
    tmp_path: Path,
    count_field: str,
) -> None:
    """Displayed trust counts must be derived from the complete preview contents."""

    reviewing, _service, _output, _fixture = _prepare_review(tmp_path)
    preview_payload = _preview_payload(reviewing)
    preview_payload["counts"][count_field] += 1
    _refresh_preview_fingerprint(preview_payload)

    with pytest.raises(ValidationError, match="count|preview"):
        FolderPlanPreviewV1.model_validate(preview_payload, strict=True)


def test_preview_rejects_dangling_link_effect_member(
    tmp_path: Path,
) -> None:
    """Every displayed link endpoint must resolve to a preview member."""

    reviewing, _service, _output, _fixture = _prepare_review(tmp_path)
    preview_payload = _preview_payload(reviewing)
    effects = list(preview_payload["supported_link_effects"])
    assert effects
    effects[0]["source_member_id"] = "0" * 64
    preview_payload["supported_link_effects"] = tuple(effects)
    _refresh_preview_fingerprint(preview_payload)

    with pytest.raises(ValidationError, match="link|member|endpoint"):
        FolderPlanPreviewV1.model_validate(preview_payload, strict=True)


def test_preview_rejects_duplicate_link_effect_even_with_matching_counts(
    tmp_path: Path,
) -> None:
    """A link reference cannot appear twice in one authorization preview."""

    reviewing, _service, _output, _fixture = _prepare_review(tmp_path)
    preview_payload = _preview_payload(reviewing)
    effects = list(preview_payload["supported_link_effects"])
    assert effects
    duplicate = deepcopy(effects[0])
    effects.append(duplicate)
    effects.sort(key=lambda item: (item["current_source_path"], item["reference_id"]))
    preview_payload["supported_link_effects"] = tuple(effects)
    preview_payload["counts"]["link_count"] += 1
    if duplicate["status"] == "rewritten":
        preview_payload["counts"]["link_updated_count"] += 1
    _refresh_preview_fingerprint(preview_payload)

    with pytest.raises(ValidationError, match="link|unique|duplicate"):
        FolderPlanPreviewV1.model_validate(preview_payload, strict=True)


def test_preview_rejects_incorrect_directory_prefixes(
    tmp_path: Path,
) -> None:
    """Tree hierarchy metadata must be derived from each exact relative path."""

    reviewing, _service, _output, _fixture = _prepare_review(tmp_path)
    preview_payload = _preview_payload(reviewing)
    current = list(preview_payload["current_tree_members"])
    selected = next(
        item
        for item in current
        if PurePosixPath(item["relative_path"]).parent.as_posix() != "."
    )
    selected["directory_prefixes"] = ("not-the-real-parent",)
    preview_payload["current_tree_members"] = tuple(current)
    _refresh_preview_fingerprint(preview_payload)

    with pytest.raises(ValidationError, match="reconcile|director|prefix|path"):
        FolderPlanPreviewV1.model_validate(preview_payload, strict=True)


@pytest.mark.anyio
async def test_revision_failed_cannot_transition_directly_to_executing(
    tmp_path: Path,
) -> None:
    """A failed replacement needs an explicit keep/review transition before accept."""

    reviewing, service, _output, _fixture = _prepare_review(tmp_path)
    assert reviewing.preview is not None

    class FailingRevisionProvider:
        provider_kind = "deterministic"

        @property
        def usage(self) -> tuple[Any, ...]:
            return ()

        async def exchange(self, _turn_input: Any, /) -> Any:
            raise RuntimeError("The scripted replacement did not compile.")

    failed = await service.revise(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=(reviewing.preview.compiled_candidate_fingerprint),
        instruction="Move the selected member into a revised section.",
        idempotency_key="prepare-failed-revision",
        provider=FailingRevisionProvider(),
    )
    assert failed.lifecycle is FolderJobLifecycleV3.REVISION_FAILED

    store = FolderRefactorJobV3Store(reviewing.job_path)
    with store.writer() as writer:
        failed = writer.rehydrate()

        assert failed.preview is not None
        assert failed.candidate_plan is not None
        authorization = build_execution_authorization(
            job=failed,
            expected_job_revision=failed.revision,
            preview_fingerprint=failed.preview.preview_fingerprint,
            candidate_fingerprint=failed.preview.compiled_candidate_fingerprint,
            output_parent=failed.output_parent,
            result_folder_name=failed.candidate_plan.result_folder_name,
            idempotency_key="must-keep-previous-first",
            channel="native_app",
        )
        executing = evolve_job_v3(
            failed,
            revision=failed.revision + 1,
            updated_at=failed.updated_at,
            lifecycle=FolderJobLifecycleV3.EXECUTING,
            revision_failure=None,
            execution_authorization=authorization,
            pending_result_path=expected_pending_result_path_v3(failed),
            final_result_path=expected_final_result_path_v3(failed),
        )

        with pytest.raises(FolderJobV3RevisionError, match="Invalid v3 transition"):
            writer.save(executing, expected_current=failed)


def test_writer_rejects_replacement_proposal_during_exact_accept(
    tmp_path: Path,
) -> None:
    """The durable writer must reject a different self-consistent preview."""

    reviewing, service, output, fixture = _prepare_review(tmp_path)
    assert reviewing.preview is not None
    replacement_targets = dict(fixture.target_paths)
    replacement_targets["media/cover.png"] = "alternate/hero-cover.png"
    replacement = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "replacement.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=replacement_targets,
        idempotency_key="prepare-replacement-review",
    )
    assert replacement.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert replacement.candidate_plan is not None
    assert replacement.reference_graph is not None
    assert replacement.preview is not None
    assert (
        replacement.preview.preview_fingerprint != reviewing.preview.preview_fingerprint
    )

    replacement_preview = build_folder_plan_preview(
        job_id=reviewing.job_id,
        expected_job_revision=reviewing.revision,
        proposal_revision=reviewing.proposal_revision,
        proposal_basis="fresh_gpt_plan",
        inventory=reviewing.source_inventory,
        reference_graph=replacement.reference_graph,
        accepted_plan=replacement.candidate_plan,
    )
    replacement_review = evolve_job_v3(
        reviewing,
        authority=replacement.authority,
        candidate_plan=replacement.candidate_plan,
        reference_graph=replacement.reference_graph,
        preview=replacement_preview,
    )
    authorization = build_execution_authorization(
        job=replacement_review,
        expected_job_revision=reviewing.revision,
        preview_fingerprint=replacement_preview.preview_fingerprint,
        candidate_fingerprint=replacement_preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=replacement.candidate_plan.result_folder_name,
        idempotency_key="accept-unseen-replacement",
        channel="native_app",
    )
    unseen_execution = evolve_job_v3(
        replacement_review,
        revision=reviewing.revision + 1,
        updated_at=reviewing.updated_at,
        lifecycle=FolderJobLifecycleV3.EXECUTING,
        execution_authorization=authorization,
        pending_result_path=expected_pending_result_path_v3(replacement_review),
        final_result_path=expected_final_result_path_v3(replacement_review),
    )

    store = FolderRefactorJobV3Store(reviewing.job_path)
    with store.writer() as writer:
        current = writer.rehydrate()
        with pytest.raises(
            FolderJobV3RevisionError,
            match="changed the durable reviewed proposal",
        ):
            writer.save(unseen_execution, expected_current=current)

    persisted = service.status(reviewing.job_path)
    assert persisted == reviewing
    assert tuple(output.iterdir()) == ()


def test_receiver_authorization_rejects_mismatched_portable_bindings(
    tmp_path: Path,
) -> None:
    """Receiver acceptance must bind the Change File and match-report preview."""

    origin, service, origin_output, fixture = _prepare_review(tmp_path)
    assert origin.preview is not None
    assert origin.candidate_plan is not None
    verified_origin = service.accept(
        origin.job_path,
        expected_revision=origin.revision,
        preview_fingerprint=origin.preview.preview_fingerprint,
        candidate_fingerprint=origin.preview.compiled_candidate_fingerprint,
        output_parent=origin_output,
        result_folder_name=origin.candidate_plan.result_folder_name,
        idempotency_key="accept-portable-binding-origin",
        channel="native_app",
    )
    change_file_path, _change_file_fingerprint, _receipt_fingerprint = (
        service.get_change_file(verified_origin.job_path)
    )
    receiver_output = tmp_path / "receiver-output"
    receiver_output.mkdir()
    receiver = service.prepare_application_review(
        change_file_path=change_file_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=tmp_path / "jobs" / "receiver-portable-binding.json",
        idempotency_key="prepare-portable-binding-receiver",
    )
    assert receiver.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert receiver.preview is not None
    assert receiver.candidate_plan is not None
    assert receiver.preview.imported_change_file_fingerprint is not None
    assert receiver.preview.match_report_fingerprint is not None

    authorization = build_execution_authorization(
        job=receiver,
        expected_job_revision=receiver.revision,
        preview_fingerprint=receiver.preview.preview_fingerprint,
        candidate_fingerprint=receiver.preview.compiled_candidate_fingerprint,
        output_parent=receiver_output,
        result_folder_name=receiver.candidate_plan.result_folder_name,
        idempotency_key="mismatched-portable-binding",
        channel="native_app",
    )
    mismatched_payload = authorization.model_dump(mode="python")
    mismatched_payload["imported_change_file_fingerprint"] = "a" * 64
    mismatched_payload["match_report_fingerprint"] = "b" * 64
    fingerprint_payload = deepcopy(mismatched_payload)
    fingerprint_payload.pop("authorization_fingerprint")
    fingerprint_payload.pop("output_parent")
    fingerprint_payload["authorization_timestamp"] = mismatched_payload[
        "authorization_timestamp"
    ].isoformat()
    mismatched_payload["authorization_fingerprint"] = canonical_sha256(
        fingerprint_payload
    )
    mismatched_authorization = FolderExecutionAuthorizationV1.model_validate(
        mismatched_payload,
        strict=True,
    )

    with pytest.raises(ValidationError, match="authorization targets another preview"):
        evolve_job_v3(
            receiver,
            revision=receiver.revision + 1,
            updated_at=receiver.updated_at,
            lifecycle=FolderJobLifecycleV3.EXECUTING,
            execution_authorization=mismatched_authorization,
            pending_result_path=expected_pending_result_path_v3(receiver),
            final_result_path=expected_final_result_path_v3(receiver),
        )

    assert service.status(receiver.job_path) == receiver
    assert tuple(receiver_output.iterdir()) == ()


def test_exact_accept_retry_recovers_promoted_result_from_executing_checkpoint(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A crash after promotion must verify and finalize, never execute a second copy."""

    reviewing, service, output, _fixture = _prepare_review(tmp_path)
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    original_save = FolderRefactorJobV3Writer.save

    def interrupt_verified_checkpoint(
        writer: FolderRefactorJobV3Writer,
        successor: FolderRefactorJobV3,
        *,
        expected_current: FolderRefactorJobV3,
    ) -> FolderRefactorJobV3:
        if successor.lifecycle is FolderJobLifecycleV3.VERIFIED:
            raise FolderJobV3WriteError(
                "Simulated interruption after promotion and before "
                "VERIFIED persistence."
            )
        return original_save(
            writer,
            successor,
            expected_current=expected_current,
        )

    with monkeypatch.context() as interrupted:
        interrupted.setattr(
            FolderRefactorJobV3Writer,
            "save",
            interrupt_verified_checkpoint,
        )
        with pytest.raises(FolderJobV3WriteError, match="Simulated interruption"):
            service.accept(
                reviewing.job_path,
                expected_revision=reviewing.revision,
                preview_fingerprint=reviewing.preview.preview_fingerprint,
                candidate_fingerprint=(
                    reviewing.preview.compiled_candidate_fingerprint
                ),
                output_parent=output,
                result_folder_name=reviewing.candidate_plan.result_folder_name,
                idempotency_key="recover-exact-accept",
                channel="native_app",
            )

    interrupted_job = service.status(reviewing.job_path)
    assert interrupted_job.lifecycle is FolderJobLifecycleV3.EXECUTING
    assert interrupted_job.execution_authorization is not None
    assert interrupted_job.final_result_path is not None
    assert interrupted_job.final_result_path.is_dir()
    assert interrupted_job.pending_result_path is not None
    assert not interrupted_job.pending_result_path.exists()
    result_before_retry = tree_state(interrupted_job.final_result_path)
    output_entries_before_retry = tuple(output.iterdir())

    recovered = service.accept(
        reviewing.job_path,
        expected_revision=reviewing.revision,
        preview_fingerprint=reviewing.preview.preview_fingerprint,
        candidate_fingerprint=reviewing.preview.compiled_candidate_fingerprint,
        output_parent=output,
        result_folder_name=reviewing.candidate_plan.result_folder_name,
        idempotency_key="recover-exact-accept",
        channel="native_app",
    )

    assert recovered.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert recovered.verified_artifacts is not None
    assert recovered.final_result_path == interrupted_job.final_result_path
    assert tuple(output.iterdir()) == output_entries_before_retry
    assert tree_state(recovered.final_result_path) == result_before_retry


def test_verified_accept_retry_rejects_every_conflicting_binding(
    tmp_path: Path,
) -> None:
    """A completed accept is reusable only by the exact original request."""

    reviewing, service, output, _fixture = _prepare_review(tmp_path)
    assert reviewing.preview is not None
    assert reviewing.candidate_plan is not None
    exact = {
        "expected_revision": reviewing.revision,
        "preview_fingerprint": reviewing.preview.preview_fingerprint,
        "candidate_fingerprint": reviewing.preview.compiled_candidate_fingerprint,
        "output_parent": output,
        "result_folder_name": reviewing.candidate_plan.result_folder_name,
        "idempotency_key": "exact-verified-retry",
        "channel": "native_app",
    }
    verified = service.accept(reviewing.job_path, **exact)
    assert verified.lifecycle is FolderJobLifecycleV3.VERIFIED
    assert verified.final_result_path is not None
    job_before = reviewing.job_path.read_bytes()
    result_before = tree_state(verified.final_result_path)
    other_output = tmp_path / "other-output"
    other_output.mkdir()
    conflicts = {
        "idempotency": {"idempotency_key": "another-key"},
        "channel": {"channel": "browser"},
        "output": {"output_parent": other_output},
        "result_name": {"result_folder_name": "another-result"},
    }

    for label, changes in conflicts.items():
        request = {**exact, **changes}
        with pytest.raises(
            FolderJobV3IdempotencyConflict,
            match="another exact request",
        ):
            service.accept(reviewing.job_path, **request)
        assert reviewing.job_path.read_bytes() == job_before, label
        assert tree_state(verified.final_result_path) == result_before, label
        assert tuple(output.iterdir()) == (verified.final_result_path,), label
        assert tuple(other_output.iterdir()) == (), label


def _prepare_review(
    tmp_path: Path,
) -> tuple[FolderRefactorJobV3, FoldweaveReviewService, Path, Any]:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    output = tmp_path / "output"
    output.mkdir()
    service = FoldweaveReviewService()
    reviewing = service.prepare_deterministic_origin_review(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=tmp_path / "jobs" / "review.json",
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
        idempotency_key="prepare-authority-review",
    )
    assert reviewing.lifecycle is FolderJobLifecycleV3.REVIEWING
    assert reviewing.preview is not None
    return reviewing, service, output, fixture


def _preview_payload(job: FolderRefactorJobV3) -> dict[str, Any]:
    assert job.preview is not None
    return deepcopy(job.preview.model_dump(mode="python"))


def _refresh_preview_fingerprint(payload: dict[str, Any]) -> None:
    payload["preview_fingerprint"] = canonical_sha256(
        {key: value for key, value in payload.items() if key != "preview_fingerprint"}
    )


def _refresh_preview_counts(payload: dict[str, Any]) -> None:
    changes = tuple(payload["member_changes"])
    regular_changes = tuple(
        item for item in changes if item["member_kind"] == "regular_file"
    )
    changed = tuple(
        item
        for item in regular_changes
        if item["current_relative_path"] != item["proposed_relative_path"]
    )
    effects = tuple(payload["supported_link_effects"])
    payload["counts"] = {
        "file_count": len(regular_changes),
        "empty_directory_count": len(changes) - len(regular_changes),
        "changed_path_count": len(changed),
        "renamed_count": sum(
            PurePosixPath(item["current_relative_path"]).name
            != PurePosixPath(item["proposed_relative_path"]).name
            for item in changed
        ),
        "moved_count": sum(
            PurePosixPath(item["current_relative_path"]).parent
            != PurePosixPath(item["proposed_relative_path"]).parent
            for item in changed
        ),
        "link_count": len(effects),
        "link_updated_count": sum(item["status"] == "rewritten" for item in effects),
        "protected_count": sum(item["protected"] for item in regular_changes),
        "blocker_count": len(payload["blocker_findings"]),
    }


def _preview_with_expected_revision(
    preview: FolderPlanPreviewV1 | None,
    expected_revision: int,
) -> FolderPlanPreviewV1:
    assert preview is not None
    payload = deepcopy(preview.model_dump(mode="python"))
    payload["expected_job_revision"] = expected_revision
    _refresh_preview_fingerprint(payload)
    return FolderPlanPreviewV1.model_validate(payload, strict=True)
