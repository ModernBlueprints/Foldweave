"""R4 five-state experience, accessibility, and packaged-asset acceptance."""

from __future__ import annotations

import re
import shutil
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlsplit

import httpx
import pytest

from name_atlas.app import create_app
from name_atlas.config import RuntimeConfig
from name_atlas.decision_cards import RecordedReplayDecisionCardProvider
from name_atlas.domain import RunMode
from name_atlas.verification import BagItPackageValidator
from name_atlas.workflow import WorkflowSession

PROJECT_ROOT = Path(__file__).parents[1]
HERO_ROOT = PROJECT_ROOT / "sample_data" / "hero"
REPLAY_RECORD = (
    PROJECT_ROOT / "src" / "name_atlas" / "recordings" / "hero_decision_card.json"
)
STATIC_ROOT = PROJECT_ROOT / "src" / "name_atlas" / "static"
WORKBENCH_ROUTES = ("/atlas", "/decide", "/stage", "/verify", "/handoff")
SELECTED_ICONS = {
    "chevron-right",
    "clipboard",
    "database",
    "diagram-tree",
    "export",
    "help",
    "history",
    "tick-circle",
    "warning-sign",
}
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class _Element:
    def __init__(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]] | None = None,
        *,
        parent: _Element | None = None,
    ) -> None:
        self.tag = tag
        self.attrs = {key: value or "" for key, value in attrs or []}
        self.parent = parent
        self.children: list[_Element | str] = []

    def descendants(self, tag: str | None = None) -> tuple[_Element, ...]:
        found: list[_Element] = []
        for child in self.children:
            if not isinstance(child, _Element):
                continue
            if tag is None or child.tag == tag:
                found.append(child)
            found.extend(child.descendants(tag))
        return tuple(found)

    def text(self) -> str:
        return " ".join(
            child.text() if isinstance(child, _Element) else child
            for child in self.children
        )

    @property
    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())


class _DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Element("document")
        self._stack = [self.root]

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        element = _Element(tag, attrs, parent=self._stack[-1])
        self._stack[-1].children.append(element)
        if tag not in VOID_ELEMENTS:
            self._stack.append(element)

    def handle_startendtag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in VOID_ELEMENTS:
            self._stack.pop()

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._stack) - 1, 0, -1):
            if self._stack[index].tag == tag:
                del self._stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if data.strip():
            self._stack[-1].children.append(data.strip())


class _RoutingWorkflow:
    """Minimal server-authority double; it never performs a product mutation."""

    def __init__(
        self,
        *,
        lifecycle: str = "review",
        export_ready: bool = False,
        hard_blocker_count: int = 0,
        proof_ready: bool = False,
        handoff_ready: bool = False,
        persisted_handoff_path: Path | None = None,
    ) -> None:
        receipt_fingerprint = "a" * 64 if handoff_ready else None
        self.output_root = Path("/tmp/name-atlas-routing-output")
        self.stage_result = (
            SimpleNamespace(
                stage_root=Path("/tmp/name-atlas-routing-handoff"),
                receipt_fingerprint=receipt_fingerprint,
            )
            if proof_ready or handoff_ready
            else None
        )
        self.case = SimpleNamespace(
            case_name="Routing case",
            case_id="1" * 32,
            lifecycle=lifecycle,
            receipt_fingerprint=receipt_fingerprint,
            local_paths=SimpleNamespace(handoff_path=persisted_handoff_path),
        )
        self.package = SimpleNamespace(families=(), content_members=())
        self.stage_calls = 0
        self._view = {
            "case_id": self.case.case_id,
            "case_name": self.case.case_name,
            "case_lifecycle": lifecycle,
            "receipt_fingerprint": receipt_fingerprint,
            "handoff_path": (
                str(self.stage_result.stage_root)
                if handoff_ready
                else (
                    str(persisted_handoff_path)
                    if persisted_handoff_path is not None
                    else None
                )
            ),
            "source_root": "/tmp/name-atlas-routing-source",
            "snapshot": SimpleNamespace(commitment="b" * 64),
            "family_count": 1,
            "ready_count": int(export_ready),
            "export_ready": export_ready,
            "hard_blocker_count": hard_blocker_count,
            "stale_differences": (
                ("content_changed: objects/item.txt",) if lifecycle == "stale" else ()
            ),
            "source_scan_blocker": None,
            "proof": None,
            "stage_root": (
                str(self.stage_result.stage_root)
                if self.stage_result is not None
                else None
            ),
        }

    def view_model(self) -> dict[str, object]:
        return self._view

    def stage(self) -> None:
        self.stage_calls += 1

    def close(self) -> None:
        return None


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def _parse(html: str) -> _Element:
    parser = _DocumentParser()
    parser.feed(html)
    parser.close()
    return parser.root


def _config() -> RuntimeConfig:
    return RuntimeConfig.from_environment(
        mode=RunMode.REPLAY,
        environ={},
        replay_record_configured=True,
    )


def _active_navigation(document: _Element) -> tuple[_Element, ...]:
    return tuple(
        element
        for element in document.descendants("a")
        if element.attrs.get("aria-current") == "page"
    )


def _assert_shell_contract(
    response: httpx.Response,
    *,
    route: str,
    label: str,
) -> _Element:
    assert response.status_code == 200
    document = _parse(response.text)
    assert len(document.descendants("main")) == 1
    assert document.descendants("header")
    assert len(document.descendants("nav")) == 1
    assert document.descendants("h1") or document.descendants("h2")
    bodies = document.descendants("body")
    assert len(bodies) == 1
    assert "bp6-dark" in bodies[0].classes
    active = _active_navigation(document)
    assert len(active) == 1
    assert active[0].attrs.get("href") == route
    assert label in active[0].text()
    nav_paths = {
        link.attrs.get("href")
        for nav in document.descendants("nav")
        for link in nav.descendants("a")
    }
    assert set(WORKBENCH_ROUTES) <= nav_paths
    shell_text = document.text()
    assert "Reversible Name Atlas" in shell_text
    assert "Migration Case" in shell_text
    assert "Source" in shell_text
    assert "Recorded GPT-5.6 response" in shell_text
    compact_summaries = tuple(
        element
        for element in document.descendants()
        if "mobile-case-summary" in element.classes
    )
    assert len(compact_summaries) == 1
    for label in ("Case", "Source", "Mode", "Resolved", "Replay"):
        assert label in compact_summaries[0].text()
    return document


def _icon_name(element: _Element) -> str | None:
    source = element.attrs.get("src", "")
    match = re.search(r"/icons/([a-z0-9-]+)\.svg(?:[?#].*)?$", source)
    if match:
        return match.group(1)
    data_icon = element.attrs.get("data-icon")
    if data_icon:
        return data_icon
    for class_name in element.classes:
        match = re.fullmatch(r"bp6-icon-([a-z0-9-]+)", class_name)
        if match:
            return match.group(1)
    return None


def _rendered_icons(document: _Element) -> dict[str, tuple[_Element, ...]]:
    icons: dict[str, list[_Element]] = {}
    for element in document.descendants():
        name = _icon_name(element)
        if name is not None:
            icons.setdefault(name, []).append(element)
    return {name: tuple(elements) for name, elements in icons.items()}


def _has_visible_ancestor_text(element: _Element) -> bool:
    parent = element.parent
    for _ in range(3):
        if parent is None:
            return False
        if parent.text().strip():
            return True
        parent = parent.parent
    return False


def _assert_no_client_authority_or_remote_assets(document: _Element) -> None:
    for element in document.descendants():
        for attribute, value in element.attrs.items():
            assert not attribute.lower().startswith("on")
            if attribute not in {"href", "src"}:
                continue
            parsed = urlsplit(value)
            if parsed.scheme == "data":
                continue
            if parsed.scheme or parsed.netloc:
                assert parsed.scheme == "http"
                assert parsed.netloc == "testserver"
        if element.tag == "script" and element.attrs.get("src"):
            assert _local_path(element.attrs["src"]).startswith("/static/")


def _local_path(value: str) -> str:
    parsed = urlsplit(value)
    return parsed.path if parsed.scheme or parsed.netloc else value.split("?", 1)[0]


def _relative_luminance(hex_color: str) -> float:
    channels = [int(hex_color[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("workflow", "expected"),
    (
        (None, "/atlas"),
        (_RoutingWorkflow(lifecycle="stale", hard_blocker_count=1), "/atlas"),
        (_RoutingWorkflow(), "/decide"),
        (_RoutingWorkflow(hard_blocker_count=1), "/decide"),
        (_RoutingWorkflow(export_ready=True), "/stage"),
        (_RoutingWorkflow(export_ready=True, proof_ready=True), "/verify"),
        (
            _RoutingWorkflow(
                lifecycle="handoff_ready",
                export_ready=True,
                handoff_ready=True,
            ),
            "/handoff",
        ),
    ),
)
async def test_root_redirect_is_computed_from_server_prerequisites(
    workflow: _RoutingWorkflow | None,
    expected: str,
) -> None:
    transport = httpx.ASGITransport(app=create_app(_config(), workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 303
    assert response.headers["location"] == expected


@pytest.mark.anyio
@pytest.mark.parametrize(
    "workflow",
    (
        _RoutingWorkflow(lifecycle="stale", hard_blocker_count=1),
        _RoutingWorkflow(),
        _RoutingWorkflow(
            lifecycle="handoff_ready",
            export_ready=True,
            handoff_ready=True,
        ),
    ),
)
async def test_stage_post_guard_never_delegates_from_ineligible_state(
    workflow: _RoutingWorkflow,
) -> None:
    transport = httpx.ASGITransport(app=create_app(_config(), workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.post("/stage")

    assert response.status_code == 303
    assert response.headers["location"] == "/stage"
    assert workflow.stage_calls == 0


@pytest.mark.anyio
async def test_review_case_handoff_pointer_cannot_serve_unverified_bytes(
    tmp_path: Path,
) -> None:
    handoff = tmp_path / "unverified-handoff"
    receipt = handoff / "name-atlas" / "change_receipt.html"
    receipt.parent.mkdir(parents=True)
    receipt.write_text("UNVERIFIED_SENTINEL", encoding="utf-8")
    workflow = _RoutingWorkflow(persisted_handoff_path=handoff)
    transport = httpx.ASGITransport(app=create_app(_config(), workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        response = await client.get("/proof-artifacts/name-atlas/change_receipt.html")

    assert response.status_code == 404
    assert "UNVERIFIED_SENTINEL" not in response.text


@pytest.mark.anyio
@pytest.mark.parametrize(
    "workflow",
    (None, _RoutingWorkflow(lifecycle="blocked")),
)
async def test_blocked_direct_routes_render_one_consistent_verdict(
    workflow: _RoutingWorkflow | None,
) -> None:
    transport = httpx.ASGITransport(app=create_app(_config(), workflow))

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        responses = [
            await client.get(route) for route in ("/stage", "/verify", "/handoff")
        ]

    for response in responses:
        assert response.status_code == 200
        assert "BLOCKED" in response.text
        assert "INCOMPLETE" not in response.text


@pytest.mark.anyio
async def test_five_state_workbench_is_semantic_local_and_human_authoritative(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    shutil.copytree(HERO_ROOT, source)
    workflow = WorkflowSession(
        source_root=source,
        output_root=tmp_path / "output",
        decision_card_provider=RecordedReplayDecisionCardProvider(
            REPLAY_RECORD.read_bytes()
        ),
        package_validator=BagItPackageValidator(),
        case_path=tmp_path / "case.json",
        case_name="R4 experience case",
    )
    app = create_app(_config(), workflow)
    transport = httpx.ASGITransport(app=app)

    try:
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            atlas = await client.get("/atlas")
            decide_before_card = await client.get("/decide")
            incomplete_verify = await client.get("/verify")
            incomplete_handoff = await client.get("/handoff")

            meaning_family = next(
                family
                for family in workflow.package.families
                if family.canonical_identifier == "NA-0001"
            )
            collision_family = next(
                family
                for family in workflow.package.families
                if family.canonical_identifier == "CASE-010"
            )
            decide_with_card = await client.post(
                f"/families/{meaning_family.family_id}/generate",
                follow_redirects=True,
            )
            workflow.approve(meaning_family.family_id)
            workflow.approve_low_risk()
            workflow.edit(collision_family.family_id, "harbor-map-north")
            workflow.approve_low_risk()
            ready_stage = await client.get("/stage")
            staged = await client.post("/stage")
            verified = await client.get("/verify")
            handoff = await client.get("/handoff")
            finalized_decide = await client.get("/decide")

            pages = {
                "/atlas": (atlas, "Atlas"),
                "/decide": (decide_with_card, "Decide"),
                "/stage": (ready_stage, "Stage"),
                "/verify": (verified, "Verify"),
                "/handoff": (handoff, "Handoff"),
            }
            documents = {
                route: _assert_shell_contract(response, route=route, label=label)
                for route, (response, label) in pages.items()
            }

            assert staged.status_code == 303
            assert staged.headers["location"] == "/verify"
            assert any(
                status in incomplete_verify.text for status in ("INCOMPLETE", "BLOCKED")
            )
            assert any(
                status in incomplete_handoff.text
                for status in ("INCOMPLETE", "BLOCKED")
            )

            atlas_document = documents["/atlas"]
            assert atlas_document.descendants("table")
            assert atlas_document.descendants("details")

            decide_document = documents["/decide"]
            assert decide_document.descendants("form")
            assert decide_document.descendants("details")
            assert "GPT is advisory" in decide_document.text()
            assert "Human authority" in decide_document.text()
            assert "Recorded GPT-5.6 response" in decide_document.text()
            assert any(
                "notice--neutral" in element.classes
                for element in decide_document.descendants()
            )
            assert not any(
                "notice--success" in element.classes
                for element in decide_document.descendants()
            )
            assert "Deterministic collision" in decide_document.text()
            assert "no model call is permitted" in decide_document.text()
            assert "No payload bytes" in decide_before_card.text
            exception_cards = tuple(
                details
                for details in decide_document.descendants("details")
                if "exception-card" in details.classes
            )
            assert len(exception_cards) >= 2
            assert sum("open" in details.attrs for details in exception_cards) == 1

            stage_document = documents["/stage"]
            stage_forms = {
                form.attrs.get("action") for form in stage_document.descendants("form")
            }
            assert "/stage" in stage_forms
            assert stage_document.descendants("details")
            assert "source untouched" in stage_document.text().lower()

            verify_document = documents["/verify"]
            for group in (
                "Source",
                "Payloads",
                "References",
                "Paths",
                "Decisions",
                "Package",
                "Receipt",
            ):
                assert group in verify_document.text()
            assert "VERIFIED" in verify_document.text()
            technical_details = tuple(
                details
                for details in verify_document.descendants("details")
                if "technical" in details.text().lower()
            )
            assert technical_details
            assert all("open" not in details.attrs for details in technical_details)

            handoff_document = documents["/handoff"]
            handoff_text = handoff_document.text()
            assert workflow.stage_result is not None
            assert workflow.stage_result.receipt_fingerprint in handoff_text
            assert str(workflow.stage_result.stage_root) in handoff_text
            assert any(
                link.attrs.get("href")
                == "/proof-artifacts/name-atlas/change_receipt.html"
                for link in handoff_document.descendants("a")
            )
            verifier_commands = tuple(
                element.attrs.get("value", "")
                for element in handoff_document.descendants("input")
                if "verify-receipt" in element.attrs.get("value", "")
            )
            assert len(verifier_commands) == 1
            rerun_forms = tuple(
                form
                for form in handoff_document.descendants("form")
                if form.attrs.get("action") == "/rerun-verifier"
            )
            assert len(rerun_forms) == 1
            assert "verifier" in rerun_forms[0].text().lower()
            restore_commands = tuple(
                element.attrs.get("value", "")
                for element in handoff_document.descendants("input")
                if "restore-receipt" in element.attrs.get("value", "")
            )
            assert len(restore_commands) == 1
            assert restore_commands[0].endswith(" RESTORE_DESTINATION")
            assert "restore-receipt" not in incomplete_handoff.text

            finalized_decide_document = _parse(finalized_decide.text)
            assert "finalized Migration Case is read-only" in (
                finalized_decide_document.text()
            )
            case_mutation_actions = {
                form.attrs.get("action", "")
                for form in finalized_decide_document.descendants("form")
                if form.attrs.get("action", "").startswith("/families/")
                or form.attrs.get("action") == "/approve-low-risk"
            }
            assert case_mutation_actions == set()

            rendered_icon_names: set[str] = set()
            icon_documents = (
                *documents.values(),
                _parse(incomplete_verify.text),
                _parse(incomplete_handoff.text),
            )
            for document in icon_documents:
                _assert_no_client_authority_or_remote_assets(document)
                technical_disclosures = tuple(
                    details
                    for details in document.descendants("details")
                    if "technical-disclosure" in details.classes
                )
                assert all(
                    "open" not in details.attrs for details in technical_disclosures
                )
                rendered = _rendered_icons(document)
                rendered_icon_names.update(rendered)
                for elements in rendered.values():
                    for element in elements:
                        assert element.attrs.get("aria-hidden") == "true"
                        assert _has_visible_ancestor_text(element)
            assert rendered_icon_names == SELECTED_ICONS

            stylesheets = [
                link.attrs["href"]
                for link in documents["/atlas"].descendants("link")
                if "stylesheet" in link.attrs.get("rel", "").split()
            ]
            assert len(stylesheets) == 2
            assert "blueprint" in stylesheets[0]
            assert "styles.css" in stylesheets[1]
            assert all(_local_path(href).startswith("/static/") for href in stylesheets)

            local_assets = {
                element.attrs[attribute].split("#", 1)[0]
                for document in documents.values()
                for element in document.descendants()
                for attribute in ("src", "href")
                if _local_path(element.attrs.get(attribute, "")).startswith("/static/")
            }
            for asset_path in sorted(local_assets):
                asset = await client.get(_local_path(asset_path))
                assert asset.status_code == 200, asset_path
                assert asset.content, asset_path
    finally:
        workflow.close()


@pytest.mark.anyio
async def test_handoff_restart_keeps_offline_receipt_and_rerun_action(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source"
    shutil.copytree(HERO_ROOT, source)
    output = tmp_path / "output"
    case_path = tmp_path / "case.json"
    provider_bytes = REPLAY_RECORD.read_bytes()
    first = WorkflowSession(
        source_root=source,
        output_root=output,
        decision_card_provider=RecordedReplayDecisionCardProvider(provider_bytes),
        package_validator=BagItPackageValidator(),
        case_path=case_path,
        case_name="Restarted handoff case",
    )
    meaning_family = next(
        family
        for family in first.package.families
        if family.canonical_identifier == "NA-0001"
    )
    collision_family = next(
        family
        for family in first.package.families
        if family.canonical_identifier == "CASE-010"
    )
    await first.generate_card(meaning_family.family_id)
    first.approve(meaning_family.family_id)
    first.approve_low_risk()
    first.edit(collision_family.family_id, "harbor-map-north")
    first.approve_low_risk()
    result = first.stage()
    expected_receipt = result.receipt_fingerprint
    first.close()

    restarted = WorkflowSession(
        source_root=source,
        output_root=output,
        decision_card_provider=RecordedReplayDecisionCardProvider(provider_bytes),
        package_validator=BagItPackageValidator(),
        case_path=case_path,
        case_name="Ignored on resume",
    )
    transport = httpx.ASGITransport(app=create_app(_config(), restarted))
    try:
        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://testserver",
        ) as client:
            page = await client.get("/handoff")
            verify_before_rerun = await client.get("/verify")
            stage_before_rerun = await client.get("/stage")
            document = _assert_shell_contract(
                page,
                route="/handoff",
                label="Handoff",
            )
            receipt_links = tuple(
                link
                for link in document.descendants("a")
                if link.attrs.get("href")
                == "/proof-artifacts/name-atlas/change_receipt.html"
            )
            assert receipt_links
            receipt = await client.get(receipt_links[0].attrs["href"])
            rerun = await client.post("/rerun-verifier")
            after_rerun = await client.get("/handoff")
            verify_after_rerun = await client.get("/verify")
            stage_after_rerun = await client.get("/stage")

            moved_handoff = tmp_path / "temporarily-unavailable-handoff"
            result.stage_root.rename(moved_handoff)
            failed_rerun = await client.post("/rerun-verifier")
            after_failed_rerun = await client.get("/handoff")
            stage_after_failed_rerun = await client.get("/stage")

        assert receipt.status_code == 200
        assert "text/html" in receipt.headers["content-type"]
        assert expected_receipt is not None
        assert expected_receipt in receipt.text
        assert "FINALIZED RECEIPT" in page.text
        assert "Verified at producer finalization" in page.text
        assert "VERIFIED HANDOFF" not in page.text
        assert "receipt-card--incomplete" in page.text
        assert "a current receiver rerun is pending" in stage_before_rerun.text
        assert "Source at finalization" in stage_before_rerun.text
        assert "Snapshot matched" in stage_before_rerun.text
        assert "status-panel--incomplete" in stage_before_rerun.text
        for group in (
            "Source",
            "Payloads",
            "References",
            "Paths",
            "Decisions",
            "Package",
            "Receipt",
        ):
            assert group in verify_before_rerun.text
            assert group in verify_after_rerun.text
        assert "a fresh receiver rerun is pending" in verify_before_rerun.text
        assert "Fresh receiver verification passed" in verify_after_rerun.text
        assert rerun.status_code == 303
        assert rerun.headers["location"] == "/handoff"
        assert "VERIFIED HANDOFF" in after_rerun.text
        assert "receipt-card--verified" in after_rerun.text
        assert expected_receipt in after_rerun.text
        assert "A current receiver run verifies" in stage_after_rerun.text
        assert "status-panel--verified" in stage_after_rerun.text
        assert failed_rerun.status_code == 303
        assert failed_rerun.headers["location"] == "/handoff"
        assert "Received bag cannot be inspected." in after_failed_rerun.text
        assert "RECEIVER CHECK BLOCKED" in after_failed_rerun.text
        assert "receipt-card--blocked" in after_failed_rerun.text
        assert "Latest receiver run: VERIFIED" not in after_failed_rerun.text
        assert "current handoff is unavailable or blocked" in (
            stage_after_failed_rerun.text
        )
        assert "status-panel--blocked" in stage_after_failed_rerun.text
        assert "A verified staged handoff already exists." not in (
            stage_after_failed_rerun.text
        )
    finally:
        restarted.close()


def test_frozen_blueprint_asset_subset_and_attribution_are_package_resources() -> None:
    vendor_root = STATIC_ROOT / "vendor" / "blueprint"
    icon_root = vendor_root / "icons"
    assert (vendor_root / "blueprint.css").is_file()
    assert (vendor_root / "LICENSE").is_file()
    assert {
        path.stem for path in icon_root.glob("*.svg") if path.is_file()
    } == SELECTED_ICONS

    notices = (PROJECT_ROOT / "THIRD_PARTY_NOTICES.md",)
    assert notices
    notice_text = "\n".join(path.read_text(encoding="utf-8") for path in notices)
    assert "@blueprintjs/core" in notice_text
    assert "6.17.2" in notice_text
    assert "@blueprintjs/icons" in notice_text
    assert "6.13.0" in notice_text
    assert "Apache-2.0" in notice_text


def test_long_receiver_notice_wraps_without_widening_the_workbench() -> None:
    styles = (STATIC_ROOT / "styles.css").read_text(encoding="utf-8")
    notice_rule = re.search(r"\.notice\s*>\s*span\s*\{(?P<body>[^}]*)\}", styles)

    assert notice_rule is not None
    declarations = notice_rule.group("body")
    assert "min-width: 0" in declarations
    assert "overflow-wrap: anywhere" in declarations


def test_mobile_shell_keeps_required_case_facts_visible() -> None:
    styles = (STATIC_ROOT / "styles.css").read_text(encoding="utf-8")
    responsive = re.search(
        r"@media\s*\(max-width:\s*860px\)\s*\{(?P<body>.*?)(?=\n@media|\Z)",
        styles,
        flags=re.DOTALL,
    )

    assert responsive is not None
    compact_rule = re.search(
        r"\.mobile-case-summary\s*\{(?P<body>[^}]*)\}",
        responsive.group("body"),
    )
    assert compact_rule is not None
    assert "display: grid" in compact_rule.group("body")

    medium = re.search(
        r"@media\s*\(max-width:\s*1180px\)\s*\{(?P<body>.*?)(?=\n@media|\Z)",
        styles,
        flags=re.DOTALL,
    )
    assert medium is not None
    assert not re.search(
        r"\.mode-badge\s*\{[^}]*display:\s*none",
        medium.group("body"),
        flags=re.DOTALL,
    )
    assert re.search(
        r"\.mode-badge\s*\{[^}]*display:\s*none",
        responsive.group("body"),
        flags=re.DOTALL,
    )


def test_receipt_card_status_modifiers_control_border_text_and_icon_color() -> None:
    styles = (STATIC_ROOT / "styles.css").read_text(encoding="utf-8")

    expected_colors = {
        "verified": "green",
        "incomplete": "amber",
        "blocked": "red",
    }
    for status, color in expected_colors.items():
        assert re.search(
            rf"\.receipt-card--{status}\s*\{{[^}}]*"
            rf"border-top:\s*3px\s+solid\s+var\(--{color}-strong\)",
            styles,
            flags=re.DOTALL,
        )
        assert re.search(
            rf"\.receipt-card--{status}\s+\.receipt-verdict\s+strong\s*"
            rf"\{{[^}}]*color:\s*var\(--{color}\)",
            styles,
            flags=re.DOTALL,
        )
        assert re.search(
            rf"\.receipt-card--{status}\s+\.receipt-verdict\s*>\s*img\s*"
            r"\{[^}]*filter:",
            styles,
            flags=re.DOTALL,
        )


def test_small_text_and_primary_hover_meet_normal_text_contrast() -> None:
    styles = (STATIC_ROOT / "styles.css").read_text(encoding="utf-8")
    faint = re.search(r"--text-faint:\s*(#[0-9a-fA-F]{6})", styles)
    hover = re.search(
        r"\.button\.bp6-intent-primary:hover:not\(:disabled\),\s*"
        r"a\.button\.bp6-intent-primary:hover\s*\{[^}]*"
        r"background:\s*(#[0-9a-fA-F]{6})",
        styles,
        flags=re.DOTALL,
    )

    assert faint is not None
    assert hover is not None
    assert _contrast_ratio(faint.group(1), "#20252c") >= 4.5
    assert _contrast_ratio(faint.group(1), "#1c2127") >= 4.5
    assert _contrast_ratio("#ffffff", hover.group(1)) >= 4.5
