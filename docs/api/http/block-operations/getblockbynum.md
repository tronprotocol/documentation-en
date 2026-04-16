# getblockbynum

TRON API method that retrieves a block by its number. This method returns detailed information about a specific block in the TRON blockchain, including all transactions contained within that block.

## HTTP Request

`POST /wallet/getblockbynum`

## Supported Paths

- `/wallet/getblockbynum`
- `/walletsolidity/getblockbynum`

## Parameters

- num — the block number to retrieve (integer)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- blockID — unique block identifier hash
- block_header — block header information containing:
  - raw_data — raw header data with timestamp, number, and parent hash
  - witness_signature — block producer’s signature
- transactions — array of transaction objects in the block
- visible — boolean indicating address format used

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getblockbynum \
  --header 'Content-Type: application/json' \
  --data '
{
  "num": 1000,
  "visible": false
}
'
```

### Response

```json
{
  "blockID": "<string>",
  "block_header": {
    "raw_data": {
      "number": 123,
      "timestamp": 123,
      "parentHash": "<string>"
    },
    "witness_signature": "<string>"
  },
  "transactions": [
    {}
  ],
  "visible": true
}
```

## Use Case

- Retrieving specific blocks for blockchain analysis and monitoring.
- Accessing transaction history within particular blocks.
- Building block explorers and analytics tools.
- Verifying block data and transaction inclusion for auditing purposes.
