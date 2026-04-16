# getavailableunfreezecount

TRON API method that retrieves the available unfreeze count for an account under the Stake 2.0 mechanism. This shows how many unfreeze operations can still be performed.

## HTTP Request

`POST /wallet/getavailableunfreezecount`

## Supported Paths

- `/wallet/getavailableunfreezecount`
- `/walletsolidity/getavailableunfreezecount`

## Parameters

- owner_address — the account address to query for available unfreeze count
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- count — the number of available unfreeze operations remaining for this account

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getavailableunfreezecount \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

## Use Case

- Checking how many more unfreeze operations an account can perform
- Planning resource management strategies
- Building user interfaces that show unfreeze limitations
- Implementing safeguards against exceeding unfreeze limits
- Monitoring account resource flexibility
