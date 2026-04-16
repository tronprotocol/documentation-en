# estimateenergy

TRON API method that estimates the energy consumption for executing a smart contract function call. This method helps predict the energy costs before actually executing a transaction, enabling better cost planning and user experience optimization.

## HTTP Request

`POST /wallet/estimateenergy`

## Supported Paths

- `/wallet/estimateenergy`
- `/walletsolidity/estimateenergy`

## Parameters

- owner_address — address of the account that would execute the contract call
- contract_address — address of the smart contract to estimate energy for
- function_selector — function signature of the contract method to call (e.g., “balanceOf(address)”)
- parameter — hex-encoded parameters to pass to the function
- visible — boolean indicating whether to use visible (Base58) address format instead of hex

## Response

- result — estimation result object containing:
  - result — boolean indicating if estimation was successful
  - energy_required — estimated energy consumption for the function call
- energy_used — total energy that would be consumed
- constant_result — array of return values if the function is a view/pure function
- transaction — transaction object with estimated costs if applicable

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/estimateenergy \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "function_selector": "balanceOf(address)",
  "parameter": "000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c",
  "visible": true
}
'
```

### Response

```json
{
  "result": {
    "result": true,
    "energy_required": 123
  },
  "energy_used": 123,
  "constant_result": "<array>",
  "transaction": {}
}
```

## Use Case

- Predicting transaction costs before executing smart contract calls.
- Building user interfaces that show estimated fees upfront.
- Optimizing contract interactions by choosing energy-efficient functions.
- Implementing cost-aware transaction batching and prioritization.
- Creating accurate fee estimation tools for wallets and dApps.
- Analyzing contract performance and identifying gas-intensive operations.

## Curl Example

Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/estimateenergy' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
 "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
 "function_selector": "balanceOf(address)",
 "parameter": "000000000000000000000000a614f803b6fd780986a42c78ec9c7f77e6ded13c",
 "visible": true
}'
Bodyapplication/jsonowner_addressstringrequiredAddress executing the contract callcontract_addressstringrequiredAddress of the smart contractfunction_selectorstringrequiredFunction signature to callparameterstringrequiredHex-encoded parameters for the functionvisiblebooleanWhether to use visible (Base58) address formatResponse200 - application/jsonEnergy consumption estimationresultobjectShow child attributesenergy_usednumberTotal energy that would be consumedconstant_resultarrayReturn values for view/pure functionstransactionobjectTransaction object with estimated costsLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/clearabi | TRONwallet/listwitnesses | TRON
