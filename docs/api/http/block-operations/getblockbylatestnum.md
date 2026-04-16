# getblockbylatestnum

TRON API method that retrieves the latest blocks from the TRON blockchain up to a specified number of blocks.

## HTTP Request

`POST /wallet/getblockbylatestnum`

## Supported Paths

- `/wallet/getblockbylatestnum`
- `/walletsolidity/getblockbylatestnum`

## Parameters

- num — number of latest blocks to retrieve (maximum 100)
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- block — array of block objects, each containing:
  - blockID — the block hash
  - block_header — block header with raw data and witness signature
  - transactions — array of transactions in each block

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getblockbylatestnum \
  --header 'Content-Type: application/json' \
  --data '
{
  "num": 5,
  "visible": true
}
'
```

### Response

```json
{
  "block": [
    {
      "blockID": "<string>",
      "block_header": {},
      "transactions": [
        {}
      ]
    }
  ]
}
```

## Use Case

- Retrieving recent blockchain activity and transactions
- Building real-time blockchain monitoring dashboards
- Analyzing recent network activity patterns
- Creating live feeds of blockchain events
- Monitoring latest block production and validation
