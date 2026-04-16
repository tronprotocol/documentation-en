# withdrawbalance

TRON API method that allows Super Representatives (witnesses) to withdraw their accumulated block production rewards. Witnesses earn TRX rewards for producing blocks and maintaining the network, and this method enables them to claim these earnings.

## HTTP Request

`POST /wallet/withdrawbalance`

## Supported Paths

- `/wallet/withdrawbalance`

## Parameters

- owner_address — address of the Super Representative (witness) withdrawing rewards
- visible — boolean indicating whether to use visible (Base58) address format instead of hex

## Response

- visible — boolean indicating whether addresses are in visible format
- txID — unique transaction ID for the balance withdrawal transaction
- raw_data — raw transaction data containing:
  - contract — array with withdrawal contract details
  - ref_block_bytes — reference block bytes for transaction validation
  - ref_block_hash — hash of the reference block
  - expiration — transaction expiration timestamp
  - timestamp — transaction creation timestamp
- raw_data_hex — complete transaction data encoded in hexadecimal format

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/withdrawbalance \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "TGj1Ej1qRzL9feLTLhjwgxXF4Ct6GTWg2U",
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

- Super Representatives claiming their block production rewards.
- Witnesses accessing earnings from network validation activities.
- Managing witness node economics and profitability calculations.
- Implementing automated reward collection systems for witness operations.
- Building witness management tools and dashboards.
- Creating financial reporting systems for TRON network validators.
