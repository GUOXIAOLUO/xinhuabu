# R4 Final Gate Checklist — Multi-Agent Integration

Only the Integration Owner evaluates this checklist against MERGED code.

Unmerged Agent branches do not count as completed architecture.

If any required item lacks evidence:

```text
R4: NOT PASS
```

---

## A0. Local-first / backup boundary

```text
[ ] all normal development evidence comes from local integration branch/worktree
[ ] no Agent pulled/fetched remote state as development authority
[ ] no PR is required for local R4 completion
[ ] any GitHub push/upload occurred only after explicit user backup instruction
[ ] any authorized backup was performed by one designated owner
[ ] local integration branch/worktree remained the implementation source of truth after backup
```

## A. Integration state

```text
[ ] all required task branches merged
[ ] no unresolved semantic ownership locks
[ ] no duplicate implementation kept after conflict resolution
[ ] integration branch tests pass
[ ] task board reflects merged reality
```

## B. Unified product architecture

```text
[ ] one user-visible Canvas entry
[ ] one actual Canvas product runtime
[ ] no permanent Classic product mode
[ ] no permanent Smart product mode
[ ] no hidden dual runtime initialization
```

## C. Persistence

```text
[ ] SQLite normal authority
[ ] one persistence coordination owner
[ ] logical revision verified
[ ] expected revision CAS verified
[ ] stale conflict verified
[ ] restart verified
[ ] rollback verified
[ ] no normal Legacy write mode under SQLite authority
```

## D. Rendering

```text
[ ] one rendering owner
[ ] normal mount unified
[ ] normal update unified
[ ] normal unmount unified
[ ] RendererRegistry canonical
[ ] Legacy renderer compatibility bounded
```

## E. Interaction

```text
[ ] one interaction owner
[ ] pan/zoom
[ ] selection/multi-selection
[ ] drag/resize
[ ] keyboard
[ ] viewport
[ ] connection lifecycle
[ ] no duplicate global listeners
```

## F. Creation

```text
[ ] one normal creation owner
[ ] context menu
[ ] toolbar/command
[ ] file drop
[ ] paste
[ ] workflow import
[ ] Smart Composer migrated
[ ] canonical creation boundary used
```

## G. Graph / Group

```text
[ ] group membership unified
[ ] group move unified
[ ] graph geometry unified
[ ] normal-connect side effects characterized
[ ] no GraphMutationService + raw Canvas double write
```

## H. Media

```text
[ ] one media lifecycle owner
[ ] image/video/audio where supported
[ ] preview/fallback/original
[ ] high-res switching
[ ] playback preservation
[ ] no duplicate player binding
[ ] no media reload storm
```

## I. Legacy readability

```text
[ ] New Canvas readable
[ ] Legacy Classic readable
[ ] Legacy Smart readable
[ ] all use Unified Runtime
```

## J. Clipboard / Workflow

```text
[ ] clipboard/subgraph parity
[ ] workflow import/export parity
[ ] reload parity
```

## K. Performance

```text
[ ] 100-node acceptance
[ ] 300-node acceptance
[ ] DOM duplication inspected
[ ] listener duplication inspected
[ ] duplicate polling/timers/observers inspected
[ ] memory growth inspected
[ ] latency acceptable
```

## L. Runtime removal

```text
[ ] Smart product runtime removed
[ ] Classic duplicate runtime removed
[ ] Smart normal routing removed
[ ] obsolete handoff removed
[ ] duplicate page/CSS removed where Gate permits
[ ] obsolete R4 flags removed
```

## M. Architecture guards

```text
[ ] no WholeHouse branches in Core
[ ] no provider-specific Canvas branches
[ ] no Codex protocol DTO imports in Core
[ ] no new Workbench systems in Legacy monoliths
[ ] no runtime Git hosting dependency
[ ] no duplicate product runtime initialization
```

## N. Documentation truth

```text
[ ] R4_OWNERSHIP_MATRIX matches merged source
[ ] CURRENT_EXECUTION_STATUS matches merged verified truth
[ ] rollback evidence recorded
[ ] acceptance evidence recorded
[ ] no future Round marked current
```

# Final decision

```text
R4: PASS
```

only when all required items are supported by merged evidence.
