"""Typed fail-closed errors for decision-card providers."""


class DecisionCardProviderError(RuntimeError):
    """Base failure: the proposal must remain unresolved."""


class InvalidEvidencePacketError(DecisionCardProviderError):
    """The outbound evidence packet is ambiguous or internally inconsistent."""


class DecisionCardCapExhaustedError(DecisionCardProviderError):
    """The configured live-call or cost cap prevents another request."""


class BudgetLedgerError(DecisionCardProviderError):
    """The persistent project budget record is unavailable or invalid."""


class DecisionCardOutputError(DecisionCardProviderError):
    """A returned decision card failed the bounded output contract."""


class MalformedDecisionCardError(DecisionCardOutputError):
    """The provider output does not validate as a DecisionCard."""


class UnknownEvidenceIdError(DecisionCardOutputError):
    """A card cites evidence that was not supplied to the provider."""


class UnknownCandidatePathError(DecisionCardOutputError):
    """A card explains a candidate path that was not mechanically supplied."""


class AuthorityClaimError(DecisionCardOutputError):
    """Advisory prose implies approval or deterministic authority."""


class LiveProviderError(DecisionCardProviderError):
    """Base failure for a live GPT-5.6 request."""


class LiveConfigurationError(LiveProviderError):
    """The live provider is missing valid local configuration."""


class LiveTransportError(LiveProviderError):
    """The live request failed before a usable response was returned."""


class LiveResponseStatusError(LiveProviderError):
    """The Responses API returned a non-completed or errored response."""


class LiveRefusalError(LiveProviderError):
    """The Responses API returned a refusal instead of a decision card."""


class LiveParsedOutputMissingError(LiveProviderError):
    """A completed response did not contain parsed structured output."""


class ReplayProviderError(DecisionCardProviderError):
    """Base failure for recorded-response replay."""


class ReplayRecordInvalidError(ReplayProviderError):
    """A replay record is missing, malformed, or not schema-valid."""


class ReplayRecordWriteError(ReplayProviderError):
    """A validated live response could not become the canonical replay record."""


class ReplayModelMismatchError(ReplayProviderError):
    """A replay record was not generated with the required model alias."""


class ReplaySchemaMismatchError(ReplayProviderError):
    """A replay record targets a different DecisionCard schema version."""


class ReplayFingerprintMismatchError(ReplayProviderError):
    """A replay record does not match the complete outbound evidence."""
