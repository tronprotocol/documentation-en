# TypeScript / npm CLI

Starting with release 4.9.7 of the `wallet-cli` repository, the repository also ships an agent-first
TypeScript CLI. This CLI is published as the npm package `@tron-walletcli/wallet-cli` and uses an
independent npm version number; `wallet-cli --version` reports the npm package version. It is
separate from the Java JAR described in the rest of this section: the Java CLI uses commands such
as `send-coin`, while the TypeScript CLI uses grouped commands such as `tx send`.

The TypeScript CLI currently supports TRON mainnet, Nile, and Shasta. EVM chains are not supported.

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
| `--wait-timeout` | Polling cap for `--wait`, in milliseconds; defaults to `config.waitTimeoutMs` (built-in: 60000). |
| `--password-stdin` | Read the master password from stdin. |

Command-scoped stdin flags are `--tx-stdin` and `--message-stdin`. Together with the global
`--password-stdin`, only one `*-stdin` flag can consume stdin in a single invocation.

Use `wallet-cli config` to persist defaults. For example:

```bash
wallet-cli config waitTimeoutMs 90000
```

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
wallet-cli change-password
```

`import mnemonic`, `import private-key`, and `change-password` are interactive-only. They require a
real terminal and read secrets through hidden prompts; there is no non-interactive stdin alternative.

For non-interactive use with commands such as `derive`, `backup`, and `tx sign`, provide the master
password through `--password-stdin`. When signing with a Ledger account, do not pipe a password or
pass `--password-stdin`. The `derive` example below shows the complete non-interactive form. To keep
later examples concise, they may omit the password pipe and `--password-stdin`.

For HD sub-account derivation, pass the HD seed id shown by `wallet-cli list`.

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli derive --seed-id wlt_ab12cd34 --label operations --password-stdin
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

Transaction-building commands support three execution modes:

| Mode | Behavior |
|------|----------|
| default | Build, sign, and broadcast. |
| `--dry-run` | Build and estimate without signing or broadcasting. |
| `--sign-only` | Sign and output the transaction without broadcasting. |

The default mode returns after the transaction is submitted. Add `--wait` to poll the FullNode's
unconfirmed view until the transaction is confirmed or failed. If the polling cap is reached, the
CLI returns the submitted receipt rather than pretending that the broadcast failed.

Broadcast a signed transaction later with:

```bash
wallet-cli tx broadcast --tx-stdin < signed.json
```

`tx status` returns a four-state model: `confirmed`, `failed`, `pending`, or `not_found`.

```bash
wallet-cli tx status --txid <TXID>
wallet-cli tx info --txid <TXID> --output json
```

The CLI also provides a pure, offline-capable signer for transactions constructed elsewhere:

```bash
wallet-cli tx sign --transaction "$TX_JSON"
```

It always verifies that `txID` is the hash of `raw_data_hex` and that the declared contract types
match the encoded transaction. For contract types that can be re-encoded, it also verifies the
field-level contents of `raw_data`. It appends to an existing signature array for multi-signature
workflows. See [Signing and security](typescript-cli-signing.md#sign-an-existing-transaction).

## Queries

Wallet-bound queries use the active account by default, or the account selected with `--account`.

```bash
wallet-cli account info --output json
wallet-cli account history --limit 10
wallet-cli account portfolio
wallet-cli networks
wallet-cli block
wallet-cli block 12345
wallet-cli chain params
wallet-cli chain prices
wallet-cli chain node
wallet-cli stake info
wallet-cli stake delegated --direction out
wallet-cli vote status
wallet-cli reward balance
```

For field-level command semantics and additional examples, see the
[upstream TypeScript command reference](https://github.com/tronprotocol/wallet-cli/tree/master/ts/docs/commands).

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

`contract info` returns a not-found error when the address has no deployed contract instead of
returning an empty contract.

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
wallet-cli stake info
wallet-cli stake delegated --direction out
```

`stake cancel-unfreeze` requires a software account; the Ledger TRON app cannot sign
`CancelAllUnfreezeV2Contract`.

`stake withdraw` checks the withdrawable amount before building a transaction and returns
`nothing_to_withdraw` when no expired unfreeze is available.

## Voting and rewards

The TypeScript CLI can inspect super representatives, replace the account's vote allocation, query
claimable rewards, and withdraw those rewards:

```bash
wallet-cli vote list
wallet-cli vote status
wallet-cli vote cast --for TZ4...=600 --for TT5...=400
wallet-cli reward balance
wallet-cli reward withdraw
```

`vote cast` replaces the complete existing vote allocation; omitted SRs receive zero votes. Both
`vote cast` and `reward withdraw` create transactions and require a signing account.
`reward withdraw` returns `no_reward` when the claimable balance is empty and
`withdraw_too_frequent` when the 24-hour withdrawal interval has not elapsed.

## Signing

In addition to `message sign`, the CLI provides `tx sign` and EIP-712/TIP-712 `typed-data sign`.
Software and Ledger accounts are supported; watch-only accounts fail before a write or signing
operation begins.

```bash
wallet-cli message sign --message 'hello'
wallet-cli tx sign --transaction "$TX_JSON"
wallet-cli typed-data sign --typed-data "$TYPED_DATA_JSON"
```

See [Signing and security](typescript-cli-signing.md) for transaction-integrity checks,
multi-signature behavior, Ledger settings, and secret-input rules.

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

Canonical command ids do not carry a `tron.` prefix: for example, the id is `tx.send`, not
`tron.tx.send`. The network family remains available separately in `chain.family`.

Invalid global values such as `--timeout 0` or an unsupported `--output` value fail with
`invalid_value` instead of silently falling back to a default.
