# /wallet/getpendingsize

Returns the number of transactions in the node's pending pool.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPendingSizeServlet.java`
- Method: `GET` / `POST`

## Request parameters

None.

For GET requests, `int64_as_string=true` may be added to the URL query to return `pendingSize` as a JSON string.

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

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Internal node error (failed to read the pending pool) | `{"Error": "<exceptionClass> : <message>"}` |
