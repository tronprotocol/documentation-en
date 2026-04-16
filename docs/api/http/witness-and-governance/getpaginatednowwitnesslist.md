# getpaginatednowwitnesslist

TRON API method that retrieves the real-time vote counts of all Super Representatives (SRs) in the current epoch, sorted in descending order, and returns a paginated list within the specified range.

## HTTP Request

`GET /wallet/getpaginatednowwitnesslist`

## Supported Paths

- `/wallet/getpaginatednowwitnesslist`
- `/walletsolidity/getpaginatednowwitnesslist`

## Parameters

- offset — the starting position of the paginated query, must be >= 0. For example, offset=5 with limit=10 returns SRs ranked 6th to 15th by vote count
- limit — the number of results to return, must be > 0 and <= 1000
- visible — optional boolean. When true, addresses are in base58 format; when false, hex format. Defaults to false

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
curl --request GET \
  --url 'https://api.shasta.trongrid.io/wallet/getpaginatednowwitnesslist?offset=0&limit=10'
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

- Displaying paginated Super Representative rankings sorted by real-time vote counts.
- Building voting dashboards that show current epoch SR standings with pagination support.
- Analyzing SR performance metrics within a specific rank range.
- Monitoring real-time vote distribution changes during the current epoch.
- Creating leaderboard-style interfaces for SR election tracking.
