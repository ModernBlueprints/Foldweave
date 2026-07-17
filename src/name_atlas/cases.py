"""Strict, restart-safe persistence for one local Migration Case."""

from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import os
import stat
import tempfile
import uuid
from collections.abc import Callable
from contextlib import suppress
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from types import TracebackType
from typing import Literal, Self, TypeVar
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from name_atlas.decision_cards.errors import DecisionCardProviderError
from name_atlas.decision_cards.evidence import (
    evidence_fingerprint,
    validate_decision_card,
)
from name_atlas.decision_cards.models import (
    DECISION_CARD_SCHEMA_VERSION,
    MODEL_ALIAS,
    ReplayUsage,
)
from name_atlas.decisions import HumanAction, HumanDecision
from name_atlas.domain import DecisionCard, EvidencePacket
from name_atlas.package_import import ObjectFamily, SourcePackage
from name_atlas.proposals import PathProposal, RiskCategory
from name_atlas.source import SourceMember, SourceSnapshot

MIGRATION_CASE_SCHEMA_VERSION = "migration-case.v1"
PACKAGE_CONTRACT_ID = "name-atlas-linked-package.v1"
PROFILE_ID = "repository-ready-identity.v1"
PORTABLE_SOURCE_SNAPSHOT_SCHEMA_VERSION = "portable-source-snapshot.v1"
DEFAULT_CASE_DIRECTORY = Path(".name-atlas/cases")
oslo_tz = ZoneInfo("Europe/Oslo")
_RecordT = TypeVar("_RecordT")


class MigrationCaseError(RuntimeError):
    """Base error for fail-closed Migration Case persistence."""


class CaseLoadError(MigrationCaseError):
    """A case is absent, unreadable, or violates its strict contract."""


class CaseWriteError(MigrationCaseError):
    """A case could not be persisted atomically."""


class CaseRevisionError(CaseWriteError):
    """The expected prior revision does not match durable state."""


class CaseLockError(CaseWriteError):
    """Another process already owns the case writer lock."""


class CaseFinalizedError(CaseWriteError):
    """A handoff-ready case cannot be changed in place."""


class CaseLifecycle(StrEnum):
    """The complete local Migration Case lifecycle."""

    REVIEW = "review"
    READY_TO_STAGE = "ready_to_stage"
    HANDOFF_READY = "handoff_ready"
    STALE = "stale"
    BLOCKED = "blocked"


class CardDisplayOrigin(StrEnum):
    """Truthful source of the exact card presented to the human."""

    LIVE = "live"
    RECORDED_REPLAY = "recorded_replay"


class CaseDecisionMethod(StrEnum):
    """Exact human interaction that produced the current decision record."""

    BATCH_APPROVAL = "batch_approval"
    INDIVIDUAL_APPROVAL = "individual_approval"
    HUMAN_EDIT = "human_edit"
    INDIVIDUAL_REFUSAL = "individual_refusal"


class _StrictFrozenCaseModel(BaseModel):
    """Immutable fail-closed base for every serialized case contract."""

    model_config = ConfigDict(extra="forbid", frozen=True, strict=True)


def _require_oslo_timestamp(value: datetime, *, label: str) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")
    oslo_value = value.astimezone(oslo_tz)
    if value.utcoffset() != oslo_value.utcoffset():
        raise ValueError(f"{label} must use the Europe/Oslo offset")
    return value


class CaseSourceSnapshot(_StrictFrozenCaseModel):
    """Path-neutral immutable source description retained by the case."""

    schema_version: Literal["portable-source-snapshot.v1"] = (
        PORTABLE_SOURCE_SNAPSHOT_SCHEMA_VERSION
    )
    members: tuple[SourceMember, ...] = Field(min_length=1)
    commitment: str = Field(pattern=r"^[a-f0-9]{64}$")

    @classmethod
    def from_source_snapshot(cls, snapshot: SourceSnapshot) -> Self:
        """Strip the sender-local root from an existing source snapshot."""

        return cls(members=snapshot.members, commitment=snapshot.commitment)

    @model_validator(mode="after")
    def require_sorted_unique_members(self) -> Self:
        paths = tuple(member.relative_path for member in self.members)
        if paths != tuple(sorted(paths)):
            raise ValueError("Case source-snapshot members must be path-sorted.")
        if len(paths) != len(set(paths)):
            raise ValueError("Case source-snapshot member paths must be unique.")
        if _source_snapshot_commitment(self.members) != self.commitment:
            raise ValueError(
                "Case source-snapshot commitment does not match its members."
            )
        return self


class CaseEvidenceRecord(_StrictFrozenCaseModel):
    """One exact canonical outbound evidence packet and its identity."""

    family_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    packet: EvidencePacket
    evidence_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")

    @model_validator(mode="after")
    def require_exact_packet_binding(self) -> Self:
        if self.packet.family_id != self.family_id:
            raise ValueError("Evidence packet family does not match its case record.")
        try:
            actual_fingerprint = evidence_fingerprint(self.packet)
        except DecisionCardProviderError as exc:
            raise ValueError("Case evidence packet is not canonical.") from exc
        if actual_fingerprint != self.evidence_fingerprint:
            raise ValueError("Evidence packet fingerprint does not match its bytes.")
        return self


def card_fingerprint(
    card: DecisionCard,
    *,
    model: str = MODEL_ALIAS,
    card_schema: str = DECISION_CARD_SCHEMA_VERSION,
) -> str:
    """Bind exact card bytes to their model and schema identity."""

    payload = json.dumps(
        {
            "card": card.model_dump(mode="json"),
            "card_schema": card_schema,
            "model": model,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class CaseDecisionCardRecord(_StrictFrozenCaseModel):
    """The exact evidence-bound advisory card shown during review."""

    family_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    evidence_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    card: DecisionCard
    card_fingerprint: str = Field(pattern=r"^[a-f0-9]{64}$")
    model: Literal["gpt-5.6"] = MODEL_ALIAS
    card_schema: Literal["decision-card.v1"] = DECISION_CARD_SCHEMA_VERSION
    display_origin: CardDisplayOrigin
    generated_at: datetime
    usage: ReplayUsage | None = None

    @field_validator("generated_at")
    @classmethod
    def require_oslo_generated_at(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value, label="generated_at")

    @model_validator(mode="after")
    def require_exact_card_fingerprint(self) -> Self:
        if (
            card_fingerprint(
                self.card,
                model=self.model,
                card_schema=self.card_schema,
            )
            != self.card_fingerprint
        ):
            raise ValueError("Decision-card fingerprint does not match its bytes.")
        return self


class CaseDecisionBinding(_StrictFrozenCaseModel):
    """One human decision plus its exact optional Meaning-review provenance."""

    family_id: str = Field(pattern=r"^[a-f0-9]{64}$")
    decision: HumanDecision
    decision_method: CaseDecisionMethod | None
    decision_timestamp: datetime | None
    evidence_fingerprint: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{64}$",
    )
    card_fingerprint: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{64}$",
    )

    @field_validator("decision_timestamp")
    @classmethod
    def require_oslo_decision_timestamp(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is None:
            return None
        return _require_oslo_timestamp(value, label="decision_timestamp")

    @model_validator(mode="after")
    def require_complete_binding(self) -> Self:
        if self.decision.family_id != self.family_id:
            raise ValueError("Human decision family does not match its case binding.")
        if (self.evidence_fingerprint is None) != (self.card_fingerprint is None):
            raise ValueError(
                "Evidence and card fingerprints must both be present or absent."
            )
        if (
            self.decision.action
            in {HumanAction.APPROVED, HumanAction.EDITED, HumanAction.REFUSED}
            and self.decision_timestamp is None
        ):
            raise ValueError("An explicit human action requires its Oslo timestamp.")
        expected_methods = {
            HumanAction.APPROVED: {
                CaseDecisionMethod.BATCH_APPROVAL,
                CaseDecisionMethod.INDIVIDUAL_APPROVAL,
            },
            HumanAction.EDITED: {CaseDecisionMethod.HUMAN_EDIT},
            HumanAction.REFUSED: {CaseDecisionMethod.INDIVIDUAL_REFUSAL},
            HumanAction.PENDING: {None},
            HumanAction.UNRESOLVED: {None},
        }
        if self.decision_method not in expected_methods[self.decision.action]:
            raise ValueError("Decision method does not match the human action.")
        return self


class LocalCasePointers(_StrictFrozenCaseModel):
    """Sender-local paths that are expressly excluded from portable artifacts."""

    output_root: Path
    case_path: Path
    stage_path: Path | None = None
    handoff_path: Path | None = None

    @field_validator("output_root", "case_path", "stage_path", "handoff_path")
    @classmethod
    def require_absolute_path(cls, value: Path | None) -> Path | None:
        if value is not None and not value.is_absolute():
            raise ValueError("Local case pointers must be absolute paths.")
        return value


class MigrationCase(_StrictFrozenCaseModel):
    """The sole mutable workflow authority serialized as one complete record."""

    schema_version: Literal["migration-case.v1"] = MIGRATION_CASE_SCHEMA_VERSION
    revision: int = Field(ge=0)
    case_id: str = Field(pattern=r"^[a-f0-9]{32}$")
    case_name: str = Field(min_length=1, max_length=200)
    package_contract_id: Literal["name-atlas-linked-package.v1"] = PACKAGE_CONTRACT_ID
    profile_id: Literal["repository-ready-identity.v1"] = PROFILE_ID
    created_at: datetime
    updated_at: datetime
    source_root: Path
    source_snapshot: CaseSourceSnapshot
    families: tuple[ObjectFamily, ...] = Field(min_length=1)
    proposals: tuple[PathProposal, ...] = Field(min_length=1)
    evidence_records: tuple[CaseEvidenceRecord, ...] = ()
    card_records: tuple[CaseDecisionCardRecord, ...] = ()
    decisions: tuple[CaseDecisionBinding, ...] = ()
    local_paths: LocalCasePointers
    receipt_fingerprint: str | None = Field(
        default=None,
        pattern=r"^[a-f0-9]{64}$",
    )
    lifecycle: CaseLifecycle = CaseLifecycle.REVIEW

    @field_validator("case_id")
    @classmethod
    def require_uuid4_hex(cls, value: str) -> str:
        parsed = uuid.UUID(hex=value)
        if parsed.version != 4 or parsed.hex != value:
            raise ValueError("case_id must be a lowercase UUID4 hexadecimal value.")
        return value

    @field_validator("created_at")
    @classmethod
    def require_oslo_created_at(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value, label="created_at")

    @field_validator("updated_at")
    @classmethod
    def require_oslo_updated_at(cls, value: datetime) -> datetime:
        return _require_oslo_timestamp(value, label="updated_at")

    @field_validator("source_root")
    @classmethod
    def require_absolute_source_root(cls, value: Path) -> Path:
        if not value.is_absolute():
            raise ValueError("source_root must be absolute.")
        return value

    @model_validator(mode="after")
    def require_complete_internal_bindings(self) -> Self:
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot precede created_at.")

        family_ids = tuple(family.family_id for family in self.families)
        if len(family_ids) != len(set(family_ids)):
            raise ValueError("Migration Case family IDs must be unique.")
        known_family_ids = set(family_ids)

        snapshot_members = {
            member.relative_path: member for member in self.source_snapshot.members
        }
        for family in self.families:
            for member in family.members:
                if snapshot_members.get(member.relative_path) != member:
                    raise ValueError(
                        "Object-family members must match the immutable source "
                        "snapshot."
                    )

        proposal_keys = tuple(
            (proposal.family_id, proposal.role) for proposal in self.proposals
        )
        if len(proposal_keys) != len(set(proposal_keys)):
            raise ValueError("Case proposals must be unique by family and role.")
        if any(
            proposal.family_id not in known_family_ids for proposal in self.proposals
        ):
            raise ValueError("Case proposal references an unknown family.")

        evidence_by_fingerprint = _unique_records(
            self.evidence_records,
            key=lambda record: record.evidence_fingerprint,
            label="evidence fingerprint",
        )
        cards_by_fingerprint = _unique_records(
            self.card_records,
            key=lambda record: record.card_fingerprint,
            label="card fingerprint",
        )
        decisions_by_family = _unique_records(
            self.decisions,
            key=lambda record: record.family_id,
            label="decision family",
        )

        meaning_family_ids = {
            proposal.family_id
            for proposal in self.proposals
            if any(
                risk.category is RiskCategory.MEANING for risk in proposal.risk_signals
            )
        }
        evidence_families: set[str] = set()
        for record in self.evidence_records:
            if record.family_id not in known_family_ids:
                raise ValueError("Case evidence references an unknown family.")
            if record.family_id not in meaning_family_ids:
                raise ValueError("GPT evidence is permitted only for Meaning risk.")
            if record.family_id in evidence_families:
                raise ValueError(
                    "Only one current evidence packet is allowed per family."
                )
            evidence_families.add(record.family_id)

        card_families: set[str] = set()
        for record in self.card_records:
            evidence = evidence_by_fingerprint.get(record.evidence_fingerprint)
            if evidence is None or evidence.family_id != record.family_id:
                raise ValueError("Decision card is not bound to its family evidence.")
            if record.family_id in card_families:
                raise ValueError(
                    "Only one current decision card is allowed per family."
                )
            card_families.add(record.family_id)
            try:
                validate_decision_card(record.card, evidence.packet)
            except DecisionCardProviderError as exc:
                raise ValueError(
                    "Decision card violates its persisted evidence boundary."
                ) from exc

        for binding in self.decisions:
            if binding.family_id not in known_family_ids:
                raise ValueError("Human decision references an unknown family.")
            family = next(
                family
                for family in self.families
                if family.family_id == binding.family_id
            )
            if binding.decision.export_ready and set(
                binding.decision.resolved_targets
            ) != {member.role for member in family.members}:
                raise ValueError(
                    "Resolved targets must cover every present family role exactly."
                )
            is_explicit_action = binding.decision.action in {
                HumanAction.APPROVED,
                HumanAction.EDITED,
                HumanAction.REFUSED,
            }
            if binding.family_id in meaning_family_ids and is_explicit_action:
                if (
                    binding.evidence_fingerprint is None
                    or binding.card_fingerprint is None
                ):
                    raise ValueError(
                        "Meaning-risk human actions require evidence and card bindings."
                    )
            elif binding.family_id not in meaning_family_ids and (
                binding.evidence_fingerprint is not None
                or binding.card_fingerprint is not None
            ):
                raise ValueError(
                    "Mechanical decisions cannot contain fabricated GPT provenance."
                )
            if binding.evidence_fingerprint is not None:
                evidence = evidence_by_fingerprint.get(binding.evidence_fingerprint)
                card = cards_by_fingerprint.get(binding.card_fingerprint or "")
                if (
                    evidence is None
                    or card is None
                    or evidence.family_id != binding.family_id
                    or card.family_id != binding.family_id
                    or card.evidence_fingerprint != evidence.evidence_fingerprint
                ):
                    raise ValueError(
                        "Human decision evidence/card binding is not exact."
                    )

        if self.lifecycle in {
            CaseLifecycle.READY_TO_STAGE,
            CaseLifecycle.HANDOFF_READY,
        } and (
            set(decisions_by_family) != known_family_ids
            or any(
                not binding.decision.export_ready
                for binding in decisions_by_family.values()
            )
        ):
            raise ValueError(
                "Ready cases require one export-ready decision per family."
            )
        if self.lifecycle is CaseLifecycle.HANDOFF_READY:
            if (
                self.receipt_fingerprint is None
                or self.local_paths.stage_path is None
                or self.local_paths.handoff_path is None
            ):
                raise ValueError(
                    "A handoff-ready case requires stage, handoff, and receipt "
                    "pointers."
                )
        elif self.receipt_fingerprint is not None:
            raise ValueError(
                "Only a handoff-ready case may retain a receipt fingerprint."
            )
        return self


def _source_snapshot_commitment(members: tuple[SourceMember, ...]) -> str:
    payload = json.dumps(
        [member.model_dump(mode="json") for member in members],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _unique_records(
    records: tuple[_RecordT, ...],
    *,
    key: Callable[[_RecordT], str],
    label: str,
) -> dict[str, _RecordT]:
    indexed: dict[str, _RecordT] = {}
    for record in records:
        identity = key(record)
        if identity in indexed:
            raise ValueError(f"Duplicate {label}: {identity}")
        indexed[identity] = record
    return indexed


def default_case_path(
    source_root: Path,
    *,
    case_directory: Path = DEFAULT_CASE_DIRECTORY,
) -> Path:
    """Return the canonical absolute default path for one resolved source root."""

    if not isinstance(source_root, Path):
        raise TypeError("source_root must be a pathlib.Path")
    resolved_source_root = source_root.resolve(strict=True)
    digest = hashlib.sha256(
        f"case-root\0{resolved_source_root.as_posix()}".encode()
    ).hexdigest()[:16]
    return case_directory.resolve(strict=False) / f"{digest}.json"


def new_migration_case(
    package: SourcePackage,
    proposals: tuple[PathProposal, ...],
    *,
    case_path: Path,
    output_root: Path,
    case_name: str,
    now: datetime | None = None,
) -> MigrationCase:
    """Create an unsaved revision-zero case from deterministic package state."""

    created_at = now or datetime.now(tz=oslo_tz)
    return MigrationCase(
        revision=0,
        case_id=uuid.uuid4().hex,
        case_name=case_name,
        created_at=created_at,
        updated_at=created_at,
        source_root=package.root,
        source_snapshot=CaseSourceSnapshot.from_source_snapshot(package.snapshot),
        families=package.families,
        proposals=proposals,
        local_paths=LocalCasePointers(
            output_root=output_root.resolve(strict=False),
            case_path=case_path.resolve(strict=False),
        ),
    )


def canonical_case_bytes(case: MigrationCase) -> bytes:
    """Serialize every declared field deterministically with one final newline."""

    payload = json.dumps(
        case.model_dump(mode="json"),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return f"{payload}\n".encode()


def load_case(path: Path) -> MigrationCase:
    """Strictly load one regular case file and verify its local path binding."""

    resolved_path = path.resolve(strict=False)
    try:
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise CaseLoadError("Migration Case path must be a regular file.")
        case = MigrationCase.model_validate_json(path.read_bytes(), strict=True)
    except CaseLoadError:
        raise
    except (OSError, ValidationError) as exc:
        raise CaseLoadError(
            "Migration Case is missing, unreadable, corrupt, or unsupported."
        ) from exc
    if case.local_paths.case_path != resolved_path:
        raise CaseLoadError(
            "Migration Case path does not match its persisted local case pointer."
        )
    return case


class MigrationCaseStore:
    """Path-bound read and process-held writer entry point."""

    def __init__(
        self,
        path: Path,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock or (lambda: datetime.now(tz=oslo_tz))

    def load(self) -> MigrationCase:
        """Load current durable state without acquiring mutation authority."""

        return load_case(self.path)

    def writer(self) -> MigrationCaseWriter:
        """Return a context that holds exclusive mutation authority."""

        return MigrationCaseWriter(self.path, clock=self._clock)


class MigrationCaseWriter:
    """Non-blocking process-held lock plus revisioned atomic case writes."""

    def __init__(self, path: Path, *, clock: Callable[[], datetime]) -> None:
        self.path = path.resolve(strict=False)
        self._clock = clock
        self._lock_descriptor: int | None = None

    def __enter__(self) -> Self:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.path.with_suffix(f"{self.path.suffix}.lock")
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            descriptor = os.open(lock_path, flags, 0o600)
            if not stat.S_ISREG(os.fstat(descriptor).st_mode):
                raise CaseLockError("Migration Case lock path is not a regular file.")
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except CaseLockError:
            with suppress(UnboundLocalError, OSError):
                os.close(descriptor)
            raise
        except (BlockingIOError, OSError) as exc:
            with suppress(UnboundLocalError, OSError):
                os.close(descriptor)
            raise CaseLockError(
                "Migration Case is already open for mutation in another process."
            ) from exc
        self._lock_descriptor = descriptor
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc_value, traceback
        descriptor = self._lock_descriptor
        self._lock_descriptor = None
        if descriptor is not None:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_UN)
            finally:
                os.close(descriptor)

    def load(self) -> MigrationCase:
        """Load durable state while this writer retains mutation authority."""

        self._require_lock()
        return load_case(self.path)

    def save(
        self,
        case: MigrationCase,
        *,
        expected_revision: int | None,
    ) -> MigrationCase:
        """Persist a creation or one mutation against the exact prior revision."""

        self._require_lock()
        if case.local_paths.case_path != self.path:
            raise CaseWriteError(
                "Migration Case local pointer does not match the store path."
            )

        if expected_revision is None:
            if self.path.exists():
                raise CaseRevisionError(
                    "Migration Case already exists; an expected revision is required."
                )
            if case.revision != 0:
                raise CaseRevisionError(
                    "A new Migration Case must start at revision 0."
                )
            updated = case
        else:
            current = load_case(self.path)
            if current.revision != expected_revision:
                raise CaseRevisionError(
                    "Migration Case revision changed before this mutation."
                )
            if case.revision != expected_revision:
                raise CaseRevisionError(
                    "Mutation input must retain the expected prior revision."
                )
            if current.lifecycle is CaseLifecycle.HANDOFF_READY:
                raise CaseFinalizedError(
                    "A handoff-ready Migration Case is read-only; create a new case."
                )
            if (
                case.case_id != current.case_id
                or case.created_at != current.created_at
                or case.source_root != current.source_root
                or case.source_snapshot != current.source_snapshot
            ):
                raise CaseRevisionError(
                    "Mutation attempted to change immutable Migration Case identity."
                )
            updated_at = self._clock()
            _require_oslo_timestamp(updated_at, label="updated_at")
            updated = MigrationCase.model_validate(
                {
                    **case.model_dump(mode="python"),
                    "revision": expected_revision + 1,
                    "updated_at": updated_at,
                },
                strict=True,
            )

        _atomic_write_case(self.path, updated)
        return updated

    def _require_lock(self) -> None:
        if self._lock_descriptor is None:
            raise CaseLockError(
                "Migration Case writes require an active process-held writer lock."
            )


def _atomic_write_case(path: Path, case: MigrationCase) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        view = memoryview(canonical_case_bytes(case))
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    except OSError as exc:
        raise CaseWriteError("Migration Case could not be written atomically.") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        with suppress(FileNotFoundError):
            temporary.unlink()


def _fsync_directory(directory: Path) -> None:
    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError as exc:
        if exc.errno in {errno.EINVAL, errno.ENOTSUP, errno.EROFS}:
            return
        raise
    try:
        try:
            os.fsync(descriptor)
        except OSError as exc:
            if exc.errno not in {errno.EINVAL, errno.ENOTSUP, errno.EROFS}:
                raise
    finally:
        os.close(descriptor)
