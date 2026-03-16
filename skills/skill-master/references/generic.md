# Generic Pattern Detection Reference

Universal patterns across all languages/frameworks.

## Detection Criteria

**Applies to:** Any codebase without specific platform detection
**Minimum files:** 2 matching files (lower threshold for generic)
**Strategy:** Structure-based detection (not language-specific)

## Universal Patterns

### Configuration Management
**Indicators:**
- Files: `.env.example`, `config.yml`, `settings.json`, `app.config`
- Patterns: Key-value pairs, environment variables, feature flags
- Common keys: `DATABASE_URL`, `API_KEY`, `PORT`, `DEBUG`

**Extraction:**
```
# Config structure
{
  "database": { "host": "...", "port": ... },
  "features": { "featureX": true },
  "api": { "baseUrl": "...", "timeout": ... }
}
```

### Environment Handling
**Indicators:**
- Files in root: `.env`, `.env.local`, `.env.production`
- Reading env vars: `process.env.`, `os.environ`, `getenv()`

**Common patterns:**
- Required vs optional env vars
- Default values
- Validation on startup

### Logging
**Indicators:**
- Logger initialization
- Log levels: DEBUG, INFO, WARN, ERROR
- Structured logging (JSON logs)

**Common patterns:**
```
logger.info("message", { context })
logger.error("error", { error, stack })
```

### Error Handling
**Indicators:**
- Custom error classes
- Global error handlers
- Error middleware
- Try/catch patterns

### API Clients
**Indicators:**
- HTTP client imports: `axios`, `fetch`, `requests`
- Base URL configuration
- Authentication headers
- Retry logic

### Database Connections
**Indicators:**
- Connection pooling
- Migration files
- Schema definitions
- Query builders

### Testing Utilities
**Indicators:**
- Test helpers in `tests/utils/`, `test/helpers/`
- Mock factories
- Shared fixtures
- Test database setup

### CI/CD Patterns
**Indicators:**
- `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`
- Build scripts
- Deploy scripts
- Environment-specific configs

### Docker Patterns
**Indicators:**
- `Dockerfile`, `docker-compose.yml`
- Multi-stage builds
- Volume mounts
- Environment injection

### Documentation
**Indicators:**
- `README.md` with setup instructions
- `docs/` directory
- API documentation (OpenAPI, GraphQL schema)
- Architecture diagrams

## Extraction Strategy for Generic

Since language is unknown, focus on:

1. **File structure:** Detect organization patterns
2. **Configuration:** Extract config management approach
3. **Documentation:** Pull from existing docs
4. **Naming conventions:** Infer from file/directory names

**Example: Detecting "deployment" pattern**

```
Files found:
- deploy.sh
- docker-compose.yml
- k8s/deployment.yaml

Pattern: deployment
Confidence: MEDIUM (3 related files)
Generated skill: deployment.md with:
- Scripts from deploy.sh
- Docker commands from compose
- K8s deployment pattern
```

## Anonymization Rules (Language-Agnostic)

**Always remove:**
- Credentials (passwords, tokens, keys)
- Hostnames, IP addresses
- Email addresses
- File paths with usernames
- Company/project-specific names

**Always keep:**
- Directory structure
- File naming patterns
- Configuration structure
- Workflow sequences
