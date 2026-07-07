# /wallet/getblockbylimitnext

Get the list of blocks in the range `[startNum, endNum)` (endNum is exclusive).

- Source: `framework/src/main/java/org/tron/core/services/http/GetBlockByLimitNextServlet.java`
- Method: `GET` / `POST`
- Request: `api.BlockLimit`
- Solidity endpoint: `/walletsolidity/getblockbylimitnext`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `startNum` | int64 | Yes | Starting block number (inclusive) |
| `endNum` | int64 | Yes | Ending block number (exclusive) |
| `visible` | bool | No | Format for addresses and text fields |

Constraints: `endNum > startNum` and `endNum - startNum <= 100`.

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbylimitnext \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "startNum": 66987565, "endNum": 66987567 }
'
```

## Response

Returns `api.BlockList`:

| Field | Type | Description |
|---|---|---|
| `block` | repeated Block | Block array |

Response example (`transactions` body omitted):

```json
{
  "block": [
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
      "transactions": [ /* ... */ ]
    },
    {
      "blockID": "0000000003fe262e...",
      "block_header": { /* ... */ },
      "transactions": [ /* ... */ ]
    }
  ]
}
```

Returns `{}` when no blocks are available.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `startNum` / `endNum` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
