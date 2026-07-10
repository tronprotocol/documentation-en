# TypeScript / npm CLI

Starting with `wallet-cli` 4.9.7, the repository also ships an agent-first TypeScript CLI published
as the npm package `@tron-walletcli/wallet-cli`. It is separate from the Java JAR described in the
rest of this section: the Java CLI uses commands such as `send-coin`, while the TypeScript CLI uses
grouped commands such as `tx send`.

The TypeScript CLI currently supports TRON mainnet, Nile, and Shasta. EVM chains are not supported
by this version.

## Install

Node.js 20 or later is required.

```bash
npm install -g @tron-walletcli/wallet-cli
wallet-cli --version
wallet-cli --help
```

## Quick start

Create a local HD wallet, select it, and use Nile for test transactions:

```bash
wallet-cli create --label main
wallet-cli list
wallet-cli use main
wallet-cli current
wallet-cli config defaultNetwork tron:nile
wallet-cli account balance
```

You can override the network for one command without changing the default:

```bash
wallet-cli account balance --network tron:nile
```

## Global options

Common global options include:

| Option | Description |
|--------|-------------|
| <code>--output text&#124;json</code>, <code>-o</code> | Select text or JSON output. |
| `--network` | Network id, such as `tron:mainnet`, `tron:nile`, or `tron:shasta`. |
| `--account` | Account id, label, or address; defaults to the active account set by `use`. |
| `--timeout` | Per RPC/device-call timeout in milliseconds. |
| `--verbose`, `-v` | Show extra diagnostics. |
| `--wait` | After broadcast, poll until the transaction is confirmed or failed. |
| `--wait-timeout` | Polling cap for `--wait`, in milliseconds. |
| `--password-stdin` | Read the master password from stdin. |

Command-scoped stdin flags include `--mnemonic-stdin`, `--private-key-stdin`, `--tx-stdin`, and
`--message-stdin`. Only one `*-stdin` flag can consume stdin in a single invocation.

## Wallets and accounts

The TypeScript CLI stores its data under `~/.wallet-cli` by default. Set `WALLET_CLI_HOME` to isolate
test or automation data.

```bash
WALLET_CLI_HOME=/tmp/wallet-cli-demo wallet-cli list --output json
```

Useful wallet commands:

```bash
wallet-cli create --label main
wallet-cli import mnemonic --label imported
wallet-cli import private-key --label hot
wallet-cli import watch --address T... --label treasury
wallet-cli import ledger --app tron --index 0 --label cold
wallet-cli list
wallet-cli use main
wallet-cli current
wallet-cli rename main --label primary
wallet-cli backup primary --out ~/primary-backup.json
```

HD sub-account derivation is explicit in 4.9.7: pass the HD seed id shown by `wallet-cli list`.

```bash
wallet-cli derive --seed-id wlt_ab12cd34 --label operations
```

Deleting a root HD wallet cascades to accounts derived from that root and cleans orphan labels. In a
non-interactive shell, pass `--yes`; otherwise the command asks for confirmation.

```bash
wallet-cli delete old --yes
```

## Transactions

Amounts passed with `--amount` are human amounts. Use `--raw-amount` for SUN or token base units.

```bash
wallet-cli tx send --to T... --amount 1 --dry-run
wallet-cli tx send --to T... --amount 1 --wait
wallet-cli tx send --to T... --token USDT --amount 5
wallet-cli tx send --to T... --contract TR7... --amount 5
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000
```

State-changing commands support three execution modes:

| Mode | Behavior |
|------|----------|
| default | Build, sign, and broadcast. |
| `--dry-run` | Build and estimate without signing or broadcasting. |
| `--sign-only` | Sign and output the transaction without broadcasting. |

Broadcast a signed transaction later with:

```bash
wallet-cli tx broadcast --tx-stdin < signed.json
```

`tx status` returns a four-state model: `confirmed`, `failed`, `pending`, or `not_found`.

```bash
wallet-cli tx status --txid <TXID>
wallet-cli tx info --txid <TXID> --output json
```

## Queries and signing

Wallet-bound account queries use the active account by default, or the account selected with
`--account`.

```bash
wallet-cli account info --output json
wallet-cli account history --limit 10
wallet-cli account portfolio
wallet-cli networks
wallet-cli block
wallet-cli block 12345
wallet-cli message sign --message 'hello'
```

## Tokens and contracts

The token address book includes common mainnet tokens such as USDT and USDC, and can be extended with
custom TRC-20 contracts.

```bash
wallet-cli token add --contract TR7...
wallet-cli token list
wallet-cli token balance --contract TR7...
wallet-cli token info --contract TR7...
wallet-cli token remove --contract TR7...
```

Contract calls use JSON-encoded parameter descriptors:

```bash
wallet-cli contract info --contract TR7...

wallet-cli contract call \
  --contract T... \
  --method 'balanceOf(address)' \
  --params '[{"type":"address","value":"T..."}]'

wallet-cli contract send \
  --contract T... \
  --method 'transfer(address,uint256)' \
  --params '[{"type":"address","value":"T..."},{"type":"uint256","value":"1000000"}]' \
  --dry-run

wallet-cli contract deploy \
  --abi '[...]' \
  --bytecode 60... \
  --fee-limit 1000000000 \
  --params '[100,"T..."]' \
  --dry-run
```

In JSON output, a successful TypeScript CLI contract deployment includes the deployed
`contractAddress` in the deploy receipt data.

Contract deployment requires a software account. The Ledger TRON app cannot sign
`CreateSmartContract`, so Ledger-backed accounts cannot use `wallet-cli contract deploy`.

## Stake 2.0

Stake amounts are specified in SUN. The TypeScript CLI exposes Stake 2.0 commands:

```bash
wallet-cli stake freeze --amount-sun 1000000 --resource energy --dry-run
wallet-cli stake delegate --amount-sun 1000000 --receiver T... --resource energy --dry-run
wallet-cli stake undelegate --amount-sun 1000000 --receiver T... --resource energy --dry-run
wallet-cli stake unfreeze --amount-sun 1000000 --resource energy --dry-run
wallet-cli stake cancel-unfreeze --dry-run
wallet-cli stake withdraw --dry-run
```

`stake cancel-unfreeze` requires a software account; the Ledger TRON app cannot sign
`CancelAllUnfreezeV2Contract`.

## Automation

JSON mode emits one `wallet-cli.result.v1` envelope to stdout and uses deterministic exit codes:

| Code | Meaning |
|------|---------|
| `0` | Success. |
| `1` | Execution, authentication, device, or chain error. |
| `2` | Invalid command usage or arguments. |

Agents and scripts can discover the complete command catalog and JSON Schemas without parsing
human-readable help:

```bash
wallet-cli --json-schema
wallet-cli tx send --json-schema
```

For secret input, pipe secrets through stdin rather than argv or exported environment variables:

```bash
printf '%s\n' "$WALLET_PASSWORD" | wallet-cli message sign --message 'hello' --password-stdin --output json
printf '%s\n' "$MNEMONIC" | wallet-cli import mnemonic --label main --mnemonic-stdin
printf '%s\n' "$PRIVATE_KEY" | wallet-cli import private-key --label hot --private-key-stdin
```

These examples assume the shell variables are populated securely and are not exported. Only one
`*-stdin` flag can consume stdin in each invocation. Commands such as `import mnemonic` and
`import private-key` need both the master password and the mnemonic/private key; if you pipe one
secret, the other must be entered interactively in a TTY. They cannot be completed as a fully
non-interactive single-stdin invocation.
