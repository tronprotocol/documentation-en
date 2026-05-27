# /wallet/freezebalancev2

Freeze TRX to obtain bandwidth / energy / TronPower (Stake 2.0). No fixed lock period.

- Source: `framework/src/main/java/org/tron/core/services/http/FreezeBalanceV2Servlet.java`
- Method: `POST`
- Contract: `protocol.FreezeBalanceV2Contract` (`balance_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Freezing account address |
| `frozen_balance` | int64 | Yes | Frozen amount (sun) |
| `resource` | enum | No | `BANDWIDTH` / `ENERGY` / `TRON_POWER`, default `BANDWIDTH` |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/freezebalancev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":  "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "frozen_balance": 1000000000,
  "resource":       "ENERGY"
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, `raw_data_hex` vary with construction moment):

```json
{
  "visible": false,
  "txID": "081256264131fbc9f3d4686aab15ae69c0e77b39d276367c11a7ab13e39747ec",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "resource": "ENERGY",
            "frozen_balance": 1000000000,
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
          },
          "type_url": "type.googleapis.com/protocol.FreezeBalanceV2Contract"
        },
        "type": "FreezeBalanceV2Contract"
      }
    ],
    "ref_block_bytes": "283b",
    "ref_block_hash": "51bf0b88daaaea37",
    "expiration": 1777446819000,
    "timestamp": 1777446761432
  },
  "raw_data_hex": "0a02283b220851bf0b88daaaea3740b8a9d8c0dd335a5b083612570a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e467265657a6542616c616e63655632436f6e7472616374121f0a1541dd791d6b49e190062d650e6a23c575510d35f2f9108094ebdc03180170d8e7d4c0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Proposal #70 `UNFREEZE_DELAY_DAYS` not activated | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support FreezeV2 transaction, need to be opened by the committee"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| `frozen_balance <= 0` | `{"Error": "... : frozenBalance must be positive"}` |
| `frozen_balance < 1_000_000` (less than 1 TRX) | `{"Error": "... : frozenBalance must be greater than or equal to 1 TRX"}` |
| `frozen_balance` exceeds account balance | `{"Error": "... : frozenBalance must be less than or equal to accountBalance"}` |
| `resource = TRON_POWER` but new resource model not enabled | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` |
| Other invalid `resource` (with new resource model enabled) | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY、TRON_POWER]"}` |
| Other invalid `resource` (without new resource model) | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
