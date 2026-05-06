# /wallet/getblockbynum

Query a block by block number.

- Source: `framework/src/main/java/org/tron/core/services/http/GetBlockByNumServlet.java`
- Method: `GET` / `POST`
- Request: `api.NumberMessage`
- Solidity endpoint: `/walletsolidity/getblockbynum`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `num` | int64 | Yes | Block number |
| `visible` | bool | No | Format for addresses and text fields |

GET example: `/wallet/getblockbynum?num=66987565`

POST example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbynum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "num": 66987565 }
'
```

## Response

Returns `protocol.Block`; fields are the same as [`/wallet/getnowblock`](getnowblock.md).

Response example (`transactions` body omitted):

```json
{
  "blockID": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
  "block_header": {
    "raw_data": {
      "number": 66987565,
      "txTrieRoot": "faf8fe3858339ead25cc892461c82a59b84dca4a51c45b026676bf3f45a352a2",
      "witness_address": "41b2f713d57dbcec679d93a8849fa0cd0e4db594ba",
      "parentHash": "0000000003fe262c85cd6b02033f4c3e5c1efa35de256a17bd906dc61fb1aeed",
      "version": 34,
      "timestamp": 1777445121000
    },
    "witness_signature": "5b3cf6cb15d52947989f7726f4907a144b39ccd667a1a0f98707b40cdfe65b96173ddf34ae8dcc5e78f136e0cf903a15c7128984aa2191f02333209d1879d3f900"
  },
  "transactions": [ /* see /wallet/gettransactionbyid for a single-transaction example */ ]
}
```

Returns `{}` if the block number does not exist.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `num` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
