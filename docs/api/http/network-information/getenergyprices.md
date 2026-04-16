# getenergyprices

TRON API method that retrieves the current energy prices on the TRON network, showing the cost of energy for smart contract execution.

## HTTP Request

`POST /wallet/getenergyprices`

## Supported Paths

- `/wallet/getenergyprices`
- `/walletsolidity/getenergyprices`

## Parameters

This method does not require any parameters.

## Response

- prices — energy pricing information including current rates and historical data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getenergyprices \
  --header 'Content-Type: application/json' \
  --data '{}'
```

## Use Case

- Monitoring current energy costs for smart contract operations
- Building fee estimation tools for DApp users
- Analyzing network congestion through energy pricing
- Optimizing smart contract execution timing
- Creating cost-aware transaction scheduling systems
