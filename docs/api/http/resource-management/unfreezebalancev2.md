# unfreezebalancev2

TRON API method that unstakes TRX from the new staking mechanism. This method releases TRX tokens that were previously staked using freezebalancev2, initiating the unstaking process with a 14-day waiting period before tokens become available for withdrawal. This is the current recommended unstaking method.

## HTTP Request

`POST /wallet/unfreezebalancev2`

## Supported Paths

- `/wallet/unfreezebalancev2`

## Parameters

- owner_address — the address that owns the staked TRX to unstake (hex format)
- unfreeze_balance — the amount of TRX to unstake (in sun, where 1 TRX = 1,000,000 sun)
- resource — the resource type to release (“BANDWIDTH” or “ENERGY”)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- visible — boolean indicating address format used
- txID — transaction ID hash
- raw_data — raw transaction data object
- raw_data_hex — hexadecimal representation of raw transaction data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/unfreezebalancev2 \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "unfreeze_balance": 1000000,
  "resource": "BANDWIDTH",
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

- Unstaking TRX using the current staking mechanism.
- Initiating the 14-day unstaking period before tokens become withdrawable.
- Managing bandwidth and energy resource allocation by reducing staked amounts.
- Flexible unstaking of partial amounts rather than all-or-nothing.
