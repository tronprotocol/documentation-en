# updateasset

TRON API method that creates an unsigned transaction for updating the information of an existing TRC10 token. This allows token issuers to modify certain properties of their tokens after creation.

## HTTP Request

`POST /wallet/updateasset`

## Supported Paths

- `/wallet/updateasset`

## Parameters

- owner_address — the address that issued the token and wants to update it
- description — new description of the token project (string)
- url — new official website URL for the token project (string)
- new_limit — new bandwidth limit provided by token issuer for token operations (integer, optional)
- new_public_limit — new public bandwidth limit available for this token (integer, optional)
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the update asset contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/updateasset \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "description": "Updated description for the TRC10 token",
  "url": "https://updated-example.com",
  "new_limit": 2000000,
  "new_public_limit": 2000000,
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

- Updating token project information such as description and website URL
- Modifying bandwidth allocations for token operations
- Building token management interfaces that allow post-issuance updates
- Implementing governance features that allow token information changes
