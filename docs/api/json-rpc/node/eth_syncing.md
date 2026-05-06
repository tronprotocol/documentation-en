# eth_syncing

Node sync status.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getSyncingStatus`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_syncing","params":[],"id":1}'
```

## Response

- If the peer list is empty: returns `false`.
- Otherwise returns a `SyncingResult` object:

| Field | Type | Description |
|---|---|---|
| `startingBlock` | hex | `nodeInfoService.getNodeInfo().getBeginSyncNum()` |
| `currentBlock` | hex | The node's current latest block height |
| `highestBlock` | hex | **Estimated**: `currentBlockNum + max(0, (now - blockTime) / 3000)` (extrapolated using a 3-second average block time) |

The example below is the real response captured from a Nile testnet call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "startingBlock": "0x3fe1dda",
    "currentBlock": "0x3fe1ded",
    "highestBlock": "0x3fe1ded"
  }
}
```

> All three values change in real time with node state. `highestBlock` is extrapolated from local system time, not from the actual highest block height of any peer; it will keep growing even when the network is disconnected.

### Error responses

None.
