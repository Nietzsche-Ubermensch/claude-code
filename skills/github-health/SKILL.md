# github-health

Autonomous GitHub repository health monitor. Keeps your repo perfect at all times.

## What it does

- Monitors PRs, CI, branches, issues on demand or on a schedule
- Auto-fixes: stale branches, broken workflows, failed CI, missing labels
- Reports repo health score with actionable fixes
- Integrates with github-yolo for auto-push fixes

## Usage

```bash
/github-health          # Full health check
/github-health fix      # Check + auto-fix everything possible
/github-health ci       # CI status only
/github-health prs      # Open PRs status
/github-health clean    # Delete merged/stale branches
```

## Health Checks

| Check | Auto-fix? |
|---|---|
| Failed CI on main | ✅ Push fix commit |
| Open PRs > 7 days | ✅ Add stale label |
| Merged branches not deleted | ✅ Delete branch |
| Broken workflow YAML | ✅ Rewrite workflow |
| Missing .gitignore entries | ✅ Append entries |
| Exposed secrets in commits | ⚠️ Alert only |
| No README | ✅ Generate stub |

## Signal to Perplexity

When a fix requires GitHub API (PR creation, label management, branch deletion),
the script emits a structured signal:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  → Tell Perplexity: [ACTION] [DETAILS]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Perplexity executes the GitHub MCP call immediately.
