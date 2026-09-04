# R1 Task — Codex Harness Foundation

Execute R1 only after R0 explicitly authorizes it.

Goal:

Establish Codex App Server behind a stable Workbench `CodexBridge`.

Do not give Codex Workbench project/Canvas mutation tools.

Before implementation:

- inspect installed/target Codex version
- inspect current official App Server schema/protocol for that version
- inspect existing codex-exec path
- create/update the required App Server proposal
- define HarnessLaunchPolicy

Protocol:

Treat App Server as Codex JSON-RPC-lite framed as JSONL over stdio.
Prefer generated/validated bindings.

HarnessLaunchPolicy:

- bounded cwd/workspace
- environment allowlist/secret filtering
- filesystem/shell policy
- destructive approval behavior
- timeout/cancellation
- child process lifecycle
- no Workbench project mutation tools

Required CodexBridge capabilities:

- start/initialize
- health/version
- Thread create/resume where supported
- simple Turn
- normalized events
- approval request/response
- model/config discovery
- cancel/shutdown/recovery
- codex-exec compatibility adapter

Non-goals:

- Canvas changes
- Agent graph mutation
- SkillRegistry
- ModelRegistry
- target ExecutionRuntime
- WholeHouse

R1 passes only when transport/runtime behavior and launch policy are tested and status authorizes R2.
