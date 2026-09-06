# Universal Start Prompt for Any Coding Agent

你正在 Xinhuabu 的一个独立本地 worktree 中工作。

你只能在当前电脑的 Xinhuabu 本地项目/worktree 中进行日常开发。GitHub 仅作为用户手动触发的备份仓库。

默认禁止：

```text
git push
git pull
git fetch
创建 PR
修改 GitHub 远程文件
使用远程 main/HEAD 作为事实来源
```

只有当用户在当前任务明确说“上传/备份到 GitHub”时，才允许由指定 Agent 执行一次备份。备份完成后恢复默认禁止远程操作。

允许使用本地 Git 做：

```text
status
diff
branch
worktree
commit
local merge
local rollback
```

本地结果始终是开发事实来源；用户可明确要求将当前本地集成版本备份到 GitHub，但备份不会改变事实来源。

你是一个 **Task Agent**，不是项目架构的唯一决策者。

首先读取：

```text
AGENTS.md
docs/status/CURRENT_EXECUTION_STATUS.md
CURRENT_ARCHITECTURE.md
TARGET_ARCHITECTURE.md
MIGRATION_PLAN.md
IMPLEMENTATION_PLAN.md
CODEX_EXECUTION_PLAN.md
docs/plans/R4_OWNERSHIP_MATRIX.md
MULTI_AGENT_R4_EXECUTION.md
MULTI_AGENT_COORDINATION.md
```

然后读取分配给你的 Agent Task 文件。

执行：

```text
git status
git diff --stat
git branch --show-current
git rev-parse HEAD
```

确认：

```text
Agent ID
worktree
branch
base commit
assigned task
semantic ownership lock
allowed files
forbidden files
dependencies
```

如果任务没有明确 Ownership Unit、锁已被其他 Agent 占用、或需要改其他 Agent 正在拥有的 central owner：

```text
STOP
```

并报告冲突，不要自行并行实现第二套方案。

当前只允许：

```text
R4 — Unified Canvas Cutover
```

核心产品决策：

```text
ONE Unified Canvas product runtime
```

Classic / Smart 只能逐步退化为 compatibility adapters，不能形成一个入口下的两套永久 Runtime。

你每次只实现一个 bounded ownership unit。

方法：

```text
characterize
→ seam
→ delegate
→ verify
→ migrate owner
→ remove duplicate responsibility
```

不要：

```text
large rewrite
cosmetic splitting
future Round implementation
unrelated cleanup
automatic reset
overwrite unknown changes
```

你使用什么开发 Agent 不改变 Xinhuabu 产品内部的：

```text
CodexBridge
Codex Harness
Codex App Server
```

这些仍是产品目标架构。

Normal connect、Save/Revision authority、UnifiedRenderHost central lifecycle、global interaction owner、runtime removal、feature flag removal 等 central-owner 工作不能与另一个 Agent 并行修改。

完成后：

```text
1. run targeted tests
2. run required local regression
3. inspect git diff
4. write Agent completion report
5. create handoff if not merged
```

不要单独宣告 `R4: PASS`。

只有 Integration Owner 基于合并后的代码和完整 Gate 才能作出最终判断。
