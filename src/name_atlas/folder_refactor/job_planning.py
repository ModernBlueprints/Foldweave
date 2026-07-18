"""Persist every folder-planner checkpoint through the sole job authority."""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import ValidationError

from name_atlas.folder_refactor.job import (
    FolderJobLifecycle,
    FolderJobRevisionError,
    FolderRefactorJob,
    FolderRefactorJobWriter,
)
from name_atlas.folder_refactor.planner_contracts import FolderPlannerProgress


@dataclass(slots=True)
class JobPlannerCheckpoint:
    """Callable adapter from planner progress to revisioned durable job state."""

    writer: FolderRefactorJobWriter
    latest_job: FolderRefactorJob | None = field(default=None, init=False)

    def __call__(self, progress: FolderPlannerProgress) -> None:
        """Rescan, bind, and atomically persist one exact planner transition."""

        self._save(self.writer, progress)

    def _save(
        self,
        writer: FolderRefactorJobWriter,
        progress: FolderPlannerProgress,
    ) -> None:
        lifecycle = _lifecycle_for(progress)
        current = writer.load()
        payload = current.model_dump(mode="python")
        payload.update(
            {
                "accepted_plan": progress.accepted_plan,
                "blocker_code": (
                    progress.blocker_code if progress.status == "blocked" else None
                ),
                "blocker_message": (
                    f"Planner blocked: {progress.blocker_code}."
                    if progress.status == "blocked"
                    else None
                ),
                "lifecycle": lifecycle,
                "planner_progress": progress,
            }
        )
        try:
            candidate = FolderRefactorJob.model_validate(payload, strict=True)
        except ValidationError as exc:
            raise FolderJobRevisionError(
                "Planner checkpoint does not satisfy the durable job contract."
            ) from exc
        self.latest_job = writer.save(
            candidate,
            expected_revision=current.revision,
        )


def _lifecycle_for(progress: FolderPlannerProgress) -> FolderJobLifecycle:
    mapping = {
        "planning": FolderJobLifecycle.PLANNING,
        "awaiting_clarification": FolderJobLifecycle.AWAITING_CLARIFICATION,
        "accepted": FolderJobLifecycle.EXECUTING,
        "blocked": FolderJobLifecycle.BLOCKED,
    }
    return mapping[progress.status]
