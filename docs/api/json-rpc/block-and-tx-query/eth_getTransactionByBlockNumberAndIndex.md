# eth_getTransactionByBlockNumberAndIndex

Query a transaction by block height + in-block index.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTransactionByBlockNumberAndIndex`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Non-negative block height (`0x`-prefixed hex or decimal) or tag (`latest` / `earliest` / `finalized`; `pending` and `safe` are explicitly unsupported) |
| `params[1]` | string | yes | In-block transaction index, hex-encoded |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionByBlockNumberAndIndex","params":["0x3fe1ca0","0x0"],"id":1}'
```

## Response

`TransactionResult` (fields described in [`eth_getTransactionByHash`](eth_getTransactionByHash.md)); returns `null` if the block does not exist or the index is out of range.

The example below is the real response captured from the Nile testnet curl above (same contract call shown in [`eth_getTransactionByHash`](eth_getTransactionByHash.md)):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "hash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
    "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "blockNumber": "0x3fe1ca0",
    "transactionIndex": "0x0",
    "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
    "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
    "value": "0x0",
    "gas": "0xae29",
    "gasPrice": "0x64",
    "input": "0xa6bd98ac0000...0000",
    "type": "0x0",
    "nonce": "0x0000000000000000",
    "v": "0x1b",
    "r": "0x2154e8ef08f014063de8a88bafe748c8cbb48633c1657c083dca1a73439b289f",
    "s": "0x6aa796bfa58797da6354d35fb7334a8c145c48ae266e4a885f7ee44791b5a3c3"
  }
}
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` is `pending` or `safe` | `-32602` | `TAG pending not supported` or `TAG safe not supported` |
| `params[0]` is neither a valid non-negative hex/decimal height nor a valid tag | `-32602` | `invalid block number` |
| `params[1]` is not valid hex | `-32602` | `invalid index value` |
