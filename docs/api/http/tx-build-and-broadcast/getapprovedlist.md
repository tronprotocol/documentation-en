# /wallet/getapprovedlist

Return the transaction's signing addresses after validating all signatures against the account's current permissions. If validation fails, return an error without an approved-address list.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionApprovedListServlet.java`
- Method: `POST`
- Response: `api.TransactionApprovedList` (`api.proto`)

## Request parameters

Same body as [`/wallet/getsignweight`](getsignweight.md):

| Field | Type | Required | Description |
|---|---|---|---|
| `raw_data` | object | Yes | Same as `createtransaction` response |
| `raw_data_hex` | string | No (node ignores) | Same as [`broadcasttransaction`](broadcasttransaction.md): client display helper, not used for signature verification |
| `signature` | string[] | No | Collected signatures; when omitted, the request is still parsed and the approved-address list is empty if the account and permission checks pass |
| `visible` | bool | No | Controls address / bytes-field formatting; `result.message` is a protobuf string and remains JSON text regardless of `visible` |

Example: the request body is a Transaction JSON with `signature`, structured the same as [`/wallet/broadcasttransaction`](broadcasttransaction.md).

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getapprovedlist \
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

> The above is a placeholder. A real permission check normally uses a multi-sig transaction JSON produced by [`/wallet/createtransaction`](createtransaction.md) and then signed, but the endpoint also accepts an empty or omitted `signature` array and returns no approved addresses if the account and permission checks pass.

## Response

| Field | Type | Description |
|---|---|---|
| `approved_list` | repeated bytes | Signed addresses; base58 array when `visible=true`, hex (21 bytes, `41` prefix) when `visible=false` |
| `result.code` | enum | `SUCCESS` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `OTHER_ERROR` |
| `result.message` | string | Error description as JSON text, independent of `visible` |
| `transaction` | TransactionExtention | The submitted transaction with its collected signatures |

On success, `result.code` has the protobuf default `SUCCESS` and is omitted from JSON, so the result object is `{}` when there is no message.

Response example:

```json
{
  "approved_list": ["41dd791d6b49e190062d650e6a23c575510d35f2f9"],
  "result":       {},
  "transaction": {
    "txid":        "<computed from raw_data>",
    "result":      { "result": true },
    "transaction": { "...": "..." }
  }
}
```

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
