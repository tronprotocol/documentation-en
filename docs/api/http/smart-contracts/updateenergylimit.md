# updateenergylimit

TRON API method that updates the origin energy limit for a smart contract. This setting determines the maximum amount of energy the contract creator provides for contract execution, affecting how much energy users need to provide when calling the contract.

## HTTP Request

`POST /wallet/updateenergylimit`

## Supported Paths

- `/wallet/updateenergylimit`

## Parameters

- owner_address — address of the contract owner who can update the energy limit
- contract_address — address of the smart contract to update energy limit for
- origin_energy_limit — maximum energy amount the contract creator provides (in energy units, not TRX/sun)
- visible — boolean indicating whether to use visible (Base58) address format instead of hex

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the energy limit update transaction
- raw_data — raw transaction data containing:
  - contract — array with contract update details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/updateenergylimit \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "origin_energy_limit": 100000000,
  "visible": true
}
'
```

### Response

```json
{
  "visible": true,
  "txID": "<string>",
  "raw_data": {
    "contract": "<array>",
    "ref_block_bytes": "<string>",
    "ref_block_hash": "<string>",
    "expiration": 123,
    "timestamp": 123
  },
  "raw_data_hex": "<string>"
}
```

## Use Case

- Setting energy subsidies for contract users to improve user experience.
- Managing contract execution costs by controlling energy allocation.
- Optimizing contract economics by adjusting energy provision strategies.
- Implementing freemium models where basic operations are subsidized.
- Balancing between contract owner costs and user accessibility.
- Adjusting energy limits based on contract usage patterns and feedback.

## Curl Example

- Account [41…] does not exist — the payer address does not exist on-chain or the format does not match visible. Query it with wallet/getaccount and fund/activate it first.
- No permission or similar — the owner_address is not the contract owner; only the origin_address can update settings.
- Contract not found — check the contract address and use hex for wallet/getcontract.
