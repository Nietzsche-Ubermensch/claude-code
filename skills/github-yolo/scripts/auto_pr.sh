#!/bin/bash
# auto_pr.sh — Fully autonomous PR creation via GitHub API (no gh CLI needed)
# Usage: auto_pr.sh --title "PR title" [--base main] [--draft]

set -euo pipefail

# ── JSON escape function ──────────────────────────────────────────────────────
json_escape() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/	/\\t/g' | awk '{printf "%s\\n", $0}' | sed '$ s/\\n$//'
}

# ── Parse args ────────────────────────────────────────────────────────────────
TITLE="Auto PR"
BASE="main"
DRAFT="false"
#!/usr/bin/env bash
# auto_pr.sh — prints git state and PR handoff instructions for Perplexity MCP
TITLE="Auto PR"
POSITIONAL_TITLE=""

# Parse arguments: support --title/-t and a single positional title
while [[ $# -gt 0 ]]; do
  case $1 in
    --title) TITLE="$2"; shift 2 ;;
    --base)  BASE="$2";  shift 2 ;;
    --draft) DRAFT="true"; shift ;;
    *) shift ;;
  esac
done

# ── Detect repo + branch ──────────────────────────────────────────────────────
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE_URL=$(git remote get-url origin)
REPO=$(echo "$REMOTE_URL" | sed 's/.*github.com[:/]//; s/\.git$//')

echo "[INFO] YOLO Auto-PR"
echo "[INFO] Branch : $BRANCH"
echo "[INFO] Base   : $BASE"
echo "[INFO] Repo   : $REPO"
echo "[INFO] Title  : $TITLE"

# ── Resolve GitHub token ──────────────────────────────────────────────────────
TOKEN=""
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
  TOKEN="$GITHUB_TOKEN"
elif command -v gh &>/dev/null; then
  TOKEN=$(gh auth token 2>/dev/null || true)
fi

if [[ -z "$TOKEN" ]]; then
  echo "[WARN] No GitHub token found. Set GITHUB_TOKEN env var or run: gh auth login"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  → Tell Perplexity: create PR \"$TITLE\""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  exit 0
fi

# ── Build PR body from commits ────────────────────────────────────────────────
BODY=$(git log "${BASE}..${BRANCH}" --pretty=format:"- %s" 2>/dev/null | head -20 || echo "Auto-generated PR")

# ── Check for existing PR ─────────────────────────────────────────────────────
EXISTING=$(curl -sf \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/${REPO}/pulls?head=${BRANCH}&base=${BASE}&state=open" \
  2>/dev/null | grep '"number"' | head -1 | grep -o '[0-9]*' || true)

if [[ -n "$EXISTING" ]]; then
  echo "[INFO] PR #$EXISTING already exists — updating title"

  # Build JSON with escaped strings
  TITLE_ESC=$(json_escape "$TITLE")
  BODY_ESC=$(json_escape "$BODY")
  PAYLOAD="{\"title\":\"${TITLE_ESC}\",\"body\":\"${BODY_ESC}\"}"

  curl -sf -X PATCH \
    -H "Authorization: Bearer $TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "Content-Type: application/json" \
    "https://api.github.com/repos/${REPO}/pulls/${EXISTING}" \
    -d "$PAYLOAD" > /dev/null
  echo "[INFO] ✓ PR #$EXISTING updated"
  echo "[INFO] → https://github.com/${REPO}/pull/${EXISTING}"
  exit 0
fi

# ── Create PR ─────────────────────────────────────────────────────────────────
# Build JSON with escaped strings
TITLE_ESC=$(json_escape "$TITLE")
BRANCH_ESC=$(json_escape "$BRANCH")
BASE_ESC=$(json_escape "$BASE")
BODY_ESC=$(json_escape "$BODY")
PAYLOAD="{\"title\":\"${TITLE_ESC}\",\"head\":\"${BRANCH_ESC}\",\"base\":\"${BASE_ESC}\",\"body\":\"${BODY_ESC}\",\"draft\":${DRAFT}}"

RESPONSE=$(curl -sf -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/${REPO}/pulls" \
  -d "$PAYLOAD" \
  2>/dev/null)

PR_URL=$(echo "$RESPONSE" | grep '"html_url"' | head -1 | sed 's/.*"html_url": "//; s/".*//')
PR_NUM=$(echo "$RESPONSE" | grep '"number"' | head -1 | grep -o '[0-9]*')

if [[ -n "$PR_URL" ]]; then
  echo "[INFO] ✓ PR #${PR_NUM} created"
  echo "[INFO] → $PR_URL"
else
  echo "[WARN] API call failed — falling back to Perplexity relay"
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  → Tell Perplexity: create PR \"$TITLE\""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi
  case "$1" in
    --title|-t)
      if [[ -n "${2:-}" && ! "$2" =~ ^- ]]; then
        TITLE="$2"
        shift 2
        continue
      fi
      shift
      ;;
    -*)
      # Ignore other flags for title purposes
      shift
      ;;
    *)
      if [[ -z "$POSITIONAL_TITLE" ]]; then
        POSITIONAL_TITLE="$1"
      fi
      shift
      ;;
  esac
done

if [[ "$TITLE" == "Auto PR" && -n "$POSITIONAL_TITLE" ]]; then
  TITLE="$POSITIONAL_TITLE"
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE_URL=$(git remote get-url origin)

# Extract "owner/repo" from common git remote URL formats.
# Handles:
#   - git@host:owner/repo(.git)
#   - ssh://git@host/owner/repo(.git)
#   - https://host/owner/repo(.git)
REPO=""
if [[ "$REMOTE_URL" =~ ^git@[^:]+:([^[:space:]]+?)(\.git)?$ ]]; then
  REPO="${BASH_REMATCH[1]}"
elif [[ "$REMOTE_URL" =~ ^ssh://git@[^/]+/([^[:space:]]+?)(\.git)?$ ]]; then
  REPO="${BASH_REMATCH[1]}"
elif [[ "$REMOTE_URL" =~ ^https?://[^/]+/([^[:space:]]+?)(\.git)?$ ]]; then
  REPO="${BASH_REMATCH[1]}"
fi

# Fall back to showing the full remote URL if we couldn't parse owner/repo.
if [[ -z "$REPO" ]]; then
  echo "[WARN] Could not parse owner/repo from remote URL: $REMOTE_URL" >&2
  REPO="$REMOTE_URL"
fi

echo "[INFO] Branch: $BRANCH"
echo "[INFO] Repo: $REPO"
echo "[INFO] Title: $TITLE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  → Tell Perplexity: create PR \"$TITLE\""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
