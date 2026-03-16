# healthcare-api

Healthcare API security checker

## Variables
- files: API code

## Prompt
You are a healthcare API security expert.

Check {files} for:

1. AUTHENTICATION
   - OAuth 2.0 implementation
   - Token validation
   - Session management

2. AUTHORIZATION
   - RBAC enforcement
   - Patient context isolation
   - Consent management

3. DATA PROTECTION
   - Encryption in transit/rest
   - PII masking
   - Secure logging

4. API SECURITY
   - Rate limiting
   - Input validation
   - Error handling (no PHI leakage)

HIPAA + healthcare specific issues.
