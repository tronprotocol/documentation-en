# /wallet/createtransaction

Create an unsigned TRX transfer transaction (`TransferContract`).

- Source: `framework/src/main/java/org/tron/core/services/http/TransferServlet.java`
- Method: `POST`
- Contract: `protocol.TransferContract` (`balance_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Sender address |
| `to_address` | string | Yes | Recipient address |
| `amount` | int64 | Yes | Amount in sun (1 TRX = 1e6 sun) |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `extra_data` | string | No | Written into `raw_data.data` (hex; UTF-8 when `visible=true`) |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createtransaction \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "to_address":    "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a",
  "amount":        1000000
}
'
```

## Response

Returns an unsigned `protocol.Transaction` (with `txID`, `raw_data`, `raw_data_hex`; `signature` is empty). Response example (real Nile capture):

```json
{
  "visible": false,
  "txID": "6303c7639f591407ef9f34a7ac8c9c9a21151f5a6af21924502515734fc267ab",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount":        1000000,
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "to_address":    "4192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a"
          },
          "type_url": "type.googleapis.com/protocol.TransferContract"
        },
        "type": "TransferContract"
      }
    ],
    "ref_block_bytes": "2927",
    "ref_block_hash":  "939ece39d08a7abe",
    "expiration":      1777447527000,
    "timestamp":       1777447470038
  },
  "raw_data_hex": "0a0229272208939ece39d08a7abe40d8c483c1dd335a67080112630a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412320a1541dd791d6b49e190062d650e6a23c575510d35f2f912154192ad11c1bf16b3b14b0bd6b5c7e2db73a0b5e83a18c0843d70d68780c1dd33"
}
```

> The `txID`, `ref_block_bytes` / `ref_block_hash`, `expiration`, `timestamp`, `raw_data_hex` above vary with construction time: `ref_block_*` is taken from the latest solidified block at construction time; `expiration = timestamp + 60_000`; `txID` is the SHA256 of `raw_data`; `raw_data_hex` is the protobuf encoding of `raw_data`, and signing takes `raw_data_hex` as input. Other construction endpoints (`/wallet/triggersmartcontract`, `freezebalancev2`, `unfreezebalancev2`, etc.) return the same ephemeral fields with identical semantics; they are not repeated below.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` |
| Field type mismatch / address decode failure | `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `extra_data` is not valid hex when `visible=false` | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (`Util.setTransactionExtraData` calls `ByteArray.fromHexString` directly, bypassing `JsonFormat`) |
| `owner_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress!"}` |
| `to_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid toAddress!"}` |
| `to_address == owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Cannot transfer TRX to yourself."}` |
| `owner_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : Validate TransferContract error, no OwnerAccount."}` |
| `amount <= 0` | `{"Error": "class org.tron.core.exception.ContractValidateException : Amount must be greater than 0."}` |
| `to_address` is a contract and the `ForbidTransferToContract` proposal is enabled | `{"Error": "class org.tron.core.exception.ContractValidateException : Cannot transfer TRX to a smartContract."}` |
| `to_address` is a v1 contract and the `AllowTvmCompatibleEvm` proposal is enabled | `{"Error": "class org.tron.core.exception.ContractValidateException : Cannot transfer TRX to a smartContract which version is one. Instead please use TriggerSmartContract "}` |
| Insufficient balance for `amount + fee` (when receiver is a new account, `fee` includes 0.1 TRX creation fee) | `{"Error": "class org.tron.core.exception.ContractValidateException : Validate TransferContract error, balance is not sufficient."}` |
| `amount + fee` or recipient balance overflows `long` | `{"Error": "class org.tron.core.exception.ContractValidateException : <ArithmeticException message>"}` |
