# /wallet/createwitness

Apply to become a Super Representative (SR) candidate. Costs 9999 TRX (chain parameter `getAccountUpgradeCost`).

- Source: `framework/src/main/java/org/tron/core/services/http/CreateWitnessServlet.java`
- Method: `POST`
- Contract: `protocol.WitnessCreateContract`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `owner_address` | string | Yes | Applicant address |
| `url` | string | Yes | Candidate URL (hex UTF-8) |
| `permission_id` | int32 | No | Multi-sig permission ID |
| `visible` | bool | No | Format of address / text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/createwitness \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
  "url":           "68747470733a2f2f747261782e696f"
}
'
```

## Response

Before construction, the validator checks that the account balance is at least `getAccountUpgradeCost` (9999 TRX) and that the account is not already an SR candidate. The example account has insufficient balance; the actual Nile response is:

```json
{"Error": "class org.tron.core.exception.ContractValidateException : balance < AccountUpgradeCost"}
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
            "url":           "68747470733a2f2f747261782e696f"
          },
          "type_url": "type.googleapis.com/protocol.WitnessCreateContract"
        },
        "type": "WitnessCreateContract"
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
| Request body exceeds `node.maxMessageSize` | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Invalid `owner_address` | `{"Error": "class org.tron.core.exception.ContractValidateException : Invalid address"}` |
| Invalid `url` (empty or too long) | `{"Error": "... : Invalid url"}` |
| owner account does not exist | `{"Error": "... : account[<address>] not exists"}` |
| Address is already an SR candidate | `{"Error": "... : Witness[<address>] has existed"}` |
| Balance < `AccountUpgradeCost` (default 9999 TRX) | `{"Error": "... : balance < AccountUpgradeCost"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
