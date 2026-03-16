# Example Workflows

This document provides example workflows for using Claude Code Desktop with your Git repositories.

## Workflow 1: Feature Development

```bash
# Start a new feature
claude-git branch user-authentication

# Check current status
claude-git status

# Make your changes to files...
# edit src/auth.py
# edit src/models/user.py
# edit tests/test_auth.py

# Review changes with syntax highlighting
claude-git diff

# Get suggested commit message
claude-git suggest

# Commit with assistance
claude-git commit -f src/auth.py -f src/models/user.py -f tests/test_auth.py
```

## Workflow 2: Bug Fix

```bash
# Create a bug fix branch
claude-git branch fix-login-issue

# Make your fix...
# edit src/auth.py

# Check what changed
claude-git context src/auth.py

# Stage and commit
git add src/auth.py
claude-git commit -m "Fix login validation error"
```

## Workflow 3: Code Review Preparation

```bash
# Check repository status
claude-git status

# Review all changes before creating PR
claude-git diff --staged

# Get context for each modified file
claude-git context src/main.py
claude-git context src/utils.py

# Generate comprehensive commit message
claude-git suggest
```

## Workflow 4: Multi-file Update

```bash
# Start feature branch
claude-git branch refactor-api

# Make changes to multiple files...

# Review status
claude-git status

# Stage specific files
git add src/api/*.py

# Auto-generate and commit
claude-git commit
```

## Workflow 5: Quick Commit

```bash
# Make a quick change
echo "# New section" >> README.md

# Quick commit with auto-generated message
git add README.md
claude-git commit

# Or specify files directly
claude-git commit -f README.md -m "Update documentation"
```

## Integration with Git Aliases

Add these to your `.gitconfig` for even faster workflows:

```bash
git config --global alias.cs '!claude-git status'
git config --global alias.cb '!claude-git branch'
git config --global alias.cc '!claude-git commit'
git config --global alias.cd '!claude-git diff'
git config --global alias.cx '!claude-git context'
```

Then use:
```bash
git cs    # claude-git status
git cb feature-name  # claude-git branch feature-name
git cc    # claude-git commit
git cd    # claude-git diff
```

## Pre-commit Hook Example

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Run Claude Code Desktop status check before commit
claude-git status
```

## Tips and Best Practices

1. **Use descriptive branch names**: `claude-git branch user-profile-page` is better than `claude-git branch feature1`

2. **Review before committing**: Always run `claude-git diff` to see what you're about to commit

3. **Get context**: Use `claude-git context <file>` to understand file status before making changes

4. **Leverage suggestions**: Let `claude-git suggest` help you write better commit messages

5. **Work incrementally**: Make small, focused commits with `claude-git commit` rather than large bulk commits
