# gettransactioninfobyid

TRON API method that retrieves detailed transaction receipt and execution information by transaction ID. This method provides comprehensive data about a transaction’s execution status, resource usage, fees, and any smart contract events that occurred.

## HTTP Request

`POST /wallet/gettransactioninfobyid`

## Supported Paths

- `/wallet/gettransactioninfobyid`
- `/walletsolidity/gettransactioninfobyid`

## Parameters

- value — the transaction ID (hash) in hexadecimal format

## Response

- id — transaction ID (hash)
- blockNumber — block number where the transaction was included
- blockTimeStamp — timestamp when the block was created (milliseconds)
- contractResult — array of smart contract execution results in hex format
- contract_address — address of the deployed contract (for contract creation transactions)
- receipt — transaction receipt containing:
  - energy_usage — total energy consumed by the transaction
  - energy_fee — energy fee paid in SUN (1 TRX = 1,000,000 SUN)
  - origin_energy_usage — original energy usage before optimizations
  - energy_usage_total — total energy usage including all operations
  - net_usage — bandwidth consumed by the transaction
  - net_fee — bandwidth fee paid in SUN
  - result — execution result status (SUCCESS, REVERT, etc.)
- log — array of event logs emitted by smart contracts during execution
- result — overall transaction execution result
- resMessage — error message if transaction failed (hex-encoded)

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/gettransactioninfobyid \
  --header 'Content-Type: application/json' \
  --data '
{
  "value": "4c85b7a5c6e1d5f6e1d5c6f7e1d5c6f7e1d5c6f7e1d5c6f7e1d5c6f7e1d5c6f7"
}
'
```

### Response

```json
{
  "id": "<string>",
  "blockNumber": 123,
  "blockTimeStamp": 123,
  "contractResult": [
    "<string>"
  ],
  "contract_address": "<string>",
  "receipt": {
    "energy_usage": 123,
    "energy_fee": 123,
    "origin_energy_usage": 123,
    "energy_usage_total": 123,
    "net_usage": 123,
    "net_fee": 123,
    "result": "<string>"
  },
  "log": [
    {}
  ],
  "result": "<string>",
  "resMessage": "<string>"
}
```

## Use Case

- Getting detailed transaction execution information and resource consumption data.
- Monitoring transaction success/failure status and error messages.
- Analyzing smart contract execution results and event logs.
- Calculating actual fees paid for energy and bandwidth usage.
- Building transaction explorers and analytics tools that need execution details.
- Debugging smart contract interactions by examining logs and results.
