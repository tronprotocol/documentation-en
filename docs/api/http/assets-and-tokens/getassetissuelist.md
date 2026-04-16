# getassetissuelist

TRON API method that retrieves a list of all TRC10 tokens that have been issued on the TRON network.

## HTTP Request

`POST /wallet/getassetissuelist`

## Supported Paths

- `/wallet/getassetissuelist`
- `/walletsolidity/getassetissuelist`

## Parameters

No parameters required for this method.

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
  --url https://api.shasta.trongrid.io/wallet/getassetissuelist \
  --header 'Content-Type: application/json' \
  --data '{}'
```

### Response

```json
{
  "assetIssue": [
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
  ]
}
```

## Use Case

- Building comprehensive token explorers and market overview dashboards
- Retrieving all available TRC10 tokens for wallet and exchange integrations
- Analyzing the complete TRC10 token ecosystem on TRON
- Creating token discovery interfaces for DeFi applications
