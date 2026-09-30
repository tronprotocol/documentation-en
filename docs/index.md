# java-tron Documentation

java-tron is the official Java implementation of the TRON network client, developed and maintained by the TRON protocol team and fully open source. It implements the complete TRON mainnet protocol, including DPoS consensus, the TVM, the account and resource models, smart contracts, the decentralized exchange, and multi-signature permission management — the foundational software for running full nodes, participating in Super Representative elections, deploying contracts, and building DApps.

This documentation is written for java-tron node operators, protocol researchers, DApp developers, and core contributors. It covers the full path from node deployment, network connectivity, and API usage to protocol mechanics and source contribution. Source and releases: [github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron).

## Choose your entry point

<div class="grid cards" markdown>

-   __Getting Started__

    ---

    New to java-tron or the TRON protocol? Begin with the guided learning sequence, then use the consensus overview and glossary as references.

    - [Get Started](getting_started/index.md)
    - [Hands-on Getting Started Guide](getting_started/getting_started_with_javatron.md)
    - [TRON Consensus (DPoS)](mechanism-algorithm/dpos.md)
    - [Glossary](glossary.md)

-   __Run a Node__

    ---

    Guides for java-tron deployment, configuration, connectivity, logging, monitoring, storage, backup, and maintenance.

    - [Node Operations Overview](using_javatron/index.md)
    - [Deploy java-tron](using_javatron/installing_javatron.md)
    - [Node Configuration](using_javatron/configuration.md)
    - [Node Logging](using_javatron/logging.md)
    - [Node Monitoring](using_javatron/metrics.md)
    - [Upgrade to a New Version](releases/upgrade-instruction.md)
    - [Private Network](using_javatron/private_network.md)

-   __DApp Development__

    ---

    Smart-contract development, java-tron APIs, and command-line tools for building DApps on TRON.

    - [Build DApps with java-tron](contracts/index.md)
    - [Choose an API](api/index.md)
    - [HTTP API](api/http/index.md)
    - [JSON-RPC API](api/json-rpc/index.md)
    - [gRPC API](api/rpc/index.md)
    - [Smart Contracts](contracts/contract.md)
    - [wallet-cli](clients/wallet-cli/index.md)

-   __Contribute to Core__

    ---

    Guides for contributing to java-tron, configuring a development environment, understanding CI and the codebase, and following issue, TIP, and network-governance processes.

    - [Contributor Overview](developers/index.md)
    - [Developer Guide](developers/java-tron.md)
    - [TIPs Workflow](developers/tip-workflow.md)
    - [Configure the IDE](developers/run-in-idea.md)
    - [Core Modules](developers/code-structure.md)

</div>

## Browse by topic

- __[Get started](getting_started/index.md)__ — A hands-on path for creating a TRON account, starting and verifying a java-tron node, and sending transactions or querying chain data with wallet-cli or cURL
- __[Operate a node](using_javatron/index.md)__ — Guides for java-tron deployment, configuration, connectivity, logging, monitoring, storage, backup, and maintenance
- __[API reference](api/index.md)__ — Guidance for choosing among the HTTP, JSON-RPC, and gRPC interfaces, plus reference indexes and machine-readable definitions
- __[wallet-cli](clients/wallet-cli/index.md)__ — A command-line wallet for TRON and selected EVM networks — interactive in Java, agent-first in TypeScript
- __[Understand the protocol](mechanism-algorithm/index.md)__ — Documentation about TRON consensus, Super Representatives, accounts and signatures, network resources, system contracts, and account permissions
- __[Contribute to java-tron](developers/index.md)__ — Guides for contributing to java-tron, configuring a development environment, understanding CI and the codebase, and following issue, TIP, and network-governance processes
- __[Build DApps](contracts/index.md)__ — Smart-contract development and developer tools for building DApps on TRON
- __[Releases](releases/index.md)__ — Node upgrade procedures, release-package signature verification, and version history
- __[Appendix](glossary.md)__ — Definitions of common TRON and java-tron terms

## Other resources

- [TRON Whitepaper](https://tron.network/static/doc/white_paper_v_2_1.pdf) — Official document on TRON's protocol design and vision
- [TRON Improvement Proposals (TIPs)](https://github.com/tronprotocol/tips) — Repository for submitting, discussing, and archiving protocol evolution proposals
- [TRON Developer Hub](https://developers.tron.network/) — DApp developer documentation, SDKs, and tutorials
- [TRON Official Site](https://tron.network/index?lng=en) — Project updates, ecosystem partners, and community entry points

## Documentation source of truth

This English repository ([`documentation-en`](https://github.com/tronprotocol/documentation-en)) is the authoritative source for java-tron documentation. The Chinese documentation ([`documentation-zh`](https://github.com/tronprotocol/documentation-zh)) is a translation that follows it. When the two diverge, the English version takes precedence; content changes should be made against the English source first and then propagated to the translation.
