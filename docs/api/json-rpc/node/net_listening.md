# net_listening

Whether the node is in P2P listening state.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#isListening`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"net_listening","params":[],"id":1}'
```

## Response

Boolean. The check is `nodeInfoService.getNodeInfo().getActiveConnectCount() >= 1`: at least 1 active peer connection counts as listening.

The example below is the real response captured from a Nile testnet call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": true
}
```

### Error responses

None.
