# R0 Task — Repository Truth + Architecture Refresh

Execute R0 only.

Read:

1. `AGENTS.md`
2. `docs/status/CURRENT_EXECUTION_STATUS.md`
3. `CURRENT_ARCHITECTURE.md`
4. `TARGET_ARCHITECTURE.md`
5. `MIGRATION_PLAN.md`
6. `IMPLEMENTATION_PLAN.md`
7. live source/tests

Do not implement product behavior.

Verify:

- live HEAD/worktree
- test baseline
- syntax/static checks
- U0-U7
- Canvas runtime paths
- NodeRecord/EdgeRecord
- NodeCreationService
- NodeMutationService
- GraphMutationService
- RendererRegistry/NodeShell
- current persistence authority
- current project/actor authorization
- provider/model settings
- Codex Exec/App Server state
- security constraints
- latest Canvas benchmark
- possible expected_revision mismatch

Update:

- `docs/status/CURRENT_EXECUTION_STATUS.md`
- `CURRENT_ARCHITECTURE.md` wherever live source/tests prove a current-state statement stale or contradictory

CURRENT_ARCHITECTURE rules:

- describe only what exists now
- do not copy target architecture into it
- separate historical audit metadata from current verified state
- mark unverified claims rather than guessing

Do not change product behavior.

Return:

1. verified facts
2. current-architecture contradictions repaired
3. files changed
4. tests/results
5. known issues
6. blockers
7. exact next authorized Round
8. forbidden next actions
