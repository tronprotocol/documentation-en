# /wallet/getavailableunfreezecount

Query the remaining number of unfreeze requests an account can initiate (Stake 2.0 allows up to 32 in-flight unfreezes per account).

- Source: `framework/src/main/java/org/tron/core/services/http/GetAvailableUnfreezeCountServlet.java`
- Method: `GET` / `POST`
- Response: `api.GetAvailableUnfreezeCountResponseMessage`
- Solidity endpoint: `/walletsolidity/getavailableunfreezecount`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

GET also accepts `ownerAddress` as an alias for `owner_address`. POST accepts only the canonical `owner_address` field; `ownerAddress` is treated as an unknown JSON field and ignored.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `owner_address` | GET / POST | string | Yes | Account address; the `ownerAddress` alias is supported only by GET |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getavailableunfreezecount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `count` | int64 | Remaining unfreeze count |

Response example (no pending unfreeze requests, full 32-quota available):

```json
{ "count": 32 }
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `owner_address` is not valid base58check (`visible=true`) | GET: with non-base58 characters, throws `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; if only the checksum is wrong, `Util.getHexAddress` silently returns empty string → no record found, returns `{}`. POST (via `JsonFormat.merge`): with non-base58 characters, throws `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`; if only the checksum is wrong, throws `{"Error": "class java.lang.NullPointerException : null"}` |
| GET / POST | `owner_address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
