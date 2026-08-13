# TypeScript CLI GasFree

GasFree transfers let an account move supported tokens without holding TRX. The TypeScript CLI
signs an EIP-712/TIP-712 authorization locally, and the GasFree provider relays the transfer and
charges its fee in the transferred token.

This workflow is separate from the Java CLI commands documented in [Java CLI GasFree](gasfree.md).

## Networks and credentials

The TypeScript GasFree commands support TRON mainnet and Nile. Shasta is not supported. Configure
API credentials that match the selected mainnet or testnet service environment:

```bash
wallet-cli config gasfreeApiKey '<api-key>'
wallet-cli config gasfreeApiSecret '<api-secret>'
```

`gasfreeApiSecret` is masked in `wallet-cli config` text and JSON output; `gasfreeApiKey` is
displayed. When the API secret is present, `config.yaml` must not be a symbolic link and must have
no group or world permissions on POSIX; otherwise it is rejected with `insecure_config`. An
unreadable or invalid configuration returns `invalid_config`.

Missing credentials return `gasfree_credentials_missing`. Rejected credentials, including
credentials for the wrong environment, return `gasfree_auth_failed`; rate limiting returns
`provider_rate_limited`. Transport failures, malformed responses, and HTTP 5xx responses return
`provider_error`. Other request or business rejection can return `gasfree_rejected`, while a
missing provider resource returns `not_found`.

## GasFree address and fees

For each wallet account, the GasFree service reports a dedicated GasFree address. The CLI obtains
this address from the provider; it does not derive it locally. Assets used for GasFree transfers are
held and sent from this address, not directly from the owner's ordinary TRON address. Query it
together with activation state, nonce, supported tokens, and the provider's current fee schedule:

```bash
wallet-cli gasfree info --account main --network tron:nile
```

Give the returned GasFree address to a sender when the account needs to receive tokens for this
workflow.

The provider deducts:

- a per-transfer service fee; and
- a one-time activation fee on the first outgoing transfer from an inactive GasFree address.

Both fees are charged in the token and are added to the requested transfer amount. The provider's
supported-token list and fees are live configuration, so query or dry-run immediately before a
transfer rather than hard-coding them.

## Preview and submit a transfer

Use `--dry-run` to retrieve fees, validate provider metadata, and check the token balance without
unlocking the wallet or submitting an authorization:

```bash
wallet-cli gasfree transfer \
  --to TRecipient... \
  --amount 25 \
  --token USDT \
  --network tron:nile \
  --dry-run
```

The balance must cover the amount plus the service fee and, when applicable, the activation fee.
An insufficient balance returns `insufficient_token_balance`.

After reviewing the fee breakdown, sign and submit:

```bash
printf '%s\n' "$WALLET_PASSWORD" |
  wallet-cli gasfree transfer \
    --to TRecipient... \
    --amount 25 \
    --token USDT \
    --network tron:nile \
    --password-stdin
```

Ledger accounts also support GasFree signing. Do not pipe a password or pass `--password-stdin` for
a Ledger account. Enable **Settings > Sign by Hash > Allowed** in the Ledger TRON app; otherwise the
CLI returns `ledger_setting_required`. An app version without TIP-712 hash signing returns
`ledger_unsupported`.

`--to` also accepts a name stored with `contact add`. The receipt includes `toContact` when a name
was resolved.

GasFree has no `--sign-only` or `--build-only` mode. Its signed authorization is bound to the
provider submission protocol and is not a normal TRON transaction artifact for offline broadcast.

## Track provider and chain state

Submission returns a provider `traceId`, not a transaction id. At this point the provider has
accepted the request, but the transfer is not necessarily on-chain:

```json
{
  "kind": "gasfree-transfer",
  "stage": "submitted",
  "traceId": "7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527"
}
```

Either add `--wait` to the original transfer or query it later:

```bash
wallet-cli gasfree trace \
  7f3e9a02-58c1-4d2e-b6a4-91d0c3f8e527 \
  --network tron:nile
```

The non-terminal provider states are ordered as follows:

```text
WAITING → INPROGRESS → CONFIRMING
```

`SUCCEED` and `FAILED` are terminal states. Polling observes snapshots and may skip one or more
intermediate states, so automation must not require every state to appear.

An on-chain `txId` appears only after the provider submits the transaction. Do not pass a GasFree
`traceId` to `tx status`; use `gasfree trace` until the provider returns a terminal state.

A failed provider transfer is still a successful status query: `gasfree trace` exits `0` with
`success: true`, while `data.state` is `FAILED`. When the provider supplies an explanation, it is
returned as `data.failureReason`. Similarly, `gasfree transfer --wait` reports
`data.stage: "failed"`. Automation must branch on these data fields rather than the command exit
code alone.

## Integrity and signing checks

Before submission, wallet-cli:

- validates supported-token and fee metadata returned by the provider;
- checks amount plus all applicable fees against the GasFree token balance;
- recomputes the typed-data digest;
- signs locally and recovers the signer address from the signature;
- rejects a signature that does not match the selected account.

Metadata inconsistency returns `gasfree_integrity`, signing mismatch or refusal returns
`signing_rejected`, and provider rejection returns `gasfree_rejected`. Watch-only accounts return
`watch_only_no_signer` before signing.

## Operational checklist

- Use `gasfree info` to obtain the correct receiving address and current fee schedule.
- Keep mainnet and Nile API credentials separate and switch them when changing environments.
- Dry-run immediately before sending, especially for an inactive GasFree address.
- Confirm `amount + serviceFee + activateFee`, not just the recipient amount.
- Treat `stage: "submitted"` as provider acceptance, not chain confirmation.
- On mainnet, confirm the recipient, token, amount, and fee with the user before signing.

For complete fields and error codes, see the upstream references for
[`gasfree info`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/gasfree/info.md),
[`gasfree transfer`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/gasfree/transfer.md),
and [`gasfree trace`](https://github.com/tronprotocol/wallet-cli/blob/master/ts/docs/commands/gasfree/trace.md).
