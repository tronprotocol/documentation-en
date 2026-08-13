# TypeScript CLI multi-signature

The TypeScript CLI supports the full TRON multi-signature lifecycle: inspect or replace account
permissions, build a transaction for a selected permission, collect weighted signatures, verify the
threshold, and broadcast. Signatures can be exchanged directly as a hex artifact or collected by
the optional TronLink multi-signature service.

## Permission model and fees

Every TRON account has:

- one owner permission, id `0`, with full control;
- an optional witness permission, id `1`, for Super Representatives;
- up to eight active permissions, ids `2`–`9`, scoped to selected contract operations.

A permission contains up to five keys. Each key has a weight, and signatures authorize a
transaction when their combined weight reaches the permission's threshold.

Two chain-set fees are especially important. wallet-cli reads their current values at runtime:

- replacing an account's permission structure burns the permission-update fee, currently **100
  TRX on mainnet**;
- broadcasting a transaction with more than one signature incurs the additional multi-signature
  fee, currently **1 TRX on mainnet**.

## Inspect and update permissions

Inspect an account before creating or signing a transaction:

```bash
wallet-cli permission show --account main --network tron:nile
wallet-cli permission show --account main --network tron:nile --output json
```

`permission show` lists owner, witness, and active groups; thresholds; weighted keys; decoded active
operations; and which keys are held by the local wallet. A bare address is also accepted, so the
account does not need to be imported locally for this read-only query.

`permission update` replaces the entire structure. Export the current data, edit it, and dry-run the
replacement before signing:

```bash
wallet-cli permission show --account main --network tron:nile --output json |
  jq '.data' > permissions.json

# Edit keys, weights, thresholds, names, and operations.
$EDITOR permissions.json

wallet-cli permission update \
  --file permissions.json \
  --account main \
  --network tron:nile \
  --dry-run
```

Each active permission contains decoded `operations`, its raw `operationsHex`, and
`unknownOperationIds` for bitmap bits that this wallet-cli version cannot name. If
`unknownOperationIds` is empty, edit `operations` and remove that group's old `operationsHex`;
wallet-cli will regenerate the bitmap. If `unknownOperationIds` is non-empty, `operations` alone
cannot preserve those bits. To keep them, retain `unknownOperationIds` and update `operationsHex`
consistently with both the named and unknown operations. To remove them deliberately, remove or
empty `unknownOperationIds` and remove `operationsHex`, so wallet-cli regenerates a bitmap from the
named `operations` only. If the fields disagree, the update is rejected with `invalid_permission`.

After reviewing the complete resulting structure and fee, submit it:

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
    A permission update can permanently lock an account, and there is no on-chain recovery. The
    chain accepts an owner group even if none of its keys are locally available or its threshold
    requires unavailable co-signers. wallet-cli emits `owner_lockout` or
    `owner_lockout_partial` warnings but does not block a deliberately multi-party setup. It also
    warns when an active permission can itself update permissions.

## Direct artifact workflow

The service-free workflow passes one transaction hex between signers.

### 1. Start the artifact

The initiator selects the permission group, extends the expiration, and produces the first
signature:

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

The default transaction expiration is approximately 60 seconds. Use an explicit expiration, up to
24 hours, when signatures will be collected manually.

`--build-only` can instead produce an unsigned artifact without unlocking a wallet. This is useful
when the first signer is on another machine or when opening a TronLink service collection.

### 2. Inspect approvals

Anyone with the artifact can inspect its permission, current weight, approved signers, missing
weight, and expiration without signing or unlocking a wallet:

```bash
wallet-cli tx approvals --file transaction.hex --network tron:nile
```

An expired transaction remains inspectable but cannot be signed or broadcast.

### 3. Append signatures

Each remaining signer appends exactly one signature while preserving the previous ones:

```bash
printf '%s\n' "$COSIGNER_PASSWORD" |
  wallet-cli tx sign \
    --file transaction.hex \
    --account cosigner \
    --network tron:nile \
    --out transaction.signed.hex \
    --password-stdin
```

Pass the resulting file to the next signer. Online signing verifies permission membership and
rejects duplicate signatures before decrypting the key. On an air-gapped machine, add `--offline`;
the node-backed weight check can be repeated later with `tx approvals`.

### 4. Validate and broadcast

After `thresholdReached` is true, validate without submission and then broadcast:

```bash
wallet-cli tx broadcast --file transaction.signed.hex --network tron:nile --dry-run
wallet-cli tx broadcast --file transaction.signed.hex --network tron:nile --wait
```

`tx broadcast` refuses an expired artifact (`tx_expired`) locally and uses the node's read-only
permission endpoints to reject one below its threshold (`not_authorized`). An incomplete
transaction is therefore never submitted to the node's broadcast endpoint.

## TronLink service collaboration

`tx multisig` is an optional convenience layer. The TronLink service stores a transaction,
accumulates signatures, and notifies co-signers over WebSocket. The direct artifact workflow above
does not require this service.

Configure credentials matching the selected mainnet or testnet environment:

```bash
wallet-cli config tronlinkSecretId '<secret-id>'
wallet-cli config tronlinkSecretKey '<secret-key>'
wallet-cli config tronlinkChannel '<channel>'
```

Build an unsigned artifact, then sign it locally and open a collection:

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

Opening a collection adds the initiator's first signature; there is no empty collection. Other
signers list work awaiting them and sign by transaction id:

```bash
wallet-cli tx multisig --account cosigner --network tron:nile

printf '%s\n' "$COSIGNER_PASSWORD" |
  wallet-cli tx multisig \
    --sign <TX_ID> \
    --account cosigner \
    --network tron:nile \
    --password-stdin
```

Use `tx multisig --watch` to receive only the count of transactions awaiting the selected account;
transaction content is not included in notifications. When the threshold is reached, the service
broadcasts automatically. Confirm the transaction on-chain before attempting the manual
`tx broadcast` fallback.

## Safety checklist

- Run `permission show` before selecting a permission or editing its keys.
- Always `--dry-run` and manually review a full permission replacement.
- Pass the newly signed artifact to the next signer. Its transaction body (`raw_data` and
  `raw_data_hex`) and `txID` must remain unchanged while the signature array grows; changing the
  transaction body invalidates all prior signatures.
- Choose an expiration long enough for collection but no longer than necessary.
- Check `thresholdReached`, not the number of signatures: signer weights may differ.
- Treat TronLink responses as third-party data. wallet-cli re-derives and cross-checks transaction
  identity, owner, contract type, weights, and signature progress before signing.
- On mainnet, obtain explicit approval before updating permissions or broadcasting a transaction.

For complete command fields and error codes, see the upstream references for
[`permission`](https://github.com/tronprotocol/wallet-cli/tree/master/ts/docs/commands/permission),
[`tx sign`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/sign.md),
[`tx approvals`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/approvals.md),
[`tx multisig`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/multisig.md),
and [`tx broadcast`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/tx/broadcast.md).
