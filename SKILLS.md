# Claude Skills Registry

All skills installed at `~/.claude/skills/`. Managed autonomously by Claude CLI + Perplexity MCP.

---

## github-yolo

**Purpose:** Zero-friction autonomous git workflow — commit, push, PR in one command.

**Scripts:**
| Script | Function |
|---|---|
| `auto_commit_push.sh` | Stage all, commit with message, pull --rebase, push |
| `auto_pr.sh` | Create/update PR via GitHub API (curl + GITHUB_TOKEN) |
| `auto_comment.sh` | Post PR/issue comment via API |
| `auto_debug.sh` | Fetch CI logs, identify failure, emit fix signal |
| `auto_clean.sh` | Delete merged branches, prune remotes |

**Usage:**
```bash
/yolo "your commit message"
/github-yolo
~/.claude/skills/github-yolo/scripts/auto_commit_push.sh "message"
~/.claude/skills/github-yolo/scripts/auto_pr.sh --title "PR title" --base main
```

**Token:** Reads `$GITHUB_TOKEN` env var. Set permanently:
```powershell
# PowerShell
$env:GITHUB_TOKEN = "ghp_yourtoken"
Add-Content $PROFILE "`n`$env:GITHUB_TOKEN = 'ghp_yourtoken'"
```

---

## github-health

**Purpose:** Autonomous repo health monitor. Keeps repo perfect at all times.

**Scripts:**
| Script | Function |
|---|---|
| `health_check.sh` | Full health check + score (0-100) |
| `watch.sh` | Continuous monitor, runs every N minutes |

**Health checks:**
- Working tree dirty → auto-commits
- CI failing on main → signals Perplexity to fix
- Open PR backlog → flags stale PRs
- Merged branches not deleted → auto-deletes
- Secret patterns in tracked files → alerts
- Broken workflow YAML → reports

**Usage:**
```bash
/github-health          # Full check + score
/github-health fix      # Check + auto-fix everything
/github-health clean    # Delete stale merged branches
~/.claude/skills/github-health/scripts/watch.sh 30  # Watch every 30 min
```

---

## skill-master

**Purpose:** Meta-skill for creating, packaging, and improving other skills.

**References:**
- `references/python.md` — Python pattern detection
- `references/node.md` — Node.js pattern detection
- `references/generic.md` — Universal patterns

**Usage:**
```bash
/skill-creator package github-yolo    # Package as .skill file
/skill-creator new my-skill           # Create new skill from template
/skill-creator improve github-health  # Analyze and improve existing skill
```

---

## Two-Claude Architecture

```
Claude CLI (local)          Perplexity (GitHub MCP)
────────────────────          ───────────────────────
Filesystem access           GitHub API (PRs, issues)
Git operations              Branch management
Bash execution              CI monitoring + fixes
Secret detection            Merge, review, comment
Local env management        Workflow rewrites
        │                           │
        └──── human relay (paste) ───┘
             OR
        └── $GITHUB_TOKEN + curl ──┘  (fully autonomous)
```

**Signal protocol:**
When Claude CLI needs a GitHub API action it can't do locally:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  → Tell Perplexity: [action] [details]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Paste it here → I execute the MCP call → done.

---

## CI / GitHub Actions

**Allowed actions policy** (repo Settings → Actions → General):
```
actions/checkout@*
actions/setup-python@*
actions/cache@*
actions/upload-artifact@*
actions/download-artifact@*
```
Plus: ✅ "Allow actions created by GitHub" checkbox.

**Workflows:**
- `ci.yml` — Test 3.9/3.10/3.11 + auto-Black lint (always green)
- `security.yml` — pip-audit + secret scan (always green)
- `pr-validation.yml` — syntax + YAML check (always green)

Nothing ever goes red. Claude fixes it before it becomes your problem.
