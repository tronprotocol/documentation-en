# TypeScript / npm CLI

Starting with release 4.9.7 of the `wallet-cli` repository, the repository also ships an agent-first
TypeScript CLI. This CLI is published as the npm package `@tron-walletcli/wallet-cli`. Starting with
4.10.1, its npm package version is aligned with the wallet-cli release line; `wallet-cli --version`
reports that package version. It remains a separate implementation from the Java JAR: the Java CLI
uses commands such as `send-coin`, while the TypeScript CLI uses grouped commands such as `tx send`.

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

GasFree and TronLink multi-signature collaboration use optional external-service configuration:

| Key | Purpose |
|-----|---------|
| `gasfreeApiKey` / `gasfreeApiSecret` | Authenticate `gasfree info`, `transfer`, and `trace`. |
| `tronlinkSecretId` / `tronlinkSecretKey` / `tronlinkChannel` | Authenticate `tx multisig`. |

These credentials are environment-specific: use credentials that match the mainnet or testnet
selected by `--network`. The secret fields `gasfreeApiSecret` and `tronlinkSecretKey` are masked
when displayed. When either secret field is present, `config.yaml` must not be a symbolic link and
must have no group or world permissions on POSIX; otherwise the CLI returns `insecure_config`. An
unreadable or invalid configuration returns `invalid_config`.

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
wallet-cli current --qr
wallet-cli rename main --label primary
wallet-cli backup primary --out ~/primary-backup.json
wallet-cli change-password
```

`import mnemonic`, `import private-key`, and `change-password` are interactive-only. They require a
real terminal and read secrets through hidden prompts; there is no non-interactive stdin alternative.

For a software account, an invocation that must decrypt a key and has no explicit interactive
password flow—such as `derive` or a signing mode of `tx sign` or `tx send`—must receive the master
password through `--password-stdin`; it never prompts when the flag is missing. `backup` is
different: it can read the password from a hidden TTY prompt, while `--password-stdin` remains
available for non-interactive backups. When signing with a Ledger account, do not pipe a password or
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

The CLI can also activate a new on-chain address and set the selected account's on-chain name or
account id:

```bash
wallet-cli account activate --address TNewAddress... --network tron:nile --dry-run
wallet-cli account set --name "Acme Treasury" --network tron:nile --dry-run
wallet-cli account set --id acme-treasury-01 --network tron:nile --dry-run
```

`account activate` makes the selected account pay the account-creation fee. An account's on-chain
name and id can each be set only once and cannot be changed afterward; `account set` has no
confirmation prompt. This is different from `rename`, which only changes a reusable local wallet
label. Signing or broadcasting `account activate` or `account set --id` requires a software account,
because the Ledger TRON app cannot decode `AccountCreateContract` or `SetAccountIdContract`.
Ledger accounts can sign `account set --name`, and can use `--dry-run` or `--build-only` for all
three operations because those modes do not sign. Review these operations with `--dry-run` before
submitting them.

## Transactions

Amounts passed with `--amount` are human amounts. Use `--raw-amount` for SUN or token base units.

```bash
wallet-cli tx send --to T... --amount 1 --dry-run
wallet-cli tx send --to T... --amount 1 --wait
wallet-cli tx send --to T... --token USDT --amount 5
wallet-cli tx send --to T... --contract TR7... --amount 5
wallet-cli tx send --to T... --asset-id 1002000 --raw-amount 1000000
```

Transaction-building commands support four execution modes:

| Mode | Behavior |
|------|----------|
| default | Build, sign, and broadcast. |
| `--dry-run` | Build and estimate without signing or broadcasting. |
| `--sign-only` | Build and sign, then output signed transaction hex without broadcasting. |
| `--build-only` | Build and output unsigned transaction hex without unlocking a wallet. |

These commands also accept `--permission-id <n>` to select the transaction's owner, witness, or
active permission. `--sign-only` and `--build-only` accept `--expiration <ms>` up to 24 hours, which
gives co-signers time to approve the same artifact. The default node expiration is approximately
60 seconds and is usually too short for a multi-party workflow.

The default mode returns after the transaction is submitted. Add `--wait` to poll the FullNode's
unconfirmed view until the transaction is confirmed or failed. If the polling cap is reached, the
CLI returns the submitted receipt rather than pretending that the broadcast failed.

Broadcast signed hex later, preferably from a file:

```bash
wallet-cli tx broadcast --file signed.hex --network tron:nile
```

`tx broadcast` also accepts inline `--hex`, or the compatibility JSON inputs `--transaction` and
`--tx-stdin`. It rejects an expired transaction locally (`tx_expired`), then queries the node's
read-only permission endpoints and rejects insufficient signature weight (`not_authorized`) before
calling the broadcast endpoint. Use `tx broadcast --dry-run` to perform those checks and calculate
the dynamic multi-signature fee without broadcasting. The fee is a chain parameter read at runtime
and applies when the transaction contains more than one signature; it is currently 1 TRX on
mainnet.

`tx status` returns a four-state model: `confirmed`, `failed`, `pending`, or `not_found`.

```bash
wallet-cli tx status --txid <TXID>
wallet-cli tx info --txid <TXID> --output json
```

The CLI supports two signing inputs. `--transaction` retains the direct single-signature JSON path;
`--hex` and `--file` append a signature to a multi-signature artifact:

```bash
wallet-cli tx sign --transaction "$TX_JSON"
wallet-cli tx approvals --file transaction.hex --network tron:nile
wallet-cli tx sign --file transaction.hex --out signed.hex --network tron:nile
```

Before decrypting a software key, the default online mode checks the selected account's permission
membership and rejects duplicate approvals. After appending the signature, it reports the updated
accumulated and missing weight. Add `--offline` to skip the node-backed permission check while
preserving local payload-integrity checks. See
[Multi-signature](typescript-cli-multisig.md) for the complete workflow and
[Signing and security](typescript-cli-signing.md) for integrity and device behavior.

## Permissions and multi-signature

TRON permissions contain weighted signer keys and a threshold. Permission id `0` is the owner,
`1` is the optional witness permission, and ids `2`–`9` are scoped active permissions.

```bash
wallet-cli permission show --account main --network tron:nile
wallet-cli permission show --account main --network tron:nile --output json
wallet-cli permission update --file permissions.json --network tron:nile --dry-run
wallet-cli tx approvals --file transaction.hex --network tron:nile
```

`permission update` replaces the entire permission structure and burns a chain-set fee that the CLI
reads at runtime; it is currently 100 TRX on mainnet. A bad owner group can permanently lock the
account; the CLI emits `owner_lockout` or `owner_lockout_partial` warnings but does not block a
deliberately multi-party configuration. The optional `tx multisig` command uses the TronLink service
to hold an artifact, collect signatures, notify co-signers, and broadcast after the threshold is
reached. The service is not required: artifacts can instead be passed directly between signers. See
[Multi-signature](typescript-cli-multisig.md).

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

Block responses are parsed losslessly. Protobuf `int64`/`uint64` values outside JavaScript's safe
integer range are returned as exact decimal strings rather than rounded numbers.

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

`contract send --dry-run` compares the supplied `--fee-limit` with the estimated energy cost and
warns when the limit is likely to make the transaction fail.

## GasFree transfers

The TypeScript CLI can transfer provider-supported tokens without holding TRX. The GasFree service
deducts its fee in the transferred token and returns a provider `traceId` while the transfer is
being relayed:

```bash
wallet-cli gasfree info --network tron:nile
wallet-cli gasfree transfer --to T... --amount 25 --token USDT --network tron:nile --dry-run
wallet-cli gasfree trace <TRACE_ID> --network tron:nile
```

GasFree supports mainnet and Nile, not Shasta, and requires `gasfreeApiKey` and
`gasfreeApiSecret`. A submitted GasFree transfer is not yet an on-chain transaction: follow its
provider states with `--wait` or `gasfree trace`, not `tx status`. See
[TypeScript CLI GasFree](typescript-cli-gasfree.md).

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

`stake freeze` and `stake unfreeze` also preflight the available balance or currently staked amount,
including in `--dry-run`, and return `insufficient_balance` or `insufficient_stake` for a request the
node would inevitably reject.

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

## Local utilities

The 4.11.0 command surface includes recipient contacts, offline key generation, address and byte
encoding conversion, and a receive QR:

```bash
wallet-cli contact add alice T... --note "Alice mainnet"
wallet-cli contact list
wallet-cli tx send --to alice --amount 1 --network tron:nile --dry-run
wallet-cli contact remove alice

wallet-cli address generate --out ./generated-keypair.json
wallet-cli encoding convert T...
wallet-cli current --qr
```

The contact book is a local plaintext file restricted to mode `0600`; contact names can be used by
`tx send --to` and `gasfree transfer --to`. `address generate` creates a keypair locally but does
not add it to the wallet. By default it writes the private key to an exclusively created `0600`
file; `--print-secret` deliberately prints it to stdout and should be used only in a controlled
offline terminal. `encoding convert` accepts public/address/byte encodings but rejects 32-byte
private-key-shaped input so secrets are not placed in shell history.

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

For broadcast commands, exit status describes whether the CLI completed the request, not the
on-chain result. With `--wait`, a mined transaction that reverted is still a successful command:
the envelope has `success: true` and exits `0`, while `data.stage` is `"failed"`. Scripts must
branch on `data.stage` after waiting and must not treat `stage: "submitted"` as confirmation.

`meta.warnings` can contain either a string or an object with stable `code` and human-readable
`message` fields. Permission lockout and post-confirmation warnings use the object form. Normalize
both shapes before displaying warnings and branch only on object `code`, never message text.

On-chain amounts and integers that may exceed JavaScript's safe range are serialized as decimal
strings. Chain- or provider-controlled text is left unchanged in JSON, so consumers must neutralize
control and invisible formatting characters before displaying it. Text mode performs that
neutralization automatically.

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

A node broadcast is considered accepted only when the node explicitly returns `result: true`.
Rejections are surfaced as `transaction_rejected` rather than as a successful receipt containing a
transaction id that never reached the node.
