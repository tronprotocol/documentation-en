# /wallet/updateaccount

Update an account's name (`account_name`). The field is not unique.

- Source: `framework/src/main/java/org/tron/core/services/http/UpdateAccountServlet.java`
- Method: `POST` (`GET` is not implemented)
- Contract: `protocol.AccountUpdateContract` (`account_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Account address |
| `account_name` | string | Yes | New account name (UTF-8 encoded as hex) |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updateaccount \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "account_name": "6e69636b6e616d65"
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction):

```json
{
  "visible": false,
  "txID": "cc4a646f211c1f92a6b1491ee625c7f6d055d031eba38e3fe8bfe2075ecc11c9",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "account_name": "6e69636b6e616d65",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9"
          },
          "type_url": "type.googleapis.com/protocol.AccountUpdateContract"
        },
        "type": "AccountUpdateContract"
      }
    ],
    "ref_block_bytes": "2704",
    "ref_block_hash": "f6ca8374136773d8",
    "expiration": 1777445880000,
    "timestamp": 1777445820842
  },
  "raw_data_hex": "0a0227042208f6ca8374136773d840c0819fc0dd335a5b080a12570a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e4163636f756e74557064617465436f6e747261637412210a086e69636b6e616d65121541dd791d6b49e190062d650e6a23c575510d35f2f970aab39bc0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `account_name` exceeds 200 bytes | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid accountName"}` |
| `owner_address` is not a valid 21-byte address | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| `owner_address` does not exist on chain | `{"Error": "class org.tron.core.exception.ContractValidateException : Account does not exist"}` |
| Account already has an `account_name` and `AllowUpdateAccountName=0` | `{"Error": "class org.tron.core.exception.ContractValidateException : This account name is already existed"}` |
| The `account_name` is already taken by another account and `AllowUpdateAccountName=0` | `{"Error": "class org.tron.core.exception.ContractValidateException : This name is existed"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
