# web3_sha3

Compute the Keccak-256 hash of the input data.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#web3Sha3`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Bytes to hash, hex-encoded (with or without `0x` prefix) |

Example request:

```bash
# Example: Keccak-256 of the ASCII string "hello"
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"web3_sha3","params":["0x68656c6c6f"],"id":1}'
```

## Response

`0x`-prefixed 32-byte hex (i.e. Keccak-256, matching EVM `KECCAK256`; **not** SHA3-256).

The example below is the real response captured from the Nile testnet curl above (`keccak256("hello") = 1c8aff95...deac8`):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8"
}
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[0]` is not a valid hex | `-32602` | `invalid input value` |
