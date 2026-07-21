# /wallet/broadcasthex

Broadcast a signed transaction whose payload is the protobuf-hex encoding of `Transaction`. Smaller body than `/wallet/broadcasttransaction`.

- Source: `framework/src/main/java/org/tron/core/services/http/BroadcastHexServlet.java`
- Method: `POST`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `transaction` | string | Yes | Hex of the protobuf serialization of a complete `protocol.Transaction` |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/broadcasthex \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "transaction": "0a8a010a02..." }
'
```

> The `transaction` field must be the hex of the entire signed Transaction protobuf — produced by signing the `raw_data_hex` returned by [`/wallet/createtransaction`](createtransaction.md) and re-serializing the full Transaction; the `0a8a010a02...` above is just a placeholder.

## Response

| Field | Type | Description |
|---|---|---|
| `result` | bool | Whether it entered the transaction pool |
| `code` | string | Same as `broadcasttransaction`, but emitted directly as the enum name |
| `message` | string | Failure reason (UTF-8) |
| `transaction` | string | The parsed Transaction JSON in **string form** (the servlet forces `visible=true` and calls `JsonFormat.printToString`, then puts the string into the response; clients need to JSON-parse this field again) |
| `txid` | string | Transaction hash |

Response example:

```json
{
  "result": true,
  "code": "SUCCESS",
  "message": "",
  "transaction": "{...}",
  "txid": "d5ec749ecc2a615399d8a6c864ea4c74ff9f8453eaa44d6b1e2f0b7b3e2f3b6a"
}
```

### Error responses

Business-level errors (`SIGERROR` / `DUP_TRANSACTION_ERROR` / `TAPOS_ERROR`, etc.) are returned in the `result/code/message` shape; `code` values match [`/wallet/broadcasttransaction`](broadcasttransaction.md).

When `transaction` is missing, not valid hex, or `Transaction.parseFrom` deserialization fails, `Util.processError` kicks in. The servlet does not have its own `Util.checkBodySize` branch, but the shared HTTP `SizeLimitHandler` can still reject oversized request bodies.

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| `transaction` field missing | Business-level response `{"result": false, "code": "CONTRACT_VALIDATE_ERROR", "message": "Contract validate error : No contract!", "transaction": "{}", "txid": "<SHA256 of empty Transaction>"}` (`getString` returns null → `ByteArray.fromHexString(null)` returns empty array → `Transaction.parseFrom` returns empty Transaction → enters broadcast) |
| `transaction` is not a string (array/object/number) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (`org.tron.json.JSONObject#getString` returns scalar values via `asText(null)` and serializes arrays/objects before handing the result to `ByteArray.fromHexString`) |
| `transaction` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` |
| `transaction` is not valid protobuf | `{"Error": "class com.google.protobuf.InvalidProtocolBufferException : <message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
