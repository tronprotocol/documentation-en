# /wallet/getdelegatedresourceaccountindexv2

Query the list of delegation counterparties for an account, both as lender and receiver (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceAccountIndexV2Servlet.java`
- Method: `GET` / `POST`
- Response: `protocol.DelegatedResourceAccountIndex`
- Solidity endpoint: `/walletsolidity/getdelegatedresourceaccountindexv2`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Account address to query |
| `visible` | bool | No | Address format |

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

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `value` is not valid base58check (`visible=true`) | With non-base58 characters: `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; if only the checksum is wrong, `Util.getHexAddress` silently returns null → no record found, returns `{}` (GET and POST behave identically; POST converts base58 → hex before merge) |
| `value` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| Request body is not valid JSON (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
