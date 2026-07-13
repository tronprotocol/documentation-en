# /wallet/getpaginatednowwitnesslist

Paginated query of currently active SRs.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPaginatedNowWitnessListServlet.java`
- Method: `GET` / `POST`
- Response: `api.WitnessList`
- Solidity endpoint: `/walletsolidity/getpaginatednowwitnesslist`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `offset` | GET | int64 | Yes | Starting offset; omission reaches `Long.parseLong(null)` and fails |
| `offset` | POST | int64 | No | Starting offset; Protobuf default is `0` |
| `limit` | GET | int64 | Yes | Page size; omission reaches `Long.parseLong(null)` and fails |
| `limit` | POST | int64 | No | Page size; Protobuf default is `0`, which returns an empty list |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpaginatednowwitnesslist \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "offset": 0,
  "limit": 2
}
'
```
## Response

Same fields as [`/wallet/listwitnesses`](listwitnesses.md).

Response example (Nile, limit=2; `voteCount`, `latestBlockNum`, `latestSlotNum` change over time):

```json
{
  "witnesses": [
    {
      "address": "41608e7e1c6f6dcc1679ea512503e41ca0254e0948",
      "voteCount": 5405850746,
      "url": "http://sr-8.com",
      "totalProduced": 1891250,
      "totalMissed": 456,
      "latestBlockNum": 66987972,
      "latestSlotNum": 592482114,
      "isJobs": true
    },
    {
      "address": "4139e58c94e9877bbe5556ee7acc6d6d428a3929e9",
      "voteCount": 2322234750,
      "url": "http://sr-27.com",
      "totalProduced": 1896883,
      "totalMissed": 619,
      "latestBlockNum": 66987973,
      "latestSlotNum": 592482115,
      "isJobs": true
    }
  ]
}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET | `offset` / `limit` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Called against the fullnode HEAD cursor during a maintenance period (non-solidity) | `{"Error": "class org.tron.core.exception.MaintenanceUnavailableException : Service temporarily unavailable during maintenance period. Please try again later."}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
