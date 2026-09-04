# Development Baseline

## Supported environment

- Python 3.10 or later on macOS, Windows, or Linux.
- Node.js 20 or later for JavaScript syntax checks.
- Optional local integrations: `ffmpeg`, Codex CLI, Gemini CLI, Jimeng CLI, and ComfyUI. The required Python environment includes `websockets` so the Canvas live-update endpoint can accept WebSocket upgrades.

The optional integrations are not required to run unit tests. Their availability is checked by the application when their corresponding features are used.

## First-time setup

From the repository root, create an isolated environment and install the project requirements:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
```

On Windows, replace `.venv/bin/python` with `.venv\\Scripts\\python.exe`.

If direct PyPI access has a TLS handshake failure, use the verified macOS fallback below. It installs only into `.venv` and does not alter the system Python:

```bash
UV_NO_PROGRESS=1 uv --system-certs pip install \
  --python .venv/bin/python \
  --default-index https://mirrors.aliyun.com/pypi/simple/ \
  -r requirements-dev.txt
```

Provider credentials belong in `API/.env`. Do not put credentials in browser storage, source files, fixtures, or committed configuration.

## Verification

Run the Python test suite:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Run the entry-point syntax checks:

```bash
.venv/bin/python -c "import ast,pathlib; ast.parse(pathlib.Path('main.py').read_text(encoding='utf-8')); print('main.py AST OK')"
node --check static/js/canvas.js
node --check static/js/smart-canvas.js
```

## Runtime files

Generated Canvas/project/conversation data, provider configuration, previews, uploaded media, outputs, test caches, and the virtual environment are intentionally ignored by Git. `data/asset_library.json` remains tracked as the current seed/template data file.

## Local and LAN mode

The default server binds only to `127.0.0.1:3000`. Launch normally with `python3 main.py` or the supplied launcher and open `http://127.0.0.1:3000/`.

LAN mode is deliberately opt-in because this compatibility server does not yet authenticate users. On a trusted network only, set the host before launching:

```bash
WORKBENCH_HOST=0.0.0.0 python3 main.py
```

`WORKBENCH_PORT` changes the port. `WORKBENCH_ALLOWED_ORIGINS` accepts a comma-separated explicit CORS allowlist; wildcard origins are rejected. LAN access uses same-origin requests and does not require adding every LAN address to this list.

## Canvas performance harness

For disposable benchmark Canvas records only, load `/static/canvas-performance-harness.html?id=<canvas-id>&expected=<node-count>`. The harness measures iframe load and the time until the existing Classic Canvas renders the expected number of node elements. Add `&interactions=1` to measure synthetic wheel zoom, board pan, and minimap-jump visual settlement from inside the same-origin iframe. The harness itself does not create, save, or delete graph records; the loaded Legacy Canvas can still issue its normal touch request, so create and purge benchmark records through a controlled test procedure.

## Manual Canvas smoke checklist

On 2026-09-02, the local server at `127.0.0.1:3300` was checked in the Codex in-app browser with disposable records only:

- Classic Canvas: created a Canvas through the workspace UI, expanded the quick toolbar, added a Legacy Image node, confirmed the auto-save API record contained one node, and reloaded the editor with that node preserved.
- Smart Canvas: loaded the empty composer, verified the provider selector and disabled Run control were visible without a provider call, and entered a prompt successfully. Run was intentionally not executed because no provider/model configuration was supplied.

The disposable Classic Canvas was purged after the check. Provider execution, uploads, and destructive user-data paths remain out of this smoke scope.

## Transitional Canvas-node API

When the server binds to a loopback host only (`127.0.0.1`, `::1`, or `localhost`), the first versioned node endpoints are available at `/api/v1/canvases/{canvas_id}/nodes` and `/api/v1/canvases/{canvas_id}/nodes/{node_id}`. They require a non-empty `X-User-ID`, a matching project identifier, and an expected Canvas revision for every write. The only currently registered definition is `legacy:image@0`; `POST` creates an empty Legacy Image node idempotently, `GET` reads it, `PUT` updates its title and/or position, and `DELETE` removes it plus any Legacy connections that reference it. Every effective write records a secret-free local audit event under ignored runtime data. The endpoints are not registered for LAN or other non-loopback bindings.

## P1.7 browser verification

To verify the opt-in frontend slice, first create or open a local Canvas through the Canvas list so its owner matches the local browser user, then append `versioned_nodes=1` to its URL. Confirm that top-level Image, Prompt, and Loop creation works; then drag from an existing node port and choose Group. For each created item, first use the editor undo command immediately and confirm the local graph returns to its prior state; create it again, wait for the saved state, reload the page, and confirm the node (and, for Group, its connection) remains present. Undo history is intentionally in-memory and is cleared by reload. In Smart Canvas, open the blank-canvas creation menu and create an empty Group; confirm its empty state and selection, undo it immediately, then create it again and confirm save/reload. Adding members to that Group and nested Group creation remain Legacy paths. Repeat without `versioned_nodes=1` and confirm the Legacy creation behavior remains available.
