#!/bin/bash
# watch.sh — continuous health monitor, runs every N minutes
# Usage: watch.sh [interval_minutes]

INTERVAL="${1:-30}"
SCRIPT_DIR="$(dirname "$0")"

echo "[INFO] GitHub Health Watch started"
echo "[INFO] Checking every ${INTERVAL} minutes"
echo "[INFO] Ctrl+C to stop"
echo ""

while true; do
  echo "[$(date '+%H:%M:%S')] Running health check..."
  bash "${SCRIPT_DIR}/health_check.sh" check 2>&1 | grep -E '(✓|✗|~|WARNING|PERFECT|GOOD|NEEDS)'
  echo "[$(date '+%H:%M:%S')] Next check in ${INTERVAL}m"
  sleep $((INTERVAL * 60))
done
