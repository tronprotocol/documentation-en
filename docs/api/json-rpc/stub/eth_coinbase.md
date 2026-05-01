# eth_coinbase

Returns the etherbase address (Ethereum compatibility; Tron has no native PoW coinbase concept).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getCoinbase`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_coinbase","params":[],"id":1}'
```

## Response

The string returned by `wallet.getCoinbase()`. Only returns a value when the node explicitly configures `node.etherbase`. With it configured, the response looks like:

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x41a614f803b6fd780986a42c78ec9c7f77e6ded13c" }
```

> Note: the 21 bytes here (`0x41` + 20 bytes) is Tron's native address format, different from Ethereum's standard 20 bytes.

### Error responses

| Trigger | Code | message |
|---|---|---|
| Node has no etherbase configured | `-32000` | `etherbase must be explicitly specified` |

The example below is the real response captured from the Nile testnet curl above (`nile.trongrid.io` has no etherbase configured, so it goes through the error branch):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32000,
    "message": "etherbase must be explicitly specified",
    "data": "{}"
  }
}
```
