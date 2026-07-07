# /wallet/getassetissuebyid

Look up a TRC-10 by token id (recommended — token ids are globally unique).

- Source: `framework/src/main/java/org/tron/core/services/http/GetAssetIssueByIdServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getassetissuebyid`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Token id (numeric string, e.g. `"1000001"`) |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuebyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "1005416"
}
'
```

## Response

Returns a `protocol.AssetIssueContract`; fields match the [`/wallet/createassetissue`](createassetissue.md) request body.

Response example (Nile token id `1005416`, name `54524e` decodes to `TRN`):

```json
{
  "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
  "name": "54524e",
  "abbr": "544e",
  "total_supply": 100000000000000000,
  "frozen_supply": [
    { "frozen_amount": 1, "frozen_days": 1 }
  ],
  "trx_num": 1,
  "precision": 6,
  "num": 1,
  "start_time": 1737690890434,
  "end_time": 2053134849000,
  "vote_score": 1,
  "description": "7465737420747263313020636f696e20666f72206e696c65",
  "url": "68747470733a2f2f6e696c6565782e696f2f",
  "free_asset_net_limit": 10000,
  "public_free_asset_net_limit": 20000,
  "id": "1005416"
}
```

Returns `{}` if not found.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
