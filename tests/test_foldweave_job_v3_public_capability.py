"""Durable public-capability contract tests for FolderRefactorJobV3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from name_atlas.folder_refactor.connected_change.job_v2 import build_new_gpt_job_v2
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderJobLifecycleV3,
    FolderJobV3RevisionError,
    FolderPublicJobCapabilityV1,
    FolderRefactorJobV3,
    FolderRefactorJobV3Store,
    canonical_job_v3_bytes,
    evolve_job_v3,
    parse_job_v3_bytes,
)
from name_atlas.folder_refactor.serialization import canonical_json_bytes

_RAW_CAPABILITY_ID = "fwjc_" + "A" * 86


def _capability(**updates: Any) -> FolderPublicJobCapabilityV1:
    payload: dict[str, Any] = {
        "capability_id_sha256": hashlib.sha256(
            _RAW_CAPABILITY_ID.encode("ascii")
        ).hexdigest(),
        "device_id": "fwd_" + "d" * 32,
        "oauth_grant_fingerprint": "a" * 64,
        "scopes": (
            "foldweave.execute",
            "foldweave.plan",
            "foldweave.review",
        ),
        "expires_at_ms": 1_800_000,
    }
    payload.update(updates)
    return FolderPublicJobCapabilityV1.model_validate(payload, strict=True)


def _planning_job(
    tmp_path: Path,
    *,
    capability: FolderPublicJobCapabilityV1 | None,
) -> FolderRefactorJobV3:
    source = tmp_path / "source"
    source.mkdir()
    (source / "note.md").write_text("See [asset](asset.txt).\n", encoding="utf-8")
    (source / "asset.txt").write_text("payload\n", encoding="utf-8")
    output = tmp_path / "output"
    output.mkdir()
    seed = build_new_gpt_job_v2(
        source_root=source,
        output_parent=output,
        job_path=tmp_path / "jobs" / "public-capability.json",
        user_request="Organize this project and preserve its supported links.",
        idempotency_key="public-capability-create",
    )
    return FolderRefactorJobV3(
        revision=seed.revision,
        job_id=seed.job_id,
        display_name=seed.display_name,
        created_at=seed.created_at,
        updated_at=seed.updated_at,
        source_root=seed.source_root,
        output_parent=seed.output_parent,
        job_path=seed.job_path,
        source_inventory=seed.source_inventory,
        local_file_identities=seed.local_file_identities,
        local_directory_identities=seed.local_directory_identities,
        user_request=seed.user_request,
        idempotency=seed.idempotency,
        operation_idempotency=seed.operation_idempotency,
        public_job_capability=capability,
        authority=seed.authority,
        lifecycle=FolderJobLifecycleV3.PLANNING,
    )


@pytest.mark.parametrize(
    "updates",
    (
        {"device_id": "another-device"},
        {"capability_id_sha256": "A" * 64},
        {"oauth_grant_fingerprint": "not-a-sha256"},
        {"scopes": ()},
        {"scopes": ("foldweave.plan", "foldweave.execute")},
        {"scopes": ("foldweave.plan", "foldweave.plan")},
        {"scopes": ("foldweave.admin",)},
        {"expires_at_ms": -1},
        {"expires_at_ms": 0},
        {"unexpected": "field"},
    ),
)
def test_public_job_capability_is_strict_and_canonical(
    updates: dict[str, Any],
) -> None:
    with pytest.raises(ValidationError):
        _capability(**updates)


def test_public_job_capability_round_trips_without_raw_capability(
    tmp_path: Path,
) -> None:
    capability = _capability()
    job = _planning_job(tmp_path, capability=capability)

    encoded = canonical_job_v3_bytes(job)
    decoded = json.loads(encoded)

    assert _RAW_CAPABILITY_ID.encode("ascii") not in encoded
    assert decoded["public_job_capability"] == {
        "capability_id_sha256": capability.capability_id_sha256,
        "device_id": capability.device_id,
        "expires_at_ms": capability.expires_at_ms,
        "oauth_grant_fingerprint": capability.oauth_grant_fingerprint,
        "schema_version": "folder-public-job-capability.v1",
        "scopes": [
            "foldweave.execute",
            "foldweave.plan",
            "foldweave.review",
        ],
    }
    assert parse_job_v3_bytes(encoded, expected_path=job.job_path) == job


def test_local_and_pre_capability_v3_jobs_remain_readable(tmp_path: Path) -> None:
    local_job = _planning_job(tmp_path, capability=None)
    canonical = canonical_job_v3_bytes(local_job)

    assert json.loads(canonical)["public_job_capability"] is None
    assert parse_job_v3_bytes(canonical, expected_path=local_job.job_path) == local_job

    historical_payload = local_job.model_dump(mode="json")
    historical_payload.pop("public_job_capability")
    historical_bytes = canonical_json_bytes(historical_payload) + b"\n"
    historical = parse_job_v3_bytes(
        historical_bytes,
        expected_path=local_job.job_path,
    )

    assert historical.public_job_capability is None
    assert historical == local_job


def test_public_job_capability_is_immutable_across_job_transitions(
    tmp_path: Path,
) -> None:
    capability = _capability()
    job = _planning_job(tmp_path, capability=capability)
    store = FolderRefactorJobV3Store(job.job_path)
    replacement = _capability(device_id="fwd_" + "e" * 32)

    with store.writer() as writer:
        current = writer.save_new(job)
        changed = evolve_job_v3(
            current,
            revision=current.revision + 1,
            updated_at=current.updated_at,
            public_job_capability=replacement,
            lifecycle=FolderJobLifecycleV3.BLOCKED,
            blocker_code="capability_contract_test",
            blocker_message="Exercise immutable public authority.",
        )
        with pytest.raises(
            FolderJobV3RevisionError,
            match="changed immutable job identity",
        ):
            writer.save(changed, expected_current=current)

        assert writer.load() == current
        preserved = evolve_job_v3(
            current,
            revision=current.revision + 1,
            updated_at=current.updated_at,
            lifecycle=FolderJobLifecycleV3.BLOCKED,
            blocker_code="capability_contract_test",
            blocker_message="Exercise immutable public authority.",
        )
        saved = writer.save(preserved, expected_current=current)

    assert saved.public_job_capability == capability
    assert store.inspect() == saved
