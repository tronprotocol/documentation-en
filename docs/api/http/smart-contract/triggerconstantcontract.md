# /wallet/triggerconstantcontract

Read-only contract call (does not go on-chain). Used to read view/pure functions or simulate transactions.

- Source: `framework/src/main/java/org/tron/core/services/http/TriggerConstantContractServlet.java`
- Method: `POST`
- Contract: `protocol.TriggerSmartContract`
- Response: `api.TransactionExtention`
- Solidity endpoint: `/walletsolidity/triggerconstantcontract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Caller address (`msg.sender` in the contract) |
| `contract_address` | string | Yes | Target contract address |
| `function_selector` | string | No | Function signature |
| `parameter` | string | No | ABI-encoded parameters (hex) |
| `data` | string | No | Call data (hex); use either this or `function_selector` |
| `call_value` | int64 | No | TRX (sun) sent with the call |
| `token_id` | int64 | No | TRC-10 token id sent with the call |
| `call_token_value` | int64 | No | TRC-10 amount sent with the call |
| `extra_data` | string | No | Transaction memo (hex; UTF-8 text when `visible=true`) |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields (response includes `result.message`, which is affected by `visible`) |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/triggerconstantcontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "function_selector": "balanceOf(address)",
  "parameter":         "000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## Response

`TransactionExtention`:

| Field | Type | Description |
|---|---|---|
| `transaction` | Transaction | Unsigned transaction (context only — should not be signed and broadcast) |
| `txid` | string(hex) | Transaction hash |
| `constant_result` | repeated bytes(hex) | ABI-encoded hex of the function return value; **on revert, this is the ABI-encoded revert reason** (the leading 4 bytes `08c379a0` are the `Error(string)` selector) |
| `result` | Return | Status; on revert / failed `require`, `result.result=false` and `result.message` contains `REVERT opcode executed` or `runtime error` |
| `energy_used` | int64 | Estimated energy consumed |
| `energy_penalty` | int64 | Energy penalty (if any) |
| `logs` | repeated TransactionLog | Event logs (if emitted) |
| `internal_transactions` | repeated InternalTransaction | Internal calls (if any) |

Response example (real Nile capture):

```json
{
  "result": { "result": true },
  "energy_used": 935,
  "constant_result": ["0000000000000000000000000000000000000000000000000000000040cfcc00"],
  "transaction": {
    "ret": [{}],
    "visible": false,
    "txID": "cff6488e738ce77f7325572fe0aa2470f87dbf1c95eeeb2c25feec59d5afa35c",
    "raw_data": {
      "contract": [
        {
          "parameter": {
            "value": {
              "data":             "70a08231000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
            },
            "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
          },
          "type": "TriggerSmartContract"
        }
      ],
      "ref_block_bytes": "28c0",
      "ref_block_hash":  "9eabbe133123b34c",
      "expiration":      1777447218000,
      "timestamp":       1777447160779
    },
    "raw_data_hex": "0a0228c022089eabbe133123b34c40d0d6f0c0dd335a8e01081f1289010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412540a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541eca9bc828a3005b9a3b909f2cc5c2a54794de05f222470a08231000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f970cb97edc0dd33"
  }
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` and other ephemeral fields share semantics with [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md). Constant calls do not go on-chain; the `transaction` field is provided only as context.

### Error responses

This endpoint never writes `{"Error": ...}`. All exceptions are caught and written into `result.code` / `result.message`; the HTTP body is still a `TransactionExtention`. Note: **EVM revert / runtime errors do not go through `result.code`** — instead `result.result=true`, `message` carries the revert/runtime info, and the failure is marked at `transaction.ret[0].ret="FAILED"`.

| Trigger | `result.result` | `result.code` | `result.message` | Other |
|---|---|---|---|---|
| Contract does not exist / validation failed (`ContractValidateException`) | default (false) | `CONTRACT_VALIDATE_ERROR` | Original validator message | — |
| EVM revert / failed `require` | true | default (`SUCCESS`, omitted) | `REVERT opcode executed` | `transaction.ret[0].ret="FAILED"`; `constant_result[0]` is the `Error(string)` ABI encoding (when the contract supplies a reason) |
| EVM runtime error (OOG, illegal opcode, etc., no `result.getException()`) | true | default (`SUCCESS`, omitted) | Raw `result.getRuntimeError()` string | Same as above |
| `result.getException() != null` (e.g. `OutOfTimeException`) | default (false) | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) | — |
| Other (hex parsing, missing parameters, proto merge, etc.) | default (false) | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) | — |

On revert, `result.message` does not carry the original reason string; you must decode it from `constant_result[0]`: skip the leading 4-byte `08c379a0` selector and ABI-decode the remaining bytes as `string`.
