# Current Architecture Baseline

## Audit metadata

- Audit date: 2026-09-02
- Repository: `https://github.com/GUOXIAOLUO/canvas.git`
- Audited revision: `544a5a0` (`2026-08-30 Remove discontinued project notices`)
- Application version file: `2026.08.28`
- Platform used for the audit: macOS arm64, zsh
- Scope: repository structure, startup scripts, dependencies, frontend pages, both Canvas implementations, FastAPI routes, persistence, providers, Agent behavior, ComfyUI, events, authentication, permissions, secrets, tests, and current worktree

At audit time the worktree contained pre-existing, uncommitted changes in:

- `main.py`
- `static/js/canvas.js`
- `static/js/smart-canvas.js`

Those changes were inspected but not modified by this architecture-baseline round.

## Executive finding

The repository is a functional local-first AI media studio with two infinite-canvas editors, a broad provider proxy, ComfyUI and RunningHub integration, asset management, chat, JSON persistence, and basic cross-tab/LAN update notification.

It is not yet the target AI Workbench architecture. The current implementation is a static-page and FastAPI monolith with provider- and feature-specific nodes hard-coded into large JavaScript files and a single 19,287-line Python module. Project, Canvas, workflow, chat, asset, provider, updater, subprocess, and media-processing concerns share the same process and mostly the same source file. A versioned, pure Python NodeRecord/EdgeRecord validation and Legacy adapter seam now exists, current Canvas load/save helpers delegate to a compatibility JSON repository, and dependency-injected creation and mutation services back a localhost-only `/api/v1` read/create/update/delete slice for restricted Legacy definitions. A second scoped route atomically creates approved Smart Image, Group, Prompt, Loop, or MiniMax nodes and their connecting edge under one Canvas revision. Both editors now load side-effect-free browser compatibility helpers and a versioned-node API client; their top-level blank Image menu entry uses it on loopback only. Grouped/imported/uploaded/output-derived images remain Legacy. The API is disabled for non-loopback bindings; writes use a revision, scoped local actor check, and secret-free audit event. These seams are not yet a dynamic Skill Runtime, broadly migrated frontend entry path, provenance runtime, Knowledge Service, or enforceable production project authorization.

The migration should reuse the working Canvas interaction kernel and provider execution paths while placing stable domain boundaries around them. A big-bang rewrite would risk the strongest parts of the current product.

## Repository shape

| Area | Current files | Current responsibility |
|---|---|---|
| Backend | `main.py` | FastAPI app, 165 route decorators, provider adapters, storage, update system, subprocesses, media transforms, chat, Agent router, Canvas, workflow, assets |
| Studio shell | `static/index.html` | Sidebar navigation and lazy iframe host for feature pages |
| Classic Canvas | `static/canvas.html`, `static/js/canvas.js`, `static/css/canvas.css` | General graph editor with fixed media/generation node types |
| Smart Canvas | `static/smart-canvas.html`, `static/js/smart-canvas.js`, `static/css/smart-canvas.css` | Media-first generation canvas with prompt, loop, group, and MiniMax nodes |
| Canvas list/projects | `static/canvas-list.html`, `static/js/canvas-list.js` | Project and Canvas selection/creation |
| Chat/Agent | `static/gpt-chat.html`, backend chat routes | Chat, image generation/edit routing, conversations |
| Provider settings | `static/api-settings.html`, `static/js/api-settings.js` | Provider/model metadata and API secret entry |
| ComfyUI settings | `static/comfyui-settings.html`, `static/js/comfyui-settings.js` | Instances and workflow/config management |
| Asset UI | `static/asset-manager.html`, `static/js/asset-manager.js` | Local files, asset libraries, captions, classification, registration |
| Workflows | `workflows/*.json`, `workflows/*.config.json` | Bundled ComfyUI graphs and UI field mappings |
| Runtime data | `data/`, `assets/`, `output/`, `history.json`, `API/.env` | JSON metadata, Canvas files, media, history, secrets |
| Tests | `tests/test_canvas_log_cleanup.py` | Canvas log deletion, media ownership cleanup, conflict behavior |
| External tools | `CLI/`, `tools/` | Codex/Gemini/Jimeng installers and browser/Photoshop connectors |

The source contains approximately 859 top-level Python functions, 77 Python classes, 882 JavaScript functions in Classic Canvas, and 1,108 JavaScript functions in Smart Canvas. These counts describe coupling and change risk; they are not quality scores.

## Runtime topology

```text
Browser
  |
  | HTTP, SSE, WebSocket
  v
FastAPI process on 127.0.0.1:3000 by default
  |-- static HTML/CSS/JavaScript and public media mounts
  |-- JSON/filesystem persistence
  |-- provider HTTP adapters
  |-- Codex, Gemini, and Jimeng subprocesses
  |-- ComfyUI LAN HTTP calls
  |-- RunningHub/ModelScope/other remote APIs
  `-- in-memory queue and WebSocket connection manager
```

`python3 main.py` starts Uvicorn on `127.0.0.1` by default. LAN binding is an explicit compatibility opt-in through `WORKBENCH_HOST=0.0.0.0`; it remains unauthenticated and is only appropriate on a trusted network. There is no reverse proxy, identity provider, or separate worker process in the repository baseline.

## Frontend

### Studio shell and navigation

`static/index.html` is the application shell. It lazy-loads feature pages into same-origin iframes for Z-Image, Enhance, Klein, Angle, Online generation, GPT chat, Canvas list, assets, API settings, and ComfyUI settings.

The shell synchronizes theme, language, scale, and selected-page state through `localStorage`, `postMessage`, and `BroadcastChannel`. This provides pragmatic isolation between existing pages but does not provide a unified Workbench state or component boundary.

The current first-level navigation reflects individual tools more than the target three-part information architecture of Projects, Workbench, and Resources.

### Frontend technology

- HTML, CSS, and browser JavaScript; no package manifest or bundler is present.
- Lucide is vendored; Tailwind CDN assets and local fonts are vendored.
- State is held in module/global variables, Canvas JSON, and browser storage.
- Rendering is primarily manual DOM creation and `innerHTML` replacement.
- Pages call FastAPI routes with `fetch` directly.
- There is no frontend type system, schema-generated client, shared domain package, or component test harness.

This technology is sufficient for the first migration seams. The audit found no evidence that a React or Vue rewrite is required before NodeRecord and registry boundaries are proven.

## Canvas

### Two Canvas implementations

The repository has two parallel editors that share backend Canvas persistence but not a single frontend kernel:

| Capability | Classic Canvas | Smart Canvas |
|---|---|---|
| Main script | `static/js/canvas.js` | `static/js/smart-canvas.js` |
| Stored kind | `classic` | `smart` |
| Node focus | Graph of typed generation/media nodes | Media-first generation and iterative workflow |
| Viewport | Saved partly in session/client behavior; backend preserves existing viewport for Classic | Persisted in Canvas JSON |
| Node render | One `renderNode` function with type branches | One large `render` path with type branches |
| Connections | `connections` array and type-specific `canConnect` | `canvas.connections` with ports and flow behavior |
| Collaboration | WebSocket invalidation plus 2.5-second metadata polling | WebSocket invalidation plus metadata polling |

Both implement their own selection, drag, resize, zoom, panning, minimap, connection rendering, undo-related behavior, file drop, asset integration, workflow transfer, persistence, and node execution coordination. This duplication is a major migration risk and also a source of reusable interaction behavior.

### Current Canvas record

A new Canvas is stored as one JSON file under `data/canvases/<canvas_id>.json` with this effective shape:

```json
{
  "id": "opaque-id",
  "title": "Canvas title",
  "icon": "layers",
  "kind": "classic",
  "owner": "",
  "color": "",
  "pinned": false,
  "project": "default",
  "created_at": 0,
  "updated_at": 0,
  "nodes": [],
  "connections": [],
  "viewport": {"x": 0, "y": 0, "scale": 1}
}
```

The save endpoint adds `logs` and `settings` when supplied. There is no Canvas-level `schema_version`, node version, workflow version, author identity, immutable revision, or formal validation of the arbitrary `nodes` dictionaries.

### Node creation

Classic Canvas has individual constructors such as `addImageNode`, `addPromptNode`, `addLoopNode`, `addGroupNode`, `addLLMNode`, `addGeneratorNode`, `addMidjourneyNode`, `addMsGenNode`, `addVideoNode`, `addMiniMaxNode`, `addRhNode`, `addLTXDirectorNode`, `addComfyNode`, and `addOutputNode`. Menu definitions are literal arrays of those types. `createNodeByType` dispatches to those functions.

Smart Canvas has separate constructors for `smart-image`, `smart-prompt`, `smart-loop`, `smart-minimax`, and `smart-group`. Its HTML creation menu hard-codes upload, group, prompt, loop, and MiniMax. `createNodeFromMenu` dispatches directly.

File uploads and workflow imports also construct dictionaries and append to node arrays. There is no single NodeCreationService, manifest lookup, permission check, or schema validation boundary.

### Node rendering

Classic `renderNode` chooses title, dimensions, ports, and body renderer with `node.type` conditionals. Generation execution repeats a similar type-dispatch list. `CANVAS_GENERATOR_TYPES` and `CANVAS_MEDIA_OUTPUT_TYPES` are literal arrays.

Smart Canvas builds Node HTML inside its main `render` function and branches on the five Smart types. The node shell, toolbar, runtime state, media behavior, and type-specific configuration are interleaved.

There is no RendererRegistry. Adding a new business Skill as a new type would require edits in creation, render, connection, execution, save/normalization, menu, and CSS paths.

### Deletion, drag, resize, zoom, selection, and groups

Both editors provide working interaction code:

- pointer-driven node drag with world/screen coordinate conversion;
- node resizing and geometry refresh;
- board panning and wheel zoom;
- single and multi-selection;
- grouping and movement of group children;
- clipboard/file drop behavior;
- soft Canvas deletion to a 30-day recycle bin and permanent purge;
- per-node deletion in the browser followed by debounced Canvas save.

The backend performs optimistic stale-write rejection using `base_updated_at`. Classic Canvas retries or applies remote state; Smart Canvas includes a merge path based primarily on node identity and media union behavior. This is useful but is not a general operation log or CRDT.

### Connections

Connections are stored as dictionaries with `id`, `from`, and `to`; Smart Canvas may also store a connection kind. Classic Canvas validates connections through hard-coded type compatibility. It can auto-create an Output node when a generator output is dragged to empty space.

Ports are generic visual handles, but compatibility is tied to current node types rather than manifest-declared input/output contracts. There are no versioned port schemas or typed Artifact references.

### Context menus and node-entry UI

Both editors support a blank-canvas context menu or double-click creation path. Classic also has link creation and input/output menus. The lists are hard-coded. There is no command palette, dynamic Skill Library source, or shared creation query.

### Toolbar and Inspector

Classic Canvas has a persistent top toolbar and multiple node-specific panels/modals. Smart Canvas has a central composer and node toolbars that appear with node state. MiniMax includes an internal timeline inspector.

There is no generic right-side Inspector that renders configuration from Node/Skill/Renderer metadata. Complex model and provider controls live inside node bodies or the Smart composer, contrary to the target “Canvas simple, Inspector deep” split.

### Minimap and semantic zoom

Both editors have working minimaps that show node bounds and viewport and allow navigation. Zoom affects the Canvas world transform.

There is no semantic zoom contract that changes representation at defined thresholds. Nodes remain structurally the same while the world scales, so very large graphs will become unreadable or expensive.

## Backend

### FastAPI application

`main.py` creates one FastAPI instance and contains almost all backend behavior. It serves static files and media, defines Pydantic request models, owns filesystem locks and in-memory queues, invokes remote APIs and subprocesses, and exposes all routes.

The application mounts:

- `/static` from `static/`;
- `/output` from `output/`;
- `/assets` from `assets/`.

The backend currently mixes domain policy, HTTP transport, persistence, protocol translation, process control, and file manipulation. The largest risk is not FastAPI itself; it is the absence of internal boundaries.

### API surface

The route surface includes:

- application update checks, downloads, rollback, and backups;
- storage settings and file deletion;
- uploads and media conversion/preview;
- local and shared-folder asset management;
- RunningHub application/workflow operations;
- Codex/Gemini/Jimeng CLI status and help;
- providers, model discovery, and provider connection tests;
- image, video, LLM, Midjourney, ModelScope, and ComfyUI generation;
- conversations, chat, Agent mode, and SSE streaming;
- projects and canvases;
- Canvas workflow import/export;
- asset and prompt libraries;
- ComfyUI instances and workflow configuration.

There is no `/api/v1` contract, domain-oriented Workbench API, generated API schema client, or separation between internal admin operations and project-user operations.

## Events and concurrency

### WebSocket

`/ws/stats` accepts unauthenticated clients. The in-memory `ConnectionManager` broadcasts:

- online client count;
- newly generated images;
- Canvas update invalidations;
- asset-library update invalidations;
- selected personal queue messages keyed by client ID.

Clients still fetch authoritative JSON after invalidation. This is a reasonable transitional pattern, but the connection manager is process-local and cannot support multiple API processes without an event bus.

### SSE

`/api/chat/stream` returns `text/event-stream` for model response deltas. Codex and Gemini CLI branches emit their completed text through the same SSE shape after the subprocess returns; they are not token-streamed from a durable Agent execution record.

### Polling and task state

Canvas clients poll metadata as a fallback. Image and ComfyUI task endpoints expose polling-based task state. The queue is held in process memory. A process restart can lose in-flight coordination even when upstream work continues.

There is no unified execution event schema, persistent job table, pause/resume state machine, approval event, or replayable audit stream.

## Agent and Codex

### Current Agent mode

The current chat Agent is an intent router with three actions:

- `chat`;
- `generate_image`;
- `edit_image`.

It uses an LLM JSON decision when available and heuristics as fallback, then calls the selected image or chat provider. It does not inspect the current Canvas, search Skills, propose a graph, request Canvas approval, call Workbench tools, or maintain task/plan/progress/tool-call state.

### Current Codex integration

Codex is registered as a provider protocol. The backend locates the local `codex` executable, runs `codex exec`, can pass local image paths, and can use a GPT Image helper. Codex chat execution receives a prompt and conversation history.

This makes Codex a worker/provider adapter today. There is no `CodexBridge`, App Server session abstraction, scoped Tool Runtime, Canvas selection API, or orchestration event bridge. Direct CLI details are spread through backend functions, so future Harness changes would touch product code without a boundary.

## Model and API providers

The provider configuration system supports OpenAI-compatible, APIMart, Gemini, Volcengine, RunningHub, Jimeng, Codex, Gemini CLI, ModelScope, and custom provider metadata. Provider records contain protocol, base URL, model lists, model name mappings, endpoints, and specialized settings.

Positive current behavior:

- Provider secrets are generally persisted in ignored `API/.env`, not in `data/api_providers.json`.
- `/api/providers` returns `has_key` and a masked preview rather than the full provider key.
- Nodes record a selected provider/model in multiple generation paths.
- Provider-specific behavior already has named helper functions that can become adapter implementations.

Gaps:

- There is no independent, canonical ModelRegistry with capability metadata.
- Provider, model, and feature dispatch are interleaved in Canvas and backend code.
- Compatibility is inferred from node/provider lists, not declared capabilities.
- Defaults and fallback behavior are duplicated.
- Phase 0 replaced the Legacy raw-token response with `{ "configured": boolean }` metadata.
- Phase 0 removed ModelScope browser-storage fallbacks and `api_key` request payloads from the Angle and Z-Image pages. Legacy request fields remain accepted but are ignored server-side.
- Masked key previews disclose part of a secret and are unnecessary for the target contract.

## ComfyUI and fixed execution nodes

ComfyUI support is extensive and reusable:

- multiple LAN instances;
- image upload to instances;
- bundled workflows and config field mappings;
- workflow upload, update, delete, and execution;
- prompt parameter mapping;
- history polling and output download;
- fixed Z-Image, Enhance, Klein, MiniMax, and custom workflow paths.

The limitation is architectural: Canvas nodes and backend functions know ComfyUI workflow names and provider-specific parameter shapes. The target should keep these functions behind a `ComfyUIAdapter` and expose them to Skills as capabilities, while retaining fixed nodes through Legacy adapters.

## Asset

Current Asset behavior includes:

- `assets/input`, `assets/output`, `assets/library`, and `assets/uploads` storage;
- configurable storage directories;
- drag/drop and browser uploads;
- asset libraries and categories in JSON;
- local asset folder operations;
- previews, image conversion, crop, caption, and classification;
- shared-folder registration and scanning;
- avatar/private-asset registration with external providers;
- Canvas asset indexing and workflow packages that may include media.

There are overlapping concepts: local uploads, generated output, asset-library items, Canvas media references, shared folders, prompt libraries, and generation history each have their own record conventions. Assets do not have one canonical `asset_id` plus immutable `asset_version_id`, project ownership, content hash, provenance, and access policy.

Static mounting makes stored assets directly addressable to anyone who can reach the server. Asset metadata is not permission-enforced.

## Knowledge

There is no separate Knowledge Service, Knowledge record, retrieval interface, embedding index, full-text index, structured query interface, scope model, or Knowledge snapshot.

Prompt libraries and asset classification are useful source features but are not a Knowledge domain. The absence is a clean opportunity to introduce the required separation rather than renaming the current asset library.

## Workflow

The word workflow currently refers to two related but distinct forms:

1. ComfyUI workflow JSON plus a UI configuration mapping under `workflows/`.
2. A selected Canvas subgraph exported or imported as JSON/ZIP and optionally stored in the asset library.

Classic and Smart Canvas can execute connected generation chains and loops. This is a useful graph execution precursor.

There is no canonical WorkflowDefinition/WorkflowVersion/WorkflowRun model, immutable graph version, pause/resume/retry contract, per-node execution record, approval checkpoint, composite Skill schema, or stale dependency propagation.

## Database and persistence

There is no relational database in the current repository. Persistence is JSON and local files guarded by process-local `threading.Lock` instances.

| Data | Current location | Notes |
|---|---|---|
| Projects | `data/projects.json` | Name/order/timestamps; Canvas count is derived |
| Canvases | `data/canvases/*.json` | Entire mutable graph per file |
| Conversations | `data/conversations/<user>/*.json` | Namespace chosen from header/IP, not authenticated identity |
| Provider metadata | `data/api_providers.json` | Runtime-created; absent in audited checkout |
| Provider secrets | `API/.env` | Ignored by Git; server and Legacy browser flows read it indirectly |
| Asset library | `data/asset_library.json` | Tracked seed/runtime file |
| Prompt libraries | `data/prompt_libraries.json` | Runtime JSON when present |
| Shared folders | `data/shared_folders.json` | Local path registrations |
| Workflows | `workflows/*.json` | Bundled and user-modifiable files |
| Generation history | `history.json` | Mutable list capped in code |
| Media | `assets/`, `output/` | Local filesystem |

Risks include non-atomic writes, weak recovery, process-local locking, whole-file contention, no migrations, no referential integrity, no transaction across metadata and files, and no efficient project-scoped query path.

SQLite is the appropriate first structured store, provided repositories and migrations allow PostgreSQL later. Binary files should remain outside database blobs.

## Authentication and permissions

There is no authentication middleware or session validation.

Conversation endpoints accept `X-User-ID`; if absent, the client IP becomes the namespace. The value is sanitized for a directory name, but possession of another ID is sufficient to address that namespace. This is not identity or authorization.

Projects and Canvases have no member table or permission checks. `owner` on a Canvas is display metadata. Owner, Editor, and Viewer roles are not implemented. All reachable clients can list, edit, delete, restore, and purge projects/Canvases and manage providers, files, updates, workflows, and shared folders.

## Security findings

### Critical

1. **No authentication or authorization:** all state-changing and destructive routes are callable by any client that can reach port 3000.
2. **Unauthenticated LAN compatibility mode:** an explicit `WORKBENCH_HOST=0.0.0.0` opt-in exposes all unauthenticated routes on the network.
3. **Administrative code-update routes are unauthenticated:** remote update and rollback can replace application files from a network request.

### High

1. **CORS lacks authenticated trust boundaries:** Phase 0 replaces wildcard origins with a local default and explicit allowlist, but all API routes remain unauthenticated.
2. **Public media mounts:** all files under mounted asset/output roots are addressable without project permission checks.
3. **Shared-folder and local-import capability:** unauthenticated endpoints can register/read local paths, increasing local-file exposure risk.
4. **Remote fetch/proxy surface:** several endpoints accept URLs and fetch or proxy them; consistent SSRF controls are not evident across the surface.
5. **Subprocess surface:** Codex, Gemini, Jimeng, ffmpeg, and helper tools run in the API process. Allowlist checks exist in some help endpoints, but there is no unified Tool Permission policy or audit trail.
6. **Upload trust:** size and extension checks exist in several paths, but content validation, malware policy, project quotas, and consistent safe extraction rules are incomplete.

### Medium

1. Phase 0 ignores local secrets, generated runtime records, media, previews, databases, and development caches; tracked seed/template boundaries still need review as persistence migrates.
2. Masked secret previews are returned to browsers.
3. WebSocket client IDs and online counts are unauthenticated and process-local.
4. Errors and debug `print` calls are widespread; a central redaction policy is absent.
5. JSON writes are not consistently write-temp, fsync, and atomic-replace operations.

No literal secret value was read during this audit. `API/.env` was checked only for presence/key names and was empty in the audited workspace.

## Technical debt

| Severity | Debt | Consequence |
|---|---|---|
| Severe | `main.py` owns nearly every backend concern | High regression risk and difficult test isolation |
| Severe | Two independent, very large Canvas implementations | Duplicate fixes, divergent behavior, difficult migration |
| Severe | Node type conditionals span create/render/connect/execute/storage | New capabilities require broad edits |
| Severe | No authentication/project authorization | Unsafe LAN/multi-user operation |
| High | JSON/filesystem records have no migration/version layer | Schema changes are implicit and hard to roll back |
| High | Provider adapters are not a registry contract | Model capability checks and user-selection rules are inconsistent |
| High | Agent means image intent router, not Workbench orchestrator | Target Codex workflows cannot be implemented safely on current boundary |
| High | Asset identity is URL/path-oriented | Version, provenance, permissions, and stale tracking are weak |
| High | No Knowledge domain | Industry knowledge cannot be scoped or snapshotted correctly |
| Low | Direct PyPI TLS handshakes can fail in this environment; the documented `uv --system-certs` mirror fallback installed the constrained dependency set and completed the test suite | Keep the fallback documented until direct PyPI is reliable |
| Medium | Runtime/source separation is now documented and ignored, but current JSON persistence still overlaps local source-adjacent paths | User state can still leak into releases if ignored paths are deliberately force-added |
| Medium | Manual DOM rendering and global state | UI boundaries and component tests are difficult |
| Medium | No semantic zoom | 100–300-node project readability is unproven |

## Reuse, refactor, and Legacy classification

### Reuse directly behind stable interfaces

- world/screen coordinate transforms;
- node drag, resize, pan, zoom, selection, grouping, minimap, and edge geometry;
- Canvas JSON load/save behavior and stale-write detection as a compatibility repository;
- asset upload, preview, crop, and media conversion primitives;
- ComfyUI instance/workflow execution primitives;
- provider HTTP request and response parsing helpers;
- RunningHub workflow discovery/execution helpers;
- Canvas workflow JSON/ZIP import/export mechanics;
- SSE formatting and WebSocket invalidation pattern;
- current browser-first deployment and static UI during the initial migration.

### Refactor progressively

- route registration and domain services out of `main.py`;
- Canvas state normalization and creation into shared services;
- render dispatch into NodeShell and RendererRegistry;
- provider/model metadata into ModelRegistry and provider adapters;
- assets into canonical records, versions, and repositories;
- Canvas graph execution into Workflow Runtime;
- chat/Codex subprocess integration behind CodexBridge;
- JSON persistence behind repository interfaces and migration tooling;
- iframe tool navigation toward Projects/Workbench/Resources without breaking Legacy pages.

### Preserve through Legacy adapters

Classic node kinds:

- `image`
- `prompt`
- `loop`
- `group`
- `promptGroup`
- `llm`
- `generator`
- `midjourney`
- `msgen`
- `video`
- `minimax`
- `rh`
- `comfy`
- `ltxDirector`
- `output`

Smart node kinds:

- `smart-image`
- `smart-prompt`
- `smart-loop`
- `smart-minimax`
- `smart-group`

Historical/imported generator type labels such as `zimage`, `enhance`, `klein`, `workflow-custom`, and `minimax-h3` also require fixture coverage where they appear in stored logs or workflow packages.

### Do not reuse as target contracts

- arbitrary node dictionaries without `schema_version`;
- browser-visible provider tokens;
- IP or client-supplied header as identity;
- provider names as Canvas business types;
- direct `nodes.push(<node>)` from every entry path;
- raw filesystem path as an Asset identity;
- chat conversation as project truth;
- in-memory queue as durable workflow execution state.

## Gap analysis

| Target capability | Current state | Gap |
|---|---|---|
| Generic Workbench Core | Tool-oriented monolith | Domain modules and pack boundary absent |
| NodeRecord | Unversioned dictionaries by Canvas type | Canonical schema, adapter, validation, versions absent |
| NodeShell | Repeated/interleaved node markup | Shared shell contract absent |
| RendererRegistry | Type conditionals | Registration and finite renderer manifests absent |
| SkillRegistry | No Workbench Skills | Discovery, validation, enable/disable/reload absent |
| ModelRegistry | Provider lists and node selectors | Capability metadata and compatibility filter absent |
| CanvasAPI | CRUD exists at whole-Canvas HTTP level | Stable node/edge/group domain commands absent |
| CodexBridge | Direct CLI provider calls | Harness abstraction, tools, events, approvals absent |
| Agent Panel | Chat page and busy bubble | Task/plan/progress/tool/approval UI absent |
| Asset Service | Several file/library systems | Canonical identity, version, project ownership absent |
| Knowledge Service | Not implemented | Entire domain and retrieval contract absent |
| Workflow Runtime | Canvas chains plus Comfy graphs | Version/run/pause/retry/approval runtime absent |
| Provenance | Partial logs/model fields | Formal immutable lineage absent |
| Outdated propagation | Not implemented | Dependency graph/version comparison absent |
| Approval/Frozen | Not implemented | State policy and human action absent |
| Industry Pack runtime | Not implemented | Pack discovery and WholeHouse package absent |
| Owner/Editor/Viewer | Display-only owner | Authentication, membership, enforcement absent |

## Baseline verification result

- `main.py` parsed successfully with the Python AST parser.
- `node --check static/js/canvas.js` passed.
- `node --check static/js/smart-canvas.js` passed.
- The discovered Node executable was `/Users/lo/.local/node-v24.20.0/bin/node`, version `v24.20.0`.
- The project `.venv` installed its constrained dependencies on macOS arm64 using `uv --system-certs` and the documented mirror fallback; no global Python was modified.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v` passed all 37 tests, including Canvas log/media, Legacy fixture, path containment, event contracts, secret-boundary redaction, exposure, and workflow archive round-trip checks.
- A local runtime smoke test on `127.0.0.1:3300` returned `local_only` exposure metadata from `/api/app-info` and HTTP 200 from the static entry point; the temporary process was stopped cleanly.

## Immediate conclusion

Phase 0 should freeze representative Legacy Canvas fixtures, create a reproducible test environment, close the raw-browser-secret path, narrow exposure defaults, and introduce module seams without changing behavior.

Phase 1 should introduce the canonical NodeRecord schema, Legacy adapters, centralized state vocabulary, and NodeCreationService behind compatibility flags. Existing node renderers and execution functions should remain in place until their adapter tests pass and the dynamic Skill Gate is ready.
