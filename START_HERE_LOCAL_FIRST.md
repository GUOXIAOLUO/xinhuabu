# START HERE — Local-First Multi-Agent Development

给任何 Coding Agent 的第一条指令：

```text
读取根目录 AGENTS.md、LOCAL_FIRST_GITHUB_BACKUP_POLICY.md、
MULTI_AGENT_R4_EXECUTION.md、MULTI_AGENT_COORDINATION.md
以及分配给你的 Agent Task。

只在当前本地项目/worktree 中进行日常开发。

GitHub 只作为备份仓库。
除非我在当前任务中明确说“上传/备份到 GitHub”，否则禁止：
push / pull / fetch / PR / 远程文件修改。

即使执行过一次 GitHub 备份，备份完成后也恢复为“远程操作默认禁止”。

本地源代码和本地已验证测试始终是实现事实来源。

当前只执行 R4 Unified Canvas Cutover。
一次只完成一个 bounded ownership unit。
完成后运行本地测试、检查本地 diff、输出 handoff/report。
不要自行宣布 R4 PASS。
```
