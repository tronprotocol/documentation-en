# freezebalancev2

TRON API method that stakes TRX for resources using the new staking mechanism. This method freezes TRX tokens to obtain bandwidth or energy resources with improved flexibility, including the ability to unfreeze resources at any time.

## HTTP Request

`POST /wallet/freezebalancev2`

## Supported Paths

- `/wallet/freezebalancev2`

## Parameters

- owner_address — the address that owns the TRX to freeze (hex format)
- frozen_balance — the amount of TRX to freeze (in sun, where 1 TRX = 1,000,000 sun)
- resource — the resource type to obtain (“BANDWIDTH” or “ENERGY”)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- visible — boolean indicating address format used
- txID — transaction ID hash
- raw_data — raw transaction data object containing freeze contract details
- raw_data_hex — hexadecimal representation of raw transaction data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/freezebalancev2 \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "frozen_balance": 1000000,
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

- Staking TRX to obtain bandwidth for free transactions using the new mechanism.
- Freezing TRX to get energy for smart contract execution with improved flexibility.
- Taking advantage of the ability to unfreeze resources without waiting periods.
- Implementing modern TRON staking in wallets and DApps with better resource management.
