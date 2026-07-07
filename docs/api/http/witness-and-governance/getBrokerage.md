# /wallet/getBrokerage

Query the SR's current-cycle reward share ratio (brokerage).

- Source: `framework/src/main/java/org/tron/core/services/http/GetBrokerageServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getBrokerage`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `address` | string | No | SR address; omitted or empty returns `brokerage: 0` |
| `visible` | bool | No | No effect (the servlet auto-detects address format via the `41` prefix; the response has no bytes fields) |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getBrokerage \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `brokerage` | int | Percentage (0–100), default 20 |

Response example (Nile, sr-15):

```json
{ "brokerage": 100 }
```

> Note: when `address` is missing or empty, no error is reported; the response is `{"brokerage": 0}` — indistinguishable from "this SR's current brokerage is 0", so callers must disambiguate themselves.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `address` starts with `41` but is not valid hex | `{"Error": "INVALID address, <hex parser info>"}` |
| `address` is not valid base58check | `{"Error": "INVALID address, <base58 check info>"}` |
| POST body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
