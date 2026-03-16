#!/usr/bin/env python3
"""
PQC Document Signing Tool
ML-DSA-87 (FIPS-204) with Bitcoin timestamping

Usage:
    python pqc.py keygen [--output DIR]
    python pqc.py sign <file> [--keys DIR] [--output DIR]
    python pqc.py verify <file> [--keys DIR]
    python pqc.py timestamp <file>
    python pqc.py full <file> [--keys DIR] [--output DIR]
"""

import argparse
import hashlib
import json
import base64
import sys
from datetime import datetime, timezone
from pathlib import Path


def ensure_deps():
    """Check dependencies."""
    try:
        from pqcrypto.sign.ml_dsa_87 import generate_keypair, sign, verify
        import requests
        return True
    except ImportError as e:
        print(f"Missing dependency: {e}")
        print("Install with: pip install pqcrypto requests")
        return False


def cmd_keygen(args):
    """Generate ML-DSA-87 keypair."""
    from pqcrypto.sign.ml_dsa_87 import generate_keypair

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Generating ML-DSA-87 keypair...")
    public_key, private_key = generate_keypair()

    pub_path = output_dir / "public.key"
    priv_path = output_dir / "private.key"

    with open(pub_path, "wb") as f:
        f.write(public_key)
    with open(priv_path, "wb") as f:
        f.write(private_key)

    # Create envelope
    envelope = {
        "algorithm": "ML-DSA-87",
        "standard": "FIPS-204",
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "public_key_sha3": hashlib.sha3_256(public_key).hexdigest()
    }
    env_path = output_dir / "envelope.json"
    with open(env_path, "w") as f:
        json.dump(envelope, f, indent=2)

    print(f"Public key:  {pub_path} ({len(public_key):,} bytes)")
    print(f"Private key: {priv_path} ({len(private_key):,} bytes)")
    print(f"Envelope:    {env_path}")
    print("\nKEYS GENERATED. Keep private.key SECRET!")


def cmd_sign(args):
    """Sign a document with ML-DSA-87."""
    from pqcrypto.sign.ml_dsa_87 import sign

    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return 1

    keys_dir = Path(args.keys).resolve()
    output_dir = Path(args.output).resolve() if args.output else file_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    priv_path = keys_dir / "private.key"
    if not priv_path.exists():
        print(f"Error: Private key not found: {priv_path}")
        print("Run: python pqc.py keygen --output <dir>")
        return 1

    with open(priv_path, "rb") as f:
        private_key = f.read()
    with open(file_path, "rb") as f:
        content = f.read()

    doc_hash = hashlib.sha3_256(content).hexdigest()
    print(f"Document: {file_path.name} ({len(content):,} bytes)")
    print(f"SHA3-256: {doc_hash}")

    print("Signing with ML-DSA-87...")
    signature = sign(private_key, content)

    sig_path = output_dir / f"{file_path.name}.sig"
    with open(sig_path, "wb") as f:
        f.write(signature)

    manifest = {
        "algorithm": "ML-DSA-87",
        "document_name": file_path.name,
        "document_size": len(content),
        "document_hash_sha3": doc_hash,
        "signature_size": len(signature),
        "signed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    manifest_path = output_dir / f"{file_path.name}.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"Signature: {sig_path} ({len(signature):,} bytes)")
    print(f"Manifest:  {manifest_path}")
    print("\nSIGNED SUCCESSFULLY")


def cmd_verify(args):
    """Verify a document signature."""
    from pqcrypto.sign.ml_dsa_87 import verify

    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return 1

    keys_dir = Path(args.keys).resolve()
    pub_path = keys_dir / "public.key"
    if not pub_path.exists():
        print(f"Error: Public key not found: {pub_path}")
        return 1

    sig_path = file_path.parent / f"{file_path.name}.sig"
    if args.signature:
        sig_path = Path(args.signature).resolve()
    if not sig_path.exists():
        print(f"Error: Signature not found: {sig_path}")
        return 1

    with open(pub_path, "rb") as f:
        public_key = f.read()
    with open(file_path, "rb") as f:
        content = f.read()
    with open(sig_path, "rb") as f:
        signature = f.read()

    print(f"Document:  {file_path.name}")
    print(f"Signature: {sig_path.name}")

    try:
        verify(public_key, content, signature)
        print("\n[VALID] Signature is authentic")
        return 0
    except Exception:
        print("\n[INVALID] Signature verification failed")
        return 1


def cmd_timestamp(args):
    """Submit document to OpenTimestamps."""
    import requests

    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return 1

    with open(file_path, "rb") as f:
        content = f.read()

    doc_hash = hashlib.sha256(content).digest()
    print(f"Document: {file_path.name}")
    print(f"SHA-256:  {doc_hash.hex()}")

    print("Submitting to OpenTimestamps...")
    try:
        r = requests.post(
            "https://a.pool.opentimestamps.org/digest",
            data=doc_hash,
            timeout=15
        )
        if r.status_code == 200:
            ots_path = file_path.parent / f"{file_path.name}.ots"
            with open(ots_path, "wb") as f:
                f.write(r.content)
            print(f"Timestamp: {ots_path}")
            print("\nTIMESTAMP SUBMITTED (confirms in 1-24 hours)")
            print("Verify at: https://opentimestamps.org")
        else:
            print(f"Error: Server returned {r.status_code}")
            return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def cmd_full(args):
    """Full workflow: sign + timestamp."""
    print("=" * 50)
    print("FULL PQC SIGNING WORKFLOW")
    print("=" * 50)

    # Check/generate keys
    keys_dir = Path(args.keys).resolve()
    if not (keys_dir / "private.key").exists():
        print("\n[1/3] Generating keys...")
        args.output = str(keys_dir)
        cmd_keygen(args)
    else:
        print(f"\n[1/3] Using existing keys in {keys_dir}")

    # Sign
    print("\n[2/3] Signing document...")
    cmd_sign(args)

    # Timestamp
    print("\n[3/3] Creating Bitcoin timestamp...")
    cmd_timestamp(args)

    print("\n" + "=" * 50)
    print("COMPLETE")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="PQC Document Signing (ML-DSA-87)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # keygen
    p_keygen = subparsers.add_parser("keygen", help="Generate keypair")
    p_keygen.add_argument("--output", "-o", default="./keys", help="Output directory")

    # sign
    p_sign = subparsers.add_parser("sign", help="Sign a document")
    p_sign.add_argument("file", help="File to sign")
    p_sign.add_argument("--keys", "-k", default="./keys", help="Keys directory")
    p_sign.add_argument("--output", "-o", help="Output directory")

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify signature")
    p_verify.add_argument("file", help="File to verify")
    p_verify.add_argument("--keys", "-k", default="./keys", help="Keys directory")
    p_verify.add_argument("--signature", "-s", help="Signature file path")

    # timestamp
    p_ts = subparsers.add_parser("timestamp", help="Create Bitcoin timestamp")
    p_ts.add_argument("file", help="File to timestamp")

    # full
    p_full = subparsers.add_parser("full", help="Full workflow: sign + timestamp")
    p_full.add_argument("file", help="File to process")
    p_full.add_argument("--keys", "-k", default="./keys", help="Keys directory")
    p_full.add_argument("--output", "-o", help="Output directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if not ensure_deps():
        return 1

    commands = {
        "keygen": cmd_keygen,
        "sign": cmd_sign,
        "verify": cmd_verify,
        "timestamp": cmd_timestamp,
        "full": cmd_full
    }

    return commands[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())
