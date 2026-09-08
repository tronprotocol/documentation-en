# wallet-cli

A command-line wallet for the [TRON network](https://tron.network) — interactive in Java, agent-first in TypeScript.

This repository holds **two independent implementations** that share the same purpose but target different users:

- **[Java](java/index.md)** — the original, full-featured reference CLI. An interactive prompt (REPL) you drive by hand.
- **[TypeScript](typescript/index.md)** — an agent-first rewrite for automation. Standard subcommands with a stable JSON envelope, built for scripts, CI, and AI agents.

Both manage the same kind of wallet, and on TRON networks a seed derives the same address in either. They cover the same TRON feature surface and differ in how you install and drive them — and the TypeScript implementation additionally speaks **EVM networks** (Ethereum, BNB Smart Chain and their testnets), which the Java implementation does not. Pick one and read its own README for depth; this page gives you the basics of each so you can choose.

## At a glance

|                        | [**Java**](java/index.md) — the original                                                                                      | [**TypeScript**](typescript/index.md) — agent-first rewrite                                                                                                                                                                                                        |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **What it is**         | The mature, full-feature reference CLI.                                                                                        | A newer rewrite focused on programmatic integration.                                                                                                                                                                                                        |
| **Runtime**            | JVM — built with Gradle, run as a `.jar`. Uses the [Trident](https://github.com/tronprotocol/trident) SDK.                     | [Node.js](https://nodejs.org) **20+**.                                                                                                                                                                                                                      |
| **Install**            | `git clone` + `./gradlew build` (see [Setup](java/index.md#setup))                                                            | `npm install -g @tron-walletcli/wallet-cli`                                                                                                                                                                                                                 |
| **How you drive it**   | An **interactive prompt only** — start it, then type commands at `>`.                                                          | **One-shot subcommands** — `wallet-cli <command>` from your shell. Interactive prompts only for secret input.                                                                                                                                               |
| **Command style**      | PascalCase verbs: `RegisterWallet`, `SendCoin`, `GetBalance`. Amounts in **SUN** (1 TRX = 1,000,000 SUN).                      | Noun-verb subcommands: `create`, `tx send`, `account balance`, with `--flags`.                                                                                                                                                                              |
| **Output for scripts** | Human-readable text.                                                                                                           | Stable JSON via `-o json` ([`wallet-cli.result.v1`](typescript/machine-interface.md)) + fixed exit codes (`0`/`1`/`2`).                                                                                                                                        |
| **Config / networks**  | `config.conf` (net type + full node), or `SwitchNetwork` at runtime. Mainnet · Nile · Shasta · custom.                         | `--network` flag / `config` command. CAIP-2 ids with short aliases: `tron:728126428` (`tron`) · `tron:3448148188` (`nile`) · `tron:2494104990` (`shasta`) · `eip155:1` (`ethereum`) · `eip155:11155111` (`sepolia`) · `eip155:56` (`bsc`) · `eip155:97` (`bsc-testnet`).                                                                                                                                                                          |
| **Signing**            | Software keystore · Ledger.                                                                                                    | Encrypted local keystore · Ledger. Secrets enter via stdin/TTY, never argv or dedicated secret env vars.                                                                                                                                                    |
| **Feature scope**      | **The full surface** — wallets and transfers, staking, voting and rewards, governance, contracts, TRC10, and the on-chain exchange. | **The full surface** — HD wallets, TRX/TRC20/TRC10 transfers, staking & delegation, voting & rewards, governance proposals & super-representative operation, contract call/deploy/governance, TRC10 issuance, the on-chain Bancor exchange, multi-sig, GasFree transfers, message signing, and on-chain queries. |
| **Best for**           | People at a terminal who want every TRON capability.                                                                           | Scripting, CI pipelines, and AI agents.                                                                                                                                                                                                                     |
| **Full docs**          | [Java CLI](java/index.md)                                                                                               | [TypeScript CLI](typescript/index.md)                                                                                                                                                                                                                                |

## Java — get a taste

Interactive only. Build it, start the prompt, then type commands:

```console
$ git clone https://github.com/tronprotocol/wallet-cli.git
$ cd wallet-cli && ./gradlew build && cd build/libs
$ java -jar wallet-cli.jar        # opens the interactive prompt
> RegisterWallet 123456           # create a keystore (password 123456)
> Login                           # unlock it
> GetAddress                      # your TRON address
> GetBalance                      # TRX balance
```

Full setup (config.conf, connecting to a node), the complete A–Z command list, and features like GasFree and multi-sig live in **[Java CLI](java/index.md)** — jump to [Setup](java/index.md#setup), [Quickstart](java/index.md#quickstart), [Commands](java/index.md#commands), or [GasFree](java/index.md#contracts-gasfree--chain-data).

## TypeScript — get a taste

Install from npm, then run subcommands directly from your shell:

```console
$ npm install -g @tron-walletcli/wallet-cli
$ wallet-cli create --label main               # prompts for a master password
$ wallet-cli account balance --network tron:3448148188
$ wallet-cli account balance -o json           # one wallet-cli.result.v1 JSON frame
```

Every command has a reference page, and the JSON contract, exit codes, and agent integration are documented in depth. Start at **[TypeScript CLI](typescript/index.md)**, then:

- [Getting started](typescript/guide/getting-started.md) — create a wallet and send your first transaction
- [Command reference](typescript/commands/index.md) — every command, A–Z
- [Machine interface](typescript/machine-interface.md) — JSON envelope, exit codes, script safety

## Which should I use?

- **Scripting, CI, or building an AI agent?** → the [TypeScript version](typescript/index.md) — the JSON envelope and deterministic exit codes exist for exactly this.
- **Working interactively** — one long-running session at a `>` prompt, with the wallet unlocked once for the whole session? → the [Java version](java/index.md).
- **Just sending TRX/tokens or staking from your own machine?** → either works; the TypeScript CLI is the lighter install (`npm install -g`, no build step).
