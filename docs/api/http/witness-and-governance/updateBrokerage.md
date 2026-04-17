# updateBrokerage

TRON API method that creates a transaction to update the brokerage rate for witness rewards. Only witnesses can call this method to adjust how they share block production rewards with their voters.

## HTTP Request

`POST /wallet/updateBrokerage`

## Supported Paths

- `/wallet/updateBrokerage`

## Parameters

- owner_address — address of the witness account updating the brokerage. Use base58 with visible: true, or hex with visible: false.
- brokerage — new brokerage percentage (0–100); lower values share more rewards with voters.
- visible — optional boolean. When true, addresses are base58; when false, hex. Default is true.

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the brokerage update transaction
- raw_data — raw transaction data containing:
  - contract — array with brokerage update contract details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/updateBrokerage \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC",
  "brokerage": 15,
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

- Adjusting witness reward sharing policies to attract more voters.
- Setting competitive brokerage rates compared to other witnesses.
- Implementing dynamic reward sharing strategies based on market conditions.
- Managing witness economics to balance profitability and voter incentives.

## Curl Example

- No permission — the owner_address is not a registered witness.
- Account […] does not exist — ensure the address is activated and the format matches visible.
- Rate bounds — brokerage must be between 0 and 100.
- Not existed witness — register the witness first via wallet/createwitness and wait until it is recognized on-chain.
