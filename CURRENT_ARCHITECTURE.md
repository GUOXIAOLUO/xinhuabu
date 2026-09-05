# Current Architecture Baseline

## Document status

This file describes the live repository verified during R0. It does not describe
the target architecture. Target contracts remain in `TARGET_ARCHITECTURE.md`.

Verified from the local worktree on 2026-09-04 at commit
`23f7895ae55bde9f76f3c1e6d4ac0f2e913531bd` (`main`, three commits ahead of
`origin/main`). The worktree was clean before R0 documentation edits.

### Historical audit metadata

The preceding architecture audit was made on 2026-09-02 against `544a5a0` and
described an earlier migration state. Its measurements are historical evidence
only. Its claims that NodeRecord, NodeCreationService, RendererRegistry, and
`/api/v1` node routes did not exist are not current facts and are replaced below.

## Executive finding

The application remains a local-first AI media studio implemented primarily by a
large FastAPI monolith and two large browser Canvas scripts. SQLite CanvasRecord is
the default page/runtime authority after explicit activation; Legacy JSON/filesystem
remain bounded import and rollback compatibility. The repository now also contains versioned
NodeRecord/EdgeRecord views, lossless Legacy adapters, restricted
NodeCreationService/NodeMutationService/GraphMutationService boundaries,
localhost-only `/api/v1` node routes, and opt-in shared Canvas runtime, NodeShell,
RendererRegistry, renderer, Inspector, graph, group, and creation-catalog modules.

These are migration seams, not the target Workbench. R3 now adds a tested SQLite
ProjectRecord/ProjectMember/CanvasRecord repository, action-based canonical
authorization, a lossless Legacy import/compare/rollback service, transactional
audit/outbox, and an explicit migration-report command. SQLite authority state is
activated after R3's verified import/compare (22 imported, none skipped or
different). R4 adds a SQLite compatibility repository with true SQL CAS and
default-on canonical routing after activation. The retained Classic/Smart editor
adapters share persistence, update-message, polling, workflow transfer, execution-result media normalization, media URL normalization/preview routing, media-reference filtering, MIME/extension media-kind classification (also used by the shared MediaRenderer), native-video event isolation, preview-failure fallback binding, native-media playback-state preservation, image-dimension loading/positive field copying, high-resolution candidate collection/async decode preloading, pure intrinsic-media/thumbnail sizing, and pure media-grid fitting, plus a side-effect-free graph fragment for subgraph/clipboard/materialization/removal, NodeShell,
and renderer seams, but remain duplicate product runtimes. There is no DefinitionResolver,
SkillRegistry, ProviderConnection or
ModelAvailability registry, ExecutorRegistry, formal Asset/Artifact/Entity/
Knowledge runtime, Workflow/Approval/Handoff runtime, or PackageRuntime. R1 adds a
bounded Codex App Server transport seam, not an execution/domain runtime.

## Repository and runtime shape

| Area | Current implementation and responsibility |
|---|---|
| Backend | `main.py`: FastAPI app, 165 route decorators, providers/CLIs, JSON/filesystem storage, update/subprocess/media/chat/Canvas/workflow/asset behavior, and migrated-node wiring |
| Backend seams | `workbench/domain`, `application`, `repositories`, `api`: records, Legacy adapters/repositories, renderer manifests, node/graph services, JSONL audit, `/api/v1` router |
| Classic Canvas | `static/canvas.html` + `static/js/canvas.js`: broad fixed-node graph editor and Legacy execution/UI |
| Smart Canvas | `static/smart-canvas.html` + `static/js/smart-canvas.js`: media-first composer and Smart Prompt/Loop/Group/MiniMax execution/UI |
| Shared Canvas seams | `static/js/workbench/canvas/*.js`: opt-in runtime state, geometry, graph/group intents, creation catalog/client, entry compatibility resolver (handoff, Canvas-list project memory and URL construction), text-copy fallback/clipboard verification, injected image-size calculation, configurable editable-target detection, media URL normalization/preview routing, MIME/extension media-kind classification, native-video event isolation, preview-failure fallback binding, and high-resolution candidate collection/async decode preloading, NodeShell, renderer registry/host, media/Legacy renderers, Inspector, semantic zoom, screen-space controls |
| Projects/list | `static/canvas-list.html` + `static/js/canvas-list.js`: still exposes and routes separate Classic/Smart kinds |
| Provider settings | API settings page and `main.py` routes: provider metadata/model lists, health checks, backend credential writes |

`python3 main.py` starts Uvicorn on `127.0.0.1:3000` by default. Explicit
`WORKBENCH_HOST=0.0.0.0` or `::` enables unauthenticated LAN compatibility mode.
There is no identity provider, worker process, or durable job queue.

## Unified Canvas U0-U7

| Stage | Status | Verified current fact |
|---|---|---|
| U0 | complete | Approved proposal, inventory, Classic/Smart fixtures, lossless round-trip tests, and unique-entry compatibility contract exist. |
| U1 | complete | Both adapters can opt into one side-effect-free CanvasRuntime for viewport, selection, move, resize, and geometry. Default is off. |
| U2 | complete | Shared graph geometry, port-drop intent, port compatibility, group membership, and command seams are used by both adapters. Smart port hover and final drop both use the shared data-type contract; complete interaction ownership remains in Legacy scripts pending U7. |
| U3 | complete | NodeShell, browser RendererRegistry, NodeCardHost, UnifiedRenderHost, two renderers, Inspector, semantic zoom, and screen-space controls exist with opt-in adapters/tests. Smart Group, Image, and Legacy node adapters submit batch card mounts through the shared host; its behavioral test verifies ordered frozen results and invalid-input rejection. Rendering remains split and gated pending U7. |
| U4 | complete | Shared creation catalog/IDs and restricted versioned blank/connected paths exist. Classic blank Image/Prompt/Loop/Group/Output and Smart blank Image/Prompt/Loop/Group/MiniMax menu creation can use NodeCreationService only on the explicitly enabled loopback compatibility path. Unmigrated constructors, uploads/imports, menus, and direct Legacy mutations remain compatibility paths. |
| U5 | complete | Shared result-placement intent and a narrow Classic/Smart compatibility execution wrapper exist. Behavioral tests verify frozen completion metadata, retained-error failure metadata, and both page entries delegating to the wrapper with Legacy fallbacks; Legacy execution remains authoritative. No unified executor adapter/runtime exists. |
| U6 | complete | Canvas list creates one normal Canvas choice, hides Legacy source-kind labels, and opens `canvas.html` for every record. A shared side-effect-free entry resolver scopes historical Smart handoff to records that require it. One runtime is intentionally not complete until U7. |
| U7 | in progress | SQLite compatibility persistence is the default route after activated authority and true SQL CAS. Legacy JSON is bounded import/rollback compatibility. Classic/Smart still retain duplicate construction, rendering, interaction, and execution runtimes, so page/runtime removal and flag retirement are not authorized. |

### Feature and compatibility gates

Backend defaults:

- `WORKBENCH_HOST=127.0.0.1`; `WORKBENCH_PORT=3000` (validated 1-65535).
- `WORKBENCH_ALLOWED_ORIGINS` defaults to loopback origins for that port and rejects
  wildcard origins.
- `WORKBENCH_LAN_ENABLED` is false unless host is `0.0.0.0` or `::`.
- `WORKBENCH_NODE_API_ENABLED` is true only for loopback host values; the `/api/v1`
  router is not registered in LAN mode.
- `WORKBENCH_CANONICAL_CANVAS_ROUTING_ENABLED` defaults true. It selects SQLite
  compatibility persistence only when explicit SQLite authority state is `sqlite`;
  explicit false remains the bounded U7 rollback control.

Browser URL gates are default-on when absent and use explicit `=0` rollback:
`unified_canvas`, `node_shell`, `legacy_renderer`, `media_renderer`,
`semantic_zoom`, and `screen_space_controls`. Renderer/Shell paths also require
loopback; semantic zoom requires NodeShell. The benchmark harness forwards only
this allowlist.

## Persistence and record contracts

Canvases remain mutable `data/canvases/<id>.json` files at the active runtime
authority. R3 also provides `SqliteProjectCanvasRepository`, which stores complete
lossless Legacy payload JSON with separately versioned ProjectRecord, ProjectMember,
CanvasRecord metadata, logical Canvas revision, and explicit authority state. Its
`legacy_json` default is intentional: import/backfill and payload comparison must
pass before a controlled `sqlite` state can be activated; rollback exports the
original payloads and restores `legacy_json`.
`LegacyJsonCanvasRepository` preserves unknown fields, hides soft-deleted records,
and serializes changes under a process-local lock. `updated_at` advances
monotonically and acts as the compatibility revision; it is not a canonical logical
`CanvasRecord.revision`. Whole-Canvas Legacy routes remain authoritative. Migrated
node APIs write compatible dictionaries into the same files. Opening a Classic
Canvas no longer performs a touch write.

`workbench.node/1` and `workbench.edge/1` Pydantic models and JSON schemas exist.
NodeRecord contains identity/project/canvas, finite Core kind, versioned definition
and renderer references, NodeState, title/geometry, ports, dictionary input
bindings, AssetVersion/ArtifactVersion output refs, optional ModelBinding,
config/provenance, actor/timestamps, positive revision, metadata, and extensions.
ModelBinding requires `provider_id` and `model_id` together but does not identify a
canonical ModelAvailability. EdgeRecord has explicit node/port endpoints,
active/disabled state, metadata, and positive revision. Legacy adapters use
`legacy.out`/`legacy.in`, derive revision from `updated_at`, and retain the complete
source payload for lossless round-trip. These records are validated views, not a
separate persistence authority.

## NodeCreationService

The command contract enumerates context menu, command palette, Skill Library drag,
file drop, workflow import, Agent proposal, and Legacy sources; not all product entry
paths have migrated. Classic blank Image, Prompt, Loop, Group, and Output plus Smart
blank Image, Prompt, Loop, Group, and MiniMax context-menu creation use the restricted
service path only when explicitly enabled on loopback.
The service validates identity and an optional positive
expected revision, calls `can_edit`, resolves through temporary
`LegacyDefinitionRegistry`, checks definition enabled/version, rejects an absent or
incompatible model when applicable, constructs NodeRecord, and uses an injected
repository. Current Legacy definitions require no model and the policy rejects any
supplied model rather than silently substituting it.

The Legacy repository supports approved Image, Prompt, Loop, Group, Output, Smart Prompt,
Smart Loop, Smart Group, and Smart MiniMax shapes. It persists idempotency request
metadata. Missing expected revision is allowed for standalone creation; supplied
revisions use `updated_at` conflict checking. Persistence precedes JSONL audit and
the two writes are not atomic.

## NodeMutationService

The update command can mutate exactly `title` and `position`; deletion is also
supported. Both require `can_edit` and a positive expected revision. The current
Legacy repository limits update/delete to Image nodes, and deletion removes
connected edges. Canvas persistence occurs before JSONL audit and is not atomic
with it.

## GraphMutationService

The only supported graph transaction is create-one-node plus create-one-edge. It
validates identity, positive expected revision, Canvas identity, an edge reference
to the new node, and `can_edit`. `create_from_node_command` prepares through
NodeCreationService and builds `legacy.out`/`legacy.in` endpoints. The Legacy
repository appends a restricted node and `{id, from, to, kind: "input"}` edge under
one Canvas lock/revision. Persistence and JSONL audit remain separate.

Standalone Node creation keeps Legacy-compatible optional `expected_revision`.
Connected creation is now explicitly different: `CreateNodeAndEdgePayload` requires
a positive revision, and `create_from_node_command` rejects a missing revision before
preparing a node. It passes the supplied revision unchanged into the graph mutation;
no missing value is normalized to `0`. This R2 repair preserves stale-write behavior
without changing NodeRecord or persistence authority.

## Rendering and shared Canvas modules

Python and browser RendererRegistry foundations exist. Python resolves versioned
RendererManifest records. Browser NodeCardHost registers MediaRenderer and a
source-payload LegacyRenderer, constructs NodeShell, and UnifiedRenderHost supplies
a page-neutral card boundary plus a batch adapter-card mounting entry point. Smart
Group, Image, and Legacy node adapters construct their card entries and pass them to
that shared entry point. NodeShell owns generic chrome, title/status,
selection/focus/menu/delete, drag/resize/connect intents, ports, content/toolbar
slots, and a model label; it owns neither persistence nor execution. Both pages have
opt-in adapters but retain large type-specific bodies, controls, rendering, and
execution. Node Inspector is read-only/ephemeral; target mutation UX is absent.

R2 adds a browser-side `WorkbenchCanvasPortCompatibility` contract. Both Legacy
page adapters delegate final port-drop acceptance to it before their existing
connection/persistence state machines run; Smart also delegates typed port-hover
eligibility to it. Unspecified Legacy ports use
`legacy.any` and remain compatible; explicitly typed endpoints must match. The
module is DOM/storage/network-free and does not branch on node or provider type.

R2 also adds `WorkbenchCanvasExecutionCompatibility`. The Classic generic-generation
entry and Smart primary-generation entry delegate through this wrapper, which
normalizes completion/failure metadata around the existing callbacks. It neither
selects nor substitutes a model/provider/runtime, persists data, or implements an
ExecutorRegistry; retained Legacy functions still execute and place results.

## Provider/model/settings and Codex

Provider metadata is normalized in `main.py`, seeded from built-in/static files,
and written to `data/api_providers.json`. Model lists/protocol maps remain provider
fields and frontend selectors. Secrets are written to ignored `API/.env`; public
responses expose configuration state/masked metadata, not raw keys. The Legacy
`/api/config/token` returns only `{configured: boolean}` and Legacy ModelScope key
payloads are ignored. There is no ProviderDefinition/ProviderConnection split,
CredentialRef, ModelRegistry, ModelAvailability, capability vocabulary, or shared
compatibility service.

Codex remains a provider/worker compatibility path. `main.py` locates `codex` or
`CODEX_BIN` and invokes `codex exec --cd <repository> --sandbox workspace-write
--skip-git-repo-check`, optionally passing model/images/output-last-message, with a
bounded timeout.

R1 adds `workbench.codex.CodexBridge`, a narrow async stdio JSONL bridge for Codex
App Server protocol v2. It was verified with installed `codex-cli 0.153.1` and its
generated schema. `HarnessLaunchPolicy` constrains cwd to the configured workspace,
allowlists child environment variables, uses read-only/no-network turns and
`approvalPolicy: never`, normalizes server events, denies server requests by
default, and supports thread start/resume, simple turns, model/config discovery,
interruption, shutdown, and explicit recovery. It exposes no Workbench domain tools,
does not persist raw events, and is not wired into Legacy HTTP routes. The existing
`codex exec` flow is retained through a compatibility adapter boundary.

## Authority map

| Domain | Current authority |
|---|---|
| Project | `data/projects.json` via `main.py` remains default page/route authority; SQLite ProjectRecord/ProjectMember records are a verified canonical foundation but not default route authority |
| Canvas | SQLite CanvasRecord is the default page/route authority after a verified 22-payload backfill/compare and activated authority state. `data/canvases/*.json` is retained only for import/rollback compatibility; Unified Canvas runtime cutover remains incomplete |
| Node/Edge | Dictionaries embedded in Canvas JSON; NodeRecord/EdgeRecord are views |
| Asset | Configured asset files plus JSON library/storage/shared-folder metadata; no AssetVersion |
| Workflow | Mutable `workflows/*.json`/configs plus Canvas archives/library items; no WorkflowVersion/Run |
| Audit | `data/audit/canvas-node-events.jsonl` for migrated node/graph actions only; non-transactional and incomplete |

Artifact, Entity, Knowledge, Approval, Handoff, and package-history authorities do
not exist.

## R3 canonical identity, authorization, and audit foundation

`LegacyIdentityMapper` maps `project: "default"` to the stable default ProjectRecord
and `owner: ""` to `local_unowned`, without creating a user identity. A non-empty
Legacy owner maps to a stable `legacy-owner:<owner>` local actor and Editor member;
an unknown project is reported as `project_mismatch` and skipped from automatic
import. `AuthorizationService` currently enforces `project.read` for Owner/Editor/
Viewer and `canvas.edit` for Owner/Editor at the canonical boundary. This is a
local migration mapping, not global authentication or a claim that LAN mode is
multi-user safe.

Canonical mutation requires the independent positive logical revision. The Canvas
payload update and `audit_outbox` insert use the same SQLite transaction; an audit
insert failure rolls the Canvas change back. Existing JSONL audit remains a separate
Legacy compatibility path until switch completion.

`tools/migrate_project_canvas.py` requires explicit Legacy project and Canvas source
paths plus a SQLite/report destination. It only backfills and compares by default;
`--activate` is required for an authority-state switch and refuses activation when a
source Canvas was skipped or differs. It has been tested only with temporary
fixtures and once against the live `data/` directory: 22 Canvas payloads imported,
0 skipped, and 0 differences. That report did not pass `--activate` and rewrote no
Legacy source file.

## Authorization and security

There is no global authentication or authorization. Most Legacy routes, WebSocket,
project/Canvas, provider administration, file/workflow, and update operations are
available to any client that reaches the server.

The transitional `/api/v1` node routes require caller-supplied `X-User-ID`, exist
only on loopback, and use `LegacyCanvasProjectAuthorizer`: project must match; a
non-empty owner must match the header; local wiring permits unowned Canvases via
`allow_unowned_local=True`. This is a scoped compatibility check, not authenticated
identity or target authorization.

CORS defaults to loopback and rejects wildcards, but LAN mode remains explicitly
unauthenticated. Secret-boundary, path-containment, media cleanup, and stale-write
tests pass. R3 has a canonical action policy and atomic audit transaction, but
neither is uniform across the active Legacy surface; no Legacy-wide SSRF policy or
subprocess/tool-permission boundary exists.

## Performance baseline

R2 latest reran `node tools/benchmark-canvas-payload.mjs`: 9,622 bytes for 100 nodes
(0.108 ms serialization) and 29,132 bytes for 300 nodes (0.096 ms), with
sub-millisecond serialization. The latest browser
evidence is `docs/benchmarks/canvas-node-shell-baseline-2026-09-04.md`: its visible
300-node Safari NodeShell sample recorded load 152 ms, render ready 362 ms, zoom 38
ms, pan 104 ms, and minimap 15 ms. The earlier offscreen 300-node minimap sample was
149 ms (141 ms recheck), retained as a P2 iframe-scheduling follow-up. These are
single local observations, not release/percentile budgets.

R4 reran the deterministic payload check after enabling the SQLite compatibility
route in an isolated local process: 9,622 bytes/0.142 ms for 100 nodes and
29,132 bytes/0.090 ms for 300 nodes. This does not replace browser interaction
acceptance.

## Legacy monolith responsibility baseline

| File | Size | Responsibilities still present | Already delegated/extracted |
|---|---:|---|---|
| `main.py` | 18,395 lines; 828 top-level functions; 75 classes; 162 routes | Composition plus most provider/model/secret/subprocess/generation/chat/project/Canvas/asset/workflow/media/queue/event and Legacy API behavior | Node router/services, records/adapters, Legacy repositories, renderer registry, JSONL audit live under `workbench/`; `main.py` wires them. Repository self-update responsibility and runtime GitHub-hosting fallback are removed. |
| `static/js/canvas.js` | 16,686 lines | Classic create/render/connect/execute, provider UI, graph/save/workflow/asset/log/minimap/selection/geometry behavior | Opt-in runtime, geometry, graph/group intents, catalog/client, records, entry compatibility resolver, NodeShell, renderer host/registry/renderers, Inspector, semantic zoom, screen controls; explicitly enabled blank Output creation delegates through the restricted NodeCreationService path |
| `static/js/smart-canvas.js` | 20,085 lines | Smart composer/create/render/connect/execute, provider/media/MiniMax, graph/save/group/minimap/selection/geometry behavior | Uses the same opt-in shared modules through adapters; Smart Group/Image/Legacy NodeShell card batches mount through `UnifiedRenderHost`; explicitly enabled blank MiniMax creation delegates through the restricted NodeCreationService path |

R0 added no Workbench business responsibility to these files and removed/delegated
none; it changed documentation only. R1 adds no Workbench business responsibility to
these Legacy monoliths; the Codex transport is new code under `workbench/codex/`.
R2 adds no Workbench business responsibility to them: Classic blank Output and Smart
blank MiniMax creation, Classic/Smart port-drop and execution compatibility delegate to shared modules, Smart NodeShell batch-card
mounting delegates to `UnifiedRenderHost`, and historical Smart-entry detection/URL
construction delegates to the shared entry compatibility resolver.

## Verification baseline

- Latest R4 baseline, `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest
  discover -s tests -q`: 240 tests passed in 2.409 seconds.
- Python AST: `main.py`, 30 `workbench/**/*.py` files, and two migration/backup
  tools passed (33 files total).
- JavaScript: 42 files, including Classic, Smart, Canvas-list, and shared Canvas
  modules, passed `node --check` using `/Users/lo/.local/node-v24.20.0/bin/node`
  (Node v24.20.0).
- R2 tests prove connected creation rejects a missing revision at the API boundary
  and before node preparation, rejects zero/negative revisions, while valid
  revisioned graph mutations still persist.
- NodeMutationService/API tests verify the update boundary accepts only `title` and
  `position` mutations (plus identity/revision fields) and rejects extra payload
  fields.
- GraphMutationService tests cover both edge directions while preserving the
  `legacy.out -> legacy.in` port contract.
- R2 execution-compatibility tests verify normalized completion metadata and
  preserved Legacy errors annotated with failed Canvas/node metadata; the wrapper
  does not select providers, models, or executors. Classic and Smart generation
  entry tests verify their respective Legacy callbacks and fallback paths.
- R2 browser acceptance on the local server verified the one normal list entry:
  a Classic record opened `canvas.html`, while a historical Smart record entered
  through that list and then reached its retained `smart-canvas.html` adapter.
  No Canvas data or execution was mutated during this check.
- R2 browser acceptance also loaded both adapter pages with explicit shared Canvas
  flags (`unified_canvas`, NodeShell, both renderers, semantic zoom, and
  screen-space controls). Classic and Smart both displayed shared NodeShell
  ready/port controls and semantic summaries without a data mutation.
- R1 bridge tests passed against a fake stdio peer; a live non-mutating App Server
  `initialize`, `model/list`, and `config/read` smoke check passed with
  `codex-cli 0.153.1`.

R0 changed no product source, schema, persistence, API, or runtime behavior.
