# getpaginatedassetissuelist

TRON API method that retrieves a paginated list of all TRC10 tokens issued on the TRON network. This method provides efficient pagination support for browsing through large numbers of tokens without overwhelming the response.

## HTTP Request

`POST /wallet/getpaginatedassetissuelist`

## Supported Paths

- `/wallet/getpaginatedassetissuelist`
- `/walletsolidity/getpaginatedassetissuelist`

## Parameters

- offset — number of records to skip from the beginning (starting point for pagination)
- limit — maximum number of TRC10 tokens to return in the response

## Response

- assetIssue — array of TRC10 token information objects, each containing:
  - id — unique token ID
  - owner_address — address of the token issuer
  - name — token name in hex format
  - abbr — token abbreviation in hex format
  - total_supply — total supply of the token
  - trx_num — TRX amount in exchange ratio
  - precision — token decimal places
  - num — token amount in exchange ratio
  - start_time — token sale start timestamp
  - end_time — token sale end timestamp
  - description — token description in hex format
  - url — token website URL in hex format
  - free_asset_net_limit — free bandwidth allocation per account
  - public_free_asset_net_limit — total public free bandwidth limit
  - frozen_supply — array of frozen token supply information

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getpaginatedassetissuelist \
  --header 'Content-Type: application/json' \
  --data '
{
  "offset": 0,
  "limit": 20
}
'
```

### Response

```json
{
  "assetIssue": [
    {
      "id": "<string>",
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
      "free_asset_net_limit": 123,
      "public_free_asset_net_limit": 123,
      "frozen_supply": "<array>"
    }
  ]
}
```

## Use Case

- Building comprehensive TRC10 token listings and directories.
- Implementing paginated token browsers for better user experience.
- Creating analytics dashboards that analyze token distribution patterns.
- Developing token discovery platforms with efficient data loading.
- Building portfolio trackers that need to browse available tokens.
- Creating market data aggregators for TRC10 token ecosystems.
