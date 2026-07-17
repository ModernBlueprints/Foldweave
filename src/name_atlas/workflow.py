"""Thin in-memory coordinator for the connected Atlas, Decisions, and Proof flow."""

from __future__ import annotations

import os
import tempfile
from contextlib import suppress
from pathlib import Path
from typing import Protocol

from name_atlas.artifacts import StageArtifacts
from name_atlas.decision_cards import (
    MODEL_ALIAS,
    BudgetLedgerError,
    BudgetSnapshot,
    DecisionCardCapExhaustedError,
    DecisionCardProviderError,
    PersistentBudgetLedger,
    RecordedDecisionCard,
    ReplayRecordInvalidError,
    ReplayRecordWriteError,
    build_evidence_packet,
    canonical_evidence_text,
    evidence_fingerprint,
    load_recorded_decision_card,
    microusd_to_usd,
    validate_decision_card,
)
from name_atlas.decisions import (
    DecisionError,
    HumanAction,
    HumanDecision,
    approve_family,
    edit_family,
    pending_family,
    proposals_after_decision,
    refuse_family,
    unresolved_family,
)
from name_atlas.domain import DecisionCard, EvidencePacket, PackageValidationResult
from name_atlas.package_import import ObjectFamily, SourcePackage, import_package
from name_atlas.proposals import PathProposal, RiskCategory, build_proposals
from name_atlas.staging import StageResult, stage_package

DEFAULT_LIVE_CALL_CAP = 8
PROJECT_COST_CAP_USD = 10.0
MAX_EVIDENCE_BYTES = 65_536
MAX_OUTPUT_TOKENS = 1_800
MAX_BILLABLE_INPUT_TOKENS = 100_000
MAX_INPUT_RESERVATION_USD_PER_MILLION = 6.25
OUTPUT_USD_PER_MILLION = 30.0


class _DecisionCardProvider(Protocol):
    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        """Return one bounded card or raise a typed fail-closed error."""


class _PackageValidator(Protocol):
    def validate(self, bag_root: Path) -> PackageValidationResult:
        """Validate a staged package without mutating it."""


class UnavailableReplayDecisionCardProvider:
    """Replay boundary used before a real validated recording exists."""

    provider_kind = "replay"

    async def generate(self, packet: EvidencePacket) -> DecisionCard:
        del packet
        raise ReplayRecordInvalidError(
            "No validated recorded GPT-5.6 response exists for this evidence yet."
        )


class WorkflowSession:
    """Coordinate domain modules without owning their calculations."""

    def __init__(
        self,
        *,
        source_root: Path,
        output_root: Path,
        decision_card_provider: _DecisionCardProvider,
        package_validator: _PackageValidator,
        replay_record_path: Path | None = None,
        budget_ledger_path: Path | None = None,
        live_call_cap: int = DEFAULT_LIVE_CALL_CAP,
        cost_cap_usd: float = PROJECT_COST_CAP_USD,
    ) -> None:
        if live_call_cap < 1:
            raise ValueError("Live call cap must be at least one.")
        if not 0 < cost_cap_usd <= PROJECT_COST_CAP_USD:
            raise ValueError("Cost cap must be positive and no more than USD 10.")
        self.package: SourcePackage = import_package(source_root)
        self.proposals: tuple[PathProposal, ...] = build_proposals(
            self.package.families
        )
        self.output_root = output_root
        self.decision_card_provider = decision_card_provider
        self.package_validator = package_validator
        self.replay_record_path = replay_record_path
        self.cards: dict[str, DecisionCard] = {}
        self.card_fingerprints: dict[str, str] = {}
        self.card_errors: dict[str, str] = {}
        self.decisions: dict[str, HumanDecision] = {}
        self.stage_result: StageResult | None = None
        self.cards_requested = 0
        self.replay_cards_used = 0
        self.cache_hits = 0
        self.live_call_cap = live_call_cap
        self.cost_cap_usd = cost_cap_usd
        self.budget_ledger = PersistentBudgetLedger(
            path=budget_ledger_path,
            live_call_cap=live_call_cap,
            cost_cap_usd=cost_cap_usd,
        )
        budget = self.budget_ledger.snapshot
        self.live_calls_made = budget.live_requests_reserved
        self.provider_attempts_reserved = budget.provider_attempts_reserved
        self.committed_live_cost_usd = microusd_to_usd(budget.committed_cost_microusd)
        self.estimated_live_cost_usd = microusd_to_usd(
            budget.reported_estimated_cost_microusd
        )
        self.last_usage: dict[str, int | float | None] | None = None
        self.replay_record_error: str | None = None
        self.budget_reporting_error: str | None = None
        self._card_cache: dict[str, DecisionCard] = {}
        self._pending_live_records: dict[
            str,
            tuple[DecisionCard, RecordedDecisionCard],
        ] = {}
        self._usage_recorded_fingerprints: set[str] = set()
        recordable_packets = tuple(
            self.evidence_packet(family.family_id)
            for family in self.package.families
            if self.family_requires_card(family.family_id)
        )
        self._recordable_packet = (
            recordable_packets[0]
            if replay_record_path is not None and len(recordable_packets) == 1
            else None
        )
        self._recordable_fingerprint = (
            evidence_fingerprint(self._recordable_packet)
            if self._recordable_packet is not None
            else None
        )

    def family(self, family_id: str) -> ObjectFamily:
        """Return one known stable family or raise a bounded user error."""

        try:
            return next(
                family
                for family in self.package.families
                if family.family_id == family_id
            )
        except StopIteration as exc:
            raise DecisionError(f"Unknown family ID: {family_id}") from exc

    def evidence_packet(self, family_id: str) -> EvidencePacket:
        """Return the complete outbound packet that the UI previews."""

        if not self.family_requires_card(family_id):
            raise DecisionError(
                "This family has no mechanically flagged Meaning risk; "
                "GPT-5.6 is not called."
            )
        return build_evidence_packet(
            self.package,
            self.family(family_id),
            self.proposals,
        )

    def family_requires_card(self, family_id: str) -> bool:
        """Return whether mechanics found a Meaning risk for this family."""

        self.family(family_id)
        return any(
            proposal.meaning_risks
            for proposal in self.proposals
            if proposal.family_id == family_id
        )

    async def generate_card(self, family_id: str) -> DecisionCard:
        """Run the selected provider only after the explicit UI action."""

        packet = self.evidence_packet(family_id)
        self.cards_requested += 1
        self.replay_record_error = None
        self.card_errors.pop(family_id, None)
        try:
            canonical_text = canonical_evidence_text(packet)
            fingerprint = evidence_fingerprint(packet)
        except DecisionCardProviderError as exc:
            self._store_card_failure(family_id, exc)
            raise
        if len(canonical_text.encode("utf-8")) > MAX_EVIDENCE_BYTES:
            error = DecisionCardCapExhaustedError(
                "Outbound evidence exceeds the configured 65,536-byte cap; "
                "the proposal remains unresolved."
            )
            self._store_card_failure(family_id, error)
            raise error
        cached = self._card_cache.get(fingerprint)
        if cached is not None:
            self.cache_hits += 1
            self._bind_card(family_id, fingerprint, cached)
            self._record_provider_usage(
                getattr(self.decision_card_provider, "provider_kind", "test"),
                fingerprint=fingerprint,
            )
            return cached

        pending_live = self._pending_live_records.get(fingerprint)
        if pending_live is not None:
            pending_card, pending_record = pending_live
            try:
                self._persist_live_record(
                    fingerprint=fingerprint,
                    card=pending_card,
                    record=pending_record,
                )
            except ReplayRecordWriteError as exc:
                self.replay_record_error = str(exc)
                self._store_card_failure(family_id, exc)
                raise
            del self._pending_live_records[fingerprint]
            self._card_cache[fingerprint] = pending_card
            self._bind_card(family_id, fingerprint, pending_card)
            self._record_provider_usage("live", fingerprint=fingerprint)
            return pending_card

        provider_kind = getattr(self.decision_card_provider, "provider_kind", "test")
        if provider_kind == "live":
            try:
                self._preflight_replay_target(fingerprint)
                self._reserve_live_budget()
            except (DecisionCardCapExhaustedError, ReplayRecordWriteError) as exc:
                if isinstance(exc, ReplayRecordWriteError):
                    self.replay_record_error = str(exc)
                self._store_card_failure(family_id, exc)
                raise
        try:
            provider_card = await self.decision_card_provider.generate(packet)
            card = validate_decision_card(provider_card, packet)
        except DecisionCardProviderError as exc:
            self._store_card_failure(family_id, exc)
            raise
        live_record: RecordedDecisionCard | None = None
        if provider_kind == "live":
            try:
                live_record = self._validated_live_record(
                    fingerprint=fingerprint,
                    card=card,
                )
                self._persist_live_record(
                    fingerprint=fingerprint,
                    card=card,
                    record=live_record,
                )
            except ReplayRecordWriteError as exc:
                if live_record is not None:
                    self._pending_live_records[fingerprint] = (card, live_record)
                self.replay_record_error = str(exc)
                self._store_card_failure(family_id, exc)
                raise
        if provider_kind == "replay":
            self.replay_cards_used += 1
        self._card_cache[fingerprint] = card
        self._bind_card(family_id, fingerprint, card)
        self._record_provider_usage(provider_kind, fingerprint=fingerprint)
        return card

    def require_replay_record_compatible(self) -> None:
        """Fail unless the configured record matches the pristine hero evidence."""

        record = getattr(self.decision_card_provider, "record", None)
        if not isinstance(record, RecordedDecisionCard):
            raise ReplayRecordInvalidError(
                "No validated recorded GPT-5.6 response is configured."
            )
        if self._recordable_packet is None or self._recordable_fingerprint is None:
            raise ReplayRecordInvalidError(
                "Replay requires exactly one pristine Meaning-risk evidence packet."
            )
        if record.evidence_fingerprint != self._recordable_fingerprint:
            raise ReplayRecordInvalidError(
                "Recorded GPT-5.6 response does not match the pristine hero evidence."
            )
        validate_decision_card(record.decision_card, self._recordable_packet)

    def approve(self, family_id: str) -> HumanDecision:
        """Apply the human's explicit atomic approval."""

        family = self.family(family_id)
        decision = approve_family(
            family,
            self.proposals,
            semantic_card_available=self._card_is_current(family_id),
        )
        self._store_decision(decision)
        return decision

    def edit(self, family_id: str, descriptor: str) -> HumanDecision:
        """Apply one exact human descriptor to every role in the family."""

        family = self.family(family_id)
        other_targets = tuple(
            proposal.proposed_relative_path
            for proposal in self.proposals
            if proposal.family_id != family_id
        )
        decision = edit_family(
            family,
            self.proposals,
            descriptor=descriptor,
            semantic_card_available=self._card_is_current(family_id),
            other_resolved_targets=other_targets,
        )
        self._store_decision(decision)
        return decision

    def approve_low_risk(self) -> tuple[HumanDecision, ...]:
        """Apply one explicit batch action to every currently eligible family."""

        decisions: list[HumanDecision] = []
        for family in self.package.families:
            if not self._low_risk_batch_eligible(family.family_id):
                continue
            decisions.append(
                approve_family(
                    family,
                    self.proposals,
                    semantic_card_available=False,
                )
            )
        if not decisions:
            raise DecisionError("No unresolved low-risk families are eligible.")
        for decision in decisions:
            self._store_decision(decision)
        return tuple(decisions)

    def _low_risk_batch_eligible(self, family_id: str) -> bool:
        """Return whether a batch action may create the first family decision."""

        if family_id in self.decisions or self.family_requires_card(family_id):
            return False
        return not any(
            proposal.mechanical_blockers
            for proposal in self.proposals
            if proposal.family_id == family_id
        )

    def refuse(self, family_id: str) -> HumanDecision:
        """Record an explicit refusal and block complete export."""

        self.family(family_id)
        decision = refuse_family(family_id)
        self._store_decision(decision)
        return decision

    def stage(self) -> StageResult:
        """Run the copy-only transaction from stored family decisions."""

        self.stage_result = None
        ordered_decisions = tuple(
            self.decisions.get(
                family.family_id,
                unresolved_family(family.family_id),
            )
            for family in self.package.families
        )
        self.stage_result = stage_package(
            self.package,
            ordered_decisions,
            output_root=self.output_root,
            package_validator=self.package_validator,
        )
        return self.stage_result

    def view_model(self) -> dict[str, object]:
        """Build the exact connected view from current domain and proof objects."""

        self._sync_budget(self.budget_ledger.snapshot)
        risk_counts = {
            category.value: len(
                {
                    proposal.family_id
                    for proposal in self.proposals
                    if any(risk.category is category for risk in proposal.risk_signals)
                }
            )
            for category in RiskCategory
        }
        families = []
        for family in self.package.families:
            proposals = tuple(
                proposal
                for proposal in self.proposals
                if proposal.family_id == family.family_id
            )
            requires_card = self.family_requires_card(family.family_id)
            packet = self.evidence_packet(family.family_id) if requires_card else None
            decision = self.decisions.get(family.family_id)
            stored_card = self.cards.get(family.family_id)
            card = (
                stored_card
                if packet is not None
                and self.card_fingerprints.get(family.family_id)
                == evidence_fingerprint(packet)
                else None
            )
            mechanical_categories = {
                risk.category
                for proposal in proposals
                for risk in proposal.mechanical_blockers
            }
            model_requirement_met = not requires_card or card is not None
            ready = bool(decision and decision.export_ready)
            families.append(
                {
                    "family": family,
                    "proposals": proposals,
                    "packet": packet,
                    "outbound_text": (
                        canonical_evidence_text(packet) if packet is not None else None
                    ),
                    "requires_card": requires_card,
                    "card": card,
                    "card_stale": stored_card is not None and card is None,
                    "card_error": self.card_errors.get(family.family_id),
                    "decision": decision,
                    "ready": ready,
                    "mechanically_blocked": bool(mechanical_categories),
                    "approve_enabled": (
                        model_requirement_met
                        and not mechanical_categories
                        and not ready
                    ),
                    "edit_enabled": (
                        model_requirement_met
                        and mechanical_categories.issubset({RiskCategory.COLLISION})
                    ),
                }
            )
        ready_count = sum(bool(item["ready"]) for item in families)
        eligible_low_risk_count = sum(
            self._low_risk_batch_eligible(item["family"].family_id) for item in families
        )
        hard_blocker_count = sum(
            bool(item["mechanically_blocked"])
            or item["card_error"] is not None
            or (
                isinstance(item["decision"], HumanDecision)
                and item["decision"].action is HumanAction.REFUSED
            )
            for item in families
        )
        decision_items = tuple(
            item
            for item in families
            if bool(item["requires_card"])
            or bool(item["mechanically_blocked"])
            or item["card"] is not None
            or bool(item["card_stale"])
            or item["card_error"] is not None
            or (
                isinstance(item["decision"], HumanDecision)
                and item["decision"].action
                in {
                    HumanAction.EDITED,
                    HumanAction.REFUSED,
                    HumanAction.UNRESOLVED,
                }
            )
        )
        proof: StageArtifacts | None = (
            self.stage_result.artifacts if self.stage_result is not None else None
        )
        return {
            "source_root": str(self.package.root),
            "snapshot": self.package.snapshot,
            "family_count": len(self.package.families),
            "content_count": len(self.package.content_members),
            "proposal_count": len(self.proposals),
            "risk_counts": {
                category.value: risk_counts[category.value] for category in RiskCategory
            },
            "families": families,
            "decision_items": decision_items,
            "eligible_low_risk_count": eligible_low_risk_count,
            "hard_blocker_count": hard_blocker_count,
            "ready_count": ready_count,
            "export_ready": ready_count == len(families),
            "cards_requested": self.cards_requested,
            "decision_metrics": {
                "model": MODEL_ALIAS,
                "cards_requested": self.cards_requested,
                "live_calls_made": self.live_calls_made,
                "provider_attempts_reserved": self.provider_attempts_reserved,
                "replay_cards_used": self.replay_cards_used,
                "cache_hits": self.cache_hits,
                "calls_avoided_by_deterministic_triage": sum(
                    not self.family_requires_card(family.family_id)
                    for family in self.package.families
                ),
                "estimated_live_cost_usd": self.estimated_live_cost_usd,
                "committed_live_cost_usd": self.committed_live_cost_usd,
                "configured_live_call_cap": self.live_call_cap,
                "configured_cost_cap_usd": self.cost_cap_usd,
                "last_usage": self.last_usage,
                "replay_record_error": self.replay_record_error,
                "budget_reporting_error": self.budget_reporting_error,
            },
            "proof": proof,
            "stage_root": (
                str(self.stage_result.stage_root)
                if self.stage_result is not None
                else None
            ),
        }

    def _store_decision(self, decision: HumanDecision) -> None:
        self.decisions[decision.family_id] = decision
        self.proposals = proposals_after_decision(self.proposals, decision)
        self.stage_result = None

    def _reserve_live_budget(self) -> None:
        policy = getattr(self.decision_card_provider, "policy", None)
        max_output_tokens = getattr(policy, "max_output_tokens", MAX_OUTPUT_TOKENS)
        sdk_max_retries = getattr(policy, "sdk_max_retries", 0)
        provider_attempts = sdk_max_retries + 1
        per_attempt_usd = (
            MAX_BILLABLE_INPUT_TOKENS * MAX_INPUT_RESERVATION_USD_PER_MILLION
            + max_output_tokens * OUTPUT_USD_PER_MILLION
        ) / 1_000_000
        snapshot = self.budget_ledger.reserve(
            reservation_usd=per_attempt_usd * provider_attempts,
            provider_attempts=provider_attempts,
        )
        self._sync_budget(snapshot)

    def _store_card_failure(
        self,
        family_id: str,
        error: DecisionCardProviderError,
    ) -> None:
        self.cards.pop(family_id, None)
        self.card_fingerprints.pop(family_id, None)
        existing = self.decisions.get(family_id)
        if existing is None or not existing.export_ready:
            self._store_decision(unresolved_family(family_id))
        self.card_errors[family_id] = str(error)

    def _clear_provider_failure(self, family_id: str) -> None:
        existing = self.decisions.get(family_id)
        if existing is not None and not existing.export_ready:
            self._store_decision(pending_family(family_id))

    def _bind_card(
        self,
        family_id: str,
        fingerprint: str,
        card: DecisionCard,
    ) -> None:
        self.cards[family_id] = card
        self.card_fingerprints[family_id] = fingerprint
        self._clear_provider_failure(family_id)

    def _card_is_current(self, family_id: str) -> bool:
        if family_id not in self.cards:
            return False
        packet = self.evidence_packet(family_id)
        return self.card_fingerprints.get(family_id) == evidence_fingerprint(packet)

    def _record_provider_usage(
        self,
        provider_kind: str,
        *,
        fingerprint: str,
    ) -> None:
        record = getattr(self.decision_card_provider, "last_record", None)
        if record is None and provider_kind == "replay":
            record = getattr(self.decision_card_provider, "record", None)
        if not isinstance(record, RecordedDecisionCard):
            return
        usage = record.usage
        self.last_usage = usage.model_dump(mode="python")
        if (
            provider_kind == "live"
            and usage.estimated_cost_usd is not None
            and fingerprint not in self._usage_recorded_fingerprints
        ):
            try:
                snapshot = self.budget_ledger.record_reported_cost(
                    usage.estimated_cost_usd
                )
            except BudgetLedgerError as exc:
                self.budget_reporting_error = (
                    "The conservative GPT budget reservation is intact, but "
                    f"reported usage could not be recorded: {exc}"
                )
                return
            self._sync_budget(snapshot)
            self._usage_recorded_fingerprints.add(fingerprint)
            self.budget_reporting_error = None

    def _sync_budget(self, snapshot: BudgetSnapshot) -> None:
        self.live_calls_made = snapshot.live_requests_reserved
        self.provider_attempts_reserved = snapshot.provider_attempts_reserved
        self.committed_live_cost_usd = microusd_to_usd(snapshot.committed_cost_microusd)
        self.estimated_live_cost_usd = microusd_to_usd(
            snapshot.reported_estimated_cost_microusd
        )

    def _validated_live_record(
        self,
        *,
        fingerprint: str,
        card: DecisionCard,
    ) -> RecordedDecisionCard:
        record = getattr(self.decision_card_provider, "last_record", None)
        if not isinstance(record, RecordedDecisionCard):
            raise ReplayRecordWriteError(
                "The live provider returned no sanitized replay record; "
                "the proposal remains unresolved."
            )
        if record.evidence_fingerprint != fingerprint or record.decision_card != card:
            raise ReplayRecordWriteError(
                "The live replay record does not match the validated response and "
                "evidence; the proposal remains unresolved."
            )
        return record

    def _preflight_replay_target(self, fingerprint: str) -> None:
        if self.replay_record_path is None:
            return
        if self._recordable_fingerprint is None:
            raise ReplayRecordWriteError(
                "Canonical replay recording requires exactly one pristine "
                "Meaning-risk family."
            )
        if fingerprint != self._recordable_fingerprint:
            return
        try:
            self.replay_record_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise ReplayRecordWriteError(
                "The canonical replay directory is unavailable; no live call was made."
            ) from exc
        if not os.path.lexists(self.replay_record_path):
            return
        try:
            existing = load_recorded_decision_card(self.replay_record_path.read_bytes())
        except (OSError, DecisionCardProviderError) as exc:
            raise ReplayRecordWriteError(
                "The existing canonical replay record is invalid; no live call "
                "was made and the file was left unchanged."
            ) from exc
        if existing.evidence_fingerprint != fingerprint:
            raise ReplayRecordWriteError(
                "The existing canonical replay record targets different evidence; "
                "no live call was made and the file was left unchanged."
            )
        if self._recordable_packet is None:
            raise ReplayRecordWriteError(
                "The pristine replay evidence is unavailable; no live call was made."
            )
        try:
            validate_decision_card(existing.decision_card, self._recordable_packet)
        except DecisionCardProviderError as exc:
            raise ReplayRecordWriteError(
                "The existing canonical replay card is incompatible with the "
                "pristine evidence; no live call was made."
            ) from exc

    def _persist_live_record(
        self,
        *,
        fingerprint: str,
        card: DecisionCard,
        record: RecordedDecisionCard,
    ) -> None:
        if (
            self.replay_record_path is None
            or fingerprint != self._recordable_fingerprint
        ):
            return
        if record.evidence_fingerprint != fingerprint or record.decision_card != card:
            raise ReplayRecordWriteError(
                "The live replay record is not bound to the validated response."
            )
        self._preflight_replay_target(fingerprint)
        if os.path.lexists(self.replay_record_path):
            return

        try:
            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{self.replay_record_path.name}.",
                suffix=".tmp",
                dir=self.replay_record_path.parent,
            )
        except OSError as exc:
            raise ReplayRecordWriteError(
                "The validated GPT-5.6 response could not be prepared for replay."
            ) from exc
        temporary = Path(temporary_name)
        try:
            payload = f"{record.model_dump_json(indent=2)}\n".encode()
            view = memoryview(payload)
            while view:
                written = os.write(descriptor, view)
                view = view[written:]
            os.fsync(descriptor)
            os.close(descriptor)
            descriptor = -1
            os.link(temporary, self.replay_record_path, follow_symlinks=False)
            directory_descriptor = os.open(
                self.replay_record_path.parent,
                os.O_RDONLY,
            )
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except FileExistsError:
            self._preflight_replay_target(fingerprint)
            return
        except OSError as exc:
            raise ReplayRecordWriteError(
                "The validated GPT-5.6 response could not be saved durably for "
                "replay; retrying will not make another provider call."
            ) from exc
        finally:
            if descriptor >= 0:
                os.close(descriptor)
            with suppress(FileNotFoundError):
                temporary.unlink()
        try:
            persisted = load_recorded_decision_card(
                self.replay_record_path.read_bytes()
            )
        except (OSError, DecisionCardProviderError) as exc:
            raise ReplayRecordWriteError(
                "The canonical replay record failed durable read-back validation."
            ) from exc
        if persisted != record:
            raise ReplayRecordWriteError(
                "The canonical replay record differs from the validated live record."
            )
