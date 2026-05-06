# eth_getWork

Compatibility method. Returns `[currentBlockHash, null, null]` — only the first element is meaningful (the current latest block hash); the other two are constant `null`. Tron has no PoW work / target / seed concepts.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethGetWork`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getWork","params":[],"id":1}'
```

## Response

A 3-element array. The example below is the real response captured from a Nile testnet call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": [
    "0x0000000003fe2429fd471ebb02f925accea59aa1d2ee593ebcba6596204e1c18",
    null,
    null
  ]
}
```

> The first element is the latest block hash at request time and changes with every new block; if the node has not yet produced any blocks, this element is `null`.

### Error responses

None.
