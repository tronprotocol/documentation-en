# eth_newBlockFilter

Register a block filter; the hash of each new block is appended to the result queue.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#newBlockFilter`
- Ports: FullNode `8545` / Solidity `8555`

> **The example here must be tested against your own node (e.g. `http://127.0.0.1:8545/jsonrpc`)**: filter state lives in a single fullnode process (`eventFilter2ResultFull` / `eventFilter2ResultSolidity`). Public gateways (such as `nile.trongrid.io`) are usually reverse proxies load-balancing across multiple nodes, so two consecutive requests may land on different nodes — the second request will see the filter ID as nonexistent.

## Request parameters

None (`params: []`).

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_newBlockFilter","params":[],"id":1}'
```

## Response

Filter ID (`0x`-prefixed hex):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0xabc123..." }
```

Behavior:

- On the FullNode port, the filter is fed by latest-block events; on the Solidity port, by solidified-block notifications.
- Expires after 5 minutes without a read.
- The number of block filters alive on a single node is capped by `node.jsonrpc.maxBlockFilterNum` (default 50000).

### Error responses

| Trigger | Code | message |
|---|---|---|
| Existing block filter count ≥ `maxBlockFilterNum` | `-32005` | `exceed max block filters: <N>, try again later` |
