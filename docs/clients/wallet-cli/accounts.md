# Accounts

On-chain account operations: creating and updating accounts, reading balances and account data, and
managing account permissions.

In the REPL, transaction-building commands take an **optional first `[OwnerAddress]`** argument. If
omitted, the currently logged-in account is used; if provided, the command is prepared as a
multi-signature transaction for that owner. In the Standard CLI the equivalent is `--owner` together
with `--multi`.

## Create an account — `create-account` / `CreateAccount`

Creates a new on-chain account for a given address. (An address only becomes an on-chain account
once it is activated, e.g. by receiving TRX or via this command.)

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile create-account --address TXyz...
    ```

    - `--address` (required) — the address to activate.
    - `--owner` (optional), `--multi` (optional). Requires auth.

=== "REPL"

    ```
    CreateAccount [OwnerAddress] Address
    ```

## Update the account name — `update-account` / `UpdateAccount`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-account --name "my account"
    ```

    - `--name` (required) — the new account name.
    - `--owner` (optional), `--multi` (optional). Requires auth.

=== "REPL"

    ```
    UpdateAccount [OwnerAddress] AccountName
    ```

## Set the account ID — `set-account-id` / `SetAccountId`

Sets a unique, human-readable account ID for the account.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile set-account-id --id myaccountid
    ```

    - `--id` (required) — the account ID to set.
    - `--owner` (optional). Requires auth.

=== "REPL"

    ```
    SetAccountId [OwnerAddress] account_id
    ```

## Read account data

### Get account info — `get-account` / `GetAccount`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account --address TXyz...
    ```

    - `--address` (required). No auth required.

=== "REPL"

    ```
    GetAccount Address
    ```

### Get account by ID — `get-account-by-id` / `GetAccountById`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account-by-id --id myaccountid
    ```

    - `--id` (required). No auth required.

=== "REPL"

    ```
    GetAccountById account_id
    ```

### Get the current address — `get-address` / `GetAddress`

Prints the address of the active/logged-in wallet.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar get-address
    ```

    Requires auth (it reports the active wallet's address).

=== "REPL"

    ```
    GetAddress
    ```

### Get the TRX balance — `get-balance` / `GetBalance`

=== "Standard CLI"

    ```bash
    # Balance of an explicit address (no auth needed)
    java -jar build/libs/wallet-cli.jar --network nile get-balance --address TXyz...

    # Balance of the active wallet (requires auth)
    java -jar build/libs/wallet-cli.jar --network nile get-balance
    ```

    - `--address` (optional). If provided, no auth is required; if omitted, the active wallet's
      balance is read and auth is required.

=== "REPL"

    ```
    GetBalance [Address]
    ```

    Omit the address to read the current account's balance.

### Show a receiving QR code — `ShowReceivingQrCode` (REPL only)

```
ShowReceivingQrCode
```

Renders a QR code of the current address for receiving funds.

## Account permissions — `update-account-permission` / `UpdateAccountPermission`

TRON accounts support a flexible permission model (an owner permission, an optional witness
permission, and multiple active permissions), enabling multi-signature control. This command
replaces the account's permission set with the one you supply.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile update-account-permission \
      --owner TXyz... --permissions '<permission-json>'
    ```

    - `--owner` (required) — the account whose permissions are updated.
    - `--permissions` (required) — the full permission set as a JSON string.
    - `--multi` (optional). Requires auth.

=== "REPL"

    ```
    UpdateAccountPermission [ownerAddress] [permissions]
    ```

    With no arguments (or just an owner address), an interactive builder walks you through editing
    the permissions. With two arguments, the second is the permission set as a JSON string.

The permission JSON has the following shape (keys, thresholds, and weighted signer lists):

```json
{
  "owner_permission": {
    "type": 0,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      { "address": "TXyz...", "weight": 1 }
    ]
  },
  "witness_permission": {
    "type": 1,
    "permission_name": "witness",
    "threshold": 1,
    "keys": [
      { "address": "TXyz...", "weight": 1 }
    ]
  },
  "active_permissions": [
    {
      "type": 2,
      "permission_name": "active",
      "threshold": 2,
      "operations": "7fff1fc0033ef30f000000000000000000000000000000000000000000000000",
      "keys": [
        { "address": "TAbc...", "weight": 1 },
        { "address": "TDef...", "weight": 1 }
      ]
    }
  ]
}
```

- `threshold` is the total signer weight required for the permission to authorize an action.
- `operations` (active permissions only) is a 32-byte hex bitmap selecting which contract/operation
  types the permission may perform. The example above matches the 4.9.7 default active-permission
  bitmap: it excludes disabled operation 51 (`ShieldedTransferContract`) while retaining active
  operations such as 49 and 52.
- `witness_permission` is only relevant for super-representative accounts.
