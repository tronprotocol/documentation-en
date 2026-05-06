# /wallet/getburntrx

Query the cumulative TRX burned (including transaction fees, contract burns, etc.).

- Source: `framework/src/main/java/org/tron/core/services/http/GetBurnTrxServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getburntrx`

## Request parameters

None.

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

### Error responses

| Trigger | Response |
|---|---|
| Internal node error (failed to read dynamic properties) | `{"Error": "<exceptionClass> : <message>"}` |
