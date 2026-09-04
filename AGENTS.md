# AI Workbench Repository Rules

## Purpose

This repository incrementally evolves `GUOXIAOLUO/canvas` into a generic AI Workbench.
It is not a greenfield rewrite.

Target:

**AI Workbench Core + Codex Harness + dynamic Workbench Skills + user-selectable Models + explicit Provider Connections + pluggable Executors + versioned project data + installable Packages.**

WholeHouse is the first deep Industry Package, not the Core.

V1 is Web UI first.

---

## Authoritative reading order

Before architecture or behavior changes, read:

1. `AGENTS.md`
2. `docs/status/CURRENT_EXECUTION_STATUS.md`
3. `CURRENT_ARCHITECTURE.md`
4. `TARGET_ARCHITECTURE.md`
5. `MIGRATION_PLAN.md`
6. `IMPLEMENTATION_PLAN.md`
7. affected source files and tests

Authority:

- executable source + verified tests = current-state facts;
- `AGENTS.md` = hard constraints;
- `TARGET_ARCHITECTURE.md` = target contracts;
- `CURRENT_ARCHITECTURE.md` = current implementation facts;
- `IMPLEMENTATION_PLAN.md` = Round/Gate order;
- `CURRENT_EXECUTION_STATUS.md` = currently authorized Round.

If `CURRENT_ARCHITECTURE.md` contradicts live source/tests, update it in the same Round that verifies the contradiction.

Do not infer the active Round from historical prose.

---

# Hard architecture constraints

## 1. Core remains industry-neutral

Core may own generic:

- Project / Canvas / authorization / audit
- Node / Edge / Group
- Asset / Artifact / Collection
- Entity / Relation
- Knowledge
- Workbench Skill / Definition resolution
- Provider / Model / ModelAvailability
- Execution
- Workflow / Approval / Handoff
- MCP / Tool runtime
- CodexBridge
- Package / WorkspaceProfile runtime

WholeHouse business implementation belongs under:

`packages/wholehouse/`

Core must start and support useful general work without WholeHouse.

---

## 2. Keep canonical concepts separate

```text
Node
≠ Workbench Skill
≠ Model
≠ ProviderDefinition
≠ ProviderConnection
≠ ModelAvailability
≠ ExecutionProfile / Executor
≠ Artifact
```

Definitions:

- Workbench Skill = reusable work/method contract.
- Model = model identity and capabilities.
- ProviderDefinition = provider/protocol adapter type.
- ProviderConnection = one configured user/workspace connection/account/endpoint.
- ModelAvailability = one executable route from a Model through a ProviderConnection and compatible Executor.
- ExecutionProfile = user-facing execution mode supported by a Skill.
- Executor = runtime mechanism that performs a run.
- Artifact = versioned produced result.
- Node = one visual work instance.

Do not make provider/model/executor identity a permanent Node type.

---

## 3. Codex has two separate roles

### Harness role

Codex Harness / App Server is the primary Agent/orchestration runtime target.

Workbench product code depends on a stable `CodexBridge`, not raw App Server/subprocess/protocol details.

### Model role

Models discovered through Codex/OpenAI are ordinary ModelRegistry/ModelAvailability choices.

The Agent's own model does not force child Node models.

Do not create a permanent "Codex model Node".

---

## 4. Workbench Skill is not Codex Skill

A Workbench Skill is the product-level capability definition.

A Codex `SKILL.md` is one possible implementation used by one `codex_harness` ExecutionProfile.

The same Workbench Skill may support Codex Harness, direct model API, script, ComfyUI, or another compatible executor without changing Skill identity.

---

## 5. One business-neutral Unified Canvas

Target:

`CanvasRecord + NodeRecord + EdgeRecord + NodeShell + RendererRegistry + DefinitionResolver`

Canvas understands graph/interaction/state, not WholeHouse meaning.

Do not add a third Canvas.

Classic/Smart are migration sources, not permanent product modes.

Legacy capability may remain through adapters after duplicate Canvas runtime removal.

---

## 6. Finite renderer vocabulary

Default renderer families:

- media
- document
- analysis
- task
- entity
- form
- table
- comparison
- approval
- composite
- legacy

New Skills normally reuse an existing renderer.

Adding a new renderer family requires architecture justification/proposal if the existing vocabulary can plausibly serve the requirement.

---

## 7. One definition resolution boundary

All Node creation resolves `definition_ref` through one generic `DefinitionResolver` or equivalent composite boundary.

It may delegate to:

- SkillRegistry
- LegacyDefinitionRegistry
- Entity definition registry
- Workflow/composite definition registry
- Package historical DefinitionSnapshots

`NodeCreationService` must not branch on package/business/provider IDs.

---

## 8. One creation/mutation boundary

Migrated creation uses:

- `NodeCreationService`
- `GraphMutationService` for atomic graph changes

Migrated edits use `NodeMutationService` or equivalent validated application boundary.

Creation/mutation must support applicable:

- authorization
- expected revision
- validation
- idempotency
- audit
- stale-write rejection
- outdated propagation

Do not add direct raw node/project JSON or DOM-based domain mutation paths.

---

## 9. One compatibility resolver

Human and Agent flows use the same compatibility logic.

Compatibility may consider:

- Port/Data type
- cardinality
- Skill/Package enabled state
- permissions
- model capability/availability
- executor availability
- project state/policy

This powers port highlighting, port drop to blank Canvas, "Use it next", dynamic toolbar, Command-K suggestions and Agent Skill selection.

Do not hard-code provider-specific or WholeHouse-specific next-step menus into Canvas Core.

---

## 10. Port/Data contracts are explicit

Do not keep `input_bindings` as an indefinitely untyped bag.

Target binding categories include:

- AssetVersion
- ArtifactVersion
- EntityRef / EntityVersion
- Collection
- literal/config input

KnowledgeSnapshot normally belongs to execution context unless a Skill explicitly declares a Knowledge input contract.

Use `PortTypeRegistry`, not an Artifact-only registry, because ports can carry Asset, Artifact, Entity and Collection references.

---

## 11. Group != Collection != ExecutionPolicy

- Group = Canvas visual organization.
- Collection = typed multi-item data semantics.
- ExecutionPolicy = batch/loop/retry/parallel semantics.

Legacy Loop remains compatible, but new batch behavior converges on ExecutionPolicy.

---

## 12. No silent runtime substitution

Model selection precedence:

1. current Node user choice
2. user's Skill default
3. Workspace/System user default

The system may filter and recommend.

It must not silently replace:

- Model
- ProviderConnection / ModelAvailability
- ExecutionProfile / Executor

Unavailable selected routes surface an explicit actionable state.

Formal provenance records requested and actual selections.

---

## 13. NodeRecord v1 migration contracts

Current NodeRecord v1 remains the migration basis until explicitly proposed otherwise.

### Execution selection

Until R8 proves the execution contract:

```json
{
  "workbench.execution": {
    "profile_id": "codex-deep",
    "executor_type": "codex_harness",
    "runtime_connection_id": null
  }
}
```

lives under `extensions`.

### ModelAvailability selection

Current NodeRecord v1 `ModelBinding` contains `provider_id + model_id`.

During migration:

- `model_id` continues to identify the selected Model.
- `provider_id` remains the Legacy/provider-connection compatibility identifier required by v1.
- canonical ModelAvailability identity is stored in a namespaced extension when needed.

Example:

```json
{
  "workbench.model_availability": {
    "availability_id": "availability_01"
  }
}
```

Do not silently reinterpret stored `provider_id` as a new incompatible concept.

Promoting stable model/execution bindings into NodeRecord v2 requires a proposal.

---

## 14. State authorities are separated

Target separation:

- `NodeState` = Canvas/task projection state.
- `ExecutionRunState` = execution authority.
- Artifact freshness = current/outdated.
- Approval/Frozen = governance state on formal versions.

A Node may project `outdated` or `frozen`, but formal Artifact/Approval records are authoritative.

Frozen applies to a formal version, not to mutable Node UI state itself.

---

## 15. Node UX stays task-oriented

NodeShell converges on:

1. task/status
2. inputs/collections
3. primary content/result
4. Skill / Model / Execution
5. actions/output

Advanced implementation details belong in Inspector.

Intermediate ArtifactVersions may exist without visible Nodes and may be materialized on demand.

---

## 16. Project data is authoritative

Project/domain persistence owns formal:

- requirements/dimensions
- Project/Canvas identity
- structured Entities
- Canvas graph
- Assets/Artifacts
- Knowledge snapshots
- Workflow versions/runs
- approvals/frozen versions
- handoffs
- audit

Codex Threads own Agent session/conversation state, not formal project truth.

---

## 17. Canonical persistence is explicit

V1 structured authority target is SQLite behind repositories.

Risky persistence changes use:

`expand -> backfill -> compare -> compatibility -> controlled switch -> verify -> contract`

Do not leave new domain systems permanently authoritative in ad-hoc Legacy JSON.

`CanvasRecord.revision` is a logical revision, not a timestamp alias.

Changing the primary database strategy requires proposal approval.

---

## 18. Legacy Project identity migration is explicit

Legacy Canvas fields such as `project: "default"` and empty/unowned `owner` must map through an explicit migration policy.

Do not invent ownership silently during migration.

R3 must define the local workspace actor/default project mapping before authority switch.

---

## 19. Authorization is action-based

Current `can_edit(...)` behavior may remain as compatibility.

Target authorization is action/resource based, for example:

- project.read
- canvas.edit
- execution.run
- artifact.write
- entity.edit
- knowledge.manage
- approval.decide
- handoff.export
- provider.manage
- package.manage

Codex tools receive least-privilege project-scoped capabilities.

---

## 20. Asset, Artifact, Entity and Knowledge are distinct

- Asset = owned file/blob/version.
- Artifact = produced result/version.
- Entity = structured formal project fact/relation.
- Knowledge = interpreted/reference information + retrieval snapshot.

Do not collapse them into one JSON/vector abstraction.

Formal Entity updates produce immutable EntityVersions.

---

## 21. Workflow/provenance/approval are versioned

Formal output provenance captures applicable:

- Node/revision
- Skill/version
- Model
- ProviderConnection / ModelAvailability
- ExecutionProfile / Executor
- RuntimeConnection
- parameters
- input/Asset versions
- Entity versions
- KnowledgeSnapshot
- WorkflowVersion
- parent version
- actor/timestamp
- usage

Dependency changes mark prior formal outputs outdated; history remains.

Formal frozen output requires authorized human approval.

Agent/runtime may request approval but cannot approve/freeze its own output.

---

## 22. Agent mutation is proposal-first

Agent graph changes use a domain record such as `GraphProposal`.

Ghost nodes are UI projections, not formal NodeRecords.

Proposal application must verify `base_revision`.

If Canvas/project state changed, the proposal becomes stale and must be recomputed/rebased or re-confirmed; it is not auto-applied.

---

## 23. Audit and domain mutation should be atomic

For canonical persistence, domain mutation and its durable audit/outbox record should commit atomically whenever they belong to the same transaction.

Do not treat "persist succeeded, audit append failed" as a successful canonical mutation.

---

## 24. Package history is independently resolvable

Package kinds:

- system
- common
- industry

WholeHouse is industry.

Historical projects must not depend solely on currently installed package folders.

Use a `ProjectPackageLock` and/or immutable `DefinitionSnapshot` sufficient to resolve historical `definition_ref` values.

WorkspaceProfile is an experience layer only; it does not bypass authorization or remove compatible general capabilities.

---

## 25. MCP tool use is not automatically MCPExecutor

Distinguish:

- Codex/Agent invoking MCP tools inside an Agent loop
- a Workbench Skill whose execution route is a direct MCP action

These are separate semantics even if they share MCP infrastructure.

---

## 26. Executor endpoints are explicit

Executor type is not enough for multi-instance runtimes.

Examples:

- ComfyUI Mac mini
- GPU workstation
- RunningHub account

ExecutionProfile/executor configuration resolves through typed RuntimeConnections/ExecutorEndpoints rather than arbitrary UI strings.

---

## 27. Skill and ExecutionProfile requirements merge predictably

Effective requirements are:

`Skill base requirements + ExecutionProfile additional/narrowing requirements`

A profile may add or narrow requirements.

It must not silently relax mandatory Skill capabilities or permissions.

---

## 28. Capability vocabulary is versioned

Use one Core capability vocabulary such as:

`workbench.capability/1`

Provider adapters normalize provider-specific names into this vocabulary.

---

## 29. Codex App Server integration rules

When implementing App Server:

- inspect installed/target Codex version
- inspect official schema/protocol for that version
- record/pin the tested version
- prefer generated/validated bindings
- treat transport as Codex JSON-RPC-lite framed as JSONL over stdio
- isolate raw protocol behind `CodexBridge`
- preserve `codex exec` compatibility until separately removed
- normalize events/approvals into Workbench contracts
- never persist raw protocol payloads as domain truth

Changing the App Server integration contract requires a proposal.

### R1 launch policy

R1 proves transport/runtime integration, not unrestricted Agent authority.

R1 must define:

- bounded working directory
- environment/secret filtering
- shell/filesystem policy
- destructive approval policy
- timeout/cancellation
- no Workbench project mutation tools

---

## 30. Secrets/security

Secrets remain backend-only.

Never expose/persist/log raw provider secrets in browser/Canvas/Node/fixtures.

For changed surfaces check applicable:

- authentication
- project authorization/roles
- CORS/CSRF
- path/symlink containment
- upload/archive safety
- SSRF/network policy
- secret redaction
- subprocess/tool scope
- timeout/cancel
- destructive confirmation
- audit
- stale-write/concurrency behavior

LAN mode is not authenticated multi-user support unless those controls exist.

---

## 31. Legacy compatibility

Until replacement Gates pass preserve:

- current Canvas JSON readability
- required Classic/Smart compatibility paths
- provider execution
- ComfyUI
- RunningHub
- Prompt/LLM/Loop/Group/fixed-node behavior
- unknown Legacy fields
- current `codex exec`

Do not delete a Legacy node family without proposal/evidence.

Use strangler/adapters, not a big-bang rewrite.

---

## 31A. Legacy monolith responsibility freeze

The following files are Legacy compatibility surfaces:

- `main.py`
- `static/js/canvas.js`
- `static/js/smart-canvas.js`

From this point forward:

> **Legacy monoliths may lose responsibility, but they must not gain new Workbench business responsibility.**

They may:

- retain existing Legacy behavior during a verified migration window;
- call new application/domain/runtime services;
- host narrowly scoped compatibility adapters;
- perform bootstrap/composition/wiring;
- delegate page-level events into shared Workbench modules;
- shrink as responsibilities move behind stable boundaries.

They must not become the primary implementation location for any new Workbench capability.

New capabilities must be implemented in the appropriate modular boundary first, including:

- SkillRegistry / DefinitionResolver;
- ProviderRegistry / ProviderConnection / ModelRegistry / ModelAvailability;
- ExecutionProfile / ExecutorRegistry / ExecutionRuntime;
- Asset / Artifact / Entity / Knowledge runtime;
- Workflow / Approval / Handoff runtime;
- PackageRuntime / WorkspaceProfile;
- CodexBridge / Agent orchestration;
- WholeHouse or other Package behavior.

Do not implement a new capability in a Legacy monolith with the intention of "moving it later".

### Backend target

`main.py` should progressively converge toward:

```text
create_app()
register_routes()
wire_services()
startup / shutdown
narrow compatibility bootstrap
```

New backend business logic should live under appropriate `workbench/` or `packages/` modules.

`main.py` may import and register new routes/services, but it should not contain the primary implementation of those capabilities.

### Frontend target

New shared Workbench/Canvas behavior should live under modular shared boundaries such as:

`static/js/workbench/...`

or a later approved replacement frontend boundary.

Do not add new Workbench business branches to:

- `static/js/canvas.js`
- `static/js/smart-canvas.js`

Those files may delegate to shared modules while their responsibility shrinks.

### Round audit requirement

Every implementation Round must report a **Legacy responsibility delta**:

- Did `main.py` gain any new Workbench business responsibility?
- Did `static/js/canvas.js` gain any new Workbench business responsibility?
- Did `static/js/smart-canvas.js` gain any new Workbench business responsibility?
- Which responsibilities moved out of Legacy monoliths?

Expected result for the first three questions is **No**, unless an approved proposal explicitly documents a temporary compatibility exception and removal Gate.

A net increase in Legacy monolith responsibility is a Gate failure by default.

---

# Development rules

## 32. Gate method

Before implementation:

1. inspect HEAD/worktree
2. read current status
3. inspect affected code/tests
4. state compatibility contract
5. state non-goals
6. list expected files
7. identify focused tests
8. identify proposal-required changes

During implementation:

- smallest seam first
- preserve unrelated changes
- no broad high-risk reformat
- no duplicate domain path
- typed/versioned public boundaries
- structured errors
- secret-safe logging
- feature flags at service/runtime boundaries

After implementation:

1. focused tests
2. baseline tests
3. syntax/static checks
4. browser acceptance where applicable
5. Legacy load/save verification where applicable
6. update `CURRENT_EXECUTION_STATUS.md`
7. update `CURRENT_ARCHITECTURE.md` when verified facts changed
8. update plan facts only when verified
9. record exact next authorized Round + forbidden next actions

Do not execute multiple architecture Rounds in one task.

---

## 33. Proposal-required decisions

Write a proposal before:

- frontend framework replacement
- primary database strategy replacement
- incompatible NodeRecord change
- Codex App Server contract change
- Legacy node family deletion
- early Canvas compatibility removal
- large infrastructure dependency
- Agent auto-mutation by default
- Industry behavior in Core
- unjustified new renderer family

Proposal includes:

- Problem
- Constraints
- Options
- Recommendation
- Migration Cost
- Compatibility Impact
- Security Impact
- Rollback
- Acceptance Criteria

---

## 34. Definition of Done

Applicable items must pass:

- requested behavior complete
- Core/Package separation holds
- Skill/Model/ProviderConnection/Executor/Artifact separation holds
- persistence authority explicit
- schemas/contracts versioned where required
- compatibility tested or approved break documented
- security checks complete
- focused/baseline/static tests pass
- browser acceptance recorded where applicable
- docs/status match verified code
- no secret leak
- no accidental generated artifacts
- current Gate acceptance criteria verified
- Legacy responsibility delta reviewed and no unapproved monolith growth occurred

Do not mark a Gate complete merely because code exists.
