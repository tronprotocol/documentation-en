# /wallet/broadcasthex

Broadcast a signed transaction whose payload is the protobuf-hex encoding of `Transaction`. Smaller body than `/wallet/broadcasttransaction`.

- Source: `framework/src/main/java/org/tron/core/services/http/BroadcastHexServlet.java`
- Method: `POST`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `transaction` | string | Yes | Hex of the protobuf serialization of a complete `protocol.Transaction`. Each embedded signature must be `65`–`68` bytes; otherwise broadcast returns `SIGERROR` |

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
| `result` | bool | Whether this broadcast attempt succeeded. A failed P2P broadcast can occur after the transaction has entered the pool |
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

Invalid hex and protobuf-deserialization errors take the `Util.processError` path. A missing or null `transaction` is parsed as an empty transaction; if earlier broadcast checks pass, the node returns `CONTRACT_VALIDATE_ERROR` with the message `Contract validate error : No contract!`. The servlet does not have its own `Util.checkBodySize` branch, but the shared HTTP `SizeLimitHandler` can still reject oversized request bodies.

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| `transaction` field missing or null | If earlier broadcast checks pass, business-level response `{"result": false, "code": "CONTRACT_VALIDATE_ERROR", "message": "Contract validate error : No contract!", "transaction": "{}", "txid": "<SHA256 of empty raw_data>"}` (`getString` returns null → `ByteArray.fromHexString(null)` returns empty array → `Transaction.parseFrom` returns empty Transaction → rejected by the node) |
| `transaction` is not a string (array/object/number) | Unsupported input shape. `getString` coerces scalars to text and serializes arrays/objects; invalid hex produces `DecoderException`, hex-valid but invalid protobuf produces `InvalidProtocolBufferException`, and protobuf-valid content proceeds to broadcast. For example, numeric `10` becomes hex `10` and fails protobuf parsing |
| `transaction` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` |
| `transaction` is not valid protobuf | `{"Error": "class com.google.protobuf.InvalidProtocolBufferException : <message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
