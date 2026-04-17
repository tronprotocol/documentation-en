# getcandelegatedmaxsize

TRON API method that retrieves the maximum amount that can be delegated by an account for bandwidth and energy resources.

## HTTP Request

`POST /wallet/getcandelegatedmaxsize`

## Supported Paths

- `/wallet/getcandelegatedmaxsize`
- `/walletsolidity/getcandelegatedmaxsize`

## Parameters

- owner_address — the account address to query for maximum delegation capacity
- type — resource type: 0 for bandwidth, 1 for energy
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- max_size — the maximum amount that can be delegated for the specified resource type

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getcandelegatedmaxsize \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "type": 0,
  "visible": true
}
'
```

## Use Case

- Determining delegation capacity before attempting resource delegation
- Building user interfaces with delegation limits
- Implementing resource delegation validation
- Planning resource sharing strategies
- Preventing delegation failures due to insufficient capacity
