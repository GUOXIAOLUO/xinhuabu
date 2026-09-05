# AI Workbench Repository Rules — V2.2.1

## Purpose

This repository incrementally evolves the existing Xinhuabu/Canvas application into a generic AI Workbench.

It is not a greenfield rewrite.

Target:

> **Unified Canvas + Workbench-owned project/resources + Codex Harness default Agent runtime + user-selectable model routes + pluggable Executors + Integration runtime + installable Packages.**

V1:

- Web UI first;
- macOS first;
- Apple Silicon / arm64 primary;
- WholeHouse is the first deep Industry Package.

---

## Authoritative reading order

Before architecture or behavior changes, read:

1. `AGENTS.md`
2. `docs/status/CURRENT_EXECUTION_STATUS.md`
3. `CURRENT_ARCHITECTURE.md`
4. `TARGET_ARCHITECTURE.md`
5. `MIGRATION_PLAN.md`
6. `IMPLEMENTATION_PLAN.md`
7. affected source/tests

Authority:

- executable source + verified tests = current-state facts;
- `AGENTS.md` = hard constraints;
- `TARGET_ARCHITECTURE.md` = target contracts;
- `CURRENT_ARCHITECTURE.md` = current implementation facts;
- `IMPLEMENTATION_PLAN.md` = Round/Gate order;
- `CURRENT_EXECUTION_STATUS.md` = only currently authorized Round.

Planning edits do not authorize future Round implementation.

---

# Hard architecture constraints

## 1. Core remains industry-neutral

Core may own generic:

- Project / Workspace / authorization / audit
- Canvas / Node / Edge / Group
- Prompt / Workbench Skill / definition resolution
- Asset / Artifact / Collection
- Catalog
- Entity / Relation
- Knowledge
- Provider / Model / ModelAvailability
- Execution
- Workflow / Approval / Handoff
- Integration
- Codex runtime adapter
- Package runtime

WholeHouse business implementation belongs under:

```text
packages/wholehouse/
```

Core must remain useful without WholeHouse.

---

## 2. Keep canonical concepts separate

```text
Node
≠ Prompt
≠ Workbench Skill
≠ Model
≠ ProviderDefinition
≠ ProviderConnection
≠ ModelAvailability
≠ ExecutionRoute
≠ ExecutionProfile
≠ Executor
≠ Asset
≠ Artifact
≠ CatalogEntry
≠ Entity
```

Do not make provider/model/executor/industry identity a permanent Node type.

---

## 3. One business-neutral Unified Canvas

Target:

```text
CanvasRecord
+ NodeRecord
+ EdgeRecord
+ NodeShell
+ RendererRegistry
+ DefinitionResolver
```

Classic/Smart are migration sources, not permanent modes.

**A single Canvas entry page is not sufficient evidence of Unified Canvas completion. Unified Canvas requires one product runtime.**

During R4, Classic/Smart may survive only as bounded compatibility adapters. Product-relevant Smart Canvas capabilities must be migrated into shared Unified Canvas modules before duplicate runtime removal. After the R4 Gate, Classic/Smart must not remain permanent product modes or independent product runtimes.

Do not add another industry Canvas.

---

## 4. One definition resolution boundary

All new definition-backed creation resolves through one `DefinitionResolver` or equivalent composite boundary.

Delegates may include:

- PromptRegistry
- SkillRegistry
- LegacyDefinitionRegistry
- Entity definitions
- Workflow/composite definitions
- Package DefinitionSnapshots

`NodeCreationService` must not branch on package/business/provider/Codex IDs.

---

## 5. One creation/mutation boundary

Migrated creation/mutation uses:

- NodeCreationService;
- NodeMutationService;
- GraphMutationService.

No direct domain mutation through:

- DOM;
- raw Canvas JSON;
- raw SQLite;
- provider callback;
- Agent tool bypass.

Applicable writes enforce authorization, expected revision, validation, idempotency/audit and stale-write rejection.

---

## 6. One CompatibilityResolver

Human UI, Workflow and Agent use the same compatibility logic.

No provider-specific or WholeHouse-specific next-step logic in Canvas Core.

---

## 7. Port/Data contracts are explicit

Do not keep `input_bindings` indefinitely untyped.

Target binding categories:

- AssetVersion;
- ArtifactVersion;
- EntityRef / EntityVersion;
- Collection;
- literal/config.

Use `PortTypeRegistry`.

---

## 8. Group != Collection != ExecutionPolicy

- Group = Canvas visual organization.
- Collection = typed multi-item data.
- ExecutionPolicy = batch/retry/parallel semantics.

---

## 9. Prompt is a first-class resource

Prompt is not merely a file inside a Skill.

Target:

- PromptDefinition;
- PromptVersion;
- PromptRegistry.

Prompt may be used by Codex, direct APIs, Workflows and media executors.

---

## 10. Workbench Skill != Codex Skill

Workbench Skill = product capability.

Codex `SKILL.md` = optional implementation for a `codex_harness` ExecutionProfile.

The same Workbench Skill may support multiple executor routes.

Do not copy Workbench Skills into the user's global Codex home as the canonical implementation strategy.

---

## 11. Model / availability / execution remain separate

ModelDefinition = model identity/capabilities.

ModelAvailability = one currently usable route for that model.

A route may be:

```text
provider
runtime
```

Examples:

```text
GPT-X · OpenAI API
GPT-X · Codex Harness
```

Codex is not a Model.

---

## 12. Codex has three roles

1. primary Agent/orchestration runtime;
2. one node execution route;
3. model discovery source.

The Agent's own model does not force child Node models.

Codex-discovered models must be eligible to appear in the same Model Picker as direct-provider models.

---

## 13. No silent runtime substitution

Never silently replace:

- Model;
- ModelAvailability;
- ProviderConnection / RuntimeConnection;
- ExecutionProfile;
- Executor.

Formal provenance records requested and actual selection.

---

## 14. Codex version independence

Workbench must not require one exact Codex release version.

Rules:

- stable App Server APIs first;
- recorded tested version = evidence/diagnostics;
- official generated/validated schema preferred;
- feature detection for optional behavior;
- experimental API use is explicit;
- a required V1 capability must have a non-experimental path or remain deferred;
- do not branch business behavior on exact Codex version strings.

---

## 15. Codex integration stays behind a boundary

Target:

```text
CodexRuntime
├── CodexExecutableResolver
├── AppServerProcess
├── CodexProtocolClient
├── CodexProtocolCompatibility
├── CodexProjectionService
├── CodexWorkbenchToolBridge
└── CodexEventNormalizer
```

Core domain must not import raw Codex protocol DTOs.

V1 transport is stdio.

Do not make experimental App Server WebSocket transport a V1 requirement.

---

## 16. Codex is not business persistence

Codex Threads/Projects own Agent runtime/session state.

Workbench persistence owns formal:

- Project/Canvas;
- Assets/Artifacts;
- Catalog;
- Entities;
- Knowledge;
- Workflow;
- Approval/Frozen;
- Handoff;
- Package history;
- audit.

If needed, use a lightweight `CodexSessionLink`.

---

## 17. Codex Auth is not duplicated by default

Codex/ChatGPT authentication remains primarily managed by Codex App Server.

Workbench CredentialRef is for Workbench-managed provider/integration credentials.

---

## 18. Codex runtime approval != Workbench business approval

Codex runtime approval covers:

- shell;
- files;
- network;
- MCP/runtime permission.

Workbench business approval covers:

- design freeze;
- product decision;
- quote/decision approval;
- CAD handoff approval.

Agent/runtime cannot approve/freeze its own Workbench formal output.

---

## 19. WorkbenchToolContract is stable; transport adapters are replaceable

Agent tools are defined as Workbench domain capabilities.

Adapters may include:

- MCP;
- optional Dynamic Tools;
- future Agent runtime adapters.

Dynamic Tools must not be the only V1 path while experimental.

All tools call Application Services.

---

## 20. Do not build another subagent framework

Codex Harness owns its internal Agent loop/subagent behavior.

Workbench owns business-level orchestration:

- Project;
- Skill;
- Workflow;
- GraphProposal;
- Approval;
- Artifact;
- Handoff.

---

## 21. Project data is authoritative

Project/domain persistence owns formal project truth.

Codex Thread history is not a substitute.

---

## 22. Canonical persistence is explicit

V1 structured authority target is SQLite behind repositories.

Risky persistence changes use:

```text
expand
-> backfill
-> compare
-> compatibility
-> controlled switch
-> verify
-> contract
```

`CanvasRecord.revision` is logical concurrency authority.

Canonical expected-revision write must not reread a newer revision and authorize stale payload.

---

## 23. Asset / Artifact / Catalog / Entity / Knowledge are distinct

- Asset = owned file/blob/version.
- Artifact = produced result/version.
- Catalog = organized reusable reference/product entries.
- Entity = structured formal project fact.
- Knowledge = interpreted/reference information and reproducible retrieval snapshot.

Do not collapse them into one generic JSON/vector record.

---

## 24. Workflow/provenance/approval are versioned

Formal provenance records applicable:

- Node/revision;
- Prompt/version;
- Skill/version;
- Model;
- ModelAvailability;
- route/connection;
- ExecutionProfile/Executor;
- input versions;
- Entity versions;
- KnowledgeSnapshot;
- WorkflowVersion;
- actor/timestamps/usage.

---

## 25. Agent mutation is proposal-first

Agent graph changes use `GraphProposal`.

Application verifies `base_revision`.

Stale proposals are recomputed/rebased/reconfirmed rather than auto-applied.

---

## 26. Package history is independently resolvable

Use `ProjectPackageLock` / `DefinitionSnapshot`.

Historical project readability must not depend only on currently installed package folders.

---

## 27. Integration is generic

Use:

- IntegrationDefinition;
- IntegrationConnection;
- IntegrationRegistry.

Mechanisms may include:

- Native API;
- MCP;
- Local Bridge;
- File Handoff;
- Webhook;
- CLI;
- Human Handoff.

Codex Apps/MCP are projected where useful rather than reimplemented.

---

## 28. macOS-first, Core portable

V1 official runtime/product target is macOS, Apple Silicon first.

macOS-specific code belongs in infrastructure adapters.

Do not inject macOS APIs into Core domain/application contracts when avoidable.

Windows support is future work.

---

## 29. Runtime is repository-independent

Workbench runtime must not depend on a Git repository address.

Do not add:

- GitHub raw/tree URLs;
- source-repository update code;
- product startup dependency on Git hosting.

Legacy self-update logic should be removed, not retargeted.

GitHub can remain external development/CI infrastructure.

---

## 30. Legacy monolith responsibility freeze

Legacy compatibility surfaces:

- `main.py`
- `static/js/canvas.js`
- `static/js/smart-canvas.js`

may retain compatibility behavior, delegate, wire and shrink.

They must not become primary implementation locations for new:

- Prompt;
- SkillRegistry;
- Catalog;
- Provider/Model;
- Execution;
- Integration;
- Asset/Entity/Knowledge/Workflow;
- Package;
- WholeHouse;
- Codex domain tooling.

Backend target for `main.py`:

```text
create_app()
register_routes()
wire_services()
startup/shutdown
narrow compatibility bootstrap
```

---

## 31. Feature flags have a removal Gate

Every migration flag records:

- introduced Round;
- purpose;
- default;
- removal Gate.

After Gate completion, remove obsolete branch/flag.

---

## 32. Security

Secrets stay backend-only.

For changed surfaces check applicable:

- authentication;
- authorization;
- CORS/CSRF;
- path/symlink containment;
- upload/archive safety;
- SSRF/network policy;
- secret redaction;
- subprocess/tool scope;
- timeout/cancel;
- destructive confirmation;
- audit;
- stale-write/concurrency.

LAN mode is not authenticated multi-user support unless explicitly implemented.

---

## 33. Platform Engineering is cross-round

New work should progressively converge on:

- Typed Settings;
- MigrationRunner;
- BlobStore;
- Durable Events;
- Backup/Restore;
- Schema/OpenAPI;
- CI/quality checks;
- Architecture Guards.

Do not overbuild infrastructure before its owning Round/Gate.

---

## 34. Architecture guards

Add automated guards when practical for:

- WholeHouse imports/branches in Core;
- provider-specific Canvas branches;
- Codex protocol DTO imports in Core;
- Agent raw DB/JSON/DOM mutation;
- new business logic in Legacy monoliths;
- runtime Git repository URL dependencies;
- required V1 feature that only works via experimental Codex API.

---

# Round discipline

Only `docs/status/CURRENT_EXECUTION_STATUS.md` authorizes the active Round.

If R4 is active:

- finish R4;
- planning documents may be updated;
- do not start R5-R17 implementation.

Partial completion is not permission to skip Gates.
