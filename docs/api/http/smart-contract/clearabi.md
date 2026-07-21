# /wallet/clearabi

Clear a contract's ABI (deployer only).

- Source: `framework/src/main/java/org/tron/core/services/http/ClearABIServlet.java`
- Method: `POST`
- Contract: `protocol.ClearABIContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Contract deployer address |
| `contract_address` | string | Yes | Target contract address |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/clearabi \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
}
'
```

## Response

Before construction, the servlet validates that `owner_address` matches the contract's `origin_address` (deployer). The example `owner_address` is not the TetherToken deployer; the actual Nile response is:

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
              "owner_address":    "41dd791d6b49e190062d650e6a23c575510d35f2f9",
              "contract_address": "41eca9bc828a3005b9a3b909f2cc5c2a54794de05f"
          },
          "type_url": "type.googleapis.com/protocol.ClearABIContract"
        },
        "type": "ClearABIContract"
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
| Chain has not activated TVM Constantinople | `{"Error": "class org.tron.core.exception.ContractValidateException : contract type error,unexpected type [ClearABIContract]"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| Contract address does not exist | `{"Error": "... : Contract not exists"}` |
| owner is not the contract deployer | `{"Error": "... : Account[<address>] is not the owner of the contract"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
