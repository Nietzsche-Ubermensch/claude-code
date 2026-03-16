# YOLO Mode

Activate autonomous GitHub workflow. No confirmations. No hand-holding.

## What happens in YOLO mode:
1. Stage all changes (respecting .gitignore)
2. Scan for potential secrets in filenames and print warnings (does not block commit)
3. Commit with a semantic message you provide (or auto-generate one)
4. Push to current branch
5. Trigger Perplexity MCP handoff for PR creation/update (no direct PR operations here)

## Usage:
/yolo "your commit message"
/yolo  ← auto-generates commit message from diff

## Invocation:
When user says "yolo", "yolo mode", "auto-push", or invokes /yolo:
- Run: ~/.claude/skills/github-yolo/scripts/auto_commit_push.sh "$MESSAGE"
- Then: ~/.claude/skills/github-yolo/scripts/auto_pr.sh --title "$PR_TITLE" (emits Perplexity MCP handoff instructions)
- Report: branch, commit SHA, and any PR or handoff information returned by the MCP integration
- Do NOT ask for confirmation at any step

## Rules:
- Never ask "are you sure?"
- Never pause for approval mid-flow
- If potential secrets detected: warn and continue (current implementation does not automatically skip files)
- If push fails: diagnose and fix automatically
- PR creation/update is handled by the downstream Perplexity MCP integration; this workflow does not call GitHub PR APIs directly
