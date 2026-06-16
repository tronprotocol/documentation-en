# Transactions

Transferring value (TRX, TRC-10 assets, USDT), the multi-signature signing workflow, and
broadcasting raw transactions.

TRX amounts are in **SUN** (1 TRX = 1,000,000 SUN). USDT amounts are in the token's smallest unit
(USDT has 6 decimals, so 1 USDT = 1,000,000).

The REPL takes an optional leading `[OwnerAddress]` for multi-sig; the Standard CLI uses `--owner`
together with `--multi`. Transfer commands require auth.

## Send TRX — `send-coin` / `SendCoin`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile send-coin \
      --to TXyz... --amount 1000000
    ```

    - `--to` (required), `--amount` (required, SUN).
    - `--owner`, `--permission-id`, `--multi` (optional).
    - In JSON mode the response `data` includes the broadcast `txid` (single-signature transfers).

=== "REPL"

    ```
    SendCoin [OwnerAddress] ToAddress Amount
    ```

## Transfer a TRC-10 asset — `transfer-asset` / `TransferAsset`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile transfer-asset \
      --to TXyz... --asset 1000001 --amount 100
    ```

    - `--to` (required), `--asset` (required, the TRC-10 asset ID), `--amount` (required).
    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    TransferAsset [OwnerAddress] ToAddress AssetID Amount
    ```

## Transfer USDT — `transfer-usdt` / `TransferUSDT`

Convenience command for transferring USDT (TRC-20). Supported on `main`, `nile`, and `shasta` only.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile transfer-usdt \
      --to TXyz... --amount 1000000
    ```

    - `--to` (required), `--amount` (required, smallest unit / 6 decimals).
    - `--owner`, `--permission-id`, `--multi` (optional).

=== "REPL"

    ```
    TransferUSDT [OwnerAddress] ToAddress Amount
    ```

## Multi-signature signing workflow (REPL only)

For multi-signature accounts, a transaction is built by one party and then signed by additional
authorized keys until the required signature weight is reached, before being broadcast. The
following commands operate on the hex-encoded transaction string and are available in the REPL:

```
AddTransactionSign           TransactionHexString   # add your signature to a transaction
GetTransactionSignWeight     TransactionHexString   # show current vs required signature weight
GetTransactionApprovedList   TransactionHexString   # list addresses that have already signed
```

Typical flow:

1. Build a transaction with a transfer/contract command and the `[OwnerAddress]` (multi) form. The
   REPL returns the unsigned/partially-signed transaction hex.
2. Each co-signer runs `AddTransactionSign <hex>` to append their signature, producing a new hex.
3. Check progress with `GetTransactionSignWeight <hex>` and `GetTransactionApprovedList <hex>`.
4. Once the threshold is met, broadcast it.

In the Standard CLI, a single-key multi-sign transaction is produced in one step using the
`--multi` and `--permission-id` options on the relevant command.

### TronLink multi-sign — `TronlinkMultiSign` (REPL only)

Interactive helper that walks through a TronLink-compatible multi-signature signing flow. It prompts
for input rather than taking arguments, and is supported on `main`, `nile`, and `shasta` only.

```
TronlinkMultiSign
```

## Broadcast a transaction — `broadcast-transaction` / `BroadcastTransaction`

Submits a signed, hex-encoded transaction to the network.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile broadcast-transaction \
      --transaction 0a83010a02...
    ```

    - `--transaction` (required) — the signed transaction as a hex string. No auth required (the
      transaction is already signed).

=== "REPL"

    ```
    BroadcastTransaction TransactionHexString
    ```
