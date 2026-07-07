# /wallet/transferasset

TRC-10 token transfer.

- Source: `framework/src/main/java/org/tron/core/services/http/TransferAssetServlet.java`
- Method: `POST`
- Contract: `protocol.TransferAssetContract` (`asset_issue_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Sender |
| `to_address` | string | Yes | Recipient |
| `asset_name` | string | Yes | Token id (since the `ALLOW_SAME_TOKEN_NAME` proposal, this is the token id as a string, e.g. `1000001`, encoded as UTF-8 hex) |
| `amount` | int64 | Yes | Amount in the smallest unit |
| `extra_data` | string | No | Memo (hex; UTF-8 text when `visible=true`) |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/transferasset \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "to_address":    "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "asset_name":    "31303035343136",
  "amount": 100
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`asset_name` `31303035343136` decodes to token id `1005416`; `txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction):

```json
{
  "visible": false,
  "txID": "7a8b50753079977b2cc0ddc19309c568e5bcaa8d2d865b3d96b40719b1b8df6f",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount": 100,
            "asset_name": "31303035343136",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "to_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
          },
          "type_url": "type.googleapis.com/protocol.TransferAssetContract"
        },
        "type": "TransferAssetContract"
      }
    ],
    "ref_block_bytes": "2765",
    "ref_block_hash": "d2e724f76534cfc4",
    "expiration": 1777446171000,
    "timestamp": 1777446111063
  },
  "raw_data_hex": "0a0227652208d2e724f76534cfc440f8e2b0c0dd335a730802126f0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e736665724173736574436f6e747261637412390a0731303035343136121541dd791d6b49e190062d650e6a23c575510d35f2f91a154192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a206470d78eadc0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| Invalid `to_address` | `{"Error": "... : Invalid toAddress"}` |
| `amount <= 0` | `{"Error": "... : Amount must be greater than 0."}` |
| Transfer to self | `{"Error": "... : Cannot transfer asset to yourself."}` |
| owner account does not exist | `{"Error": "... : No owner account!"}` |
| Token does not exist | `{"Error": "... : No asset!"}` |
| owner has no balance for this token | `{"Error": "... : assetBalance must be greater than 0."}` |
| owner balance for this token is insufficient | `{"Error": "... : assetBalance is not sufficient."}` |
| Recipient is a contract address (after proposal #41) | `{"Error": "... : Cannot transfer asset to smartContract."}` |
| Balance addition overflow | `{"Error": "... : long overflow"}` |
| Recipient does not exist and owner balance is insufficient for the account-creation fee | `{"Error": "... : Validate TransferAssetActuator error, insufficient fee."}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
