# eth_getTransactionReceipt

Query a transaction receipt by txid.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTransactionReceipt`
- Data structure: `framework/src/main/java/org/tron/core/services/jsonrpc/types/TransactionReceipt.java`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | 32-byte txid |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params":["0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"],"id":1}'
```

## Response

`TransactionReceipt` object; returns `null` when not found (e.g. the transaction has no `TransactionInfo` yet).

| Field | Type | Description |
|---|---|---|
| `blockHash` / `blockNumber` / `transactionIndex` | hex | Block locator |
| `transactionHash` | hex | txid |
| `from` / `to` | hex | Addresses |
| `cumulativeGasUsed` | hex | Total energy consumed by all transactions up to and including this one in the block |
| `gasUsed` | hex | Energy used by this transaction |
| `effectiveGasPrice` | hex | Energy unit price at block time (sun) |
| `contractAddress` | hex | Only set for `CreateSmartContract` type |
| `logs` | array | Log array (each entry includes `logIndex`, `address`, `data`, `topics[]`, `blockHash`, `blockNumber`, `blockTimestamp`, `transactionHash`, `transactionIndex`, `removed`) |
| `logsBloom` | hex | Constant 256 bytes of zeros |
| `status` | hex | `0x1` success / `0x0` failure (based on `TransactionInfo.resultValue <= 1`) |
| `type` | hex | Constant `0x0` |
| `root` | null | Not populated (post-Byzantium) |

> **Note**: To parse the `logs` field, please ensure the transaction succeeded (`status == "0x1"`) first — this alignment is recommended for data consistency. 

The example below is the real response captured from the Nile testnet curl above (a contract call producing 1 log; cross-check at [Nile Tronscan](https://nile.tronscan.org/#/transaction/01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca)):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "blockNumber": "0x3fe1ca0",
    "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
    "transactionIndex": "0x0",
    "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
    "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
    "cumulativeGasUsed": "0xae29",
    "gasUsed": "0xae29",
    "effectiveGasPrice": "0x64",
    "contractAddress": null,
    "logs": [
      {
        "address": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
        "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
        "blockNumber": "0x3fe1ca0",
        "blockTimestamp": "0x697999ef",
        "transactionHash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
        "transactionIndex": "0x0",
        "logIndex": "0x0",
        "removed": false,
        "topics": [
          "0xc66625d03b4a832d8245f0df593e32e0fbbbad96d4aa45440aa1535b80983083",
          "0x000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
          "0x0000000000000000000000000000000000000000000000000000000000000007"
        ],
        "data": "0x0000...05f"
      }
    ],
    "logsBloom": "0x0000...0000",
    "status": "0x1",
    "type": "0x0"
  }
}
```

> The log `data` is actually 224 bytes; only the head and tail are kept here for brevity. `logsBloom` is actually 256 bytes of zeros; other fields are the node's real return values.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` does not match `(0x)?[0-9a-fA-F]{64}` | `-32602` | `invalid hash value` |
