#!/usr/bin/env bash
#
# auto_pr.sh - Autonomous PR creation/update
# Part of github-yolo skill

set -euo pipefail

# Parse arguments
TITLE=""
BODY=""
DRAFT=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --title)
      TITLE="$2"
      shift 2
      ;;
    --body)
      BODY="$2"
      shift 2
      ;;
    --draft)
      DRAFT=true
      shift
      ;;
    *)
      shift
      ;;
  esac
done

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

CURRENT_BRANCH="$(git branch --show-current)"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"

# Generate title from commits if not provided
generate_title() {
  local recent_commit
  recent_commit="$(git log --oneline -1 --pretty=format:%s)"

  # Clean up commit message for PR title
  echo "$recent_commit" | sed 's/^[a-z]*: //' | sed 's/^[A-Z]/\U&/'
}

# Generate body from template or commits
generate_body() {
  if [[ -f ".github/PULL_REQUEST_TEMPLATE.md" ]]; then
    cat ".github/PULL_REQUEST_TEMPLATE.md"
  elif [[ -f ".github/pr-body.md" ]]; then
    cat ".github/pr-body.md"
  else
    echo "## Changes"
    echo ""
    git log --oneline --pretty=format:"- %s" "$DEFAULT_BRANCH..$CURRENT_BRANCH" | head -10
    echo ""
    echo ""
    echo "## Files Changed"
    echo ""
    git diff --name-status "$DEFAULT_BRANCH...$CURRENT_BRANCH" | head -20
  fi
}

# Check if PR exists for current branch
pr_exists() {
  gh pr list --head "$CURRENT_BRANCH" --json number --jq '.[0].number' 2>/dev/null || echo ""
}

main() {
  log_info "YOLO Auto-PR"
  log_info "Current branch: $CURRENT_BRANCH"

  # Auto-generate title/body if not provided
  if [[ -z "$TITLE" ]]; then
    TITLE="$(generate_title)"
    log_info "Auto-generated title: $TITLE"
  fi

  if [[ -z "$BODY" ]]; then
    BODY="$(generate_body)"
    log_info "Using auto-generated body"
  fi

  # Check if PR exists
  existing_pr="$(pr_exists)"

  if [[ -n "$existing_pr" ]]; then
    log_info "PR #$existing_pr already exists for this branch"
    log_info "Updating PR..."

    # Update PR
    gh pr edit "$existing_pr" \
      --title "$TITLE" \
      --body "$BODY"

    log_info "✓ PR #$existing_pr updated"
    gh pr view "$existing_pr" --web 2>/dev/null || true
  else
    log_info "Creating new PR..."

    # Create PR
    local pr_args=(
      "--title" "$TITLE"
      "--body" "$BODY"
      "--base" "$DEFAULT_BRANCH"
    )

    if [[ "$DRAFT" == "true" ]]; then
      pr_args+=("--draft")
    fi

    pr_url="$(gh pr create "${pr_args[@]}")"

    log_info "✓ PR created: $pr_url"
    gh pr view --web 2>/dev/null || true
  fi
}

main "$@"
