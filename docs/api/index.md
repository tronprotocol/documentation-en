# java-tron APIs

A java-tron node exposes three API surfaces. They share most underlying functionality but differ in transport, encoding, and ecosystem fit. Pick by client environment first; only fall back to "what each one supports" when you need a method the others don't have.

## Pick one

| Need | Recommended | Why |
|---|---|---|
| Calling from a browser, mobile, or any HTTP client | **HTTP API** | Plain `POST` + JSON, no codegen, the broadest method coverage on the node |
| Reusing existing Ethereum tooling (web3.js, ethers.js, MetaMask, Hardhat, Foundry) | **JSON-RPC API** | Implements the `eth_*` / `net_*` / `web3_*` method set so EVM tools work unchanged |
| Server-to-server in a typed language (Java, Go, Rust, C++) where latency or throughput matters | **gRPC API** | Persistent HTTP/2 connections, protobuf encoding, generated stubs |

If you're undecided: start with **HTTP API**. It has the smallest setup cost and the widest method coverage. Switch to JSON-RPC only when EVM-tool compatibility is the goal, and to gRPC only when profiling shows the HTTP path is the bottleneck.

Notes:

- All three connect to the same underlying database. Choosing one doesn't restrict what data you can read — it restricts which method names and shapes are available.
- The Solidity-suffixed variant of each API serves only solidified data (i.e. blocks that have crossed the irreversibility threshold). Use it when you need finality at the cost of ~1 minute of staleness.

## Reference indexes

- [HTTP API reference](http/index.md) — endpoints under `/wallet/*`, organized by feature
- [JSON-RPC API reference](json-rpc/index.md) — `eth_*` / `net_*` / `web3_*` methods plus the Tron-specific `buildTransaction`
- [gRPC API reference](rpc/index.md) — `protocol.Wallet` / `protocol.WalletSolidity` methods
