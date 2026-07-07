# /wallet/createassetissue

Build a TRC-10 token issuance transaction.

- Source: `framework/src/main/java/org/tron/core/services/http/CreateAssetIssueServlet.java`
- Method: `POST`
- Contract: `protocol.AssetIssueContract` (`asset_issue_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Issuer address |
| `name` | string | Yes | Token name (UTF-8 encoded as hex) |
| `abbr` | string | No | Abbreviation (UTF-8 encoded as hex) |
| `total_supply` | int64 | Yes | Total supply |
| `frozen_supply` | repeated FrozenSupply | No | Frozen portion; element `{frozen_amount, frozen_days}` |
| `trx_num` | int32 | Yes | Exchange ratio denominator (trx_num TRX = num tokens) |
| `num` | int32 | Yes | Exchange ratio numerator |
| `precision` | int32 | No | Precision |
| `start_time` | int64 | Yes | Fundraising start time, milliseconds |
| `end_time` | int64 | Yes | Fundraising end time, milliseconds |
| `description` | string | No | Description (UTF-8 hex) |
| `url` | string | Yes | Project URL (UTF-8 hex, ≤ 256 bytes) |
| `free_asset_net_limit` | int64 | No | Per-account free bandwidth quota for this token |
| `public_free_asset_net_limit` | int64 | No | Public free bandwidth quota for this token |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createassetissue \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "name": "44494345",
  "abbr": "44494345",
  "total_supply": 1000000000,
  "trx_num": 1,
  "num": 1,
  "start_time": 1900000000000,
  "end_time": 2000000000000,
  "description": "44494345",
  "url": "68747470733a2f2f747261782e696f"
}
'
```

## Response

Returns an unsigned `protocol.Transaction`. Once on chain, an `assetIssueID` is assigned and visible in `TransactionInfo.assetIssueID`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction; `start_time` must be later than the current block time):

```json
{
  "visible": false,
  "txID": "a9c125300a5e5c6fa9490ab599b3f37db756aa1e421d883167955c91e4cfe409",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "name": "44494345",
            "abbr": "44494345",
            "total_supply": 1000000000,
            "trx_num": 1,
            "num": 1,
            "start_time": 1900000000000,
            "end_time": 2000000000000,
            "description": "44494345",
            "url": "68747470733a2f2f747261782e696f"
          },
          "type_url": "type.googleapis.com/protocol.AssetIssueContract"
        },
        "type": "AssetIssueContract"
      }
    ],
    "ref_block_bytes": "275a",
    "ref_block_hash": "8aeea897e90cdc79",
    "expiration": 1777446138000,
    "timestamp": 1777446080622
  },
  "raw_data_hex": "0a02275a22088aeea897e90cdc794090e1aec0dd335a8c0108061287010a2f747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e41737365744973737565436f6e747261637412540a1541dd791d6b49e190062d650e6a23c575510d35f2f91204444943451a0444494345208094ebdc03300140014880f0cc86a6375080c0a8ca9a3aa2010444494345aa010f68747470733a2f2f747261782e696f70eea0abc0dd33"
}
```

Cost: issuing a TRC-10 burns a sizable amount of TRX (governed by chain parameter `getAssetIssueFee`, currently 1024 TRX).

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| Invalid `name` (empty, length > 32, or contains illegal characters) | `{"Error": "... : Invalid assetName"}` |
| `name` decodes to "trx" | `{"Error": "... : assetName can't be trx"}` |
| `precision` exceeds 6 | `{"Error": "... : precision cannot exceed 6"}` |
| Invalid `abbr` | `{"Error": "... : Invalid abbreviation for token"}` |
| Invalid `url` | `{"Error": "... : Invalid url"}` |
| Invalid `description` (length too long) | `{"Error": "... : Invalid description"}` |
| `start_time` missing | `{"Error": "... : Start time should be not empty"}` |
| `end_time` missing | `{"Error": "... : End time should be not empty"}` |
| `end_time <= start_time` | `{"Error": "... : End time should be greater than start time"}` |
| `start_time <= current block time` | `{"Error": "... : Start time should be greater than HeadBlockTime"}` |
| Token with the same name already exists | `{"Error": "... : Token exists"}` |
| `total_supply <= 0` | `{"Error": "... : TotalSupply must greater than 0!"}` |
| `trx_num <= 0` | `{"Error": "... : TrxNum must greater than 0!"}` |
| `num <= 0` | `{"Error": "... : Num must greater than 0!"}` |
| `public_free_asset_net_usage` not 0 | `{"Error": "... : PublicFreeAssetNetUsage must be 0!"}` |
| `frozen_supply` list too long | `{"Error": "... : Frozen supply list length is too long"}` |
| Invalid `free_asset_net_limit` | `{"Error": "... : Invalid FreeAssetNetLimit"}` |
| Invalid `public_free_asset_net_limit` | `{"Error": "... : Invalid PublicFreeAssetNetLimit"}` |
| `frozen_amount <= 0` | `{"Error": "... : Frozen supply must be greater than 0!"}` |
| Sum of `frozen_amount` exceeds `total_supply` | `{"Error": "... : Frozen supply cannot exceed total supply"}` |
| `frozen_days` out of valid range | `{"Error": "... : frozenDuration must be less than <max> days and more than <min> days"}` |
| `start_time + frozen_days` overflows | `{"Error": "... : Start time and frozen days would cause expire time overflow"}` |
| `owner_address` account does not exist | `{"Error": "... : Account not exists"}` |
| Account has already issued a token | `{"Error": "... : An account can only issue one asset"}` |
| Insufficient balance for the issuance fee | `{"Error": "... : No enough balance for fee!"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
