# transferasset

TRON API method that creates an unsigned transaction for transferring TRC10 tokens between accounts.

## HTTP Request

`POST /wallet/transferasset`

## Supported Paths

- `/wallet/transferasset`

## Parameters

- owner_address — the address sending the TRC10 tokens
- to_address — the address receiving the TRC10 tokens
- asset_name — the name or ID of the TRC10 token to transfer
- amount — the amount of tokens to transfer
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the asset transfer contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/transferasset \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "to_address": "TFgY1uN8buRxAtV2r6Zy5sG3ACko6pJT1y",
  "asset_name": "TOKEN_NAME",
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
  "raw_data": {},
  "raw_data_hex": "<string>"
}
```

## Use Case

- Transferring TRC10 tokens between accounts
- Building token transfer functionality in wallets and DApps
- Creating automated token distribution systems
- Implementing payment systems using TRC10 tokens
- Facilitating token trading and exchange operations
