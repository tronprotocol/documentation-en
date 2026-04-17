# proposalcreate

TRON API method that creates a new governance proposal on the TRON network. Super Representatives can use this method to propose changes to network parameters.

## HTTP Request

`POST /wallet/proposalcreate`

## Supported Paths

- `/wallet/proposalcreate`

## Parameters

- owner_address — the Super Representative address creating the proposal. Must be in base58 or hex format.
- parameters — object containing the parameter ID and its new value to be proposed.
- visible — optional boolean parameter. When set to true, the address should be in base58 format. Default is false.

## Response

- txID — the transaction hash of the proposal creation
- raw_data — the raw transaction data
- raw_data_hex — the raw transaction data in hex format
- signature — array of transaction signatures

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/proposalcreate \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "parameters": {
    "0": 3000000
  },
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

- Creating governance proposals to modify network parameters
- Proposing changes to transaction fees and resource costs
- Initiating protocol upgrades and parameter adjustments
- Participating in TRON’s decentralized governance system
