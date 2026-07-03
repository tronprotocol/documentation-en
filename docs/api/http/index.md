# java-tron HTTP API

This directory documents the FullNode HTTP endpoints under `framework/src/main/java/org/tron/core/services/http/`. One markdown file per endpoint, named after the last segment of the URL (e.g. `/wallet/getnodeinfo` → `getnodeinfo.md`).

The following categories are intentionally not covered:

- Exchange (DEX) endpoints
- Market (order book) endpoints
- Shielded (anonymous transaction) endpoints

## Common conventions

- **Method**: a few pure-query endpoints accept `GET`, but most POST endpoints only accept `POST` with a JSON body.
- **`visible`**: when `true`, addresses are base58check strings and text fields (URL, descriptions, etc.) are UTF-8 strings; when `false` (default), they are hex strings.
- **Builder endpoints** return an unsigned `protocol.Transaction`. The caller signs it locally and broadcasts it via [`/wallet/broadcasttransaction`](tx-build-and-broadcast/broadcasttransaction.md) or [`/wallet/broadcasthex`](tx-build-and-broadcast/broadcasthex.md).
- **`permission_id`**: optional on builder endpoints; selects which `Permission` to use for multi-sig accounts.
- **Amount unit**: TRC-10 amounts use the issuer-defined precision; every other amount is in sun (1 TRX = 1e6 sun).

!!! warning "XSS security note"

    Although the HTTP API reduces the risk of the browser parsing responses directly as HTML by setting `Content-Type` to `application/json`, this does not fully eliminate XSS. Some endpoints do not strictly validate their inputs, and responses may echo user-controlled content (especially when `visible=true`, where fields such as addresses and memos may be returned verbatim as UTF-8 strings). Before rendering any data returned by the API into a page, handle it safely according to the output context.

    The correct approach is to choose the encoding that matches where the data is placed: in an HTML text context, use HTML entity encoding (e.g. `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`), or rely on your front-end framework's default output escaping (such as React JSX or Vue template escaping). Only use `encodeURIComponent()` and similar URL-encoding methods when the data is placed into a URL parameter. Note that `encodeURIComponent()` / `escape()` are URL encoding (or legacy encoding) and cannot replace output escaping in an HTML context.

    For more guidance, see the [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html).

## Error responses

In the vast majority of cases the HTTP status is **200** — business errors are conveyed in the response body, so the client must parse the body to determine success or failure. Known exceptions:

- When an endpoint is explicitly disabled via the node's `disabledApiList`, `HttpApiAccessFilter` returns **HTTP 404** with body `{"Error": "this API is unavailable due to config"}`.
- When the node runs in lite fullnode mode and `openHistoryQueryWhenLiteFN` is not enabled, `LiteFnQueryHttpFilter` returns **HTTP 200** for ~24 historical-query endpoints (`getblockbynum` / `gettransactionbyid` / `gettransactioninfobyid` / `gettransactioninfobyblocknum` / `getblockbyid` / `getblockbylatestnum` / `getblockbylimitnext` / `gettransactioncountbyblocknum`, etc.) but the body is the bare string `this API is closed because this node is a lite fullnode` (**not JSON**) — a naive `JSON.parse` will throw, so clients must check the prefix as a string first.
- Network-layer errors produced by the servlet container or a reverse proxy (502, 504, connection refused, etc.) are out of scope for this document.

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
