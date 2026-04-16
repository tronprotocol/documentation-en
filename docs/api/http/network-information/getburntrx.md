# getburntrx

TRON API method that retrieves information about burned TRX tokens, showing the total amount of TRX permanently removed from circulation.

## HTTP Request

`POST /wallet/getburntrx`

## Supported Paths

- `/wallet/getburntrx`
- `/walletsolidity/getburntrx`

## Parameters

This method does not require any parameters.

## Response

- burnTrxAmount — the total amount of TRX that has been burned (in sun units)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getburntrx \
  --header 'Content-Type: application/json' \
  --data '{}'
```

## Use Case

- Monitoring the deflationary mechanism of the TRON network
- Analyzing the total supply reduction over time
- Building economic analysis tools for TRON tokenomics
- Creating dashboards showing network burn statistics
- Tracking the impact of transaction fees on TRX supply
