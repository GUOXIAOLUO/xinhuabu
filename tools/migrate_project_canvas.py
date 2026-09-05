#!/usr/bin/env python3
"""Produce an R3 Project/Canvas migration report without changing Legacy routes.

This tool is intentionally explicit: callers must supply source paths and an
output SQLite path.  It defaults to backfill-and-compare only; ``--activate``
performs the controlled authority-state switch only when every source Canvas
was imported and compares cleanly.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Direct script execution puts ``tools/`` rather than the repository root on
# sys.path. Keep the operational entry point independent of shell PYTHONPATH.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from workbench.application.project_canvas_migration import ProjectCanvasMigrationService
from workbench.repositories.sqlite_project_canvas_repository import SqliteProjectCanvasRepository


REPORT_SCHEMA_VERSION = "workbench.project-canvas-migration-report/1"


def _read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def _read_projects(path: Path) -> list[dict[str, Any]]:
    payload = _read_json(path)
    projects = payload.get("projects", []) if isinstance(payload, dict) else payload
    if not isinstance(projects, list) or not all(isinstance(project, dict) for project in projects):
        raise ValueError("projects input must be a JSON list or an object with a projects list")
    return projects


def _read_canvases(directory: Path) -> list[dict[str, Any]]:
    if not directory.is_dir():
        raise ValueError(f"canvas directory does not exist: {directory}")
    canvases: list[dict[str, Any]] = []
    for path in sorted(directory.glob("*.json")):
        payload = _read_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"canvas JSON must be an object: {path}")
        canvases.append(payload)
    return canvases


def _report(*, repository: SqliteProjectCanvasRepository, import_report, comparisons, activated: bool) -> dict[str, Any]:
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "canvas_authority": repository.canvas_authority(),
        "activated": activated,
        "imported_canvas_ids": list(import_report.imported_canvas_ids),
        "skipped_canvas_ids": list(import_report.skipped_canvas_ids),
        "identity_resolutions": {
            canvas_id: {
                "project_id": resolution.project_id,
                "owner_actor_id": resolution.owner_actor_id,
                "owner_state": resolution.owner_state,
                "issues": list(resolution.issues),
            }
            for canvas_id, resolution in sorted(import_report.identity_resolutions.items())
        },
        "comparisons": [
            {"canvas_id": comparison.canvas_id, "matches": comparison.matches, "differences": list(comparison.differences)}
            for comparison in comparisons
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--projects", required=True, type=Path, help="Legacy projects JSON file")
    parser.add_argument("--canvases-dir", required=True, type=Path, help="Directory containing Legacy Canvas JSON files")
    parser.add_argument("--database", required=True, type=Path, help="SQLite destination (created or updated)")
    parser.add_argument("--report", required=True, type=Path, help="JSON report destination")
    parser.add_argument("--activate", action="store_true", help="Switch SQLite authority only after a clean full comparison")
    args = parser.parse_args()

    repository = SqliteProjectCanvasRepository(args.database)
    service = ProjectCanvasMigrationService(repository)
    legacy_projects = _read_projects(args.projects)
    legacy_canvases = _read_canvases(args.canvases_dir)
    imported, comparisons = service.backfill(legacy_projects, legacy_canvases, now=datetime.now(UTC))
    activated = False
    if args.activate:
        if imported.skipped_canvas_ids:
            raise ValueError("cannot activate canonical authority while source canvases were skipped")
        service.activate_after_compare(legacy_canvases, comparisons)
        activated = True
    report = _report(repository=repository, import_report=imported, comparisons=comparisons, activated=activated)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
