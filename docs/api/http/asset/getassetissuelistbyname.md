# /wallet/getassetissuelistbyname

Query all TRC-10 tokens with a given name.

- Source: `framework/src/main/java/org/tron/core/services/http/GetAssetIssueListByNameServlet.java`
- Method: `GET` / `POST`
- Response: `api.AssetIssueList`
- Solidity endpoint: `/walletsolidity/getassetissuelistbyname`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Token name (UTF-8 encoded as hex) |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuelistbyname \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "54524e"
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | All tokens with this name |

Response example (Nile name `54524e` decodes to `TRN`; two tokens share this name, first 2 shown):

```json
{
  "assetIssue": [
    {
      "owner_address": "414607716a6ca8fe2dc8f9e27c349a435191e48639",
      "name": "54524e",
      "abbr": "544e",
      "total_supply": 100000000000000000,
      "frozen_supply": [{ "frozen_amount": 1, "frozen_days": 1 }],
      "trx_num": 1,
      "num": 1,
      "start_time": 1737613011138,
      "end_time": 2053134849000,
      "description": "74726964656e74",
      "url": "68747470733a2f2f7777772e74726964656e742e636f6d",
      "free_asset_net_limit": 20,
      "public_free_asset_net_limit": 1,
      "id": "1005415"
    },
    {
      "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
      "name": "54524e",
      "abbr": "544e",
      "total_supply": 100000000000000000,
      "trx_num": 1,
      "precision": 6,
      "num": 1,
      "id": "1005416"
    }
  ]
}
```

Returns `{}` if there is no match.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `value` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : exception decoding Hex string: <details>"}` |
| Request body is not valid JSON (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
