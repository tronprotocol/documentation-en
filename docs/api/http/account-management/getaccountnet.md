# getaccountnet

TRON API method that retrieves network resource information for a specific account. This method provides detailed information about an account’s bandwidth usage, including free bandwidth, frozen bandwidth, and network resource consumption statistics.

## HTTP Request

`POST /wallet/getaccountnet`

## Supported Paths

- `/wallet/getaccountnet`

## Parameters

- address — the account address to query network resources for (hex format)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- freeNetUsed — amount of free bandwidth used
- freeNetLimit — total free bandwidth limit available
- NetUsed — amount of staked bandwidth used
- NetLimit — total staked bandwidth limit available
- TotalNetLimit — total network bandwidth limit
- TotalNetWeight — total network weight for bandwidth calculation
- netUsed — current bandwidth usage
- netLimit — current bandwidth limit
- TotalEnergyLimit — total energy limit (if applicable)
- TotalEnergyWeight — total energy weight (if applicable)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getaccountnet \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "visible": false
}
'
```

### Response

```json
{
  "freeNetUsed": 123,
  "freeNetLimit": 123,
  "NetUsed": 123,
  "NetLimit": 123,
  "TotalNetLimit": 123,
  "TotalNetWeight": 123,
  "netUsed": 123,
  "netLimit": 123,
  "TotalEnergyLimit": 123,
  "TotalEnergyWeight": 123
}
```

## Use Case

- Monitoring bandwidth usage and limits for transaction planning.
- Checking free bandwidth allocation and consumption.
- Analyzing network resource utilization for cost optimization.
- Determining if additional bandwidth staking is needed for smooth operations.
