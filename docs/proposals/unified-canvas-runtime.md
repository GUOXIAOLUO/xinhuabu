# Unified Canvas Runtime Proposal

## Decision status

- Product direction requested and clarified by the user on 2026-09-04: the final product does not distinguish old/new, Classic/Smart, or Legacy/current nodes.
- This proposal is the required architecture gate before changing or retiring a Canvas mode.
- Implementation remains incremental for data safety. Classic and Smart source URLs stay available only until the acceptance criteria in this document pass; the completed product retains one Canvas page and one entry.

## Problem

The application exposes two Canvas products for one project graph:

- Classic Canvas (`static/canvas.html` + `static/js/canvas.js`) contains the broad fixed-node catalog and general workflow tooling.
- Smart Canvas (`static/smart-canvas.html` + `static/js/smart-canvas.js`) contains the media-first composer, Smart Group behavior, Prompt/Loop/MiniMax cards, and media operations.

They share Canvas JSON persistence, but each page separately implements viewport state, selection, drag, resize, connections, grouping, minimap, undo behavior, uploads, workflow transfer, save conflict handling, and execution coordination. The Canvas list also asks users to choose a mode and routes them to different pages. This produces inconsistent behavior and prevents a Classic node and a Smart node from being operated in one graph.

The requested outcome is one user-facing Canvas entry in which every retained node family can coexist and use the same selection, port, grouping, viewport, save, and creation behavior.

## Current-state facts

| Boundary | Classic | Smart | Existing shared seam |
|---|---|---|---|
| Stored discriminator | `kind: classic` | `kind: smart` | Same Canvas repository and whole-Canvas API |
| Node families | image, prompt, loop, group, LLM, generator, Midjourney, ModelScope generation, video, MiniMax, RunningHub, ComfyUI, LTX Director, output, prompt group, imported workflow | smart-image, smart-prompt, smart-loop, smart-group, smart-minimax | Lossless Legacy adapter and canonical NodeRecord view |
| Interaction | Independent viewport, selection, multi-select, drag, resize, links, minimap, undo | Independent viewport, selection, multi-select, drag, resize, links, minimap, undo | NodeShell intents, screen-space controls, semantic zoom |
| Creation | Fixed constructors and dispatch in `canvas.js` | Fixed constructors and dispatch in `smart-canvas.js` | Shared command IDs; restricted NodeCreationService and graph mutation paths |
| Rendering | Large type-conditional renderer | Large type-conditional renderer | NodeShell, LegacyRenderer, MediaRenderer, RendererRegistry contract |
| Execution | Classic fixed-node executors and provider panels | Smart composer plus Smart node executors | Backend provider routes; no unified executor adapter yet |
| Save behavior | Legacy whole-Canvas PUT; Classic viewport is not replaced by the request | Legacy whole-Canvas PUT; request viewport is persisted | Revision-safe compatibility repository and versioned node APIs |

The existing shared modules prove that common chrome and command semantics can be extracted without changing the stored Legacy payload. They do not yet constitute a shared Canvas interaction kernel.

## Constraints

1. Do not perform a big-bang rewrite of either high-risk editor script.
2. Keep existing Canvas JSON readable and preserve unknown fields losslessly.
3. Keep Classic and Smart URLs loadable only throughout the bounded migration window, then remove the duplicate page and route.
4. Do not add a third independent Canvas engine.
5. Canvas Core may understand graph interaction, but not provider, Skill, or industry meaning.
6. Node creation converges on NodeCreationService; render dispatch converges on NodeRecord + NodeShell + RendererRegistry.
7. Existing provider, ComfyUI, RunningHub, MiniMax, LLM, media, output, loop, group, import/export, and asset flows remain operational through adapters until migrated.
8. Existing optimistic revision checks, path containment, backend-only secrets, and loopback restrictions must not be weakened.
9. User-visible entry consolidation happens only after one runtime can open both fixture families and operate their nodes.
10. Migration source is an internal adapter concern. No final UI, node definition, menu, renderer, or Inspector may label a node as old, new, Classic, Smart, or Legacy.

## Options

### Option A: Copy Smart features into Classic Canvas

This reaches one page quickly, but duplicates or interleaves more provider-specific branches inside the largest Legacy file. It makes later RendererRegistry and Skill migration harder and has the highest regression risk.

### Option B: Add a router page that embeds either Legacy editor

This creates one URL but not one Canvas. Cross-family nodes still cannot coexist, interaction bugs remain duplicated, and the result is two engines hidden behind one shell.

### Option C: Extract one shared runtime and retain both pages as adapters during migration

This incrementally moves graph interaction into business-neutral modules. Both source pages call the same runtime while their node bodies and executors are extracted into canonical renderers and executors. After parity, `canvas.html` becomes the only host; `smart-canvas.html` is first reduced to a temporary forwarder and then removed after the migration window.

## Recommendation

Choose Option C.

The canonical target is:

```text
Canvas list / deep link
        |
        v
  /static/canvas.html            one user-facing entry
        |
        v
UnifiedCanvasPageAdapter
        |
        +-- CanvasRuntime        viewport, selection, drag, resize, undo
        +-- GraphInteraction     ports, edges, connection validation intents
        +-- GroupInteraction     membership and layout intents
        +-- NodeCreationClient   NodeCreationService / GraphMutationService
        +-- NodeShell
        `-- RendererRegistry
              +-- MediaRenderer
              +-- Form/Task/Composite renderers
              `-- temporary source-payload adapter
```

The two source scripts remain references for working behavior during extraction, not peer runtimes in the final product. Every retained function must move behind a canonical renderer, application service, or executor contract. Temporary source adapters are internal migration tools and must be removed after their payload fields have canonical owners.

## Canonical entry and Canvas identity

- The final user-facing route is `/static/canvas.html?id=<canvas_id>&project=<project_id>`.
- The Canvas list stops offering “Classic” versus “Smart”; it creates one “Canvas”.
- Canonical persisted records use a versioned Canvas schema and one Canvas kind. Existing `classic` and `smart` values are accepted only as import/migration inputs.
- Opening a source record first adapts it losslessly. A checkpointed migration writes the canonical record only after the unified renderer and executor for every contained node are available.
- Canonical nodes use one definition per function. Pairs such as `image`/`smart-image`, `prompt`/`smart-prompt`, `loop`/`smart-loop`, and `group`/`smart-group` converge rather than remaining two user-visible variants.
- `smart-canvas.html` is a temporary deep-link forwarder after cutover and is removed with its duplicate runtime after the compatibility window defined here passes.

## Capability convergence

### Shared runtime responsibilities

- world/screen coordinate conversion and viewport recovery;
- pan, wheel/pinch zoom, fit selection, and minimap viewport;
- single selection, additive selection, marquee selection, and keyboard focus;
- node drag, group drag, resize, z-order, and undo/redo commands;
- input/output port geometry, edge hit-testing, connection preview, and edge rendering;
- generic group membership intents and drop targeting;
- file/drop and context-menu intent dispatch;
- save scheduling, expected revision, remote invalidation, and conflict presentation;
- NodeShell, semantic zoom, screen-space controls, and accessibility behavior.

### Temporary source-adapter responsibilities during migration

- preserve source DOM controls and event listeners until the equivalent canonical renderer is complete;
- map source node payloads to uniform NodeRecord views;
- expose port capability metadata without branching CanvasRuntime on source type names;
- delegate provider/model execution until the equivalent canonical executor is complete;
- translate source group payloads and output synchronization;
- round-trip the original payload with unknown fields intact;
- disappear after every field and behavior has a canonical owner.

### Catalog visible in the unified Canvas

The creation query exposes one catalog containing the union of retained functions. Common concepts such as Image, Prompt, Loop, Group, and MiniMax resolve to one canonical definition. Provider-backed functions remain available through ordinary definitions and executor adapters; users do not see a Legacy section or source-mode distinction.

## Migration plan

### U0 — Contract and inventory

- Record this proposal and a machine-checked capability inventory.
- Freeze Classic and Smart golden fixtures and expected round-trip behavior.
- Define the unique-entry compatibility contract.

Exit: architecture direction and non-destructive constraints are reviewable before runtime edits.

### U1 — Shared CanvasRuntime state model

- Add a side-effect-free runtime for viewport, selection, geometry, and transaction intents.
- Adapt both pages to the same state model behind `unified_canvas=1`.
- Keep existing DOM rendering and persistence unchanged.

Exit: the same tests drive pan/zoom, selection, multi-select, drag, resize, and viewport recovery for both adapters.

### U2 — Shared graph and group interaction

- Move port anchors, edge previews, edge selection, connection completion, and group drop targeting behind shared contracts.
- Express compatibility through definition/port metadata rather than Canvas type branches.
- Preserve the existing connection dictionary on write.

Exit: a Classic fixture and a Smart fixture use identical port geometry and interaction commands; legacy edges round-trip unchanged.

### U3 — Unified render host

- Make NodeShell the common node chrome.
- Register canonical media, form/task, and composite renderers in one browser RendererRegistry; use the temporary source adapter only for fields not yet extracted.
- Render both fixture families in one host without importing one entire editor into the other.

Exit: one test Canvas contains and operates nodes adapted from both fixture families, with no source-family label or behavior switch in the UI.

### U4 — Unified creation catalog

- Replace page-specific menu filtering with one registry-backed creation query.
- Route context menu, port-to-empty-space, upload, workflow import, and group creation through NodeCreationService or GraphMutationService.
- Keep every retained fixed function in the same catalog while its executor is extracted; do not expose a Legacy subsection.

Exit: no migrated entry directly appends a node; one menu can create all retained families.

### U5 — Executor and workflow adapters

- Extract both source execution paths behind canonical definition/executor adapters.
- Normalize input/output bindings while preserving source result payloads until canonical persistence is verified.
- Verify cross-family connections only when declared port/content contracts are compatible.

Exit: representative media, Prompt/LLM, Loop, group, output, and one provider-backed flow execute in the unified host.

### U6 — Switch the user-facing entry

- Make Canvas list create one Canvas type and always open `canvas.html`.
- Make direct Smart links temporarily forward into the canonical route while preserving query parameters and Canvas identity.
- Remove all mode labels, mode toggles, source-family catalog sections, and runtime branching from the product UI.

Exit: all normal product navigation has one Canvas entry; old links still open the same data.

### U7 — Compatibility window and duplicate removal

- Run load/edit/save/reload and workflow import/export against both fixture families and real user acceptance Canvases.
- Compare performance with the 100/300-node baseline.
- Migrate backed-up source records to the canonical Canvas schema after per-record validation.
- Remove `smart-canvas.html`, its duplicate runtime and CSS, Classic/Smart creation choices, source-mode routing, and obsolete renderer/executor branches.

Exit: the repository and workbench expose one Canvas page, one runtime, one catalog, and one Canvas record model. This user-approved proposal authorizes that scoped duplicate removal only after all acceptance gates pass and rollback backups exist.

## Migration cost

This is a multi-round convergence, not a one-file change. Most cost is in interaction characterization and executor adaptation, not HTML composition. The safest sequence completes U1–U3 before changing the visible entry. During that period, both pages remain available but increasingly thin.

Expected high-risk files are `static/js/canvas.js`, `static/js/smart-canvas.js`, both Canvas HTML/CSS files, Canvas list routing, and frontend compatibility tests. New code should live under `static/js/workbench/canvas/` and remain independent of provider and industry modules.

## Compatibility impact

- No existing Canvas record is rewritten by U0.
- U1–U3 are feature-gated and retain temporary source render/execution fallbacks.
- Source `kind`, node `type`, connections, groups, settings, logs, viewport, and unknown extensions survive adaptation until their canonical record migration succeeds.
- Existing whole-Canvas PUT remains available until all mutation entries converge on command services.
- Existing old URLs and bookmarks remain loadable during the bounded compatibility window; after U7 they are removed from the workbench together with the duplicate page.
- Cross-family connections are not accepted merely because both nodes are visible; declared port/content compatibility must pass.

## Security impact

U0 introduces no endpoint or secret handling change. Later implementation must:

- keep provider secrets backend-only;
- retain project/actor checks and expected revisions on command APIs;
- avoid adding browser-side token fallbacks;
- validate imports/uploads and preserve current path-containment rules;
- keep remote URL and provider execution behind existing backend policy;
- emit secret-free audit events for command-service mutations.

## Rollback

- U1–U5 are enabled only by a service-boundary feature flag and can return to the two source adapters without changing persisted payloads.
- The Canvas list route switch in U6 is reversible while the temporary forwarding page remains present.
- Before U7, each source Canvas has a validated backup and migration report. Rollback restores that exact record and temporarily re-enables the source adapter.
- No migration changes provider credentials.
- A failed unified save must not silently fall back to overwriting the Canvas; the previous revision remains authoritative.

## Acceptance criteria

1. One canonical URL opens both Classic and Smart fixture records.
2. One Canvas can contain every retained node function, including functions previously available in only one source editor, without displaying a source distinction.
3. Pan, zoom, minimap, viewport recovery, selection, multi-select, marquee, keyboard focus, drag, resize, delete, undo, and redo use one runtime path.
4. Left/right ports share one geometry contract and connect only through typed compatibility rules.
5. Image, Prompt, Loop, Group, MiniMax, media, output, LLM, and representative provider nodes remain operable.
6. Group collection/layout and workflow/output behavior are available as ordinary unified Canvas functions.
7. Context menu, port creation, upload, import, and other migrated creation entries call the centralized creation/mutation services.
8. Save/reload and workflow export/import preserve every known and unknown source field through migration, then use the canonical schema.
9. Expected-revision conflicts never overwrite newer Canvas state.
10. The normal Canvas list and new-Canvas flow expose one Canvas choice and one entry URL.
11. Existing source deep links open the same Canvas during the compatibility window; after U7 the workbench contains no duplicate Canvas entry or page.
12. The 100/300-node interaction baseline remains within the documented regression budget.
13. Both source fixtures, the canonical mixed fixture, API, security, syntax, migration, and browser smoke checks pass before duplicate removal.

## Non-goals

- Replacing the frontend framework.
- Replacing JSON persistence or the database strategy.
- Rewriting provider integrations while extracting the Canvas runtime.
- Treating Skill IDs or provider names as Canvas Core render branches.
- Removing a retained node function; only duplicate mode/runtime implementations are removed.
