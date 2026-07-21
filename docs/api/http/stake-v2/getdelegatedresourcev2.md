# /wallet/getdelegatedresourcev2

Query the resource delegation records from→to (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceV2Servlet.java`
- Method: `GET` / `POST`
- Response: `api.DelegatedResourceList`
- Solidity endpoint: `/walletsolidity/getdelegatedresourcev2`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `fromAddress` | GET | string | Yes | Delegator address |
| `fromAddress` | POST | string | No | Delegator address; omitted uses empty bytes and returns an empty result |
| `toAddress` | GET | string | Yes | Receiver address |
| `toAddress` | POST | string | No | Receiver address; omitted uses empty bytes and returns an empty result |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresourcev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "fromAddress": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "toAddress":   "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
}
'
```
## Response

Same fields as [`/wallet/getdelegatedresource`](../stake-v1/getdelegatedresource.md), but only contains Stake 2.0 delegation records.

Response example (no delegation between from→to, returns empty `{}`; with delegation it looks like):

```json
{}
```

```json
{
  "delegatedResource": [
    {
      "from": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
      "to":   "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
      "frozen_balance_for_energy": 1000000000,
      "expire_time_for_energy":    1700000000000
    }
  ]
}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `fromAddress` / `toAddress` is not valid base58check (`visible=true`) | GET: with non-base58 characters, throws `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; if only the checksum is wrong, `Util.getHexAddress` silently returns empty string → no record found, returns `{}`. POST (via `JsonFormat.merge`): with non-base58 characters, throws `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`; if only the checksum is wrong, throws `{"Error": "class java.lang.NullPointerException : null"}` |
| GET / POST | `fromAddress` / `toAddress` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
