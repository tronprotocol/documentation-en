# /wallet/withdrawbalance

Withdraw SR block-production rewards or voting account's reward share to balance.

- Source: `framework/src/main/java/org/tron/core/services/http/WithdrawBalanceServlet.java`
- Method: `POST`
- Contract: `protocol.WithdrawBalanceContract` (`balance_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Claiming account address (SR or voter) |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/withdrawbalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, `raw_data_hex` vary with construction moment):

```json
{
  "visible": false,
  "txID": "ee9e2c192a1c9508e5d4944c000dbe3b99f05399221a9b02848cd44ef27cc8a3",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
          },
          "type_url": "type.googleapis.com/protocol.WithdrawBalanceContract"
        },
        "type": "WithdrawBalanceContract"
      }
    ],
    "ref_block_bytes": "27d2",
    "ref_block_hash": "bd570b8df4e022d6",
    "expiration": 1777446498000,
    "timestamp": 1777446439141
  },
  "raw_data_hex": "0a0227d22208bd570b8df4e022d640d0ddc4c0dd335a53080d124f0a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e576974686472617742616c616e6365436f6e747261637412170a15419c7c7049d26108be0dcb5f78479c6ff27ba101d170e591c1c0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : Account[<address>] not exists"}` |
| owner is a genesis SR (Guard Representative) | `{"Error": "... : Account[<address>] is a guard representative and is not allowed to withdraw Balance"}` |
| Less than 24 hours since last withdrawal | `{"Error": "... : The last withdraw time is <ts>, less than 24 hours"}` |
| No reward to withdraw | `{"Error": "... : witnessAccount does not have any reward"}` |
| Balance accumulation overflow | `{"Error": "... : <ArithmeticException message>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
