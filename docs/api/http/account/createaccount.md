# /wallet/createaccount

Build an unsigned transaction that creates a new account. The new account is activated passively: the payer (`owner_address`) covers the activation fee, and the new address (`account_address`) is created.

- Source: `framework/src/main/java/org/tron/core/services/http/CreateAccountServlet.java`
- Method: `POST`
- Contract: `protocol.AccountCreateContract` (`protocol/src/main/protos/core/contract/account_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Payer address |
| `account_address` | string | Yes | Address of the new account to create |
| `type` | enum | No | 0=Normal (default), 1=AssetIssue, 2=Contract |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "account_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
}
'
```

## Response

Returns an unsigned `protocol.Transaction` (with `txID`, `raw_data`, `raw_data_hex`, and an empty `signature`). The caller signs locally and then broadcasts via `/wallet/broadcasttransaction` or `/wallet/broadcasthex`.

Response example (`txID`, `ref_block_bytes`, `ref_block_hash`, `expiration`, `timestamp`, and `raw_data_hex` depend on the node's current height and change every call):

```json
{
  "visible": false,
  "txID": "411bbca37a92b5a9554274c5f0f05b0e486136d3bfe072c1c6454460b5290df3",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "account_address": "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
          },
          "type_url": "type.googleapis.com/protocol.AccountCreateContract"
        },
        "type": "AccountCreateContract"
      }
    ],
    "ref_block_bytes": "26fc",
    "ref_block_hash": "e6e9a02b83e65c03",
    "expiration": 1777445856000,
    "timestamp": 1777445797130
  },
  "raw_data_hex": "0a0226fc2208e6e9a02b83e65c034080c69dc0dd335a6612640a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74437265617465436f6e7472616374122e0a1541dd791d6b49e190062d650e6a23c575510d35f2f912154192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a708afa99c0dd33"
}
```

The activation fee is deducted from `owner_address`; the amount is governed by chain parameters (typically 1 TRX).

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `owner_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `owner_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : Account[<addr>] not exists"}` |
| `owner_address` balance is insufficient for the activation fee | `{"Error": "class org.tron.core.exception.ContractValidateException : Validate CreateAccountActuator error, insufficient fee."}` |
| `account_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid account address"}` |
| `account_address` already exists | `{"Error": "class org.tron.core.exception.ContractValidateException : Account has existed"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
