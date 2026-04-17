# getaccount

TRON API method that retrieves detailed account information for a given address. This method returns comprehensive data about an account including balances, resources, and account metadata.

## HTTP Request

`POST /wallet/getaccount`

## Supported Paths

- `/wallet/getaccount`
- `/walletsolidity/getaccount`

## Parameters

- address — the TRON account address to query. Can be in base58 or hex format.
- visible — optional boolean parameter. When set to true, the address should be in base58 format. Default is false.

## Response

- address — the account address in hex format
- balance — the TRX balance in sun (1 TRX = 1,000,000 sun)
- create_time — account creation timestamp
- latest_operation_time — timestamp of the last operation
- free_net_usage — free bandwidth used
- latest_consume_free_time — last free bandwidth consumption time
- account_resource — resource information including energy and bandwidth
- owner_permission — owner permission settings
- active_permission — active permission settings
- frozenV2 — frozen balance details for resource delegation
- asset — TRC10 token balances
- assetV2 — detailed TRC10 token information

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getaccount \
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
  "address": "<string>",
  "balance": 123,
  "create_time": 123,
  "latest_operation_time": 123,
  "free_net_usage": 123,
  "account_resource": {},
  "owner_permission": {},
  "active_permission": "<array>"
}
```

## Use Case

- Retrieving account balances and resource information.
- Checking account permissions and multi-signature settings.
- Monitoring frozen balances and resource delegations.
- Displaying account information in wallets and explorers.
- Verifying account existence before sending transactions.
