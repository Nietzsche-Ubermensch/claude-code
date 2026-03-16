---
name: quantum-sign
description: |
  Post-quantum document signing with ML-DSA-87 (FIPS-204) and Bitcoin/blockchain timestamping.
  Use when user asks to: sign a document, create quantum-safe signature, timestamp a file,
  verify a signature, create proof of existence, notarize a document, or anchor to blockchain.
  Supports any file type. Creates .sig (signature), .json (manifest), and .ots (Bitcoin timestamp).
---

# Quantum Sign

Post-quantum document signing with ML-DSA-87 and Bitcoin timestamping.

## Commands

```bash
/quantum-sign <file>           # Sign a document
/quantum-sign verify <file>    # Verify signature
/quantum-sign timestamp <file> # Add Bitcoin timestamp only
/quantum-sign keygen           # Generate new keypair
```

## Quick Start

```python
# 1. Generate keys (once)
from pqcrypto.sign.ml_dsa_87 import generate_keypair
public_key, private_key = generate_keypair()

# 2. Sign document
from pqcrypto.sign.ml_dsa_87 import sign
with open('document.pdf', 'rb') as f:
    data = f.read()
signature = sign(private_key, data)

# 3. Verify
from pqcrypto.sign.ml_dsa_87 import verify
verify(public_key, data, signature)  # Raises exception if invalid
```

## Bitcoin Timestamp (Free)

```python
import hashlib, requests

with open('document.pdf', 'rb') as f:
    doc_hash = hashlib.sha256(f.read()).digest()

r = requests.post('https://a.pool.opentimestamps.org/digest', data=doc_hash)
with open('document.pdf.ots', 'wb') as f:
    f.write(r.content)
```

Verify at: https://opentimestamps.org

## Output Structure

```
output_folder/
├── document.pdf          # Original
├── document.pdf.sig      # ML-DSA-87 signature (4.6 KB)
├── document.pdf.json     # Manifest with hash + metadata
├── document.pdf.ots      # Bitcoin timestamp proof
├── public.key            # Share for verification
└── private.key           # KEEP SECRET
```

## Workflow

1. **keygen** → Creates ML-DSA-87 keypair
2. **sign** → Hash document (SHA3-256), sign with private key
3. **timestamp** → Submit SHA-256 hash to OpenTimestamps
4. **verify** → Check signature with public key

## Key Sizes

| Component | Size |
|-----------|------|
| Public Key | 2,592 bytes |
| Private Key | 4,896 bytes |
| Signature | ~4,627 bytes |

## Dependencies

```bash
pip install pqcrypto requests
```

## Verification

Anyone with `public.key` can verify:

```python
from pqcrypto.sign.ml_dsa_87 import verify

with open('public.key', 'rb') as f:
    public_key = f.read()
with open('document.pdf', 'rb') as f:
    document = f.read()
with open('document.pdf.sig', 'rb') as f:
    signature = f.read()

try:
    verify(public_key, document, signature)
    print("VALID")
except:
    print("INVALID")
```

## Security Notes

- ML-DSA-87 is NIST FIPS-204 standard (quantum-resistant)
- SHA3-256 for document hashing
- Private key must remain confidential
- Bitcoin timestamp provides independent proof of existence
