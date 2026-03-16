---
name: github-yolo
description: Autonomous GitHub operations with automatic approval (YOLO mode). Handles commits, pushes, PRs, issue comments, debugging, code cleanup, and git workflows without permission prompts. Use when user wants autonomous GitHub workflow, says "yolo mode", "auto-push", "auto-commit", "just push it", "handle GitHub automatically", or needs hands-free git operations.
---

# GitHub YOLO Mode

Autonomous GitHub operations with automatic approval. Handles the complete workflow from code changes to deployed PRs without permission prompts.

## Core Capabilities

1. **Auto-commit & Push** - Commit all changes and push to remote
2. **Auto-PR Management** - Create or update pull requests automatically
3. **Auto-commenting** - Comment on issues and PRs
4. **Auto-debugging** - Read errors, fix code, commit fixes
5. **Auto-cleanup** - Format code, clean branches, remove dead code
6. **Git workflow automation** - Pull, rebase, merge, resolve conflicts

## When to Use

Trigger this skill when:
- User says "yolo mode", "auto-push", "just commit and push"
- User wants hands-free GitHub workflow
- User says "handle it automatically", "don't ask me"
- User wants to fix all issues and push without interruption
- User needs rapid iteration without approval friction

## Safety Guardrails

Even in YOLO mode, preserve these safeguards:

1. **Never force push to main/master** - Always create a feature branch
2. **Never commit secrets** - Check for `.env`, `*.key`, `*token*`, API keys
3. **Never delete main/master branch** - Protected branches remain protected
4. **Always create backups** - Use `git stash` before destructive operations
5. **Verify remote exists** - Don't push to non-existent remotes

## Workflow Patterns

### Pattern 1: Fix and Ship

```bash
# 1. Fix all issues
scripts/auto_debug.sh

# 2. Clean and format
scripts/auto_clean.sh

# 3. Commit and push
scripts/auto_commit_push.sh "fix: address all review comments"

# 4. Update PR
scripts/auto_pr.sh
```

### Pattern 2: Create Feature PR

```bash
# 1. Create feature branch
git checkout -b feat/new-feature

# 2. Make changes (already done)

# 3. Commit and push
scripts/auto_commit_push.sh "feat: implement new feature"

# 4. Create PR
scripts/auto_pr.sh --title "Add new feature" --body "$(cat .github/pr-body.md)"
```

### Pattern 3: Address PR Comments

```bash
# 1. Read PR comments
gh pr view --comments

# 2. Fix each issue automatically
scripts/auto_debug.sh

# 3. Commit and push
scripts/auto_commit_push.sh "fix: address PR review comments"

# 4. Comment on PR
scripts/auto_comment.sh "All review comments addressed"
```

## Scripts Reference

### auto_commit_push.sh

Commits all changes and pushes to remote.

**Usage:**
```bash
scripts/auto_commit_push.sh [commit_message]
```

**Default message:** "chore: auto-commit via YOLO mode"

**Safety checks:**
- Warns if committing to main/master (but proceeds if user confirmed YOLO mode)
- Scans for secrets in staged files
- Creates feature branch if on main/master
- Pulls with rebase before pushing

### auto_pr.sh

Creates or updates pull request automatically.

**Usage:**
```bash
scripts/auto_pr.sh [--title "Title"] [--body "Body"] [--draft]
```

**Behavior:**
- Detects if PR exists for current branch
- Updates existing PR or creates new one
- Uses `.github/PULL_REQUEST_TEMPLATE.md` if no body provided
- Auto-generates title from recent commits if not provided

### auto_comment.sh

Comments on issues or PRs.

**Usage:**
```bash
scripts/auto_comment.sh <issue_or_pr_number> <comment_text>
```

**Features:**
- Supports both issues and PRs
- Can mention users with `@username`
- Supports markdown formatting

### auto_debug.sh

Reads errors from recent runs and attempts automatic fixes.

**Usage:**
```bash
scripts/auto_debug.sh [error_log_file]
```

**Process:**
1. Read error logs (from CI, local tests, or specified file)
2. Identify error patterns (import errors, type errors, test failures)
3. Apply automated fixes:
   - Remove unused imports
   - Add missing imports
   - Fix type annotations
   - Update test assertions
4. Run tests to verify fixes
5. Commit if fixes successful

**Error patterns handled:**
- Unused imports → Remove
- Missing imports → Add
- Type mismatches → Fix annotations
- Test failures → Update assertions (with caution)
- Linting errors → Auto-format

### auto_clean.sh

Cleans up code and git state.

**Usage:**
```bash
scripts/auto_clean.sh [--branches] [--code] [--all]
```

**Operations:**
- `--branches`: Remove merged branches, prune remote refs
- `--code`: Format code (ruff, prettier, etc.), remove dead code
- `--all`: Both branches and code

**Code cleanup:**
- Run formatters (ruff format, prettier, etc.)
- Remove unused imports
- Remove commented code blocks
- Fix trailing whitespace

**Branch cleanup:**
- Delete merged local branches
- Prune `[gone]` branches
- Clean up stale remote refs

## GitHub API Integration

Uses `gh` CLI for all GitHub operations. Requires authentication:

```bash
gh auth login
gh auth status
```

### Common Commands

```bash
# Create PR
gh pr create --title "Title" --body "Body" --base main

# Update PR
gh pr edit <number> --title "New Title" --body "New Body"

# Comment on issue
gh issue comment <number> --body "Comment"

# Comment on PR
gh pr comment <number> --body "Comment"

# View PR comments
gh pr view <number> --comments
```

## Configuration

Optional config file: `~/.claude/skills/github-yolo/config.json`

```json
{
  "autoApprove": true,
  "defaultBranch": "main",
  "protectedBranches": ["main", "master", "production"],
  "commitMessagePrefix": "chore: ",
  "alwaysCreateFeatureBranch": true,
  "secretPatterns": [
    ".env",
    "*.key",
    "*token*",
    "*secret*",
    "*password*"
  ]
}
```

## Error Handling

### Push Rejected

```bash
# Auto-pull with rebase
git pull --rebase origin $(git branch --show-current)
# Retry push
git push
```

### Merge Conflicts

```bash
# Stash changes
git stash
# Pull latest
git pull
# Reapply changes
git stash pop
# Auto-resolve conflicts (take ours/theirs based on context)
# Commit resolution
```

### PR Already Exists

```bash
# Update existing PR instead of creating new one
gh pr edit <number> --title "Updated Title"
```

## Usage Examples

### Example 1: Fix All Review Comments

```
User: "Fix all the review comments and push"
Claude response: *Enables YOLO mode, reads PR comments, fixes all issues*

Steps taken:
1. Read PR #1444 comments via `gh pr view 1444 --comments`
2. Fix unused imports → Edit files to remove
3. Add API key validation → Edit thermo_executor.py
4. Fix streaming bugs → Edit session.py
5. Add tests → Write new test file
6. Commit: "fix: address all PR review comments"
7. Push to origin/feat/thermodynamic-cli
8. Comment on PR: "All 28 review comments have been addressed"
```

### Example 2: Create and Ship Feature

```
User: "yolo mode - create the new authentication module and ship it"

Claude response: *Autonomous feature implementation*

Steps taken:
1. Create feature branch: feat/auth-module
2. Generate auth module code
3. Write tests
4. Run tests → all passing
5. Format code with ruff
6. Commit: "feat: add authentication module"
7. Push to origin/feat/auth-module
8. Create PR with auto-generated description
9. Return PR URL: #1445
```

### Example 3: Emergency Hotfix

```
User: "production is down, fix the null pointer bug and deploy NOW"

Claude response: *Emergency fix workflow*

Steps taken:
1. Create hotfix branch from main
2. Identify null pointer in user_service.py:45
3. Add null check guard
4. Run tests → passing
5. Commit: "fix: add null check in user service (hotfix)"
6. Push to origin/hotfix/null-pointer-fix
7. Create PR with [URGENT] tag
8. Return PR URL for immediate review
```

## Integration with Other Skills

### Works with /pr-comments

```bash
# Read PR comments first
/pr-comments

# Then fix in YOLO mode
/github-yolo "fix all comments and push"
```

### Works with /smart-review

```bash
# Get review insights
/smart-review

# Auto-fix issues
/github-yolo "address all review findings"
```

### Works with /test

```bash
# Run tests to identify failures
/test

# Auto-fix and re-test
/github-yolo "fix test failures"
```

## Limitations

1. **Cannot merge PRs** - Merging still requires manual approval or separate automation
2. **Cannot resolve complex conflicts** - Human review needed for non-trivial merge conflicts  
3. **Cannot generate new features** - Works best with defined fixes/changes
4. **Secret detection is heuristic** - May not catch all secret patterns

## Best Practices

1. **Review before enabling** - Understand what will be auto-committed
2. **Use feature branches** - Let the skill create branches off main
3. **Clear commit messages** - Provide specific messages when invoking
4. **Monitor PR comments** - Check that auto-responses are appropriate
5. **Have rollback plan** - Know how to revert if needed

## Rollback

If YOLO mode makes unwanted changes:

```bash
# Undo last commit (keep changes)
git reset HEAD~1

# Undo last commit (discard changes)  
git reset --hard HEAD~1

# Force push to revert remote
git push --force origin <branch>

# Close unwanted PR
gh pr close <number>
```
