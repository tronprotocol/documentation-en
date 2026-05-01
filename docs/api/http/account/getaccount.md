# /wallet/getaccount

Query account information.

- Source: `framework/src/main/java/org/tron/core/services/http/GetAccountServlet.java`
- Method: `GET` / `POST`
- Solidity endpoint: `/walletsolidity/getaccount`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `address` | string | Yes | Account address; hex (21 bytes, 0x41 prefix) when `visible=false`, base58check when `visible=true` |
| `visible` | bool | No | Format for addresses and text fields |

POST example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## Response

Returns a `protocol.Account` (see `protocol/src/main/protos/core/Tron.proto`). Common fields:

| Field | Type | Description |
|---|---|---|
| `address` | bytes | Account address |
| `account_name` | bytes | Account name |
| `type` | enum | `Normal` / `AssetIssue` / `Contract` |
| `balance` | int64 | TRX balance (sun, 1 TRX = 1e6 sun) |
| `create_time` | int64 | Creation time, milliseconds |
| `votes` | repeated Vote | Vote records |
| `frozen` | repeated Frozen | Stake 1.0 freezes (bandwidth) |
| `frozenV2` | repeated FreezeV2 | Stake 2.0 freezes |
| `unfrozenV2` | repeated UnFreezeV2 | Stake 2.0 unfreezes in progress |
| `account_resource` | AccountResource | Energy-related |
| `asset` / `assetV2` | map\<string,int64\> | TRC10 holdings |
| `allowance` | int64 | Unwithdrawn witness rewards |
| `latest_opration_time` | int64 | Time of the most recent operation |
| `owner_permission` / `witness_permission` / `active_permission` | Permission | Permission configuration |

Response example:

```json
{
  "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "balance": 1793227200,
  "create_time": 1776933207000,
  "latest_opration_time": 1777444809000,
  "free_net_usage": 441,
  "latest_consume_free_time": 1777431471000,
  "net_window_size": 28800000,
  "net_window_optimized": true,
  "account_resource": {
    "latest_consume_time_for_energy": 1777444809000,
    "energy_window_size": 28800000,
    "energy_window_optimized": true
  },
  "owner_permission": {
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
    ]
  },
  "active_permission": [
    {
      "type": "Active",
      "id": 2,
      "permission_name": "active",
      "threshold": 1,
      "operations": "7fff1fc0033efb0f000000000000000000000000000000000000000000000000",
      "keys": [
        { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9", "weight": 1 }
      ]
    }
  ],
  "frozenV2": [
    {},
    { "type": "ENERGY" },
    { "type": "TRON_POWER" }
  ],
  "assetV2": [
    { "key": "1005416", "value": 100000000 }
  ],
  "free_asset_net_usageV2": [
    { "key": "1005416", "value": 0 }
  ],
  "asset_optimized": true
}
```

Returns `{}` if `address` is missing or the account does not exist.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `address` is not valid hex (`visible=false`) | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID hex String"}` |
| `address` is not valid base58check (`visible=true`) | Non-base58 characters → `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <pos>: INVALID base58 String, <details>"}`; checksum-only error → `{"Error": "class java.lang.NullPointerException : null"}` (GET and POST behave identically: the GET path wraps `address` into JSON and goes through the same `JsonFormat.merge`) |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
