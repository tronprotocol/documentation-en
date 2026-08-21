# TypeScript CLI multi-signature

The TypeScript CLI can inspect and replace account permissions, build a transaction for a selected
permission, collect weighted signatures, and broadcast after the threshold is reached.

Signers can exchange a transaction file directly or use the optional TronLink multi-signature
service.

## Permissions and fees

A TRON account can have:

- one owner permission, id `0`;
- an optional witness permission, id `1`; and
- up to eight active permissions, ids `2`–`9`.

Each permission can contain up to five keys. Every key has a weight, and the combined weight of the
signatures must reach the permission threshold.

Two chain fees are especially relevant:

- replacing the account's permission structure currently costs **100 TRX on mainnet**; and
- broadcasting a transaction with more than one signature currently adds **1 TRX on mainnet**.

These are chain parameters and can change. wallet-cli reads the current values at runtime.

## Inspect and update permissions

Inspect an account before creating or signing a transaction:

```bash
wallet-cli permission show --account main --network tron:nile
wallet-cli permission show --account main --network tron:nile --output json
```

`permission update` replaces the complete permission structure. Export the current structure,
edit only the intended fields, and dry-run the replacement:

```bash
wallet-cli permission show --account main --network tron:nile --output json |
  jq '.data' > permissions.json

$EDITOR permissions.json

wallet-cli permission update \
  --file permissions.json \
  --account main \
  --network tron:nile \
  --dry-run
```

Preserve fields you do not intend to change and review the complete dry-run result. When changing
allowed operations, follow the upstream [`permission` reference](https://github.com/tronprotocol/wallet-cli/tree/master/ts/docs/commands/permission),
because the related fields must remain consistent. If `permission show` reports unknown operations,
leave that active permission unchanged unless you can preserve its bitmap. After checking the keys,
weights, threshold, allowed operations, and fee, submit the update:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli permission update \
    --file permissions.json \
    --account main \
    --network tron:nile \
    --wait \
    --password-stdin
```

!!! danger
    A permission update can permanently lock an account, and there is no on-chain recovery. Confirm
    that the new owner permission contains the intended keys and that available signers can reach
    its threshold.

## Exchange a transaction file

The direct workflow does not require an external collaboration service.

### 1. Create the first artifact

Select the permission, allow enough time for co-signers, and create the first signature:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx send \
    --to TRecipient... \
    --amount 1000 \
    --permission-id 2 \
    --sign-only \
    --expiration 86400000 \
    --network tron:nile \
    --password-stdin \
    --output text > transaction.hex
```

The default transaction expiration is approximately 60 seconds. For manual collection, set an
expiration long enough for every signer, up to 24 hours. Use `--build-only` instead of
`--sign-only` when the first signer is on another machine.

### 2. Inspect approvals

```bash
wallet-cli tx approvals --file transaction.hex --network tron:nile
```

This shows the permission, approved signers, accumulated and missing weight, and expiration. An
expired transaction can be inspected but not signed or broadcast.

### 3. Add signatures

Each signer uses the latest file produced by the previous signer:

```bash
printf '%s\n' "$COSIGNER_PASSWORD" |
  wallet-cli tx sign \
    --file transaction.hex \
    --account cosigner \
    --network tron:nile \
    --out transaction.signed.hex \
    --password-stdin
```

Online signing checks permission membership and rejects duplicate signatures. On an air-gapped
machine, add `--offline` and check the artifact later with `tx approvals`.

### 4. Validate and broadcast

When `thresholdReached` is true, validate and broadcast the final artifact:

```bash
wallet-cli tx broadcast --file transaction.signed.hex --network tron:nile --dry-run
wallet-cli tx broadcast --file transaction.signed.hex --network tron:nile --wait
```

wallet-cli refuses an expired transaction or one whose signature weight is below the threshold.

## Use the TronLink service

`tx multisig` can store the transaction, coordinate signatures, and notify co-signers. Configure
credentials that match the selected mainnet or testnet environment:

```bash
wallet-cli config tronlinkSecretId '<secret-id>'
wallet-cli config tronlinkSecretKey '<secret-key>'
wallet-cli config tronlinkChannel '<channel>'
```

Build an unsigned artifact and create a collection:

```bash
wallet-cli tx send \
  --to TRecipient... \
  --amount 1000 \
  --permission-id 2 \
  --build-only \
  --expiration 86400000 \
  --network tron:nile \
  --output text > transaction.unsigned.hex

printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli tx multisig \
    --create \
    --file transaction.unsigned.hex \
    --network tron:nile \
    --password-stdin
```

Creating a collection adds the initiator's first signature. Other signers can list requests and sign
by transaction id:

```bash
wallet-cli tx multisig --account cosigner --network tron:nile

printf '%s\n' "$COSIGNER_PASSWORD" |
  wallet-cli tx multisig \
    --sign <TX_ID> \
    --account cosigner \
    --network tron:nile \
    --password-stdin
```

Use `tx multisig --watch` to receive notifications. The service broadcasts automatically when the
threshold is reached. Confirm the transaction on-chain before attempting a manual broadcast.

## Safety checklist

- Inspect current permissions before selecting or changing one.
- Dry-run and review the complete permission replacement.
- Pass only the latest artifact to the next signer; changing the transaction invalidates earlier
  signatures.
- Choose an expiration long enough for collection but no longer than necessary.
- Check `thresholdReached`, not the number of signatures, because weights can differ.
- Confirm the recipient, amount, permission, and fee before signing or broadcasting on mainnet.

For all options and response fields, see the upstream references for
[`permission`](https://github.com/tronprotocol/wallet-cli/tree/master/ts/docs/commands/permission),
[`tx sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/sign.md),
[`tx approvals`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/approvals.md),
[`tx multisig`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/multisig.md),
and
[`tx broadcast`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/broadcast.md).
