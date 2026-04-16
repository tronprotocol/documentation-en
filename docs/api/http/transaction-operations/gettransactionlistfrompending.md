# gettransactionlistfrompending

TRON API method that retrieves a list of all pending transactions currently in the mempool. This allows applications to monitor unconfirmed transactions awaiting inclusion in a block.

## HTTP Request

`GET /wallet/gettransactionlistfrompending`

## Supported Paths

- `/wallet/gettransactionlistfrompending`

## Parameters

This method requires no parameters. It returns all pending transactions in the current mempool.

## Response

- transactions — array of pending transaction objects, each containing:
  - txID — unique transaction identifier hash
  - raw_data — raw transaction data including:
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
curl --request GET \
  --url https://api.shasta.trongrid.io/wallet/gettransactionlistfrompending
```

### Response

```json
{
  "transactions": [
    {
      "txID": "f34f1c799700a9d83b67fdcadd7be697010a8dbbcd520de4ac46a648e3e7ae3d",
      "raw_data": {
        "contract": [
          {
            "type": "TransferContract",
            "parameter": {}
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
  ]
}
```

## Use Case

- Monitoring pending transactions in real-time for transaction status tracking.
- Building transaction pool analytics and network congestion monitoring tools.
- Implementing custom mempool explorers and pending transaction dashboards.
- Analyzing transaction patterns and fee structures before confirmation.
- Creating alerts for specific pending transactions or transaction types.
