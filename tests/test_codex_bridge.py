import asyncio
import sys
import tempfile
import unittest
from pathlib import Path

from workbench.codex.bridge import CodexBridge, CodexBridgeError, HarnessLaunchPolicy


FAKE_SERVER = r'''import json, sys
pending_turn = None
for raw in sys.stdin:
    message = json.loads(raw)
    if message.get("method") == "initialized": continue
    if message.get("method") == "initialize":
        print(json.dumps({"id": message["id"], "result": {"protocolVersion": "2"}}), flush=True)
    elif message.get("method") == "thread/start":
        print(json.dumps({"id": message["id"], "result": {"thread": {"id": "thread-1"}}}), flush=True)
    elif message.get("method") == "turn/start":
        pending_turn = message["id"]
        print(json.dumps({"id": 99, "method": "item/commandExecution/requestApproval", "params": {"reason": "fixture"}}), flush=True)
    elif message.get("id") == 99 and pending_turn:
        assert message["result"] == {"decision": "decline"}
        print(json.dumps({"method": "turn/completed", "params": {"turn": {"id": "turn-1"}}}), flush=True)
        print(json.dumps({"id": pending_turn, "result": {"turn": {"id": "turn-1"}}}), flush=True)
        pending_turn = None
    elif message.get("method") == "turn/interrupt":
        print(json.dumps({"id": message["id"], "result": {}}), flush=True)
    elif message.get("method") == "model/list":
        print(json.dumps({"id": message["id"], "result": {"data": []}}), flush=True)
    elif message.get("method") == "config/read":
        print(json.dumps({"id": message["id"], "result": {"config": {}}}), flush=True)
'''


class CodexBridgeTests(unittest.IsolatedAsyncioTestCase):
    async def test_bridge_initializes_uses_restrictive_options_and_normalizes_events(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = HarnessLaunchPolicy(
                Path(directory), executable=sys.executable, arguments=("-u", "-c", FAKE_SERVER)
            )
            bridge = CodexBridge(policy)
            initialized = await bridge.start()
            thread = await bridge.create_thread()
            turn = await bridge.start_turn(thread["thread"]["id"], "hello")
            self.assertEqual(await bridge.list_models(), {"data": []})
            self.assertEqual(await bridge.read_config(), {"config": {}})
            approval = await asyncio.wait_for(bridge.events.get(), timeout=1)
            event = await asyncio.wait_for(bridge.events.get(), timeout=1)
            self.assertEqual(initialized["protocolVersion"], "2")
            self.assertEqual(turn["turn"]["id"], "turn-1")
            self.assertEqual(approval.kind, "approval_requested")
            self.assertEqual(event.kind, "turn_completed")
            self.assertEqual(policy.turn_options()["sandboxPolicy"], {"type": "readOnly", "networkAccess": False})
            self.assertEqual(policy.thread_options()["approvalPolicy"], "never")
            await bridge.shutdown()

    async def test_interrupt_and_explicit_recovery_are_supported(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = HarnessLaunchPolicy(
                Path(directory), executable=sys.executable, arguments=("-u", "-c", FAKE_SERVER)
            )
            bridge = CodexBridge(policy)
            await bridge.start()
            self.assertEqual(await bridge.interrupt_turn("thread-1", "turn-1"), {})
            recovered = await bridge.recover()
            self.assertEqual(recovered["protocolVersion"], "2")
            await bridge.shutdown()

    async def test_policy_bounds_cwd_and_filters_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            policy = HarnessLaunchPolicy(Path(directory))
            self.assertEqual(policy.environment({"PATH": "/bin", "OPENAI_API_KEY": "secret"}), {"PATH": "/bin"})
            with self.assertRaises(CodexBridgeError):
                policy.resolve_cwd(Path(directory).parent)
