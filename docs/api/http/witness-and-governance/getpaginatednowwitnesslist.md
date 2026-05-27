# /wallet/getpaginatednowwitnesslist

Paginated query of currently active SRs.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPaginatedNowWitnessListServlet.java`
- Method: `GET` / `POST`
- Response: `api.WitnessList`
- Solidity endpoint: `/walletsolidity/getpaginatednowwitnesslist`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `offset` | int64 | No | Starting offset; defaults to `0` |
| `limit` | int64 | No | Page size; defaults to `0`, which returns an empty list |
| `visible` | bool | No | Address format |

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

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `offset` / `limit` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Called against the fullnode HEAD cursor during a maintenance period (non-solidity) | `{"Error": "class org.tron.core.exception.MaintenanceUnavailableException : Service temporarily unavailable during maintenance period. Please try again later."}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
