# Current Execution Status

status_schema: workbench.execution-status/2

## Repository

repository: local worktree (remote repository out of scope)
verified_head: 23f7895ae55bde9f76f3c1e6d4ac0f2e913531bd
verified_commit: "docs: refine migration architecture plan"
branch: main
remote_state: not checked; GitHub/remote synchronization is out of scope for this local task
verified_at: 2026-09-05T08:18:02+08:00
verification_source: current local worktree
worktree_before_R0: clean
worktree_after_R4_partial: dirty_only_by_R0_R1_R2_R3_and_R4_changes

## Product contract

product: generic AI Workbench
client_v1: Web UI
orchestration_target: Codex Harness / App Server
wholehouse_role: first Industry Package, not Core
canvas_target: one Unified Canvas
current_persistence_authority: SQLite CanvasRecord for normal Canvas routing; Legacy JSON/filesystem compatibility elsewhere
agent_dom_mutation_allowed: false
silent_model_provider_executor_fallback_allowed: false

## Active Round

active_round: R4
active_round_name: Unified Canvas Cutover
round_status: in_progress
blocking_issues: []

R3 is complete. R4 is active. R3 supplied the SQLite Project/Canvas foundation, explicit identity mapping,
revision, authorization, migration comparison, rollback export, transactional
audit/outbox, and migration-report command are tested. The live Legacy report at
2026-09-04T23:36:06Z imported 22 Canvas files, skipped 0, and found 0 payload
differences. R4 now has a tested SQLite compatibility repository with true SQL
compare-and-swap. SQLite authority was activated locally after the validated
backup/compare (22 payloads), and canonical routing is now the default runtime when
that authority state is `sqlite`; an explicit false value is a bounded rollback
control while U7 remains in progress. Isolated API, browser read, browser write,
restart, stale-conflict, and rollback-export acceptance passed. The retained
Classic/Smart editor adapters now share the neutral CanvasRecord load/save/metadata
client, version-poll coordinator, and transport-neutral update-message filter;
their existing polling intervals and merge behavior remain adapter-owned.
The shared state runtime is now default-on, with `unified_canvas=0` retained as
the bounded U7 rollback control. Read-only browser rechecks of both Classic and
historical Smart records passed on the default URL path; this does not yet
authorize page deletion. NodeShell base is also default-on on loopback, with
`node_shell=0` retained as its bounded U7 rollback control. MediaRenderer is
default-on on loopback with `media_renderer=0` as its bounded U7 rollback control.
Legacy source-payload rendering inside NodeShell is also default-on, with
`legacy_renderer=0` retained as its bounded U7 rollback control.
Semantic zoom is default-on with `semantic_zoom=0` retained as its bounded U7
rollback control.
Smart screen-space controls are default-on with `screen_space_controls=0`
retained as their bounded U7 rollback control.
The historical Smart handoff now preserves query parameters while replacing the
Canvas id and cache version, so the explicit all-zero rollback is effective from
the normal Canvas URL as well as the retained adapter URL.
Canvas list and asset-manager openings now both use the normal `canvas.html`
entry through the same `normalCanvasUrl` contract; direct Smart page routing is
confined to the retained compatibility boundary.
The asset manager now presents a single business-neutral `画布` category and no
longer exposes Classic/Smart source labels or filters; retained `kind` is
compatibility metadata only.
Classic and Smart workflow import/export now share one transport-only archive
client for the existing backend contract. Each retained adapter still owns its
selection payload, node insertion, save scheduling, and UI feedback.
An automated source-reference guard verifies that Canvas list, asset manager, and
the Canvas editor contain no direct Smart page URL; only the compatibility module
may construct that historical deep link.
The Canvas editor also no longer duplicates the Smart `kind` check; it delegates
the handoff decision exclusively to that compatibility module.
Legacy JSON remains the bounded import/rollback adapter, and duplicate page/runtime
removal has not occurred.

R4 source backup/validation is complete locally: `data/canvas-source-backups/`
contains a verified 22-file snapshot with manifest SHA-256
`180e3064d10487441d7ffba26f878194ec5b93013d0f883311ad3b2a64f7dec8`.
The generic repository contract now covers metadata writes, listing, and expired
trash cleanup, plus project-delete Canvas reassignment. Media cleanup intentionally
retains its conservative Legacy unreadable-source scan until an equivalent canonical
diagnostic exists.

## Unified Canvas verified ledger

| Stage | Status | Evidence summary |
|---|---|---|
| U0 | complete | Approved proposal, inventory, golden fixtures, lossless round-trip tests, unique-entry contract |
| U1 | complete | Shared CanvasRuntime/recovery/coordinates used by both adapters behind an off-by-default flag; tests pass |
| U2 | complete | Shared graph geometry, port-drop, port compatibility, group membership, and commands are used by both adapters; Smart hover and final drop use the same typed compatibility contract. Full interaction ownership remains Legacy pending U7. |
| U3 | complete | NodeShell, registries/host, renderers, Inspector, semantic zoom, and screen controls are shared opt-in adapters; Smart Group/Image/Legacy batches mount through UnifiedRenderHost, whose behavioral test verifies ordered frozen results and invalid-input rejection. Render paths remain gated pending U7. |
| U4 | complete | Shared catalog and restricted versioned creation/graph APIs are used by Classic blank Image/Prompt/Loop/Group/Output and Smart blank Image/Prompt/Loop/Group/MiniMax menus when explicitly enabled on loopback. Unmigrated page-owned constructors/imports remain compatibility paths. |
| U5 | complete | Shared result-placement intent and narrow Classic/Smart compatibility wrapper preserve Legacy execution. Behavioral tests cover frozen completion metadata, retained-error failure metadata, and both page-entry fallbacks. No unified executor runtime exists. |
| U6 | complete | Canvas list exposes one normal creation choice, hides source-kind labels, and opens one normal `canvas.html` entry; a side-effect-free resolver scopes historical Smart handoff to its retained compatibility adapter. |
| U7 | in_progress | SQLite is the default canonical page/route persistence after validated authority activation; retained Classic/Smart adapters now use one neutral CanvasRecord load/save/metadata client, version-poll coordinator, transport-neutral update-message filter, and workflow archive transport client while preserving their polling, merge, selection, insertion, and UI behavior. Shared state, NodeShell base, MediaRenderer, LegacyRenderer, semantic zoom, and Smart screen-space controls are default-on with explicit `unified_canvas=0` / `node_shell=0` / `media_renderer=0` / `legacy_renderer=0` / `semantic_zoom=0` / `screen_space_controls=0` rollback. Canvas list and asset manager use the normal entry; the asset manager presents one neutral `画布` category, while source guards confine Smart URLs and handoff decisions to the compatibility module. Default-path browser reads and the all-zero rollback both passed for Classic and historical Smart, and the Smart handoff preserves the rollback query. Isolated browser creation, restart, stale-conflict, and lossless rollback export are tested. Duplicate runtime/page removal and final flag removal remain pending. |

## Verified authority map

| Domain | Authority and status |
|---|---|
| Project | `data/projects.json` remains page/route runtime authority; R3 SQLite ProjectRecord/ProjectMember records and action authorization are a verified canonical foundation awaiting R4 cutover |
| Canvas | SQLite CanvasRecord is the default page/route persistence when explicit authority state is `sqlite`; it stores lossless payload plus logical revision. `data/canvases/*.json` is retained only as import/rollback compatibility. A live 22-file backfill/compare, isolated Classic/Smart browser reads, browser creation, restart, stale-conflict, and lossless rollback-export acceptance passed; duplicate UI runtime removal is incomplete |
| Node/Edge | Embedded Canvas dictionaries; NodeRecord/EdgeRecord are validated adapter/API views only |
| Asset | Files in configured asset directories plus JSON library/storage/shared-folder metadata; no AssetVersion authority |
| Workflow | `workflows/*.json`/configs and Canvas workflow archives/library items; no formal WorkflowVersion/Run |
| audit | `data/audit/canvas-node-events.jsonl` covers migrated node/graph actions only; append occurs after persistence and is not atomic/comprehensive. The inactive R3 SQLite path has transactional `audit_outbox` entries. |

artifact: not_implemented
entity: not_implemented
knowledge: not_implemented
approval: not_implemented
handoff: not_implemented

## Verified record and service boundaries

- NodeRecord `workbench.node/1` and EdgeRecord `workbench.edge/1` plus JSON schemas
  exist. Legacy payloads/edges round-trip losslessly. ModelBinding pairs
  `provider_id + model_id`; input bindings remain dictionaries and port types remain
  string aliases.
- NodeCreationService validates identity, optional positive revision,
  `can_edit`, temporary Legacy definition resolution, definition state/version, and
  model compatibility. Current Legacy policy rejects supplied models. It supports a
  restricted Legacy definition set (including Classic Output) and durable request
  idempotency. Persistence and JSONL audit are separate.
- NodeMutationService can update exactly `title` and `position`, or delete. Current
  Legacy repository applies this only to Image nodes; delete removes connected
  edges. Positive revision and `can_edit` are required. Persistence/audit are
  separate.
- GraphMutationService supports only atomic create-node-plus-edge. It validates
  revision/Canvas/new-node edge reference/`can_edit`; edge ports are
  `legacy.out -> legacy.in`. The Legacy repository writes node and edge under one
  Canvas lock/revision; audit is a later separate append.
- Python/browser RendererRegistry, NodeShell, NodeCardHost, UnifiedRenderHost,
  MediaRenderer, LegacyRenderer, read-only Node Inspector, and shared Canvas modules
  exist. Smart Group/Image/Legacy adapters submit their NodeShell card batches to
  `UnifiedRenderHost.mountAdapterCards`; they remain opt-in adapters rather than one
  product runtime.

## Feature and compatibility flags

| Flag | Default | Verified behavior |
|---|---|---|
| `WORKBENCH_HOST` | `127.0.0.1` | `0.0.0.0`/`::` explicitly enable unauthenticated LAN compatibility |
| `WORKBENCH_PORT` | `3000` | Must be integer 1-65535 |
| `WORKBENCH_ALLOWED_ORIGINS` | loopback origins on selected port | Explicit comma list allowed; wildcard rejected |
| `WORKBENCH_LAN_ENABLED` | false | Derived from wildcard bind host |
| `WORKBENCH_NODE_API_ENABLED` | true on default loopback | `/api/v1` router registered only for loopback host values |
| `WORKBENCH_CANONICAL_CANVAS_ROUTING_ENABLED` | true | Selects SQLite compatibility persistence when SQLite authority state is `sqlite`; explicit false is the bounded U7 rollback control, and inactive authority does not initialize/switch data |
| `unified_canvas=0` | default-on | Shared state adapter is enabled whenever its module is present; explicit `0` is the bounded U7 rollback control pending complete page/runtime replacement |
| `node_shell=0` | default-on | Enables NodeShell base on loopback; explicit `0` is the bounded U7 rollback control pending complete page/runtime replacement |
| `legacy_renderer=0` | default-on | Uses source-payload rendering inside NodeShell; explicit `0` is the bounded U7 rollback control pending complete page/runtime replacement |
| `media_renderer=0` | default-on | Enables media renderer/NodeShell paths on loopback; explicit `0` is the bounded U7 rollback control pending complete page/runtime replacement |
| `semantic_zoom=0` | default-on | Enables NodeShell semantic presentation on loopback; explicit `0` is the bounded U7 rollback control pending complete page/runtime replacement |
| `screen_space_controls=0` | default-on | Enables Smart NodeShell screen-space controls on loopback; explicit `0` is the bounded U7 rollback control pending complete page/runtime replacement |

## Provider/model/settings and Codex

- Provider metadata/model lists remain provider-shaped fields in `main.py`, frontend
  settings/selectors, built-in/static seeds, and `data/api_providers.json`.
- Credentials remain backend-side in ignored `API/.env`; public endpoints expose
  configuration/masked state. No ProviderConnection, ModelRegistry,
  ModelAvailability, or shared capability/compatibility registry exists.
- Existing Codex integration remains `codex exec` from `main.py`, with repository
  cwd, `workspace-write`, optional model/images/output file, and bounded timeout.
- R1 adds `workbench.codex.CodexBridge` for App Server protocol v2, tested against
  installed `codex-cli 0.153.1`. It is stdio JSONL only, uses an allowlisted child
  environment and workspace-contained cwd, and exposes no Workbench domain tools.
- `HarnessLaunchPolicy` pins thread sandbox to `read-only`; turns are `readOnly`
  with network disabled and `approvalPolicy: never`. Server requests are normalized
  and denied by default. `codex exec` remains compatible and is not rerouted.

## Authorization and security

- There is no global authentication or action/resource authorization. Most Legacy
  routes and WebSocket are reachable to any client able to reach the service.
- `/api/v1` node routes are loopback-only, require caller-supplied `X-User-ID`, and
  check project plus Legacy owner. Local wiring explicitly permits unowned Canvases.
  This is compatibility scoping, not authenticated identity.
- CORS defaults local and rejects wildcard origins; LAN mode remains unauthenticated.
- Current path-containment, media cleanup, redaction, secret-boundary, stale-write,
  and exposure tests pass. No uniform SSRF/tool/subprocess/audit policy exists.

## Automated test baseline

Command:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -q
```

Result: PASS after current R4 work — 221 tests in 1.591 seconds, Python 3.14.7.

R4 canonical-routing local acceptance:

```text
WORKBENCH_HOST=127.0.0.1 WORKBENCH_PORT=3001 WORKBENCH_CANONICAL_CANVAS_ROUTING_ENABLED=true .venv/bin/python main.py
GET /api/canvases
GET /api/canvases/ca914662f0dc4923bd5b60b29eb55b68
GET /api/canvases/ca914662f0dc4923bd5b60b29eb55b68/meta
```

Result: PASS — isolated local server read 16 active Canvas records through SQLite
compatibility routing; the Smart fixture loaded with 3 nodes and unchanged Legacy
`updated_at`. The process was stopped after the read-only check; existing 3000
service was not changed.

R4 browser acceptance (same isolated 3001 process): PASS — Canvas list rendered 16
active records; Classic record `7ed83bf56f234d77a9e67ae1f6496577` rendered its
6-node page; Smart record `ca914662f0dc4923bd5b60b29eb55b68` rendered its 3-node
page. No save/generation/delete action was invoked. The temporary process was
stopped after the browser retained a WebSocket connection; its cancellation log is
shutdown noise, not an application request failure.

R4 default-routing browser write acceptance: PASS — a separate localhost service
used a process-lifetime temporary SQLite database, seeded one Classic and one Smart
record under activated SQLite authority, and had startup hooks disabled. The list
rendered both records; browser creation of `R4 browser write acceptance` increased
the visible count from 2 to 3. The process stopped and its temporary database was
discarded. No user project Canvas was written.

R4 persistence acceptance: PASS — focused tests prove SQL `id + revision` CAS,
409 stale-write semantics through the Legacy compatibility API, restart persistence,
unknown-field retention, and lossless rollback export back to `legacy_json` authority.
Startup no longer rewrites `static/*.html`; runtime cache-version responses remain
dynamic and source files stay unchanged after a server start.

R3 focused command:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_sqlite_project_canvas_repository tests.test_project_canvas_wiring tests.test_project_canvas_migration_tool -v
```

Result: PASS — 10 tests in 0.217 seconds. The migration command imports a
temporary Legacy project/Canvas source, emits a lossless compare report without
switching authority by default, and switches only with explicit `--activate`.

Live R3 report command (no `--activate`):

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python tools/migrate_project_canvas.py --projects data/projects.json --canvases-dir data/canvases --database data/workbench.sqlite3 --report data/r3-project-canvas-migration-report.json
```

Result: PASS — 22 imported, 0 skipped, 0 comparison differences; authority remains
`legacy_json`. Both outputs are ignored under `data/`; no Legacy source file was
rewritten.

Browser acceptance (read-only, local `127.0.0.1:3000`): PASS — from the single
Canvas-list entry, Classic record `7ed83bf56f234d77a9e67ae1f6496577` remained at
`/static/canvas.html`, and historical Smart record
`ca914662f0dc4923bd5b60b29eb55b68` reached its retained
`/static/smart-canvas.html` compatibility page. No Canvas data or execution was
mutated.

Shared-render browser acceptance (read-only, same local server): PASS — the same
Classic and Smart records loaded with `unified_canvas=1`, `node_shell=1`, both
renderer flags, `semantic_zoom=1`, and `screen_space_controls=1`. Both displayed
shared NodeShell ready state, generic ports, and semantic summary controls; no
Canvas data or execution was mutated.

Default-on `unified_canvas` browser recheck (read-only, isolated
`127.0.0.1:3005` server): PASS — Classic record
`7ed83bf56f234d77a9e67ae1f6496577` loaded at its normal `canvas.html` URL with
its nodes and controls visible. Historical Smart record
`ca914662f0dc4923bd5b60b29eb55b68` opened from the same normal URL and reached
its retained `smart-canvas.html` adapter with nodes and controls visible. Neither
Canvas was saved, created, or executed. This does not authorize page deletion.

Default-on `node_shell` browser recheck (read-only, same isolated server): PASS
— the Classic record remained readable at its normal URL, and the retained Smart
adapter displayed its Smart Group through a ready NodeShell with generic Input and
Output ports. Neither Canvas was saved, created, or executed. Explicit
`node_shell=0` remains the bounded U7 rollback control.

Default-on `media_renderer` browser recheck (read-only, same isolated server):
PASS — the Classic media node rendered through a ready unified card with its media
controls and generic Input/Output ports. The retained Smart adapter remained
readable with its ready Smart Group shell and ports. Neither Canvas was saved,
created, or executed; `media_renderer=0` remains the bounded U7 rollback control.

Default-on `legacy_renderer` browser recheck (read-only, same isolated server):
PASS — Classic video, LLM, Comfy, and Output nodes were ready inside NodeShell
while retaining their source-owned controls and generic ports. The retained Smart
Legacy skill node was likewise ready in NodeShell with its original controls.
Neither Canvas was saved, created, or executed; `legacy_renderer=0` remains the
bounded U7 rollback control.

Default-on `semantic_zoom` browser recheck (read-only, same isolated server):
PASS — Classic displayed the semantic indicator at `100% · 完整 · 6 节点`, while
the retained Smart adapter displayed `65% · 摘要 · 2 节点` and its corresponding
summary node presentation. Neither Canvas was saved, created, or executed;
`semantic_zoom=0` remains the bounded U7 rollback control.

Default-on `screen_space_controls` browser recheck (read-only, same isolated
server): PASS — the retained Smart adapter remained readable in semantic summary
mode with generic Input/Output ports visible for both ready NodeShell nodes.
Neither Canvas was saved, created, or executed; `screen_space_controls=0` remains
the bounded U7 rollback control.

All-zero UI-flag rollback browser recheck (read-only, same isolated server): PASS
— Classic restored its retained non-NodeShell presentation. Historical Smart was
opened through the normal `canvas.html` URL with all six explicit zero flags; the
handoff retained every flag in its `smart-canvas.html` URL and restored the
retained non-NodeShell presentation. Neither Canvas was saved, created, or
executed.

R1 focused command:

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_codex_bridge -v
```

Result: PASS — 3 tests in 0.074 seconds. Covers initialize, Thread create, simple
Turn, normalized events, default approval denial, model/config discovery,
interruption, shutdown/recovery, workspace containment, and secret filtering.

The pre-R1 baseline coverage includes Legacy fixtures/round-trip, Canvas cleanup and stale writes,
versioned node APIs/runtime, shared Canvas runtime/modules, events/exposure,
NodeRecord/renderer/services/repositories, Inspector, security boundaries, semantic
zoom, screen-space controls, and workflow archive round-trip.

## Syntax/static checks

Commands and results:

```text
.venv/bin/python -c "import ast, pathlib; paths=[pathlib.Path('main.py'), *pathlib.Path('workbench').rglob('*.py'), pathlib.Path('tools/migrate_project_canvas.py'), pathlib.Path('tools/backup_canvas_sources.py')]; [ast.parse(p.read_text(encoding='utf-8'), filename=str(p)) for p in paths]; print(f'Python AST OK: {len(paths)} files')"
PASS — 33 Python files parsed in the latest R4 verification.

NODE_BIN=/Users/lo/.local/node-v24.20.0/bin/node
"$NODE_BIN" --check static/js/canvas.js
"$NODE_BIN" --check static/js/smart-canvas.js
"$NODE_BIN" --check static/js/canvas-list.js
rg --files static/js/workbench/canvas static/js | rg '\\.js$' | sort -u | xargs -n 1 "$NODE_BIN" --check
PASS — 42 JavaScript files, including Classic, Smart, Canvas-list, and shared Canvas modules; Node v24.20.0.

git diff --check
PASS
```

No repository-supported Ruff, mypy, ESLint, or bundled frontend build configuration
was found; none is claimed as run.

Additional R1 checks:

```text
git diff --check
PASS

PYTHONDONTWRITEBYTECODE=1 .venv/bin/python - <<'PY' ... CodexBridge.start(); list_models(); read_config(); shutdown() ... PY
PASS — live, non-mutating `initialize`, `model/list`, and `config/read` through
installed `codex app-server` (`codex-cli 0.153.1`).
```

## Performance baseline

Command:

```text
node tools/benchmark-canvas-payload.mjs
```

Result: PASS/reproduced for R4 — 100 nodes = 9,622 bytes (0.102 ms serialization);
300 nodes = 29,132 bytes (0.088 ms serialization). This is deterministic payload
construction, not a browser interaction budget.

Latest available browser record:
`docs/benchmarks/canvas-node-shell-baseline-2026-09-04.md`. Visible 300-node Safari
NodeShell sample: load 152 ms, render ready 362 ms, zoom 38 ms, pan 104 ms, minimap
15 ms. Earlier offscreen minimap was 149 ms (141 ms recheck) and remains a P2
follow-up. All are single local samples, not percentile/release commitments.

## Verified known issues

1. RESOLVED IN R2 — connected graph creation now requires a positive revision at
   `CreateNodeAndEdgePayload`; the service also rejects a missing, zero, or negative
   revision before persistence/node preparation. It no longer normalizes absence to
   `0`; focused and full tests verify the behavior.
2. PARTIALLY RESOLVED IN R3 — canonical SQLite mutation plus audit/outbox insertion
   is one tested transaction and audit insertion failure rolls the Canvas change
   back. Legacy JSON routes still persist before JSONL audit until switch completion.
3. PARTIALLY RESOLVED IN R3 — SQLite CanvasRecord has tested independent logical
   revisions. Legacy runtime routes still use `updated_at` until controlled switch.
4. VERIFIED — visible 300-node browser sample is healthy against the provisional
   interaction alert, but earlier offscreen minimap timing exceeded it; retain the
   documented P2 follow-up and repeat after material Canvas changes.
5. VERIFIED LIMIT — R1's Codex bridge has no Workbench project/Canvas/node/graph
   mutation tools and intentionally has no interactive approval UI. Requests are
   denied by default; future authority must be proposed and gated.

## Legacy monolith responsibility baseline

### `main.py`

- Size/profile: 19,466 lines; 868 top-level functions; 77 classes; 165 route
  decorators. It still owns most backend provider/model/secret/subprocess,
  generation/chat, project/Canvas, asset/workflow/update/media/queue/event, and
  Legacy API behavior.
- Already delegated: record/adapter/repository contracts, RendererRegistry,
  NodeCreation/Mutation/GraphMutation, JSONL audit sink, and `/api/v1` node router
  live under `workbench/`; `main.py` wires them.
- R4 added Workbench business responsibility: no.
- R4 responsibilities removed/delegated: Canvas metadata writes, listing, expired
  trash cleanup, project-delete reassignment, and media-reference diagnostics now
  delegate through the CanvasRepository contract; canonical SQLite compatibility
  persistence remains under `workbench/`, while `main.py` only composes it.

### `static/js/canvas.js`

- Size/profile: 16,705 lines. It still owns Classic construction/render/connect/
  execution, provider controls, graph/save/conflict, workflow/assets/logs, minimap,
  selection, drag, resize, and page adaptation.
- Already delegated: opt-in runtime, geometry, graph/group intents, creation
  catalog/client, records, entry compatibility resolver, NodeShell, renderer registry/host/renderers, Inspector,
  semantic zoom, and screen controls live in `static/js/workbench/canvas/`.
- R4 added Workbench business responsibility: no.
- R2 responsibilities removed/delegated: Classic blank Output creation now delegates
  to the restricted NodeCreationService route when the explicitly enabled loopback
  compatibility path is active; Classic port-drop acceptance delegates to
  shared `WorkbenchCanvasPortCompatibility`; its generic generation entry delegates
  through `WorkbenchCanvasExecutionCompatibility`; historical Smart-entry detection
  and URL construction delegate to `WorkbenchCanvasEntryCompatibility`.

### `static/js/smart-canvas.js`

- Size/profile: 20,082 lines. It still owns Smart composer, construction/render/
  connect/execution, provider/media/MiniMax, graph/save/conflict, groups, minimap,
  selection, drag, resize, and page adaptation.
- Already delegated: consumes the same opt-in shared Canvas modules as Classic.
- R4 added Workbench business responsibility: no.
- R2 responsibilities removed/delegated: Smart blank MiniMax creation delegates to
  the restricted NodeCreationService route when the explicitly enabled loopback
  compatibility path is active; Smart port-drop hover and acceptance
  delegate to shared `WorkbenchCanvasPortCompatibility`; its primary generation
  entry delegates through `WorkbenchCanvasExecutionCompatibility`; Smart Group/Image/Legacy
  NodeShell card batches delegate to `UnifiedRenderHost.mountAdapterCards`.

## Blockers

No external blocker. Source backup/validation, SQLite authority activation, default
canonical routing, isolated Classic/Smart browser reads and browser creation,
restart/stale-conflict/rollback verification, workflow archive round-trip, and the
deterministic benchmark are complete. R4 remains incomplete only at U7: duplicate
Classic/Smart runtime and page removal, followed by UI migration-flag retirement.

## Exactly one next authorized Round

No next Round is authorized while R4 is active.

## Forbidden next actions

Until R4 passes, do not execute R5-R17, make NodeRecord incompatible changes, implement SkillRegistry,
ProviderConnection/ModelRegistry/
ModelAvailability, ExecutorRegistry/ExecutionRuntime, Asset/Artifact/Entity/
Knowledge/Workflow/Approval/Handoff runtimes, PackageRuntime, Common/WholeHouse
packages, Agent graph mutation, interactive Codex approval, or unverified Legacy
Canvas adapter/page removal. U7 may remove a duplicate only after its replacement
has focused interaction, browser, rollback, and source-reference acceptance. Do not
add new Workbench business responsibility to `main.py`,
`static/js/canvas.js`, or `static/js/smart-canvas.js`.
