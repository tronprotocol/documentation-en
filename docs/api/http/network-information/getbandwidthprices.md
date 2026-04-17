# getbandwidthprices

TRON API method that retrieves the current bandwidth prices on the TRON network, showing the cost of bandwidth for transaction processing.

## HTTP Request

`POST /wallet/getbandwidthprices`

## Supported Paths

- `/wallet/getbandwidthprices`
- `/walletsolidity/getbandwidthprices`

## Parameters

This method does not require any parameters.

## Response

- prices — bandwidth pricing information including current rates and historical data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getbandwidthprices \
  --header 'Content-Type: application/json' \
  --data '{}'
```

## Use Case

- Monitoring current bandwidth costs for transaction processing
- Building transaction fee estimation tools
- Analyzing network congestion through bandwidth pricing
- Optimizing transaction timing based on cost
- Creating cost-aware transaction batching systems
