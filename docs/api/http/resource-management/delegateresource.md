# delegateresource

TRON API method that delegates resources to another account. This method allows you to delegate bandwidth or energy resources obtained from staking TRX to another address, enabling that address to use your resources for transactions.

## HTTP Request

`POST /wallet/delegateresource`

## Supported Paths

- `/wallet/delegateresource`

## Parameters

- owner_address — the address that owns the resources to delegate (hex format)
- receiver_address — the address that will receive the delegated resources (hex format)
- balance — the amount of TRX equivalent resources to delegate (in sun)
- resource — the resource type to delegate (“BANDWIDTH” or “ENERGY”)
- lock — optional boolean to lock the delegation (default: false)
- lock_period — optional lock period in seconds (if lock is true)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- visible — boolean indicating address format used
- txID — transaction ID hash
- raw_data — raw transaction data object containing delegation contract details
- raw_data_hex — hexadecimal representation of raw transaction data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/delegateresource \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "receiver_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d",
  "balance": 1000000,
  "resource": "BANDWIDTH",
  "lock": false,
  "lock_period": 0,
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

- Sharing bandwidth or energy resources with other accounts that need them.
- Implementing resource rental or delegation services in DApps.
- Allowing users to sponsor transaction costs for other accounts.
- Building resource management systems that optimize usage across multiple addresses.
