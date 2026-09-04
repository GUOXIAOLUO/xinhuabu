# Target Architecture — AI Workbench V2.1

## 1. Objective

Build a Web UI first generic AI Workbench on top of the existing `GUOXIAOLUO/canvas` strengths.

Codex Harness / App Server is the primary Agent/orchestration runtime target.

Codex/OpenAI models are also ordinary user-selectable Node model choices.

WholeHouse is the first deep Industry Package, not the Core.

The target introduces explicit contracts for:

- Project identity / authorization
- Canvas identity / revision
- Node creation / mutation / definition resolution
- Port/Data binding
- Skill
- ProviderDefinition / ProviderConnection
- Model / ModelAvailability
- ExecutionProfile / Executor / RuntimeConnection
- Asset / Artifact / Entity / Knowledge
- Workflow / Approval / Handoff
- GraphProposal
- Package lock / definition snapshots
- persistence / audit / migration

---

## 2. Non-negotiable outcomes

1. Core starts and supports useful general projects without WholeHouse.
2. One Unified Canvas product runtime remains after migration.
3. Canvas does not branch on business Skill IDs.
4. A conforming Skill can be discovered/created/rendered without Canvas source edits.
5. Model, ProviderDefinition, ProviderConnection, ModelAvailability and Executor are separate.
6. Codex-discovered models can be selected like other compatible models.
7. Codex Harness can be system Orchestrator and one execution route.
8. User-selected model/provider/executor routes are never silently replaced.
9. Agent changes project state through typed services/tools, never DOM/raw JSON.
10. Project/domain persistence is authoritative, not Codex Threads.
11. Asset, Artifact, Entity and Knowledge remain distinct.
12. Formal output/workflow/provenance/approval is versioned.
13. Frozen authority applies to immutable formal versions and requires human approval.
14. Legacy nodes remain readable/executable during migration.
15. Secrets remain server-side.
16. Package disable/uninstall does not destroy historical project readability.
17. WholeHouse WorkspaceProfile does not remove general compatible capabilities.
18. Canonical domain mutation + durable audit is atomic.
19. Canonical revision numbers are not timestamp aliases.

---

## 3. Logical architecture

```text
Browser Web UI
├── Projects
├── Unified Canvas
├── Inspector
├── Resources
│   ├── Skills
│   ├── Models & API Connections
│   ├── Executors / ComfyUI
│   ├── MCP / Tools
│   ├── Workflows
│   ├── Knowledge
│   └── Assets
└── Agent Panel
        │
        ▼
FastAPI API
├── Auth / Project authorization
├── Canvas commands / queries
├── Asset / Artifact / Entity / Knowledge APIs
├── Workflow / Approval / Handoff APIs
└── Agent / Execution events
        │
        ▼
Application services
├── ProjectService
├── AuthorizationService
├── DefinitionResolver
├── NodeCreationService
├── NodeMutationService
├── GraphMutationService
├── CompatibilityResolver
├── SkillService
├── ModelCompatibilityService
├── ExecutionService
├── AssetService
├── ArtifactService
├── EntityService
├── KnowledgeService
├── WorkflowService
├── ApprovalService
├── HandoffService
└── ProposalService
        │
        ▼
Core records
├── ProjectRecord / ProjectMember
├── CanvasRecord
├── NodeRecord / EdgeRecord
├── InputBinding / Port contracts
├── Asset / AssetVersion / BlobRef
├── Artifact / ArtifactVersion / Collection
├── Entity / EntityVersion / Relation
├── KnowledgeRecord / KnowledgeSnapshot
├── ExecutionRun / Attempt / Event
├── WorkflowDefinition / Version / Run
├── Approval / Frozen
├── GraphProposal
└── Handoff
        │
        ▼
Registries / runtimes
├── RendererRegistry
├── PortTypeRegistry
├── SkillRegistry
├── ProviderRegistry
├── ProviderConnectionRegistry
├── ModelRegistry
├── ModelAvailabilityRegistry
├── ExecutorRegistry
├── PackageRegistry
├── CodexBridge
└── MCP / Tool runtime
        │
        ▼
Infrastructure
├── SQLite -> later PostgreSQL
├── local files -> later NAS/object storage
├── provider adapters
├── ComfyUI / RunningHub adapters
├── Codex App Server
├── migration runner
├── durable audit/outbox
└── Legacy JSON adapters
```

---

# Canonical identity and persistence

## 4. ProjectRecord

Draft:

```json
{
  "schema_version": "workbench.project/1",
  "id": "project_01",
  "name": "Project",
  "workspace_id": "local",
  "created_by": "actor_01",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "revision": 1,
  "metadata": {}
}
```

Project is the ownership, authorization and persistence boundary.

Initial roles:

- Owner
- Editor
- Viewer

Long-term authorization is action/resource based.

---

## 5. Legacy Project identity migration

Legacy Canvas may contain:

```json
{
  "project": "default",
  "owner": ""
}
```

R3 must define and test an explicit migration:

- a stable local workspace actor;
- a stable default ProjectRecord;
- mapping of existing non-empty owner values;
- mapping of unowned local Canvases without inventing remote identity;
- rollback/export mapping.

Migration reports identity/ownership changes.

---

## 6. CanvasRecord

Draft:

```json
{
  "schema_version": "workbench.canvas/1",
  "id": "canvas_01",
  "project_id": "project_01",
  "title": "Canvas",
  "viewport": {"x": 0, "y": 0, "scale": 1},
  "revision": 12,
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "metadata": {}
}
```

Rules:

- `revision` is monotonic logical concurrency authority.
- `updated_at` is display/audit time.
- Classic/Smart `kind` is Legacy migration metadata, not final user identity.
- CanvasRecord is canonical graph-container identity.

---

## 7. SQLite authority

V1 structured authority is SQLite behind repositories.

Migration:

1. expand
2. backfill
3. compare
4. compatibility read
5. controlled switch
6. verification
7. contract Legacy writes later

Canonical mutation + durable audit/outbox commit atomically.

Changing database strategy requires proposal approval.

---

# Canvas and Node contracts

## 8. NodeRecord v1

Current NodeRecord v1 remains the migration basis.

Core kind vocabulary remains compatible:

- asset
- skill
- artifact
- entity
- task
- approval
- group
- composite
- legacy

Business meaning comes from `definition_ref`, not `kind`.

---

## 9. ModelBinding v1 migration

Current v1 fields:

```text
selection_mode
provider_id
model_id
parameters
```

and current code requires provider/model together.

Migration contract:

- `model_id` = selected canonical model identity or compatibility mapping.
- `provider_id` = current Legacy/provider-connection compatibility ID required by v1.
- canonical ModelAvailability identity is carried in `extensions["workbench.model_availability"]`.

Example:

```json
{
  "model_binding": {
    "selection_mode": "user",
    "provider_id": "provider_legacy_01",
    "model_id": "openai/model-x",
    "parameters": {}
  },
  "extensions": {
    "workbench.model_availability": {
      "availability_id": "availability_01"
    }
  }
}
```

Do not reinterpret stored `provider_id` without migration/versioning.

A later proposal may define a stable ModelSelectionBinding v2.

---

## 10. Execution binding migration

Until R8 proves the contract:

```json
{
  "extensions": {
    "workbench.execution": {
      "profile_id": "codex-deep",
      "executor_type": "codex_harness",
      "runtime_connection_id": null
    }
  }
}
```

A stable NodeRecord v2 field requires proposal approval.

---

## 11. Node / Execution / Freshness / Governance states

### NodeState

Existing projection vocabulary remains compatible.

### ExecutionRunState

Target:

```text
created
queued
running
waiting_user
waiting_approval
completed
failed
cancelled
interrupted
timed_out
```

### Artifact freshness

```text
current
outdated
```

### Governance

Approval/Frozen is authoritative on formal immutable versions.

Node `outdated` / `frozen` is a UI projection.

---

## 12. DefinitionResolver

```text
DefinitionResolver.resolve(DefinitionRef)
  -> ResolvedNodeDefinition
```

Delegates may include:

- SkillRegistry
- LegacyDefinitionRegistry
- Entity definition registry
- Workflow/composite definitions
- Package historical DefinitionSnapshot store

Core does not import WholeHouse implementation.

---

## 13. NodeCreationService

All migrated creation sources use NodeCreationService:

- context menu
- Command-K
- Skill Library
- file drop
- workflow import
- compatible next step
- Agent proposal
- Legacy adapter

It enforces applicable authorization, definition resolution, renderer resolution, typed bindings, model compatibility, idempotency, revision and audit.

---

## 14. NodeMutationService

Canonical mutation boundary for applicable:

- title
- position/size
- InputBindings
- model binding
- model availability extension
- execution extension
- config
- compatible definition replacement

Enforces authorization, expected revision, compatibility, audit and outdated propagation.

---

## 15. GraphMutationService

Owns atomic graph changes such as:

- create node + edge
- proposal application
- graph/group operations
- workflow import batches

Proposal application re-checks base revision.

---

## 16. RendererRegistry

Finite target vocabulary:

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

---

# Typed data contracts

## 17. PortTypeRegistry

Replaces the Artifact-only registry name.

Examples:

```text
asset.image
asset.video
asset.pdf
asset.document
artifact.text
artifact.analysis
artifact.image
artifact.video
artifact.table
artifact.comparison
artifact.review
artifact.handoff
entity.ref
entity.version
collection.ref
literal.json
```

A type definition may contain ID/version, schema ref, compatibility/inheritance, cardinality and renderer hints.

---

## 18. InputBinding

Draft:

```json
{
  "schema_version": "workbench.input-binding/1",
  "port_id": "source",
  "source_type": "asset_version",
  "source_ref": "asset_version_01",
  "index": 0,
  "metadata": {}
}
```

Initial categories:

- asset_version
- artifact_version
- entity_ref
- entity_version
- collection
- literal

KnowledgeSnapshot normally belongs to execution context.

Current NodeRecord v1 may persist dict form during migration, but new code validates/constructs through the typed contract.

---

## 19. Collection

Collection is typed multi-item data semantics and is independent from Canvas Group.

A Collection may reference ordered AssetVersion, ArtifactVersion or EntityVersion items.

---

## 20. CompatibilityResolver

One service powers human and Agent compatibility flows.

Inputs may include:

- source PortType
- destination contract/cardinality
- Skill/Package enabled state
- authorization
- model capability/availability
- executor availability
- project state
- WorkspaceProfile ranking

Outputs include compatibility, reasons, missing prerequisites and ranking.

---

# Skill contracts

## 21. Workbench Skill

A Workbench Skill is a product capability definition.

A Codex `SKILL.md` is an optional implementation used by a Codex execution profile.

---

## 22. Skill manifest V2

Draft:

```json
{
  "schema_version": "workbench.skill-manifest/2",
  "id": "common.image-analysis",
  "name": "Image Analysis",
  "version": "1.0.0",
  "renderer": {"id": "analysis", "version": "1"},
  "inputs": [
    {"id": "source", "types": ["asset.image"], "required": true, "multiple": false}
  ],
  "outputs": [
    {"id": "analysis", "types": ["artifact.analysis"], "multiple": false}
  ],
  "model_requirements": {
    "capabilities": ["vision", "structured_output"]
  },
  "permissions": ["asset.read", "artifact.write"],
  "execution_profiles": [
    {
      "id": "codex-deep",
      "display_name": "Deep analysis",
      "executor_type": "codex_harness",
      "implementation": {
        "type": "codex_skill",
        "entrypoint": "SKILL.md"
      }
    },
    {
      "id": "direct",
      "display_name": "Direct",
      "executor_type": "model_api",
      "implementation": {
        "type": "prompt_template",
        "entrypoint": "references/prompt.md"
      }
    }
  ]
}
```

SkillDefinition is immutable per version.

---

## 23. Requirement merge rule

Effective requirements:

`Skill base requirements + ExecutionProfile additional/narrowing requirements`

Profile requirements cannot relax mandatory Skill capabilities or permissions.

---

## 24. SkillRegistry

Supports:

- discover
- list
- search
- get
- enable
- disable
- reload
- diagnostics/quarantine

R6 proves discovery/create/render/restore only.

Actual unified execution proof belongs to R8.

---

# Provider and Model

## 25. ProviderDefinition

Represents adapter/protocol family, not one user's account.

Fields may include:

- ID/display name
- adapter/protocol kind
- connection config schema
- discovery support
- capability hints

---

## 26. ProviderConnection

Represents one configured account/endpoint.

```json
{
  "schema_version": "workbench.provider-connection/1",
  "id": "connection_01",
  "provider_id": "openai",
  "display_name": "My OpenAI",
  "credential_ref": "credential_01",
  "endpoint": null,
  "enabled": true,
  "status": "available",
  "metadata": {}
}
```

Secrets remain behind CredentialRef.

---

## 27. ModelDefinition

```json
{
  "schema_version": "workbench.model/2",
  "id": "openai/model-x",
  "family": "model-x",
  "display_name": "Model X",
  "capabilities": ["reasoning", "vision", "structured_output", "tool_use"],
  "input_modalities": ["text", "image"],
  "output_modalities": ["text", "json"],
  "parameter_schema": {},
  "metadata": {}
}
```

---

## 28. Capability vocabulary

Core normalized vocabulary is versioned, e.g. `workbench.capability/1`.

Provider-native capability names are normalized by adapters.

---

## 29. ModelAvailability

```json
{
  "schema_version": "workbench.model-availability/1",
  "id": "availability_01",
  "model_ref": "openai/model-x",
  "provider_connection_id": "connection_01",
  "executor_types": ["model_api"],
  "enabled": true,
  "status": "available",
  "constraints": {},
  "metadata": {}
}
```

Same Model may have several availabilities.

Codex-discovered availability may use `codex_harness`.

---

## 30. ModelCompatibilityService

Combines:

- Skill requirements
- ExecutionProfile requirements
- Model capabilities
- ModelAvailability
- selected Executor
- project/user policy

R7 proves discover/filter/select/persist.

Execution proof belongs to R8.

---

## 31. API Center

Backend becomes authority for:

- ProviderDefinitions
- ProviderConnections
- credential presence
- model discovery
- model capability metadata
- ModelAvailability
- connection health

Browser hard-coded lists retire only after parity.

---

# Execution

## 32. ExecutionProfile

Draft:

```json
{
  "schema_version": "workbench.execution-profile/1",
  "id": "codex-deep",
  "display_name": "Deep analysis",
  "executor_type": "codex_harness",
  "runtime_connection_id": null,
  "model_requirements": {},
  "parameter_schema": {},
  "permissions": [],
  "capabilities": {
    "streaming": true,
    "cancel": true,
    "pause": false,
    "batch": false
  }
}
```

---

## 33. RuntimeConnection / ExecutorEndpoint

Multi-instance runtimes use typed connections.

Examples:

- ComfyUI Mac mini
- ComfyUI GPU workstation
- RunningHub account
- local script sandbox

---

## 34. ExecutorRegistry

Initial target executors:

- CodexHarnessExecutor
- ModelApiExecutor
- ComfyUIExecutor
- RunningHubExecutor
- ScriptExecutor
- MCPExecutor

Normalized contract:

- validate
- start
- events/poll
- cancel where supported
- status
- partial result
- final result
- errors
- usage

Capabilities are explicit.

---

## 35. MCP semantics

Distinguish:

1. Agent/Codex calls MCP tools inside an Agent loop.
2. A Workbench Skill uses a direct MCP execution profile.

---

## 36. ExecutionPolicy

Batch/Loop semantics:

```json
{
  "mode": "batch",
  "item_selector": "input.references",
  "parallelism": 4,
  "retry": {"max_attempts": 2},
  "failure_policy": "continue"
}
```

Legacy Loop remains compatible until migrated.

---

## 37. Execution records

### ExecutionRun
One logical run.

### ExecutionAttempt
One concrete attempt.

### ExecutionEvent
Append-only normalized events:

- queued
- started
- progress
- partial_result
- tool_activity
- waiting_user
- waiting_approval
- usage
- completed
- failed
- cancelled
- interrupted
- timed_out

---

# Asset / Artifact / Entity / Knowledge

## 38. Asset
Logical owned file.

## 39. AssetVersion
Immutable content version.

## 40. BlobRef
Storage pointer.

## 41. Artifact
Logical produced result.

## 42. ArtifactVersion
Immutable formal result version.

Formal output references version IDs, not only URLs.

---

## 43. Artifact materialization

ArtifactVersion existence is independent of visible Node presence.

Intermediate results may remain non-materialized.

---

## 44. Entity Runtime

Core defines:

- EntityTypeDefinition
- PropertyDefinition
- RelationTypeDefinition
- EntityRecord
- EntityVersion
- EntityRelation

Formal Entity updates create immutable EntityVersions.

Industry Packages register namespaced definitions.

---

## 45. Knowledge Runtime

Scopes:

- System
- Common
- Industry
- Company
- Project
- User

Retrieval may combine exact/metadata, full text, vector, structured query, entity traversal and reranking.

Formal execution records exact KnowledgeSnapshot.

---

# Workflow / Governance / Agent

## 46. Workflow Runtime

Records:

- WorkflowDefinition
- WorkflowVersion
- WorkflowRun
- NodeRun

Supports create/version/duplicate/run/retry/cancel/import/export/compare and pause/resume where executor support exists.

---

## 47. Provenance and outdated

Formal ArtifactVersion provenance records applicable:

- Node/revision
- Skill/version
- Model
- ProviderConnection/ModelAvailability
- ExecutionProfile/Executor
- RuntimeConnection
- parameters
- InputBindings
- Asset versions
- Entity versions
- KnowledgeSnapshot
- WorkflowVersion
- parent version
- actor/timestamps
- usage

Changing dependencies marks dependent formal versions outdated.

---

## 48. Approval and Frozen

Approval targets a formal version.

Fields include action, target, requester, eligible reviewers, decision, reason, timestamps and audit refs.

Frozen authority applies to approved immutable formal version.

Node frozen state is a projection.

Agent/provider runtime cannot approve/freeze its own output.

---

## 49. Handoff Runtime

Core owns:

- manifest
- referenced version set
- checksums
- export package
- validation
- creator/approver
- timestamps

WholeHouse owns handoff schema/content expectations.

---

## 50. GraphProposal

```json
{
  "schema_version": "workbench.graph-proposal/1",
  "id": "proposal_01",
  "project_id": "project_01",
  "canvas_id": "canvas_01",
  "base_revision": 12,
  "proposed_nodes": [],
  "proposed_edges": [],
  "proposed_mutations": [],
  "reason": "Analyze selected image",
  "created_by": "agent_task_01",
  "status": "pending",
  "approval_id": null
}
```

Rules:

- ghost nodes are UI projections;
- apply only after base-revision check;
- stale proposals require recompute/rebase/reconfirmation;
- accepted application is atomic and audited.

---

# Codex Harness

## 51. CodexBridge

Responsibilities:

- start/initialize
- health/version
- Thread lifecycle supported by target version
- Turn start/cancel
- normalized events
- approval round trip
- model/config discovery
- reconnect/recovery
- shutdown
- bounded context
- scoped Workbench tools

Protocol boundary:

Codex JSON-RPC-lite request/response/notification protocol framed as JSONL over stdio.

Use tested Codex schema/version and generated/validated bindings where practical.

`codex exec` remains compatibility until separately retired.

---

## 52. R1 HarnessLaunchPolicy

R1 defines:

- tested Codex version
- bounded cwd/workspace
- environment allowlist
- secret filtering
- filesystem/shell policy
- destructive approval policy
- timeout/cancel
- child-process lifecycle
- no Workbench mutation tools

R1 proves transport/runtime integration only.

---

## 53. Agent Workbench tools

Later project-scoped tools may include:

- canvas.get_context
- canvas.get_selection
- canvas.node.get
- skill.search/get
- model.list_compatible
- asset.get
- artifact.get
- entity.search/get
- knowledge.search
- workflow.get/propose
- execution.start/get/cancel
- proposal.submit
- approval.request

No DOM/raw database mutation tools.

---

# Package architecture

## 54. Package Runtime

Kinds:

- system
- common
- industry

Manifest contains package ID/version, Workbench compatibility, dependencies, permissions, migrations and registrations.

Lifecycle:

- discover
- install
- enable
- disable
- upgrade
- uninstall with dependency analysis

---

## 55. ProjectPackageLock / DefinitionSnapshot

Historical project readability must not depend solely on installed package folders.

Persist applicable:

- package ID/version
- manifest snapshot/hash
- immutable DefinitionSnapshots needed by persisted DefinitionRefs
- migrations applied

Disable/uninstall blocks new usage according to policy but does not erase required history.

---

## 56. WorkspaceProfile

May influence:

- ranking/defaults
- Agent instructions
- Knowledge scopes
- templates
- Inspector sections
- preferred Model/Execution defaults

It does not change domain compatibility, bypass authorization or remove compatible general capabilities.

---

## 57. Common Package

`packages/common/` proves general capability before WholeHouse.

Candidates:

- image analysis
- document analysis
- structured extraction
- text generation
- image generation/edit
- video generation
- comparison
- code/repository analysis
- research when ready

---

## 58. WholeHouse Package

Location:

`packages/wholehouse/`

Registers:

- Skills
- Entities
- Knowledge
- Workflows
- templates
- review/handoff rules

V1 includes design optimization and CAD/file handoff readiness.

V1 excludes production/CNC, installation, after-sales and direct Agent control of Kujiale/GuiGui.

---

## 59. First generic proof

1. create/open generic Project
2. drop image
3. AssetVersion created
4. Asset Node created
5. `common.image-analysis` dynamically discovered
6. user creates Skill Node
7. compatible models/availabilities shown
8. user selects ModelAvailability + ExecutionProfile
9. ExecutionRuntime runs
10. ArtifactVersion created
11. optional Artifact Node materialized
12. workflow/project saved
13. restart restores state/provenance
14. Codex Agent later proposes equivalent graph
15. user confirms
16. same application services execute

This proves the platform before WholeHouse scale-up.

---

## 60. Legacy monolith shrink target

The migration is not complete merely because new modular Workbench code exists beside the old monoliths.

The following Legacy surfaces have a one-way responsibility rule:

```text
main.py
static/js/canvas.js
static/js/smart-canvas.js
```

Their responsibility set must trend downward over time.

### Backend target

`main.py` converges toward a composition/bootstrap role:

```text
create_app()
  -> construct FastAPI application

register_routes()
  -> attach modular API routers

wire_services()
  -> construct repositories, registries, runtimes and application services

startup / shutdown
  -> process lifecycle

compatibility bootstrap
  -> narrowly scoped Legacy adapters during migration
```

Target business implementation lives behind modular boundaries such as:

```text
workbench/api/
workbench/application/
workbench/domain/
workbench/repositories/
workbench/runtimes/
packages/
```

A new Workbench domain/runtime should not be implemented in `main.py` first and extracted later.

### Frontend target

Legacy page scripts progressively become page adapters:

```text
canvas.js
smart-canvas.js
    ↓
delegate user intents / compatibility events
    ↓
static/js/workbench/...
    ↓
shared Canvas application/domain/renderer modules
```

Target rules:

- shared interaction behavior moves to shared Canvas modules;
- new registries/services are consumed through modular APIs;
- Skill/Model/Execution/Package-specific behavior is not added as new large branches in Legacy page scripts;
- Legacy source-mode distinctions shrink until R4 cutover removes duplicate product runtime.

### Architecture metric

File size is not itself the Gate.

The architectural metric is **responsibility delta**:

```text
new Workbench responsibility added to Legacy monolith = regression
responsibility delegated/extracted from Legacy monolith = progress
compatibility-only wiring with bounded removal Gate = allowed
```

R0 should establish a practical baseline for these three files.
Later Rounds should report responsibility movement, not merely line counts.
