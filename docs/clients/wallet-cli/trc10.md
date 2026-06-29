# TRC-10 Assets

TRC-10 is TRON's native token standard (managed by the system, not by a smart contract). These
commands issue tokens, update their parameters, participate in token sales, transfer tokens, and
query token information.

REPL transaction-building commands use an optional leading `[OwnerAddress]` for multi-sig; the
Standard CLI uses `--owner` + `--multi`. Issuance, update, participate, transfer, and unfreeze
require auth; queries do not.

## Issue a token — `asset-issue` / `AssetIssue`

Creates a new TRC-10 token. `TrxNum` and `AssetNum` together define the TRX-to-token exchange ratio
during the sale.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile asset-issue \
      --name MyToken --abbr MTK --total-supply 1000000000 \
      --trx-num 1 --ico-num 100 --precision 6 \
      --start-time 1700000000000 --end-time 1701000000000 \
      --description "My token" --url https://example.com \
      --free-net-limit 0 --public-free-net-limit 0
    ```

    - Required: `--name`, `--abbr`, `--total-supply`, `--trx-num`, `--ico-num`, `--start-time`,
      `--end-time`, `--url`, `--free-net-limit`, `--public-free-net-limit`.
    - Optional: `--precision`, `--description`, `--owner`, `--multi`.

=== "REPL"

    ```
    AssetIssue [OwnerAddress] AssetName AbbrName TotalSupply TrxNum AssetNum Precision \
      StartDate EndDate Description Url FreeNetLimitPerAccount PublicFreeNetLimit \
      [FrozenAmount0 FrozenDays0 ... FrozenAmountN FrozenDaysN]
    ```

    `StartDate`/`EndDate` use the format `2018-03-01 2018-03-21`. Trailing
    `FrozenAmount/FrozenDays` pairs are optional and freeze part of the supply.

## Update a token — `update-asset` / `UpdateAsset`

Updates mutable parameters of a token you issued.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-asset \
      --description "Updated" --url https://example.com \
      --new-limit 0 --new-public-limit 0
    ```

    - Required: `--description`, `--url`, `--new-limit`, `--new-public-limit`.
    - Optional: `--owner`, `--multi`.

=== "REPL"

    ```
    UpdateAsset [OwnerAddress] newLimit newPublicLimit description url
    ```

## Participate in a token sale — `participate-asset-issue` / `ParticipateAssetIssue`

Buys a token during its ICO window by sending TRX to the issuer.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile participate-asset-issue \
      --to TIssuer... --asset 1000001 --amount 1000000
    ```

    - Required: `--to`, `--asset`, `--amount`. Optional: `--owner`, `--multi`.

=== "REPL"

    ```
    ParticipateAssetIssue [OwnerAddress] ToAddress AssetID Amount
    ```

## Transfer a token

TRC-10 transfers use `transfer-asset` / `TransferAsset`. See
[Transactions → Transfer a TRC-10 asset](transactions.md#transfer-a-trc-10-asset-transfer-asset-transferasset).

## Unfreeze token supply — `unfreeze-asset` / `UnfreezeAsset`

Unfreezes supply that was frozen at issuance, once its lock period has elapsed.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile unfreeze-asset
    ```

    - `--owner`, `--multi` (optional).

=== "REPL"

    ```
    UnfreezeAsset [OwnerAddress]
    ```

## Token queries (no auth required)

### By issuing account — `get-asset-issue-by-account` / `GetAssetIssueByAccount`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-by-account --address TXyz...
    ```

    - `--address` (required).

=== "REPL"

    ```
    GetAssetIssueByAccount Address
    ```

### By ID — `get-asset-issue-by-id` / `GetAssetIssueById`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-by-id --id 1000001
    ```

    - `--id` (required).

=== "REPL"

    ```
    GetAssetIssueById AssetID
    ```

### By name — `get-asset-issue-by-name` / `GetAssetIssueByName`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-by-name --name MyToken
    ```

    - `--name` (required).

=== "REPL"

    ```
    GetAssetIssueByName AssetName
    ```

### All with a given name — `get-asset-issue-list-by-name` / `GetAssetIssueListByName`

Token names are not unique; this returns every token sharing a name.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-asset-issue-list-by-name --name MyToken
    ```

    - `--name` (required).

=== "REPL"

    ```
    GetAssetIssueListByName AssetName
    ```

### List all tokens — `list-asset-issue` / `ListAssetIssue`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-asset-issue
    ```

=== "REPL"

    ```
    ListAssetIssue
    ```

### List tokens (paginated) — `list-asset-issue-paginated` / `ListAssetIssuePaginated`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile list-asset-issue-paginated \
      --offset 0 --limit 20
    ```

    - `--offset` (required), `--limit` (required).

=== "REPL"

    ```
    ListAssetIssuePaginated offset limit
    ```
