# /wallet/getdelegatedresourceaccountindexv2

Query the list of delegation counterparties for an account, both as lender and receiver (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceAccountIndexV2Servlet.java`
- Method: `GET` / `POST`
- Response: `protocol.DelegatedResourceAccountIndex`
- Solidity endpoint: `/walletsolidity/getdelegatedresourceaccountindexv2`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `value` | GET | string | Yes | Account address to query |
| `value` | POST | string | No | Account address; omitted uses empty bytes and returns the default empty result |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresourceaccountindexv2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```
## Response

Same fields as [`/wallet/getdelegatedresourceaccountindex`](../stake-v1/getdelegatedresourceaccountindex.md) (Stake 2.0 data).

Response example (the account neither delegates to others nor receives delegations; only `account` is returned; `fromAccounts` and `toAccounts` are proto default empty lists):

```json
{
  "account": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
```

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `value` is not valid base58check (`visible=true`) | With non-base58 characters: `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; if only the checksum is wrong, `Util.getHexAddress` silently returns null → no record found, returns `{}` (GET and POST behave identically; POST converts base58 → hex before merge) |
| GET / POST | `value` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
