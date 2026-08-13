# wallet-cli

`wallet-cli` is a command-line wallet for the TRON network; its official repository is
[tronprotocol/wallet-cli](https://github.com/tronprotocol/wallet-cli). It manages keys and accounts
locally and connects to TRON services to query chain data and build, sign, and broadcast
transactions.

The repository provides two implementations:

- **[Java CLI](java-cli.md)** — the original implementation. It provides an interactive REPL for
  people and a non-interactive Standard CLI for scripts using the Java JAR. It has the broadest
  protocol feature coverage, including TRC-10 issuance, the on-chain DEX, and governance proposals.
- **[TypeScript / npm CLI](typescript-cli.md)** — an agent-first Node.js implementation published as
  `@tron-walletcli/wallet-cli`, with grouped commands, deterministic exit codes, and structured JSON
  output. It includes first-class [multi-signature](typescript-cli-multisig.md) and
  [GasFree](typescript-cli-gasfree.md) workflows.

## Compare entry points

Each interface can query account data. The Java CLI accepts an arbitrary address, while the
TypeScript CLI operates on an account already stored in its local wallet:

=== "Java Standard CLI"

    ```bash
    java -jar java/build/libs/wallet-cli.jar --network nile get-account --address TXyz...
    ```

=== "Java REPL"

    ```
    GetAccount TXyz...
    ```

=== "TypeScript / npm CLI"

    ```bash
    wallet-cli account info --network tron:nile
    ```

    This uses the active account. Pass `--account` with an account id, label, or address already
    present in the local wallet to select a different stored account.

## Choose an implementation

| Implementation | Command style | Feature emphasis | Best suited for |
|----------------|---------------|------------------|-----------------|
| [Java CLI](java-cli.md) | Interactive commands such as `GetAccount`, or Standard CLI commands such as `get-account` | Broadest protocol surface, including TRC-10 issuance, DEX, and governance/proposals | Manual operation and Java JAR integrations |
| [TypeScript / npm CLI](typescript-cli.md) | Grouped commands such as `account info` and `tx send` | Core wallet operations, multi-sig, GasFree, local utilities, and a stable machine interface | Automation, CI/CD, structured JSON integrations, and AI agents |

The two implementations have separate installation and runtime requirements. Continue with the
[Java CLI overview](java-cli.md) or the [TypeScript / npm CLI overview](typescript-cli.md). For the
TypeScript implementation's security-sensitive workflows, see [Multi-signature](typescript-cli-multisig.md),
[GasFree](typescript-cli-gasfree.md), and [Signing and Security](typescript-cli-signing.md).
