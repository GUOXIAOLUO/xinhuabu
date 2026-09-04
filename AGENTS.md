# AI Workbench Repository Rules

## Purpose and scope

This file governs the entire repository. The repository is an incremental second-stage development of `GUOXIAOLUO/canvas`; it is not a greenfield rewrite.

The product direction is a Web UI first, infinite-canvas AI Workbench with a generic Core and installable Industry Packs. The first supported Industry Pack is WholeHouse, but Core must remain useful when that pack is absent.

Before changing architecture or behavior, read these files in order:

1. `AGENTS.md`
2. `CURRENT_ARCHITECTURE.md`
3. `TARGET_ARCHITECTURE.md`
4. `MIGRATION_PLAN.md`
5. `IMPLEMENTATION_PLAN.md`
6. The affected source files and tests

When documentation conflicts with executable code, treat the executable code as the current-state fact, then update the documentation in the same change. Product hard constraints in this file remain mandatory unless the user explicitly approves a replacement architecture proposal.

## Product boundary

`AI Workbench Core` owns generic project, graph, execution, asset, knowledge, model, version, permission, and tool abstractions.

`WholeHouse Pack` owns whole-house-specific skills, entity definitions, workflow templates, knowledge, UI metadata, and validation rules.

The V1 client is a browser application. Do not introduce Electron, Tauri, native macOS, iOS, or Android clients without an approved proposal. The local FastAPI process may serve browser clients on localhost or a trusted LAN.

## Hard architecture constraints

### Core is industry-neutral

Do not place whole-house concepts such as cabinet, wardrobe, material, hardware, room, or wholehouse business rules in Core modules. Industry identifiers may appear in generic test fixtures and pack-loading integration tests, but Core behavior must not branch on them.

Put WholeHouse implementation under `packages/wholehouse/`. A disabled or absent WholeHouse Pack must not prevent Core from starting or serving generic projects and canvases.

### Canvas is business-neutral

Canvas Core may understand nodes, edges, groups, ports, position, size, selection, viewport, zoom, graph interaction, and generic execution state. It must not decide what a floorplan, cabinet, contract, or design-review node means.

Do not add one Canvas node class or render branch per Skill. The migration target is:

`NodeRecord + NodeShell + RendererRegistry + SkillDefinition`

The finite renderer set may grow through a reviewed registration contract. The number of Skills must not cause a matching increase in Canvas Core branches.

### Node creation has one service boundary

All new node-entry paths must call `NodeCreationService`, including context menu, command palette, Skill Library drag, file drop, workflow import, and Agent proposals.

Do not add another direct `nodes.push(<node>)` path for migrated node kinds. Existing direct creation functions are Legacy and remain supported until their callers have migrated.

### Skills are dynamic and model-independent

A Workbench Skill is discovered from a versioned manifest and execution instructions. Adding a conforming Skill must not require editing the main Canvas node menu or render dispatch.

A Skill declares capability requirements; it does not select a provider or model. The model-selection precedence is fixed:

1. current Node user selection;
2. user default for the Skill;
3. user system default.

The system may filter incompatible models and recommend a model, but it must not silently switch the user's selection.

### Project data is authoritative

Project records, canvas graph state, formal requirements, dimensions, assets, workflow versions, approvals, and final artifacts belong to project persistence. Codex or chat threads may retain reasoning and conversation, but they are not the source of truth for project deliverables.

### Knowledge and Asset are separate domains

Knowledge represents facts, documents interpreted as knowledge, structured records, and retrieval indexes. Asset represents owned files and their metadata. Do not merge them into one vector-store abstraction.

### Workflow and provenance are versioned

Workflow is a dynamic graph that can be created, edited, saved, duplicated, versioned, run, paused, resumed, retried, imported, and exported.

Every formal output must be traceable to its Node version, Skill ID and version, provider, model ID, parameters, inputs and input versions, Asset versions, Knowledge snapshot, Workflow version, parent version, user, and timestamp.

Dependency changes create an `outdated` result; they do not delete the prior result. Frozen results require explicit human approval.

### Agents use APIs, not DOM control

Codex is the orchestration runtime, not the only model provider. Agent code must call stable Workbench, Canvas, Project, Skill, Workflow, Asset, Knowledge, Model, or MCP APIs. It must not use selectors, synthetic clicks, or element dragging to change project state.

Agent-created graph changes are proposals by default. Bulk changes require user confirmation unless a user has explicitly enabled an auto-modify policy.

### Secrets remain backend-only

Provider secrets must never be returned to browser code, embedded in Canvas records, logged, committed, or stored in browser storage. Browser clients may receive `has_secret` metadata and a non-sensitive provider identifier; do not return the secret or a reversible representation.

All provider calls flow through the backend. New endpoints require authentication and authorization design, project-scope checks where applicable, bounded input validation, and audit events for sensitive actions.

## Current-system compatibility rules

The existing application is a FastAPI and static HTML/CSS/JavaScript monolith. `main.py`, `static/js/canvas.js`, and `static/js/smart-canvas.js` are high-risk compatibility surfaces.

Until migration gates pass:

- Keep Classic Canvas and Smart Canvas loadable.
- Keep current Canvas JSON readable.
- Keep current provider, ComfyUI, RunningHub, MiniMax, LLM, Prompt, Image, Output, Loop, Group, and workflow paths operational.
- Mark migrated fixed node kinds as Legacy through adapters; do not delete them.
- Preserve unknown fields when adapting or re-saving Legacy nodes.
- Do not mass-move functions merely to create a cleaner directory tree.
- Do not change the frontend framework without an approved proposal.
- Do not replace JSON persistence or SQLite/PostgreSQL strategy without an approved proposal.

The first compatibility boundary is a pure adapter: Legacy Canvas JSON in, validated `NodeRecord` view out, with a lossless path back to the existing storage shape during the transition.

## Intended dependency direction

New backend code must follow this direction:

`API routes -> application services -> domain -> repository/runtime interfaces`

Adapters and infrastructure implement interfaces; domain code must not import FastAPI, filesystem paths, provider SDKs, ComfyUI protocol details, or Industry Packs.

New frontend code must follow this direction:

`page adapters -> Canvas application services -> domain records/registries -> renderer implementations`

Renderer implementations receive safe view models and emit user intents. They do not write storage or call provider endpoints directly.

Cross-domain references use stable IDs and version IDs. Do not pass mutable filesystem paths as formal domain identity.

## State and schema rules

Use one centralized Node state vocabulary:

- `draft`
- `ready`
- `missing_input`
- `queued`
- `running`
- `waiting_user`
- `waiting_approval`
- `completed`
- `failed`
- `outdated`
- `frozen`

All persisted schemas require a `schema_version`. Public manifests require JSON Schema validation and explicit compatibility rules. IDs are opaque strings; do not infer business meaning by parsing an ID.

`SkillDefinition` and `SkillInstance` are different records. Multiple nodes may reference the same definition version.

Model capabilities, input types, and output types are registry metadata. Provider-specific parameters belong in provider adapters or a namespaced extension object, not in generic Canvas logic.

## Security baseline

Treat the current localhost/LAN deployment as untrusted by default because the server binds to `0.0.0.0`.

For every changed endpoint, check:

- authentication and project authorization;
- CORS behavior;
- path traversal and symlink escape;
- upload size, type, and content validation;
- remote URL allowlisting and SSRF protections;
- secret redaction in response bodies, exceptions, and logs;
- command execution and subprocess argument boundaries;
- destructive-action confirmation and audit records;
- concurrency and stale-write behavior.

Do not weaken the existing path-containment checks. Do not add new browser-side token fallbacks. Remove Legacy browser token paths only through a compatibility migration with tests.

## Development method

Use gate-based, incremental development.

Before implementation:

1. Inspect the affected current code paths and current worktree.
2. State the compatibility contract.
3. Identify new and modified files.
4. Add or update tests that fail for the missing behavior.
5. Prefer a small seam over a broad rewrite.

During implementation:

- Preserve unrelated user changes.
- Keep diffs focused.
- Add types at new boundaries.
- Use structured errors and useful logs without secrets.
- Avoid duplicate code paths for the same domain action.
- Maintain read compatibility before changing write behavior.
- Put feature flags or compatibility switches at service boundaries, not scattered UI branches.

After implementation:

1. Run focused tests.
2. Run the repository baseline checks.
3. Exercise the relevant browser flow manually.
4. Verify Legacy Canvas loading and saving when Canvas persistence changes.
5. Update architecture and migration documents if a contract changed.

## Baseline commands

The repository currently has no pinned development environment. Install runtime requirements into an isolated environment before running Python tests:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Run syntax checks for the high-risk entry points:

```bash
.venv/bin/python -c "import ast,pathlib; ast.parse(pathlib.Path('main.py').read_text(encoding='utf-8')); print('main.py AST OK')"
node --check static/js/canvas.js
node --check static/js/smart-canvas.js
```

When a new package or tool is introduced, document one reproducible install command and pin or constrain versions before making it part of the required baseline.

## Definition of Done

A change is complete only when all applicable items are true:

- The requested behavior is implemented without placeholders.
- The change obeys Core/Industry Pack and Canvas/business separation.
- Persisted or public schemas are versioned and validated.
- Backward compatibility is tested or the approved breaking change is documented.
- Security-sensitive routes have authentication, authorization, validation, and audit treatment appropriate to their risk.
- Focused automated tests pass.
- Relevant syntax/static checks pass.
- Manual verification steps are recorded and reproducible.
- Architecture and migration documents match the code.
- No provider secret appears in browser storage, responses, logs, fixtures, or commits.
- The worktree contains no accidental generated artifacts.

## Architecture gates

### Gate 1: dynamic Skill

A new conforming Skill folder is discovered, appears in Skill Library, creates a Skill node, and executes without a change to Canvas node creation or rendering source. Do not scale WholeHouse Skill development before this gate passes.

### Gate 2: user-selected model

One Skill executes with at least two compatible provider/model choices selected by the user. The Skill definition remains unchanged, and no runtime silently changes the selection.

### Gate 3: Codex dynamic workflow

Codex reads Canvas selection through an API, searches Skills, proposes a workflow, waits for confirmation, creates nodes through the domain API, executes, and records a traceable result.

## Proposal-required decisions

Stop and write a proposal before any of these changes:

- replacing the frontend framework;
- replacing the primary database strategy;
- deleting a Legacy node family or Canvas mode;
- changing the canonical NodeRecord incompatibly;
- changing the Codex Harness/App Server integration contract;
- introducing a large infrastructure dependency;
- enabling Agent auto-modification by default;
- placing Industry Pack behavior in Core.

Each proposal must contain Problem, Constraints, Options, Recommendation, Migration Cost, Compatibility Impact, Security Impact, Rollback, and Acceptance Criteria.

## V1 non-goals

Do not expand V1 into production ERP, CNC, automatic nesting, production scheduling, edge banding, packaging, logistics, installation, after-sales, full CRM, public Skill Marketplace, native desktop/mobile applications, autonomous control of Kujiale or Guigui, complex enterprise RBAC, multi-industry commercial operation, or production-grade automatic order splitting.

The V1 handoff boundary is a versioned Design/CAD Handoff containing inspectable JSON, PDF, CSV, and image artifacts. SVG and DXF come only after the handoff contract is stable.

## Required completion report

Every implementation round must report:

1. completed work;
2. modified files;
3. added files;
4. deleted files;
5. architecture changes;
6. database changes;
7. API changes;
8. UI changes;
9. compatibility impact;
10. automated test results;
11. manual test steps;
12. known issues;
13. recommended next step.

Do not report completion when required tests could not run. Report the exact blocker and distinguish authored changes from verified behavior.
