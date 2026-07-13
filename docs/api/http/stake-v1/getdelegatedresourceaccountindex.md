# /wallet/getdelegatedresourceaccountindex

> **Legacy lookup**: Returns only Stake 1.0 delegation counterparty index; does not work with V2 data. There is no version gate in the source, so it can still be called after V2 is enabled to look up legacy V1 positions. For new use cases, use [`/wallet/getdelegatedresourceaccountindexv2`](../stake-v2/getdelegatedresourceaccountindexv2.md).

Query the list of delegation counterparties for an account, both as lender and receiver (Stake 1.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceAccountIndexServlet.java`
- Method: `GET` / `POST`
- Response: `protocol.DelegatedResourceAccountIndex`
- Solidity endpoint: `/walletsolidity/getdelegatedresourceaccountindex`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `value` | GET / POST | string | Yes | Account address to query |
| `visible` | GET / POST | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresourceaccountindex \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `account` | string | Queried account |
| `fromAccounts` | repeated string | Accounts that delegate resources to me |
| `toAccounts` | repeated string | Accounts to which I delegate resources |

Response example (the example account has no V1 counterparties; proto default empty arrays are not serialized):

```json
{
  "account": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
```

Response when V1 counterparties exist:

```json
{
  "account":      "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "fromAccounts": [],
  "toAccounts":   ["4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"]
}
```

Returns `{}` when there are no records at all.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `value` is not valid base58check (`visible=true`) | With non-base58 characters: `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; if only the checksum is wrong, `Util.getHexAddress` silently returns null → no record found, returns `{}` (GET and POST behave identically; POST converts base58 → hex before merge) |
| GET / POST | `value` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
