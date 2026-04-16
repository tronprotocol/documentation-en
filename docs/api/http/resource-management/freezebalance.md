# freezebalance

TRON API method that stakes TRX for bandwidth or energy resources (deprecated method). This method freezes TRX tokens to obtain bandwidth or energy resources, which are required for transaction execution. legacy staking closed on mainnetThe legacy wallet/freezebalance endpoint is disabled on mainnet and returns:{"Error":"class org.tron.core.exception.ContractValidateException : freeze v2 is open, old freeze is closed"} Use the current staking method instead: wallet/freezebalancev2. The examples below are kept for historical context and may only work on specific networks where legacy staking is still enabled.

## HTTP Request

`POST /wallet/freezebalance`

## Supported Paths

- `/wallet/freezebalance`

## Parameters

- owner_address — the address that owns the TRX to freeze (hex format)
- frozen_balance — the amount of TRX to freeze (in sun, where 1 TRX = 1,000,000 sun)
- frozen_duration — the duration to freeze for (minimum 3 days)
- resource — the resource type to obtain (“BANDWIDTH” or “ENERGY”)
- receiver_address — optional address to receive the resources. Omit this field to freeze for yourself. If provided, it must be different from owner_address.
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
  --url https://api.shasta.trongrid.io/wallet/freezebalance \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
  "frozen_balance": 1000000,
  "frozen_duration": 3,
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

- Staking TRX to obtain bandwidth for free transactions (legacy method).
- Freezing TRX to get energy for smart contract execution (legacy method).
- Supporting older applications that still use the original staking mechanism.
- Migrating from the deprecated staking system to the new freezebalancev2 method.

## Curl Examples

freeze for yourself (omit receiver_address):
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/freezebalance' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
 "frozen_balance": 1000000,
 "frozen_duration": 3,
 "resource": "BANDWIDTH",
 "visible": false
 }'

delegate resources to another account (receiver must differ from owner):
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/freezebalance' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
 "frozen_balance": 1000000,
 "frozen_duration": 3,
 "resource": "ENERGY",
 "receiver_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d",
 "visible": false
 }'

if you pass receiver_address equal to owner_address, the node returns:{
 "Error": "class org.tron.core.exception.ContractValidateException : receiverAddress must not be the same as ownerAddress"
}
To freeze for yourself, simply omit receiver_address. For new staking, prefer wallet/freezebalancev2.

## Recommended V2 Equivalent

Use the v2 staking endpoint (no duration or receiver in the body):
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/freezebalancev2' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
 "frozen_balance": 1000000,
 "resource": "BANDWIDTH",
 "visible": false
 }'

To unstake and withdraw in v2, use wallet/unfreezebalancev2 followed by wallet/withdrawexpireunfreeze after the waiting period.Bodyapplication/jsonowner_addressstringdefault:41608f8da72479edc7dd921e4c30bb7e7cddbe722erequiredfrozen_balanceintegerdefault:1000000requiredfrozen_durationintegerdefault:3requiredresourceenum<string>default:BANDWIDTHrequiredAvailable options: BANDWIDTH, ENERGY receiver_addressstringOptional. Address to receive the resources. Omit to freeze for yourself. Must not equal owner_address.visiblebooleandefault:falseResponse200application/jsonFreeze balance transactionvisiblebooleantxIDstringraw_dataobjectShow child attributesraw_data_hexstringLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/getaccountresource | TRONwallet/unfreezebalance | TRON
