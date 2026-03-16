/**
 * eth-attest — Deploy BateyAttestation contract + register PQC-signed JSONs on-chain.
 *
 * Usage:
 *   DEPLOYER_KEY=0x... node deploy_and_register.mjs [att_dir] [rpc_url]
 *
 * Defaults:
 *   att_dir  = current working directory (scans for ATT_*_signed.json)
 *   rpc_url  = https://eth-sepolia.g.alchemy.com/v2/<ALCHEMY_KEY>
 *
 * If DEPLOYER_KEY is not set, generates a new wallet and exits with funding instructions.
 * If CONTRACT_ADDRESS is set, skips deployment and registers to existing contract.
 *
 * Requires: ethers, solc  (npm install ethers solc)
 * Node.js >= 20
 */

import { ethers } from 'ethers';
import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import solc from 'solc';

const __dir   = dirname(fileURLToPath(import.meta.url));
const ATT_DIR = process.argv[2] || process.cwd();
const RPC_URL = process.argv[3] || process.env.RPC_URL || 'https://eth-sepolia.g.alchemy.com/v2/QjOdji0W5LXSVxKDAx8e2';

// ── Compile contract ──────────────────────────────────────────────────────────
const SOL = readFileSync(join(__dir, 'BateyAttestation.sol'), 'utf8');
const compiled = JSON.parse(solc.compile(JSON.stringify({
  language: 'Solidity',
  sources: { 'BateyAttestation.sol': { content: SOL } },
  settings: { outputSelection: { '*': { '*': ['abi', 'evm.bytecode'] } } },
})));
const { abi: ABI, evm: { bytecode: { object: bc } } } =
  compiled.contracts['BateyAttestation.sol']['BateyAttestation'];
const BYTECODE = '0x' + bc;

// ── Wallet ────────────────────────────────────────────────────────────────────
const provider = new ethers.JsonRpcProvider(RPC_URL);

if (!process.env.DEPLOYER_KEY) {
  const w = ethers.Wallet.createRandom();
  console.log('\n⚠️  No DEPLOYER_KEY. Generated a fresh wallet:');
  console.log('  Address    :', w.address);
  console.log('  Private key:', w.privateKey);
  console.log('\nFund with Sepolia ETH then re-run:');
  console.log(`  DEPLOYER_KEY=${w.privateKey} node deploy_and_register.mjs`);
  console.log('\nFaucet: https://www.alchemy.com/faucets/ethereum-sepolia');
  console.log('Or use Alchemy Smart Wallets (gas sponsored) — see SKILL.md');
  process.exit(0);
}

const wallet  = new ethers.Wallet(process.env.DEPLOYER_KEY, provider);
const balance = await provider.getBalance(wallet.address);
console.log(`Deployer: ${wallet.address}  (${ethers.formatEther(balance)} ETH)`);

// ── Deploy (unless CONTRACT_ADDRESS already set) ──────────────────────────────
let contractAddress = process.env.CONTRACT_ADDRESS;
if (!contractAddress) {
  console.log('\nDeploying BateyAttestation...');
  const factory  = new ethers.ContractFactory(ABI, BYTECODE, wallet);
  const deployed = await factory.deploy();
  await deployed.waitForDeployment();
  contractAddress = await deployed.getAddress();
  console.log(`✓ Contract: ${contractAddress}`);
  console.log(`  Explorer: https://sepolia.etherscan.io/address/${contractAddress}`);
}

// ── Load attestation JSONs ────────────────────────────────────────────────────
const files = readdirSync(ATT_DIR)
  .filter(f => /^ATT_\d+.*signed\.json$/.test(f))
  .sort();

console.log(`\nRegistering ${files.length} attestations → ${contractAddress}`);
const instance = new ethers.Contract(contractAddress, ABI, wallet);
const results  = [];

for (const file of files) {
  const att = JSON.parse(readFileSync(join(ATT_DIR, file), 'utf8'));
  process.stdout.write(`  ${att.attestation_id} — ${att.document.slice(0, 45)}... `);
  try {
    const tx      = await instance.register(att.attestation_id, att.document, att.author, att.sha3_512);
    const receipt = await tx.wait();
    console.log(`✓  tx: ${receipt.hash}`);
    results.push({ id: att.attestation_id, tx: receipt.hash, block: receipt.blockNumber });
  } catch (e) {
    console.log(`✗  ${e.message.slice(0, 80)}`);
  }
}

// ── Save deployment record ────────────────────────────────────────────────────
const record = {
  network: 'sepolia',
  contract: contractAddress,
  explorer: `https://sepolia.etherscan.io/address/${contractAddress}`,
  deployer: wallet.address,
  deployed_at: new Date().toISOString(),
  attestations_registered: results,
};
const outFile = join(ATT_DIR, 'batey_onchain_record.json');
writeFileSync(outFile, JSON.stringify(record, null, 2));
console.log(`\n✓ ${results.length}/${files.length} attestations registered`);
console.log(`✓ Record saved → ${outFile}`);
console.log(`\nContract: ${contractAddress}`);
console.log(`Explorer: https://sepolia.etherscan.io/address/${contractAddress}`);
