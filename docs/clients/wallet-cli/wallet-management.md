# Wallet Management

Commands for creating, importing, exporting, and selecting local wallets, plus the Standard CLI
alias system.

A few mode differences to keep in mind:

- The **REPL** keeps a logged-in session: you authenticate once with `Login` / `LoginAll` and the
  wallet stays unlocked until you `Logout`, `Lock`, or exit.
- The **Standard CLI** is stateless per invocation: there is no interactive login. Commands that
  sign transactions read the password from `MASTER_PASSWORD` (or `--password-stdin`) and act on the
  **active wallet** (`set-active-wallet`) or the wallet named by `--wallet`.
- Several REPL wallet operations (private-key/mnemonic/Ledger import, mnemonic/keystore export,
  password change) have no Standard CLI equivalent because they require interactive secret entry.

## Create a wallet — `register-wallet` / `RegisterWallet`

Creates a brand-new wallet with a freshly generated mnemonic and stores an encrypted keystore in
`Wallet/`.

=== "Standard CLI"

    ```bash
    export MASTER_PASSWORD='your-wallet-password'
    java -jar build/libs/wallet-cli.jar --network nile register-wallet --name my-wallet --words 12
    ```

    - `--name` (required) — wallet name.
    - `--words` (optional) — mnemonic word count, `12` or `24` (default `12`).
    - The keystore is encrypted with `MASTER_PASSWORD`. The newly created wallet is set as the
      active wallet automatically.

=== "REPL"

    ```
    RegisterWallet
    ```

    Prompts interactively for a password (entered twice) and the mnemonic word count (12 or 24).

## Generate a sub-account — `generate-sub-account` / `GenerateSubAccount`

Derives an additional account from the current wallet's mnemonic at a given index.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile generate-sub-account --index 1 --name sub-1
    ```

    - `--index` (required) — derivation index.
    - `--name` (required) — name for the sub-account. Requires auth.

=== "REPL"

    ```
    GenerateSubAccount
    ```

    Prompts interactively for the derivation index and name.

## Import a wallet (REPL only)

These commands accept secret material interactively and exist only in the REPL.

```
ImportWallet                 # import from a raw private key (prompted)
ImportWalletByMnemonic       # import from a 12/24-word BIP39 mnemonic (prompted)
ImportWalletByBase64         # import from a Base64-encoded private key (prompted)
ImportWalletByKeystore  tronlink <keystore-file>   # import from a TronLink keystore file
ImportWalletByLedger         # import an account from a Ledger hardware wallet
```

- `ImportWalletByKeystore` takes a fixed `tronlink` channel keyword followed by the path to the
  exported keystore JSON file. The keystore password is entered interactively when prompted.
- `ImportWalletByLedger` requires a connected Ledger device and guides you through account
  selection.

## Generate a standalone address — `GenerateAddress` (REPL only)

Generates a random TRON key pair and prints the address and private key, without storing a keystore.

```
GenerateAddress [isECKey]
```

- `isECKey` (optional) — defaults to an EC (secp256k1) key.

## Log in and select a wallet

=== "Standard CLI"

    The Standard CLI does not log in interactively. Instead it acts on the **active wallet**, or a
    wallet selected per-command with the global `--wallet <name|path>` option.

    ```bash
    # List wallets and their active status
    java -jar build/libs/wallet-cli.jar list-wallet

    # Set the active wallet by address or by name
    java -jar build/libs/wallet-cli.jar set-active-wallet --address TXyz...
    java -jar build/libs/wallet-cli.jar set-active-wallet --name my-wallet

    # Show the current active wallet
    java -jar build/libs/wallet-cli.jar get-active-wallet
    ```

    - `set-active-wallet` accepts `--address` or `--name` (provide one).
    - Authentication for signing commands uses `MASTER_PASSWORD` (or `--password-stdin`).

=== "REPL"

    ```
    Login           # choose one wallet and log in
    LoginAll        # log in to all stored wallets
    SwitchWallet    # switch the active wallet among logged-in wallets
    Logout          # end the session
    Lock            # lock the wallet (must Unlock before use)
    Unlock [durationSeconds]   # unlock for N seconds (default 300)
    ```

## Back up a wallet (REPL only)

```
BackupWallet            # print the wallet's private key (after password check)
BackupWallet2Base64     # print the private key Base64-encoded
ExportWalletMnemonic    # print the wallet's BIP39 mnemonic (after password check)
ExportWalletKeystore  tronlink <directory>   # export the keystore file to a directory
ViewBackupRecords       # list local backup history
```

All of these require the wallet password and are interactive, so they are REPL-only.

## Derive a private key from a mnemonic — `GetPrivateKeyByMnemonic` (REPL only)

Prompts for a BIP39 mnemonic and prints the private key derived at the default path
`m/44'/195'/0'/0/0`. This does not import or store a wallet.

```
GetPrivateKeyByMnemonic
```

## Change the wallet password — `ChangePassword` (REPL only)

```
ChangePassword
```

Prompts for the current password and a new password.

## Rename a wallet — `modify-wallet-name` / `ModifyWalletName`

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar modify-wallet-name --name new-name
    ```

    - `--name` (required) — the new wallet name. Requires auth.

=== "REPL"

    ```
    ModifyWalletName new_wallet_name
    ```

## Clear the keystore — `clear-wallet-keystore` / `ClearWalletKeystore`

Deletes the encrypted keystore file(s) for the wallet from local storage. This is destructive.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar clear-wallet-keystore --force
    ```

    - `--force` is syntactically optional, but required to execute the destructive action in
      Standard CLI mode — without it the command fails with a usage error. Requires auth.

=== "REPL"

    ```
    ClearWalletKeystore
    ```

## Reset the wallet — `reset-wallet` / `ResetWallet`

Wipes local wallet state back to an initial condition. This is destructive.

=== "Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar reset-wallet --confirm delete-all-wallets
    ```

    - `--confirm` must be passed with the exact value `delete-all-wallets` to perform the reset.
      Running `reset-wallet` with no `--confirm` is a dry-run (it lists the files that would be
      deleted); any other value is a usage error.

=== "REPL"

    ```
    ResetWallet
    ```

## Address book — `AddressBook` (REPL only)

Opens the interactive local address book, where you can store and manage friendly names for
frequently used addresses. It prompts for input rather than taking arguments.

```
AddressBook
```

## View transaction history — `ViewTransactionHistory` (REPL only)

Lists locally recorded transaction history for the current wallet.

```
ViewTransactionHistory
```

## Aliases (Standard CLI only)

The Standard CLI supports **aliases** — friendly names for accounts and tokens — so you can write
`--to my-friend` instead of a raw Base58 address. Aliases are scoped per network and come from two
layers: a set of **built-in** aliases (read-only) and your **user** aliases.

Alias resolution applies to **address** fields, not to numeric IDs:

- **Account aliases** (`--type ACCOUNT`) resolve on address fields such as `--to`, `--from`,
  `--owner`, `--receiver`, and `--address`.
- **Token aliases** (`--type TOKEN`) resolve on contract-address fields — the contract `--contract`
  option and the `--address` of `get-contract` / `get-contract-info`.

They do **not** apply to TRC-10 asset IDs (`--asset`) or to `--token-id`, which are read verbatim as
numeric IDs. When an alias is resolved, the resolution is reported under `meta.resolved` in JSON
mode.

```bash
# Add an account alias
java -jar build/libs/wallet-cli.jar --network nile alias-add \
  --name treasury --type ACCOUNT --address TXyz... --note "team treasury"

# Add a token alias (with decimals)
java -jar build/libs/wallet-cli.jar --network nile alias-add \
  --name usdt --type TOKEN --address TR7NHq... --decimals 6

# List aliases (optionally filter by type)
java -jar build/libs/wallet-cli.jar --network nile alias-list --type ACCOUNT

# Resolve an alias or address to its canonical form
java -jar build/libs/wallet-cli.jar --network nile alias-resolve --name treasury

# Remove a user alias
java -jar build/libs/wallet-cli.jar --network nile alias-remove --name treasury
```

Option notes:

- `alias-add`: `--name`, `--type` (`ACCOUNT` or `TOKEN`), `--address` are required. `--decimals` is
  valid only for `TOKEN`; `--note` is valid only for `ACCOUNT`.
- Built-in aliases cannot be overridden or removed. To replace a user alias, `alias-remove` it
  first, then `alias-add` again.
- `alias-list` and `alias-resolve` accept an optional `--type` filter.
