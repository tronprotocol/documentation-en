# withdrawexpireunfreeze

TRON API method that withdraws TRX tokens that have completed the unstaking waiting period. This method allows you to claim TRX that was previously unstaked using unfreezebalancev2 and has passed the mandatory 14-day waiting period, making the tokens available for transfer.

## HTTP Request

`POST /wallet/withdrawexpireunfreeze`

## Supported Paths

- `/wallet/withdrawexpireunfreeze`

## Parameters

- owner_address — the address that owns the expired unstaked TRX (hex format)
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
  --url https://api.shasta.trongrid.io/wallet/withdrawexpireunfreeze \
  --header 'Content-Type: application/json' \
  --data '
{
  "owner_address": "41608f8da72479edc7dd921e4c30bb7e7cddbe722e",
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

- Claiming TRX tokens that have completed the 14-day unstaking period.
- Making previously staked TRX available for transfers and trading.
- Completing the unstaking process started with unfreezebalancev2.
- Managing liquidity by converting staked TRX back to transferable tokens.
