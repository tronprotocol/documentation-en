# /wallet/gettransactionlistfrompending

Returns the list of all transaction IDs in the pending pool.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionListFromPendingServlet.java`
- Method: `GET` / `POST`
- Response: `api.TransactionIdList`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `visible` | GET / POST | bool | No | No effect (response has no bytes fields) |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactionlistfrompending \
     --header 'accept: application/json'
```
## Response

| Field | Type | Description |
|---|---|---|
| `txId` | repeated string | List of transaction ID hex strings |

Response example:

```json
{
  "txId": [
    "7a265c89822d2dd9ee2187a728db3f273784943d588fd7b79ce972fc14a3f1de",
    "93347d947c339a2a7df588d3a96a003ec8745a4e0ee93a8074db3f1a754f21b5"
  ]
}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to read the pending pool) | `{"Error": "<exceptionClass> : <message>"}` |
