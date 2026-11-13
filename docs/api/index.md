# java-tron APIs

A java-tron node exposes three API surfaces. They share most underlying functionality but differ in transport, encoding, and ecosystem fit. Pick by client environment first; only fall back to "what each one supports" when you need a method the others don't have.

## Pick one

| Need | Recommended | Why |
|---|---|---|
| Calling from a browser, mobile, or any HTTP client | **HTTP API** | `POST` / `GET` (partial support), no codegen, the broadest method coverage on the node |
| Server-to-server in a typed language (Java, Go, Rust, C++) where latency or throughput matters | **gRPC API** | Persistent HTTP/2 connections, protobuf encoding, client code can be auto-generated from `.proto` with no hand-written networking |
| Using Ethereum-style queries and contract calls through clients such as web3.js or ethers.js | **JSON-RPC API** | Supports a subset of `eth_*` / `net_*` / `web3_*` methods |

If you're undecided: start with **HTTP API**. It has the smallest setup cost and the widest method coverage. Use JSON-RPC when its supported Ethereum-style queries and calls fit your client, and consider gRPC when profiling shows the HTTP path is the bottleneck.

Notes:

- All three connect to the same underlying database. Choosing one doesn't restrict what data you can read — it restricts which method names and shapes are available.
- The Solidity-suffixed variant of each API serves only solidified data (i.e. blocks that have crossed the irreversibility threshold). Use it when you need finality at the cost of ~1 minute of staleness.

## Reference indexes

- [HTTP API reference](http/index.md) — endpoints under `/wallet/*` and `/walletsolidity/*` (partial support), organized by feature
- [gRPC API reference](rpc/index.md) — `protocol.Wallet` / `protocol.WalletSolidity` (partial support) methods, organized by feature
- [JSON-RPC API reference](json-rpc/index.md) — `eth_*` / `net_*` / `web3_*` methods plus the Tron-specific `buildTransaction`, organized by feature
- [Machine-readable API definitions](interface-definitions.md) — OpenAPI for HTTP and OpenRPC for JSON-RPC
