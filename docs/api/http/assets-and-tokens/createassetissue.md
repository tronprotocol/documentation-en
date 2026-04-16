# createassetissue

TRON API method that creates an unsigned transaction for issuing a new TRC10 token on the TRON network. TRC10 tokens are native TRON assets that can be created without deploying smart contracts.

## HTTP Request

`POST /wallet/createassetissue`

## Supported Paths

- `/wallet/createassetissue`

## Parameters

- owner_address — the address that will issue and own the token
- name — the full name of the token (string)
- abbr — the token symbol or abbreviation (string)
- total_supply — the total number of tokens to be issued (integer)
- trx_num — the TRX amount used in the exchange rate calculation (integer)
- num — the token amount used in the exchange rate calculation (integer)
- precision — the number of decimal places supported by the token (integer, 0-6)
- start_time — ICO start timestamp in milliseconds (integer)
- end_time — ICO end timestamp in milliseconds (integer)
- description — detailed description of the token project (string)
- url — official website URL for the token project (string)
- free_asset_net_limit — bandwidth provided by token issuer for token operations (integer, optional)
- public_free_asset_net_limit — public bandwidth limit available for this token (integer, optional)
- frozen_supply — array of frozen supply configurations (optional)
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the asset issue contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
  - fee_limit — maximum fee allowed for this transaction
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/createassetissue \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "name": "MyToken",
  "abbr": "MTK",
  "total_supply": 1000000000000,
  "trx_num": 1,
  "num": 1000,
  "start_time": 1640995200000,
  "end_time": 1672531200000,
  "description": "A new TRC10 token for the TRON ecosystem",
  "url": "https://example.com",
  "precision": 6,
  "free_asset_net_limit": 1000000,
  "public_free_asset_net_limit": 1000000,
  "frozen_supply": [
    {
      "frozen_amount": 123,
      "frozen_days": 123
    }
  ],
  "visible": true
}
'
```

### Response

```json
{
  "visible": true,
  "txID": "<string>",
  "raw_data": {
    "contract": "<array>",
    "ref_block_bytes": "<string>",
    "ref_block_hash": "<string>",
    "expiration": 123,
    "timestamp": 123,
    "fee_limit": 123
  },
  "raw_data_hex": "<string>"
}
```

## Use Case

- Creating new TRC10 tokens for projects and organizations
- Launching Initial Coin Offerings (ICOs) and token sales
- Building token issuance functionality in wallet applications
- Developing automated token creation systems for DeFi platforms
