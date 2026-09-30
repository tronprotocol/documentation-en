# Contribute to java-tron

Guides for contributing to java-tron, configuring a development environment, understanding CI and the codebase, and following issue, TIP, and network-governance processes.

## Start contributing

1. [Developer guide](java-tron.md) — Contribution and submission rules, branch management, code review, CI requirements, naming conventions, pull-request and commit-message specifications, and conduct.
2. [IntelliJ IDEA configuration](run-in-idea.md) — JDK requirements, source compilation, code-style checks, and running or debugging java-tron.
3. [Development example](demo.md) — Adding a `setPeer` HTTP API, writing tests, running CheckStyle, and submitting a pull request.
4. [CI workflows](workflows.md) — Workflow triggers, PR checks, builds, coverage, integration tests, security checks, reviewer assignment, and local checks.
5. [Issue workflow](issue-workflow.md) — Issue submission and handling process, and label classification.
6. [Network governance](governance.md) — Network-parameter proposal discussion, on-chain submission, Super Representative voting, and implementation.
7. [TIP specification and guidelines](tip-workflow.md) — TIP types, submission and review workflow, statuses, composition, linking rules, and auxiliary files.

## TIPs

- [TRON Improvement Proposals](tips.md) — TIPs indexed by category and status.

## Understand the codebase

- [Core modules](code-structure.md) — Code organization and responsibilities across the Protocol, Common, ChainBase, Consensus, Actuator, Crypto, and Framework modules.
- [ChainBase deep dive](chainbase.md) — Transaction handling, state rollback, persistence, block solidification, and atomicity in ChainBase.
- [P2P network deep dive](network.md) — Peer connection management, block synchronization, and block and transaction broadcast, including limits, validation, and backpressure.
