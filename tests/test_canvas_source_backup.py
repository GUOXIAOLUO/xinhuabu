import tempfile
import unittest
from pathlib import Path

from workbench.application.canvas_source_backup import CanvasBackupError, create_canvas_source_backup, validate_canvas_source_backup


class CanvasSourceBackupTests(unittest.TestCase):
    def test_backup_is_complete_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "canvases"
            source.mkdir()
            (source / "one.json").write_text('{"id":"one","unknown":{"kept":true}}', encoding="utf-8")
            (source / "two.json").write_text('{"id":"two"}', encoding="utf-8")
            backup = root / "backup"
            report = create_canvas_source_backup(source, backup)
            self.assertEqual(report.file_count, 2)
            self.assertEqual(validate_canvas_source_backup(backup).manifest_sha256, report.manifest_sha256)
            (backup / "one.json").write_text("changed", encoding="utf-8")
            with self.assertRaises(CanvasBackupError):
                validate_canvas_source_backup(backup)
