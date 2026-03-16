#!/bin/bash
# github-health: Autonomous repo health monitor
# Usage: health_check.sh [fix|ci|prs|clean]

set -euo pipefail

MODE="${1:-check}"
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
REPO=$(echo "$REMOTE_URL" | sed 's/.*github.com[:/]//; s/\.git$//')
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
TOKEN="${GITHUB_TOKEN:-}"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║     GitHub Health Monitor            ║"
echo "╚══════════════════════════════════════╝"
echo "[INFO] Repo   : $REPO"
echo "[INFO] Branch : $BRANCH"
echo "[INFO] Mode   : $MODE"
echo ""

SCORE=100
ISSUES=()

# ── Helper ──────────────────────────────────────────────────────────────────
signal() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  → Tell Perplexity: $1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

api() {
  if [[ -z "$TOKEN" ]]; then echo "{}"; return; fi
  curl -sf -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/${REPO}/$1" 2>/dev/null || echo "{}"
}

# ── Check: git status ───────────────────────────────────────────────────────
check_dirty() {
  if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
    ISSUES+=("Uncommitted changes in working tree")
    SCORE=$((SCORE - 5))
    if [[ "$MODE" == "fix" ]]; then
      echo "[FIX] Staging and committing dirty files..."
      git add -A
      ~/.claude/skills/github-yolo/scripts/auto_commit_push.sh "chore: auto-commit dirty working tree" 2>/dev/null || true
    fi
  else
    echo "[✓] Working tree clean"
  fi
}

# ── Check: main branch CI ───────────────────────────────────────────────────
check_ci() {
  echo "[CHECK] CI status on main..."
  local STATUS
  STATUS=$(api "commits/main/status" | grep '"state"' | head -1 | sed 's/.*"state": "//; s/".*//')
  if [[ "$STATUS" == "failure" ]]; then
    ISSUES+=("CI failing on main")
    SCORE=$((SCORE - 20))
    echo "[✗] CI FAILING on main"
    signal "check CI on main and fix failures"
  elif [[ "$STATUS" == "success" ]]; then
    echo "[✓] CI passing on main"
  else
    echo "[~] CI status: ${STATUS:-unknown}"
  fi
}

# ── Check: open PRs ─────────────────────────────────────────────────────────
check_prs() {
  echo "[CHECK] Open PRs..."
  local COUNT
  COUNT=$(api "pulls?state=open&per_page=100" | grep -c '"number"' 2>/dev/null || echo "0")
  if [[ "$COUNT" -gt 5 ]]; then
    ISSUES+=("$COUNT open PRs — review backlog building")
    SCORE=$((SCORE - 10))
    echo "[✗] $COUNT open PRs"
    signal "list open PRs and flag any older than 7 days"
  else
    echo "[✓] $COUNT open PRs (healthy)"
  fi
}

# ── Check: stale merged branches ────────────────────────────────────────────
check_branches() {
  echo "[CHECK] Stale merged branches..."
  local STALE
  STALE=$(git branch -r --merged main 2>/dev/null | grep -v 'HEAD\|main\|master' | wc -l | tr -d ' ')
  if [[ "$STALE" -gt 0 ]]; then
    ISSUES+=("$STALE merged remote branches not deleted")
    SCORE=$((SCORE - 5))
    echo "[✗] $STALE stale merged branches"
    if [[ "$MODE" == "fix" ]] || [[ "$MODE" == "clean" ]]; then
      git branch -r --merged main | grep -v 'HEAD\|main\|master' | sed 's/origin\///' | while read -r b; do
        echo "[FIX] Deleting merged branch: $b"
        git push origin --delete "$b" 2>/dev/null || true
      done
    fi
  else
    echo "[✓] No stale merged branches"
  fi
}

# ── Check: secrets in env ───────────────────────────────────────────────────
check_secrets() {
  echo "[CHECK] Exposed secrets..."
  local FOUND=0
  # Check for common secret patterns in tracked files
  if git grep -rE '(ghp_[A-Za-z0-9]{36}|AKIA[A-Z0-9]{16}|sk-[A-Za-z0-9]{48})' \
    -- ':(exclude).git' 2>/dev/null | grep -v '.gitignore' | head -1 | grep -q .; then
    FOUND=1
  fi
  if [[ "$FOUND" -eq 1 ]]; then
    ISSUES+=("⚠️  POSSIBLE SECRET EXPOSED in tracked files")
    SCORE=$((SCORE - 30))
    echo "[✗] WARNING: Possible secret pattern found in tracked files"
    signal "scan repo for exposed secrets and report findings"
  else
    echo "[✓] No exposed secrets detected"
  fi
}

# ── Check: workflow health ───────────────────────────────────────────────────
check_workflows() {
  echo "[CHECK] Workflow files..."
  local BAD=0
  find .github/workflows/ -name '*.yml' 2>/dev/null | while read -r f; do
    python3 -c "import yaml; yaml.safe_load(open('$f'))" 2>/dev/null || {
      echo "[✗] Invalid YAML: $f"
      BAD=$((BAD+1))
    }
  done
  if [[ "$BAD" -eq 0 ]]; then
    echo "[✓] All workflow files valid"
  fi
}

# ── Run checks ──────────────────────────────────────────────────────────────
check_dirty
check_workflows
[[ "$MODE" != "clean" ]] && check_ci
[[ "$MODE" != "clean" ]] && check_prs
check_branches
check_secrets

# ── Health Score ────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════╗"
if [[ "$SCORE" -ge 90 ]]; then
  echo "║  Health Score: ${SCORE}/100  ✅ PERFECT     ║"
elif [[ "$SCORE" -ge 70 ]]; then
  echo "║  Health Score: ${SCORE}/100  ⚠️  GOOD        ║"
else
  echo "║  Health Score: ${SCORE}/100  ❌ NEEDS WORK  ║"
fi
echo "╚══════════════════════════════════════╝"

if [[ ${#ISSUES[@]} -gt 0 ]]; then
  echo ""
  echo "Issues found:"
  for i in "${ISSUES[@]}"; do
    echo "  • $i"
  done
  echo ""
  if [[ "$MODE" != "fix" ]]; then
    echo "Run '/github-health fix' to auto-fix all issues"
  fi
else
  echo ""
  echo "  Repo is perfect. Nothing to fix."
fi
