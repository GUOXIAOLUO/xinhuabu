# Xinhuabu — Codex 本地开发入口

> 用途：将本文件及同目录文件复制到 **xinhuabu 本地项目根目录**。
>
> 本计划只面向本地项目文件夹开发，不要求、也不授权 Codex 修改远程 GitHub 仓库。

## Codex 启动方式

打开本地 xinhuabu 项目文件夹后，把下面这句话发给 Codex：

```text
严格读取并执行 CODEX_NEXT_TASK.md。遵守 AGENTS.md 和当前 Round/Gate，不要提前实施后续 Round。直接检查本地工作树并继续当前授权任务。
```

Codex 必须把本地工作树作为唯一当前执行现场。

## 文件位置

复制后目录应类似：

```text
xinhuabu/
├── AGENTS.md                         # 项目已有，不覆盖
├── CURRENT_ARCHITECTURE.md           # 项目已有
├── TARGET_ARCHITECTURE.md            # 项目已有
├── MIGRATION_PLAN.md                 # 项目已有
├── IMPLEMENTATION_PLAN.md            # 项目已有
├── CODEX_README.md                   # 新增
├── CODEX_NEXT_TASK.md                # 新增
├── CODEX_PROJECT_CONTEXT.md          # 新增
├── CODEX_EXECUTION_PLAN.md           # 新增
└── docs/
    └── plans/
        └── R4_OWNERSHIP_MATRIX.md    # 新增
```

## 权威顺序

Codex 必须优先服从项目已有：

1. `AGENTS.md`
2. `docs/status/CURRENT_EXECUTION_STATUS.md`
3. `CURRENT_ARCHITECTURE.md`
4. `TARGET_ARCHITECTURE.md`
5. `MIGRATION_PLAN.md`
6. `IMPLEMENTATION_PLAN.md`

本文件包用于把上述架构讨论转成具体执行方式，**不能覆盖项目已有硬规则**。

## 核心约束

- 只在本地工作树开发。
- 不要求 push、PR、远程同步。
- 不把远程 GitHub 状态当作当前工作树事实。
- 当前若仍为 R4，只执行 R4。
- 不因为存在统一入口 URL 就认为 Unified Canvas 已完成。
- R4 的最终指标是：**Classic/Smart Runtime Ownership 归零，Unified Canvas 成为唯一产品 Runtime。**
