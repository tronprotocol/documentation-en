# gettransactionbyid

TRON API method that retrieves transaction details by transaction ID. This method returns comprehensive information about a specific transaction, including its execution results, resource consumption, and contract details.

## HTTP Request

`POST /wallet/gettransactionbyid`

## Supported Paths

- `/wallet/gettransactionbyid`
- `/walletsolidity/gettransactionbyid`

## Parameters

- value — the transaction ID (hash) to retrieve
- visible — optional boolean to specify address format (default: false for hex format)

## Response

- ret — array of execution results containing:
  - contractRet — contract execution result (SUCCESS, REVERT, etc.)
  - fee — transaction fee paid
- signature — array of transaction signatures
- txID — transaction ID hash
- net_usage — bandwidth consumed
- raw_data_hex — hexadecimal representation of raw transaction data
- net_fee — network fee paid
- energy_usage — energy consumed (for smart contracts)
- blockNumber — block number containing the transaction
- block_timestamp — block timestamp
- contract_result — contract execution return data (for smart contracts)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/gettransactionbyid \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "d5ec749ecc2a615399d6573b3550650b4e6606d9ff0d123cd5bdc0bc6a33b0a2",
  "visible": false
}
'
```

### Response

```json
{
  "ret": [
    {
      "contractRet": "<string>",
      "fee": 123
    }
  ],
  "signature": [
    "<string>"
  ],
  "txID": "<string>",
  "net_usage": 123,
  "raw_data_hex": "<string>",
  "net_fee": 123,
  "energy_usage": 123,
  "blockNumber": 123,
  "block_timestamp": 123,
  "contract_result": [
    "<string>"
  ]
}
```

## Use Case

- Checking transaction status and execution results after broadcasting.
- Retrieving detailed transaction information for wallets and explorers.
- Analyzing transaction fees and resource consumption.
- Debugging smart contract execution and validating transaction outcomes.
