# Implementation Plan and Execution Checklist

## How to use this file

This is the execution ledger for the migration. Complete tasks in dependency order. A checked documentation item means the artifact exists; it does not mean the corresponding product code is implemented.

Status vocabulary:

- `complete`: implemented and verified against its acceptance criteria;
- `in progress`: active implementation with an owner;
- `blocked`: cannot proceed without a named decision or external condition;
- `not started`: no implementation claim.

## Round 1 baseline status

- [x] Audit repository structure, startup, dependencies, frontend, backend, Canvas, nodes, Agent, providers, ComfyUI, events, persistence, authentication, permissions, security, and tests.
- [x] Create `AGENTS.md` with repository-specific hard constraints.
- [x] Create `CURRENT_ARCHITECTURE.md` with reuse/refactor/Legacy/security classifications and Gap Analysis.
- [x] Create `TARGET_ARCHITECTURE.md` with NodeRecord, NodeShell, registries, Canvas API, CodexBridge, services, workflows, versions, and pack boundaries.
- [x] Create `MIGRATION_PLAN.md` with incremental phases, exact Phase 0/1 file lists, risks, rollback, and gates.
- [x] Create this implementation ledger.
- [x] Implement Phase 0 code changes. Status: complete; environment, fixtures, secret boundary, exposure policy, package seams, performance baseline, and Canvas smoke checks meet the Phase 0 scope.
- [ ] Implement Phase 1 code changes. Status: not started by design.

## Current verification baseline

| Check | Result | Interpretation |
|---|---|---|
| Python AST parse of `main.py` | Passed | Current Python syntax parsed |
| `node --check static/js/canvas.js` | Passed | Current Classic Canvas JavaScript syntax passed |
| `node --check static/js/smart-canvas.js` | Passed | Current Smart Canvas JavaScript syntax passed |
| Python unit discovery | Passed: 37 tests | `.venv` dependencies installed successfully with `uv --system-certs` and the documented mirror fallback; all discovered tests passed |
| Existing test count | 37 methods | Legacy fixtures, Canvas log/media, exposure, repository baseline, event-contract, and secret-boundary tests passed |
| Worktree cleanliness | Dirty before this round | User changes exist in three high-risk source files |

## Phase 0: Repository Baseline

### P0.1 Reproducible development environment

| Field | Value |
|---|---|
| Status | complete |
| Task | Add a documented isolated Python environment and `requirements-dev.txt`; constrain test tooling and make one command run unit discovery. |
| Dependency | None |
| Files | `requirements-dev.txt`, `README.md` or developer setup document; `requirements.txt` only if runtime constraints are required |
| Risk | Python 3.10/3.14 and Pydantic/FastAPI version drift may reveal latent incompatibility. |
| Acceptance criteria | Fresh virtual environment installs successfully; unit discovery imports `main.py`; no global Python modification is required. |

Checklist:

- [x] Record supported Python range.
- [x] Add runtime dependency constraints and a development requirements file.
- [x] Verify macOS arm64 install in `.venv` without changing global Python.
- [x] Verify the exact baseline test command: 30 tests passed.
- [x] Record external binaries used by optional flows: ffmpeg, Codex CLI, Gemini CLI, Jimeng CLI.

### P0.2 Runtime/source separation and ignore policy

| Field | Value |
|---|---|
| Status | complete |
| Task | Prevent runtime data, secrets, previews, generated media, local databases, caches, and test artifacts from dirtying source control while retaining deliberate seed files. |
| Dependency | P0.1 for test cache observation |
| Files | `.gitignore`, runtime-data documentation |
| Risk | An overbroad ignore rule could hide a source template or fixture. |
| Acceptance criteria | Normal smoke use creates no unexpected tracked/untracked source artifacts; every retained seed/template path is documented. |

Checklist:

- [x] Ignore `API/.env` and all alternate local secret files.
- [x] Ignore generated `global_config.json` and local databases.
- [x] Ignore project/Canvas/conversation runtime JSON except explicit fixtures/seeds.
- [x] Ignore generated `assets/input`, `assets/output`, `assets/uploads`, previews, and `output` content.
- [x] Keep `data/asset_library.json` as the current deliberate seed/template data file.
- [x] Ignore Python/Node/test caches.

### P0.3 Golden Legacy fixtures

| Field | Value |
|---|---|
| Status | complete |
| Task | Capture representative Classic, Smart, unknown-field, group/connection, provider-specific, and historical workflow records. |
| Dependency | P0.1 |
| Files | `tests/fixtures/canvas/*.json`, `tests/test_canvas_legacy_fixtures.py` |
| Risk | Repository fixtures may not represent private user records. |
| Acceptance criteria | All known node families occur in at least one fixture; load/save preserves every field; fixture inventory is machine-checked. |

Checklist:

- [x] Classic node families represented.
- [x] Smart node families represented.
- [x] Unknown top-level and nested fields represented.
- [x] Connections, groups, logs, settings, viewport, and project metadata represented and machine-checked.
- [x] Historical/imported type labels represented.
- [x] Sensitive values replaced with inert fixture data.

### P0.4 Characterization tests

| Field | Value |
|---|---|
| Status | complete |
| Task | Lock current load/save, conflict, delete/restore, workflow package, asset containment, and event behaviors. |
| Dependency | P0.1, P0.3 |
| Files | `tests/test_repository_baseline.py`, `tests/test_canvas_legacy_fixtures.py`, current tests |
| Risk | Tests can accidentally encode an unsafe behavior as desirable. |
| Acceptance criteria | Compatibility behaviors are explicit; unsafe behaviors are marked for security replacement rather than asserted as permanent contracts. |

Checklist:

- [x] Canvas monotonic revision behavior.
- [x] Stale save rejection.
- [x] Soft delete/restore/purge.
- [x] Workflow export/import archive round trip preserves Legacy graph fields.
- [x] Asset path containment and media ownership, including traversal and symlink escape rejection.
- [x] Unknown-field preservation.
- [x] WebSocket invalidation payload contract.
- [x] SSE chat event contract.

### P0.5 Secret boundary containment

| Field | Value |
|---|---|
| Status | complete |
| Task | Remove raw ModelScope/provider token responses and browser storage fallbacks; ensure provider calls remain backend-mediated. |
| Dependency | P0.1, focused Legacy page flow inventory |
| Files | `main.py`, `static/angle.html`, `static/zimage.html`, `tests/test_secret_boundary.py` |
| Risk | Angle/Z-Image Legacy flows currently depend on the raw token and could stop working. |
| Acceptance criteria | No browser endpoint returns a raw provider secret; no provider secret is stored in local/session storage; equivalent backend flows work. |

Checklist:

- [x] Replace `/api/config/token` response with non-secret configuration metadata.
- [x] Remove `modelscope_api_token` browser fallback.
- [x] Remove request payload `api_key` from browser pages.
- [x] Scan ModelScope compatibility response and Legacy pages for raw secret paths.
- [x] Test server logs and exceptions for redaction, including Bearer tokens, query values, proxy userinfo, and nested upstream payloads.
- [x] Keep `API/.env` server-only.

### P0.6 Exposure configuration

| Field | Value |
|---|---|
| Status | complete |
| Task | Make localhost/LAN binding and allowed origins explicit; stop presenting unauthenticated LAN mode as safe collaboration. |
| Dependency | Resolved: default local bind with explicit LAN opt-in |
| Files | `main.py`, macOS/Windows launchers, usage documentation, security tests |
| Risk | Changing the default bind can affect existing studio users. |
| Acceptance criteria | Default and LAN modes are explicit; CORS is configured; the UI reports the active exposure mode; documentation matches behavior. |

Checklist:

- [x] Add bind host and allowed-origin configuration.
- [x] Default to local-only binding; require `WORKBENCH_HOST=0.0.0.0` for LAN.
- [x] Add startup warning for unauthenticated LAN compatibility mode.
- [x] Cover origin parsing and runtime metadata with tests.

### P0.7 Security inventory and route classes

| Field | Value |
|---|---|
| Status | complete |
| Task | Classify public, project, provider-admin, storage-admin, update-admin, and tool-execution routes. |
| Dependency | P0.4 |
| Files | security policy document/test matrix; route metadata seam in `workbench/api/` |
| Risk | Ad hoc checks in route functions can diverge. |
| Acceptance criteria | Every route has an intended permission class and project scope; critical unauthenticated admin routes are scheduled before studio deployment. |

Checklist:

- [x] Update/rollback routes classified.
- [x] Provider secret/settings routes classified.
- [x] Shared folders/storage paths classified.
- [x] Project/Canvas/asset/workflow routes classified.
- [x] Subprocess/tool routes classified.
- [x] Media delivery policy recorded as requiring authorized delivery before studio mode.

### P0.8 Minimal backend package seam

| Field | Value |
|---|---|
| Status | complete |
| Task | Add empty/low-behavior `workbench` package boundaries without relocating working code. |
| Dependency | P0.1 |
| Files | `workbench/__init__.py`, `workbench/api/__init__.py`, `workbench/domain/__init__.py`, `workbench/application/__init__.py` |
| Risk | Premature directory growth without behavior. |
| Acceptance criteria | Each package has a documented next responsibility; no duplicated implementation; `main.py` remains entry point. |

### P0.9 Performance baseline

| Field | Value |
|---|---|
| Status | complete — payload, save, iframe render-ready, zoom, pan, and minimap baselines are recorded for 100/300 lightweight nodes. An initially observed Tailwind CDN runtime exception did not reproduce in clean direct or iframe Canvas checks; its production-use warning remains documented. |
| Task | Measure initial render, pan/zoom responsiveness, minimap refresh, and save payload for 100/300 lightweight nodes. |
| Dependency | P0.3 |
| Files | benchmark fixture/scripts and recorded baseline |
| Risk | Browser/hardware variance can make absolute thresholds misleading. |
| Acceptance criteria | Reproducible hardware/browser profile and relative regression budget are recorded. |

### Phase 0 exit checklist

- [x] Fresh isolated environment works.
- [x] Existing tests run and pass.
- [x] Golden fixtures cover known Legacy types.
- [x] Raw browser-secret path is closed.
- [x] Runtime/source separation is established.
- [x] Exposure and CORS policy are explicit.
- [x] Route permission inventory exists.
- [x] Performance baseline is recorded.
- [x] Current Canvas flows pass manual smoke tests.

## Phase 1: Canvas Kernel / NodeRecord

### P1.1 Canonical schemas

| Field | Value |
|---|---|
| Status | complete — versioned Python records, JSON Schema contracts, typed Legacy default ports, centralized state transitions, and fixture validation are implemented as a pure read boundary. |
| Task | Implement NodeRecord v1, EdgeRecord v1, ports, centralized state vocabulary, and validation. |
| Dependency | Phase 0 exit |
| Files | `schemas/node-record/*.schema.json`, `workbench/domain/canvas/models.py`, `states.py`, `ports.py` |
| Risk | Schema may overfit one Canvas mode or current provider nodes. |
| Acceptance criteria | Both Canvas fixture families validate through adapters; Core schema has no provider/industry branch. |

Checklist:

- [x] `schema_version` required.
- [x] Generic kinds only.
- [x] Versioned definition and renderer references.
- [x] Typed port contracts.
- [x] User model binding separated from Skill definition.
- [x] Artifact/Asset version references supported.
- [x] Unknown namespaced extensions preserved.
- [x] State transitions tested.

### P1.2 Lossless Legacy adapters

| Field | Value |
|---|---|
| Status | in progress — the backend adapter provides lossless node/connection views and fixture round trips; frontend compatibility modules and runtime integration are not started. |
| Task | Convert every known Classic/Smart node into a NodeRecord view and back without losing fields. |
| Dependency | P1.1, P0.3 |
| Files | `workbench/domain/canvas/legacy_adapter.py`, `static/js/workbench/canvas/legacy-node-adapter.js`, adapter tests |
| Risk | Hidden private records may contain undocumented shapes. |
| Acceptance criteria | Golden fixture round-trip diff is empty except approved normalization; unknown fields survive. |

Checklist:

- [x] Classic adapters (backend read/write view).
- [x] Smart adapters (backend read/write view).
- [x] Historical type labels preserved in `definition_ref` and raw payload.
- [x] Connection default-port adapters.
- [x] Group membership preserved in raw payload.
- [x] Error diagnostics without data loss.

### P1.3 Canvas repository interface

| Field | Value |
|---|---|
| Status | complete — a JSON compatibility repository preserves Legacy record shape, monotonic revisions, soft-delete visibility, purge semantics, and stale-write rejection. Existing load/save helpers and whole-Canvas PUT delegate to it. |
| Task | Wrap current JSON persistence with repository operations and expected-revision semantics. |
| Dependency | P1.1, P1.2 |
| Files | `workbench/repositories/canvas_repository.py`, `legacy_json_canvas_repository.py` |
| Risk | Lock and atomicity behavior may change unintentionally. |
| Acceptance criteria | Existing Canvas endpoints behave the same through the adapter; stale writes remain rejected; tests use a temporary repository. |

### P1.4 NodeCreationService

| Field | Value |
|---|---|
| Status | complete — a pure application service now validates authorization, definition availability, explicit model compatibility, expected revision, idempotency, and audit emission through injected interfaces. It is intentionally not wired to a browser entry yet. |
| Task | Implement the single creation pipeline with idempotency, authorization/registry interfaces, model compatibility validation, revision update, and audit hook. |
| Dependency | P1.1, P1.3 |
| Files | `workbench/application/node_creation.py`, service unit tests |
| Risk | Compatibility implementations may become permanent bypasses. |
| Acceptance criteria | One request creates one validated node; duplicate request is idempotent; disabled/missing definition fails safely; service has no Canvas DOM/provider/industry imports. |

Checklist:

- [x] Command/request model.
- [x] Source enum for menu, command, drag, import, Agent, Legacy.
- [x] Actor/project authorization interface.
- [x] Definition/renderer resolution interfaces.
- [x] Model compatibility interface without auto-switch.
- [x] Atomic repository update.
- [x] Audit/domain event.
- [x] Idempotency test.

### P1.5 Versioned Canvas node API

| Field | Value |
|---|---|
| Status | complete (restricted compatibility slice) — localhost-only `GET`, `POST`, `PUT`, and `DELETE` routes are registered for `legacy:image@0`. They require explicit `X-User-ID` and project/owner scope checks; all writes require an expected revision; create is idempotent; and writes emit secret-free JSONL audit events. Deletion removes Legacy connections that reference the deleted node. |
| Task | Expose node get/create/update/delete through a versioned router backed by application services. |
| Dependency | P1.3, P1.4 |
| Files | `workbench/api/canvas_nodes.py`, `main.py`, contract tests |
| Risk | New commands and whole-Canvas PUT can race. |
| Acceptance criteria | Expected revision protects both paths; response includes new revision; authorization hook is mandatory; OpenAPI shapes match contract tests. |

### P1.6 Frontend NodeRecord compatibility modules

| Field | Value |
|---|---|
| Status | complete — both Canvas pages load side-effect-free browser compatibility/state helpers and an explicit versioned-node API client before the existing editor script. Their top-level blank Image context-menu entry uses the versioned create service on loopback; group, upload, import, output-conversion, and all non-loopback creation remain Legacy pending separate migrations. |
| Task | Load shared node schema/state/creation modules in both Canvas pages. |
| Dependency | P1.1, P1.2, P1.5 |
| Files | `static/js/workbench/canvas/*.js`, `static/canvas.html`, `static/smart-canvas.html` |
| Risk | Script order/global collisions in the no-bundler frontend. |
| Acceptance criteria | Modules expose one namespaced API; both pages load without console errors; Node syntax checks and browser smoke pass. |

### P1.7 Migrate first creation paths

| Field | Value |
|---|---|
| Status | complete — with explicit `versioned_nodes=1` on loopback, Classic top-level and quick-toolbar blank Image, Prompt, Loop, plus linked Group creation use versioned service boundaries; every Classic quick-toolbar item first resolves through the shared creation catalog, while its un-migrated fixed-node constructors remain Legacy. Smart supports independent Image, Prompt, Loop, and empty Group definitions. Successful creates retain the respective editor's undo snapshot. Upload, import, output conversion, adding members to a Smart Group, nested grouping, and all non-loopback paths remain Legacy. Browser creation, immediate undo, and save/reload verification completed on 2026-09-02. |
| Task | Route blank Media/Image creation in both Canvases through NodeCreationService, then migrate Prompt, Loop, Group, and fixed nodes one family at a time. |
| Dependency | P1.6 |
| Files | `static/js/canvas.js`, `static/js/smart-canvas.js` |
| Risk | These files already contain user changes; direct node expectations may break. |
| Acceptance criteria | Created node looks and saves the same; undo/selection/position work; compatibility flag can revert to Legacy creation during the verification window. |

The linked-Group path requires the new `GraphMutationService` contract: it validates one Canvas revision, authorization, a new node, and an edge that references that node as one atomic repository action. `LegacyJsonGraphMutationRepository` now persists the restricted `legacy:group@0` shape and its edge under one lock; successful transactions emit a secret-free audit event. No endpoint or UI path uses this contract yet.

Required precondition:

- [x] Inspect the relevant current creation and save paths without reformatting unrelated code.
- [ ] Avoid unrelated formatting or function moves.
- [x] Add focused browser/manual steps for each migrated family.

### Phase 1 exit checklist

- [ ] NodeRecord/EdgeRecord schemas pass contract tests.
- [ ] All known Legacy nodes adapt losslessly.
- [ ] Central state vocabulary is used at the new boundary.
- [ ] NodeCreationService is the only path for at least one entry in each Canvas.
- [ ] Versioned node API is revision-safe.
- [ ] Classic and Smart Canvas round trips pass.
- [ ] Existing fixed nodes still execute.
- [ ] No WholeHouse/provider logic entered Core.
- [ ] User changes were preserved.

## Phase 2: NodeShell / RendererRegistry

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P2.1 | Add Renderer manifest schema and registry | Phase 1 | Registry becomes Skill-specific | complete — `RendererManifest` and `RendererRegistry` resolve finite versioned renderer IDs without Skill branches; no current DOM renderer is switched in this increment. |
| P2.2 | Implement NodeShell | P2.1 | Interaction regression | in progress — `WorkbenchNodeShell` supplies accessible header, content, status, footer, toolbar, port, drag, resize, selection, and focus intent hosts without writing Canvas state. With explicit local `node_shell=1`, it mounts for Smart Groups including groups with members; selection, focus, menu, port-drag, drag, and resize intents flow through the Smart Canvas page adapter and reuse the corresponding Legacy state machines. Classic Canvas now mounts the same shell for opt-in media Image and Group nodes, maps shell intents back to its existing selection, drag, resize, and link state machines, and promotes shell ports to the outer Legacy `.node` element so original port geometry and link hit-testing are retained. A Classic Group input accepts Image/Prompt connections and records the incoming member in its existing `items` payload. Both Classic and Smart canvas context menus expose Group creation; when the local versioned-node path is enabled, Classic creates the empty Group through `NodeCreationService`. Their shared create/group command IDs, create-menu order, connection-start, connected-node creation, and add-to-group intents are defined centrally in `WorkbenchCanvasCommands`; on either page, dragging a port to empty canvas opens the shared Core create choices. Smart's versioned Image, Group, Prompt, Loop, and MiniMax selections now use `GraphMutationService` to persist the new node plus edge atomically; existing execution and provider configuration remain on their Legacy compatibility paths. The clean Smart Canvas port-create manual acceptance passed on 2026-09-03. |
| P2.3 | Implement LegacyRenderer | P2.2 | Existing DOM assumptions | complete — `WorkbenchLegacyRenderer` mounts any lossless Legacy payload through the NodeShell content host without node-type branches. Its content slot preserves existing Smart Group body DOM and the Classic Group's already-built Legacy summary when it has no displayable media. With the explicit local `node_shell=1&legacy_renderer=1` gate, Smart non-media top-level nodes and all current Classic non-media families adopt their existing body DOM into that slot: Prompt, Loop, Prompt Group, Output, LLM, Generator, Midjourney, ModelScope Generation, Video, Comfy, RunningHub, LTX Director, and MiniMax. Their form controls, event listeners, execution paths, and stored JSON remain Legacy-owned, while NodeShell owns ports, drag, resize, title, and state chrome. Existing floating actions remain page-owned, and Classic plus non-opted-in Smart nodes retain Legacy rendering as the fallback. |
| P2.4 | Implement MediaRenderer | P2.2 | Media playback/preview regression | complete — `WorkbenchMediaRenderer` derives display items from media/output records, supports lazy image and video rendering with native controls, metadata preload, and inline playback, and has no node-type branches or persistence side effects. Native video interaction stops propagation at the renderer boundary without preventing default browser playback, so Canvas selection/drag handlers cannot recreate a playing video; Legacy Smart and Classic preview overlays also follow real `play`, `pause`, and `ended` events. Existing media DOM remains the default. With explicit local `media_renderer=1`, top-level Smart image nodes and Smart Groups with member media mount through NodeShell and MediaRenderer; with `node_shell=1` as well, Classic Image and Group media cards use NodeShell chrome while retaining Classic state machines. |
| P2.5 | Add semantic zoom | P2.2 | Performance/legibility | complete — pure `WorkbenchSemanticZoom` policy produces two view models: full content at scale `>= 0.75`, and a summary strip below `0.75`. With explicit local `node_shell=1&semantic_zoom=1`, Smart applies those view models to NodeShell and Legacy Smart nodes, and Classic applies them to opt-in NodeShell media/group cards plus every retained Legacy Classic card. Both presentations are visual-only; existing viewport math, persisted node sizes, graph anchors, and port connectivity remain unchanged. |
| P2.6 | Screen-space toolbar/ports | P2.2 | Coordinate mismatch | complete — pure `WorkbenchScreenSpaceControls` converts node positions into toolbar/input/output screen anchors and preserves a requested pixel target through inverse world sizing. With explicit local `node_shell=1&screen_space_controls=1`, Smart Canvas applies it to mounted NodeShell ports and selected-node toolbars; persisted node geometry and connection anchors remain unchanged. Manual zoom, port-drag, and toolbar acceptance passed on 2026-09-03. |

Phase 2 checklist:

P2.3 extension: Classic Video Generation now adopts the lossless Legacy body under the same explicit local `node_shell=1&legacy_renderer=1` gate. Its provider/model and video settings, media/reference controls, run/cascade controls, and input/output ports retain their existing behavior.

Classic Comfy nodes also adopt the lossless Legacy body under that gate. Their workflow selection, mode-specific field schema, parameter/random controls, media inputs, run/cascade controls, and input/output ports remain adapter-owned.

Classic RunningHub nodes also adopt the lossless Legacy body under that gate. Their WebApp/workflow selection, payment and machine configuration, dynamic parameter schema, media inputs, run/cascade controls, and input/output ports remain adapter-owned.

Classic LTX Director nodes also adopt the lossless Legacy body under that gate. Their timeline editor, duration and frame parameters, linked-image inputs, run/cascade controls, and input/output ports remain adapter-owned.

Classic MiniMax nodes also adopt the lossless Legacy body under that gate. Their timeline, media library, clip settings, references, preview, run/cascade controls, and input/output ports remain adapter-owned.

Classic Prompt Group nodes also adopt the lossless Legacy summary body under that gate. Their member grouping, summarized prompt count and output-only port contract remain adapter-owned.

The Classic adapter now has a consolidated regression gate for every migrated non-media family: both local feature flags, the complete allowlist, and each input/output contract are asserted together. The complete Classic fixture also load-saves without changing its nodes, connections, or settings.

Manual acceptance passed on 2026-09-04 using the existing `P2.4 Classic video acceptance` canvas: without flags, the Classic cards retained their Legacy rendering; with `node_shell=1&legacy_renderer=1`, the Image, Video, LLM, Comfy, and Output cards showed shared NodeShell chrome, resize controls, and the expected graph ports without editing or saving node data. P2.3 is complete for the current adapter boundary; feature gates remain intentional, and Legacy DOM/execution/persistence removal is deferred to the Unified Canvas convergence gates.

P2.4 MediaRenderer acceptance also passed on 2026-09-04 on that canvas with `node_shell=1&media_renderer=1`: the video media card remained visually primary, promoted its NodeShell chrome and graph ports, and opened native inline video controls on playback without changing canvas data.

P2.5 semantic-zoom acceptance passed on 2026-09-04 without editing or saving node data. The Classic six-node acceptance canvas showed the full cards at 100% and the six title/status strips with ports at 72%. The Smart acceptance canvas showed full content at 105% and a summary card at 65%. This completes the current visual-only, opt-in semantic-zoom boundary; persistent geometry, ports, and graph state remain Legacy-owned.

The opt-in Classic NodeShell plus LegacyRenderer path now has a dedicated 100/300-node Prompt-card baseline in `docs/benchmarks/canvas-node-shell-baseline-2026-09-04.md`. Both samples rendered all expected nodes and completed the harness interactions. The 300-node minimap refresh measured 149 ms, above the provisional 120 ms local alert, so minimap scheduling remains a tracked P2 performance follow-up rather than a completed performance acceptance.

The first minimap follow-up separates viewport-box updates from geometry rebuilds and bypasses inactive semantic-zoom card walks. The source-level contract is covered by frontend checks. Safari's offscreen iframe recheck remained at 141 ms, confirming it cannot validate the improvement. The harness now has an explicit visible, pointer-inert target mode; its 300-node NodeShell recheck measured zoom 38 ms, pan 104 ms, and minimap refresh 15 ms, all below the provisional 120 ms local alert. This remains a single local sample rather than a percentile budget.

- [x] Migrated and Legacy nodes coexist.
- [x] Renderer lookup is data-driven.
- [x] NodeShell owns common chrome.
- [x] Media remains visually primary.
- [ ] Performance stays within recorded regression budget.

## Unified Canvas convergence program

The program is governed by `docs/proposals/unified-canvas-runtime.md`. It does not add a third Canvas engine: every retained behavior is extracted under shared Canvas application/runtime, renderer, and executor boundaries. The existing pages are temporary source adapters; after canonical migration and acceptance, `canvas.html` is the only page and entry. The UI, catalog, and canonical NodeRecord do not distinguish old/new or Classic/Smart nodes.

| ID | Status | Task | Acceptance criterion |
|---|---|---|---|
| U0 | complete | Record current capability inventory, canonical-entry contract, options, compatibility, rollback, and acceptance gates | Proposal authorizes duplicate mode/runtime removal only after all gates and backups pass |
| U1 | complete — shared, side-effect-free CanvasRuntime owns viewport normalization, coordinate conversion, anchor-preserving zoom, selection, geometry, and command events. With `unified_canvas=1`, both source adapters route selection, pan, zoom, drag, and resize through it. Shared pure viewport fitting now drives both zoom-preview/recovery paths; renderers and persistence remain adapter-owned. | Add shared viewport, selection, geometry, and transaction-intent state model behind one feature flag | Both page adapters pass the same pan/zoom, selection, multi-select, drag, resize, and recovery tests |
| U2 | in progress — shared side-effect-free graph geometry supplies left/right port anchors and horizontal edge curves; a shared port-drop intent normalizes either drag direction into one `out → in` connection proposal; shared membership queries resolve parent groups and edge-display scopes. Classic and Smart adapters use these seams while retaining compatibility validation, group UI/drag behavior, and stored edge dictionaries. | Add shared graph/port/group interaction contracts | Classic and Smart fixtures use one port geometry and edge interaction path without changing stored edges |
| U3 | in progress — `WorkbenchUnifiedRenderHost` is the common card-host boundary for NodeShell construction and RendererRegistry selection. Classic media/groups, Classic Prompt/Loop behind the opt-in compatibility flag, and Smart media/groups/adapter cards now pass a normalized record plus optional lossless DOM payload into that host. NodeShell now declares visible ports per card: Prompt retains its output-only contract, while Loop always exposes both ports so connections can be created before configuring its input mode. A focused mixed-record check mounts a Classic Prompt and Smart Image in the same host/registry without a source-mode input; renderer selection follows normalized record capability only. Both page adapters retain their Legacy DOM selector lists and concrete interaction actions, then delegate control cleanup, card mount, generic Shell-intent dispatch, and NodeShell view-model construction through shared host contracts. | Compose one render host from NodeShell and canonical browser RendererRegistry adapters | One host renders both source fixtures without a source-family label or behavior switch |
| U4 | in progress — `WorkbenchCreationCatalog` now validates stable creation IDs, definition references, ordering, and adapter metadata without DOM or storage side effects. `WorkbenchCanvasCommands` projects the catalog for each retained page adapter; both context menus order and hide entries from that projection, and every Classic quick-toolbar item resolves through it before invoking a page adapter. Top-level Image, Prompt, Loop, and Group menu creation in Classic and Smart consult one catalog-declared versioned-creation capability and dispatch through their existing `NodeCreationService` client adapters. Smart port-to-empty-space creation for Image, Prompt, Loop, Group, and MiniMax, plus Classic port-to-empty-space Group creation, use a catalog-declared graph-mutation capability to select their existing atomic node-and-edge client adapters. Smart nested group creation and all remaining fixed-node constructors retain their compatibility behavior. | Expose one registry-backed creation catalog and converge mutation entries | Every migrated creation entry uses NodeCreationService or GraphMutationService |
| U5 | in progress — `WorkbenchGenerationIntent` now derives a side-effect-free `branch` or `in_place` result target from generic source/output conditions. Smart generation consumes that intent before applying its unchanged Legacy pending-output or in-place mutation behavior; Composer/provider requests, output payloads, and persistence remain page-owned. | Wrap retained execution and workflow behavior behind executor adapters | Representative media, Prompt/LLM, Loop, Group, output, and provider flows run in one host |
| U6 | pending | Switch Canvas list and new-Canvas UX to one `canvas.html` entry | Product navigation offers one Canvas; old deep links still resolve |
| U7 | pending | Migrate records, run the compatibility/performance window, and remove duplicate mode/runtime code | Backups validate; canonical records round-trip; only one Canvas page, runtime, catalog, and entry remain |

The next implementation slice continues U3 by extracting the remaining renderer contracts into the shared host. It must add focused tests before wiring each adapter and must not change Canvas JSON, Canvas `kind`, provider behavior, or the visible Canvas-list route.

## Phase 3: Inspector / Toolbar / Command Palette

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P3.1 | Schema-driven Inspector | Phase 2 | Provider parameters leak into Core | Generic sections plus namespaced adapter schemas render correctly |
| P3.2 | Generic Toolbar intents | P3.1 | Renderers mutate state directly | Actions emit commands through services |
| P3.3 | Registry search query | Phase 2 | Divergent menus remain | Context menu, slash, Command-K, Skill Library share results |
| P3.4 | Unified fixed-function coverage | P3.3 | Users lose current tools | All retained fixed entries remain reachable without a Legacy or source-mode label |

Phase 3 checklist:

- [ ] Advanced settings move to Inspector for migrated nodes.
- [ ] Canvas display remains concise.
- [ ] All migrated creation entry points call NodeCreationService.
- [ ] Search supports keyboard and accessibility behavior.

## Phase 4: SkillRegistry / SkillNode

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P4.1 | Skill manifest JSON Schema | Phase 3 | Schema too provider-specific | Image Analysis and a non-model script Skill both validate |
| P4.2 | Discover/list/search/get | P4.1 | Unsafe paths or duplicate IDs | Invalid Skills quarantine with diagnostics |
| P4.3 | Enable/disable/reload | P4.2 | Active projects lose definitions | Historical references remain readable |
| P4.4 | Skill executor interface | P4.2 | Executor bypasses permissions | Declared permissions are enforced |
| P4.5 | Skill Library | P4.2, P3.3 | UI duplicates registry logic | Library is a registry projection |
| P4.6 | `common.image-analysis` | P4.1–P4.5 | Reference Skill overfits WholeHouse | Generic image input and analysis output only |

Gate 1 checklist:

- [ ] Add a new Skill folder.
- [ ] Make no Canvas source edit.
- [ ] Registry discovers it.
- [ ] Skill Library displays it.
- [ ] NodeCreationService creates it.
- [ ] RendererRegistry renders it.
- [ ] Runtime executes it.
- [ ] Restart restores it.

## Phase 5: ModelRegistry / user selection

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P5.1 | ProviderAdapter interface | Gate 1 | Breaking current protocols | Current providers remain reachable through compatibility adapters |
| P5.2 | Model metadata/capabilities | P5.1 | Inconsistent capability vocabulary | Registry validates normalized models |
| P5.3 | Compatibility filter | P5.2 | False compatibility | Skill inputs/outputs/capabilities are checked |
| P5.4 | Selection precedence | P5.3 | Silent fallback remains | Node > Skill user default > system user default; missing selection is explicit |
| P5.5 | Provenance choice capture | P5.4 | Requested and actual model diverge | Both are validated and actual use is recorded |

Gate 2 checklist:

- [ ] Two compatible providers/models available.
- [ ] User selects provider/model A.
- [ ] User selects provider/model B in a separate run.
- [ ] Skill definition is unchanged.
- [ ] No silent switch occurs.
- [ ] Provenance records each actual choice.

## Phase 6: CodexBridge / Agent Panel

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P6.1 | Inspect current stable Harness/App Server | Gate 2 | Binding to obsolete protocol | Findings and selected adapter contract documented |
| P6.2 | CodexBridge interface | P6.1 | CLI details leak upward | Product services import only bridge interface |
| P6.3 | CLI compatibility adapter | P6.2 | Existing Codex flow regresses | Current chat/image behavior remains available |
| P6.4 | Scoped Workbench tools | P6.2 | Agent overreach | Default-deny project-scoped tools and audit |
| P6.5 | Persistent Agent events | P6.2 | UI loses progress on reconnect | Task/plan/tool/approval/result can replay |
| P6.6 | Agent Panel | P6.5 | Becomes chat-only UI | All required execution states render |
| P6.7 | Graph proposal approval | P6.4–P6.6 | Silent bulk mutation | User confirmation is default |

Gate 3 checklist:

- [ ] Read Canvas selection through API.
- [ ] Search SkillRegistry.
- [ ] Propose workflow.
- [ ] Display proposed node changes.
- [ ] Receive user confirmation.
- [ ] Create nodes/edges through services.
- [ ] Execute Skill.
- [ ] Display progress/tool activity.
- [ ] Persist result and provenance.

## Phase 7: Asset + Knowledge

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P7.1 | Asset/AssetVersion/BlobRef | Gate 3 | URL identity assumptions | Stable IDs and immutable versions coexist with Legacy URLs |
| P7.2 | Asset backfill | P7.1 | Duplicate/unresolved media | Hash-based report with no source deletion |
| P7.3 | Authorized delivery | Auth baseline | Current public URLs break | Compatibility URLs transition with permission tests |
| P7.4 | Drop/paste integration | P7.1, NodeCreationService | Partial blob/record creation | Transaction/cleanup behavior tested |
| P7.5 | Knowledge schemas/scopes | Gate 3 | Asset and Knowledge merge | Independent IDs and repositories |
| P7.6 | Hybrid retrieval foundation | P7.5 | Vector-only implementation | Full text, exact, metadata contracts pass |
| P7.7 | KnowledgeSnapshot | P7.6 | Non-reproducible retrieval | Formal run records exact source versions |

## Phase 8: Workflow + Version

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P8.1 | WorkflowDefinition/Version | Phase 7 | Mutable graph overwrites history | Versions are immutable |
| P8.2 | WorkflowRun/NodeRun/events | P8.1 | In-memory loss | Restart recovers authoritative state |
| P8.3 | Run/retry/cancel | P8.2 | Duplicate provider calls | Idempotency and attempt records |
| P8.4 | Pause/resume adapters | P8.2 | Provider cannot pause | Capability is explicit; unsupported is safe |
| P8.5 | ArtifactVersion/Provenance | P8.2 | Incomplete lineage | Required fields validate |
| P8.6 | Versioned import/export | P8.1, P8.5 | Unsafe archives/schema drift | Validate, contain paths, verify inventory |

## Phase 9: Outdated + Approval

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P9.1 | Dependency/version comparison | Phase 8 | False stale propagation | Deterministic graph tests |
| P9.2 | Outdated UI/actions | P9.1 | Old result disappears | Prior versions remain accessible |
| P9.3 | Approval records/policy | Auth baseline, P8.5 | Agent self-approval | Actor/role separation enforced |
| P9.4 | Frozen immutability | P9.3 | Hidden mutation of formal result | Changes create new version |

## Phase 10: WholeHouse Pack

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P10.1 | Pack manifest/runtime | Gates 1–3 | Core imports pack | Disable test proves Core independence |
| P10.2 | Entity registrations | P10.1 | Domain tables enter Core | Namespaced generic definitions only |
| P10.3 | 12–15 core Skills | P10.1 | Catalog expands before quality | Each Skill has manifest, instructions, tests, permissions |
| P10.4 | Workflow templates | P10.2, P10.3 | Workflow hard-coded in Core | Templates are pack data |
| P10.5 | Industry/company knowledge | Phase 7, P10.1 | Wrong scope leakage | Scope and snapshot tests |
| P10.6 | V1 business-loop validation | P10.2–P10.5 | Feature creep | Stops at approved/frozen design and handoff readiness |

WholeHouse initial catalog checklist:

- [ ] Project Intake
- [ ] Requirement Analysis
- [ ] Floorplan Analysis
- [ ] Site Photo Analysis
- [ ] Reference Analysis
- [ ] Style Direction
- [ ] Space Concept
- [ ] Cabinet Concept
- [ ] Material Proposal
- [ ] Render
- [ ] Image Edit
- [ ] Version Compare
- [ ] Design Review
- [ ] Pending Issues
- [ ] CAD Handoff

The exact release subset must stay within the agreed 12–15 range.

## Phase 11: CAD Handoff

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P11.1 | Handoff manifest schema | Phase 10, frozen versions | Premature CAD detail | Generic versioned contract only |
| P11.2 | JSON/PDF/CSV/image exporter | P11.1 | Package inconsistency | Inventory/checksum validation |
| P11.3 | Read-back validator | P11.2 | Export appears valid but is incomplete | Independent parser verifies required entries |
| P11.4 | Audit/provenance linkage | P11.2 | Untraceable package | Every formal artifact resolves |

Checklist:

- [ ] Manifest.
- [ ] Project summary.
- [ ] Structured project/spaces data.
- [ ] Materials and cabinet concepts.
- [ ] Renders/references.
- [ ] Pending issues.
- [ ] Checksums and provenance.
- [ ] Package inventory test.
- [ ] No production CAD promise.

## Phase 12: Real Project Validation

| ID | Task | Dependency | Primary risk | Acceptance criteria |
|---|---|---|---|---|
| P12.1 | Select representative projects | Phase 11 | Biased sample | Small/medium/large complexity represented |
| P12.2 | Execute complete workflow | P12.1 | Manual gaps hidden | Recorded steps and results |
| P12.3 | Performance/recovery tests | P12.1 | Lab-only confidence | Restart, retry, 100–300 nodes tested |
| P12.4 | Permission/security review | Auth implementation | LAN exposure remains | Owner/Editor/Viewer matrix passes |
| P12.5 | Handoff review | P12.2 | Downstream unusable | Designer/CAD reviewer accepts package contract |

## Cross-phase quality checklist

Apply to every code round:

- [ ] Read current diffs before editing.
- [ ] Preserve unrelated user changes.
- [ ] State compatibility contract.
- [ ] Add focused tests before or with behavior.
- [ ] Use types at new boundaries.
- [ ] Use structured errors.
- [ ] Log useful events without secrets.
- [ ] Validate paths, uploads, URLs, and subprocess arguments.
- [ ] Enforce project permission at application-service boundary.
- [ ] Keep Skill/model separation.
- [ ] Keep Knowledge/Asset separation.
- [ ] Keep Core/Industry Pack separation.
- [ ] Record schema/API/database/UI changes.
- [ ] Run syntax and focused automated checks.
- [ ] Perform manual browser verification.
- [ ] Update architecture documents when contracts change.

## Manual smoke matrix for early phases

### Classic Canvas

1. Open an existing fixture-backed Canvas.
2. Pan and zoom.
3. Create, drag, resize, select, group, connect, and delete a node.
4. Save and reload.
5. Open the same Canvas in a second tab and verify stale/remote update behavior.
6. Export/import a selected workflow.
7. Verify minimap navigation.

### Smart Canvas

1. Open an existing Smart Canvas.
2. Create Image, Prompt, Loop, Group, and MiniMax nodes.
3. Connect nodes and move nodes into/out of groups.
4. Save and reload.
5. Verify media preview and asset-panel interaction.
6. Verify minimap and workflow transfer.
7. Verify remote update behavior.

### Provider and secret boundary

1. Open API settings.
2. Confirm configured-secret presence can be shown without value/preview.
3. Save a new secret through the backend.
4. Inspect network responses and browser storage for absence of the secret.
5. Run one backend-mediated provider request.
6. Confirm logs redact the secret.

## Required per-round report template

Every implementation round reports these sections in this order:

1. Completed work
2. Modified files
3. Added files
4. Deleted files
5. Architecture changes
6. Database changes
7. API changes
8. UI changes
9. Compatibility
10. Automated test results
11. Manual test steps
12. Known issues
13. Recommended next step

## Next authorized action after this baseline

The next implementation round should be Phase 0 only, beginning with environment reproducibility, golden fixtures, and the secret-boundary test. It should not begin NodeShell, Skill catalog development, WholeHouse business logic, database authority switching, or frontend framework replacement.
