# broadcasttransaction

TRON API method that broadcasts a signed transaction to the TRON network. This method submits a fully constructed and signed transaction for processing and inclusion in the blockchain.

## HTTP Request

`POST /wallet/broadcasttransaction`

## Supported Paths

- `/wallet/broadcasttransaction`

## Parameters

- raw_data — the raw transaction data object containing:
  - contract — array of contract objects with transaction details
  - ref_block_bytes — reference block bytes
  - ref_block_hash — reference block hash
  - expiration — transaction expiration time in milliseconds
  - timestamp — transaction creation timestamp
- raw_data_hex — hexadecimal representation of the raw transaction data
- signature — array of transaction signatures (required for signed transactions)
- visible — optional boolean for address format

## Response

- result — boolean indicating broadcast success
- code — error code if broadcast failed
- message — hexadecimal error message if broadcast failed
- txid — transaction ID if broadcast succeeded

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/broadcasttransaction \
  --header 'Content-Type: application/json' \
  --data '
{
  "raw_data": {
    "contract": [
      {
        "parameter": {
          "value": {
            "amount": 1000,
            "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
            "to_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d"
          },
          "type_url": "type.googleapis.com/protocol.TransferContract"
        },
        "type": "TransferContract"
      }
    ],
    "ref_block_bytes": "5e4b",
    "ref_block_hash": "47c9dc89341b300d",
    "expiration": 1591089627000,
    "timestamp": 1591089567635
  },
  "raw_data_hex": "0a025e4b220847c9dc89341b300d40f8fed3a2a72e5a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541608f8da72479edc7dd921e4c30bb7e7cddbe722e121541e9d79cc47518930bc322d9bf7cddd260a0260a8d18e8077093afd0a2a72e",
  "signature": [
    "deadbeefcafebabefacec0011234abcd0badf00d9999777755553333222211114321dcba0f0ff0f013579bdf2468ace0987654321a2b3c4d5e6f7a8b9c0deeff1b"
  ],
  "visible": false
}
'
```

### Response

```json
{
  "result": true,
  "code": "<string>",
  "message": "<string>",
  "txid": "<string>"
}
```

## Use Case

- Submitting signed transactions to the TRON network for processing.
- Broadcasting transfers, smart contract interactions, and other operations.
- Finalizing transactions after they have been created and signed offline.
- Implementing transaction submission in wallets and DApps.

## Curl Example

Use a fully signed transaction object. The example below is syntactically valid and will return a JSON result from the node. If the signature does not match the raw_data, the node responds with SIGERROR. Replace the signature value with a real signature produced from the exact raw_data to get result: true.
Shellcurl --request POST \
 --url 'https://api.shasta.trongrid.io/wallet/broadcasttransaction' \
 --header 'Content-Type: application/json' \
 --data '{
 "raw_data": {
 "contract": [
 {
 "parameter": {
 "value": {
 "amount": 1000,
 "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
 "to_address": "41e9d79cc47518930bc322d9bf7cddd260a0260a8d"
 },
 "type_url": "type.googleapis.com/protocol.TransferContract"
 },
 "type": "TransferContract"
 }
 ],
 "ref_block_bytes": "5e4b",
 "ref_block_hash": "47c9dc89341b300d",
 "expiration": 1591089627000,
 "timestamp": 1591089567635
 },
 "raw_data_hex": "0a025e4b220847c9dc89341b300d40f8fed3a2a72e5a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541608f8da72479edc7dd921e4c30bb7e7cddbe722e121541e9d79cc47518930bc322d9bf7cddd260a0260a8d18e8077093afd0a2a72e",
 "signature": [
 "deadbeefcafebabefacec0011234abcd0badf00d9999777755553333222211114321dcba0f0ff0f013579bdf2468ace0987654321a2b3c4d5e6f7a8b9c0deeff1b"
 ],
 "visible": false
 }'

Example response with an invalid signature (connectivity and payload are correct, signature is not):
{
 "result": false,
 "code": "SIGERROR",
 "message": "..."
}

to get a successful result: true, create the transaction with wallet/createtransaction, sign the exact raw_data with your private key, then broadcast the signed transaction here. Keep your private key secure and never paste it in client-side code.Bodyapplication/jsonraw_dataobjectrequiredraw_data_hexstringdefault:0a025e4b220847c9dc89341b300d40f8fed3a2a72e5a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541608f8da72479edc7dd921e4c30bb7e7cddbe722e121541e9d79cc47518930bc322d9bf7cddd260a0260a8d18e8077093afd0a2a72erequiredsignaturestring[]Array of hex-encoded signatures (65-byte secp256k1).visiblebooleandefault:falseResponse200 - application/jsonTransaction broadcast resultresultbooleancodestringmessagestringtxidstringLast modified on April 15, 2026Was this page helpful?YesNoSuggest editsRaise issuewallet/validateaddress | TRONwallet/broadcasthex | TRON
