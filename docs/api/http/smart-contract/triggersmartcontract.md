# /wallet/triggersmartcontract

Trigger a smart contract (state-changing call). Returns the unsigned transaction and pre-execution result.

- Source: `framework/src/main/java/org/tron/core/services/http/TriggerSmartContractServlet.java`
- Method: `POST`
- Contract: `protocol.TriggerSmartContract`
- Response: `api.TransactionExtention`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Caller address |
| `contract_address` | string | Yes | Target contract address |
| `function_selector` | string | No | Function signature (e.g. `transfer(address,uint256)`); pair with `parameter` |
| `parameter` | string | No | ABI-encoded parameters (hex, without function selector) |
| `data` | string | No | Pre-built call data (hex); use either this or `function_selector` |
| `call_value` | int64 | No | TRX (sun) sent with the call |
| `token_id` | int64 | No | TRC-10 token id sent with the call |
| `call_token_value` | int64 | No | TRC-10 amount sent with the call |
| `fee_limit` | int64 | No | Transaction fee limit (sun); omitted defaults to `0` |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields (response includes `result.message`, which is affected by `visible`) |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/triggersmartcontract \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "function_selector": "transfer(address,uint256)",
  "parameter":         "000000000000000000000000088a2bfcb1c7271029fd69a66859d555608958840000000000000000000000000000000000000000000000000000000000000064",
  "fee_limit":  100000000,
  "call_value": 0
}
'
```

## Response

`TransactionExtention`:

| Field | Type | Description |
|---|---|---|
| `transaction` | Transaction | Unsigned transaction |
| `txid` | string(hex) | Transaction hash |
| `constant_result` | repeated bytes(hex) | Populated only when the ABI marks the function as `view` / `pure` (state-changing calls usually don't have this) |
| `result` | Return | Status |
| `energy_used` | int64 | Populated only on the constant-call path; not returned for ordinary state-changing calls |
| `energy_penalty` | int64 | Energy penalty (if any) |

Response example (real Nile capture):

```json
{
  "result": { "result": true },
  "transaction": {
    "visible": false,
    "txID": "8c621a0dc9bd4d405b20d0a43143955b9f546f98bbfde1aec295a65b0f925629",
    "raw_data": {
      "contract": [
        {
          "parameter": {
            "value": {
              "data":             "a9059cbb000000000000000000000000088a2bfcb1c7271029fd69a66859d5556089588400000000000000000000000000000000000000000000000000000000000000064",
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
            },
            "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
          },
          "type": "TriggerSmartContract"
        }
      ],
      "ref_block_bytes": "28c3",
      "ref_block_hash":  "ce6d340282788569",
      "fee_limit":       100000000,
      "expiration":      1777447227000,
      "timestamp":       1777447168009
    },
    "raw_data_hex": "0a0228c32208ce6d34028278856940f89cf1c0dd335aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541eca9bc828a3005b9a3b909f2cc5c2a54794de05f2244a9059cbb000000000000000000000000088a2bfcb1c7271029fd69a66859d5556089588400000000000000000000000000000000000000000000000000000000000000647089d0edc0dd33900180c2d72f"
  }
}
```

> `txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` and other ephemeral fields share semantics with [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md). The state-changing path does not populate `txid` / `constant_result` / `energy_used`; for a simulated execution result, use [`/wallet/triggerconstantcontract`](triggerconstantcontract.md).

> For simulation only (no on-chain effect), use [`/wallet/triggerconstantcontract`](triggerconstantcontract.md); for energy estimation only, use [`/wallet/estimateenergy`](estimateenergy.md).

### Error responses

This endpoint never writes `{"Error": ...}` after the request reaches the servlet. Servlet-handled exceptions are caught and written into `result.code` / `result.message`; the HTTP body is still a `TransactionExtention`.

Before the request reaches this servlet, shared layers can still return a different shape: `SizeLimitHandler` usually returns HTTP 413 `Payload Too Large` for an oversized body, and a non-blocking rate-limit rejection returns HTTP 200 with `{"Error":"class java.lang.IllegalAccessException : lack of computing resources"}`.

| Trigger | `result.result` | `result.code` | `result.message` |
|---|---|---|---|
| Empty `owner_address` / `contract_address` (`InvalidParameterException`) | false | `OTHER_ERROR` | `class java.security.InvalidParameterException : owner_address isn't set.` etc. |
| `contract_address` does not point to an existing smart contract | false | `CONTRACT_VALIDATE_ERROR` | `No contract or not a valid smart contract` |
| Other (hex parsing, proto merge, etc.) | false | `OTHER_ERROR` | `<exceptionClass> : <message>` (`"` → `'`) |
