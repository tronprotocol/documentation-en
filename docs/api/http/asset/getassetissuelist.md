# /wallet/getassetissuelist

Query all TRC-10 tokens on the network.

- Source: `framework/src/main/java/org/tron/core/services/http/GetAssetIssueListServlet.java`
- Method: `GET` / `POST`
- Response: `api.AssetIssueList`
- Solidity endpoint: `/walletsolidity/getassetissuelist`

## Request parameters

Both GET and POST read these fields from URL query parameters; the servlet does not parse the POST body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `visible` | GET / POST | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuelist \
     --header 'accept: application/json'
```
## Response

| Field | Type | Description |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | All TRC-10 tokens (structure matches the [`/wallet/createassetissue`](createassetissue.md) request body) |

Response example (the full Nile list is long, only the first item shown; for paging use [`/wallet/getpaginatedassetissuelist`](getpaginatedassetissuelist.md)):

```json
{
  "assetIssue": [
    {
      "owner_address": "417e95e45f5a60cc45f2d0afe37ee9f77fb8ce9fff",
      "name": "74726f6e6c696e6b5f746f6b656e",
      "abbr": "74726f6e6c696e6b5f746f6b656e",
      "total_supply": 1000000000000000,
      "frozen_supply": [{ "frozen_amount": 1, "frozen_days": 1 }],
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "start_time": 1574757000000,
      "end_time": 1757595000000,
      "description": "4465736372697074696f6e",
      "id": "1000001"
    }
    /* ... other tokens */
  ]
}
```

Returns `{}` if there are none.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | Internal node error (failed to read AssetIssue store) | `{"Error": "<exceptionClass> : <message>"}` |
