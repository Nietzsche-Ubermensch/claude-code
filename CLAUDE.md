# User Preferences - Nietzsche-Ubermensch

## Identity
- GitHub: Nietzsche-Ubermensch
- Email: peterbilt5018@gmail.com
- Organization: Nietzsche-Ubermenschs

## Code Style
- TypeScript with strict mode
- 2-space indentation
- JSDoc comments for public APIs
- Async/await over raw promises

## Git Workflow
- Conventional commits: feat, fix, docs, refactor, test, chore, ci
- Branch naming: feature/, bugfix/, hotfix/
- Always create PRs, never push directly to main

## Testing
- Write tests for all new code
- Aim for >80% coverage
- Run tests after every change

## Communication
- Be direct and concise
- Show code examples over explanations
- Use agents proactively

## Project Context
- Stack: TypeScript, React, Node.js, Supabase
- GitHub org: Nietzsche-Ubermenschs
- Supabase project: ccjdctnmgrweserduxhi

## Custom Skills

### quantum-sign
Post-quantum document signing with ML-DSA-87 (FIPS-204) and Bitcoin timestamping.
```bash
/quantum-sign <file>        # Sign + timestamp
/quantum-sign verify <file> # Verify signature
```
- Location: ~/.claude/skills/quantum-sign/
- Script: scripts/pqc.py
- Outputs: .sig (signature), .json (manifest), .ots (Bitcoin timestamp)
- Dependencies: pip install pqcrypto requests