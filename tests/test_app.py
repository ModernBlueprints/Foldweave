"""Application-shell tests."""

import httpx
import pytest

from name_atlas.app import create_app
from name_atlas.config import RuntimeConfig
from name_atlas.domain import RunMode


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_replay_shell_exposes_safe_runtime_status() -> None:
    config = RuntimeConfig.from_environment(mode=RunMode.REPLAY, environ={})
    transport = httpx.ASGITransport(app=create_app(config))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/")
        health = await client.get("/healthz")

    assert response.status_code == 200
    assert "Refactor the collection." in response.text
    assert "Replay provider configured" in response.text
    assert "loopback only" in response.text
    assert health.json() == {
        "status": "blocked",
        "mode": "replay",
        "model": "gpt-5.6",
        "api_key_configured": False,
    }


@pytest.mark.anyio
async def test_live_shell_is_blocked_without_api_key() -> None:
    config = RuntimeConfig.from_environment(mode=RunMode.LIVE, environ={})
    transport = httpx.ASGITransport(app=create_app(config))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        health = await client.get("/healthz")

    assert health.json()["status"] == "blocked"
    assert "OPENAI_API_KEY" not in str(health.json())
