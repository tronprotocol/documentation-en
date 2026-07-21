# eth_newFilter

Register a log filter; subsequently use [`eth_getFilterChanges`](eth_getFilterChanges.md) to pull increments and [`eth_getFilterLogs`](eth_getFilterLogs.md) to pull the full set.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#newFilter`
- Ports: FullNode `8545` / Solidity `8555`

> **The example here must be tested against your own node (e.g. `http://127.0.0.1:8545/jsonrpc`)**: filter state lives in a single fullnode process (`eventFilter2ResultFull` / `eventFilter2ResultSolidity`). Public gateways (such as `nile.trongrid.io`) are usually reverse proxies load-balancing across multiple nodes, so two consecutive requests may land on different nodes — the second request will see the filter ID as nonexistent.

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | object | yes | `FilterRequest` (fields described in [`eth_getLogs`](eth_getLogs.md)). **The `finalized`, `pending`, and `safe` tags are not accepted** |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_newFilter","params":[{"fromBlock":"latest","address":"0x4112ab345..."}],"id":1}'
```

## Response

Filter ID (`0x`-prefixed hex string):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x55b2af16ed1f4f3a..." }
```

Behavior:

- The FullNode port stores filters in `eventFilter2ResultFull`; the Solidity port stores them in `eventFilter2ResultSolidity`. The two are mutually invisible.
- When the node produces / solidifies blocks, matching logs are asynchronously appended to the filter's result queue.
- **Expires after 5 minutes without a read** (`getFilterChanges` / `getFilterLogs`) (`EXPIRE_SECONDS = 300`); subsequent access throws `-32000 filter not found`.
- The number of log filters alive on a single node is capped by `node.jsonrpc.maxLogFilterNum` (default 20000).

### Error responses

| Trigger | Code | message |
|---|---|---|
| Existing log filter count >= `maxLogFilterNum` | `-32005` | `exceed max log filters: <N>, try again later` |
| `fromBlock` or `toBlock` is `finalized` | `-32602` | `invalid block range params` |
| `fromBlock` or `toBlock` is `pending` or `safe` | `-32602` | `TAG pending not supported` or `TAG safe not supported` |
| Other `FilterRequest` validation failures | `-32602` | passes through `LogFilterWrapper` validation message |
