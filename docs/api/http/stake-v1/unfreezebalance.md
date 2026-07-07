# /wallet/unfreezebalance

> **Legacy still active**: Unlike `freezebalance`, this endpoint **still works after Stake 2.0 is enabled** — `UnfreezeBalanceActuator` has no `supportUnfreezeDelay` gate, and legacy V1 positions still need to be unfrozen through it. For new use cases, use [`/wallet/unfreezebalancev2`](../stake-v2/unfreezebalancev2.md).

Unfreeze matured Stake 1.0 assets.

- Source: `framework/src/main/java/org/tron/core/services/http/UnFreezeBalanceServlet.java`
- Method: `POST`
- Contract: `protocol.UnfreezeBalanceContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Account to unfreeze |
| `resource` | enum | No | `BANDWIDTH` / `ENERGY`, default `BANDWIDTH` |
| `receiver_address` | string | No | Delegation target address (when undelegating) |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/unfreezebalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "resource":      "BANDWIDTH"
}
'
```

## Response

Before construction, the validator checks that the account has matured V1 freeze/delegation records. The example account has no V1 freeze on BANDWIDTH; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(BANDWIDTH)"}
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
              "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "resource":      "BANDWIDTH"
          },
          "type_url": "type.googleapis.com/protocol.UnfreezeBalanceContract"
        },
        "type": "UnfreezeBalanceContract"
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
| `owner_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| `owner_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] does not exist"}` |
| `receiver_address == owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : receiverAddress must not be the same as ownerAddress"}` |
| `receiver_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid receiverAddress"}` |
| `receiver_address` is set but `AllowTvmConstantinople=0` and the receiver account does not exist | `{"Error": "class org.tron.core.exception.ContractValidateException : Receiver Account[<addr>] does not exist"}` |
| `receiver_address` is set but no delegation record exists from owner→receiver | `{"Error": "class org.tron.core.exception.ContractValidateException : delegated Resource does not exist"}` |
| Undelegating `BANDWIDTH` but the delegation record's bandwidth frozen amount is 0 | `{"Error": "class org.tron.core.exception.ContractValidateException : no delegatedFrozenBalance(BANDWIDTH)"}` |
| Undelegating `ENERGY` but the delegation record's energy frozen amount is 0 | `{"Error": "class org.tron.core.exception.ContractValidateException : no delegateFrozenBalance(Energy)"}` |
| Receiver's used resource is less than the delegated amount when undelegating (invariant violation) | `{"Error": "class org.tron.core.exception.ContractValidateException : AcquiredDelegatedFrozenBalanceFor<Resource>[<X>] < delegated<Resource>[<Y>]"}` |
| Undelegating but the delegation has not yet matured | `{"Error": "class org.tron.core.exception.ContractValidateException : It's not time to unfreeze."}` |
| Self-unfreeze `BANDWIDTH` but no BANDWIDTH freeze on the account | `{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(BANDWIDTH)"}` |
| Self-unfreeze `BANDWIDTH` but none of the records have matured | `{"Error": "class org.tron.core.exception.ContractValidateException : It's not time to unfreeze(BANDWIDTH)."}` |
| Self-unfreeze `ENERGY` but no ENERGY freeze on the account | `{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(Energy)"}` |
| Self-unfreeze `ENERGY` but not yet matured | `{"Error": "class org.tron.core.exception.ContractValidateException : It's not time to unfreeze(Energy)."}` |
| Self-unfreeze `TRON_POWER` (only when `AllowNewResourceModel` is enabled) but no TronPower freeze / not yet matured | `{"Error": "class org.tron.core.exception.ContractValidateException : no frozenBalance(TronPower)"}` or `... It's not time to unfreeze(TronPower).` |
| Invalid `resource` | `{"Error": "class org.tron.core.exception.ContractValidateException : ResourceCode error.valid ResourceCode[BANDWIDTH、Energy]"}` (with `AllowNewResourceModel` enabled: `... [BANDWIDTH、Energy、TRON_POWER]`) |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
