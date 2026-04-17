# getcontract

TRON API method that retrieves detailed information about a smart contract deployed on the TRON network. This method provides comprehensive contract data including bytecode, ABI, deployment information, and resource configuration.

## HTTP Request

`POST /wallet/getcontract`

## Supported Paths

- `/wallet/getcontract`

## Parameters

- value — the smart contract address in hexadecimal format

## Response

- bytecode — compiled contract bytecode in hexadecimal format
- name — human-readable name of the smart contract
- origin_address — address of the account that deployed the contract
- contract_address — the contract’s address in hexadecimal format
- abi — Application Binary Interface defining contract methods and events
- origin_energy_limit — maximum energy limit set during contract deployment
- consume_user_resource_percent — percentage of caller’s resources used for contract execution (0-100)
- code_hash — unique hash identifier of the contract’s bytecode
- trx_hash — transaction hash of the original contract deployment transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getcontract \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "41a614f803b6fd780986a42c78ec9c7f77e6ded13c"
}
'
```

### Response

```json
{
  "bytecode": "<string>",
  "name": "<string>",
  "origin_address": "<string>",
  "contract_address": "<string>",
  "abi": {},
  "origin_energy_limit": 123,
  "consume_user_resource_percent": 123,
  "code_hash": "<string>",
  "trx_hash": "<string>"
}
```

## Use Case

- Retrieving comprehensive information about deployed smart contracts.
- Obtaining contract ABI for building user interfaces and interaction tools.
- Analyzing contract resource configuration and deployment details.
- Verifying contract bytecode and comparing with expected implementations.
- Building block explorers and contract verification tools.
- Understanding contract resource consumption settings for optimization.
