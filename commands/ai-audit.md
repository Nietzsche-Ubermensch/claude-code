# ai-audit

Audit AI-generated code for quality and security

## Variables
- files: AI-generated code to audit

## Prompt
You are an expert at auditing AI-generated code.

Check {files} for AI coding mistakes:

1. HALLUCINATED DEPENDENCIES
   - Non-existent packages
   - Wrong version numbers
   - Incorrect imports

2. LOGIC ERRORS
   - Incorrect algorithms
   - Edge case failures
   - Race conditions

3. SECURITY FLAWS
   - Injection vulnerabilities
   - Insecure patterns
   - Over-privileged operations

4. PERFORMANCE ISSUES
   - Inefficient algorithms
   - Memory leaks
   - Unnecessary complexity

Rate severity 1-10 and provide fixes.
