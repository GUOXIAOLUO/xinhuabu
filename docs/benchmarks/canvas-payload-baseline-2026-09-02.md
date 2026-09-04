# Canvas Payload Baseline — 2026-09-02

## Environment

- Host: macOS Apple Silicon development machine.
- Node: `v24.20.0`.
- Command: `node tools/benchmark-canvas-payload.mjs`.

## Result

| Lightweight Classic nodes | Serialized Canvas payload |
|---:|---:|
| 100 | 9,622 bytes |
| 300 | 29,132 bytes |

The tool also reports construction/serialization duration, but timing is intentionally not a release threshold because it varies by machine and runtime. The reported values were below one millisecond on this host.

## Scope and limitation

This is a deterministic payload-size baseline only. It does not measure DOM render, media decoding, panning, zooming, minimap refresh, or network save latency. Those browser measurements remain required before Phase 0 exit and must record browser version, viewport, node media mix, and hardware profile.

## Empty-state browser smoke check

On the same macOS development machine, the local server was started on `127.0.0.1:3300` and checked through the Codex in-app browser without creating project records or calling providers:

| Page | Observed state | Console errors |
|---|---|---:|
| Classic project workspace (`static/canvas-list.html?project=default`) | `complete`; 138 DOM elements; no Canvas cards; empty hint visible | 0 |
| Smart Canvas (`static/smart-canvas.html`) | `complete`; 861 DOM elements; zero Canvas nodes; Run disabled in empty state | 0 |

The browser automation evaluation environment does not expose the Navigation Timing API, so no navigation-time number is recorded here. This smoke check confirms empty-state loading only; it is not a substitute for the required 100/300-node interaction benchmark.

The smoke test initially exposed that the constrained runtime environment did not include a WebSocket implementation, causing `/ws/stats` upgrades to fall back to HTTP 404. `websockets` is now a required constrained dependency. After installation, Smart Canvas loaded with no console errors and the server recorded an accepted `/ws/stats` connection followed by a clean disconnect.

## 100/300-node Classic Canvas render smoke check

Temporary Classic Canvas records containing lightweight Image nodes were created through the existing Canvas API, opened in the local browser, and purged after the check. No user Canvas data was modified.

| Nodes | Rendered `[data-id]` / `.image-node` elements | DOM elements | Console errors |
|---:|---:|---:|---:|
| 100 | 100 / 100 | 2,692 | 0 |
| 300 | 300 / 300 | 6,692 | 0 |

This confirms that both sample sizes load and render completely in the local browser. It does not establish browser navigation, pan/zoom, or minimap-refresh budgets; those remain the P0.9 completion requirement because Navigation Timing is not available through the current automation surface.

## Iframe render-ready timing harness

The developer-only `/static/canvas-performance-harness.html` page starts its timer inside the browser page, loads a same-origin Classic Canvas iframe, and polls on animation frames until the expected number of `[data-id]` elements appears. It therefore measures the combined iframe load, Canvas fetch, and initial DOM-render path; it does not measure media decoding, pan/zoom, or minimap refresh.

| Nodes | Iframe load (ms) | Render ready (ms) | Target DOM elements | Result |
|---:|---:|---:|---:|---|
| 100 | 79.800 | 153.000 | 2,592 | PASS |
| 300 | 53.300 | 95.500 | 6,392 | PASS |

Both runs used the local server at `127.0.0.1:3300` in the Codex in-app browser on the macOS Apple Silicon development machine. These are single local samples, not release budgets: module and HTTP caches can affect results, and the 300-node sample ran after the 100-node sample.

The first 100/300-node capture produced a `MutationObserver.observe` exception attributed by the browser to the Tailwind CDN runtime, plus its existing production-use warning. A clean recheck on 2026-09-02 opened both a direct temporary Canvas and the same Canvas in the same-origin iframe; neither reproduced the exception. The recheck emitted only Tailwind's existing production-use warning. The anomaly is retained here for traceability, but is not treated as a reproducible P0.9 blocker.

## Interaction visual-settlement baseline

The harness can run with `interactions=1` after the expected node count has rendered. It dispatches one wheel zoom at the board centre, one 80-by-50-pixel board pan, and one minimap jump inside the same-origin iframe. For each operation, it records the browser-page duration until the Canvas transform or rebuilt minimap viewport is visible on an animation frame. This measures UI update and scheduled minimap work, not input-device latency or GPU presentation.

| Nodes | Zoom visual update (ms) | Pan visual update (ms) | Minimap refresh (ms) | Result |
|---:|---:|---:|---:|---|
| 100 | 19.700 | 14.300 | 26.100 | PASS |
| 300 | 7.500 | 20.500 | 50.200 | PASS |

The samples used a 1280-by-800 offscreen, same-origin iframe in the Codex in-app browser on the macOS Apple Silicon development machine and a media-free Image-node mix. They are single local observations, not a cross-device performance commitment. Until repeated samples establish a percentile budget, use 120 ms as a local 300-node regression alert threshold for each measured visual-settlement operation (more than twice the slowest initial observation). Tailwind's production-use warning remains a dependency-hardening concern, but the earlier runtime exception did not reproduce in clean direct or iframe Canvas checks.

## Local Canvas save API baseline

Five sequential `PUT /api/canvases/{id}` requests were issued for each temporary lightweight-node Canvas on the local server. The timer starts immediately before `fetch` and ends after the JSON response is received. Each temporary Canvas was purged after its runs.

| Nodes | Samples (ms) | Median (ms) | Maximum (ms) |
|---:|---|---:|---:|
| 100 | 3.260, 4.630, 3.492, 4.591, 3.410 | 3.492 | 4.630 |
| 300 | 5.676, 5.502, 5.114, 4.836, 5.324 | 5.324 | 5.676 |

These are localhost API round-trip measurements for small, media-free JSON graphs. They are useful as a relative regression signal for Canvas persistence, but do not measure browser interaction or a networked deployment.
