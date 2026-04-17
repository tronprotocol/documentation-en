# getcontractinfo

TRON API method that retrieves detailed information about a smart contract, including its ABI, bytecode, source code, and metadata. This method is essential for understanding and interacting with deployed contracts on the TRON network.

## HTTP Request

`POST /wallet/getcontractinfo`

## Supported Paths

- `/wallet/getcontractinfo`

## Parameters

- value — contract address to retrieve information for
- visible — boolean indicating whether to use visible (Base58) address format instead of hex

## Response

- contract_address — the contract address
- bytecode — contract bytecode in hex format
- name — contract name if available
- abi — Application Binary Interface defining contract functions and events
- source_map — source code mapping for debugging purposes
- source_code — original contract source code if available
- compiler_version — Solidity compiler version used
- consume_user_resource_percent — percentage of user resources consumed
- origin_address — address that deployed the contract
- origin_energy_limit — energy limit set by contract creator
- contract_state — current state of the contract
- code_hash — hash of the contract code

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/getcontractinfo \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs",
  "visible": true
}
'
```

### Response

```json
{
  "contract_address": "<string>",
  "bytecode": "<string>",
  "name": "<string>",
  "abi": {},
  "source_map": "<string>",
  "source_code": "<string>",
  "compiler_version": "<string>",
  "consume_user_resource_percent": 123,
  "origin_address": "<string>",
  "origin_energy_limit": 123,
  "contract_state": "<string>",
  "code_hash": "<string>"
}
```

## Use Case

- Retrieving contract ABI for building function calls and parsing events.
- Verifying contract source code and understanding contract functionality.
- Building contract explorers and analysis tools for developers.
- Debugging contract deployments and understanding energy consumption settings.
- Implementing contract interaction interfaces in wallets and dApps.
- Auditing smart contracts and understanding their implementation details.
