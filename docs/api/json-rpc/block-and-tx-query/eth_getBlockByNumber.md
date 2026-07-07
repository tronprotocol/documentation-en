# eth_getBlockByNumber

Query a block by height or tag.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetBlockByNumber`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Block height (`0x`-prefixed hex) or tag: `latest` / `earliest` / `finalized` (`pending` and `safe` are explicitly unsupported, see Error responses) |
| `params[1]` | bool | yes | Whether to return full transaction objects |

Tag semantics (resolved by `Wallet.getByJsonBlockId`):

| tag | meaning |
|---|---|
| `latest` | Latest block (FullNode port) / latest solidified block (Solidity) |
| `earliest` | Block 0 (genesis) |
| `finalized` | Latest solidified block |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBlockByNumber","params":["0x3fe1c00", false],"id":1}'
```

## Response

A `BlockResult` object (fields described in [`eth_getBlockByHash`](eth_getBlockByHash.md)); returns `null` when not found.

The example below is the real response captured from the Nile testnet curl above (block height `0x3fe1c00` = 67025920; cross-check at [Nile Tronscan](https://nile.tronscan.org/#/block/67025920)):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "number": "0x3fe1c00",
    "hash": "0x0000000003fe1c00462b498ddae67717e96c785078adb5ccb7279148916e6f97",
    "parentHash": "0x0000000003fe1bff062fa008dcd68f6ab2a96a25bc175df22a04baa0cd391573",
    "miner": "0xa234e405a2c6fd67cdd4d0ea2f6188f65534c8b1",
    "timestamp": "0x69f18a5c",
    "size": "0x73d",
    "transactionsRoot": "0xfda5b0a23514a969259ae378185fc833e2c4e35874ee2f8b6d26d15acd976c6e",
    "stateRoot": "0x",
    "transactions": [
      "0x95aad4dfc3d5d389291c093425d06b2ce5a97b5b4953645316371158ebde3f27",
      "0x3142278c604b0c1ebcc9dd3644d89c4af690a923b4e78636ef58c60355dc325e",
      "0x5391938f5e61ad803a553710121ea5c158df4c3d7fc8d924e7138b550bb1bc7a",
      "0x04e8f7f804d0028a9b766e833710a4e01a7e5adf6156c286fb51d9803df18d65",
      "0x54cdfa7c97baea20cd559ca744e55f5e93aaa35c8e2e7e056f14caa79e5c1dee",
      "0x37b9671f6388eb45fd6497a635dc171f683f1e995f1e3d8f468f71c53fc59374",
      "0xd60d78362788faf992decd5022babdbfd9b2ae4e8a5e15646623dcef6f02f668",
      "0x496b12de5debec7697a29e63157fcc6b53be4fec4c9401a8245a8b3e430d8e72"
    ],
    "uncles": [],
    "gasLimit": "0x0",
    "gasUsed": "0x0",
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

> `logsBloom` is actually 256 bytes of zeros, abbreviated above; other fields are the node's real return values.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` is `pending` or `safe` | `-32602` | `TAG pending not supported` or `TAG safe not supported` |
| `params[0]` is neither valid hex nor a valid tag | `-32602` | `invalid block number` |
