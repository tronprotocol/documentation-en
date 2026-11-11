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
| `signature` | string[] | No | Optional at JSON/Protobuf parsing time. Each hex-encoded signature must decode to `65`–`68` bytes (normally `130`–`136` hex characters); a supplied signature outside this range is rejected immediately with `SIGERROR`. An ordinary transaction normally needs one valid signature to broadcast successfully, while multi-sig transactions must satisfy the selected permission threshold. A missing or cryptographically invalid signature normally results in `SIGERROR` when signature validation is reached |
| `visible` | bool | No | Format of address / text fields |

The same signature-length validation is applied to transactions submitted through the gRPC `BroadcastTransaction` method and other API endpoints that use the node's transaction broadcast path.

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
| `result` | bool | Whether this broadcast attempt succeeded; `false` is a protobuf default and is omitted from JSON. A failed P2P broadcast can occur after the transaction has entered the pool |
| `code` | enum | `SUCCESS` (default, omitted from JSON) / `SIGERROR` / `CONTRACT_VALIDATE_ERROR` / `CONTRACT_EXE_ERROR` / `BANDWITH_ERROR` / `DUP_TRANSACTION_ERROR` / `TAPOS_ERROR` / `TOO_BIG_TRANSACTION_ERROR` / `TRANSACTION_EXPIRATION_ERROR` / `SERVER_BUSY` / `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` / `BLOCK_UNSOLIDIFIED` / `OTHER_ERROR` |
| `message` | string | Failure reason; UTF-8 text when `visible=true`, hex of UTF-8 bytes when `visible=false` |
| `txid` | string | Transaction hash |

`result: true` only means the node received and pooled the transaction; whether it ultimately makes it on-chain must be confirmed via [`/wallet/gettransactioninfobyid`](../block-and-tx-query/gettransactioninfobyid.md).

Response example:

```json
{
  "result": true,
  "txid": "d5ec749ecc2a615399d8a6c864ea4c74ff9f8453eaa44d6b1e2f0b7b3e2f3b6a"
}
```

The protobuf JSON parser also accepts a single hex string for `signature` as a one-element list; a non-array value does not always cause a parse error. Use the documented array form for normal requests.

### Error responses

Business-level errors use `code` / `message` / `txid`; the default `result=false` is omitted. The following examples assume `visible=true`, so the messages are text:

```json
{ "code": "DUP_TRANSACTION_ERROR", "message": "Dup transaction.", "txid": "..." }
```

```json
{ "code": "SIGERROR", "message": "Validate signature error: <details>", "txid": "..." }
```

```json
{ "code": "TAPOS_ERROR", "message": "Tapos check error.", "txid": "..." }
```

With `visible=false` (the default), `message` is hex-encoded; for example, `Dup transaction.` becomes `447570207472616e73616374696f6e2e`. Successful responses omit the default `code=SUCCESS`.

`code` semantics:

| code | Meaning |
|---|---|
| `SIGERROR` | Signature verification failed, or a supplied signature is shorter than `65` bytes or longer than `68` bytes |
| `CONTRACT_VALIDATE_ERROR` | Pre-execution contract validation failed (insufficient balance, invalid params, etc.) |
| `CONTRACT_EXE_ERROR` | Failed during execution |
| `BANDWITH_ERROR` | Insufficient bandwidth |
| `DUP_TRANSACTION_ERROR` | Duplicate transaction |
| `TAPOS_ERROR` | `ref_block_*` not on chain (most often due to expiration or an out-of-sync chain) |
| `TOO_BIG_TRANSACTION_ERROR` | Transaction body too large |
| `TRANSACTION_EXPIRATION_ERROR` | Expiration precedes the next block slot, is at or before the head block timestamp, or is more than 24 hours after the head block timestamp |
| `SERVER_BUSY` | Node busy (pending pool full) |
| `NO_CONNECTION` / `NOT_ENOUGH_EFFECTIVE_CONNECTION` | When `node.rpc.minEffectiveConnection` is nonzero (default: `1`): no active peers, too few peers that have finished syncing, or P2P broadcasting reached no peers |
| `BLOCK_UNSOLIDIFIED` | With the unsolidified-block check enabled, the gap between the head and solidified block heights has reached the configured `maxUnsolidifiedBlocks` threshold, so broadcast is rejected |
| `OTHER_ERROR` | Other |

Request JSON and outer-structure failures take the `Util.processError` path; malformed individual contracts can instead be dropped during parsing, as described below:

| Trigger | Response |
|---|---|
| Request body exceeds `node.http.maxMessageSize` | Usually HTTP 413 `Payload Too Large` when rejected by `SizeLimitHandler` |
| Request body is not valid JSON | `{"Error": "class org.tron.json.JSONException : <parser info>"}` |
| Missing or null `raw_data` / `raw_data.contract` | `{"Error": "class java.lang.NullPointerException : <message>"}` while accessing the missing object or array |
| `raw_data` is not an object, or `raw_data.contract` is not an array (excluding JSON strings that can be parsed into the required structure) | `{"Error": "class org.tron.json.JSONException : <message>"}`, for example `Field 'contract' is not an array` |
| Invalid signature hex or a `raw_data` field value that `JsonFormat.merge` cannot decode | `packTransaction` catches the final `JsonFormat$ParseException` and returns `null`; the downstream operation then returns `{"Error": "class java.lang.NullPointerException : <message>"}` |
| Field type mismatch inside `raw_data.contract[i].parameter.value` | The affected contract is caught and dropped inside `packTransaction`. If no contracts remain after parsing and earlier broadcast checks pass, the response contains `code: "CONTRACT_VALIDATE_ERROR"` and `message` encoding `Contract validate error : No contract!` (hex by default; text with `visible=true`) |
| Other exceptions | `{"Error": "<exceptionClass> : <message>"}` |
