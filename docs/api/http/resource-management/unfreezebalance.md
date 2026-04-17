# unfreezebalance

TRON API method that unstakes TRX previously frozen for bandwidth or energy resources (deprecated method). This method releases TRX tokens that were previously frozen, making them available for transfer after the lock period expires. This is the legacy unstaking mechanism; for the current staking model, use unfreezebalancev2. legacy unstake works only for legacy freezesOn mainnet, new legacy freezes are disabled. You can only use wallet/unfreezebalance if your account still has legacy‑frozen balance. For v2 staking, use wallet/unfreezebalancev2.

## HTTP Request

`POST /wallet/unfreezebalance`

## Supported Paths

- `/wallet/unfreezebalance`

## Parameters

- owner_address — the address that owns the frozen TRX to unfreeze (hex format)
- resource — the resource type to release (“BANDWIDTH” or “ENERGY”)
- receiver_address — optional address that was receiving the resources. Omit to unfreeze to yourself. If provided, it must be different from owner_address.
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- visible — boolean indicating address format used
- txID — transaction ID hash
- raw_data — raw transaction data object
- raw_data_hex — hexadecimal representation of raw transaction data

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/unfreezebalance \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "resource": "BANDWIDTH",
  "visible": false
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

- Unstaking TRX to make tokens transferable again (legacy method).
- Releasing bandwidth or energy resources that are no longer needed (legacy method).
- Supporting older applications that still use the original unstaking mechanism.
- Migrating from the deprecated unstaking system to the new unfreezebalancev2 method.

## Curl Examples

unfreeze to yourself (omit receiver_address):
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/unfreezebalance' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
 "resource": "BANDWIDTH",
 "visible": false
 }'

unfreeze delegated resources to another account (receiver must differ from owner):
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/unfreezebalance' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
 "resource": "ENERGY",
 "receiver_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d",
 "visible": false
 }'

if you pass receiver_address equal to owner_address, the node returns:{
 "Error": "class org.tron.core.exception.ContractValidateException : receiverAddress must not be the same as ownerAddress"
}
For the current staking model, use wallet/unfreezebalancev2. After the v2 waiting period ends, withdraw with wallet/withdrawexpireunfreeze.Bodyapplication/jsonowner_addressstringdefault:41608f8da72479edc7dd921e4c30bb7e7cddbe722erequiredresourceenum<string>default:BANDWIDTHrequiredAvailable options: BANDWIDTH, ENERGY receiver_addressstringOptional. Address that was receiving the resources. Omit to unfreeze to yourself. Must not equal owner_address.visiblebooleandefault:falseResponse200application/jsonUnfreeze balance transactionvisiblebooleantxIDstringraw_dataobjectShow child attributesraw_data_hexstringLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/freezebalance | TRONwallet/freezebalancev2 | TRON
