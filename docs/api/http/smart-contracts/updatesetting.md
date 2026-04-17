# updatesetting

TRON API method that updates the consume user resource percentage setting for a smart contract. This setting determines what percentage of the contract caller’s resources (bandwidth and energy) should be consumed when executing the contract.

## HTTP Request

`POST /wallet/updatesetting`

## Supported Paths

- `/wallet/updatesetting`

## Parameters

- owner_address — address of the contract owner who can update settings
- contract_address — address of the smart contract to update settings for
- consume_user_resource_percent — percentage (0–100) of caller’s resources to consume
- visible — boolean indicating whether to use visible (Base58) address format instead of hex

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the setting update transaction
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
  --url https://api.shasta.trongrid.io/wallet/updatesetting \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
  "consume_user_resource_percent": 10,
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

- Adjusting resource consumption patterns for smart contract execution.
- Optimizing contract costs by controlling user vs contract owner resource usage.
- Managing energy and bandwidth allocation between contract and users.
- Implementing different pricing models for contract interactions.
- Fine-tuning contract economics and user experience trade-offs.
- Setting up contracts to be more or less resource-friendly to callers.

## Curl Example

- Account [41…] does not exist — the payer address is not activated or visible does not match the provided address format.
- No permission — the owner_address is not the contract owner (origin_address).
- Contract not found — verify the contract address and format.
