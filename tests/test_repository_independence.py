import unittest
from pathlib import Path

import main


ROOT = Path(__file__).resolve().parents[1]


class RepositoryIndependenceTests(unittest.TestCase):
    def test_product_no_longer_exposes_source_repository_update_routes(self):
        paths = {route.path for route in main.app.routes if hasattr(route, "path")}
        self.assertTrue({
            "/api/check-update",
            "/api/update-connectivity",
            "/api/update-connectivity/probe",
            "/api/update-from-github",
            "/api/update-backups",
            "/api/update-rollback",
        }.isdisjoint(paths))

    def test_app_info_contains_local_runtime_information_only(self):
        info = main.app_info()
        self.assertIn("version", info)
        self.assertIn("server", info)
        self.assertNotIn("repo_url", info)
        self.assertNotIn("sources", info)

    def test_home_shell_does_not_offer_or_trigger_the_legacy_self_updater(self):
        source = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
        self.assertNotIn('id="update-now-btn"', source)
        self.assertNotIn('id="project-version-badge"', source)
        self.assertNotIn("checkForUpdates();", source)
