# Queries

Read-only lookups for blocks, transactions, chain parameters and resource prices, the current
network, connected nodes, and USDT balances.

Queries that take an explicit address generally require no auth. Queries that default to the current
wallet when an address is omitted require auth: `get-address` always reports the active wallet (and
so always requires auth), while `get-balance` and `get-usdt-balance` require auth only when
`--address` is not supplied.

Account, staking/resource, asset, contract, witness, and proposal queries live on their own pages
([Accounts](accounts.md), [Staking & Resources](staking.md), [TRC-10 Assets](trc10.md),
[Smart Contracts](smart-contracts.md), [Governance](governance.md)).

## Network & chain

### Current network — `current-network` / `CurrentNetwork`

Shows which network the client is currently connected to (`MAIN`, `NILE`, `SHASTA`, or `CUSTOM`).

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile current-network
    ```

=== "REPL"

    ```
    CurrentNetwork
    ```

### Chain parameters — `get-chain-parameters` / `GetChainParameters`

Returns the on-chain governance parameters and their current values.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-chain-parameters
    ```

=== "REPL"

    ```
    GetChainParameters
    ```

### Next maintenance time — `get-next-maintenance-time` / `GetNextMaintenanceTime`

Returns the timestamp (ms) of the next maintenance period, when SR/voting changes take effect.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-next-maintenance-time
    ```

=== "REPL"

    ```
    GetNextMaintenanceTime
    ```

### Bandwidth prices — `get-bandwidth-prices` / `GetBandwidthPrices`

Returns the historical bandwidth price schedule.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-bandwidth-prices
    ```

=== "REPL"

    ```
    GetBandwidthPrices
    ```

### Energy prices — `get-energy-prices` / `GetEnergyPrices`

Returns the historical energy price schedule.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-energy-prices
    ```

=== "REPL"

    ```
    GetEnergyPrices
    ```

### Memo fee — `get-memo-fee` / `GetMemoFee`

Returns the fee charged for attaching a memo to a transaction.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-memo-fee
    ```

=== "REPL"

    ```
    GetMemoFee
    ```

## Blocks

### Get block — `get-block` / `GetBlock`

Returns a block by number, or the latest block when no number is given.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block --number 1000000
    ```

    - `--number` (optional) — block number; defaults to the latest block.

=== "REPL"

    ```
    GetBlock [BlockNum]
    ```

    With no argument, returns the current block.

### Get block by ID — `get-block-by-id` / `GetBlockById`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-id --id 00000000000f4240...
    ```

    - `--id` (required) — the block ID (hash).

=== "REPL"

    ```
    GetBlockById block_id
    ```

### Get block by ID or number — `get-block-by-id-or-num` / `GetBlockByIdOrNum`

Accepts either a block number or a block ID.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-id-or-num --value 1000000
    ```

    - `--value` (required) — a block number or block ID.

=== "REPL"

    ```
    GetBlockByIdOrNum [idOrNum] [true]
    ```

    With no argument, returns the current header. A trailing `true` returns the full block instead
    of just the header. Run `GetBlockByIdOrNum help` for all forms.

### Get latest N blocks — `get-block-by-latest-num` / `GetBlockByLatestNum`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-latest-num --count 5
    ```

    - `--count` (required) — number of most-recent blocks to return.

=== "REPL"

    ```
    GetBlockByLatestNum num
    ```

### Get block range — `get-block-by-limit-next` / `GetBlockByLimitNext`

Returns blocks in the half-open range `[start, end)`.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-block-by-limit-next \
      --start 1000000 --end 1000005
    ```

    - `--start` (required), `--end` (required, must be greater than `start`).

=== "REPL"

    ```
    GetBlockByLimitNext start_block_number end_block_number
    ```

### Transaction count in a block — `get-transaction-count-by-block-num` / `GetTransactionCountByBlockNum`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile \
      get-transaction-count-by-block-num --number 1000000
    ```

    - `--number` (required) — block number.

=== "REPL"

    ```
    GetTransactionCountByBlockNum number
    ```

## Transactions

### Get transaction — `get-transaction-by-id` / `GetTransactionById`

Returns the transaction body for a transaction ID.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-transaction-by-id --id <txid>
    ```

    - `--id` (required) — the transaction ID (hash).

=== "REPL"

    ```
    GetTransactionById txid
    ```

### Get transaction info — `get-transaction-info-by-id` / `GetTransactionInfoById`

Returns the execution result of a transaction: fees, energy/bandwidth usage, contract result, and
logs. Use this to read the outcome of a state-changing contract call.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-transaction-info-by-id --id <txid>
    ```

    - `--id` (required).

=== "REPL"

    ```
    GetTransactionInfoById txid
    ```

### Transaction info in a block — `GetTransactionInfoByBlockNum` (REPL only)

Returns the execution results of every transaction in a block.

```
GetTransactionInfoByBlockNum number
```

- `number` (required) — block number.

## Nodes

### List nodes — `list-nodes` / `ListNodes`

Lists the peer nodes the connected node is aware of.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-nodes
    ```

=== "REPL"

    ```
    ListNodes
    ```

## USDT

### USDT balance — `get-usdt-balance` / `GetUSDTBalance`

Returns the USDT (TRC-20) balance of an address. Supported on `main`, `nile`, and `shasta` only.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-usdt-balance --address TXyz...
    ```

    - `--address` (optional) — defaults to the current wallet's address.

=== "REPL"

    ```
    GetUSDTBalance [Address]
    ```

    With no argument, uses the logged-in account's address.

### USDT transfer by ID — `GetUsdtTransferById` (REPL only)

Looks up a previously recorded USDT transfer in the local transaction history by its transaction
ID. Supported on `main`, `nile`, and `shasta` only.

```
GetUsdtTransferById txId
```

- `txId` (required) — the transaction ID to look up in local history.

## Encoding converter — `EncodingConverter` (REPL only)

Interactive helper that converts between address/value encodings (e.g. Base58Check ↔ hex). It
prompts for input rather than taking arguments.

```
EncodingConverter
```
