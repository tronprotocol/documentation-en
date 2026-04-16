# getassetissuebyid

TRON API method that retrieves detailed information about a TRC10 token using its unique asset ID. TRC10 tokens are native TRON assets that can be issued directly on the blockchain without requiring smart contracts.

## HTTP Request

`POST /wallet/getassetissuebyid`

## Supported Paths

- `/wallet/getassetissuebyid`
- `/walletsolidity/getassetissuebyid`

## Parameters

- value — the TRC10 token ID to query (string format)

## Response

- owner_address — address of the account that issued the token
- name — full name of the token
- abbr — token symbol or abbreviation
- total_supply — total number of tokens issued
- trx_num — TRX amount used in the exchange rate calculation
- precision — number of decimal places supported by the token
- num — token amount used in the exchange rate calculation (tokens per TRX)
- start_time — ICO start timestamp (when token sale began)
- end_time — ICO end timestamp (when token sale ended)
- description — detailed description of the token project
- url — official website URL for the token project
- id — unique identifier for the token
- free_asset_net_limit — bandwidth provided by token issuer for token operations
- public_free_asset_net_limit — public bandwidth limit available for this token
- public_free_asset_net_usage — amount of public bandwidth currently used
- public_latest_free_net_time — timestamp of the latest free bandwidth usage

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getassetissuebyid \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "1000001"
}
'
```

### Response

```json
{
  "owner_address": "<string>",
  "name": "<string>",
  "abbr": "<string>",
  "total_supply": 123,
  "trx_num": 123,
  "precision": 123,
  "num": 123,
  "start_time": 123,
  "end_time": 123,
  "description": "<string>",
  "url": "<string>",
  "id": "<string>",
  "free_asset_net_limit": 123,
  "public_free_asset_net_limit": 123,
  "public_free_asset_net_usage": 123,
  "public_latest_free_net_time": 123
}
```

## Use Case

- Retrieving comprehensive information about TRC10 tokens for display in wallets and exchanges.
- Analyzing token economics including supply, exchange rates, and ICO details.
- Building token explorers and analytical tools for the TRON ecosystem.
- Verifying token authenticity and project information before trading or investing.
- Understanding bandwidth allocation and usage patterns for specific tokens.
- Implementing token management features in decentralized applications.
