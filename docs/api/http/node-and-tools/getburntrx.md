# /wallet/getburntrx

Query the cumulative TRX burned (including transaction fees, contract burns, etc.).

- Source: `framework/src/main/java/org/tron/core/services/http/GetBurnTrxServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getburntrx`

## Request parameters

POST has no request parameters and its body is not parsed. GET accepts the following URL query parameter:

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `int64_as_string` | GET | bool | No | When `true`, returns `burnTrxAmount` as a JSON string |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getburntrx \
     --header 'accept: application/json'
```

## Response

`burnTrxAmount` is in sun.

Response example:

```json
{ "burnTrxAmount": 153731208869910 }
```

With `?int64_as_string=true` on a GET request:

```json
{ "burnTrxAmount": "153731208869910" }
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to read dynamic properties) | `{"Error": "<exceptionClass> : <message>"}` |
