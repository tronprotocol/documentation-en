# updatewitness

TRON API method that creates a transaction to update a witness account’s URL. This allows witnesses to update their public information and promotional content displayed to voters in the TRON network governance system.

## HTTP Request

`POST /wallet/updatewitness`

## Supported Paths

- `/wallet/updatewitness`

## Parameters

- owner_address — hexadecimal address of the witness account to update
- update_url — new URL string for the witness (maximum 256 bytes)
- visible — boolean indicating whether addresses should be in visible format (Base58Check)

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the witness update transaction
- raw_data — raw transaction data containing:
  - contract — array with witness update contract details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/updatewitness \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TPswDDCAWhJAZGdHPidFg5nEf8TkNToDX1",
  "update_url": "https://example.com/witness",
  "visible": true
}
'
```

### Response

```json
{
  "visible": true,
  "txID": "<string>",
  "raw_data": {
    "contract": [
      {
        "type": "UpdateWitnessContract",
        "parameter": {
          "type_url": "type.googleapis.com/protocol.UpdateWitnessContract",
          "value": {
            "owner_address": "<string>",
            "update_url": "<string>"
          }
        }
      }
    ],
    "ref_block_bytes": "<string>",
    "ref_block_hash": "<string>",
    "expiration": 123,
    "timestamp": 123
  },
  "raw_data_hex": "<string>"
}
```

## Use Case

- Updating witness promotional URLs and information for voters.
- Maintaining current witness contact information and websites.
- Building witness management dashboards and governance tools.
- Implementing automated witness information updates in applications.
- Creating witness profile management systems for TRON governance participants.
