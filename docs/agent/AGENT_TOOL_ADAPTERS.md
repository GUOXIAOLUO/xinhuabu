# Coding Agent Compatibility Notes — Local-First

This project uses one neutral execution contract.

Different tools may discover instructions differently, so use the following rules.

---

## Local-first rule

Every supported tool must work only inside the assigned local workspace/worktree.

Do not use built-in GitHub/PR/remote-repository actions during normal development. Only use a GitHub upload/push action when the user explicitly requests a backup in the current task.

The Agent may use local shell + local Git only.

---

## Universal minimum

Any Agent must be able to:

```text
read repository files
edit repository files
run tests/commands
inspect Git status/diff
work inside a specific local directory
```

If a tool cannot satisfy those capabilities, use it only as a reviewer/planner, not as an implementation Agent.

---

## Codex

Use:

```text
AGENTS.md
MULTI_AGENT_START_PROMPT.md
assigned Agent Task
```

Product Codex architecture names remain unchanged.

---

## ZCode

Open the assigned worktree as Workspace.

Read root `AGENTS.md`, then use:

```text
MULTI_AGENT_START_PROMPT.md
assigned Agent Task
```

---

## Claude Code

Start in the assigned worktree.

Explicitly instruct it to read:

```text
AGENTS.md
MULTI_AGENT_R4_EXECUTION.md
MULTI_AGENT_COORDINATION.md
assigned Agent Task
```

If local Claude-specific instruction files already exist, do not overwrite them; reconcile them with AGENTS.md.

---

## Cursor / Windsurf

Open only the assigned worktree/project folder.

Provide the universal start prompt in the Agent/Chat task and attach/reference the assigned task file.

Do not let an IDE Agent operate on the integration worktree while another Agent is editing it.

---

## Cline / Roo Code

Use the assigned worktree as workspace root.

Give the universal start prompt plus the task file.

Require command approval/settings consistent with local project safety.

---

## Aider

Run Aider from the assigned worktree and give it only task-relevant files when practical.

Use the task file as the implementation contract.

Aider should not be the integration owner unless it has the complete repository/test context needed.

---

## Other Agents

If the tool supports repo-local rules, point it to `AGENTS.md`.

Otherwise paste `MULTI_AGENT_START_PROMPT.md`.

Never create competing architecture-specific instruction files unless they are thin adapters pointing back to the neutral contract.
