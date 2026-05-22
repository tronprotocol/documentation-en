# /wallet/getpaginatedassetissuelist

Query TRC10 tokens with pagination.

- Source: `framework/src/main/java/org/tron/core/services/http/GetPaginatedAssetIssueListServlet.java`
- Method: `GET` / `POST`
- Response: `api.AssetIssueList`
- Solidity endpoint: `/walletsolidity/getpaginatedassetissuelist`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `offset` | int64 | No | Starting offset; defaults to `0` |
| `limit` | int64 | No | Number of records to return; defaults to `0`, which returns an empty list |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getpaginatedassetissuelist \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "offset": 0,
  "limit": 2
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | Paginated token list |

Response example (Nile, limit=2):

```json
{
  "assetIssue": [
    {
      "owner_address": "41a8a906cd9d5e7ff3e472d34ca568441ceeb4cf5b",
      "name": "303044696365",
      "abbr": "307830",
      "total_supply": 1000000000000000000,
      "trx_num": 1000000,
      "precision": 6,
      "num": 100000000,
      "start_time": 1592841600000,
      "end_time": 1592928000000,
      "description": "e794a8e4ba8ee6b58be8af95",
      "url": "68747470733a2f2f7777772e62616964752e636f6d",
      "id": "1000052"
    },
    {
      "owner_address": "41f18b0c6d290d57464aeddeb98f429c9dd318e31e",
      "name": "3031303031313031303130313031",
      "abbr": "3031303031313031303130313031",
      "total_supply": 1000000,
      "frozen_supply": [{ "frozen_amount": 1000, "frozen_days": 2 }],
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "start_time": 1663344000000,
      "end_time": 1694880000000,
      "description": "e68f8fe8bfb0",
      "url": "75726c33",
      "free_asset_net_limit": 1000,
      "public_free_asset_net_limit": 1000,
      "id": "1004963"
    }
  ]
}
```

Returns `{}` if there are no results.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `offset` / `limit` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
