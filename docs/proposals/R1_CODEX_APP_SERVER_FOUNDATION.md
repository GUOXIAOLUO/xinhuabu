# R1 Proposal — Codex App Server Foundation

## Problem

The repository has a `codex exec` compatibility path in `main.py`, but no bounded
long-lived App Server integration or stable Workbench-facing transport boundary.

## Constraints

- Pin behavior to the installed Codex CLI and its generated protocol schema.
- Preserve `codex exec`; do not modify its call path in R1.
- Do not expose Workbench Project, Canvas, Node, Graph, provider, or filesystem
  mutation tools to Codex.
- Do not change NodeRecord or persistence authority.

## Options and recommendation

Use Codex App Server over its default stdio JSONL transport, behind
`workbench.codex.CodexBridge`. The tested wire contract is Codex CLI `0.153.1`,
App Server protocol `v2`; it was inspected with:

```text
codex app-server generate-json-schema --out <temporary-directory>
```

R1 uses generated-schema field names for initialize, threads, turns, model/config
discovery, and interruption. It retains no generated files because the CLI emits a
large version-specific tree; the command above is the reproducible validation step.

## Launch policy

- cwd resolves only within the configured workspace root (including symlink
  resolution).
- Child environment is an allowlist; raw provider/API key variables are omitted.
- Thread uses `sandbox: read-only`; every Turn uses `readOnly` plus
  `networkAccess: false` and `approvalPolicy: never`.
- Server approval requests are normalized and denied by default. R1 has no
  interactive approval UI and no Workbench mutation tool surface.
- Calls have a bounded timeout; shutdown terminates, then kills on timeout;
  recovery is an explicit restart.

## Compatibility, security, rollback

`CodexExecCompatibilityAdapter` wraps the existing runner shape without routing it
through App Server. Removing the new module restores the pre-R1 behavior. The
bridge neither persists raw events nor supplies domain mutation tools.

## Acceptance criteria

- Fake-stdio transport tests cover initialize, thread, turn, normalized event,
  model/config calls, restrictive policy, cancellation lifecycle, and shutdown.
- A live non-mutating App Server initialize/config/model smoke check is recorded
  against the pinned CLI version.
- Current architecture/status documents distinguish this bounded foundation from
  later Agent and Workbench runtime rounds.
