# Xinhuabu Local-Only Development Policy

## Hard rule

All development happens only in the user's local Xinhuabu project.

Remote Git hosting is outside the execution boundary.

## Forbidden

```text
git push
git pull
git fetch
GitHub/GitLab PR creation
remote file editing
remote branch synchronization
remote CI as a required Gate
remote repository as source of truth
```

## Allowed local Git operations

```text
git status
git diff
git log
git branch
git worktree
git add
git commit
git merge
coordinated local rebase
local restore/rollback that preserves user work
```

## Multi-Agent topology

Recommended:

```text
local integration worktree
├── local worktree: agent/codex/...
├── local worktree: agent/zcode/...
├── local worktree: agent/claude/...
└── local worktree: agent/review/...
```

All branches and worktrees remain local.

## Source of truth

```text
current local source
+ verified local tests
+ AGENTS.md
+ authoritative local project docs
```

Never:

```text
remote main
remote HEAD
GitHub tree
```

as implementation authority.

## Final delivery

R4 completion means the local integration branch/worktree passes the complete local Gate.

Publishing or syncing the result to a remote repository is a separate user decision and is not part of this development contract.
