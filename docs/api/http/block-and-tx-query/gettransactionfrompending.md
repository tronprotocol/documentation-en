# /wallet/gettransactionfrompending

Fetch a transaction from the pending pool by transaction ID.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionFromPendingServlet.java`
- Method: `GET` / `POST`
- Request: `api.BytesMessage`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Transaction ID hex |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
# First call /wallet/gettransactionlistfrompending to get a pending txID, then use it for value
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactionfrompending \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "7a265c89822d2dd9ee2187a728db3f273784943d588fd7b79ce972fc14a3f1de"
}
'
```

## Response

Returns `protocol.Transaction` (same structure as [`/wallet/gettransactionbyid`](gettransactionbyid.md)).

Response example (pending contract call, same structure as `gettransactionbyid`):

```json
{
  "signature": ["..."],
  "txID": "<pending transaction ID>",
  "raw_data": {
    "contract": [ /* see /wallet/gettransactionbyid example */ ],
    "ref_block_bytes": "...",
    "ref_block_hash": "...",
    "expiration": 1777445400000,
    "timestamp": 1777445307000
  },
  "raw_data_hex": "..."
}
```

> Pending transactions are typically packed into blocks within ≈ 3 seconds; in practice they almost always disappear from pending instantly, so this call most often returns `{}`.

Returns `{}` if the transaction is not in pending (already packed or expired).

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `value` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
