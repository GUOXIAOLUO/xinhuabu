# AI Workbench — Development Execution Plan V2.2.1

Status: active Gate program  
Method: incremental / strangler / evidence-based Gates  
V1 client: Web UI  
V1 product platform: macOS, Apple Silicon / arm64 first  
Primary Agent runtime: Codex Harness / App Server  
First Industry Package: WholeHouse  

This plan evolves V2.1 without restarting completed work. R0-R3 remain historical/completed evidence. The active Round remains whatever `docs/status/CURRENT_EXECUTION_STATUS.md` authorizes; planning changes do not authorize later implementation.

---

## Execution rules

For every architecture/behavior task:

1. read `AGENTS.md`;
2. read `docs/status/CURRENT_EXECUTION_STATUS.md`;
3. read `CURRENT_ARCHITECTURE.md`;
4. read `TARGET_ARCHITECTURE.md`;
5. read `MIGRATION_PLAN.md`;
6. read this file;
7. inspect affected source/tests;
8. execute exactly the currently authorized Round.

A Gate passes only after evidence.

Never rewrite current-state/status documents as though future V2.2.1 work already exists.

---

## Cross-round hard rules

1. One Unified Canvas.
2. SQLite is the V1 structured authority after controlled cutover.
3. `main.py`, `canvas.js`, `smart-canvas.js` may lose responsibility but not gain new Workbench business responsibility.
4. Workbench Runtime does not depend on a Git repository URL.
5. V1 product support is macOS-first; Core remains portable.
6. Codex is the primary Agent runtime, but Workbench does not depend on one exact Codex version.
7. Stable Codex App Server APIs are preferred; experimental APIs cannot be the only required V1 path.
8. Codex-discovered models must be normal ModelAvailability choices.
9. Codex Thread/Project state is not Workbench business authority.
10. WholeHouse remains an Industry Package.
11. No silent ModelAvailability/Executor fallback.
12. Agent mutation is typed/proposal-first.
13. Platform Engineering requirements apply across all Rounds.

---

## Round overview

| Round | Name | Primary result |
|---|---|---|
| R0 | Repository Truth + Architecture Refresh | live facts + repaired current-state docs |
| R1 | Codex App Server Client Foundation | safe CodexBridge transport/runtime foundation |
| R2 | Unified Canvas Convergence A | U2-U6 compatibility convergence |
| R3 | Project Identity + Canonical Canvas Persistence | Project/Canvas/SQLite/auth/audit foundation |
| R4 | Unified Canvas Cutover | U7 + SQLite cutover + duplicate runtime removal |
| R5 | Generic Node UX + Mutation | NodeShell V2 + Inspector + mutation contract |
| R6 | Port/Data + Definition + Prompt + Skill | typed data + dynamic resources |
| R7 | Provider + Model + Codex Projection | ModelAvailability + Codex/direct discovery |
| R8 | Execution Runtime + Integration Contracts | multi-route typed execution |
| R9 | Asset + Artifact + Asset Library + Catalog | durable resources + product/catalog foundation |
| R10 | Entity + Knowledge Runtime | structured facts + reproducible context |
| R11 | Workflow + Approval + Handoff | durable business process/governance |
| R12 | Package + Workspace + Integration Runtime | package lifecycle + shared resources + integrations |
| R13 | Common Capability Package | useful general Workbench |
| R14 | Codex Workbench Agent Integration | scoped tools + GraphProposal + Agent Panel |
| R15 | WholeHouse Vertical Slice | one real design path end-to-end |
| R16 | WholeHouse Expansion | approved V1 capability catalog |
| R17 | CAD/File Handoff + Real Project Validation | production-like design workflow validation |

---

# R0 — Repository Truth + Architecture Refresh

Historical purpose remains unchanged.

Verify current source/test truth, architecture/status accuracy, feature flags, authorities, Legacy monolith responsibility and security boundaries.

R0 does not implement target features.

Gate: current truth is explicit and exactly one next Round is authorized.

---

# R1 — Codex App Server Client Foundation

R1 historical foundation remains valid, but the target interpretation is clarified.

## Goal

Establish a safe App Server client boundary without Workbench mutation authority.

## Required design

```text
Workbench
-> CodexBridge / CodexRuntime boundary
-> official Codex App Server
```

R1 does not implement another Harness.

## Foundation concerns

- local executable resolution
- bounded cwd/workspace
- environment/secret filtering
- stdio JSONL transport
- initialize/initialized handshake
- Thread/Turn basics
- model/config discovery
- normalized events
- cancel/shutdown/recovery
- Codex Exec compatibility
- restrictive runtime policy
- no Workbench mutation tools

## Long-term compatibility rule

Recorded/tested Codex versions are diagnostics/evidence, not hard runtime equality requirements.

Stable App Server APIs are the default baseline.

Gate: transport/runtime foundation verified; no Workbench project mutation tools.

---

# R2 — Unified Canvas Convergence A

Historical purpose remains unchanged.

Complete shared graph/port/group interaction, unified rendering/NodeShell, unified creation catalog/application-service paths, compatibility execution adapters and one normal Canvas entry.

Do not implement final ExecutionRuntime or SQLite authority switch here.

Gate: U2-U6 proven; U7 remains R4.

---

# R3 — Project Identity + Canonical Canvas Persistence

Historical purpose remains unchanged.

Deliver:

- ProjectRecord / ProjectMember;
- CanvasRecord;
- logical revision;
- authorization;
- SQLite migrations/repositories;
- Legacy import/backfill/compare;
- authority state;
- transactional mutation + durable audit/outbox;
- rollback/reporting.

Canonical concurrency must converge on true logical revision semantics.

Gate: durable Project/Canvas foundation and migration evidence.

---

# R4 — Unified Canvas Cutover

## Goal

Complete U7 against R3 canonical authority.

**R4 completion requires removal of the Classic/Smart dual-runtime product architecture, not merely a unified Canvas entry URL. Smart Canvas capabilities that remain product-relevant must first migrate into shared Unified Canvas modules or bounded compatibility adapters before duplicate runtime removal.**

This remains the only active implementation priority until its Gate passes.

## Deliver

- source-record backup and checksum validation;
- true expected-revision conflict handling;
- fix any compatibility lost-update path before cutover;
- SQLite canonical Canvas authority enabled as normal runtime;
- workflow import/export parity;
- Unified Canvas default entry/runtime/catalog;
- old records import/read;
- remove product-visible Classic/Smart source distinction;
- remove duplicate Classic/Smart runtime/page/CSS after acceptance;
- retire migration flags whose purpose ends at R4;
- 100/300-node verification;
- restart/read/write/conflict/rollback verification.

## Repository independence cleanup allowed in R4

Remove/disable Legacy product self-update responsibility that depends on a Git repository URL.

Do not merely replace an old repository URL with a new one.

## Forbidden

- PromptRegistry implementation;
- Catalog/Product implementation;
- R7 Model Registry;
- R8 ExecutionRuntime;
- WholeHouse business features.

Gate:

```text
one user-visible Canvas entry
+ one canonical Canvas persistence authority
+ one product Canvas runtime
+ one shared interaction/render/creation system
+ no permanent Classic/Smart product modes
+ no duplicate Classic/Smart product runtime
+ retained Smart capabilities migrated before runtime removal
+ verified conflict semantics
+ rollback evidence
```

A unified entry URL alone does not satisfy the R4 Gate.

---

# R5 — Generic Node UX + Mutation

## Goal

Make the Unified Canvas a generic task-oriented Workbench surface.

## Deliver

- NodeShell V2;
- Inspector;
- NodeMutationService expansion;
- typed editing seam for InputBindings;
- ModelAvailability selection editing;
- execution-profile/route editing;
- branch/materialization/next-step intent seams.

## UX target

NodeShell five regions:

1. task/status;
2. inputs;
3. main content/result;
4. Skill/Prompt/Model/Execution;
5. actions/output.

Advanced implementation details remain in Inspector.

Gate:

- no new raw mutation path;
- no provider/WholeHouse/Codex protocol branches in Canvas;
- all generic renderers share NodeShell.

---

# R6 — Port/Data + Definition + Prompt + Skill

## Goal

Prove dynamic resources independent from fixed Canvas code.

## Deliver

- PortTypeRegistry;
- typed InputBinding;
- Collection;
- CompatibilityResolver foundation;
- DefinitionResolver;
- PromptDefinition;
- PromptVersion;
- PromptRegistry;
- PromptService;
- Workbench Skill manifest;
- SkillRegistry;
- Skill Library;
- Workbench Skill vs Codex Skill separation;
- one `common.image-analysis` proof.

## Prompt proof

A Prompt can be discovered, versioned, referenced by a Skill/Workflow and represented on Canvas without provider-specific Canvas code.

## Skill proof

A conforming Skill:

- is discovered/listed;
- resolves through DefinitionResolver;
- creates through NodeCreationService;
- renders through RendererRegistry/NodeShell;
- validates typed bindings;
- survives restart.

Actual target execution remains R8.

---

# R7 — Provider + Model + Codex Projection

## Goal

Make ModelAvailability the canonical user-facing model-route selection layer.

## Deliver — provider/model

- ProviderDefinition;
- ProviderConnection;
- CredentialRef;
- ProviderRegistry;
- ModelDefinition;
- normalized capability vocabulary;
- ModelRegistry;
- ModelAvailability;
- ModelCompatibilityService;
- direct-provider discovery;
- API Center backend;
- Model Picker;
- NodeRecord v1 availability-extension migration.

## ModelAvailability v2 direction

Support neutral route identity:

```text
route_type = provider | runtime
route_ref
executor_type
```

This allows:

```text
GPT-X · OpenAI API
GPT-X · Codex Harness
```

to coexist without pretending Codex is a ProviderConnection.

## Deliver — Codex compatibility/projection

Introduce/strengthen:

```text
CodexExecutableResolver
AppServerProcess
CodexProtocolClient
CodexProtocolCompatibility
CodexProjectionService
CodexEventNormalizer
```

R7 compatibility work must:

- inspect installed Codex version;
- verify current official stable App Server schema;
- regenerate/compare protocol schema where used;
- verify initialize/initialized;
- verify Thread/Turn basics;
- verify `model/list`;
- verify config/account/skills discovery used by this Round;
- keep stdio as V1 transport;
- treat experimental API as optional;
- update the recorded tested version without requiring exact equality.

## CodexBridge hardening

Before R7 Gate:

- drain stderr;
- fail pending requests on unexpected EOF;
- bound event queues;
- handle overload `-32001` with bounded retry/backoff where appropriate;
- replace generic server-request decline with typed dispatch;
- normalize Thread/Turn/Item/server-request events;
- use generated/validated DTOs where practical;
- identify the client as Xinhuabu Workbench.

## Codex projection

Examples:

```text
model/list -> ModelDefinition / ModelAvailability
skills/list -> CodexSkillAvailability
provider/runtime capability data -> normalized capability projection
account/config -> runtime diagnostics
```

No Codex Project/Thread record becomes Workbench business authority.

## Gate B

For one Skill:

- at least two compatible ModelAvailabilities can be discovered/filtered where environment permits;
- a Codex-discovered availability can appear in the same Model Picker as direct-provider availability;
- selection persists/reloads;
- incompatibility reason is explainable;
- no silent route fallback;
- NodeRecord v1 remains readable.

Execution is R8.

---

# R8 — Execution Runtime + Integration Contracts

## Goal

Prove:

```text
Skill
+ Prompt
+ ModelAvailability
+ ExecutionProfile
+ Executor
```

## Deliver

- ExecutionProfile;
- RuntimeConnection / ExecutorEndpoint;
- ExecutorRegistry;
- CodexHarnessExecutor;
- ModelApiExecutor;
- ComfyUIExecutor;
- RunningHubExecutor;
- ScriptExecutor;
- MCPExecutor;
- ExecutionPolicy;
- ExecutionRun / ExecutionAttempt / ExecutionEvent;
- timeout/cancel/partial-result/usage;
- explicit executor capabilities;
- requirement merge rules;
- IntegrationDefinition;
- IntegrationConnection;
- IntegrationRegistry foundation.

## CodexHarnessExecutor rule

Keep it thin. It may:

- resolve Skill/Prompt/ModelAvailability;
- attach Codex Skill/context;
- start/resume Thread;
- start Turn;
- normalize output;
- materialize ArtifactVersion.

It must not reimplement:

- Agent loop;
- Codex tool loop;
- Codex MCP runtime;
- subagent framework;
- Codex authentication.

## Gate C

Same Workbench Skill:

- executes through a Codex Harness ModelAvailability where available;
- executes through at least one compatible non-Codex route where available;
- produces the same typed output contract;
- records requested/actual model, route, runtime, executor and profile;
- proves cancel or explicit unsupported-cancel;
- durable run state survives the designed restart/disconnect scenario.

---

# R9 — Asset + Artifact + Asset Library + Catalog

## Deliver

- BlobRef;
- Asset / AssetVersion;
- Artifact / ArtifactVersion;
- Collection persistence;
- provenance/dependency/freshness;
- Asset Library UX/API;
- Catalog;
- CatalogCategory;
- CatalogEntry;
- CatalogService;
- authorized delivery URLs.

## Asset Library

Support workspace/project Assets, search, tags, collections/favorites as product UX evolves.

## Catalog

Catalog is generic.

WholeHouse products are not Core ProductRecord special cases.

Gate:

- old versions preserved;
- rerun produces versioned result;
- Catalog survives restart;
- Workspace/Project scope is representable.

---

# R10 — Entity + Knowledge Runtime

## Deliver

Entity:

- Entity definitions/properties/relations;
- EntityRecord;
- immutable EntityVersion;
- authorization/audit.

Knowledge:

- sources/scopes;
- retrieval contract;
- KnowledgeSnapshot/evidence.

Gate:

- formal Entity mutation creates EntityVersion;
- formal execution captures KnowledgeSnapshot where applicable.

---

# R11 — Workflow + Approval + Handoff

## Deliver

- WorkflowDefinition / WorkflowVersion / WorkflowRun;
- NodeRun;
- retry/cancel/pause;
- import/export/compare;
- Workflow-as-Node/composite representation;
- ApprovalRequest / ApprovalDecision;
- Frozen formal version;
- generic Handoff manifest/checksums.

Keep Codex runtime approval separate from Workbench business approval.

Gate:

- restartable workflow;
- authorized human freeze;
- frozen version immutable;
- generic handoff validates.

---

# R12 — Package + Workspace + Integration Runtime

## Deliver

- PackageRegistry;
- package manifest/lifecycle;
- dependency checks;
- ProjectPackageLock;
- DefinitionSnapshot;
- package migrations;
- Workspace resource scope;
- WorkspaceProfile;
- Integration Runtime;
- Native API / MCP / Local Bridge / File Handoff / Human Handoff seams.

Codex Apps/MCP are projected where useful rather than reimplemented.

Gate:

- package lock/version persists;
- historical DefinitionRefs remain resolvable;
- shared workspace resources work across projects;
- one non-model Integration can be represented through the generic contract.

---

# R13 — Common Capability Package

## Goal

Prove useful general Workbench without WholeHouse.

Candidates:

- image/document analysis;
- structured extraction;
- text generation;
- image generation/edit;
- video generation;
- comparison;
- code/repository analysis;
- research.

Gate: WholeHouse can be absent while Canvas/Prompt/Skill/Model/Codex/API/Asset/Artifact/Entity/Knowledge/Workflow remain useful.

---

# R14 — Codex Workbench Agent Integration

## Goal

Expose Workbench domain capabilities safely to Codex Harness.

This Round does not build another Agent Harness.

## Deliver

- WorkbenchToolContract;
- CodexWorkbenchToolBridge;
- stable MCP adapter or another approved stable bridge;
- optional DynamicTool adapter only when treated as experimental;
- Agent Panel;
- GraphProposal;
- stale/rebase policy;
- CodexSessionLink where useful.

## Tool examples

- project.read;
- canvas.get_context;
- asset.search/read;
- catalog.search/read;
- prompt.read;
- skill.search/resolve;
- compatibility.resolve;
- workflow.read;
- execution.get;
- artifact.read;
- graph.propose;
- approval.request.

Every tool routes through Application Services.

## Gate D

```text
select Asset
-> Codex reads scoped Workbench context
-> CompatibilityResolver
-> Skill/model/executor proposal
-> GraphProposal
-> user confirmation
-> revision check
-> application services mutate
-> ExecutionRuntime
-> ArtifactVersion
-> Canvas result
```

No raw DOM/DB/project JSON mutation.

---

# R15 — WholeHouse Vertical Slice

## End-to-end slice

```text
Project Intake
-> Requirement Analysis
-> Floorplan Analysis
-> Space Entity
-> Space Concept
-> Product / Material Selection
-> Render
-> Design Review
-> Approval / Frozen
-> CAD/File Handoff
```

WholeHouse uses generic:

- Prompt;
- Skill;
- Asset;
- Catalog;
- Entity;
- Workflow;
- Approval;
- Handoff;
- ModelAvailability;
- ExecutionRuntime.

No WholeHouse branch is added to Canvas/Model/Executor Core.

---

# R16 — WholeHouse Expansion

Candidates:

- site photo analysis;
- reference analysis;
- style direction;
- cabinet concept;
- material proposal;
- product selection;
- render;
- image edit;
- version compare;
- pending-issues review;
- CAD review.

V1 still excludes:

- production/CNC;
- installation;
- after-sales.

---

# R17 — CAD/File Handoff + Real Project Validation

Use real studio work:

- real customer;
- real floorplan;
- real product/material/hardware catalog;
- real images/renders;
- real CAD;
- real Kujiale/GuiGui file handoff.

Validate:

- restart/recovery;
- backup/restore;
- Codex compatibility after supported local update;
- Codex/direct API node routes;
- ModelAvailability persistence;
- provenance/version/outdated;
- Workflow;
- Approval/Frozen;
- Package history;
- Handoff checksum/readiness;
- 100/300-node Canvas behavior.

Direct Agent control of Kujiale/GuiGui is not required for V1 acceptance.

---

# WholeHouse parallel validation track

Use WholeHouse as an acceptance scenario throughout without moving business logic into Core.

| Round | WholeHouse validation |
|---|---|
| R4 | real project Canvas migration/open/save |
| R5 | space/task Node UX |
| R6 | Prompt/Skill/Data contracts |
| R7 | Codex/direct API Model Picker |
| R8 | same Skill through multiple routes |
| R9 | CAD/photo/render/product resources |
| R10 | Customer/Room/Space/Product facts |
| R11 | design Workflow/Approval/Handoff |
| R12 | WholeHouse Package + shared resources |
| R14 | Agent GraphProposal |
| R15 | full vertical slice |

---

# Platform Engineering track

Applies to every Round.

## Settings

Move new configuration behind typed settings groups.

## Migration

Use versioned MigrationRunner rather than indefinite ad-hoc startup repairs.

## Storage

Domain uses BlobRef; V1 LocalBlobStore, future NAS/object adapters.

## Durable events

Long-running execution/workflow state must not live only in browser memory/WebSocket connection objects.

## Backup

Provide backup/verify/restore/dry-run restore for formal Workbench data.

## Feature flags

Every migration flag declares its removal Gate.

## Schema/API

Prefer Pydantic -> JSON Schema -> OpenAPI -> frontend types.

## Quality gates

Add CI, lint/type/coverage/dependency checks and architecture guards incrementally.

## Architecture guards

Eventually reject:

- new Workbench business systems in Legacy monoliths;
- provider/Codex/WholeHouse branching in Canvas;
- Codex protocol DTOs in Core;
- Agent raw DB/DOM/JSON mutation;
- runtime dependency on Git repository URL;
- required V1 feature depending only on experimental Codex API.

---

# Mac-first product rule

V1 official product/runtime target:

```text
macOS
Apple Silicon / arm64 first
```

Core remains portable.

Windows support is future work through infrastructure/release adapters, not a current Gate.
