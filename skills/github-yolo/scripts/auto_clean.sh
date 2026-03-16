#!/usr/bin/env bash
#
# auto_clean.sh - Clean code and git state
# Part of github-yolo skill

set -euo pipefail

MODE="all"
if [[ $# -gt 0 ]]; then
  MODE="$1"
fi

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

clean_branches() {
  log_info "Cleaning branches..."

  # Fetch and prune
  git fetch --prune

  # Get current branch
  local current_branch
  current_branch="$(git branch --show-current)"

  # Delete merged branches (except main, master, and current)
  git branch --merged | grep -vE "main|master|^\*" | xargs -r git branch -d 2>/dev/null || true

  # Delete gone branches
  git branch -vv | grep ': gone]' | awk '{print $1}' | xargs -r git branch -D 2>/dev/null || true

  log_info "✓ Branches cleaned"
}

clean_code() {
  log_info "Cleaning code..."

  # Python formatting
  if command -v ruff &> /dev/null; then
    log_info "Running ruff format..."
    ruff format . 2>/dev/null || true

    log_info "Running ruff check --fix..."
    ruff check --fix . 2>/dev/null || true
  fi

  # TypeScript/JavaScript formatting
  if command -v prettier &> /dev/null; then
    log_info "Running prettier..."
    prettier --write "**/*.{ts,tsx,js,jsx,json,md}" 2>/dev/null || true
  fi

  # ESLint auto-fix
  if command -v eslint &> /dev/null; then
    log_info "Running eslint --fix..."
    eslint --fix --quiet . 2>/dev/null || true
  fi

  log_info "✓ Code cleaned"
}

main() {
  log_info "YOLO Auto-Clean"
  log_info "Mode: $MODE"

  case "$MODE" in
    --branches)
      clean_branches
      ;;
    --code)
      clean_code
      ;;
    --all|*)
      clean_code
      clean_branches
      ;;
  esac

  log_info "✓ Cleanup complete"
}

main "$@"
