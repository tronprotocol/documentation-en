# getblock

TRON API method that retrieves detailed block information from the TRON blockchain by block number or block hash.

## HTTP Request

`POST /wallet/getblock`

## Supported Paths

- `/wallet/getblock`
- `/walletsolidity/getblock`

## Parameters

- id_or_num — block hash (as hex string) or block number to retrieve
- detail — optional boolean. When true, returns detailed transaction information. Default is false.
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- blockID — the block hash
- block_header — block header information including:
  - raw_data — raw header data with timestamp, number, parent hash, etc.
  - witness_signature — block producer signature
- transactions — array of transactions in the block (detailed if detail=true)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getblock \
  --header 'Content-Type: application/json' \
  --data '
{
  "id_or_num": "66677878",
  "detail": true,
  "visible": true
}
'
```

### Response

```json
{
  "blockID": "<string>",
  "block_header": {
    "raw_data": {},
    "witness_signature": "<string>"
  },
  "transactions": [
    {}
  ]
}
```

## Use Case

- Retrieving specific block information for analysis
- Building block explorers and blockchain visualization tools
- Verifying block contents and transaction inclusion
- Monitoring blockchain state at specific block heights
- Analyzing block production patterns and timing
