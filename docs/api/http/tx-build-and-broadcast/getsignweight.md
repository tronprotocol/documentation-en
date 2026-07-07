# /wallet/getsignweight

Validate a partially-signed multi-sig transaction; returns the current weight and whether it has reached the threshold.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionSignWeightServlet.java`
- Method: `POST`
- Response: `api.TransactionSignWeight` (`api.proto`)

## Request parameters

Pass the JSON form of `protocol.Transaction` directly (with the collected `signature`s):

| Field | Type | Required | Description |
|---|---|---|---|
| `raw_data` | object | Yes | Same as `createtransaction` response |
| `raw_data_hex` | string | No (node ignores) | Same as [`broadcasttransaction`](broadcasttransaction.md): client display helper, not used for signature verification |
| `signature` | string[] | Yes | Collected signatures (can be just one) |
| `visible` | bool | No | Format of address / text fields (the response includes `result.message`, which is affected by `visible`) |

Example: the request body is a Transaction JSON with `signature`, structured the same as [`/wallet/broadcasttransaction`](broadcasttransaction.md).

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getsignweight \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "raw_data":     { "...": "..." },
  "raw_data_hex": "0a02...",
  "signature":    ["b8c0...01"]
}
'
```

> The above is a placeholder; the real request body is a multi-sig transaction JSON with at least one `signature`.

## Response

| Field | Type | Description |
|---|---|---|
| `permission` | Permission | The currently effective permission |
| `current_weight` | int64 | Currently accumulated weight |
| `result.code` | enum | `ENOUGH_PERMISSION` / `NOT_ENOUGH_PERMISSION` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `PERMISSION_ERROR` / `OTHER_ERROR` |
| `result.message` | string | Error description |
| `transaction` | TransactionExtention | Original transaction; its `transaction.transaction` field is rewritten by `Util.printTransactionToJSON` into a complete unsigned-transaction JSON (with `txID`, `raw_data.contract`, `raw_data_hex`) |
| `approved_list` | repeated bytes | base58 address array when `visible=true`; hex (21 bytes, `41` prefix) when `visible=false` |

Response example:

```json
{
  "permission": {
    "type":            "Active",
    "id":              2,
    "permission_name": "active",
    "threshold":       2,
    "keys": [
      { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 },
      { "address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a", "weight": 1 }
    ]
  },
  "current_weight": 1,
  "approved_list":  ["41dd791d6b49e190062d650e6a23c575510d35f2f9"],
  "result":         { "code": "NOT_ENOUGH_PERMISSION" },
  "transaction": {
    "txid":        "<computed from raw_data>",
    "transaction": { "...": "..." }
  }
}
```

When `current_weight >= permission.threshold`, `code=ENOUGH_PERMISSION` and the transaction can be broadcast.

> Note: signature parse, address recovery, and insufficient-permission errors **do not** go through `Util.processError` — they are written into the response's `result.code` / `result.message` (HTTP 200). The table below only lists failures that produce `{"Error": ...}`-shaped responses.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Missing `raw_data`, `raw_data.contract` is not an array, `signature` is not an array or its elements are not hex, field type mismatch in `raw_data`, etc. | `{"Error": "class java.lang.NullPointerException : null"}` (`Util.packTransaction` silently catches `JsonFormat$ParseException` / `ClassCastException` and returns `null`; downstream `getTransactionSignWeight(null)` triggers NPE) |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
