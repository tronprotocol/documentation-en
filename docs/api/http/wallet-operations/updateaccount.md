# updateaccount

TRON API method that updates an account’s name on the TRON blockchain. This method creates an unsigned transaction to set or modify the account name field.

## HTTP Request

`POST /wallet/updateaccount`

## Supported Paths

- `/wallet/updateaccount`

## Parameters

- owner_address — the account address whose name will be updated.
- account_name — the new name for the account in hexadecimal format. Must be converted from string to hex before sending.
- visible — optional boolean parameter. When set to true, the address is in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the account update contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/updateaccount \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "account_name": "0x7570646174654e616d6531353330383933343635353139",
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

- Setting a human-readable name for an account.
- Updating account metadata for identification purposes.
- Labeling accounts in wallet applications and explorers.
- Organizing multiple accounts with descriptive names.
