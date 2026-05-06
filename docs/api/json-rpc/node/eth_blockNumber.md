# eth_blockNumber

Latest block height.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getLatestBlockNum`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## Response

Hex-encoded `wallet.getNowBlock().getBlockHeader().getRawData().getNumber()`. The Solidity port returns the height of the latest solidified block.

The example below is the real response captured from a Nile testnet call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x3fe1dec"
}
```

> The value advances with every new block; subsequent requests will return higher values.

### Error responses

None.
