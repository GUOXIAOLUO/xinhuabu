import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ProjectCanvasMigrationToolTests(unittest.TestCase):
    def test_defaults_to_compare_report_and_requires_explicit_activation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            projects = root / "projects.json"
            canvases = root / "canvases"
            canvases.mkdir()
            database = root / "workbench.sqlite3"
            report = root / "report.json"
            projects.write_text(json.dumps({"projects": [{"id": "default", "name": "Default"}]}), encoding="utf-8")
            canvas = {
                "id": "canvas-1", "project": "default", "owner": "", "title": "Legacy",
                "kind": "classic", "nodes": [], "connections": [], "viewport": {"x": 0, "y": 0, "scale": 1},
                "unknown_future_field": {"preserve": True},
            }
            (canvases / "canvas-1.json").write_text(json.dumps(canvas), encoding="utf-8")
            command = [
                sys.executable, "tools/migrate_project_canvas.py", "--projects", str(projects),
                "--canvases-dir", str(canvases), "--database", str(database), "--report", str(report),
            ]
            subprocess.run(command, check=True, cwd=Path(__file__).resolve().parents[1])

            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["schema_version"], "workbench.project-canvas-migration-report/1")
            self.assertEqual(payload["canvas_authority"], "legacy_json")
            self.assertFalse(payload["activated"])
            self.assertEqual(payload["imported_canvas_ids"], ["canvas-1"])
            self.assertEqual(payload["comparisons"], [{"canvas_id": "canvas-1", "matches": True, "differences": []}])

            subprocess.run([*command, "--activate"], check=True, cwd=Path(__file__).resolve().parents[1])
            activated = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(activated["canvas_authority"], "sqlite")
            self.assertTrue(activated["activated"])
