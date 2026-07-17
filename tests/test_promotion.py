"""Atomic no-replace final-stage promotion tests."""

from pathlib import Path

import pytest

from name_atlas.verification.promotion import promote_directory_no_replace


def test_pending_directory_promotes_only_to_absent_destination(
    tmp_path: Path,
) -> None:
    pending = tmp_path / ".stage.pending"
    final = tmp_path / "stage"
    pending.mkdir()
    (pending / "proof.txt").write_text("verified", encoding="utf-8")

    promote_directory_no_replace(pending, final)

    assert not pending.exists()
    assert (final / "proof.txt").read_text(encoding="utf-8") == "verified"


def test_existing_destination_is_never_replaced(tmp_path: Path) -> None:
    pending = tmp_path / ".stage.pending"
    final = tmp_path / "stage"
    pending.mkdir()
    final.mkdir()

    with pytest.raises(FileExistsError):
        promote_directory_no_replace(pending, final)

    assert pending.is_dir()
    assert final.is_dir()
