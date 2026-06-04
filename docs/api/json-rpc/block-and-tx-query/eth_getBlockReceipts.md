# eth_getBlockReceipts

Query all transaction receipts of an entire block by height / hash / tag.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getBlockReceipts`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Block hash (64 hex chars) / block height (hex) / tag (`latest` / `earliest` / `finalized`; `pending` is explicitly unsupported) |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockReceipts","params":["0x3fe1ca0"],"id":1}'
```

## Response

An array of `TransactionReceipt` (fields described in [`eth_getTransactionReceipt`](eth_getTransactionReceipt.md)), ordered by transaction index in the block. `cumulativeGasUsed` accumulates from transaction 0.

Special cases:

- Block does not exist → `null`
- **Block 0 (genesis)** → `null`
- Block has been pruned by a lite fullnode → `null`

> **Note**: To parse `logs` from the returned receipts, please ensure each receipt's `status` is `"0x1"` (success) first — this alignment is recommended for data consistency.

The example below is the real response captured from the Nile testnet curl above (block `0x3fe1ca0` has 4 transactions: 1 contract call + 3 TRX transfers):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    {
      "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
      "blockNumber": "0x3fe1ca0",
      "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
      "transactionIndex": "0x0",
      "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
      "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "gasUsed": "0xae29",
      "cumulativeGasUsed": "0xae29",
      "effectiveGasPrice": "0x64",
      "contractAddress": null,
      "logs": [
        {
          "address": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
          "topics": [
            "0xc66625d03b4a832d8245f0df593e32e0fbbbad96d4aa45440aa1535b80983083",
            "0x000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
            "0x0000000000000000000000000000000000000000000000000000000000000007"
          ],
          "data": "0x0000...05f",
          "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
          "blockNumber": "0x3fe1ca0",
          "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
          "transactionIndex": "0x0",
          "logIndex": "0x0",
          "removed": false
        }
      ],
      "logsBloom": "0x0000...0000",
      "status": "0x1",
      "type": "0x0"
    },
    {
      "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
      "blockNumber": "0x3fe1ca0",
      "transactionHash": "0x74034bfbb426506e7a0a3c0f329ca84cc9c7783f4307137dcc2fdbb184a9910e",
      "transactionIndex": "0x1",
      "from": "0xf7c3feccb6461aab0fd25f61d9560645b08228cb",
      "to": "0xb06b4139895c9f51c967c9f3d9089ca721e8e34c",
      "gasUsed": "0x0",
      "cumulativeGasUsed": "0xae29",
      "effectiveGasPrice": "0x64",
      "contractAddress": null,
      "logs": [],
      "logsBloom": "0x0000...0000",
      "status": "0x1",
      "type": "0x0"
    }
  ]
}
```

> The actual response includes all 4 receipts; only the first 2 are shown here for brevity. `cumulativeGasUsed` stays at `0xae29` after index `0x1` because only the contract call at index `0x0` consumed energy (`0xae29`), and the remaining 3 TRX transfers all have `gasUsed` of `0x0`. `logsBloom` is actually 256 bytes of zeros; other fields are the node's real return values.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` is neither hash-shaped nor a valid hex height / tag | `-32602` | `invalid block number` |
| `params[0]` is hash-shaped (`(0x)?[a-zA-Z0-9]{64}`) but contains non-hex characters | `-32602` | passes through the message thrown by `ByteArray.fromHexString` |
| `params[0]` is `pending` | `-32602` | `TAG pending not supported` |
| Block transaction list and `TransactionInfoList` lengths mismatch (should not happen; defensive check only) | `-32000` | `TransactionList size mismatch: block has %d transactions, but transactionInfoList has %d` |
