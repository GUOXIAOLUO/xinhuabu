"""Small, version-pinned stdio boundary for Codex App Server.

Raw JSONL protocol details remain here so future application code depends on
``CodexBridge`` rather than the Codex App Server protocol.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping


CODEX_APP_SERVER_PROTOCOL = "v2"
CODEX_APP_SERVER_TESTED_VERSION = "0.153.1"


class CodexBridgeError(RuntimeError):
    """A local transport, protocol, or launch-policy failure."""


@dataclass(frozen=True)
class HarnessLaunchPolicy:
    """R1's deliberately restrictive process and turn policy."""

    workspace_root: Path
    executable: str = "codex"
    arguments: tuple[str, ...] = ("app-server",)
    timeout_seconds: float = 30.0
    allowed_environment: frozenset[str] = frozenset(
        {"PATH", "HOME", "CODEX_HOME", "TMPDIR", "LANG", "LC_ALL", "TERM", "USER", "LOGNAME", "SHELL"}
    )

    def resolve_cwd(self, cwd: str | Path | None = None) -> Path:
        root = self.workspace_root.resolve()
        candidate = Path(cwd or root).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise CodexBridgeError("Codex working directory escapes the configured workspace") from exc
        return candidate

    def environment(self, source: Mapping[str, str] | None = None) -> dict[str, str]:
        source = source or os.environ
        return {key: source[key] for key in self.allowed_environment if source.get(key)}

    def command(self) -> list[str]:
        executable = shutil.which(self.executable) if os.path.sep not in self.executable else self.executable
        if not executable:
            raise CodexBridgeError("Codex CLI executable was not found")
        return [executable, *self.arguments]

    def thread_options(self, cwd: str | Path | None = None) -> dict[str, Any]:
        return {
            "cwd": str(self.resolve_cwd(cwd)),
            "approvalPolicy": "never",
            "sandbox": "read-only",
        }

    def turn_options(self, cwd: str | Path | None = None) -> dict[str, Any]:
        return {
            "cwd": str(self.resolve_cwd(cwd)),
            "approvalPolicy": "never",
            "sandboxPolicy": {"type": "readOnly", "networkAccess": False},
        }


@dataclass(frozen=True)
class CodexBridgeEvent:
    kind: str
    method: str
    payload: Mapping[str, Any] = field(default_factory=dict)


class CodexBridge:
    """Async JSONL client for the version-pinned App Server v2 protocol."""

    def __init__(self, policy: HarnessLaunchPolicy):
        self.policy = policy
        self._process: asyncio.subprocess.Process | None = None
        self._next_id = 1
        self.events: asyncio.Queue[CodexBridgeEvent] = asyncio.Queue()
        self._pending: dict[int, asyncio.Future[Mapping[str, Any]]] = {}
        self._reader_task: asyncio.Task[None] | None = None

    @property
    def running(self) -> bool:
        return self._process is not None and self._process.returncode is None

    async def start(self) -> Mapping[str, Any]:
        if self.running:
            return await self.health()
        self._process = await asyncio.create_subprocess_exec(
            *self.policy.command(),
            cwd=str(self.policy.resolve_cwd()),
            env=self.policy.environment(),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._reader_task = asyncio.create_task(self._read_messages())
        result = await self.request(
            "initialize",
            {"clientInfo": {"name": "ai-workbench", "version": "r1"}, "capabilities": {}},
        )
        await self.notify("initialized", {})
        return result

    async def health(self) -> Mapping[str, Any]:
        return {
            "running": self.running,
            "protocol": CODEX_APP_SERVER_PROTOCOL,
            "tested_codex_cli": CODEX_APP_SERVER_TESTED_VERSION,
            "pid": self._process.pid if self._process else None,
        }

    async def create_thread(self, cwd: str | Path | None = None) -> Mapping[str, Any]:
        return await self.request("thread/start", self.policy.thread_options(cwd))

    async def resume_thread(self, thread_id: str, cwd: str | Path | None = None) -> Mapping[str, Any]:
        return await self.request("thread/resume", {"threadId": thread_id, **self.policy.thread_options(cwd)})

    async def start_turn(self, thread_id: str, text: str, cwd: str | Path | None = None) -> Mapping[str, Any]:
        return await self.request(
            "turn/start",
            {"threadId": thread_id, "input": [{"type": "text", "text": text}], **self.policy.turn_options(cwd)},
        )

    async def interrupt_turn(self, thread_id: str, turn_id: str) -> Mapping[str, Any]:
        return await self.request("turn/interrupt", {"threadId": thread_id, "turnId": turn_id})

    async def list_models(self) -> Mapping[str, Any]:
        return await self.request("model/list", {})

    async def read_config(self, cwd: str | Path | None = None) -> Mapping[str, Any]:
        return await self.request("config/read", {"cwd": str(self.policy.resolve_cwd(cwd)), "includeLayers": True})

    async def request(self, method: str, params: Mapping[str, Any]) -> Mapping[str, Any]:
        if not self.running or not self._process or not self._process.stdin:
            raise CodexBridgeError("Codex App Server is not running")
        request_id = self._next_id
        self._next_id += 1
        future: asyncio.Future[Mapping[str, Any]] = asyncio.get_running_loop().create_future()
        self._pending[request_id] = future
        await self._send({"id": request_id, "method": method, "params": params})
        try:
            return await asyncio.wait_for(future, timeout=self.policy.timeout_seconds)
        finally:
            self._pending.pop(request_id, None)

    async def notify(self, method: str, params: Mapping[str, Any]) -> None:
        await self._send({"method": method, "params": params})

    async def shutdown(self) -> None:
        process, self._process = self._process, None
        if self._reader_task:
            self._reader_task.cancel()
            self._reader_task = None
        if process and process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=self.policy.timeout_seconds)
            except TimeoutError:
                process.kill()
                await process.wait()
        for future in self._pending.values():
            if not future.done():
                future.set_exception(CodexBridgeError("Codex App Server stopped"))
        self._pending.clear()

    async def recover(self) -> Mapping[str, Any]:
        await self.shutdown()
        return await self.start()

    async def _send(self, message: Mapping[str, Any]) -> None:
        if not self._process or not self._process.stdin:
            raise CodexBridgeError("Codex App Server stdin is unavailable")
        self._process.stdin.write((json.dumps(message, separators=(",", ":")) + "\n").encode())
        await self._process.stdin.drain()

    async def _read_messages(self) -> None:
        assert self._process and self._process.stdout
        while line := await self._process.stdout.readline():
            try:
                message = json.loads(line)
            except json.JSONDecodeError:
                await self.events.put(CodexBridgeEvent("protocol_error", "invalid-json", {"line": line.decode(errors="replace")}))
                continue
            if "id" in message and (future := self._pending.get(message["id"])):
                if "error" in message:
                    future.set_exception(CodexBridgeError(str(message["error"])))
                else:
                    future.set_result(message.get("result", {}))
                continue
            method = str(message.get("method", "unknown"))
            kind = "approval_requested" if "approval" in method.lower() else self._event_kind(method)
            await self.events.put(CodexBridgeEvent(kind, method, message.get("params", {})))
            # R1 has no approval UI or mutation authority. Any server request is denied.
            if "id" in message:
                await self._send({"id": message["id"], "result": {"decision": "decline"}})

    @staticmethod
    def _event_kind(method: str) -> str:
        if method == "turn/completed":
            return "turn_completed"
        if method.startswith("item/"):
            return "item_event"
        return "notification"


class CodexExecCompatibilityAdapter:
    """Keeps existing ``codex exec`` callers outside the App Server bridge."""

    def __init__(self, runner: Callable[..., Awaitable[Any]]):
        self._runner = runner

    async def run(self, prompt: str, **options: Any) -> Any:
        return await self._runner(prompt, **options)
