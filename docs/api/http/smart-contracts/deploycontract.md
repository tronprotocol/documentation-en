# deploycontract

TRON API method that creates a transaction to deploy a new smart contract to the TRON network. This method prepares the deployment transaction with all necessary parameters, which must then be signed and broadcast to complete the contract deployment.

## HTTP Request

`POST /wallet/deploycontract`

## Supported Paths

- `/wallet/deploycontract`

## Parameters

- owner_address — address of the account deploying the contract in hexadecimal format
- abi — contract ABI (Application Binary Interface) as a JSON string defining contract methods and events
- bytecode — compiled contract bytecode in hexadecimal format
- parameter — (optional) constructor parameters encoded in hexadecimal format
- call_value — (optional) amount of TRX to transfer to the contract during deployment (in SUN, 1 TRX = 1,000,000 SUN)
- consume_user_resource_percent — (optional) percentage of caller’s resources used for contract calls (0-100, default 100)
- fee_limit — (optional) maximum energy fee willing to pay for deployment (in SUN)
- origin_energy_limit — (optional) energy limit provided by the contract creator for future calls
- name — (optional) human-readable name for the contract

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the deployment transaction
- raw_data — raw transaction data containing all deployment parameters
- raw_data_hex — raw transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/deploycontract \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41b487cdb2d8dc7b2a8e5e7e7b4e3e8b8b8b8b8b",
  "abi": "[{\"inputs\":[],\"name\":\"name\",\"outputs\":[{\"name\":\"\",\"type\":\"string\"}],\"type\":\"function\"}]",
  "bytecode": "608060405234801561001057600080fd5b5061012a806100206000396000f3fe6080604052",
  "parameter": "",
  "call_value": 0,
  "consume_user_resource_percent": 100,
  "fee_limit": 1000000000,
  "origin_energy_limit": 10000000,
  "name": "MyContract"
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

- Deploying new smart contracts to the TRON blockchain.
- Creating TRC20 tokens, NFT contracts, and other decentralized applications.
- Setting up contract resource limits and fee structures during deployment.
- Preparing deployment transactions that can be signed offline for security.
- Building deployment tools and contract management platforms.
- Establishing smart contract infrastructure for DApps and services.
