# triggerconstantcontract

TRON API method that calls a constant (read-only) smart contract method without consuming energy or bandwidth. This method allows you to query contract state and call view functions without broadcasting a transaction to the blockchain.

## HTTP Request

`POST /wallet/triggerconstantcontract`

## Supported Paths

- `/wallet/triggerconstantcontract`
- `/walletsolidity/triggerconstantcontract`

## Parameters

- owner_address — (optional) address calling the contract method in hexadecimal format
- contract_address — smart contract address to call in hexadecimal format
- function_selector — function signature or selector (e.g., “balanceOf(address)”)
- parameter — (optional) encoded parameters for the function call in hexadecimal format

## Response

- result — execution result object containing:
  - result — boolean indicating if the call was successful
- energy_used — estimated energy consumption if this were a real transaction
- constant_result — array of return values from the contract method in hexadecimal format
- transaction — transaction object that would be created (for reference, not executed)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/triggerconstantcontract \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41b487cdb2d8dc7b2a8e5e7e7b4e3e8b8b8b8b8b",
  "contract_address": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c",
  "function_selector": "balanceOf(address)",
  "parameter": "000000000000000000000000b487cdb2d8dc7b2a8e5e7e7b4e3e8b8b8b8b8b"
}
'
```

### Response

```json
{
  "result": {
    "result": true
  },
  "energy_used": 123,
  "constant_result": [
    "<string>"
  ],
  "transaction": {}
}
```

## Use Case

- Calling read-only smart contract methods to query blockchain state.
- Reading token balances, contract variables, and other view data without costs.
- Testing contract method calls before executing actual transactions.
- Building user interfaces that need to display current contract state.
- Implementing contract interaction tools that require state queries.
- Estimating energy costs for contract method calls before execution.
