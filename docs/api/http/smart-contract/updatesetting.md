# /wallet/updatesetting

Update a contract's `consume_user_resource_percent` (deployer only).

- Source: `framework/src/main/java/org/tron/core/services/http/UpdateSettingServlet.java`
- Method: `POST`
- Contract: `protocol.UpdateSettingContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Deployer address |
| `contract_address` | string | Yes | Contract address |
| `consume_user_resource_percent` | int64 | Yes | Caller-paid energy percentage 0–100 |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updatesetting \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":                 "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address":              "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
  "consume_user_resource_percent": 100
}
'
```

## Response

Before construction, the servlet validates that `owner_address` is the contract deployer. The example `owner_address` is not the TetherToken deployer; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : Account[41dd791d6b49e190062d650e6a23c575510d35f2f9] is not the owner of the contract"}
```

When validation passes, returns an unsigned `protocol.Transaction`. Structure outline (`txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` semantics are the same as [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)):

```json
{
  "visible": false,
  "txID": "<computed from raw_data>",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
              "owner_address":                 "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address":              "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f",
              "consume_user_resource_percent": 100
          },
          "type_url": "type.googleapis.com/protocol.UpdateSettingContract"
        },
        "type": "UpdateSettingContract"
      }
    ],
    "ref_block_bytes": "<latest solidified block at construction time>",
    "ref_block_hash":  "<latest solidified block at construction time>",
    "expiration":      "<timestamp + 60_000>",
    "timestamp":       "<construction moment>"
  },
  "raw_data_hex": "<protobuf encoding of raw_data>"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] does not exist"}` |
| `consume_user_resource_percent` not in [0, 100] | `{"Error": "... : percent not in [0, 100]"}` |
| Contract address does not exist | `{"Error": "... : Contract does not exist"}` |
| owner is not the contract deployer | `{"Error": "... : Account[<address>] is not the owner of the contract"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
