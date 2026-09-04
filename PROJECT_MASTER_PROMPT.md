# AI Workbench — Project Master Prompt V2.1

You are developing `GUOXIAOLUO/xinhuabu` incrementally from the existing canvas application into a generic AI Workbench.

Do not treat it as greenfield.

Before code changes read:

1. `AGENTS.md`
2. `docs/status/CURRENT_EXECUTION_STATUS.md`
3. `CURRENT_ARCHITECTURE.md`
4. `TARGET_ARCHITECTURE.md`
5. `MIGRATION_PLAN.md`
6. `IMPLEMENTATION_PLAN.md`
7. affected source/tests

Execute only the authorized Round.

Core rules:

- WholeHouse belongs under `packages/wholehouse/`.
- One Unified Canvas.
- Node != Skill != Model != ProviderConnection != ModelAvailability != Executor != Artifact.
- Workbench Skill != Codex `SKILL.md`.
- DefinitionRefs resolve through one generic DefinitionResolver.
- Node creation/mutation uses application services.
- Port/Data bindings become typed.
- Group != Collection != ExecutionPolicy.
- Do not silently switch model/provider/executor.
- Project/Canvas logical revision is distinct from timestamps.
- Project persistence is authoritative; Codex Threads are not.
- Asset != Artifact != Entity != Knowledge.
- Formal Entity changes are versioned.
- Frozen applies to approved immutable formal versions.
- Agent graph mutation is GraphProposal-first and revision-checked.
- Package historical definitions remain resolvable after disable/uninstall.
- Secrets remain backend-only.
- Legacy capability remains compatible until its Gate permits removal.

Codex roles:

1. Harness/App Server = system Agent/orchestration runtime.
2. Codex/OpenAI models = ordinary ModelRegistry/ModelAvailability choices.

WholeHouse V1 focuses on design optimization and CAD/file handoff readiness, not production, installation, after-sales or direct software control.

Follow `IMPLEMENTATION_PLAN.md` R0-R17.
