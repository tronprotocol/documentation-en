# eth_getFilterChanges

Pull a filter's incremental results since the last read, **draining the queue and resetting the expiration timer**.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getFilterChanges`
- Ports: FullNode `8545` / Solidity `8555`

> **The example here must be tested against your own node (e.g. `http://127.0.0.1:8545/jsonrpc`)**: filter state lives in a single fullnode process (`eventFilter2ResultFull` / `eventFilter2ResultSolidity`). Public gateways (such as `nile.trongrid.io`) are usually reverse proxies load-balancing across multiple nodes, so two consecutive requests may land on different nodes — the second request will see the filter ID as nonexistent.

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Filter ID (`0x`-prefixed hex), returned by `eth_newFilter` or `eth_newBlockFilter` |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getFilterChanges","params":["0xabc123..."],"id":1}'
```

## Response

The return type depends on the filter kind:

- block filter → array of block hash strings (`0x`-prefixed 32-byte hex)
- log filter → array of `LogFilterElement` (fields described in [`eth_getLogs`](eth_getLogs.md))

After the call, the queue is drained and the expiration timer is reset to 5 minutes.

```json
{ "jsonrpc": "2.0", "id": 1, "result": [
  "0x000000000048d3198a657ce15a8c80b66db8de58e3df9d5612eb1d80a98e4cee",
  "0x000000000048d31a..."
]}
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| Filter ID does not exist / has expired / belongs to another port | `-32000` | `filter not found` |
