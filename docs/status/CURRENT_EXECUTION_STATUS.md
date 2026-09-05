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
The retained Classic/Smart adapters also delegate Canvas-list project memory and
encoded list-URL construction to that same entry boundary; this changes no Canvas
record and leaves their page-specific navigation UI intact.
Their text-copy fallback and optional secure-context clipboard verification are
also delegated to a DOM-neutral shared helper; error/modal and page-specific UI
decisions remain adapter-owned.
The API image-size calculation now likewise shares only its pure, injected
algorithm; each adapter retains its own ratio parser, size map, model choice, and
provider/execution behavior.
Editable-target detection for keyboard/drag guards now shares its base DOM
semantics; Smart supplies its retained prompt-control selector while Classic keeps
its existing narrower selector behavior.
The asset manager now presents a single business-neutral `画布` category and no
longer exposes Classic/Smart source labels or filters; retained `kind` is
compatibility metadata only.
Classic and Smart workflow import/export now share one archive transport, JSON
export and import-normalization client for the existing backend contract, plus one
side-effect-free shared Canvas Graph Fragment for selected-subgraph (including
clipboard copy), import-graph-materialization (including center-anchored clipboard
paste), and graph-record removal. Each retained adapter still owns its archive format, node
serializer/order, page-specific import normalization and selection UI, save
scheduling, file naming and UI feedback;
shared download keeps each adapter's fallback filename and revoke timing, while
shared failure formatting retains the Legacy string, validation-array, and
nested-detail behavior.
Classic and Smart also delegate their generic HTTP error parsing to one shared
Canvas module; provider, execution, and error-presentation decisions remain in the
retained adapters.

Classic and Smart now also delegate pure media original-URL normalization and
local `/output`/`/assets` preview routing. Classic retains its remote-media proxy
and FLV compatibility while Smart retains its display-URL fallback; media HTML,
interaction, and provider behavior remain adapter-owned.

Their native-video overlay synchronization and event-propagation isolation also
delegate to one shared helper. The adapters retain their existing overlay selectors,
binding markers, player activation, and Smart playback-end behavior.

The same helper now binds preview-image load failures: each adapter supplies its
existing original-URL and video-fallback rules, while shared code performs one-time
event binding, replacement, and inline-player binding. No media format, player, or
adapter-specific fallback policy was changed.

Single-image asynchronous load/decode now also has one shared promise helper. Each
adapter retains its own cache, in-flight de-duplication, viewport gating, selected
node scope, and high-resolution source policy.

High-resolution candidate scanning and preview/original source switching are now
shared callback-driven logic. Classic and Smart still provide their own roots,
viewport test, URL display/proxy policy, caches, and delayed application lifecycle.

Pure media-kind classification now resolves MIME, extensions, and explicit media
kinds in one shared module. Classic explicitly retains FLV support; Smart retains
text/workflow classification. Provider, asset-library, and execution behavior remain
adapter-owned.

The shared MediaRenderer now consumes that same classification boundary for its
video element choice and Inspector media summary; it no longer keeps a separate
video/audio regular-expression branch.

Classic and Smart execution-result media extraction now delegates traversal and
URL de-duplication to one shared pure normalizer. Classic retains its historical
root-key/string-output contract; Smart retains root-object traversal and positive
dimension metadata. Execution/provider behavior remains adapter-owned.

Image-dimension load/error handling and positive dimension-field copying now share
one helper. Smart retains all media layout, grid, and group sizing decisions; Classic
retains its own display URL choice.

The Smart adapter now delegates its pure square media-grid fitting and deterministic
candidate scoring to one shared Canvas module. It retains all Smart-specific media
group membership, grid placement, scroll/overflow treatment, and layout policy; the
module has no DOM, network, persistence, or execution responsibility.

Intrinsic media-size field selection, aspect-ratio contain fitting, and thumbnail
minimum-size fallback now share one pure Canvas module. Smart retains the decisions
to invoke it, audio/default-card exceptions, group policy, and all DOM application.

Native media playback-state capture and restoration now share one Canvas module.
The adapters retain their own render lifecycle and node/stage transplantation rules;
the shared contract only preserves time, paused state, rate, mute, and volume across
their existing re-renders.

Image/video/audio reference filtering and remote video-reference detection now share
one callback-driven Canvas module. Classic retains FLV-aware classification and its
image limit; Smart retains its image-disguised-as-video exclusion rule.

Media-reference browser smoke (read-only, isolated `127.0.0.1:3010`): PASS —
Classic record `bf43426d46e648e2b069f4a2313f4aab` retained its video/image cards
and ports; the normal Smart URL for `ca914662f0dc4923bd5b60b29eb55b68` handed off
and retained Composer, Smart group, upload, and video-workflow controls. No
user-initiated save, create, execution, or deletion occurred; the isolated service
was stopped after the check.

Playback-state browser smoke (read-only, isolated `127.0.0.1:3010`): PASS — the
Classic local-video card remained readable with native media controls and NodeShell
ports; the normal Smart URL for `ca914662f0dc4923bd5b60b29eb55b68` handed off and
retained Composer, Smart group, upload, and video-workflow controls. No
user-initiated save, create, execution, or deletion occurred; the isolated service
was stopped after the check.

Intrinsic-media layout browser smoke (read-only, isolated `127.0.0.1:3010`): PASS
— Classic record `bf43426d46e648e2b069f4a2313f4aab` retained its local video/image
cards and NodeShell ports; the normal Smart URL for
`ca914662f0dc4923bd5b60b29eb55b68` handed off and retained Composer, Smart group,
upload, and video-workflow controls. No user-initiated save, create, execution, or
deletion occurred; the isolated service was stopped after the check.

Media-grid browser smoke (read-only, isolated `127.0.0.1:3010`): PASS — Classic
record `bf43426d46e648e2b069f4a2313f4aab` rendered the existing local video/image
cards and NodeShell ports; the normal Smart URL for
`ca914662f0dc4923bd5b60b29eb55b68` handed off and retained Composer, Smart group,
upload, and video-workflow controls. No user-initiated save, create, execution, or
deletion occurred; the isolated service was stopped after the check.

Dimension-helper browser smoke (read-only, isolated `127.0.0.1:3010`): PASS —
Classic record `bf43426d46e648e2b069f4a2313f4aab` rendered its existing local
image/video cards and NodeShell ports; the normal Smart URL for
`ca914662f0dc4923bd5b60b29eb55b68` handed off and retained Composer, Smart group,
upload, and video-workflow controls. No save, create, execution, deletion, or other
Canvas mutation was invoked; the isolated service was stopped after the check.

Execution-result media-normalizer browser smoke (read-only, isolated
`127.0.0.1:3010`): PASS — Classic record
`bf43426d46e648e2b069f4a2313f4aab` loaded its NodeShell-ready local video/image
cards; the normal Smart URL for `ca914662f0dc4923bd5b60b29eb55b68` handed off and
retained Composer, Smart group, upload, and video-workflow controls. No save,
create, execution, deletion, or other Canvas mutation was invoked; the isolated
service was stopped after the check.
Legacy source-repository self-update responsibility has been removed from both
`main.py` and the home shell; the runtime no longer exposes update routes, source
repository URLs, update download/staging, self-restart, or update rollback logic.
The only remaining runtime GitHub-hosted fallback, a RunningHub model-registry raw
URL, has also been removed. RunningHub model discovery now uses its official OpenAPI,
an optional installed local snapshot, then the existing built-in fallback; Workbench
runtime source guards prohibit GitHub hosting URLs in `main.py`, the home shell,
Canvas-list, both Canvas entries/adapters, and shared Canvas modules. A retained
third-party LTX extension link is outside this Workbench runtime guard and remains
unchanged in R4.
An isolated restart/read check on `127.0.0.1:3006` returned local-only `/api/app-info`
and served an index shell with none of the removed self-update endpoints or source
repository URL tokens.
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
| U7 | in_progress | SQLite is the default canonical page/route persistence after validated authority activation; retained Classic/Smart adapters now use one neutral CanvasRecord load/save/metadata client, version-poll coordinator, transport-neutral update-message filter, workflow archive transport/JSON-export/import-normalization client, side-effect-free Canvas Graph Fragment for selected-subgraph (including clipboard copy)/import-graph-materialization (including center-anchored clipboard paste)/graph-record removal, generic HTTP error parser, shared text-copy fallback/clipboard verification, and media original-URL/preview routing, callback-driven media-reference filtering, MIME/extension media-kind classification (also used by MediaRenderer), native-video event isolation, preview-failure fallback binding, native-media playback-state preservation, high-resolution candidate collection, single-image async decode preloading, pure intrinsic-media/thumbnail sizing, and pure media-grid fitting while preserving their polling, merge, archive format, node serialization/order, page-specific import normalization/selection UI, media display/proxy rules, Classic FLV classification/image limits, Smart image-disguised-as-video exclusion, player activation, render lifecycle and node/stage transplantation policy, cache/scope/delayed application policy, Smart default/audio card treatment and group/grid placement and overflow policy, download, provider, execution, and UI behavior. Canvas-list project memory and encoded list-URL construction also use the same side-effect-free entry boundary. Shared state, NodeShell base, MediaRenderer, LegacyRenderer, semantic zoom, and Smart screen-space controls are default-on with explicit `unified_canvas=0` / `node_shell=0` / `legacy_renderer=0` / `media_renderer=0` / `semantic_zoom=0` / `screen_space_controls=0` rollback. Canvas list and asset manager use the normal entry; the asset manager presents one neutral `画布` category, while source guards confine Smart URLs and handoff decisions to the compatibility module. Default-path browser reads and the all-zero rollback both passed for Classic and historical Smart, and the Smart handoff preserves the rollback query. Isolated browser creation, restart, stale-conflict, and lossless rollback export are tested. Duplicate runtime/page removal and final flag removal remain pending. |

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

Result: PASS after current R4 work — 240 tests in 2.409 seconds, Python 3.14.7.

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

Shared-entry browser recheck (read-only, isolated `127.0.0.1:3010` server): PASS
— the normal `canvas.html` URL for historical Smart record
`ca914662f0dc4923bd5b60b29eb55b68` handed off to its retained Smart adapter with
the existing two nodes and workflow controls visible. This verifies the shared
Canvas-list project-memory/URL module after its cache-version update; no Canvas
data or execution was mutated.

Shared-render browser acceptance (read-only, same local server): PASS — the same
Classic and Smart records loaded with `unified_canvas=1`, `node_shell=1`, both
renderer flags, `semantic_zoom=1`, and `screen_space_controls=1`. Both displayed
shared NodeShell ready state, generic ports, and semantic summary controls; no
Canvas data or execution was mutated.

Current-worktree browser recheck (read-only, isolated `127.0.0.1:3011` server):
PASS — Classic record `bf43426d46e648e2b069f4a2313f4aab` remained on the normal
entry with four ready NodeShell cards, media controls, and generic ports. Historical
Smart record `ca914662f0dc4923bd5b60b29eb55b68` entered via that same URL, handed
off to its retained adapter, and displayed its Smart composer, template entry,
workflow controls, and two nodes. No Canvas data or execution was mutated; the
temporary server was stopped.

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

Current-worktree all-zero rollback recheck (read-only, isolated
`127.0.0.1:3010`): PASS — Classic record
`bf43426d46e648e2b069f4a2313f4aab` rendered its retained non-NodeShell cards;
its existing video preview fallback received a `415` preview response and retained
native video controls. Historical Smart record `ca914662f0dc4923bd5b60b29eb55b68`
opened through the same normal URL, preserved all six zero flags during handoff,
and rendered its retained group, upload, and Skill controls. No user-initiated
save, create, execution, or deletion occurred; the isolated service was stopped.

Current-worktree browser recheck (read-only, isolated `127.0.0.1:3008`): PASS —
the normal Classic URL for `7ed83bf56f234d77a9e67ae1f6496577` rendered its title,
six nodes, NodeShell-ready cards, and generic ports. The normal Smart URL for
`ca914662f0dc4923bd5b60b29eb55b68` handed off to the retained adapter and rendered
the Smart composer, Smart group, upload node, and Skill node. Reopening the same
Smart record with all six explicit zero flags preserved every rollback parameter
through the handoff and rendered the retained legacy controls. No create, save,
generation, delete, or other Canvas mutation was invoked; the isolated service was
stopped after verification.

Workflow-dialog browser follow-up on the same local fixture is intentionally not
accepted as read-only evidence: selecting one Classic node showed a newer
`updated_at`, even though the direct Classic/Smart selection handlers have a focused
contract prohibiting `scheduleSave()`. The source of that metadata update was not
attributed during the attempt, so no export was triggered and the service was
stopped. Repeat workflow UI export only against a process-lifetime temporary SQLite
fixture before using it as R4 acceptance evidence.

Workflow UI export browser acceptance (isolated `127.0.0.1:3009` temporary
SQLite authority): PASS — one seeded Classic and one seeded Smart Canvas each
selected one node and opened the workflow dialog from the normal Canvas entry.
Both exposed `已选择 1 个节点，0 条连线`; Classic JSON export completed, and Smart
explicitly reported `已导出智能画布工作流 JSON`. No import, execution, or user Canvas
was used. The fixture service was stopped; after environment deletion protection
initially rejected a force-delete, its isolated temporary directory was moved to the
local Trash and is recoverable.

Media URL shared-boundary browser smoke (read-only, isolated `127.0.0.1:3010`):
PASS — Classic record `bf43426d46e648e2b069f4a2313f4aab` rendered its existing
local video and image through the shared `media-url.js` module, with NodeShell-ready
cards and generic ports. Opening historical Smart record
`ca914662f0dc4923bd5b60b29eb55b68` through the normal Canvas URL handed off to its
retained adapter and preserved the Composer, Smart group, upload node, and video
workflow node. No save, create, execution, deletion, or other Canvas mutation was
invoked; the isolated service was stopped after the smoke check.

Native-video shared-control browser smoke (read-only, isolated `127.0.0.1:3010`):
PASS — Classic record `bf43426d46e648e2b069f4a2313f4aab` loaded its local video
controls and media/image cards after `media-preview-controls.js` loaded. Historical
Smart record `ca914662f0dc4923bd5b60b29eb55b68` again handed off from the normal URL
and retained its Composer, Smart group, upload, and video workflow controls. No
save, create, execution, deletion, or other Canvas mutation was invoked; the
isolated service was stopped after verification.

Preview-fallback shared-control browser smoke (read-only, isolated
`127.0.0.1:3010`): PASS — Classic record
`bf43426d46e648e2b069f4a2313f4aab` retained its existing local video and image
cards; the normal URL for historical Smart record
`ca914662f0dc4923bd5b60b29eb55b68` again handed off and retained Composer, Smart
group, upload, and video-workflow controls. No save, create, execution, deletion,
or other Canvas mutation was invoked; the isolated service was stopped after the
check.

High-resolution candidate shared-helper browser smoke (read-only, isolated
`127.0.0.1:3010`): PASS — Classic record
`bf43426d46e648e2b069f4a2313f4aab` retained its local video/image cards and
NodeShell ports; the normal Smart URL for `ca914662f0dc4923bd5b60b29eb55b68`
handed off and retained Composer, Smart group, upload, and video-workflow controls.
No save, create, execution, deletion, or other Canvas mutation was invoked; the
isolated service was stopped after the check.

MediaRenderer classification browser smoke (read-only, isolated
`127.0.0.1:3010`): PASS — Classic record
`bf43426d46e648e2b069f4a2313f4aab` rendered its NodeShell-ready local video/image
cards; historical Smart record `ca914662f0dc4923bd5b60b29eb55b68` handed off from
the normal URL and retained Composer, Smart group, upload, and video-workflow
controls. No save, create, execution, deletion, or other Canvas mutation was
invoked; the isolated service was stopped after the check.

Media-kind shared-module browser smoke (read-only, isolated `127.0.0.1:3010`):
PASS — Classic record `bf43426d46e648e2b069f4a2313f4aab` retained its video and
image cards; the normal URL for Smart record `ca914662f0dc4923bd5b60b29eb55b68`
handed off and retained Composer, Smart group, upload, and video-workflow controls.
No save, create, execution, deletion, or other Canvas mutation was invoked; the
isolated service was stopped after the check.

Async-decode shared-helper browser smoke (read-only, isolated `127.0.0.1:3010`):
PASS — Classic record `bf43426d46e648e2b069f4a2313f4aab` completed media-card
rendering with its existing local image/video; the normal Smart URL for historical
record `ca914662f0dc4923bd5b60b29eb55b68` handed off and preserved Composer, Smart
group, upload, and video-workflow controls. No save, create, execution, deletion,
or other Canvas mutation was invoked; the isolated service was stopped after the
check.

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

Result: PASS/reproduced for current R4 worktree — 100 nodes = 9,622 bytes (0.108 ms serialization);
300 nodes = 29,132 bytes (0.096 ms serialization). This is deterministic payload
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

- Size/profile: 18,397 lines; 828 top-level functions; 75 classes; 162 route
  decorators. It still owns most backend provider/model/secret/subprocess,
  generation/chat, project/Canvas, asset/workflow/media/queue/event, and
  Legacy API behavior.
- Already delegated: record/adapter/repository contracts, RendererRegistry,
  NodeCreation/Mutation/GraphMutation, JSONL audit sink, and `/api/v1` node router
  live under `workbench/`; `main.py` wires them.
- R4 added Workbench business responsibility: no.
- R4 responsibilities removed/delegated: Canvas metadata writes, listing, expired
  trash cleanup, project-delete reassignment, and media-reference diagnostics now
  delegate through the CanvasRepository contract; canonical SQLite compatibility
  persistence remains under `workbench/`, while `main.py` only composes it. The
  Legacy repository self-update, staging, self-restart, rollback, source URL, and
  GitHub-hosted model-registry fallback responsibility have been removed.

### `static/js/canvas.js`

- Size/profile: 16,686 lines. It still owns Classic construction/render/connect/
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

- Size/profile: 20,085 lines. It still owns Smart composer, construction/render/
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

### U7 duplicate-runtime exit inventory

- Shared now: canonical Canvas persistence/CAS, remote-update filtering and polling,
  archive transport, HTTP error formatting, pure media URL normalization/preview
  routing, native-video event isolation, preview-failure fallback binding, and
  MIME/extension media-kind classification, high-resolution candidate collection,
  and async decode preloading, pure graph fragment operations, common
  NodeShell/render host, generic ports, semantic presentation, and screen controls.
- Smart-only still product-relevant: composer and dynamic provider/media controls,
  prompt preset/template and asset-library UX, image edit/crop/draw/grid/panorama
  tools, Smart group media actions, and Smart-specific cascade/execution UI.
- Classic-only still product-relevant: provider-shaped generator/LLM/Comfy/Video/
  MiniMax/LTX/RunningHub cards, Classic output/log/asset management, and Classic
  cascade/execution UI.

Consequently, U7 cannot delete either Runtime/page or retire UI flags until each
listed product-relevant responsibility has an accepted shared replacement or an
explicit bounded compatibility adapter with focused interaction, browser, rollback,
and source-reference evidence.

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
