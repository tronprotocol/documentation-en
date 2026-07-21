# /wallet/updateBrokerage

SR updates its reward share ratio (brokerage).

- Source: `framework/src/main/java/org/tron/core/services/http/UpdateBrokerageServlet.java`
- Method: `POST`
- Contract: `protocol.UpdateBrokerageContract` (`storage_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | SR address |
| `brokerage` | int32 | No | New brokerage percentage 0–100; omitted defaults to `0`, which is valid |
| `Permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updateBrokerage \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "brokerage": 20
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, `raw_data_hex` vary with construction moment):

```json
{
  "visible": false,
  "txID": "63732aa3bc1e95227af2d09782d430f7032ee9500bf035d4fd82001f50744745",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "brokerage": 20,
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1"
          },
          "type_url": "type.googleapis.com/protocol.UpdateBrokerageContract"
        },
        "type": "UpdateBrokerageContract"
      }
    ],
    "ref_block_bytes": "27c9",
    "ref_block_hash": "c22bba19ac9d6cf3",
    "expiration": 1777446471000,
    "timestamp": 1777446411781
  },
  "raw_data_hex": "0a0227c92208c22bba19ac9d6cf340d88ac3c0dd335a55083112510a34747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e55706461746542726f6b6572616765436f6e747261637412190a15419c7c7049d26108be0dcb5f78479c6ff27ba101d110147085bcbfc0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| ChangeDelegation proposal not enabled on the chain | `{"Error": "class org.tron.core.exception.ContractValidateException : contract type error, unexpected type [UpdateBrokerageContract]"}` |
| Invalid `owner_address` | `{"Error": "... : Invalid ownerAddress"}` |
| `brokerage` not in [0, 100] | `{"Error": "... : Invalid brokerage"}` |
| Address is not an SR | `{"Error": "... : Not existed witness:<address hex>"}` |
| owner account does not exist | `{"Error": "... : Account does not exist"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
