"""R3 backfill/compare orchestration; intentionally independent of HTTP and UI."""

from dataclasses import dataclass
from typing import Any

from workbench.repositories.sqlite_project_canvas_repository import (
    CanonicalNotFoundError,
    DEFAULT_PROJECT_ID,
    LOCAL_WORKSPACE_ACTOR_ID,
    LegacyIdentityMapper,
    LegacyImportReport,
    SqliteProjectCanvasRepository,
)
from workbench.domain.project.models import ProjectRecord


@dataclass(frozen=True)
class CanvasMigrationComparison:
    canvas_id: str
    matches: bool
    differences: tuple[str, ...]


class ProjectCanvasMigrationService:
    """Backfills then compares before any authority-state change is permitted."""

    def __init__(self, repository: SqliteProjectCanvasRepository):
        self._repository = repository

    def backfill(self, legacy_projects: list[dict[str, Any]], legacy_canvases: list[dict[str, Any]], *, now) -> tuple[LegacyImportReport, tuple[CanvasMigrationComparison, ...]]:
        project_ids = {str(project.get("id") or "").strip() for project in legacy_projects if str(project.get("id") or "").strip()}
        project_ids.add(DEFAULT_PROJECT_ID)
        for project_id in sorted(project_ids):
            try:
                self._repository.load_project(project_id)
            except CanonicalNotFoundError:
                source = next((item for item in legacy_projects if item.get("id") == project_id), {})
                record = ProjectRecord(
                    id=project_id, name=str(source.get("name") or ("默认项目" if project_id == DEFAULT_PROJECT_ID else project_id)),
                    workspace_id="local", created_by=LOCAL_WORKSPACE_ACTOR_ID,
                    created_at=now, updated_at=now,
                    metadata={"legacy": {"project_order": source.get("order")}},
                )
                self._repository.create_project(record)
        report = self._repository.import_legacy_canvases(legacy_canvases, LegacyIdentityMapper(project_ids))
        comparisons = tuple(
            CanvasMigrationComparison(str(canvas.get("id") or ""), *self._repository.compare_legacy_payload(canvas))
            for canvas in legacy_canvases
            if str(canvas.get("id") or "") in report.imported_canvas_ids
        )
        return report, comparisons

    def activate_after_compare(self, legacy_canvases: list[dict[str, Any]], comparisons: tuple[CanvasMigrationComparison, ...]) -> None:
        if any(not comparison.matches for comparison in comparisons):
            raise ValueError("cannot activate canonical authority while comparisons differ")
        self._repository.activate_sqlite_authority(legacy_canvases)
