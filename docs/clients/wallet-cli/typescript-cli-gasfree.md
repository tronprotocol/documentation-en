# TypeScript CLI GasFree

GasFree lets an account transfer supported tokens without holding TRX. The GasFree service submits
the transfer and charges its fee in the transferred token.

This workflow is separate from the Java commands described in
[Java CLI GasFree](gasfree.md).

## Configure the service

GasFree supports TRON mainnet and Nile; Shasta is not supported. Configure credentials for the
selected mainnet or testnet environment:

```bash
wallet-cli config gasfreeApiKey '<api-key>'
wallet-cli config gasfreeApiSecret '<api-secret>'
```

The API secret is masked when configuration is displayed. Keep `config.yaml` private; on POSIX,
wallet-cli refuses to use an insecure configuration file that contains the secret.

## Find the GasFree address and fees

The GasFree service provides a dedicated address for each wallet account. Tokens used in this
workflow must be sent to that address rather than the account's ordinary TRON address.

Query the address, activation state, supported tokens, and current fees:

```bash
wallet-cli gasfree info --account main --network tron:nile
```

The service charges:

- a fee for each transfer; and
- a one-time activation fee on the first outgoing transfer from an inactive GasFree address.

Both fees are paid in the token and added to the requested transfer amount. Fees and supported
tokens can change, so query or dry-run immediately before transferring.

## Preview and submit a transfer

Use `--dry-run` to review the fees and check whether the GasFree address holds enough tokens:

```bash
wallet-cli gasfree transfer \
  --to TRecipient... \
  --amount 25 \
  --token USDT \
  --network tron:nile \
  --dry-run
```

The balance must cover the recipient amount plus the service fee and any activation fee.

After reviewing the result, sign and submit:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli gasfree transfer \
    --to TRecipient... \
    --amount 25 \
    --token USDT \
    --network tron:nile \
    --password-stdin
```

`--to` also accepts a name stored with `contact add`.

Ledger accounts support GasFree signing. Do not pass `--password-stdin` for a Ledger account, and
enable **Settings > Sign by Hash > Allowed** in the Ledger TRON app.

GasFree does not support `--sign-only` or `--build-only`. Its authorization is submitted through
the GasFree service rather than broadcast as a normal transaction artifact.

## Track the transfer

Submission returns a GasFree `traceId`, not an on-chain transaction id. The transfer may still be
waiting for the service or the network:

```bash
wallet-cli gasfree trace <TRACE_ID> --network tron:nile
```

You can also add `--wait` to `gasfree transfer`.

The service reports progress through `WAITING`, `INPROGRESS`, and `CONFIRMING`.
`SUCCEED` and `FAILED` are terminal states. Polling may skip intermediate states.

Do not pass a GasFree trace id to `tx status`. Continue using `gasfree trace` until the service
returns a terminal state. An on-chain transaction id appears after the service submits the
transaction.

For automation, inspect the returned `state` or `stage`. A successful status query can still
report a failed transfer.

## Checklist

- Use `gasfree info` to obtain the correct receiving address and current fees.
- Keep mainnet and Nile credentials separate.
- Dry-run immediately before sending.
- Confirm the balance covers the amount and all fees.
- Treat a submitted request as pending until it reaches a terminal state.
- On mainnet, confirm the recipient, token, amount, and fee before signing.

For all options and response fields, see the upstream references for
[`gasfree info`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/gasfree/info.md),
[`gasfree transfer`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/gasfree/transfer.md),
and
[`gasfree trace`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/gasfree/trace.md).
