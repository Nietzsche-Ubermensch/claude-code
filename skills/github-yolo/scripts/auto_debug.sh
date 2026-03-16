#!/usr/bin/env bash
#
# auto_debug.sh - Autonomous error fixing
# Part of github-yolo skill

set -euo pipefail

ERROR_LOG="${1:-}"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

# Find error logs if not specified
find_error_logs() {
  # Check common locations
  local logs=()

  # GitHub Actions logs (if in CI)
  if [[ -f ".github/workflows/ci.log" ]]; then
    logs+=(".github/workflows/ci.log")
  fi

  # pytest output
  if [[ -f "pytest.log" ]]; then
    logs+=("pytest.log")
  fi

  # npm test output
  if [[ -f "npm-debug.log" ]]; then
    logs+=("npm-debug.log")
  fi

  # Last git commit message might mention errors
  local last_commit_msg
  last_commit_msg="$(git log -1 --pretty=%B 2>/dev/null || echo '')"

  echo "${logs[@]}"
}

# Read errors from log
read_errors() {
  local log_file="$1"

  if [[ ! -f "$log_file" ]]; then
    log_error "Log file not found: $log_file"
    return 1
  fi

  # Extract error patterns
  grep -E "(Error|error|ERROR|FAILED|failed|✗)" "$log_file" || true
}

# Fix unused imports (Python)
fix_python_unused_imports() {
  log_info "Fixing unused Python imports..."

  # Use ruff to remove unused imports
  if command -v ruff &> /dev/null; then
    ruff check --select F401 --fix . 2>/dev/null || true
  fi
}

# Fix unused imports (TypeScript/JavaScript)
fix_js_unused_imports() {
  log_info "Fixing unused TypeScript/JavaScript imports..."

  # Use eslint --fix
  if command -v eslint &> /dev/null; then
    eslint --fix --quiet . 2>/dev/null || true
  fi
}

# Auto-format code
auto_format() {
  log_info "Auto-formatting code..."

  # Python
  if command -v ruff &> /dev/null; then
    ruff format . 2>/dev/null || true
  fi

  # TypeScript/JavaScript
  if command -v prettier &> /dev/null; then
    prettier --write "**/*.{ts,tsx,js,jsx}" 2>/dev/null || true
  fi
}

main() {
  log_info "YOLO Auto-Debug"

  # Find error logs
  if [[ -z "$ERROR_LOG" ]]; then
    local logs
    logs="$(find_error_logs)"

    if [[ -z "$logs" ]]; then
      log_info "No error logs found, running general cleanup"
      fix_python_unused_imports
      fix_js_unused_imports
      auto_format
      log_info "✓ General cleanup complete"
      exit 0
    fi

    ERROR_LOG="${logs%% *}"  # Use first log
  fi

  log_info "Reading errors from: $ERROR_LOG"
  local errors
  errors="$(read_errors "$ERROR_LOG")"

  if [[ -z "$errors" ]]; then
    log_info "No errors found in log"
    exit 0
  fi

  log_info "Applying fixes..."

  # Apply fixes based on error patterns
  if echo "$errors" | grep -q "unused import"; then
    fix_python_unused_imports
    fix_js_unused_imports
  fi

  # Always auto-format as final step
  auto_format

  log_info "✓ Fixes applied"
  log_info "Run tests to verify fixes"
}

main "$@"
