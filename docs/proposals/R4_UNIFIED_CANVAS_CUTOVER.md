# R4 Proposal — Unified Canvas Cutover

## Problem

R3 established and verified the SQLite Project/Canvas records, but active page
routes still call the JSON `CanvasRepository` directly.  Changing the SQLite
authority flag alone would not alter runtime reads or writes, and would create a
misleading split authority.

## Constraints

- Use the R3 SQLite records; do not create a second canonical JSON store.
- Preserve complete Legacy Canvas payloads, unknown fields, workflow import/export,
  Classic/Smart execution compatibility, and `updated_at` responses during the
  migration window.
- Canonical logical revision, action authorization, and audit/outbox remain the
  authority for canonical mutations.
- No NodeRecord v1 change, new provider/model/executor system, or WholeHouse code.
- `main.py`, `canvas.js`, and `smart-canvas.js` may only wire/delegate or lose
  responsibility; no new Workbench business implementation belongs there.

## Options

1. Flip `authority_state` only. Rejected: routes would still write JSON.
2. Rewrite every Legacy route/page at once. Rejected: unbounded compatibility risk.
3. Add a SQLite-backed implementation of the existing Canvas repository contract,
   route existing helpers through an authority selector after backup/compare, then
   replace duplicate page runtime only after behavior parity. Recommended.

## Recommendation

First add a lossless, SQLite-backed compatibility repository behind the existing
`CanvasRepository` contract. It maps legacy `updated_at` checks at the HTTP boundary
to the canonical logical revision without treating timestamps as canonical revision.
It writes the payload and audit/outbox atomically, and preserves a validated JSON
export rollback path. Then use an explicit cutover feature boundary to select it
only after source backup, compare, and focused compatibility tests pass.

Classic and Smart page behavior must be characterized and delegated into shared
modules before duplicate page/script removal. Page deletion is a final R4 operation,
not an initial shortcut.

## Migration cost

Adds a compatibility repository/selector, backup-validation tooling, tests, and
narrow composition wiring. Existing pages initially retain their request/response
shape while their persistence boundary changes.

## Compatibility impact

Legacy JSON stays readable and is exported for rollback. Existing `updated_at`
fields continue to be returned as compatibility metadata, while the SQLite logical
revision remains independent. Existing Classic/Smart routes and provider execution
are retained until their shared-runtime equivalents prove parity.

## Security impact

Canonical writes require the R3 action boundary and atomic audit/outbox. The local
Legacy HTTP compatibility surface is not thereby claimed to be authenticated;
cutover must not broaden LAN access or expose secrets.

## Rollback

Before activation, create and validate a source backup and compare it to SQLite.
Rollback exports canonical payloads, restores the explicit `legacy_json` authority
state, and rehydrates the validated JSON directory without deleting the backup.

## Acceptance criteria

- SQLite compatibility repository can read/write/reopen losslessly.
- Logical revision rejects stale writes and `updated_at` remains compatibility-only.
- Canonical mutation/audit rollback together.
- Backup, import/compare, authority switch, and rollback are tested.
- Existing Canvas route compatibility and workflow import/export are characterized.
- One shared page/runtime/catalog replaces Classic/Smart only after verified parity.
- 100/300-node benchmarks and browser acceptance pass before deletion.
