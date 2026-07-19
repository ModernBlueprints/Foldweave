"""Bounded native adapter tests with no real GUI process."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import pytest

import name_atlas.native_bridge as native_bridge_module
from name_atlas.native_bridge import (
    FIXED_PICKER_SCRIPTS,
    MacOSNativePathBridge,
    NativeOpenStatus,
    NativePathRole,
    NativeSelectionStatus,
)


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


class _FakeProcess:
    def __init__(
        self,
        *,
        stdout: bytes = b"",
        stderr: bytes = b"",
        returncode: int = 0,
        communicate_gate: asyncio.Event | None = None,
        exit_on_terminate: bool = True,
        communicate_error: OSError | None = None,
    ) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.final_returncode = returncode
        self.returncode: int | None = None
        self.communicate_gate = communicate_gate
        self.exit_on_terminate = exit_on_terminate
        self.communicate_error = communicate_error
        self.communicate_started = asyncio.Event()
        self.exit_event = asyncio.Event()
        self.terminate_calls = 0
        self.kill_calls = 0
        self.wait_calls = 0

    async def communicate(self) -> tuple[bytes, bytes]:
        self.communicate_started.set()
        if self.communicate_gate is not None:
            await self.communicate_gate.wait()
        if self.communicate_error is not None:
            raise self.communicate_error
        self.returncode = self.final_returncode
        self.exit_event.set()
        return self.stdout, self.stderr

    def terminate(self) -> None:
        self.terminate_calls += 1
        if self.exit_on_terminate:
            self.returncode = -15
            self.exit_event.set()

    def kill(self) -> None:
        self.kill_calls += 1
        self.returncode = -9
        self.exit_event.set()

    async def wait(self) -> int:
        self.wait_calls += 1
        await self.exit_event.wait()
        assert self.returncode is not None
        return self.returncode


class _FakeProcessFactory:
    def __init__(self, *processes: _FakeProcess) -> None:
        self.processes = list(processes)
        self.calls: list[tuple[str, tuple[str, ...], dict[str, Any]]] = []
        self.error: OSError | None = None

    async def __call__(
        self,
        program: str,
        *args: str,
        **kwargs: Any,
    ) -> _FakeProcess:
        self.calls.append((program, args, kwargs))
        if self.error is not None:
            raise self.error
        assert self.processes
        return self.processes.pop(0)


@pytest.fixture(autouse=True)
def executable_utilities(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(native_bridge_module, "_is_executable", lambda _path: True)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("role", "chooser", "prompt"),
    (
        (
            NativePathRole.SOURCE_FOLDER,
            "choose folder",
            "Choose the folder to organize",
        ),
        (
            NativePathRole.OUTPUT_PARENT,
            "choose folder",
            "Choose where Foldweave should create the result",
        ),
        (
            NativePathRole.CHANGE_FILE,
            "choose file",
            "Choose a Foldweave Change File",
        ),
        (
            NativePathRole.RESTORE_DESTINATION,
            "choose folder",
            "Choose where Foldweave should recreate the original layout",
        ),
    ),
)
async def test_picker_roles_use_only_fixed_shell_free_scripts(
    role: NativePathRole,
    chooser: str,
    prompt: str,
) -> None:
    process = _FakeProcess(stdout=b"NAME_ATLAS_SELECTED\n/Users/example/project\n")
    factory = _FakeProcessFactory(process)
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=factory,
    )

    selection = await bridge.choose_path(role)

    assert selection.status is NativeSelectionStatus.SELECTED
    assert selection.path == Path("/Users/example/project")
    assert selection.reason_code is None
    assert factory.calls == [
        (
            "/usr/bin/osascript",
            ("-e", FIXED_PICKER_SCRIPTS[role]),
            {
                "stdout": asyncio.subprocess.PIPE,
                "stderr": asyncio.subprocess.PIPE,
            },
        )
    ]
    assert chooser in FIXED_PICKER_SCRIPTS[role]
    assert prompt in FIXED_PICKER_SCRIPTS[role]
    assert "shell" not in factory.calls[0][2]


@pytest.mark.anyio
async def test_picker_preserves_a_path_terminal_newline() -> None:
    process = _FakeProcess(stdout=b"NAME_ATLAS_SELECTED\n/Users/example/line-ended\n\n")
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(process),
    )

    selection = await bridge.choose_path(NativePathRole.SOURCE_FOLDER)

    assert selection.path == Path("/Users/example/line-ended\n")


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("stdout", "returncode", "status", "reason_code"),
    (
        (
            b"NAME_ATLAS_CANCELLED\n",
            0,
            NativeSelectionStatus.CANCELLED,
            "picker_cancelled",
        ),
        (b"", 0, NativeSelectionStatus.FAILED, "picker_output_invalid"),
        (b"unexpected\n", 0, NativeSelectionStatus.FAILED, "picker_output_invalid"),
        (
            b"NAME_ATLAS_SELECTED\nrelative/path\n",
            0,
            NativeSelectionStatus.FAILED,
            "picker_output_invalid",
        ),
        (
            b"NAME_ATLAS_SELECTED\n/absolute/with\x00nul\n",
            0,
            NativeSelectionStatus.FAILED,
            "picker_output_invalid",
        ),
        (
            b"NAME_ATLAS_SELECTED\n/invalid/\xff\n",
            0,
            NativeSelectionStatus.FAILED,
            "picker_output_invalid",
        ),
        (b"ignored\n", 7, NativeSelectionStatus.FAILED, "picker_failed"),
    ),
)
async def test_picker_distinguishes_cancel_and_invalid_or_failed_output(
    stdout: bytes,
    returncode: int,
    status: NativeSelectionStatus,
    reason_code: str,
) -> None:
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(
            _FakeProcess(stdout=stdout, returncode=returncode)
        ),
    )

    selection = await bridge.choose_path(NativePathRole.SOURCE_FOLDER)

    assert selection.status is status
    assert selection.reason_code == reason_code
    assert selection.path is None


@pytest.mark.anyio
async def test_picker_rejects_oversized_output() -> None:
    process = _FakeProcess(
        stdout=b"NAME_ATLAS_SELECTED\n/" + b"a" * (16 * 1024) + b"\n"
    )
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(process),
    )

    selection = await bridge.choose_path(NativePathRole.SOURCE_FOLDER)

    assert selection.status is NativeSelectionStatus.FAILED
    assert selection.reason_code == "picker_output_invalid"
    assert selection.path is None


@pytest.mark.anyio
async def test_picker_is_unavailable_without_macos_or_executable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    factory = _FakeProcessFactory()
    linux = MacOSNativePathBridge(
        platform_name="linux",
        process_factory=factory,
    )

    unsupported = await linux.choose_path(NativePathRole.SOURCE_FOLDER)
    monkeypatch.setattr(native_bridge_module, "_is_executable", lambda _path: False)
    missing = await MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=factory,
    ).choose_path(NativePathRole.SOURCE_FOLDER)

    assert unsupported.status is NativeSelectionStatus.UNAVAILABLE
    assert missing.status is NativeSelectionStatus.UNAVAILABLE
    assert unsupported.path is None and missing.path is None
    assert factory.calls == []


@pytest.mark.anyio
async def test_picker_spawn_or_communication_failure_returns_no_path() -> None:
    spawn_factory = _FakeProcessFactory()
    spawn_factory.error = OSError("not exposed")
    spawn_bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=spawn_factory,
    )
    communication = _FakeProcess(communicate_error=OSError("not exposed"))
    communication_bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(communication),
    )

    spawn_result = await spawn_bridge.choose_path(NativePathRole.CHANGE_FILE)
    communication_result = await communication_bridge.choose_path(
        NativePathRole.CHANGE_FILE
    )

    assert spawn_result.status is NativeSelectionStatus.FAILED
    assert communication_result.status is NativeSelectionStatus.FAILED
    assert spawn_result.path is None and communication_result.path is None
    assert communication.terminate_calls == 1
    assert communication.wait_calls == 1


@pytest.mark.anyio
@pytest.mark.parametrize("exit_on_terminate", (True, False))
async def test_picker_timeout_terminates_and_always_reaps(
    exit_on_terminate: bool,
) -> None:
    process = _FakeProcess(
        communicate_gate=asyncio.Event(),
        exit_on_terminate=exit_on_terminate,
    )
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        picker_timeout_seconds=0.001,
        termination_grace_seconds=0.001,
        process_factory=_FakeProcessFactory(process),
    )

    selection = await bridge.choose_path(NativePathRole.SOURCE_FOLDER)

    assert selection.status is NativeSelectionStatus.TIMEOUT
    assert selection.path is None
    assert process.terminate_calls == 1
    assert process.kill_calls == (0 if exit_on_terminate else 1)
    assert process.wait_calls >= 1
    assert process.returncode in {-15, -9}


@pytest.mark.anyio
async def test_only_one_picker_process_can_run() -> None:
    release = asyncio.Event()
    first_process = _FakeProcess(
        stdout=b"NAME_ATLAS_SELECTED\n/Users/example/project\n",
        communicate_gate=release,
    )
    first_factory = _FakeProcessFactory(first_process)
    second_factory = _FakeProcessFactory(
        _FakeProcess(stdout=b"NAME_ATLAS_SELECTED\n/never/opened\n")
    )
    first_bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=first_factory,
    )
    second_bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=second_factory,
    )

    first_task = asyncio.create_task(
        first_bridge.choose_path(NativePathRole.SOURCE_FOLDER)
    )
    await first_process.communicate_started.wait()
    second = await second_bridge.choose_path(NativePathRole.CHANGE_FILE)
    release.set()
    first = await first_task

    assert first.status is NativeSelectionStatus.SELECTED
    assert second.status is NativeSelectionStatus.FAILED
    assert second.reason_code == "picker_busy"
    assert second.path is None
    assert len(first_factory.calls) == 1
    assert second_factory.calls == []


@pytest.mark.anyio
async def test_cancelled_picker_task_terminates_reaps_and_releases_lock() -> None:
    blocked_process = _FakeProcess(communicate_gate=asyncio.Event())
    first_bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(blocked_process),
    )
    next_process = _FakeProcess(stdout=b"NAME_ATLAS_SELECTED\n/Users/example/next\n")
    next_bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(next_process),
    )

    cancelled_task = asyncio.create_task(
        first_bridge.choose_path(NativePathRole.SOURCE_FOLDER)
    )
    await blocked_process.communicate_started.wait()
    cancelled_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await cancelled_task
    next_selection = await next_bridge.choose_path(NativePathRole.SOURCE_FOLDER)

    assert blocked_process.terminate_calls == 1
    assert blocked_process.wait_calls == 1
    assert blocked_process.returncode == -15
    assert next_selection.status is NativeSelectionStatus.SELECTED


@pytest.mark.anyio
async def test_finder_opens_only_exact_real_directory_without_shell(
    tmp_path: Path,
) -> None:
    result_data = tmp_path / "verified-result" / "data"
    result_data.mkdir(parents=True)
    factory = _FakeProcessFactory(_FakeProcess())
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=factory,
    )

    outcome = await bridge.show_in_finder(result_data)

    assert outcome.status is NativeOpenStatus.OPENED
    assert outcome.reason_code is None
    assert factory.calls == [
        (
            "/usr/bin/open",
            (str(result_data),),
            {
                "stdout": asyncio.subprocess.DEVNULL,
                "stderr": asyncio.subprocess.PIPE,
            },
        )
    ]
    assert "shell" not in factory.calls[0][2]


@pytest.mark.anyio
async def test_finder_rejects_relative_missing_file_and_symlink_paths(
    tmp_path: Path,
) -> None:
    regular_file = tmp_path / "file.txt"
    regular_file.write_text("not a directory", encoding="utf-8")
    real_directory = tmp_path / "real"
    real_directory.mkdir()
    symlink = tmp_path / "link"
    symlink.symlink_to(real_directory, target_is_directory=True)
    factory = _FakeProcessFactory()
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=factory,
    )

    outcomes = [
        await bridge.show_in_finder(Path("relative")),
        await bridge.show_in_finder(tmp_path / "missing"),
        await bridge.show_in_finder(regular_file),
        await bridge.show_in_finder(symlink),
    ]

    assert all(outcome.status is NativeOpenStatus.FAILED for outcome in outcomes)
    assert all(outcome.reason_code == "finder_path_invalid" for outcome in outcomes)
    assert factory.calls == []


@pytest.mark.anyio
async def test_finder_unavailable_spawn_failure_and_nonzero_exit(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    result_data = tmp_path / "data"
    result_data.mkdir()
    never_called = _FakeProcessFactory()
    unsupported = await MacOSNativePathBridge(
        platform_name="linux",
        process_factory=never_called,
    ).show_in_finder(result_data)

    spawn_factory = _FakeProcessFactory()
    spawn_factory.error = OSError("not exposed")
    spawn_failure = await MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=spawn_factory,
    ).show_in_finder(result_data)

    nonzero = await MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=_FakeProcessFactory(_FakeProcess(returncode=3)),
    ).show_in_finder(result_data)

    monkeypatch.setattr(native_bridge_module, "_is_executable", lambda _path: False)
    missing = await MacOSNativePathBridge(
        platform_name="darwin",
        process_factory=never_called,
    ).show_in_finder(result_data)

    assert unsupported.status is NativeOpenStatus.UNAVAILABLE
    assert missing.status is NativeOpenStatus.UNAVAILABLE
    assert spawn_failure.status is NativeOpenStatus.FAILED
    assert nonzero.status is NativeOpenStatus.FAILED
    assert never_called.calls == []


@pytest.mark.anyio
@pytest.mark.parametrize("exit_on_terminate", (True, False))
async def test_finder_timeout_terminates_and_always_reaps(
    tmp_path: Path,
    exit_on_terminate: bool,
) -> None:
    result_data = tmp_path / "data"
    result_data.mkdir()
    process = _FakeProcess(
        communicate_gate=asyncio.Event(),
        exit_on_terminate=exit_on_terminate,
    )
    bridge = MacOSNativePathBridge(
        platform_name="darwin",
        finder_timeout_seconds=0.001,
        termination_grace_seconds=0.001,
        process_factory=_FakeProcessFactory(process),
    )

    outcome = await bridge.show_in_finder(result_data)

    assert outcome.status is NativeOpenStatus.TIMEOUT
    assert process.terminate_calls == 1
    assert process.kill_calls == (0 if exit_on_terminate else 1)
    assert process.wait_calls >= 1
    assert process.returncode in {-15, -9}
