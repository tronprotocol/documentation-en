# eth_getLogs

Query event logs by criteria.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getLogs`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | object | yes | `FilterRequest` object (see below) |

`FilterRequest` fields:

| Field | Type | Default | Description |
|---|---|---|---|
| `fromBlock` | string | `latest` | Start block; accepts `latest` / `earliest` / `finalized` or a hex height (`pending` and `safe` are explicitly unsupported) |
| `toBlock` | string | `latest` | End block; same as above |
| `address` | string \| string[] | null | Single or multiple contract addresses; only logs produced by these addresses match |
| `topics` | array | null | Up to 4 slots; each slot can be a single topic, `null`, or an array of topics (OR semantics); slots are AND-combined |
| `blockHash` | string | null | If specified, equivalent to `fromBlock = toBlock = that block height` (EIP-234); mutually exclusive with `fromBlock` / `toBlock` |

```bash
# Example: list all logs in block 0x3fe1ca0 produced by contract 0x9ff8fc48...
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"eth_getLogs",
    "params":[{
      "fromBlock":"0x3fe1ca0",
      "toBlock":"0x3fe1ca0",
      "address":"0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825"
    }]
  }'
```

## Response

An array of `LogFilterElement` (matched by `address` / `topic` / block range):

| Field | Type | Description |
|---|---|---|
| `logIndex` | hex | Global index of the log within its block |
| `transactionIndex` | hex | Index of the parent transaction within the block |
| `transactionHash` | hex | txid |
| `blockHash` | hex | Block hash |
| `blockNumber` | hex | Block height |
| `blockTimestamp` | hex | Block timestamp in seconds |
| `address` | hex | Address of the contract that emitted the log |
| `data` | hex | abi-encoded concatenation of non-indexed parameters |
| `topics` | array | Indexed parameters (the first entry is the event signature hash) |
| `removed` | bool | Whether rolled back due to a reorg |

The example below is the real response captured from the Nile testnet curl above (the same log also appears in the [`eth_getTransactionReceipt`](../block-and-tx-query/eth_getTransactionReceipt.md) response for that transaction):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
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
  ]
}
```

> The log `data` is actually 224 bytes; only the head and tail are kept here for brevity. Other fields are the node's real return values.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `fromBlock` / `toBlock` is `pending` or `safe` | `-32602` | `TAG pending not supported` or `TAG safe not supported` |
| `blockHash` is given together with `fromBlock` / `toBlock` | `-32602` | `cannot specify both BlockHash and FromBlock/ToBlock, choose one or the other` |
| `blockHash` does not match the strict `(0x)?[0-9a-fA-F]{64}` hash rule | `-32602` | `invalid hash value` |
| `blockHash` decodes successfully but does not exist on this node | `-32602` | `invalid blockHash` |
| `fromBlock > toBlock` | `-32602` | `please verify: fromBlock <= toBlock` |
| Range exceeds `maxBlockRange` (default 5000) | `-32602` | `exceed max block range: <N>` |
| `address` array length > `maxAddressSize` (default 1000) | `-32602` | `exceed max addresses: <N>` |
| `topics` array length > 4 | `-32602` | `topics size should be <= 4` |
| A `topics` slot is an array with > `maxSubTopics` entries (default 1000) | `-32602` | `exceed max topics: <N>` |
| A `topics` element or `address` is not valid hex | `-32602` | `invalid topic(s): <value>` / `invalid address at index <i>: <value>` etc. |
| Hit count exceeds the limit | `-32005` | passes through `JsonRpcTooManyResultException` message |
| Node is a lite fullnode and the queried block has been pruned | `-32000` | passes through `BadItemException` / `ItemNotFoundException` message |
