# gettransactionfrompending

TRON API method that retrieves a specific pending transaction from the mempool by its transaction ID. This allows applications to check the status and details of an unconfirmed transaction.

## HTTP Request

`POST /wallet/gettransactionfrompending`

## Supported Paths

- `/wallet/gettransactionfrompending`

## Parameters

- value — transaction ID hash of the pending transaction to retrieve

## Response

- txID — unique transaction identifier hash
- raw_data — raw transaction data containing:
  - contract — array with transaction contract details
  - ref_block_bytes — reference block bytes for validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
  - fee_limit — maximum fee allowed for this transaction
- signature — array of transaction signatures
- ret — transaction result information (if available)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/gettransactionfrompending \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "f34f1c799700a9d83b67fdcadd7be697010a8dbbcd520de4ac46a648e3e7ae3d"
}
'
```

### Response

```json
{
  "txID": "f34f1c799700a9d83b67fdcadd7be697010a8dbbcd520de4ac46a648e3e7ae3d",
  "raw_data": {
    "contract": [
      {
        "type": "TransferContract",
        "parameter": {
          "type_url": "type.googleapis.com/protocol.TransferContract",
          "value": {}
        }
      }
    ],
    "ref_block_bytes": "6f80",
    "ref_block_hash": "1c9c4b8c43c5e0b1",
    "expiration": 1704067260000,
    "timestamp": 1704067200000,
    "fee_limit": 100000000
  },
  "signature": [
    "<string>"
  ],
  "ret": [
    {
      "contractRet": "SUCCESS"
    }
  ]
}
```

## Use Case

- Checking the status of a specific pending transaction by its ID.
- Retrieving detailed information about unconfirmed transactions for verification.
- Building transaction tracking systems that monitor pending transactions.
- Validating transaction parameters before confirmation in custom applications.
- Implementing transaction status polling for user interfaces and notifications.
