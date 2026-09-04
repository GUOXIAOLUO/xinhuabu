# Target Architecture

## Architecture objective

Build a Web UI first AI Workbench whose Core remains generic and whose first Industry Pack, WholeHouse, can be installed, enabled, disabled, and upgraded without adding whole-house logic to Canvas or Core.

The target preserves the current working infinite-canvas interaction model and FastAPI deployment while introducing explicit domain, registry, runtime, repository, security, and version boundaries.

## Non-negotiable outcomes

1. Core starts and serves generic projects without WholeHouse Pack.
2. Canvas renders generic NodeRecords and does not branch on business Skill IDs.
3. A conforming Skill is discoverable without editing Canvas creation or render dispatch.
4. The user selects the model; runtime only filters incompatible choices.
5. Agent changes Canvas through APIs and default approval policy, never DOM automation.
6. Project persistence, not a chat thread, is the authoritative record.
7. Knowledge and Asset have different identities, repositories, and lifecycle rules.
8. Workflow definitions, runs, outputs, approvals, and provenance are versioned.
9. Legacy nodes remain readable and executable during migration.
10. Secrets remain server-side and every project mutation is authorized and auditable.

## Logical architecture

```text
Browser Web UI
  |-- Projects
  |-- Workbench Canvas
  |-- Resources
  |-- Inspector
  `-- Agent Panel
          |
          v
FastAPI API layer
  |-- Auth and Project authorization
  |-- Workbench/Canvas commands and queries
  |-- Project/Asset/Knowledge/Workflow APIs
  `-- Agent event stream
          |
          v
Application services
  |-- NodeCreationService
  |-- CanvasService
  |-- WorkflowService
  |-- ExecutionService
  |-- ApprovalService
  `-- ProvenanceService
          |
          v
Core domain
  |-- Project
  |-- Canvas graph
  |-- NodeRecord and EdgeRecord
  |-- Entity/EntityType/Relation
  |-- WorkflowDefinition/Version/Run
  |-- Artifact/Version/Provenance
  `-- Permission/Audit policy
          |
          +------------------------------+
          |                              |
          v                              v
Registries and runtimes             Domain services
  |-- RendererRegistry                |-- Asset Service
  |-- SkillRegistry                   |-- Knowledge Service
  |-- ModelRegistry                   |-- Project Service
  |-- IndustryPackRegistry            `-- Handoff Service
  |-- CodexBridge
  |-- MCP/Tool Runtime
  `-- Provider adapters
          |
          v
Repositories and infrastructure
  |-- SQLite -> PostgreSQL
  |-- local files -> object storage/NAS
  |-- migration runner
  |-- event/outbox adapter
  `-- Legacy JSON repositories
```

## Deployment target

### V1 single-user/local deployment

- One FastAPI API process.
- One browser UI served by the backend.
- SQLite for structured records.
- Local filesystem for binary assets.
- Local Codex Harness/App Server or CLI compatibility adapter.
- Local/LAN access with explicit bind and authentication configuration.

### Studio deployment

- Same application and APIs.
- PostgreSQL for shared structured data.
- NAS or object storage for binary assets.
- Multiple authenticated users with Owner, Editor, and Viewer roles.
- Persistent execution/event adapter suitable for more than one API process.

Domain code must not branch on SQLite versus PostgreSQL or local files versus object storage.

## Repository target and migration seams

The target directory layout is reached incrementally. Directory creation is justified by an active boundary, not appearance.

```text
apps/
  api/
  web/
workbench/
  api/
  application/
  domain/
    canvas/
    entities/
    workflow/
    versions/
    permissions/
  repositories/
  runtimes/
    codex/
    skills/
    models/
    mcp/
  services/
    projects/
    assets/
    knowledge/
    handoff/
schemas/
  node-record/
  renderer/
  skill/
  workflow/
packages/
  wholehouse/
tests/
  fixtures/
  unit/
  integration/
  contract/
```

During Phase 0 and Phase 1, `main.py` remains the executable entry point and registers routers from `workbench/api/`. Existing static pages remain served from `static/`. The final `apps/` split is deferred until service boundaries exist.

## Core domain model

### Project

Project is the authorization, ownership, and persistence boundary.

Required relationships:

- Project has members and role assignments.
- Project has Canvases.
- Project has Assets and AssetVersions.
- Project has Project Knowledge.
- Project has WorkflowDefinitions, WorkflowVersions, and WorkflowRuns.
- Project has Artifacts, ArtifactVersions, approvals, and handoffs.
- Project has an append-only AuditLog.

Threads and Agent conversations reference `project_id`; they do not own formal project state.

### Generic Entity model

Core defines:

- `EntityTypeDefinition`
- `EntityRecord`
- `PropertyDefinition`
- `RelationTypeDefinition`
- `EntityRelation`

Industry Packs register namespaced definitions. Core stores and queries them generically and never imports a WholeHouse class.

## NodeRecord schema draft

This is the Phase 1 canonical draft. The authoritative implementation will be a versioned JSON Schema plus matching Python and JavaScript types.

```json
{
  "schema_version": "workbench.node/1",
  "id": "node_01",
  "project_id": "project_01",
  "canvas_id": "canvas_01",
  "kind": "skill",
  "definition_ref": {
    "type": "skill",
    "id": "common.image-analysis",
    "version": "1.0.0"
  },
  "renderer": {
    "id": "analysis",
    "version": "1"
  },
  "state": "ready",
  "title": "Image analysis",
  "position": {"x": 120, "y": 240},
  "size": {"width": 360, "height": 240},
  "ports": {
    "inputs": [
      {"id": "source", "accepts": ["asset.image"], "required": true, "multiple": false}
    ],
    "outputs": [
      {"id": "analysis", "produces": ["artifact.analysis"], "multiple": false}
    ]
  },
  "input_bindings": [],
  "output_refs": [],
  "model_binding": {
    "selection_mode": "user",
    "provider_id": "provider_01",
    "model_id": "model_01",
    "parameters": {}
  },
  "config": {},
  "provenance_ref": null,
  "created_by": "user_01",
  "created_at": "2026-09-02T00:00:00Z",
  "updated_at": "2026-09-02T00:00:00Z",
  "revision": 1,
  "metadata": {},
  "extensions": {}
}
```

### NodeRecord rules

- `schema_version` is mandatory.
- `id`, `project_id`, and `canvas_id` are opaque identifiers.
- `kind` is a small Core vocabulary such as `asset`, `skill`, `artifact`, `entity`, `task`, `approval`, `group`, `composite`, and `legacy`.
- Business meaning comes from `definition_ref`, not from `kind`.
- Renderer selection comes from a registry-resolved ID and version.
- Connections bind compatible port IDs; arbitrary node-to-node edges are adapted into default Legacy ports.
- Model binding is optional for nodes that require no model.
- Provider-specific parameters use namespaced fields validated by the provider adapter.
- Formal outputs refer to ArtifactVersion or AssetVersion IDs, never only a URL.
- Mutable UI-only state is not persisted in the domain record unless it affects project meaning.
- Unknown `extensions` fields are preserved through compatible reads and writes.

## EdgeRecord schema draft

```json
{
  "schema_version": "workbench.edge/1",
  "id": "edge_01",
  "canvas_id": "canvas_01",
  "from": {"node_id": "node_source", "port_id": "image"},
  "to": {"node_id": "node_analysis", "port_id": "source"},
  "state": "active",
  "metadata": {},
  "revision": 1
}
```

Compatibility checks use port artifact/media contracts resolved through registries. Canvas highlights compatible targets while a connection is being created.

## Node state machine

Core owns the state vocabulary and permitted transitions.

```text
draft -> ready -> queued -> running -> completed
  |        |         |         |           |
  |        |         |         |           +-> outdated
  |        |         |         +-> waiting_user
  |        |         |         +-> waiting_approval
  |        |         |         +-> failed -> queued
  |        |         +-> failed
  |        +-> missing_input -> ready
  +-> frozen only through an approved artifact/version path
```

`frozen` is a human-governed formal result state. A runtime may propose approval but cannot transition to `frozen` without an authorized user action.

## NodeShell

NodeShell is the shared visual and interaction frame for all migrated nodes.

It owns:

- selection and focus behavior;
- drag and resize handles;
- Header with icon, title, status, and menu;
- Content host for one registered Renderer;
- status/progress presentation;
- Footer with user-selected model, runtime, and version when applicable;
- hover/selected Toolbar host;
- input/output connection handles;
- semantic zoom representation;
- accessibility roles and keyboard focus;
- error and outdated indicators.

Third-party Skills do not replace NodeShell. A Renderer receives a constrained content host and intent callbacks.

Media nodes use content-as-node presentation: the media is primary, decoration is minimal, and controls appear on hover or selection.

## RendererRegistry

The initial finite renderer vocabulary is:

- `media`
- `document`
- `analysis`
- `task`
- `entity`
- `form`
- `table`
- `comparison`
- `approval`
- `composite`
- `legacy`

The registry supports `register`, `resolve`, `list`, and compatibility validation. Core render dispatch is one registry lookup, not a Skill-specific conditional.

### Renderer manifest draft

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "schema_version": "workbench.renderer-manifest/1",
  "id": "analysis",
  "version": "1",
  "display_name": "Analysis",
  "node_kinds": ["skill", "artifact"],
  "accepted_content_types": ["artifact.analysis", "application/json", "text/markdown"],
  "capabilities": {
    "resizable": true,
    "semantic_zoom": true,
    "toolbar_actions": ["preview", "create_version", "more"]
  },
  "module": "/static/js/workbench/renderers/analysis-renderer.js",
  "export": "AnalysisRenderer",
  "permissions": []
}
```

Renderer modules are first-party in early phases. Third-party renderer installation is deferred until code-signing, sandboxing, and permission policy exist.

## Semantic zoom

NodeShell requests one of four renderer presentation levels based on viewport scale and performance policy:

| Approximate scale | Presentation |
|---|---|
| 100% and above | Full content and controls |
| 60% | Title, summary, state |
| 25% | Title and state |
| 10% | Icon/block and state color |

Screen-space toolbars and connection handles retain usable pixel size. Large-graph tests must cover 100, 300, and 500 generic nodes with media decoding deferred outside the viewport.

## NodeCreationService

NodeCreationService is the only creation command for migrated nodes.

### Command

```json
{
  "request_id": "request_01",
  "project_id": "project_01",
  "canvas_id": "canvas_01",
  "source": "context_menu",
  "actor_id": "user_01",
  "definition_ref": {
    "type": "skill",
    "id": "common.image-analysis",
    "version": "1.0.0"
  },
  "position": {"x": 120, "y": 240},
  "initial_bindings": [],
  "initial_config": {},
  "requested_model_binding": null,
  "approval_id": null
}
```

### Pipeline

1. Authenticate actor and authorize Canvas edit.
2. Resolve definition from Skill, Asset, Entity, Workflow, or Legacy registry.
3. Validate enabled state, pack availability, manifest version, and permissions.
4. Resolve renderer and generic port contracts.
5. Validate requested model compatibility without choosing a different model.
6. Build a NodeRecord with centralized defaults and state.
7. Validate initial bindings and cycle policy.
8. Persist node and Canvas revision atomically.
9. Append audit and domain events.
10. Return NodeRecord plus new Canvas revision.

### Entry adapters

- Context menu queries registries and submits a creation command.
- `/` and Command-K use the same search query and command.
- Skill Library drag supplies the Skill definition and drop position.
- File drop first creates an AssetVersion, then creates an Asset node.
- Workflow import submits a batch command through the same service.
- Agent proposal produces commands and executes them only after approval policy passes.
- Legacy menu entries resolve through LegacyDefinitionRegistry and return `kind: legacy` records.

Idempotency is keyed by `request_id`. Batch creation is transactional at the Canvas revision level.

## Skill Runtime

### Skill package shape

```text
skill-name/
  SKILL.md
  skill.json
  scripts/
  references/
  assets/
  tests/
```

Scopes are system, common, company, and Industry Pack. A resolved Skill ID is globally namespaced.

### Skill manifest draft

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "schema_version": "workbench.skill-manifest/1",
  "id": "common.image-analysis",
  "name": "Image Analysis",
  "version": "1.0.0",
  "description": "Analyze an image into structured observations.",
  "industry": null,
  "renderer": {"id": "analysis", "version": "1"},
  "inputs": [
    {"id": "source", "types": ["asset.image"], "required": true, "multiple": false}
  ],
  "outputs": [
    {"id": "analysis", "types": ["artifact.analysis"], "multiple": false}
  ],
  "model_requirements": {
    "capabilities": ["vision", "structured_output"],
    "input_modalities": ["image", "text"],
    "output_modalities": ["text", "json"]
  },
  "model_selection": {"mode": "user"},
  "permissions": ["asset.read", "artifact.write"],
  "executor": {
    "type": "codex_skill",
    "entrypoint": "SKILL.md"
  },
  "ui": {
    "icon": "scan-search",
    "category": "Analysis",
    "keywords": ["image", "analysis", "vision"]
  }
}
```

### SkillRegistry contract

The registry supports:

- `discover(scope)`
- `list(filters)`
- `search(query, filters)`
- `get(id, version)`
- `enable(id, version, scope)`
- `disable(id, version, scope)`
- `reload(scope)`

Install, uninstall, update, and multi-version resolution follow after discovery and execution are stable.

Discovery validates the manifest, path containment, unique `(id, version)`, renderer availability, declared permissions, input/output contracts, and executor availability. Invalid Skills are quarantined with diagnostics; they do not prevent Core startup.

`SkillDefinition` is immutable per version. `SkillInstance` is represented by a NodeRecord plus execution configuration and bindings.

## ModelRegistry

ModelRegistry is distinct from SkillRegistry and provider adapters.

### Model metadata

```json
{
  "schema_version": "workbench.model/1",
  "provider_id": "openai-main",
  "model_id": "model-id",
  "display_name": "Model display name",
  "capabilities": ["vision", "structured_output"],
  "input_modalities": ["text", "image"],
  "output_modalities": ["text", "json"],
  "context_window": 0,
  "enabled": true,
  "parameter_schema": {},
  "metadata": {}
}
```

Provider adapters implement model discovery, validation, request translation, response normalization, error normalization, cancellation, and usage extraction.

The compatibility service computes matching models from Skill requirements. It never mutates a Node selection. If no selected/default model is compatible, the Node remains `missing_input` and prompts the user.

Secrets are referenced by a server-side `secret_ref`; registry responses never include a secret or secret preview.

## Canvas API

Canvas API is a domain command/query layer exposed through HTTP and MCP-compatible tools. Concrete paths are versioned; these logical operations are stable:

### Queries

- `canvas.get_context`
- `canvas.get_selection`
- `canvas.node.get`
- `canvas.graph.get`
- `canvas.revision.get`

### Commands

- `canvas.node.create`
- `canvas.node.update`
- `canvas.node.delete`
- `canvas.edge.create`
- `canvas.edge.delete`
- `canvas.group.create`
- `canvas.group.update`
- `canvas.workflow.save`
- `canvas.workflow.load`

Every command requires actor, project, Canvas, expected revision, idempotency key, and optional approval reference. Responses include the new revision and normalized records.

Browser UI, Agent tools, and importers call the same application services. The API does not expose DOM coordinates beyond generic Canvas position/viewport records.

## CodexBridge and Agent Runtime

CodexBridge isolates the Workbench from current Harness/App Server protocol details.

### CodexBridge responsibilities

- create/resume an Agent session linked to user and project;
- pass bounded project context and Canvas selection;
- expose scoped Workbench tools;
- translate Harness/App Server events into Workbench execution events;
- persist task, plan, progress, tool activity, waiting-user, approval, result, and error events;
- support cancellation and reconnect;
- normalize current CLI compatibility behavior behind one adapter;
- prevent direct access to provider secrets and unauthorized project data.

### Agent policy

The Agent may read authorized context, search Skills, inspect model compatibility, propose workflows, and execute approved commands.

The Agent may not silently choose a different model, freeze a result, expand its tool scope, read unrelated projects, or mutate Canvas outside Canvas API.

### Agent Panel

The Agent Panel renders persistent execution state, not only chat bubbles:

- Task summary;
- proposed and accepted Plan;
- step progress;
- Tool activity with redacted inputs;
- Waiting User state;
- Approval requests;
- results and created Node references;
- retry/cancel controls.

The Canvas shows work structure and results; the Agent Panel shows execution and decisions.

## Asset Service

### Identity

- `Asset` is the logical owned file.
- `AssetVersion` is an immutable content version.
- `BlobRef` points to local/object storage.
- URLs are delivery details, not identity.

Required metadata includes asset ID, version ID, project, media type, source, parent version, content hash, size, created by, producing Skill, provider/model, tags, arbitrary namespaced metadata, created time, and access policy.

### UX command

Dragging or pasting a file into Canvas performs:

1. validate and store blob;
2. create Asset and AssetVersion;
3. create a generic Asset Node through NodeCreationService;
4. record audit and provenance;
5. return a displayable delivery URL authorized for the current user.

Asset Library remains a resource-management view; it is not a required detour before Canvas use.

## Knowledge Service

Knowledge has System, Industry, Company, Project, and User scopes. Industry Pack knowledge is registered by the pack and is absent when the pack is disabled.

The retrieval interface supports composable strategies:

- full text;
- vector similarity;
- metadata filtering;
- exact match;
- structured query;
- entity relation traversal;
- reranking.

V1 may implement full text, exact/metadata match, and an optional vector adapter, but the query and result schemas must preserve strategy and evidence metadata.

A `KnowledgeSnapshot` records the exact sources and versions used by a formal execution. Asset files may be sources for ingestion, but the AssetVersion and resulting Knowledge records remain distinct.

## Workflow Runtime

### Records

- `WorkflowDefinition`: stable logical workflow identity.
- `WorkflowVersion`: immutable versioned graph.
- `WorkflowRun`: execution of one version with bindings.
- `NodeRun`: execution state per graph node.
- `ExecutionEvent`: append-only state event.
- `ApprovalRequest`: explicit human checkpoint.

### Operations

Create, save new version, load, duplicate, run, pause, resume, retry failed/outdated nodes, import, export, and compare versions.

Workflow graphs use the same NodeRecord/EdgeRecord contracts as Canvas snapshots, with UI layout separated from execution semantics.

Composite Skill is a later projection of a versioned workflow. V1 reserves definition references and expansion metadata; it does not require full nested editing.

## Version and provenance runtime

Every formal ArtifactVersion stores:

```json
{
  "schema_version": "workbench.provenance/1",
  "artifact_version_id": "artifact_version_01",
  "node_id": "node_01",
  "node_revision": 4,
  "skill": {"id": "common.image-analysis", "version": "1.0.0"},
  "provider_id": "provider_01",
  "model_id": "model_01",
  "model_parameters": {},
  "input_refs": [],
  "asset_version_refs": [],
  "knowledge_snapshot_id": "knowledge_snapshot_01",
  "workflow_version_id": "workflow_version_01",
  "parent_version_id": null,
  "created_by": "user_01",
  "created_at": "2026-09-02T00:00:00Z"
}
```

When an input version changes, dependency comparison marks downstream outputs `outdated`. Existing outputs remain available. Rerun creates a new ArtifactVersion and records the parent relationship.

## Approval and freezing

Approval is a domain record with requested action, target version, requester, eligible reviewers, decision, reason, and timestamps.

The standard formal lifecycle is:

`draft -> review -> approved -> frozen`

Only authorized users can approve/freeze. A frozen version is immutable; changes create a new version. Agent and provider runtimes can create drafts and request review but cannot approve their own output.

## Industry Pack runtime

An Industry Pack contains namespaced, versioned registrations:

```text
packages/wholehouse/
  manifest/
  skills/
  entities/
  knowledge/
  workflows/
  templates/
  assets/
  tests/
```

The pack manifest declares compatible Workbench versions, contained registrations, permissions, migrations, enable/disable hooks, and dependencies.

Disabling a pack prevents new use of its definitions but preserves existing project records as resolvable historical definitions or read-only placeholders. Core must still start. Pack uninstall requires dependency analysis and explicit confirmation.

WholeHouse V1 is limited to roughly 12–15 core Skills covering intake through CAD Handoff. Gate 1 must pass before this catalog is built at scale.

## WholeHouse boundary and CAD Handoff

WholeHouse owns project-intake semantics, requirements, floorplan/site/reference analysis, style and space concepts, cabinet/material proposals, rendering/editing workflows, version comparison, design review, pending issues, and CAD Handoff templates.

Core owns the generic Project, Skill, Entity, Workflow, Artifact, Approval, Asset, and Handoff mechanisms.

V1 does not automate production CAD or directly control Kujiale/Guigui. A frozen design produces a versioned handoff package with manifest, project summary, structured project/spaces/material/cabinet/pending-issue data, renders, notes, and checksums. JSON, PDF, CSV, PNG, and JPG are first. SVG and DXF require later approved phases.

## Security architecture

### Identity and roles

V1 roles:

- Owner: project administration, membership, destructive actions, freeze.
- Editor: project and Canvas edits, executions, asset/knowledge changes.
- Viewer: read-only access and downloads allowed by project policy.

Authentication may begin with a local-workspace identity mechanism, but authorization is always enforced server-side. Client headers do not establish identity by themselves.

### Endpoint policy

- Default-deny CORS with configured origins.
- CSRF protection where cookie authentication is used.
- Project-scope authorization in application services.
- Separate admin permission for provider secrets, updates, storage paths, and shared folders.
- Signed or authorized media delivery instead of open project file mounts.
- File content validation, quotas, safe archive extraction, and path containment.
- URL fetch policy that blocks private/metadata networks unless explicitly authorized for known local adapters.
- Tool Runtime allowlists, parameter schemas, timeouts, cancellation, and audit.
- Central secret redaction and structured logging.

### Audit

Append-only audit events cover login, membership, project mutation, provider secret changes, tool invocation, execution, approval, freeze, export, deletion, update, and restore.

## Persistence and migrations

### Structured data

SQLite is the first database. Use repository interfaces and migrations from the first structured schema. PostgreSQL migration must not require domain rewrites.

### Binary data

Blob storage is external to relational rows. Store content hash, size, MIME, storage key, and encryption/access metadata in the database.

### Migration pattern

Every risky persistence migration uses:

1. Expand: add new schema/tables/fields and readers.
2. Backfill: import Legacy JSON with checkpoints and reports.
3. Dual read: prefer new store, fall back to Legacy.
4. Dual write or write-through: keep rollback possible for a bounded period.
5. Switch: make new storage authoritative after verification.
6. Contract: remove Legacy writes only after an approved gate and backup.

Migrations are idempotent, observable, restartable, and never silently drop unknown Legacy fields.

## Legacy architecture

LegacyDefinitionRegistry maps existing node kinds to generic definition references and the `legacy` renderer. LegacyExecutor delegates to existing functions. LegacyNodeAdapter converts stored dictionaries into NodeRecord views and preserves the original payload in a namespaced extension.

The migration sequence is per node family:

1. fixture and characterization tests;
2. adapter read path;
3. NodeShell with LegacyRenderer;
4. centralized creation path;
5. executor adapter;
6. migrated persistence;
7. usage telemetry and compatibility window;
8. separate proposal before deletion.

Classic and Smart are migration sources, not permanent product modes. The approved target and safety gates are documented in `docs/proposals/unified-canvas-runtime.md`: one `canvas.html` entry composes one CanvasRuntime, NodeShell, RendererRegistry, creation catalog, and Canvas record model. Source adapters stay internal only until mixed-fixture rendering, canonical execution, lossless migration, backups, and browser acceptance pass; the duplicate Smart page/runtime is then removed under that proposal. No final UI or node identity distinguishes old/new, Classic/Smart, or Legacy/current nodes.

## First end-to-end architecture proof

The Image Analysis Demo is the first cross-boundary proof:

1. User creates a project.
2. User drops an image on Canvas.
3. Asset Service creates Asset and AssetVersion.
4. NodeCreationService creates a Media/Asset Node.
5. Skill Library discovers `common.image-analysis` dynamically.
6. User adds the Skill by context menu or command palette.
7. User selects a compatible provider/model.
8. User connects the image output to the Skill input.
9. Workflow Runtime executes the Skill.
10. An Analysis ArtifactVersion and Analysis Node are created.
11. Canvas and workflow are saved.
12. Restart restores the project and provenance.
13. Codex reads selection, proposes the same workflow, waits for confirmation, and executes through APIs.

Passing this flow demonstrates the generic architecture before WholeHouse scale-up.

## Architecture acceptance gates

### Gate 1: dynamic Skill

- Add a Skill folder without editing Canvas node source.
- Registry discovers and validates it.
- Skill Library lists it.
- NodeCreationService creates it.
- RendererRegistry resolves its renderer.
- Runtime executes it.
- Restart preserves it.

### Gate 2: user-selected model

- The same Skill lists at least two compatible provider/model options.
- User explicitly selects each in separate runs.
- Skill definition is unchanged.
- Provenance records the actual choice.
- Runtime never silently switches the model.

### Gate 3: Codex dynamic workflow

- Codex reads current selection through Canvas API.
- Codex searches SkillRegistry.
- Codex proposes a workflow.
- User confirms.
- NodeCreationService creates nodes and edges.
- Workflow Runtime executes and persists results.
- Agent Panel shows plan, progress, tools, approval, and result.

## Explicit target non-goals for V1

V1 excludes production ERP, manufacturing/CNC, automatic nesting, production scheduling, full CRM, public Skill Marketplace, native clients, direct Agent control of third-party CAD/design applications, complex enterprise roles, multi-industry commercial launch, and production-grade automatic order splitting.
