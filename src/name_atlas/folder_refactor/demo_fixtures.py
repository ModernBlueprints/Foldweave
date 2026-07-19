"""Packaged Connected Change fixtures used by replay and release proof."""

from __future__ import annotations

import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

from name_atlas.folder_refactor.serialization import canonical_sha256

HERO_REQUEST = (
    "Prepare this Apollo client-project folder for handoff as Northstar. Keep every "
    "file. Use the briefing and project notes to organize approved deliverables, "
    "working material, research, and meeting notes into clear folders. Rename "
    "Apollo-labelled paths to Northstar and keep every supported link working."
)
HERO_RESULT_FOLDER_NAME = "northstar"
HERO_FILE_COUNT = 24
HERO_MARKDOWN_FILE_COUNT = 5
HERO_SUPPORTED_LINK_COUNT = 23
HERO_EMPTY_DIRECTORY = "working/templates/empty"

AMBIGUITY_REQUEST = (
    "Prepare this Apollo presentation folder for Northstar handoff. Keep both "
    "presentations. Put the approved presentation in final deliverables and the "
    "internal-review presentation in working material. Keep every supported link "
    "working."
)
AMBIGUITY_ANSWER = (
    "Candidate A (`presentations/Apollo-candidate-a.pdf`) is the approved "
    "presentation. Candidate B is internal review."
)
AMBIGUITY_RESULT_FOLDER_NAME = "northstar-presentations"
FOLDWEAVE_F0B_FIXTURE_NAME = "sofia-apollo-native-root-review.v1"
# Pinned below after hashing the complete packaged source, request, expected
# target map, and explicit empty-directory requirement. The focused contract-
# freeze test independently recomputes it from the packaged assets.
FOLDWEAVE_F0B_FIXTURE_FINGERPRINT = (
    "fd2e57938875453d3eca99085bb80e266f44b9c8e2195453247373ec4e593fa7"
)


@dataclass(frozen=True, slots=True)
class DemoLogicalMember:
    """One expected logical role across the two differently arranged projects.

    This correspondence is fixture truth for replay qualification and tests. It is
    never supplied to the receiver matcher as matching evidence.
    """

    sofia_path: str
    martin_path: str
    target_path: str


@dataclass(frozen=True, slots=True)
class PackagedFixtureTemplates:
    """Read-only paths to the fixture templates included in the distribution."""

    root: Path
    sofia_root: Path
    martin_root: Path
    ambiguity_root: Path


@dataclass(frozen=True, slots=True)
class MaterializedHeroFixture:
    """Writable copy of the two-layout hero with explicit empty directories."""

    root: Path
    sofia_root: Path
    martin_root: Path
    request: str
    result_folder_name: str


@dataclass(frozen=True, slots=True)
class MaterializedAmbiguityFixture:
    """Writable copy of the one-question textual fixture."""

    root: Path
    source_root: Path
    request: str
    answer: str
    result_folder_name: str


HERO_LOGICAL_MEMBERS: tuple[DemoLogicalMember, ...] = (
    DemoLogicalMember(".env.example", ".env.example", ".env.example"),
    DemoLogicalMember(
        "briefing/Apollo-client-brief.md",
        "intake/client/brief.md",
        "handoff/briefing/Northstar-client-brief.md",
    ),
    DemoLogicalMember(
        "notes/Apollo-project-notes.md",
        "desk/project-overview.md",
        "handoff/notes/Northstar-project-notes.md",
    ),
    DemoLogicalMember(
        "notes/meetings/Apollo-kickoff-notes.md",
        "conversations/kickoff.md",
        "handoff/meeting-notes/Northstar-kickoff-notes.md",
    ),
    DemoLogicalMember(
        "notes/meetings/Apollo-approval-notes.md",
        "conversations/approval.md",
        "handoff/meeting-notes/Northstar-approval-notes.md",
    ),
    DemoLogicalMember(
        "handoff/Apollo-delivery-notes.md",
        "sendoff/delivery.md",
        "handoff/Northstar-delivery-notes.md",
    ),
    DemoLogicalMember(
        "research/Apollo-audience-research.txt",
        "evidence/audience.txt",
        "research/audience-research.txt",
    ),
    DemoLogicalMember(
        "research/Apollo-interview-summary.txt",
        "evidence/interviews.txt",
        "research/interview-summary.txt",
    ),
    DemoLogicalMember(
        "research/Apollo-source-log.csv",
        "evidence/sources.csv",
        "research/source-log.csv",
    ),
    DemoLogicalMember(
        "working/design/Apollo-cover-draft.png",
        "drafts/visual/cover.png",
        "working/design/Northstar-cover-draft.png",
    ),
    DemoLogicalMember(
        "working/design/Apollo-layout-draft.jpg",
        "drafts/visual/layout.jpg",
        "working/design/Northstar-layout-draft.jpg",
    ),
    DemoLogicalMember(
        "working/audio/Apollo-narration-draft.wav",
        "drafts/sound/narration.wav",
        "working/audio/Northstar-narration-draft.wav",
    ),
    DemoLogicalMember(
        "working/audio/Apollo-interview-excerpt.mp3",
        "drafts/sound/interview.mp3",
        "working/audio/Northstar-interview-excerpt.mp3",
    ),
    DemoLogicalMember(
        "working/data/Apollo-budget-working.csv",
        "drafts/numbers/budget.csv",
        "working/data/Northstar-budget-working.csv",
    ),
    DemoLogicalMember(
        "working/data/Apollo-timeline-working.xlsx",
        "drafts/numbers/timeline.xlsx",
        "working/data/Northstar-timeline-working.xlsx",
    ),
    DemoLogicalMember(
        "working/cache/Apollo-layout-cache.bin",
        "drafts/tmp/layout.bin",
        "working/cache/Northstar-layout-cache.bin",
    ),
    DemoLogicalMember(
        "approved/Apollo-final-report.pdf",
        "ready/report.pdf",
        "deliverables/approved/Northstar-final-report.pdf",
    ),
    DemoLogicalMember(
        "approved/Apollo-presentation.pdf",
        "ready/slides.pdf",
        "deliverables/approved/Northstar-presentation.pdf",
    ),
    DemoLogicalMember(
        "approved/Apollo-cover.png",
        "ready/cover.png",
        "deliverables/approved/Northstar-cover.png",
    ),
    DemoLogicalMember(
        "approved/Apollo-budget.csv",
        "ready/budget.csv",
        "deliverables/approved/Northstar-budget.csv",
    ),
    DemoLogicalMember(
        "approved/Apollo-narration.wav",
        "ready/narration.wav",
        "deliverables/approved/Northstar-narration.wav",
    ),
    DemoLogicalMember(
        "references/Apollo-brand-guide.pdf",
        "library/brand.pdf",
        "research/references/Northstar-brand-guide.pdf",
    ),
    DemoLogicalMember(
        "references/Apollo-contact-sheet.jpg",
        "library/contact.jpg",
        "research/references/Northstar-contact-sheet.jpg",
    ),
    DemoLogicalMember(
        "references/Apollo-terms.txt",
        "library/terms.txt",
        "research/references/Northstar-terms.txt",
    ),
)

AMBIGUITY_TARGET_PATH_PAIRS: tuple[tuple[str, str], ...] = (
    (
        "notes/client-approval.md",
        "handoff/notes/client-approval.md",
    ),
    (
        "notes/internal-review.md",
        "handoff/notes/internal-review.md",
    ),
    (
        "presentations/Apollo-candidate-a.pdf",
        "deliverables/final/Northstar-approved-presentation.pdf",
    ),
    (
        "presentations/Apollo-candidate-b.pdf",
        "working/internal-review/Northstar-presentation-review.pdf",
    ),
)


def packaged_fixture_templates() -> PackagedFixtureTemplates:
    """Locate the source templates in either a checkout or an installed wheel."""

    package_root = Path(__file__).resolve().parents[1]
    checkout_root = package_root.parents[1]
    if (checkout_root / "pyproject.toml").is_file() and (
        checkout_root / "src" / "name_atlas"
    ).resolve() == package_root:
        root = checkout_root / "sample_data" / "connected_change"
    else:
        root = package_root / "sample_data" / "connected_change"
    templates = PackagedFixtureTemplates(
        root=root,
        sofia_root=root / "sofia_apollo",
        martin_root=root / "martin_apollo",
        ambiguity_root=root / "ambiguity",
    )
    for required in (
        templates.sofia_root,
        templates.martin_root,
        templates.ambiguity_root,
    ):
        if not required.is_dir():
            raise FileNotFoundError(
                f"Packaged fixture directory is missing: {required}"
            )
    return templates


def materialize_hero_fixture(destination: Path) -> MaterializedHeroFixture:
    """Create an absent writable Sofia/Martin fixture pair at ``destination``."""

    if destination.exists():
        raise FileExistsError(f"Fixture destination already exists: {destination}")
    templates = packaged_fixture_templates()
    destination.mkdir(parents=True)
    sofia_root = destination / "sofia-apollo"
    martin_root = destination / "martin-apollo"
    shutil.copytree(templates.sofia_root, sofia_root)
    shutil.copytree(templates.martin_root, martin_root)
    for root in (sofia_root, martin_root):
        (root / HERO_EMPTY_DIRECTORY).mkdir(parents=True)
    return MaterializedHeroFixture(
        root=destination,
        sofia_root=sofia_root,
        martin_root=martin_root,
        request=HERO_REQUEST,
        result_folder_name=HERO_RESULT_FOLDER_NAME,
    )


def materialize_ambiguity_fixture(destination: Path) -> MaterializedAmbiguityFixture:
    """Create an absent writable one-question fixture at ``destination``."""

    if destination.exists():
        raise FileExistsError(f"Fixture destination already exists: {destination}")
    templates = packaged_fixture_templates()
    source_root = destination / "apollo-presentations"
    destination.mkdir(parents=True)
    shutil.copytree(templates.ambiguity_root, source_root)
    return MaterializedAmbiguityFixture(
        root=destination,
        source_root=source_root,
        request=AMBIGUITY_REQUEST,
        answer=AMBIGUITY_ANSWER,
        result_folder_name=AMBIGUITY_RESULT_FOLDER_NAME,
    )


def hero_target_paths() -> dict[str, str]:
    """Return a fresh origin-path-to-target map for planner qualification."""

    return {member.sofia_path: member.target_path for member in HERO_LOGICAL_MEMBERS}


def hero_correspondence() -> dict[str, str]:
    """Return fixture-only Sofia-to-Martin correspondence for assertions."""

    return {member.sofia_path: member.martin_path for member in HERO_LOGICAL_MEMBERS}


def foldweave_f0b_fixture_fingerprint() -> str:
    """Fingerprint the exact source and expected plan used for F0b qualification."""

    source_root = packaged_fixture_templates().sofia_root
    source_members = []
    for member_path in sorted(source_root.rglob("*")):
        if not member_path.is_file() or member_path.is_symlink():
            continue
        payload = member_path.read_bytes()
        source_members.append(
            {
                "relative_path": member_path.relative_to(source_root).as_posix(),
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return canonical_sha256(
        {
            "domain": "foldweave:f0b:qualification-fixture:v1",
            "fixture_name": FOLDWEAVE_F0B_FIXTURE_NAME,
            "request": HERO_REQUEST,
            "result_folder_name": HERO_RESULT_FOLDER_NAME,
            "source_members": source_members,
            "explicit_empty_directories": [HERO_EMPTY_DIRECTORY],
            "expected_targets": hero_target_paths(),
        }
    )


def ambiguity_target_paths() -> dict[str, str]:
    """Return the expected plan after the canonical clarification answer."""

    return dict(AMBIGUITY_TARGET_PATH_PAIRS)
