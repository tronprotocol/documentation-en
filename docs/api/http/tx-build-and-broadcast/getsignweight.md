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
| `signature` | string[] | No | Collected signatures; when omitted, the request is still parsed and `current_weight` remains `0` |
| `visible` | bool | No | Controls address / bytes-field formatting; `result.message` is a protobuf string and remains JSON text regardless of `visible` |

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

> The above is a placeholder. A real weight calculation normally uses a signed multi-sig transaction JSON, but the endpoint also accepts an empty or omitted `signature` array and reports `current_weight=0` together with the permission result.

## Response

| Field | Type | Description |
|---|---|---|
| `permission` | Permission | The currently effective permission |
| `current_weight` | int64 | Currently accumulated weight |
| `result.code` | enum | `ENOUGH_PERMISSION` / `NOT_ENOUGH_PERMISSION` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `PERMISSION_ERROR` / `OTHER_ERROR` |
| `result.message` | string | Error description as JSON text, independent of `visible` |
| `transaction` | TransactionExtention | The submitted transaction with its collected signatures |
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
    "result":      { "result": true },
    "transaction": { "...": "..." }
  }
}
```

When `current_weight >= permission.threshold`, the result code is `ENOUGH_PERMISSION` (the default enum value, omitted from JSON). This confirms only the selected permission's signature threshold. Broadcast still checks signature length, TAPOS, expiration, and transaction validity.

> Note: after the transaction JSON is decoded, signature-format, address-recovery, and permission-check failures are written into the response's `result.code` / `result.message` (HTTP 200). The table below lists failures that produce `{"Error": ...}`-shaped responses, including invalid signature hex during JSON decoding.

The protobuf JSON parser also accepts a single hex string for `signature` as a one-element list; a non-array value does not always cause a parse error. Use the documented array form for normal requests.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Missing or null `raw_data` / `raw_data.contract` | `{"Error": "class java.lang.NullPointerException : <message>"}` while accessing the missing object or array |
| `raw_data` is not an object, or `raw_data.contract` is not an array (excluding JSON strings that can be parsed into the required structure) | `{"Error": "class org.tron.json.JSONException : <message>"}`, for example `Field 'contract' is not an array` |
| Invalid signature hex or a `raw_data` field value that `JsonFormat.merge` cannot decode | `packTransaction` catches the final `JsonFormat$ParseException` and returns `null`; the downstream operation then returns `{"Error": "class java.lang.NullPointerException : <message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
