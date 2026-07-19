"""Provider-free Connected Change command dispatch tests."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from connected_change_fixtures import make_connected_change_fixture

from name_atlas.connected_cli import run_apply_change
from name_atlas.folder_refactor.connected_change.service import (
    create_connected_change_origin,
)

_FORBIDDEN_IMPORTS = (
    "name_atlas.cli",
    "name_atlas.folder_refactor.planner",
    "name_atlas.decision_cards.budget",
    "name_atlas.decision_cards.providers",
    "name_atlas.folder_refactor.planner_provider",
    "openai",
)


def test_apply_change_early_dispatch_is_provider_free_and_idempotent(
    tmp_path: Path,
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    job_path = tmp_path / "jobs" / "receiver.json"
    budget_path = tmp_path / "api_budget.json"
    budget_path.write_bytes(b'{"sentinel":"must-remain-byte-identical"}\n')
    before_budget = _sha256(budget_path)
    source_before = {
        path.relative_to(fixture.martin_root).as_posix(): path.read_bytes()
        for path in fixture.martin_root.rglob("*")
        if path.is_file()
    }
    change_before = origin.change_file_path.read_bytes()
    script = """
import builtins
import hashlib
import json
import os
import socket
import sys

forbidden = {
    "name_atlas.cli",
    "name_atlas.folder_refactor.planner",
    "name_atlas.decision_cards.budget",
    "name_atlas.decision_cards.providers",
    "name_atlas.folder_refactor.planner_provider",
    "openai",
}
real_import = builtins.__import__
network_attempts = []
credential_reads = []

def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name in forbidden or name.startswith("openai."):
        raise AssertionError(f"forbidden import: {name}")
    return real_import(name, globals, locals, fromlist, level)

class GuardedEnvironment(dict):
    def __getitem__(self, key):
        if key == "OPENAI_API_KEY":
            credential_reads.append(key)
            raise AssertionError("receiver read OPENAI_API_KEY")
        return super().__getitem__(key)

    def get(self, key, default=None):
        if key == "OPENAI_API_KEY":
            credential_reads.append(key)
            raise AssertionError("receiver read OPENAI_API_KEY")
        return super().get(key, default)

def blocked_connection(*args, **kwargs):
    network_attempts.append((repr(args), repr(kwargs)))
    raise AssertionError("receiver attempted an external connection")

builtins.__import__ = guarded_import
os.environ = GuardedEnvironment(os.environ)
socket.create_connection = blocked_connection
socket.socket.connect = blocked_connection
socket.socket.connect_ex = blocked_connection

from name_atlas.launcher import run
from name_atlas.folder_refactor.connected_change.job_v2 import (
    FolderRefactorJobV2Store,
)

budget = sys.argv[5]
before = hashlib.sha256(open(budget, "rb").read()).hexdigest()
arguments = [
    "apply-change",
    sys.argv[1],
    "--source",
    sys.argv[2],
    "--output",
    sys.argv[3],
    "--job",
    sys.argv[4],
]
first = run(arguments)
second = run(arguments)
after = hashlib.sha256(open(budget, "rb").read()).hexdigest()
job = FolderRefactorJobV2Store(__import__("pathlib").Path(sys.argv[4])).inspect()
origin = job.authority.execution_origin
print("RESULT_JSON=" + json.dumps({
    "first": first,
    "second": second,
    "budget_unchanged": before == after,
    "forbidden_imported": sorted(forbidden.intersection(sys.modules)),
    "network_attempts": network_attempts,
    "credential_reads": credential_reads,
    "provider_call_count": origin.provider_call_count,
    "api_used": origin.api_used,
    "external_network_used": origin.external_network_used,
}))
"""
    environment = os.environ.copy()
    environment["OPENAI_API_KEY"] = "test-value-that-must-not-be-used"
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(origin.change_file_path),
            str(fixture.martin_root),
            str(receiver_output),
            str(job_path),
            str(budget_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert completed.returncode == 0, completed.stderr
    result_line = next(
        line
        for line in completed.stdout.splitlines()
        if line.startswith("RESULT_JSON=")
    )
    result = json.loads(result_line.removeprefix("RESULT_JSON="))
    assert result == {
        "first": 0,
        "second": 0,
        "budget_unchanged": True,
        "forbidden_imported": [],
        "network_attempts": [],
        "credential_reads": [],
        "provider_call_count": 0,
        "api_used": False,
        "external_network_used": False,
    }
    assert _sha256(budget_path) == before_budget
    assert len(tuple(receiver_output.iterdir())) == 1
    assert origin.change_file_path.read_bytes() == change_before
    assert {
        path.relative_to(fixture.martin_root).as_posix(): path.read_bytes()
        for path in fixture.martin_root.rglob("*")
        if path.is_file()
    } == source_before


def test_apply_change_default_paths_are_separate_and_resume_exactly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    origin_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.chdir(workspace)

    exit_code = run_apply_change(
        [
            str(origin.change_file_path),
            "--source",
            str(fixture.martin_root),
        ]
    )

    assert exit_code == 0
    output = workspace / ".name-atlas" / "folder-results"
    jobs = workspace / ".name-atlas" / "jobs"
    assert output.is_dir()
    assert len(tuple(output.iterdir())) == 1
    assert len(tuple(jobs.glob("*.json"))) == 1
    assert "VERIFIED " in capsys.readouterr().out


def test_installed_name_atlas_command_uses_the_early_launcher(tmp_path: Path) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    receiver_output = tmp_path / "receiver-output"
    origin_output.mkdir()
    receiver_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    job_path = tmp_path / "jobs" / "installed-command.json"
    executable = Path(sys.executable).with_name("name-atlas")

    command = [
        str(executable),
        "apply-change",
        str(origin.change_file_path),
        "--source",
        str(fixture.martin_root),
        "--output",
        str(receiver_output),
        "--job",
        str(job_path),
    ]
    environment = {
        key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"
    }
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert completed.returncode == 0, completed.stderr
    assert "VERIFIED " in completed.stdout
    assert f"JOB {job_path.resolve()}" in completed.stdout
    first_job_bytes = job_path.read_bytes()
    repeated = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )
    assert repeated.returncode == 0, repeated.stderr
    assert repeated.stdout == completed.stdout
    assert job_path.read_bytes() == first_job_bytes
    assert len(tuple(receiver_output.iterdir())) == 1


def test_default_paths_do_not_create_state_inside_selected_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = make_connected_change_fixture(tmp_path / "projects")
    origin_output = tmp_path / "origin-output"
    origin_output.mkdir()
    origin = create_connected_change_origin(
        source_root=fixture.sofia_root,
        output_parent=origin_output,
        request=fixture.request,
        result_folder_name=fixture.result_name,
        target_by_original_path=fixture.target_paths,
    )
    monkeypatch.chdir(fixture.martin_root)

    exit_code = run_apply_change(
        [
            str(origin.change_file_path),
            "--source",
            str(fixture.martin_root),
        ]
    )

    assert exit_code == 1
    assert not (fixture.martin_root / ".name-atlas").exists()
    assert "APPLY BLOCKED" in capsys.readouterr().err


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
