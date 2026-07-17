"""Tests for the product-owned deterministic BagIt writer."""

from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path

import pytest

from name_atlas.verification.bag_writer import BagItWriter, BagItWriterError
from name_atlas.verification.bagit_validator import BagItPackageValidator


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _make_pending_stage(parent: Path, name: str = "pending") -> Path:
    root = parent / name
    (root / "data" / "objects").mkdir(parents=True)
    (root / "data" / "metadata").mkdir(parents=True)
    (root / "name-atlas").mkdir()
    (root / "data" / "objects" / "z.txt").write_bytes(b"z\n")
    (root / "data" / "metadata" / "metadata.csv").write_bytes(
        b"filename\nobjects/z.txt\n"
    )
    (root / "name-atlas" / "verification_report.json").write_text(
        '{"valid":false}\n', encoding="utf-8"
    )
    (root / "name-atlas" / "verification_summary.md").write_text(
        "Pending proof\n", encoding="utf-8"
    )
    return root


def _expected_manifest(root: Path, relative_paths: list[str]) -> str:
    return "".join(
        f"{_sha256(root / relative_path)}  {relative_path}\n"
        for relative_path in sorted(relative_paths)
    )


def test_write_creates_exact_deterministic_valid_bag(tmp_path: Path) -> None:
    root = _make_pending_stage(tmp_path)
    payload_paths = ["data/metadata/metadata.csv", "data/objects/z.txt"]
    payload_bytes = sum((root / path).stat().st_size for path in payload_paths)

    result = BagItWriter().write(root, bagging_date=date(2026, 7, 17))

    assert result.bag_root == root.resolve()
    assert result.payload_file_count == 2
    assert result.payload_bytes == payload_bytes
    assert result.tag_file_count == 5
    assert (root / "bagit.txt").read_text(encoding="utf-8") == (
        "BagIt-Version: 1.0\nTag-File-Character-Encoding: UTF-8\n"
    )
    assert (root / "bag-info.txt").read_text(encoding="utf-8") == (
        "Bagging-Date: 2026-07-17\n"
        "Bag-Software-Agent: Reversible Name Atlas 0.1.0\n"
        f"Payload-Oxum: {payload_bytes}.2\n"
    )
    assert (root / "manifest-sha256.txt").read_text(
        encoding="utf-8"
    ) == _expected_manifest(root, payload_paths)

    tag_paths = [
        "bag-info.txt",
        "bagit.txt",
        "manifest-sha256.txt",
        "name-atlas/verification_report.json",
        "name-atlas/verification_summary.md",
    ]
    assert (root / "tagmanifest-sha256.txt").read_text(
        encoding="utf-8"
    ) == _expected_manifest(root, tag_paths)
    assert BagItPackageValidator().validate(root).valid is True


def test_output_is_identical_for_equivalent_stages(tmp_path: Path) -> None:
    first = _make_pending_stage(tmp_path, "first")
    second = _make_pending_stage(tmp_path, "second")
    writer = BagItWriter()

    writer.write(first, bagging_date=date(2026, 7, 17))
    writer.write(second, bagging_date=date(2026, 7, 17))

    generated = (
        "bagit.txt",
        "bag-info.txt",
        "manifest-sha256.txt",
        "tagmanifest-sha256.txt",
    )
    assert {name: (first / name).read_bytes() for name in generated} == {
        name: (second / name).read_bytes() for name in generated
    }


def test_rejects_symlink_member(tmp_path: Path) -> None:
    root = _make_pending_stage(tmp_path)
    outside = tmp_path / "outside.txt"
    outside.write_text("must not be read\n", encoding="utf-8")
    (root / "data" / "objects" / "link.txt").symlink_to(outside)

    with pytest.raises(BagItWriterError, match="contains a symlink"):
        BagItWriter().write(root, bagging_date=date(2026, 7, 17))

    assert not (root / "bagit.txt").exists()


def test_refuses_preexisting_bag_file_without_overwrite(tmp_path: Path) -> None:
    root = _make_pending_stage(tmp_path)
    preexisting = root / "bagit.txt"
    preexisting.write_text("not ours\n", encoding="utf-8")

    with pytest.raises(BagItWriterError, match="root structure is invalid"):
        BagItWriter().write(root, bagging_date=date(2026, 7, 17))

    assert preexisting.read_text(encoding="utf-8") == "not ours\n"
    assert not (root / "manifest-sha256.txt").exists()


def test_refresh_after_verification_report_mutation_restores_validity(
    tmp_path: Path,
) -> None:
    root = _make_pending_stage(tmp_path)
    writer = BagItWriter()
    writer.write(root, bagging_date=date(2026, 7, 17))
    protected_paths = (
        "bagit.txt",
        "bag-info.txt",
        "manifest-sha256.txt",
        "name-atlas/verification_summary.md",
    )
    before = {path: (root / path).read_bytes() for path in protected_paths}

    report = root / "name-atlas" / "verification_report.json"
    report.write_text('{"valid":true}\n', encoding="utf-8")
    assert BagItPackageValidator().validate(root).valid is False

    result = writer.refresh_tagmanifest(root)

    assert result.tag_file_count == 5
    assert {path: (root / path).read_bytes() for path in protected_paths} == before
    tag_paths = [
        "bag-info.txt",
        "bagit.txt",
        "manifest-sha256.txt",
        "name-atlas/verification_report.json",
        "name-atlas/verification_summary.md",
    ]
    assert (root / "tagmanifest-sha256.txt").read_text(
        encoding="utf-8"
    ) == _expected_manifest(root, tag_paths)
    assert BagItPackageValidator().validate(root).valid is True
    assert not (root / ".tagmanifest-sha256.txt.tmp").exists()


def test_refresh_rejects_changes_outside_verification_report(tmp_path: Path) -> None:
    root = _make_pending_stage(tmp_path)
    writer = BagItWriter()
    writer.write(root, bagging_date=date(2026, 7, 17))
    manifest = root / "tagmanifest-sha256.txt"
    before = manifest.read_bytes()
    (root / "name-atlas" / "verification_summary.md").write_text(
        "Changed summary\n", encoding="utf-8"
    )

    with pytest.raises(BagItWriterError, match="Only .*verification_report.json"):
        writer.refresh_tagmanifest(root)

    assert manifest.read_bytes() == before


def test_finalize_tagmanifest_binds_added_receipt_files(tmp_path: Path) -> None:
    root = _make_pending_stage(tmp_path)
    writer = BagItWriter()
    writer.write(root, bagging_date=date(2026, 7, 17))
    (root / "name-atlas" / "change_receipt.json").write_text(
        '{"receipt_fingerprint":"abc"}\n',
        encoding="utf-8",
    )
    (root / "name-atlas" / "change_receipt.html").write_text(
        "<!doctype html><title>Receipt</title>\n",
        encoding="utf-8",
    )

    result = writer.finalize_tagmanifest(root)

    assert result.tag_file_count == 7
    tag_paths = [
        "bag-info.txt",
        "bagit.txt",
        "manifest-sha256.txt",
        "name-atlas/change_receipt.html",
        "name-atlas/change_receipt.json",
        "name-atlas/verification_report.json",
        "name-atlas/verification_summary.md",
    ]
    assert (root / "tagmanifest-sha256.txt").read_text(
        encoding="utf-8"
    ) == _expected_manifest(root, tag_paths)
    assert BagItPackageValidator().validate(root).valid is True
