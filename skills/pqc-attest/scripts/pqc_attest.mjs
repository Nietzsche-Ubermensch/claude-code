#!/usr/bin/env node
/**
 * PQC Dual Attestation — ML-DSA-87 (FIPS 204) + SPHINCS+-SHAKE-256s (FIPS 205)
 *
 * Accepts either a PDF file path OR a raw SHA3-512 hex hash as the first argument.
 *
 * Usage (PDF — recommended):
 *   node pqc_attest.mjs <path/to/file.pdf> <attestation_id> "<document_title>" "<author>" [key_id]
 *
 * Usage (raw hash):
 *   node pqc_attest.mjs <sha3_512_hex> <attestation_id> "<document_title>" "<author>" [key_id]
 *
 * Outputs:
 *   <attestation_id>_signed.json  — self-contained: title, author, full document text, hash, both signatures
 *   ~/Desktop/<attestation_id>_<lastname>_signed.json — Desktop copy
 *
 * Keys stored at: ~/.claude/pqc_keys/<key_id>_mldsa87.{pk,sk}
 *                               and  <key_id>_sphincs_shake256s.{pk,sk}
 *
 * Requires: @noble/post-quantum  (npm install @noble/post-quantum)
 *           pdftotext             (poppler-utils — for PDF text extraction)
 * Node.js >= 20
 */

import { ml_dsa87 } from '@noble/post-quantum/ml-dsa.js';
import { slh_dsa_shake_256s } from '@noble/post-quantum/slh-dsa.js';
import { randomBytes, createHash } from 'crypto';
import { writeFileSync, existsSync, readFileSync, mkdirSync, copyFileSync } from 'fs';
import { join, basename } from 'path';
import { homedir } from 'os';
import { execSync } from 'child_process';

// ── Args ──────────────────────────────────────────────────────────────────────
const [input, attestation_id, document_title, author, key_id = 'prime'] = process.argv.slice(2);

if (!input || !attestation_id || !document_title || !author) {
  console.error('Usage: node pqc_attest.mjs <pdf_path|sha3_512_hex> <attestation_id> "<document>" "<author>" [key_id]');
  process.exit(1);
}

// ── Determine if input is a file path or raw hash ────────────────────────────
const isHash = /^[0-9a-fA-F]{128}$/.test(input);
const isFile = !isHash && existsSync(input);

if (!isHash && !isFile) {
  console.error(`Error: "${input}" is neither a valid SHA3-512 hex string (128 chars) nor an existing file path.`);
  process.exit(1);
}

// ── Setup ─────────────────────────────────────────────────────────────────────
const KEY_DIR = join(homedir(), '.claude', 'pqc_keys');
const DESKTOP = join(homedir(), 'Desktop');
mkdirSync(KEY_DIR, { recursive: true });

let sha3_512_hex, payload, document_text = null;

if (isFile) {
  console.log(`\nReading: ${input}`);
  const fileBytes = readFileSync(input);
  sha3_512_hex = createHash('sha3-512').update(fileBytes).digest('hex');

  // Extract text if pdftotext available
  try {
    document_text = execSync(`pdftotext "${input}" -`, { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }).trim();
    console.log(`Extracted text: ${document_text.length} chars`);
  } catch {
    console.log('pdftotext not available — document_text will be omitted');
  }
} else {
  sha3_512_hex = input;
}

payload = Buffer.from(sha3_512_hex, 'hex');
console.log(`\nATT: ${attestation_id} | ${document_title} | ${author}`);
console.log(`SHA3-512: ${sha3_512_hex.slice(0, 16)}... (${payload.length} bytes)\n`);

// ── Helper ────────────────────────────────────────────────────────────────────
function loadOrGenerate(pkPath, skPath, genFn) {
  if (existsSync(pkPath) && existsSync(skPath)) {
    const pk = new Uint8Array(readFileSync(pkPath));
    const sk = new Uint8Array(readFileSync(skPath));
    console.log(`  Loaded keypair — pk:${pk.length}B sk:${sk.length}B`);
    return { pk, sk };
  }
  const { pk, sk } = genFn();
  writeFileSync(pkPath, Buffer.from(pk.buffer, pk.byteOffset, pk.byteLength));
  writeFileSync(skPath, Buffer.from(sk.buffer, sk.byteOffset, sk.byteLength));
  console.log(`  Generated — pk:${pk.length}B sk:${sk.length}B  → saved`);
  return { pk, sk };
}

// ── ML-DSA-87 (FIPS 204) ─────────────────────────────────────────────────────
console.log('[1/2] ML-DSA-87...');
const { pk: mlPk, sk: mlSk } = loadOrGenerate(
  join(KEY_DIR, `${key_id}_mldsa87.pk`),
  join(KEY_DIR, `${key_id}_mldsa87.sk`),
  () => {
    const keys = ml_dsa87.keygen(randomBytes(32));
    return { pk: keys.publicKey, sk: keys.secretKey };
  }
);
const mlSig = ml_dsa87.sign(payload, mlSk);
const mlValid = ml_dsa87.verify(mlSig, payload, mlPk);
console.log(`  Signature: ${mlSig.length}B  Verify: ${mlValid ? '✓ VALID' : '✗ INVALID'}`);
if (!mlValid) { console.error('FATAL: ML-DSA-87 verification failed'); process.exit(1); }

// ── SPHINCS+-SHAKE-256s (FIPS 205) ───────────────────────────────────────────
console.log('[2/2] SPHINCS+-SHAKE-256s...');
const { pk: spPk, sk: spSk } = loadOrGenerate(
  join(KEY_DIR, `${key_id}_sphincs_shake256s.pk`),
  join(KEY_DIR, `${key_id}_sphincs_shake256s.sk`),
  () => {
    const keys = slh_dsa_shake_256s.keygen(randomBytes(96));
    return { pk: keys.publicKey, sk: keys.secretKey };
  }
);
const spSig = slh_dsa_shake_256s.sign(payload, spSk);
const spValid = slh_dsa_shake_256s.verify(spSig, payload, spPk);
console.log(`  Signature: ${spSig.length}B  Verify: ${spValid ? '✓ VALID' : '✗ INVALID'}`);
if (!spValid) { console.error('FATAL: SPHINCS+ verification failed'); process.exit(1); }

// ── Manifest ──────────────────────────────────────────────────────────────────
const manifest = {
  attestation_id,
  document: document_title,
  author,
  ...(document_text && { document_text }),
  sha3_512: sha3_512_hex,
  timestamp_utc: new Date().toISOString(),
  signatures: {
    ml_dsa_87: {
      algorithm: 'ML-DSA-87 (FIPS 204 / CRYSTALS-Dilithium Level 5)',
      public_key_b64: Buffer.from(mlPk).toString('base64'),
      signature_b64: Buffer.from(mlSig).toString('base64'),
      signature_length_bytes: mlSig.length,
      verified: mlValid,
    },
    sphincs_shake_256s: {
      algorithm: 'SPHINCS+-SHAKE-256s (FIPS 205)',
      public_key_b64: Buffer.from(spPk).toString('base64'),
      signature_b64: Buffer.from(spSig).toString('base64'),
      signature_length_bytes: spSig.length,
      verified: spValid,
    },
  },
};

const outFile = `${attestation_id}_signed.json`;
writeFileSync(outFile, JSON.stringify(manifest, null, 2));
console.log(`\n✓ Attestation written → ${outFile}`);

// Desktop copy: <ATT_ID>_<lastname>_signed.json
try {
  const lastname = author.trim().split(/\s+/).pop();
  const desktopFile = join(DESKTOP, `${attestation_id}_${lastname}_signed.json`);
  copyFileSync(outFile, desktopFile);
  console.log(`✓ Desktop copy     → ${desktopFile}`);
} catch (e) {
  console.log(`  Desktop copy skipped: ${e.message}`);
}

console.log(`\nML-DSA-87: ${mlValid ? 'VALID' : 'INVALID'} | SPHINCS+-SHAKE-256s: ${spValid ? 'VALID' : 'INVALID'}`);
if (document_text) console.log(`Document text: ${document_text.length} chars embedded`);
