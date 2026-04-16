# getaccountresource

TRON API method that queries the resource information of an account, including bandwidth, energy, and TRON Power (voting power). This endpoint provides comprehensive resource metrics for managing transaction costs and network participation.

## HTTP Request

`POST /wallet/getaccountresource`

## Supported Paths

- `/wallet/getaccountresource`

## Parameters

- address — the account address in hex format (41 prefix) or base58check format
- visible — whether the address is in readable base58check format (optional, default: true)

## Response

- freeNetUsed — free bandwidth used by the account
- freeNetLimit — total free bandwidth available to the account
- NetUsed — used amount of bandwidth obtained by staking
- NetLimit — total bandwidth obtained by staking
- TotalNetLimit — total network bandwidth limit
- TotalNetWeight — total network weight for bandwidth
- EnergyUsed — energy consumed by the account
- EnergyLimit — total energy obtained by staking
- TotalEnergyLimit — total energy limit on the network
- TotalEnergyWeight — total energy weight on the network
- tronPowerLimit — TRON Power available for voting
- tronPowerUsed — TRON Power used for voting
- totalTronPowerWeight — total TRON Power weight on the network
- assetNetUsed — bandwidth used for TRC10 assets (array)
- assetNetLimit — bandwidth limit for TRC10 assets (array)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getaccountresource \
  --header 'Content-Type: application/json' \
  --data '
{
  "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

### Response

```json
{
  "freeNetUsed": 0,
  "freeNetLimit": 5000,
  "NetUsed": 0,
  "NetLimit": 0,
  "TotalNetLimit": 43200000000,
  "TotalNetWeight": 84687233463517,
  "EnergyUsed": 0,
  "EnergyLimit": 0,
  "TotalEnergyLimit": 90000000000,
  "TotalEnergyWeight": 13369831825062,
  "tronPowerLimit": 0,
  "tronPowerUsed": 0,
  "totalTronPowerWeight": 0,
  "assetNetUsed": [
    {
      "key": "<string>",
      "value": 123
    }
  ],
  "assetNetLimit": [
    {
      "key": "<string>",
      "value": 123
    }
  ]
}
```

## Use Case

- Monitoring account bandwidth and energy consumption
- Calculating transaction fees based on available resources
- Managing resource delegation and staking strategies
- Tracking voting power (TRON Power) for network governance
- Analyzing resource usage for TRC10 token transfers
- Building wallet interfaces that display resource availability
