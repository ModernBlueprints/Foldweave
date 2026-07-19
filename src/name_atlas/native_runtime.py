"""Health-gated pywebview lifecycle over one FastAPI loopback control plane."""

from __future__ import annotations

import fcntl
import http.client
import json
import os
import socket
import stat
import threading
import time
from contextlib import suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import uvicorn
from fastapi import FastAPI

LOOPBACK_HOST = "127.0.0.1"
STARTUP_TIMEOUT_SECONDS = 15.0
HEALTH_REQUEST_TIMEOUT_SECONDS = 0.5
HEALTH_POLL_INTERVAL_SECONDS = 0.05
GRACEFUL_SHUTDOWN_SECONDS = 130.0
FORCED_SHUTDOWN_SECONDS = 5.0


class NativeRuntimeError(RuntimeError):
    """One stable native lifecycle failure."""


class NativeInstanceAlreadyRunning(NativeRuntimeError):
    """The state root already has a live native owner."""


class WebviewBackend(Protocol):
    """The only pywebview calls owned by the native composition root."""

    def create_window(self, title: str, url: str, **kwargs: Any) -> object: ...

    def start(self, **kwargs: Any) -> None: ...


class PywebviewBackend:
    """Lazy pywebview adapter so non-native commands do not import Cocoa."""

    def create_window(self, title: str, url: str, **kwargs: Any) -> object:
        import webview

        return webview.create_window(title, url, **kwargs)

    def start(self, **kwargs: Any) -> None:
        import webview

        webview.start(**kwargs)


@dataclass(slots=True)
class SingleInstanceLock:
    """One kernel-owned nonblocking process lock below the stable state root."""

    path: Path
    _descriptor: int | None = field(default=None, init=False, repr=False)

    def acquire(self) -> None:
        if self._descriptor is not None:
            return
        if not self.path.is_absolute():
            raise NativeRuntimeError("Native instance lock path must be absolute.")
        self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        metadata = self.path.parent.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise NativeRuntimeError("Native instance lock parent is not a directory.")
        descriptor = os.open(
            self.path,
            os.O_CREAT | os.O_RDWR | os.O_CLOEXEC | os.O_NOFOLLOW,
            0o600,
        )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            os.close(descriptor)
            raise NativeInstanceAlreadyRunning(
                "Foldweave is already running for this state root."
            ) from exc
        except BaseException:
            os.close(descriptor)
            raise
        self._descriptor = descriptor

    def release(self) -> None:
        descriptor = self._descriptor
        self._descriptor = None
        if descriptor is None:
            return
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)

    def __enter__(self) -> SingleInstanceLock:
        self.acquire()
        return self

    def __exit__(self, *_: object) -> None:
        self.release()


@dataclass(slots=True)
class LoopbackServer:
    """Own one pre-bound ephemeral socket and one bounded Uvicorn thread."""

    app: FastAPI
    instance_nonce: str
    startup_timeout_seconds: float = STARTUP_TIMEOUT_SECONDS
    graceful_shutdown_seconds: float = GRACEFUL_SHUTDOWN_SECONDS
    forced_shutdown_seconds: float = FORCED_SHUTDOWN_SECONDS
    _socket: socket.socket | None = field(default=None, init=False, repr=False)
    _server: uvicorn.Server | None = field(default=None, init=False, repr=False)
    _thread: threading.Thread | None = field(default=None, init=False, repr=False)
    _port: int | None = field(default=None, init=False)

    @property
    def port(self) -> int:
        if self._port is None:
            raise NativeRuntimeError("Loopback server has not started.")
        return self._port

    @property
    def url(self) -> str:
        return f"http://{LOOPBACK_HOST}:{self.port}"

    @property
    def thread_alive(self) -> bool:
        return bool(self._thread is not None and self._thread.is_alive())

    def start(self) -> None:
        if self._thread is not None:
            raise NativeRuntimeError("Loopback server can only be started once.")
        bound = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bound.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            bound.bind((LOOPBACK_HOST, 0))
            bound.listen(socket.SOMAXCONN)
            port = int(bound.getsockname()[1])
            config = uvicorn.Config(
                self.app,
                host=LOOPBACK_HOST,
                port=port,
                loop="asyncio",
                http="h11",
                lifespan="on",
                log_level="warning",
                access_log=False,
                reload=False,
                workers=1,
            )
            server = uvicorn.Server(config)
            thread = threading.Thread(
                target=server.run,
                kwargs={"sockets": [bound]},
                name="foldweave-loopback",
                daemon=False,
            )
            self._socket = bound
            self._port = port
            self._server = server
            self._thread = thread
            thread.start()
            self._wait_for_health()
        except BaseException:
            self.stop()
            raise

    def request_stop(self) -> None:
        if self._server is not None:
            self._server.should_exit = True

    def stop(self) -> None:
        thread = self._thread
        server = self._server
        if server is not None:
            server.should_exit = True
        if thread is not None and thread.is_alive():
            thread.join(self.graceful_shutdown_seconds)
        if thread is not None and thread.is_alive() and server is not None:
            server.force_exit = True
            thread.join(self.forced_shutdown_seconds)
        remaining_alive = bool(thread is not None and thread.is_alive())
        owned_socket = self._socket
        self._socket = None
        if owned_socket is not None:
            with suppress(OSError):
                owned_socket.close()
        if remaining_alive:
            raise NativeRuntimeError(
                "Foldweave loopback server did not terminate cleanly."
            )

    def _wait_for_health(self) -> None:
        deadline = time.monotonic() + self.startup_timeout_seconds
        latest_error: BaseException | None = None
        while time.monotonic() < deadline:
            if self._thread is not None and not self._thread.is_alive():
                break
            try:
                connection = http.client.HTTPConnection(
                    LOOPBACK_HOST,
                    self.port,
                    timeout=HEALTH_REQUEST_TIMEOUT_SECONDS,
                )
                connection.request("GET", "/healthz", headers={"Host": "127.0.0.1"})
                response = connection.getresponse()
                payload = response.read()
                cache_control = response.getheader("Cache-Control")
                connection.close()
                parsed = json.loads(payload.decode("utf-8", errors="strict"))
                if (
                    response.status == 200
                    and cache_control == "no-store"
                    and parsed
                    == {
                        "application": "Foldweave",
                        "instance_nonce": self.instance_nonce,
                        "ready": True,
                    }
                ):
                    return
                latest_error = NativeRuntimeError("Health response was not exact.")
            except (OSError, UnicodeDecodeError, ValueError) as exc:
                latest_error = exc
            time.sleep(HEALTH_POLL_INTERVAL_SECONDS)
        raise NativeRuntimeError(
            "Foldweave loopback server did not become healthy."
        ) from latest_error


def run_native_window(
    *,
    app: FastAPI,
    instance_nonce: str,
    lock_path: Path,
    backend: WebviewBackend | None = None,
    title: str = "Foldweave",
) -> None:
    """Run one main-thread native window and leave no loopback server behind."""

    if threading.current_thread() is not threading.main_thread():
        raise NativeRuntimeError(
            "Foldweave native runtime must start on the main thread."
        )
    webview = backend or PywebviewBackend()
    with SingleInstanceLock(lock_path):
        server = LoopbackServer(app=app, instance_nonce=instance_nonce)
        try:
            server.start()
            window = webview.create_window(
                title,
                server.url,
                width=1440,
                height=900,
                min_size=(960, 640),
                resizable=True,
                text_select=True,
                zoomable=False,
                js_api=None,
            )
            events = getattr(window, "events", None)
            closed = getattr(events, "closed", None)
            if closed is not None:
                closed += lambda: server.request_stop()
            webview.start(private_mode=True, debug=False)
        finally:
            server.stop()
