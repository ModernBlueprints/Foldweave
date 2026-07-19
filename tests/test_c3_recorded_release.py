"""Release-bound C3 GPT-5.6 recordings and keyless transaction proof."""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest
from connected_change_fixtures import make_symmetric_fixture

from name_atlas import connected_browser_cli
from name_atlas.folder_refactor.connected_change.contracts import ConnectedChangeError
from name_atlas.folder_refactor.connected_change.job_service import (
    ConnectedChangeJobService,
)
from name_atlas.folder_refactor.connected_change.job_v2 import (
    FolderJobLifecycleV2,
    GptPlannedJobAuthorityV2,
)
from name_atlas.folder_refactor.connected_change.planning import (
    ConnectedOriginPlanningService,
)
from name_atlas.folder_refactor.connected_change.service import (
    apply_connected_change,
    create_connected_change_origin,
)
from name_atlas.folder_refactor.connected_change.verification import (
    ConnectedReceiptVerificationStatus,
    verify_connected_result,
)
from name_atlas.folder_refactor.demo_fixtures import (
    AMBIGUITY_ANSWER,
    AMBIGUITY_REQUEST,
    HERO_REQUEST,
    materialize_ambiguity_fixture,
    materialize_hero_fixture,
)
from name_atlas.folder_refactor.inventory import scan_folder
from name_atlas.folder_refactor.planner_recording import (
    RecordedPlannerProvider,
    load_folder_planner_replay,
)
from name_atlas.folder_refactor.portable_artifacts import (
    ACCEPTED_PLAN_PATH,
    canonical_portable_json_bytes,
)
from name_atlas.folder_refactor.serialization import canonical_json_bytes
from name_atlas.verification.bag_writer import BagItWriter
from name_atlas.verification.bagit_validator import BagItPackageValidator

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src" / "name_atlas"
HERO_RECORDING = PACKAGE_ROOT / "recordings" / "folder_hero_zero_question.json"
AMBIGUITY_RECORDING = PACKAGE_ROOT / "recordings" / "folder_ambiguity_one_question.json"


def _tree(root: Path) -> dict[str, bytes | None]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes() if path.is_file() else None
        for path in sorted(root.rglob("*"))
    }


def _recording(path: Path):
    payload = path.read_bytes()
    text = payload.decode("utf-8")
    assert "/Users/" not in text
    assert "OPENAI_API_KEY" not in text
    assert "response_id" not in text
    replay = load_folder_planner_replay(payload)
    assert replay.live_evidence_ledger.provider_kind == "live"
    assert replay.live_evidence_ledger.store_false is True
    assert len(replay.live_evidence_ledger.usage) == len(replay.turns)
    assert all(item.usage.recorded_at is not None for item in replay.turns)
    assert hashlib.sha256(payload).hexdigest()
    return replay


def _verified_commitment(job) -> str:
    verification = ConnectedChangeJobService().verify_result(job.job_path)
    assert verification.status.value == "verified"
    assert verification.failed_check_ids == ()
    assert verification.organized_tree_commitment is not None
    return verification.organized_tree_commitment


async def _create_recorded_hero_origin(tmp_path: Path):
    fixture = materialize_hero_fixture(tmp_path / "fixtures")
    output = tmp_path / "origin-output"
    jobs = tmp_path / "jobs"
    output.mkdir()
    jobs.mkdir()
    origin = await ConnectedOriginPlanningService().start(
        source_root=fixture.sofia_root,
        output_parent=output,
        job_path=jobs / "origin.json",
        request=HERO_REQUEST,
        idempotency_key="release-refusal-hero-origin",
        provider=RecordedPlannerProvider(_recording(HERO_RECORDING)),
    )
    assert origin.lifecycle is FolderJobLifecycleV2.VERIFIED
    change_path, _change_id, _origin_receipt = (
        ConnectedChangeJobService().get_change_file(origin.job_path)
    )
    return fixture, origin, change_path


def test_bundled_demo_keeps_job_state_outside_source_and_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    def capture_browser_paths(**kwargs: object) -> int:
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(connected_browser_cli, "PROJECT_ROOT", tmp_path)
    monkeypatch.setattr(
        connected_browser_cli,
        "_run_connected_browser",
        capture_browser_paths,
    )

    assert connected_browser_cli.run_connected_demo(["--mode", "replay"]) == 0

    source = captured["source"]
    output = captured["output"]
    job = captured["job"]
    assert isinstance(source, Path)
    assert isinstance(output, Path)
    assert isinstance(job, Path)
    assert source == (
        tmp_path
        / ".name-atlas"
        / "connected-demo"
        / "replay"
        / "fixture"
        / "sofia-apollo"
    )
    assert output == (
        tmp_path / ".name-atlas" / "connected-demo" / "replay" / "results"
    )
    assert job == (
        tmp_path / ".name-atlas" / "connected-demo" / "replay" / "state" / "job.json"
    )
    assert source not in job.parents
    assert job.parent not in source.parents
    assert output not in job.parents
    assert job.parent not in output.parents


@pytest.mark.anyio
async def test_browser_refuses_cross_mode_label_for_persisted_replay_job(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _fixture, origin, _change_path = await _create_recorded_hero_origin(tmp_path)

    assert (
        connected_browser_cli._run_connected_browser(
            mode="live",
            source=None,
            output=None,
            job=origin.job_path,
            port=8765,
            demo=False,
        )
        == 2
    )
    error = capsys.readouterr().err
    assert "persisted job was created in 'replay' mode" in error
    assert "restart with --mode replay" in error


@pytest.mark.anyio
async def test_recorded_hero_converges_with_keyless_receiver_and_restore(
    tmp_path: Path,
) -> None:
    replay = _recording(HERO_RECORDING)
    assert replay.fixture_kind == "hero"
    assert replay.clarification_question is None
    assert len(replay.turns) == 3

    fixture = materialize_hero_fixture(tmp_path / "fixtures")
    sofia_before = _tree(fixture.sofia_root)
    martin_before = _tree(fixture.martin_root)
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    jobs = tmp_path / "jobs"
    origin_output.mkdir()
    receiver_output.mkdir()
    jobs.mkdir()

    provider = RecordedPlannerProvider(replay)
    origin = await ConnectedOriginPlanningService().start(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        job_path=jobs / "origin.json",
        request=HERO_REQUEST,
        idempotency_key="release-recorded-hero-origin",
        provider=provider,
    )
    assert origin.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert provider.consumed_count == 3
    assert isinstance(origin.authority, GptPlannedJobAuthorityV2)
    assert origin.authority.evidence_ledger is not None
    assert origin.authority.evidence_ledger.provider_kind == "recorded_replay"
    assert origin.authority.evidence_ledger.usage == ()

    change_path, _change_id, _origin_receipt = (
        ConnectedChangeJobService().get_change_file(origin.job_path)
    )
    receiver = ConnectedChangeJobService().start_application(
        change_file_path=change_path,
        source_root=fixture.martin_root,
        output_parent=receiver_output,
        job_path=jobs / "receiver.json",
        idempotency_key="release-recorded-hero-receiver",
    )
    assert receiver.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert _verified_commitment(receiver) == _verified_commitment(origin)

    restored = ConnectedChangeJobService().recreate_original(
        receiver.job_path,
        tmp_path / "martin-restored",
    )
    assert all(check.passed for check in restored.checks)
    assert _tree(restored.destination) == martin_before
    assert _tree(fixture.sofia_root) == sofia_before
    assert _tree(fixture.martin_root) == martin_before


@pytest.mark.anyio
async def test_recorded_ambiguity_asks_one_question_then_verifies(
    tmp_path: Path,
) -> None:
    replay = _recording(AMBIGUITY_RECORDING)
    assert replay.fixture_kind == "clarification"
    assert replay.clarification_question is not None
    assert replay.clarification_answer == AMBIGUITY_ANSWER
    assert len(replay.turns) == 3

    fixture = materialize_ambiguity_fixture(tmp_path / "fixture")
    source_before = _tree(fixture.source_root)
    output = tmp_path / "output"
    jobs = tmp_path / "jobs"
    output.mkdir()
    jobs.mkdir()
    service = ConnectedOriginPlanningService()
    waiting = await service.start(
        source_root=fixture.source_root,
        output_parent=output,
        job_path=jobs / "ambiguity.json",
        request=AMBIGUITY_REQUEST,
        idempotency_key="release-recorded-ambiguity",
        provider=RecordedPlannerProvider(replay),
    )
    assert waiting.lifecycle is FolderJobLifecycleV2.AWAITING_CLARIFICATION
    assert waiting.authority.planner_checkpoint.clarification_question == (
        replay.clarification_question
    )

    verified = await service.answer(
        waiting.job_path,
        continuation_token=waiting.job_id,
        answer=AMBIGUITY_ANSWER,
        provider=RecordedPlannerProvider(replay),
    )
    assert verified.lifecycle is FolderJobLifecycleV2.VERIFIED
    assert isinstance(verified.authority, GptPlannedJobAuthorityV2)
    checkpoint = verified.authority.planner_checkpoint
    clarification_calls = sum(
        type(call).__name__ == "RequestClarificationCall"
        for turn in checkpoint.progress.turns
        for call in turn.tool_calls
    )
    assert clarification_calls == 1
    assert checkpoint.clarification_question == replay.clarification_question
    assert checkpoint.clarification_answer == AMBIGUITY_ANSWER
    assert verified.authority.evidence_ledger is not None
    assert verified.authority.evidence_ledger.provider_kind == "recorded_replay"
    assert verified.authority.evidence_ledger.usage == ()
    _verified_commitment(verified)

    restored = ConnectedChangeJobService().recreate_original(
        verified.job_path,
        tmp_path / "ambiguity-restored",
    )
    assert all(check.passed for check in restored.checks)
    assert _tree(restored.destination) == source_before
    assert _tree(fixture.source_root) == source_before


@pytest.mark.anyio
async def test_release_hero_refuses_every_equivalence_change_without_output(
    tmp_path: Path,
) -> None:
    fixture, _origin, change_path = await _create_recorded_hero_origin(tmp_path)
    change_before = change_path.read_bytes()
    mutations = (
        (
            "payload",
            "receiver_payload_changed",
            lambda root: (root / "ready/report.pdf").write_bytes(
                b"changed final report payload\n"
            ),
        ),
        (
            "markdown-prose",
            "receiver_markdown_content_changed",
            lambda root: (root / "desk/project-overview.md").write_bytes(
                (root / "desk/project-overview.md")
                .read_bytes()
                .replace(b"The notes separate", b"Changed notes separate", 1)
            ),
        ),
        (
            "markdown-relationship",
            "receiver_relationship_changed",
            lambda root: (root / "desk/project-overview.md").write_bytes(
                (root / "desk/project-overview.md")
                .read_bytes()
                .replace(
                    b"../conversations/kickoff.md#kickoff",
                    b"../conversations/approval.md#kickoff",
                    1,
                )
            ),
        ),
        (
            "protected-member",
            "receiver_protected_member_mismatch",
            lambda root: (root / ".env.example").write_bytes(
                b"NAME_ATLAS_DEMO=changed\n"
            ),
        ),
    )

    for name, expected_blocker, mutate in mutations:
        receiver = tmp_path / f"receiver-{name}"
        output = tmp_path / f"output-{name}"
        shutil.copytree(fixture.martin_root, receiver)
        output.mkdir()
        mutate(receiver)
        receiver_before = _tree(receiver)

        with pytest.raises(ConnectedChangeError) as raised:
            apply_connected_change(
                change_file_path=change_path,
                source_root=receiver,
                output_parent=output,
            )

        assert raised.value.code == expected_blocker
        assert tuple(output.iterdir()) == ()
        assert _tree(receiver) == receiver_before
        assert change_path.read_bytes() == change_before


@pytest.mark.anyio
async def test_release_hero_refuses_change_file_fingerprint_mismatch(
    tmp_path: Path,
) -> None:
    fixture, _origin, change_path = await _create_recorded_hero_origin(tmp_path)
    receiver_before = _tree(fixture.martin_root)
    payload = json.loads(change_path.read_bytes())
    payload["core"]["request"] += " altered"
    tampered = tmp_path / "tampered.nameatlas-change.json"
    tampered.write_bytes(canonical_json_bytes(payload))
    output = tmp_path / "receiver-output"
    output.mkdir()

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=tampered,
            source_root=fixture.martin_root,
            output_parent=output,
        )

    assert raised.value.code == "change_file_fingerprint_mismatch"
    assert tuple(output.iterdir()) == ()
    assert _tree(fixture.martin_root) == receiver_before


@pytest.mark.anyio
async def test_release_hero_receipt_rejects_bagit_valid_plan_alteration(
    tmp_path: Path,
) -> None:
    _fixture, origin, _change_path = await _create_recorded_hero_origin(tmp_path)
    assert origin.final_result_path is not None
    altered = tmp_path / "altered-result"
    shutil.copytree(origin.final_result_path, altered)
    accepted_path = altered / ACCEPTED_PLAN_PATH
    payload = json.loads(accepted_path.read_bytes())
    mapping = next(
        item
        for item in payload["file_mappings"]
        if item["original_path"] == "briefing/Apollo-client-brief.md"
    )
    mapping["target_path"] = "syntactically-valid/changed-target.md"
    accepted_path.write_bytes(canonical_portable_json_bytes(payload))
    BagItWriter().finalize_tagmanifest(altered)

    assert BagItPackageValidator().validate(altered).valid is True
    verification = verify_connected_result(altered)
    assert verification.status is ConnectedReceiptVerificationStatus.BLOCKED
    assert verification.failed_check_ids == ("artifact_digest_mismatch:accepted_plan",)


def test_release_symmetric_fixture_blocks_without_guessing(tmp_path: Path) -> None:
    fixture = make_symmetric_fixture(tmp_path / "symmetric")
    inventory = scan_folder(fixture.origin_root).inventory
    origin_output = tmp_path / "symmetric-origin-output"
    receiver_output = tmp_path / "symmetric-receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.origin_root,
        output_parent=origin_output,
        request="Organize every file and preserve every supported link.",
        result_folder_name="organized-copy",
        target_by_original_path={
            item.relative_path: f"organized/{item.relative_path}"
            for item in inventory.files
        },
    )
    receiver_before = _tree(fixture.receiver_root)

    with pytest.raises(ConnectedChangeError) as raised:
        apply_connected_change(
            change_file_path=origin.change_file_path,
            source_root=fixture.receiver_root,
            output_parent=receiver_output,
        )

    assert raised.value.code == "receiver_ambiguous_duplicate_group"
    assert tuple(receiver_output.iterdir()) == ()
    assert _tree(fixture.receiver_root) == receiver_before
