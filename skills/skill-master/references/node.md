# Node.js Pattern Detection Reference

Patterns to detect in Node.js/TypeScript codebases for skill generation.

## Detection Criteria

**Source roots:** `src/`, `lib/`, `app/`, `server/`
**Minimum files:** 3 matching files required
**File extensions:** `.js`, `.ts`, `.jsx`, `.tsx`, `.mjs`

## Common Patterns

### Express Controllers
**Signature:** `class {Entity}Controller`, `{entity}Controller`
**Indicators:**
```typescript
export class UserController {
  async getUser(req: Request, res: Response) {}
  async createUser(req: Request, res: Response) {}
}
```

**File locations:**
- `src/controllers/`
- `app/controllers/`
- `server/controllers/`

### Services
**Signature:** `class {Entity}Service`, `{entity}Service`
**Indicators:**
```typescript
export class AuthService {
  async login(credentials) {}
  async validateToken(token) {}
}
```

### Express Routes
**Signature:** `Router()`, `express.Router()`
**Indicators:**
```javascript
const router = express.Router();
router.get('/:id', controller.get);
router.post('/', controller.create);
```

### Middleware
**Signature:** `function {name}Middleware`, `(req, res, next) =>`
**Indicators:**
```javascript
export function authMiddleware(req, res, next) {
  // validate token
  next();
}
```

### React Components
**Signature:** `export function {Name}`, `export const {Name}: FC`
**Indicators:**
```tsx
export function UserProfile({ user }: Props) {
  return <div>{user.name}</div>
}
```

### TypeScript Interfaces/Types
**Signature:** `interface {Name}`, `type {Name}`
**Indicators:**
```typescript
export interface User {
  id: number;
  email: string;
}
```

### Test Suites
**Signature:** `describe(`, `test(`, `it(`
**Indicators:**
```javascript
describe('UserService', () => {
  test('should create user', async () => {
    expect(result).toBeDefined();
  });
});
```

## Extraction Rules

**Imports to extract:**
- `import { ... } from 'express'` → Express patterns
- `import { Request, Response } from ...` → HTTP handlers
- `import React from 'react'` → React patterns
- Type imports → TypeScript patterns

**Decorators to preserve (if using decorators):**
- `@Get()`, `@Post()`, `@Injectable()` (NestJS)

**Patterns to anonymize:**
- Entity names → Generic terms
- Business logic → Keep structure, remove specifics
- API endpoints → Keep pattern, genericize resources

**Remove entirely:**
- API keys in headers
- JWT secrets
- Database connection strings
- OAuth credentials
