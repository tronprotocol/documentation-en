# /wallet/getnextmaintenancetime

Get the start time of the next SR maintenance period.

- Source: `framework/src/main/java/org/tron/core/services/http/GetNextMaintenanceTimeServlet.java`
- Method: `GET` / `POST`

## Request parameters

GET and POST read `visible` from the URL query; the servlet does not parse the POST body. `int64_as_string` is honored only on GET by `RateLimiterServlet`.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `visible` | GET / POST | bool | No | Output format; the default is `false` |
| `int64_as_string` | GET | bool | No | When `true`, returns `num` as a JSON string |

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

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error | `{"Error": "<exceptionClass> : <message>"}` |
