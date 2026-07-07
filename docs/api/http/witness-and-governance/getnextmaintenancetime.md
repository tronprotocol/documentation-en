# /wallet/getnextmaintenancetime

Get the start time of the next SR maintenance period.

- Source: `framework/src/main/java/org/tron/core/services/http/GetNextMaintenanceTimeServlet.java`
- Method: `GET` / `POST`

## Request parameters

None (only `visible`).

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getnextmaintenancetime \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `num` | int64 | Next maintenance time (millisecond timestamp) |

Response example (`num` advances at the end of each maintenance period):

```json
{ "num": 1777446600000 }
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Internal node error | `{"Error": "<exceptionClass> : <message>"}` |
