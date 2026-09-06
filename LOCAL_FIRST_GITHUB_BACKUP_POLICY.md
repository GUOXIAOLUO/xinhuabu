# Xinhuabu Local-First + Manual GitHub Backup Policy

## 1. Core rule

Xinhuabu development happens only in the user's local project/worktrees.

```text
LOCAL PROJECT = development source of truth
GitHub = backup / archive destination only
```

Remote GitHub must never become the normal development authority.

---

## 2. Default Agent behavior

Unless the user explicitly asks for a GitHub backup/upload in the current task, every Coding Agent must treat remote operations as disabled.

Default forbidden:

```text
git push
git pull
git fetch
git clone replacement repository
create/update PR
edit GitHub repository files
remote branch synchronization
remote CI as development authority
```

Allowed local operations:

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
local restore / rollback with user work protected
```

---

## 3. Explicit backup exception

GitHub upload is allowed ONLY when the user explicitly issues a backup instruction such as:

```text
上传到 GitHub
备份到 GitHub
把当前本地版本同步到 GitHub 作为备份
```

That permission applies only to the requested backup operation.

After the backup is complete:

```text
remote operations return to DISABLED by default
```

Do not interpret an earlier backup permission as permanent authorization.

---

## 4. Backup semantics

When a GitHub backup is explicitly requested:

```text
LOCAL → GitHub
```

is allowed.

The backup operation must not silently change the local architecture or replace local source truth with remote state.

Do not automatically perform:

```text
git pull
git fetch + merge
remote rebase
reset --hard to remote
remote conflict resolution that discards local work
```

unless the user explicitly asks for that separate operation.

---

## 5. Before backup

Before any explicitly authorized GitHub backup:

```text
git status
git diff --stat
git branch --show-current
git rev-parse HEAD
```

Confirm:

```text
current local branch
local HEAD
dirty/uncommitted files
backup scope
```

Do not silently omit dirty work that the user intended to back up.

Do not silently include unrelated secrets or temporary files.

---

## 6. Secret / sensitive file check

Before GitHub backup, inspect changed/tracked files for likely secrets.

Especially check:

```text
.env
API/.env
API keys
tokens
credentials
private config
local machine paths where sensitive
```

If a likely secret would be uploaded:

```text
STOP the backup
report the exact risk
```

Do not push secrets just because the user said "backup".

---

## 7. Multi-Agent rule

All Coding Agents may develop in local worktrees.

Only one designated Integration/Backup Owner should perform an explicitly requested GitHub backup.

Do not allow multiple Agents to push competing branches simultaneously unless the user explicitly requests that workflow.

Recommended:

```text
local agent worktrees
        ↓
local integration branch
        ↓
local verification
        ↓
USER explicitly says "backup to GitHub"
        ↓
one backup operation
        ↓
remote operations disabled again
```

---

## 8. Source of truth

Always:

```text
current local source
+ verified local tests
+ AGENTS.md
+ authoritative local project docs
```

Never use:

```text
remote main
remote HEAD
GitHub tree
```

as implementation authority unless the user explicitly asks to inspect/compare the backup.

Even after backup, local remains authoritative.

---

## 9. Final principle

GitHub is:

```text
backup
archive
manual synchronization target
```

GitHub is not:

```text
automatic development source
automatic sync authority
automatic CI Gate
automatic merge authority
```
