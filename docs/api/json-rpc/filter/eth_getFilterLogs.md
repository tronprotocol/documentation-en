# eth_getFilterLogs

Re-execute an `eth_getLogs`-equivalent query against the filter's current `[fromBlock, toBlock]` and return the **full** result (does **not** consume the queue, does **not** reset the expiration timer; semantically equivalent to running the filter as a saved query).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getFilterLogs`
- Ports: FullNode `8545` / Solidity `8555`

> **The example here must be tested against your own node (e.g. `http://127.0.0.1:8545/jsonrpc`)**: filter state lives in a single fullnode process (`eventFilter2ResultFull` / `eventFilter2ResultSolidity`). Public gateways (such as `nile.trongrid.io`) are usually reverse proxies load-balancing across multiple nodes, so two consecutive requests may land on different nodes — the second request will see the filter ID as nonexistent.

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Log filter ID (returned by `eth_newFilter`; block filter IDs are not accepted) |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getFilterLogs","params":["0xabc123..."],"id":1}'
```

## Response

Array of `LogFilterElement` (fields described in [`eth_getLogs`](eth_getLogs.md)).

### Error responses

| Trigger | Code | message |
|---|---|---|
| Filter ID does not exist / has expired / belongs to a block filter or another port | `-32000` | `filter not found` |
| Hit count exceeds the limit | `-32005` | passes through `JsonRpcTooManyResultException` message |
| Node is a lite fullnode and the queried block has been pruned | `-32000` | passes through `BadItemException` / `ItemNotFoundException` message |
