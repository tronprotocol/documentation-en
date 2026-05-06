# /wallet/delegateresource

Delegate already-frozen resources to another account (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/DelegateResourceServlet.java`
- Method: `POST`
- Contract: `protocol.DelegateResourceContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Delegator address |
| `receiver_address` | string | Yes | Receiver address |
| `balance` | int64 | Yes | Frozen amount to delegate (sun) |
| `resource` | enum | No | `BANDWIDTH` / `ENERGY` |
| `lock` | bool | No | Whether the delegation is locked (cannot be undelegated early when true) |
| `lock_period` | int64 | No | Lock duration (block count, only when `lock=true`) |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/delegateresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "receiver_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "balance":          1000000000,
  "resource":         "ENERGY",
  "lock":             false
}
'
```

## Response

Before construction, the validator checks that owner's currently delegatable amount under the given `resource` covers `balance`. The example account has no delegatable ENERGY; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : delegateBalance must be less than or equal to available FreezeEnergyV2 balance"}
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
            "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "receiver_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
            "balance":          1000000000,
            "resource":         "ENERGY",
            "lock":             false
          },
          "type_url": "type.googleapis.com/protocol.DelegateResourceContract"
        },
        "type": "DelegateResourceContract"
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
| Chain has not enabled resource delegation | `{"Error": "class org.tron.core.exception.ContractValidateException : No support for resource delegate"}` |
| Proposal #70 `UNFREEZE_DELAY_DAYS` not activated | `{"Error": "... : Not support Delegate resource transaction, need to be opened by the committee"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| `balance < 1_000_000` (less than 1 TRX) | `{"Error": "... : delegateBalance must be greater than or equal to 1 TRX"}` |
| Insufficient delegatable BANDWIDTH | `{"Error": "... : delegateBalance must be less than or equal to available FreezeBandwidthV2 balance"}` |
| Insufficient delegatable ENERGY | `{"Error": "... : delegateBalance must be less than or equal to available FreezeEnergyV2 balance"}` |
| Invalid `resource` | `{"Error": "... : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` |
| Invalid `receiver_address` | `{"Error": "... : Invalid receiverAddress"}` |
| `receiver_address == owner_address` | `{"Error": "... : receiverAddress must not be the same as ownerAddress"}` |
| receiver account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| `lock_period` out of range (after proposal #76) | `{"Error": "... : The lock period of delegate resource cannot be less than 0 and cannot exceed <max>!"}` |
| Existing locked delegation still in lock period and the new lock period is shorter | `{"Error": "... : The lock period for <Resource> this time cannot be less than the remaining time[<n>ms] of the last lock period for <Resource>!"}` |
| receiver is a contract address | `{"Error": "... : Do not allow delegate resources to contract addresses"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
