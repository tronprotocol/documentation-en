# /wallet/getassetissuebyaccount

Query all TRC-10 tokens issued by an account.

- Source: `framework/src/main/java/org/tron/core/services/http/GetAssetIssueByAccountServlet.java`
- Method: `GET` / `POST`
- Response: `api.AssetIssueList`

## Request parameters

GET reads these fields from URL query parameters; POST reads them from a JSON request body.

| Field | Method | Type | Required | Description |
|---|---|---|---|---|
| `address` | GET | string | Yes | Account address |
| `address` | POST | string | No | Account address; omitted uses the Protobuf empty address and returns `{}` |
| `visible` | GET / POST | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuebyaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41088a2bfcb1c7271029fd69a66859d55560895884"
}
'
```
## Response

| Field | Type | Description |
|---|---|---|
| `assetIssue` | repeated AssetIssueContract | TRC-10 tokens issued by this account (structure in `asset_issue_contract.proto`; fields match the [`/wallet/createassetissue`](createassetissue.md) request body) |

Response example:

```json
{
  "assetIssue": [
    {
      "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
      "name": "54524e",
      "abbr": "544e",
      "total_supply": 100000000000000000,
      "frozen_supply": [{ "frozen_amount": 1, "frozen_days": 1 }],
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
  ]
}
```

Returns `{}` if the account has not issued any token.

### Error responses

| Method | Trigger | Response |
|---|---|---|
| GET / POST | Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| GET / POST | `address` is not valid base58check (`visible=true`) | GET: non-base58 characters → `{"Error": "class java.lang.IllegalArgumentException : <details>"}`; checksum-only error makes `Util.getHexAddress` silently return an empty string, the lookup misses and `{}` is returned. POST (via `JsonFormat.merge`): non-base58 characters → `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, ..."}`; checksum-only error → `{"Error": "class java.lang.NullPointerException : null"}` |
| GET / POST | `address` is not valid hex (`visible=false`) | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| POST | Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| GET / POST | Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
