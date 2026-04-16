# getblockbylimitnext

TRON API method that retrieves a range of blocks from the TRON blockchain starting from a specific block number with a specified limit.

## HTTP Request

`POST /wallet/getblockbylimitnext`

## Supported Paths

- `/wallet/getblockbylimitnext`
- `/walletsolidity/getblockbylimitnext`

## Parameters

- startNum — the starting block number to retrieve from
- endNum — the ending block number (range limit)
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- block — array of block objects within the specified range, each containing:
  - blockID — the block hash
  - block_header — block header with raw data and witness signature
  - transactions — array of transactions in each block

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getblockbylimitnext \
  --header 'Content-Type: application/json' \
  --data '
{
  "startNum": 66677870,
  "endNum": 66677880,
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

- Retrieving specific ranges of blocks for analysis
- Building paginated block explorers
- Analyzing blockchain activity within specific time periods
- Creating historical data analysis tools
- Implementing efficient block synchronization mechanisms
