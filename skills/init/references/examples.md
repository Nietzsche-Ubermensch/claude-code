# CLAUDE.md Examples

This file contains real examples of well-structured CLAUDE.md files for different project types.

## Example 1: Workspace with Multiple Projects

For home directories or workspaces containing multiple projects:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Workspace Overview

```
C:\Users\peter\
├── GitHub/ai-suite/            # Multi-provider AI platform (React + Express)
├── GitHub/multimodal-ai-integr/ # Multimodal AI integration (public repo)
├── document-signing/           # Post-quantum signing (Python, ML-DSA-87)
└── package.json                # Root-level deps (openai, readline)
```

## Active Projects

### AI Suite — `GitHub/ai-suite/`

Multi-provider AI platform supporting OpenRouter, Hugging Face, Venice AI.

**Stack:** React + Vite (frontend :3000), Express.js (backend :8080), Node.js >=18

```bash
# From GitHub/ai-suite/
npm run install:all   # Install all deps
npm run dev           # Start frontend + backend
npm run build         # Build both
```

**Architecture:**
- `backend/src/server.ts` — Single-file Express server; all provider routing here
- `frontend/src/App.tsx` — Root React component
- `frontend/src/lib/api.ts` — API client connecting to backend

### Document Signing — `document-signing/`

Post-quantum cryptographic signing using ML-DSA-87.

**Stack:** Python 3.x

```bash
python sign_document.py file.pdf
python verify_document.py file.pdf.sig
```

## Environment

**Platform:** Windows 11, Git Bash
**Node.js:** npm/npx require `.cmd` suffix in bash — `"/c/Program Files/nodejs/npm.cmd"`
**Python:** 3.10+
```

---

## Example 2: React + Express Monorepo

For full-stack TypeScript projects:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack AI chat application with React frontend and Express backend.

**Stack:** TypeScript, React 18, Express, Vite, Node.js >=18

## Development

```bash
npm install           # Install all dependencies
npm run dev           # Start both frontend (3000) and backend (8080)
npm run dev:frontend  # Frontend only
npm run dev:backend   # Backend only
npm run build         # Build for production
npm test              # Run all tests
```

## Architecture

### Frontend (`/frontend`)

- `src/App.tsx` — Main application component with routing
- `src/components/` — Reusable React components
- `src/lib/api.ts` — API client (axios wrapper)
- `src/store/` — Zustand state management

Build: Vite → `dist/`
Port: 3000 (dev), served from Express in production

### Backend (`/backend`)

- `src/server.ts` — Express app entry point
- `src/routes/` — API route handlers
- `src/middleware/` — Auth, CORS, error handling
- `src/services/` — Business logic (AI providers, database)

Port: 8080
Database: PostgreSQL (connection via `DATABASE_URL` env var)

## Environment Variables

Create `.env` in root:

```bash
DATABASE_URL=postgresql://localhost/mydb
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## Testing

```bash
npm test              # All tests (frontend + backend)
npm run test:watch    # Watch mode
npm run test:coverage # Coverage report
```

Uses Vitest for both frontend and backend.

## GitHub Actions

- `.github/workflows/ci.yml` — Run tests on PRs
- `.github/workflows/deploy.yml` — Deploy to production on main branch merge
```

---

## Example 3: Python Django Project

For Django web applications:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Django REST API for content management with PostgreSQL database.

**Stack:** Python 3.11, Django 5.0, DRF, PostgreSQL, Redis (caching)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

## Development

```bash
python manage.py runserver              # Start dev server (localhost:8000)
python manage.py makemigrations         # Create new migrations
python manage.py migrate                # Apply migrations
python manage.py test                   # Run tests
python manage.py shell                  # Django shell
```

## Architecture

**Django apps:**
- `content/` — Content models (Article, Page, Media)
- `users/` — User authentication and profiles
- `api/` — DRF viewsets and serializers

**Key files:**
- `config/settings.py` — Django settings (loads from environment)
- `config/urls.py` — URL routing
- `content/models.py` — Database models
- `api/serializers.py` — API serialization

**Database:** PostgreSQL with these key models:
- `Article` — Blog posts/articles
- `Page` — Static pages
- `Media` — File uploads (S3 storage in production)

## Testing

```bash
pytest                           # Run all tests
pytest tests/test_api.py         # Specific test file
pytest -k "test_article"         # Tests matching pattern
pytest --cov                     # Coverage report
```

Uses pytest-django. Test database created/destroyed automatically.

## Environment Variables

Create `.env`:

```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=...           # For media uploads
AWS_SECRET_ACCESS_KEY=...
```

## Deployment

Production uses:
- Gunicorn (WSGI server)
- Nginx (reverse proxy)
- PostgreSQL (RDS)
- Redis (ElastiCache)
- S3 (media storage)

Deploy: `git push heroku main` (Heroku configured with auto-migrations)
```

---

## Example 4: Rust CLI Tool

For Rust command-line applications:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Fast command-line tool for parsing and analyzing log files.

**Stack:** Rust 1.75+, clap (CLI), serde (serialization), regex

## Development

```bash
cargo build              # Build debug binary
cargo run -- [args]      # Run with arguments
cargo test               # Run tests
cargo clippy             # Lint
cargo fmt                # Format code
cargo build --release    # Build optimized binary (target/release/)
```

## Architecture

**Main components:**
- `src/main.rs` — CLI entry point (clap argument parsing)
- `src/parser.rs` — Log parsing logic (regex patterns)
- `src/analyzer.rs` — Analysis and statistics
- `src/output.rs` — Formatting output (JSON, CSV, table)

**Key dependencies:**
- `clap` — Command-line argument parsing
- `regex` — Log pattern matching
- `serde` — JSON/CSV serialization
- `anyhow` — Error handling

## Testing

```bash
cargo test                    # Unit tests
cargo test --test integration # Integration tests only
cargo test -- --nocapture     # Show println! output
```

Integration tests in `tests/` directory test the full CLI.

## Usage Example

```bash
# Parse nginx access logs
cargo run -- parse nginx.log --format json > output.json

# Analyze error patterns
cargo run -- analyze app.log --filter "ERROR" --stats
```
```

---

## Pattern: Monorepo with Workspaces

For npm/pnpm workspaces:

```markdown
## Project Structure

This is a monorepo using npm workspaces.

```
project/
├── packages/
│   ├── core/        # Shared types and utilities
│   ├── ui/          # React component library
│   └── api/         # API client
└── apps/
    ├── web/         # Main web app
    └── admin/       # Admin dashboard
```

## Development

```bash
npm install           # Install all workspace dependencies
npm run dev -w web    # Start web app only
npm run dev -w admin  # Start admin only
npm run build         # Build all packages and apps
npm run test          # Test all workspaces
```

**Architecture:**
- Shared code in `packages/` (imported by apps)
- Each app independent (own package.json)
- Build order: packages → apps
```

---

## Key Principles Demonstrated

1. **Start with required header** — All examples begin with "# CLAUDE.md" and description
2. **Focus on architecture** — Not file listings, but how things connect
3. **Practical commands** — Real commands developers use daily
4. **Platform-specific details** — Windows quirks, shell differences
5. **No generic advice** — Nothing about "write tests" or "use meaningful names"
6. **Concise** — Get to the point quickly
