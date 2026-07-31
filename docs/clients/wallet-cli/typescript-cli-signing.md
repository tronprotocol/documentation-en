# TypeScript CLI signing and security

The TypeScript CLI supports software keystores, Ledger accounts, and watch-only accounts. Software
private keys stay encrypted locally, Ledger private keys never leave the device, and watch-only
accounts can query state but cannot sign.

## Sign an existing transaction

`tx sign` signs a TRON transaction constructed outside wallet-cli without broadcasting it:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign --transaction "$TX_JSON" --password-stdin --output json
```

For a software account, signing is offline and `--network` is optional. The command is a pure
signer: it does not decide whether the signer owns the transaction, whether a contract call is
desirable, or how much value should move. The caller remains responsible for policy checks.

### Transaction integrity

A TRON transaction represents its content in three related fields:

| Field | Purpose |
|-------|---------|
| `raw_data` | Human- and application-readable transaction content. |
| `raw_data_hex` | Bytes executed by the node. |
| `txID` | Hash covered by the signature. |

Before signing, wallet-cli requires `txID` to equal the SHA-256 hash of `raw_data_hex`. It also
decodes the outer transaction envelope and requires the contract types declared in `raw_data` to
match those encoded in `raw_data_hex`. For contract types that can be re-encoded, it additionally
requires the field-level contents of `raw_data` to produce the same bytes. A mismatch returns
`tx_integrity` and no signature is produced.

`MarketSellAssetContract`, `MarketCancelOrderContract`, and `ShieldedTransferContract` cannot be
re-encoded by the underlying library. Their transaction hash and contract type are still checked,
but their `raw_data` field values cannot be verified against `raw_data_hex`; callers must treat those
displayed field values as unverified.

### Multi-signature transactions

When the input already contains a `signature` array, `tx sign` appends the new signature rather than
replacing existing signatures. The same partially signed transaction can therefore move from one
authorized signer to the next until its permission threshold is met.

Extract the signed payload and broadcast it later:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign --transaction "$TX_JSON" --password-stdin --output json |
  jq -c '.data.signed' > signed.json

wallet-cli tx broadcast --network tron:nile --tx-stdin < signed.json
```

Text output prints the complete signature rather than an abbreviated transaction identifier.

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
before software and Ledger signing alike.

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

Secrets are never accepted as command-line arguments or environment configuration.

The supported stdin channels are:

| Flag | Input |
|------|-------|
| `--password-stdin` | Master password used to unlock a software keystore. |
| `--tx-stdin` | Signed transaction JSON consumed by `tx broadcast`. |
| `--message-stdin` | Message consumed by `message sign`. |

Only one `*-stdin` flag can consume stdin in a single invocation.

The following high-value setup operations are interactive-only and require hidden input from a real
TTY:

- `import mnemonic`
- `import private-key`
- `change-password`

They do not accept `--mnemonic-stdin`, `--private-key-stdin`, or `--password-stdin`. Without a TTY,
they fail with `tty_required`.

## Failure behavior

- Watch-only accounts return `watch_only_no_signer` before a signing or write operation starts.
- Invalid global values return `invalid_value` rather than falling back to defaults.
- Ledger setting and version problems use `ledger_setting_required` and `ledger_unsupported`.
- A transaction whose representations disagree returns `tx_integrity`.
- User or device refusal returns `signing_rejected`.

JSON mode returns these codes in a single `wallet-cli.result.v1` envelope and uses exit code 1 for
execution failures and exit code 2 for invalid usage.

For complete field-level command references, see
[`tx sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/sign.md) and
[`typed-data sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/typed-data/sign.md).
