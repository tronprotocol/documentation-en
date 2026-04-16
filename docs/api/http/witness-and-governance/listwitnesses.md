# listwitnesses

TRON API method that retrieves a complete list of all witnesses (validators) on the TRON network. Witnesses are responsible for block production and network governance in TRON’s Delegated Proof of Stake (DPoS) consensus mechanism.

## HTTP Request

`POST /wallet/listwitnesses`

## Supported Paths

- `/wallet/listwitnesses`
- `/walletsolidity/listwitnesses`

## Parameters

This method accepts no parameters.

## Response

- witnesses — array containing information about all witnesses:
  - address — witness address in hexadecimal format
  - voteCount — total number of votes received from TRX holders
  - pubKey — public key used for block signing and validation
  - url — witness website or information URL
  - totalProduced — total number of blocks successfully produced
  - totalMissed — total number of blocks missed during assigned slots
  - latestBlockNum — block number of the most recent block produced
  - latestSlotNum — most recent time slot assigned for block production
  - isJobs — boolean indicating whether the witness is currently active in block production

## Example

### Request

```shell
curl --request POST \
  --url https://api.shasta.trongrid.io/wallet/listwitnesses \
  --header 'Content-Type: application/json' \
  --data '{}'
```

### Response

```json
{
  "witnesses": [
    {
      "address": "<string>",
      "voteCount": 123,
      "pubKey": "<string>",
      "url": "<string>",
      "totalProduced": 123,
      "totalMissed": 123,
      "latestBlockNum": 123,
      "latestSlotNum": 123,
      "isJobs": true
    }
  ]
}
```

## Use Case

- Displaying all available witnesses for voting and governance participation.
- Building voting interfaces and governance dashboards.
- Analyzing witness performance metrics including blocks produced and missed.
- Monitoring network health by tracking active witnesses and their statistics.
- Creating witness ranking and comparison tools based on votes and performance.
- Implementing governance features that require witness selection and information.
