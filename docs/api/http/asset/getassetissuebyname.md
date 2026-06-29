# /wallet/getassetissuebyname

Look up a single TRC-10 by name. **Note**: since the `ALLOW_SAME_TOKEN_NAME` proposal, names are no longer unique — this endpoint errors when duplicates exist; prefer [`/wallet/getassetissuebyid`](getassetissuebyid.md) or [`/wallet/getassetissuelistbyname`](getassetissuelistbyname.md).

- Source: `framework/src/main/java/org/tron/core/services/http/GetAssetIssueByNameServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getassetissuebyname`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Token name (UTF-8 encoded as hex) |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getassetissuebyname \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "303044696365"
}
'
```

## Response

Returns a `protocol.AssetIssueContract`; fields match the [`/wallet/createassetissue`](createassetissue.md) request body.

Response example (Nile token name `303044696365` decodes to `00Dice`):

```json
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
}
```

Returns `{}` if not found.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `value` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : exception decoding Hex string: <details>"}` |
| More than one token with this name (after `ALLOW_SAME_TOKEN_NAME`) | `{"Error": "class org.tron.core.exception.NonUniqueObjectException : To get more than one asset, please use getAssetIssueById syntax"}` |
| Request body is not valid JSON (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
