# GasFree

GasFree lets an account transfer tokens (USDT) without holding TRX for gas — the GasFree service
relayer submits the on-chain transaction and deducts the fee from the transferred token. These
commands query the service, send a GasFree transfer, and trace a previous transfer.

GasFree transfers are signed locally with your key and relayed by the GasFree service, so they
require auth (an active/logged-in wallet). `gas-free-info` requires auth only when `--address` is
omitted (it then reports the current wallet); `gas-free-trace` requires no auth.

## Service info — `gas-free-info` / `GasFreeInfo`

Shows the GasFree account info for an address: the derived GasFree address, activation status, and
current nonce/balance details used when building a transfer.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile gas-free-info --address TXyz...
    ```

    - `--address` (optional) — defaults to the current wallet's address. With `--address`, no auth
      is required; without it, the current wallet is used and auth is required.

=== "REPL"

    ```
    GasFreeInfo [Address]
    ```

    With no argument, uses the logged-in account's address.

## GasFree transfer — `gas-free-transfer` / `GasFreeTransfer`

Sends a GasFree token transfer (USDT) to a recipient. The fee is paid in the transferred token via
the GasFree relayer rather than in TRX. In JSON mode the response `data` includes the
`gas_free_id` of the submitted request.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile gas-free-transfer \
      --to TXyz... --amount 1000000
    ```

    - `--to` (required), `--amount` (required, smallest unit / 6 decimals).

=== "REPL"

    ```
    GasFreeTransfer receiverAddress amount
    ```

## Trace a transfer — `gas-free-trace` / `GasFreeTrace`

Looks up the status of a previously submitted GasFree transfer by its trace/request ID (the
`gas_free_id` returned by a transfer).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile gas-free-trace --id <traceId>
    ```

    - `--id` (required). No auth required.

=== "REPL"

    ```
    GasFreeTrace id
    ```
