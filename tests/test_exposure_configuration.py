import unittest

import main


class ExposureConfigurationTests(unittest.TestCase):
    def test_default_origins_are_local_only(self):
        self.assertEqual(
            main.parse_allowed_origins(None, 4312),
            [
                "http://127.0.0.1:4312",
                "http://localhost:4312",
                "http://[::1]:4312",
            ],
        )

    def test_explicit_origins_are_normalized(self):
        self.assertEqual(
            main.parse_allowed_origins(" https://example.test/ , http://localhost:3000 ", 3000),
            ["https://example.test", "http://localhost:3000"],
        )

    def test_wildcard_origin_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "must not contain wildcard"):
            main.parse_allowed_origins("*", 3000)

    def test_app_info_reports_safe_runtime_metadata(self):
        payload = main.app_info()
        self.assertIn(payload["server"]["exposure_mode"], {"local_only", "lan_opt_in"})
        self.assertNotIn("*", payload["server"]["allowed_origins"])
