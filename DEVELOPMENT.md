# Development Baseline — V2.2.1

## Product/development platform

V1 official product and primary development target:

- macOS
- Apple Silicon / arm64 first

Core architecture remains platform-neutral so Windows support can be added later through infrastructure/release adapters.

Windows and Linux are not V1 product-support targets.

---

## Supported local development environment

Recommended:

- current supported macOS on Apple Silicon;
- Python 3.10 or later;
- Node.js 20 or later for JavaScript checks;
- optional local integrations as needed: `ffmpeg`, Codex CLI, Gemini CLI, Jimeng CLI, ComfyUI.

The optional integrations are not required for the base unit test suite unless a focused integration test explicitly needs them.

---

## Repository-independent runtime rule

Normal Workbench startup/runtime must not require the source Git repository or a Git hosting service.

Do not add runtime GitHub/GitLab repository URLs for:

- self-update;
- version discovery;
- source tree download;
- normal product startup.

Git remains an external developer/version-control tool.

---

## First-time setup

From the repository root, create an isolated Python environment and install project requirements.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt
```

If direct PyPI access has a TLS handshake problem on macOS, a project-approved mirror/fallback may be used only inside the virtual environment.

Provider credentials belong in backend-only secret configuration such as `API/.env` until the target CredentialRef/connection systems replace the Legacy path.

Never put raw credentials in:

- browser storage;
- Canvas/Node data;
- source files;
- fixtures;
- committed configuration.

---

## Base verification

Run the Python test suite:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests -v
```

Run syntax/static checks applicable to the current Round:

```bash
.venv/bin/python -c "import ast,pathlib; ast.parse(pathlib.Path('main.py').read_text(encoding='utf-8')); print('main.py AST OK')"
node --check static/js/canvas.js
node --check static/js/smart-canvas.js
```

As the repository evolves, CI should add Ruff/type/coverage/dependency/schema/architecture checks without changing the Round/Gate discipline.

---

## Runtime files

Generated project/Canvas/runtime data, provider configuration, uploaded media, previews, outputs, caches and virtual environments remain runtime data rather than source.

Formal target authorities move progressively to:

- SQLite for structured records;
- BlobStore-backed files;
- versioned Asset/Artifact records.

---

## Local server mode

Default product-development mode remains loopback-only.

Typical development launch remains:

```bash
python3 main.py
```

and the Web UI uses the configured local host/port.

LAN compatibility is not authenticated multi-user support.

Do not treat wildcard bind as safe remote deployment.

---

## Codex development baseline

Codex App Server is the preferred rich integration boundary.

V1 client transport:

```text
stdio JSONL
```

Do not make experimental WebSocket App Server transport a V1 dependency.

### Compatibility policy

Workbench does not require one exact Codex version string.

For Codex integration work:

1. record installed Codex version;
2. inspect the official App Server stable protocol for that version;
3. generate/compare official schema where used;
4. run the repository's Codex compatibility tests;
5. update the recorded tested version as evidence;
6. do not branch business behavior on exact version equality.

Official generation commands include:

```bash
codex app-server generate-json-schema --out <dir>
codex app-server generate-ts --out <dir>
```

Generated Codex protocol artifacts belong inside the Codex integration boundary and must not become Core domain contracts.

### Codex process reliability

App Server client code must eventually cover:

- stdout and stderr draining;
- unexpected EOF/process exit;
- pending request failure;
- bounded event queues;
- overload/backoff;
- typed server request dispatch;
- shutdown/recovery.

---

## Codex Skills

Workbench Skill and Codex Skill are different concepts.

When Workbench packages provide Codex `SKILL.md` implementations, prefer session/runtime-supported skill discovery/extra roots rather than treating the user's global Codex home as Workbench authority.

---

## Model Picker development rule

A Codex-discovered model route should be represented through Workbench ModelAvailability just like a direct provider route.

Example UI choices:

```text
GPT-X · Codex Harness
GPT-X · OpenAI API
```

Do not encode Codex as a ModelDefinition.

---

## Canvas performance

R4 and later Canvas Gates must keep reproducible 100/300-node measurements.

Performance harnesses are evidence tools, not business data sources.

A later release budget may add larger/percentile measurements.

---

## Transitional versioned node API

During migration, versioned node routes remain compatibility surfaces until Unified Canvas/canonical mutation owns normal product behavior.

Every write must use expected revision and application services.

Do not add new business systems directly to Legacy page routes.

---

## macOS-specific infrastructure

V1 may use macOS-specific infrastructure adapters for:

- Keychain;
- file/folder pickers;
- Finder;
- local application launching;
- local software bridges;
- filesystem permission workflows.

Keep these adapters out of Core domain models so future Windows support can be added without redesigning business records.

---

## Repository hygiene direction

Do not perform broad directory cleanup during an unrelated active Gate.

After R4, plan a bounded hygiene task for historical vendored runtimes/wheels.

Target:

```text
packages/
├── common/
├── wholehouse/
└── media/

vendor/
├── wheels/
└── optional-runtimes/
```

Windows runtime artifacts are not part of the Mac-first V1 product target.

---

## Manual smoke principle

Manual browser smoke tests use disposable or backed-up records.

For destructive paths:

- create backup first;
- use known test records;
- verify restart/reload;
- remove disposable data afterward.

Do not use unbacked-up real customer data for migration experimentation.

---

## Planning/status discipline

These files have different meanings:

- `CURRENT_ARCHITECTURE.md` = verified current facts;
- `docs/status/CURRENT_EXECUTION_STATUS.md` = active Round/current evidence;
- `TARGET_ARCHITECTURE.md` = future architecture;
- `IMPLEMENTATION_PLAN.md` = Round/Gate plan;
- `MIGRATION_PLAN.md` = compatibility/authority-switch strategy;
- `AGENTS.md` = hard repository constraints.

Do not copy future V2.2.1 claims into current-state files until source/tests prove them.
