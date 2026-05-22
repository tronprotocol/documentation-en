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

| Trigger | Code | message |
|---|---|---|
| Unable to load block 0 (extreme cases such as the node not having finished loading the genesis block) | `-32000` | passes through the underlying `Exception.getMessage()` |
