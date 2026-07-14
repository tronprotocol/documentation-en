# /wallet/getblockbyid

Query a block by block hash.

- Source: `framework/src/main/java/org/tron/core/services/http/GetBlockByIdServlet.java`
- Method: `GET` / `POST`
- Request: `api.BytesMessage`
- Solidity endpoint: `/walletsolidity/getblockbyid`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `value` | GET / POST | string | No | Block hash hex; omitted uses empty bytes for the lookup and returns `{}` |
| `visible` | GET / POST | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "value": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e" }
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

Returns `{}` if the hash does not exist.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `value` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
