# TronGrid

The up-to-date TronGrid API Documentation is at [https://developers.tron.network/docs/tron-grid-intro](https://developers.tron.network/docs/tron-grid-intro).

## Introduction

TronGrid provides TRON clients running in the cloud, so you don't have to run one yourself to work with TRON on your next project.

TronGrid offers an easy to use hosted API, load balanced full nodes, secure and reliable developer tools with direct access to the TRON Network.

TronGrid uses a set of NodeJS apps to talk with Redis and PostgreSQL to provide a simple, fast and reliable query interface for the TRON API.

TronGrid supports 2 types of api:

- FullNode & SolidityNode api

TronGrid supports all the FullNode and SolidityNode api calls, you only need to add the url: `https://api.trongrid.io/`, like:

`https://api.trongrid.io/wallet/getnowblock`

- TronGrid v3 (TG3) api version

As this is the first iteration of the improved TronGrid, it starts with v1.
Example: `https://api.trongrid.io/v1`

**Parameters, Queries, & Return Values**

- Addresses in TG3 can be passed in base58 or hex formats.
- Query parameters can be passed in camelCase or snake_case.
- All returned JSON properties will be in snake_case (at the first level at least).
- **NB:** In this document, we will primarily use base58 and snake_case formats.

## Account APIs

1.&nbsp;Get Account Info By Address
*API:*
`https://api.trongrid.io/v1/accounts/:address`
*Params:*
address: The account’s address in base58 or hex format (0x... and 41...)
*Options:*
`only_confirmed` Shows only the situation at latest confirmed block.`true` | `false` default `false`.
*Example:*
`https://api.trongrid.io/v1/accounts/TLCuBEirVzB6V4menLZKw1jfBTFMZbuKq7?only_confirmed=false`


2.&nbsp;Get Transactions By Account Address
*API:*
`https://api.trongrid.io/v1/accounts/:address/transactions`
*Params:*
address: The account’s address.
*Options:*
`only_confirmed` Shows only confirmed. `true` | `false` default `false`.
`only_unconfirmed` Shows only unconfirmed. `true` | `false` default `false`.
`only_to` Only transaction to address. `true` | `false` default `false`.
`only_from` Only transaction from address. `true` | `false` default `false`.
`limit` The requested number of transaction per page. Default `20`. Max `200`.
`fingerprint` The fingerprint of the last transaction returned by the previous page.
`order_by` Pre sorts the results during the query. `order_by=block_number,asc`, `order_by=block_timestamp,desc`. `min_block_timestamp` The minimum transaction timestamp default `0`. `max_block_timestamp` The maximum transaction timestamp default `now`.

*Example:*
`https://api.trongrid.io/v1/accounts/TLCuBEirVzB6V4menLZKw1jfBTFMZbuKq/transactions?only_to=true&only_from=true`


3.&nbsp;Get Account Resources By Address
*API:*
`https://api.trongrid.io/v1/accounts/:address/resources`
*Params:*
address: The account’s address.
*Example:*
`https://api.trongrid.io/v1/accounts/TLCuBEirVzB6V4menLZKw1jfBTFMZbuKq/resources`

## Asset APIs

1.&nbsp;Get All Assets
*API:*
`https://api.trongrid.io/v1/assets`
*Options:*
`order_by` Sorts the results. Accepted fields: `total_supply,asc` | `total_supply,desc`, `start_time,asc` | `start_time,desc`, `end_time,asc` | `end_time,desc`, `id,asc` | `id,desc`. Example: `order_by=total_supply,asc`.

2.&nbsp;Get Assets By Identifier
*API:*
`https://api.trongrid.io/v1/assets/:identifier`
*Params:*
identifier: The identifier to be used to retrieve the asset. It can be the ID of the asset, or the issuer address.

3.&nbsp;Get Assets By Name
*API:*
`https://api.trongrid.io/v1/assets/:name/list`
*Params:*
name: The name of the asset.
*Options:*
`limit` The requested number of assets per page. Default `20`. Max `200`. When there is a pagination, the minimum limit is set to `20`.
`fingerprint` The fingerprint of the last asset returned by the previous page.
`order_by` Pre sorts the results during the query. `order_by=total_supply,asc` (starts from the rarest token). `order_by=start_time,desc` (starts from the most recent ICO).

## Block APIs

1.&nbsp;Returns Events By Block Identifier
*API:*
`https://api.trongrid.io/v1/blocks/:identifier/events`
*Params:*
identifier: It can be either latest, a block number or a block id.

## Contract APIs

1.&nbsp;Get Events By Contract Address
*API:*
`https://api.trongrid.io/v1/contracts/:address/events`
*Params:*
address: The address of the deployed contract.
*Options:*
`only_confirmed` Shows only confirmed. `true` | `false` default `false`.
`only_unconfirmed` Shows only unconfirmed. `true` | `false` default `false`.
`event_name` The name of the event.
`block_number` The block number for which the events are required.
`min_block_timestamp` The minimum block timestamp default `0`.
`max_block_timestamp` The maximum block timestamp default `now`.
`limit` For pagination. Limit 20.
`fingerprint` The fingerprint of last event retrieved in the page.
`order_by` Sort the events. Accepted values: `block_timestamp,asc`, `block_timestamp,desc`(default).

2.&nbsp;Get Transactions By Contract Address
*API:*
`https://api.trongrid.io/v1/contracts/:address/transactions`
*Params:*
address: The address of the deployed contract.
*Options:*
`only_confirmed` Shows only confirmed. `true` | `false` default `false`.
`only_unconfirmed` Shows only unconfirmed. `true` | `false` default `false`.
`min_block_timestamp` The minimum block timestamp default `0`.
`max_block_timestamp` The maximum block timestamp default `now`.
`limit` For pagination. Limit `20`.
`fingerprint` The fingerprint of last event retrieved in the page.
`order_by` Sort the events. Accepted values: `block_timestamp,asc`, `block_timestamp,desc` (default).

## Transaction APIs

1.&nbsp;Get Events By Transaction ID
*API:*
`https://api.trongrid.io/v1/transactions/:id/events`
*Params:*
id: The id of the transaction.

2.&nbsp;Get Transaction By Transaction ID
*API:*
`https://api.trongrid.io/v1/transactions/:id/events`
*Params:*
id: The id of the transaction.
