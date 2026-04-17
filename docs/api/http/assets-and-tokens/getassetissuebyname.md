# getassetissuebyname

TRON API method that retrieves information about a TRC10 token by its name.

## HTTP Request

`POST /wallet/getassetissuebyname`

## Supported Paths

- `/wallet/getassetissuebyname`
- `/walletsolidity/getassetissuebyname`

## Parameters

- value — the name of the TRC10 token to retrieve information for
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- assetIssue — array of asset issue information containing:
  - owner_address — token creator address
  - name — token name
  - abbr — token abbreviation
  - total_supply — total token supply
  - trx_num — TRX amount for exchange rate
  - num — token amount for exchange rate
  - start_time — ICO start time
  - end_time — ICO end time
  - description — token description
  - url — token website URL
  - id — token ID

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getassetissuebyname \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "54525854657374436f696e",
  "visible": false
}
'
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
      "num": 123,
      "start_time": 123,
      "end_time": 123,
      "description": "<string>",
      "url": "<string>",
      "id": "<string>"
    }
  ]
}
```

## Use Case

- Retrieving detailed information about TRC10 tokens
- Building token information displays in wallets and DApps
- Verifying token authenticity and properties
- Creating token discovery and analysis tools
- Implementing token trading interfaces

## Curl Examples

- search by name to see all matches
- fetch the exact token by id
- if you call wallet/getassetissuebyname with a non‑unique name (for example, SEED), the node can respond with:
- prefer wallet/getassetissuelistbyname to discover candidates, then wallet/getassetissuebyid to retrieve a specific token.
