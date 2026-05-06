# /wallet/getpendingsize

Returns the number of transactions in the node's pending pool.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPendingSizeServlet.java`
- Method: `GET` / `POST`

## Request parameters

None.

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

### Error responses

| Trigger | Response |
|---|---|
| Internal node error (failed to read the pending pool) | `{"Error": "<exceptionClass> : <message>"}` |
