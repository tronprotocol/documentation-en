# /wallet/getBrokerage

Query the SR's current-cycle reward share ratio (brokerage).

- Source: `framework/src/main/java/org/tron/core/services/http/GetBrokerageServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getBrokerage`

## Request parameters

GET reads `address` from the URL query; POST reads it from a JSON request body. `visible` is ignored.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `address` | GET / POST | string | No | SR address; omitted or empty returns `brokerage: 0` |
| `visible` | GET / POST | bool | No | No effect (the servlet auto-detects address format via the `41` prefix; the response has no bytes fields) |

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

> Missing or empty addresses, and Base58Check addresses rejected for length, checksum, or decoded-address validity, return `{"brokerage": 0}`. This is indistinguishable from a valid zero brokerage. Validate the address before using the result; parser exceptions follow the error table below.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `address` starts with `41` but is not valid hex | `{"Error": "INVALID address, <hex parser info>"}` |
| GET / POST | Base58 decoding throws (for example, an illegal character in an address of the expected length) | `{"Error": "INVALID address, <base58 parser info>"}` |
| GET / POST | Base58Check address has the wrong length, checksum, or decoded-address validity | `{"brokerage": 0}` |
| POST | POST body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
