# AI Workbench — Incremental Migration Plan V2.2.1

## Purpose

Incrementally evolve the existing Xinhuabu/Canvas application into the target AI Workbench through strangler migration, compatibility adapters, verified authority switches and bounded rollback.

This is not a rewrite.

V2.2.1 preserves completed R0-R3 evidence and the active R4 Gate while extending future migration contracts for Prompt, Catalog, Integration, Codex compatibility, Workspace resources and platform engineering.

---

## Invariants

1. Preserve behavior before replacing it.
2. Add a seam before moving implementation.
3. Read compatibility before write-authority switch.
4. Preserve unknown Legacy fields.
5. One Unified Canvas only.
6. Prompt/Skill/Model/ModelAvailability/Executor/Artifact remain separate concepts.
7. Do not scale WholeHouse before generic Gates.
8. Do not delete Legacy node families without evidence.
9. Do not change NodeRecord incompatibly without proposal.
10. Agent never mutates DOM/raw project JSON/raw DB directly.
11. New domain systems do not become ad-hoc Legacy JSON authorities.
12. WholeHouse removal must not prevent Core startup.
13. Logical revision is separate from timestamps.
14. Historical Package definitions remain resolvable after disable/uninstall.
15. Workbench Runtime does not depend on a Git repository URL.
16. V1 is macOS-first while Core remains platform-neutral.
17. Codex integration is Stable-API-first and not bound to exact version equality.
18. Experimental Codex APIs do not become the only required path for a V1 capability.
19. Codex Project/Thread records never become Workbench business authority.
20. Legacy monolith responsibility only moves outward/downward.

---

## Compatibility baseline

Preserve until relevant Gates pass:

- startup/browser shell;
- current Canvas JSON readability;
- required Classic/Smart links during migration;
- pan/zoom/selection/drag/resize/group/connect/minimap;
- fixed node families;
- provider execution;
- ComfyUI;
- RunningHub;
- Prompt/LLM/Loop/Group compatibility;
- workflow import/export;
- asset flows;
- Codex Exec compatibility;
- stale-write behavior;
- security containment.

---

# 1. Current-state vs target-state

`CURRENT_ARCHITECTURE.md` and `docs/status/CURRENT_EXECUTION_STATUS.md` describe verified current reality only.

Future V2.2.1 contracts belong in target/plan documents.

Do not mark a Round complete because planning text exists.

---

# 2. Codex migration

Legacy:

```text
codex exec
```

Target:

```text
Workbench
-> CodexRuntime / CodexBridge
-> official Codex App Server
```

Migration principles:

- V1 uses local stdio JSONL;
- raw protocol stays behind Codex integration modules;
- official generated schema may be used for DTO/compatibility validation;
- recorded tested version is evidence, not a hard equality requirement;
- stable App Server APIs are preferred;
- experimental API use is explicit and optional;
- Codex authentication remains primarily owned by Codex;
- Codex Project/Thread state is linked/projection state only;
- Workbench business truth stays in Workbench persistence.

`codex exec` remains compatibility until a later explicit retirement Gate.

---

# 3. Unified Canvas split migration

Approved U0-U7 migration remains split:

- R2: shared interaction/render/creation + compatibility execution;
- R3: canonical Project/Canvas persistence foundation;
- R4: U7 cutover/removal.

R4 must finish before new R5+ platform systems are implemented.

---

# 4. R4 authority cutover

Legacy:

```text
data/canvases/*.json
```

Target:

```text
SQLite CanvasRecord
+
logical revision
```

Migration:

1. backup Legacy source;
2. import/backfill;
3. compare losslessly;
4. verify revision semantics;
5. fix any compatibility lost-update path;
6. switch canonical routing;
7. verify browser/API write conflicts;
8. verify workflow parity;
9. remove duplicate Canvas product runtime;
10. retain bounded import/rollback adapter.

Canonical expected-revision writes converge on SQL compare-and-swap semantics.

---

# 5. Repository-independent runtime migration

Legacy source may contain self-update/source-repository URLs.

Migration rule:

```text
do not retarget old repository URL
-> remove/disable runtime source-repository update responsibility
```

Workbench product startup and normal operation must not require GitHub/GitLab/other source-control availability.

Version/build information may exist without repository URL.

---

# 6. Mac-first cleanup

V1 product support is macOS/Apple Silicon first.

Do not perform broad vendor/runtime cleanup during active R4 unless required for the Gate.

After R4, historical Windows runtime/wheel content may be moved/removed through a separate repository hygiene task.

Core contracts remain portable.

---

# 7. Node ModelBinding migration

NodeRecord v1 stays readable.

During R7:

- map Legacy model identity to ModelDefinition;
- map Legacy provider IDs to compatibility ProviderConnection where applicable;
- introduce ModelAvailability with neutral execution route semantics;
- store canonical availability identity in namespaced extension while v1 requires legacy fields;
- verify round-trip;
- do not reinterpret stored fields silently.

Target ModelAvailability supports provider or runtime route.

A stable ModelSelectionBinding v2 requires separate schema proposal after R8 evidence.

---

# 8. Execution binding migration

During R8 use namespaced execution extension until stable schema promotion.

Legacy provider/ComfyUI/RunningHub execution remains compatibility until ExecutorRegistry parity.

No silent fallback.

---

# 9. Port/data binding migration

R6 introduces:

- PortTypeRegistry;
- typed InputBinding;
- Collection.

Legacy dict bindings remain readable.

Unknown semantics remain Legacy rather than guessed.

---

# 10. Prompt migration

Prompt becomes a first-class resource in R6.

Legacy prompt text/templates may remain readable.

Migration may introduce:

```text
PromptDefinition
PromptVersion
PromptRegistry
```

without requiring every Prompt to become a Codex Skill.

Skill/Workflow/Node references move toward versioned Prompt refs.

---

# 11. Skill migration

Workbench Skill remains a product capability.

Codex `SKILL.md` remains one optional implementation.

Where available, Workbench-managed Codex sessions may expose Workbench Skill roots using App Server-supported discovery/extra roots rather than copying files into global Codex configuration.

---

# 12. Provider/model migration

R7 backend becomes authority for:

- ProviderDefinition;
- ProviderConnection;
- ModelDefinition;
- ModelAvailability;
- normalized capabilities;
- availability health;
- direct-provider discovery;
- Codex discovery projections.

Browser hard-coded model/provider lists retire after parity.

Codex-discovered models become normal ModelAvailability choices.

---

# 13. Codex protocol compatibility migration

R7 hardens the R1 bridge.

Migration sequence:

1. inspect installed Codex;
2. obtain/compare official stable schema for tested version where used;
3. verify initialize/initialized;
4. verify required stable methods;
5. generate/validate DTOs;
6. normalize events/server requests;
7. bound event queues;
8. drain stderr;
9. fail pending calls on process EOF;
10. handle overload/retry policy;
11. keep experimental features behind optional adapters.

Do not place Codex protocol DTOs in Core domain.

---

# 14. Execution migration

R8 moves compatibility execution into:

- ExecutionProfile;
- RuntimeConnection;
- ExecutorRegistry;
- ExecutionRun/Attempt/Event;
- policy/cancel/usage.

CodexHarnessExecutor is an adapter around Harness, not a reimplementation of the Harness.

---

# 15. Asset/Artifact migration

Introduce:

- BlobRef;
- Asset/AssetVersion;
- Artifact/ArtifactVersion;
- Collection.

Absolute local path is not durable Asset identity.

Existing asset files/metadata may be imported into versioned records.

---

# 16. Catalog/Product migration

R9 introduces generic:

- Catalog;
- CatalogCategory;
- CatalogEntry.

WholeHouse Product Library is layered on Catalog + WholeHouse Entity definitions.

Do not migrate product-specific schema into Canvas/Core.

---

# 17. Entity migration

Formal project facts that need downstream consistency move into versioned Entity records.

Industry packages register Entity definitions.

---

# 18. Knowledge migration

Asset may feed Knowledge ingestion, but identities remain separate.

Formal execution captures KnowledgeSnapshot.

Vector search remains optional.

---

# 19. Workflow/Approval/Handoff migration

Workflow moves to:

- WorkflowDefinition;
- WorkflowVersion;
- WorkflowRun;
- NodeRun.

Business Approval/Frozen remains separate from Codex runtime approval.

Handoff becomes a durable manifest with version references/checksums.

WholeHouse V1 uses file/CAD handoff before direct external software control.

---

# 20. Workspace/resource-scope migration

R12 introduces resource scopes:

```text
personal
workspace
project
package
```

Shared Assets/Catalogs/Prompts/Skills/Workflows/Knowledge can be workspace-scoped.

Workspace profile remains an experience/default layer.

---

# 21. Integration migration

R8 defines generic integration contracts; R12 proves runtime.

Mechanisms may include:

- Native API;
- MCP;
- Local Bridge;
- File Handoff;
- Webhook;
- CLI;
- Human Handoff.

Codex-native Apps/MCP are projected rather than reimplemented.

---

# 22. Agent migration

R14 adds WorkbenchToolContract and GraphProposal.

Initial Agent mutation flow:

```text
read/search
-> compatibility
-> propose
-> user confirmation
-> base revision check
-> application services
```

Dynamic Tools may be an optional adapter, not the only Tool Bridge.

MCP or another stable adapter may carry the same WorkbenchToolContract.

---

# 23. Codex session linkage

If persistent association is needed, use a lightweight Workbench `CodexSessionLink`.

Do not duplicate all Codex Thread/Item history into Workbench DB.

Persist business-relevant execution/provenance and link to thread/turn IDs.

---

# 24. Package history migration

Persist:

- ProjectPackageLock;
- manifest/version hash;
- needed DefinitionSnapshots;
- applied migrations.

Disable/uninstall preserves historical readability.

---

# 25. Platform migration

## Typed settings

Move new configuration behind typed settings.

## MigrationRunner

Converge startup repairs and schema migration into versioned migration tracking.

## Storage

Domain uses BlobRef; storage adapter remains replaceable.

## Durable events

Execution/workflow state must survive browser disconnect and designed restart scenarios.

## Backup

Introduce formal backup/verify/restore.

## Feature flags

Every migration flag has removal Gate.

## Schema/API

Generate/validate Workbench schemas and frontend types systematically.

---

# 26. Legacy monolith responsibility migration

Legacy:

- `main.py`
- `static/js/canvas.js`
- `static/js/smart-canvas.js`

may retain compatibility behavior temporarily but do not receive new Workbench business systems.

Extraction pattern:

```text
characterize behavior
-> introduce modular seam
-> delegate Legacy caller
-> verify parity
-> remove old responsibility
-> remove compatibility path at Gate
```

Success metric is responsibility reduction, not cosmetic file splitting.

---

# 27. Rollback principles

Bounded rollback examples:

- R1/R7 App Server integration -> explicit Codex Exec compatibility where still supported;
- R3/R4 canonical DB -> validated pre-switch backup/import route during migration window;
- R7 registry -> Legacy provider compatibility during window;
- R8 executor -> explicitly selected compatibility executor during window.

Rollback never justifies permanent duplicate product runtimes.

---

# 28. WholeHouse migration boundary

WholeHouse lives under `packages/wholehouse/`.

Registers:

- Skills;
- Prompts;
- Entities;
- Catalog/Product definitions;
- Knowledge;
- Workflows;
- templates;
- review/handoff rules.

V1 ends at approved/frozen design + CAD/file handoff readiness.

Not V1:

- production/CNC;
- installation;
- after-sales;
- mandatory direct Agent control of Kujiale/GuiGui.

---

# Authoritative order

Use `IMPLEMENTATION_PLAN.md` for Round/Gate sequence.

Use `docs/status/CURRENT_EXECUTION_STATUS.md` for the only currently authorized Round.
