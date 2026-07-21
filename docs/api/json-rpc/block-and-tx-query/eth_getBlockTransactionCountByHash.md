# eth_getBlockTransactionCountByHash

Query the number of transactions in a block by its hash.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockTransactionCountByHash`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | 32-byte block hash |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockTransactionCountByHash","params":["0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c"],"id":1}'
```

## Response

Hex-encoded `block.getTransactionsList().size()`. Returns `null` if the block does not exist.

The example below is the real response captured from the Nile testnet curl above (block `0x3fe1ca0` has 4 transactions):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x4" }
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` does not match `(0x)?[0-9a-fA-F]{64}` | `-32602` | `invalid hash value` |
