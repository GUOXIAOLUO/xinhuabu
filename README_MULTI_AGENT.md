# Xinhuabu — Local-First + Manual GitHub Backup Multi-Agent R4 Pack

> **HARD RULE — LOCAL-FIRST**
>
> 日常开发只操作当前电脑上的 Xinhuabu 本地项目；GitHub 仅作为用户手动触发的备份仓库。
>
> 禁止开发 Agent：
>
> ```text
> push
> pull
> fetch
> clone replacement repo
> create PR
> update GitHub files
> use remote main as source of truth
> ```
>
> Git 只作为本地版本控制与多 Agent 隔离工具使用：
>
> ```text
> local branch
> local worktree
> local commit
> local merge
> local diff
> local rollback
> ```
>
> 是否以后同步到 GitHub，由用户在开发完成后另行决定，不属于 Agent 当前任务。

本包用于让多个 Coding Agent 在同一个 Xinhuabu 项目上协同开发，例如：

```text
Codex
ZCode
Claude Code
Cursor Agent
Windsurf
Cline
Roo Code
Aider
其他支持本地仓库 / shell / Git 的 Coding Agent
```

本包不要求所有 Agent 使用同一种产品或同一种提示词机制。

核心原则：

```text
ONE PROJECT ARCHITECTURE
ONE R4 SOURCE OF TRUTH
MULTIPLE ISOLATED AGENT WORKSPACES
NO SHARED DIRTY WORKTREE
NO OVERLAPPING OWNERSHIP UNIT
```

---

## 1. 不覆盖现有 AGENTS.md

项目已有：

```text
AGENTS.md
```

它仍然是所有 Agent 的第一层硬约束。

本包不会提供第二个 AGENTS.md。

支持自动读取 `AGENTS.md` 的 Agent 直接读取；
不支持自动读取的 Agent，必须由启动 Prompt 明确要求读取。

---

## 2. 推荐放置结构

复制本包到项目根目录：

```text
xinhuabu/
├── AGENTS.md
├── MULTI_AGENT_R4_EXECUTION.md
├── MULTI_AGENT_START_PROMPT.md
├── MULTI_AGENT_COORDINATION.md
├── README_MULTI_AGENT.md
├── docs/
│   ├── agent/
│   │   ├── AGENT_TASK_TEMPLATE.md
│   │   ├── AGENT_HANDOFF_TEMPLATE.md
│   │   └── AGENT_TOOL_ADAPTERS.md
│   └── plans/
│       └── R4_FINAL_GATE_CHECKLIST_MULTI_AGENT.md
└── .agent/
    ├── TASK_BOARD.example.md
    └── OWNERSHIP_LOCKS.example.md
```

`.agent/*.example.md` 是模板。

实际并行开发时建议复制为：

```text
.agent/TASK_BOARD.md
.agent/OWNERSHIP_LOCKS.md
```

是否提交这两个运行时协调文件由你决定。

---

## 3. 多 Agent 并行的正确方式

不要让多个 Agent 共用同一个 dirty working tree。

推荐：

```text
main local checkout
│
├── worktree/r4-rendering
│   └── agent: Codex
│
├── worktree/r4-selection
│   └── agent: ZCode
│
├── worktree/r4-media
│   └── agent: Claude Code
│
└── worktree/r4-tests
    └── agent: Cursor/Windsurf
```

每个 Agent：

```text
独立 worktree
独立 branch
独立 task
独立 file scope
独立 ownership unit
```

然后按依赖关系顺序合并。

---

## 4. 什么可以并行，什么不能并行

适合并行：

```text
互不重叠的测试补强
互不重叠的 architecture guards
独立 renderer characterization
独立 interaction characterization
Legacy fixture verification
performance instrumentation
documentation evidence
```

谨慎并行：

```text
Rendering ownership
Interaction ownership
Media ownership
Creation ownership
```

只有文件范围和运行时 owner 明确不重叠时才能并行。

不建议并行：

```text
Canvas save/revision/polling authority
normal-connect transaction boundary
same runtime state owner
same central renderer host
same creation coordinator
same SQLite authority path
runtime removal
feature flag contraction
R4 final Gate/status update
```

这些必须由单一 owner 串行完成。

---

## 5. 产品架构不能因开发 Agent 改变

开发工具可以变化：

```text
Codex / ZCode / Claude Code / Cursor / Windsurf / Cline ...
```

但 Xinhuabu 产品内部已经确定的：

```text
CodexBridge
Codex Harness
Codex App Server
CodexHarnessExecutor
CodexWorkbenchToolBridge
```

仍属于产品目标架构。

不要因为换开发工具而改名。

---

## 6. 开始方式

给任意 Agent 的第一条指令使用：

```text
MULTI_AGENT_START_PROMPT.md
```

然后为每个 Agent 创建一份：

```text
docs/agent/AGENT_TASK_TEMPLATE.md
```

填写：

```text
Agent ID
Branch
Worktree
Ownership Unit
Allowed Files
Forbidden Files
Dependencies
Acceptance
```

---

## 7. 最重要的并行开发规则

任何 Agent 在动代码前都必须先确认：

```text
这个 Ownership Unit 有没有被其他 Agent 锁定？
```

如果已锁：

```text
不要修改。
```

如果两个任务会修改同一个 central owner：

```text
不要并行。
```

如果一个任务依赖另一个未合并 patch：

```text
标记 BLOCKED，不要自行复制/重写对方实现。
```

---

## 8. R4 最终目标

无论使用多少开发 Agent，最终产品仍然只有：

```text
ONE Unified Canvas product runtime
```

多 Agent 是开发组织方式，不是运行时架构。
