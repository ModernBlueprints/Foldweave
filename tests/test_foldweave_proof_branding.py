"""Schema-aware Foldweave proof-branding compatibility tests."""

from __future__ import annotations

from name_atlas.folder_refactor.connected_change.proof import (
    render_connected_proof_html,
)


def test_legacy_proof_bytes_keep_historical_name_atlas_title() -> None:
    proof = render_connected_proof_html("a" * 64, "b" * 64)

    assert b"<title>Name Atlas proof</title>" in proof
    assert b"Foldweave proof" not in proof


def test_foldweave_proof_bytes_use_active_product_title() -> None:
    proof = render_connected_proof_html(
        "a" * 64,
        "b" * 64,
        release_profile="foldweave",
    )

    assert b"<title>Foldweave proof</title>" in proof
    assert b"Name Atlas proof" not in proof
