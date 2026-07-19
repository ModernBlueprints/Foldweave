"""Focused trust-boundary tests for Foldweave direct provider composition."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

import name_atlas.foldweave_provider_factory as provider_factory_module
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.foldweave_paths import FoldweaveBudgetAuthority
from name_atlas.native_settings import DirectEndpointProfile


@dataclass(slots=True)
class _CountingCredentialStore:
    value: str = field(repr=False)
    read_count: int = 0

    def read(self) -> str:
        self.read_count += 1
        return self.value


@dataclass(frozen=True, slots=True)
class _FakeGptAuthority:
    planner_checkpoint: object
    evidence_ledger: object | None = None


def _usage(response_turn: int) -> FolderPlannerUsage:
    return FolderPlannerUsage(
        response_turn=response_turn,
        input_tokens=100 * response_turn,
        output_tokens=20 * response_turn,
        cached_input_tokens=0,
        total_tokens=120 * response_turn,
        estimated_cost_microusd=1_000 * response_turn,
    )


def _install_budget(
    monkeypatch: pytest.MonkeyPatch,
    *,
    expected_path: Path,
    events: list[object],
) -> object:
    budget = object()

    def open_existing(cls: type[object], *, path: Path) -> object:
        del cls
        events.append(("open_budget", path))
        assert path == expected_path
        return budget

    monkeypatch.setattr(
        provider_factory_module.PersistentBudgetLedger,
        "open_existing_foldweave_planner",
        classmethod(open_existing),
    )
    return budget


def _qualification_authority(path: Path) -> FoldweaveBudgetAuthority:
    return FoldweaveBudgetAuthority(kind="qualification_existing", path=path)


def _installation_authority(path: Path) -> FoldweaveBudgetAuthority:
    return FoldweaveBudgetAuthority(kind="installation_persistent", path=path)


def _install_job_authority(
    monkeypatch: pytest.MonkeyPatch,
    *,
    job_path: Path,
    authority: _FakeGptAuthority,
) -> None:
    job_path.parent.mkdir(parents=True, exist_ok=True)
    job_path.write_bytes(b"durable-job-placeholder")

    class FakeStore:
        def __init__(self, path: Path) -> None:
            assert path == job_path

        def inspect(self) -> object:
            return SimpleNamespace(authority=authority)

    monkeypatch.setattr(
        provider_factory_module,
        "GptPlannedJobAuthorityV3",
        _FakeGptAuthority,
    )
    monkeypatch.setattr(
        provider_factory_module,
        "FolderRefactorJobV3Store",
        FakeStore,
    )


def test_initial_provider_is_lazy_and_uses_only_the_official_profile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    secret = "qualification-secret-never-rendered"
    credential_store = _CountingCredentialStore(secret)
    ledger_path = tmp_path / "api-budget.json"
    events: list[object] = []

    budget = _install_budget(
        monkeypatch,
        expected_path=ledger_path,
        events=events,
    )
    provider = object()
    captured: dict[str, Any] = {}

    def from_api_key(api_key: str, **kwargs: Any) -> object:
        events.append("construct_provider")
        captured["api_key"] = api_key
        captured.update(kwargs)
        return provider

    monkeypatch.setattr(
        provider_factory_module.LiveFolderPlannerProvider,
        "from_api_key",
        staticmethod(from_api_key),
    )
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=tmp_path / "jobs" / "absent.json",
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_qualification_authority(ledger_path),
    )

    assert credential_store.read_count == 0
    assert events == []
    assert secret not in repr(factory)

    assert factory.initial_provider() is provider
    assert credential_store.read_count == 1
    assert events == [
        ("open_budget", ledger_path),
        "construct_provider",
    ]
    assert captured == {
        "api_key": secret,
        "base_url": "https://api.openai.com/v1",
        "budget": budget,
        "existing_usage": (),
        "prompt_profile": (provider_factory_module.FOLDWEAVE_PLANNER_PROMPT_PROFILE),
    }
    assert secret not in repr(provider)


def test_installation_authority_opens_lazy_installation_ledger(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    credential_store = _CountingCredentialStore("installation-secret")
    ledger_path = tmp_path / "state" / "api_budget.json"
    installation_budget = object()
    calls: list[Path] = []

    def open_installation(cls: type[object], *, path: Path) -> object:
        del cls
        calls.append(path)
        return installation_budget

    monkeypatch.setattr(
        provider_factory_module.PersistentBudgetLedger,
        "open_foldweave_installation",
        classmethod(open_installation),
    )
    captured: dict[str, Any] = {}

    def from_api_key(api_key: str, **kwargs: Any) -> object:
        captured["api_key"] = api_key
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(
        provider_factory_module.LiveFolderPlannerProvider,
        "from_api_key",
        staticmethod(from_api_key),
    )
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=tmp_path / "jobs" / "absent.json",
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_installation_authority(ledger_path),
    )

    assert calls == []
    assert credential_store.read_count == 0

    factory.initial_provider()

    assert calls == [ledger_path]
    assert captured["budget"] is installation_budget
    assert credential_store.read_count == 1


def test_initial_provider_restores_checkpoint_usage_prefix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checkpoint_usage = (_usage(1), _usage(2))
    job_path = tmp_path / "jobs" / "initial-prefix.json"
    _install_job_authority(
        monkeypatch,
        job_path=job_path,
        authority=_FakeGptAuthority(
            planner_checkpoint=SimpleNamespace(usage=checkpoint_usage),
        ),
    )
    credential_store = _CountingCredentialStore("qualification-secret")
    ledger_path = tmp_path / "api-budget.json"
    events: list[object] = []
    _install_budget(monkeypatch, expected_path=ledger_path, events=events)
    captured: dict[str, Any] = {}

    def from_api_key(api_key: str, **kwargs: Any) -> object:
        captured["api_key"] = api_key
        captured.update(kwargs)
        return object()

    monkeypatch.setattr(
        provider_factory_module.LiveFolderPlannerProvider,
        "from_api_key",
        staticmethod(from_api_key),
    )
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=job_path,
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_qualification_authority(ledger_path),
    )

    factory.initial_provider()

    assert captured["existing_usage"] == checkpoint_usage
    assert credential_store.read_count == 1


def test_revision_provider_restores_complete_composite_usage_prefix(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    checkpoint_usage = (_usage(1),)
    composite_usage = (_usage(1), _usage(2), _usage(3))
    job_path = tmp_path / "jobs" / "revision-prefix.json"
    _install_job_authority(
        monkeypatch,
        job_path=job_path,
        authority=_FakeGptAuthority(
            planner_checkpoint=SimpleNamespace(usage=checkpoint_usage),
            evidence_ledger=SimpleNamespace(usage=composite_usage),
        ),
    )
    credential_store = _CountingCredentialStore("qualification-secret")
    ledger_path = tmp_path / "api-budget.json"
    events: list[object] = []
    budget = _install_budget(
        monkeypatch,
        expected_path=ledger_path,
        events=events,
    )
    captured: dict[str, Any] = {}
    provider = object()

    def from_api_key(api_key: str, **kwargs: Any) -> object:
        captured["api_key"] = api_key
        captured.update(kwargs)
        return provider

    monkeypatch.setattr(
        provider_factory_module.LiveFolderPlanRevisionProvider,
        "from_api_key",
        staticmethod(from_api_key),
    )
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=job_path,
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_qualification_authority(ledger_path),
    )

    assert factory.revision_provider() is provider
    assert captured == {
        "api_key": "qualification-secret",
        "base_url": "https://api.openai.com/v1",
        "budget": budget,
        "existing_usage": composite_usage,
    }
    assert captured["existing_usage"] != checkpoint_usage
    assert credential_store.read_count == 1


def test_revision_without_composite_evidence_fails_before_secret_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    job_path = tmp_path / "jobs" / "unreviewed.json"
    _install_job_authority(
        monkeypatch,
        job_path=job_path,
        authority=_FakeGptAuthority(
            planner_checkpoint=SimpleNamespace(usage=(_usage(1),)),
        ),
    )
    credential_store = _CountingCredentialStore("qualification-secret")
    ledger_path = tmp_path / "api-budget.json"
    events: list[object] = []
    _install_budget(monkeypatch, expected_path=ledger_path, events=events)
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=job_path,
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_qualification_authority(ledger_path),
    )

    with pytest.raises(
        RuntimeError,
        match="durable job has no accepted planning evidence",
    ):
        factory.revision_provider()

    assert credential_store.read_count == 0


def test_compatible_profile_is_rejected_without_credential_or_ledger_access(
    tmp_path: Path,
) -> None:
    credential_store = _CountingCredentialStore("qualification-secret")

    with pytest.raises(
        ValueError,
        match="requires the official OpenAI endpoint",
    ):
        provider_factory_module.FoldweaveDirectProviderFactory(
            job_path=tmp_path / "jobs" / "compatible.json",
            credential_store=credential_store,
            endpoint=DirectEndpointProfile.compatible(
                endpoint="https://models.example.test/v1",
                model_alias="compatible-model",
            ),
            budget_authority=_qualification_authority(tmp_path / "api-budget.json"),
        )

    assert credential_store.read_count == 0


def test_budget_failure_precedes_secret_read_and_discloses_no_secret(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    secret = "qualification-secret-never-disclose"
    credential_store = _CountingCredentialStore(secret)
    ledger_path = tmp_path / "api-budget.json"

    def fail_open(cls: type[object], *, path: Path) -> object:
        del cls
        assert path == ledger_path
        raise RuntimeError("Foldweave ledger is not migrated.")

    monkeypatch.setattr(
        provider_factory_module.PersistentBudgetLedger,
        "open_existing_foldweave_planner",
        classmethod(fail_open),
    )
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=tmp_path / "jobs" / "live.json",
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_qualification_authority(ledger_path),
    )

    with pytest.raises(RuntimeError, match="ledger is not migrated") as exc_info:
        factory.initial_provider()

    assert credential_store.read_count == 0
    assert secret not in str(exc_info.value)
    assert secret not in repr(factory)


def test_provider_construction_failure_discloses_no_secret(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    secret = "qualification-secret-never-disclose"
    credential_store = _CountingCredentialStore(secret)
    ledger_path = tmp_path / "api-budget.json"
    events: list[object] = []
    _install_budget(monkeypatch, expected_path=ledger_path, events=events)

    def fail_provider(api_key: str, **kwargs: Any) -> object:
        del kwargs
        assert api_key == secret
        raise RuntimeError("Provider construction failed safely.")

    monkeypatch.setattr(
        provider_factory_module.LiveFolderPlannerProvider,
        "from_api_key",
        staticmethod(fail_provider),
    )
    factory = provider_factory_module.FoldweaveDirectProviderFactory(
        job_path=tmp_path / "jobs" / "live.json",
        credential_store=credential_store,
        endpoint=DirectEndpointProfile.official(),
        budget_authority=_qualification_authority(ledger_path),
    )

    with pytest.raises(RuntimeError, match="failed safely") as exc_info:
        factory.initial_provider()

    assert credential_store.read_count == 1
    assert secret not in str(exc_info.value)
    assert secret not in repr(factory)
