# eth_getBlockTransactionCountByNumber

Query the number of transactions in a block by height or tag.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockTransactionCountByNumber`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Block height (hex) or tag (`latest` / `earliest` / `finalized`; `pending` and `safe` are explicitly unsupported) |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockTransactionCountByNumber","params":["0x3fe1ca0"],"id":1}'
```

## Response

Hex-encoded transaction count. Returns `null` if the block does not exist.

The example below is the real response captured from the Nile testnet curl above (block `0x3fe1ca0` has 4 transactions):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x4" }
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` is `pending` or `safe` | `-32602` | `TAG pending not supported` or `TAG safe not supported` |
| `params[0]` is neither valid hex nor a valid tag | `-32602` | `invalid block number` |
