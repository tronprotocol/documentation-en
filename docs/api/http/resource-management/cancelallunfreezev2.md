# cancelallunfreezev2

TRON API method that cancels all unfreezing operations for an account under the Stake 2.0 mechanism. This allows users to cancel pending unfreeze requests and return resources to the frozen state.

## HTTP Request

`POST /wallet/cancelallunfreezev2`

## Supported Paths

- `/wallet/cancelallunfreezev2`

## Parameters

- owner_address — the account address that wants to cancel all unfreezing operations
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the cancel unfreeze contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/cancelallunfreezev2 \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "visible": true
}
'
```

### Response

```json
{
  "visible": true,
  "txID": "<string>",
  "raw_data": {},
  "raw_data_hex": "<string>"
}
```

## Use Case

- Canceling all pending unfreeze requests to maintain staked resources
- Responding to market conditions by keeping resources frozen
- Managing resource allocation in DeFi protocols
- Implementing dynamic staking strategies
- Preventing accidental resource unfreezing
