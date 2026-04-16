# getsignweight

TRON API method that checks the multi-signature status of a transaction. It returns the total weight of signatures provided, the threshold required, and a list of authorized addresses, helping verify if a transaction has enough approvals to be broadcast.

## HTTP Request

`POST /wallet/getsignweight`

## Supported Paths

- `/wallet/getsignweight`

## Parameters

- txID — the transaction ID (hash).
- raw_data — the raw transaction object.
- raw_data_hex — the raw transaction in hexadecimal.
- signature — array of 65-byte hex signatures.
- visible — optional boolean. When true, addresses in raw_data use base58; when false, hex. Defaults to false.

## Response

- result — result object, empty `{}` on success; contains error code and message on failure
- approved_list — array of signer addresses recovered from the signatures
- permission — the permission object used for this transaction's verification
- current_weight — total weight of the provided signatures
- transaction — the echoed transaction with validation result

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getsignweight \
  --header 'Content-Type: application/json' \
  --data '
{
  "txID": "4ad97d49409cfff338d2f9e71d4019c70e82030b52e15e208b1808f2f3ea782e",
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "data": "a9059cbb0000000000000000000000415d4a41a3b0cdda5c03df72b38a20aa1b88777c7500000000000000000000000000000000000000000000000000000000f9cd95c0",
            "owner_address": "41cf2e99409d2a9a9190197ab0bff35ca87818c41e",
            "contract_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c"
          },
          "type_url": "type.googleapis.com/protocol.TriggerSmartContract"
        },
        "type": "TriggerSmartContract"
      }
    ],
    "ref_block_bytes": "68bd",
    "ref_block_hash": "bc830d2c09fa23d1",
    "expiration": 1761952567698,
    "fee_limit": 225000000,
    "timestamp": 1761952507695
  },
  "raw_data_hex": "0a0268bd2208bc830d2c09fa23d14092a3bae4a3335aae01081f12a9010a31747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e54726967676572536d617274436f6e747261637412740a1541cf2e99409d2a9a9190197ab0bff35ca87818c41e121541a614f803b6fd780986a42c78ec9c7f77e6ded13c2244a9059cbb0000000000000000000000415d4a41a3b0cdda5c03df72b38a20aa1b88777c7500000000000000000000000000000000000000000000000000000000f9cd95c070afceb6e4a3339001c0f4a46b",
  "signature": [
    "c99cdc8af6f47dc65a75aa0c6da1c5be8510736e581043162c3e8525c6e0ed8f592adaa74ba250136ea6e1fb125b3d3d024ac6abd3e24c28097d66a8e2a0c0aa01"
  ],
  "visible": false
}
'
```

### Response

```json
{
  "result": {},
  "approved_list": [
    "<string>"
  ],
  "permission": {
    "keys": [
      {
        "address": "<string>",
        "weight": 1
      }
    ],
    "threshold": 1,
    "permission_name": "owner"
  },
  "current_weight": 1,
  "transaction": {}
}
```

## Use Case

- Checking whether a multi-signature transaction has gathered enough signature weight to meet the threshold.
- Verifying the approval progress after calling multiSign in multi-key account workflows.
- Building wallet UIs that display current signature weight vs. required threshold.
- Auditing which addresses have signed a transaction before broadcasting.
- Implementing multi-signature governance workflows that require multiple key approvals.
