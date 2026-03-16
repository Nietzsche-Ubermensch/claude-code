/**
 * eth-attest AA — Deploy BateyAttestation + register all ATT_*_signed.json
 * using Alchemy Account Abstraction (ERC-4337). No ETH required — gas is
 * sponsored by the Alchemy gas policy.
 *
 * Usage:
 *   node deploy_and_register_aa.mjs [att_dir] [policy_id]
 *
 * Defaults:
 *   att_dir   = current working directory
 *   policy_id = 85da6ab4-970b-4fef-ba7d-d58e12063fe8
 *
 * Resolves node_modules from C:\Users\peter\my-smart-wallets-app
 * Node.js >= 20
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __dir   = dirname(fileURLToPath(import.meta.url));
const ATT_DIR = process.argv[2] || process.cwd();
const POLICY  = process.argv[3] || '85da6ab4-970b-4fef-ba7d-d58e12063fe8';
const RPC_KEY = 'QjOdji0W5LXSVxKDAx8e2';
const RPC_URL = `https://eth-sepolia.g.alchemy.com/v2/${RPC_KEY}`;
const CHAIN_ID = 11155111;

// Resolve modules from the smart-wallets-app which has viem + account-kit
const APP_MODULES = 'C:/Users/peter/my-smart-wallets-app/node_modules';
const req = createRequire(join(APP_MODULES, 'placeholder'));

// ── Imports via dynamic require from app node_modules ─────────────────────────
const { createPublicClient, http, encodeFunctionData, encodeDeployData,
        parseAbi, keccak256, toBytes, pad, concat, toHex } = await import(
  join(APP_MODULES, 'viem/index.js').replace(/\\/g, '/')
).catch(() => import('viem'));

const { sepolia } = await import(
  join(APP_MODULES, 'viem/chains/index.js').replace(/\\/g, '/')
).catch(() => import('viem/chains'));

const { privateKeyToAccount, generatePrivateKey } = await import(
  join(APP_MODULES, 'viem/accounts/index.js').replace(/\\/g, '/')
).catch(() => import('viem/accounts'));

// ── Load contract ABI + bytecode ──────────────────────────────────────────────
const CONTRACT_JSON = JSON.parse(
  readFileSync(join('C:/Users/peter/my-smart-wallets-app/lib/BateyAttestation.json'), 'utf8')
);
const CONTRACT_ABI      = CONTRACT_JSON.abi;
const CONTRACT_BYTECODE = CONTRACT_JSON.bytecode;

// ── Load attestation files ────────────────────────────────────────────────────
const files = readdirSync(ATT_DIR)
  .filter(f => /^ATT_\d+.*signed\.json$/.test(f))
  .sort();

if (files.length === 0) {
  console.error(`No ATT_*_signed.json files found in ${ATT_DIR}`);
  process.exit(1);
}
console.log(`Found ${files.length} attestation files in ${ATT_DIR}`);

const attestations = files.map(f => {
  const j = JSON.parse(readFileSync(join(ATT_DIR, f), 'utf8'));
  return { id: j.attestation_id, document: j.document, author: j.author, sha3_512: j.sha3_512 };
});

// ── ERC-4337 constants (Sepolia v0.6) ─────────────────────────────────────────
const ENTRY_POINT      = '0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789';
const LIGHT_ACCOUNT_FACTORY = '0x00004EC70002a32400f8ae005A26081065620D20'; // Alchemy LightAccount factory v1

// ── Signer ─────────────────────────────────────────────────────────────────────
const KEY_FILE = join(__dir, '../light_account.key');
let privateKey;
if (existsSync(KEY_FILE)) {
  privateKey = readFileSync(KEY_FILE, 'utf8').trim();
  console.log('Loaded existing signer key');
} else {
  privateKey = generatePrivateKey();
  writeFileSync(KEY_FILE, privateKey);
  console.log('Generated new signer key (saved for reuse)');
}
const owner = privateKeyToAccount(privateKey);
console.log(`Signer: ${owner.address}`);

// ── Public client ─────────────────────────────────────────────────────────────
const publicClient = createPublicClient({ chain: sepolia, transport: http(RPC_URL) });

// ── RPC helper ────────────────────────────────────────────────────────────────
async function rpc(method, params) {
  const res = await fetch(RPC_URL, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
  });
  const j = await res.json();
  if (j.error) throw new Error(`RPC ${method}: ${j.error.message}`);
  return j.result;
}

// ── Compute LightAccount address ──────────────────────────────────────────────
const FACTORY_ABI = parseAbi([
  'function createAccount(address owner, uint256 salt) returns (address)',
  'function getAddress(address owner, uint256 salt) view returns (address)',
]);

const SALT = 0n;
const smartAccountAddress = await publicClient.readContract({
  address: ENTRY_POINT, // placeholder — read from factory
  abi: FACTORY_ABI,
  functionName: 'getAddress',
  args: [owner.address, SALT],
}).catch(async () => {
  // Fallback: simulate via eth_call on factory
  const data = encodeFunctionData({ abi: FACTORY_ABI, functionName: 'getAddress', args: [owner.address, SALT] });
  const result = await rpc('eth_call', [{ to: LIGHT_ACCOUNT_FACTORY, data }, 'latest']);
  return ('0x' + result.slice(-40));
});

console.log(`Smart account: ${smartAccountAddress}`);

// Check if already deployed
const code = await rpc('eth_getCode', [smartAccountAddress, 'latest']);
const isDeployed = code !== '0x';
console.log(`Smart account deployed: ${isDeployed}`);

// ── Get initCode (for first UserOp if account not deployed) ──────────────────
function getInitCode() {
  if (isDeployed) return '0x';
  const calldata = encodeFunctionData({
    abi: FACTORY_ABI,
    functionName: 'createAccount',
    args: [owner.address, SALT],
  });
  return LIGHT_ACCOUNT_FACTORY + calldata.slice(2);
}

// ── Get account nonce ─────────────────────────────────────────────────────────
const ENTRY_ABI = parseAbi(['function getNonce(address sender, uint192 key) view returns (uint256)']);
async function getNonce() {
  const data = encodeFunctionData({ abi: ENTRY_ABI, functionName: 'getNonce', args: [smartAccountAddress, 0n] });
  const result = await rpc('eth_call', [{ to: ENTRY_POINT, data }, 'latest']);
  return BigInt(result);
}

// ── LightAccount execute ABI ──────────────────────────────────────────────────
const EXECUTE_ABI = parseAbi(['function execute(address target, uint256 value, bytes calldata data)']);

// ── Build + send a sponsored UserOperation ───────────────────────────────────
async function sendUserOp(callData, label) {
  const nonce = await getNonce();
  const initCode = nonce === 0n ? getInitCode() : '0x';

  // Dummy UserOp for gas estimation
  const dummyOp = {
    sender: smartAccountAddress,
    nonce: toHex(nonce),
    initCode,
    callData,
    callGasLimit: '0x0',
    verificationGasLimit: '0x0',
    preVerificationGas: '0x0',
    maxFeePerGas: '0x0',
    maxPriorityFeePerGas: '0x0',
    paymasterAndData: '0x',
    signature: '0x' + 'ff'.repeat(65),
  };

  // Request gas + paymaster data from Alchemy
  const sponsored = await rpc('alchemy_requestGasAndPaymasterAndData', [{
    policyId: POLICY,
    entryPoint: ENTRY_POINT,
    userOperation: dummyOp,
    dummySignature: '0x' + 'ff'.repeat(65),
  }]);

  const userOp = {
    ...dummyOp,
    callGasLimit:         sponsored.callGasLimit,
    verificationGasLimit: sponsored.verificationGasLimit,
    preVerificationGas:   sponsored.preVerificationGas,
    maxFeePerGas:         sponsored.maxFeePerGas,
    maxPriorityFeePerGas: sponsored.maxPriorityFeePerGas,
    paymasterAndData:     sponsored.paymasterAndData,
  };

  // Compute UserOp hash and sign
  const abiCoder = { encode: (...args) => { /* viem encodeAbiParameters */ } };
  // Manual ABI encoding of userOpHash
  const { encodeAbiParameters, parseAbiParameters } = await import(
    join(APP_MODULES, 'viem/index.js').replace(/\\/g, '/')
  ).catch(() => import('viem'));

  const packed = encodeAbiParameters(
    parseAbiParameters('address,uint256,bytes32,bytes32,uint256,uint256,uint256,uint256,uint256,bytes32'),
    [
      userOp.sender,
      BigInt(userOp.nonce),
      keccak256(userOp.initCode),
      keccak256(userOp.callData),
      BigInt(userOp.callGasLimit),
      BigInt(userOp.verificationGasLimit),
      BigInt(userOp.preVerificationGas),
      BigInt(userOp.maxFeePerGas),
      BigInt(userOp.maxPriorityFeePerGas),
      keccak256(userOp.paymasterAndData),
    ]
  );

  const opHash = keccak256(
    encodeAbiParameters(
      parseAbiParameters('bytes32,address,uint256'),
      [keccak256(packed), ENTRY_POINT, BigInt(CHAIN_ID)]
    )
  );

  const sig = await owner.signMessage({ message: { raw: toBytes(opHash) } });
  userOp.signature = sig;

  process.stdout.write(`  ${label} ... `);
  const userOpHash = await rpc('eth_sendUserOperation', [userOp, ENTRY_POINT]);

  // Wait for receipt
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 2000));
    const receipt = await rpc('eth_getUserOperationReceipt', [userOpHash]).catch(() => null);
    if (receipt?.success === true || receipt?.success === 'true') {
      console.log(`✓  tx: ${receipt.receipt.transactionHash}`);
      return receipt.receipt.transactionHash;
    }
    if (receipt?.success === false) throw new Error(`UserOp failed: ${JSON.stringify(receipt)}`);
  }
  throw new Error(`Timeout waiting for UserOp ${userOpHash}`);
}

// ── Step 1: Deploy BateyAttestation contract ──────────────────────────────────
let contractAddress = process.env.CONTRACT_ADDRESS;

if (!contractAddress) {
  console.log('\nDeploying BateyAttestation contract...');
  const deployCalldata = encodeFunctionData({
    abi: EXECUTE_ABI,
    functionName: 'execute',
    args: ['0x0000000000000000000000000000000000000000', 0n, CONTRACT_BYTECODE],
  });

  const deployTx = await sendUserOp(deployCalldata, 'Deploy BateyAttestation');

  // Fetch the tx receipt to find the created contract address
  await new Promise(r => setTimeout(r, 3000));
  const txReceipt = await rpc('eth_getTransactionReceipt', [deployTx]);
  // Contract is created as a log or in the receipt contractAddress field
  // For a CREATE from a smart account, look at internal txs
  // Alchemy provides this via alchemy_getTransactionReceipts or trace
  const trace = await rpc('debug_traceTransaction', [deployTx, { tracer: 'callTracer' }]).catch(() => null);
  if (trace) {
    const findCreated = (call) => {
      if (call.type === 'CREATE' || call.type === 'CREATE2') return call.to;
      if (call.calls) for (const c of call.calls) { const r = findCreated(c); if (r) return r; }
      return null;
    };
    contractAddress = findCreated(trace);
  }

  if (!contractAddress) {
    // Fallback: compute CREATE address from smart account + nonce
    const { getContractAddress } = await import('viem');
    const acctNonce = await rpc('eth_getTransactionCount', [smartAccountAddress, 'latest']);
    contractAddress = getContractAddress({ from: smartAccountAddress, nonce: BigInt(acctNonce) - 1n });
  }

  console.log(`✓ Contract deployed: ${contractAddress}`);
  console.log(`  Explorer: https://sepolia.etherscan.io/address/${contractAddress}`);
}

// ── Step 2: Register all attestations ────────────────────────────────────────
console.log(`\nRegistering ${attestations.length} attestations → ${contractAddress}`);
const results = [];

for (const att of attestations) {
  const registerData = encodeFunctionData({
    abi: CONTRACT_ABI,
    functionName: 'register',
    args: [att.id, att.document, att.author, att.sha3_512],
  });
  const callData = encodeFunctionData({
    abi: EXECUTE_ABI,
    functionName: 'execute',
    args: [contractAddress, 0n, registerData],
  });

  try {
    const tx = await sendUserOp(callData, `${att.id} — ${att.document.slice(0, 40)}`);
    results.push({ id: att.id, tx, block: null });
  } catch (e) {
    console.log(`✗  ${e.message.slice(0, 80)}`);
    results.push({ id: att.id, error: e.message.slice(0, 80) });
  }
}

// ── Save record ───────────────────────────────────────────────────────────────
const record = {
  network: 'sepolia',
  contract: contractAddress,
  explorer: `https://sepolia.etherscan.io/address/${contractAddress}`,
  smart_account: smartAccountAddress,
  deployed_at: new Date().toISOString(),
  attestations_registered: results,
};
const outFile = join(ATT_DIR, 'batey_onchain_record.json');
writeFileSync(outFile, JSON.stringify(record, null, 2));
console.log(`\n✓ ${results.filter(r => r.tx).length}/${attestations.length} attestations registered`);
console.log(`✓ Record: ${outFile}`);
console.log(`\nContract: ${contractAddress}`);
console.log(`Explorer: https://sepolia.etherscan.io/address/${contractAddress}`);
