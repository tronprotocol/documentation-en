# /wallet/unfreezeasset

Unfreeze the issuer's `frozen_supply` portion (issuer-only; only succeeds after the freeze period matures).

- Source: `framework/src/main/java/org/tron/core/services/http/UnFreezeAssetServlet.java`
- Method: `POST`
- Contract: `protocol.UnfreezeAssetContract` (`asset_issue_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | TRC-10 issuer address |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/unfreezeasset \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884"
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction):

```json
{
  "visible": false,
  "txID": "bd5088fe645fbbaf7e4410a170e78d9645ecaa1c52f457fa9635a76ddc74276b",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41088a2bfcb1c7271029fd69a66859d55560895884"
          },
          "type_url": "type.googleapis.com/protocol.UnfreezeAssetContract"
        },
        "type": "UnfreezeAssetContract"
      }
    ],
    "ref_block_bytes": "2799",
    "ref_block_hash": "0734893a1ba1ff5e",
    "expiration": 1777446327000,
    "timestamp": 1777446268128
  },
  "raw_data_hex": "0a02279922080734893a1ba1ff5e40d8a5bac0dd335a51080e124d0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e556e667265657a654173736574436f6e747261637412170a1541088a2bfcb1c7271029fd69a66859d5556089588470e0d9b6c0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] does not exist"}` |
| No frozen supply (`frozen_supply` is empty) | `{"Error": "... : no frozen supply balance"}` |
| Account has never issued a token | `{"Error": "... : this account has not issued any asset"}` |
| Nothing has matured | `{"Error": "... : It's not time to unfreeze asset supply"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
