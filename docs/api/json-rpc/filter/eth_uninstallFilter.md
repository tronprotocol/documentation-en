# eth_uninstallFilter

Uninstall a registered filter (log filter or block filter).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#uninstallFilter`
- Ports: FullNode `8545` / Solidity `8555`

> **The example here must be tested against your own node (e.g. `http://127.0.0.1:8545/jsonrpc`)**: filter state lives in a single fullnode process (`eventFilter2ResultFull` / `eventFilter2ResultSolidity`). Public gateways (such as `nile.trongrid.io`) are usually reverse proxies load-balancing across multiple nodes, so two consecutive requests may land on different nodes — the second request will see the filter ID as nonexistent.

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Filter ID (`0x`-prefixed hex) |

```bash
curl -X POST http://127.0.0.1:8545/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_uninstallFilter","params":["0xabc123..."],"id":1}'
```

## Response

Always returns `true` on success:

```json
{ "jsonrpc": "2.0", "id": 1, "result": true }
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| Filter ID does not exist (expired / never registered / belongs to another port) | `-32000` | `filter not found` |
