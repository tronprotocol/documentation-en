# /wallet/getaccountbalance

Query an account's TRX balance at a specific block (block-anchored).

- Source: `framework/src/main/java/org/tron/core/services/http/GetAccountBalanceServlet.java`
- Method: `POST`
- Request: `protocol.AccountBalanceRequest` (`balance_contract.proto`)
- Response: `protocol.AccountBalanceResponse` (`balance_contract.proto`)

## Request parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `account_identifier.address` | string | Yes | Account address |
| `block_identifier.hash` | string | Yes | Block hash |
| `block_identifier.number` | int64 | Yes | Block number |
| `visible` | bool | No | Address format |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/getaccountbalance \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "account_identifier": { "address": "41dd791d6b49e190062d650e6a23c575510d35f2f9" },
  "block_identifier": {
    "hash": "0000000003fe262d52bfa4b2814f816fd2e57af5b98a33d60d8630a03a908e0e",
    "number": 66987565
  }
}
'
```

## Response

| Field | Type | Description |
|---|---|---|
| `balance` | int64 | The account's balance at the anchored block (sun) |
| `block_identifier` | object | Hash/number of the anchored block |

Response example (Nile returns `block_identifier` as the most recent block in which the node tracked this account's balance, which may differ from the anchor in the request):

```json
{
  "balance": 1793227200,
  "block_identifier": {
    "hash": "0000000003fe25c69a3321cd009c484efe62b11abf0f8966fc81c1ff4a917cad",
    "number": 66987462
  }
}
```

The node must enable `storage.balance.history.lookup = true` (equivalent to the `--history-balance-lookup` startup flag). Otherwise no error is raised — the response is `balance: 0` together with the request's `block_identifier` echoed verbatim, which is indistinguishable from a successful "no record for this account before this block" response and can easily be misread.

### Error responses

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON / field type mismatch | `{"Error": "class org.tron.json.JSONException : <parser info>"}` or `{"Error": "class org.tron.core.services.http.JsonFormat$ParseException : <decoder info>"}` |
| `account_identifier` missing | `{"Error": "class java.lang.IllegalArgumentException : account_identifier is null"}` |
| `account_identifier.address` missing | `{"Error": "class java.lang.IllegalArgumentException : account_identifier address is null"}` |
| `block_identifier` missing | `{"Error": "class java.lang.IllegalArgumentException : block_identifier null"}` |
| `block_identifier.number < 0` | `{"Error": "class java.lang.IllegalArgumentException : block_identifier number less than 0"}` |
| `block_identifier.hash` is not 32 bytes | `{"Error": "class java.lang.IllegalArgumentException : block_identifier hash length not equals 32"}` |
| `block_identifier`'s `number` and `hash` do not match | `{"Error": "class java.lang.IllegalArgumentException : number and hash do not match"}` |
| Block number does not exist | `{"Error": "class org.tron.core.exception.ItemNotFoundException : number: <N> is not found!"}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
