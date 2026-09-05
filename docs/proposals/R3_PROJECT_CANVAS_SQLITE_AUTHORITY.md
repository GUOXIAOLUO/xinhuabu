# R3 Proposal — Project and Canvas SQLite Authority

## Problem

Project identity and Canvas graph data are currently stored in mutable JSON files.
Canvas `updated_at` acts as a compatibility conflict marker, but it is not a
logical revision. Migrated node/graph writes append JSONL audit records after the
file mutation, so canonical mutation and audit are not atomic.

## Constraints

- Preserve Legacy Canvas JSON readability, unknown fields, Classic/Smart pages,
  provider execution, and `codex exec` through R3.
- Do not change NodeRecord v1 or remove U7 compatibility paths.
- Map `project: "default"`, empty owner, non-empty owner, and mismatches explicitly;
  never invent a remote identity for an unowned Legacy Canvas.
- Canonical Canvas mutation and durable audit/outbox must share one SQLite
  transaction.
- New logic belongs under `workbench/`; `main.py` may only wire it.

## Options

1. Keep JSON authoritative and add only another JSON index. Rejected: no atomic
   audit, no independent logical revision, and no durable authorization boundary.
2. Replace Legacy files/pages immediately. Rejected: this is U7/R4 and would break
   required compatibility.
3. Add SQLite records, import/backfill and compare Legacy records, then controlled
   switch through a repository boundary while retaining a rollback/export adapter.
   Recommended.

## Recommendation

Introduce versioned ProjectRecord, ProjectMember, and CanvasRecord SQLite tables
behind R3 repositories. Store the complete lossless Legacy Canvas payload in the
canonical Canvas record, while keeping normalized identity, timestamps, deleted
state, and a monotonic logical revision in columns. Add an append-only audit/outbox
table written by the same transaction as canonical mutations.

Backfill uses an explicit identity policy: `default` maps to the stable local
default ProjectRecord; empty owner maps to a local-unowned membership state rather
than a fabricated user; non-empty owners map to stable local actor IDs; project
mismatches are reported and rejected from automatic import. A comparison report and
JSON export permit controlled switch and rollback.

## Migration cost

This adds SQLite schema/bootstrap code, repositories, identity/backfill/compare
services, tests, and narrow composition wiring. Legacy JSON remains untouched and
authoritative until comparison succeeds and the controlled authority state is
explicitly selected.

## Compatibility impact

No Legacy node family, page, URL, provider execution route, or Canvas JSON field is
removed. Unknown Canvas fields are retained in the canonical payload. Existing
`updated_at` checks remain a Legacy compatibility concern; canonical callers use
CanvasRecord.revision.

## Security impact

Authorization is action/resource based at the canonical repository boundary. R3
only establishes local actor/member mappings; it does not claim global
authentication or make LAN mode multi-user safe. Audit payloads exclude provider
secrets and raw credentials.

## Rollback

Before a controlled switch, emit an identity/migration report and JSON export. A
failed comparison leaves Legacy JSON authority unchanged. The canonical store can
be rebuilt from Legacy JSON; switching back uses the validated export adapter and
does not delete source files.

## Acceptance criteria

- Project and Canvas records survive SQLite reopen.
- Logical revision rejects stale canonical mutations independently of timestamps.
- Canonical Canvas mutation and audit/outbox insertion roll back together.
- Identity report covers default, empty owner, non-empty owner, project mismatch,
  and rollback/export.
- Legacy fixtures import and compare losslessly.
- Canonical authorization enforces `project.read` and `canvas.edit` for local
  ProjectMember roles.
- Status documents one explicit authority state and R4 remains forbidden.
