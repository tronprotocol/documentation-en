# /wallet/broadcasttransaction

Broadcast a signed transaction.

- Source: `framework/src/main/java/org/tron/core/services/http/BroadcastServlet.java`
- Method: `POST`
- Response: `api.Return` + `txid`

## Request parameters

Pass the JSON form of `protocol.Transaction` directly (i.e., the response from `createtransaction`-style endpoints plus signatures):

| Field | Type | Required | Description |
|---|---|---|---|
| `raw_data` | object | Yes | Same as `createtransaction` response; the node re-serializes it into protobuf bytes for SHA256 signature verification |
| `raw_data_hex` | string | No (node ignores) | Client-side display helper — the protobuf encoding of `raw_data`. **Not a proto field of `protocol.Transaction`**; `JsonFormat.merge` skips it during parse, so the node neither reads it nor cross-checks it against `raw_data`. Clients usually SHA256 it to derive `txID` when signing, but whether it matches or is even valid hex when broadcast does not affect processing |
| `signature` | string[] | Yes | Signature array (1 for ordinary accounts; per permission rules for multi-sig) |
| `visible` | bool | No | Format of address / text fields |

Example:

```bash
curl --request POST \
     --url https://nile.trongrid.io/wallet/broadcasttransaction \
     --header 'accept: application/json' \
     --header 'content-type: application/json' \
     --data '
{
  "raw_data":     { "...": "..." },
  "raw_data_hex": "0a02...",
  "signature":    ["b8c0...01"]
}
'
```

> The example above is a placeholder; before actually calling, replace `raw_data` / `raw_data_hex` / `signature` with the signed content of a real unsigned transaction returned by [`/wallet/createtransaction`](createtransaction.md) etc.

## Response

| Field | Type | Description |
|---|---|---|
| `result` | bool | Whether the transaction entered the pool |
| `code` | enum | `SUCCESS` / `SIGERROR` / `CONTRACT_VALIDATE_ERROR` / `CONTRACT_EXE_ERROR` / `BANDWITH_ERROR` / `DUP_TRANSACTION_ERROR` / `TAPOS_ERROR` / `TOO_BIG_TRANSACTION_ERROR` / `TRANSACTION_EXPIRATION_ERROR` / `SERVER_BUSY` / `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` / `BLOCK_UNSOLIDIFIED` / `OTHER_ERROR` |
| `message` | string | Failure reason; UTF-8 text when `visible=true`, hex of UTF-8 bytes when `visible=false` |
| `txid` | string | Transaction hash |

`result: true` only means the node received and pooled the transaction; whether it ultimately makes it on-chain must be confirmed via [`/wallet/gettransactioninfobyid`](../block-and-tx-query/gettransactioninfobyid.md).

Response example:

```json
{
  "result": true,
  "code": "SUCCESS",
  "txid": "d5ec749ecc2a615399d8a6c864ea4c74ff9f8453eaa44d6b1e2f0b7b3e2f3b6a"
}
```

### Error responses

Business-level errors are **still returned in the same `result/code/message` shape**, e.g.:

```json
{ "result": false, "code": "DUP_TRANSACTION_ERROR", "message": "Dup transaction.", "txid": "..." }
{ "result": false, "code": "SIGERROR", "message": "validateSignature error", "txid": "..." }
{ "result": false, "code": "TAPOS_ERROR", "message": "Tapos failed", "txid": "..." }
```

`code` semantics:

| code | Meaning |
|---|---|
| `SIGERROR` | Signature verification failed |
| `CONTRACT_VALIDATE_ERROR` | Pre-execution contract validation failed (insufficient balance, invalid params, etc.) |
| `CONTRACT_EXE_ERROR` | Failed during execution |
| `BANDWITH_ERROR` | Insufficient bandwidth |
| `DUP_TRANSACTION_ERROR` | Duplicate transaction |
| `TAPOS_ERROR` | `ref_block_*` not on chain (most often due to expiration or an out-of-sync chain) |
| `TOO_BIG_TRANSACTION_ERROR` | Transaction body too large |
| `TRANSACTION_EXPIRATION_ERROR` | `expiration` already passed |
| `SERVER_BUSY` | Node busy (pending pool full) |
| `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` | Insufficient outbound connections; not broadcast |
| `BLOCK_UNSOLIDIFIED` | Block not yet solidified (for related queries) |
| `OTHER_ERROR` | Other |

JSON parse failure, missing `raw_data`, type mismatch, etc. take the `Util.processError` path:

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Missing `raw_data`, `raw_data.contract` is not an array, `signature` is not an array or its elements are not hex, field type mismatch in `raw_data`, etc. | `{"Error": "class java.lang.NullPointerException : null"}` (`Util.packTransaction` silently catches `JsonFormat$ParseException` / `ClassCastException` and returns `null`; downstream `TransactionCapsule(null)` triggers NPE) |
| Field type mismatch inside `raw_data.contract[i].parameter.value` | That contract is caught and dropped inside `packTransaction`, broadcast ends up with an empty contract list, returns `{"code": "CONTRACT_VALIDATE_ERROR", "message": "<hex of \"No contract!\">", ...}` |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
