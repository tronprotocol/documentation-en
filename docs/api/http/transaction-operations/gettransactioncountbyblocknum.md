# gettransactioncountbyblocknum

TRON API method that retrieves the count of transactions in a specific block by block number.

## HTTP Request

`POST /wallet/gettransactioncountbyblocknum`

## Supported Paths

- `/wallet/gettransactioncountbyblocknum`
- `/walletsolidity/gettransactioncountbyblocknum`

## Parameters

- num — the block number to query for transaction count

## Response

- count — the number of transactions in the specified block

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/gettransactioncountbyblocknum \
  --header 'Content-Type: application/json' \
  --data '
{
  "num": 1000000
}
'
```

### Response

```json
{
  "count": 123
}
```

## Use Case

- Quickly checking how many transactions are included in a given block without fetching full transaction data.
- Building block explorers that display transaction counts per block.
- Analyzing network activity and transaction throughput by block.
- Monitoring block utilization over time for capacity planning.
