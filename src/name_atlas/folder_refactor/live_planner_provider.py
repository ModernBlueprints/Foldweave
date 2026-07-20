"""Bounded live GPT-5.6 Responses provider for connected-folder planning."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import ROUND_CEILING, Decimal
from time import perf_counter
from typing import Any, Literal, Protocol
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from name_atlas.decision_cards.budget import PersistentBudgetLedger
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderDerivativeRevisionTurnInputV1,
    FolderPlannerRevisionTurnInputV1,
    FolderPlanRevisionV1,
    FolderRevisionProviderResponseV1,
    canonical_derivative_turn_input_bytes,
    canonical_revision_turn_input_bytes,
)
from name_atlas.folder_refactor.foldweave_revision_prompt import (
    FOLDWEAVE_REVISION_INSTRUCTIONS,
    FOLDWEAVE_REVISION_RESPONSE_TOOLS,
    SubmitPlanRevisionArguments,
)
from name_atlas.folder_refactor.live_planner_policy import (
    DEFAULT_LIVE_PLANNER_POLICY,
    DEFAULT_LIVE_REVISION_POLICY,
    LivePlannerPolicy,
)
from name_atlas.folder_refactor.planner_contracts import (
    FolderPlannerTurnInput,
    InspectMarkdownLinksCall,
    ListInventoryPageCall,
    PlannerToolCall,
    ProviderBlockedResponse,
    ProviderToolResponse,
    ReadTextExcerptCall,
    RequestClarificationCall,
    SubmitPlanCall,
)
from name_atlas.folder_refactor.planner_prompt import (
    FOLDWEAVE_PLANNER_INSTRUCTIONS,
    PLANNER_ARGUMENT_MODELS,
    PLANNER_INSTRUCTIONS,
    PLANNER_RESPONSE_TOOLS,
    InspectMarkdownLinksArguments,
    ListInventoryPageArguments,
    ReadTextExcerptArguments,
    RequestClarificationArguments,
    SubmitPlanArguments,
)
from name_atlas.folder_refactor.planner_provider import (
    PlannerProviderResponseError,
    PlannerProviderTimeoutError,
    PlannerProviderTransportError,
)
from name_atlas.folder_refactor.portable_artifacts import strict_json_object
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.folder_refactor.serialization import canonical_json_bytes

oslo_tz = ZoneInfo("Europe/Oslo")

STANDARD_INPUT_USD_PER_MILLION = Decimal("5")
STANDARD_CACHED_INPUT_USD_PER_MILLION = Decimal("0.5")
STANDARD_OUTPUT_USD_PER_MILLION = Decimal("30")
RESERVATION_INPUT_TOKEN_OVERHEAD = 4_096


class _ResponsesResource(Protocol):
    async def create(self, **kwargs: Any) -> object:
        """Create one Responses API result."""


class _ResponsesClient(Protocol):
    responses: _ResponsesResource


@dataclass(frozen=True, slots=True)
class LivePlannerPromptProfile:
    """Exact prompt and tool set used for one initial planning surface."""

    instructions: str
    tools: tuple[dict[str, Any], ...]


LEGACY_PLANNER_PROMPT_PROFILE = LivePlannerPromptProfile(
    instructions=PLANNER_INSTRUCTIONS,
    tools=PLANNER_RESPONSE_TOOLS,
)
FOLDWEAVE_PLANNER_PROMPT_PROFILE = LivePlannerPromptProfile(
    instructions=FOLDWEAVE_PLANNER_INSTRUCTIONS,
    tools=PLANNER_RESPONSE_TOOLS,
)


def _strict_async_openai_client(
    *,
    api_key: str,
    base_url: str,
    timeout_seconds: float,
    max_retries: int,
) -> _ResponsesClient:
    """Build one TLS-validating client that never follows an HTTP redirect."""

    from openai import AsyncOpenAI, DefaultAsyncHttpxClient

    http_client = DefaultAsyncHttpxClient(
        timeout=timeout_seconds,
        follow_redirects=False,
    )
    return AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout_seconds,
        max_retries=max_retries,
        http_client=http_client,
    )


class LiveFolderPlannerProvider:
    """Exchange one fully bound turn for strict, sanitized function calls."""

    provider_kind: Literal["live"] = "live"

    def __init__(
        self,
        client: _ResponsesClient,
        *,
        budget: PersistentBudgetLedger,
        policy: LivePlannerPolicy = DEFAULT_LIVE_PLANNER_POLICY,
        existing_usage: tuple[FolderPlannerUsage, ...] = (),
        prompt_profile: LivePlannerPromptProfile = LEGACY_PLANNER_PROMPT_PROFILE,
    ) -> None:
        expected_turns = tuple(range(1, len(existing_usage) + 1))
        if tuple(item.response_turn for item in existing_usage) != expected_turns:
            raise ValueError("Existing live usage must be one contiguous prefix.")
        self._client = client
        self._budget = budget
        self.policy = policy
        self._prompt_profile = prompt_profile
        self._usage = list(existing_usage)

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        *,
        budget: PersistentBudgetLedger,
        policy: LivePlannerPolicy = DEFAULT_LIVE_PLANNER_POLICY,
        existing_usage: tuple[FolderPlannerUsage, ...] = (),
        prompt_profile: LivePlannerPromptProfile = LEGACY_PLANNER_PROMPT_PROFILE,
        base_url: str = "https://api.openai.com/v1",
    ) -> LiveFolderPlannerProvider:
        """Create the exact no-retry SDK client without exposing the key."""

        if not api_key.strip():
            raise PlannerProviderResponseError(
                "Configure OPENAI_API_KEY locally before live GPT-5.6 planning."
            )
        client = _strict_async_openai_client(
            api_key=api_key,
            base_url=base_url,
            timeout_seconds=policy.timeout_seconds,
            max_retries=policy.sdk_max_retries,
        )
        return cls(
            client,
            budget=budget,
            policy=policy,
            existing_usage=existing_usage,
            prompt_profile=prompt_profile,
        )

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        """Return the append-only observable usage prefix."""

        return tuple(self._usage)

    async def exchange(
        self,
        turn_input: FolderPlannerTurnInput,
        /,
    ) -> ProviderToolResponse | ProviderBlockedResponse:
        """Reserve once, call once, sanitize once, and never retry."""

        if turn_input.provider_kind != "live":
            raise PlannerProviderResponseError(
                "Live provider received a non-live planner turn."
            )
        if turn_input.response_turn != len(self._usage) + 1:
            raise PlannerProviderResponseError(
                "Live usage prefix does not match the persisted response turn."
            )
        request = _responses_request(
            turn_input,
            policy=self.policy,
            prompt_profile=self._prompt_profile,
        )
        reservation_microusd = _reservation_microusd(
            request,
            policy=self.policy,
        )
        try:
            self._budget.reserve_microusd(
                reservation_microusd=reservation_microusd,
                provider_attempts=1,
            )
        except Exception as exc:
            raise PlannerProviderResponseError(
                "The cumulative GPT-5.6 budget cannot reserve this turn."
            ) from exc

        started = perf_counter()
        try:
            response = await self._client.responses.create(
                **request,
                timeout=self.policy.timeout_seconds,
            )
        except Exception as exc:
            if isinstance(exc, TimeoutError) or "timeout" in type(exc).__name__.lower():
                raise PlannerProviderTimeoutError(
                    "The GPT-5.6 planner request timed out without a retry."
                ) from exc
            raise PlannerProviderTransportError(
                "The GPT-5.6 planner request failed without a retry."
            ) from exc

        latency_ms = (perf_counter() - started) * 1_000
        usage = _usage_from_response(
            response,
            response_turn=turn_input.response_turn,
            latency_ms=latency_ms,
        )
        if usage is not None:
            try:
                self._budget.record_reported_cost_microusd(
                    usage.estimated_cost_microusd
                )
            except Exception as exc:
                raise PlannerProviderResponseError(
                    "The cumulative GPT-5.6 usage record could not be committed."
                ) from exc
            self._usage.append(usage)

        returned_model = _bounded_text(getattr(response, "model", None), 200)
        observable = _sanitize_output_items(getattr(response, "output", None))
        if getattr(response, "error", None) is not None:
            return _observed_blocker(
                returned_model=returned_model,
                observable=observable,
                blocker_code="provider_response_error",
                message="GPT-5.6 returned a provider error.",
            )
        if getattr(response, "status", None) != "completed":
            return _observed_blocker(
                returned_model=returned_model,
                observable=observable,
                blocker_code="provider_turn_incomplete",
                message="GPT-5.6 did not complete the planner turn.",
            )
        if usage is None:
            return _observed_blocker(
                returned_model=returned_model,
                observable=observable,
                blocker_code="provider_usage_missing",
                message="GPT-5.6 returned no complete usage record.",
            )
        if _has_refusal(getattr(response, "output", None)):
            return _observed_blocker(
                returned_model=returned_model,
                observable=observable,
                blocker_code="provider_refusal",
                message="GPT-5.6 refused the bounded planner request.",
            )
        try:
            calls = _parse_tool_calls(getattr(response, "output", None))
            return ProviderToolResponse(
                provider_kind="live",
                returned_model=returned_model,
                observable_output_items=observable,
                tool_calls=calls,
            )
        except (TypeError, ValueError, ValidationError):
            return _observed_blocker(
                returned_model=returned_model,
                observable=observable,
                blocker_code="provider_response_invalid",
                message="GPT-5.6 returned invalid planner tool arguments.",
            )


class LiveFolderPlanRevisionProvider:
    """Exchange one exact sparse Foldweave revision with no retry."""

    provider_kind: Literal["live"] = "live"

    def __init__(
        self,
        client: _ResponsesClient,
        *,
        budget: PersistentBudgetLedger,
        policy: LivePlannerPolicy = DEFAULT_LIVE_REVISION_POLICY,
        existing_usage: tuple[FolderPlannerUsage, ...] = (),
    ) -> None:
        expected_turns = tuple(range(1, len(existing_usage) + 1))
        if tuple(item.response_turn for item in existing_usage) != expected_turns:
            raise ValueError("Existing revision usage must be one contiguous prefix.")
        self._client = client
        self._budget = budget
        self.policy = policy
        self._usage = list(existing_usage)

    @classmethod
    def from_api_key(
        cls,
        api_key: str,
        *,
        budget: PersistentBudgetLedger,
        policy: LivePlannerPolicy = DEFAULT_LIVE_REVISION_POLICY,
        existing_usage: tuple[FolderPlannerUsage, ...] = (),
        base_url: str = "https://api.openai.com/v1",
    ) -> LiveFolderPlanRevisionProvider:
        """Create the exact no-retry revision client without exposing the key."""

        if not api_key.strip():
            raise PlannerProviderResponseError(
                "Configure an OpenAI API key locally before live Foldweave revision."
            )
        client = _strict_async_openai_client(
            api_key=api_key,
            base_url=base_url,
            timeout_seconds=policy.timeout_seconds,
            max_retries=policy.sdk_max_retries,
        )
        return cls(
            client,
            budget=budget,
            policy=policy,
            existing_usage=existing_usage,
        )

    @property
    def usage(self) -> tuple[FolderPlannerUsage, ...]:
        return tuple(self._usage)

    async def exchange(
        self,
        turn_input: FolderPlannerRevisionTurnInputV1
        | FolderDerivativeRevisionTurnInputV1,
        /,
    ) -> FolderRevisionProviderResponseV1:
        """Reserve, call, sanitize, and parse exactly one sparse revision."""

        if turn_input.provider_kind != "live":
            raise PlannerProviderResponseError(
                "Live revision provider received a non-live turn."
            )
        if turn_input.turn_contract_freeze_fingerprint is None:
            raise PlannerProviderResponseError(
                "A new live revision requires an exact contract-freeze binding."
            )
        if turn_input.response_turn != len(self._usage) + 1:
            raise PlannerProviderResponseError(
                "Live revision usage prefix does not match the durable turn."
            )
        request = _revision_responses_request(turn_input, policy=self.policy)
        reservation_microusd = _reservation_microusd(request, policy=self.policy)
        try:
            self._budget.reserve_microusd(
                reservation_microusd=reservation_microusd,
                provider_attempts=1,
            )
        except Exception as exc:
            raise PlannerProviderResponseError(
                "The cumulative GPT-5.6 budget cannot reserve this revision turn."
            ) from exc

        started = perf_counter()
        try:
            response = await self._client.responses.create(
                **request,
                timeout=self.policy.timeout_seconds,
            )
        except Exception as exc:
            if isinstance(exc, TimeoutError) or "timeout" in type(exc).__name__.lower():
                raise PlannerProviderTimeoutError(
                    "The GPT-5.6 revision request timed out without a retry."
                ) from exc
            raise PlannerProviderTransportError(
                "The GPT-5.6 revision request failed without a retry."
            ) from exc

        latency_ms = (perf_counter() - started) * 1_000
        usage = _usage_from_response(
            response,
            response_turn=turn_input.response_turn,
            latency_ms=latency_ms,
        )
        if usage is None:
            raise PlannerProviderResponseError(
                "GPT-5.6 returned no complete revision usage record."
            )
        try:
            self._budget.record_reported_cost_microusd(usage.estimated_cost_microusd)
        except Exception as exc:
            raise PlannerProviderResponseError(
                "The cumulative GPT-5.6 revision usage could not be committed."
            ) from exc
        self._usage.append(usage)

        returned_model = _bounded_text(getattr(response, "model", None), 200)
        observable = _sanitize_output_items(getattr(response, "output", None))
        if getattr(response, "error", None) is not None:
            raise PlannerProviderResponseError("GPT-5.6 returned a revision error.")
        if getattr(response, "status", None) != "completed":
            raise PlannerProviderResponseError(
                "GPT-5.6 did not complete the revision turn."
            )
        if _has_refusal(getattr(response, "output", None)):
            raise PlannerProviderResponseError("GPT-5.6 refused the revision turn.")
        call_id, revision = _parse_revision_tool_call(getattr(response, "output", None))
        return FolderRevisionProviderResponseV1(
            provider_kind="live",
            returned_model=returned_model,
            observable_output_items=observable,
            call_id=call_id,
            revision=revision,
        )


def _revision_responses_request(
    turn_input: FolderPlannerRevisionTurnInputV1 | FolderDerivativeRevisionTurnInputV1,
    *,
    policy: LivePlannerPolicy,
) -> dict[str, Any]:
    return {
        "model": "gpt-5.6",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": _canonical_sparse_turn_input_bytes(turn_input).decode(
                            "utf-8"
                        ),
                    }
                ],
            }
        ],
        "instructions": FOLDWEAVE_REVISION_INSTRUCTIONS,
        "tools": list(FOLDWEAVE_REVISION_RESPONSE_TOOLS),
        "tool_choice": {
            "type": "function",
            "name": "submit_plan_revision",
        },
        "parallel_tool_calls": False,
        "max_tool_calls": 1,
        "max_output_tokens": policy.max_output_tokens,
        "reasoning": {"effort": policy.reasoning_effort},
        "store": False,
    }


def _canonical_sparse_turn_input_bytes(
    turn_input: FolderPlannerRevisionTurnInputV1 | FolderDerivativeRevisionTurnInputV1,
) -> bytes:
    """Preserve the schema-distinct root or derivative provider input."""

    if isinstance(turn_input, FolderDerivativeRevisionTurnInputV1):
        return canonical_derivative_turn_input_bytes(turn_input)
    return canonical_revision_turn_input_bytes(turn_input)


def _parse_revision_tool_call(output: object) -> tuple[str, FolderPlanRevisionV1]:
    if not isinstance(output, list):
        raise PlannerProviderResponseError("Revision output must be a list.")
    calls = [item for item in output if getattr(item, "type", None) == "function_call"]
    non_reasoning = [
        item
        for item in output
        if getattr(item, "type", None) not in {"reasoning", "function_call"}
    ]
    if len(calls) != 1 or non_reasoning:
        raise PlannerProviderResponseError(
            "Revision output must contain exactly one declared function call."
        )
    call = calls[0]
    if getattr(call, "name", None) != "submit_plan_revision":
        raise PlannerProviderResponseError("Revision function call is unsupported.")
    call_id = _bounded_text(getattr(call, "call_id", None), 128)
    arguments = getattr(call, "arguments", None)
    if not isinstance(arguments, str):
        raise PlannerProviderResponseError("Revision arguments are malformed.")
    try:
        argument_bytes = arguments.encode("utf-8", errors="strict")
        strict_json_object(argument_bytes)
        parsed = SubmitPlanRevisionArguments.model_validate_json(
            argument_bytes,
            strict=True,
        )
    except (UnicodeError, ValueError, ValidationError) as exc:
        raise PlannerProviderResponseError(
            "Revision arguments violate the strict schema."
        ) from exc
    return call_id, parsed.revision


def _responses_request(
    turn_input: FolderPlannerTurnInput,
    *,
    policy: LivePlannerPolicy,
    prompt_profile: LivePlannerPromptProfile = LEGACY_PLANNER_PROMPT_PROFILE,
) -> dict[str, Any]:
    turn_json = canonical_json_bytes(turn_input).decode("utf-8")
    return {
        "model": "gpt-5.6",
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": turn_json}],
            }
        ],
        "instructions": prompt_profile.instructions,
        "tools": list(prompt_profile.tools),
        "tool_choice": "required",
        "parallel_tool_calls": True,
        "max_tool_calls": 24,
        "max_output_tokens": policy.max_output_tokens,
        "reasoning": {"effort": policy.reasoning_effort},
        "store": False,
    }


def _reservation_microusd(
    request: dict[str, Any],
    *,
    policy: LivePlannerPolicy,
) -> int:
    input_token_ceiling = (
        len(canonical_json_bytes(request)) + RESERVATION_INPUT_TOKEN_OVERHEAD
    )
    microdollars = (
        Decimal(input_token_ceiling) * STANDARD_INPUT_USD_PER_MILLION
        + Decimal(policy.max_output_tokens) * STANDARD_OUTPUT_USD_PER_MILLION
    )
    return int(microdollars.to_integral_value(rounding=ROUND_CEILING))


def _reported_cost_microusd(
    *,
    input_tokens: int,
    cached_input_tokens: int,
    output_tokens: int,
) -> int:
    uncached = input_tokens - cached_input_tokens
    value = (
        Decimal(uncached) * STANDARD_INPUT_USD_PER_MILLION
        + Decimal(cached_input_tokens) * STANDARD_CACHED_INPUT_USD_PER_MILLION
        + Decimal(output_tokens) * STANDARD_OUTPUT_USD_PER_MILLION
    )
    return int(value.to_integral_value(rounding=ROUND_CEILING))


def _usage_from_response(
    response: object,
    *,
    response_turn: int,
    latency_ms: float,
) -> FolderPlannerUsage | None:
    raw = getattr(response, "usage", None)
    if raw is None:
        return None
    input_tokens = getattr(raw, "input_tokens", None)
    output_tokens = getattr(raw, "output_tokens", None)
    total_tokens = getattr(raw, "total_tokens", None)
    input_details = getattr(raw, "input_tokens_details", None)
    output_details = getattr(raw, "output_tokens_details", None)
    cached = getattr(input_details, "cached_tokens", 0) if input_details else 0
    reasoning = (
        getattr(output_details, "reasoning_tokens", None) if output_details else None
    )
    values = (input_tokens, output_tokens, cached)
    if any(type(value) is not int or value < 0 for value in values):
        return None
    if total_tokens is not None and (type(total_tokens) is not int or total_tokens < 0):
        return None
    if reasoning is not None and (type(reasoning) is not int or reasoning < 0):
        return None
    return FolderPlannerUsage(
        response_turn=response_turn,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_input_tokens=cached,
        reasoning_tokens=reasoning,
        total_tokens=total_tokens,
        latency_ms=latency_ms,
        recorded_at=datetime.now(tz=oslo_tz),
        estimated_cost_microusd=_reported_cost_microusd(
            input_tokens=input_tokens,
            cached_input_tokens=cached,
            output_tokens=output_tokens,
        ),
    )


def _parse_tool_calls(output: object) -> tuple[PlannerToolCall, ...]:
    if not isinstance(output, list):
        raise ValueError("Provider output must be a list.")
    parsed: list[PlannerToolCall] = []
    for item in output:
        item_type = getattr(item, "type", None)
        if item_type == "reasoning":
            continue
        if item_type != "function_call":
            raise ValueError("Provider output contains a non-tool item.")
        name = _bounded_text(getattr(item, "name", None), 128)
        call_id = _bounded_text(getattr(item, "call_id", None), 128)
        arguments = getattr(item, "arguments", None)
        if name not in PLANNER_ARGUMENT_MODELS or not isinstance(arguments, str):
            raise ValueError("Provider function call is unknown or malformed.")
        argument_bytes = arguments.encode("utf-8", errors="strict")
        strict_json_object(argument_bytes)
        model = PLANNER_ARGUMENT_MODELS[name]
        args = model.model_validate_json(argument_bytes, strict=True)
        parsed.append(_domain_call(name=name, call_id=call_id, arguments=args))
    if not parsed:
        raise ValueError("Provider output contains no planner tool call.")
    return tuple(parsed)


def _domain_call(
    *,
    name: str,
    call_id: str,
    arguments: object,
) -> PlannerToolCall:
    if isinstance(arguments, ListInventoryPageArguments):
        return ListInventoryPageCall(
            call_id=call_id,
            cursor=arguments.cursor,
            page_size=arguments.page_size,
        )
    if isinstance(arguments, ReadTextExcerptArguments):
        return ReadTextExcerptCall(
            call_id=call_id,
            file_id=arguments.file_id,
            start_byte=arguments.start_byte,
            max_bytes=arguments.max_bytes,
        )
    if isinstance(arguments, InspectMarkdownLinksArguments):
        return InspectMarkdownLinksCall(
            call_id=call_id,
            file_id=arguments.file_id,
            cursor=arguments.cursor,
            page_size=arguments.page_size,
        )
    if isinstance(arguments, SubmitPlanArguments):
        return SubmitPlanCall(call_id=call_id, plan=arguments.plan)
    if isinstance(arguments, RequestClarificationArguments):
        return RequestClarificationCall(
            call_id=call_id,
            reason=arguments.reason,
            question=arguments.question,
            missing_facts=arguments.missing_facts,
            evidence_ids=arguments.evidence_ids,
        )
    raise TypeError(f"Unsupported planner argument model for {name}.")


def _sanitize_output_items(output: object) -> tuple[dict[str, Any], ...]:
    if not isinstance(output, list):
        return ()
    sanitized: list[dict[str, Any]] = []
    for item in output:
        item_type = _bounded_text(getattr(item, "type", None), 64, allow_none=True)
        if item_type == "function_call":
            sanitized.append(
                {
                    "type": "function_call",
                    "name": _bounded_text(
                        getattr(item, "name", None), 128, allow_none=True
                    ),
                    "call_id": _bounded_text(
                        getattr(item, "call_id", None), 128, allow_none=True
                    ),
                    "status": _bounded_text(
                        getattr(item, "status", None), 64, allow_none=True
                    ),
                }
            )
        elif item_type == "reasoning":
            sanitized.append(
                {
                    "type": "reasoning",
                    "status": _bounded_text(
                        getattr(item, "status", None), 64, allow_none=True
                    ),
                }
            )
        else:
            sanitized.append({"type": item_type or "unexpected"})
    return tuple(sanitized)


def _has_refusal(output: object) -> bool:
    if not isinstance(output, list):
        return False
    for item in output:
        content = getattr(item, "content", None)
        if isinstance(content, list) and any(
            getattr(part, "type", None) == "refusal" for part in content
        ):
            return True
    return False


def _observed_blocker(
    *,
    returned_model: str | None,
    observable: tuple[dict[str, Any], ...],
    blocker_code: str,
    message: str,
) -> ProviderBlockedResponse:
    if returned_model is None:
        raise PlannerProviderResponseError(
            "GPT-5.6 response did not identify the returned model."
        )
    return ProviderBlockedResponse(
        provider_kind="live",
        returned_model=returned_model,
        blocker_code=blocker_code,
        message=message,
        observable_output_items=observable,
    )


def _bounded_text(
    value: object,
    maximum: int,
    *,
    allow_none: bool = False,
) -> str | None:
    if value is None and allow_none:
        return None
    if not isinstance(value, str) or not value or len(value) > maximum:
        if allow_none:
            return None
        raise ValueError("Provider text field is missing or outside its bound.")
    return value
