# eth_getBlockByHash

Query a block by its hash.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockByHash`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | 32-byte block hash, hex-encoded (with or without `0x`) |
| `params[1]` | bool | yes | `true` returns an array of full `TransactionResult` objects; `false` returns only an array of txids |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByHash","params":["0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c", true],"id":1}'
```

## Response

Returns a `BlockResult` object (see `BlockResult.java`), or `null` if not found. Fields:

| Field | Type | Description |
|---|---|---|
| `number` | hex | Block height |
| `hash` | hex | Block hash (i.e. BlockId; the first 8 bytes are the height in big-endian) |
| `parentHash` | hex | Parent block hash |
| `nonce` | hex | Constant 8 bytes of zeros (Tron has no PoW) |
| `sha3Uncles` | hex | Constant 32 bytes of zeros (Tron has no uncle blocks) |
| `logsBloom` | hex | Constant 256 bytes of zeros (block-level bloom is not maintained) |
| `transactionsRoot` | hex | Transaction trie root |
| `stateRoot` | hex | Account state root |
| `receiptsRoot` | hex | Constant 32 bytes of zeros |
| `miner` | hex | Block-producing witness address (all zeros for the genesis block) |
| `difficulty` / `totalDifficulty` | hex | Constant `0x0` |
| `extraData` | hex | Constant `0x` |
| `size` | hex | Serialized byte length |
| `gasLimit` | hex | Sum of `feeLimit` of all transactions in the block |
| `gasUsed` | hex | Sum of energy usage of all transactions in the block |
| `timestamp` | hex | Block timestamp, in **seconds** (the proto value is milliseconds, divided by 1000 here) |
| `transactions` | array | Array of `TransactionResult` objects when `params[1]=true`; otherwise an array of `0x`-prefixed txid strings |
| `uncles` | array | Always empty array `[]` |
| `baseFeePerGas` | hex | Constant `0x0` (no EIP-1559 base fee) |
| `mixHash` | hex | Constant 32 bytes of zeros |

The example below is the real response captured from the Nile testnet curl above (block height `0x3fe1ca0` = 67026080; cross-check at [Nile Tronscan](https://nile.tronscan.org/#/block/67026080)):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "number": "0x3fe1ca0",
    "hash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
    "parentHash": "0x0000000003fe1c9f1030bf08074186a7c119391405507ce6cceb95855f5ef164",
    "miner": "0xa234e405a2c6fd67cdd4d0ea2f6188f65534c8b1",
    "timestamp": "0x69f18c42",
    "size": "0x60a",
    "transactionsRoot": "0xb488e770d80b4431e356111db97fca5b14f3f6a4d630c565ff15ee4ed9abee72",
    "stateRoot": "0x",
    "transactions": [
      {
        "blockHash": "0x0000000003fe1ca05cf728c92ee79f5f2758c3e4e4ea88501826726880e8b81c",
        "blockNumber": "0x3fe1ca0",
        "from": "0xdd791d6b49e190062d650e6a23c575510d35f2f9",
        "to": "0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
        "hash": "0x01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
        "transactionIndex": "0x0",
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
    ],
    "uncles": [],
    "gasLimit": "0x2540be400",
    "gasUsed": "0xae29",
    "difficulty": "0x0",
    "totalDifficulty": "0x0",
    "extraData": "0x",
    "logsBloom": "0x0000...0000",
    "nonce": "0x0000000000000000",
    "sha3Uncles": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "receiptsRoot": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "baseFeePerGas": "0x0"
  }
}
```

> The block has 4 transactions in total; only the first contract call (`transactionIndex: 0x0`) is shown. The actual `input` is 580 bytes (contract selector `0xa6bd98ac` + arguments); only the head and tail are kept here for brevity. `logsBloom` is actually 256 bytes of zeros; other fields are the node's real return values.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` does not match `(0x)?[a-zA-Z0-9]{64}` | `-32602` | `invalid hash value` |
| `params[0]` is a valid 64-char string but fails to decode | `-32602` | passes through the message thrown by `ByteArray.fromHexString` |
