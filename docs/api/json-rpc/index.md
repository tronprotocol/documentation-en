# java-tron JSON-RPC API documentation

This directory holds request / response documentation for the JSON-RPC interfaces under `framework/src/main/java/org/tron/core/services/jsonrpc/`. Each method has its own markdown file, named after the `method` field (e.g. `eth_blockNumber` → `eth_blockNumber.md`).

## Services and default ports

| Service | Default port | Enable switch | Data source |
|---|---|---|---|
| FullNode JSON-RPC | `8545` | `node.jsonrpc.httpFullNodeEnable` | Full database (the latest block is visible) |
| Solidity JSON-RPC | `8555` | `node.jsonrpc.httpSolidityEnable` | Solidified data only |

Ports can be overridden via `node.jsonrpc.httpFullNodePort` / `httpSolidityPort` (see the `jsonrpc {}` block in `framework/src/main/resources/config.conf`).

> **Disabled by default**: every switch in the `jsonrpc {}` block of `config.conf` is commented out; in `Args` both `httpFullNodeEnable` and `httpSolidityEnable` are `false` (see `Args.java`). You must explicitly set `httpFullNodeEnable = true` / `httpSolidityEnable = true` in the config to start them with the node. The Solidity JSON-RPC service additionally requires the current process to be a FullNode (not a standalone SolidityNode process; see `JsonRpcServiceOnSolidity.java`).

The URL path is always `/jsonrpc` (see `FullNodeJsonRpcHttpService.java`).

## Protocol conventions

- **Transport**: `POST` only; the request body is in [JSON-RPC 2.0](https://www.jsonrpc.org/specification) format: `{"jsonrpc":"2.0","method":"...","params":[...],"id":1}`.
- **HTTP status code**: always 200; business errors are conveyed via the `error` field in the response body (see `JsonRpcServlet.java`).
- **Numeric encoding**: all numbers (block number, balance, gas, timestamp, etc.) use `0x`-prefixed hex strings; null values map to `0x` or `0x0`.
- **Address encoding**: JSON-RPC interfaces accept `0x`-prefixed 20-byte hex addresses by default; base58check is also accepted (internally converted by `JsonRpcApiUtil.addressCompatibleToByteArray`).
- **Block tags**: among the common `latest` / `earliest` / `pending` / `finalized`, **only a few methods support these tags**:
    - Block-query methods such as `eth_getBlockByNumber` and `eth_getBlockReceipts` accept `latest` / `earliest` / `finalized`; `pending` is explicitly unsupported and throws `-32602 TAG pending not supported`.
    - `eth_getBalance` / `eth_getStorageAt` / `eth_getCode` / `eth_call` **only support `latest`**; `earliest` / `pending` / `finalized` raise `-32602 TAG [earliest | pending | finalized] not supported`, and a specific height raises `-32602 QUANTITY not supported, just support TAG as latest`.
    - `eth_newFilter` does not support `finalized` (raises `-32602 invalid block range params`).

## Error responses

JSON-RPC protocol errors use `error.code` / `error.message`. Business exceptions map as follows (see annotations on `TronJsonRpc.java` + `JsonRpcErrorResolver.java`):

| Code | Exception class | Meaning |
|---|---|---|
| `-32600` | `JsonRpcInvalidRequestException` | Request body is invalid or contract validation failed (e.g. `eth_call`'s `params[1]` is neither a tag string nor a `{blockNumber/blockHash}` object, or `ContractValidateException`) |
| `-32601` | `JsonRpcMethodNotFoundException` | Method does not exist or is unavailable on the current node type (Solidity nodes disable `buildTransaction`, plus a set of always-unsupported methods) |
| `-32602` | `JsonRpcInvalidParamsException` | Invalid parameters (wrong hash length, wrong address format, unsupported block tag, etc.) |
| `-32000` | `JsonRpcInternalException` / `ItemNotFoundException` / `BadItemException` / `ExecutionException` / `InterruptedException` | Server-side internal error (block does not exist, VM execution fails, `etherbase` not configured, filter not found, lite fullnode pruned, etc.) |
| `-32005` | `JsonRpcExceedLimitException` / `JsonRpcTooManyResultException` | Limit hit (`eth_newBlockFilter` exceeded `maxBlockFilterNum`, or `eth_getLogs` results exceed `LogBlockQuery.MAX_RESULT=10000`; `maxBlockRange` overflow throws `-32602` `exceed max block range` separately) |

Example error response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "invalid hash value",
    "data": "{}"
  }
}
```

> **Note**: the `disabledApi` config item **does not affect JSON-RPC** (see the comment "but not jsonrpc" in `config.conf`). To disable JSON-RPC, turn off the corresponding `httpFullNodeEnable` / `httpSolidityEnable`.

## Node info / chain identity

| Method | Description |
|---|---|
| [`web3_clientVersion`](node/web3_clientVersion.md) | Client version string |
| [`web3_sha3`](node/web3_sha3.md) | Keccak-256 hash |
| [`net_version`](node/net_version.md) | Network ID (same as `eth_chainId`) |
| [`net_listening`](node/net_listening.md) | Whether listening on P2P |
| [`net_peerCount`](node/net_peerCount.md) | Number of peers |
| [`eth_chainId`](node/eth_chainId.md) | chainId (last 4 bytes of the genesis block hash) |
| [`eth_protocolVersion`](node/eth_protocolVersion.md) | Protocol version of the current block header |
| [`eth_syncing`](node/eth_syncing.md) | Sync status |
| [`eth_blockNumber`](node/eth_blockNumber.md) | Latest block height |
| [`eth_gasPrice`](node/eth_gasPrice.md) | Current energy unit price (sun) |

## Block / transaction query

| Method | Description |
|---|---|
| [`eth_getBlockByHash`](block-and-tx-query/eth_getBlockByHash.md) | Query a block by hash |
| [`eth_getBlockByNumber`](block-and-tx-query/eth_getBlockByNumber.md) | Query a block by height / tag |
| [`eth_getBlockTransactionCountByHash`](block-and-tx-query/eth_getBlockTransactionCountByHash.md) | Block transaction count (by hash) |
| [`eth_getBlockTransactionCountByNumber`](block-and-tx-query/eth_getBlockTransactionCountByNumber.md) | Block transaction count (by height) |
| [`eth_getTransactionByHash`](block-and-tx-query/eth_getTransactionByHash.md) | Query a transaction by txid |
| [`eth_getTransactionByBlockHashAndIndex`](block-and-tx-query/eth_getTransactionByBlockHashAndIndex.md) | Query a transaction by block hash + index |
| [`eth_getTransactionByBlockNumberAndIndex`](block-and-tx-query/eth_getTransactionByBlockNumberAndIndex.md) | Query a transaction by block height + index |
| [`eth_getTransactionReceipt`](block-and-tx-query/eth_getTransactionReceipt.md) | Query a receipt by txid |
| [`eth_getBlockReceipts`](block-and-tx-query/eth_getBlockReceipts.md) | Receipt list for an entire block |

## Account state

| Method | Description |
|---|---|
| [`eth_getBalance`](account/eth_getBalance.md) | Account TRX balance (sun) |
| [`eth_getStorageAt`](account/eth_getStorageAt.md) | Contract storage slot |
| [`eth_getCode`](account/eth_getCode.md) | Contract runtime bytecode |

## Smart contract calls

| Method | Description |
|---|---|
| [`eth_call`](smart-contract/eth_call.md) | Read-only contract call |
| [`eth_estimateGas`](smart-contract/eth_estimateGas.md) | Estimate energy consumption |

## Logs / filters

| Method | Description |
|---|---|
| [`eth_getLogs`](filter/eth_getLogs.md) | One-shot log query |
| [`eth_newFilter`](filter/eth_newFilter.md) | Register a log filter |
| [`eth_newBlockFilter`](filter/eth_newBlockFilter.md) | Register a new-block filter |
| [`eth_uninstallFilter`](filter/eth_uninstallFilter.md) | Uninstall a filter |
| [`eth_getFilterChanges`](filter/eth_getFilterChanges.md) | Pull and drain filter increments |
| [`eth_getFilterLogs`](filter/eth_getFilterLogs.md) | Pull a log filter's full set (without draining) |

Filter-related defaults (see the `jsonrpc {}` block in `config.conf`):

| Config item | Default | Meaning |
|---|---|---|
| `maxBlockRange` | 5000 | Per-request `[fromBlock, toBlock]` span allowed for `eth_getLogs` |
| `maxSubTopics` | 1000 | OR-candidate count allowed in a single topic slot |
| `maxBlockFilterNum` | 50000 | Max block filters alive concurrently on a single node |

## Transaction build

| Method | Description |
|---|---|
| [`buildTransaction`](tx-build/buildTransaction.md) | Build an unsigned transaction (FullNode only; TRX transfer / TRC10 transfer / contract deploy / contract trigger) |

> JSON-RPC does not provide a broadcast endpoint; after signing, send via HTTP [`/wallet/broadcasttransaction`](../http/tx-build-and-broadcast/broadcasttransaction.md) or [`/wallet/broadcasthex`](../http/tx-build-and-broadcast/broadcasthex.md).

## Compatibility stub methods

Tron uses DPoS consensus and has no PoW work, uncle, or miner concepts. The following methods exist only to be compatible with standard ETH clients and always return constants:

| Method | Returns | Description |
|---|---|---|
| [`eth_coinbase`](stub/eth_coinbase.md) | The configured etherbase address | Throws `-32000 etherbase must be explicitly specified` if not configured |
| [`eth_accounts`](stub/eth_accounts.md) | `[]` | Nodes don't custody private keys |
| [`eth_getWork`](stub/eth_getWork.md) | `[blockHash, null, null]` | Current block hash + two nulls |
