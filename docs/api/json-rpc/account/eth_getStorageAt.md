# eth_getStorageAt

Query the value of a contract storage slot.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getStorageAt`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Contract address (20-byte hex or base58check) |
| `params[1]` | string | yes | Storage slot index, 32-byte hex |
| `params[2]` | string | yes | Block tag, **only `latest` is supported** |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getStorageAt","params":["0x9ff8fc48fb114ccd5bbdc24a86f0c73082f08825","0x0","latest"],"id":1}'
```

## Response

The 32-byte slot value, hex-encoded. Returns 32 bytes of zeros when the **address is not a contract** or the slot has never been written.

The example below is the real response captured from the Nile testnet curl above (the contract's slot 0 holds a `uint256` counter with value `0x8`):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x0000000000000000000000000000000000000000000000000000000000000008" }
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[2]` is `earliest` / `pending` / `finalized` | `-32602` | `TAG [earliest \| pending \| finalized] not supported` |
| `params[2]` is a valid hex number | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `params[2]` is neither a valid tag nor a valid hex | `-32602` | `invalid block number` |
| `params[0]` is not a valid address | `-32602` | passes through the message |
