"""Exact sanitized GPT-5.6 planner recordings and keyless replay."""

from __future__ import annotations

import os
import tempfile
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Literal, Self
from zoneinfo import ZoneInfo

from pydantic import Field, model_validator

from name_atlas.folder_refactor.connected_change.accepted_plan import (
    FolderAcceptedPlanV2,
)
from name_atlas.folder_refactor.contracts import SHA256_PATTERN, StrictFrozenModel
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    PlannerObservableTurn,
    ProviderToolResponse,
)
from name_atlas.folder_refactor.planner_prompt import (
    PLANNER_INSTRUCTIONS_FINGERPRINT,
    PLANNER_TOOL_SCHEMA_FINGERPRINT,
)
from name_atlas.folder_refactor.planner_provider import (
    PlannerProviderResponseError,
    ScriptedProviderExhaustedError,
)
from name_atlas.folder_refactor.portable_artifacts import strict_json_object
from name_atlas.folder_refactor.receipt_contracts import (
    FolderEvidenceLedger,
    FolderPlannerUsage,
)
from name_atlas.folder_refactor.serialization import (
    canonical_json_bytes,
    canonical_sha256,
    request_fingerprint,
)

oslo_tz = ZoneInfo("Europe/Oslo")


class PlannerReplayError(RuntimeError):
    """A planner recording is missing, malformed, or incompatible."""


class RecordedPlannerTurn(StrictFrozenModel):
    """One live response bound to the provider-neutral exact turn input."""

    response_turn: int = Field(ge=1, le=8)
    input_binding_fingerprint: str = Field(pattern=SHA256_PATTERN)
    response: ProviderToolResponse
    usage: FolderPlannerUsage

    @model_validator(mode="after")
    def require_live_turn(self) -> Self:
        if self.response.provider_kind != "live":
            raise ValueError(
                "A recorded planner turn must derive from a live response."
            )
        if self.usage.response_turn != self.response_turn:
            raise ValueError("Recorded usage must target the same response turn.")
        if self.usage.recorded_at is None or self.usage.latency_ms is None:
            raise ValueError("Recorded live usage requires timestamp and latency.")
        return self


class FolderPlannerReplay(StrictFrozenModel):
    """One exact, sanitized, fixture-bound successful GPT-5.6 planning run."""

    schema_version: Literal["folder-planner-replay.v1"] = "folder-planner-replay.v1"
    fixture_kind: Literal["hero", "clarification"]
    fixture_name: str = Field(min_length=1, max_length=200)
    fixture_fingerprint: str = Field(pattern=SHA256_PATTERN)
    source_commitment: str = Field(pattern=SHA256_PATTERN)
    request: str = Field(min_length=1, max_length=8_000)
    request_fingerprint: str = Field(pattern=SHA256_PATTERN)
    planner_turn_schema_version: Literal["folder-planner-turn-input.v1"] = (
        "folder-planner-turn-input.v1"
    )
    tool_schema_version: Literal["folder-planner-tools.v1"] = "folder-planner-tools.v1"
    planner_instructions_fingerprint: str = Field(pattern=SHA256_PATTERN)
    tool_schema_fingerprint: str = Field(pattern=SHA256_PATTERN)
    evidence_schema_version: Literal["folder-evidence-ledger.v1"] = (
        "folder-evidence-ledger.v1"
    )
    model_alias: Literal["gpt-5.6"] = "gpt-5.6"
    returned_model_ids: tuple[str, ...] = Field(min_length=1)
    store_false: Literal[True] = True
    generated_at: datetime
    clarification_question: str | None = Field(
        default=None,
        min_length=1,
        max_length=1_000,
    )
    clarification_answer: str | None = Field(
        default=None,
        min_length=1,
        max_length=4_000,
    )
    live_evidence_ledger: FolderEvidenceLedger
    accepted_plan: FolderAcceptedPlanV2
    originating_receipt_fingerprint: str = Field(pattern=SHA256_PATTERN)
    change_file_fingerprint: str = Field(pattern=SHA256_PATTERN)
    turns: tuple[RecordedPlannerTurn, ...] = Field(min_length=1, max_length=8)
    replay_fingerprint: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def require_exact_recording(self) -> Self:
        if self.generated_at.tzinfo is None or self.generated_at.utcoffset() is None:
            raise ValueError("Replay generation time must be timezone-aware.")
        if (
            self.generated_at.utcoffset()
            != self.generated_at.astimezone(oslo_tz).utcoffset()
        ):
            raise ValueError("Replay generation time must use Europe/Oslo.")
        if self.request_fingerprint != request_fingerprint(self.request):
            raise ValueError("Replay request fingerprint does not match its text.")
        if (
            self.planner_instructions_fingerprint != PLANNER_INSTRUCTIONS_FINGERPRINT
            or self.tool_schema_fingerprint != PLANNER_TOOL_SCHEMA_FINGERPRINT
        ):
            raise ValueError("Replay prompt or tool contract differs from this build.")
        ledger = self.live_evidence_ledger
        if (
            ledger.provider_kind != "live"
            or ledger.store_false is not True
            or ledger.source_commitment != self.source_commitment
            or ledger.request_fingerprint != self.request_fingerprint
            or ledger.returned_model_ids != self.returned_model_ids
            or ledger.clarification_question != self.clarification_question
            or ledger.clarification_answer != self.clarification_answer
            or canonical_sha256(self.accepted_plan) != ledger.accepted_plan_fingerprint
        ):
            raise ValueError("Replay does not match its successful live transcript.")
        expected_kind = (
            "clarification" if self.clarification_question is not None else "hero"
        )
        if self.fixture_kind != expected_kind:
            raise ValueError("Replay fixture kind conflicts with clarification state.")
        if tuple(item.response_turn for item in self.turns) != tuple(
            range(1, len(self.turns) + 1)
        ):
            raise ValueError("Recorded planner turns must be contiguous.")
        if len(self.turns) != ledger.response_turn_count:
            raise ValueError("Replay turn count differs from live evidence.")
        usage_by_turn = {item.response_turn: item for item in ledger.usage}
        if len(usage_by_turn) != len(self.turns):
            raise ValueError("Every successful live turn requires one usage record.")
        for recorded, observable in zip(
            self.turns,
            ledger.observable_turns,
            strict=True,
        ):
            response = _provider_response_from_turn(observable)
            turn_input = FolderPlannerTurnInput.model_validate_json(
                canonical_json_bytes(observable.input_payload),
                strict=True,
            )
            if (
                recorded.response != response
                or recorded.usage != usage_by_turn[recorded.response_turn]
                or recorded.input_binding_fingerprint
                != replay_turn_input_fingerprint(turn_input)
            ):
                raise ValueError("Recorded turn differs from its live observable turn.")
        if self.fixture_fingerprint != planner_fixture_fingerprint(
            source_commitment=self.source_commitment,
            request=self.request,
            accepted_plan=self.accepted_plan,
            live_evidence_ledger=ledger,
        ):
            raise ValueError("Replay fixture fingerprint is not exact.")
        if self.replay_fingerprint != canonical_sha256(replay_core_payload(self)):
            raise ValueError("Planner replay fingerprint is not exact.")
        return self


def replay_turn_input_payload(
    turn_input: FolderPlannerTurnInput,
) -> dict[str, object]:
    """Return the exact replay binding while excluding run-local authority."""

    payload = turn_input.model_dump(mode="json")
    payload.pop("job_id")
    payload.pop("provider_kind")
    prior_turns = payload.get("prior_turns")
    if not isinstance(prior_turns, list):
        raise ValueError("Planner turn history must serialize as a list.")
    for prior in prior_turns:
        if not isinstance(prior, dict):
            raise ValueError("Planner turn history item must be an object.")
        prior.pop("provider_kind")
        prior.pop("response_fingerprint")
    return payload


def replay_turn_input_fingerprint(turn_input: FolderPlannerTurnInput) -> str:
    """Bind every portable turn fact except job ID and provider origin label."""

    return canonical_sha256(replay_turn_input_payload(turn_input))


def planner_fixture_fingerprint(
    *,
    source_commitment: str,
    request: str,
    accepted_plan: FolderAcceptedPlanV2,
    live_evidence_ledger: FolderEvidenceLedger,
) -> str:
    """Bind the exact fixture, instruction, schemas, evidence, and accepted map."""

    return canonical_sha256(
        {
            "accepted_plan": accepted_plan.model_dump(mode="json"),
            "domain": "name-atlas:folder-planner-replay-fixture:v1",
            "evidence_schema_version": live_evidence_ledger.schema_version,
            "live_transcript_fingerprint": (
                live_evidence_ledger.transcript_fingerprint
            ),
            "model_alias": live_evidence_ledger.model_alias,
            "planner_instructions_fingerprint": PLANNER_INSTRUCTIONS_FINGERPRINT,
            "planner_turn_schema_version": "folder-planner-turn-input.v1",
            "request": request,
            "request_fingerprint": request_fingerprint(request),
            "source_commitment": source_commitment,
            "tool_schema_version": "folder-planner-tools.v1",
            "tool_schema_fingerprint": PLANNER_TOOL_SCHEMA_FINGERPRINT,
        }
    )


def replay_core_payload(replay: FolderPlannerReplay) -> dict[str, object]:
    """Return the replay hash domain without its own fingerprint."""

    return replay.model_dump(mode="json", exclude={"replay_fingerprint"})


def build_folder_planner_replay(
    *,
    fixture_kind: Literal["hero", "clarification"],
    fixture_name: str,
    request: str,
    live_evidence_ledger: FolderEvidenceLedger,
    accepted_plan: FolderAcceptedPlanV2,
    originating_receipt_fingerprint: str,
    change_file_fingerprint: str,
    generated_at: datetime | None = None,
) -> FolderPlannerReplay:
    """Build one canonical replay only from a successful live result."""

    usage_by_turn = {item.response_turn: item for item in live_evidence_ledger.usage}
    turns = tuple(
        RecordedPlannerTurn(
            response_turn=turn.response_turn,
            input_binding_fingerprint=replay_turn_input_fingerprint(
                FolderPlannerTurnInput.model_validate_json(
                    canonical_json_bytes(turn.input_payload),
                    strict=True,
                )
            ),
            response=_provider_response_from_turn(turn),
            usage=usage_by_turn[turn.response_turn],
        )
        for turn in live_evidence_ledger.observable_turns
    )
    values = {
        "fixture_kind": fixture_kind,
        "fixture_name": fixture_name,
        "fixture_fingerprint": planner_fixture_fingerprint(
            source_commitment=live_evidence_ledger.source_commitment,
            request=request,
            accepted_plan=accepted_plan,
            live_evidence_ledger=live_evidence_ledger,
        ),
        "source_commitment": live_evidence_ledger.source_commitment,
        "request": request,
        "request_fingerprint": request_fingerprint(request),
        "planner_instructions_fingerprint": PLANNER_INSTRUCTIONS_FINGERPRINT,
        "tool_schema_fingerprint": PLANNER_TOOL_SCHEMA_FINGERPRINT,
        "returned_model_ids": live_evidence_ledger.returned_model_ids,
        "generated_at": generated_at or datetime.now(tz=oslo_tz),
        "clarification_question": live_evidence_ledger.clarification_question,
        "clarification_answer": live_evidence_ledger.clarification_answer,
        "live_evidence_ledger": live_evidence_ledger,
        "accepted_plan": accepted_plan,
        "originating_receipt_fingerprint": originating_receipt_fingerprint,
        "change_file_fingerprint": change_file_fingerprint,
        "turns": turns,
    }
    draft = FolderPlannerReplay.model_construct(
        **values,
        replay_fingerprint="0" * 64,
    )
    return FolderPlannerReplay(
        **values,
        replay_fingerprint=canonical_sha256(replay_core_payload(draft)),
    )


def load_folder_planner_replay(
    value: bytes | bytearray | FolderPlannerReplay,
) -> FolderPlannerReplay:
    """Strictly parse one canonical replay and reject byte-level drift."""

    if isinstance(value, FolderPlannerReplay):
        return value
    payload = bytes(value)
    try:
        strict_json_object(payload)
        replay = FolderPlannerReplay.model_validate_json(payload, strict=True)
    except (OSError, TypeError, ValueError) as exc:
        raise PlannerReplayError("Recorded GPT-5.6 planning run is invalid.") from exc
    if canonical_json_bytes(replay) != payload:
        raise PlannerReplayError("Recorded GPT-5.6 planning run is not canonical JSON.")
    return replay


def write_folder_planner_replay(path: Path, replay: FolderPlannerReplay) -> None:
    """Promote one immutable canonical replay without replacing another record."""

    payload = canonical_json_bytes(replay)
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.path.lexists(path):
        if path.is_file() and path.read_bytes() == payload:
            return
        raise PlannerReplayError("A different planner replay already exists.")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        os.link(temporary, path, follow_symlinks=False)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    except OSError as exc:
        raise PlannerReplayError(
            "Recorded GPT-5.6 planning run could not be promoted."
        ) from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        with suppress(FileNotFoundError):
            temporary.unlink()


class RecordedPlannerProvider:
    """Keyless provider that replays one exact successful GPT-5.6 tool sequence."""

    provider_kind: Literal["recorded_replay"] = "recorded_replay"

    def __init__(self, replay: bytes | bytearray | FolderPlannerReplay) -> None:
        self.replay = load_folder_planner_replay(replay)
        self._invocation_count = 0

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        """Replay makes no provider request and therefore reports no live usage."""

        return ()

    @property
    def consumed_count(self) -> int:
        return self._invocation_count

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> ProviderToolResponse:
        turn_index = turn_input.response_turn - 1
        if turn_index >= len(self.replay.turns):
            raise ScriptedProviderExhaustedError(
                "Recorded planner has no remaining response turn."
            )
        recorded = self.replay.turns[turn_index]
        if (
            turn_input.response_turn != recorded.response_turn
            or turn_input.source_commitment != self.replay.source_commitment
            or turn_input.request != self.replay.request
            or turn_input.request_fingerprint != self.replay.request_fingerprint
            or replay_turn_input_fingerprint(turn_input)
            != recorded.input_binding_fingerprint
        ):
            raise PlannerProviderResponseError(
                "Recorded GPT-5.6 planning run does not match this exact fixture."
            )
        self._invocation_count += 1
        response = recorded.response
        return ProviderToolResponse(
            provider_kind="recorded_replay",
            returned_model=response.returned_model,
            observable_output_items=response.observable_output_items,
            tool_calls=response.tool_calls,
        )


def _provider_response_from_turn(
    turn: PlannerObservableTurn,
) -> ProviderToolResponse:
    if turn.provider_kind != "live" or turn.blocker_code is not None:
        raise ValueError("A successful replay can contain only live tool responses.")
    return ProviderToolResponse(
        provider_kind="live",
        returned_model=turn.returned_model,
        observable_output_items=turn.observable_output_items,
        tool_calls=turn.tool_calls,
    )
