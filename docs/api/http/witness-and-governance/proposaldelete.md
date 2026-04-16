# proposaldelete

TRON API method that allows the proposal creator to delete or cancel a governance proposal before it reaches the execution phase.

## HTTP Request

`POST /wallet/proposaldelete`

## Supported Paths

- `/wallet/proposaldelete`

## Parameters

- owner_address — the address of the proposal creator who wants to delete the proposal. Must be in base58 or hex format.
- proposal_id — the ID of the proposal to delete.
- visible — optional boolean parameter. When set to true, the address should be in base58 format. Default is false.

## Response

- txID — the transaction hash of the proposal deletion
- raw_data — the raw transaction data
- raw_data_hex — the raw transaction data in hex format
- signature — array of transaction signatures

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/proposaldelete \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "proposal_id": 1,
  "visible": true
}
'
```

### Response

```json
{
  "txID": "<string>",
  "raw_data": {
    "contract": "<array>",
    "ref_block_bytes": "<string>",
    "ref_block_hash": "<string>",
    "expiration": 123,
    "timestamp": 123
  },
  "raw_data_hex": "<string>",
  "signature": [
    "<string>"
  ]
}
```

## Use Case

- Cancelling proposals that are no longer needed
- Withdrawing proposals with errors or incorrect parameters
- Managing proposal lifecycle in governance systems
- Preventing unwanted proposals from reaching execution
