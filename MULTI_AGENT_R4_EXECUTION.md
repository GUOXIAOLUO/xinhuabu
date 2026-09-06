# Multi-Agent R4 Execution Contract — Xinhuabu

**Authorized Round:** R4 — Unified Canvas Cutover  
**Development model:** multiple isolated Coding Agents  
**Product target:** ONE Unified Canvas product runtime

---

# 0A. LOCAL-FIRST execution boundary

All normal development occurs only on the current machine and assigned local worktree. GitHub is a manual backup destination only.

Forbidden by default unless the user explicitly requests a GitHub backup/upload in the current task:

```text
git push
git pull
git fetch
GitHub PR creation
GitHub file edits
remote branch synchronization
remote repository replacement
remote HEAD as implementation authority
```

Allowed:

```text
git status
git diff
git log
git branch
git worktree
git add
git commit
git merge
git rebase between LOCAL branches when coordinated
local restore/rollback with user changes protected
```

The integration result remains local and authoritative. A user-requested GitHub backup is a one-way backup action, not a development authority switch.

---

# 0. Universal authority order

EVERY Agent must read:

```text
1. AGENTS.md
2. docs/status/CURRENT_EXECUTION_STATUS.md
3. CURRENT_ARCHITECTURE.md
4. TARGET_ARCHITECTURE.md
5. MIGRATION_PLAN.md
6. IMPLEMENTATION_PLAN.md
7. CODEX_EXECUTION_PLAN.md
8. docs/plans/R4_OWNERSHIP_MATRIX.md
9. MULTI_AGENT_R4_EXECUTION.md
10. MULTI_AGENT_COORDINATION.md
11. its assigned task file
12. affected source/tests
```

Authority:

```text
source + verified tests
> AGENTS.md
> authoritative project docs
> this execution contract
> individual agent task
```

No individual Agent may redefine architecture or Round order.

---

# 1. Mandatory local truth

Each Agent runs in its OWN worktree and executes:

```text
git status
git diff --stat
git branch --show-current
git rev-parse HEAD
```

Record:

```text
Agent ID
worktree path
branch
base commit
dirty files
assigned ownership unit
allowed files
blocked dependencies
```

Rules:

```text
DO NOT reset user changes.
DO NOT work in another Agent's worktree.
DO NOT edit files outside assigned scope without coordination.
DO NOT use any remote repository as implementation truth.
DO NOT silently rebase/merge another Agent's LOCAL branch.
```

---

# 2. Locked product architecture

Final target:

```text
CanvasRecord(s)
      ↓
Unified Canvas Runtime
├── Interaction
├── Rendering
├── Creation
├── Graph / Group
├── Media lifecycle
└── Persistence coordination
      ↓
Application Services
      ↓
SQLite canonical authority
```

Legacy Classic / Smart are compatibility sources only.

Forbidden final states:

```text
one entry + two hidden runtimes
Unified frontend + two permanent node backends
Classic/Smart permanent product modes
```

---

# 3. Ownership migration metric

Primary metric:

```text
Classic Runtime Ownership ↓
Smart Runtime Ownership ↓
Unified Runtime Ownership ↑
```

Each Agent patch must state:

```text
Before owner
After owner
Classic responsibility removed
Smart responsibility removed
Unified responsibility added
```

A shared helper without ownership reduction is not sufficient.

---

# 4. Unit-of-work rule

The maximum safe parallel unit is:

```text
ONE bounded ownership unit
```

Examples:

```text
selection state delegation
renderer mount ownership
media playback binding ownership
file-drop creation projection
architecture guard for Smart routing
100-node instrumentation
```

Bad task:

```text
"finish Unified Canvas"
```

Bad parallel task:

```text
Agent A: refactor renderer lifecycle
Agent B: refactor renderer lifecycle differently
```

---

# 5. Candidate R4 streams

Potential streams:

```text
S1 Save / Remote Apply
S2 Rendering
S3 Interaction
S4 Creation
S5 Graph / Group
S6 Media
S7 Persistence verification
S8 Legacy execution compatibility
S9 Runtime removal
S10 Acceptance / Performance / Guards
```

These streams are NOT automatically independent.

Central-owner work is serialized.

---

# 6. Current preferred path

After confirming local reality:

```text
finish current Save / Remote Apply ownership
→ Rendering
→ Interaction
→ Creation
→ Graph / Group
→ Media
→ Persistence verification
→ Legacy execution compatibility
→ Smart retained capability parity
→ Smart runtime removal
→ Classic duplicate runtime removal
→ cleanup / flags
→ acceptance / guards
→ R4 PASS
```

Parallel work may support this path, but may not bypass dependencies.

---

# 7. Parallelization classes

## GREEN — normally safe to parallelize

```text
read-only characterization
test fixture additions in disjoint files
architecture guards in disjoint files
performance measurements
documentation evidence
Legacy record fixture verification
media test coverage isolated from runtime owner changes
```

## YELLOW — parallel only with explicit file + owner separation

```text
Rendering sub-units
Interaction sub-units
Creation sub-units
Media sub-units
Group behavior
browser acceptance automation
```

## RED — serialize

```text
Canvas revision authority
SaveScheduler core
remote apply/polling coordinator
normal-connect canonical transaction
UnifiedRenderHost central lifecycle
global interaction state owner
Creation coordinator
SQLite authority switch
runtime/page removal
feature flag removal
CURRENT_EXECUTION_STATUS final update
R4 final Gate decision
```

---

# 8. Conflict rule

If two Agents need the same file or central owner:

```text
STOP parallel execution.
```

Choose one:

```text
A. make Agent B wait
B. split the task at a real stable seam
C. merge Agent A first, then rebase Agent B
```

Never resolve architectural conflict by keeping both implementations.

---

# 9. Dependency rule

Every task declares:

```text
depends_on:
blocks:
```

If dependency is not merged:

```text
status = BLOCKED
```

Agent must not copy unmerged implementation from another worktree unless explicitly coordinated.

---

# 10. Normal-connect special rule

This is RED / serialized.

Before modification characterize all side effects:

```text
target execution config
inputNodeIds
group membership
generator/output synchronization
other Legacy effects
```

Avoid:

```text
GraphMutationService write
+
raw Canvas save
```

Do not prematurely implement Typed InputBinding or R8 Execution schema.

---

# 11. Runtime removal special rule

Smart/Classic runtime removal is RED / serialized.

Prerequisites:

```text
retained capability parity
functional parity
media parity
legacy record readability
rollback evidence
no hidden lifecycle dependencies
```

No Agent may delete runtime/page/CSS merely because another task "plans" to migrate behavior.

Only merged evidence counts.

---

# 12. Legacy monolith freeze

`main.py`, `static/js/canvas.js`, `static/js/smart-canvas.js` may:

```text
delegate
wire
compatibility
shrink
```

They may not receive new Workbench business systems.

Do not cosmetic-split them.

---

# 13. Product Codex architecture is preserved

Development Agent identity is irrelevant to product architecture.

Do not rename/remove:

```text
CodexBridge
Codex Harness
Codex App Server
CodexHarnessExecutor
CodexWorkbenchToolBridge
```

unless an authoritative future Round explicitly changes product architecture.

---

# 14. Future Round prohibition

R4 Agents must not implement:

```text
NodeShell V2 product expansion
PromptRegistry
SkillRegistry
ProviderRegistry
ModelRegistry
ModelAvailability Runtime
ExecutorRegistry
Artifact Runtime
Entity/Knowledge Runtime
Agent Panel
WorkbenchToolContract
GraphProposal
WholeHouse
```

Do not invent R4.5.

---

# 15. Test rule

Each Agent runs:

```text
targeted tests
+
minimum necessary regression for touched owner
```

Before merge, integration owner runs cross-stream regression.

An Agent may not claim global R4 PASS based only on its branch.

---

# 16. Documentation ownership

Parallel Agents may propose evidence.

Only the integration owner should finalize:

```text
docs/status/CURRENT_EXECUTION_STATUS.md
R4 final Gate decision
obsolete feature flag removal list
runtime removal completion statement
```

`R4_OWNERSHIP_MATRIX.md` may be updated per task, but merge conflicts must be reconciled against merged source truth.

---

# 17. Completion report

Every Agent must produce:

```text
Agent ID:
branch:
base:
ownership unit:

Before owner:
After owner:

Files changed:
Tests:
Behavior preserved:
Unexpected diff:
Dependencies:
Blocks:
R4 Gate impact:
Remaining risks:
Recommended merge order:
```
