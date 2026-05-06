# /wallet/updatewitness

Update an SR candidate's URL (candidate only).

- Source: `framework/src/main/java/org/tron/core/services/http/UpdateWitnessServlet.java`
- Method: `POST`
- Contract: `protocol.WitnessUpdateContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Candidate address |
| `update_url` | string | Yes | New URL (hex UTF-8) |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format of address / text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/updatewitness \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
  "update_url":    "68747470733a2f2f747261782e696f"
}
'
```

## Response

Returns an unsigned `protocol.Transaction`.

Response example (`txID`, `ref_block_*`, `expiration`, `timestamp`, `raw_data_hex` vary with construction moment):

```json
{
  "visible": false,
  "txID": "9452c5a333ccd579a720e406c2acb0b11d26cad7a8c01876ba3cfddc10f250b5",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "owner_address": "419c7c7049d26108be0dcb5f78479c6ff27ba101d1",
            "update_url": "68747470733a2f2f747261782e696f"
          },
          "type_url": "type.googleapis.com/protocol.WitnessUpdateContract"
        },
        "type": "WitnessUpdateContract"
      }
    ],
    "ref_block_bytes": "27c7",
    "ref_block_hash": "e51bd4751a4d7222",
    "expiration": 1777446465000,
    "timestamp": 1777446406948
  },
  "raw_data_hex": "0a0227c72208e51bd4751a4d722240e8dbc2c0dd335a620808125e0a32747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5769746e657373557064617465436f6e747261637412280a15419c7c7049d26108be0dcb5f78479c6ff27ba101d1620f68747470733a2f2f747261782e696f70a496bfc0dd33"
}
```

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| owner account does not exist | `{"Error": "... : account does not exist"}` |
| Invalid `update_url` (empty or too long) | `{"Error": "... : Invalid url"}` |
| Address is not an SR candidate | `{"Error": "... : Witness does not exist"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
