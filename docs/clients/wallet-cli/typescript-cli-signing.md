# TypeScript CLI signing and security

The TypeScript CLI supports software keystores, Ledger accounts, and watch-only accounts. Software
private keys stay encrypted locally, Ledger private keys never leave the device, and watch-only
accounts can query state but cannot sign.

## Transaction signing modes

`tx sign` accepts two transaction representations with different purposes:

| Input | Purpose | Network behavior |
|-------|---------|------------------|
| `--transaction <json>` | Compatibility path for signing one unsigned JSON transaction | Offline for a software account; `--network` is optional |
| `--hex <hex>` / `--file <path>` | Append one signature to an unsigned or partially signed artifact | Checks permission membership and approval weight online by default; `--offline` disables those checks |

The command never broadcasts. Use `tx broadcast` after signing.

### Sign unsigned JSON

The JSON compatibility path signs a transaction built elsewhere and returns the same `data.signed`
shape as a transaction-building command in `--sign-only` mode:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign \
    --transaction "$TX_JSON" \
    --password-stdin \
    --output json
```

This is a direct single-signature path. The caller remains responsible for deciding who should sign
and whether the operation is desirable; wallet-cli verifies payload integrity before using the key.

### Append a signature to a hex artifact

For multi-signature transactions, use `--hex` or `--file`. Existing signatures are preserved and
exactly one signature from the selected account is appended:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign \
    --file transaction.hex \
    --account cosigner \
    --network tron:nile \
    --out transaction.signed.hex \
    --password-stdin
```

Before decrypting a software key, the default online mode asks the node for the transaction's
permission group and refuses when:

- the selected account is not a key in the group (`not_authorized`);
- that account has already signed (`already_signed`);
- the transaction has expired (`tx_expired`).

The result reports the signer's weight, accumulated weight, missing weight, whether the threshold
has been reached, and the new transaction hex. `tx sign` has no `--permission-id`: the permission id
is already part of the transaction body and cannot change between signers.

Use `--offline` with `--hex` or `--file` on an air-gapped signing machine. It skips permission and
approval lookups but retains local decoding and integrity checks. The receipt then reports a
signature count rather than authoritative weight; inspect the artifact later with `tx approvals`.
`--out` writes the resulting artifact atomically with mode `0644`. A signed transaction is not a
secret, although its contents should still be reviewed before distribution.

For the end-to-end permission, co-signing, and broadcast sequence, see
[TypeScript CLI multi-signature](typescript-cli-multisig.md).

## Transaction integrity

A TRON transaction represents its content in three related fields:

| Field | Purpose |
|-------|---------|
| `raw_data` | Human- and application-readable transaction content |
| `raw_data_hex` | Bytes executed by the node |
| `txID` | SHA-256 hash covered by every signature |

Before signing, wallet-cli requires `txID` to equal the SHA-256 hash of `raw_data_hex`. It decodes
the outer transaction envelope and requires the contract types declared in `raw_data` to match the
encoded bytes. For contract types that can be re-encoded, it also requires the field-level content
of `raw_data` to produce the same bytes. A mismatch returns `tx_integrity` and no signature is
produced.

Six contract types cannot be re-encoded by TronWeb for the field-level integrity comparison:

- `VoteAssetContract`
- `UnfreezeAssetContract`
- `CustomContract`
- `ShieldedTransferContract`
- `MarketSellAssetContract`
- `MarketCancelOrderContract`

Hex/file input containing any of these contracts is rejected with `invalid_transaction`, because
the artifact cannot be displayed and verified completely. `VoteAssetContract` and `CustomContract`
are rejected as unsupported contract type ids; the other four are rejected because they cannot be
decoded losslessly. The JSON compatibility path can sign all six after checking the transaction
hash and contract type, but their displayed `raw_data` field values cannot be independently verified
against `raw_data_hex`.

## Sign typed data

`typed-data sign` signs EIP-712/TIP-712 structured data and returns the signer address, inferred or
declared primary type, digest, and signature:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli typed-data sign \
    --typed-data "$TYPED_DATA_JSON" \
    --password-stdin \
    --output json
```

The payload follows the usual `domain`, `types`, `primaryType`, and `message` structure. The CLI:

- ignores `EIP712Domain` when it appears inside `types`;
- accepts `value` as an alias for `message`;
- accepts TRON Base58 addresses in `address` fields;
- infers `primaryType` when omitted and reports the resolved type;
- rejects a declared `primaryType` that is not the root message type.

`domain.chainId` is signed exactly as supplied and is not compared with `--network`. Review the
domain and message before signing.

## Ledger behavior

Both `tx sign` and `typed-data sign` support Ledger accounts. Transaction-integrity checks run
before software and Ledger signing alike. Do not pass `--password-stdin` for a Ledger account.

Typed-data signing uses the TRON application's hash-signing capability. Enable
**Settings > Sign by Hash > Allowed** on the device. Otherwise the CLI returns
`ledger_setting_required`. A TRON application version that does not support the instruction returns
`ledger_unsupported`.

Other Ledger application settings, such as transaction data or custom-contract signing, are also
reported as actionable `ledger_setting_required` errors instead of an opaque APDU error. A device
timeout or cancellation closes the transport so a later attempt can reconnect cleanly.

The Ledger screen cannot render every typed-data field and may show only hashes. Verify the payload
on the host before approving it on the device.

## Secret input policy

Wallet secrets — master passwords, mnemonics, and private keys — are never accepted as command-line
arguments or environment configuration. Supported stdin channels are:

Signing with a software account requires the master password through `--password-stdin`. Commands
without an explicit interactive password flow never prompt for a missing password, even when run
from a terminal.

| Flag | Input |
|------|-------|
| `--password-stdin` | Master password used to unlock a software keystore |
| `--tx-stdin` | Signed transaction JSON consumed by `tx broadcast` |
| `--message-stdin` | Message consumed by `message sign` |

Only one `*-stdin` flag can consume stdin in a single invocation. Transaction JSON and hex are not
secrets; they remain command/file inputs so stdin stays available for a password.

The following high-value setup operations are interactive-only and require hidden input from a real
TTY:

- `import mnemonic`
- `import private-key`
- `change-password`

They do not accept `--mnemonic-stdin`, `--private-key-stdin`, or `--password-stdin`. Without a TTY,
they fail with `tty_required`.

## Local files and terminal output

- Software keystores and backups contain secrets. Backups and generated keypairs are written with
  mode `0600`, and an existing output file is never overwritten.
- The contact book is plaintext but restricted to mode `0600`; a symlink or group/world-readable
  file is rejected.
- `config.yaml` is rejected with `insecure_config` when it contains a non-empty
  `gasfreeApiSecret` or `tronlinkSecretKey` and is a symlink or group/world-readable. Those two
  secret fields are masked when displayed; the corresponding API key, secret id, and channel are
  not masked.
- In text mode, control bytes are removed and invisible Unicode formatting characters from chain or
  provider data are rendered visibly, for example `<U+202E>`. JSON is not rewritten; machine
  consumers must neutralize untrusted text before displaying it.
- Files produced by `tx sign --out` contain transaction artifacts rather than private keys and use
  mode `0644`.

## Failure behavior

- Watch-only accounts return `watch_only_no_signer` before a signing operation starts.
- Invalid global values return `invalid_value` rather than falling back to defaults.
- Ledger setting and version problems use `ledger_setting_required` and `ledger_unsupported`.
- A transaction whose representations disagree returns `tx_integrity`.
- An unauthorized, duplicate, or late multi-signature attempt returns `not_authorized`,
  `already_signed`, or `tx_expired`.
- User or device refusal returns `signing_rejected`.

JSON mode returns these codes in a single `wallet-cli.result.v1` envelope and uses exit code 1 for
execution failures and exit code 2 for invalid usage.

For complete field-level command references, see
[`tx sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/sign.md),
[`tx approvals`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/approvals.md),
and [`typed-data sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/typed-data/sign.md).
