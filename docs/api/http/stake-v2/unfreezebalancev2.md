# /wallet/unfreezebalancev2

Initiate an unfreeze request (Stake 2.0). Enters a 14-day waiting period; after maturity, withdraw via [`/wallet/withdrawexpireunfreeze`](withdrawexpireunfreeze.md).

- Source: `framework/src/main/java/org/tron/core/services/http/UnFreezeBalanceV2Servlet.java`
- Method: `POST`
- Contract: `protocol.UnfreezeBalanceV2Contract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Unfreezing account address |
| `unfreeze_balance` | int64 | Yes | Unfreeze amount (sun) |
| `resource` | enum | No | `BANDWIDTH` / `ENERGY` / `TRON_POWER` |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/unfreezebalancev2 \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "unfreeze_balance": 1000000000,
  "resource":         "ENERGY"
}
'
```

## Response

Before construction, the validator checks that owner has enough frozen balance under the given `resource`. The example account has no V2 ENERGY freeze; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(Energy)"}
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
            "unfreeze_balance": 1000000000,
            "resource":         "ENERGY"
          },
          "type_url": "type.googleapis.com/protocol.UnfreezeBalanceV2Contract"
        },
        "type": "UnfreezeBalanceV2Contract"
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
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Proposal #70 `UNFREEZE_DELAY_DAYS` not activated | `{"Error": "class org.tron.core.exception.ContractValidateException : Not support UnfreezeV2 transaction, need to be opened by the committee"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] does not exist"}` |
| `resource = BANDWIDTH` but no corresponding freeze | `{"Error": "... : no frozenBalance(BANDWIDTH)"}` |
| `resource = ENERGY` but no corresponding freeze | `{"Error": "... : no frozenBalance(Energy)"}` |
| `resource = TRON_POWER` (with new resource model) but no corresponding freeze | `{"Error": "... : no frozenBalance(TronPower)"}` |
| `resource = TRON_POWER` but new resource model not enabled | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` |
| Other invalid `resource` (with new resource model enabled) | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy、TRON_POWER]"}` |
| Other invalid `resource` (without new resource model) | `{"Error": "... : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` |
| Invalid `unfreeze_balance` (≤0, exceeds available, outstanding delegations not yet recalled, etc.) | `{"Error": "... : Invalid unfreeze_balance, [<n>] is error"}` |
| Concurrent unfreeze count exceeds `UNFREEZE_MAX_TIMES` | `{"Error": "... : Invalid unfreeze operation, unfreezing times is over limit"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
