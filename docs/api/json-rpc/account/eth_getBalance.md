# eth_getBalance

Query an account's TRX balance.

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getTrxBalance`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | string | yes | Account address. 20-byte hex (with or without `0x`) or base58check (e.g. `T...`) |
| `params[1]` | string | yes | Block tag, **only `latest` is supported** |

```bash
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xdd791d6b49e190062d650e6a23c575510d35f2f9","latest"],"id":1}'
```

## Response

Hex-encoded balance (in sun); a non-existent account is treated as 0.

The example below is the real response captured from the Nile testnet curl above (`0x6d1a6c48` ≈ 1.83 TRX):

```json
{ "jsonrpc": "2.0", "id": 1, "result": "0x6d1a6c48" }
```

> Balance is live data; subsequent requests will reflect account activity.

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[1]` is `earliest` / `pending` / `finalized` / `safe` | `-32602` | `TAG [earliest \| pending \| finalized \| safe] not supported` |
| `params[1]` is a valid hex number (a specific height) | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `params[1]` is neither a valid tag nor a valid hex | `-32602` | `invalid block number` |
| `params[0]` is not a valid address | `-32602` | passes through the message thrown by `addressCompatibleToByteArray` |

> Tron does not support state queries at arbitrary historical heights, so passing a specific height is explicitly rejected.
