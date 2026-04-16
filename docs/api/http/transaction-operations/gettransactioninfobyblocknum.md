# gettransactioninfobyblocknum

TRON API method that retrieves detailed transaction information for all transactions within a specific block number.

## HTTP Request

`POST /wallet/gettransactioninfobyblocknum`

## Supported Paths

- `/wallet/gettransactioninfobyblocknum`
- `/walletsolidity/gettransactioninfobyblocknum`

## Parameters

- num — the block number to retrieve transaction information from
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- Array of transaction info objects, each containing:
  - id — transaction hash
  - fee — transaction fee in sun
  - blockNumber — block number containing the transaction
  - blockTimeStamp — block timestamp
  - contractResult — contract execution result
  - receipt — transaction receipt with energy usage and result
  - log — event logs from smart contract execution

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/gettransactioninfobyblocknum \
  --header 'Content-Type: application/json' \
  --data '
{
  "num": 66677878,
  "visible": true
}
'
```

### Response

```json
[
  {
    "id": "<string>",
    "fee": 123,
    "blockNumber": 123,
    "blockTimeStamp": 123,
    "contractResult": [
      "<string>"
    ],
    "receipt": {},
    "log": [
      {}
    ]
  }
]
```

## Use Case

- Analyzing all transaction details within a specific block
- Building block explorers with detailed transaction information
- Monitoring transaction fees and energy consumption patterns
- Auditing smart contract execution results in a block
- Creating comprehensive transaction analysis tools
