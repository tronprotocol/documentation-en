# wallet-cli — TypeScript implementation

The agent-first implementation of wallet-cli, built for automation: every command has a stable JSON envelope, deterministic exit codes, and discoverable schemas; interactive prompts are kept to a short allowlist — `create`, the `import` variants, `backup`, `change-password` and `delete` — and everywhere else a missing credential is an error, never a prompt. For what wallet-cli is and how the two implementations compare, see the [repository overview](../index.md); for the original, see the [Java implementation](../java/index.md).

## Key features

- **Agent-first** — stable JSON output, deterministic exit codes, and discoverable schemas, built for scripts, CI, and AI agents (details in [The contract, in one paragraph](#the-contract-in-one-paragraph)).
- **Encrypted local storage** — software keystores are encrypted on disk; secrets enter via stdin/TTY, never argv or dedicated secret environment variables.
- **Software and Ledger signing** — sign in software, or on a Ledger device (the private key never leaves the device).
- **Covers the full TRON feature surface** — HD wallets, TRX and TRC20/TRC10 transfers, staking / resource delegation, voting / rewards, governance proposals and super-representative operation, smart-contract calls, deployment and governance, TRC10 issuance, the on-chain Bancor exchange, multi-sig, GasFree transfers, message signing, and on-chain queries.
- **EVM chains too** — transfers, tokens, contracts, and signing also run on Ethereum and BNB Smart Chain. TRON-protocol-only commands refuse an EVM network with `family_mismatch`; see [which commands run on which networks](commands/index.md#which-commands-run-on-which-networks).

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
- [Understanding TRON mechanics](#understanding-tron-mechanics)
- [Troubleshooting](#troubleshooting)

## Supported chains

Seven built-in networks are supported. Networks use a canonical [CAIP-2](https://chainagnostic.org/CAIPs/caip-2) `namespace:reference` id. The namespace is not the family: `eip155` is CAIP-2's namespace for EVM chains, while the family this CLI branches on is `evm`. An **alias** is a short name you may type instead; it resolves at selection and never appears in output:

| Network id | Alias | What it is | Native coin value |
|---|---|---|---|
| `tron:728126428` | `tron` | Production TRON | **Real funds** |
| `tron:3448148188` | `nile` | Primary TRON testnet (faucet at nileex.io) | None — use freely |
| `tron:2494104990` | `shasta` | Alternate TRON testnet | None |
| `eip155:1` | `ethereum` | Ethereum mainnet (ETH) | **Real funds** |
| `eip155:11155111` | `sepolia` | Ethereum test network (ETH) | None |
| `eip155:56` | `bsc` | BNB Smart Chain (BNB) | **Real funds** |
| `eip155:97` | `bsc-testnet` | BNB Smart Chain test network (BNB) | None |

Within a family your address is the same on every network (base58 `T…` on TRON, `0x…` on EVM — the two families derive **different** addresses from the same seed), while balances, tokens, and transactions stay isolated per network. Fees follow the family: TRON's `tron-resource` model (bandwidth + energy) or EVM gas — see [networks](concepts/networks.md) and [energy & bandwidth](concepts/energy-bandwidth.md).

## Install

**Prerequisites**: [Node.js](https://nodejs.org) **20 or later** (`node --version` to check). Ledger signing additionally needs a supported Ledger device with the app for the selected family installed — TRON for TRON accounts, Ethereum for EVM accounts. See the [Ledger guide](guide/ledger.md).

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
  EVM address   0x5c8e1b04A7f39d62C0B3e85A1d47F9028b6ce713
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

### Local tools and configuration

Offline local commands and configuration.

| Command | Description |
|---|---|
| [`encoding convert`](commands/encoding/convert.md) | Convert / validate addresses and encodings |
| [`address generate`](commands/address/generate.md) | Generate a random keypair (local, not stored) |
| [`config`](commands/config.md) | Show / get / set configuration values |
| [`networks`](commands/networks.md) | List known networks |

## The contract, in one paragraph

Every command supports `-o json` and then prints **exactly one** terminal JSON frame on stdout, schema [`wallet-cli.result.v1`](machine-interface.md#the-result-envelope). Exit codes are fixed: `0` success, `1` execution failure, `2` usage error. Secrets (passwords, mnemonics, private keys) are never accepted via argv and are not read from dedicated secret environment variables. Passwords can enter through stdin flags or interactive TTY prompts; mnemonic/private-key import and `change-password` are interactive-only (no stdin path at all). Full spec: [machine-interface.md](machine-interface.md).

## Understanding TRON mechanics

TRON differs a lot from EVM chains in fees, accounts, and key permissions — these are worth understanding up front to avoid surprises:

- [Networks](concepts/networks.md) — the seven built-in networks, CAIP-2 ids, and the two chain families
- [Accounts & HD](concepts/accounts-and-hd.md) — mnemonics, derivation paths, account activation
- [Energy & bandwidth](concepts/energy-bandwidth.md) — TRON's resource-based fee model (in place of EVM gas)
- [Security](concepts/security.md) — keystore encryption, secret handling, multi-sig permissions

## Troubleshooting

A command errored or behaved unexpectedly? Common issues and how to diagnose them are in [troubleshooting.md](troubleshooting.md).

> Copy-pasteable examples that spend anything target a testnet — **Nile** (`--network tron:3448148188`) on TRON, **Sepolia** (`--network eip155:11155111`) on EVM. Mainnet ids (`tron:728126428`, `eip155:1`) also appear: in read-only examples such as token-book listings and config paths, and in a few illustrations of mainnet token contracts. Those last ones carry placeholder recipients (`T...` / `0x...`) and are not runnable as written.
