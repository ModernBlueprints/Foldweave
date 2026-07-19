from pathlib import Path

import pytest

from name_atlas.foldweave_paths import (
    FOLDWEAVE_BUDGET_LEDGER_ENV,
    FOLDWEAVE_STATE_ROOT_ENV,
    foldweave_paths,
    resolve_foldweave_budget_authority,
    resolve_foldweave_job_path,
    resolve_qualification_budget_ledger,
)


def test_state_root_and_job_are_absolute_and_cwd_independent(tmp_path: Path) -> None:
    root = tmp_path / "Foldweave State"
    environ = {FOLDWEAVE_STATE_ROOT_ENV: str(root)}

    paths = foldweave_paths(environ=environ)

    assert paths.state_root == root
    assert (
        resolve_foldweave_job_path(None, environ=environ) == root / "jobs/active.json"
    )


def test_state_root_rejects_relative_and_link_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must be an absolute"):
        foldweave_paths(environ={FOLDWEAVE_STATE_ROOT_ENV: "relative"})

    target = tmp_path / "target"
    target.mkdir()
    link = tmp_path / "link"
    link.symlink_to(target, target_is_directory=True)
    with pytest.raises(ValueError, match="must be a directory"):
        foldweave_paths(environ={FOLDWEAVE_STATE_ROOT_ENV: str(link)})


def test_qualification_ledger_requires_one_existing_absolute_regular_file(
    tmp_path: Path,
) -> None:
    ledger = tmp_path / "api_budget.json"
    ledger.write_text("{}", encoding="utf-8")

    assert (
        resolve_qualification_budget_ledger(
            environ={FOLDWEAVE_BUDGET_LEDGER_ENV: str(ledger)}
        )
        == ledger
    )

    with pytest.raises(ValueError, match="must name"):
        resolve_qualification_budget_ledger(environ={})

    linked_ledger = tmp_path / "linked-budget.json"
    linked_ledger.symlink_to(ledger)
    with pytest.raises(ValueError, match="must be a regular file"):
        resolve_qualification_budget_ledger(
            environ={FOLDWEAVE_BUDGET_LEDGER_ENV: str(linked_ledger)}
        )


def test_budget_authority_uses_explicit_existing_qualification_ledger(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "state"
    ledger = tmp_path / "qualification.json"
    ledger.write_text("{}", encoding="utf-8")

    authority = resolve_foldweave_budget_authority(
        environ={
            FOLDWEAVE_STATE_ROOT_ENV: str(state_root),
            FOLDWEAVE_BUDGET_LEDGER_ENV: str(ledger),
        }
    )

    assert authority.kind == "qualification_existing"
    assert authority.path == ledger
    assert not state_root.exists()


def test_budget_authority_defaults_to_lazy_installation_ledger(
    tmp_path: Path,
) -> None:
    state_root = tmp_path / "Foldweave State"

    authority = resolve_foldweave_budget_authority(
        environ={FOLDWEAVE_STATE_ROOT_ENV: str(state_root)}
    )

    assert authority.kind == "installation_persistent"
    assert authority.path == state_root / "api_budget.json"
    assert not state_root.exists()


def test_installation_budget_authority_rejects_a_link(tmp_path: Path) -> None:
    state_root = tmp_path / "state"
    state_root.mkdir()
    target = tmp_path / "target.json"
    target.write_text("{}", encoding="utf-8")
    (state_root / "api_budget.json").symlink_to(target)

    with pytest.raises(ValueError, match="must be a regular file"):
        resolve_foldweave_budget_authority(
            environ={FOLDWEAVE_STATE_ROOT_ENV: str(state_root)}
        )
