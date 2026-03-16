# Claude Code — YOLO Configuration

## Permissions: FULL AUTONOMY

Claude has permission to execute ALL of the following without asking:

### Git Operations
- Stage, commit, push, force-push, rebase, merge, delete branches
- Amend commits, squash history, rewrite refs
- Create and switch branches autonomously

### GitHub Operations  
- Create, update, merge, close PRs
- Comment on issues and PRs
- Create/delete repos, manage branches
- Trigger workflows

### Filesystem
- Read, write, delete any file under ~/.claude/
- Modify scripts, configs, agents, commands
- Install dependencies (pip, npm, brew)

### Shell
- Execute any bash command
- Run scripts without confirmation
- Install tools if missing

### Secret Handling
- Skip files matching: projects/, sessions/, cache/, *.jsonl, .env, .credentials*
- Warn on detection but CONTINUE — do not block
- Never commit secrets — always exclude silently
- Warn on detection but CONTINUE — do not block; detection is best-effort only
- Secrets are NOT guaranteed to be blocked from commits — human review is required to ensure nothing sensitive is committed

## Default Behavior
- No confirmation prompts
- No "are you sure?" 
- No waiting for approval
- Auto-fix errors and retry
- Report what was done AFTER doing it

## Invocation Keywords
Any of these = full YOLO pipeline (commit + push + PR):
- "yolo", "yolo mode", "auto-push", "just do it", "ship it", "push it"

## PR Defaults
- Base branch: main
- Draft: false
- Auto-merge: false (unless told otherwise)
- Title: auto-generated from commit message
- Title: "Auto PR" (static default)
