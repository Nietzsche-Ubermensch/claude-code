---
name: init
description: Analyze codebases and create/improve CLAUDE.md documentation files. Use when the user runs /init, asks to "create CLAUDE.md", "document this codebase", "analyze this project for CLAUDE.md", or wants to improve existing CLAUDE.md files. Works with any project type (React, Express, Python, monorepos, workspaces).
---

# CLAUDE.md Documentation Generator

Analyze codebases and generate comprehensive CLAUDE.md files that help future Claude instances be productive quickly.

## Quick Start

When invoked, follow this workflow:

1. **Check for existing CLAUDE.md** - Read it if present to understand what's already documented
2. **Analyze the codebase** - Identify project type, structure, and patterns
3. **Generate or improve** - Create new CLAUDE.md or suggest improvements to existing one
4. **Avoid slop** - No generic advice, obvious instructions, or unnecessary content

## What to Include

### Required Sections

**High-level architecture** - The "big picture" that requires reading multiple files to understand:
- Project structure (monorepo vs single project)
- Key architectural patterns (server entry points, routing, state management)
- Technology stack (frameworks, databases, cloud services)
- Important file paths and their purposes

**Common commands** - How to build, run, test, and develop:
- Installation: `npm install`, `pip install -r requirements.txt`, etc.
- Development: `npm run dev`, `python manage.py runserver`, etc.
- Building: `npm run build`, `docker-compose build`, etc.
- Testing: `npm test`, `pytest`, etc.
- Linting: `npm run lint`, `ruff check`, etc.

**Environment specifics** - Platform quirks and requirements:
- OS requirements (Windows, macOS, Linux)
- Shell differences (PowerShell vs Bash, .cmd suffix on Windows)
- Package manager requirements (npm, pnpm, pip, uv)
- Virtual environment setup
- Required environment variables

### Optional Sections (include if relevant)

**GitHub Actions workflows** - If `.github/workflows/` exists
**Git configuration** - If special signing, hooks, or branch patterns exist
**MCP servers** - If `.mcp.json` or MCP configuration exists
**Common workflows** - Multi-step procedures for frequent tasks
**File locations** - Quick reference for finding config files

### What NOT to Include

- Generic development practices
- Obvious instructions ("write tests", "use meaningful names")
- Comprehensive file listings (users can explore)
- Information that duplicates README.md
- Made-up sections like "Tips for Development" unless present in existing docs

## Analysis Process

### 1. Detect Project Type

Read these files in parallel to understand the project:

**Package managers:**
- `package.json` → Node.js project (check for workspaces, scripts, dependencies)
- `pyproject.toml` or `requirements.txt` → Python project
- `Cargo.toml` → Rust project
- `go.mod` → Go project
- `composer.json` → PHP project

**Build tools:**
- `tsconfig.json` → TypeScript
- `vite.config.ts` → Vite
- `next.config.js` → Next.js
- `docker-compose.yml` → Docker services

**Frameworks:**
- `src/App.tsx` → React
- `src/main.ts` → Various (check imports)
- `manage.py` → Django
- `app.py` or `wsgi.py` → Flask

### 2. Extract Commands

Look for npm scripts, Makefile targets, or scripts in the repository:

```bash
# Node.js - read package.json scripts
# Python - check for common patterns (pytest, manage.py, etc.)
# Docker - read docker-compose.yml services
```

Document the **commonly used** commands, not every possible command.

### 3. Identify Architecture Patterns

Read key files to understand:
- **Entry points**: `server.ts`, `main.py`, `index.tsx`
- **Routing**: Express routes, Django urls.py, React Router
- **State management**: Redux, Zustand, Context API
- **Database**: ORM files, schema definitions, migrations
- **API patterns**: REST endpoints, GraphQL schema

### 4. Check for Special Configurations

Look for:
- `.cursorrules` or `.cursor/rules/` → Include important parts
- `.github/copilot-instructions.md` → Include important parts
- Existing README.md → Extract non-obvious information
- `.env.example` → Document required env vars (never include actual values)

## Generation Guidelines

### Structure

Start with the required header:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
```

### Writing Style

- **Concise** - Get to the point, no fluff
- **Specific** - Use exact commands, file paths, and examples
- **Imperative** - "Run `npm install`" not "You should run npm install"
- **Organized** - Use clear headers and consistent formatting

### Code Blocks

Always use proper shell syntax for the platform:

```bash
# Good - cross-platform
npm install
pytest tests/

# Good - Windows-specific when needed
"/c/Program Files/nodejs/npm.cmd" install

# Good - with explanations
npm run dev     # Start frontend (port 3000)
npm run build   # Build for production
```

### File Paths

Use forward slashes for cross-platform compatibility:

```
project/
├── src/
│   ├── components/
│   └── lib/
└── tests/
```

## Examples

See [examples.md](references/examples.md) for complete CLAUDE.md examples:
- Workspace with multiple projects
- React + Express monorepo
- Python Django project
- Rust CLI tool

## Handling Edge Cases

**No package.json or obvious project type:**
- Look for source files to infer language
- Check for build artifacts (dist/, target/, __pycache__)
- Document what you find, even if minimal

**Workspace/monorepo:**
- Document the overall structure
- List each project with its purpose
- Include commands for each subproject

**Existing CLAUDE.md:**
- Read it carefully
- Identify what's missing or outdated
- Suggest specific improvements (don't rewrite unless necessary)
- Preserve good existing content

## Output Format

When creating a new CLAUDE.md:
1. Show a preview of the generated content
2. Ask if the user wants to save it
3. Use Write tool to create CLAUDE.md in the current directory

When improving existing CLAUDE.md:
1. Show specific suggestions with line numbers
2. Explain what's missing or should be improved
3. Offer to apply the changes with Edit tool
