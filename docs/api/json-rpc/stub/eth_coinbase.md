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

The string returned by `wallet.getCoinbase()`. The node must run in witness mode (`isWitness=true`), and an address derived from its configured local witness private keys must match an entry in the chain's witness list. The first matching local address is returned. For a matching address, an illustrative response is:

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x41a614f803b6fd780986a42c78ec9c7f77e6ded13c" }
```

> Note: the 21 bytes here (`0x41` + 20 bytes) is Tron's native address format, different from Ethereum's standard 20 bytes.

### Error responses

| Trigger | Code | message |
|---|---|---|
| Node is not in witness mode, or none of its local witness key addresses matches the chain witness list | `-32000` | `etherbase must be explicitly specified` |

The example below is the real response captured from the Nile testnet curl above (the serving node does not return a matching witness address, so it goes through the error branch):

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
