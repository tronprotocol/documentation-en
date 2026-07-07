# /wallet/freezebalance

> **Disabled on-chain**: After proposal #70 `UNFREEZE_DELAY_DAYS` is approved (already active on mainnet), `FreezeBalanceActuator.validate()` throws `freeze v2 is open, old freeze is closed` directly, so all new requests fail. Use [`/wallet/freezebalancev2`](../stake-v2/freezebalancev2.md) instead.

Freeze TRX to obtain bandwidth or energy; can be delegated to others. On nodes with `block.checkFrozenTime=1`, the duration must be within the chain's current dynamic range (normally exactly 3 days).

- Source: `framework/src/main/java/org/tron/core/services/http/FreezeBalanceServlet.java`
- Method: `POST`
- Contract: `protocol.FreezeBalanceContract` (`balance_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Freezing account address |
| `frozen_balance` | int64 | Yes | Frozen amount (sun) |
| `frozen_duration` | int64 | No | Freeze duration in days; omitted defaults to `0`. Validated only when `block.checkFrozenTime=1`, when it must be within `[minFrozenTime, maxFrozenTime]` (normally `[3, 3]`) |
| `resource` | enum | No | `BANDWIDTH` / `ENERGY`, default `BANDWIDTH` |
| `receiver_address` | string | No | Delegate target address (omit to freeze for self) |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/freezebalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":   "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "frozen_balance":  1000000000,
  "frozen_duration": 3,
  "resource":        "BANDWIDTH"
}
'
```

## Response

Mainnet/Nile have Stake 2.0 enabled, so this endpoint returns `Error` directly:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : freeze v2 is open, old freeze is closed"}
```

On chains where proposal #70 has not been activated, the endpoint still returns an unsigned `protocol.Transaction`. Structure outline (`txID` / `ref_block_*` / `expiration` / `timestamp` / `raw_data_hex` semantics are the same as [`/wallet/createtransaction`](../tx-build-and-broadcast/createtransaction.md)):

```json
{
  "visible": false,
  "txID": "<computed from raw_data>",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
              "owner_address":   "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "frozen_balance":  1000000000,
              "frozen_duration": 3,
              "resource":        "BANDWIDTH"
          },
          "type_url": "type.googleapis.com/protocol.FreezeBalanceContract"
        },
        "type": "FreezeBalanceContract"
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
| Proposal #70 `UNFREEZE_DELAY_DAYS` activated (mainnet default) | `{"Error": "class org.tron.core.exception.ContractValidateException : freeze v2 is open, old freeze is closed"}` |
| `owner_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| `owner_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] not exists"}` |
| `frozen_balance <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenBalance must be positive"}` |
| `frozen_balance < 1_000_000` (less than 1 TRX) | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenBalance must be greater than or equal to 1 TRX"}` |
| Existing frozen-record count on the account is not in `{0,1}` | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenCount must be 0 or 1"}` |
| `frozen_balance > account balance` | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenBalance must be less than or equal to accountBalance"}` |
| `frozen_duration` outside `[minFrozenTime, maxFrozenTime]` (only when `block.checkFrozenTime=1`) | `{"Error": "class org.tron.core.exception.ContractValidateException : frozenDuration must be less than <max> days and more than <min> days"}` |
| Invalid `resource` (when `AllowNewResourceModel` is not enabled, `TRON_POWER` is not allowed) | `{"Error": "class org.tron.core.exception.ContractValidateException : ResourceCode error, valid ResourceCode[BANDWIDTH、ENERGY]"}` or `... [BANDWIDTH、ENERGY、TRON_POWER]` |
| `resource=TRON_POWER` but `receiver_address` is also set | `{"Error": "class org.tron.core.exception.ContractValidateException : TRON_POWER is not allowed to delegate to other accounts."}` |
| `receiver_address == owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : receiverAddress must not be the same as ownerAddress"}` |
| `receiver_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid receiverAddress"}` |
| `receiver_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] not exists"}` |
| `receiver_address` is a contract address and `AllowTvmConstantinople` is enabled | `{"Error": "class org.tron.core.exception.ContractValidateException : Do not allow delegate resources to contract addresses"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
