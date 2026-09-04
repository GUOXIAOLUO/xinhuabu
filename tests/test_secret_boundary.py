import asyncio
import inspect
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import httpx

import main


class SecretBoundaryTests(unittest.TestCase):
    def test_legacy_configuration_route_exposes_only_configuration_state(self):
        secret = "fixture-secret-that-must-not-cross-the-browser-boundary"
        with patch.object(main, "modelscope_api_key", return_value=secret):
            payload = asyncio.run(main.get_global_token())
        self.assertEqual(payload, {"configured": True})
        self.assertNotIn(secret, repr(payload))
        self.assertNotIn("token", payload)

    def test_modelscope_generation_routes_ignore_legacy_request_api_key(self):
        for handler in (
            main.poll_angle_cloud,
            main.generate_angle_cloud,
            main.generate_cloud,
            main.ms_generate,
        ):
            self.assertNotIn("modelscope_api_key(req.api_key)", inspect.getsource(handler))

    def test_legacy_pages_do_not_read_or_submit_modelscope_tokens(self):
        for relative_path in ("static/angle.html", "static/zimage.html"):
            source = Path(relative_path).read_text(encoding="utf-8")
            self.assertNotIn("modelscope_api_token", source)
            self.assertNotIn("/api/config/token", source)
            self.assertNotIn("api_key:", source)

    def test_sensitive_text_redaction_removes_auth_query_and_proxy_credentials(self):
        secret = "fixture-secret-that-must-not-appear-in-logs"
        value = (
            f"Bearer {secret}; https://user:{secret}@proxy.test:8443 "
            f"https://api.test/path?api_key={secret}&token={secret}"
        )

        redacted = main.redact_sensitive_value(value)

        self.assertNotIn(secret, redacted)
        self.assertIn("Bearer [REDACTED]", redacted)
        self.assertIn("api_key=[REDACTED]", redacted)
        self.assertIn("token=[REDACTED]", redacted)
        self.assertIn("://[REDACTED]@", redacted)

    def test_network_error_logs_do_not_include_request_secrets(self):
        secret = "fixture-secret-that-must-not-appear-in-network-error"
        request = httpx.Request("GET", f"https://api.test/path?api_key={secret}")
        error = httpx.ConnectError(f"Authorization: Bearer {secret}", request=request)

        with patch("builtins.print") as printed:
            main.log_net_error(f"provider token={secret}", error)

        output = "\n".join(str(call.args[0]) for call in printed.call_args_list)
        self.assertNotIn(secret, output)
        self.assertIn("[REDACTED]", output)

    def test_runninghub_log_redacts_nested_sensitive_fields(self):
        secret = "fixture-secret-that-must-not-appear-in-runninghub-log"
        with patch("builtins.print") as printed:
            main.log_runninghub_error(
                "submit",
                raw={"token": secret, "nested": {"api_key": secret}, "message": "failed"},
            )

        payload = json.loads(str(printed.call_args.args[0]).removeprefix("RunningHub error: "))
        self.assertEqual(payload["raw"]["token"], "[REDACTED]")
        self.assertEqual(payload["raw"]["nested"]["api_key"], "[REDACTED]")
        self.assertNotIn(secret, json.dumps(payload))
