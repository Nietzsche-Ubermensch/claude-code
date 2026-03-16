#!/usr/bin/env python3
"""
PQC Dual Sign — ML-DSA-87 + SPHINCS+-SHAKE-256s
Requires: pip install dilithium-py pyspx
Usage: python pqc_dual_sign.py <sha3_512_hex> <attestation_id> <document_title> <author>

Signs a SHA3-512 hash with both ML-DSA-87 (FIPS 204) and SPHINCS+-SHAKE-256s (FIPS 205).
Outputs: <attestation_id>.json
"""
import hashlib
import json
import base64
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

KEY_DIR = Path.home() / ".claude" / "pqc_keys"
KEY_DIR.mkdir(parents=True, exist_ok=True)


def load_or_generate_mldsa87_keys(key_id: str):
    from dilithium_py.ml_dsa import ML_DSA_87
    pk_path = KEY_DIR / f"{key_id}_mldsa87.pk"
    sk_path = KEY_DIR / f"{key_id}_mldsa87.sk"
    if pk_path.exists() and sk_path.exists():
        pk = pk_path.read_bytes()
        sk = sk_path.read_bytes()
    else:
        pk, sk = ML_DSA_87.keygen()
        pk_path.write_bytes(pk)
        sk_path.write_bytes(sk)
        print(f"  Generated ML-DSA-87 keypair → {key_id}_mldsa87.{{pk,sk}}")
    return pk, sk


def load_or_generate_sphincs_keys(key_id: str):
    from pyspx import shake_256s
    pk_path = KEY_DIR / f"{key_id}_sphincs_shake256s.pk"
    sk_path = KEY_DIR / f"{key_id}_sphincs_shake256s.sk"
    if pk_path.exists() and sk_path.exists():
        pk = pk_path.read_bytes()
        sk = sk_path.read_bytes()
    else:
        seed = os.urandom(shake_256s.crypto_sign_SEEDBYTES)
        pk, sk = shake_256s.generate_keypair(seed)
        pk_path.write_bytes(pk)
        sk_path.write_bytes(sk)
        print(f"  Generated SPHINCS+-SHAKE-256s keypair → {key_id}_sphincs_shake256s.{{pk,sk}}")
    return pk, sk


def dual_sign(sha3_512_hex: str, attestation_id: str, document_title: str, author: str, key_id: str = "prime"):
    from dilithium_py.ml_dsa import ML_DSA_87
    from pyspx import shake_256s

    payload_bytes = bytes.fromhex(sha3_512_hex)

    # ML-DSA-87
    print("[1/2] ML-DSA-87 signing...")
    ml_pk, ml_sk = load_or_generate_mldsa87_keys(key_id)
    ml_sig = ML_DSA_87.sign(ml_sk, payload_bytes)

    # SPHINCS+-SHAKE-256s
    print("[2/2] SPHINCS+-SHAKE-256s signing...")
    sp_pk, sp_sk = load_or_generate_sphincs_keys(key_id)
    sp_sig = shake_256s.sign(payload_bytes, sp_sk)

    manifest = {
        "attestation_id": attestation_id,
        "document": document_title,
        "author": author,
        "sha3_512": sha3_512_hex,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "signatures": {
            "ml_dsa_87": {
                "algorithm": "ML-DSA-87 (FIPS 204, CRYSTALS-Dilithium Level 5)",
                "public_key_b64": base64.b64encode(ml_pk).decode(),
                "signature_b64": base64.b64encode(ml_sig).decode(),
            },
            "sphincs_shake_256s": {
                "algorithm": "SPHINCS+-SHAKE-256s (FIPS 205)",
                "public_key_b64": base64.b64encode(sp_pk).decode(),
                "signature_b64": base64.b64encode(sp_sig).decode(),
            }
        }
    }

    out = Path(f"{attestation_id}.json")
    out.write_text(json.dumps(manifest, indent=2))
    print(f"\nAttestation written → {out}")
    return manifest


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python pqc_dual_sign.py <sha3_512_hex> <attestation_id> <document_title> <author>")
        sys.exit(1)
    dual_sign(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
