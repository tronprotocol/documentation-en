# unfreezeasset

TRON API method that creates an unsigned transaction for unfreezing TRC10 tokens that were previously frozen during token creation. This releases frozen tokens back to the token issuer’s available balance.

## HTTP Request

`POST /wallet/unfreezeasset`

## Supported Paths

- `/wallet/unfreezeasset`

## Parameters

- owner_address — the address that issued the token and wants to unfreeze tokens
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the unfreeze asset contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/unfreezeasset \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
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

- Releasing frozen TRC10 tokens after the freeze period expires
- Managing token supply and liquidity by unfreezing previously locked tokens
- Building token management tools that handle frozen supply schedules
- Implementing automated token unlock mechanisms in smart contracts
