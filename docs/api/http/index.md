# java-tron HTTP API

This directory documents the FullNode HTTP endpoints under `framework/src/main/java/org/tron/core/services/http/`. One markdown file per endpoint, named after the last segment of the URL (e.g. `/wallet/getnodeinfo` → `getnodeinfo.md`).

The following categories are intentionally not covered:

- Exchange (DEX) endpoints
- Market (order book) endpoints
- Shielded (anonymous transaction) endpoints

## Common conventions

- **Method**: a few pure-query endpoints accept `GET`, but most POST endpoints only accept `POST` with a JSON body.
- **GET / POST boundaries**: on endpoints that support both methods, request and error tables identify the applicable method. GET normally reads URL query parameters; POST normally reads a JSON body, except where the endpoint page states that POST reuses query parameters or ignores its body.
- **`visible`**: when `true`, addresses are base58check strings and text fields (URL, descriptions, etc.) are UTF-8 strings; when `false` (default), they are hex strings.
- **Builder endpoints** return an unsigned `protocol.Transaction`. The caller signs it locally and broadcasts it via [`/wallet/broadcasttransaction`](tx-build-and-broadcast/broadcasttransaction.md) or [`/wallet/broadcasthex`](tx-build-and-broadcast/broadcasthex.md).
- **`Permission_id`**: optional on builder endpoints; selects which `Permission` to use for multi-sig accounts. The field name is case-sensitive.
- **Amount unit**: TRC-10 amounts use the issuer-defined precision; every other amount is in sun (1 TRX = 1e6 sun).
- **`int64_as_string`**: GET requests may add `int64_as_string=true` in the URL query. When enabled, int64 / uint64 fields in protobuf JSON responses are serialized as JSON strings to avoid precision loss in clients such as JavaScript. This flag is honored only for GET requests; POST bodies are not affected.
- **Request body size**: HTTP request bodies are limited by `node.http.maxMessageSize` in `config.conf` (default `4194304`, about 4 MiB; `0` rejects every non-empty body). JSON-RPC has its own independent `node.jsonrpc.maxMessageSize`.
- **Rate limiting**: per-endpoint HTTP limits are configured in `rate.limiter.http`. The global `rate.limiter.apiNonBlocking` switch controls over-limit behavior: `true` rejects immediately with HTTP 200 and `{"Error":"class java.lang.IllegalAccessException : lack of computing resources"}`; `false` queues and blocks the caller until a permit is available.

!!! warning "XSS security note"

    Although the HTTP API reduces the risk of the browser parsing responses directly as HTML by setting `Content-Type` to `application/json`, this does not fully eliminate XSS. Some endpoints do not strictly validate their inputs, and responses may echo user-controlled content (especially when `visible=true`, where fields such as addresses and memos may be returned verbatim as UTF-8 strings). Before rendering any data returned by the API into a page, handle it safely according to the output context.

    The correct approach is to choose the encoding that matches where the data is placed: in an HTML text context, use HTML entity encoding (e.g. `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`), or rely on your front-end framework's default output escaping (such as React JSX or Vue template escaping). Only use `encodeURIComponent()` and similar URL-encoding methods when the data is placed into a URL parameter. Note that `encodeURIComponent()` / `escape()` are URL encoding (or legacy encoding) and cannot replace output escaping in an HTML context.

    For more guidance, see the [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

## Error responses

In the vast majority of cases the HTTP status is **200** — business errors are conveyed in the response body, so the client must parse the body to determine success or failure. Known exceptions:

- When an endpoint is explicitly disabled via the node's `disabledApiList`, `HttpApiAccessFilter` returns **HTTP 404** with body `{"Error": "this API is unavailable due to config"}`.
- When a request body exceeds `node.http.maxMessageSize`, the shared HTTP `SizeLimitHandler` may reject it with **HTTP 413** (`Payload Too Large`) before the target servlet handles the request. If the request reaches a servlet and the servlet-side `Util.checkBodySize` check detects the oversized body, the endpoint follows its own error-response format, which for some endpoints is still **HTTP 200** with an error body.
- When non-blocking rate limiting is enabled and the shared `RateLimiterServlet` cannot acquire a permit, it returns **HTTP 200** with body `{"Error":"class java.lang.IllegalAccessException : lack of computing resources"}` before the target servlet runs. This is a shared-layer error rather than an endpoint business error.
- When the node runs in lite fullnode mode and `openHistoryQueryWhenLiteFN` is not enabled, `LiteFnQueryHttpFilter` returns **HTTP 200** for ~24 historical-query endpoints (`getblockbynum` / `gettransactionbyid` / `gettransactioninfobyid` / `gettransactioninfobyblocknum` / `getblockbyid` / `getblockbylatestnum` / `getblockbylimitnext` / `gettransactioncountbyblocknum`, etc.) but the body is the bare string `this API is closed because this node is a lite fullnode` (**not JSON**) — a naive `JSON.parse` will throw, so clients must check the prefix as a string first.
- Network-layer errors produced by the servlet container or a reverse proxy (502, 504, connection refused, etc.) are out of scope for this document.

<!-- BEGIN GENERATED HTTP ERROR CATALOG -->
### HTTP error catalog

Catalog IDs and retry classifications are defined by `openapi.yaml` under `x-tron-error-model`. They are machine-readable documentation classifications, not fields returned by java-tron on the wire.

`Automatic retry` maps exactly to catalog `retryable`: only `Yes` permits automatic replay of the same logical operation. Conditional retry classes remain `No` until the `Scope / action` precondition is satisfied.

| Catalog ID | Wire signal | Meaning | Automatic retry | Retry class | Scope / action |
|---|---|---|---|---|---|
| `HTTP_RATE_LIMITED` | HTTP 200 + `$.Error` contains `lack of computing resources` | The shared servlet rate limiter rejected the request. | Yes | `SAFE_WITH_BACKOFF` | Retry automatically with exponential backoff and jitter; no Retry-After header is returned. |
| `HTTP_SERVLET_EXCEPTION` | HTTP 200 + free-form `$.Error` | A servlet returned an exception class and message in JavaTronError. | No | `UNKNOWN` | Inspect the concrete Error text and endpoint context; do not retry automatically from this fallback classification. |
| `HTTP_API_DISABLED` | HTTP 404 + `$.Error` = `this API is unavailable due to config` | The endpoint is disabled by node configuration. | No | `AFTER_STATE_CHANGE` | Use a node where the endpoint is enabled, or wait for node configuration to change. |
| `HTTP_LITE_FULLNODE_HISTORY_DISABLED` | HTTP 200 + bare text `this API is closed because this node is a lite fullnode` | A lite FullNode rejected a historical block or transaction query. | No | `AFTER_STATE_CHANGE` | Use a full node, or wait for openHistoryQueryWhenLiteFN to change. |
| `HTTP_REQUEST_TOO_LARGE` | HTTP 413 (`text/html`) | The request exceeds node.http.maxMessageSize. | No | `AFTER_REQUEST_REBUILD` | Reduce the request body before resubmitting. |
| `RETURN_SIGERROR` | `$.code` or `$.result.code` = `SIGERROR` | The transaction signature is invalid. | No | `NEVER` | Correct the signature and sign again. |
| `RETURN_CONTRACT_VALIDATE_ERROR` | `$.code` or `$.result.code` = `CONTRACT_VALIDATE_ERROR` | Contract validation failed. | No | `AFTER_REQUEST_REBUILD` | Correct parameters, balance, or permissions and rebuild the request. |
| `RETURN_CONTRACT_EXE_ERROR` | `$.code` or `$.result.code` = `CONTRACT_EXE_ERROR` | Contract execution failed. | No | `AFTER_STATE_CHANGE` | Inspect the message; retry only after relevant contract or chain state changes. |
| `RETURN_BANDWITH_ERROR` | `$.code` or `$.result.code` = `BANDWITH_ERROR` | Account bandwidth or another account resource is insufficient. | No | `AFTER_STATE_CHANGE` | Retry only after bandwidth/resource recovery; rebuild if the transaction expires. |
| `RETURN_DUP_TRANSACTION_ERROR` | `$.code` or `$.result.code` = `DUP_TRANSACTION_ERROR` | The transaction is already known to the node. | No | `VERIFY_BEFORE_RETRY` | Query by txid before deciding whether a new transaction is required. |
| `RETURN_TAPOS_ERROR` | `$.code` or `$.result.code` = `TAPOS_ERROR` | The transaction block reference is invalid or stale. | No | `AFTER_REQUEST_REBUILD` | Rebuild with a recent reference block and sign again. |
| `RETURN_TOO_BIG_TRANSACTION_ERROR` | `$.code` or `$.result.code` = `TOO_BIG_TRANSACTION_ERROR` | The transaction is too large. | No | `AFTER_REQUEST_REBUILD` | Reduce or split the transaction before resubmitting. |
| `RETURN_TRANSACTION_EXPIRATION_ERROR` | `$.code` or `$.result.code` = `TRANSACTION_EXPIRATION_ERROR` | The transaction has expired. | No | `AFTER_REQUEST_REBUILD` | Rebuild with a new expiration and sign again. |
| `RETURN_SERVER_BUSY` | `$.code` or `$.result.code` = `SERVER_BUSY` | The node has too many pending transactions. | Yes | `SAFE_WITH_BACKOFF` | Retry automatically with exponential backoff and jitter, or use another healthy node. |
| `RETURN_NO_CONNECTION` | `$.code` or `$.result.code` = `NO_CONNECTION` | The node has no active peer connection. | Yes | `SAFE_WITH_BACKOFF` | Retry with backoff after connectivity recovers, or use another connected node. |
| `RETURN_NOT_ENOUGH_EFFECTIVE_CONNECTION` | `$.code` or `$.result.code` = `NOT_ENOUGH_EFFECTIVE_CONNECTION` | The node has too few effective peer connections. | Yes | `SAFE_WITH_BACKOFF` | Retry with backoff after effective peers recover, or use another node. |
| `RETURN_BLOCK_UNSOLIDIFIED` | `$.code` or `$.result.code` = `BLOCK_UNSOLIDIFIED` | The node is temporarily in an unsolidified-block state. | Yes | `SAFE_WITH_BACKOFF` | Retry with backoff after block solidification, or use another synchronized node. |
| `RETURN_OTHER_ERROR` | `$.code` or `$.result.code` = `OTHER_ERROR` | The Return payload reports an unclassified failure. | No | `UNKNOWN` | Inspect the message; do not retry automatically without a more specific transient cause. |
| `SIGN_WEIGHT_NOT_ENOUGH_PERMISSION` | `$.result.code` = `NOT_ENOUGH_PERMISSION` | The accumulated signature weight is insufficient. | No | `AFTER_REQUEST_REBUILD` | Add valid signatures for the selected permission before trying again. |
| `SIGN_WEIGHT_SIGNATURE_FORMAT_ERROR` | `$.result.code` = `SIGNATURE_FORMAT_ERROR` | A signature has an invalid format. | No | `NEVER` | Correct the signature format and sign again. |
| `SIGN_WEIGHT_COMPUTE_ADDRESS_ERROR` | `$.result.code` = `COMPUTE_ADDRESS_ERROR` | An address cannot be recovered from a signature. | No | `NEVER` | Correct the signature so the signer address can be recovered. |
| `SIGN_WEIGHT_PERMISSION_ERROR` | `$.result.code` = `PERMISSION_ERROR` | Permission evaluation failed for the account, selected permission, operation, or supplied signatures. | No | `UNKNOWN` | Inspect result.message; correct Permission_id/signatures or wait for account permission state to change. Do not retry automatically. |
| `SIGN_WEIGHT_OTHER_ERROR` | `$.result.code` = `OTHER_ERROR` | Signature-weight evaluation returned an unclassified failure. | No | `UNKNOWN` | Inspect result.message; do not retry automatically without a more specific transient cause. |
| `APPROVED_LIST_SIGNATURE_FORMAT_ERROR` | `$.result.code` = `SIGNATURE_FORMAT_ERROR` | A signature has an invalid format. | No | `NEVER` | Correct the signature format and sign again. |
| `APPROVED_LIST_COMPUTE_ADDRESS_ERROR` | `$.result.code` = `COMPUTE_ADDRESS_ERROR` | An address cannot be recovered from a signature. | No | `NEVER` | Correct the signature so the signer address can be recovered. |
| `APPROVED_LIST_OTHER_ERROR` | `$.result.code` = `OTHER_ERROR` | Approved-list evaluation returned an unclassified failure. | No | `UNKNOWN` | Inspect result.message; do not retry automatically without a more specific transient cause. |
| `TRANSACTION_RESULT_FAILED` | `$.transaction.ret[0].ret` = `FAILED` | The generated transaction result reports FAILED. | No | `AFTER_STATE_CHANGE` | Inspect the transaction result and correct or rebuild the transaction. |
| `INVALID_ADDRESS` | `wallet_validateaddress_get` or `wallet_validateaddress_post`: `$.result` = `false` | Address validation returned result=false. | No | `NEVER` | Correct the address encoding or visible mode before validating again. |
<!-- END GENERATED HTTP ERROR CATALOG -->

## Account

| Endpoint | Description |
|---|---|
| [`/wallet/getaccount`](account/getaccount.md) | Query an account by address |
| [`/wallet/getaccountbalance`](account/getaccountbalance.md) | Query an account's balance at a specific block |
| [`/wallet/getaccountnet`](account/getaccountnet.md) | Query an account's bandwidth resources |
| [`/wallet/getaccountresource`](account/getaccountresource.md) | Query bandwidth + energy + TronPower |
| [`/wallet/createaccount`](account/createaccount.md) | Create an on-chain account (costs 1 TRX) |
| [`/wallet/updateaccount`](account/updateaccount.md) | Update an account's name |
| [`/wallet/accountpermissionupdate`](account/accountpermissionupdate.md) | Configure multi-sig permissions |
| [`/wallet/validateaddress`](account/validateaddress.md) | Validate an address |

## Block / transaction query

| Endpoint | Description |
|---|---|
| [`/wallet/getnowblock`](block-and-tx-query/getnowblock.md) | Latest block |
| [`/wallet/getblock`](block-and-tx-query/getblock.md) | Generic block query (by num or hash) |
| [`/wallet/getblockbynum`](block-and-tx-query/getblockbynum.md) | Block by height |
| [`/wallet/getblockbyid`](block-and-tx-query/getblockbyid.md) | Block by hash |
| [`/wallet/getblockbylimitnext`](block-and-tx-query/getblockbylimitnext.md) | Blocks in a range |
| [`/wallet/getblockbylatestnum`](block-and-tx-query/getblockbylatestnum.md) | The most recent N blocks |
| [`/wallet/getblockbalance`](block-and-tx-query/getblockbalance.md) | Per-account balance changes within a block |
| [`/wallet/gettransactioncountbyblocknum`](block-and-tx-query/gettransactioncountbyblocknum.md) | Transaction count in a block |
| [`/wallet/gettransactionbyid`](block-and-tx-query/gettransactionbyid.md) | Transaction by txid |
| [`/wallet/gettransactioninfobyid`](block-and-tx-query/gettransactioninfobyid.md) | Transaction receipt by txid |
| [`/wallet/gettransactioninfobyblocknum`](block-and-tx-query/gettransactioninfobyblocknum.md) | Transaction receipts by block |
| [`/wallet/getpendingsize`](block-and-tx-query/getpendingsize.md) | Pending pool size |
| [`/wallet/gettransactionfrompending`](block-and-tx-query/gettransactionfrompending.md) | Single pending transaction |
| [`/wallet/gettransactionlistfrompending`](block-and-tx-query/gettransactionlistfrompending.md) | All pending transaction IDs |

## Transaction build / broadcast

| Endpoint | Description |
|---|---|
| [`/wallet/createtransaction`](tx-build-and-broadcast/createtransaction.md) | Build a TRX transfer transaction |
| [`/wallet/getsignweight`](tx-build-and-broadcast/getsignweight.md) | Current multi-sig weight |
| [`/wallet/getapprovedlist`](tx-build-and-broadcast/getapprovedlist.md) | Addresses that have already signed |
| [`/wallet/broadcasttransaction`](tx-build-and-broadcast/broadcasttransaction.md) | Broadcast a signed transaction (JSON) |
| [`/wallet/broadcasthex`](tx-build-and-broadcast/broadcasthex.md) | Broadcast a signed transaction (hex) |

## TRC-10 asset

| Endpoint | Description |
|---|---|
| [`/wallet/createassetissue`](asset/createassetissue.md) | Issue a TRC-10 token |
| [`/wallet/updateasset`](asset/updateasset.md) | Update a TRC-10's description / URL / limits |
| [`/wallet/transferasset`](asset/transferasset.md) | Transfer TRC-10 |
| [`/wallet/participateassetissue`](asset/participateassetissue.md) | Participate in a TRC-10 fundraising |
| [`/wallet/unfreezeasset`](asset/unfreezeasset.md) | Unfreeze TRC-10 frozen by the issuer |
| [`/wallet/getassetissuebyid`](asset/getassetissuebyid.md) | Look up a TRC-10 by id (recommended) |
| [`/wallet/getassetissuebyname`](asset/getassetissuebyname.md) | Look up a TRC-10 by name (errors on duplicates) |
| [`/wallet/getassetissuelistbyname`](asset/getassetissuelistbyname.md) | All TRC-10s with a given name |
| [`/wallet/getassetissuebyaccount`](asset/getassetissuebyaccount.md) | TRC-10s issued by an account |
| [`/wallet/getassetissuelist`](asset/getassetissuelist.md) | All TRC-10s on the network |
| [`/wallet/getpaginatedassetissuelist`](asset/getpaginatedassetissuelist.md) | Paginated TRC-10 list |

## Smart contract

| Endpoint | Description |
|---|---|
| [`/wallet/deploycontract`](smart-contract/deploycontract.md) | Deploy a contract |
| [`/wallet/triggersmartcontract`](smart-contract/triggersmartcontract.md) | Trigger a contract (write) |
| [`/wallet/triggerconstantcontract`](smart-contract/triggerconstantcontract.md) | Read-only contract call |
| [`/wallet/estimateenergy`](smart-contract/estimateenergy.md) | Estimate energy usage of a call |
| [`/wallet/getcontract`](smart-contract/getcontract.md) | Contract metadata |
| [`/wallet/getcontractinfo`](smart-contract/getcontractinfo.md) | Full contract runtime info |
| [`/wallet/clearabi`](smart-contract/clearabi.md) | Clear a contract's ABI |
| [`/wallet/updatesetting`](smart-contract/updatesetting.md) | Change the user-energy percentage |
| [`/wallet/updateenergylimit`](smart-contract/updateenergylimit.md) | Change the deployer's energy limit |

## Witness / governance

| Endpoint | Description |
|---|---|
| [`/wallet/createwitness`](witness-and-governance/createwitness.md) | Apply to become an SR candidate |
| [`/wallet/updatewitness`](witness-and-governance/updatewitness.md) | Update an SR's URL |
| [`/wallet/listwitnesses`](witness-and-governance/listwitnesses.md) | All SR candidates |
| [`/wallet/getpaginatednowwitnesslist`](witness-and-governance/getpaginatednowwitnesslist.md) | Paginated SR list |
| [`/wallet/votewitnessaccount`](witness-and-governance/votewitnessaccount.md) | Vote for SRs |
| [`/wallet/getBrokerage`](witness-and-governance/getBrokerage.md) | An SR's current brokerage rate |
| [`/wallet/updateBrokerage`](witness-and-governance/updateBrokerage.md) | Update an SR's brokerage |
| [`/wallet/getReward`](witness-and-governance/getReward.md) | Claimable rewards for an account |
| [`/wallet/withdrawbalance`](witness-and-governance/withdrawbalance.md) | Withdraw block production rewards / dividends |
| [`/wallet/proposalcreate`](witness-and-governance/proposalcreate.md) | Create a chain-parameter proposal |
| [`/wallet/proposalapprove`](witness-and-governance/proposalapprove.md) | Vote on a proposal as an SR |
| [`/wallet/proposaldelete`](witness-and-governance/proposaldelete.md) | Withdraw your own proposal |
| [`/wallet/listproposals`](witness-and-governance/listproposals.md) | List of proposals |
| [`/wallet/getproposalbyid`](witness-and-governance/getproposalbyid.md) | Proposal by ID |
| [`/wallet/getpaginatedproposallist`](witness-and-governance/getpaginatedproposallist.md) | Paginated proposal list |
| [`/wallet/getchainparameters`](witness-and-governance/getchainparameters.md) | Current chain parameters |
| [`/wallet/getnextmaintenancetime`](witness-and-governance/getnextmaintenancetime.md) | Next maintenance period time |

## Stake 1.0 (unfreeze and query only)

After proposal #70 `UNFREEZE_DELAY_DAYS` was approved (already active on mainnet), new V1 freezes are rejected by the chain; the unfreeze and query endpoints are kept to handle outstanding positions.

| Endpoint | Description |
|---|---|
| [`/wallet/freezebalance`](stake-v1/freezebalance.md) | Freeze TRX for resources (V1, **chain rejects new requests**) |
| [`/wallet/unfreezebalance`](stake-v1/unfreezebalance.md) | Unfreeze matured resources (V1, still usable for legacy positions) |
| [`/wallet/getdelegatedresource`](stake-v1/getdelegatedresource.md) | Query delegation records (V1, read-only) |
| [`/wallet/getdelegatedresourceaccountindex`](stake-v1/getdelegatedresourceaccountindex.md) | Query delegation counterparty addresses (V1, read-only) |

## Stake 2.0

| Endpoint | Description |
|---|---|
| [`/wallet/freezebalancev2`](stake-v2/freezebalancev2.md) | Freeze TRX for resources |
| [`/wallet/unfreezebalancev2`](stake-v2/unfreezebalancev2.md) | Initiate unfreeze (14-day waiting period) |
| [`/wallet/withdrawexpireunfreeze`](stake-v2/withdrawexpireunfreeze.md) | Withdraw matured unfreezes |
| [`/wallet/cancelallunfreezev2`](stake-v2/cancelallunfreezev2.md) | Cancel all unmatured unfreezes |
| [`/wallet/delegateresource`](stake-v2/delegateresource.md) | Delegate resources to another account |
| [`/wallet/undelegateresource`](stake-v2/undelegateresource.md) | Undelegate resources from another account |
| [`/wallet/getdelegatedresourcev2`](stake-v2/getdelegatedresourcev2.md) | Query delegation records |
| [`/wallet/getdelegatedresourceaccountindexv2`](stake-v2/getdelegatedresourceaccountindexv2.md) | Query delegation counterparty addresses |
| [`/wallet/getcandelegatedmaxsize`](stake-v2/getcandelegatedmaxsize.md) | Current maximum delegatable amount |
| [`/wallet/getavailableunfreezecount`](stake-v2/getavailableunfreezecount.md) | Remaining unfreeze count |
| [`/wallet/getcanwithdrawunfreezeamount`](stake-v2/getcanwithdrawunfreezeamount.md) | Withdrawable unfreeze amount at a given time |

## Node / pricing / tools

| Endpoint | Description |
|---|---|
| [`/wallet/getnodeinfo`](node-and-tools/getnodeinfo.md) | Node status (also `/monitor/getnodeinfo`) |
| [`/wallet/listnodes`](node-and-tools/listnodes.md) | Known peers (also `/net/listnodes`) |
| [`/wallet/getenergyprices`](node-and-tools/getenergyprices.md) | Historical energy unit prices |
| [`/wallet/getbandwidthprices`](node-and-tools/getbandwidthprices.md) | Historical bandwidth unit prices |
| [`/wallet/getburntrx`](node-and-tools/getburntrx.md) | Cumulative burned TRX |
