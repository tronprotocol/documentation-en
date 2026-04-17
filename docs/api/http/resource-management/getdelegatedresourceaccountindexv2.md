# getdelegatedresourceaccountindexv2

TRON API method that retrieves the delegation index of an account using the Stake 2.0 mechanism, showing all accounts involved in resource delegation relationships.

## HTTP Request

`POST /wallet/getdelegatedresourceaccountindexv2`

## Supported Paths

- `/wallet/getdelegatedresourceaccountindexv2`
- `/walletsolidity/getdelegatedresourceaccountindexv2`

## Parameters

- value — the account address to query for delegation relationships
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- account — the queried account address
- fromAccounts — array of accounts that have delegated resources to this account
- toAccounts — array of accounts that have received delegated resources from this account

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getdelegatedresourceaccountindexv2 \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

### Response

```json
{
  "account": "<string>",
  "fromAccounts": [
    "<string>"
  ],
  "toAccounts": [
    "<string>"
  ]
}
```

## Use Case

- Discovering all Stake 2.0 delegation relationships for a specific account
- Building updated resource delegation network graphs
- Analyzing modern delegation patterns and resource flow
- Monitoring accounts involved in Stake 2.0 resource sharing
- Creating comprehensive resource management interfaces for the new staking system
