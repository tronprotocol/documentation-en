# /wallet/gettransactioninfobyblocknum

Return the array of `TransactionInfo` (execution results) for all transactions in the block, by block number.

- Source: `framework/src/main/java/org/tron/core/services/http/GetTransactionInfoByBlockNumServlet.java`
- Method: `GET` / `POST`
- Request: `api.NumberMessage`
- Response: `api.TransactionInfoList`
- Solidity endpoint: `/walletsolidity/gettransactioninfobyblocknum`

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `num` | int64 | Yes | Block number |
| `visible` | bool | No | Format for addresses and text fields; when `visible=true` the servlet additionally rewrites `log[].address` (EVM 20 bytes) by prepending `0x41` and converting to base58 |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/gettransactioninfobyblocknum \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "num": 66987565
}
'
```

## Response

Returns a JSON array (equivalent to the original `TransactionInfoList.transactionInfo`); each element has the same structure as [`/wallet/gettransactioninfobyid`](gettransactioninfobyid.md).

Response example (block 66987565 contains 4 transactions; first 2 shown):

```json
[
  {
    "id": "ff44a2823a870c12f12a4ca6e7647650356bc2bb5e02c5855312cf2db4c950c1",
    "fee": 267000,
    "blockNumber": 66987565,
    "blockTimeStamp": 1777445121000,
    "contractResult": [""],
    "receipt": { "net_fee": 267000 }
  },
  {
    "id": "0419405287081aa44f4d78725e6fabac8d14e71abf9e28825ad4f4e61a5bccb7",
    "fee": 267000,
    "blockNumber": 66987565,
    "blockTimeStamp": 1777445121000,
    "contractResult": [""],
    "receipt": { "net_fee": 267000 }
  }
]
```

An empty block (no transactions) returns `[]`; `num <= 0` returns `{}`.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.maxMessageSize` (POST) | `{"Error": "class java.lang.Exception : body size is too big, the limit is <N>"}` |
| `num` is not numeric (GET) | `{"Error": "class java.lang.NumberFormatException : <message>"}` |
| Request body is not valid JSON / field type mismatch (POST) | `{"Error": "class com.alibaba.fastjson.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
