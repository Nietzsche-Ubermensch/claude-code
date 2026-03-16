#!/usr/bin/env bash
#
# auto_comment.sh - Auto-comment on issues/PRs
# Part of github-yolo skill

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: auto_comment.sh <issue_or_pr_number> <comment_text>"
  exit 1
fi

ISSUE_NUMBER="$1"
COMMENT="$2"

GREEN='\033[0;32m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }

main() {
  log_info "YOLO Auto-Comment"
  log_info "Target: #$ISSUE_NUMBER"

  # Try as PR first, fall back to issue
  if gh pr view "$ISSUE_NUMBER" &>/dev/null; then
    log_info "Commenting on PR #$ISSUE_NUMBER"
    gh pr comment "$ISSUE_NUMBER" --body "$COMMENT"
  else
    log_info "Commenting on issue #$ISSUE_NUMBER"
    gh issue comment "$ISSUE_NUMBER" --body "$COMMENT"
  fi

  log_info "✓ Comment posted"
}

main "$@"
