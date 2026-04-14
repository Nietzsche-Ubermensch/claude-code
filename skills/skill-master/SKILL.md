---
name: skill-master
description: Autonomous skill discovery and generation from codebase patterns. Scans project structure, detects architectural patterns (classes, modules, configs), compares with existing .claude/skills/, and auto-generates SKILL files with real code examples. Use when user asks to "analyze project for skills", "generate skills from codebase", "skill discovery", "sync skills with project", or "what skills are missing".
---

# Skill Master

Autonomous skill discovery and generation engine. Analyzes your codebase to identify patterns, compares them with existing skills, and generates new SKILL files with real examples extracted from your code.

## Core Workflow

```
Scan Project → Detect Patterns → Compare with Existing → Generate Missing Skills
```

**What it finds:**
- Architectural patterns (ViewModel, Repository, Service, etc.)
- Module structures (auth/, api/, db/, utils/)
- Configuration patterns (env handling, feature flags)
- Testing patterns (fixtures, mocks, helpers)
- Build/deployment patterns (CI/CD, Docker, scripts)

## Usage

```bash
/skill-master                    # Full discovery + report
/skill-master discover           # Analysis only (no generation)
/skill-master generate           # Generate all missing skills
/skill-master generate <pattern> # Generate specific pattern only
/skill-master update             # Update existing skills from codebase
```

## Discovery Algorithm

### Step 1: Platform Detection

Detect stack by reading build/config files in order:

```bash
# Python
[ -f "pyproject.toml" ] || [ -f "requirements.txt" ] || [ -f "setup.py" ]
→ Load references/python.md

# Node.js
[ -f "package.json" ]
→ Load references/node.md

# Generic fallback
→ Load references/generic.md
```

### Step 2: Pattern Scanning

For each detected platform, scan source roots:

**Python example:**
```bash
find src/ -type f -name "*.py" | while read file; do
  # Detect patterns
  grep -l "class.*Repository" "$file"  # Repository pattern
  grep -l "class.*Service" "$file"     # Service pattern
  grep -l "class.*ViewModel" "$file"   # ViewModel pattern
  grep -l "@dataclass" "$file"         # Data models
  grep -l "pytest.fixture" "$file"     # Test fixtures
done
```

**Node.js example:**
```bash
find src/ -type f -name "*.js" -o -name "*.ts" | while read file; do
  grep -l "export.*Controller" "$file"  # Controller pattern
  grep -l "export.*Service" "$file"     # Service pattern
  grep -l "describe(" "$file"           # Test suites
done
```

### Step 3: Gap Analysis

Compare detected patterns with existing `.claude/skills/`:

```
Detected Patterns:
- repository (12 files)
- service (8 files)
- viewmodel (5 files)
- test-fixtures (3 files)

Existing Skills:
- repository.md ✓
- service.md ✓

Missing Skills:
- viewmodel (5 files) → GENERATE
- test-fixtures (3 files) → GENERATE
```

### Step 4: Content Extraction

For each missing pattern, extract real examples:

1. **Find representative files** (2-3 best examples)
2. **Extract structure:**
   - Imports/dependencies
   - Class/function signatures
   - Decorators/annotations
   - Naming conventions
3. **Anonymize business logic:**
   - Replace domain terms with generic names
   - Remove hardcoded values
   - Keep structural patterns
4. **Extract rules** from `.ruler/*.md` if present

## Generation Templates

### Pattern-Based Generation

**Example: Repository Pattern**

Input (from codebase):
```python
# src/repositories/user_repository.py
from typing import Optional
from models import User
from database import db

class UserRepository:
    def find_by_id(self, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def save(self, user: User) -> User:
        db.add(user)
        db.commit()
        return user
```

Generated SKILL.md:
```markdown
---
name: repository
description: Repository pattern for data access. Use when implementing data persistence, database queries, or data access layer.
---

# Repository Pattern

Data access abstraction layer that isolates domain logic from data persistence.

## Structure

```python
class {Entity}Repository:
    def find_by_id(self, id: int) -> Optional[Entity]:
        """Retrieve single entity by primary key"""

    def find_all(self) -> List[Entity]:
        """Retrieve all entities"""

    def save(self, entity: Entity) -> Entity:
        """Persist entity"""

    def delete(self, id: int) -> bool:
        """Remove entity"""
```

## Implementation

**File location:** `src/repositories/{entity}_repository.py`

**Imports:**
- `from typing import Optional, List`
- `from models import {Entity}`
- `from database import db`

**Methods:**
- Always return `Optional[Entity]` for single queries
- Always commit in save/delete methods
- Use type hints for all parameters

## Rules

### Do
- One repository per domain entity
- Name as `{Entity}Repository`
- Place in `src/repositories/`
- Return domain models, not DB objects
- Handle transaction management
- Use dependency injection

### Don't
- Mix business logic in repositories
- Return raw database objects
- Hardcode connection strings
- Create generic "data access" classes

## File Location
- `src/repositories/user_repository.py` (3 examples found)
- `src/repositories/product_repository.py`

<!-- Generated by skill-master
Sources:
- src/repositories/user_repository.py
- src/repositories/product_repository.py
Last updated: 2026-03-16
-->
```

## Update Strategy

### First-Time Generation (No Marker)

1. Check if `SKILL.md` exists
2. If exists: Create `SKILL.md.bak` backup
3. Generate fresh content from current codebase
4. Add source marker at end
5. Report: `[BACKED_UP+CREATED]`

### Subsequent Updates (Marker Present)

1. Detect marker: `<!-- Generated by skill-master`
2. Parse existing sections
3. **Preserve custom content:**
   - Keep all sections not in marker sources
   - Keep user-added examples
   - Keep custom rules
4. **Update from codebase:**
   - Refresh file locations
   - Update code examples if source changed
   - Add new patterns if found
5. Update marker timestamp
6. Report: `[UPDATED]`

### Clean Generation (No Existing File)

1. Generate from template
2. Extract all content from codebase
3. Add source marker
4. Report: `[CREATED]`

## Platform-Specific References

When platform detected, load corresponding reference for pattern guidance:

### Python (`references/python.md`)

Common patterns to detect:
- **Repository:** `class {Entity}Repository`
- **Service:** `class {Entity}Service`
- **Data Models:** `@dataclass`, `BaseModel` (Pydantic)
- **FastAPI Routes:** `@app.get`, `APIRouter`
- **Django Views:** `class {Entity}View(View)`
- **CLI Commands:** `@click.command`
- **Test Fixtures:** `@pytest.fixture`
- **ORM Models:** `Base`, `models.Model`

### Node.js (`references/node.md`)

Common patterns to detect:
- **Controllers:** `export class {Entity}Controller`
- **Services:** `export class {Entity}Service`
- **Middleware:** `export function {name}Middleware`
- **Routes:** `router.get`, `app.use`
- **Express Apps:** `const app = express()`
- **Test Suites:** `describe(`, `test(`
- **TypeScript Types:** `interface {Entity}`, `type {Name}`

### Generic (`references/generic.md`)

Universal patterns (any language):
- Configuration files
- Environment handling
- Logging patterns
- Error handling
- API clients
- Database connections
- Testing utilities

## Output Report

```
═══════════════════════════════════════════════════════════
SKILL MASTER DISCOVERY REPORT
═══════════════════════════════════════════════════════════

Platform: Python 3.13
Source Root: src/
Existing Skills: 3

Detected Patterns:
┌────────────────┬────────┬─────────────────────────────┐
│ Pattern        │ Count  │ Example Location            │
├────────────────┼────────┼─────────────────────────────┤
│ repository     │ 12     │ src/repositories/user_repo  │
│ service        │ 8      │ src/services/auth_service   │
│ viewmodel      │ 5      │ src/viewmodels/user_vm      │
│ test-fixtures  │ 3      │ tests/fixtures/db_fixture   │
│ fastapi-routes │ 15     │ src/routes/users.py         │
└────────────────┴────────┴─────────────────────────────┘

Gap Analysis:
✓ repository.md exists (up to date)
✓ service.md exists (up to date)
✗ viewmodel.md missing (5 files found)
✗ test-fixtures.md missing (3 files found)
✗ fastapi-routes.md missing (15 files found)

Recommendations:
→ Generate 3 missing skills
→ Update 0 existing skills
→ Run: /skill-master generate
═══════════════════════════════════════════════════════════
```

After generation:

```
═══════════════════════════════════════════════════════════
SKILL GENERATION REPORT
═══════════════════════════════════════════════════════════

Skills Generated: 3

viewmodel [CREATED]
├── Analyzed: 5 source files
├── Sources:
│   ├── src/viewmodels/user_viewmodel.py
│   ├── src/viewmodels/product_viewmodel.py
│   └── src/viewmodels/order_viewmodel.py
├── Rules from: .ruler/mvvm.md
└── Output: .claude/skills/viewmodel/SKILL.md (247 lines)

test-fixtures [CREATED]
├── Analyzed: 3 source files
├── Sources:
│   ├── tests/fixtures/database.py
│   └── tests/fixtures/auth.py
└── Output: .claude/skills/test-fixtures/SKILL.md (189 lines)

fastapi-routes [CREATED]
├── Analyzed: 15 source files
├── Sources:
│   ├── src/routes/users.py
│   ├── src/routes/products.py
│   └── src/routes/auth.py
├── Rules from: .ruler/api.md
└── Output: .claude/skills/fastapi-routes/SKILL.md (312 lines)

Validation:
✓ All YAML frontmatter valid
✓ All descriptions include trigger keywords
✓ All content under 500 lines
✓ All required sections present
✓ Source markers added

Next Steps:
→ Review generated skills in .claude/skills/
→ Customize examples if needed
→ Run /skill-master update to refresh from codebase
═══════════════════════════════════════════════════════════
```

## Safety & Constraints

### File System Safety
- ✓ Only write to `.claude/skills/{skill-name}/SKILL.md`
- ✓ Never modify files outside `.claude/skills/`
- ✓ Always create `.bak` backup before first modification
- ✓ Never overwrite without backup

### Content Safety
- ✓ Anonymize business logic (replace domain terms)
- ✓ Remove all secrets, API keys, tokens
- ✓ Remove hardcoded values
- ✓ Remove PII (emails, names, addresses)
- ✗ Never include `.env` file contents
- ✗ Never include credential files

### Quality Guarantees
- ✓ Only include patterns verified in 2+ files
- ✓ Use actual code from codebase (anonymized)
- ✓ Include trigger keywords in description
- ✓ Keep SKILL.md under 500 lines
- ✓ Preserve user customizations on update
- ✓ Deterministic output (same input → same output)

## Advanced Features

### Pattern Confidence Scoring

Before generating, score pattern confidence:

```
Pattern: repository
Files Found: 12
Consistency: 11/12 files match naming convention (91%)
Examples Extracted: 3 (top 25%)
Confidence: HIGH → GENERATE

Pattern: controller
Files Found: 2
Consistency: 1/2 files match naming convention (50%)
Examples Extracted: 1
Confidence: LOW → SKIP (wait for 3+ files)
```

Only generate skills for HIGH confidence patterns (3+ files, >80% consistency).

### Rule Inheritance

If `.ruler/*.md` files exist, extract rules:

```markdown
# .ruler/repository.md

## Architecture Rules
- All repositories MUST extend BaseRepository
- Use dependency injection, not direct imports
- Transaction handling in service layer, not repository

## Naming
- Suffix with "Repository"
- Place in repositories/ directory
```

Extracted to SKILL.md:

```markdown
## Rules

### Do (from .ruler/repository.md)
- Extend BaseRepository for all implementations
- Use dependency injection
- Handle transactions in service layer

### Don't
- Direct import database connections
- Mix business logic in data access
```

### Cross-Skill References

Detect related skills and create references:

```markdown
## Related Skills

See also:
- [service.md](../service/SKILL.md) - Service layer calling repositories
- [test-fixtures.md](../test-fixtures/SKILL.md) - Testing repositories
```

## Troubleshooting

**No patterns detected:**
- Check platform detection (build files present?)
- Verify source root path (default: `src/`)
- Lower threshold (generate for 2+ files instead of 3+)

**Too many patterns (noise):**
- Increase threshold (require 5+ files)
- Add exclusion filters (skip test files, migrations)
- Focus on specific directories only

**Generated content has secrets:**
- Review anonymization rules
- Add custom patterns to `.gitignore`
- Report issue (this should never happen)

**Custom sections lost on update:**
- Check marker present in file
- Backup not created (first run should backup)
- Report corruption issue
