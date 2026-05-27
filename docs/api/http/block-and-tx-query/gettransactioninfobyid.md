# /wallet/gettransactioninfobyid

Query the **execution result** of a transaction by ID (includes receipt, logs, internal transactions, resource consumption).

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionInfoByIdServlet.java`
- Method: `GET` / `POST`
- Request: `api.BytesMessage`
- Response: `protocol.TransactionInfo` (`Tron.proto`)
- Solidity endpoint: `/walletsolidity/gettransactioninfobyid`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `value` | string | Yes | Transaction ID hex |
| `visible` | bool | No | Format for addresses and text fields; when `visible=true` the servlet additionally rewrites `log[].address` (EVM 20 bytes) by prepending `0x41` and converting to base58 |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactioninfobyid \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "value": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca"
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `id` | bytes | Transaction ID |
| `fee` | int64 | TRX fee actually deducted (sun) |
| `blockNumber` | int64 | Block number where the transaction was packed |
| `blockTimeStamp` | int64 | Block timestamp in milliseconds |
| `contractResult` | repeated bytes | Contract call return value |
| `contract_address` | bytes | Address of the deployed/called contract |
| `receipt` | ResourceReceipt | Resource consumption (see below) |
| `log` | repeated Log | Event logs (`{address, topics[], data}`) |
| `result` | enum | `SUCESS` / `FAILED` |
| `resMessage` | bytes | Failure reason |
| `internal_transactions` | repeated InternalTransaction | Internal transactions |
| `withdraw_amount` | int64 | Withdrawn witness reward (only for WithdrawBalance) |
| `unfreeze_amount` | int64 | Unfrozen amount (only for UnfreezeBalance V1) |
| `withdraw_expire_amount` | int64 | Withdrawn expired-unfreeze amount (V2) |
| `cancel_unfreezeV2_amount` | map\<string,int64\> | Cancelled unfreeze amount (V2) |
| `assetIssueID` | string | Newly created TRC10 ID (only for CreateAssetIssue) |
| `exchange_*` / `orderId` | — | Exchange / Market related fields |

`ResourceReceipt` (`Tron.proto`):

| Field | Type | Description |
|---|---|---|
| `energy_usage` | int64 | Caller's energy burned (own energy) |
| `energy_fee` | int64 | TRX burned due to insufficient energy |
| `origin_energy_usage` | int64 | Energy paid by the contract creator |
| `energy_usage_total` | int64 | Total energy consumed |
| `net_usage` | int64 | Bandwidth consumed |
| `net_fee` | int64 | TRX burned due to insufficient bandwidth |
| `result` | enum | Contract execution result (same as `Transaction.Result.contractResult`) |
| `energy_penalty_total` | int64 | Energy penalty |

Response example (real Nile contract call; full `data` and `internal_transactions` content truncated):

```json
{
  "id": "01b4cde4197b9d1a1ff09ef5d2b1d939d3ec2401b3f002ebd0802c0f30a6e4ca",
  "fee": 5254500,
  "blockNumber": 66985120,
  "blockTimeStamp": 1777437762000,
  "contractResult": [""],
  "contract_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
  "receipt": {
    "energy_fee": 4458500,
    "energy_usage_total": 44585,
    "net_fee": 796000,
    "result": "SUCCESS"
  },
  "log": [
    {
      "address": "9ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "topics": [
        "c66625d03b4a832d8245f0df593e32e0fbbbad96d4aa45440aa1535b80983083",
        "000000000000000000000000dd791d6b49e190062d650e6a23c575510d35f2f9",
        "0000000000000000000000000000000000000000000000000000000000000007"
      ],
      "data": "0000000000000000000000000000000000000000000000000000000000000007..."
    }
  ],
  "internal_transactions": [
    {
      "hash": "61318c1e41c5fd387f1e4e4e8ec1fc98f295d3ef002bab1b33dd1cba2f93cb75",
      "caller_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "transferTo_address": "419ff8fc48fb114ccd5bbdc24a86f0c73082f08825",
      "callValueInfo": [{}],
      "note": "63616c6c"
    }
    /* ... remaining internal calls omitted */
  ]
}
```

Returns `{}` if the transaction is not on-chain.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `value` is not valid hex | `{"Error": "class org.bouncycastle.util.encoders.DecoderException : <message>"}` (GET); `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <message>"}` (POST) |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
