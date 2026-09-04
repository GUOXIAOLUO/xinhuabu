# AI Workbench — Development Execution Plan V2.1

Status: active Gate program  
Repository: `GUOXIAOLUO/xinhuabu`  
Method: incremental / strangler / evidence-based Gates  
V1: Web UI  
Primary orchestration target: Codex Harness / App Server  
First Industry Package: WholeHouse

---

## Execution rules

For every Codex task:

1. read `AGENTS.md`
2. read `docs/status/CURRENT_EXECUTION_STATUS.md`
3. read `CURRENT_ARCHITECTURE.md`
4. read `TARGET_ARCHITECTURE.md`
5. read `MIGRATION_PLAN.md`
6. read this file
7. inspect affected source/tests
8. execute exactly one authorized Round

A Gate passes only when its acceptance criteria are verified.

---

## Round overview

| Round | Name | Primary result |
|---|---|---|
| R0 | Repository Truth + Architecture Refresh | live facts + repaired current-state docs |
| R1 | Codex Harness Foundation | CodexBridge transport/runtime + launch policy |
| R2 | Unified Canvas Convergence A | U2-U6 with compatibility adapters |
| R3 | Project Identity + Canonical Canvas Persistence | ProjectRecord/CanvasRecord/SQLite/auth/audit |
| R4 | Unified Canvas Cutover | U7 + canonical cutover + duplicate runtime removal |
| R5 | Generic Node UX + Mutation | NodeShell V2 + Inspector + mutation contract |
| R6 | Port/Data Contracts + SkillRegistry | typed bindings + discovery/create/render Gate |
| R7 | Provider + Model Registry | ProviderConnection + ModelAvailability selection Gate |
| R8 | Execution Runtime | cross-model + cross-executor execution Gate |
| R9 | Asset + Artifact + Version | durable versioned inputs/results/provenance |
| R10 | Entity + Knowledge Runtime | structured project facts + reproducible context |
| R11 | Workflow + Approval + Handoff Core | formal workflow/governance/export |
| R12 | Package Runtime + WorkspaceProfile | package lifecycle + historical definitions |
| R13 | Common Capability Package | useful general Workbench without WholeHouse |
| R14 | Codex Workbench Orchestration | scoped tools + GraphProposal + Agent Panel |
| R15 | WholeHouse Vertical Slice | one real room/space end-to-end |
| R16 | WholeHouse Expansion | approved V1 capability catalog |
| R17 | CAD Handoff + Real Project Validation | production-like design-work validation |

---

# R0 — Repository Truth + Architecture Refresh

## Goal

Make current-state documentation trustworthy before feature work.

Verify:

- live HEAD/worktree
- test/static baseline
- U0-U7 actual state
- feature flags
- Legacy read/write authority
- NodeRecord/EdgeRecord
- NodeCreation/NodeMutation/GraphMutation
- RendererRegistry/NodeShell
- provider/model settings
- Codex Exec/App Server status
- security boundary
- benchmark/performance follow-up

### CURRENT_ARCHITECTURE requirement

If source/tests disprove a current-state statement, update `CURRENT_ARCHITECTURE.md`.

Do not inject target-state design.

### Known issue to verify

Verify whether optional `NodeCreateCommand.expected_revision` can be normalized to `0` in create-node-and-edge flow and then rejected by graph mutation validation.

Allowed changes: current/status docs plus narrowly necessary test-harness repair only.

Forbidden: product behavior, App Server code, Canvas redesign, schema change, persistence switch, Skill/Model/Execution implementation, WholeHouse.

Gate: current truth is explicit and exactly one next Round is authorized.

---

# R1 — Codex Harness Foundation

## Goal

Establish App Server behind `CodexBridge` without Workbench mutation authority.

Pre-work:

- inspect installed/target Codex version
- inspect official schema/protocol for that version
- create/update proposal
- inspect codex-exec compatibility
- define HarnessLaunchPolicy

HarnessLaunchPolicy covers:

- bounded cwd/workspace
- environment/secret filtering
- filesystem/shell policy
- destructive approval
- timeout/cancel
- child-process lifecycle
- no Workbench mutation tools

Deliver:

- start/initialize
- health/version
- Thread/Turn basics
- normalized events
- approval round trip
- model/config discovery
- cancel/shutdown/recovery
- codex-exec compatibility

Gate: transport/runtime + launch policy verified; no project mutation tools.

---

# R2 — Unified Canvas Convergence A

## Goal

Complete U2-U6 without prematurely implementing R3 canonical persistence or R8 target ExecutionRuntime.

### U2
shared graph/port/group interaction.

### U3
unified render host + NodeShell + RendererRegistry.

### U4
unified creation catalog + application-service paths.

### U5
**compatibility execution adapters only** around current Classic/Smart/provider execution.

U5 does not prove final ExecutorRegistry.

### U6
one normal product Canvas entry; old deep links remain during migration.

### Explicitly not R2

- U7 is not executed in R2.
- no SQLite authority switch.
- no final ExecutorRegistry/ExecutionProfile runtime.

Gate:

- one normal product Canvas entry
- shared interaction/render/creation
- representative Legacy execution through compatibility adapter
- U7 remains pending
- status authorizes R3

---

# R3 — Project Identity + Canonical Canvas Persistence

## Goal

Create canonical Project/Canvas authority before U7.

Deliver:

- ProjectRecord
- ProjectMember/local actor mapping
- CanvasRecord
- logical Canvas revision
- action/resource AuthorizationService
- SQLite migrations/repositories
- Legacy import/backfill/compare
- explicit authority state
- transactional mutation + durable audit/outbox
- migration/rollback report

Test Legacy identity cases:

- project="default"
- owner=""
- non-empty owner
- project mismatch
- rollback

Rules:

- no silent owner invention
- revision != updated_at
- NodeRecord v1 remains compatible
- source Canvas runtimes/pages remain until R4

Gate:

- Project/Canvas survive restart
- revision concurrency works
- Legacy fixtures compare
- identity mapping report works
- canonical mutation + audit atomic
- authorization enforced
- rollback exists

---

# R4 — Unified Canvas Cutover

## Goal

Complete **U7** against R3 canonical authority.

Deliver:

- source-record backup/validation
- canonical cutover
- workflow import/export verification
- expected-revision conflict verification
- Legacy function verification through adapters
- 100/300-node performance verification
- duplicate Classic/Smart runtime/page/CSS removal only after acceptance

Important:

U7 canonical persistence means R3 authority.
Do not invent a second canonical JSON authority.

Gate:

- one Canvas page/runtime/catalog
- canonical persistence active
- old records import/read
- no product source-mode distinction
- duplicate runtime removed after acceptance
- benchmark budget passes
- rollback backup tested

---

# R5 — Generic Node UX + Mutation

Goal: generic task-oriented Node UX.

Deliver:

- NodeShell V2 five regions
- Inspector
- NodeMutationService expansion
- model-availability extension editing
- execution extension editing
- next-step/materialization/branch intent seams

Gate:

- Inspector uses application service
- no raw new mutation path
- generic renderers share NodeShell
- no WholeHouse branches

---

# R6 — Port/Data Contracts + SkillRegistry

## Goal

Prove dynamic definition discovery/create/render without borrowing the future ExecutionRuntime.

Deliver:

- PortTypeRegistry
- typed InputBinding
- Collection
- CompatibilityResolver foundation
- DefinitionResolver
- Skill manifest V2
- Workbench Skill vs Codex Skill separation
- SkillRegistry
- Skill Library
- `common.image-analysis`

### Gate A — Dynamic definition

A conforming Skill:

- no Canvas source edit
- discovered/listed
- resolves through DefinitionResolver
- creates through NodeCreationService
- renders through RendererRegistry/NodeShell
- validates typed bindings
- survives restart

Actual target execution is not part of R6.

---

# R7 — Provider + Model Registry

## Goal

Prove Provider/Connection/Model/Availability semantics before target execution.

Deliver:

- ProviderDefinition
- ProviderConnection
- CredentialRef
- ProviderRegistry
- ModelDefinition
- capability vocabulary
- ModelRegistry
- ModelAvailability
- ModelCompatibilityService
- Codex discovery source
- direct-provider discovery
- API Center backend endpoints
- Model Picker
- NodeRecord v1 availability-extension migration

No silent Model/Connection/Availability fallback.

### Gate B — Model selection

For one Skill:

- two compatible ModelAvailabilities can be discovered/filtered
- either can be selected
- selection persists/reloads
- incompatibility reason is explainable
- v1 ModelBinding remains compatible
- provenance-ready requested selection is representable

Actual execution is deferred to R8.

---

# R8 — Execution Runtime

## Goal

Prove `Skill + ModelAvailability + ExecutionProfile + Executor`.

Deliver:

- ExecutionProfile
- RuntimeConnection / ExecutorEndpoint
- ExecutorRegistry
- CodexHarnessExecutor
- ModelApiExecutor
- ComfyUIExecutor
- RunningHubExecutor
- ScriptExecutor
- MCPExecutor seam
- MCP tool-vs-executor separation
- ExecutionPolicy
- ExecutionRun/Attempt/State/Event
- timeout/cancel/partial-result/usage
- explicit executor capabilities
- requirement merge rules

No silent executor fallback.

### Gate C — Actual execution

Same Skill:

- runs with two compatible ModelAvailabilities where available
- runs through at least two compatible execution routes
- produces same typed output contract
- records actual model/provider/runtime/executor/profile
- demonstrates cancel or explicit unsupported-cancel
- durable execution state behaves as designed

---

# R9 — Asset + Artifact + Version

Deliver:

- BlobRef
- Asset/AssetVersion
- Artifact/ArtifactVersion
- Collection persistence
- Artifact materialization
- parent/branch/new-version
- provenance core
- dependency/freshness
- authorized delivery URLs

Gate: old versions preserved, outdated deterministic, rerun creates version, intermediate Artifact may remain non-materialized.

---

# R10 — Entity + Knowledge Runtime

Entity:

- definitions/properties/relations
- EntityRecord
- immutable EntityVersion
- authorization/audit

Knowledge:

- sources/scopes
- retrieval contract
- KnowledgeSnapshot/evidence

Gate: formal execution captures KnowledgeSnapshot; formal Entity mutation creates EntityVersion.

---

# R11 — Workflow + Approval + Handoff Core

Deliver:

- WorkflowDefinition/Version/Run
- NodeRun
- retry/cancel/pause semantics
- import/export/compare
- ApprovalRequest/Decision
- reviewer policy
- Frozen formal version
- generic Handoff manifest/checksums

Gate: restartable workflow, authorized human freeze, frozen formal version immutable, generic handoff validates.

---

# R12 — Package Runtime + WorkspaceProfile

Deliver:

- PackageRegistry
- package manifest/lifecycle
- dependency checks
- ProjectPackageLock
- DefinitionSnapshot
- package migrations
- WorkspaceProfile

Gate:

- package lock/version persists
- disable blocks new usage as intended
- historical DefinitionRefs remain resolvable
- profile changes defaults/ranking only

---

# R13 — Common Capability Package

Goal: prove general Workbench without WholeHouse.

Candidates:

- image/document analysis
- structured extraction
- text generation
- image generation/edit
- video generation
- comparison
- code/repository analysis
- research when ready

Gate: WholeHouse absent and general Canvas/Skill/Model/Codex/API/ComfyUI/Artifact/Entity/Knowledge/Workflow remain useful.

---

# R14 — Codex Workbench Orchestration

Deliver:

- scoped Workbench tools
- GraphProposal
- stale/rebase policy
- Agent Panel

Gate D:

```text
select Asset
-> Agent reads scoped context
-> CompatibilityResolver
-> Skill/model/executor choice
-> GraphProposal
-> user confirmation
-> revision check
-> application services mutate
-> ExecutionRuntime
-> ArtifactVersion
-> Canvas result
```

No DOM/raw DB/project JSON mutation.

---

# R15 — WholeHouse Vertical Slice

```text
Project Intake
-> Requirement/Floorplan Analysis
-> Space Entity
-> Space Concept
-> Render
-> Design Review
-> Approval/Frozen
-> CAD Handoff preparation
```

Gate: no WholeHouse Core branches; versioned data, KnowledgeSnapshot, model/availability/execution choice, approval/freeze/handoff.

---

# R16 — WholeHouse Expansion

Target approximately 12-15 high-quality capabilities:

- Project Intake
- Requirement Analysis
- Floorplan Analysis
- Site Photo Analysis
- Reference Analysis
- Style Direction
- Space Concept
- Cabinet Concept
- Material Proposal
- Render
- Image Edit
- Version Compare
- Design Review
- Pending Issues
- CAD Handoff

Production/installation/after-sales remain outside V1.

---

# R17 — CAD Handoff + Real Project Validation

Validate:

- small/medium/complex projects
- restart/recovery
- retry/cancel
- version/outdated
- 100-300 Node Canvas
- authorization/security
- proposal stale handling
- model/provider/executor correctness
- package history
- designer/CAD reviewer acceptance
- handoff checksums/completeness

Exit:

1. WholeHouse completes approved/frozen design + handoff.
2. WholeHouse disabled still leaves a useful generic AI Workbench.

---

## Cross-Round report format

Every Round reports:

1. Completed work
2. Modified files
3. Added files
4. Deleted files
5. Architecture changes
6. Persistence changes
7. API changes
8. UI changes
9. Compatibility
10. Security impact
11. Automated tests
12. Browser/manual tests
13. Known issues
14. Exact next authorized Round
15. Forbidden next actions
