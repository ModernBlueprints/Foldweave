"""Trusted direct-provider composition for Foldweave native review jobs."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from name_atlas.decision_cards.budget import PersistentBudgetLedger
from name_atlas.folder_refactor.connected_change.job_v3 import (
    FolderRefactorJobV3Store,
    GptDerivativeJobAuthorityV3,
    GptPlannedJobAuthorityV3,
)
from name_atlas.folder_refactor.foldweave_planning_contracts import (
    FolderPlanRevisionProvider,
)
from name_atlas.folder_refactor.live_planner_provider import (
    FOLDWEAVE_PLANNER_PROMPT_PROFILE,
    LiveFolderPlannerProvider,
    LiveFolderPlanRevisionProvider,
)
from name_atlas.folder_refactor.planner_provider import PlannerProvider
from name_atlas.folder_refactor.receipt_contracts import FolderPlannerUsage
from name_atlas.foldweave_paths import FoldweaveBudgetAuthority
from name_atlas.native_settings import CredentialStore, DirectEndpointProfile


class FoldweavePlanningProviderFactory(Protocol):
    """Create only providers bound to the current durable job prefix."""

    provider_kind: str

    def initial_provider(self) -> PlannerProvider:
        """Return the exact initial planning provider for this job."""
        ...

    def revision_provider(self) -> FolderPlanRevisionProvider:
        """Return the exact sparse-revision provider for this job."""
        ...

    def derivative_revision_provider(
        self,
        job_path: Path,
    ) -> FolderPlanRevisionProvider:
        """Return a provider bound to one derivative child usage prefix."""
        ...


@dataclass(frozen=True, slots=True)
class FoldweaveDirectProviderFactory:
    """Read secrets only inside trusted Python and share the sole ledger."""

    provider_kind = "live"

    job_path: Path
    credential_store: CredentialStore
    endpoint: DirectEndpointProfile
    budget_authority: FoldweaveBudgetAuthority

    def __post_init__(self) -> None:
        if not self.job_path.is_absolute():
            raise ValueError("Foldweave provider job path must be absolute.")
        if self.endpoint.profile_kind != "openai_official":
            raise ValueError(
                "Exact GPT-5.6 qualification requires the official OpenAI endpoint."
            )

    def initial_provider(self) -> PlannerProvider:
        """Create one no-retry GPT-5.6 provider over the persisted usage prefix."""

        budget = self._budget()
        existing_usage = self._existing_usage()
        api_key = self.credential_store.read()
        return LiveFolderPlannerProvider.from_api_key(
            api_key,
            budget=budget,
            existing_usage=existing_usage,
            prompt_profile=FOLDWEAVE_PLANNER_PROMPT_PROFILE,
            base_url=self.endpoint.endpoint,
        )

    def revision_provider(self) -> FolderPlanRevisionProvider:
        """Create one no-retry sparse provider over the same usage authority."""

        budget = self._budget()
        existing_usage = self._existing_usage(require_composite=True)
        api_key = self.credential_store.read()
        return LiveFolderPlanRevisionProvider.from_api_key(
            api_key,
            budget=budget,
            existing_usage=existing_usage,
            base_url=self.endpoint.endpoint,
        )

    def derivative_revision_provider(
        self,
        job_path: Path,
    ) -> FolderPlanRevisionProvider:
        """Create one provider for a schema-distinct derivative child turn."""

        child_factory = FoldweaveDirectProviderFactory(
            job_path=job_path.expanduser().resolve(strict=False),
            credential_store=self.credential_store,
            endpoint=self.endpoint,
            budget_authority=self.budget_authority,
        )
        budget = child_factory._budget()
        existing_usage = child_factory._derivative_usage()
        api_key = child_factory.credential_store.read()
        return LiveFolderPlanRevisionProvider.from_api_key(
            api_key,
            budget=budget,
            existing_usage=existing_usage,
            base_url=child_factory.endpoint.endpoint,
        )

    def _budget(self) -> PersistentBudgetLedger:
        if self.budget_authority.kind == "qualification_existing":
            return PersistentBudgetLedger.open_existing_foldweave_planner(
                path=self.budget_authority.path
            )
        return PersistentBudgetLedger.open_foldweave_installation(
            path=self.budget_authority.path
        )

    def _existing_usage(
        self,
        *,
        require_composite: bool = False,
    ) -> tuple[FolderPlannerUsage, ...]:
        if not os.path.lexists(self.job_path):
            if require_composite:
                raise RuntimeError(
                    "A reviewed Foldweave job is required before revision."
                )
            return ()
        job = FolderRefactorJobV3Store(self.job_path).inspect()
        if not isinstance(job.authority, GptPlannedJobAuthorityV3):
            raise RuntimeError(
                "The durable job is not bound to Foldweave GPT planning."
            )
        if job.authority.evidence_ledger is not None:
            return job.authority.evidence_ledger.usage
        if require_composite:
            raise RuntimeError(
                "The durable job has no accepted planning evidence to revise."
            )
        return job.authority.planner_checkpoint.usage

    def _derivative_usage(self) -> tuple[FolderPlannerUsage, ...]:
        if not os.path.lexists(self.job_path):
            return ()
        job = FolderRefactorJobV3Store(self.job_path).inspect()
        authority = job.authority
        if not isinstance(authority, GptDerivativeJobAuthorityV3):
            raise RuntimeError("The durable job is not a Foldweave derivative child.")
        if authority.evidence_ledger is None:
            return ()
        return authority.evidence_ledger.usage
