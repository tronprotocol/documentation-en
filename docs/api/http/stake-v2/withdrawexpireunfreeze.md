# /wallet/withdrawexpireunfreeze

Withdraw matured unfreeze TRX to balance (Stake 2.0).

- Source: `framework/src/main/java/org/tron/core/services/http/WithdrawExpireUnfreezeServlet.java`
- Method: `POST`
- Contract: `protocol.WithdrawExpireUnfreezeContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Account address |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/withdrawexpireunfreeze \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
}
'
```

## Response

Before construction, the validator checks that the account has matured unfreeze entries. The example account has none; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : no unFreeze balance to withdraw "}
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
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
          },
          "type_url": "type.googleapis.com/protocol.WithdrawExpireUnfreezeContract"
        },
        "type": "WithdrawExpireUnfreezeContract"
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
| Proposal #70 `UNFREEZE_DELAY_DAYS` not activated | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support WithdrawExpireUnfreeze transaction, need to be opened by the committee"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| No matured withdrawable unfreeze balance | `{"Error": "... : no unFreeze balance to withdraw "}` |
| Balance accumulation overflow | `{"Error": "... : <ArithmeticException message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
