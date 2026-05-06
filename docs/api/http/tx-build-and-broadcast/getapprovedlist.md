# /wallet/getapprovedlist

Return the list of addresses that have already signed a multi-sig transaction (does not compute weight, just lists signers).

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionApprovedListServlet.java`
- Method: `POST`
- Response: `api.TransactionApprovedList` (`api.proto`)

## Request parameters

Same body as [`/wallet/getsignweight`](getsignweight.md):

| Field | Type | Required | Description |
|---|---|---|---|
| `raw_data` | object | Yes | Same as `createtransaction` response |
| `raw_data_hex` | string | No (node ignores) | Same as [`broadcasttransaction`](broadcasttransaction.md): client display helper, not used for signature verification |
| `signature` | string[] | Yes | Collected signatures |
| `visible` | bool | No | Format of address / text fields (the response includes `result.message`, which is affected by `visible`) |

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

> The above is a placeholder; the real request body is a multi-sig transaction JSON with at least one `signature` (from [`/wallet/createtransaction`](createtransaction.md) etc., then signed).

## Response

| Field | Type | Description |
|---|---|---|
| `approved_list` | repeated bytes | Signed addresses; base58 array when `visible=true`, hex (21 bytes, `41` prefix) when `visible=false` |
| `result.code` | enum | `SUCCESS` / `SIGNATURE_FORMAT_ERROR` / `COMPUTE_ADDRESS_ERROR` / `OTHER_ERROR` |
| `result.message` | string | Error description (UTF-8 when `visible=true`, otherwise hex) |
| `transaction` | TransactionExtention | Original transaction; its `transaction.transaction` is rewritten by `Util.printTransactionToJSON` into a complete unsigned-transaction JSON (with `txID`, `raw_data.contract`, `raw_data_hex`) |

Response example:

```json
{
  "approved_list": ["41dd791d6b49e190062d650e6a23c575510d35f2f9"],
  "result":       { "code": "SUCCESS" },
  "transaction": {
    "txid":        "<computed from raw_data>",
    "transaction": { "...": "..." }
  }
}
```

> Note: signature parse and address recovery errors **do not** go through `Util.processError` — they are written into the response's `result.code` / `result.message` (HTTP 200). The table below only lists failures that produce `{"Error": ...}`-shaped responses.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` |
| Missing `raw_data`, `raw_data.contract` is not an array, `signature` is not an array or its elements are not hex, field type mismatch in `raw_data`, etc. | `{"Error": "class java.lang.NullPointerException : null"}` (`Util.packTransaction` silently catches `JsonFormat$ParseException` / `ClassCastException` and returns `null`; downstream `getTransactionApprovedList(null)` triggers NPE) |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
