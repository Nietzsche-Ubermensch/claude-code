#!/usr/bin/env bash
# auto_pr.sh — prints git state and PR handoff instructions for Perplexity MCP
TITLE="Auto PR"
POSITIONAL_TITLE=""

# Parse arguments: support --title/-t and a single positional title
while [[ $# -gt 0 ]]; do
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
