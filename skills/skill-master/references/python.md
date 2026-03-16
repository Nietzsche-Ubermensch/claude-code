# Python Pattern Detection Reference

Patterns to detect in Python codebases for skill generation.

## Detection Criteria

**Source roots:** `src/`, `app/`, root `*.py` files
**Minimum files:** 3 matching files required for pattern confidence
**File extensions:** `.py`, `.pyi`

## Common Patterns

### Repository Pattern
**Signature:** `class {Entity}Repository`
**Indicators:**
- Methods: `find_by_id`, `find_all`, `save`, `delete`
- Imports: `from typing import Optional, List`
- Database imports: `sqlalchemy`, `django.db`, `asyncpg`

**File locations:**
- `src/repositories/`
- `app/repositories/`
- `{module}/repositories/`

### Service Pattern
**Signature:** `class {Entity}Service`
**Indicators:**
- Business logic methods
- Calls to repositories
- Transaction handling

**File locations:**
- `src/services/`
- `app/services/`
- `{module}/services/`

### FastAPI Routes
**Signature:** `@app.get`, `@router.get`, `APIRouter()`
**Indicators:**
```python
from fastapi import APIRouter, Depends
router = APIRouter()

@router.get("/{entity}")
async def get_entity():
```

**File locations:**
- `src/routes/`, `src/api/`, `app/routes/`

### Pydantic Models
**Signature:** `BaseModel`, `@dataclass`
**Indicators:**
```python
from pydantic import BaseModel, Field
class EntityModel(BaseModel):
    field: str
```

### Django Models
**Signature:** `models.Model`
**Indicators:**
```python
from django.db import models
class Entity(models.Model):
```

### CLI Commands
**Signature:** `@click.command`, `@app.command`
**Indicators:**
```python
import click
@click.command()
@click.option('--flag')
def command():
```

### Pytest Fixtures
**Signature:** `@pytest.fixture`
**Indicators:**
```python
import pytest
@pytest.fixture
def fixture_name():
```

## Extraction Rules

**Imports to extract:**
- `from typing import ...` → Type hints used
- `from pydantic import ...` → Validation patterns
- `from fastapi import ...` → API patterns
- `import pytest` → Testing patterns

**Decorators to preserve:**
- `@dataclass`, `@pytest.fixture`, `@app.get`, `@click.command`

**Patterns to anonymize:**
- Class/function names: Keep pattern, replace domain terms
- String literals: Remove or genericize
- Hardcoded values: Replace with placeholders

**Patterns to remove entirely:**
- API keys, tokens, secrets
- Database URLs with credentials
- File paths containing usernames
- Email addresses, phone numbers
