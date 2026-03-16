# YOLO Mode

Activate autonomous GitHub workflow. No confirmations. No hand-holding.

## What happens in YOLO mode:
1. Stage all changes (respecting .gitignore)
2. Detect and skip secrets automatically
3. Commit with a semantic message you provide (or auto-generate one)
4. Push to current branch
5. Create or update PR if one doesn't exist

## Usage:
/yolo "your commit message"
/yolo  ← auto-generates commit message from diff

## Invocation:
When user says "yolo", "yolo mode", "auto-push", or invokes /yolo:
- Run: ~/.claude/skills/github-yolo/scripts/auto_commit_push.sh "$MESSAGE"
- Then: ~/.claude/skills/github-yolo/scripts/auto_pr.sh --title "$PR_TITLE"
- Report: branch, commit SHA, PR URL
- Do NOT ask for confirmation at any step

## Rules:
- Never ask "are you sure?"
- Never pause for approval mid-flow
- If secrets detected: skip those files, warn, continue
- If push fails: diagnose and fix automatically
- If PR exists: update it, don't create duplicate
