# eth_accounts

Compatibility method. Tron nodes don't custody account private keys; always returns an empty array.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getAccounts`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

None.

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_accounts","params":[],"id":1}'
```

## Response

Always an empty array. The example below is the real response captured from a Nile testnet call:

```json
{ "jsonrpc": "2.0", "id": 1, "result": [] }
```

### Error responses

None.
