# getdelegatedresourcev2

TRON API method that retrieves delegated resource information using the Stake 2.0 mechanism between accounts on the TRON blockchain.

## HTTP Request

`POST /wallet/getdelegatedresourcev2`

## Supported Paths

- `/wallet/getdelegatedresourcev2`
- `/walletsolidity/getdelegatedresourcev2`

## Parameters

- fromAddress — the address that delegated resources to another account
- toAddress — the address that received the delegated resources
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- delegatedResource — array of delegated resource information containing:
  - from — the delegator address
  - to — the recipient address
  - frozen_balance_for_bandwidth — amount of TRX frozen for bandwidth delegation
  - frozen_balance_for_energy — amount of TRX frozen for energy delegation
  - expire_time_for_bandwidth — expiration timestamp for bandwidth delegation
  - expire_time_for_energy — expiration timestamp for energy delegation

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getdelegatedresourcev2 \
  --header 'Content-Type: application/json' \
  --data '
{
  "fromAddress": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "toAddress": "TFgY1uN8buRxAtV2r6Zy5sG3ACko6pJT1y",
  "visible": true
}
'
```

### Response

```json
{
  "delegatedResource": [
    {
      "from": "<string>",
      "to": "<string>",
      "frozen_balance_for_bandwidth": 123,
      "frozen_balance_for_energy": 123,
      "expire_time_for_bandwidth": 123,
      "expire_time_for_energy": 123
    }
  ]
}
```

## Use Case

- Checking Stake 2.0 delegated resources between specific accounts
- Monitoring resource delegation relationships under the new staking mechanism
- Verifying delegation amounts and expiration times
- Building modern resource management dashboards
- Analyzing updated resource sharing patterns
