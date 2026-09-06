# Xinhuabu — Codex 本地执行计划

## Status

本文件面向 Codex 在 **本地项目文件夹** 中直接开发。

本文件不授权修改远程 GitHub 仓库。

任何实际实现必须首先服从：

```text
AGENTS.md
docs/status/CURRENT_EXECUTION_STATUS.md
```

---

# Phase 0 — Establish Local Truth

读取 authoritative docs 和 affected source/tests。

执行：

```text
git status
git diff --stat
git branch --show-current
git rev-parse HEAD
```

记录：

```text
local HEAD
branch
working tree dirty files
active Round
current Canvas authority
current feature flags
```

不要自动 reset 用户本地改动。

不要覆盖未知本地修改。

---

# Phase 1 — R4 Ownership Inventory

完整扫描：

```text
static/canvas.html
static/smart-canvas.html
static/js/canvas.js
static/js/smart-canvas.js
static/js/workbench/canvas/**
Canvas backend/application/domain modules
relevant tests
```

更新：

```text
docs/plans/R4_OWNERSHIP_MATRIX.md
```

每一项使用：

```text
UNIFIED
PARTIAL
CLASSIC
SMART
COMPAT_ONLY
REMOVE
```

状态。

重点不是 helper，而是 owner。

---

# Phase 2 — Rendering Ownership

目标：

```text
NodeRecord
→ UnifiedRenderHost
→ NodeShell
→ RendererRegistry
```

所有产品级 migrated node 应从 Unified 路径渲染。

流程：

```text
characterize current behavior
→ add/strengthen Unified seam
→ delegate one Legacy caller
→ compare behavior
→ migrate second caller
→ run browser tests
→ remove duplicate renderer responsibility
```

不得提前增加 Rich Node 产品能力。

---

# Phase 3 — Interaction Ownership

依次收口：

```text
selection
multi-selection
drag
resize
connect
keyboard
viewport
group interaction
```

目标：

```text
one interaction state owner
```

Legacy adapter 不能继续拥有独立状态机。

不要仅共享 geometry/helper。

---

# Phase 4 — Creation Ownership

扫描：

```text
menus
toolbar
context menu
file drop
paste
import
Smart composer
connected creation
```

所有正常产品创建最终：

```text
CreationCatalog
→ NodeCreationService
```

图变化：

```text
GraphMutationService
```

Legacy constructors 只能用于历史兼容读取，不能继续承担正常创建。

---

# Phase 5 — Graph / Group Ownership

保持：

```text
Group = visual organization
```

统一：

```text
membership
move
selection
connect
graph record mutation
```

不要在 R4 引入 Collection 业务系统。

---

# Phase 6 — Media Ownership

保留已经共享的：

```text
classification
URL normalization
preview/original resolution
playback preservation
size helpers
grid math
```

但继续检查：

```text
media DOM render ownership
render lifecycle
high-resolution switching lifecycle
player binding ownership
```

如果仍由 Classic/Smart 两套主流程拥有，应迁入 Unified ownership。

---

# Phase 7 — Persistence Verification

保持：

```text
SQLite CanvasRecord = normal authority
Legacy JSON = import/rollback compatibility
```

验证：

```text
read
write
restart
CAS revision
stale conflict
rollback export
```

不能为了解决 stale conflict 自动覆盖用户新数据。

---

# Phase 8 — Legacy Execution Decoupling

R4 只做兼容层解耦。

保持当前 provider/execution behavior。

但确保：

```text
execution trigger
result normalization
result placement
Canvas graph mutation
```

边界逐渐清楚。

不要实现 R8 ExecutorRegistry。

---

# Phase 9 — Duplicate Runtime Removal

删除前必须证明 Smart retained capabilities 已迁移。

目标删除：

```text
Smart product runtime ownership
Classic duplicate product runtime ownership
direct Smart product routing
obsolete compatibility handoff
obsolete feature flags
```

可保留：

```text
bounded Legacy import/read adapters
```

最终 `canvas.html` 直接使用唯一 Unified Runtime。

---

# Phase 10 — Acceptance

## Functional

验证：

```text
new Canvas
legacy Classic
legacy Smart
```

包括：

```text
open
pan
zoom
select
multi-select
drag
resize
connect
group
create
delete
save
reload
```

## Media

验证：

```text
image
video
audio if supported
preview fallback
playback state
```

## Data

验证：

```text
restart
stale conflict
rollback
workflow import/export
clipboard/subgraph
```

## Performance

验证：

```text
100 nodes
300 nodes
```

观察：

```text
DOM duplication
listener duplication
full rerenders
visible input lag
media reload storms
memory growth
```

只修复与 R4 Gate 相关问题。

---

# Phase 11 — Architecture Guards

增加/保持 guards：

```text
no WholeHouse branches in Core
no provider-specific Canvas branches
no Codex protocol DTO imports in Core
no new Workbench systems in Legacy monoliths
no runtime Git hosting dependency
no direct Smart page routing from normal product flow
```

---

# Phase 12 — R4 Final Gate

使用 checklist：

```text
[ ] one visible Canvas entry
[ ] one actual Canvas runtime
[ ] SQLite normal persistence authority
[ ] one interaction ownership
[ ] one rendering ownership
[ ] one creation ownership
[ ] Classic no longer product runtime
[ ] Smart no longer product runtime
[ ] retained Smart capability parity
[ ] old Classic readable
[ ] old Smart readable
[ ] stale conflict verified
[ ] restart verified
[ ] rollback verified
[ ] workflow parity
[ ] 100-node pass
[ ] 300-node pass
[ ] obsolete flags removed
[ ] architecture guards pass
```

全部满足：

```text
R4: PASS
```

否则：

```text
R4: NOT PASS
```

继续执行 R4。

---

# Future Contract Guardrails — DO NOT IMPLEMENT DURING R4

R4 代码不能破坏以下后续方向：

## R5

```text
NodeShell V2
PresentationHost
card / expanded / workspace / inspector
WorkspaceSession
NodeAction surface
branch/materialization
```

## R6

```text
PortTypeRegistry
typed InputBinding
Collection
CompatibilityResolver
DefinitionResolver
Prompt
Skill
```

## R8

```text
ExecutionProfile
ExecutorRegistry
ExecutionRun / Attempt / Event
Codex / API / ComfyUI / MCP adapters
```

## R9

```text
Asset / AssetVersion
Artifact / ArtifactVersion
lineage
result tray
explicit materialization
```

## R14

```text
Codex Agent Panel
WorkbenchToolContract
GraphProposal
```

## WholeHouse

```text
package only
no Core branches
file/CAD handoff first
```

---

# Development Discipline

每一个 patch 都优先满足：

```text
small
bounded
behavior-preserving
tested
ownership-reducing
```

优先模式：

```text
characterize
→ seam
→ delegate
→ verify
→ migrate owner
→ remove duplicate
```

不要：

```text
large rewrite
cosmetic splitting
parallel new architecture
future Round implementation
```

---

# Required Codex Progress Report

每完成一个可验证小阶段，输出：

```text
## Local repository
HEAD:
branch:
dirty files:

## Ownership migration
Before:
After:

## Files changed

## Behavior preserved

## Tests

## R4 Gate impact

## Remaining Classic ownership

## Remaining Smart ownership

## Next R4 action
```
