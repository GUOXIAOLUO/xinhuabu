# Xinhuabu Workbench — Codex 本地项目上下文

## 1. 产品目标

Xinhuabu 不是要长期维护 Classic Canvas + Smart Canvas 两套产品。

最终产品：

```text
Xinhuabu Workbench
├── Projects
├── Unified Canvas
├── Resources
├── Agent
└── Settings
```

核心：

```text
ONE Unified Canvas
```

WholeHouse（全屋定制）是第一个深度 Industry Package，不是 Core，也不拥有第二套 Canvas。

---

# 2. 最终核心架构

```text
Unified Canvas
      │
      ▼
 Canvas Runtime
      │
 ┌────┼────────────┐
 │    │            │
Graph Interaction View
 │
 ▼
NodeRecord
 │
DefinitionResolver
 │
RendererRegistry
 │
NodeShell
 │
Presentation
 │
Skill / Workflow
 │
InputBinding / Collection
 │
CompatibilityResolver
 │
ExecutionProfile
 │
ModelAvailability
 │
ExecutorRegistry
 │
ExecutionRun
 │
ArtifactVersion
```

相关独立资源：

```text
Asset
Artifact
Collection
Entity
Knowledge
Prompt
Skill
Workflow
Approval
Handoff
Package
```

---

# 3. Node 原则

Node 是：

> 某个资源、任务、流程在 Canvas 上的工作界面。

Node 不是整个业务对象本身。

Node 也不是执行器。

保持有限 Core kinds：

```text
asset
skill
artifact
entity
task
approval
group
composite
legacy
```

业务含义来自：

```text
definition_ref
```

不要增加：

```text
agent
codex
comfyui
customer
space
cabinet
quote
wholehouse
```

等永久 Core NodeKind。

---

# 4. Rich Node 产品方向

DX-OS 视频最值得吸收的是 Rich Node，而不是它的具体技术节点。

目标交互：

```text
card
→ expanded
→ workspace
→ inspector
```

富节点应该让用户在一个业务对象内部完成连续工作。

例如 Image：

```text
Image
├── preview
├── crop
├── annotate
├── vision
├── AI edit
├── variants
└── history
```

但底层不要新增很多永久 NodeKind：

```text
CropNode
MaskNode
VisionNode
ResizeNode
```

复杂能力通过：

```text
Renderer / Workspace
+
Action
+
Skill
+
Workflow
+
Executor
```

组合。

这些主要属于 R5/R6/R8/R13，当前 R4 不提前实现。

---

# 5. Group / Collection 严格分开

```text
Group
=
Canvas visual organization
```

```text
Collection
=
typed semantic multi-item data
```

```text
ExecutionPolicy
=
batch/retry/parallel execution semantics
```

不要合并。

WholeHouse 中“客厅参考资料集合”应优先由 Collection 表达，而不是给 Group 增加业务语义。

---

# 6. Edge / InputBinding 严格分开

```text
Edge
=
Canvas graph relationship
```

```text
InputBinding
=
任务执行真正消费的数据绑定
```

未来 InputBinding 应能够表达：

```text
source_type
source_ref
port_id
role_ref
order
enabled
metadata
```

role_ref 不应成为 Core 行业枚举。

例如：

```text
wholehouse.reference.floorplan
wholehouse.reference.style
```

由 Package/Definition 解释。

当前 R4 不提前改 schema。

---

# 7. Renderer / Presentation 原则

不要新增另一套重量级 Presentation Domain。

优先：

```text
RendererRegistry V2
```

让一个 renderer family 支持：

```text
card
expanded
workspace
inspector
```

NodeShell 保持通用 chrome / intent host。

禁止把：

```text
image crop
CAD controls
WholeHouse UI
provider logic
Codex protocol
```

塞进 NodeShell。

---

# 8. Action 原则

未来富节点内部动作采用轻量 Action descriptor，而不是再造 CapabilityDefinition 体系。

概念关系：

```text
Node Action
→ Skill 或 Application Command
→ Workflow（需要时）
→ ExecutionProfile
→ Executor
```

不要新增重量级：

```text
CapabilityDefinition
```

除非后续有明确证据表明 Skill/Workflow 无法承载。

---

# 9. Workspace Session 原则

富节点内部的临时编辑：

```text
crop
mask
annotate
undo
redo
parameter tuning
```

不能每一步都生成正式 ArtifactVersion。

未来：

```text
ArtifactVersion
↓
WorkspaceSession
↓
temporary edits
↓
commit
↓
new ArtifactVersion
```

Workspace session 需要基于 base revision/version 防止 stale overwrite。

主要属于 R5/R9。

---

# 10. Execution Result 不等于 Canvas Node

未来 AI 一次生成 4 个结果：

不应该自动创建 4 个 Canvas Node。

目标：

```text
ExecutionRun
↓
results
↓
result tray
↓
select / compare
↓
materialize
↓
Canvas Node
```

Canvas 只展示当前工作需要的对象。

这能防止大项目 Canvas 爆炸。

R4 只保留解耦 seam，不提前实现 Artifact Runtime。

---

# 11. Artifact 原则

```text
Asset
=
用户/项目拥有的输入文件或数据
```

```text
Artifact
=
Workbench 执行产生的结果
```

正式结果必须版本化、非覆盖。

未来保持 lineage：

```text
Artifact V1
↓ derived from
Artifact V2
↓
Artifact V3
```

并记录：

```text
Prompt/version
Skill/version
inputs/version
model
ModelAvailability
route
ExecutionProfile
Executor
actor
timestamps
```

---

# 12. Draft / Formal / Frozen

全屋定制正式业务不能把：

```text
AI completed
```

等同于：

```text
approved design
```

未来至少有语义：

```text
draft
→ formal
→ approved/frozen
```

Frozen 只能由授权人类完成。

Node frozen state 只是正式状态的 UI projection。

---

# 13. Workflow 两种概念不能混

Workbench Business Workflow：

```text
需求
→ 方案
→ 审核
→ 确认
→ Handoff
```

Executor-native workflow：

```text
ComfyUI JSON
RunningHub workflow
CAD processing graph
```

二者不是同一个 authority/schema。

ComfyUI 技术 DAG 应隐藏在 Executor/Integration 后面。

---

# 14. Codex 的位置

Codex 有三种角色：

```text
1. primary Agent runtime
2. one execution route
3. model discovery source
```

不要新增：

```text
CodexNodeKind
```

系统 Agent 优先是：

```text
Canvas + Agent side panel
```

Codex 不能直接：

```text
mutate DOM
write raw Canvas JSON
write raw SQLite
```

正式变化：

```text
read
→ reason
→ GraphProposal
→ user confirmation
→ Application Service
→ mutation
```

---

# 15. WholeHouse 边界

WholeHouse 最终位于：

```text
packages/wholehouse/
```

注册：

```text
Skills
Prompts
Entities
Catalog definitions
Knowledge
Workflows
templates
review rules
handoff rules
```

Core 不出现：

```text
if wholehouse
```

V1：

```text
project intake
→ requirement/floorplan analysis
→ space/design concept
→ material/product selection
→ render/review
→ approval/frozen
→ CAD/file handoff readiness
```

暂不覆盖：

```text
production/CNC
installation
after-sales
mandatory direct Agent control of Kujiale/GuiGui
```

酷家乐/柜柜前期通过 CAD/PDF/Excel/图片/Handoff 交接。

---

# 16. Round 演进约束

保持项目已有 Round 编号。

推荐理解：

```text
R4  Unified Canvas 真正收口
R5  Generic Node UX + Presentation/Workspace seams
R6  Typed Binding/Collection/Prompt/Skill
R7  Provider/Model/ModelAvailability
R8  Execution Runtime
R9  Asset/Artifact/Lineage
R10 Entity/Knowledge
R11 Workflow/Approval/Handoff
R12 Package/Workspace/Integration
R13 Common Rich Node proof
R14 Codex Agent integration
R15-R17 WholeHouse
```

不要重新编号，也不要越级实施。
