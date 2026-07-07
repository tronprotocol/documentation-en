# eth_chainId

Returns the chain ID.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#ethChainId`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":1}'
```

## Response

The **last 4 bytes** of the BlockId byte stream of block 0 (the genesis block), hex-encoded. Each chain has its own constant value; common references:

| Network | chainId |
|---|---|
| Mainnet | `0x2b6653dc` |
| Nile testnet | `0xcd8690dc` |
| Shasta testnet | `0x94a9059e` |

The example below is the real response captured from a Nile testnet call:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0xcd8690dc"
}
```

### Error responses

The implementation can throw `JsonRpcInternalException` if block 0 cannot be loaded, but the `eth_chainId` interface declaration does not define a `@JsonRpcErrors` mapping for that exception. Because of that, java-tron does not expose a stable method-level `-32000` mapping for this endpoint.
