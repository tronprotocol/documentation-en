# eth_call

Read-only call to a smart contract (no on-chain effect, no energy consumed).

- Source: `framework/src/main/java/org/tron/core/services/jsonrpc/TronJsonRpcImpl.java#getCall`
- Ports: FullNode `8545` / Solidity `8555`

## Request parameters

| Position | Type | Required | Description |
|---|---|---|---|
| `params[0]` | object | yes | `CallArguments` object, see below |
| `params[1]` | string \| object | yes | Block tag: a tag string, or a `{"blockNumber": "0x..."}` / `{"blockHash": "0x..."}` object (EIP-1898). String tags only support `latest`; object form checks that the referenced block exists, but execution still uses the latest state |

`CallArguments` fields (`framework/src/main/java/org/tron/core/services/jsonrpc/types/CallArguments.java`):

| Field | Default | Description |
|---|---|---|
| `from` | `0x0000000000000000000000000000000000000000` | Caller address |
| `to` | required | Contract address |
| `value` | `""` | callValue sent to the contract (sun, hex) |
| `data` | `null` | calldata (4-byte selector + abi-encoded args) |
| `input` | `null` | Alias for `data`; if both are set, `input` takes precedence for `eth_call` |
| `gas` / `gasPrice` / `nonce` | unused | — |

`input` follows stricter execution-API hex rules: it must have a `0x` prefix and an even number of hex digits; `""` is accepted as empty bytes. `data` keeps the legacy lenient parser for backward compatibility.

For `params[1]`, a string block tag must be `latest`. EIP-1898 object form accepts an existing `blockNumber` / `blockHash` and checks that the block exists, but the call still executes against latest state rather than historical state.

```bash
# Example: call symbol() of Tether USD (USDT) on Nile testnet
curl -X POST https://nile.trongrid.io/jsonrpc \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc":"2.0","id":1,"method":"eth_call",
    "params":[{
      "to":"0xeca9bc828a3005b9a3b909f2cc5c2a54794de05f",
      "data":"0x95d89b41"
    },"latest"]
  }'
```

## Response

The return value of the contract's `view` / `pure` function (concatenation of all `constantResult` segments), hex-encoded.

The example below is the real response captured from the Nile testnet curl above (USDT's `symbol()` returns the ABI-encoded string `"USDT"`: offset `0x20` + length `0x4` + UTF-8 bytes `5553445400...`):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": "0x000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000045553445400000000000000000000000000000000000000000000000000000000"
}
```

### Error responses

| Trigger | Code | message |
|---|---|---|
| `params[1]` is neither a string nor an object | `-32600` | `invalid json request` |
| `params[1]` object form has neither `blockNumber` nor `blockHash` | `-32600` | `invalid json request` |
| `blockNumber` in `params[1]` is not valid hex | `-32602` | `invalid block number` |
| The block specified in `params[1]` does not exist | `-32000` | `header not found` or `header for hash not found` |
| `params[1]` tag is `earliest` / `pending` / `finalized` / `safe` | `-32602` | `TAG [earliest \| pending \| finalized \| safe] not supported` |
| `params[1]` is a specific hex height (even if valid) | `-32602` | `QUANTITY not supported, just support TAG as latest` |
| `from` / `to` address is invalid | `-32602` | passes through the message |
| `input` is not strict hex | `-32602` | passes through `JsonRpcApiUtil.requireValidHex` validation message |
| `value` is not valid hex | `-32602` | `invalid param value: invalid hex number` |
| Contract validation fails (e.g. `to` is not a contract, args don't match, etc.) | `-32600` | passes through `ContractValidateException` message (fallback `Contract validate error : ` if no message) |
| EVM execution `REVERT` | `-32000` | message + (if revert data starts with the `Error(string)` selector) the parsed string; `error.data` carries the original revert hex |
| Other execution / encoding errors | `-32000` | passes through message (double quotes are replaced with single quotes) |
