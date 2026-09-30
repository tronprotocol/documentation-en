# wallet-cli — TypeScript implementation

The agent-first implementation of wallet-cli, built for automation: every command has a stable JSON envelope, deterministic exit codes, and discoverable schemas; interactive prompts are kept to a short allowlist — `create`, the `import` variants, `backup`, `change-password` and `delete` — and everywhere else a missing credential is an error, never a prompt. For what wallet-cli is and how the two implementations compare, see the [repository overview](../index.md); for the original, see the [Java implementation](../java/index.md).

## Key features

- **Agent-first** — stable JSON output, deterministic exit codes, and discoverable schemas, built for scripts, CI, and AI agents (details in [The contract, in one paragraph](#the-contract-in-one-paragraph)).
- **Encrypted local storage** — software keystores are encrypted on disk; secrets are never passed via argv or environment variables.
- **Software and Ledger signing** — sign in software, or on a Ledger device (the private key never leaves the device).
- **Covers the full TRON feature surface** — HD wallets, TRX and TRC20/TRC10 transfers, staking / resource delegation, voting / rewards, governance proposals and super-representative operation, smart-contract calls, deployment and governance, TRC10 issuance, the on-chain Bancor exchange, multi-sig, GasFree transfers, message signing, and on-chain queries.
- **TRON and EVM chains** — one account holds an address on each; transfers, tokens, contracts, signing and chain queries work the same on both, and TRON-only protocol features are refused on EVM rather than half-working.

## Table of contents

- [Supported chains](#supported-chains)
- [Install](#install)
- [Quickstart](#quickstart)
- [Commands](#commands)
  - [Wallets and accounts](#wallets-and-accounts)
  - [Transactions](#transactions)
  - [On-chain queries](#on-chain-queries)
  - [Tokens, contracts, staking, signing](#tokens-contracts-staking-signing)
  - [Governance, TRC10, and the on-chain exchange](#governance-trc10-and-the-on-chain-exchange)
  - [Local tools and configuration](#local-tools-and-configuration)
- [The contract, in one paragraph](#the-contract-in-one-paragraph)
- [Understanding the chains](#understanding-the-chains)
- [Troubleshooting](#troubleshooting)

## Supported chains

Networks are identified by a canonical [CAIP-2](https://chainagnostic.org/CAIPs/caip-2) `namespace:reference` id, and each belongs to one of two chain **families**, `tron` or `evm`. `--network` also accepts the short alias:

| Network id | Alias | What it is | Native coin value |
|---|---|---|---|
| `tron:728126428` | `tron` | Production TRON | **Real funds** |
| `tron:3448148188` | `nile` | Primary TRON testnet (faucet at nileex.io) | None — use freely |
| `tron:2494104990` | `shasta` | Alternate TRON testnet | None |
| `eip155:1` | `ethereum` | Ethereum mainnet | **Real funds** |
| `eip155:11155111` | `sepolia` | Ethereum test network | None |
| `eip155:56` | `bsc` | BNB Smart Chain | **Real funds** |
| `eip155:97` | `bsc-testnet` | BNB Smart Chain test network | None |
| `eip155:8453` | `base` | Base | **Real funds** |
| `eip155:84532` | `base-sepolia` | Base test network | None |

Balances, tokens, and transactions are isolated per network. The family decides two things: **which address** a command acts as — one account holds a TRON base58 address and an EVM `0x` address, derived from the same seed — and **which commands exist**, since TRON protocol features (staking, SR voting, TRC10, the Bancor exchange, on-chain permissions, GasFree) have no EVM counterpart and are refused there with `family_mismatch`. Fees follow the family too: TRON's `tron-resource` model (bandwidth + energy) or EVM gas. See [networks](concepts/networks.md), [accounts](concepts/accounts-and-hd.md) and [energy & bandwidth](concepts/energy-bandwidth.md).

The TRON ids used before CAIP-2 (`tron:mainnet`, `tron:nile`, `tron:shasta`) remain permanent aliases, so existing invocations keep working — but **output** now reports the CAIP-2 id, so a consumer that string-matches `tron:nile` must be updated.

## Install

**Prerequisites**: [Node.js](https://nodejs.org) **20 or later** (`node --version` to check). Ledger signing additionally needs a supported Ledger device with the TRON or Ethereum app installed — see the [Ledger guide](guide/ledger.md).

```bash
npm install -g @tron-walletcli/wallet-cli
```

Note the scope: the package is `@tron-walletcli/wallet-cli`, not the bare `wallet-cli` name (which is an unrelated third-party package).

Verify:

```bash
wallet-cli --version
```

```console
<version>          # shows the installed version
```

Upgrade with `npm update -g @tron-walletcli/wallet-cli`; uninstall with `npm uninstall -g @tron-walletcli/wallet-cli`.

**From source** (contributors, or to run unreleased changes) — additionally requires Git:

```bash
git clone https://github.com/tronprotocol/wallet-cli.git
cd wallet-cli/ts
npm ci && npm run build
npm link             # puts `wallet-cli` on your PATH (or run: node dist/index.js)
```

## Quickstart

**Create your first wallet.** `create` prompts for a master password, then shows the new account:

```bash
wallet-cli create --label main
```

```console
✅ Created wallet "main"
  Account ID    wlt_2dbv24de.0
  Type          HD
  TRON address  TTVdGTBXY5mmY3nJFGUp7Vo898kUJ6gtFQ
  EVM address   0x7B28FE10FBccE88c3967ff0Fd64f1ffB46b46C9C
  Active        yes

⚠️ Recovery phrase is encrypted locally and was not printed.
⚠️ Run `backup` soon and store the file offline.
```

```bash
wallet-cli list
```

```console
HD  wlt_2dbv24de
└─ [0] main  TTVdGTBXY5mmY3nJFGUp7Vo898kUJ6gtFQ  (active)
```

The full flow — fund it on a testnet, check the balance, send your first TRX — is in the [getting-started guide](guide/getting-started.md). From there, go deeper by topic: [sending tokens](guide/send-tokens.md) · [staking & resources](guide/stake-and-resources.md) · [using a Ledger hardware wallet](guide/ledger.md) · [scripting](guide/scripting.md).

## Commands

Every command — including every subcommand — has its own reference page; the full per-command list is in the **[command index](commands/index.md)**, and `wallet-cli <command> --help` is the built-in equivalent.

### Wallets and accounts

Create, import, and manage local wallets and accounts.

| Command | Description |
|---|---|
| [`create`](commands/create.md) | Create a new HD wallet (BIP39 seed) |
| `import` | Import a wallet — [mnemonic](commands/import/mnemonic.md) · [private-key](commands/import/private-key.md) · [keystore](commands/import/keystore.md) · [ledger](commands/import/ledger.md) · [watch](commands/import/watch.md)-only |
| [`list`](commands/list.md) | List wallets and accounts |
| [`use`](commands/use.md) · [`current`](commands/current.md) | Set / show the active account (`current --qr` for a receive QR) |
| [`derive`](commands/derive.md) | Derive the next HD account from a seed wallet |
| [`rename`](commands/rename.md) · [`backup`](commands/backup.md) · [`delete`](commands/delete.md) | Rename, back up, or delete an account (backup writes secret + metadata, mode 0600; `--keystore` for Web3 keystore format, `--records` for the export audit log) |
| [`change-password`](commands/change-password.md) | Change the master password (re-encrypt all software keystores) |

### Transactions

Send, broadcast, inspect, and co-sign transactions.

| Command | Description |
|---|---|
| [`tx send`](commands/tx/send.md) | Send native TRX or TRC20/TRC10 tokens |
| [`tx broadcast`](commands/tx/broadcast.md) | Broadcast a presigned transaction |
| [`tx status`](commands/tx/status.md) · [`tx info`](commands/tx/info.md) | Confirmation status, or full detail + receipt |
| [`tx sign`](commands/tx/sign.md) · [`tx approvals`](commands/tx/approvals.md) · [`tx multisig`](commands/tx/multisig.md) | Co-sign multi-sig transactions and inspect approvals |

### On-chain queries

Read account, block, and chain state.

| Command | Description |
|---|---|
| [`account balance`](commands/account/balance.md) · [`info`](commands/account/info.md) · [`portfolio`](commands/account/portfolio.md) | Balance, raw account data, or balances with USD estimate |
| [`account history`](commands/account/history.md) | Transaction history (requires TronGrid) |
| [`account activate`](commands/account/activate.md) · [`set`](commands/account/set.md) | Activate an account, or set its on-chain name / ID |
| [`block`](commands/block.md) | Get a block (latest if omitted) |
| [`chain params`](commands/chain/params.md) · [`prices`](commands/chain/prices.md) · [`node`](commands/chain/node.md) | Governance params, resource prices, or node status |

### Tokens, contracts, staking, signing

Token and contract operations, resource staking, voting rewards, message signing, and permissions.

| Command                                                                                         | Description                                                                                                                                                                                                                          |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`token`](commands/token/index.md)                                                         | Token address book and queries ([balance](commands/token/balance.md) · [info](commands/token/info.md) · [add](commands/token/add.md) · [list](commands/token/list.md) · [remove](commands/token/remove.md)) |
| [`contact`](commands/contact/index.md)                                                     | Recipient contact book ([add](commands/contact/add.md) · [list](commands/contact/list.md) · [remove](commands/contact/remove.md))                                                                                     |
| [`contract`](commands/contract/index.md)                                                   | Call, send, deploy, inspect, and govern contracts ([call](commands/contract/call.md) · [send](commands/contract/send.md) · [deploy](commands/contract/deploy.md) · [info](commands/contract/info.md) · [clear-abi](commands/contract/clear-abi.md) · [set-origin-energy-limit](commands/contract/set-origin-energy-limit.md) · [set-user-resource-percent](commands/contract/set-user-resource-percent.md) · [create2](commands/contract/create2.md)) |
| [`stake`](commands/stake/index.md)                                                         | Stake / delegate resources ([freeze](commands/stake/freeze.md) · [unfreeze](commands/stake/unfreeze.md) · [delegate](commands/stake/delegate.md) · [info](commands/stake/info.md), …)                            |
| [`vote`](commands/vote/index.md) · [`reward`](commands/reward/index.md)               | Vote for super representatives and claim voting rewards                                                                                                                                                                              |
| [`message`](commands/message/index.md) · [`typed-data`](commands/typed-data/index.md) | Sign arbitrary messages, or EIP-712/TIP-712 structured data                                                                                                                                                                          |
| [`permission`](commands/permission/index.md)                                               | View / update account permissions for multi-sig                                                                                                                                                                                      |
| [`gasfree`](commands/gasfree/index.md)                                                     | Gas-free token transfers via the GasFree service                                                                                                                                                                                     |

### Governance, TRC10, and the on-chain exchange

Chain governance, super-representative operation, and TRON's protocol-level TRC10 and Bancor exchange mechanics.

| Command | Description |
|---|---|
| [`proposal`](commands/proposal/index.md) | Chain-parameter proposals ([list](commands/proposal/list.md) · [show](commands/proposal/show.md) · [create](commands/proposal/create.md) · [approve](commands/proposal/approve.md) · [delete](commands/proposal/delete.md)) — `list` / `show` are open to anyone, the write commands require a registered witness |
| [`witness`](commands/witness/index.md) | Register and operate a super representative ([create](commands/witness/create.md) · [update](commands/witness/update.md) · [set-brokerage](commands/witness/set-brokerage.md)) |
| [`asset`](commands/asset/index.md) | Issue and manage TRC10 tokens ([issue](commands/asset/issue.md) · [update](commands/asset/update.md) · [participate](commands/asset/participate.md) · [unfreeze](commands/asset/unfreeze.md) · [info](commands/asset/info.md) · [list](commands/asset/list.md)); TRC10 transfers go through [`tx send`](commands/tx/send.md) |
| [`exchange`](commands/exchange/index.md) | The protocol-level Bancor exchange between TRX and TRC10 ([create](commands/exchange/create.md) · [inject](commands/exchange/inject.md) · [withdraw](commands/exchange/withdraw.md) · [trade](commands/exchange/trade.md) · [show](commands/exchange/show.md) · [list](commands/exchange/list.md)) |

### Payments and Agent identity

| Command | Description |
|---|---|
| [`x402`](commands/x402/index.md) | Pay x402-protected HTTP endpoints, run a local paywall, and browse the provider catalog |
| [`bai`](commands/bai/index.md) | B.AI credits, usage records, and stablecoin recharges |
| [`8004`](commands/8004/index.md) | Read and manage ERC-8004 Agent identities |

### Local tools and configuration

Offline local commands and configuration.

| Command | Description |
|---|---|
| [`encoding convert`](commands/encoding/convert.md) | Convert / validate addresses and encodings |
| [`address generate`](commands/address/generate.md) | Generate a random keypair (local, not stored) |
| [`config`](commands/config.md) | Show / get / set configuration values |
| [`networks`](commands/networks.md) | List known networks |

## The contract, in one paragraph

Every command supports `-o json` and then prints **exactly one** terminal JSON frame on stdout, schema [`wallet-cli.result.v1`](machine-interface.md#the-result-envelope). Exit codes are fixed: `0` success, `1` execution failure, `2` usage error. Secrets (passwords, mnemonics, private keys) are never accepted via argv or environment variables — only via stdin flags or interactive TTY prompts; mnemonic/private-key import and `change-password` are interactive-only (no stdin path at all). Full spec: [machine-interface.md](machine-interface.md).

## Understanding the chains

TRON differs a lot from EVM chains in fees, accounts, and key permissions — these are worth understanding up front to avoid surprises:

- [Networks](concepts/networks.md) — CAIP-2 ids and aliases, the two chain families, and the two fee models
- [Accounts & HD](concepts/accounts-and-hd.md) — mnemonics, derivation paths, one address per family, account activation
- [Energy & bandwidth](concepts/energy-bandwidth.md) — TRON's resource-based fee model (in place of EVM gas)
- [Security](concepts/security.md) — keystore encryption, secret handling, multi-sig permissions
- [Which commands run on which networks](commands/index.md#which-commands-run-on-which-networks) — portable, TRON-only, and local commands

## Troubleshooting

A command errored or behaved unexpectedly? Common issues and how to diagnose them are in [troubleshooting.md](troubleshooting.md).

> All copy-pasteable examples in this documentation run against a test network — the **Nile testnet** (`--network nile`) on TRON, **Sepolia** (`--network sepolia`) on EVM. Mainnet commands move real funds; they appear only as annotated, non-copyable descriptions.
>
> Examples pass the short **alias** because it reads better; the output samples beside them show the canonical id (`tron:3448148188`, `eip155:11155111`), because that is what the CLI always reports. Aliases are local config and can be re-pointed, so scripts should pass canonical ids — see [machine interface](machine-interface.md#calling-convention).
