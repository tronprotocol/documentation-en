# getblockbalance

TRON API method that returns the balance deltas within a specific block. It shows, per transaction, how account balances changed in that block.

## HTTP Request

`POST /wallet/getblockbalance`

## Supported Paths

- `/wallet/getblockbalance`

## Parameters

- hash — block hash as a 64‑character hex string.
- number — block number. Must match the provided hash.
- visible — optional boolean. When true, addresses are base58; when false, hex. Default is true.

## Response

- timestamp — block timestamp in milliseconds.
- block_identifier — object with hash and number.
- transaction_balance_trace — array per transaction with:
  - transaction_identifier — transaction hash.
  - operation — list with operation_identifier, address, and amount (sun; negative for debits, positive for credits).
  - type — contract type (for example, TransferContract).
  - status — execution status.

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getblockbalance \
  --header 'Content-Type: application/json' \
  --data '
{
  "hash": "0000000004986736812cbf15ffbcdd229bd3d76a595db895719867cc2da3a5bd",
  "number": 77096758,
  "visible": true
}
'
```

### Response

```json
{
  "timestamp": 123,
  "block_identifier": {
    "hash": "<string>",
    "number": 123
  },
  "transaction_balance_trace": [
    {
      "transaction_identifier": "<string>",
      "operation": [
        {
          "operation_identifier": 123,
          "address": "<string>",
          "amount": 123
        }
      ],
      "type": "<string>",
      "status": "<string>"
    }
  ]
}
```

## Use Case

- Auditing balance changes for a given block.
- Building explorers or analytics that summarize per‑address deltas.
- Reconciling application balances against chain state.

## Curl Example

Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/getblockbalance' \
 --header 'Content-Type: application/json' \
 --data '{
 "hash": "0000000004986736812cbf15ffbcdd229bd3d76a595db895719867cc2da3a5bd",
 "number": 77096758,
 "visible": true
 }'

## Get A Valid Block Pair Automatically

- provide both hash (64 hex chars) and number that match the same block to avoid errors like INVALID hex String, hash length not equals 32, or number and hash do not match.
- amounts are in sun (1 TRX = 1,000,000 sun).
