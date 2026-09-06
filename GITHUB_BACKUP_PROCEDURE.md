# GitHub Backup Procedure — Manual Trigger Only

This file is used only when the user explicitly requests:

```text
上传到 GitHub
备份到 GitHub
同步当前本地版本到 GitHub 作为备份
```

## Before backup

Run locally:

```text
git status
git diff --stat
git branch --show-current
git rev-parse HEAD
```

Confirm the intended local integration branch and backup scope.

## Safety check

Before upload:

```text
check .env / API/.env
check likely API keys/tokens
check credentials
check temporary/local-only files
```

If secrets are likely included:

```text
STOP
report risk
do not upload
```

## Backup direction

Allowed:

```text
LOCAL verified integration state
        ↓
GitHub backup
```

Do not automatically:

```text
pull
fetch + merge
reset to remote
rebase onto remote
```

A backup request is not permission for remote-to-local synchronization.

## After backup

Report:

```text
local branch
local HEAD
backup target
backup result
```

Then restore policy:

```text
REMOTE OPERATIONS DISABLED BY DEFAULT
```

Local remains the source of truth.
