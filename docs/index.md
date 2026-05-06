# java-tron Documentation

java-tron is the official Java implementation of the TRON network client, developed and maintained by the TRON protocol team and fully open source. It implements the complete TRON mainnet protocol, including DPoS consensus, the TVM, the account and resource models, smart contracts, the decentralized exchange, and multi-signature permission management — the foundational software for running full nodes, participating in Super Representative elections, deploying contracts, and building DApps.

This documentation is written for java-tron node operators, protocol researchers, DApp developers, and core contributors. It covers the full path from node deployment, network connectivity, and API usage to protocol mechanics and source contribution. Source and releases: [github.com/tronprotocol/java-tron](https://github.com/tronprotocol/java-tron).

## Choose your entry point

<div class="grid cards" markdown>

-   __Getting Started__

    ---

    First time with java-tron or the TRON protocol? Start here.

    - [Getting Started Guide](getting_started/getting_started_with_javatron.md)
    - [TRON Consensus (DPoS)](mechanism-algorithm/dpos.md)
    - [Glossary](glossary.md)

-   __Run a Node__

    ---

    Operations guide for deploying, monitoring, and maintaining java-tron nodes.

    - [Deploy java-tron](using_javatron/installing_javatron.md)
    - [Node Monitoring](using_javatron/metrics.md)
    - [Upgrade to a New Version](releases/upgrade-instruction.md)
    - [Private Network](using_javatron/private_network.md)

-   __DApp Development__

    ---

    Build applications against the HTTP, gRPC, and JSON-RPC interfaces exposed by java-tron.

    - [HTTP API](api/http/index.md)
    - [JSON-RPC API](api/json-rpc/index.md)
    - [Smart Contracts](contracts/contract.md)
    - [wallet-cli](clients/wallet-cli.md)

-   __Contribute to Core__

    ---

    Modify java-tron source, submit TIPs, and participate in protocol evolution.

    - [Developer Guide](developers/java-tron.md)
    - [TIPs Workflow](developers/tips.md)
    - [Configure the IDE](developers/run-in-idea.md)
    - [Core Modules](developers/code-structure.md)

</div>

## Browse by topic

- __[Using java-tron](using_javatron/installing_javatron.md)__ — Deployment, backup and restore, lite node, private network, event subscription, database configuration, node monitoring, maintenance tooling
- __[API](api/http/index.md)__ — HTTP, gRPC, JSON-RPC
- __[Core Protocol](mechanism-algorithm/dpos.md)__ — DPoS consensus, Super Representatives, account model, resource model, smart contracts, system contracts, decentralized exchange, account permission management
- __[For java-tron Developers](developers/java-tron.md)__ — Developer guide, TIPs workflow, issue workflow, governance workflow, IDE configuration, development examples, core modules
- __[For DApp Developers](contracts/tools.md)__ — Development tooling
- __[Clients](clients/wallet-cli.md)__ — wallet-cli
- __[Releases](releases/upgrade-instruction.md)__ — Deployment manual for new versions, integrity check, release history
- __[Appendix](glossary.md)__ — Glossary

## Other resources

- [TRON Whitepaper](https://tron.network/static/doc/white_paper_v_2_1.pdf) — Official document on TRON's protocol design and vision
- [TRON Improvement Proposals (TIPs)](https://github.com/tronprotocol/tips) — Repository for submitting, discussing, and archiving protocol evolution proposals
- [TRON Developer Hub](https://developers.tron.network/) — DApp developer documentation, SDKs, and tutorials
- [TRON Official Site](https://tron.network/index?lng=en) — Project updates, ecosystem partners, and community entry points
