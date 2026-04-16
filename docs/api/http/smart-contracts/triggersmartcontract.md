# triggersmartcontract

TRON API method that triggers a smart contract function call. This method creates a transaction to interact with deployed smart contracts on the TRON network, allowing you to call contract functions with specified parameters.

## HTTP Request

`POST /wallet/triggersmartcontract`

## Supported Paths

- `/wallet/triggersmartcontract`

## Parameters

- contract_address — the smart contract address (hex format)
- function_selector — the function signature to call (e.g., “transfer(address,uint256)”)
- parameter — encoded parameters for the function call (hex format)
- owner_address — the caller’s TRON address (hex format)
- call_value — optional TRX amount to send with the call (in sun)
- fee_limit — maximum energy cost for the transaction (in sun)
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- result — execution result object containing:
  - result — boolean indicating call success
  - code — status code
  - message — error message if call failed
- energy_used — amount of energy consumed
- constant_result — array of return values from the contract function
- transaction — transaction object if creating a transaction
- logs — array of event logs generated during execution

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/triggersmartcontract \
  --header 'Content-Type: application/json' \
  --data '
{
  "contract_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
  "function_selector": "transfer(address,uint256)",
  "parameter": "000000000000000000000000e9d79cc47518930bc322d9bf7cddd260a0260a8d00000000000000000000000000000000000000000000000000000000000003e8",
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "call_value": 0,
  "fee_limit": 10000000,
  "visible": false
}
'
```

### Response

```json
{
  "result": {
    "result": true,
    "code": "<string>",
    "message": "<string>"
  },
  "energy_used": 123,
  "constant_result": [
    "<string>"
  ],
  "transaction": {},
  "logs": "<array>"
}
```

## Use Case

- Calling smart contract functions to read data or execute state changes.
- Interacting with DApps and DeFi protocols on the TRON network.
- Token transfers using TRC-20 contract methods.
- Querying contract state and executing complex business logic.
