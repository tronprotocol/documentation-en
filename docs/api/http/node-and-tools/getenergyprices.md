# /wallet/getenergyprices

Get historical energy unit prices (a new entry is appended after each governance proposal change).

- Source: `framework/src/main/java/org/tron/core/services/http/GetEnergyPricesServlet.java`
- Method: `GET` / `POST`
- Response: `api.PricesResponseMessage`
- Solidity endpoint: `/walletsolidity/getenergyprices`

## Request parameters

None.

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getenergyprices \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `prices` | string | Comma-separated `<effectiveTimestamp>:<priceInSun>` records, e.g. `0:100,1572597600000:10` |

Response example:

```json
{
  "prices": "0:100,1572597600000:10,1606282800000:40,1612768800000:140,1612769400000:140,1612778400000:140,1628674200000:420,1635143400000:280,1669603800000:420,1726283400000:210,1754644200000:100"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Internal node error (failed to read price history or serialize) | `{"Error": "<exceptionClass> : <message>"}` |
