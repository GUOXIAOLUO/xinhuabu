# Canvas NodeShell Baseline — 2026-09-04

## Scope

This local, single-sample baseline measures the opt-in Classic Canvas migration path:

- `node_shell=1&legacy_renderer=1`;
- 100 and 300 media-free Legacy Prompt nodes; and
- the existing same-origin `/static/canvas-performance-harness.html` iframe harness with `interactions=1`.

The harness now forwards only its allowlisted renderer feature gates to the target frame, so this capture measures the NodeShell plus LegacyRenderer path rather than the default Legacy DOM path. It only observes a disposable Canvas and does not execute a provider or save user data.

## Environment

- Host: macOS Apple Silicon development machine.
- Browser: local Safari browser window.
- Server: `http://127.0.0.1:3000`.
- Canvas data: temporary Classic Canvas records, purged immediately after capture.

## Result

| Nodes | Iframe load (ms) | Render ready (ms) | Target DOM elements | Zoom visual update (ms) | Pan visual update (ms) | Minimap refresh (ms) | Result |
|---:|---:|---:|---:|---:|---:|---:|---|
| 100 | 146 | 267 | 3,617 | 14 | 21 | 49 | PASS |
| 300 | 98 | 297 | 9,417 | 9 | 59 | 149 | PASS |

The 300-node NodeShell run adds roughly 3,025 target DOM elements over the prior media-free Image-node baseline, which is expected because Prompt bodies retain their Legacy controls inside the shared shell. Zoom and pan remain below the provisional 120 ms local visual-settlement alert. The 300-node minimap refresh at 149 ms exceeds that alert and is therefore a recorded P2 follow-up, not a release-performance claim.

These values are single local observations, not cross-device budgets. Cache state, browser scheduling, the retained Legacy Prompt controls, and the iframe environment all affect them. Re-run this capture after minimap or renderer-host changes and use repeated samples before setting a percentile target.

## Minimap scheduling follow-up

Classic Canvas now separates viewport-only minimap updates from node-geometry rebuilds. A pan, zoom, or minimap jump updates the existing viewport box on the next animation frame; rendering nodes, node resize/drag, and refreshed card content still rebuild the minimap bounds and node rectangles. When semantic zoom is not explicitly enabled, the Classic adapter also skips its former full NodeShell/Legacy card walk during viewport movement.

A single 300-node Safari recheck in the existing offscreen iframe harness reported 141 ms for minimap refresh. That result is not evidence that the source-level change regressed or failed: the iframe's animation-frame scheduling dominates the measurement and produced the same approximately 140 ms cadence before and after the change.

The harness now accepts the explicit developer-only `visible=1` query parameter. It keeps the target frame visible but pointer-inert behind the status panel, and reports `target_visibility` so results remain comparable. A disposable 300-node Prompt-card capture using that mode produced the following result:

| Nodes | Visibility | Iframe load (ms) | Render ready (ms) | Target DOM elements | Zoom visual update (ms) | Pan visual update (ms) | Minimap refresh (ms) | Result |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 300 | visible | 152 | 362 | 9,418 | 38 | 104 | 15 | PASS |

All three visible-frame interaction samples are below the provisional 120 ms local alert. This is still one local sample, not a cross-device commitment or a percentile budget; retain the alert and repeat visible captures after material Canvas changes.
