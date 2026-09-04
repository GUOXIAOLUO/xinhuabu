# Current Execution Status

status_schema: workbench.execution-status/2

## Repository

repository: GUOXIAOLUO/xinhuabu
observed_head: 03c2a1680fe73473a2e4e3a68419f327cef30088
observed_commit: "feat: establish unified canvas migration boundaries"
last_verified_from_live_worktree: null

> R0 must replace observed values with live verified values.

## Product contract

product: generic AI Workbench
client_v1: Web UI
orchestration_target: Codex Harness / App Server
wholehouse_role: first Industry Package, not Core
canvas_target: one Unified Canvas
project_persistence_authoritative: true
agent_dom_mutation_allowed: false
silent_model_provider_executor_fallback_allowed: false

## Active Round

active_round: R0
active_round_name: Repository Truth + Architecture Refresh
round_status: authorized
blocking_issues: []

## Observed facts requiring R0 verification

- NodeRecord v1 exists
- EdgeRecord v1 exists
- NodeCreationService exists
- NodeMutationService exists but current mutable-field coverage is limited
- GraphMutationService exists
- RendererRegistry foundation exists
- Legacy JSON Canvas repository remains active
- current ModelBinding stores provider_id + model_id
- current ports use string ArtifactType aliases
- Codex has a codex-exec compatibility path
- Unified Canvas proposal U0-U7 exists

## Unified Canvas observed ledger

U0: complete
U1: complete
U2: in_progress
U3: in_progress
U4: in_progress
U5: in_progress
U6: pending
U7: pending

R0 must verify.

## Current architecture document warning

`CURRENT_ARCHITECTURE.md` may mix older audit prose with newer migration facts.

R0 must repair verified contradictions while keeping the file current-state only.

## Known issue to verify

Potential revision mismatch:

- NodeCreateCommand.expected_revision may be optional
- create-node-and-edge may coerce missing revision to zero
- graph mutation validation requires positive revision

R0 must verify exact behavior.

## Target contracts not yet proven

- ProjectRecord
- CanvasRecord logical revision
- action-based AuthorizationService
- transactional audit/outbox
- DefinitionResolver
- PortTypeRegistry
- typed InputBinding
- ProviderConnection
- canonical ModelRegistry
- ModelAvailability
- ExecutionProfile
- RuntimeConnection
- ExecutorRegistry
- Asset/Artifact version runtime
- immutable EntityVersion runtime
- KnowledgeSnapshot
- Workflow/Approval/Handoff
- ProjectPackageLock / DefinitionSnapshot
- Common Package
- Codex Workbench orchestration
- WholeHouse vertical slice

## Compatibility currently expected

- Canvas JSON readability
- required Classic/Smart compatibility
- provider execution
- ComfyUI
- RunningHub
- Prompt/LLM/Loop/Group/fixed nodes
- unknown Legacy fields
- Codex Exec

## Authority map

project: unverified
canvas: legacy_json_expected_but_R0_must_verify
node: canonical_view_plus_legacy_persistence_expected_but_R0_must_verify
asset: unverified
artifact: not_proven
entity: not_proven
knowledge: not_proven
workflow: not_proven
approval: not_proven

## Test baseline

verified_head: null
verified_at: null
commands: []
result: not_run_for_this_status_file

## Performance baseline

latest_benchmark_document: unverified
accepted_sample: unverified
open_performance_issue: unverified

## Current authorized action

Execute R0 only.

R0 must:

1. inspect live worktree/source/tests
2. verify U0-U7
3. verify authority/mutation paths
4. verify Codex/provider architecture
5. verify revision issue
6. run baseline
7. repair verified current-state contradictions in CURRENT_ARCHITECTURE.md
8. update this status file
9. authorize exactly one next Round

## Forbidden next actions during R0

- product behavior changes
- App Server implementation
- Canvas redesign
- NodeRecord incompatible change
- persistence authority switch
- SkillRegistry implementation
- ModelRegistry implementation
- WholeHouse implementation

## Expected next Round

R1 — Codex Harness Foundation, only if R0 finds no blocker.
