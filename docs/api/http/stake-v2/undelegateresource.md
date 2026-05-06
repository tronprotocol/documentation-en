# /wallet/undelegateresource

Undelegate resources (Stake 2.0) and reclaim the delegated amount.

- Source: `framework/src/main/java/org/tron/core/services/http/UnDelegateResourceServlet.java`
- Method: `POST`
- Contract: `protocol.UnDelegateResourceContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Delegator address |
| `receiver_address` | string | Yes | Receiver address |
| `balance` | int64 | Yes | Frozen amount to undelegate (sun) |
| `resource` | enum | No | `BANDWIDTH` / `ENERGY` |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/undelegateresource \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "receiver_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "balance":          1000000000,
  "resource":         "ENERGY"
}
'
```

## Response

Before construction, the validator checks that there is enough undelegatable delegation between (owner, receiver) under the given `resource`. The example account has no ENERGY delegation to that receiver; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : delegated Resource does not exist"}
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
            "resource":         "ENERGY"
          },
          "type_url": "type.googleapis.com/protocol.UnDelegateResourceContract"
        },
        "type": "UnDelegateResourceContract"
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
| Proposal #70 `UNFREEZE_DELAY_DAYS` not activated | `{"Error": "... : Not support unDelegate resource transaction, need to be opened by the committee"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] does not exist"}` |
| Invalid `receiver_address` | `{"Error": "... : Invalid receiverAddress"}` |
| `receiver_address == owner_address` | `{"Error": "... : receiverAddress must not be the same as ownerAddress"}` |
| No delegation between (owner, receiver) | `{"Error": "... : delegated Resource does not exist"}` |
| `balance <= 0` | `{"Error": "... : unDelegateBalance must be more than 0 TRX"}` |
| Insufficient undelegatable BANDWIDTH (locked-not-yet-matured portion does not count) | `{"Error": "... : insufficient delegatedFrozenBalance(BANDWIDTH), request=<n>, unlock_balance=<m>"}` |
| Insufficient undelegatable ENERGY | `{"Error": "... : insufficient delegateFrozenBalance(Energy), request=<n>, unlock_balance=<m>"}` |
| Invalid `resource` | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
