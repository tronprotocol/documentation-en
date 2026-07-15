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
- **HTTP status code**: after a request reaches `JsonRpcServlet`, JSON-RPC business errors are returned with HTTP 200 and an `error` field in the response body. Transport-layer failures can still return non-200 status codes; for example, an oversized request body may be rejected before servlet dispatch.
- **Numeric encoding**: response quantities use `0x`-prefixed hex strings. Block-query selectors additionally accept non-negative decimal heights because `JsonRpcApiUtil.parseBlockNumber` supports both decimal and `0x`-prefixed input.
- **Address encoding**: JSON-RPC state/call/build interfaces accept hexadecimal addresses only: either a 20-byte EVM-style address or a 21-byte Tron address beginning with `41`, with or without `0x`. Base58check (`T...`) is not accepted by `JsonRpcApiUtil.addressCompatibleToByteArray`. Log filters use 20-byte hexadecimal addresses.
- **Call data fields**: `eth_call`, `eth_estimateGas`, and `buildTransaction` accept both `data` and `input`. `input` follows stricter execution-API hex rules (`0x` prefix, even length; empty string means empty bytes). `data` remains lenient for backward compatibility.
- **Block tags**: among the common `latest` / `earliest` / `pending` / `finalized` / `safe`, **only a few methods support these tags**:
    - Block-query methods such as `eth_getBlockByNumber` and `eth_getBlockReceipts` accept `latest` / `earliest` / `finalized`; `pending` and `safe` are explicitly unsupported and throw `-32602 TAG pending not supported` or `-32602 TAG safe not supported`.
    - `eth_getBalance` / `eth_getStorageAt` / `eth_getCode` / `eth_call` **only support `latest`**; `earliest` / `pending` / `finalized` / `safe` raise `-32602 TAG [earliest | pending | finalized | safe] not supported`, and a specific height raises `-32602 QUANTITY not supported, just support TAG as latest`.
    - `eth_newFilter` does not support `finalized` (raises `-32602 invalid block range params`), nor `pending` / `safe` (raises the corresponding `TAG ... not supported`).

## Error responses

<!-- BEGIN GENERATED JSON-RPC ERROR CATALOG -->
### JSON-RPC error catalog

Catalog IDs and retry classifications are defined by `openrpc.json` under `x-tron-error-model`. They are machine-readable documentation classifications, not fields returned by java-tron on the wire.

`Automatic retry` maps exactly to catalog `retryable`: only `Yes` permits automatic replay of the same logical operation. Conditional retry classes remain `No` until the `Scope / action` precondition is satisfied.

Evaluate executable `sharedCatalogIds` matches first, then restrict method-declared candidates through the method's `x-tron-error-catalog`. `sourceException` is source metadata, not a wire field. If reused codes such as `-32000` or `-32005` still identify multiple candidates, classify the response as `UNKNOWN` and do not retry automatically.

| Catalog ID | Wire signal | Source declaration | Meaning | Automatic retry | Retry class | Scope / action |
|---|---|---|---|---|---|---|
| `JSON_RPC_PARSE_ERROR` | `error.code` = `-32700` | — | The request body is not valid JSON. | No | `AFTER_REQUEST_REBUILD` | Correct the JSON syntax or reduce constructs that exceed parser limits before resubmitting. |
| `JSON_RPC_INVALID_REQUEST` | `error.code` = `-32600` | `JsonRpcInvalidRequestException` | The JSON-RPC protocol structure is invalid or method-level request or contract validation failed. | No | `AFTER_REQUEST_REBUILD` | Correct the JSON-RPC envelope, invalid batch item, method request, or contract parameters before resubmitting. |
| `JSON_RPC_METHOD_NOT_FOUND` | `error.code` = `-32601` | `JsonRpcMethodNotFoundException` | The requested method is unavailable or unsupported on this node/port. | No | `AFTER_STATE_CHANGE` | Use a compatible node/port, or wait for node availability or configuration to change. |
| `JSON_RPC_INVALID_PARAMS` | `error.code` = `-32602` | `JsonRpcInvalidParamsException` | Parameters could not be bound to the method signature or failed method validation. | No | `AFTER_REQUEST_REBUILD` | Correct parameter count, types, formats, block tags, or ranges before resubmitting. |
| `JSON_RPC_SERVLET_INTERNAL_ERROR` | `error.code` = `-32603` + `error.message` = `Internal error` | — | The JSON-RPC servlet caught an unexpected fallback exception. | No | `UNKNOWN` | Inspect node logs or use another healthy node; do not retry automatically from this fallback classification. |
| `JSON_RPC_RESPONSE_TOO_LARGE` | `error.code` = `-32003` + `error.message` starts with `Response exceeds the limit of ` | — | The encoded JSON-RPC response exceeds maxResponseSize. | No | `AFTER_REQUEST_REBUILD` | Narrow or split the query so the encoded response fits maxResponseSize. |
| `JSON_RPC_BATCH_TOO_LARGE` | `error.code` = `-32005` + `error.message` starts with `Batch size ` | — | The request batch contains more entries than maxBatchSize permits. | No | `AFTER_REQUEST_REBUILD` | Split the batch so each request contains no more than maxBatchSize entries. |
| `JSON_RPC_FILTER_LIMIT_EXCEEDED` | `error.code` = `-32005` | `JsonRpcExceedLimitException` | The node has reached its active filter limit. | No | `AFTER_STATE_CHANGE` | Retry only after filter capacity is released, or use another node. |
| `JSON_RPC_TOO_MANY_RESULTS` | `error.code` = `-32005` | `JsonRpcTooManyResultException` | The log query would return more results than the node permits. | No | `AFTER_REQUEST_REBUILD` | Narrow the block range, addresses, or topics before resubmitting. |
| `JSON_RPC_UNDERLYING_INTERNAL_ERROR` | `error.code` = `-32001` + fallback match | `JsonRpcInternalException`; message metadata `<underlying exception message>` | Chain identity lookup failed with an underlying exception message. | No | `UNKNOWN` | Inspect the returned message and node context; do not retry automatically without a specific transient cause. |
| `JSON_RPC_INTERNAL_ERROR` | `error.code` = `-32000` | `JsonRpcInternalException` | The method raised a java-tron JSON-RPC internal error. | No | `UNKNOWN` | Inspect error.message and node logs; do not retry automatically without a more specific classification. |
| `JSON_RPC_ITEM_NOT_FOUND` | `error.code` = `-32000` | `ItemNotFoundException` | A requested filter, block item, or cached item was not found. | No | `AFTER_STATE_CHANGE` | Recreate a missing filter, wait for the item to become available, or use a node that has the requested data. |
| `JSON_RPC_BAD_ITEM` | `error.code` = `-32000` | `BadItemException` | Log processing encountered an invalid underlying item. | No | `UNKNOWN` | Inspect the invalid underlying item and query context; do not retry automatically. |
| `JSON_RPC_EXECUTION_ERROR` | `error.code` = `-32000` | `ExecutionException` | Asynchronous log-query execution failed. | No | `UNKNOWN` | Inspect the asynchronous execution failure and node logs before deciding whether to try again. |
| `JSON_RPC_INTERRUPTED` | `error.code` = `-32000` | `InterruptedException` | Log-query execution declared InterruptedException, but the wire response cannot distinguish it safely from other -32000 failures. | No | `UNKNOWN` | The current wire response is ambiguous with other -32000 failures; do not retry automatically. |
| `JSON_RPC_RATE_LIMITED` | HTTP 200 outside the JSON-RPC envelope + `$.Error` contains `lack of computing resources` | — | The shared servlet rate limiter rejected the request before a JSON-RPC envelope was written. | Yes | `SAFE_WITH_BACKOFF` | Retry automatically with exponential backoff and jitter; no Retry-After header is returned. |
| `JSON_RPC_REQUEST_TOO_LARGE` | HTTP 413 outside the JSON-RPC envelope | — | The HTTP request body exceeds node.jsonrpc.maxMessageSize before servlet dispatch. | No | `AFTER_REQUEST_REBUILD` | Reduce the HTTP request body before resubmitting. |
<!-- END GENERATED JSON-RPC ERROR CATALOG -->

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
| `maxBlockRange` | 5000 | Per-request `[fromBlock, toBlock]` span allowed for `eth_getLogs` and `eth_getFilterLogs` |
| `maxAddressSize` | 1000 | Address count allowed in one filter request |
| `maxSubTopics` | 1000 | OR-candidate count allowed in a single topic slot |
| `maxBlockFilterNum` | 50000 | Max block filters alive concurrently on a single node |
| `maxLogFilterNum` | 20000 | Max log filters alive concurrently on a single node |
| `maxBatchSize` | 100 | Max JSON-RPC batch request size |
| `maxResponseSize` | 26214400 | Max response body size in bytes (25 MiB) |
| `maxMessageSize` | 4194304 | Max JSON-RPC request body size in bytes (about 4 MiB); independent from HTTP/gRPC limits |

## Transaction build

| Method | Description |
|---|---|
| [`buildTransaction`](tx-build/buildTransaction.md) | Build an unsigned transaction (FullNode only; TRX transfer / TRC-10 transfer / contract deploy / contract trigger) |

> JSON-RPC does not provide a broadcast endpoint; after signing, send via HTTP [`/wallet/broadcasttransaction`](../http/tx-build-and-broadcast/broadcasttransaction.md) or [`/wallet/broadcasthex`](../http/tx-build-and-broadcast/broadcasthex.md).

## Compatibility stub methods

Tron uses DPoS consensus and has no PoW work, uncle, or miner concepts. The following methods exist only to be compatible with standard ETH clients and always return constants:

| Method | Returns | Description |
|---|---|---|
| [`eth_coinbase`](stub/eth_coinbase.md) | The configured etherbase address | Throws `-32000 etherbase must be explicitly specified` if not configured |
| [`eth_accounts`](stub/eth_accounts.md) | `[]` | Nodes don't custody private keys |
| [`eth_getWork`](stub/eth_getWork.md) | `[blockHash, null, null]` | Current block hash + two nulls |
