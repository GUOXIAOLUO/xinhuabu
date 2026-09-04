# AI Workbench — Incremental Migration Plan V2.1

## Purpose

Migrate the existing `GUOXIAOLUO/canvas` application into the target AI Workbench through strangler migration, compatibility adapters and verified authority switches.

This is not a rewrite.

---

## Invariants

1. Preserve behavior before replacing it.
2. Add a seam before moving implementation.
3. Read compatibility before write-authority switch.
4. Preserve unknown Legacy fields.
5. One Unified Canvas only.
6. Skill/Model/ProviderConnection/Executor/Artifact remain separate.
7. Do not scale WholeHouse before generic Gates.
8. Do not delete Legacy node families without proposal/evidence.
9. Do not change NodeRecord incompatibly without proposal.
10. Do not change App Server contract without proposal.
11. Agent never mutates DOM/raw project JSON.
12. New domain systems do not become ad-hoc Legacy JSON authorities.
13. WholeHouse removal must not prevent Core startup.
14. Logical revision is separate from timestamps.
15. Historical Package definitions remain resolvable after disable/uninstall.

---

## Compatibility baseline

Preserve until relevant Gates pass:

- startup/browser shell
- current Canvas JSON
- required Classic/Smart links during migration
- pan/zoom/selection/drag/resize/group/connect/minimap
- fixed node families
- providers
- ComfyUI
- RunningHub
- Prompt/LLM/Loop/Group
- workflow import/export
- asset flows
- Codex Exec
- stale-write behavior
- security containment

---

## 1. Current architecture truth

R0 repairs `CURRENT_ARCHITECTURE.md` when live source/tests prove a statement stale.

Current-state and target-state text remain separate.

---

## 2. Codex

Existing: `codex exec`.

Target foundation: `CodexBridge -> App Server`.

Bridge hides child process, JSONL framing, JSON-RPC-lite protocol details, approvals and model discovery.

R1 includes bounded HarnessLaunchPolicy and no Workbench mutation tools.

---

## 3. Unified Canvas split migration

The approved U0-U7 proposal is implemented across three program Rounds:

### R2
Complete U2-U6 with compatibility execution adapters.

### R3
Create canonical Project/Canvas persistence authority.

### R4
Complete U7 cutover/removal against R3 authority.

This prevents U7 from inventing persistence before R3 and prevents U5 from being mistaken for the target R8 ExecutionRuntime.

---

## 4. Project identity

Legacy:

- `project` string
- optional/empty owner

Target:

- ProjectRecord
- ProjectMember/local actor
- action-based AuthorizationService

Migration reports identity/ownership changes explicitly.

---

## 5. Canvas authority

Legacy conflict logic may depend on `updated_at`.

Target:

- CanvasRecord.revision for concurrency
- timestamps separately

Migration:

1. adapt Legacy JSON
2. backfill SQLite
3. compare
4. verify logical revision
5. controlled authority switch
6. keep import/rollback adapter
7. contract Legacy writes later

---

## 6. Audit

Canonical SQLite mutation + durable audit/outbox is one transaction.

Legacy file/audit compatibility may remain until authority switch.

---

## 7. Node ModelBinding

NodeRecord v1 stays readable.

During R7:

- map Legacy provider IDs to ProviderConnection compatibility records
- map model IDs to ModelDefinition
- store canonical availability ID in namespaced extension
- round-trip verify
- propose v2 only after execution proof

Do not reinterpret stored provider IDs silently.

---

## 8. Execution binding

During R8 use `workbench.execution` extension.

No incompatible NodeRecord write before proposal.

Legacy provider/ComfyUI/RunningHub execution remains compatibility until target ExecutorRegistry parity.

---

## 9. Port/data bindings

R6 introduces:

- PortTypeRegistry
- typed InputBinding
- Collection

Legacy `legacy.any` and dict bindings remain readable.

Unknown semantics remain Legacy rather than guessed.

---

## 10. Skill

R6 proves dynamic definition discovery/create/render.

Execution is deliberately not an R6 proof.

---

## 11. Provider/model

R7 backend becomes authority for:

- ProviderDefinition
- ProviderConnection
- ModelDefinition
- ModelAvailability
- capability vocabulary
- availability health

Browser hard-coded lists retire after parity.

---

## 12. Execution

R8 moves compatibility execution into:

- ExecutionProfile
- RuntimeConnection
- ExecutorRegistry
- durable run/attempt/event
- policy/cancel/usage

No silent route fallback.

---

## 13. Asset/Artifact

URLs are delivery details, not identity.

Introduce immutable AssetVersion, ArtifactVersion, BlobRef and Collection.

Intermediate Artifact may remain non-materialized.

---

## 14. Entity

Formal project facts that need downstream consistency move into versioned Entity records.

Industry Packages register Entity definitions.

---

## 15. Knowledge

Asset may feed Knowledge ingestion, but identities remain separate.

Formal execution records KnowledgeSnapshot.

Vector search is optional.

---

## 16. Workflow/Approval

Workflow moves to durable version/run records.

Frozen authority applies to immutable formal versions.

Node frozen state is projection.

Agent/runtime cannot self-approve/freeze.

---

## 17. Package history

Installed folders are not the only historical-definition source.

Persist ProjectPackageLock, manifest/version hash, required DefinitionSnapshots and applied migrations.

Disable/uninstall preserves history.

---

## 18. Agent

Agent first receives read/search/propose tools.

Mutation later:

`GraphProposal -> base revision check -> confirmation -> application services`

Changed base revision makes proposal stale.

---

## 19. WholeHouse

Lives under `packages/wholehouse/`.

Registers Skills, Entities, Knowledge, Workflows, templates and review/handoff rules.

Does not add WholeHouse branches to Canvas/Model/Executor Core.

---

## 20. V1 downstream boundary

V1 ends at:

**approved/frozen design + CAD/file handoff readiness**

Not included:

- production/CNC
- installation
- after-sales
- direct Agent control of Kujiale/GuiGui

---

## 21. Legacy monolith responsibility migration

The strangler strategy is one-way.

Legacy monoliths:

- `main.py`
- `static/js/canvas.js`
- `static/js/smart-canvas.js`

may retain compatibility behavior temporarily, but they do not receive new Workbench business systems.

### New capability placement

Implement new capability contracts directly in modular target boundaries.

Examples:

```text
SkillRegistry
-> workbench/domain|application|runtimes/skills

Provider / Model
-> workbench/domain|application|runtimes/models|providers

Execution
-> workbench/domain|application|runtimes/executors

Artifact / Entity / Knowledge / Workflow
-> corresponding workbench domain/application/repository boundaries

WholeHouse
-> packages/wholehouse/
```

`main.py` may wire/register those modules.

Legacy Canvas scripts may delegate to `static/js/workbench/...`.

They must not contain a second implementation of the same new capability.

### Extraction sequence

For an existing Legacy responsibility:

```text
characterize existing behavior
-> introduce modular seam
-> delegate Legacy caller
-> verify parity
-> remove old implementation responsibility
-> remove compatibility path at its approved Gate
```

Avoid:

```text
implement new feature in Legacy monolith
-> duplicate it in workbench/
-> maintain both
-> migrate someday
```

### Compatibility exception

If an unavoidable Legacy compatibility patch temporarily adds code to a monolith:

- it must not create a new domain authority;
- it must delegate as soon as the stable seam exists;
- the active Round records the exception;
- the status/plan records the removal Gate.

The success metric is responsibility reduction, not cosmetic file splitting.

## Rollback principles

Bounded rollback examples:

- R1 App Server -> Codex Exec
- R2 unified entry -> temporary source adapter/deep link
- R3 canonical DB -> pre-switch Legacy authority during verification
- R4 cutover -> validated backups/import path
- R7 registry -> Legacy provider compatibility
- R8 executor -> explicitly selected compatibility route during window

Rollback does not justify permanent duplicate runtimes.

---

## Authoritative order

Use `IMPLEMENTATION_PLAN.md` for R0-R17.

Use `docs/status/CURRENT_EXECUTION_STATUS.md` for the only authorized current Round.
