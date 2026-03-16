---
name: pqc-attest
description: Post-quantum cryptographic attestation using ML-DSA-87 (FIPS 204) + SPHINCS+-SHAKE-256s (FIPS 205). Use when user asks to sign a document, create a PQC attestation, dual-sign a hash, produce a quantum-safe signature, generate an attestation JSON for a paper/document, or says things like "sign this", "attest ATT_XXX", "create attestation for <document>". Accepts a PDF file path directly — automatically hashes it and extracts the full document text into the output JSON. Outputs a self-contained attestation JSON (no AI/tool references) with the document writing embedded, suitable for regulatory submission. Keys are persistent and reused across calls.
---

# PQC Attestation

Signs a PDF (or SHA3-512 hash) with ML-DSA-87 + SPHINCS+-SHAKE-256s and outputs a self-contained JSON containing the full document text, hash, and both signatures.

## Quickstart — PDF (recommended)

```bash
cd <project-dir>
node ~/.claude/skills/pqc-attest/scripts/pqc_attest.mjs \
  "<path/to/document.pdf>" <attestation_id> "<document_title>" "<author>" [key_id]
```

**Example:**
```bash
node ~/.claude/skills/pqc-attest/scripts/pqc_attest.mjs \
  "C:/Users/peter/Downloads/batey forensic analysis.pdf" \
  ATT_784 \
  "Batey Forensic Analysis" \
  "Matthew Batey"
```

## Quickstart — Raw hash

```bash
node ~/.claude/skills/pqc-attest/scripts/pqc_attest.mjs \
  bcb54da0666eec90...  ATT_773  "Document Title"  "Author Name"
```

## Parameters

| Param | Required | Notes |
|---|---|---|
| `pdf_path` or `sha3_512_hex` | Yes | File path to PDF, or 128 hex chars raw hash |
| `attestation_id` | Yes | e.g. `ATT_784` |
| `document_title` | Yes | Quote if it contains spaces |
| `author` | Yes | Full name — lastname used in Desktop filename |
| `key_id` | No | Keypair name prefix, default `prime` |

## Outputs

- `<attestation_id>_signed.json` — in current working directory, includes `document_text`
- `~/Desktop/<attestation_id>_<lastname>_signed.json` — Desktop copy for submission

## Requirements

- Node.js >= 20
- `@noble/post-quantum` installed in CWD or any parent: `npm install @noble/post-quantum`
- If not installed: `cd <project-dir> && npm install @noble/post-quantum`

## Key Storage

Keys live at `~/.claude/pqc_keys/` as:
- `<key_id>_mldsa87.pk` / `.sk`
- `<key_id>_sphincs_shake256s.pk` / `.sk`

First run generates and saves keys. Subsequent runs reuse them — the same public key appears in every attestation for that `key_id`, enabling independent verification.

## Output JSON Structure

```json
{
  "attestation_id": "ATT_773",
  "document": "Document Title",
  "author": "Author Name",
  "sha3_512": "<128 hex chars>",
  "timestamp_utc": "2026-02-21T13:39:10.808Z",
  "signatures": {
    "ml_dsa_87": {
      "algorithm": "ML-DSA-87 (FIPS 204 / CRYSTALS-Dilithium Level 5)",
      "public_key_b64": "...",
      "signature_b64": "...",
      "signature_length_bytes": 4627,
      "verified": true
    },
    "sphincs_shake_256s": {
      "algorithm": "SPHINCS+-SHAKE-256s (FIPS 205)",
      "public_key_b64": "...",
      "signature_b64": "...",
      "signature_length_bytes": 29792,
      "verified": true
    }
  }
}
```

No tool, AI, or Claude references appear in the output — clean for regulatory submission.

## API Notes (baked into script)

These are the correct @noble/post-quantum v0.5.x argument orders — do not change:

- ML-DSA-87 keygen: `ml_dsa87.keygen(randomBytes(32))` — 32-byte seed
- SLH-DSA keygen: `slh_dsa_shake_256s.keygen(randomBytes(96))` — 96-byte seed (3×N, N=32)
- Both sign: `sign(msg, secretKey)` — message first
- Both verify: `verify(sig, msg, publicKey)` — signature first

## SHA3-512 Hashing (if needed)

If the user provides a file path instead of a hash, compute the SHA3-512 first:

```bash
node -e "
const {createHash}=require('crypto');
const fs=require('fs');
const h=createHash('sha3-512');
h.update(fs.readFileSync(process.argv[1]));
console.log(h.digest('hex'));
" path/to/document.pdf
```
