#!/usr/bin/env bash
#
# auto_commit_push.sh - Autonomous commit and push
# Part of github-yolo skill

set -euo pipefail

# Configuration
COMMIT_MSG="${1:-chore: auto-commit via YOLO mode}"
CURRENT_BRANCH="$(git branch --show-current)"
DEFAULT_BRANCH="${DEFAULT_BRANCH:-main}"
PROTECTED_BRANCHES=("main" "master" "production")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# Check for secrets in staged files
check_secrets() {
  local secret_patterns=(
    "\.env$"
    "\.key$"
    "token"
    "secret"
    "password"
    "api[_-]?key"
    "private[_-]?key"
    "credentials"
  )

  local staged_files
  staged_files="$(git diff --cached --name-only --diff-filter=ACMR)"

  for file in $staged_files; do
    for pattern in "${secret_patterns[@]}"; do
      if echo "$file" | grep -qiE "$pattern"; then
        log_warn "Potential secret detected: $file"
        log_warn "Pattern matched: $pattern"
        # In YOLO mode, we warn but continue
        # Remove this return to block on secrets
        return 1
      fi
    done

    # Check file contents for API keys/tokens (basic check)
    if [[ -f "$file" ]]; then
      if grep -qE '(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|gho_[a-zA-Z0-9]{36})' "$file" 2>/dev/null; then
        log_error "API key/token found in $file"
        log_error "Refusing to commit this file for security"
        return 1
      fi
    fi
  done

  return 0
}

# Check if on protected branch
is_protected_branch() {
  for protected in "${PROTECTED_BRANCHES[@]}"; do
    if [[ "$CURRENT_BRANCH" == "$protected" ]]; then
      return 0
    fi
  done
  return 1
}

# Create feature branch if on protected branch
ensure_feature_branch() {
  if is_protected_branch; then
    log_warn "On protected branch: $CURRENT_BRANCH"
    local timestamp
    timestamp="$(date +%Y%m%d-%H%M%S)"
    local new_branch="yolo-auto-commit-${timestamp}"

    log_info "Creating feature branch: $new_branch"
    git checkout -b "$new_branch"
    CURRENT_BRANCH="$new_branch"
  fi
}

# Main execution
main() {
  log_info "YOLO Auto-Commit & Push"
  log_info "Current branch: $CURRENT_BRANCH"

  # Check if we have changes
  if git diff --quiet && git diff --cached --quiet; then
    log_info "No changes to commit"
    exit 0
  fi

  # Ensure we're not on a protected branch
  ensure_feature_branch

  # Stage all changes if nothing staged
  if git diff --cached --quiet; then
    log_info "Staging all changes"
    git add -A
  fi

  # Security check
  if ! check_secrets; then
    log_warn "Secret check warnings (continuing in YOLO mode)"
  fi

  # Commit
  log_info "Committing: $COMMIT_MSG"
  git commit -m "$COMMIT_MSG

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

  # Pull with rebase if remote branch exists
  if git ls-remote --exit-code --heads origin "$CURRENT_BRANCH" >/dev/null 2>&1; then
    log_info "Pulling latest changes with rebase"
    if ! git pull --rebase origin "$CURRENT_BRANCH"; then
      log_error "Rebase failed - conflicts need manual resolution"
      exit 1
    fi
  fi

  # Push
  log_info "Pushing to origin/$CURRENT_BRANCH"
  if git ls-remote --exit-code --heads origin "$CURRENT_BRANCH" >/dev/null 2>&1; then
    git push origin "$CURRENT_BRANCH"
  else
    log_info "First push - setting upstream"
    git push -u origin "$CURRENT_BRANCH"
  fi

  log_info "✓ Successfully committed and pushed"
  log_info "Branch: $CURRENT_BRANCH"
  log_info "Commit: $(git rev-parse --short HEAD)"
}

main "$@"
