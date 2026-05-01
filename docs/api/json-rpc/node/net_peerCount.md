# net_peerCount

Number of peers.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getPeerCount`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"net_peerCount","params":[],"id":1}'
```

## Response

Hex-encoded `nodeInfoService.getNodeInfo().getPeerList().size()` (**counts all peers, not only active ones**).

The example below is the real response captured from the Nile testnet curl above (`0x3b` = 59 peers):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x3b"
}
```

> Peer count fluctuates with network topology; subsequent requests may return different values.

### Error responses

None.
