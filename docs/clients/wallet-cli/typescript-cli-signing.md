# TypeScript CLI signing and security

The TypeScript CLI supports software, Ledger, and watch-only accounts. Software keys remain
encrypted locally, Ledger keys stay on the device, and watch-only accounts cannot sign.

## Sign a transaction

`tx sign` accepts two forms of input:

| Input | Use |
|-------|-----|
| `--transaction <json>` | Sign a JSON transaction directly. |
| `--hex <hex>` / `--file <path>` | Add a signature to a transaction artifact. |

The command signs but never broadcasts. Use `tx broadcast` afterward.

For a software account, provide the password through stdin:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign \
    --transaction "$TX_JSON" \
    --password-stdin
```

For a multi-signature artifact, existing signatures are preserved and the selected account adds one
signature:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx sign \
    --file transaction.hex \
    --account cosigner \
    --network tron:nile \
    --out transaction.signed.hex \
    --password-stdin
```

By default, artifact signing checks the selected permission and existing approvals online. It
refuses an expired transaction, an unauthorized signer, or a duplicate signature. Use `--offline`
on an air-gapped machine, then inspect the artifact later with `tx approvals`.

For the complete co-signing workflow, see
[TypeScript CLI multi-signature](typescript-cli-multisig.md).

## Review before signing

wallet-cli validates the transaction representation before signing. Hex and file artifacts are
refused when they cannot be safely decoded and verified.

Always confirm the sender, recipient, amount, token or contract, permission, and expiration before
signing. For offline signing, transfer the artifact through a trusted channel and do not modify its
transaction content between signers.

## Sign typed data

`typed-data sign` signs EIP-712/TIP-712 structured data:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli typed-data sign \
    --typed-data "$TYPED_DATA_JSON" \
    --password-stdin \
    --output json
```

The payload uses `domain`, `types`, `primaryType`, and `message`. TRON Base58 addresses are
accepted in address fields. The value of `domain.chainId` is signed as supplied and is not checked
against `--network`, so review both the domain and message carefully.

## Ledger accounts

Ledger accounts support transaction and typed-data signing. Do not pipe a password or pass
`--password-stdin` when using one.

For typed data, enable **Settings > Sign by Hash > Allowed** in the Ledger TRON app. The device may
show hashes instead of every typed-data field, so verify the complete payload on the host before
approving it.

Other operations may require the corresponding transaction or custom-contract signing setting in
the TRON app. If the app or device cannot sign an operation, wallet-cli returns an actionable Ledger
error.

## Password and secret input

Master passwords, mnemonics, and private keys are never accepted as command-line arguments or
configuration values.

Signing with a software account requires `--password-stdin`. Commands without an explicit
interactive password flow do not prompt when the password flag is missing.

Only one stdin flag can be used in an invocation:

| Flag | Input |
|------|-------|
| `--password-stdin` | Software-wallet master password. |
| `--tx-stdin` | Transaction JSON for `tx broadcast`. |
| `--message-stdin` | Message for `message sign`. |

`import mnemonic`, `import private-key`, and `change-password` require hidden input from a real
terminal.

## Protect local data

- Wallet files, backups, and generated keypairs contain secrets. Store them securely and do not
  share them.
- Service secrets in `config.yaml` are masked when displayed. Keep the configuration file private.
- Signed transaction files do not contain private keys, but their contents should still be reviewed
  before sharing or broadcasting.
- Use `--print-secret` only in a controlled offline terminal.

For all options and response fields, see the upstream references for
[`tx sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/sign.md),
[`tx approvals`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/approvals.md),
and
[`typed-data sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/typed-data/sign.md).
