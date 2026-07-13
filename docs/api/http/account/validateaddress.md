# /wallet/validateaddress

Validate the format of an address (auto-detects hex / base58check / base64). **Does not query the chain** — only checks encoding + checksum.

- Source: `framework/src/main/java/org/tron/core/services/http/ValidateAddressServlet.java`
- Method: `GET` / `POST`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `address` | GET / POST | string | Yes | Address to validate; format is detected by length: 42 chars hex / 34 chars base58check / 28 chars base64 |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/validateaddress \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9" }
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `result` | bool | Whether the address is valid |
| `message` | string | `Hex string format` / `Base58check format` / `Base64 format` / `Length error` / `Invalid address` |

Response example:

```json
{ "result": true, "message": "Hex string format" }
```

### Error responses

Address-parsing errors (length mismatch, checksum failure, base58/base64 decode failure, etc.) are conveyed via `result=false` plus `message` — they do **not** produce an `{"Error": ...}` body.

Two failures bypass the normal `result=false` response: an oversized request body may be rejected by the shared HTTP layer before the servlet runs, while malformed JSON can fail inside `doPost`. The latter exception is caught and only logged, so the client receives **HTTP 200 with an empty body**:

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| POST | Request body is not valid JSON (POST) | Empty body (`JSON.parseObject` throws `org.tron.json.JSONException`, which is swallowed) |
