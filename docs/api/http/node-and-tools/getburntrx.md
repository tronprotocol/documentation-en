# /wallet/getburntrx

Query the cumulative TRX burned (including transaction fees, contract burns, etc.).

- Source: `framework/src/main/java/org/tron/core/services/http/GetBurnTrxServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getburntrx`

## Request parameters

None.

For GET requests, `int64_as_string=true` may be added to the URL query to return `burnTrxAmount` as a JSON string.

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

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Internal node error (failed to read dynamic properties) | `{"Error": "<exceptionClass> : <message>"}` |
