# /wallet/gettransactionbyid

Query a transaction by its ID (**execution result not included** — only the pre-broadcast transaction body is returned).

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionByIdServlet.java`
- Method: `GET` / `POST`
- Request: `api.BytesMessage`
- Solidity endpoint: `/walletsolidity/gettransactionbyid`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Transaction ID hex (32 bytes) |
| `visible` | bool | No | Format for addresses and text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactionbyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"
}
'
```

## Response

Returns `protocol.Transaction`:

| Field | Type | Description |
|---|---|---|
| `txID` | string | Transaction ID (extra field added by HTTP output) |
| `raw_data.contract` | repeated Contract | Contract array (typically 1) |
| `raw_data.ref_block_*` | bytes/int64 | Reference block info |
| `raw_data.expiration` | int64 | Expiration time in milliseconds |
| `raw_data.timestamp` | int64 | Transaction timestamp |
| `raw_data.fee_limit` | int64 | Smart contract call fee limit |
| `raw_data_hex` | string | Hex encoding of raw_data |
| `signature` | repeated bytes | Signatures |
| `ret` | repeated Result | Transaction result (includes `contractRet`) |

Response example (real Nile contract call; long `data` / `raw_data_hex` fields truncated):

```json
{
  "ret": [{ "contractRet": "SUCCESS" }],
  "signature": ["2154e8ef08f014063de8a88bafe748c8cbb48633c1657c083dca1a73439b289f6aa796bfa58797da6354d35fb7334a8c145c48ae266e4a885f7ee44791b5a3c31b"],
  "txID": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "data": "a6bd98ac0000000000000000000000000000000000000000000000000000000000000007...",
            "owner_address": "41dd791d6b49e190062d650e6a23c575510d35f2f9",
            "contract_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825"
          },
          "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
        },
        "type": "TriggerSmartContract"
      }
    ],
    "ref_block_bytes": "1c8b",
    "ref_block_hash": "d78785ed02dd918f",
    "expiration": 1777437813000,
    "fee_limit": 10000000000,
    "timestamp": 1777437756016
  },
  "raw_data_hex": "0a021c8b2208d78785ed02dd918f4088d2b2bcdd335af004081f12eb04..."
}
```

Returns `{}` if not found. For execution results (receipt, logs), use [`/wallet/gettransactioninfobyid`](gettransactioninfobyid.md).

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` (POST) | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| `value` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
