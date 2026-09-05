import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from workbench.application.project_canvas_migration import ProjectCanvasMigrationService
from workbench.repositories.legacy_json_canvas_repository import LegacyJsonCanvasRepository
from workbench.repositories.sqlite_canvas_compatibility_repository import SqliteCanvasCompatibilityRepository


class ProjectCanvasWiringTests(unittest.TestCase):
    def test_main_wires_the_r3_repository_without_replacing_legacy_canvas_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "workbench.sqlite3"
            with patch.object(main, "WORKBENCH_DATABASE_PATH", str(database)):
                canonical = main.canonical_project_canvas_repository()
                migration = main.project_canvas_migration_service()

            self.assertEqual(canonical.canvas_authority(), "legacy_json")
            self.assertTrue(database.exists())
            self.assertIsInstance(migration, ProjectCanvasMigrationService)

    def test_r4_routing_requires_both_feature_flag_and_sqlite_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "workbench.sqlite3"
            with patch.object(main, "WORKBENCH_DATABASE_PATH", str(database)), patch.object(main, "WORKBENCH_CANONICAL_CANVAS_ROUTING_ENABLED", False):
                self.assertIsInstance(main.canvas_repository(), LegacyJsonCanvasRepository)
                self.assertFalse(database.exists())
            with patch.object(main, "WORKBENCH_DATABASE_PATH", str(database)), patch.object(main, "WORKBENCH_CANONICAL_CANVAS_ROUTING_ENABLED", True):
                canonical = main.canonical_project_canvas_repository()
                canonical.activate_sqlite_authority([])
                self.assertIsInstance(main.canvas_repository(), SqliteCanvasCompatibilityRepository)
