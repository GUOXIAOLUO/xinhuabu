# Agent Task

## Identity

```text
Task ID:
Agent ID:
Agent tool:
Branch:
Worktree:
Base commit:
```

## Status

```text
READY | LOCKED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | MERGED | REJECTED
```

## Execution boundary

```text
LOCAL-FIRST
remote operations disabled by default
GitHub backup only on explicit user request
```

## Authorized Round

```text
R4 — Unified Canvas Cutover
```

## Ownership Unit

```text
semantic owner:
before owner:
target owner:
```

## Goal

Describe ONE bounded ownership migration.

## Dependencies

```text
depends_on:
blocks:
```

## Scope

### Allowed files

```text
-
```

### Forbidden files

```text
-
```

## Required characterization

```text
current behavior:
legacy side effects:
tests covering behavior:
```

## Implementation rule

```text
characterize
→ seam
→ delegate
→ verify
→ migrate owner
→ remove duplicate responsibility
```

## Acceptance

```text
[ ] behavior preserved
[ ] ownership moved
[ ] duplicate owner reduced/removed
[ ] targeted tests pass
[ ] required regression passes
[ ] no future Round leakage
[ ] no unrelated cleanup
```

## Completion report

```text
Before owner:
After owner:
Classic responsibility removed:
Smart responsibility removed:
Unified responsibility added:
Files changed:
Tests:
Unexpected diff:
Remaining risks:
Recommended merge order:
```
