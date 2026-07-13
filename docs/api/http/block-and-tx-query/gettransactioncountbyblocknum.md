# /wallet/gettransactioncountbyblocknum

Returns the number of transactions contained in a given block number.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionCountByBlockNumServlet.java`
- Method: `GET` / `POST`
- Request: `api.NumberMessage`
- Solidity endpoint: `/walletsolidity/gettransactioncountbyblocknum`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `num` | GET | int64 | Yes | Block number; omission reaches `Long.parseLong(null)` and fails |
| `num` | POST | int64 | No | Block number; Protobuf default is `0` |
| `int64_as_string` | GET | bool | No | GET only; when `true`, returns `count` as a JSON string |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactioncountbyblocknum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "num": 66987565 }
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `count` | int64 | Number of transactions in the block; returns 0 if the block does not exist |

Response example:

```json
{ "count": 4 }
```

With `?int64_as_string=true` on a GET request:

```json
{ "count": "4" }
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET | `num` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
