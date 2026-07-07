# /wallet/getblockbylatestnum

Get the most recent N blocks.

- Source: `framework/src/main/java/org/tron/core/services/http/GetBlockByLatestNumServlet.java`
- Method: `GET` / `POST`
- Request: `api.NumberMessage`
- Solidity endpoint: `/walletsolidity/getblockbylatestnum`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `num` | int64 | Yes | How many of the most recent blocks to fetch (must satisfy `0 < num < 100`, max 99; out-of-range silently returns `{}`) |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbylatestnum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{ "num": 2 }
'
```

## Response

Returns `api.BlockList`; fields are the same as [`/wallet/getblockbylimitnext`](getblockbylimitnext.md).

Response example (the latest 2 Nile blocks, `transactions` body omitted):

```json
{
  "block": [
    {
      "blockID": "0000000003fe266c55d8ec678995cff469dd46ee18671a96f5866f8cb227eed8",
      "block_header": {
        "raw_data": {
          "number": 66987628,
          "txTrieRoot": "1e45d06980078902492470bbce85cf652261f50881503ee81df6fd041af98848",
          "witness_address": "416606973497a56dcfcedb684e60a2386f2ae39db5",
          "parentHash": "0000000003fe266bf6b6d392f654dc2e5011601546ed04623d9fcc4e9d439a25",
          "version": 34,
          "timestamp": 1777445310000
        },
        "witness_signature": "22bb7fdb5cdd33b8eca9104925f0dbd89f65d8e6ee4f7eed6f21d81b1428977e521865406b3ef70abc77b051d930081c2b9e368dc3f2c20c4b5e31187ba945bd00"
      },
      "transactions": [ /* ... */ ]
    },
    {
      "blockID": "0000000003fe266bf6b6d392f654dc2e5011601546ed04623d9fcc4e9d439a25",
      "block_header": { /* ... */ },
      "transactions": [ /* ... */ ]
    }
  ]
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `num` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
