# TypeScript / npm CLI

Starting with release 4.9.7, the `wallet-cli` repository also ships a TypeScript CLI. It is
published as `@tron-walletcli/wallet-cli` on npm. Starting with 4.10.1, the npm package version is
aligned with the wallet-cli release line.

The TypeScript CLI is separate from the Java JAR. It uses grouped commands such as `tx send` and
supports TRON mainnet, Nile, and Shasta. EVM chains are not supported.

## Install

Node.js 20 or later is required.

```bash
npm install -g @tron-walletcli/wallet-cli
wallet-cli --version
wallet-cli --help
```

## Quick start

Create a wallet, select it, and use Nile for testing:

```bash
wallet-cli create --label main
wallet-cli list
wallet-cli use main
wallet-cli config defaultNetwork tron:nile
wallet-cli account balance
```

Override the network for one command with `--network`:

```bash
wallet-cli account balance --network tron:nile
```

## Common options

| Option | Description |
|--------|-------------|
| <code>--output text&#124;json</code>, <code>-o</code> | Select text or JSON output. |
| `--network` | Select `tron:mainnet`, `tron:nile`, or `tron:shasta`. |
| `--account` | Select an account by id, label, or address. |
| `--wait` | After submission, poll until a final state or the wait timeout. |
| `--password-stdin` | Read a software-wallet password from stdin. |

Use `wallet-cli config` to view or persist defaults:

```bash
wallet-cli config
wallet-cli config waitTimeoutMs 90000
```

## Wallets and accounts

Wallet data is stored under `~/.wallet-cli` by default. Set `WALLET_CLI_HOME` to use another
location, for example when testing or running automation.

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

Mnemonic and private-key imports and password changes require a real terminal and use hidden
prompts. They do not accept secrets as command-line arguments.

Software accounts must provide the master password through `--password-stdin` for commands that
sign or decrypt a key without an interactive password flow. Backups can use either a hidden terminal
prompt or `--password-stdin`. Ledger accounts do not use `--password-stdin`.

To keep later command listings concise, signing examples may omit the password pipe and
`--password-stdin`. Software accounts must add them; Ledger accounts must not.

For HD sub-account derivation, pass the seed id shown by `wallet-cli list`:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli derive --seed-id wlt_ab12cd34 --label operations --password-stdin
```

Delete an account with `wallet-cli delete`. Deleting a root HD wallet also removes accounts derived
from it. Use `--yes` only when you intentionally want to skip confirmation.

The CLI can activate a new address and set the selected account's on-chain name or id:

```bash
wallet-cli account activate --address TNewAddress... --network tron:nile --dry-run
wallet-cli account set --name "Acme Treasury" --network tron:nile --dry-run
wallet-cli account set --id acme-treasury-01 --network tron:nile --dry-run
```

`account activate` charges the selected account the current account-creation fee. An on-chain
account name and id can each be set only once. This differs from `rename`, which changes only a
reusable local label. `account activate` and `account set --id` cannot be signed by a Ledger account.
Review these operations with `--dry-run` before submitting them.

## Transactions

Amounts passed with `--amount` are human-readable amounts. Use `--raw-amount` for SUN or token base
units.

```bash
wallet-cli tx send --to T... --amount 1 --dry-run
wallet-cli tx send --to T... --token USDT --amount 5 --dry-run
wallet-cli tx send --to T... --contract TR7... --amount 5 --dry-run
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000 --dry-run
```

Transaction-building commands support four modes:

| Mode | Behavior |
|------|----------|
| default | Build, sign, and broadcast. |
| `--dry-run` | Build and estimate without signing or broadcasting. |
| `--sign-only` | Build and sign without broadcasting. |
| `--build-only` | Build without signing or unlocking a wallet. |

Add `--wait` to poll for a confirmed or failed result. If the wait timeout is reached first, the
command returns `submitted`; without `--wait`, it returns immediately after submission.

Broadcast a previously signed artifact from a file:

```bash
wallet-cli tx broadcast --file signed.hex --network tron:nile
wallet-cli tx status --txid <TXID>
wallet-cli tx info --txid <TXID> --output json
```

`tx sign` accepts JSON for the direct signing path and hex or file input for multi-signature
artifacts:

```bash
wallet-cli tx sign --transaction "$TX_JSON"
wallet-cli tx approvals --file transaction.hex --network tron:nile
wallet-cli tx sign --file transaction.hex --out signed.hex --network tron:nile
```

Hex and file signing checks the selected permission and existing approvals online. Use `--offline`
on an air-gapped signer, then check the result later with `tx approvals`. See
[Multi-signature](typescript-cli-multisig.md) and
[Signing and security](typescript-cli-signing.md).

## Permissions and multi-signature

TRON permissions use weighted signer keys and a threshold. Inspect the current permissions and
dry-run any replacement before signing it:

```bash
wallet-cli permission show --account main --network tron:nile
wallet-cli permission update --file permissions.json --network tron:nile --dry-run
wallet-cli tx approvals --file transaction.hex --network tron:nile
```

`permission update` replaces the complete permission structure and charges the chain's current
permission-update fee. An incorrect owner permission can permanently lock the account.

The optional `tx multisig` command uses the TronLink service to coordinate signatures. The service
is not required; signers can exchange transaction files directly. See
[Multi-signature](typescript-cli-multisig.md) for both workflows.

## Queries

Wallet-bound queries use the active account unless `--account` selects another one.

```bash
wallet-cli account info --output json
wallet-cli account history --limit 10
wallet-cli account portfolio
wallet-cli networks
wallet-cli block 12345
wallet-cli chain params
wallet-cli chain prices
wallet-cli chain node
wallet-cli stake info
wallet-cli vote status
wallet-cli reward balance
```

For all supported options and response fields, see the
[upstream command reference](https://github.com/tronprotocol/wallet-cli/tree/master/ts/docs/commands).

## Tokens and contracts

The token address book includes common mainnet tokens and supports custom TRC-20 contracts.

```bash
wallet-cli token add --contract TR7...
wallet-cli token list
wallet-cli token balance --contract TR7...
wallet-cli token info --contract TR7...
wallet-cli token remove --contract TR7...
```

Contract calls use JSON-encoded parameters:

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

Signing or broadcasting a contract deployment requires a software account. Ledger accounts can use
`--dry-run` or `--build-only` because those modes do not sign.

## GasFree transfers

GasFree can transfer supported tokens without requiring the account to hold TRX. The service
charges its fee in the transferred token.

```bash
wallet-cli gasfree info --network tron:nile
wallet-cli gasfree transfer --to T... --amount 25 --token USDT --network tron:nile --dry-run
wallet-cli gasfree trace <TRACE_ID> --network tron:nile
```

GasFree supports mainnet and Nile and requires service credentials. A submitted request returns a
GasFree trace id; follow it with `--wait` or `gasfree trace`. See
[TypeScript CLI GasFree](typescript-cli-gasfree.md).

## Stake 2.0

Stake amounts are specified in SUN.

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

Signing or broadcasting `stake cancel-unfreeze` requires a software account. Ledger accounts can
use `--dry-run` or `--build-only` because those modes do not sign.

## Voting and rewards

```bash
wallet-cli vote list
wallet-cli vote status
wallet-cli vote cast --for TZ4...=600 --for TT5...=400
wallet-cli reward balance
wallet-cli reward withdraw
```

`vote cast` replaces the complete vote allocation, so omitted representatives receive no votes.
Signing or broadcasting `vote cast` or `reward withdraw` requires a software or Ledger account;
`--dry-run` and `--build-only` do not sign.

## Local utilities

```bash
wallet-cli contact add alice T... --note "Alice mainnet"
wallet-cli contact list
wallet-cli tx send --to alice --amount 1 --network tron:nile --dry-run
wallet-cli contact remove alice

wallet-cli address generate --out ./generated-keypair.json
wallet-cli encoding convert T...
wallet-cli current --qr
```

Contacts are stored locally and can be used as recipients for `tx send` and `gasfree transfer`.
`address generate` creates a keypair without importing it into the wallet. Protect the generated
private-key file and use `--print-secret` only in a controlled offline terminal.

## Signing

The CLI supports message, transaction, and EIP-712/TIP-712 typed-data signing. Software and Ledger
accounts can sign; watch-only accounts cannot.

```bash
wallet-cli message sign --message 'hello'
wallet-cli tx sign --transaction "$TX_JSON"
wallet-cli typed-data sign --typed-data "$TYPED_DATA_JSON"
```

See [Signing and security](typescript-cli-signing.md) for password input, Ledger settings, offline
signing, and transaction review.

## Automation

JSON output uses a single `wallet-cli.result.v1` envelope. Exit codes are stable:

| Code | Meaning |
|------|---------|
| `0` | The command completed successfully. |
| `1` | A runtime or execution failure occurred. |
| `2` | A usage, input, or configuration error occurred. |

For commands using `--wait`, inspect `data.stage`: `"confirmed"` and `"failed"` are final outcomes,
while `"submitted"` is not.

Scripts can discover commands and JSON Schemas without parsing human-readable help:

```bash
wallet-cli --json-schema
wallet-cli tx send --json-schema
```
