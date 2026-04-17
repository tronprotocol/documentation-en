# getassetissuelistbyname

TRON API method that retrieves a list of TRC10 tokens that match a specified name pattern. This method allows searching for tokens by their names and is useful for discovering assets with similar or related names.

## HTTP Request

`POST /wallet/getassetissuelistbyname`

## Supported Paths

- `/wallet/getassetissuelistbyname`
- `/walletsolidity/getassetissuelistbyname`

## Parameters

- value — token name or pattern. Use plain text with visible: true, or hex‑encoded UTF‑8 with visible: false.
- visible — optional boolean. When true, value is plain text; when false, hex‑encoded. Default is true.

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
  - free_asset_net_limit — free bandwidth allocation
  - public_free_asset_net_limit — public free bandwidth limit
  - frozen_supply — frozen token supply details

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getassetissuelistbyname \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "SEED",
  "visible": true
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

- Searching for TRC10 tokens by name pattern or partial name matches.
- Discovering tokens with similar names or themes in the ecosystem.
- Building token discovery and search functionality in applications.
- Validating token names before creating new assets to avoid conflicts.
- Implementing auto-complete features for token selection interfaces.
- Analyzing token naming patterns and trends in the TRON network.

## Curl Examples

Search by plain name (recommended):
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/getassetissuelistbyname' \
 --header 'Content-Type: application/json' \
 --data '{
 "value": "SEED",
 "visible": true
 }'

The response lists multiple SEED tokens; each entry includes an id. To fetch a specific token, use wallet/getassetissuebyid with that id.
Query with a hex‑encoded name:
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/getassetissuelistbyname' \
 --header 'Content-Type: application/json' \
 --data '{
 "value": "54525854657374436f696e",
 "visible": false
 }'

TRC10 names are not unique. Prefer this endpoint to discover candidates, then call wallet/getassetissuebyid to retrieve the exact token by id.Bodyapplication/jsonvaluestringrequiredToken name or pattern. When visible is true, provide plain UTF‑8. When visible is false, provide hex‑encoded UTF‑8.visiblebooleandefault:trueWhen true, value is plain text; when false, hex‑encoded.Response200 - application/jsonList of TRC10 tokens matching the name patternassetIssueobject[]Array of TRC10 token informationShow child attributesLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/getassetissuelist | TRONwallet/getpaginatedassetissuelist | TRON
