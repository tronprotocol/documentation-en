# net_version

Returns the current network ID.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getNetVersion`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"net_version","params":[],"id":1}'
```

## Response

Same value as [`eth_chainId`](eth_chainId.md): the last 4 bytes of block 0's (genesis) BlockId, hex-encoded. Mainnet / Nile / Shasta each have their own value.

The example below is the real response captured from the Nile testnet curl above (Nile chainId = `0xcd8690dc`):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0xcd8690dc"
}
```

### Error responses

Same as [`eth_chainId`](eth_chainId.md): if the underlying genesis block cannot be loaded, throws `-32000`, passing through the underlying `Exception.getMessage()`.
