# /wallet/participateassetissue

Participate in a TRC-10 fundraising (buy with TRX).

- Source: `framework/src/main/java/org/tron/core/services/http/ParticipateAssetIssueServlet.java`
- Method: `POST`
- Contract: `protocol.ParticipateAssetIssueContract` (`asset_issue_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Buyer |
| `to_address` | string | Yes | Token issuer address |
| `asset_name` | string | Yes | Token id (since the `ALLOW_SAME_TOKEN_NAME` proposal, this is the token id as a string, e.g. `1000001`, encoded as UTF-8 hex) |
| `amount` | int64 | Yes | TRX paid, in sun |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format for addresses and text fields |

Constraints: must fall within `[start_time, end_time)`; the token amount received is computed as `amount * num / trx_num`.

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/participateassetissue \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "to_address":    "41088a2bfcb1c7271029fd69a66859d55560895884",
  "asset_name":    "31303035343136",
  "amount": 1000000
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`asset_name` `31303035343136` decodes to token id `1005416`; `txID`, `ref_block_*`, `expiration`, `timestamp`, and `raw_data_hex` vary by the moment of construction):

```json
{
  "visible": false,
  "txID": "1c2d37ad679f720266a0565d0170bcce2b4d096953badf5c848b85137005b5d4",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount": 1000000,
            "asset_name": "31303035343136",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "to_address": "41088a2bfcb1c7271029fd69a66859d55560895884"
          },
          "type_url": "type.googleapis.com/protocol.ParticipateAssetIssueContract"
        },
        "type": "ParticipateAssetIssueContract"
      }
    ],
    "ref_block_bytes": "2794",
    "ref_block_hash": "ba3c3fb8fa06d426",
    "expiration": 1777446312000,
    "timestamp": 1777446253445
  },
  "raw_data_hex": "0a0227942208ba3c3fb8fa06d42640c0b0b9c0dd335a7d080912790a3a747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e506172746963697061746541737365744973737565436f6e7472616374123b0a1541dd791d6b49e190062d650e6a23c575510d35f2f9121541088a2bfcb1c7271029fd69a66859d555608958841a073130303534313620c0843d7085e7b5c0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid ownerAddress"}` |
| Invalid `to_address` | `{"Error": "... : Invalid toAddress"}` |
| `amount <= 0` | `{"Error": "... : Amount must greater than 0!"}` |
| owner == to | `{"Error": "... : Cannot participate asset Issue yourself !"}` |
| owner account does not exist | `{"Error": "... : Account does not exist!"}` |
| owner balance is insufficient for amount + fee | `{"Error": "... : No enough balance !"}` |
| Token does not exist | `{"Error": "... : No asset named <name>"}` |
| `to_address` is not the issuer of this token | `{"Error": "... : The asset is not issued by <toAddress hex>"}` |
| Outside fundraising window | `{"Error": "... : No longer valid period!"}` |
| Exchange does not divide evenly | `{"Error": "... : Can not process the exchange!"}` |
| `to_address` account does not exist | `{"Error": "... : To account does not exist!"}` |
| Issuer's remaining distributable balance is insufficient | `{"Error": "... : Asset balance is not enough !"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
