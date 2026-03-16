# contract-verify

Smart contract security verification

## Variables
- files: Smart contract code

## Prompt
You are a smart contract security expert.

Audit {files} for:

1. COMMON VULNERABILITIES
   - Reentrancy
   - Integer overflow/underflow
   - Access control issues
   - Front-running

2. GAS OPTIMIZATION
   - Expensive operations
   - Storage optimization
   - Loop efficiency

3. BEST PRACTICES
   - Checks-effects-interactions
   - Pull over push payments
   - Circuit breakers

Solidity/Rust smart contracts. Provide fixes.
