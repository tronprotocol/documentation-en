# broadcasthex

TRON API method that broadcasts a transaction to the TRON network using hexadecimal format. This method allows you to submit pre-signed transactions directly to the blockchain without needing to use the standard JSON transaction format.

## HTTP Request

`POST /wallet/broadcasthex`

## Supported Paths

- `/wallet/broadcasthex`

## Parameters

- transaction — the complete transaction data encoded in hexadecimal format, including all signatures and necessary fields

## Response

- result — boolean indicating whether the broadcast was successful
- txid — the transaction hash if the broadcast was successful
- message — descriptive message about the broadcast status

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/broadcasthex \
  --header 'Content-Type: application/json' \
  --data '
{
  "transaction": "0a84010a025e4b220847c9dc89341b300d40f8fed3a2a72e5a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a1541608f8da72479edc7dd921e4c30bb7e7cddbe722e121541e9d79cc47518930bc322d9bf7cddd260a0260a8d18e8077093afd0a2a72e1241deadbeefcafebabefacec0011234abcd0badf00d9999777755553333222211114321dcba0f0ff0f013579bdf2468ace0987654321a2b3c4d5e6f7a8b9c0deeff1b"
}
'
```

### Response

```json
{
  "result": true,
  "txid": "<string>",
  "message": "<string>"
}
```

## Use Case

- Broadcasting pre-signed transactions in hex format to the TRON network.
- Submitting transactions that were created and signed offline for security purposes.
- Integrating with external signing tools and hardware wallets that output hex-encoded transactions.
- Building custom transaction broadcasting workflows that require hex format compatibility.
- Supporting legacy systems or tools that work with hexadecimal transaction data.

## Curl Example

- take the raw transaction bytes (raw_data_hex)
- prefix with 0a then a protobuf varint of the raw bytes length
- append each signature as 12 + 41 + 65‑byte signature hex (repeat for multisig)
