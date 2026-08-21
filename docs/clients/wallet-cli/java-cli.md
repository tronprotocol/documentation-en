# Java CLI

The Java implementation of `wallet-cli` provides two entry points:

- **Interactive (REPL) mode** — a human-friendly shell with tab completion and interactive prompts.
- **Standard CLI mode** — a non-interactive interface with deterministic exit codes and optional
  JSON output.

Both use the same Java JAR and together expose the Java implementation's feature surface, although
some commands are available in only one mode. For the npm-based implementation, see
[TypeScript / npm CLI](typescript-cli.md).

## Build

The Java implementation is located in the repository's `java/` directory. It is built with Gradle
and requires **Java 8**. The commands below keep the working directory at the repository root so the
paths used throughout this section stay consistent.

```bash
git clone https://github.com/tronprotocol/wallet-cli.git
cd wallet-cli

# Build the project and the fat JAR
./java/gradlew -p java build shadowJar
```

After `shadowJar`, you can run the wallet from the produced JAR:

```bash
java -jar java/build/libs/wallet-cli.jar
```

## Run

### Interactive (REPL) mode

Launch the interactive shell with no command. Either of these works:

```bash
./java/gradlew -p java run
# or, from the built JAR:
java -jar java/build/libs/wallet-cli.jar
```

You then type commands at the prompt (for example `Login`, `GetBalance`, `SendCoin ...`). Command
names are case-insensitive and support tab completion. Type `Help` to list commands, or
`Help <Command>` for details on one command.

### Standard CLI mode

Pass a command (and its options) on the command line. The process runs the single command, prints
the result, and exits:

```bash
java -jar java/build/libs/wallet-cli.jar --network nile get-balance --address TXyz...
java -jar java/build/libs/wallet-cli.jar --output json --network nile get-account --address TXyz...
```

Standard CLI command names use kebab-case (`get-account`, `send-coin`); most commands also accept a
no-dash alias (`getaccount`, `sendcoin`). Not every command registers one — the `alias-*` commands,
for example, are only available in their dashed form.

There is also a `help` command for per-command usage:

```bash
java -jar java/build/libs/wallet-cli.jar help --command send-coin
```

## Global options (Standard CLI)

The following options configure Standard CLI commands:

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

- Network, output, wallet, logging, and password options may appear before or after the command.
- Put `--version` and `--interactive` before the command name.
- Put `--help` before a command for global help or after it for command-specific help.
- Options with values accept both `--network nile` and `--network=nile` forms.

## Authentication (Standard CLI)

Standard CLI mode is non-interactive, so it never prompts for a password. Commands that build and
sign a transaction (marked **requires auth** in this documentation) read the wallet password from
`MASTER_PASSWORD`, or from stdin when `--password-stdin` is passed. Stdin takes precedence. Use
`--wallet <name|path>` to select a wallet, or set an **active wallet** with `set-active-wallet` (see
[Wallet Management](wallet-management.md)).

Most read-only query commands do not require authentication. The exceptions are queries that act on
the current wallet: `get-address` always requires auth, and `get-balance` / `get-usdt-balance` /
`gas-free-info` require auth when `--address` is omitted (see [Queries](query.md) and
[GasFree](gasfree.md)).

```bash
export MASTER_PASSWORD='your-wallet-password'
java -jar java/build/libs/wallet-cli.jar --network nile send-coin --to TXyz... --amount 1000000
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

Transaction commands may add identifiers such as `txid` or `contract_address` to `data`. Alias
resolution details may appear under `meta.resolved` (see [Wallet Management](wallet-management.md)).

Exit codes:

| Code | Meaning |
|------|---------|
| `0` | Success. |
| `1` | Execution error (`"error": "execution_error"` and others). |
| `2` | Usage error (`"error": "usage_error"` — bad flags, missing required option, etc.). |

For scripts, check the exit code and parse the JSON object from stdout.

## Networks and configuration

The `--network` flag selects `main`, `nile` (testnet), `shasta` (testnet), or `custom`. For a custom
network, provide the node endpoint with `--grpc-endpoint host:port`.

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
