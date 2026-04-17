# participateassetissue

TRON API method that creates an unsigned transaction for participating in a TRC10 token Initial Coin Offering (ICO). This allows users to purchase newly issued TRC10 tokens during the offering period.

## HTTP Request

`POST /wallet/participateassetissue`

## Supported Paths

- `/wallet/participateassetissue`

## Parameters

- owner_address — the address participating in the token offering
- to_address — the address of the token issuer (who created the asset)
- asset_name — the name or ID of the TRC10 token to purchase
- amount — the amount of TRX to spend on purchasing tokens
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the participate asset issue contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/participateassetissue \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "to_address": "TFgY1uN8buRxAtV2r6Zy5sG3ACko6pJT1y",
  "asset_name": "MyToken",
  "amount": 1000000,
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
    "timestamp": 123
  },
  "raw_data_hex": "<string>"
}
```

## Use Case

- Participating in TRC10 token ICOs and crowdfunding campaigns
- Building automated investment tools for token offerings
- Creating token purchase functionality in wallet applications
- Implementing token sale participation features in DeFi platforms
