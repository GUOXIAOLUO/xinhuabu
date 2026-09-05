# Target Architecture — AI Workbench V2.2.1

## 1. Objective

Build a macOS-first, local-first, repository-independent generic AI Workbench by incrementally evolving the existing Xinhuabu/Canvas codebase.

The product target is:

> **Unified Canvas work environment + Workbench-owned project/resource data + Codex Harness as the default Agent runtime + multi-model/multi-executor execution + Integration runtime + installable Industry Packages.**

V1 is Web UI first and officially targets macOS, with Apple Silicon / arm64 as the primary development and product environment.

Codex Harness / App Server is the primary Agent/orchestration runtime target, but Workbench must not depend on one specific Codex release version. Codex-discovered models are ordinary user-selectable model options for compatible Canvas nodes.

WholeHouse is the first deep Industry Package, not the Core. Media and other industry packages may be added later without changing Canvas Core contracts.

The target introduces explicit contracts for:

- Project / Workspace identity and authorization
- Canvas identity / revision
- Node creation / mutation / definition resolution
- Port / typed data binding
- Prompt
- Workbench Skill
- ProviderDefinition / ProviderConnection
- Model / ModelAvailability / ExecutionRoute
- ExecutionProfile / Executor / RuntimeConnection
- Asset / AssetVersion / BlobRef
- Artifact / ArtifactVersion / Collection
- Catalog / CatalogEntry
- Entity / EntityVersion / Relation
- Knowledge / KnowledgeSnapshot
- Workflow / Approval / Frozen / Handoff
- IntegrationDefinition / IntegrationConnection
- GraphProposal
- Package lock / DefinitionSnapshot
- persistence / migration / audit / backup
- Codex App Server compatibility
- durable execution events

---

## 2. Non-negotiable outcomes

1. Core starts and supports useful general projects without WholeHouse.
2. One Unified Canvas product runtime remains after migration.
3. Canvas does not branch on business Skill IDs, Provider IDs, Codex protocol fields, or industry IDs.
4. A conforming Prompt, Skill, Workflow or Entity definition can be discovered/created/rendered through registries without Canvas source edits.
5. Model, ProviderDefinition, ProviderConnection, ModelAvailability, ExecutionRoute and Executor remain separate.
6. Codex-discovered models can be selected like direct-provider compatible models.
7. Codex Harness can be both the system Agent runtime and one node execution route.
8. Workbench never silently replaces a user-selected ModelAvailability, route or Executor.
9. Agent changes project state through typed Workbench tools/application services, never DOM/raw JSON/raw DB mutation.
10. Workbench Project/domain persistence is authoritative; Codex Thread/Project state is not business truth.
11. Asset, Artifact, Catalog, Entity and Knowledge remain distinct.
12. Prompt, Workflow, Artifact, Entity and formal output history are versioned where applicable.
13. Frozen authority applies to immutable formal versions and requires authorized human approval.
14. Legacy nodes remain readable/executable until their migration Gate passes.
15. Secrets remain server-side.
16. Package disable/uninstall does not destroy historical project readability.
17. Workspace profile/resource scope changes ranking/defaults, not domain compatibility.
18. Canonical domain mutation + durable audit/outbox is atomic where they share one transaction.
19. Canonical revision numbers are logical concurrency values, not timestamp aliases.
20. Workbench Runtime does not depend on or embed a Git repository URL.
21. V1 product support is macOS-first; platform-neutral Core must remain portable.
22. Codex compatibility is Stable-API-first and capability/feature aware, not hard-coded to one Codex version.
23. Experimental Codex APIs must not be the only path for a required V1 capability.
24. Legacy monoliths may lose responsibility but must not gain new Workbench business responsibility.

---

## 3. Product surface

```text
Browser Web UI
├── Projects
├── Workbench / Unified Canvas
├── Resources
│   ├── Assets
│   ├── Catalogs / Products
│   ├── Prompts
│   ├── Skills
│   ├── Workflows
│   ├── Knowledge
│   ├── Models
│   ├── Connections
│   ├── Integrations
│   └── Executors
├── Agent Panel
└── Settings
```

Keep top-level navigation small. Agent is primarily a side panel/contextual surface rather than another product mode.

---

## 4. Logical architecture

```text
Browser Web UI
        │
        ▼
FastAPI API
├── Project / Workspace
├── Canvas commands / queries
├── Resource APIs
├── Execution / Workflow events
└── Agent / Proposal APIs
        │
        ▼
Application services
├── ProjectService / AuthorizationService
├── DefinitionResolver
├── NodeCreationService
├── NodeMutationService
├── GraphMutationService
├── CompatibilityResolver
├── PromptService / SkillService
├── ModelCompatibilityService
├── ExecutionService
├── AssetService / ArtifactService
├── CatalogService
├── EntityService / KnowledgeService
├── WorkflowService / ApprovalService / HandoffService
├── IntegrationService
└── ProposalService
        │
        ▼
Core records
├── ProjectRecord / ProjectMember / Workspace scope
├── CanvasRecord
├── NodeRecord / EdgeRecord
├── InputBinding / Port contracts
├── PromptDefinition / PromptVersion
├── Asset / AssetVersion / BlobRef
├── Artifact / ArtifactVersion / Collection
├── Catalog / CatalogEntry
├── Entity / EntityVersion / Relation
├── KnowledgeRecord / KnowledgeSnapshot
├── ExecutionRun / Attempt / Event
├── WorkflowDefinition / Version / Run
├── Approval / Frozen
├── GraphProposal
├── Handoff
└── IntegrationDefinition / IntegrationConnection
        │
        ▼
Registries / runtimes
├── RendererRegistry
├── PortTypeRegistry
├── PromptRegistry
├── SkillRegistry
├── ProviderRegistry
├── ModelRegistry
├── ModelAvailabilityRegistry
├── ExecutorRegistry
├── IntegrationRegistry
├── PackageRegistry
├── CodexRuntime
└── WorkflowRuntime
        │
        ▼
Infrastructure
├── SQLite
├── LocalBlobStore -> later NAS/object storage adapters
├── migration runner
├── durable audit/outbox
├── durable execution events
├── backup/restore
├── macOS infrastructure adapters
└── Legacy compatibility adapters
```

---

# Canonical identity and persistence

## 5. ProjectRecord

Project is the business ownership, authorization and persistence boundary.

Initial roles:

- Owner
- Editor
- Viewer

Authorization evolves toward action/resource policy.

Codex App Server experimental Project APIs do not replace Workbench ProjectRecord.

---

## 6. Workspace and resource scope

Workspace is a reusable resource boundary above individual projects.

Initial resource scopes:

```text
personal
workspace
project
package
```

Examples:

- shared board/product catalog -> workspace
- one customer's CAD file -> project
- WholeHouse default Prompt/Skill -> package

Workspace profile may influence defaults/ranking/instructions, but never bypass authorization or compatibility.

---

## 7. CanvasRecord

`CanvasRecord.revision` is monotonic logical concurrency authority.

Rules:

- timestamps are display/audit values;
- Classic/Smart source identity is Legacy migration metadata;
- final Canvas identity is business-neutral;
- canonical writes use expected revision;
- SQLite mutation should use true compare-and-swap semantics.

Target write shape:

```text
UPDATE canvas
SET payload = ?, revision = revision + 1
WHERE id = ? AND revision = expected_revision
```

A zero-row update is a stale-write conflict.

---

## 8. SQLite authority

V1 structured authority is SQLite behind repositories.

Migration:

```text
expand
-> backfill
-> compare
-> compatibility read
-> controlled switch
-> verify
-> contract Legacy writes
```

Legacy JSON remains import/rollback compatibility after cutover, not normal authority.

---

# Canvas and Node contracts

## 9. NodeRecord

NodeRecord remains business-neutral.

Core kind vocabulary stays finite:

- asset
- skill
- artifact
- entity
- task
- approval
- group
- composite
- legacy

Business meaning comes from `definition_ref`.

Do not create permanent node kinds for:

- Codex
- OpenAI
- WholeHouse products
- specific Skills
- specific providers

---

## 10. Node mutation boundary

All migrated creation/mutation goes through:

```text
NodeCreationService
NodeMutationService
GraphMutationService
```

They enforce applicable:

- authorization
- expected revision
- definition resolution
- renderer resolution
- typed bindings
- compatibility
- idempotency
- audit
- outdated propagation

No raw DOM/domain JSON mutation path may become authoritative.

---

## 11. RendererRegistry

Finite target renderer families:

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

Skills normally reuse these renderers.

---

# Typed data

## 12. PortTypeRegistry

Examples:

```text
asset.image
asset.video
asset.pdf
asset.document
asset.cad

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

---

## 13. InputBinding

Initial typed binding categories:

- asset_version
- artifact_version
- entity_ref
- entity_version
- collection
- literal

NodeRecord v1 may temporarily store the serialized dict representation, but all new construction/validation goes through typed contracts.

---

## 14. CompatibilityResolver

One compatibility service powers:

- port highlighting/drop
- "use next"
- Command-K
- Resource suggestions
- Workflow validation
- Agent planning

It may consider:

- Port/Data types
- cardinality
- Prompt/Skill/Package state
- authorization
- model capabilities
- ModelAvailability
- execution route
- executor availability
- project/workspace policy

It returns compatibility, reasons, prerequisites and ranking.

---

# Prompt and Skill

## 15. PromptDefinition / PromptVersion

Prompt is a first-class Workbench resource.

Prompt may be:

- dragged to Canvas;
- referenced by Workbench Skills;
- used by Workflows;
- used by Codex;
- used by direct model APIs;
- used by image/video/ComfyUI integrations;
- searched by Agent.

Prompt identity is separate from Codex `SKILL.md`.

---

## 16. Workbench Skill

Workbench Skill is a product capability definition.

A Codex `SKILL.md` is one optional implementation of one execution profile.

The same Workbench Skill may support:

- codex_harness
- model_api
- script
- ComfyUI
- MCP
- another executor

without changing Skill identity.

Codex Skills should be exposed to Workbench-managed Codex sessions through App Server-supported discovery/extra roots where practical; do not require copying Workbench Skills into the user's global Codex home.

---

# Provider / Model / availability

## 17. ProviderDefinition / ProviderConnection

ProviderDefinition represents adapter/protocol family.

ProviderConnection represents one configured endpoint/account.

Third-party API credentials remain behind Workbench CredentialRef.

Codex/ChatGPT authentication should normally remain owned by Codex App Server rather than duplicated in Workbench credential storage.

---

## 18. ModelDefinition

Core fields:

```text
id
family
display_name
normalized_capabilities
input_modalities
output_modalities
parameter_schema
native_metadata
```

Provider/runtime-specific fields remain in `native_metadata`.

Do not continuously expand Core ModelDefinition with Codex-only metadata.

---

## 19. ModelAvailability v2 direction

A Model may have multiple executable availabilities.

Target shape:

```json
{
  "schema_version": "workbench.model-availability/2",
  "id": "availability_01",
  "model_ref": "openai/model-x",
  "route_type": "runtime",
  "route_ref": "codex_local",
  "executor_type": "codex_harness",
  "normalized_capabilities": ["reasoning", "vision"],
  "constraints": {},
  "enabled": true,
  "status": "available",
  "native_metadata": {}
}
```

`route_type` initially supports:

```text
provider
runtime
```

Examples:

```text
GPT-X · OpenAI API
route_type = provider
executor_type = model_api

GPT-X · Codex Harness
route_type = runtime
executor_type = codex_harness
```

NodeRecord v1 continues compatibility mapping through its current ModelBinding plus namespaced availability extension until a later schema proposal.

---

## 20. No silent fallback

The Workbench may filter/recommend routes, but never silently replace:

- requested model
- ModelAvailability
- ProviderConnection / RuntimeConnection
- ExecutionProfile
- Executor

Execution provenance records requested and actual route/model.

Codex experimental provider model fallback is omitted/disabled by default for Workbench-controlled execution.

---

# Execution

## 21. ExecutionProfile

ExecutionProfile is a user-facing execution mode supported by a Skill.

Examples:

```text
codex-deep
direct-fast
comfyui-local
runninghub-cloud
```

---

## 22. ExecutorRegistry

Initial executors:

- CodexHarnessExecutor
- ModelApiExecutor
- ComfyUIExecutor
- RunningHubExecutor
- ScriptExecutor
- MCPExecutor

Normalized executor contract covers:

- validate
- start
- events/poll
- cancel if supported
- status
- partial result
- final result
- errors
- usage

---

## 23. Execution records

Canonical records:

```text
ExecutionRun
ExecutionAttempt
ExecutionEvent
```

ExecutionRun records applicable:

- Skill/version
- Prompt/version
- requested model
- actual model
- ModelAvailability
- ProviderConnection or RuntimeConnection
- ExecutionProfile
- Executor
- inputs
- output ArtifactVersion
- usage
- timestamps
- final state/error

---

## 24. Durable execution events

Long-running work must survive browser disconnects.

V1 may implement durable state in SQLite.

Do not require Redis/Celery/Kafka for V1.

---

# Codex Harness integration

## 25. Codex role

Codex has three Workbench roles:

1. primary Agent/orchestration runtime;
2. one node execution route through `CodexHarnessExecutor`;
3. a model discovery source whose models become normal ModelAvailability choices.

Codex is not itself a ModelDefinition.

---

## 26. CodexRuntime

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

This is an App Server client boundary, not another Agent Harness.

---

## 27. Stable API first

Workbench must not depend on one exact Codex version.

Policy:

- use official App Server stable APIs first;
- record installed/tested version for diagnostics;
- generate/compare official protocol schema during compatibility work;
- feature-detect optional functionality;
- unknown optional fields must not break Core;
- experimental API use requires an explicit adapter/policy;
- no required V1 feature may have only an experimental Codex path.

V1 transport is local stdio JSONL.

Do not make App Server WebSocket transport a V1 requirement.

---

## 28. Codex protocol generation

Use official:

```text
codex app-server generate-json-schema
codex app-server generate-ts
```

as protocol evidence/generation inputs.

Generated protocol DTOs remain inside the Codex integration boundary.

Core domain models must not import raw Codex protocol DTOs.

---

## 29. CodexProjectionService

Projects relevant App Server state into Workbench runtime choices.

Examples:

```text
model/list
-> ModelDefinition / ModelAvailability projection

model/provider capability data
-> normalized capability projection

skills/list
-> CodexSkillAvailability

account/config state
-> runtime diagnostics

Apps/MCP status
-> Integration projections
```

Codex native data is projection/runtime state, not Workbench domain authority.

---

## 30. CodexSessionLink

Optional lightweight Workbench record:

```text
id
project_id
thread_id
purpose
role
last_turn_id
created_at
status
```

It links business work to a Codex Thread without duplicating all Codex history into Workbench.

---

## 31. CodexWorkbenchToolBridge

Stable internal layer:

```text
WorkbenchToolContract
```

Example tools:

- project.read
- canvas.get_context
- asset.search/read
- catalog.search/read
- prompt.read
- skill.search/resolve
- compatibility.resolve
- workflow.read
- execution.get
- artifact.read
- graph.propose
- approval.request

Adapters may include:

```text
MCP adapter
DynamicTool adapter [experimental/optional]
```

Dynamic Tools must not be the only V1 Agent tool route.

All tools call Application Services; no raw DB/DOM/project JSON tools.

---

## 32. Codex runtime approval vs business approval

Keep separate:

```text
Codex approval
= shell/filesystem/network/MCP/runtime safety

Workbench approval
= design/product/quote/CAD/business authority
```

Codex cannot approve/freeze its own Workbench formal result.

---

## 33. Codex policy mapping

Workbench defines high-level policy such as:

```text
read_only
workspace_write
interactive
```

The Codex adapter maps this onto currently supported stable sandbox/permission mechanisms.

Core must not depend on experimental permission profile field names.

---

# Assets / Catalog / Entity / Knowledge

## 34. Asset / AssetVersion / BlobRef

Asset is a logical owned file.

AssetVersion is immutable content.

BlobRef points to storage.

Canvas and formal records reference versions rather than local absolute path identity.

---

## 35. Asset Library

Product UX includes:

- Workspace Assets
- Project Assets
- Recent
- Favorites
- Collections
- Tags
- Search

---

## 36. BlobStore

V1:

```text
LocalBlobStore
```

Future adapters:

```text
NASBlobStore
ObjectBlobStore
```

Domain only knows BlobRef.

---

## 37. Catalog

Generic Core:

```text
Catalog
CatalogCategory
CatalogEntry
CatalogService
```

Do not create a Core ProductRecord special case.

WholeHouse Product Library is Catalog + WholeHouse Entity definitions.

Media can reuse Catalog for Character/Scene/Props.

---

## 38. Entity Runtime

Core owns generic Entity/EntityVersion/Relation contracts.

WholeHouse may define:

- Customer
- ProjectRequirement
- Room
- Space
- Cabinet
- MaterialSelection
- ProductSelection
- DesignDecision

Formal mutation creates immutable EntityVersion.

---

## 39. Knowledge Runtime

Knowledge may be scoped:

- system
- common
- industry
- company/workspace
- project
- user

Formal execution captures a KnowledgeSnapshot sufficient for reproducibility.

---

# Workflow / governance / handoff

## 40. Workflow Runtime

Records:

- WorkflowDefinition
- WorkflowVersion
- WorkflowRun
- NodeRun

Workflow is not Canvas and is not Codex Thread.

A Workflow can be represented as a collapsible/expandable Composite/Workflow node on Canvas.

---

## 41. Approval / Frozen

Approval targets a formal immutable version.

Frozen formal output requires an authorized human decision.

Node frozen state is only UI projection.

---

## 42. Handoff Runtime

Core owns:

- manifest
- referenced versions
- checksums
- destination
- export package
- validation
- creator/approver
- timestamps/status

WholeHouse V1 uses CAD/DXF/DWG/PDF/image file handoff before direct external software control.

---

# Integration

## 43. IntegrationRegistry

Core records:

```text
IntegrationDefinition
IntegrationConnection
IntegrationRegistry
IntegrationService
```

Supported integration mechanisms may include:

- Native API
- MCP
- Local Bridge
- File Handoff
- Webhook
- CLI
- Human Handoff

Codex-native Apps/MCP remain managed by Codex; Workbench exposes them as projections where useful rather than reimplementing Codex's runtime.

---

# Package architecture

## 44. Package Runtime

Kinds:

- system
- common
- industry

Package history uses:

```text
ProjectPackageLock
DefinitionSnapshot
Package migrations
```

Historical projects remain readable after package disable/upgrade/uninstall.

---

## 45. Package layout

Target:

```text
packages/
├── common/
├── wholehouse/
└── media/
```

Current vendored wheels/runtime content must eventually move out of `packages/`; do not perform that cleanup during active R4 unless specifically authorized.

---

## 46. Common Package

Candidates:

- image/document analysis
- structured extraction
- text generation
- image generation/edit
- video generation
- comparison
- research
- repository/code analysis

---

## 47. WholeHouse Package

Registers:

- Skills
- Prompts
- Entities
- Catalog/Product definitions
- Knowledge
- Workflows
- templates
- review/handoff rules

V1 boundary:

```text
project intake
-> requirement/floorplan analysis
-> space concept
-> product/material selection
-> render/review
-> approval/frozen
-> CAD/file handoff readiness
```

V1 excludes:

- production/CNC
- installation
- after-sales
- mandatory direct Agent control of Kujiale/GuiGui

---

## 48. Media Package

Future package may define:

- Character
- Scene
- Script
- Episode
- Shot
- Storyboard
- Voice
- Video

It must reuse the same Canvas/Asset/Catalog/Prompt/Skill/Workflow/Execution contracts.

---

# Platform engineering

## 49. Typed Settings

Target settings groups:

- ServerSettings
- DatabaseSettings
- StorageSettings
- SecuritySettings
- CodexSettings
- FeatureSettings
- RuntimeSettings

New modules should not scatter direct `os.getenv()` calls across business code.

---

## 50. MigrationRunner

All durable schema/data migrations converge on one versioned runner.

Avoid indefinite startup-time ad-hoc file repair.

Migration records include:

```text
migration_id
checksum
applied_at
status
```

---

## 51. Backup / Restore

Formal Workbench backup covers:

- database
- BlobRefs/blobs as configured
- definitions/snapshots
- package locks
- manifest/checksums

Support:

- backup
- verify
- restore
- dry-run restore

---

## 52. Feature Flag lifecycle

Each migration flag declares:

```text
introduced_round
purpose
default
removal_gate
```

After its Gate passes, retire the flag and obsolete path.

---

## 53. Schema / API

Canonical contract pipeline:

```text
Pydantic
-> JSON Schema
-> OpenAPI
-> frontend generated/validated types
```

Codex generated protocol schemas remain separate from Workbench domain schemas.

---

## 54. Security

Unified policies cover:

- authentication
- authorization
- credentials
- network/SSRF
- filesystem/path containment
- subprocess/tool scope
- Integration/MCP
- destructive confirmation
- audit
- stale-write/concurrency

LAN mode is not authenticated multi-user support until explicitly implemented.

---

## 55. macOS-first infrastructure

V1 may implement macOS adapters for:

- Keychain
- Finder/File Picker
- local app launching
- Local Bridge
- filesystem permissions
- local MCP/software integration

Core remains platform-neutral so Windows can be added later through adapters.

---

# Repository / legacy rules

## 56. Repository-independent runtime

Workbench runtime must not require:

- GitHub repository URL
- GitHub tree/raw APIs
- source-control server availability

Legacy self-update code that points to a repository is removed rather than retargeted.

GitHub may remain a development/CI system external to product runtime.

---

## 57. Legacy monolith responsibility freeze

Legacy surfaces:

```text
main.py
static/js/canvas.js
static/js/smart-canvas.js
```

may:

- retain compatibility behavior temporarily;
- delegate to modular Workbench services;
- shrink;
- perform composition/bootstrap.

They must not become the primary implementation location for new:

- Prompt/Catalog/Integration
- Provider/Model
- Execution
- Asset/Entity/Knowledge/Workflow
- Package
- WholeHouse
- Codex protocol/domain tooling

Backend target for `main.py`:

```text
create_app()
register_routes()
wire_services()
startup/shutdown
narrow compatibility bootstrap
```

---

## 58. Architecture guards

Automated checks should eventually reject patterns such as:

- WholeHouse-specific branches in Core Canvas/Model/Executor
- provider-specific logic in Canvas
- Codex protocol DTO imports in Core domain
- new business systems implemented in `main.py`
- Agent raw DB/JSON/DOM mutation
- runtime Git repository URL dependencies
- required V1 feature implemented only through a Codex experimental API

---

# First generic proof

## 59. Generic platform proof

1. create/open generic Project;
2. drop image;
3. AssetVersion created;
4. Asset Node created;
5. Prompt/Skill discovered dynamically;
6. compatible ModelAvailabilities shown;
7. user can choose a Codex-discovered availability or direct-provider availability;
8. ExecutionRuntime runs selected route;
9. ArtifactVersion created;
10. optional result Node materialized;
11. project/workflow saved;
12. restart restores state/provenance;
13. Codex Agent can later propose equivalent graph through WorkbenchToolContract;
14. user confirms;
15. same application services apply the graph.

This proves the Workbench before WholeHouse scale-up.
