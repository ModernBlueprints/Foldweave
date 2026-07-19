import http.client
import threading
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from name_atlas.native_runtime import (
    LoopbackServer,
    NativeInstanceAlreadyRunning,
    SingleInstanceLock,
    run_native_window,
)


def _health_app(nonce: str) -> FastAPI:
    app = FastAPI()

    @app.get("/healthz")
    async def health() -> JSONResponse:
        return JSONResponse(
            {
                "application": "Foldweave",
                "instance_nonce": nonce,
                "ready": True,
            },
            headers={"Cache-Control": "no-store"},
        )

    return app


def test_loopback_server_uses_ephemeral_port_and_stops_cleanly() -> None:
    nonce = "a" * 64
    server = LoopbackServer(
        app=_health_app(nonce),
        instance_nonce=nonce,
        graceful_shutdown_seconds=2.0,
        forced_shutdown_seconds=1.0,
    )

    server.start()
    try:
        assert server.port > 0
        assert server.thread_alive is True
        connection = http.client.HTTPConnection("127.0.0.1", server.port, timeout=1)
        connection.request("GET", "/healthz")
        response = connection.getresponse()
        assert response.status == 200
        response.read()
        connection.close()
    finally:
        server.stop()

    assert server.thread_alive is False
    server.stop()


def test_health_nonce_mismatch_stops_failed_server() -> None:
    server = LoopbackServer(
        app=_health_app("b" * 64),
        instance_nonce="c" * 64,
        startup_timeout_seconds=0.2,
        graceful_shutdown_seconds=2.0,
        forced_shutdown_seconds=1.0,
    )

    with pytest.raises(RuntimeError, match="did not become healthy"):
        server.start()

    assert server.thread_alive is False


def test_single_instance_lock_refuses_second_owner(tmp_path: Path) -> None:
    path = tmp_path / "state/runtime.lock"
    first = SingleInstanceLock(path)
    second = SingleInstanceLock(path)

    first.acquire()
    try:
        with pytest.raises(NativeInstanceAlreadyRunning):
            second.acquire()
    finally:
        first.release()

    second.acquire()
    second.release()


class FakeWebview:
    def __init__(self) -> None:
        self.url: str | None = None
        self.start_thread: threading.Thread | None = None

    def create_window(self, title: str, url: str, **kwargs):
        assert title == "Foldweave"
        assert kwargs["js_api"] is None
        self.url = url
        return SimpleNamespace(events=SimpleNamespace(closed=None))

    def start(self, **kwargs) -> None:
        assert kwargs == {"private_mode": True, "debug": False}
        self.start_thread = threading.current_thread()


def test_native_window_health_gates_main_thread_and_leaves_no_listener(
    tmp_path: Path,
) -> None:
    nonce = "d" * 64
    backend = FakeWebview()

    run_native_window(
        app=_health_app(nonce),
        instance_nonce=nonce,
        lock_path=tmp_path / "runtime.lock",
        backend=backend,
    )

    assert backend.url is not None
    assert backend.start_thread is threading.main_thread()
