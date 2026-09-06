# R4 Unified Canvas — Runtime Ownership Matrix

> 本文件由 Codex 在本地项目执行 R4 时持续维护。
>
> 目标不是统计 shared helper，而是确认每一项产品 Runtime responsibility 的唯一 Owner。

## 状态定义

```text
UNIFIED      = Unified runtime 已拥有完整产品责任
PARTIAL      = 有 shared seam/helper，但 Legacy 仍拥有主流程
CLASSIC      = Classic 独立拥有
SMART        = Smart 独立拥有
COMPAT_ONLY  = 仅 Legacy compatibility 仍需要
REMOVE       = 可删除/待删除
```

---

## Ownership Matrix

| Responsibility | Classic | Smart | Unified | Status | Final owner | Required action | Evidence |
|---|---|---|---|---|---|---|---|
| Canvas entry | compatibility handoff | compatibility page | `canvas.html` | PARTIAL | Unified | Remove retained Smart deep-link handoff after Smart record rendering is native. | `canvas-entry-compatibility.js`; status U6 |
| Canvas persistence | adapter client | adapter client | SQLite `CanvasRecord` | UNIFIED | Unified | Keep Legacy JSON only as import/rollback. | status R3/R4 acceptance |
| revision/CAS | none | none | API/application service | UNIFIED | Unified | Maintain conflict coverage. | `tests/test_canvas_nodes_runtime.py` |
| remote/version polling | interval/merge policy | interval/merge policy | transport-neutral coordinator only | PARTIAL | Unified | Move polling policy/state into the product runtime. | `canvas-remote-sync.js`; save/merge characterization below |
| viewport state | page state + runtime mirror; default fit/recovery commits use runtime | page state + runtime mirror; default fit/recovery commits use runtime | `CanvasRuntime` policy/mirror | PARTIAL | Unified | Make one runtime state authoritative. | `canvas.js`, `smart-canvas.js`, `runtime-state.js`; fit/recovery contract |
| pan | page DOM/save shell; shared viewport pan session on default path | page DOM/save shell; shared viewport pan session on default path | CanvasRuntime command plus shared pan session | PARTIAL | Unified | Migrate remaining DOM/persistence lifecycle. | `runtime-state.js`; pan-session contract |
| zoom | page preview/minimap shell; shared wheel-scale, centering and default preview-exit commits | page preview/minimap shell; shared wheel-scale, centering and default preview-exit commits | CanvasRuntime command plus shared viewport policy | PARTIAL | Unified | Migrate remaining DOM/minimap/persistence lifecycle. | `runtime-state.js`; viewport interaction contracts |
| semantic zoom | adapter application | adapter application | shared policy | PARTIAL | Unified | Move DOM application into Unified renderer. | `semantic-zoom.js` |
| selection | page state machine, except NodeShell and box-selection completion | page state machine, except NodeShell/box completion, media-thumbnail, upload-target and group-menu selection | runtime command primitive plus migrated completion transitions | PARTIAL | Unified | Migrate remaining selection lifecycle. | `runtime-state.js`; NodeShell/box/media-thumbnail/upload-target/group-menu contracts |
| multi-selection | page state machine | page state machine | runtime command primitive | PARTIAL | Unified | Migrate selection lifecycle. | same |
| drag | page state machine | page state machine | NodeShell intent only | PARTIAL | Unified | Migrate drag lifecycle. | NodeShell intent adapters |
| resize | page state machine | page state machine | NodeShell intent only | PARTIAL | Unified | Migrate resize lifecycle. | NodeShell intent adapters |
| keyboard handling | page handlers | page handlers | editable-target helper | PARTIAL | Unified | Migrate key command lifecycle. | `interaction-targets.js` |
| connection start | page port drag | page port drag | shared command/geometry | PARTIAL | Unified | Migrate port-drag lifecycle. | `graph-interaction.js` |
| connection hover | page hover logic | page hover logic | compatibility helper | PARTIAL | Unified | Migrate hover lifecycle. | status U2 |
| port compatibility | adapter invocation | adapter invocation | shared compatibility contract | PARTIAL | Unified | Route one interaction runtime through it. | `port-compatibility.js` |
| connection mutation | GraphMutationService/API for supported connected Group/Image/Prompt/default Loop creation; page mutation otherwise | GraphMutationService/API for supported connected creation; page mutation otherwise | GraphMutationService/API available | PARTIAL | Unified | Migrate normal connect to service. | graph API tests; save/merge characterization below records the side-effect blocker |
| graph geometry | adapter invocation | adapter invocation | shared geometry algorithms | PARTIAL | Unified | Move graph lifecycle owner. | `graph-geometry.js` |
| group membership | adapter mutation | adapter mutation | shared membership algorithms | PARTIAL | Unified | Migrate group interaction owner. | `group-membership.js` |
| group move | page behavior | page behavior | none | CLASSIC/SMART | Unified | Migrate after shared drag owner exists. | adapter drag code |
| group render | Classic DOM | Smart DOM | partial NodeShell adapter | PARTIAL | Unified | Finish shared renderer before page deletion. | NodeShell mounts |
| node shell | adapter supplies records/intent | adapter supplies records/intent | NodeShell/host | PARTIAL | Unified | Make Unified renderer select and mount all normal cards. | `unified-render-host.js` |
| renderer resolution | Classic policy projection | Smart policy projection | RendererRegistry/host plus RendererAdmission | PARTIAL | Unified | Unified evaluates declared admission; retain page product policy until card parity is explicit. | `renderer-admission.js`; frontend renderer-admission contract |
| generic node rendering | Legacy DOM | Legacy DOM | lossless Legacy renderer | PARTIAL | Unified | Migrate product-relevant card renderers. | `legacy-renderer.js` |
| media rendering | adapter mount/lifecycle | adapter mount/lifecycle | MediaRenderer | PARTIAL | Unified | Move mount/lifecycle ownership. | `media-renderer.js` |
| media lifecycle | adapter re-render/transplant | adapter re-render/transplant | playback helpers | PARTIAL | Unified | Move re-render lifecycle. | `media-playback-state.js` |
| media playback preservation | adapter invocation | adapter invocation | shared state contract | PARTIAL | Unified | Fold into Unified media lifecycle. | `media-playback-state.js` |
| creation catalog | menu adapter | menu adapter | command/catalog definitions | PARTIAL | Unified | Replace page constructors for normal creation. | `command-registry.js` |
| node creation | fallback constructors for unsupported/historical and file-drop paths; shared top-level/connected result commits | fallback constructors for unsupported/historical and file-drop paths; shared top-level/connected result commits | NodeCreationService/GraphMutationService APIs plus shared node/graph result commits | PARTIAL | Unified | Migrate file-drop lifecycle and remaining adapter request projection; retain only bounded compatibility. | `node-creation-client.js`; default-on/Smart-shape/node-and-graph-result contracts |
| node deletion | versioned mutation for standalone blank Image/Prompt/default Loop/empty Output/empty Group; compatibility for configured/content/connected/group-member/other nodes | versioned mutation for standalone blank Smart Image/Prompt/empty Smart Group/default Smart Loop; compatibility for media/group/history/dependent nodes | NodeMutationService/API | PARTIAL | Unified | Migrate remaining deletion contracts only after group/media parity is explicit. | Canvas-node route tests; Classic/Smart versioned-delete contracts |
| node mutation | versioned position update for standalone blank Image/Prompt/default Loop/empty Output/empty Group; compatibility for configured/richer/group-member moves/edits | versioned position update for standalone blank Smart Image/Prompt/empty Smart Group/default Smart Loop; compatibility for richer moves/edits | NodeMutationService/API with backend blank-shape enforcement | PARTIAL | Unified | Migrate resize/group/media and other edit contracts only after parity is explicit. | Canvas-node route tests; Classic/Smart versioned-position contracts; backend unsupported-shape rejection contract |
| context-menu creation | fallback constructors for unsupported/group-member paths; shared top-level and connected result commits | fallback constructors for group-member paths; shared top-level and connected result commits | catalog/API plus shared node/graph result commit for migrated top-level and connected creation | PARTIAL | Unified | Centralize remaining page request projection; retain only bounded compatibility. | `node-creation-client.js`; node-and-graph-result contract |
| file-drop creation | adapter media/layout/save; shared DataTransfer and upload transport | adapter media/layout/save; shared DataTransfer and upload transport | shared DataTransfer traversal/payload resolution/multipart upload; adapter-owned result materialization | PARTIAL | Unified | Migrate result materialization only after media/group parity is explicit. | `media-drop-payload.js`; payload-and-upload contract |
| clipboard copy | adapter selection/UI | adapter selection/UI | graph fragment + clipboard helper | PARTIAL | Unified | Move selection/UI lifecycle. | `canvas-clipboard.js` |
| clipboard paste | adapter placement/UI | adapter placement/UI | graph fragment + clipboard helper | PARTIAL | Unified | Move placement/UI lifecycle. | `canvas-graph-fragment.js` |
| selected subgraph | adapter selection | adapter selection | graph fragment | PARTIAL | Unified | Move selection lifecycle. | same |
| workflow import | adapter format/UI | adapter format/UI | transfer client + graph fragment | PARTIAL | Unified | Retain format compatibility; migrate product flow. | `workflow-transfer-client.js` |
| workflow export | adapter format/UI | adapter format/UI | transfer client | PARTIAL | Unified | Retain format compatibility; migrate product flow. | same |
| result normalization | Classic traversal policy | Smart traversal policy | shared normalizer | PARTIAL | compatibility until R8 | Keep provider behavior; continue compatibility-only decoupling. | `media-result-normalizer.js` |
| result placement | adapter behavior | adapter behavior | generation intent seam | PARTIAL | compatibility seam | Do not introduce R8 executor runtime. | `generation-intent.js` |
| execution trigger | adapter/provider behavior | adapter/provider behavior | none | CLASSIC/SMART | compatibility until R8 | Keep compatibility-only in R4. | adapters |
| minimap | page DOM/event/save shell; shared pointer projection and world-point viewport centering on default path | page DOM/event/save shell; shared pointer projection and world-point viewport centering on default path | CanvasRuntime command plus shared minimap projection/viewport-centering policy | PARTIAL | Unified | Migrate remaining render/persistence lifecycle. | `runtime-state.js`; minimap interaction contract |
| screen-space controls | n/a | Smart application | shared policy | PARTIAL | Unified | Move DOM application with renderer ownership. | `screen-space-controls.js` |
| normal navigation | retained entry adapter | retained entry adapter | normal URL resolver | PARTIAL | Unified | Remove Smart branch when records render natively. | `canvas-entry-compatibility.js` |
| Smart handoff | initiates retained handoff | destination runtime | compatibility module | COMPAT_ONLY | REMOVE | Remove only after Smart product runtime is retired. | status U6/U7 |
| Classic product runtime | full adapter | n/a | partial shared seams | CLASSIC | REMOVE | Migrate interaction, creation and render lifecycle. | `canvas.js` |
| Smart product runtime | n/a | full adapter | partial shared seams | SMART | REMOVE | Migrate Composer, group/media lifecycle, interaction and creation. | `smart-canvas.js` |

---

# Legacy Capability Review

## Classic-only

| Capability | Keep/Migrate/Compat/Remove | Target | Evidence |
|---|---|---|---|
| Legacy provider/execution cards | Compat | bounded Legacy renderer/execution seam | provider behavior unchanged; R8 owns runtime replacement |
| Classic upload/file-drop | Migrate | Unified creation/mutation runtime | direct local node construction remains page-owned |

## Smart-only

| Capability | Keep/Migrate/Compat/Remove | Target | Evidence |
|---|---|---|---|
| Composer | Migrate | Unified card/render and creation runtime | `updateComposer()` remains Smart-page-owned |
| Smart group behavior | Migrate | Unified interaction/renderer | Smart membership/move/resize policy remains page-owned |
| upload | Migrate | Unified creation/mutation runtime | Smart direct `createNode()` remains page-owned |
| video workflow | Compat | Legacy renderer/execution seam | R8 owns runtime replacement |
| Smart media layout | Migrate | Unified media renderer lifecycle | layout math is shared; DOM lifecycle remains Smart-owned |
| MiniMax compatibility | Compat | Legacy renderer/execution seam | must remain readable; not an R8 implementation |

---

# Feature Flag Lifecycle

| Flag | Introduced | Purpose | Current default | Removal gate | Status |
|---|---|---|---|---|---|
| versioned_nodes | R3/R4 | canonical normal blank creation rollback | on | R4 PASS | `versioned_nodes=0` retains adapter constructors during U7 |
| unified_canvas | R2/R4 | bounded U7 rollback | on | R4 PASS | retain until one runtime evidence |
| node_shell | R3/R4 | bounded U7 rollback | on | R4 PASS | retain until one renderer evidence |
| legacy_renderer | R3/R4 | bounded Legacy payload renderer rollback | on | R4 PASS | retain until migrated card parity |
| media_renderer | R3/R4 | bounded media renderer rollback | on | R4 PASS | retain until lifecycle parity |
| semantic_zoom | R3/R4 | bounded semantic zoom rollback | on | R4 PASS | retain until renderer ownership |
| screen_space_controls | R3/R4 | bounded Smart controls rollback | on | R4 PASS | retain until renderer ownership |

---

# Acceptance Evidence

## Unit / contract

```text
2026-09-05 inventory baseline: python -m unittest tests.test_frontend_workbench_modules
PASS (76 tests). This characterizes shared-module seams only; it is not R4 Gate evidence.

2026-09-05 normal blank-creation authority cutover: loopback defaults to the existing `NodeCreationService` route for supported Classic and Smart top-level commands; `versioned_nodes=0` is the bounded rollback. `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_frontend_workbench_modules tests.test_canvas_nodes_runtime`: PASS (89 tests).

2026-09-05 NodeShell selection ownership: Classic NodeShell select/focus/menu now dispatches through `CanvasRuntime` on the default path, with local state only as the `unified_canvas=0` rollback. `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -q`: PASS (241 tests).

2026-09-05 box-selection ownership: both adapters retain their existing coordinate/overlap policy, then commit completed selection through `CanvasRuntime` on the default path; `unified_canvas=0` retains the local state fallback. Focused API/frontend regression: PASS (90 tests); full regression: PASS (242 tests).

2026-09-05 Classic standalone blank-Image deletion: the default loopback path calls `NodeMutationService`; successful API response projects the revision locally, while stale/rejected requests do not fall through to a raw adapter save. Focused regression: PASS (103 tests); full regression: PASS (243 tests).

2026-09-06 Classic standalone blank-Image position: a single non-Alt, non-grouped blank Image drag calls `NodeMutationService` on completion; stale/rejected writes restore its original visual position and do not issue a raw Canvas save. Focused regression: PASS (104 tests); full regression: PASS (244 tests).

2026-09-06 Smart standalone blank-Image deletion: the default loopback path calls `NodeMutationService` only for an ungrouped, media-free, idle `smart-image` without history or dependent input references. The repository preserves Smart's `title` field; stale/rejected requests do not fall through to a raw adapter save. Focused regression: PASS (106 tests); full regression: PASS (246 tests).

2026-09-06 Smart standalone blank-Image position: a single non-Alt/non-Ctrl, non-thumbnail-drag, non-grouped blank Smart Image drag calls `NodeMutationService` on completion; rejected or stale writes restore its original visual position and do not issue a raw Canvas save. Focused regression: PASS (107 tests); full regression: PASS (247 tests).

2026-09-06 Smart blank-Image creation projection: the Legacy persistence adapter writes a NodeCreationService-created Image as `smart-image` with Smart `title` and empty `images` when the target Canvas is Smart. Reload no longer depends on local type projection for this normal creation path. Focused regression: PASS (108 tests); full regression: PASS (248 tests).

2026-09-06 Smart connected creation transaction: supported connected Image/Group/Prompt/Loop/MiniMax creation persists its new node, edge, and target `inputNodeIds` in the one GraphMutationService transaction. The local projection no longer schedules a raw Canvas save after that successful API response. Focused regression: PASS (104 tests); full regression: PASS (248 tests).

2026-09-06 Classic connected blank-Image creation: the normal supported Classic Image connection now creates the blank Image and edge through GraphMutationService, using the same transaction-persisted input relationship and no raw Canvas save. Focused regression: PASS (106 tests); full regression: PASS (250 tests).

2026-09-06 Smart Canvas-node route coverage: the mounted local API creates the durable Smart Image shape and updates/deletes it through the same expected-revision contract. Focused regression: PASS (116 tests); full regression: PASS (252 tests).

2026-09-06 shared pan interaction: Classic and Smart default paths delegate pointer delta, viewport origin and their preserved movement threshold (Classic Euclidean, Smart Manhattan) to `WorkbenchCanvasRuntime.createViewportPanSession`; `unified_canvas=0` retains the page-local calculation. Focused regression: PASS (103 tests); full regression: PASS (253 tests).

2026-09-06 shared zoom interaction: Classic and Smart default wheel paths delegate scale calculation to `WorkbenchCanvasRuntime.viewportScaleForWheel`, preserving Classic's step factors and Smart's clamped exponential policy; `unified_canvas=0` retains the page-local formula. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 minimap viewport-centering interaction: Classic and Smart default minimap paths delegate the world-point-to-centered-viewport calculation and `CanvasRuntime` viewport command to `WorkbenchCanvasRuntime.viewportCenteredOnWorldPoint`; their minimap DOM, event binding and save lifecycles remain page-owned, while `unified_canvas=0` retains the page-local formula. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 minimap pointer projection: Classic and Smart default minimap paths delegate client-pointer-to-world-point projection to `WorkbenchCanvasRuntime.worldPointFromMinimapPointer`, retaining each adapter's bounds, offsets and scale inputs; their minimap DOM, event binding and save lifecycles remain page-owned, while `unified_canvas=0` retains the page-local formula. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 fitted/recovered viewport commit: Classic's shared recovery fit and Smart's normal, corrupt-camera and visible-node recovery fits now dispatch their resulting viewport through CanvasRuntime by default. Adapter-specific fit inputs/fallbacks, recovery eligibility, DOM application and persistence remain page-owned; `unified_canvas=0` retains direct assignment. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 zoom-preview exit viewport commit: Classic and Smart default preview exits, including readable node focus, compute their retained preview-specific scale and then restore/center through CanvasRuntime. Preview mode, adapter scale rules, DOM application and persistence remain page-owned; `unified_canvas=0` retains direct assignment. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 Smart media-thumbnail selection: Smart's media thumbnail single-click and preview/double-click selection paths now commit their node selection through `applySmartNodeSelection` and CanvasRuntime by default. Smart retains its media focal item, preview, Composer and video behavior; `unified_canvas=0` retains direct selection state. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 Smart upload-target selection: Smart's node upload entry now commits its target-node selection through `applySmartNodeSelection` and CanvasRuntime by default before opening the existing file picker. Upload target, file picker, media focal state and Composer behavior remain adapter-owned; `unified_canvas=0` retains direct selection state. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 Smart group-menu selection: Smart's group right-click menu now commits its target-node selection through `applySmartNodeSelection` and CanvasRuntime by default before opening the existing group menu. Group/menu/creation behavior remains adapter-owned; `unified_canvas=0` retains direct selection state. Focused regression: PASS (98 tests); full regression: PASS (253 tests).

2026-09-06 blank-Image creation result commit: Classic and Smart default blank-Image menu creation now route the API success result through `WorkbenchNodeClient.applyCreationResult`, which appends the projected node, records the undo snapshot and applies the authoritative Canvas revision. Adapters retain their distinct node shape, Smart selection and render feedback; unsupported/group-member creation remains compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 blank-Prompt creation result commit: Classic and Smart default blank-Prompt menu creation now use the same `WorkbenchNodeClient.applyCreationResult` commit. The shared path owns append/undo/revision; adapters retain their Prompt card shape, Smart selection and render feedback, while connected/group-member and unsupported creation remain compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 blank-Loop creation result commit: Classic and Smart default blank-Loop menu creation now use that same shared success-result commit. The shared path owns append/undo/revision; adapters retain Loop card shape, Smart selection and render feedback, while connected/group-member and unsupported creation remain compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 blank-Group creation result commit: Classic and Smart default blank-Group menu creation now use that same shared success-result commit. The shared path owns append/undo/revision; adapters retain their group card shape, Smart selection and render feedback, while group-member editing, connected creation and media behavior remain compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 Classic blank-Output creation result commit: Classic default blank-Output menu creation now uses `WorkbenchNodeClient.applyCreationResult`. The shared path owns append/undo/revision; Classic retains Output card shape and render feedback, while connected creation and unsupported paths remain compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 Smart blank-MiniMax creation result commit: Smart default MiniMax menu creation now uses `WorkbenchNodeClient.applyCreationResult`. Its adapter-owned node projection still initializes the existing timeline segment before the shared append/undo/revision/selection commit; all MiniMax media, timeline and execution interaction remains compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 connected creation result commit: Classic connected Group/Image and Smart connected Group/Prompt/Loop/Image/MiniMax now route their already-atomic GraphMutationService result through `WorkbenchNodeClient.applyGraphCreationResult`. The shared path validates/projects the node and edge, commits node/edge/undo/revision/selection, and (where requested) updates the graph's generic input relationship. Adapters retain only card projection, Classic post-connection sync, and Smart product feedback; file-drop, unsupported and group-member creation remain compatibility. Focused regression: PASS (99 tests); full regression: PASS (254 tests).

2026-09-06 connected-result browser read smoke: local `127.0.0.1:3000` loaded the existing Classic fixture with six nodes and `100% · 完整 · 6 节点`, and the historical Smart fixture with Group/Input/Output ports, upload and Prompt cards and `65% · 摘要 · 2 节点`. The check was read-only: no creation, save or execution was invoked.

2026-09-06 file-drop traversal ownership: Classic and Smart now delegate DataTransfer directory traversal and supported-file filtering to `WorkbenchCanvasMediaDrop`. Their upload endpoints, media type handling, target selection, group layout and Canvas save scheduling remain adapter-owned. Focused regression: PASS (100 tests); full regression: PASS (255 tests).

2026-09-06 file-drop browser read smoke: local `127.0.0.1:3000` loaded both existing fixtures with the new media-drop runtime script order. Classic retained six ready cards and `100% · 完整 · 6 节点`; Smart retained Composer and `65% · 摘要 · 2 节点`. The check was read-only: no upload, creation, save or execution was invoked.

2026-09-06 file-drop payload resolution: Classic and Smart now delegate files/directories/local paths/remote URL payload precedence to `WorkbenchCanvasMediaDrop`; Classic retains its existing directory-fallback eligibility. Upload API, media policy, target selection, group layout and Canvas save remain adapter-owned. Focused regression: PASS (100 tests); full regression: PASS (255 tests).

2026-09-06 file-drop payload browser read smoke: local `127.0.0.1:3000` loaded both fixtures using the new payload-resolution script version. Classic retained its six ready cards and `100% · 完整 · 6 节点`; Smart retained Composer, Group/Input/Output, upload and Prompt cards, and `65% · 摘要 · 2 节点`. The check was read-only: no upload, creation, save or execution was invoked.

2026-09-06 file-drop upload transport: Classic and Smart now delegate `/api/ai/upload` multipart transport and response file-list extraction to `WorkbenchCanvasMediaDrop`. Classic retains its existing JSON failure semantics; Smart retains named multipart files, readable error text and media-kind projection. Adapter-owned media handling, target selection, group layout and Canvas save remain unchanged. Focused regression: PASS (100 tests); full regression: PASS (255 tests).

2026-09-06 file-drop upload browser read smoke: local `127.0.0.1:3000` loaded both fixtures using the shared upload-transport script version. Classic retained its six ready cards and `100% · 完整 · 6 节点`; Smart retained Composer, Group/Input/Output, upload and Prompt cards, and `65% · 摘要 · 2 节点`. The check was read-only: no upload, creation, save or execution was invoked.

2026-09-06 Classic standalone blank-Prompt mutation: the Legacy mutation repository now accepts the durable `prompt` shape. A Classic Prompt with empty text, no links and no group membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Content-bearing, connected or grouped Prompts remain compatibility. Focused regression: PASS (116 tests); full regression: PASS (257 tests).

2026-09-06 Classic blank-Prompt browser read smoke: local `127.0.0.1:3000` loaded the existing Classic fixture using the new mutation script version, retaining six ready cards and `100% · 完整 · 6 节点`. The check was read-only: no Prompt move/delete, save or execution was invoked.

2026-09-06 Classic standalone default-Loop mutation: the Legacy mutation repository now accepts the durable `loop` shape. Only a Classic Loop with its default serial/count/start/batch configuration, no prompt or media inputs, no links and no group membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Configured, connected or grouped Loops remain compatibility. Focused regression: PASS (118 tests); full regression: PASS (259 tests).

2026-09-06 Classic standalone empty-Output mutation: the Legacy mutation repository now accepts the durable `output` shape. Only a Classic Output with no images, pending tasks, comparison state, links or group membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Output clearing, execution results, configured, connected or grouped Outputs remain compatibility. Focused regression: PASS (120 tests); full regression: PASS (261 tests).

2026-09-06 Classic standalone empty-Group mutation: the Legacy mutation repository now accepts the durable `group` shape. Only a Classic Group with no members, links or nesting membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Group-member movement, membership changes, resize and graph behavior remain compatibility. Focused regression: PASS (122 tests); full regression: PASS (263 tests).

2026-09-06 Smart standalone empty-Group mutation: the Legacy mutation repository now accepts the durable `smart-group` shape. Only a Smart Group with no members, media, input references, links or nesting membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Smart group media, history, membership, resize and Composer behavior remain compatibility. Focused regression: PASS (124 tests); full regression: PASS (265 tests).

2026-09-06 Smart standalone default-Loop mutation: the Legacy mutation repository now accepts the durable `smart-loop` shape. Only a single-round serial Smart Loop with no prompt/image input, variable prompt, input references, links or group membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Workflow, connected, grouped and configured Smart Loops remain compatibility. Focused regression: PASS (20 adapter tests); full regression: PASS (266 tests).

2026-09-06 Smart standalone blank-Prompt mutation: the Legacy mutation repository now accepts the durable `smart-prompt` shape. Only a Smart Prompt without text/result, stale-result marker, LLM activation/instruction, attachments, input references, links or group membership updates position or deletes through NodeMutationService; rejected writes do not fall through to raw save. Content-bearing, connected, grouped and configured Prompts remain compatibility. Focused regression: PASS (111 tests); full regression: PASS (272 tests).

2026-09-06 Classic connected blank Prompt/default Loop creation: normal port-menu creation now persists the new node, edge and target input relationship through one GraphMutationService transaction. The page retains only node projection and post-connection compatibility refresh; provider/execution nodes and configured paths remain adapter-owned. Focused API/frontend regression: PASS (16 API tests); full regression: PASS (274 tests).
```

### 2026-09-06 backend mutation safety boundary and canonical data repair

```text
2026-09-06 backend blank-shape mutation boundary: the Legacy mutation repository no longer trusts the
frontend eligibility gate. Inside the same canvas lock that performs the mutation, it now rejects
content-bearing, grouped, history-linked, input-referenced, and (except the characterized Image edge
cleanup) connected nodes for both update and delete with `NodeMutationUnsupportedError`
(`unsupported_node_shape`, HTTP 422), while stale revisions still fail with 409 and supported blank
shapes keep their existing contracts. New adapter tests cover rich update/delete rejection, group-member
rejection, dependent-input-reference rejection, connected-Prompt rejection, adapter-level stale
rejection, and unchanged blank contracts; a route test pins the 422 mapping and the unchanged payload.
Focused regression: PASS; full regression: PASS (280 tests). Python AST (33 files) and JS syntax checks
pass. This closes the audited gap where a direct API caller could delete a group-linked, referenced, or
content-bearing node because the repository gated only on `node.type`.

2026-09-06 canonical data-integrity repair: a legacy-routed (rollback) server session on 2026-09-06
morning produced a verified split-brain — one orphan Canvas (`b489247e…`, created 07:41 through the
versioned API with JSONL audit evidence) existed only in Legacy JSON, sixteen active Canvases carried
list-board position drift, and the SQLite `canvases` table contained a `revision`/`baseline` row leaked
by an older `tests/test_repository_baseline.py` run before that test gained its routing patch. Repair:
pre-repair snapshot `data/canvas-source-backups/r4-repair-20260906T091748/` (23 payload files plus the
purged row's recovered JSON), the stale `7ed83bf5…` rollback file was refreshed from its newer canonical
payload, the orphan and board-only drifts were converged through the tested migration import path
(`tools/migrate_project_canvas.py`), and the test-artifact row was purged through
`purge_canvas_payload` with audit. Post-repair report `data/r4-repair-migration-report.json`: authority
`sqlite`, 23 imported, 0 skipped, 23 comparisons, 0 differences; SQLite rows 23 == Legacy files 23 with
zero divergent payloads and the orphan's two nodes present. R4 Gate items
`source_count == canonical_count` / `skipped == 0` / `differences == 0` are re-established as of this
repair; the general prohibition on running legacy-routed servers while SQLite authority is active is
recorded in CURRENT_EXECUTION_STATUS.md. An isolated restart read on `127.0.0.1:3012` then listed 17
active Canvases with no phantom `baseline` row, read the imported orphan with its two nodes and merged
board position, and read the repaired Classic record's canonical metadata; the temporary service was
stopped after the read-only check.

2026-09-06 SQLite-path mutation boundary coverage: the same blank-shape update/delete contracts,
`unsupported_node_shape` rejection (content-bearing and grouped nodes), and stale-revision rejection now
have focused tests through the `SqliteCanvasCompatibilityRepository`, pinning that the backend boundary
holds identically on the canonical store rather than only on the Legacy JSON path. Focused regression:
PASS (8 tests); full regression: PASS (283 tests).

Assessed and deferred (2026-09-06): normal-connect service migration remains blocked because both
adapters couple the edge commit with page-owned side effects on the same raw save (Smart mutates target
execution config and `inputNodeIds`; Classic adds group membership and generator/output sync), so a
service split today would force double writes or a premature rich-mutation API. Keyboard command
lifecycle migration is likewise deferred: the two adapters own genuinely different command maps and
selection models, so unification requires the command-registry step, not a bounded move. Polling
interval/eligibility ownership is blocked on the save/merge machinery unification. No ownership was
reduced by these assessments; they are recorded to prevent re-deriving the same blockers.
```

# Save/merge machinery characterization (U7 blocker analysis, 2026-09-06)

This table characterizes the two adapter save state machines that block the polling, normal-connect,
and viewport ownership rows. It is the prerequisite for one shared save coordinator; it does not itself
migrate ownership.

| Concern | Classic (`canvas.js`) | Smart (`smart-canvas.js`) |
|---|---|---|
| Debounce | `scheduleSave` 500 ms | `scheduleSave` 450 ms |
| Dirty tracking | `localCanvasDirty` flag gates 409 recovery and remote apply deferral | none; any scheduled save sends the full current payload |
| In-flight coalescing | `savingCanvasNow` + `saveCanvasAgain` re-run loop | `canvasSyncInFlight` guard only |
| Payload projection | `serializableCanvasNodes()` | `canvasForStorage()` (media/run-settings stripping, settings projection, prompt-draft flush) |
| Base revision source | `lastCanvasUpdatedAt` (separate mirror; versioned writes update both it and `canvas.updated_at`) | `canvas.updated_at` directly (single source) |
| 409 conflict policy | dirty → adopt remote revision and retry; clean → replace-apply remote canvas | merge server canvas (node-list merge, image union, connection merge) then re-save after 300 ms — neither side is dropped |
| Remote-apply semantics | `applyRemoteCanvasData`: whole-canvas replace preserving local viewport + selection; deferred 1 s while dirty/saving | `applyMergedServerCanvas`: merge into local state, adopt title/revision, re-save if local cleanup recovered state; deferred 600 ms while dragging/selecting |
| Remote-read sync | `syncRemoteCanvasNow`: replace if remote >= local | `mergeReloadCanvasNow`: merge, with drag/selection deferral |
| Remote-sync poll eligibility | `!applyingRemoteCanvas && !document.hidden`, 2.5 s | `!canvasSyncInFlight && !dragState && !selectionState`, 8 s |
| WS update-message path | shared filter → cancel pending save timer, replace-apply | shared filter → skip while in-flight, schedule merge reload |

Design consequence: the two machines share debounce/coalescing/revision-bookkeeping/transport shape but
disagree on the two hard parts — conflict resolution (replace vs merge-union) and remote application.
The unified seam must therefore own scheduling, coalescing, dirty lifecycle, one authoritative revision
mirror, and 409 detection, while delegating conflict resolution and remote application to adapter-supplied
policies until the node-list merge semantics become a shared characterized module. Unifying Classic's
dual revision mirror onto the single authoritative revision is part of that seam's first migration unit.
Classic's replace semantics additionally depend on preserving local viewport and selection, which remain
page-owned state until the viewport row migrates.

Migration order derived from this table (each unit is independently testable with `unified_canvas=0`
rollback): (1) one revision-mirror owner; (2) shared schedule/debounce/coalesce/in-flight coordinator
with adapter payload projection; (3) shared 409 detection with adapter conflict policy; (4) shared
remote-apply scheduling with adapter apply policy; (5) only then, polling eligibility and normal-connect
commit can move without double writes.

Migration unit (1) complete (2026-09-06): `WorkbenchCanvasPersistence.adoptRevision` now owns the
versioned-write revision adoption chain (positive server revision, else keep current, else explicit
fallback). All 26 adoption sites delegate to it — Classic's 10 paired position/delete sites and 8
`onRevision` creation commits (which keep `lastCanvasUpdatedAt` and `canvas.updated_at` coherent through
the single owner), plus Smart's 4 position and 4 delete sites with their preserved per-site fallbacks
(`Date.now()` for position, `0` for delete). A sandbox test pins the adoption chain and source assertions
pin the exact call counts; JS syntax and the full regression (284 tests) pass. Read-only mutation-path
browser evidence is deferred to unit (2), which touches the save scheduling those paths exercise.

Migration unit (2) complete (2026-09-06): `WorkbenchCanvasSaveScheduler`
(`canvas-save-scheduler.js`, loaded by both editor pages before each adapter) now owns debounce,
in-flight coalescing, retry marking, cancel, and the in-flight observers. Classic's
`savingCanvasNow`/`saveCanvasAgain`/`saveTimer` and Smart's `canvasSyncInFlight`/`saveTimer` are removed;
adapters keep only payload projection, conflict policy (Classic replace/defer, Smart merge-and-resave),
dirty flag, and DOM/status effects, and commit through `schedule`/`flush`/`cancel`/`markAgain`. Classic
runs with coalescing (`allowOverlap` off, exact prior semantics including the 409 retry-with-dirty path
via `onRetry`); Smart runs with `allowOverlap: true`, preserving its characterized concurrent-save
behavior while its merge guards now read the shared in-flight state (whose window is marginally wider:
it starts at flush entry rather than after payload preparation). Characterized side fix: Classic's
`applyRemoteCanvasData` deferral condition read a stale `saveTimer` handle (never cleared after a
debounced fire except by a WS update message), so after any local save the poll-driven remote application
deferred forever in a 1-second reload loop; the scheduler's real `hasScheduled()` replaces it. Sandbox
tests cover debounce, coalesced retry (with `onRetry`), overlap mode, cancel, and the observers; source
assertions pin script order and the removal of all legacy state variables. Full regression: PASS (285
tests). Remaining in this seam: unit (3) shared 409 detection, unit (4) shared remote-apply scheduling.

Browser write smoke for units 1–2 (read-isolated, `127.0.0.1:3013`, process-local temporary data
directory, 2026-09-06): the Classic editor booted with all edited wiring (NodeShell-ready page,
`100% · 完整 · 0 节点`), a context-menu 上传节点 creation went through the versioned NodeCreationService
route, the page's revision mirror adopted the server revision (`lastCanvasUpdatedAt` ==
persisted `updated_at` == 1788661517529), the created `image` node with its idempotency request id was
found in the isolated canvas payload after reload (`100% · 完整 · 1 节点`, NodeShell-ready Image card),
and no runtime wiring errors surfaced. The in-editor back-navigation was not directly exercised in the
browser; its changed lines (`saveScheduler.cancel` / flush wrapper) are covered by the sandbox
behavioral tests.

Unit (3) assessment (2026-09-06): no migration remains — the 409 transport normalization (response
`canvas`/`updatedAt` extraction from the conflict body) is already owned by the shared persistence
client, and both adapters consume that shared contract; the divergent parts are the conflict policies
themselves, which stay adapter-owned by design. Remaining seam work is unit (4) only (shared
remote-apply scheduling: Classic's `remoteSyncTimer` deferral and Smart's `canvasSyncTimer` merge
deferral), which is deferred until its owning batch.
```

## Browser — new Canvas

```text
Not yet run in this task. Existing status records read-only acceptance only.
```

## Browser — Legacy Classic

```text
2026-09-05 read-only isolated `127.0.0.1:3012`: normal `canvas.html` URL rendered Classic fixture `7ed83bf56f234d77a9e67ae1f6496577` with six ready NodeShell cards, ports, media controls and workflow controls. No Canvas mutation or execution was invoked.

2026-09-06 read-only local `127.0.0.1:3000/static/canvas.html`: Classic fixture `7ed83bf56f234d77a9e67ae1f6496577` rendered six nodes, link controls and the default semantic indicator `100% · 完整 · 6 节点`. No Canvas mutation or execution was invoked.

2026-09-06 read-only local post-connected-result smoke: the same Classic fixture rendered six nodes, link controls and `100% · 完整 · 6 节点`. No Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-file-drop-runtime smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading `media-drop-payload.js`. No upload, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-file-drop-payload smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading the new payload-resolution script version. No upload, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-file-drop-upload smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading the shared upload-transport script version. No upload, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-blank-Prompt-mutation smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading the new mutation script version. No Prompt move/delete, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-default-Loop-mutation smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading the new mutation script version. No Loop move/delete, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-empty-Output-mutation smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading the new mutation script version. No Output move/delete, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-empty-Group-mutation smoke: the same Classic fixture rendered its six ready cards and `100% · 完整 · 6 节点` after loading the new mutation script version. No Group move/delete, Canvas mutation, creation or execution was invoked.
```

## Browser — Legacy Smart

```text
2026-09-05 read-only isolated `127.0.0.1:3012`: the same normal `canvas.html` entry handed historical Smart fixture `ca914662f0dc4923bd5b60b29eb55b68` to its bounded compatibility adapter, which rendered Composer, Smart Group, upload node, ready NodeShell ports and workflow controls. No Canvas mutation or execution was invoked. The temporary server was stopped after verification.

2026-09-06 read-only local `127.0.0.1:3000/static/smart-canvas.html`: historical Smart fixture `ca914662f0dc4923bd5b60b29eb55b68` rendered Composer, Smart Group with Input/Output ports, upload node and the default semantic indicator `65% · 摘要 · 2 节点`. No Canvas mutation or execution was invoked.

2026-09-06 read-only local post-connected-result smoke: the same Smart fixture rendered Composer, Smart Group/Input/Output ports, upload and Prompt cards, plus `65% · 摘要 · 2 节点`. No Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-file-drop-runtime smoke: the same Smart fixture rendered Composer and `65% · 摘要 · 2 节点` after loading `media-drop-payload.js`. No upload, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-file-drop-payload smoke: the same Smart fixture rendered Composer, Group/Input/Output, upload and Prompt cards and `65% · 摘要 · 2 节点` after loading the new payload-resolution script version. No upload, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-file-drop-upload smoke: the same Smart fixture rendered Composer, Group/Input/Output, upload and Prompt cards and `65% · 摘要 · 2 节点` after loading the shared upload-transport script version. No upload, Canvas mutation, creation or execution was invoked.

2026-09-06 read-only local post-default-Smart-Loop-mutation smoke: the same Smart fixture rendered Composer and `65% · 摘要 · 2 节点` after loading the new mutation script version. No Loop move/delete, Canvas mutation, creation or execution was invoked.

2026-09-06 media playback-state contract: shared capture/restore now has explicit transport- and persistence-neutral coverage for time, pause, rate, mute and volume; Classic/Smart player binding and fallback policy remain adapter-owned. Focused regression: PASS (95 tests); full regression: PASS (270 tests).

2026-09-06 Renderer Admission browser read smoke: local Classic fixture retained six rendered cards and `100% · 完整 · 6 节点`; historical Smart fixture retained Composer, Smart Group, upload and Prompt cards with `65% · 摘要 · 2 节点`. Both used the shared admission module; no mutation, creation, save or execution was invoked.

2026-09-06 Smart blank-Prompt mutation browser read smoke: local `127.0.0.1:3000` loaded historical Smart fixture `ca914662f0dc4923bd5b60b29eb55b68` after the cache-version update, retaining its Composer and `65% · 摘要 · 2 节点`. The check was read-only: no Prompt move/delete, save, creation or execution was invoked.

2026-09-06 Classic connected-creation browser read smoke: local `127.0.0.1:3000` loaded Classic fixture `7ed83bf56f234d77a9e67ae1f6496577` after the command cache update, retaining six ready cards, generic Input/Output ports, media controls, workflow controls, and `100% · 完整 · 6 节点`. The check was read-only: no connection, creation, save, deletion or execution was invoked.
```

## Persistence / restart

```text
SQLite authority/CAS evidence is recorded in CURRENT_EXECUTION_STATUS.md; no new persistence mutation or restart was run in this pass.
```

## Stale conflict

```text
No new stale-write run in this inventory pass.
```

## Rollback

```text
No new rollback run in this inventory pass.
```

## Workflow import/export

```text
No new workflow transfer run in this inventory pass.
```

## 100 nodes

```text
Not yet accepted.
```

## 300 nodes

```text
Not yet accepted.
```

---

# Remaining Runtime Owners

## Classic

```text
Classic still owns product interaction state except NodeShell select/focus/menu and box completion, fallback node constructors, upload/file-drop creation, renderer lifecycle, all non-blank/group-linked deletion, rich move/edit behavior and Legacy execution behavior.
```

## Smart

```text
Smart still owns product interaction state, Composer, fallback node constructors, group/media/history/dependent-node deletion, group/media lifecycle, upload, MiniMax/video compatibility and execution behavior.
```

## Unified

```text
Unified owns SQLite CanvasRecord authority, CAS application services, the normal entry resolver, creation catalog, default-on supported blank creation, shared runtime primitives, NodeShell/renderer seams, graph/media/transfer algorithms and compatibility clients. These are not yet one product runtime.
```

---

# R4 Gate

```text
R4: NOT PASS
```

Change to `PASS` only when all requirements in `CODEX_EXECUTION_PLAN.md` are evidenced.
