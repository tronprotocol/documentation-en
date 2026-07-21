# wallet-cli

`wallet-cli` is a command-line wallet for the TRON network; its official repository is
[tronprotocol/wallet-cli](https://github.com/tronprotocol/wallet-cli). It manages keys and accounts locally
and talks to a TRON node primarily over gRPC (through the
[Trident SDK](https://github.com/tronprotocol/trident)) to query chain data and build, sign, and
broadcast transactions. A few features (such as GasFree fee-delegated transfers) instead call the
relevant service over HTTP.

It offers three ways to drive it:

- **Java Interactive (REPL) mode** — a human-friendly shell with tab completion and interactive
  prompts. Best for manual exploration and day-to-day wallet management.
- **Java Standard CLI mode** — a non-interactive, scriptable interface with deterministic exit codes
  and optional JSON output. Best for automation and scripts that use the Java JAR.
- **TypeScript / npm CLI** — a separate Node.js-based CLI introduced in 4.9.7 and published as
  `@tron-walletcli/wallet-cli`. It uses grouped commands such as `tx send` and `account balance`,
  and is designed for automation, CI/CD, and AI agents.

The command reference pages below focus on the Java JAR's REPL and Standard CLI modes. For the
Node.js command surface, see [TypeScript / npm CLI](typescript-cli.md). Use the tabs below to compare
the same account query across the three entry points:

=== "Java Standard CLI"

    ```bash
    java -jar build/libs/wallet-cli.jar --network nile get-account --address TXyz...
    ```

=== "Java REPL"

    ```
    GetAccount TXyz...
    ```

=== "TypeScript / npm CLI"

    ```bash
    wallet-cli account info --network tron:nile --account TXyz...
    ```

## Build

`wallet-cli` is built with Gradle and requires **Java 8**.

```bash
# Build the project (also generates protobuf sources into src/main/gen/)
./gradlew build

# Build the fat JAR (output: build/libs/wallet-cli.jar)
./gradlew shadowJar
```

After `shadowJar`, you can run the wallet from the produced JAR:

```bash
java -jar build/libs/wallet-cli.jar
```

## Run

### Interactive (REPL) mode

Launch the interactive shell with no command. Either of these works:

```bash
./gradlew run
# or, from the built JAR:
java -jar build/libs/wallet-cli.jar
```

You then type commands at the prompt (for example `Login`, `GetBalance`, `SendCoin ...`). Command
names are case-insensitive and support tab completion. Type `Help` to list commands, or
`Help <Command>` for details on one command.

### Standard CLI mode

Pass a command (and its options) on the command line. The process runs the single command, prints
the result, and exits:

```bash
java -jar build/libs/wallet-cli.jar --network nile get-balance --address TXyz...
java -jar build/libs/wallet-cli.jar --output json --network nile get-account --address TXyz...
```

Standard CLI command names use kebab-case (`get-account`, `send-coin`); most commands also accept a
no-dash alias (`getaccount`, `sendcoin`). Not every command registers one — the `alias-*` commands,
for example, are only available in their dashed form.

There is also a `help` command for per-command usage:

```bash
java -jar build/libs/wallet-cli.jar help --command send-coin
```

## Global options (Standard CLI)

Execution-modifier global options are parsed by `GlobalOptions` and may appear either **before or
after** the command name. Top-level mode selectors have stricter placement rules, as described
below.

| Option | Values | Description |
|--------|--------|-------------|
| `--network` | `main`, `nile`, `shasta`, `custom` | Select the network to connect to. |
| `--grpc-endpoint` | `host:port` | Override the gRPC endpoint (used with `--network custom`). |
| `--output` | `text` (default), `json` | Output format. |
| `--wallet` | name or path | Select a specific wallet keystore by name or path. |
| `--quiet` | flag | Suppress non-essential informational output. |
| `--verbose` | flag | Enable debug logging. (Conflicts with `--quiet`.) |
| `--password-stdin` | flag | Read the wallet password from stdin (overrides `MASTER_PASSWORD`). |
| `--interactive` | flag | Launch the interactive REPL instead of running a command. |
| `--help`, `-h` | flag | Show global help, or help for the named command. (The `help --command <name>` command does the same.) |
| `--version` | flag | Print version information. |

Notes:

- The execution modifiers `--network`, `--grpc-endpoint`, `--output`, `--wallet`, `--quiet`,
  `--verbose`, and `--password-stdin` are recognized before or after the command name.
- The top-level mode selectors `--version` and `--interactive` must appear before the command name.
  After a command, they are treated as command-local arguments instead.
- `--help` and `-h` before the command request global help; after the command they request help for
  that command.
- Valued global options (`--output`, `--network`, `--wallet`, and `--grpc-endpoint`) accept their
  value either as the next token (`--network nile`) or inline (`--network=nile`).
- Options that take a value cannot be repeated, and unknown global options are rejected.

## Authentication (Standard CLI)

Standard CLI mode is non-interactive, so it never prompts for a password. Commands that build and
sign a transaction (marked **requires auth** in this documentation) authenticate automatically:

1. The wallet password is read from the `MASTER_PASSWORD` environment variable, or from **stdin**
   when `--password-stdin` is passed (stdin takes precedence).
2. The keystore is loaded from the `Wallet/` directory. Use `--wallet <name|path>` to pick a
   specific wallet, or set an **active wallet** with `set-active-wallet` (see
   [Wallet Management](wallet-management.md)).

Most read-only query commands do not require authentication. The exceptions are queries that act on
the current wallet: `get-address` always requires auth, and `get-balance` / `get-usdt-balance` /
`gas-free-info` require auth when `--address` is omitted (see [Queries](query.md) and
[GasFree](gasfree.md)).

```bash
export MASTER_PASSWORD='your-wallet-password'
java -jar build/libs/wallet-cli.jar --network nile send-coin --to TXyz... --amount 1000000
```

The REPL handles authentication differently: you log in interactively with `Login` / `LoginAll`
and the session stays unlocked. See [Wallet Management](wallet-management.md).

## JSON output and exit codes (Standard CLI)

With `--output json`, every command emits a single JSON envelope on stdout.

Success:

```json
{
  "success": true,
  "data": { }
}
```

Error:

```json
{
  "success": false,
  "error": "execution_error",
  "message": "human-readable explanation"
}
```

Additional rules:

- Commands that broadcast a transaction include the transaction id as `txid` in `data`
  (single-signature broadcasts only).
- `deploy-contract` includes the deployed `contract_address` in `data`.
- When an alias is resolved for an option, the envelope includes a `meta.resolved` array describing
  the resolution (see the alias system in [Wallet Management](wallet-management.md)).

Exit codes:

| Code | Meaning |
|------|---------|
| `0` | Success. |
| `1` | Execution error (`"error": "execution_error"` and others). |
| `2` | Usage error (`"error": "usage_error"` — bad flags, missing required option, etc.). |

This makes the standard CLI safe to drive from scripts: check the exit code, and parse the single
JSON object from stdout.

## Networks and configuration

The default node endpoints for each network, plus other defaults, live in
`src/main/resources/config.conf` (HOCON format). The `--network` flag selects among `main`, `nile`
(testnet), `shasta` (testnet), and `custom`. For `custom`, provide the endpoint with
`--grpc-endpoint host:port`.

In the REPL, use `SwitchNetwork` to change networks and `CurrentNetwork` to see the active one.

## Command reference

Commands are grouped by domain:

- [Wallet Management](wallet-management.md) — create/import/export wallets, login, backup, lock,
  active wallet, aliases.
- [Accounts](accounts.md) — on-chain account creation and updates, balances, permissions.
- [Staking & Resources](staking.md) — freeze/unfreeze (v1 & v2), resource delegation, rewards.
- [Transactions](transactions.md) — transfer TRX/assets/USDT, multi-signature signing, broadcast.
- [Smart Contracts](smart-contracts.md) — deploy, trigger, constant calls, energy estimation.
- [TRC-10 Assets](trc10.md) — issue, update, participate, transfer, and query TRC-10 tokens.
- [Governance](governance.md) — witnesses, voting, proposals, brokerage, reward withdrawal.
- [GasFree](gasfree.md) — gas-free (sponsored) USDT transfers.
- [Queries](query.md) — blocks, transactions, chain parameters, prices, nodes, and utilities.
