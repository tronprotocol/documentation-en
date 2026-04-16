# undelegateresource

TRON API method that revokes delegated bandwidth or energy resources from another address. This method allows you to reclaim resources that were previously delegated to another account using delegateresource, making those resources available to your own account again.

## HTTP Request

`POST /wallet/undelegateresource`

## Supported Paths

- `/wallet/undelegateresource`

## Parameters

- owner_address — the address that originally delegated the resources (hex format)
- receiver_address — the address that was receiving the delegated resources (hex format)
- balance — the amount of TRX worth of resources to undelegate (in sun, where 1 TRX = 1,000,000 sun)
- resource — the resource type to undelegate (“BANDWIDTH” or “ENERGY”)
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
  --url https://api.shasta.trongrid.io/wallet/undelegateresource \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "receiver_address": "41e552f6487585c2b58bc2c9bb4492bc1f17132cd0",
  "balance": 1000000,
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

- Reclaiming bandwidth or energy resources that were delegated to other accounts.
- Managing resource allocation when delegation is no longer needed.
- Redistributing resources between different accounts in your control.
- Optimizing resource utilization across multiple addresses.
