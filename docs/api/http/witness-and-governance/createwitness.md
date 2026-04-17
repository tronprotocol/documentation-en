# createwitness

TRON API method that creates a transaction to register an account as a witness (validator) on the TRON network. Witnesses participate in block production and network governance through the Delegated Proof of Stake (DPoS) consensus mechanism.

## HTTP Request

`POST /wallet/createwitness`

## Supported Paths

- `/wallet/createwitness`

## Parameters

- owner_address — address of the account that will become a witness. Use base58 with visible: true, or hex with visible: false.
- url — witness website URL providing information about the witness (must be a valid URL)
- visible — optional boolean. When true, addresses are base58; when false, hex. Default is true.

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the witness creation transaction
- raw_data — raw transaction data containing:
  - contract — array with witness creation contract details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/createwitness \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "url": "https://mywitness.example.com",
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

- Registering an account as a witness to participate in TRON network governance.
- Setting up block production capabilities for earning rewards from the network.
- Establishing a public presence for community voting and trust building.
- Preparing to compete for one of the 27 Super Representative positions.
- Contributing to network security and decentralization through validation services.
- Building reputation and credibility within the TRON ecosystem.

## Curl Example

Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/createwitness' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
 "url": "https://mywitness.example.com",
 "visible": true
}'

seeing INVALID hex String? Provide a base58 address with visible: true, or a 21‑byte hex address (starts with 41…) with visible: false.Bodyapplication/jsonowner_addressstringrequiredAddress that will become a witness. Use base58 with visible: true, or hex with visible: false.urlstringrequiredWitness website URL (must be a valid URL)visiblebooleandefault:trueWhen true, addresses are base58; when false, hex.Response200 - application/jsonWitness creation transactionvisiblebooleanWhether addresses are in visible formattxIDstringTransaction ID for witness creationraw_dataobjectShow child attributesraw_data_hexstringRaw transaction data in hex formatLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/listwitnesses | TRONwallet/updatewitness | TRON
