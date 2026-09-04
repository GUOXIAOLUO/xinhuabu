# Phase 0 Route Security Inventory

This inventory records intended authorization classes for the current route surface. It does not claim that authorization is implemented. Until authentication and authorization ship, LAN operation remains unauthenticated compatibility mode.

| Route group | Examples | Intended class | Phase 0 status |
|---|---|---|---|
| Health and static shell | `/`, static UI, app info | Public local bootstrap | Existing behavior retained |
| Canvas and project data | `/api/projects`, `/api/canvases` | Project Owner, Editor, Viewer by operation | Authorization not implemented |
| Asset data and media | asset libraries, uploads, mounted media | Project role plus asset policy | Authorization not implemented |
| Provider configuration | `/api/providers`, `/api/config` | Provider administrator | Secret browser path contained; authorization not implemented |
| ModelScope compatibility metadata | `/api/config/token` | Provider administrator or authorized feature query | Now returns only `configured`; legacy route remains temporarily |
| ComfyUI and workflows | `/api/comfyui/*`, `/api/workflows/*` | Tool/workflow administrator, project-scoped execution | Authorization not implemented |
| External provider execution | image/video/chat/RunningHub routes | Project Editor plus provider permission | Authorization not implemented |
| Local storage and shared folders | storage, shared-folder routes | Storage administrator | Authorization not implemented |
| Application update and rollback | update, backup, rollback routes | Update administrator | Authorization not implemented |
| CLI and subprocess operations | Codex, Gemini, Jimeng, ffmpeg helpers | Tool administrator with scoped allowlist | Authorization not implemented |
| WebSocket and SSE | `/ws/stats`, chat stream | Authenticated session/project subscription | Authentication not implemented |

Before any studio/LAN multi-user claim, protect provider, storage, update, shared-folder, subprocess, project, Canvas, asset, workflow, WebSocket, and media-delivery routes with server-side identity and authorization checks.
