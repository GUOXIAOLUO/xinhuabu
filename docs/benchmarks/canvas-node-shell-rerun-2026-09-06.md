# Canvas NodeShell Rerun After Interaction-Session Changes — 2026-09-06

## Scope

Re-measurement of the 2026-09-04 NodeShell baseline after the accumulated material
interaction-path changes (shared remote-apply scheduling, semantic-zoom DOM
application owner, shared node-drag position projection, shared node-resize size
proposal, unified-runtime lifecycle reset on canvas state swaps). Same methodology
as the baseline:

- NodeShell + LegacyRenderer path: `node_shell=1&legacy_renderer=1` (remaining
  gates at their current defaults, including `unified_canvas` and `semantic_zoom`);
- 100 and 300 media-free Legacy Prompt nodes (`type:'prompt'`, empty `text`,
  20-column grid, no connections);
- the same-origin `/static/canvas-performance-harness.html` iframe harness with
  `interactions=1` and the developer-only `visible=1` parameter;
- disposable Classic Canvas records created through the canonical API on an
  isolated server, deleted with the server afterwards.

## Environment

- Host: macOS Apple Silicon development machine.
- Browser: ZCode in-app browser (Chromium-based), 1280×800 viewport.
- Server: `http://127.0.0.1:3016` (process-local copy of the local SQLite
  database; canonical default routing).
- Canvas data: two disposable benchmark canvases, removed with the temporary
  server and database copy after capture.

## Result

| Nodes | Iframe load (ms) | Render ready (ms) | Target DOM elements | Zoom visual update (ms) | Pan visual update (ms) | Minimap refresh (ms) | Result |
|---:|---:|---:|---:|---:|---:|---:|---|
| 100 | 212.7 | 265.4 | 3,645 | 16.5 | 16.9 | 33.0 | PASS |
| 300 | 123.6 | 191.2 | 9,445 | 16.6 | 37.6 | 28.9 | PASS |

Baseline comparison (visible-frame 2026-09-04 samples):

| Metric | 100 baseline → rerun | 300 baseline → rerun |
|---|---|---|
| Render ready | 267 → 265 ms | 362 → 191 ms |
| Zoom visual update | 14 → 16.5 ms | 38 → 16.6 ms |
| Pan visual update | 21 → 16.9 ms | 104 → 37.6 ms |
| Minimap refresh | 49 → 33 ms | 15 → 28.9 ms |
| Target DOM elements | 3,617 → 3,645 | 9,418 → 9,445 |

All visible-frame interaction samples are below the provisional 120 ms local
visual-settlement alert. The DOM element delta (+28/+27) matches the semantic
zoom indicator and related shell additions. No interaction regression is
attributable to the shared interaction sessions; render-ready and pan improved
at 300 nodes. The earlier offscreen minimap cadence note (~140 ms, iframe
animation-frame dominated) remains a recorded P2 follow-up.

These values are single local observations, not cross-device budgets or
percentile commitments. Re-run after further material Canvas changes.
