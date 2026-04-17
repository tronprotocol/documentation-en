# accountpermissionupdate

TRON API method that updates the permissions of an account on the TRON blockchain. This method allows modification of owner, witness, and active permissions for multi-signature account management.

## HTTP Request

`POST /wallet/accountpermissionupdate`

## Supported Paths

- `/wallet/accountpermissionupdate`

## Parameters

- owner_address — the account address whose permissions are being updated
- owner — optional object containing owner permission settings with threshold and keys
- witness — optional object containing witness permission settings with threshold and keys
- actives — optional array of active permission objects with threshold, operations, and keys
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the permission update contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/accountpermissionupdate \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "owner": {
    "type": 0,
    "permission_name": "owner",
    "threshold": 1,
    "keys": [
      {
        "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
        "weight": 1
      }
    ]
  },
  "witness": {
    "type": 1,
    "permission_name": "witness",
    "threshold": 1,
    "keys": [
      {
        "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
        "weight": 1
      }
    ]
  },
  "actives": [
    {
      "type": 2,
      "permission_name": "active",
      "threshold": 1,
      "operations": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",
      "keys": [
        {
          "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
          "weight": 1
        }
      ]
    }
  ],
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

- Setting up multi-signature accounts with custom permission structures
- Modifying existing account permissions and thresholds
- Managing witness permissions for Super Representative accounts
- Implementing advanced security models for institutional accounts

## Curl Example

- operations must be a 32‑byte hex string (64 hex chars) representing the allowed operations bitmask.
- Each keys entry requires an address and weight. The sum of weights for a permission must be greater than or equal to its threshold.
- Use base58 addresses with visible: true, or hex addresses with visible: false.
