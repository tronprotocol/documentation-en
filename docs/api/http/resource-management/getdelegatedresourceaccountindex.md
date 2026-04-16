# getdelegatedresourceaccountindex

TRON API method that retrieves the delegation index of an account, showing all accounts that have delegated resources to or received resources from the specified account.

## HTTP Request

`POST /wallet/getdelegatedresourceaccountindex`

## Supported Paths

- `/wallet/getdelegatedresourceaccountindex`
- `/walletsolidity/getdelegatedresourceaccountindex`

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
  --url https://api.shasta.trongrid.io/wallet/getdelegatedresourceaccountindex \
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

- Discovering all delegation relationships for a specific account
- Building resource delegation network graphs
- Analyzing delegation patterns and resource flow
- Monitoring accounts involved in resource sharing
- Creating comprehensive resource management interfaces
