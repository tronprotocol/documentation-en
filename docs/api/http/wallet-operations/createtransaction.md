# createtransaction

TRON API method that creates an unsigned TRX transfer transaction. This method generates a transaction object that transfers TRX from one address to another, which can then be signed and broadcast to the network.

## HTTP Request

`POST /wallet/createtransaction`

## Supported Paths

- `/wallet/createtransaction`

## Parameters

- to_address — the recipient’s TRON address (hex format)
- owner_address — the sender’s TRON address (hex format)
- amount — the amount of TRX to transfer (in sun, where 1 TRX = 1,000,000 sun)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- visible — boolean indicating address format used
- txID — transaction ID hash
- raw_data — raw transaction data object containing:
  - contract — array with transfer contract details
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of raw transaction data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/createtransaction \
  --header 'Content-Type: application/json' \
  --data '
{
  "to_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d",
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "amount": 1000,
  "visible": false
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

- Creating unsigned TRX transfer transactions that need to be signed separately.
- Building transactions for offline signing in secure environments.
- Implementing wallet functionality that separates transaction creation from signing.
- Preparing transactions for multi-signature workflows.
