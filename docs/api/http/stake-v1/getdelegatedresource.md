# /wallet/getdelegatedresource

> **Legacy lookup**: Returns only Stake 1.0 delegation records; does not work with V2 data. There is no version gate in the source, so it can still be called after V2 is enabled to look up legacy V1 positions. For new use cases, use [`/wallet/getdelegatedresourcev2`](../stake-v2/getdelegatedresourcev2.md).

Query all resource delegation records from→to (Stake 1.0).

- Source: `framework/src/main/java/org/tron/core/services/http/GetDelegatedResourceServlet.java`
- Method: `GET` / `POST`
- Response: `api.DelegatedResourceList`
- Solidity endpoint: `/walletsolidity/getdelegatedresource`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `fromAddress` | string | Yes | Resource lender address |
| `toAddress` | string | Yes | Resource receiver address |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getdelegatedresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "fromAddress": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "toAddress":   "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `delegatedResource` | repeated DelegatedResource | Delegation record list |

`DelegatedResource` fields:

| Field | Type | Description |
|---|---|---|
| `from` | string | Delegator |
| `to` | string | Receiver |
| `frozen_balance_for_bandwidth` | int64 | Frozen amount delegated for bandwidth |
| `frozen_balance_for_energy` | int64 | Frozen amount delegated for energy |
| `expire_time_for_bandwidth` | int64 | Bandwidth delegation expiry |
| `expire_time_for_energy` | int64 | Energy delegation expiry |

Response example (no V1 delegation between the example accounts on Nile, returns empty object):

```json
{}
```

Response when V1 delegation exists:

```json
{
  "delegatedResource": [
    {
      "from": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
      "to":   "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
      "frozen_balance_for_energy": 1000000000,
      "expire_time_for_energy":    1700000000000
    }
  ]
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `fromAddress` / `toAddress` is not valid base58check (`visible=true`) | GET: with non-base58 characters, throws `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; if only the checksum is wrong, `Util.getHexAddress` silently returns empty string → no record found, returns `{}`. POST (via `JsonFormat.merge`): with non-base58 characters, throws `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`; if only the checksum is wrong, throws `{"Error": "class java.lang.NullPointerException : null"}` |
| `fromAddress` / `toAddress` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
