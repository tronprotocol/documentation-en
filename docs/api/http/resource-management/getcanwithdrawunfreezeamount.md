# getcanwithdrawunfreezeamount

TRON API method that retrieves the amount that can be withdrawn after unfreezing resources under the Stake 2.0 mechanism.

## HTTP Request

`POST /wallet/getcanwithdrawunfreezeamount`

## Supported Paths

- `/wallet/getcanwithdrawunfreezeamount`
- `/walletsolidity/getcanwithdrawunfreezeamount`

## Parameters

- owner_address — the account address to query for withdrawable unfreeze amount
- timestamp — optional timestamp to check withdrawable amount at a specific time
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- amount — the total amount of TRX that can be withdrawn from completed unfreeze operations

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getcanwithdrawunfreezeamount \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "timestamp": 123,
  "visible": true
}
'
```

## Use Case

- Checking how much TRX is available for withdrawal after unfreezing
- Planning liquidity management for accounts
- Building user interfaces showing withdrawable balances
- Implementing automatic withdrawal triggers
- Monitoring completed unfreeze operations
