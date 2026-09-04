import json
import tempfile
import unittest
from pathlib import Path
from threading import Lock

from workbench.repositories.canvas_repository import CanvasDeletedError, CanvasNotFoundError, StaleCanvasRevisionError
from workbench.repositories.legacy_json_canvas_repository import LegacyJsonCanvasRepository


class LegacyJsonCanvasRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name) / "canvases"
        self.clock = 500
        self.repository = LegacyJsonCanvasRepository(self.directory, clock_ms=lambda: self.clock, lock=Lock())

    def tearDown(self):
        self.temp.cleanup()

    def canvas(self, canvas_id="canvas-1", updated_at=0):
        return {"id": canvas_id, "title": "fixture", "nodes": [], "connections": [], "updated_at": updated_at}

    def test_save_is_monotonic_when_the_clock_does_not_advance(self):
        canvas = self.canvas(updated_at=500)
        self.repository.save(canvas)
        self.assertEqual(canvas["updated_at"], 501)
        self.assertEqual(self.repository.load("canvas-1")["updated_at"], 501)

    def test_load_hides_deleted_records_unless_requested(self):
        canvas = self.canvas()
        canvas["deleted_at"] = 1
        self.repository.save(canvas)
        with self.assertRaises(CanvasDeletedError):
            self.repository.load("canvas-1")
        self.assertEqual(self.repository.load("canvas-1", include_deleted=True)["id"], "canvas-1")

    def test_save_if_current_rejects_stale_write_without_mutation(self):
        self.repository.save(self.canvas(updated_at=500))
        replacement = self.canvas(updated_at=500)
        replacement["title"] = "stale overwrite"
        with self.assertRaises(StaleCanvasRevisionError) as raised:
            self.repository.save_if_current(replacement, expected_updated_at=499)
        self.assertEqual(raised.exception.current["title"], "fixture")
        self.assertEqual(self.repository.load("canvas-1")["title"], "fixture")

    def test_purge_is_idempotent_and_removes_file(self):
        self.repository.save(self.canvas())
        self.assertTrue(self.repository.purge("canvas-1"))
        self.assertFalse(self.repository.purge("canvas-1"))
        with self.assertRaises(CanvasNotFoundError):
            self.repository.load("canvas-1")

    def test_save_preserves_unknown_legacy_fields(self):
        canvas = self.canvas()
        canvas["future_field"] = {"opaque": [1, 2, 3]}
        self.repository.save(canvas)
        raw = json.loads(self.repository.path_for("canvas-1").read_text(encoding="utf-8"))
        self.assertEqual(raw["future_field"], {"opaque": [1, 2, 3]})
