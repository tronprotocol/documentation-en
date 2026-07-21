# /wallet/getblock

Query a block by number or hash, optionally returning the full transaction list. Unified replacement for `getnowblock` / `getblockbynum` / `getblockbyid`.

- Source: `framework/src/main/java/org/tron/core/services/http/GetBlockServlet.java`
- Method: `GET` / `POST`
- Request: `api.BlockReq`
- Solidity endpoint: `/walletsolidity/getblock`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `id_or_num` | GET / POST | string | No | Block number (decimal string) or block hash hex; empty returns the latest block |
| `detail` | GET / POST | bool | No | Whether to return full `transactions`; if false only the header is returned (default false) |
| `visible` | GET / POST | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblock \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "id_or_num": "66987565", "detail": false }
'
```
## Response

Returns `protocol.Block` (whether `transactions` is populated depends on `detail`); fields are the same as [`/wallet/getnowblock`](getnowblock.md).

Response example (`detail=false`, `transactions` omitted):

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
  }
}
```

Returns `{}` if not found.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| POST | Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | `id_or_num` is negative | `{"Error": "num must be non-positive number."}` |
| GET / POST | `id_or_num` length is not 64 (not a valid block hash length) | `{"Error": "id must be legal block hash."}` |
| GET / POST | `id_or_num` is hex but parsing fails / hash cannot be resolved to a block number | `{"Error": "id must be legal block hash."}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
