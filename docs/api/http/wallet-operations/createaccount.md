# createaccount

TRON API method that creates a new account on the TRON blockchain. This method generates an unsigned transaction to activate a new account address by sending it TRX for the first time.

## HTTP Request

`POST /wallet/createaccount`

## Supported Paths

- `/wallet/createaccount`

## Parameters

- owner_address — the address that will create and pay for the new account. Must have sufficient TRX balance to cover the account creation fee.
- account_address — the new account address to be created and activated on the blockchain.
- visible — optional boolean parameter. When set to true, addresses are in base58 format. Default is false.

## Response

- visible — indicates the address format used in the response
- txID — the transaction hash
- raw_data — raw transaction data including:
  - contract — array containing the account creation contract
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/createaccount \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
  "account_address": "TFgY1uN8buRxAtV2r6Zy5sG3ACko6pJT1y",
  "visible": true
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

- Activating new TRON addresses on the blockchain.
- Creating accounts for new users in wallet applications.
- Setting up multi-signature or contract accounts.
- Onboarding new users to the TRON ecosystem.

## Curl Example

The node validates that the owner_address can cover the protocol’s account creation fee. If the owner is not funded, you will get a validation error instead of an unsigned transaction.
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/createaccount' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
 "account_address": "TFgY1uN8buRxAtV2r6Zy5sG3ACko6pJT1y",
 "visible": true
 }'

Example error when the owner address lacks enough TRX to cover the account creation fee:
{
 "Error": "class org.tron.core.exception.ContractValidateException : Validate CreateAccountActuator error, insufficient fee."
}

When the owner is funded, the response is an unsigned transaction that you must sign and then broadcast using wallet/broadcasttransaction or wallet/broadcasthex.
you can also create an account implicitly by sending TRX to a new address; on first receipt the account is created and the sender pays the creation fee. Addresses can be provided in base58 with visible: true or in hex with visible: false.

## End To End Steps

1check the payer balanceUse wallet/getaccount to confirm the owner_address has enough TRX to cover the account creation fee.Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/getaccount' \
 --header 'Content-Type: application/json' \
 --data '{
 "address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g",
 "visible": true
 }'
2option: use nile testnetFor testing, you can use a Nile endpoint and get test TRX from the faucet. Replace with your own Nile endpoint from the console.Shellcurl --request POST \
 --url 'https://tron-nile.core.chainstack.com/11112222333444555666677778888/wallet/createaccount' \
 --header 'Content-Type: application/json' \
 --data '{
 "owner_address": "TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
 "account_address": "TYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",
 "visible": true
 }'
Fund owner_address with test TRX from the Nile faucet, then run the call again.3sign and broadcastOn success, you receive an unsigned transaction. Sign the raw_data with your private key and broadcast via wallet/broadcasttransaction or provide the built hex to wallet/broadcasthex.
getting insufficient fee is expected when the payer has no TRX. Fund the owner_address first or create the account implicitly by sending TRX to the new address.Bodyapplication/jsonowner_addressstringdefault:TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2grequiredThe existing account that pays the account creation fee. Must have sufficient TRX.account_addressstringdefault:TFgY1uN8buRxAtV2r6Zy5sG3ACko6pJT1yrequiredThe new account address to be activated.visiblebooleandefault:trueWhen true, addresses are base58; when false, hex.Response200application/jsonUnsigned account creation transactionvisiblebooleantxIDstringraw_dataobjectraw_data_hexstringLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/createtransaction | TRONwallet/updateaccount | TRON
