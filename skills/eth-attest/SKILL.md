---
name: eth-attest
description: Deploy an Ethereum smart contract and register PQC-signed attestation JSONs on-chain to Ethereum Sepolia. Use when user wants to anchor PQC attestations to blockchain, register documents on-chain, deploy BateyAttestation contract, create an immutable blockchain record of signed documents, or says things like "register on-chain", "deploy the contract", "put this on the blockchain", "anchor to Ethereum". Works with ATT_*_signed.json files produced by the pqc-attest skill. Gas-sponsored via Alchemy Smart Wallets — no ETH required.
---

# eth-attest — On-Chain Attestation Registry

Deploys `BateyAttestation.sol` to Ethereum Sepolia and registers all `ATT_*_signed.json` files from a directory. Gas is sponsored by Alchemy (no ETH needed).

## Infrastructure

| Service | Value |
|---|---|
| RPC endpoint | `https://eth-sepolia.g.alchemy.com/v2/QjOdji0W5LXSVxKDAx8e2` |
| Gas sponsor policy | `71192c32-ae08-4e0a-9ad7-0162a4f06aff` |
| Smart wallet app | `C:\Users\peter\my-smart-wallets-app` → `http://localhost:3000/attestations` |
| Chain | Ethereum Sepolia (chainId 11155111) |

## Option A — Smart Wallet UI (recommended, no ETH needed)

```bash
cd C:\Users\peter\my-smart-wallets-app
npm run dev
# Open http://localhost:3000/attestations
# Log in with email/passkey → Deploy Contract + Register All
```

The Alchemy gas sponsorship policy covers all transaction fees.

**Next.js version note:** App was built on 14.2.4. If prompted to upgrade, run:
```bash
npm install next@latest --legacy-peer-deps
```

## Option B — CLI script (requires funded wallet)

```bash
# Install deps in target project
npm install ethers solc

# Run (generates wallet if DEPLOYER_KEY not set)
DEPLOYER_KEY=0x... node ~/.claude/skills/eth-attest/scripts/deploy_and_register.mjs \
  [path/to/att/json/dir] [rpc_url]

# Register to existing contract (skip deployment)
DEPLOYER_KEY=0x... CONTRACT_ADDRESS=0x... node ~/.claude/skills/eth-attest/scripts/deploy_and_register.mjs
```

If `DEPLOYER_KEY` is missing, a fresh wallet is generated and printed with funding instructions.

## Contract: BateyAttestation.sol

Source in `scripts/BateyAttestation.sol`. Functions:

```solidity
register(string id, string document, string author, string sha3_512)
get(string id) → Attestation
count() → uint256
```

- Each attestation is immutable once written (reverts on duplicate `id`)
- Emits `AttestationRegistered` event indexed by `attestation_id`

## Output

CLI script writes `batey_onchain_record.json` in the attestation directory:
```json
{
  "network": "sepolia",
  "contract": "0x...",
  "explorer": "https://sepolia.etherscan.io/address/0x...",
  "deployer": "0x...",
  "deployed_at": "2026-02-21T...",
  "attestations_registered": [
    { "id": "ATT_773", "tx": "0x...", "block": 12345 }
  ]
}
```

## Requirements

- Node.js >= 20
- `ethers` + `solc` npm packages (CLI path)
- OR: `C:\Users\peter\my-smart-wallets-app` running (UI path)
