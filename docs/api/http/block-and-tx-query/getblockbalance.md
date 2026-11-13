# /wallet/getblockbalance

Returns the block balance trace, containing transactions with recorded TRX balance-change operations. Transactions without such operations are omitted; match entries by `transaction_identifier`, not by their position in the block's transaction list.

- Source: `framework/src/main/java/org/tron/core/services/http/GetBlockBalanceServlet.java`
- Method: `POST`
- Request: `protocol.BlockBalanceTrace.BlockIdentifier`
- Response: `protocol.BlockBalanceTrace` (`balance_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `hash` | string | Yes | Block hash hex |
| `number` | int64 | No | Block number; omitted defaults to `0`. It may be omitted only for the genesis block; for other blocks it must match the height represented by `hash` |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getblockbalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "hash": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
  "number": 66987565
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `block_identifier.hash` | bytes | Block hash |
| `block_identifier.number` | int64 | Block number |
| `timestamp` | int64 | Block timestamp in milliseconds |
| `transaction_balance_trace` | repeated TransactionBalanceTrace | Entries for transactions with a nonempty list of recorded balance-change operations |

`TransactionBalanceTrace` (`balance_contract.proto`):

| Field | Type | Description |
|---|---|---|
| `transaction_identifier` | bytes | Transaction ID |
| `operation` | repeated Operation | Multiple `(operation_identifier, address, amount)` triples |
| `type` | string | Contract type, e.g. `TransferContract` |
| `status` | string | Status |

Response example (only the first trace entry shown; the actual response contains 4 entries):

```json
{
  "block_identifier": {
    "hash": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
    "number": 66987565
  },
  "timestamp": 1777445121000,
  "transaction_balance_trace": [
    {
      "transaction_identifier": "ff44a2823a870c12f12a4ca6e7647650356bc2bb5e02c5855312cf2db4c950c1",
      "operation": [
        { "operation_identifier": 0, "address": "41f7c3feccb6461aab0fd25f61d9560645b08228cb", "amount": -267000 },
        { "operation_identifier": 1, "address": "41f7c3feccb6461aab0fd25f61d9560645b08228cb", "amount": -848000 },
        { "operation_identifier": 2, "address": "41b06b4139895c9f51c967c9f3d9089ca721e8e34c", "amount": 848000 }
      ],
      "type": "TransferContract",
      "status": "SUCCESS"
    }
  ]
}
```

The target block must have a balance trace recorded on this node. `storage.balance.history.lookup = true` (equivalent to launch flag `--history-balance-lookup`) enables trace recording; reads access the stored trace regardless of the current setting. Previously recorded traces remain queryable after recording is disabled, and enabling or re-enabling it does not backfill missing history. A missing trace produces the `ItemNotFoundException` shown below.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `BlockIdentifier` missing | `{"Error": "class java.lang.IllegalArgumentException : block_identifier null"}` |
| `number < 0` | `{"Error": "class java.lang.IllegalArgumentException : block_identifier number less than 0"}` |
| `hash` length is not 32 bytes | `{"Error": "class java.lang.IllegalArgumentException : block_identifier hash length not equals 32"}` |
| `number` and `hash` do not match | `{"Error": "class java.lang.IllegalArgumentException : number and hash do not match"}` |
| Block has no balance trace or does not exist | `{"Error": "class org.tron.core.exception.ItemNotFoundException : This block does not exist"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
