# proposalapprove

TRON API method that allows Super Representatives to approve a governance proposal. Proposals need majority approval from Super Representatives to be executed.

## HTTP Request

`POST /wallet/proposalapprove`

## Supported Paths

- `/wallet/proposalapprove`

## Parameters

- owner_address — the Super Representative address approving the proposal. Must be in base58 or hex format.
- proposal_id — the ID of the proposal to approve.
- is_add_approval — boolean indicating whether to approve (true) or remove approval (false).
- visible — optional boolean parameter. When set to true, the address should be in base58 format. Default is false.

## Response

- txID — the transaction hash of the approval action
- raw_data — the raw transaction data
- raw_data_hex — the raw transaction data in hex format
- signature — array of transaction signatures

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/proposalapprove \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "proposal_id": 1,
  "is_add_approval": true,
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

- Approving governance proposals by Super Representatives
- Participating in the proposal voting process
- Supporting or rejecting proposed network parameter changes
- Managing proposal approval status in governance workflows
