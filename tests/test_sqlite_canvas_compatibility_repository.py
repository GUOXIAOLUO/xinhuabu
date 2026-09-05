import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from workbench.domain.project.models import ProjectRecord
from workbench.repositories.canvas_repository import CanvasDeletedError, CanvasNotFoundError, StaleCanvasRevisionError
from workbench.repositories.sqlite_canvas_compatibility_repository import SqliteCanvasCompatibilityRepository
from workbench.repositories.sqlite_project_canvas_repository import DEFAULT_PROJECT_ID, LOCAL_WORKSPACE_ACTOR_ID, SqliteProjectCanvasRepository


class SqliteCanvasCompatibilityRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.clock = datetime(2026, 9, 5, tzinfo=UTC)
        canonical = SqliteProjectCanvasRepository(Path(self.temp.name) / "workbench.sqlite3", clock=lambda: self.clock)
        canonical.create_project(ProjectRecord(id=DEFAULT_PROJECT_ID, name="Default", workspace_id="local", created_by=LOCAL_WORKSPACE_ACTOR_ID, created_at=self.clock, updated_at=self.clock))
        self.canonical = canonical
        self.repository = SqliteCanvasCompatibilityRepository(canonical, actor_id=LOCAL_WORKSPACE_ACTOR_ID, clock_ms=lambda: 500)

    def tearDown(self):
        self.temp.cleanup()

    def canvas(self, **extra):
        payload = {"id": "canvas-1", "project": "default", "title": "Fixture", "nodes": [], "connections": [], "updated_at": 500, "future": {"kept": True}}
        payload.update(extra)
        return payload

    def test_round_trips_losslessly_through_canonical_revisioned_storage(self):
        canvas = self.canvas()
        self.repository.save(canvas)
        self.assertEqual(canvas["updated_at"], 500)
        self.assertEqual(self.repository.load("canvas-1")["future"], {"kept": True})
        self.assertEqual(self.canonical.load_canvas_record("canvas-1").revision, 1)
        canvas["title"] = "Updated"
        self.repository.save(canvas)
        self.assertEqual((canvas["updated_at"], self.canonical.load_canvas_record("canvas-1").revision), (501, 2))

    def test_legacy_stale_check_and_soft_delete_semantics_are_preserved(self):
        self.repository.save(self.canvas())
        stale = self.canvas(title="Stale")
        with self.assertRaises(StaleCanvasRevisionError):
            self.repository.save_if_current(stale, expected_updated_at=499)
        deleted = self.repository.load("canvas-1")
        deleted["deleted_at"] = 1
        self.repository.save(deleted)
        with self.assertRaises(CanvasDeletedError):
            self.repository.load("canvas-1")
        self.assertEqual(self.repository.load("canvas-1", include_deleted=True)["id"], "canvas-1")

    def test_purge_is_idempotent_and_audited(self):
        self.repository.save(self.canvas())
        self.assertTrue(self.repository.purge("canvas-1"))
        self.assertFalse(self.repository.purge("canvas-1"))
        with self.assertRaises(CanvasNotFoundError):
            self.repository.load("canvas-1")
        self.assertEqual([event["event_type"] for event in self.canonical.outbox_events()], ["canvas.created", "canvas.purged"])

    def test_metadata_save_keeps_legacy_timestamp_but_advances_canonical_revision(self):
        self.repository.save(self.canvas())
        canvas = self.repository.load("canvas-1")
        canvas["pinned"] = True
        self.repository.save_metadata(canvas)
        self.assertEqual(self.repository.load("canvas-1")["updated_at"], 500)
        self.assertEqual(self.canonical.load_canvas_record("canvas-1").revision, 2)

    def test_project_reassignment_is_canonical_and_preserves_legacy_timestamp(self):
        other = ProjectRecord(id="other", name="Other", workspace_id="local", created_by=LOCAL_WORKSPACE_ACTOR_ID, created_at=self.clock, updated_at=self.clock)
        self.canonical.create_project(other)
        self.repository.save(self.canvas(project="other"))
        self.assertEqual(self.repository.reassign_project(source_project_id="other", target_project_id="default"), 1)
        self.assertEqual(self.repository.load("canvas-1")["project"], "default")
        self.assertEqual(self.repository.load("canvas-1")["updated_at"], 500)
