# /wallet/updateasset

Update a TRC10 token's description, URL, and bandwidth limits (issuer-only).

- Source: `framework/src/main/java/org/tron/core/services/http/UpdateAssetServlet.java`
- Method: `POST`
- Contract: `protocol.UpdateAssetContract` (`asset_issue_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Issuer address |
| `description` | string | No | New description (UTF-8 hex) |
| `url` | string | No | New URL (UTF-8 hex) |
| `new_limit` | int64 | No | Per-account free bandwidth quota |
| `new_public_limit` | int64 | No | Public free bandwidth quota |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updateasset \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41088a2bfcb1c7271029fd69a66859d55560895884",
  "description":      "44494345",
  "url":              "68747470733a2f2f747261782e696f",
  "new_limit":        5000,
  "new_public_limit": 10000
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction):

```json
{
  "visible": false,
  "txID": "6c1b46170308da102f2b70b4976ead59b3c9c02bba044c18da27f7e25779e10d",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884",
            "description": "44494345",
            "url": "68747470733a2f2f747261782e696f",
            "new_limit": 5000,
            "new_public_limit": 10000
          },
          "type_url": "type.googleapis.com/protocol.UpdateAssetContract"
        },
        "type": "UpdateAssetContract"
      }
    ],
    "ref_block_bytes": "2799",
    "ref_block_hash": "0734893a1ba1ff5e",
    "expiration": 1777446327000,
    "timestamp": 1777446269173
  },
  "raw_data_hex": "0a02279922080734893a1ba1ff5e40d8a5bac0dd335a6c080f12680a30747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5570646174654173736574436f6e747261637412340a1541088a2bfcb1c7271029fd69a66859d555608958841204444943451a0f68747470733a2f2f747261782e696f20882728904e70f5e1b6c0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| Account does not exist | `{"Error": "... : Account does not exist"}` |
| Account has not issued any token (V1) | `{"Error": "... : Account has not issued any asset"}` |
| Token not found in AssetIssueStore (V1) | `{"Error": "... : Asset is not existed in AssetIssueStore"}` |
| Token not found in AssetIssueV2Store | `{"Error": "... : Asset is not existed in AssetIssueV2Store"}` |
| Invalid `url` | `{"Error": "... : Invalid url"}` |
| Invalid `description` | `{"Error": "... : Invalid description"}` |
| Invalid `new_limit` | `{"Error": "... : Invalid FreeAssetNetLimit"}` |
| Invalid `new_public_limit` | `{"Error": "... : Invalid PublicFreeAssetNetLimit"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
