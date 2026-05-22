# /wallet/gettransactioncountbyblocknum

Returns the number of transactions contained in a given block number.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionCountByBlockNumServlet.java`
- Method: `GET` / `POST`
- Request: `api.NumberMessage`
- Solidity endpoint: `/walletsolidity/gettransactioncountbyblocknum`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `num` | int64 | Yes | Block number |

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

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `num` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
