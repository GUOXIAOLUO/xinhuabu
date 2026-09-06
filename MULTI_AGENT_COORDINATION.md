# Multi-Agent Coordination Protocol

This file defines how Codex, ZCode, Claude Code, Cursor, Windsurf, Cline, Roo, Aider, or other local Coding Agents work on Xinhuabu simultaneously.

---

# 0. Local-first coordination

Development coordination is entirely local.

The repository on the user's machine is the only development target and source of truth. GitHub may be used only for an explicitly user-requested backup.

By default do not:

```text
push branches
pull/fetch remote changes
open PRs
edit GitHub
depend on remote CI
use remote branch state to resolve local conflicts
```

If the user explicitly requests “backup/upload to GitHub”, one designated Backup Owner may perform that backup only. Remote operations return to disabled afterward.

All coordination happens through:

```text
local worktrees
local branches
local commits
local merges
.agent task board
.agent ownership locks
local test results
```

---

# 1. Roles

Use three conceptual roles:

```text
INTEGRATION OWNER
TASK AGENT
REVIEW / TEST AGENT
```

## Integration Owner

Owns:

```text
task decomposition
ownership locks
merge order
cross-branch regression
R4 status truth
final Gate decision
```

Only one Integration Owner at a time.

## Task Agent

Owns one bounded implementation unit.

## Review / Test Agent

May independently inspect/test a patch, but must not silently rewrite the implementation in parallel.

---

# 2. Workspace isolation

Preferred:

```text
git worktree
```

One Agent per worktree.

Example branch convention:

```text
agent/<agent-id>/r4-<ownership-unit>
```

Examples:

```text
agent/codex/r4-render-mount
agent/zcode/r4-selection-state
agent/claude/r4-media-playback-tests
```

Do not allow two Agents to edit the same physical working directory simultaneously.

---

# 3. Task board

Maintain:

```text
.agent/TASK_BOARD.md
```

Each task has:

```text
ID
status
agent
branch
worktree
ownership unit
depends_on
blocks
allowed files
forbidden files
acceptance
merge order
```

Statuses:

```text
READY
LOCKED
IN_PROGRESS
BLOCKED
READY_FOR_REVIEW
MERGED
REJECTED
```

---

# 4. Ownership lock

Maintain:

```text
.agent/OWNERSHIP_LOCKS.md
```

Lock by semantic owner, not only file.

Example:

```text
runtime.save-coordinator        → LOCKED by agent/codex
runtime.renderer-mount          → LOCKED by agent/zcode
tests.media-playback            → LOCKED by agent/claude
```

Why semantic locks matter:

Two Agents may touch different files but still implement competing owners.

---

# 5. Lock acquisition rule

Before editing:

```text
1. read TASK_BOARD
2. read OWNERSHIP_LOCKS
3. confirm task READY
4. claim semantic ownership unit
5. set task IN_PROGRESS
6. edit only assigned scope
```

If lock exists:

```text
STOP and choose another task.
```

---

# 6. File scope

Each task defines:

```text
allowed_files
forbidden_files
```

Example:

```text
allowed:
- static/js/workbench/canvas/unified-render-host.js
- tests/test_frontend_workbench_modules.py

forbidden:
- static/js/smart-canvas.js
- docs/status/CURRENT_EXECUTION_STATUS.md
```

If a necessary change falls outside scope:

```text
report NEEDS_SCOPE_EXPANSION
```

Do not silently expand scope.

---

# 7. Shared-file policy

High-conflict files:

```text
main.py
static/js/canvas.js
static/js/smart-canvas.js
docs/plans/R4_OWNERSHIP_MATRIX.md
docs/status/CURRENT_EXECUTION_STATUS.md
```

Prefer one owner at a time.

For `R4_OWNERSHIP_MATRIX.md`, parallel Agents may provide a suggested patch/evidence, while Integration Owner reconciles the final merged state.

---

# 8. Merge order

Merge dependencies first.

Example:

```text
A: shared render lifecycle seam
↓
B: Classic delegate
↓
C: Smart delegate
↓
D: duplicate renderer removal
↓
E: acceptance tests
```

Do not merge D before B/C parity exists.

---

# 9. Rebase rule

Before LOCAL review/merge:

```text
update branch from the LOCAL integration base
resolve conflicts against authoritative merged behavior
rerun tests
```

Do not resolve conflicts by keeping both competing code paths.

---

# 10. Handoff rule

When Agent stops, it writes a handoff using:

```text
docs/agent/AGENT_HANDOFF_TEMPLATE.md
```

Must include:

```text
what changed
what remains
known risks
tests run
files touched
semantic owner state
next dependency
```

---

# 11. Review rule

Review Agent checks:

```text
architecture compliance
ownership reduction
behavior parity
test sufficiency
unexpected new responsibility in Legacy
future Round leakage
hidden duplicate lifecycle
```

Review Agent should prefer comments/findings over parallel rewrite.

---

# 12. Integration test checkpoints

Run integration regression:

```text
after central owner merge
after every 2-3 independent task merges
before runtime removal
after runtime removal
before R4 Gate
```

---

# 13. No asynchronous assumptions

No Agent should leave undocumented "background" work.

Every stopped task must be one of:

```text
MERGED
READY_FOR_REVIEW
BLOCKED
REJECTED
```

with a handoff.

---

# 14. Final authority

The merged LOCAL integration branch is the only implementation truth.

Unmerged agent branches are evidence/proposals, not architecture truth.
