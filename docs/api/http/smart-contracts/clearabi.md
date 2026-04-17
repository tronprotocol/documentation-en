# clearabi

TRON API method that clears (removes) the ABI (Application Binary Interface) information from a smart contract. This operation removes the contract’s ABI data from the blockchain, making the contract functions less discoverable but still executable if the function signatures are known.

## HTTP Request

`POST /wallet/clearabi`

## Supported Paths

- `/wallet/clearabi`

## Parameters

- owner_address — address of the contract owner who can clear the ABI
- contract_address — address of the smart contract to clear ABI for
- visible — boolean indicating whether to use visible (Base58) address format instead of hex

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the ABI clearing transaction
- raw_data — raw transaction data containing:
  - contract — array with contract ABI clearing details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/clearabi \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
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

- Removing contract ABI information for privacy or security reasons.
- Cleaning up contract metadata when ABI information is no longer needed.
- Implementing obfuscation strategies for proprietary smart contracts.
- Managing contract visibility and discoverability in explorers.
- Reducing on-chain storage by removing unnecessary ABI data.
- Preparing contracts for migration or deprecation processes.

## Curl Example

Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/clearabi' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
 "contract_address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
 "visible": true
}'
Bodyapplication/jsonowner_addressstringrequiredAddress of the contract ownercontract_addressstringrequiredAddress of the smart contractvisiblebooleanWhether to use visible (Base58) address formatResponse200 - application/jsonContract ABI clearing transactionvisiblebooleanWhether addresses are in visible formattxIDstringTransaction ID for the ABI clearingraw_dataobjectShow child attributesraw_data_hexstringRaw transaction data in hex formatLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/updateenergylimit | TRONwallet/estimateenergy | TRON
