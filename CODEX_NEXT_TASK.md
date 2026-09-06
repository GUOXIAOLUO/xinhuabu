# CODEX NEXT TASK — 本地项目执行入口

## 任务模式

你正在直接开发当前打开的 **xinhuabu 本地项目文件夹**。

不要以远程 GitHub 仓库作为执行目标。
不要要求先 push / pull / 建 PR。
不要修改远程仓库。

本地工作树、项目现有源码、测试与状态文档才是当前事实来源。

---

# 1. 启动检查

每次开始工作，严格按顺序读取：

```text
AGENTS.md
docs/status/CURRENT_EXECUTION_STATUS.md
CURRENT_ARCHITECTURE.md
TARGET_ARCHITECTURE.md
MIGRATION_PLAN.md
IMPLEMENTATION_PLAN.md
CODEX_PROJECT_CONTEXT.md
CODEX_EXECUTION_PLAN.md
docs/plans/R4_OWNERSHIP_MATRIX.md
```

然后检查：

```text
git status
git branch --show-current
git rev-parse HEAD
```

Git 仅用于理解当前**本地工作树**，不是要求操作远程仓库。

禁止因为远程状态未知而停止本地任务。

---

# 2. Round 授权

读取：

```text
docs/status/CURRENT_EXECUTION_STATUS.md
```

以其中的：

```text
active_round
```

作为唯一实现授权。

如果当前仍为：

```text
R4 — Unified Canvas Cutover
```

则：

# 只允许实施 R4。

不得提前实现：

```text
R5 NodeShell V2 新产品功能
Node Workspace 正式产品能力
Typed InputBinding 新 schema
PromptRegistry
SkillRegistry
ModelAvailability Runtime
ExecutorRegistry
Artifact Runtime
Agent Panel
WholeHouse
```

可以记录后续 seam / TODO / compatibility constraints，但不能越级实现。

---

# 3. 当前执行目标

如果 active_round == R4：

立即执行：

```text
重新扫描 Classic / Smart / Unified Canvas 的 Runtime Ownership
→ 更新 docs/plans/R4_OWNERSHIP_MATRIX.md
→ 找出仍由 Classic/Smart 独立拥有的产品 Runtime 责任
→ 选择风险最低、边界最清晰的一项
→ characterize
→ add seam if needed
→ delegate
→ migrate ownership
→ run tests
→ remove obsolete responsibility if Gate evidence permits
→ 更新 Ownership Matrix
→ 继续下一项
```

不要继续以“又抽出一个 shared helper”为主要完成指标。

主要指标：

```text
Classic Runtime Ownership ↓
Smart Runtime Ownership ↓
Unified Runtime Ownership ↑
```

---

# 4. 当前 R4 优先级

按以下顺序处理，除非本地代码事实证明必须调整：

```text
P0 Rendering ownership
P0 Interaction ownership
P0 Creation ownership
P0 Unified page/runtime ownership

P1 Group / graph ownership
P1 Clipboard / import / export ownership
P1 media render lifecycle ownership

P2 Legacy execution compatibility decoupling
P2 obsolete feature flags
P2 duplicate page/runtime removal
```

Persistence 已经切到 SQLite 的部分必须继续验证，但不要重复重写已经通过 Gate 的基础。

---

# 5. 每次修改前

必须先回答：

```text
1. 当前责任现在由谁拥有？
2. 为什么这仍然构成双 Runtime？
3. 迁移到哪个 Unified module？
4. 是否会改变现有产品行为？
5. 如何证明 parity？
6. 迁移完成后能删除什么 Legacy responsibility？
```

如果只能回答：

```text
“我可以再抽一个 helper”
```

但不能减少 Classic/Smart ownership：

不要做该修改。

---

# 6. 每次修改后

执行最相关的：

```text
unit tests
contract tests
architecture guards
browser smoke
```

并更新：

```text
docs/plans/R4_OWNERSHIP_MATRIX.md
```

记录：

```text
before owner
after owner
files changed
tests/evidence
remaining Legacy responsibility
```

---

# 7. 禁止行为

禁止：

```text
新增第三套 Canvas Runtime
新增 WholeHouse Canvas
把 Smart Canvas 永久包装在统一入口下面
给 main.py 增加新 Workbench 业务系统
给 canvas.js / smart-canvas.js 增加新业务系统
为 Provider/Codex/WholeHouse 增加 Canvas Core 分支
把 Group 改成 AI Context 数据模型
把 Execution Result 强绑定为自动 Canvas Node
为了减少文件行数机械拆文件
提前实现后续 Round
```

---

# 8. R4 完成判定

R4 必须同时满足：

```text
one visible Canvas entry
one actual product Canvas runtime
one persistence authority
one rendering ownership
one interaction ownership
one normal node creation ownership
Classic no longer product runtime
Smart no longer product runtime
retained Smart capabilities migrated
old Classic records readable
old Smart records readable
stale-write behavior verified
workflow import/export parity
100-node acceptance
300-node acceptance
restart acceptance
rollback evidence
obsolete R4 flags removed
architecture guards pass
```

单一 URL 不算完成。

---

# 9. 工作方式

除非遇到真正无法在本 Round 解决的 blocker：

不要停在分析。

优先：

```text
inspect
→ edit
→ test
→ inspect
→ edit
→ test
```

一次做小而完整的 ownership migration。

不要大爆炸重写。

---

# 10. 每轮输出

完成一批修改后报告：

```text
Repository facts
Changes
Ownership moved
Behavior preserved
Tests
Remaining Classic ownership
Remaining Smart ownership
Unified ownership
R4 Gate impact
Next R4 task
```

如果 R4 未通过：

明确写：

```text
R4: NOT PASS
```

然后继续处理 R4。

只有所有 Gate 证据完成后才允许：

```text
R4: PASS
```

并按项目正式流程更新状态进入 R5。
