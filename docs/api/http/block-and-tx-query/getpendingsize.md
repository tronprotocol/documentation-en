# /wallet/getpendingsize

Returns the number of transactions in the node's pending pool.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPendingSizeServlet.java`
- Method: `GET` / `POST`

## Request parameters

POST has no request parameters and its body is not parsed. GET accepts the following URL query parameter:

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `int64_as_string` | GET | bool | No | When `true`, returns `pendingSize` as a JSON string |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpendingsize \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `pendingSize` | int64 | Number of transactions in the pending pool |

Response example:

```json
{ "pendingSize": 2 }
```

With `?int64_as_string=true` on a GET request:

```json
{ "pendingSize": "2" }
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to read the pending pool) | `{"Error": "<exceptionClass> : <message>"}` |
