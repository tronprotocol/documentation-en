# getassetissuebyaccount

TRON API method that queries the TRC10 token information issued by an account. TRC10 tokens are native TRON assets that can be issued directly on the blockchain without requiring smart contracts.

## HTTP Request

`POST /wallet/getassetissuebyaccount`

## Supported Paths

- `/wallet/getassetissuebyaccount`

## Parameters

- address — the token issuer's account address
- visible — optional boolean. When true, the address is in base58 format; when false, hex format. Defaults to false

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
  --url https://api.shasta.trongrid.io/wallet/getassetissuebyaccount \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
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

- Querying all TRC10 tokens issued by a specific account.
- Building token portfolio views showing all tokens created by an issuer.
- Auditing token issuance history for a given account.
- Displaying issuer-level token information in wallets and explorers.
- Verifying token ownership and issuance details for compliance purposes.
