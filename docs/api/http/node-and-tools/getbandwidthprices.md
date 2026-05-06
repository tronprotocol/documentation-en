# /wallet/getbandwidthprices

Get historical bandwidth unit prices.

- Source: `framework/src/main/java/org/tron/core/services/http/GetBandwidthPricesServlet.java`
- Method: `GET` / `POST`
- Response: `api.PricesResponseMessage`
- Solidity endpoint: `/walletsolidity/getbandwidthprices`

## Request parameters

None.

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getbandwidthprices \
     --header 'accept: application/json'
```

## Response

| Field | Type | Description |
|---|---|---|
| `prices` | string | Comma-separated `<effectiveTimestamp>:<priceInSun>` records |

Response example:

```json
{
  "prices": "0:10,1606282800000:40,1612778400000:140,1625815200000:100,1626253800000:1000"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Internal node error (failed to read price history or serialize) | `{"Error": "<exceptionClass> : <message>"}` |
