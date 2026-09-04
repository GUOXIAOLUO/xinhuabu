# R3 Task — Project Identity + Canonical Canvas Persistence

Execute R3 only after R2 explicitly authorizes it.

Goal:

Create canonical Project/Canvas authority required before U7.

Deliver:

- ProjectRecord
- ProjectMember/local actor mapping
- CanvasRecord with logical revision
- action/resource AuthorizationService seam
- SQLite migration runner/repositories
- Legacy import/backfill/compare
- explicit authority state
- transactional domain mutation + durable audit/outbox
- migration reports
- rollback/export mapping

Test Legacy identity:

- project="default"
- owner=""
- non-empty owner
- project mismatch
- rollback

Rules:

- no silent owner invention
- CanvasRecord.revision != updated_at
- NodeRecord v1 remains compatible
- do not remove source Canvas runtimes/pages
- do not implement Skill/Model/Execution platform features

Gate:

- Project/Canvas persist across restart
- revision/stale-write behavior verified
- Legacy fixtures compare
- ownership mapping/report verified
- canonical mutation + audit atomic
- authorization actions enforced
- rollback available
- status authorizes R4
