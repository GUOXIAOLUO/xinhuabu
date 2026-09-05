import asyncio
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import main
from workbench.domain.project.models import ProjectRecord
from workbench.repositories.sqlite_project_canvas_repository import DEFAULT_PROJECT_ID, LOCAL_WORKSPACE_ACTOR_ID


class CanonicalCanvasRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.database = Path(self.temp.name) / "workbench.sqlite3"
        self.db_patch = patch.object(main, "WORKBENCH_DATABASE_PATH", str(self.database))
        self.flag_patch = patch.object(main, "WORKBENCH_CANONICAL_CANVAS_ROUTING_ENABLED", True)
        self.db_patch.start()
        self.flag_patch.start()
        canonical = main.canonical_project_canvas_repository()
        now = datetime(2026, 9, 5, tzinfo=UTC)
        canonical.create_project(ProjectRecord(id=DEFAULT_PROJECT_ID, name="Default", workspace_id="local", created_by=LOCAL_WORKSPACE_ACTOR_ID, created_at=now, updated_at=now))
        canonical.activate_sqlite_authority([])
        main.canvas_repository().save({"id": "canvas-1", "project": "default", "title": "Before", "icon": "layers", "kind": "classic", "nodes": [], "connections": [], "viewport": {}, "logs": [], "settings": {}, "updated_at": 500})

    def tearDown(self):
        self.flag_patch.stop()
        self.db_patch.stop()
        self.temp.cleanup()

    def test_existing_save_route_updates_canonical_payload_and_preserves_stale_409(self):
        current_updated_at = main.canvas_repository().load("canvas-1")["updated_at"]
        request = main.CanvasSaveRequest(title="After", nodes=[], connections=[], viewport={}, logs=[], settings={}, base_updated_at=current_updated_at)
        response = asyncio.run(main.update_canvas("canvas-1", request))
        self.assertEqual(response["canvas"]["title"], "After")
        self.assertEqual(main.canonical_project_canvas_repository().load_canvas_record("canvas-1").revision, 2)
        stale = main.CanvasSaveRequest(title="Stale", nodes=[], connections=[], viewport={}, logs=[], settings={}, base_updated_at=current_updated_at)
        with self.assertRaises(main.HTTPException) as raised:
            asyncio.run(main.update_canvas("canvas-1", stale))
        self.assertEqual(raised.exception.status_code, 409)
        self.assertEqual(main.canvas_repository().load("canvas-1")["title"], "After")
