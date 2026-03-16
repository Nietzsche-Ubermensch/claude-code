#!/bin/bash
# auto_pr.sh — pushes branch, PR created via Perplexity MCP
TITLE="${2:-Auto PR}"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
REMOTE_URL=$(git remote get-url origin)
REPO=$(echo "$REMOTE_URL" | sed 's/.*github.com[:/]\(.*\)\.git/\1/')

echo "[INFO] Branch: $BRANCH"
echo "[INFO] Repo: $REPO"
echo "[INFO] Title: $TITLE"
echo "[INFO] Push complete. Ask Perplexity to create PR:"
echo "  → 'create PR: $TITLE'"
