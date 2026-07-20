"""Pure human-readable proof rendering for Connected Change results."""

from __future__ import annotations

from typing import Literal


def render_connected_proof_html(
    receipt_fingerprint: str,
    organized_tree_commitment: str,
    *,
    release_profile: Literal["legacy_name_atlas", "foldweave"] = ("legacy_name_atlas"),
) -> bytes:
    """Render exact portable proof bytes from independently verified identities."""

    title = "Foldweave proof" if release_profile == "foldweave" else "Name Atlas proof"

    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{title}</title><style>"
        "*{box-sizing:border-box}body{margin:0;background:#0d1117;color:#e6edf3;"
        "font:16px/1.55 system-ui,sans-serif}main{width:min(100%,48rem);margin:auto;"
        "padding:clamp(1.25rem,5vw,3rem)}h1{font-size:clamp(1.75rem,6vw,2.5rem);"
        "line-height:1.15}details{margin-top:1.5rem;padding:1rem;border:1px solid "
        "#30363d;border-radius:.75rem;background:#161b22}summary{cursor:pointer;"
        "font-weight:700}code{overflow-wrap:anywhere;word-break:break-word;color:#a5d6ff}"
        "</style></head><body><main><h1>Your new folder is verified</h1>"
        "<p>Every in-scope file is present exactly once. The original folder was "
        "not changed.</p><details><summary>Technical proof</summary><p>Receipt: "
        f"<code>{receipt_fingerprint}</code></p><p>Organized tree: <code>"
        f"{organized_tree_commitment}</code></p></details></main></body></html>\n"
    ).encode()
